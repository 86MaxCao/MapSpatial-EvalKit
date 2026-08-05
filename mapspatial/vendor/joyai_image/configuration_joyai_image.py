# --------------------------------------------------------
# VeOmni Integration of JoyAI-Image
# Original code: JoyAI-Image (Qwen3-VL + MMDiT + Wan2.1 VAE)
# --------------------------------------------------------

import copy
import json
import os
from typing import Any, Dict, Optional

from transformers.configuration_utils import PretrainedConfig
from transformers.utils import logging

logger = logging.get_logger(__name__)


class JoyAIImageConfig(PretrainedConfig):
    """VeOmni config wrapper for JoyAI-Image.

    JoyAI-Image has three components:
    - text_encoder: Qwen3-VL (HuggingFace format in JoyAI-Image-Und/)
    - transformer: MMDiT (PyTorch .pth in transformer/)
    - vae: Wan2.1 VAE (PyTorch .pth in vae/)
    """

    model_type = "joyai_image"
    architectures = ["JoyAIImageModel"]

    def __init__(
        self,
        transformer_ckpt: str = None,
        vae_ckpt: str = None,
        text_encoder_ckpt: str = None,
        # DiT architecture config
        dit_hidden_size: int = 4096,
        dit_heads_num: int = 32,
        dit_mm_double_blocks_depth: int = 40,
        dit_in_channels: int = 16,
        dit_out_channels: int = 16,
        dit_patch_size: list = None,
        dit_rope_dim_list: list = None,
        dit_text_states_dim: int = 4096,
        dit_rope_type: str = "rope",
        dit_modulation_type: str = "wanx",
        dit_theta: int = 10000,
        **kwargs,
    ):
        kwargs.pop("architectures", None)
        super().__init__(**kwargs)

        if dit_patch_size is None:
            dit_patch_size = [1, 2, 2]
        if dit_rope_dim_list is None:
            dit_rope_dim_list = [16, 56, 56]

        self.transformer_ckpt = transformer_ckpt
        self.vae_ckpt = vae_ckpt
        self.text_encoder_ckpt = text_encoder_ckpt

        self.dit_hidden_size = dit_hidden_size
        self.dit_heads_num = dit_heads_num
        self.dit_mm_double_blocks_depth = dit_mm_double_blocks_depth
        self.dit_in_channels = dit_in_channels
        self.dit_out_channels = dit_out_channels
        self.dit_patch_size = dit_patch_size
        self.dit_rope_dim_list = dit_rope_dim_list
        self.dit_text_states_dim = dit_text_states_dim
        self.dit_rope_type = dit_rope_type
        self.dit_modulation_type = dit_modulation_type
        self.dit_theta = dit_theta

    def to_dict(self):
        output = copy.deepcopy(self.__dict__)
        output["model_type"] = self.__class__.model_type
        return output

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, **kwargs):
        """Load config from a JoyAI-Image checkpoint."""
        config_path = os.path.join(pretrained_model_name_or_path, "config.json")
        if not os.path.exists(config_path):
            config_dict, kwargs = cls.get_config_dict(pretrained_model_name_or_path, **kwargs)
        else:
            with open(config_path, "r") as f:
                config_dict = json.load(f)

        if "model_type" not in config_dict:
            config_dict["model_type"] = "joyai_image"
        if "architectures" not in config_dict:
            config_dict["architectures"] = ["JoyAIImageModel"]

        return cls.from_dict(config_dict, **kwargs)
