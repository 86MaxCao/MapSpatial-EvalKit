"""Test backend registry and lazy loading."""

from mapspatial.backends import available_backends, get_backend_cls


def test_all_backends_registered():
    """All 7 Phase 1 backends should be registered."""
    backends = available_backends()
    expected = {"api", "cambrian", "sensenova_si", "spatial_mllm",
                "transformers", "vilasr", "vllm"}
    assert expected.issubset(set(backends))


def test_backend_caps():
    """Check capabilities of registered backends."""
    for name in available_backends():
        cls = get_backend_cls(name)
        caps = cls.caps
        assert hasattr(caps, "batch")
        assert hasattr(caps, "draw")
        assert hasattr(caps, "native_interleave")
        assert hasattr(caps, "max_images")
        assert hasattr(caps, "video")


def test_vllm_caps():
    """vLLM should have batch=True, draw=False."""
    cls = get_backend_cls("vllm")
    assert cls.caps.batch is True
    assert cls.caps.draw is False


def test_api_caps():
    """API should have batch=False."""
    cls = get_backend_cls("api")
    assert cls.caps.batch is False


def test_transformers_caps():
    """Transformers should have batch=False."""
    cls = get_backend_cls("transformers")
    assert cls.caps.batch is False


def test_unknown_backend():
    """Unknown backend should raise KeyError."""
    try:
        get_backend_cls("nonexistent")
        assert False, "should have raised"
    except KeyError:
        pass
