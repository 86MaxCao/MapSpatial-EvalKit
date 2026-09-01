"""Vendored official LatentUM (`model.latentum` / `model.decoder`). See ORIGIN.md."""

from model.latentum.configuration_latentum import LatentUMConfig

__all__ = ["LatentUMConfig", "LatentUMModel"]


def __getattr__(name):
    if name == "LatentUMModel":
        from model.latentum.modeling_latentum import LatentUMModel

        return LatentUMModel
    raise AttributeError(name)
