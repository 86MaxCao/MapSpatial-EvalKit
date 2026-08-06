"""Test all model configs load correctly."""

import glob
from pathlib import Path

from mapspatial.config import load_model_config
from mapspatial.backends import available_backends


CONFIGS_DIR = Path(__file__).parent.parent / "configs" / "models"


def test_all_configs_load():
    """Every YAML in configs/models/ should load without error."""
    configs = sorted(glob.glob(str(CONFIGS_DIR / "*.yaml")))
    assert len(configs) >= 17  # 14 understanding + 1 bagel + existing ones

    for path in configs:
        cfg = load_model_config(path)
        assert cfg.name, f"{path}: name is empty"
        assert cfg.backend, f"{path}: backend is empty"
        assert cfg.strategies, f"{path}: strategies is empty"


def test_understanding_models_use_direct():
    """All Phase 1 models should support direct strategy."""
    configs = sorted(glob.glob(str(CONFIGS_DIR / "*.yaml")))
    for path in configs:
        cfg = load_model_config(path)
        if cfg.backend == "veomni_bagel":
            continue  # Phase 2
        assert "direct" in cfg.strategies, f"{path}: missing direct strategy"


def test_api_configs_have_backend_args():
    """API configs should have api_url in backend_args."""
    api_configs = [p for p in glob.glob(str(CONFIGS_DIR / "*.yaml"))
                   if "qwen3.5" in p or "qwen3.6" in p or "gemini" in p]
    for path in api_configs:
        cfg = load_model_config(path)
        assert cfg.backend == "api", f"{path}: expected api backend"
        assert "api_url" in cfg.backend_args or "api_model" in cfg.backend_args, \
            f"{path}: missing api_url/api_model in backend_args"


def test_configs_match_registered_backends():
    """Every config's backend should be registered (except Phase 2)."""
    backends = available_backends()
    configs = sorted(glob.glob(str(CONFIGS_DIR / "*.yaml")))
    for path in configs:
        cfg = load_model_config(path)
        if cfg.backend.startswith("veomni"):
            continue  # Phase 2
        assert cfg.backend in backends, \
            f"{path}: backend {cfg.backend!r} not registered"
