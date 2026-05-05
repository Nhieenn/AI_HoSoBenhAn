import re
from typing import List, Dict, Any, Optional

class ClinicalNER:
    def __init__(self):
        # Mock Ontology Dictionary (UC-NER-03)
        self.ontology_map = {
            "tăng huyết áp": {"code": "I10", "system": "ICD-10"},
            "đái tháo đường": {"code": "E11", "system": "ICD-10"},
            "viêm phổi": {"code": "J18.9", "system": "ICD-10"},
            "sốt": {"code": "R50.9", "system": "ICD-10"},
            "ho": {"code": "R05", "system": "ICD-10"},
            "paracetamol": {"code": "N02BE01", "system": "ATC"},
            "amlodipin": {"code": "C08CA01", "system": "ATC"},
            "glucose": {"code": "14749-6", "system": "LOINC"},
            "hba1c": {"code": "4548-4", "system": "LOINC"},
            "siêu âm tim": {"code": "18748-4", "system": "LOINC"},
            "nội soi dạ dày": {"code": "44247-5", "system": "LOINC"}
        }

        # Keywords for entity extraction (UC-NER-01)
        self.entity_patterns = {
            "DISEASE": [r"\btăng huyết áp\b", r"\bđái tháo đường\b", r"\bviêm phổi\b", r"\bsuy tim\b"],
            "SYMPTOM": [r"\bsốt\b", r"\bho\b", r"\bkhó thở\b", r"\bđau đầu\b", r"\bchóng mặt\b"],
            "DRUG": [r"\bparacetamol\b", r"\bamlodipin\b", r"\baspirin\b", r"\bmetformin\b"],
            "DOSAGE": [r"\b\d+\s*mg\b", r"\b\d+\s*ml\b", r"\b\d+\s*viên\b", r"\b\d+\s*lần/ngày\b", r"\b\d+\s*g\b"],
            "TEST": [r"\bglucose\b", r"\bhba1c\b", r"\bcreatinin\b", r"\bhuyết đồ\b"],
            "PROCEDURE": [r"\bsiêu âm tim\b", r"\bnội soi dạ dày\b", r"\bx-quang phổi\b", r"\bmổ ruột thừa\b"]
        }

        # Negation keywords (UC-NER-02)
        self.negation_keywords = ["không", "chưa", "chẳng", "hiếm khi"]
        self.negation_window = 5  # số token (từ) xét phía trước thực thể

    def _find_negation(self, text: str, entity_start: int) -> bool:
        """Kiểm tra xem thực thể có bị phủ định không dựa trên ngữ cảnh phía trước."""
        prefix = text[:entity_start]
        
        # Chỉ xét trong cùng một câu/mệnh đề (cắt tại dấu phẩy, chấm, chấm phẩy)
        clauses = re.split(r'[,.;\n]', prefix)
        current_clause = clauses[-1] if clauses else ""
        
        # Tokenize mệnh đề hiện tại
        tokens = [t.lower() for t in re.findall(r'\b\w+\b', current_clause)]
        
        # Lấy window các từ gần nhất
        context = tokens[-self.negation_window:]
        
        # Nếu có từ khẳng định như "có", "thấy" ngay trước thực thể mà sau từ phủ định thì hủy phủ định
        # Đơn giản nhất là nếu có từ phủ định trong clause hiện tại
        for word in context:
            if word in self.negation_keywords:
                return True
        return False

    def link_ontology(self, entity_text: str) -> Optional[Dict[str, str]]:
        """Map text với bộ mã chuẩn."""
        normalized = entity_text.lower()
        for key, value in self.ontology_map.items():
            if key in normalized:
                return value
        return None

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Trích xuất danh sách các thực thể từ văn bản."""
        entities = []
        lower_text = text.lower()

        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, lower_text):
                    start, end = match.span()
                    # Lấy text gốc (giữ nguyên hoa thường)
                    entity_text = text[start:end]
                    
                    # UC-NER-02: Phân tích bối cảnh phủ định
                    is_negative = self._find_negation(text, start)
                    
                    # UC-NER-03: Liên kết Ontology
                    ontology = self.link_ontology(entity_text)
                    
                    entities.append({
                        "text": entity_text,
                        "type": entity_type,
                        "start": start,
                        "end": end,
                        "is_negative": is_negative,
                        "ontology": ontology
                    })

        # Sắp xếp các thực thể theo thứ tự xuất hiện trong văn bản
        entities.sort(key=lambda x: x["start"])
        return entities
