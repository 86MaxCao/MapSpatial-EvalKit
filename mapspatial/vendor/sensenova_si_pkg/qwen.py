import os
from typing import Any

from transformers import AutoModelForImageTextToText, AutoProcessor

from models.sensenova_si.model import Model
from models.sensenova_si.utils import to_openai_format


class SenseNovaSIQwenModel(Model):
    def __init__(
        self,
        model_path: str,
        generation_config: dict[str, Any] | str | os.PathLike | None = None,
        device_map: str = "auto",
        dtype: str = "auto",
    ):
        super().__init__(generation_config)
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_path, device_map=device_map, dtype=dtype
        )
        self.processor = AutoProcessor.from_pretrained(model_path)
       
        # 安全检查并赋值
        # Set pad_token_id to eos_token_id to suppress warning
        # import pdb;pdb.set_trace()
        if not hasattr(self.model.config.text_config, 'pad_token_id') or self.model.config.text_config.pad_token_id is None:
            self.model.config.text_config.pad_token_id = self.model.config.text_config.eos_token_id

    def generate(self, question: str, images: list[str] | None = None, **kwargs) -> str:
        generation_config = self.default_generation_config.copy()
        generation_config.update(kwargs)
        # Explicitly set pad_token_id to suppress warning
        if "pad_token_id" not in generation_config:
            # import pdb;pdb.set_trace()
            # generation_config["pad_token_id"] = self.model.config.pad_token_id or self.model.config.eos_token_id
            generation_config["pad_token_id"] = self.model.config.text_config.pad_token_id or self.model.config.text_config.eos_token_id
        openai_style_input = to_openai_format(question, images)
        inputs = self.processor.apply_chat_template(
            openai_style_input,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True,
        ).to(self.model.device)
        generated_ids = self.model.generate(**inputs, **generation_config)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :]
            for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )
        return output_text
