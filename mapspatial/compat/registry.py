"""Compatibility patch registry.

Patches are idempotent, self-disabling, narrow, and declarative.
Each patch returns True if applied, False if upstream already fixed (no-op).
"""

from __future__ import annotations

from typing import Callable

_applied: set[str] = set()
_registry: dict[str, dict] = {}


def patch(name: str, *, reason: str, affects: tuple[str, ...] = ()):
    """Decorator to register a compat patch."""
    def deco(fn: Callable[[], bool]):
        _registry[name] = {
            "fn": fn,
            "reason": reason,
            "affects": affects,
            "name": name,
        }
        return fn
    return deco


def apply(*names: str) -> list[str]:
    """Apply named patches. Idempotent — safe to call multiple times.
    Returns list of patch names that were actually applied (first time only).
    """
    newly_applied = []
    for name in names:
        if name in _applied:
            continue
        if name not in _registry:
            raise KeyError(f"unknown compat patch: {name!r}; available: {sorted(_registry)}")
        result = _registry[name]["fn"]()
        if result:
            _applied.add(name)
            newly_applied.append(name)
        # If result is False, upstream fixed it — no-op, don't mark as applied
    return newly_applied


def applied() -> set[str]:
    """Return set of patches currently in effect."""
    return set(_applied)


def describe() -> list[dict]:
    """Describe all registered patches and their current status."""
    out = []
    for name, info in sorted(_registry.items()):
        out.append({
            "name": name,
            "reason": info["reason"],
            "affects": list(info["affects"]),
            "active": name in _applied,
        })
    return out


# Auto-register built-in patches
from .patches import tied_weights as _tied_weights  # noqa: E402,F401
from .patches import meta_tensor_item as _meta_tensor  # noqa: E402,F401
