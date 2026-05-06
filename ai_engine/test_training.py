import os
import json
import pytest
from core.training import ActiveLearningManager, FineTuningPipeline

def test_extract_diff():
    manager = ActiveLearningManager()
    original = "Bệnh nhân nam 45 tuổi.\nTiền sử: Khỏe mạnh."
    edited = "Bệnh nhân nam 45 tuổi.\nTiền sử: Tăng huyết áp."
    
    diff = manager.extract_diff(original, edited)
    assert len(diff) == 1
    assert diff[0]["type"] == "replace"
    assert diff[0]["original"] == ["Tiền sử: Khỏe mạnh."]
    assert diff[0]["edited"] == ["Tiền sử: Tăng huyết áp."]

def test_save_to_dataset(tmp_path):
    dataset_file = tmp_path / "test_dataset.jsonl"
    manager = ActiveLearningManager(dataset_path=str(dataset_file))
    
    instruction = "Sửa lỗi nháp lâm sàng"
    input_text = "Bệnh nhân khỏe mạnh"
    output_text = "Bệnh nhân tăng huyết áp"
    
    result = manager.save_to_dataset(instruction, input_text, output_text)
    assert result["status"] == "success"
    
    # Read back
    with open(dataset_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["instruction"] == instruction
        assert data["input"] == input_text
        assert data["output"] == output_text

def test_fine_tuning_pipeline(tmp_path):
    pipeline = FineTuningPipeline()
    
    # Test DAPT preparation
    dapt_result = pipeline.prepare_dapt_data(["Bệnh án 1", "Bệnh án 2"])
    assert dapt_result["status"] == "prepared"
    assert dapt_result["documents_count"] == 2
    
    # Test LoRA config
    lora_config = pipeline.configure_lora(r=8)
    assert lora_config["r"] == 8
    assert lora_config["peft_type"] == "LORA"
    
    # Test SFT Run
    dataset_file = tmp_path / "train.jsonl"
    dataset_file.write_text("dummy")
    
    sft_result = pipeline.run_sft_finetuning(str(dataset_file), lora_config)
    assert sft_result["status"] == "training_started"
    assert sft_result["model_id"] == "vinai/PhoGPT-7B"
    assert sft_result["lora_config_applied"]["r"] == 8
