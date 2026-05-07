from typing import Dict, List, Any

class ClinicalGenerator:
    def __init__(self, rag_engine=None):
        self.rag_engine = rag_engine
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
        extracted_symptoms = self._extract_entities_by_type(entities, "SYMPTOM")
        symptoms = ", ".join(extracted_symptoms)
        
        # Lấy thông tin bệnh lý và thuốc trước
        diseases = ", ".join(self._extract_entities_by_type(entities, "DISEASE")) or "Không ghi nhận"
        drugs = ", ".join(self._extract_entities_by_type(entities, "DRUG")) or "Không ghi nhận"
        tests = ", ".join(self._extract_entities_by_type(entities, "TEST")) or "Không có"
        treatments = ", ".join(self._extract_entities_by_type(entities, "PROCEDURE")) or "Điều trị nội khoa"

        # CỨU CÁNH: Nếu không có thực thể, tìm kiếm từ khóa trực tiếp từ văn bản thô
        raw_reason = patient_data.get("reason", "").lower()
        if not symptoms or symptoms == "Không ghi nhận":
            if "đau" in raw_reason:
                symptoms = patient_data.get("reason", "Không ghi nhận")
            else:
                symptoms = patient_data.get("reason", "Không ghi nhận")

        # Cải thiện phần Chẩn đoán: Sử dụng RAG (Truy xuất kiến thức)
        diagnosis = patient_data.get("diagnosis", "")
        if not diagnosis:
            low_symptoms = (symptoms + " " + raw_reason).lower()
            
            # ƯU TIÊN 1: Tra cứu từ RAG (Module 5)
            rag_context = ""
            if self.rag_engine:
                # Dịch thuật ngữ đời thường sang chuẩn y khoa (chuẩn hóa ngữ nghĩa)
                synonym_map = {
                    "hầm hập": "sốt",
                    "nóng ran": "sốt",
                    "rột rột": "lạo xạo",
                    "lục cục": "lạo xạo",
                    "khúc khắc": "ho",
                    "quặn thắt": "đau thắt",
                    "thở rít": "khò khè"
                }
                
                query_symptoms = symptoms.lower()
                for slang, formal in synonym_map.items():
                    query_symptoms = query_symptoms.replace(slang, formal)
                    
                # LỖI TAM SAO THẤT BẢN: PhoBERT có thể nhận diện thiếu triệu chứng (VD sót "mắt lồi", "tay run").
                # Do đó, bắt buộc phải dùng NGUYÊN VĂN CÂU NÓI CỦA BỆNH NHÂN để hỏi RAG!
                raw_reason_query = patient_data.get("reason", "").lower()
                for slang, formal in synonym_map.items():
                    raw_reason_query = raw_reason_query.replace(slang, formal)
                    
                query = raw_reason_query if len(raw_reason_query) > 5 else query_symptoms
                results = self.rag_engine.retrieve_context(query, top_k=3)
                rag_context = results["combined_context"] if results["citations"] else ""
                
                diagnoses_list = []
                evidence_map = {}
                unused_symptoms = list(extracted_symptoms)
                
                def add_evidence(diag: str, keywords: List[str]):
                    matched = [s for s in unused_symptoms if any(k in s.lower() for k in keywords)]
                    if matched:
                        evidence_map[diag] = matched
                        for m in matched:
                            unused_symptoms.remove(m)

                # Đánh giá độc lập từng hệ cơ quan (Multi-morbidity)
                if "Sốt xuất huyết" in rag_context and ("xuất huyết" in low_symptoms or "phát ban" in low_symptoms or "hốc mắt" in low_symptoms):
                    diagnoses_list.append("Sốt xuất huyết Dengue")
                    add_evidence("Sốt xuất huyết Dengue", ["xuất huyết", "phát ban", "hốc mắt", "sốt"])
                    
                elif "sốt rét" in rag_context.lower() and ("rét" in low_symptoms or "vã mồ hôi" in low_symptoms):
                    diagnoses_list.append("Sốt rét")
                    add_evidence("Sốt rét", ["rét", "mồ hôi", "sốt"])
                    
                elif "sốt" in low_symptoms or "đau đầu" in low_symptoms:
                    diagnoses_list.append("Hội chứng nhiễm siêu vi")
                    add_evidence("Hội chứng nhiễm siêu vi", ["sốt", "đau đầu", "mệt"])
                    
                if "Suy tim" in rag_context and "phù" in low_symptoms and ("khó thở" in low_symptoms or "tĩnh mạch" in low_symptoms):
                    diagnoses_list.append("Theo dõi Suy tim")
                    add_evidence("Theo dõi Suy tim", ["phù", "khó thở", "tĩnh mạch", "mệt"])
                    
                if "đau ngực" in low_symptoms or "bóp nghẹt" in low_symptoms or "quặn thắt" in low_symptoms or "đau thắt ngực" in low_symptoms:
                    diagnoses_list.append("Theo dõi Nhồi máu cơ tim cấp / Cơn đau thắt ngực")
                    add_evidence("Theo dõi Nhồi máu cơ tim cấp / Cơn đau thắt ngực", ["đau ngực", "bóp nghẹt", "quặn thắt", "vã mồ hôi", "xương ức"])
                    
                if "thủy tinh thể" in rag_context and "mờ" in low_symptoms:
                    diagnoses_list.append("Đục thủy tinh thể")
                    add_evidence("Đục thủy tinh thể", ["mờ", "mắt"])
                    
                if "Viêm tụy" in rag_context and "đau bụng" in low_symptoms:
                    diagnoses_list.append("Theo dõi Viêm tụy cấp")
                    add_evidence("Theo dõi Viêm tụy cấp", ["đau bụng", "nôn", "sốt"])
                    
                if "thượng vị" in low_symptoms or "ợ chua" in low_symptoms or "chướng bụng" in low_symptoms or "dạ dày" in low_symptoms:
                    diagnoses_list.append("Trào ngược / Viêm loét dạ dày tá tràng")
                    add_evidence("Trào ngược / Viêm loét dạ dày tá tràng", ["thượng vị", "ợ", "chướng", "dạ dày"])
                    
                if "lạo xạo" in low_symptoms or "cứng khớp" in low_symptoms or "đau lan" in low_symptoms or "thoái hóa" in low_symptoms:
                    diagnoses_list.append("Thoái hóa khớp")
                    add_evidence("Thoái hóa khớp", ["lạo xạo", "cứng", "lan", "đau", "thoái hóa"])
                    
                if "Thoát vị đĩa đệm" in rag_context and "tê bì" in low_symptoms:
                    diagnoses_list.append("Theo dõi Thoát vị đĩa đệm cột sống")
                    add_evidence("Theo dõi Thoát vị đĩa đệm cột sống", ["tê bì", "đau lưng", "lan"])
                    
                if "run" in low_symptoms and ("chậm chạp" in low_symptoms or "nghỉ ngơi" in low_symptoms):
                    diagnoses_list.append("Bệnh Parkinson")
                    add_evidence("Bệnh Parkinson", ["run", "chậm chạp", "nghỉ ngơi", "cứng"])
                    
                # Lấy thêm bệnh từ Top 1 RAG nếu chưa có trong danh sách
                if results["citations"] and results["citations"][0]["score"] > 0.6:
                    meta = results["citations"][0].get("metadata", {})
                    suggested_name = meta.get("disease", "")
                    
                    if not suggested_name:
                        suggested_name = results["citations"][0]["text_snippet"].split(":")[0].strip()
                        if len(suggested_name) > 40:
                            suggested_name = "Bệnh lý theo RAG gợi ý"
                        
                    is_duplicate = any(word.lower() in suggested_name.lower() for word in ["sốt xuất huyết", "sốt rét", "siêu vi", "suy tim", "nhồi máu", "đau thắt", "thủy tinh thể", "viêm tụy", "dạ dày", "thoái hóa khớp", "thoát vị", "mồ hôi"])
                    if not is_duplicate:
                        diagnoses_list.append(suggested_name)
                        # Add remaining symptoms to this RAG diagnosis
                        if unused_symptoms:
                            evidence_map[suggested_name] = list(unused_symptoms)
                            unused_symptoms.clear()

                # Tổng hợp kết quả đa bệnh lý
                if diagnoses_list:
                    diagnosis = " + ".join(list(set(diagnoses_list))) + " [Đa bệnh lý - Gợi ý AI]"
                else:
                    if diseases != "Không ghi nhận":
                        diagnosis = f"{diseases} [UNCERTAIN: Cần bác sĩ xác nhận lại]"
                    else:
                        diagnosis = "[CẢNH BÁO: CHƯA RÕ CHẨN ĐOÁN - YÊU CẦU BỔ SUNG]"

                if unused_symptoms:
                    evidence_map["Các triệu chứng khác (Chưa rõ bệnh)"] = unused_symptoms

        else:
            # Fallback if diagnosis was already provided
            evidence_map = {"Các triệu chứng khác (Chưa rõ bệnh)": extracted_symptoms}

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
        return filled.strip(), evidence_map

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
        return filled.strip(), {"Bằng chứng CĐHA": self._extract_entities_by_type(entities, "SYMPTOM")}
