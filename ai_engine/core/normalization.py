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
        # Simple word-based replacement for now
        # In production, this would use a more sophisticated NER/Context-aware approach
        words = text.split()
        expanded_words = [dictionary.get(word.upper(), word) for word in words]
        return " ".join(expanded_words)

    def detect_unknown_abbreviations(self, text: str, dictionary: dict) -> list:
        """UC-NORM-04: Detect potential abbreviations (all caps) not in dictionary."""
        # Find words that are 2+ characters and all uppercase
        potential_abbrs = re.findall(r"\b[A-Z]{2,}\b", text)
        unknown = [abbr for abbr in potential_abbrs if abbr.upper() not in dictionary]
        return list(set(unknown)) # Return unique unknown abbreviations

    def process(self, text: str, dictionary: dict = None) -> dict:
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
        
        for section, content in sections.items():
            sections[section] = self.expand_abbreviations(content, dict_content)
                
        return {
            "full_text": text,
            "sections": sections,
            "unknown_abbreviations": unknown_abbrs
        }
