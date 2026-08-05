"""VeOmni backends subpackage.

Phase 2: Bagel + ThinkMorph
Phase 3: BLIP3o/U1/LatentUM/Janus
Phase 3.5: ShowO2 + MingUniVision + JoyAI + InternVLU (unified models)
"""

from .bagel import BagelBackend  # noqa: F401
from .thinkmorph import ThinkMorphBackend  # noqa: F401
from .blip3o import BLIP3oBackend  # noqa: F401
from .u1 import U1Backend  # noqa: F401
from .latentum import LatentUMBackend  # noqa: F401
from .janus import JanusBackend  # noqa: F401
from .showo2 import ShowO2Backend  # noqa: F401
from .mingunivision import MingUniVisionBackend  # noqa: F401
from .joyai import JoyAIBackend  # noqa: F401
from .internvlu import InternVLUBackend  # noqa: F401
