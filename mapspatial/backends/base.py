"""Backend base class and Capabilities.

Backend declares abilities (Capabilities), Strategy decides how to orchestrate.
The two dimensions are orthogonal — Qwen3-VL + direct and Bagel + native_interleave
produce identical Prediction schema.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from ..types import Capabilities, Message, Prediction
from ..config import BackendConfig


class Backend(ABC):
    """Abstract backend. Subclasses declare caps and implement understand().

    draw() and interleave() are optional — only for caps.draw / caps.native_interleave.
    """

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False, draw=False, native_interleave=False, max_images=1, video=False
    )
    COMPAT: ClassVar[tuple[str, ...]] = ()

    @abstractmethod
    def __init__(self, cfg: BackendConfig) -> None: ...

    @property
    @abstractmethod
    def model_name(self) -> str: ...

    @abstractmethod
    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Always accepts list and returns equal-length list.

        caps.batch=False → serial loop internally.
        caps.batch=True → submit all at once (e.g. vLLM llm.generate(all)).
        """
        ...

    def draw(self, context: Message, instruction: str, **kw):
        """Generate an intermediate image. Only for caps.draw=True."""
        raise NotImplementedError(f"{self.model_name} does not support draw()")

    def interleave(self, message: Message, *, max_rounds: int, **kw) -> Prediction:
        """Native interleaved reasoning loop. Only for caps.native_interleave=True."""
        raise NotImplementedError(f"{self.model_name} does not support interleave()")

    def forced_interleave(
        self,
        message: Message,
        instruction: str = "",
        *,
        max_images: int = 1,
        image_first: bool = True,
        followup: str = "",
        **kw,
    ) -> Prediction:
        """Stateful image-first G2U. Only for caps.forced_interleave=True."""
        raise NotImplementedError(f"{self.model_name} does not support forced_interleave()")
