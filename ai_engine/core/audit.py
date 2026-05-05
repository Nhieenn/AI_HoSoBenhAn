import time
import uuid
import json
from typing import Dict, Any, List

class AuditLogger:
    """UC-AUD-01: Ghi log hoạt động chi tiết"""
    def __init__(self):
        self._logs = []

    def log_action(self, user_id: str, action: str, target_id: str, details: Dict[str, Any] = None):
        log_entry = {
            "log_id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "user_id": user_id,
            "action": action,
            "target_id": target_id,
            "details": details or {}
        }
        self._logs.append(log_entry)
        return log_entry

    def get_logs(self):
        # Đảm bảo tính immutable ở tầng ứng dụng bằng cách trả về bản copy
        return [dict(log) for log in self._logs]

class RBACManager:
    """UC-AUD-02: Phân quyền vai trò (RBAC)"""
    def __init__(self):
        self.roles_permissions = {
            "ADMIN": ["view_all", "manage_users", "manage_templates", "view_audit"],
            "DOCTOR": ["create_draft", "edit_draft", "approve_draft", "reject_draft", "view_own_drafts"],
            "NURSE": ["create_draft", "view_own_drafts"],
            "RESEARCHER": ["view_anonymized_data", "view_transparency_reports"]
        }

    def check_permission(self, role: str, action: str) -> bool:
        role = role.upper()
        if role not in self.roles_permissions:
            return False
        return action in self.roles_permissions[role]

class DataIsolator:
    """UC-AUD-03: Cô lập dữ liệu (On-premise)"""
    @staticmethod
    def verify_no_external_request(url: str) -> bool:
        # Mock logic đảm bảo không gọi request ra internet công cộng
        # Chỉ cho phép localhost, 127.0.0.1 hoặc dải IP nội bộ bệnh viện (VD: 192.168.x.x, 10.x.x.x)
        allowed_domains = ["localhost", "127.0.0.1", "192.168.", "10."]
        for domain in allowed_domains:
            if domain in url:
                return True
        return False

class TransparencyReporter:
    """UC-AUD-04: Báo cáo minh bạch theo chuẩn quốc tế"""
    @staticmethod
    def generate_model_card() -> Dict[str, Any]:
        return {
            "model_name": "ViMedAI-Clinical-Generative",
            "version": "1.0.0",
            "intended_use": "Hỗ trợ soạn thảo bệnh án, chẩn đoán hình ảnh (Assisted Mode). Không dùng để thay thế quyết định y khoa.",
            "training_data": "MIMIC-IV, VinDr-CXR (đã ẩn danh), dữ liệu nội bộ Bệnh viện (đã ẩn danh).",
            "evaluation_metrics": {
                "phi_leak_rate": "0.0%",
                "hallucination_rate": "< 1.5%"
            },
            "limitations": "Mô hình có thể sinh thông tin thiếu chính xác đối với các ca bệnh siêu hiếm."
        }

    @staticmethod
    def generate_data_sheet() -> Dict[str, Any]:
        return {
            "dataset_name": "ViMedAI-Corpus-v1",
            "composition": "500,000 báo cáo X-Quang, 200,000 tóm tắt xuất viện.",
            "preprocessing": "Masking 8 loại PHI (Tên, SDT, CMND, Địa chỉ, ...).",
            "collection_process": "Trích xuất từ HIS nội bộ và MIMIC-IV."
        }
        
    @staticmethod
    def verify_clinical_protocol(protocol_details: Dict[str, Any]) -> Dict[str, Any]:
        # Kiểm tra sơ bộ SPIRIT-AI checklist
        required_fields = ["ai_intervention_description", "human_ai_interaction", "error_analysis_plan"]
        missing = [f for f in required_fields if f not in protocol_details]
        
        return {
            "compliant": len(missing) == 0,
            "missing_fields": missing
        }
