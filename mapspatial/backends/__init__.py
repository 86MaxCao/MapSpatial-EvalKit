"""Backend package — registers lazy loaders only.

Importing this module does NOT import vllm, transformers, or any heavy dependency.
Heavy imports happen only when get_backend_cls(name) is called.
"""

from .registry import register, get_backend_cls, available_backends  # noqa: F401


@register("vllm")
def _vllm():
    from .vllm import VllmBackend
    return VllmBackend


@register("api")
def _api():
    from .api import APIBackend
    return APIBackend


@register("transformers")
def _transformers():
    from .transformers import TransformersBackend
    return TransformersBackend


@register("cambrian")
def _cambrian():
    from .cambrian import CambrianBackend
    return CambrianBackend


@register("vilasr")
def _vilasr():
    from .vilasr import VilasrBackend
    return VilasrBackend


@register("spatial_mllm")
def _spatial_mllm():
    from .spatial_mllm import SpatialMLLMBackend
    return SpatialMLLMBackend


@register("sensenova_si")
def _sensenova_si():
    from .sensenova_si import SenseNovaSIBackend
    return SenseNovaSIBackend


# Phase 2: VeOmni backends
@register("veomni_bagel")
def _veomni_bagel():
    from .veomni.bagel import BagelBackend
    return BagelBackend


@register("veomni_thinkmorph")
def _veomni_thinkmorph():
    from .veomni.thinkmorph import ThinkMorphBackend
    return ThinkMorphBackend


# Phase 3: VeOmni unified model backends
@register("veomni_blip3o")
def _veomni_blip3o():
    from .veomni.blip3o import BLIP3oBackend
    return BLIP3oBackend


@register("veomni_u1")
def _veomni_u1():
    from .veomni.u1 import U1Backend
    return U1Backend


@register("veomni_latentum")
def _veomni_latentum():
    from .veomni.latentum import LatentUMBackend
    return LatentUMBackend


@register("veomni_janus")
def _veomni_janus():
    from .veomni.janus import JanusBackend
    return JanusBackend


# Phase 3.5: New unified model backends
@register("veomni_showo2")
def _veomni_showo2():
    from .veomni.showo2 import ShowO2Backend
    return ShowO2Backend


@register("veomni_mingunivision")
def _veomni_mingunivision():
    from .veomni.mingunivision import MingUniVisionBackend
    return MingUniVisionBackend


@register("veomni_joyai")
def _veomni_joyai():
    from .veomni.joyai import JoyAIBackend
    return JoyAIBackend


@register("veomni_internvlu")
def _veomni_internvlu():
    from .veomni.internvlu import InternVLUBackend
    return InternVLUBackend


