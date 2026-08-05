"""Nested configuration with YAML loading and ${ENV_VAR} expansion.

Fixes gate2building's per-backend config pollution (bagel_mode, vilasr_max_steps,
spatial_mllm_model_type all in flat RunConfig) by nesting backend-specific args.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_ENV_PATTERN = re.compile(r"\$\{([^}]+)\}")


def _expand_env(value: str) -> str:
    """Expand ${ENV_VAR} references in a string."""
    def replacer(m: re.Match) -> str:
        return os.environ.get(m.group(1), m.group(0))
    return _ENV_PATTERN.sub(replacer, value)


def _expand_recursive(obj):
    """Recursively expand ${...} in all string values of a nested structure."""
    if isinstance(obj, str):
        return _expand_env(obj)
    if isinstance(obj, dict):
        return {k: _expand_recursive(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_expand_recursive(v) for v in obj]
    return obj


@dataclass
class BackendConfig:
    """Per-model configuration, loaded from configs/models/*.yaml."""
    name: str
    backend: str
    model_path: str = ""
    load: dict = field(default_factory=dict)
    generate: dict = field(default_factory=dict)
    batch_size: int = 0
    backend_args: dict = field(default_factory=dict)
    strategies: list[str] = field(default_factory=lambda: ["direct"])
    system_prompt: str = ""

    @property
    def effective_batch_size(self) -> int:
        return self.batch_size if self.batch_size > 0 else 32


@dataclass
class RunConfig:
    """Top-level run configuration."""
    model: BackendConfig
    data_dir: Path
    output_dir: Path
    input_dir: Path
    views: list[str] = field(default_factory=lambda: ["sat", "webrd04", "blank"])
    tasks: list[str] = field(default_factory=lambda: ["t1", "t2", "t3", "t4"])
    variants: list[str] = field(default_factory=lambda: ["direct", "oracle"])
    strategy: str = "direct"
    batch_size: int = 0
    skip_preflight: bool = False
    allow_missing: int = 0
    store_question: bool = False
    no_save_generated: bool = False
    rank: int = 0
    world_size: int = 1

    @property
    def effective_batch_size(self) -> int:
        return self.batch_size if self.batch_size > 0 else self.model.effective_batch_size


def load_model_config(path: str | Path) -> BackendConfig:
    """Load a single model YAML config."""
    path = Path(path)
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
    raw = _expand_recursive(raw)
    return BackendConfig(
        name=raw["name"],
        backend=raw["backend"],
        model_path=raw.get("model_path", ""),
        load=raw.get("load", {}),
        generate=raw.get("generate", {}),
        batch_size=raw.get("batch_size", 0),
        backend_args=raw.get("backend_args", {}),
        strategies=raw.get("strategies", ["direct"]),
        system_prompt=raw.get("system_prompt", ""),
    )


def load_run_config(
    model_config_path: str | Path,
    *,
    data_dir: str | Path,
    input_dir: str | Path,
    output_dir: str | Path,
    strategy: str = "direct",
    views: list[str] | None = None,
    tasks: list[str] | None = None,
    variants: list[str] | None = None,
    batch_size: int = 0,
    skip_preflight: bool = False,
    allow_missing: int = 0,
    store_question: bool = False,
    no_save_generated: bool = False,
    rank: int = 0,
    world_size: int = 1,
) -> RunConfig:
    """Build a RunConfig from a model YAML + CLI overrides."""
    model = load_model_config(model_config_path)
    return RunConfig(
        model=model,
        data_dir=Path(data_dir),
        input_dir=Path(input_dir),
        output_dir=Path(output_dir),
        strategy=strategy,
        views=views or ["sat", "webrd04", "blank"],
        tasks=tasks or ["t1", "t2", "t3", "t4"],
        variants=variants or ["direct", "oracle"],
        batch_size=batch_size,
        skip_preflight=skip_preflight,
        allow_missing=allow_missing,
        store_question=store_question,
        no_save_generated=no_save_generated,
        rank=rank,
        world_size=world_size,
    )
