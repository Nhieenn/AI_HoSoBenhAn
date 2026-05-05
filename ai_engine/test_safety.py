from core.safety import SafetyChecker

def test_safety_checker():
    checker = SafetyChecker()
    
    # 1. Test PHI Leak
    draft_with_phi = "Bệnh nhân Nguyễn Văn A sinh ngày 12/05/1980, số điện thoại 0912345678."
    phi_warnings = checker.check_phi_leak(draft_with_phi)
    
    assert len(phi_warnings) > 0, "Phải phát hiện được ít nhất 1 lỗi PHI"
    assert any("0912345678" in w for w in phi_warnings), "Phải bắt được số điện thoại"
    assert any("12/05/1980" in w for w in phi_warnings), "Phải bắt được ngày sinh"
    
    draft_safe = "Bệnh nhân [NAME_1] sinh ngày [DATE_1], số điện thoại [PHONE_1]."
    safe_warnings = checker.check_phi_leak(draft_safe)
    assert len(safe_warnings) == 0, "Không được báo lỗi khi PHI đã được mask đúng chuẩn"

    # 2. Test Hallucination
    original_entities = [
        {"type": "DISEASE", "text": "Đái tháo đường"},
        {"type": "DRUG", "text": "Metformin"}
    ]
    
    # Bản nháp tự "đẻ" ra bệnh Tăng huyết áp và thuốc Amlodipin
    draft_entities = [
        {"type": "DISEASE", "text": "Đái tháo đường"},
        {"type": "DISEASE", "text": "Tăng huyết áp"},
        {"type": "DRUG", "text": "Amlodipin"}
    ]
    
    hall_warnings = checker.check_hallucination(original_entities, draft_entities)
    assert len(hall_warnings) == 2, "Phải phát hiện 2 lỗi hallucination (1 bệnh, 1 thuốc)"
    assert any("Tăng huyết áp" in w for w in hall_warnings), "Phải cảnh báo bịa bệnh Tăng huyết áp"
    assert any("Amlodipin" in w for w in hall_warnings), "Phải cảnh báo bịa thuốc Amlodipin"

    # 3. Test Internal Conflict
    patient_male = {"gender": "Nam", "age": 30}
    conflict_draft_entities = [{"type": "DISEASE", "text": "U xơ tử cung"}]
    conflict_warnings = checker.check_internal_conflict(patient_male, conflict_draft_entities)
    assert len(conflict_warnings) == 1, "Phải phát hiện mâu thuẫn Nam - tử cung"
    assert "tử cung" in conflict_warnings[0]
    
    patient_child = {"gender": "Nữ", "age": 5}
    conflict_draft_entities_2 = [{"type": "DISEASE", "text": "Bệnh người già"}]
    conflict_warnings_2 = checker.check_internal_conflict(patient_child, conflict_draft_entities_2)
    assert len(conflict_warnings_2) == 1, "Phải phát hiện mâu thuẫn tuổi - lão khoa"
    assert "người già" in conflict_warnings_2[0]

if __name__ == "__main__":
    test_safety_checker()
    print("All Safety tests passed!")
