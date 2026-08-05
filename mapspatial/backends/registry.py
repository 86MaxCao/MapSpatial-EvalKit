"""Backend registry with lazy loading via decorator pattern.

Register a loader function (not a class) that imports the implementation only
when get_backend_cls() is called. This means `mapspatial run --model qwen3-vl-8b`
never imports cambrian / veomni / etc.
"""

from __future__ import annotations

from typing import Callable

_REGISTRY: dict[str, Callable[[], type]] = {}


def register(name: str):
    """Decorator to register a lazy backend loader.

    The decorated function should return the backend class (importing it lazily).
    """
    def deco(loader: Callable[[], type]):
        _REGISTRY[name] = loader
        return loader
    return deco


def get_backend_cls(name: str):
    """Get the backend class by name. Triggers import on first call."""
    if name not in _REGISTRY:
        raise KeyError(
            f"unknown backend {name!r}; available: {sorted(_REGISTRY)}"
        )
    return _REGISTRY[name]()


def available_backends() -> list[str]:
    """List registered backend names."""
    return sorted(_REGISTRY)
