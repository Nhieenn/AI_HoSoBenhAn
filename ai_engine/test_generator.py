import sys
import os

# Add the current directory to sys.path to import core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.generator import ClinicalGenerator

def test_generation():
    generator = ClinicalGenerator()
    
    # Mock data
    patient_data = {
        "name": "Nguyễn Văn A",
        "age": "45",
        "gender": "Nam",
        "reason": "Đau tức ngực",
    }
    
    entities = [
        {"text": "Tăng huyết áp", "type": "DISEASE", "is_negative": False},
        {"text": "Đau ngực", "type": "SYMPTOM", "is_negative": False},
        {"text": "sốt", "type": "SYMPTOM", "is_negative": True},  # bị phủ định, sẽ không điền
        {"text": "Amlodipin", "type": "DRUG", "is_negative": False},
        {"text": "Siêu âm tim", "type": "PROCEDURE", "is_negative": False}
    ]
    
    print("=== TEST 1: DISCHARGE SUMMARY (General) ===")
    summary1 = generator.generate_discharge_summary(patient_data, entities, "General")
    print(summary1)
    print("-" * 40)
    
    # Assertions Test 1
    assert "Nguyễn Văn A" in summary1
    assert "Đau ngực" in summary1
    assert "sốt" not in summary1  # Because it's negated
    assert "[UNCERTAIN: Cần bác sĩ xác nhận lại]" in summary1 # Missing exact diagnosis but has diseases
    
    print("=== TEST 2: DISCHARGE SUMMARY (Cardiology) ===")
    summary2 = generator.generate_discharge_summary(patient_data, entities, "Cardiology")
    print(summary2)
    print("-" * 40)
    
    print("=== TEST 3: RADIOLOGY REPORT (No explicit conclusion) ===")
    raw_findings = "Bóng tim to nhẹ. Phổi sáng. Không thấy hình ảnh tràn dịch màng phổi."
    rad_report = generator.generate_radiology_report(raw_findings, entities)
    print(rad_report)
    print("-" * 40)
    
    # Assertion Test 3
    assert "[UNCERTAIN: Cần bác sĩ CĐHA kết luận trực tiếp]" in rad_report
    
    print("=== TEST 4: RADIOLOGY REPORT (With conclusion) ===")
    raw_findings2 = "Bóng tim to nhẹ. Phổi sáng. Kết luận: Tim to độ 1."
    rad_report2 = generator.generate_radiology_report(raw_findings2, entities)
    print(rad_report2)
    print("-" * 40)
    
    assert "Tim to độ 1." in rad_report2
    assert "UNCERTAIN" not in rad_report2
    
    print("All Generation tests passed!")

if __name__ == "__main__":
    test_generation()
