import re
import unicodedata

class Normalizer:
    def __init__(self):
        # Regex for section splitting based on common Vietnamese medical headers
        self.section_patterns = {
            "HÀNH CHÍNH": r"^(HÀNH CHÍNH|1\. HÀNH CHÍNH)",
            "LÝ DO VÀO VIỆN": r"^(LÝ DO VÀO VIỆN|2\. LÝ DO VÀO VIỆN)",
            "BỆNH SỬ": r"^(BỆNH SỬ|3\. BỆNH SỬ)",
            "TIỀN SỬ": r"^(TIỀN SỬ|4\. TIỀN SỬ)",
            "KHÁM BỆNH": r"^(KHÁM BỆNH|5\. KHÁM BỆNH)",
            "CẬN LÂM SÀNG": r"^(CẬN LÂM SÀNG|6\. CẬN LÂM SÀNG)",
            "CHẨN ĐOÁN": r"^(CHẨN ĐOÁN|7\. CHẨN ĐOÁN)",
            "KẾ HOẠCH ĐIỀU TRỊ": r"^(KẾ HOẠCH ĐIỀU TRỊ|8\. KẾ HOẠCH ĐIỀU TRỊ)"
        }
        
        # Basic unit normalization
        self.unit_map = {
            r"\bml\b": "mL",
            r"\bmg\b": "mg",
            r"\bkg\b": "kg",
            r"\bgr\b": "g",
            r"\bmmHg\b": "mmHg",
        }

        # UC-NORM-03: Default abbreviation dictionary
        self.default_dictionary = {
            "THA": "tăng huyết áp",
            "ĐTD": "đái tháo đường",
            "ĐTĐ": "đái tháo đường",
            "ECG": "điện tâm đồ",
            "NSTEMI": "nhồi máu cơ tim cấp không ST chênh lên",
            "ĐMV": "động mạch vành",
            "LAD": "động mạch liên thất trước",
            "CLS": "cận lâm sàng",
            "KHĐT": "kế hoạch điều trị"
        }

    def normalize_unicode(self, text: str) -> str:
        """UC-NORM-01: Normalize Unicode to NFC form."""
        if not text:
            return ""
        return unicodedata.normalize('NFC', text)

    def normalize_units(self, text: str) -> str:
        """UC-NORM-01: Standardize medical units."""
        for pattern, replacement in self.unit_map.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

    def split_sections(self, text: str) -> dict:
        """UC-NORM-02: Split medical record into sections."""
        lines = text.split('\n')
        sections = {}
        current_section = "GENERAL"
        sections[current_section] = []

        for line in lines:
            stripped_line = line.strip()
            found_header = False
            for section_name, pattern in self.section_patterns.items():
                if re.match(pattern, stripped_line, re.IGNORECASE):
                    current_section = section_name
                    sections[current_section] = []
                    found_header = True
                    break
            
            if not found_header:
                sections[current_section].append(line)

        return {k: "\n".join(v).strip() for k, v in sections.items() if v}

    def expand_abbreviations(self, text: str, dictionary: dict) -> str:
        """UC-NORM-03: Expand abbreviations based on a dictionary."""
        # Merge default dictionary with provided one
        full_dict = {**self.default_dictionary, **(dictionary or {})}
        
        # Simple word-based replacement for now (using regex for better boundary handling)
        for abbr, full_form in full_dict.items():
            pattern = rf"\b{re.escape(abbr)}\b"
            text = re.sub(pattern, full_form, text, flags=re.IGNORECASE)
        return text

    def detect_unknown_abbreviations(self, text: str, dictionary: dict) -> list:
        """UC-NORM-04: Detect potential abbreviations (all caps) not in dictionary."""
        # Find words that are 2+ characters and all uppercase
        potential_abbrs = re.findall(r"\b[A-Z]{2,}\b", text)
        unknown = [abbr for abbr in potential_abbrs if abbr.upper() not in dictionary]
        return list(set(unknown)) # Return unique unknown abbreviations

    def check_template_compliance(self, extracted_sections: dict, required_keys: list) -> list:
        """FR-NORM-06: Check if drafted text matches the required template sections."""
        warnings = []
        actual_keys = list(extracted_sections.keys())
        
        for key in required_keys:
            if key not in actual_keys:
                warnings.append(f"Cảnh báo: Bản nháp đang thiếu mục bắt buộc [{key}] theo yêu cầu của Template.")
                
        return warnings

    def process(self, text: str, dictionary: dict = None, required_keys: list = None) -> dict:
        """Full normalization pipeline."""
        dict_content = dictionary or {}
        
        # 1. Unicode Normalization
        text = self.normalize_unicode(text)
        
        # 2. Unit Normalization
        text = self.normalize_units(text)
        
        # 3. Section Splitting
        sections = self.split_sections(text)
        
        # 4. Abbreviation Expansion & Detection
        unknown_abbrs = self.detect_unknown_abbreviations(text, dict_content)
        
        # Create a fully normalized text (expanded abbreviations)
        normalized_text = self.expand_abbreviations(text, dict_content)
        
        for section, content in sections.items():
            sections[section] = self.expand_abbreviations(content, dict_content)
            
        # 5. Template Compliance Check
        compliance_warnings = []
        if required_keys:
            compliance_warnings = self.check_template_compliance(sections, required_keys)
                
        return {
            "full_text": text,
            "normalized_text": normalized_text,
            "sections": sections,
            "unknown_abbreviations": unknown_abbrs,
            "compliance_warnings": compliance_warnings
        }
