"""Self-contained model loader — no VeOmni dependency.

Implements the minimal loading chain:
  1. Read config.json from model_path
  2. Instantiate model via _from_config() under init_empty_weights()
  3. Load safetensors weights into the empty model

This replaces VeOmni's loader.py + module_utils.py (~1800 lines)
with ~80 lines that do exactly what we need for inference.

The key difference from VeOmni's loader: no MODELING_REGISTRY, no
MODEL_CONFIG_REGISTRY, no OpsImplementationConfig, no FSDP/DTensor
support — just load a model and its weights.
"""

from __future__ import annotations

import json
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import torch
from torch import nn


@contextmanager
def init_empty_weights():
    """Context manager that places new parameters on meta device.

    Borrowed from accelerate v1.0.0rc1, simplified.
    Allows instantiating large models without allocating real memory.
    """
    original_register_parameter = nn.Module.register_parameter

    def register_parameter(self, name, param):
        if param is not None:
            param = nn.Parameter(param.detach().to("meta"), requires_grad=param.requires_grad)
        original_register_parameter(self, name, param)

    try:
        nn.Module.register_parameter = register_parameter
        yield
    finally:
        nn.Module.register_parameter = original_register_parameter


def _load_safetensors(model_path: str) -> dict[str, torch.Tensor]:
    """Load all safetensors files from a model directory into a single dict."""
    from safetensors import safe_open

    model_path = Path(model_path)
    state_dict: dict[str, torch.Tensor] = {}

    # 1. Sharded safetensors (model.safetensors.index.json)
    index_file = model_path / "model.safetensors.index.json"
    if index_file.exists():
        with open(index_file) as f:
            index = json.load(f)
        weight_files = index.get("weight_map", {})
        seen_files = set()
        for filename in weight_files.values():
            if filename not in seen_files:
                seen_files.add(filename)
                fp = model_path / filename
                if fp.exists():
                    with safe_open(str(fp), framework="pt", device="cpu") as st:
                        for key in st.keys():
                            state_dict[key] = st.get_tensor(key)
        if state_dict:
            return state_dict

    # 2. Single safetensors file
    single = model_path / "model.safetensors"
    if single.exists():
        with safe_open(str(single), framework="pt", device="cpu") as st:
            for key in st.keys():
                state_dict[key] = st.get_tensor(key)
        return state_dict

    # 3. Sharded .bin files (pytorch_model.bin.index.json OR diffusion_pytorch_model.bin.index.json)
    for index_name in ("pytorch_model.bin.index.json", "diffusion_pytorch_model.bin.index.json"):
        bin_index = model_path / index_name
        if bin_index.exists():
            with open(bin_index) as f:
                index = json.load(f)
            weight_files = index.get("weight_map", {})
            seen_files = set()
            for filename in weight_files.values():
                if filename not in seen_files:
                    seen_files.add(filename)
                    fp = model_path / filename
                    if fp.exists():
                        shard = torch.load(str(fp), map_location="cpu", weights_only=True)
                        state_dict.update(shard)
                        del shard
            if state_dict:
                return state_dict

    # 4. Single .bin file
    bin_file = model_path / "pytorch_model.bin"
    if bin_file.exists():
        return torch.load(str(bin_file), map_location="cpu", weights_only=True)

    # 5. Any safetensors files in directory (glob)
    safetensors_files = sorted(model_path.glob("*.safetensors"))
    for fp in safetensors_files:
        with safe_open(str(fp), framework="pt", device="cpu") as st:
            for key in st.keys():
                state_dict[key] = st.get_tensor(key)
    if state_dict:
        return state_dict

    raise FileNotFoundError(f"No weight files found in {model_path}")


def load_model(
    model_path: str,
    model_cls: type,
    *,
    device: str = "cuda",
    dtype: str = "bfloat16",
    config_overrides: dict | None = None,
    **kwargs,
) -> tuple[nn.Module, Any]:
    """Load a model from a checkpoint directory.

    Follows VeOmni's loading pattern:
      1. config_class.from_pretrained(model_path) → proper config with nested subconfigs
      2. init_empty_weights() → model_cls._from_config(config)
      3. model.to_empty(device) → model.to(bfloat16)
      4. model.load_weights_from_checkpoint(model_path) OR _load_safetensors + load_state_dict

    Returns:
        (model, config) — model is on device and in eval mode
    """
    dt = getattr(torch, dtype)

    # 1. Load config — use from_pretrained to properly create nested config objects
    #    (BagelConfig has llm_config, vit_config, vae_config; from_dict doesn't init these)
    config = None
    if hasattr(model_cls, "config_class"):
        config = model_cls.config_class.from_pretrained(model_path, trust_remote_code=True)
        if config_overrides:
            for k, v in config_overrides.items():
                setattr(config, k, v)

    if config is None:
        # Fallback: read config.json and pass dict directly
        config_path = Path(model_path) / "config.json"
        if not config_path.exists():
            raise FileNotFoundError(f"No config.json in {model_path}")
        with open(config_path) as f:
            config_dict = json.load(f)
        if config_overrides:
            config_dict.update(config_overrides)
        config = config_dict

    # 2. Instantiate model on meta device
    with init_empty_weights():
        if isinstance(config, dict):
            model = model_cls._from_config(config_dict=config, **kwargs)
        else:
            model = model_cls._from_config(config=config, **kwargs)

    # 3. Move to real device and dtype (matching VeOmni: to_empty then to(bf16))
    model = model.to_empty(device=device).to(dt)

    # 4. Load weights — check for custom loader first (Show-o2, JoyAI use this)
    if hasattr(model, "load_weights_from_checkpoint"):
        model.load_weights_from_checkpoint(model_path)
    else:
        state_dict = _load_safetensors(model_path)
        missing, unexpected = model.load_state_dict(state_dict, strict=False)
        if missing:
            real_missing = [k for k in missing if not k.endswith("position_ids")]
            if real_missing:
                print(f"WARNING: {len(real_missing)} missing keys (first 10): {real_missing[:10]}")
        if unexpected:
            print(f"WARNING: {len(unexpected)} unexpected keys (first 10): {unexpected[:10]}")
        del state_dict

    model.eval()
    return model, config


def load_tokenizer(model_path: str, **kwargs):
    """Load a tokenizer from a model directory."""
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, **kwargs)


def load_processor(model_path: str, **kwargs):
    """Load a processor from a model directory."""
    from transformers import AutoProcessor
    return AutoProcessor.from_pretrained(model_path, trust_remote_code=True, **kwargs)
