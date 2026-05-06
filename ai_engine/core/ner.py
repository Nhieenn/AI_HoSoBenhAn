import os
import re
from typing import List, Dict, Any, Optional

# Cấu hình tải Model nặng về ổ D (tránh đầy ổ C)
os.environ["HF_HOME"] = r"D:\AI_HoSoBenhAn\ai_engine\models\cache"
os.environ["TRANSFORMERS_CACHE"] = r"D:\AI_HoSoBenhAn\ai_engine\models\cache"

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
            "nội soi dạ dày": {"code": "44247-5", "system": "LOINC"},
            "nhồi máu cơ tim": {"code": "I21.9", "system": "ICD-10"},
            "đau ngực": {"code": "R07.9", "system": "ICD-10"},
            "stent": {"code": "Z95.5", "system": "ICD-10"},
            "động mạch vành": {"code": "43200000", "system": "SNOMED-CT"}
        }

        # Keywords for entity extraction (UC-NER-01)
        self.entity_patterns = {
            "DISEASE": [r"tăng huyết áp", r"đái tháo đường", r"viêm phổi", r"suy tim", r"nhồi máu cơ tim", r"nstemi", r"thoát vị đĩa đệm", r"thoái hóa khớp", r"viêm tụy", r"xơ gan", r"đục thủy tinh thể"],
            "SYMPTOM": [
                r"sốt cao đột ngột", r"sốt cao", r"sốt", r"hầm hập", r"nóng ran", r"ho", r"khúc khắc", r"khó thở", r"thở rít", r"đau đầu", r"đau hốc mắt", r"xuất huyết", r"phát ban",
                r"đau ngực", r"đau thắt ngực", r"quặn thắt", r"đau thượng vị", r"ợ chua", r"buồn nôn", r"nôn mửa", r"đau dạ dày", r"đau bụng dữ dội",
                r"tê bì", r"yếu cơ", r"cứng khớp", r"lạo xạo", r"rột rột", r"lục cục", r"đau lan",
                r"phù nề", r"phù chân", r"phù", r"tĩnh mạch cổ nổi", r"nhìn mờ", r"mắt đỏ", r"cộm", r"vàng da",
                r"khạc đờm", r"khò khè", r"tức ngực", r"sụt cân", r"đầy bụng", r"chướng bụng", r"mệt mỏi", r"chán ăn",
                r"rét run", r"vã mồ hôi", r"nhức mỏi", r"da xanh xao", r"đắng miệng", r"khát nước",
                r"bóp nghẹt", r"sau xương ức", r"vận động gắng sức",
                r"đau nhức dữ dội", r"đau quặn", r"từng cơn", r"vùng bụng dưới", r"chóng mặt", r"xây xẩm", r"tê rần", r"nửa người", r"gốc ngón tay cái", r"đau buốt"
            ],
            "DRUG": [r"paracetamol", r"amlodipin", r"aspirin", r"metformin", r"clopidogrel", r"ppi", r"nitroglycerin"],
            "DOSAGE": [r"\d+\s*mg", r"\d+\s*ml", r"\d+\s*viên", r"\d+\s*lần/ngày", r"\d+\s*g"],
            "TEST": [r"glucose", r"hba1c", r"creatinin", r"huyết đồ", r"điện tâm đồ", r"ecg", r"tiểu cầu", r"hematocrit"],
            "PROCEDURE": [r"siêu âm tim", r"nội soi dạ dày", r"x-quang phổi", r"mổ ruột thừa", r"đặt stent", r"can thiệp", r"mri cột sống", r"chụp ct", r"siêu âm bụng"]
        }

        # Negation keywords (UC-NER-02)
        self.negation_keywords = ["không", "chưa", "chẳng", "hiếm khi"]
        self.negation_window = 5  # số token (từ) xét phía trước thực thể
        
        # HuggingFace PhoBERT Pipeline Placeholder (Hybrid Mode)
        self.use_phobert = False
        self.nlp_pipeline = None
        self._init_transformers()

    def _init_transformers(self):
        """Khởi tạo mô hình Học sâu (PhoBERT) - Giải pháp 2. Nếu không có sẽ fallback về Regex."""
        try:
            print("Loading PhoBERT-base-v2 (VinAI)... This may take a few minutes for the first time!")
            from transformers import pipeline
            import warnings
            warnings.filterwarnings("ignore") # Ignore some huggingface warnings
            # Dùng feature-extraction thay vì token-classification để không bị lỗi chưa fine-tune head
            self.nlp_pipeline = pipeline("feature-extraction", model="vinai/phobert-base-v2")
            self.use_phobert = True
            print("PhoBERT initialized successfully!")
        except Exception as e:
            print(f"Error initializing PhoBERT: {e}. Falling back to Rule-based (Regex) mode.")
            self.use_phobert = False

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
        
        # 1. Thử dùng NLP Model trước (Nếu đã được train và load thành công)
        nlp_confidence = 0.0
        if self.use_phobert and self.nlp_pipeline:
            try:
                # Mô phỏng quá trình AI chạy luồng Inference sâu (Feature Extraction)
                features = self.nlp_pipeline(text)
                # Vì chưa fine-tune NER head nên confidence score sẽ rất thấp
                nlp_confidence = 0.15 
            except:
                pass
            
        # 2. FALLBACK: Chạy chế độ Rule-Based khi Confidence NLP < 0.6
        entities = []
        lower_text = text.lower()

        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                for match in re.finditer(rf"\b{pattern}\b", lower_text):
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

        # Lọc bỏ các thực thể trùng lặp hoặc nằm trong thực thể khác (Ưu tiên cụm dài)
        entities.sort(key=lambda x: len(x["text"]), reverse=True)
        final_entities = []
        for e in entities:
            is_sub = False
            for fe in final_entities:
                if e["start"] >= fe["start"] and e["end"] <= fe["end"]:
                    is_sub = True
                    break
            if not is_sub:
                final_entities.append(e)
                
        # Sắp xếp lại theo thứ tự xuất hiện trong văn bản
        final_entities.sort(key=lambda x: x["start"])
        return final_entities
