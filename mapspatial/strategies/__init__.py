"""Strategy package — provides get_strategy() to look up by name."""

from .base import Strategy  # noqa: F401
from .direct import DirectStrategy  # noqa: F401
from .native_interleave import NativeInterleaveStrategy  # noqa: F401
from .external_draw import ExternalDrawStrategy  # noqa: F401

_STRATEGY_REGISTRY: dict[str, type[Strategy]] = {
    "direct": DirectStrategy,
    "native_interleave": NativeInterleaveStrategy,
    "external_draw": ExternalDrawStrategy,
}


def get_strategy(name: str) -> Strategy:
    """Get a strategy instance by name."""
    if name not in _STRATEGY_REGISTRY:
        raise KeyError(
            f"unknown strategy {name!r}; available: {sorted(_STRATEGY_REGISTRY)}"
        )
    return _STRATEGY_REGISTRY[name]()


def available_strategies() -> list[str]:
    return sorted(_STRATEGY_REGISTRY)
