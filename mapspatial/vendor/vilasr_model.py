"""
ViLaSR model wrapper for multi-turn spatial reasoning with Object Mapper / Path Tracer.

Used by the vilasr backend in inference. Supports multi-image input and answer
extraction from the model's <answer>...</answer> or last assistant turn.
All logic is self-contained.
"""

from __future__ import annotations

import copy
import os
import re
import traceback
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from PIL import Image

# Optional heavy imports
try:
    from vllm import LLM, SamplingParams
    from transformers import AutoProcessor, AutoTokenizer
    from qwen_vl_utils import process_vision_info, fetch_image
    import torch
    from utils.edit_image import (
        merge_bbox_movement,
        parse_bbox_and_movement,
        plot_movement,
        plot_bounding_boxes,
    )
    VILASR_AVAILABLE = True
except ImportError:
    VILASR_AVAILABLE = False
    LLM = None
    SamplingParams = None


# ---------- Constants and prompts copied from the official ViLaSR repo ----------
# (github.com/AntResearchNLP/ViLaSR, eval/infer.py — see vilasr_utils/ORIGIN.md)
MAX_IMAGES = 45

SYSTEM_PROMPT = """### Guidance:
You are a spatial reasoning assistant with access to two powerful visualization tools.
Your task is to break down complex spatial problems and iteratively refine your solution through visualization feedback.

### Available tools:
You can use the following two tools to visualize. After each tool usage, you must wait for and analyze the visualization feedback before proceeding.

1. **Object Mapper**
- Purpose: Identifies and maps key items in the space
- Input format: JSON
```json
[{{
    "index": i, # Image index
    "bbox_2d": [x1, y1, x2, y2],
    "label": "object name/description"
}}]
```
- Output: Generates bounding boxes for visual inspection of the i-th image

2. **Path Tracer**
- Purpose: Plots movement or connections between points
- Input format: JSON
```json
[{{
    "index": i, # Image index
    "start_point_2d": [x1, y1],
    "end_point_2d": [x2, y2],
    "label": "trace_description"
}}]
```
- Output: Generates visual paths for verification of the i-th image

### Required Output Format:
For each reasoning step, you must structure your response as follows:
<think> [Your detailed reasoning process] </think> Action: [Object Mapper/Path Tracer]
```json
[JSON format coordinates]
```

After your reasoning and iteratively refine your solution through visualization feedback, you should arrive at a final answer and structure your response as follows:
<think> [Your detailed reasoning process] </think> Action: Answer
<answer> [Your final answer] </answer>

### Please NOTE the following reasoning techniques:
1. Initial Analysis
   - Break down the spatial problem
   - Plan your approach

2. Iterative Reasoning for Each Step
   - Choose appropriate tool
   - Provide absolute coordinates in JSON format (The top-left corner of the image is (0, 0) and the bottom-right corner is ({width}, {height}))
   - Observe the visualization output
   - Reflect on the visualization:
     * Is the placement/path accurate?
     * Does it align with your reasoning?
     * What adjustments are needed?
   - Backtrack and Adjust:
     * If errors found, backtrack to previous step to modify actions or decisions as needed"""

PROMPT_TEMPLATE = """
### Question:
{question}

Begin your reasoning. After each tool use, critically evaluate the visualization and adjust if needed:
"""


@dataclass
class ProcessData:
    index: int
    response: str
    mm_data: Dict
    bbox_list_origin: Dict
    movement_list_origin: Dict
    finish_reason: str
    is_finished: bool
    grid_size: int


def _process_single_response(data: ProcessData) -> Optional[Dict]:
    """Process a single model response (parse bbox/movement, draw on image)."""
    if data.is_finished is True:
        return {
            "index": data.index,
            "response": data.response,
            "finish_reason": data.finish_reason,
            "is_finished": data.is_finished,
            "processed_image_idx": [None],
        }
    try:
        bbox_list_new, movement_list_new = parse_bbox_and_movement(data.response)
        current_image_index = len(data.mm_data["image"])
        image_index_list, image_list = [], []
        bbox_list, movement_list = data.bbox_list_origin, data.movement_list_origin
        finish_reason = None

        try:
            allindex = {}
            for tmp_bbox_list in bbox_list_new:
                tmp_bbox_list = copy.deepcopy(tmp_bbox_list)
                if tmp_bbox_list["index"] in allindex:
                    if "bbox_list" in allindex[tmp_bbox_list["index"]]:
                        allindex[tmp_bbox_list["index"]]["bbox_list"].append(tmp_bbox_list)
                    else:
                        allindex[tmp_bbox_list["index"]]["bbox_list"] = [tmp_bbox_list]
                else:
                    allindex[tmp_bbox_list["index"]] = {
                        "bbox_list": [tmp_bbox_list],
                        "movement_list": [],
                    }
            for tmp_movement_list in movement_list_new:
                tmp_movement_list = copy.deepcopy(tmp_movement_list)
                if tmp_movement_list["index"] in allindex:
                    if "movement_list" in allindex[tmp_movement_list["index"]]:
                        allindex[tmp_movement_list["index"]]["movement_list"].append(
                            tmp_movement_list
                        )
                    else:
                        allindex[tmp_movement_list["index"]]["movement_list"] = [
                            tmp_movement_list
                        ]
                else:
                    allindex[tmp_movement_list["index"]] = {
                        "bbox_list": [],
                        "movement_list": [tmp_movement_list],
                    }
        except Exception:
            traceback.print_exc()
            finish_reason = "ToolGenError"

        if len(allindex) == 0:
            finish_reason = "ToolError"
        elif len(data.mm_data["image"]) >= MAX_IMAGES + 1:
            finish_reason = "TooManyImages"

        if finish_reason is not None:
            return {
                "index": data.index,
                "processed_image_idx": [None],
                "image": [data.mm_data["image"][0].copy()],
                "response": data.response,
                "finish_reason": finish_reason,
                "bbox_list": bbox_list,
                "movement_list": movement_list,
                "is_finished": True,
            }
        for cnt, tmp_index in enumerate(allindex):
            bbox_list_new = allindex[tmp_index]["bbox_list"]
            movement_list_new = allindex[tmp_index]["movement_list"]
            image_index_new = current_image_index + cnt
            image_index, bbox_list, movement_list = merge_bbox_movement(
                bbox_list_origin=data.bbox_list_origin,
                movement_list_origin=data.movement_list_origin,
                bbox_list_new=bbox_list_new,
                movement_list_new=movement_list_new,
                image_index_new=image_index_new,
            )
            image_index_list.append(image_index)
            if image_index == -1:
                return {
                    "index": data.index,
                    "processed_image_idx": [None],
                    "image": [data.mm_data["image"][0].copy()],
                    "response": data.response,
                    "finish_reason": "ToolError",
                    "bbox_list": bbox_list,
                    "movement_list": movement_list,
                    "is_finished": True,
                }
            image = data.mm_data["image"][image_index].copy()
            assert isinstance(image, Image.Image)
            input_width, input_height = image.size
            plot_bounding_boxes(
                image,
                bbox_list[image_index_new],
                input_height=input_height,
                input_width=input_width,
            )
            plot_movement(
                image,
                movement_list[image_index_new],
                input_height=input_height,
                input_width=input_width,
            )
            image_list.append(image)

        return {
            "index": data.index,
            "processed_image_idx": image_index_list,
            "image": image_list,
            "response": data.response,
            "finish_reason": data.finish_reason,
            "bbox_list": bbox_list,
            "movement_list": movement_list,
            "is_finished": data.is_finished,
        }
    except Exception as e:
        print(f"Error processing response {data.index}: {str(e)}")
        traceback.print_exc()
        return None


def _multi_turn_generate(
    inference_engine,
    tokenizer,
    vllm_inputs=None,
    sampling_params=None,
    use_tqdm=False,
    save_dir=None,
    max_num_steps=10,
):
    """Run multi-turn generation with tool-use loop (Object Mapper / Path Tracer)."""
    sampling_params = copy.deepcopy(sampling_params)
    new_vllm_inputs = []
    for single_vllm_input in vllm_inputs:
        prompt = tokenizer.decode(
            single_vllm_input["prompt_token_ids"], skip_special_tokens=False
        )
        new_vllm_inputs.extend(
            [
                {
                    "prompt": prompt,
                    "multi_modal_data": single_vllm_input["multi_modal_data"],
                    "grid_size": single_vllm_input["grid_size"],
                }
                for _ in range(sampling_params.n)
            ]
        )

    sampling_params.n = 1
    sampling_params.detokenize = True
    samples_info = []
    for index, item in enumerate(new_vllm_inputs):
        processed_image = [
            fetch_image({"image": origin_image})
            for origin_image in item["multi_modal_data"]["image"]
        ]
        sample_info = {
            "prompt": item["prompt"],
            "sequence": item["prompt"],
            "multi_modal_data": {"image": processed_image},
            "response": "",
            "stop": False,
            "finish_reason": None,
            "processed_image_idx": [],
            "index": index,
            "mask_info": [],
            "execution_pass": 0,
            "bbox_list": {img_idx: [] for img_idx in range(len(processed_image))},
            "movement_list": {img_idx: [] for img_idx in range(len(processed_image))},
            "grid_size": item["grid_size"],
        }
        samples_info.append(sample_info)

    intermediate_prompt = (
        "The index of the given image is {current_image_idx} (width: {width}, "
        "height: {height}). Continue your reasoning. After each tool use, "
        "critically evaluate the visualization and adjust if needed:"
    )
    final_prompt = (
        "The index of the given image is {current_image_idx} (width: {width}, "
        "height: {height}). Then, you can not invoke the Object Mapper or Path Tracer "
        "tool. Please answer the initial question and structure your response as required:"
    )
    intermediate_template = """<|im_end|>
<|im_start|>user
{pad}
{prompt}
<|im_end|>
<|im_start|>assistant
"""

    num_llm_calls_available = max_num_steps - 1
    while num_llm_calls_available >= 0:
        num_llm_calls_available -= 1
        input_prompts, multi_modal_data, indices = [], [], []
        for index, info in enumerate(samples_info):
            if not info["stop"] and len(info["multi_modal_data"]["image"]) <= MAX_IMAGES:
                input_prompts.append(info["sequence"])
                multi_modal_data.append(info["multi_modal_data"])
                indices.append(info["index"])

        if not indices:
            break

        # Build vLLM requests with length guard: skip items whose estimated
        # input (text tokens + ~1000/image) would exceed max_model_len margin.
        vllm_requests = []
        kept_indices = []
        for p_text, mm_data, idx in zip(input_prompts, multi_modal_data, indices):
            token_ids = tokenizer.encode(p_text, add_special_tokens=False)
            n_images = len(mm_data.get("image", []))
            est_len = len(token_ids) + n_images * 1000
            if est_len > 30000:  # leave margin below max_model_len=32768
                samples_info[idx]["stop"] = True
                samples_info[idx]["finish_reason"] = "length"
                continue
            vllm_requests.append({
                "prompt_token_ids": token_ids,
                "multi_modal_data": mm_data,
            })
            kept_indices.append(idx)
        indices = kept_indices

        if not vllm_requests:
            continue

        # Generate with error guard — engine crash shouldn't hang the run
        try:
            outputs = inference_engine.generate(
                prompts=vllm_requests,
                sampling_params=sampling_params,
                use_tqdm=use_tqdm,
            )
        except Exception as e:
            for idx in indices:
                samples_info[idx]["stop"] = True
                samples_info[idx]["finish_reason"] = "error"
                samples_info[idx]["response"] += f"\n[engine error: {e}]"
            break

        sorted_outputs = sorted(outputs, key=lambda output: int(output.request_id))
        responses = [x.outputs[0].text for x in sorted_outputs]
        finish_reason = [x.outputs[0].finish_reason for x in sorted_outputs]
        stop_reason = [x.outputs[0].stop_reason for x in sorted_outputs]

        if num_llm_calls_available == -1:
            for i, idx in enumerate(indices):
                samples_info[idx]["response"] += responses[i]
                samples_info[idx]["sequence"] += responses[i]
                samples_info[idx]["stop"] = True
                samples_info[idx]["finish_reason"] = finish_reason[i]
            break

        def _is_finished(fr, sr, resp):
            if fr == "stop" and sr is None and "<answer>" in resp and "</answer>" in resp:
                return True
            if fr == "length":
                return True
            if fr == "rule":
                return True
            return False

        is_finished = [
            _is_finished(finish_reason[i], stop_reason[i], responses[i])
            for i in range(len(finish_reason))
        ]
        if all(is_finished):
            for i, idx in enumerate(indices):
                samples_info[idx]["response"] += responses[i]
                samples_info[idx]["sequence"] += responses[i]
                samples_info[idx]["stop"] = True
                samples_info[idx]["finish_reason"] = finish_reason[i]
            break

        process_data_list = [
            ProcessData(
                index=idx,
                response=responses[i],
                mm_data=samples_info[idx]["multi_modal_data"],
                bbox_list_origin=samples_info[idx]["bbox_list"],
                movement_list_origin=samples_info[idx]["movement_list"],
                finish_reason=finish_reason[i],
                is_finished=is_finished[i],
                grid_size=samples_info[idx]["grid_size"],
            )
            for i, idx in enumerate(indices)
        ]
        with ThreadPoolExecutor(
            max_workers=max(min(len(indices), os.cpu_count() // 2, 64), 1)
        ) as executor:
            results = list(executor.map(_process_single_response, process_data_list))

        for result in results:
            if result is not None:
                index = result["index"]
                samples_info[index]["response"] += result["response"]
                samples_info[index]["stop"] = result["is_finished"]
                samples_info[index]["finish_reason"] = result["finish_reason"]
                samples_info[index]["processed_image_idx"].extend(
                    result["processed_image_idx"]
                )
                if result["is_finished"] is False:
                    current_image_count = len(samples_info[index]["multi_modal_data"]["image"])
                    if len(result["image"]) > 1:
                        current_image_idx = current_image_count + 1
                        pad_prompt = ""
                        for tmp_image_idx, tmp_image in enumerate(result["image"]):
                            width, height = fetch_image({"image": tmp_image}).size
                            if current_image_count + tmp_image_idx + 1 >= MAX_IMAGES:
                                pad_prompt += (
                                    "<|vision_start|><|image_pad|><|vision_end|>"
                                    + final_prompt.format(
                                        current_image_idx=current_image_idx + tmp_image_idx,
                                        width=width,
                                        height=height,
                                    )
                                )
                                samples_info[index]["multi_modal_data"]["image"].append(
                                    tmp_image
                                )
                                break
                            else:
                                if tmp_image_idx <= len(result["image"]) - 2:
                                    pad_prompt += (
                                        "<|vision_start|><|image_pad|><|vision_end|>"
                                        "The index of the given image is "
                                        f"{current_image_idx + tmp_image_idx} "
                                        f"(width: {width}, height: {height}).\n"
                                    )
                                else:
                                    if num_llm_calls_available > 0:
                                        pad_prompt += (
                                            "<|vision_start|><|image_pad|><|vision_end|>"
                                            + intermediate_prompt.format(
                                                current_image_idx=current_image_idx
                                                + tmp_image_idx,
                                                width=width,
                                                height=height,
                                            )
                                        )
                                    else:
                                        pad_prompt += (
                                            "<|vision_start|><|image_pad|><|vision_end|>"
                                            + final_prompt.format(
                                                current_image_idx=current_image_idx
                                                + tmp_image_idx,
                                                width=width,
                                                height=height,
                                            )
                                        )
                                samples_info[index]["multi_modal_data"]["image"].append(
                                    tmp_image
                                )
                        samples_info[index]["sequence"] += result["response"] + (
                            intermediate_template.format(prompt="", pad=pad_prompt)
                        )
                    else:
                        current_image_idx = current_image_count + 1
                        width, height = fetch_image(
                            {"image": result["image"][0]}
                        ).size
                        if current_image_count + 1 >= MAX_IMAGES:
                            prompt = final_prompt.format(
                                current_image_idx=current_image_idx,
                                width=width,
                                height=height,
                            )
                        else:
                            prompt = (
                                intermediate_prompt
                                if num_llm_calls_available > 0
                                else final_prompt
                            ).format(
                                current_image_idx=current_image_idx,
                                width=width,
                                height=height,
                            )
                        samples_info[index]["sequence"] += result["response"] + (
                            intermediate_template.format(
                                prompt=prompt,
                                pad="<|vision_start|><|image_pad|><|vision_end|>",
                            )
                        )
                        samples_info[index]["multi_modal_data"]["image"].append(
                            result["image"][0]
                        )
                    samples_info[index]["bbox_list"] = result["bbox_list"]
                    samples_info[index]["movement_list"] = result["movement_list"]
                else:
                    samples_info[index]["sequence"] += result["response"]

    for i in range(len(samples_info)):
        if samples_info[i]["finish_reason"] != "length":
            samples_info[i]["sequence"] += tokenizer.eos_token

    return [sample["sequence"] for sample in samples_info]


# ---------- Public API ----------
def extract_answer_from_vilasr_sequence(sequence: str) -> str:
    """Extract final answer text from ViLaSR multi-turn sequence for benchmark scoring."""
    # Find all assistant blocks, then filter out empty ones from the end
    # This handles the case where intermediate_template adds an empty assistant at the end
    assistants = re.findall(
        r"<\|im_start\|>assistant\n(.*?)(?=<\|im_end\|>|<\|im_start\|>|\Z)",
        sequence,
        re.DOTALL,
    )
    
    content = None
    for a in reversed(assistants):  # Search from the end
        stripped = a.strip()
        if stripped:  # Find first non-empty assistant block
            content = stripped
            break
    
    if content is None:
        return sequence
    
    answer_match = re.search(
        r"<answer>\s*(.*?)\s*</answer>", content, re.DOTALL | re.IGNORECASE
    )
    if answer_match:
        return answer_match.group(1).strip()
    return content


class VilasrModel:
    """ViLaSR model: vLLM + processor + tokenizer for multi-turn spatial reasoning."""

    def __init__(
        self,
        model_id: str,
        temperature: float = 0.2,
        max_tokens: int = 16384,
        top_p: float = 0.9,
        gpu_memory_utilization: float = 0.85,
    ):
        if not VILASR_AVAILABLE:
            raise ImportError(
                "vllm, qwen_vl_utils, torch, utils.edit_image required for ViLaSR"
            )
        self.model_id = model_id
        self._model_name = model_id.rstrip("/").split("/")[-1]
        self.llm = LLM(
            model=model_id,
            dtype="bfloat16",
            tensor_parallel_size=torch.cuda.device_count(),
            limit_mm_per_prompt={"image": 62, "video": 10},
            gpu_memory_utilization=gpu_memory_utilization,
            max_model_len=32768,
            enable_prefix_caching=True,
            enforce_eager=True,
        )
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.tokenizer.padding_side = "left"
        self.processor.tokenizer = self.tokenizer
        self.sampling_params = SamplingParams(
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stop_token_ids=[],
        )

    @property
    def model_name(self) -> str:
        return self._model_name

    def run(
        self,
        image_paths: List[Union[Path, str]],
        prompt: str,
        max_num_steps: int = 10,
        timeout: Optional[int] = None,
    ) -> str:
        """
        Run ViLaSR multi-turn inference.

        Args:
            image_paths: List of image paths or URLs.
            prompt: Question/prompt text.
            max_num_steps: Max multi-turn reasoning steps.
            timeout: Optional timeout for URL image download.

        Returns:
            Extracted answer text (from <answer> or last assistant turn).
        """
        image_paths_str = [str(p) if isinstance(p, Path) else p for p in image_paths]
        if not image_paths_str:
            return ""

        first_path = image_paths_str[0]
        if isinstance(first_path, str) and first_path.startswith(("http://", "https://")):
            try:
                from utils.file_io import download_image_from_url
                import tempfile
                img = download_image_from_url(
                    first_path, timeout=timeout or 30, convert_to_rgb=True
                )
                if img is None:
                    raise ValueError(f"Failed to download image from URL: {first_path}")
                tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                img.save(tmp.name)
                tmp.close()
                first_path = tmp.name
                image_paths_str[0] = first_path
            except Exception as e:
                raise RuntimeError(f"Error downloading image from {first_path}: {e}")
        first_img = fetch_image({"image": first_path})
        width, height = first_img.size

        user_content: List[Dict[str, Any]] = []
        for i, path in enumerate(image_paths_str):
            user_content.append({"type": "image", "image": path})
            user_content.append({
                "type": "text",
                "text": f"The index of the given image is {i + 1} (width: {width}, height: {height}).\n",
            })
        user_content.append({
            "type": "text",
            "text": PROMPT_TEMPLATE.format(question=prompt),
        })
        msg = [
            {"role": "system", "content": SYSTEM_PROMPT.format(width=width, height=height)},
            {"role": "user", "content": user_content},
        ]

        prompt_str = self.processor.apply_chat_template(
            msg, tokenize=False, add_generation_prompt=True
        )
        prompt_token_ids = self.tokenizer.encode(prompt_str, add_special_tokens=False)
        image_inputs, video_inputs, video_kwargs = process_vision_info(
            [msg], return_video_kwargs=True
        )
        multi_modal_data = {"image": list(image_inputs)} if image_inputs else {"image": []}
        vllm_inputs = [{
            "prompt": prompt_str,
            "prompt_token_ids": prompt_token_ids,
            "multi_modal_data": multi_modal_data,
            "grid_size": None,
        }]

        batch_sequences = _multi_turn_generate(
            self.llm,
            self.tokenizer,
            vllm_inputs=vllm_inputs,
            sampling_params=self.sampling_params,
            save_dir=None,
            max_num_steps=max_num_steps,
        )
        sequence = batch_sequences[0] if batch_sequences else ""
        # import pdb; pdb.set_trace()
        return extract_answer_from_vilasr_sequence(sequence)


__all__ = [
    "VilasrModel",
    "extract_answer_from_vilasr_sequence",
    "VILASR_AVAILABLE",
    "SYSTEM_PROMPT",
    "PROMPT_TEMPLATE",
]
