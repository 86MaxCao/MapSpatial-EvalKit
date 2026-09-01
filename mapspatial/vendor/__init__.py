"""Vendor package — third-party modeling and inference code.

See ORIGIN.md files in each subdirectory for source attribution.

Some vendored packages were copied from repos whose internal imports use
top-level absolute names (e.g. ``from cambrian... import``, ``from
models.sensenova_si... import``). To keep those imports working without
rewriting the vendored source, we register namespace placeholders in
``sys.modules`` so the absolute names resolve into the vendored tree.
"""

from __future__ import annotations

import os
import sys
import types

_VDIR = os.path.dirname(os.path.abspath(__file__))


def _ensure_namespace(name: str, path: str) -> None:
    """Register ``name`` as a namespace package rooted at ``path``.

    Because the placeholder is already in ``sys.modules``, Python will not
    try to execute an ``__init__.py`` for that name; submodule lookups fall
    through to ``path`` (and the real, differently-named vendored package
    still imports normally when accessed by its ``mapspatial.vendor.*`` name).
    """
    parts = name.split(".")
    # Ensure ancestor namespace packages exist so dotted lookups resolve.
    for i in range(1, len(parts)):
        parent = ".".join(parts[:i])
        if parent not in sys.modules:
            mod = types.ModuleType(parent)
            mod.__path__ = []  # type: ignore[attr-defined]
            mod.__package__ = parent
            sys.modules[parent] = mod
    if name not in sys.modules:
        mod = types.ModuleType(name)
        mod.__path__ = [path]  # type: ignore[attr-defined]
        mod.__package__ = name
        sys.modules[name] = mod


# Expose the vendored trees under the absolute names their own code expects.
_ensure_namespace("cambrian", os.path.join(_VDIR, "cambrian", "cambrian_pkg"))
_ensure_namespace("models.cambrian", os.path.join(_VDIR, "cambrian", "cambrian_pkg"))
_ensure_namespace("models.sensenova_si", os.path.join(_VDIR, "sensenova_si_pkg"))
_ensure_namespace("utils", os.path.join(_VDIR, "vilasr_utils"))
# Official LatentUM is the `model` package (model.latentum / model.decoder).
_ensure_namespace("model", os.path.join(_VDIR, "latentum"))
