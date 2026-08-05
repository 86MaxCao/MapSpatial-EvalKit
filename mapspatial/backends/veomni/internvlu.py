"""InternVLU backend — wraps VeOmni InternVLUPipeline.

Implements all three backend methods:
  - understand(): text understanding via pipeline.__call__(generation_mode="text")
  - draw(): image generation via pipeline.__call__(generation_mode="image")
  - interleave(): native CoT loop via pipeline.__call__(generation_mode="text_image")

InternVLU uses a unified pipeline with three generation modes:
  - "text": text-only understanding output
  - "image": image-only generation output
  - "text_image": native CoT loop — generates text first, then conditions image
    generation on the expanded text, producing interleaved text+image output

Strategy mapping:
  direct              → understand()
  native_interleave   → interleave() (generation_mode="text_image")
  external_draw       → understand() + draw()
"""

from __future__ import annotations

import os
import time
import torch
from pathlib import Path
from typing import ClassVar

from ...types import Capabilities, Message, Prediction, TraceStep
from ...config import BackendConfig
from ...compat import apply as apply_compat
from ...messages import to_interleave_list, to_placeholder_prompt, strip_placeholders
from ...media import load_image
from ..base import Backend


class InternVLUBackend(Backend):
    """InternVLU backend with native interleaved understanding + generation."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False,              # serial inference only
        draw=True,                # pipeline supports image generation
        native_interleave=True,   # pipeline has "text_image" CoT loop
        max_images=24,
        video=False,
    )
    COMPAT: ClassVar[tuple[str, ...]] = ()

    def __init__(self, cfg: BackendConfig) -> None:
        for var in ("WORLD_SIZE", "RANK", "LOCAL_RANK"):
            os.environ.pop(var, None)

        apply_compat(*self.COMPAT)

        self._cfg = cfg
        model_path = cfg.model_path
        device = cfg.load.get("device", "cuda")
        dtype = cfg.load.get("dtype", "bfloat16")

        # InternVL-U uses diffusers pipeline format (model_index.json at root)
        # InternVLUConfig.from_pretrained detects model_index.json and loads
        # all sub-configs (vlm_config, generation_decoder_config, vae_config) properly.
        import torch
        from ...vendor.internvlu.modeling_internvlu import InternVLUModel

        vlm_path = os.path.join(model_path, "vlm")
        if not os.path.exists(vlm_path):
            vlm_path = model_path  # fallback for single-dir format

        # Load from root path (has model_index.json for pipeline-format checkpoints)
        from ...loader import load_model, load_processor
        (self._pipeline, _) = load_model(
            model_path, InternVLUModel,
            device=device, dtype=dtype,
        )

        # Try loading processor from the processor/ subdirectory
        proc_path = os.path.join(model_path, "processor")
        if not os.path.exists(proc_path):
            proc_path = vlm_path
        try:
            self._processor = load_processor(proc_path)
        except Exception:
            self._processor = None

        # Load tokenizer from processor/ subdirectory (has tokenizer files)
        from ...loader import load_tokenizer
        tok_path = os.path.join(model_path, "processor")
        if not os.path.exists(os.path.join(tok_path, "tokenizer_config.json")):
            tok_path = vlm_path  # fallback
        self._tokenizer = load_tokenizer(tok_path)

        # Add special tokens
        from ...vendor.internvlu.vlm.constants import SPECIAL_TOKEN_LIST
        self._tokenizer.add_tokens(SPECIAL_TOKEN_LIST)
        if hasattr(self._pipeline, "init_special_tokens"):
            self._pipeline.init_special_tokens(self._tokenizer)

        # Load VAE from vae/ subdirectory (diffusers AutoencoderKLQwenImage)
        from diffusers import AutoencoderKLQwenImage, DPMSolverMultistepScheduler
        vae_path = os.path.join(model_path, "vae")
        if os.path.exists(vae_path):
            try:
                vae = AutoencoderKLQwenImage.from_pretrained(vae_path, torch_dtype=getattr(torch, dtype))
                vae = vae.to(device)
                self._pipeline.set_vae(vae)
                print(f"  Loaded VAE")
            except Exception as e:
                print(f"  WARNING: Failed to load VAE: {e}")

        # Load scheduler from scheduler/ subdirectory
        sched_path = os.path.join(model_path, "scheduler")
        if os.path.exists(sched_path):
            try:
                self._scheduler = DPMSolverMultistepScheduler.from_pretrained(sched_path)
            except Exception:
                self._scheduler = DPMSolverMultistepScheduler()
        else:
            self._scheduler = DPMSolverMultistepScheduler()

        # Build a lightweight pipeline wrapper for draw()/interleave() support.
        # We can't use InternVLUPipeline directly because it extends DiffusionPipeline
        # which has strict type checking that rejects InternVLUProcessor's video_processor.
        try:
            from ...vendor.internvlu.processing_internvlu import InternVLUProcessor
            from ...vendor.internvlu.diffusion import InternVLUDiffusionPipeline
            internvlu_processor = InternVLUProcessor.from_pretrained(proc_path)
            self._internvlu_processor = internvlu_processor
            self._image_pipeline = InternVLUDiffusionPipeline(
                vae=self._pipeline.vae,
                generation_decoder=self._pipeline.generation_decoder,
                scheduler=self._scheduler,
            )
            # Stash references for the pipeline methods that need them
            self._vlm = self._pipeline.vlm
            self._generation_decoder = self._pipeline.generation_decoder
            self._vae = self._pipeline.vae
            # Init special tokens on VLM
            self._pipeline.init_special_tokens(self._tokenizer)
            self._full_pipeline = True  # flag: components are ready
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"  WARNING: Failed to build pipeline components: {e}")
            self._full_pipeline = None

        self._device = device

        # Generation params from config
        gen = cfg.generate
        self._temperature = gen.get("temperature", 0.0)
        self._max_new_tokens = gen.get("max_new_tokens", 512)

        # Draw params from backend_args
        ba = cfg.backend_args
        self._cfg_scale_draw = ba.get("all_cfg_scale", 4.5)
        self._num_steps_draw = ba.get("num_inference_steps", 20)

        # Interleave params
        self._cfg_scale_interleave = ba.get("cfg_scale_interleave", 3.5)
        self._max_new_tokens_interleave = ba.get("max_new_tokens_interleave", 200)

        # System prompt
        self._system_prompt = cfg.system_prompt or None

    @property
    def model_name(self) -> str:
        return self._cfg.name

    # ------------------------------------------------------------------
    # understand()
    # ------------------------------------------------------------------

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Text-only understanding via model.generate_text().

        Matches VeOmni infer_internvlu_understand calling convention.
        """
        results = []
        for msg in messages:
            try:
                text = self._understand_one(msg, gen_kw)
                results.append(Prediction(text=text))
            except Exception as e:
                results.append(Prediction(error=str(e)))
        return results

    def _understand_one(self, msg: Message, gen_kw: dict) -> str:
        """Single-sample understanding matching VeOmni infer_internvlu_understand."""
        import numpy as np
        from PIL import Image
        from transformers import GenerationConfig

        device = self._device
        model = self._pipeline
        tokenizer = self._tokenizer

        # Extract text and images
        input_list = to_interleave_list(msg)
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = "\n".join(text_parts)
        prompt = strip_placeholders(prompt)

        max_new_tokens = gen_kw.get("max_new_tokens", self._max_new_tokens)

        # Build chat template (VeOmni convention)
        if images:
            text_str = (
                f"<|im_start|>system\nYou are a helpful assistant.<|im_end|>"
                f"\n<|im_start|>user\n<image>\n{prompt}<|im_end|>"
                f"\n<|im_start|>assistant\n"
            )
            # Replace <image> with <img><IMG_CONTEXT>\xd7256</img>
            num_img_tokens = 256
            img_context_str = (
                "<img>" + "<IMG_CONTEXT>" * num_img_tokens + "</img>"
            )
            text_str = text_str.replace("<image>", img_context_str)
        else:
            text_str = (
                f"<|im_start|>system\nYou are a helpful assistant.<|im_end|>"
                f"\n<|im_start|>user\n{prompt}<|im_end|>"
                f"\n<|im_start|>assistant\n"
            )

        input_ids = tokenizer.encode(text_str, return_tensors="pt").to(device)
        attention_mask = torch.ones_like(input_ids)

        pixel_values = None
        if images:
            # Preprocess: pil_img2rgb -> resize 448x448 LANCZOS
            #  -> /255.0 -> ImageNet normalize -> bf16 -> (1, 3, 448, 448)
            img = images[0]
            if img.mode != "RGB":
                img = img.convert("RGB")
            img = img.resize((448, 448), Image.LANCZOS)
            pixel_values = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
            # ImageNet normalize
            mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
            std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
            pixel_values = (pixel_values - mean) / std
            pixel_values = pixel_values.unsqueeze(0).to(device)
            pixel_values = pixel_values.to(
                dtype=next(model.parameters()).dtype,
            )

        # Generate text (VeOmni convention)
        with torch.no_grad():
            eos_id = tokenizer.convert_tokens_to_ids("<|im_end|>")
            gen_config = GenerationConfig(
                max_new_tokens=max_new_tokens,
                do_sample=False,
                eos_token_id=eos_id,
                pad_token_id=eos_id,
                repetition_penalty=1.1,
            )
            output_ids = model.generate_text(
                input_ids=input_ids,
                attention_mask=attention_mask,
                pixel_values=pixel_values,
                generation_config=gen_config,
            )

        # Unwrap if HF GenerateOutput
        if hasattr(output_ids, "sequences"):
            output_ids = output_ids.sequences

        generated_ids = output_ids[0, input_ids.shape[1]:]
        response = tokenizer.decode(generated_ids, skip_special_tokens=True)
        return response.strip()

    # ------------------------------------------------------------------
    # draw()
    # ------------------------------------------------------------------

    def draw(self, context: Message, instruction: str, **kw) -> "Image.Image":
        """Generate an image via InternVL-U image generation pipeline.

        Flow: processor → VLM hidden states → diffusion decoder → VAE → PIL image
        """
        import numpy as np
        import torch
        from PIL import Image

        if not self._full_pipeline:
            raise RuntimeError("InternVL-U pipeline components not loaded — cannot generate images")

        # Build the text prompt
        input_list = to_interleave_list(context)
        text_parts = [item for item in input_list if isinstance(item, str)]
        context_images = [item for item in input_list if not isinstance(item, str)]
        context_text = "\n".join(text_parts)
        prompt = f"{context_text}\n{instruction}" if context_text else instruction

        cfg_scale = kw.get("all_cfg_scale", self._cfg_scale_draw)
        part_cfg_scale = kw.get("part_cfg_scale", 2.0)
        num_steps = kw.get("num_inference_steps", self._num_steps_draw)

        # Get generation image dimensions from decoder config
        gen_h = getattr(self._generation_decoder.config, "gen_image_height", 768)
        gen_w = getattr(self._generation_decoder.config, "gen_image_width", 768)

        # Build inputs via processor
        with torch.no_grad():
            inputs = self._internvlu_processor(
                prompt=prompt,
                image=context_images[0] if context_images else None,
                generation_mode="image",
                padding=True,
                return_tensors="pt",
                height=gen_h,
                width=gen_w,
            )
            for k, v in inputs.items():
                if isinstance(v, torch.Tensor):
                    inputs[k] = v.to(self._device)

            # Generate VLM hidden states
            vlm_outputs = self._vlm.generate_hidden_states(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                pixel_values=inputs.get("pixel_values"),
            )
            vlm_hidden_states = vlm_outputs.hidden_states

            # Prepare diffusion inputs (replicating pipeline._prepare_diffusion_inputs)
            from ...vendor.internvlu.pipeline_internvlu import InternVLUPipeline
            # Create a temporary pipeline-like object to access methods
            class _PipeProxy:
                pass
            proxy = _PipeProxy()
            proxy.vlm = self._vlm
            proxy.generation_decoder = self._generation_decoder
            proxy.vae = self._vae
            proxy.tokenizer = self._tokenizer
            proxy.image_pipeline = self._image_pipeline
            # Bind methods from InternVLUPipeline
            proxy._prepare_diffusion_inputs = InternVLUPipeline._prepare_diffusion_inputs.__get__(proxy)
            proxy._prepare_hidden_state_mask = InternVLUPipeline._prepare_hidden_state_mask.__get__(proxy)
            proxy._prepare_image_hidden_state_mask = InternVLUPipeline._prepare_image_hidden_state_mask.__get__(proxy)

            diffusion_inputs = proxy._prepare_diffusion_inputs(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                pixel_values=inputs.get("pixel_values"),
                pixel_values_gen=inputs.get("pixel_values_gen"),
                image_grid_thw_gen=inputs.get("image_grid_thw_gen"),
                generation_flags=inputs["generation_flags"],
                vlm_hidden_states=vlm_hidden_states,
            )

            # Run image generation pipeline
            output = self._image_pipeline(
                **diffusion_inputs,
                all_cfg_scale=cfg_scale,
                part_cfg_scale=part_cfg_scale,
                num_inference_steps=num_steps,
                num_images_per_prompt=1,
                use_resolution_binning=False,
                height=gen_h,
                width=gen_w,
            ).images

            # Post-process: [-1,1] → [0,255] PIL
            output = ((127.5 * output + 128.0) / 255).clamp(0, 1)
            img = Image.fromarray(
                (output[0].cpu().float().numpy().transpose(1, 2, 0) * 255).astype(np.uint8)
            )
            # Resize to original gen dimensions
            img = img.resize((gen_w, gen_h), Image.Resampling.LANCZOS)
            return img

    # ------------------------------------------------------------------
    # interleave()
    # ------------------------------------------------------------------

    def interleave(
        self,
        message: Message,
        *,
        max_rounds: int = 3,
        marker: str = "<image_start>",
        **kw,
    ) -> Prediction:
        """Native interleaved reasoning loop via pipeline "text_image" mode.

        InternVLU's "text_image" generation mode implements a native CoT loop:
        1. Generates text first (reasoning / description)
        2. Expands the text with image-conditioning tokens
        3. Generates an image conditioned on the expanded text
        This produces interleaved text+image output in a single pipeline call.
        """
        import torch
        from PIL import Image

        # Convert Message to interleave input list
        input_list = to_interleave_list(message)

        # Build the full prompt
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = "\n".join(text_parts)
        if self._system_prompt:
            prompt = f"{self._system_prompt}\n{prompt}"

        max_new_tokens = kw.get(
            "max_new_tokens", self._max_new_tokens_interleave,
        )
        cfg_scale = kw.get("all_cfg_scale", self._cfg_scale_interleave)

        trace: list[TraceStep] = []
        t0 = time.time()

        with torch.no_grad():
            # --- Build inputs via processor ---
            if images:
                inputs = self._processor(
                    text=prompt, images=images, return_tensors="pt",
                )
            else:
                inputs = self._processor(
                    text=prompt, return_tensors="pt",
                )
            inputs = {
                k: v.to(self._device) if hasattr(v, "to") else v
                for k, v in inputs.items()
            }

            # --- Run pipeline in text_image CoT mode ---
            # This generates text first, then produces an image conditioned
            # on the expanded text. The output contains both text and image.
            result = self._pipeline(
                prompt=prompt,
                image=images[0] if images else None,
                generation_mode="text_image",
                max_new_tokens=max_new_tokens,
                all_cfg_scale=cfg_scale,
                input_ids=inputs.get("input_ids"),
                attention_mask=inputs.get("attention_mask"),
                pixel_values=inputs.get("pixel_values"),
            )

        elapsed = time.time() - t0

        # --- Parse output ---
        # The pipeline may return a dict with "text" and "image" keys,
        # or a list of mixed text/image items.
        text_parts_out = []
        generated_images = []
        round_num = 0

        if isinstance(result, dict):
            text = result.get("text", "")
            img = result.get("image")
            if text:
                text_parts_out.append(text)
                trace.append(TraceStep(
                    round=round_num, kind="text",
                    text=text,
                    triggered_by=None,
                    elapsed_s=elapsed / 2,
                ))
                if marker in text:
                    round_num += 1
            if img is not None:
                if isinstance(img, Image.Image):
                    generated_images.append(img)
                    trace.append(TraceStep(
                        round=round_num, kind="image",
                        triggered_by="model_marker",
                        elapsed_s=elapsed / 2,
                    ))
                elif isinstance(img, (list, tuple)):
                    for im in img:
                        if isinstance(im, Image.Image):
                            generated_images.append(im)
                            trace.append(TraceStep(
                                round=round_num, kind="image",
                                triggered_by="model_marker",
                                elapsed_s=elapsed / 2,
                            ))
        elif isinstance(result, (list, tuple)):
            for item in result:
                if isinstance(item, str):
                    text_parts_out.append(item)
                    trace.append(TraceStep(
                        round=round_num, kind="text",
                        text=item,
                        triggered_by=None,
                        elapsed_s=elapsed / max(len(result), 1),
                    ))
                    if marker in item:
                        round_num += 1
                elif isinstance(item, Image.Image):
                    generated_images.append(item)
                    trace.append(TraceStep(
                        round=round_num, kind="image",
                        triggered_by="model_marker",
                        elapsed_s=elapsed / max(len(result), 1),
                    ))
        elif isinstance(result, str):
            text_parts_out.append(result)
            trace.append(TraceStep(
                round=0, kind="text",
                text=result,
                triggered_by=None,
                elapsed_s=elapsed,
            ))
        elif isinstance(result, Image.Image):
            generated_images.append(result)
            trace.append(TraceStep(
                round=0, kind="image",
                triggered_by="model_marker",
                elapsed_s=elapsed,
            ))

        final_text = text_parts_out[-1] if text_parts_out else ""

        return Prediction(
            text=final_text,
            generated_images=generated_images,
            trace=trace,
            meta={
                "rounds": round_num,
                "draw_triggered": len(generated_images) > 0,
            },
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _extract_text(self, result) -> str:
        """Extract text from a pipeline result (str, dict, or list)."""
        if isinstance(result, str):
            return result
        if isinstance(result, dict):
            return result.get("text", "")
        if isinstance(result, (list, tuple)):
            parts = []
            for item in result:
                if isinstance(item, str):
                    parts.append(item)
            return "\n".join(parts)
        return str(result)

    def _extract_image(self, result):
        """Extract a PIL Image from a pipeline result. Returns None if not found."""
        from PIL import Image

        if isinstance(result, Image.Image):
            return result
        if isinstance(result, dict):
            img = result.get("image") or result.get("generated_image")
            if isinstance(img, Image.Image):
                return img
            if isinstance(img, (list, tuple)):
                for im in img:
                    if isinstance(im, Image.Image):
                        return im
        if isinstance(result, (list, tuple)):
            for item in result:
                if isinstance(item, Image.Image):
                    return item
        # Tensor output
        if hasattr(result, "shape") and len(result.shape) == 4:
            import numpy as np
            pixels = (result[0].clamp(-1, 1) + 1) / 2
            pixels = (pixels.cpu().permute(1, 2, 0).numpy() * 255).astype("uint8")
            return Image.fromarray(pixels)
        return None
