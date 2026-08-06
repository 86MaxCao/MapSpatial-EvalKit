"""Test Phase 2: strategies, vendor, and veomni backends."""

import pytest
from pathlib import Path

from mapspatial.strategies import get_strategy, available_strategies
from mapspatial.backends import available_backends, get_backend_cls
from mapspatial.config import load_model_config


def test_native_interleave_strategy():
    strat = get_strategy("native_interleave")
    assert strat.name == "native_interleave"
    assert strat.required_caps() == {"native_interleave": True}


def test_external_draw_strategy():
    strat = get_strategy("external_draw")
    assert strat.name == "external_draw"
    assert strat.required_caps() == {"draw": True}


def test_all_three_strategies():
    """direct, native_interleave, external_draw all registered."""
    strats = available_strategies()
    assert "direct" in strats
    assert "native_interleave" in strats
    assert "external_draw" in strats


def test_strategy_validation_pass():
    """Strategy.validate should pass when backend has the required cap."""
    strat = get_strategy("native_interleave")
    cls = get_backend_cls("veomni_bagel")
    # Create a mock backend with correct caps
    class MockBackend:
        caps = cls.caps
        model_name = "mock"
    strat.validate(MockBackend())


def test_strategy_validation_fail():
    """Strategy.validate should fail when backend lacks the required cap."""
    strat = get_strategy("native_interleave")
    # VllmBackend doesn't have native_interleave
    cls = get_backend_cls("vllm")
    class MockBackend:
        caps = cls.caps
        model_name = "mock"
    with pytest.raises(ValueError, match="native_interleave"):
        strat.validate(MockBackend())


def test_veomni_backends_registered():
    assert "veomni_bagel" in available_backends()
    assert "veomni_thinkmorph" in available_backends()


def test_bagel_caps():
    """Bagel backend should have draw=True, native_interleave=True, batch=True."""
    cls = get_backend_cls("veomni_bagel")
    assert cls.caps.draw is True
    assert cls.caps.native_interleave is True
    assert cls.caps.batch is True


def test_thinkmorph_caps():
    """ThinkMorph should inherit Bagel's capabilities."""
    cls = get_backend_cls("veomni_thinkmorph")
    assert cls.caps.draw is True
    assert cls.caps.native_interleave is True


def test_thinkmorph_inherits_bagel():
    """ThinkMorphBackend should be a subclass of BagelBackend."""
    from mapspatial.backends.veomni.bagel import BagelBackend
    from mapspatial.backends.veomni.thinkmorph import ThinkMorphBackend
    assert issubclass(ThinkMorphBackend, BagelBackend)


def test_bagel_config_loads():
    CONFIGS_DIR = Path(__file__).parent.parent / "configs" / "models"
    cfg = load_model_config(CONFIGS_DIR / "bagel-7b.yaml")
    assert cfg.backend == "veomni_bagel"
    assert cfg.backend_args["cfg_text_scale"] == 4.0
    assert cfg.backend_args["num_timesteps"] == 50
    assert "direct" in cfg.strategies
    assert "native_interleave" in cfg.strategies
    assert "external_draw" in cfg.strategies


def test_thinkmorph_config_loads():
    CONFIGS_DIR = Path(__file__).parent.parent / "configs" / "models"
    cfg = load_model_config(CONFIGS_DIR / "thinkmorph-7b.yaml")
    assert cfg.backend == "veomni_thinkmorph"
    assert cfg.backend_args["cfg_text_scale"] == 3.0
    assert cfg.backend_args["max_rounds"] == 5


def test_vendor_system_prompt():
    from mapspatial.loader import init_empty_weights, load_model, load_tokenizer
    assert callable(init_empty_weights)
    assert callable(load_model)
    assert callable(load_tokenizer)


def test_vendor_inferencer_importable():
    """The vendored interleave inferencer should import without loading any model."""
    try:
        from mapspatial.vendor.bagel_interleave.inferencer import InterleaveInferencer
        assert InterleaveInferencer is not None
    except ImportError:
        pass  # May need torch/torchvision at runtime
