"""Input preparation for Spatial-MLLM.

Vendored from Spatial-MLLM official repo (src/inference.py:prepare_spatial_mllm_inputs).
Builds VGGT-compatible image_tchw / video_tchw tensors from the outputs of
qwen_vl_utils.process_vision_info and merges them into the processor batch.
"""

from __future__ import annotations

import numpy as np
import torch
from PIL import Image


def prepare_spatial_mllm_inputs(batch, video_inputs, image_inputs):
    """
    Prepare inputs for Spatial-MLLM model.

    batch: dict returned by the processor
    video_inputs / image_inputs: returned by qwen_vl_utils.process_vision_info

    video_inputs: List[torch.Tensor[Int]] | List[torch.Tensor[Float]] | List[List[PIL.Image]]
    image_inputs: List[PIL.Image]
    """
    video_tchw = []
    image_tchw = []

    if video_inputs:
        for video_input in video_inputs:
            if isinstance(video_input, torch.Tensor):
                video_input = video_input.float() / 255.0  # Normalize to [0, 1]
            elif isinstance(video_input, list) and all(isinstance(img, Image.Image) for img in video_input):
                video_input = torch.stack(
                    [torch.tensor(np.array(img)).permute(2, 0, 1) for img in video_input]
                ).float() / 255.0
            else:
                raise ValueError("Unsupported video input format.")
            video_tchw.append(video_input)

    if image_inputs:
        for image_input in image_inputs:
            if isinstance(image_input, Image.Image):
                image_input = torch.tensor(np.array(image_input)).permute(2, 0, 1).float() / 255.0
            else:
                raise ValueError("Unsupported image input format.")
            image_tchw.append(image_input)

    # When only images are provided (no video), spatial encoder expects [T, C, H, W].
    # Treat each image as 1-frame video: [C, H, W] -> [1, C, H, W]. Supports single and multi image.
    if not video_tchw and image_tchw:
        video_tchw = [img.unsqueeze(0) for img in image_tchw]

    batch.update({
        "video_tchw": video_tchw if video_tchw else None,
        "image_tchw": image_tchw if image_tchw else None,
    })

    return batch
