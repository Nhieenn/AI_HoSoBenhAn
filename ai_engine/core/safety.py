import re
from typing import List, Dict, Any

class SafetyChecker:
    def __init__(self):
        # UC-SAFE-01: Quét các định dạng PHI cơ bản chưa được mask
        self.phi_patterns = [
            (r"\b\d{9,12}\b", "Cảnh báo lọt CMND/CCCD hoặc Số điện thoại"), # Số có 9-12 chữ số
            (r"\b[A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)*\b", "Cảnh báo lọt Tên riêng (viết hoa chữ cái đầu)"),
            (r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", "Cảnh báo lọt Ngày sinh/Ngày tháng")
        ]
        
    def check_phi_leak(self, draft_text: str) -> List[str]:
        """
        Kiểm tra xem bản nháp có vô tình lọt PHI nào chưa được mã hóa thành [NAME_1], [DATE_1] không.
        """
        warnings = []
        # Loại bỏ các placeholder hợp lệ để tránh false positive (VD: [NAME_1])
        clean_text = re.sub(r"\[[A-Z]+_\d+\]", "", draft_text)
        
        for pattern, warning_msg in self.phi_patterns:
            matches = re.finditer(pattern, clean_text)
            for match in matches:
                # Nếu text match là các từ quá thông dụng thì có thể bỏ qua, nhưng tạm thời cảnh báo hết
                text = match.group()
                if len(text) > 3: # Bỏ qua chuỗi quá ngắn
                    warnings.append(f"{warning_msg}: '{text}'")
                    
        return list(set(warnings)) # Unique warnings

    def check_hallucination(self, original_entities: List[Dict[str, Any]], draft_entities: List[Dict[str, Any]]) -> List[str]:
        """
        UC-SAFE-01: Kiểm tra xem bản nháp có sinh ra các thực thể (Thuốc, Bệnh) mà không có trong tài liệu gốc không.
        """
        warnings = []
        
        # Chỉ check 2 loại nhạy cảm nhất là Bệnh (DISEASE) và Thuốc (DRUG)
        sensitive_types = ["DISEASE", "DRUG"]
        
        original_dict = {e["type"]: set() for e in original_entities if e["type"] in sensitive_types}
        for e in original_entities:
            if e["type"] in sensitive_types:
                original_dict[e["type"]].add(e["text"].lower())
                
        for e in draft_entities:
            if e["type"] in sensitive_types:
                # Nếu thực thể trong nháp không có trong gốc -> Bịa thông tin!
                # Note: Có thể so khớp mờ (fuzzy match) thay vì exact match, hiện tại dùng exact match lower
                if e["text"].lower() not in original_dict.get(e["type"], set()):
                    warnings.append(f"Cảnh báo Hallucination: {e['type']} '{e['text']}' có trong nháp nhưng không tìm thấy ở văn bản gốc!")
                    
        return warnings
        
    def check_internal_conflict(self, patient_data: Dict[str, Any], draft_entities: List[Dict[str, Any]]) -> List[str]:
        """
        UC-SAFE-01: Kiểm tra mâu thuẫn nội bộ giữa thông tin bệnh nhân và thực thể sinh ra.
        VD: Bệnh nhân nam nhưng có thông tin thai kỳ.
        """
        warnings = []
        gender = patient_data.get("gender", "").lower()
        age = patient_data.get("age", 0)
        
        # Tập hợp các từ khóa bệnh lý nhạy cảm giới tính/độ tuổi
        female_only_keywords = ["thai", "tử cung", "buồng trứng", "kinh nguyệt", "tiền sản"]
        male_only_keywords = ["tiền liệt tuyến", "tinh hoàn", "dương vật"]
        pediatric_keywords = ["sơ sinh", "trẻ em", "nhi khoa"]
        geriatric_keywords = ["lão khoa", "người già", "mãn kinh"]
        
        for e in draft_entities:
            text = e.get("text", "").lower()
            
            # Kiểm tra mâu thuẫn giới tính
            if gender in ["nam", "male"]:
                if any(kw in text for kw in female_only_keywords):
                    warnings.append(f"Mâu thuẫn nội bộ: Bệnh nhân Nam nhưng có thực thể '{e['text']}'")
            elif gender in ["nữ", "female"]:
                if any(kw in text for kw in male_only_keywords):
                    warnings.append(f"Mâu thuẫn nội bộ: Bệnh nhân Nữ nhưng có thực thể '{e['text']}'")
                    
            # Kiểm tra mâu thuẫn độ tuổi
            if isinstance(age, (int, float)):
                if age > 18 and any(kw in text for kw in pediatric_keywords):
                    warnings.append(f"Mâu thuẫn nội bộ: Bệnh nhân Người lớn ({age} tuổi) nhưng có thực thể '{e['text']}'")
                elif age < 50 and any(kw in text for kw in geriatric_keywords):
                    warnings.append(f"Mâu thuẫn nội bộ: Bệnh nhân chưa đến tuổi lão khoa ({age} tuổi) nhưng có thực thể '{e['text']}'")

        return warnings
        
    def process_safety_check(self, draft_text: str, original_entities: List[Dict[str, Any]], draft_entities: List[Dict[str, Any]], patient_data: Dict[str, Any] = None) -> Dict[str, Any]:
        phi_warnings = self.check_phi_leak(draft_text)
        hallucination_warnings = self.check_hallucination(original_entities, draft_entities)
        
        conflict_warnings = []
        if patient_data:
            conflict_warnings = self.check_internal_conflict(patient_data, draft_entities)
        
        is_safe = len(phi_warnings) == 0 and len(hallucination_warnings) == 0 and len(conflict_warnings) == 0
        
        return {
            "is_safe": is_safe,
            "phi_warnings": phi_warnings,
            "hallucination_warnings": hallucination_warnings,
            "conflict_warnings": conflict_warnings
        }
