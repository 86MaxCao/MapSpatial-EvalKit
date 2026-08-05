# --------------------------------------------------------
# VeOmni Integration of Show-o2
# Original code: Show-o (show-o2)
# --------------------------------------------------------

import copy
import json
import os
from typing import Any, Dict, Optional

from transformers.configuration_utils import PretrainedConfig
from transformers.utils import logging

logger = logging.get_logger(__name__)


class Showo2Config(PretrainedConfig):
    """VeOmni config wrapper for Show-o2.

    Show-o2 checkpoints use diffusers-style config.json with @register_to_config.
    This config wraps those fields in a HuggingFace PretrainedConfig for VeOmni's registry.
    """

    model_type = "showo2"
    architectures = ["Showo2Model"]

    def __init__(
        self,
        llm_vocab_size: int = 151669,
        llm_model_path: str = "Qwen/Qwen2.5-7B-Instruct",
        load_from_showo: bool = True,
        image_latent_dim: int = 16,
        image_latent_height: int = 27,
        image_latent_width: int = 27,
        video_latent_height: int = 27,
        video_latent_width: int = 27,
        patch_size: int = 2,
        hidden_size: int = 3584,
        clip_latent_dim: int = 1152,
        num_diffusion_layers: int = 10,
        add_time_embeds: bool = True,
        add_qk_norm: bool = True,
        clip_pretrained_model_path: str = "google/siglip-so400m-patch14-384",
        **kwargs,
    ):
        kwargs.pop("architectures", None)
        kwargs.pop("_class_name", None)
        kwargs.pop("_diffusers_version", None)
        super().__init__(**kwargs)

        self.llm_vocab_size = llm_vocab_size
        self.llm_model_path = llm_model_path
        self.load_from_showo = load_from_showo
        self.image_latent_dim = image_latent_dim
        self.image_latent_height = image_latent_height
        self.image_latent_width = image_latent_width
        self.video_latent_height = video_latent_height
        self.video_latent_width = video_latent_width
        self.patch_size = patch_size
        self.hidden_size = hidden_size
        self.clip_latent_dim = clip_latent_dim
        self.num_diffusion_layers = num_diffusion_layers
        self.add_time_embeds = add_time_embeds
        self.add_qk_norm = add_qk_norm
        self.clip_pretrained_model_path = clip_pretrained_model_path

    def to_dict(self):
        output = copy.deepcopy(self.__dict__)
        output["model_type"] = self.__class__.model_type
        return output

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, **kwargs):
        """Load config from a Show-o2 checkpoint (diffusers-style config.json)."""
        config_path = os.path.join(pretrained_model_name_or_path, "config.json")
        if not os.path.exists(config_path):
            # Fallback to standard HF config loading
            config_dict, kwargs = cls.get_config_dict(pretrained_model_name_or_path, **kwargs)
        else:
            with open(config_path, "r") as f:
                config_dict = json.load(f)

        if "model_type" not in config_dict:
            config_dict["model_type"] = "showo2"
        if "architectures" not in config_dict:
            config_dict["architectures"] = ["Showo2Model"]

        return cls.from_dict(config_dict, **kwargs)
