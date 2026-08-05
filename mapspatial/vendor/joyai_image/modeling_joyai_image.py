# --------------------------------------------------------
# VeOmni Integration of JoyAI-Image
# Original code: JoyAI-Image (Qwen3-VL + MMDiT + Wan2.1 VAE)
# --------------------------------------------------------

import os
from types import SimpleNamespace
from typing import List, Optional, Tuple, Union

import torch
import torch.nn as nn
from transformers.modeling_utils import PreTrainedModel
from transformers.utils import logging

from .configuration_joyai_image import JoyAIImageConfig

logger = logging.get_logger(__name__)


class JoyAIImageModel(PreTrainedModel):
    """VeOmni wrapper for JoyAI-Image.

    JoyAI-Image is a two-component architecture:
    - Understanding: Qwen3-VL (HuggingFace format, loaded from JoyAI-Image-Und/)
    - Generation: MMDiT (PyTorch .pth, loaded from transformer/transformer.pth)
    - VAE: Wan2.1 VAE (PyTorch .pth, loaded from vae/Wan2.1_VAE.pth)

    The understanding inference delegates to the Qwen3-VL model.
    The generation inference uses the official pipeline.
    """

    config_class = JoyAIImageConfig
    main_input_name = "input_ids"
    base_model_prefix = ""
    _supports_flash_attn_2 = True
    supports_gradient_checkpointing = True

    def __init__(self, config: JoyAIImageConfig, **kwargs):
        super().__init__(config)
        # Components are loaded lazily in load_weights_from_checkpoint
        self.text_encoder = None  # Qwen3-VL model
        self.dit = None           # MMDiT Transformer3DModel
        self.vae = None           # Wan2.1 VAE
        self.pipeline = None     # Generation pipeline
        self.tokenizer = None

    def load_weights_from_checkpoint(self, checkpoint_path: str):
        """Load all three components from the JoyAI-Image checkpoint.

        checkpoint_path has:
          JoyAI-Image-Und/     (HuggingFace Qwen3-VL)
          transformer/transformer.pth
          vae/Wan2.1_VAE.pth
          config.json
          infer_config.py      (InferConfig with DiT/VAE/scheduler arch configs)
        """
        import json
        import sys

        # Add joyai_image dir to sys.path so 'modules' and 'infer_runtime'
        # are importable as top-level packages (required by build_from_config
        # which uses absolute import paths like "modules.models.Transformer3DModel").
        # __file__ is .../joyai_image/modeling_joyai_image.py, so one dirname
        # gives .../joyai_image/ which contains both modules/ and infer_runtime/.
        joyai_image_dir = os.path.dirname(os.path.abspath(__file__))
        if joyai_image_dir not in sys.path:
            sys.path.insert(0, joyai_image_dir)

        # Read config.json for component paths
        config_path = os.path.join(checkpoint_path, "config.json")
        with open(config_path, "r") as f:
            ckpt_config = json.load(f)

        # Resolve text encoder path
        te_path = ckpt_config.get("text_encoder_ckpt", "JoyAI-Image-Und")
        if not os.path.isabs(te_path):
            te_path = os.path.join(checkpoint_path, "JoyAI-Image-Und")

        # Resolve DiT path
        dit_path = ckpt_config.get("transformer_ckpt", "transformer/transformer.pth")
        if not os.path.isabs(dit_path):
            dit_path = os.path.join(checkpoint_path, "transformer", "transformer.pth")

        # Resolve VAE path
        vae_path = ckpt_config.get("vae_ckpt", "vae/Wan2.1_VAE.pth")
        if not os.path.isabs(vae_path):
            # Strip leading checkpoint dir name if present (e.g. "JoyAI-Image-Edit/vae/...")
            vae_path = vae_path.split("/")[-1] if "/" in vae_path else vae_path
            vae_path = os.path.join(checkpoint_path, "vae", "Wan2.1_VAE.pth")

        device = next(self.parameters()).device if list(self.parameters()) else torch.device("cuda")

        # Load InferConfig from checkpoint's infer_config.py.
        # This file contains the proper DiT/VAE/scheduler/text_encoder arch configs
        # with resolved checkpoint paths (via _resolve_root()).
        from infer_runtime.infer_config import load_infer_config_class_from_pyfile

        infer_config_path = os.path.join(checkpoint_path, "infer_config.py")
        config_class = load_infer_config_class_from_pyfile(infer_config_path)
        cfg = config_class()
        cfg.dit_ckpt = dit_path
        cfg.training_mode = False
        # Use fp32 for VAE to avoid precision issues during decode
        cfg.vae_precision = "fp32"
        self._infer_cfg = cfg  # store for pipeline access

        # 1. Load Qwen3-VL text encoder (for understanding)
        logger.info(f"Loading Qwen3-VL from {te_path}...")
        from transformers import AutoTokenizer, Qwen3VLForConditionalGeneration

        self.text_encoder = Qwen3VLForConditionalGeneration.from_pretrained(
            te_path, torch_dtype=torch.bfloat16
        )
        self.text_encoder = self.text_encoder.to(device)
        self.text_encoder.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(te_path)
        logger.info(f"Qwen3-VL loaded ({sum(p.numel() for p in self.text_encoder.parameters()) / 1e9:.2f}B params)")

        # 2. Load MMDiT transformer using load_dit with proper InferConfig
        logger.info(f"Loading MMDiT from {dit_path}...")
        try:
            from modules.models import load_dit

            self.dit = load_dit(cfg, device=device)
            self.dit.requires_grad_(False)
            self.dit.eval()
            logger.info(f"MMDiT loaded ({sum(p.numel() for p in self.dit.parameters()) / 1e9:.2f}B params)")
        except Exception as e:
            logger.warning(f"Failed to load MMDiT: {e}")
            import traceback
            logger.warning(traceback.format_exc())

        # 3. Load VAE using build_from_config with cfg.vae_arch_config
        logger.info(f"Loading VAE...")
        try:
            from modules.models.mmdit.vae import WanxVAE
            from modules.utils.constants import PRECISION_TO_TYPE

            vae_dtype = PRECISION_TO_TYPE[cfg.vae_precision]
            # WanxVAE takes 'pretrained' arg (path to .pth file), not 'vae_pth'
            self.vae = WanxVAE(
                pretrained=vae_path,
                torch_dtype=vae_dtype,
                device=device,
            )
            logger.info(f"VAE loaded with weights from {vae_path}")
        except Exception as e:
            logger.warning(f"Failed to load VAE: {e}")
            import traceback
            logger.warning(traceback.format_exc())

        # 4. Build scheduler and full Pipeline for generation
        logger.info("Building generation pipeline...")
        try:
            from modules.models.pipeline import Pipeline
            from modules.utils.utils import build_from_config

            scheduler = build_from_config(cfg.scheduler_arch_config)
            self.pipeline = Pipeline(
                vae=self.vae,
                tokenizer=self.tokenizer,
                text_encoder=self.text_encoder,
                transformer=self.dit,
                scheduler=scheduler,
                args=cfg,
            )
            self.pipeline = self.pipeline.to(device)
            logger.info("Generation pipeline built")
        except Exception as e:
            logger.warning(f"Failed to build pipeline: {e}")
            import traceback
            logger.warning(traceback.format_exc())

    def forward(self, **kwargs):
        """Forward pass - delegates to Qwen3-VL for understanding."""
        if self.text_encoder is None:
            raise RuntimeError("JoyAIImageModel not loaded. Call load_weights_from_checkpoint() first.")
        return self.text_encoder(**kwargs)

    @torch.no_grad()
    def generate_text(self, input_ids, attention_mask, pixel_values=None, **kwargs):
        """Understanding inference via Qwen3-VL."""
        if self.text_encoder is None:
            raise RuntimeError("JoyAIImageModel not loaded.")
        return self.text_encoder.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            pixel_values=pixel_values,
            **kwargs,
        )

    @torch.no_grad()
    def generate_image(
        self,
        prompt: str,
        height: int = 768,
        width: int = 768,
        num_inference_steps: int = 50,
        guidance_scale: float = 4.0,
        negative_prompt: str = "",
        seed: int = 42,
        output_type: str = "pt",
    ):
        """Generation inference via the MMDiT + VAE pipeline.

        Args:
            prompt: Text prompt for image generation.
            height: Output image height in pixels.
            width: Output image width in pixels.
            num_inference_steps: Number of denoising steps.
            guidance_scale: Classifier-free guidance scale.
            negative_prompt: Negative prompt (empty string for none).
            seed: Random seed for reproducibility.
            output_type: 'pt' for tensor, 'pil' for PIL Image.

        Returns:
            Generated image (torch.Tensor or PIL.Image depending on output_type).
        """
        if self.pipeline is None:
            raise RuntimeError("Generation pipeline not loaded. Call load_weights_from_checkpoint() first.")

        generator = torch.Generator(device=self.pipeline.device).manual_seed(seed)
        output = self.pipeline(
            prompt=[prompt],
            negative_prompt=[negative_prompt],
            images=None,
            height=height,
            width=width,
            num_frames=1,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
            num_videos_per_prompt=1,
            output_type=output_type,
            return_dict=False,
        )
        return output
