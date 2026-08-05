# --------------------------------------------------------
# VeOmni Integration of InternVL-U
# Copyright (c) 2026 OpenGVLab (original code)
# Licensed under The MIT License
# --------------------------------------------------------

import copy
import json
import os
from typing import Any, Dict, Optional

from transformers.configuration_utils import PretrainedConfig
from transformers.utils import logging

logger = logging.get_logger(__name__)


class InternVLUConfig(PretrainedConfig):
    """Unified configuration for InternVL-U model.

    Wraps three sub-configs:
    - vlm_config: InternVLUChatConfig (InternViT + Qwen3 LLM)
    - generation_decoder_config: InternVLUGenerationDecoderConfig (DiT)
    - vae_config: dict for AutoencoderKLQwenImage (loaded by diffusers)
    """

    model_type = "internvlu"
    architectures = ["InternVLUModel"]

    def __init__(
        self,
        vlm_config: Optional[Dict[str, Any]] = None,
        generation_decoder_config: Optional[Dict[str, Any]] = None,
        vae_config: Optional[Dict[str, Any]] = None,
        scheduler_config: Optional[Dict[str, Any]] = None,
        processor_config: Optional[Dict[str, Any]] = None,
        # Training-relevant fields
        mse_weight: float = 1.0,
        ce_weight: float = 1.0,
        freeze_vit: bool = True,
        freeze_llm: bool = True,
        freeze_vae: bool = True,
        freeze_gen_modules: bool = False,
        **kwargs,
    ):
        kwargs.pop("architectures", None)
        super().__init__(**kwargs)

        # Parse sub-configs from dicts
        if vlm_config is not None:
            if isinstance(vlm_config, dict):
                from .vlm.configuration_internvlu_chat import InternVLUChatConfig

                self.vlm_config = InternVLUChatConfig(**vlm_config)
            else:
                self.vlm_config = vlm_config
        else:
            self.vlm_config = None

        if generation_decoder_config is not None:
            if isinstance(generation_decoder_config, dict):
                from .diffusion.configuration_internvlu_generation_decoder import (
                    InternVLUGenerationDecoderConfig,
                )

                self.generation_decoder_config = InternVLUGenerationDecoderConfig(
                    **generation_decoder_config
                )
            else:
                self.generation_decoder_config = generation_decoder_config
        else:
            self.generation_decoder_config = None

        self.vae_config = vae_config if vae_config is not None else None
        self.scheduler_config = scheduler_config if scheduler_config is not None else None
        self.processor_config = processor_config if processor_config is not None else None

        # Training fields
        self.mse_weight = mse_weight
        self.ce_weight = ce_weight
        self.freeze_vit = freeze_vit
        self.freeze_llm = freeze_llm
        self.freeze_vae = freeze_vae
        self.freeze_gen_modules = freeze_gen_modules

    def to_dict(self):
        output = copy.deepcopy(self.__dict__)
        if self.vlm_config is not None and hasattr(self.vlm_config, "to_dict"):
            output["vlm_config"] = self.vlm_config.to_dict()
        if self.generation_decoder_config is not None and hasattr(
            self.generation_decoder_config, "to_dict"
        ):
            output["generation_decoder_config"] = self.generation_decoder_config.to_dict()
        output["model_type"] = self.__class__.model_type
        return output

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, **kwargs):
        """Load config from a multi-directory checkpoint.

        InternVL-U checkpoints have:
          model_index.json
          vlm/config.json + vlm/model.safetensors
          generation_decoder/config.json + generation_decoder/model.safetensors
          vae/config.json + vae/diffusion_pytorch_model.safetensors
          scheduler/scheduler_config.json
          processor/processor_config.json
        """
        path = pretrained_model_name_or_path

        # Check if this is a pipeline-style checkpoint (has model_index.json)
        model_index_path = os.path.join(path, "model_index.json")
        if os.path.exists(model_index_path):
            return cls._from_pipeline_checkpoint(path, **kwargs)

        # Otherwise, try standard config.json (single-dir format)
        config_dict, kwargs = cls.get_config_dict(path, **kwargs)
        if "model_type" not in config_dict:
            config_dict["model_type"] = "internvlu"
        if "architectures" not in config_dict:
            config_dict["architectures"] = ["InternVLUModel"]
        return cls.from_dict(config_dict, **kwargs)

    @classmethod
    def _from_pipeline_checkpoint(cls, path, **kwargs):
        """Load from a pipeline-style checkpoint with model_index.json."""
        import json

        with open(os.path.join(path, "model_index.json"), "r") as f:
            model_index = json.load(f)

        config_dict = {
            "model_type": "internvlu",
            "architectures": ["InternVLUModel"],
        }

        # Load VLM config
        vlm_dir = os.path.join(path, "vlm")
        if os.path.isdir(vlm_dir):
            vlm_config_path = os.path.join(vlm_dir, "config.json")
            if os.path.exists(vlm_config_path):
                with open(vlm_config_path, "r") as f:
                    config_dict["vlm_config"] = json.load(f)

        # Load generation decoder config
        gen_dir = os.path.join(path, "generation_decoder")
        if os.path.isdir(gen_dir):
            gen_config_path = os.path.join(gen_dir, "config.json")
            if os.path.exists(gen_config_path):
                with open(gen_config_path, "r") as f:
                    config_dict["generation_decoder_config"] = json.load(f)

        # Load VAE config
        vae_dir = os.path.join(path, "vae")
        if os.path.isdir(vae_dir):
            vae_config_path = os.path.join(vae_dir, "config.json")
            if os.path.exists(vae_config_path):
                with open(vae_config_path, "r") as f:
                    config_dict["vae_config"] = json.load(f)

        # Load scheduler config
        sched_dir = os.path.join(path, "scheduler")
        if os.path.isdir(sched_dir):
            sched_config_path = os.path.join(sched_dir, "scheduler_config.json")
            if os.path.exists(sched_config_path):
                with open(sched_config_path, "r") as f:
                    config_dict["scheduler_config"] = json.load(f)

        # Load processor config
        proc_dir = os.path.join(path, "processor")
        if os.path.isdir(proc_dir):
            proc_config_path = os.path.join(proc_dir, "processor_config.json")
            if os.path.exists(proc_config_path):
                with open(proc_config_path, "r") as f:
                    config_dict["processor_config"] = json.load(f)

        return cls.from_dict(config_dict, **kwargs)
