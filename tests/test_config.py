"""Test config.py — YAML loading and env var expansion."""

import os
import tempfile
from pathlib import Path

import pytest

from mapspatial.config import load_model_config, BackendConfig


def test_load_yaml_config(tmp_path):
    yaml_content = """
name: TestModel
backend: vllm
model_path: /tmp/test-model
load:
  max_model_len: 4096
  gpu_memory_utilization: 0.5
generate:
  temperature: 0.1
  max_new_tokens: 512
batch_size: 16
backend_args:
  prompt_style: qwen
strategies: [direct, external_draw]
"""
    config_path = tmp_path / "test-model.yaml"
    config_path.write_text(yaml_content)

    cfg = load_model_config(config_path)
    assert cfg.name == "TestModel"
    assert cfg.backend == "vllm"
    assert cfg.model_path == "/tmp/test-model"
    assert cfg.load["max_model_len"] == 4096
    assert cfg.generate["temperature"] == 0.1
    assert cfg.batch_size == 16
    assert cfg.backend_args["prompt_style"] == "qwen"
    assert cfg.strategies == ["direct", "external_draw"]


def test_env_var_expansion(tmp_path, monkeypatch):
    monkeypatch.setenv("CKPT_DIR", "/mnt/checkpoints")
    yaml_content = """
name: TestModel
backend: vllm
model_path: ${CKPT_DIR}/TestModel
"""
    config_path = tmp_path / "test-model.yaml"
    config_path.write_text(yaml_content)

    cfg = load_model_config(config_path)
    assert cfg.model_path == "/mnt/checkpoints/TestModel"


def test_defaults():
    yaml_content = """
name: TestModel
backend: vllm
model_path: /tmp/test-model
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        f.flush()
        cfg = load_model_config(f.name)
        assert cfg.strategies == ["direct"]
        assert cfg.batch_size == 0
        assert cfg.load == {}
        assert cfg.backend_args == {}
