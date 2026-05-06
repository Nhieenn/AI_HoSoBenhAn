import sys
import os

# Add the current directory to sys.path to import core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.deid import DeIdentifier

def test_deidentification():
    deid = DeIdentifier()
    
    test_text = """
    BỆNH NHÂN: Nguyễn Văn A
    NGÀY SINH: 01/01/1980
    SỐ ĐIỆN THOẠI: 0912345678
    ĐỊA CHỈ: số 123 đường Giải Phóng, quận Hai Bà Trưng, Hà Nội
    CMND: 123456789
    SỐ BHYT: GD4010110110001
    SỐ HỒ SƠ: SHS.2024.001
    
    DIỄN BIẾN LÂM SÀNG:
    Bệnh nhân Nguyễn Văn A tỉnh táo, tiếp xúc tốt. 
    Huyết áp: 120/80 mmHg. Nhiệt độ: 37 độ C.
    Nhịp tim: 80 lần/phút.
    Xét nghiệm Glucose: 5.6 mmol/l.
    """
    
    print("Original Text:")
    print(test_text)
    print("-" * 20)
    
    result = deid.process(test_text)
    masked_text = result["masked_text"]
    logs = result["audit_logs"]
    
    print("Masked Text:")
    print(masked_text)
    print("-" * 20)
    
    print("Audit Logs:")
    for log in logs:
        print(f"Type: {log['entityType']}, Original: {log['originalValue']}, Masked: {log['maskedValue']}")
    print("-" * 20)
    
    # Simple assertions
    assert "[NAME_1]" in masked_text
    assert "[BIRTHDATE_1]" in masked_text
    assert "[PHONE_1]" in masked_text
    assert "[ADDRESS_1]" in masked_text
    assert "[ID_CARD_1]" in masked_text
    assert "[INSURANCE_ID_1]" in masked_text
    assert "[RECORD_ID_1]" in masked_text
    
    # Check clinical values protection
    assert "120/80 mmHg" in masked_text
    assert "5.6 mmol/l" in masked_text
    
    print("All tests passed!")

if __name__ == "__main__":
    test_deidentification()
