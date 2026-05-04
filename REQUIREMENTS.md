# Danh sách Chức năng Chi tiết ViMedAI (Requirements)
*Dựa trên đối soát 1:1 với tài liệu BA_ViMedAI.md*

## Module 1: Chuẩn hóa và Xử lý văn bản (Normalization)

### UC-NORM-01: Chuẩn hóa Unicode và định dạng y khoa
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Chuẩn hóa Unicode, đơn vị đo, dấu câu và ký tự đặc biệt.
- Luồng chính: (Theo FR-NORM-01)

### UC-NORM-02: Phân đoạn section bệnh án tự động
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Tự động phân tách: hành chính, bệnh sử, tiền sử, khám, CLS, chẩn đoán, KHĐT.
- Luồng chính: (Theo FR-NORM-02)

### UC-NORM-03: Mở rộng viết tắt theo ngữ cảnh
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Tra cứu và mở rộng viết tắt theo từ điển nội bộ và ngữ cảnh từng section.
- Luồng chính: (Theo FR-NORM-03)

### UC-NORM-04: Cảnh báo và bổ sung viết tắt mới
- Ưu tiên: SHOULD
- Actor: Bác sĩ, Hệ thống
- Mô tả: Cảnh báo khi gặp viết tắt chưa có trong từ điển, cho phép bác sĩ bổ sung nhanh.
- Luồng chính: (Theo FR-NORM-04)

### UC-NORM-05: Quản trị từ điển viết tắt
- Ưu tiên: MUST
- Actor: Admin
- Mô tả: Cập nhật từ điển viết tắt nội viện theo từng khoa/phòng.
- Luồng chính: (Theo FR-NORM-05)

---

## Module 2: Ẩn danh dữ liệu (De-identification)

### UC-DEID-01: Phát hiện và Mask 8 nhóm PHI
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Tự động che tên, ngày sinh, địa chỉ, SĐT, định danh cá nhân...
- Luồng chính: (Theo FR-DEID-01)

### UC-DEID-02: Kiểm soát De-id đa tầng
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Đảm bảo De-id hoạt động trước mọi tác vụ: huấn luyện, inference, lưu trữ.
- Luồng chính: (Theo FR-DEID-02)

### UC-DEID-03: Pseudonymization nhất quán
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Đảm bảo cùng một bệnh nhân trong một tập dữ liệu sẽ có cùng một mã giả danh.
- Luồng chính: (Theo FR-DEID-03)

### UC-DEID-04: Audit log thực thể ẩn danh
- Ưu tiên: MUST
- Actor: Hệ thống, Admin
- Mô tả: Báo cáo chi tiết mỗi thực thể bị mask phục vụ hậu kiểm.
- Luồng chính: (Theo FR-DEID-04)

### UC-DEID-05: Bảo vệ giá trị lâm sàng
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Đảm bảo không mask nhầm các số liệu xét nghiệm, chỉ số sinh tồn.
- Luồng chính: (Theo FR-DEID-05)

---

## Module 3: Trích xuất khái niệm lâm sàng (NER)

### UC-NER-01: Nhận dạng thực thể y khoa chuyên sâu
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Trích xuất: bệnh lý, triệu chứng, thuốc, liều dùng, xét nghiệm, thủ thuật.
- Luồng chính: (Theo FR-NER-01, FR-NER-02)

### UC-NER-02: Phân tích bối cảnh phủ định
- Ưu tiên: SHOULD
- Actor: Hệ thống
- Mô tả: Nhận diện chính xác các thực thể ở dạng phủ định (vd: "không ho").
- Luồng chính: (Theo FR-NER-03)

### UC-NER-03: Liên kết Ontology (ICD/SNOMED)
- Ưu tiên: SHOULD
- Actor: Hệ thống
- Mô tả: Ánh xạ các thực thể trích xuất được với các bộ mã chuẩn quốc tế.
- Luồng chính: (Theo FR-NER-04)

---

## Module 4: Sinh nháp (Generation)

### UC-GEN-01: Sinh nháp Discharge Summary
- Ưu tiên: MUST
- Actor: Bác sĩ, Hệ thống
- Mô tả: Tổng hợp từ dữ liệu cấu trúc đầu vào để tạo bản tóm tắt xuất viện.
- Luồng chính: (Theo FR-GEN-01)

### UC-GEN-02: Cấu trúc hóa báo cáo Radiology
- Ưu tiên: MUST
- Actor: Bác sĩ CĐHA
- Mô tả: Chuyển text mô tả tự do sang định dạng báo cáo chuẩn.
- Luồng chính: (Theo FR-GEN-02)

### UC-GEN-03: Tiền điền tự động (Auto-fill)
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Tự động điền các trường hành chính và clinical facts có thể kiểm chứng.
- Luồng chính: (Theo FR-GEN-03)

### UC-GEN-04: Xử lý thông tin mơ hồ (Uncertainty)
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Gắn cờ cảnh báo khi thông tin đầu vào thiếu hoặc mơ hồ; không tự ý bịa thông tin.
- Luồng chính: (Theo FR-GEN-04, FR-GEN-05)

### UC-GEN-05: Quản lý Template theo khoa
- Ưu tiên: SHOULD
- Actor: Admin, Bác sĩ
- Mô tả: Hỗ trợ các mẫu biểu tùy chỉnh riêng cho từng chuyên khoa.
- Luồng chính: (Theo FR-GEN-06)

---

## Module 5: Truy hồi và Neo đầu ra (RAG)

### UC-RAG-01: Quản lý kho tri thức y khoa
- Ưu tiên: MUST
- Actor: Hệ thống, Admin
- Mô tả: Lập chỉ mục phác đồ, hướng dẫn, từ điển quy ước bệnh viện.
- Luồng chính: (Theo FR-RAG-01, FR-RAG-05)

### UC-RAG-02: Truy hồi và Citation
- Ưu tiên: MUST
- Actor: Hệ thống, Bác sĩ
- Mô tả: Tìm tài liệu liên quan và gắn trích dẫn nguồn vào bản thảo AI sinh ra.
- Luồng chính: (Theo FR-RAG-02, FR-RAG-03)

---

## Module 6: Kiểm soát an toàn và Workflow

### UC-SAFE-01: Hậu kiểm an toàn (Safety Layer)
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Kiểm tra PHI, mâu thuẫn nội bộ và hallucination trước khi hiển thị nháp.
- Luồng chính: (Theo FR-SAFE-01 -> FR-SAFE-04)

### UC-WF-01: Review và Phê duyệt (Assisted Mode)
- Ưu tiên: MUST
- Actor: Bác sĩ
- Mô tả: Cho phép chỉnh sửa trực tiếp, phê duyệt hoặc từ chối bản thảo.
- Luồng chính: (Theo FR-WF-01 -> FR-WF-03)

### UC-WF-02: Active Learning từ phản hồi bác sĩ
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Ghi lại sự khác biệt (diff) giữa nháp gốc và bản duyệt để cải thiện mô hình.
- Luồng chính: (Theo FR-WF-04)

### UC-WF-03: Chế độ chạy ngầm (Silent Mode)
- Ưu tiên: SHOULD
- Actor: Hệ thống, Admin
- Mô tả: Sinh nháp ngầm không hiển thị trong workflow thật để đánh giá chất lượng.
- Luồng chính: (Theo FR-WF-05)

---

## Module 7: Audit và Bảo mật

### UC-AUD-01: Ghi log hoạt động chi tiết
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Log toàn bộ: sinh, sửa, duyệt, reject, block kèm timestamp và ID.
- Luồng chính: (Theo FR-AUD-01, FR-AUD-02)

### UC-AUD-02: Phân quyền vai trò (RBAC)
- Ưu tiên: MUST
- Actor: Admin
- Mô tả: Phân quyền chi tiết cho Bác sĩ, Điều dưỡng, Quản trị, Nhà nghiên cứu.
- Luồng chính: (Theo FR-AUD-03)

### UC-AUD-03: Cô lập dữ liệu (On-premise)
- Ưu tiên: MUST
- Actor: Hệ thống
- Mô tả: Đảm bảo không truyền dữ liệu bệnh nhân ra ngoài network bệnh viện.
- Luồng chính: (Theo FR-AUD-04)
