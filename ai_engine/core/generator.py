from typing import Dict, List, Any

class ClinicalGenerator:
    def __init__(self):
        # UC-GEN-05: Quản lý Template theo khoa
        self.templates = {
            "discharge_summary": {
                "General": """
BỆNH VIỆN ĐA KHOA
TÓM TẮT HỒ SƠ BỆNH ÁN

1. HÀNH CHÍNH
Họ và tên: {name}
Tuổi: {age}
Giới tính: {gender}

2. TÓM TẮT BỆNH ÁN
Bệnh nhân vào viện với lý do: {reason}
- Triệu chứng: {symptoms}
- Bệnh lý đã ghi nhận: {diseases}
- Thuốc đã dùng: {drugs}

3. CHẨN ĐOÁN XUẤT VIỆN
{diagnosis}

4. PHƯƠNG PHÁP ĐIỀU TRỊ
{treatments}

5. LỜI KHUYÊN
{advices}
""",
                "Cardiology": """
BỆNH VIỆN ĐA KHOA - KHOA TIM MẠCH
TÓM TẮT HỒ SƠ BỆNH ÁN TIM MẠCH

1. HÀNH CHÍNH
Họ và tên: {name}
Tuổi: {age}

2. DIỄN BIẾN LÂM SÀNG
- Triệu chứng tim mạch: {symptoms}
- Kết quả xét nghiệm/siêu âm: {tests}
- Bệnh nền: {diseases}

3. CHẨN ĐOÁN
{diagnosis}

4. ĐIỀU TRỊ
{drugs}
"""
            },
            "radiology_report": {
                "XRay": """
KẾT QUẢ CHẨN ĐOÁN HÌNH ẢNH

- Kỹ thuật: {procedure}
- Mô tả tổn thương: {findings}
- Kết luận: {conclusion}
"""
            }
        }

    def _extract_entities_by_type(self, entities: List[Dict], entity_type: str) -> List[str]:
        # Chỉ lấy những entity KHÔNG bị phủ định
        return [e["text"] for e in entities if e.get("type") == entity_type and not e.get("is_negative", False)]

    def generate_discharge_summary(self, patient_data: Dict[str, Any], entities: List[Dict], department: str = "General") -> str:
        """Sinh nháp Tóm tắt xuất viện."""
        # Lấy template theo khoa
        template = self.templates.get("discharge_summary", {}).get(department, self.templates["discharge_summary"]["General"])
        
        # UC-GEN-03: Auto-fill từ các thực thể đã trích xuất
        symptoms = ", ".join(self._extract_entities_by_type(entities, "SYMPTOM")) or "Không ghi nhận"
        diseases = ", ".join(self._extract_entities_by_type(entities, "DISEASE")) or "Không ghi nhận"
        drugs = ", ".join(self._extract_entities_by_type(entities, "DRUG")) or "Không ghi nhận"
        tests = ", ".join(self._extract_entities_by_type(entities, "TEST")) or "Không có"
        treatments = ", ".join(self._extract_entities_by_type(entities, "PROCEDURE")) or "Điều trị nội khoa"

        # UC-GEN-04: Xử lý thông tin mơ hồ (Uncertainty)
        diagnosis = patient_data.get("diagnosis", "")
        if not diagnosis:
            if diseases != "Không ghi nhận":
                diagnosis = f"{diseases} [UNCERTAIN: Cần bác sĩ xác nhận lại]"
            else:
                diagnosis = "[CẢNH BÁO: CHƯA RÕ CHẨN ĐOÁN - YÊU CẦU BỔ SUNG]"

        # Điền dữ liệu vào template
        filled = template.format(
            name=patient_data.get("name", "[CHƯA CÓ THÔNG TIN]"),
            age=patient_data.get("age", "[CHƯA CÓ THÔNG TIN]"),
            gender=patient_data.get("gender", "[CHƯA CÓ THÔNG TIN]"),
            reason=patient_data.get("reason", "Khám bệnh"),
            symptoms=symptoms,
            diseases=diseases,
            drugs=drugs,
            tests=tests,
            diagnosis=diagnosis,
            treatments=treatments,
            advices=patient_data.get("advices", "Tái khám sau 1 tuần hoặc khi có dấu hiệu bất thường.")
        )
        return filled.strip()

    def generate_radiology_report(self, raw_findings: str, entities: List[Dict], department: str = "XRay") -> str:
        """Sinh nháp Báo cáo Chẩn đoán hình ảnh."""
        template = self.templates.get("radiology_report", {}).get(department, self.templates["radiology_report"]["XRay"])
        
        procedure = ", ".join(self._extract_entities_by_type(entities, "PROCEDURE")) or "Chụp X-Quang / Siêu âm"
        
        # UC-GEN-04: Uncertainty cho phần kết luận nếu mô tả thô không rõ ràng
        conclusion = "[UNCERTAIN: Cần bác sĩ CĐHA kết luận trực tiếp]"
        if "kết luận:" in raw_findings.lower():
            try:
                # Cắt chuỗi sau chữ "kết luận:"
                parts = raw_findings.lower().split("kết luận:")
                if len(parts) > 1 and parts[1].strip():
                    conclusion = parts[1].strip().capitalize()
            except Exception:
                pass

        filled = template.format(
            procedure=procedure,
            findings=raw_findings.replace("Kết luận:", "").strip(),
            conclusion=conclusion
        )
        return filled.strip()
