import json
import os
import difflib
from typing import Dict, Any, List

class ActiveLearningManager:
    """
    Manages data collection for Active Learning by extracting differences
    between AI-generated drafts and final physician-edited documents.
    """
    def __init__(self, dataset_path: str = "dataset.jsonl"):
        self.dataset_path = dataset_path

    def extract_diff(self, original_text: str, edited_text: str) -> List[Dict[str, Any]]:
        """
        Extracts line-by-line differences to highlight what was changed.
        """
        original_lines = original_text.splitlines()
        edited_lines = edited_text.splitlines()
        
        matcher = difflib.SequenceMatcher(None, original_lines, edited_lines)
        diff_summary = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != 'equal':
                diff_summary.append({
                    "type": tag,
                    "original": original_lines[i1:i2],
                    "edited": edited_lines[j1:j2]
                })
        return diff_summary

    def save_to_dataset(self, instruction: str, input_text: str, output_text: str) -> Dict[str, Any]:
        """
        Saves a training sample to a JSONL file in Alpaca/SFT format.
        """
        sample = {
            "instruction": instruction,
            "input": input_text,
            "output": output_text
        }
        
        try:
            with open(self.dataset_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            return {"status": "success", "sample": sample}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class FineTuningPipeline:
    """
    Mock pipeline for setting up DAPT and SFT (LoRA) configurations.
    """
    def prepare_dapt_data(self, corpus_texts: List[str]) -> Dict[str, Any]:
        """
        Mocks the preparation of a text corpus for Domain-Adaptive Pretraining.
        """
        total_tokens_mock = sum(len(text.split()) for text in corpus_texts)
        return {
            "status": "prepared",
            "type": "DAPT",
            "documents_count": len(corpus_texts),
            "estimated_tokens": total_tokens_mock
        }

    def configure_lora(self, r: int = 16, lora_alpha: int = 32, lora_dropout: float = 0.05) -> Dict[str, Any]:
        """
        Creates a LoRA configuration object (mocked representation of peft LoraConfig).
        """
        return {
            "peft_type": "LORA",
            "task_type": "CAUSAL_LM",
            "r": r,
            "lora_alpha": lora_alpha,
            "lora_dropout": lora_dropout,
            "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"]
        }

    def run_sft_finetuning(self, dataset_path: str, lora_config: Dict[str, Any], model_id: str = "vinai/PhoGPT-7B") -> Dict[str, Any]:
        """
        Mocks the triggering of a fine-tuning job.
        """
        if not os.path.exists(dataset_path):
            return {"status": "error", "message": f"Dataset {dataset_path} not found"}
            
        return {
            "status": "training_started",
            "model_id": model_id,
            "lora_config_applied": lora_config,
            "dataset_used": dataset_path,
            "estimated_time": "mocked_execution"
        }
