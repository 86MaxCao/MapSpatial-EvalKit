"""Strategy base class and validation.

Backend provides capabilities, Strategy decides how to orchestrate them.
Both produce the same Prediction schema — this orthogonality is what makes
cross-model accuracy comparison meaningful.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar, TYPE_CHECKING

from ..types import Capabilities, TaskSample, Prediction, RunContext

if TYPE_CHECKING:
    from ..backends.base import Backend


class Strategy(ABC):
    """Abstract strategy. Subclasses implement run()."""

    name: ClassVar[str]

    @abstractmethod
    def required_caps(self) -> dict[str, Any]:
        """Declare required capabilities for startup validation (fail-fast)."""
        ...

    @abstractmethod
    def run(
        self,
        backend: Any,  # Backend, but use Any to avoid circular import
        samples: list[TaskSample],
        ctx: RunContext,
    ) -> list[Prediction]:
        """Execute the strategy, producing one Prediction per sample."""
        ...

    def validate(self, backend: Any) -> None:
        """Check backend capabilities against strategy requirements.

        Must be called BEFORE loading model weights — fail-fast.
        """
        caps: Capabilities = backend.caps
        for cap, expected in self.required_caps().items():
            actual = getattr(caps, cap)
            if actual != expected:
                from ..types import Capabilities as Caps
                raise ValueError(
                    f"strategy {self.name!r} requires {cap}={expected}, "
                    f"but backend {getattr(backend, 'model_name', '?')!r} has {cap}={actual}. "
                    f"Available strategies: {_available_strategies(caps)}"
                )

    @staticmethod
    def _inject_system_prompt(messages: list, gen_kw: dict) -> list:
        """Prepend system_prompt from gen_kw to the first text item of each message.

        Model-agnostic: backends just see the modified text, no per-backend
        system_prompt handling needed.
        """
        sys_prompt = gen_kw.get("system_prompt")
        if not sys_prompt:
            return messages
        result = []
        for msg in messages:
            injected = False
            new_msg = []
            for item in msg:
                if item["type"] == "text" and not injected:
                    new_msg.append({
                        "type": "text",
                        "value": f"{sys_prompt}\n\n{item['value']}",
                    })
                    injected = True
                else:
                    new_msg.append(dict(item))
            if not injected:
                new_msg.append({"type": "text", "value": sys_prompt})
            result.append(new_msg)
        return result


def _available_strategies(caps: Capabilities) -> list[str]:
    """List which strategies are available given the capabilities."""
    s = ["direct"]
    if caps.native_interleave:
        s.append("native_interleave")
    if caps.draw:
        s.append("external_draw")
    if getattr(caps, "forced_interleave", False):
        s.append("forced_interleave")
    return s
