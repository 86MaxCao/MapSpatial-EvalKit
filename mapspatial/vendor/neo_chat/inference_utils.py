"""Vendored inference helpers for SenseNova-U1 (NEOChatModel).

Copied verbatim from the official SenseNova-U1 package
(``src/sensenova_u1/models/neo_unify/utils.py`` and ``modeling_neo_chat.py``)
so that understanding inference aligns with ``examples/vqa/inference.py``.

These are pure image/tensor utilities with no torch-model or transformers
dependency, so they run under transformers 5.x where the official modeling
package cannot (it pins transformers==4.57.1).
"""

from __future__ import annotations

import math

import torch
import torchvision.transforms as T
from PIL import Image

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def round_by_factor(number: float, factor: int) -> int:
    return round(number / factor) * factor


def ceil_by_factor(number: float, factor: int) -> int:
    return math.ceil(number / factor) * factor


def floor_by_factor(number: float, factor: int) -> int:
    return math.floor(number / factor) * factor


def smart_resize(
    height: int,
    width: int,
    factor: int = 32,
    min_pixels: int = 65536,
    max_pixels: int = 4194304,
) -> tuple[int, int]:
    """Rescale so that H/W are divisible by `factor` and total pixels in [min, max]."""
    if max(height, width) / min(height, width) > 200:
        raise ValueError(
            f"absolute aspect ratio must be smaller than 200, got {max(height, width) / min(height, width)}"
        )
    h_bar = max(factor, round_by_factor(height, factor))
    w_bar = max(factor, round_by_factor(width, factor))
    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = max(factor, floor_by_factor(height / beta, factor))
        w_bar = max(factor, floor_by_factor(width / beta, factor))
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = ceil_by_factor(height * beta, factor)
        w_bar = ceil_by_factor(width * beta, factor)
    return h_bar, w_bar


def dynamic_preprocess_native_resolution(
    image: Image.Image,
    size_factor: int = 32,
    min_pixels: int = 65536,
    max_pixels: int = 4194304,
    **_kwargs,
) -> Image.Image:
    width, height = image.size
    resized_height, resized_width = smart_resize(
        height, width, factor=size_factor, min_pixels=min_pixels, max_pixels=max_pixels,
    )
    return image.resize((resized_width, resized_height))


def preprocess_pixel_values(pixel_values: torch.Tensor, patch_size: int = 16):
    c, h, w = pixel_values.shape
    grid_h = h // patch_size
    grid_w = w // patch_size
    flatten_pixel_values = (
        pixel_values.view(c, grid_h, patch_size, grid_w, patch_size)
        .permute(1, 3, 0, 2, 4)  # [grid_h, grid_w, c, patch_size, patch_size]
        .reshape(grid_h * grid_w, c * patch_size ** 2)
    )
    grid_hw = torch.tensor([[grid_h, grid_w]], device=pixel_values.device)
    return flatten_pixel_values, grid_hw


def get_contrasting_background(image: Image.Image):
    del image
    return (255, 255, 255)


def load_image_native(
    image,
    patch_size: int = 16,
    downsample_ratio: float = 0.5,
    min_pixels: int = 65536,
    max_pixels: int = 4194304,
    upscale: bool = False,
):
    """Load and preprocess an image: RGB convert, smart-resize, normalize, patchify."""
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    if image.mode == "RGBA":
        bg_color = get_contrasting_background(image)
        if bg_color:
            background = Image.new("RGB", image.size, bg_color)
            background.paste(image, mask=image.split()[3])
            image = background.convert("RGB")
        else:
            image = image.convert("RGB")
    else:
        image = image.convert("RGB")

    if upscale:
        image = image.resize((image.width * 2, image.height * 2), Image.BILINEAR)

    transform = T.Compose(
        [
            T.Lambda(lambda img: img.convert("RGB") if img.mode != "RGB" else img),
            T.ToTensor(),
            T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ]
    )
    new_image = dynamic_preprocess_native_resolution(
        image,
        size_factor=int(patch_size // downsample_ratio),
        min_pixels=min_pixels,
        max_pixels=max_pixels,
    )
    pixel_values, grid_hw = preprocess_pixel_values(
        transform(new_image).to(torch.float32), patch_size=patch_size
    )
    return pixel_values, grid_hw


def build_abs_positions_from_grid_hw(grid_hw: torch.Tensor, device=None):
    """Compute patch coordinates (x, y) from grid_hw: (B, 2) tensor of (H, W)."""
    device = grid_hw.device
    B = grid_hw.shape[0]
    H = grid_hw[:, 0]
    W = grid_hw[:, 1]
    N = H * W
    N_total = N.sum()
    patch_to_sample = torch.repeat_interleave(torch.arange(B, device=device), N)
    patch_id_within_image = torch.arange(N_total, device=device)
    patch_id_within_image = patch_id_within_image - torch.cumsum(
        torch.cat([torch.tensor([0], device=device), N[:-1]]), dim=0
    )[patch_to_sample]
    W_per_patch = W[patch_to_sample]
    abs_x = patch_id_within_image % W_per_patch
    abs_y = patch_id_within_image // W_per_patch
    return abs_x, abs_y


def get_thw_indexes(
    input_ids: torch.Tensor,
    grid_hw: torch.Tensor | None,
    img_start_token_id: int,
    img_context_token_id: int,
    downsample_ratio: float,
) -> torch.Tensor:
    """Build M-RoPE indexes [3, T] (temporal, height, width) for a single sequence.

    Mirrors ``NEOChatModel.get_thw_indexes``: temporal index is the cumulative
    position; image-context tokens get 2D grid (h, w) coordinates from
    ``build_abs_positions_from_grid_hw``; non-image tokens get h=w=0.
    """
    device = input_ids.device
    img_start_shift = torch.cat(
        [torch.zeros(1, dtype=torch.long, device=device),
         (input_ids == img_start_token_id).long()],
        dim=0,
    )[:-1]
    not_img_token = (input_ids != img_context_token_id).long()
    t_indexes = (img_start_shift + not_img_token).cumsum(0) - 1
    h_indexes = torch.zeros_like(t_indexes)
    w_indexes = torch.zeros_like(t_indexes)
    if grid_hw is not None:
        selected = (input_ids == img_context_token_id)
        if selected.long().sum() > 0:
            merged_grid_hw = grid_hw // int(1 / downsample_ratio)
            abs_pos_w, abs_pos_h = build_abs_positions_from_grid_hw(
                merged_grid_hw, device=t_indexes.device
            )
            h_indexes[selected] = abs_pos_h.to(t_indexes.device, t_indexes.dtype)
            w_indexes[selected] = abs_pos_w.to(t_indexes.device, t_indexes.dtype)
    return torch.stack([t_indexes, h_indexes, w_indexes], dim=0)


# Empty think block appended to the prompt when think_mode is disabled,
# forcing the model to emit a direct answer instead of a long reasoning
# trace. Exact bytes from official modeling_neo_chat.py:1864.
THINK_SKIP_SUFFIX = b"\x3cthink\x3e\n\n\x3c/think\x3e\n\n".decode("utf-8")
