import re
import hashlib
from typing import List, Dict, Tuple

class DeIdentifier:
    def __init__(self):
        # UC-DEID-01: Regex patterns for 8 PHI groups
        self.patterns = {
            "PHONE": r"(?:\+84|0)(?:\d{9,10})\b",
            "BIRTHDATE": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            "ID_CARD": r"\b\d{9}\b|\b\d{12}\b", # CMND/CCCD
            "INSURANCE_ID": r"\b[A-Z]{2}\d{10,13}\b", # BHYT
            "RECORD_ID": r"\bSHS[.:\s-]?\d+(?:\.\d+)*\b", # Số hồ sơ
            "ADDRESS": r"(?:số\s+\d+|đường\s+[A-ZÀ-Ỹ]|phường\s+[A-ZÀ-Ỹ]|quận\s+[A-ZÀ-Ỹ]|huyện\s+[A-ZÀ-Ỹ]|thành phố\s+[A-ZÀ-Ỹ])\b.*?(?=\n|,|$)",
            "NAME": r"\b[A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ][a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứcửữựỳýỷỹỵ]*(\s[A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ][a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứcửữựỳýỷỹỵ]*){1,4}\b"
        }
        
        # UC-DEID-05: Protection patterns
        self.protection_patterns = [
            r"\b\d+\s*(?:mmHg|mg|ml|mL|kg|g|mmol/l|U/L|g/L|%|độ C|lần/phút)\b",
            r"\b(?:Huyết áp|HA|Nhịp tim|Nhiệt độ|SpO2|Cân nặng|Chiều cao|Glucose)\s*[:]?\s*\d+(?:\.\d+)?\b"
        ]

    def _is_protected(self, text: str, start: int, end: int) -> bool:
        """Check if the detected PHI overlaps with a protected clinical value."""
        for pattern in self.protection_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                if match.start() < end and match.end() > start:
                    return True
        return False

    def mask_phi(self, text: str) -> Tuple[str, List[Dict]]:
        """
        UC-DEID-01, UC-DEID-03, UC-DEID-05: Detect, mask and pseudonymize PHI.
        """
        audit_logs = []
        masked_text = text
        
        mapping = {} 
        type_counters = {} 
        
        order = ["RECORD_ID", "INSURANCE_ID", "ID_CARD", "PHONE", "BIRTHDATE", "ADDRESS", "NAME"]
        
        for p_type in order:
            pattern = self.patterns.get(p_type)
            if not pattern: continue
            
            # Use finditer on the CURRENT masked_text
            matches = list(re.finditer(pattern, masked_text))
            for match in sorted(matches, key=lambda x: x.start(), reverse=True):
                start, end = match.start(), match.end()
                original_value = match.group()
                
                if self._is_protected(masked_text, start, end):
                    continue
                
                # Consistent pseudonym per type
                mapping_key = f"{p_type}:{original_value}"
                if mapping_key not in mapping:
                    count = type_counters.get(p_type, 0) + 1
                    type_counters[p_type] = count
                    mapping[mapping_key] = f"[{p_type}_{count}]"
                
                masked_value = mapping[mapping_key]
                masked_text = masked_text[:start] + masked_value + masked_text[end:]
                
                audit_logs.append({
                    "entityType": p_type,
                    "originalValue": original_value,
                    "maskedValue": masked_value,
                    "startPos": start,
                    "endPos": start + len(masked_value)
                })
                
        return masked_text, audit_logs

    def process(self, text: str) -> Dict:
        """Full de-identification pipeline."""
        masked_text, logs = self.mask_phi(text)
        return {
            "masked_text": masked_text,
            "audit_logs": logs
        }
