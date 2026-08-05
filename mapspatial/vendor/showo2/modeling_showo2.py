# --------------------------------------------------------
# VeOmni Integration of Show-o2
# Original code: Show-o (show-o2)
# --------------------------------------------------------

import os
from types import SimpleNamespace
from typing import List, Optional, Tuple, Union

import torch
import torch.nn as nn
from transformers.modeling_utils import PreTrainedModel
from transformers.utils import logging

from .configuration_showo2 import Showo2Config

logger = logging.get_logger(__name__)


class Showo2Model(PreTrainedModel):
    """VeOmni wrapper for Show-o2 (Showo2Qwen2_5).

    Show-o2 uses diffusers ModelMixin, not HuggingFace PreTrainedModel.
    This wrapper provides VeOmni-compatible interface while delegating
    to the inner Showo2Qwen2_5 model loaded via from_pretrained().
    """

    config_class = Showo2Config
    main_input_name = "input_ids"
    base_model_prefix = ""
    _supports_flash_attn_2 = True
    supports_gradient_checkpointing = True
    _no_split_modules = ["Qwen2DecoderLayer", "ModulatedAttentionBlock"]

    def __init__(self, config: Showo2Config, **kwargs):
        super().__init__(config)
        # The inner model is created lazily in load_weights_from_checkpoint
        # to avoid loading SigLIP/Qwen2 from HF during meta-device init.
        self.showo2 = None
        self.vae = None
        self._device = None  # target device for inner model

    def to_empty(self, *args, device=None, **kwargs):
        """Capture target device since wrapper has no parameters."""
        if device is not None:
            self._device = str(device)
        return self

    @property
    def lm_head(self):
        if self.showo2 is not None:
            return self.showo2.showo.lm_head
        return None

    def get_input_embeddings(self):
        if self.showo2 is not None:
            return self.showo2.showo.model.embed_tokens
        return None

    def get_output_embeddings(self):
        if self.showo2 is not None:
            return self.showo2.showo.lm_head
        return None

    def set_vae(self, vae):
        """Set the Wan2.1 VAE (loaded externally)."""
        self.vae = vae

    def load_weights_from_checkpoint(
        self,
        checkpoint_path: str,
        device: Optional[Union[str, torch.device]] = None,
    ):
        """Load the inner Showo2Qwen2_5 model from checkpoint.

        Show-o2 uses diffusers ModelMixin.from_pretrained() which handles
        both config reading and weight loading from .bin files.

        Args:
            checkpoint_path: Path to the Show-o2 checkpoint directory.
            device: Target device for the model. If None, attempts to detect
                from the wrapper's existing parameters/buffers, falling back
                to CPU. Pass this explicitly when the wrapper has no parameters
                (e.g., after meta-device init).
        """
        from .models.modeling_showo2_qwen2_5 import Showo2Qwen2_5

        # Determine the target device.
        # The wrapper itself may have no parameters (self.showo2 starts as None),
        # so next(self.parameters()) can raise StopIteration.
        if device is not None:
            target_device = torch.device(device)
        elif self._device is not None:
            target_device = torch.device(self._device)
        else:
            target_device = None
            try:
                target_device = next(self.parameters()).device
            except StopIteration:
                try:
                    target_device = next(self.buffers()).device
                except StopIteration:
                    target_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    logger.warning(
                        "Showo2Model has no parameters/buffers to infer device. "
                        f"Using {target_device}."
                    )

        logger.info(f"Loading Showo2Qwen2_5 from {checkpoint_path} on {target_device}...")
        self.showo2 = Showo2Qwen2_5.from_pretrained(
            checkpoint_path,
            use_safetensors=False,
            torch_dtype=torch.bfloat16,
        )
        self.showo2 = self.showo2.to(target_device)
        self.showo2.eval()
        logger.info("Showo2Qwen2_5 loaded successfully")

    def forward(self, **kwargs):
        """Forward pass - delegates to inner Showo2Qwen2_5."""
        if self.showo2 is None:
            raise RuntimeError("Showo2Model not loaded. Call load_weights_from_checkpoint() first.")
        return self.showo2(**kwargs)

    @torch.no_grad()
    def mmu_generate(self, input_embeds, attention_mask, max_new_tokens=100,
                     temperature=1.0, top_k=None, eos_token=None):
        """Understanding inference - delegates to inner model."""
        if self.showo2 is None:
            raise RuntimeError("Showo2Model not loaded.")
        return self.showo2.mmu_generate(
            input_embeds=input_embeds,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_k=top_k,
            eos_token=eos_token,
        )

    @torch.no_grad()
    def t2i_generate(self, **kwargs):
        """Text-to-image generation - delegates to inner model."""
        if self.showo2 is None:
            raise RuntimeError("Showo2Model not loaded.")
        return self.showo2.t2i_generate(**kwargs)
