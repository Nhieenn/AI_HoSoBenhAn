# Chính sách Bảo mật — ViMedAI

## 1. Nguyên tắc Ẩn danh (De-identification)
- **Tự động hóa:** Hệ thống bắt buộc sử dụng NER để phát hiện và che giấu 18 loại thông tin định danh (theo chuẩn HIPAA cải biên cho Việt Nam).
- **Pseudonymization:** Sử dụng mã giả định thay cho tên thật (vd: Patient A, Patient B) để duy trì tính logic trong văn bản mà không lộ danh tính.

## 2. Bảo mật Dữ liệu (Data Security)
- **Mã hóa:** 
  - Dữ liệu tĩnh (At-rest): Mã hóa AES-256 cho các trường PHI trong DB.
  - Dữ liệu di chuyển (In-transit): Bắt buộc dùng TLS 1.3 trong mạng nội bộ.
- **On-premise Isolation:** Toàn bộ hệ thống không có kết nối internet ra ngoài. Các bộ thư viện và mô hình AI phải được quét mã độc trước khi đưa vào mạng nội bộ.

## 3. Quản lý Truy cập (Access Control)
- **RBAC:** Phân quyền nghiêm ngặt giữa Bác sĩ điều trị, Bác sĩ CĐHA, và Admin.
- **MFA:** Bắt buộc xác thực 2 yếu tố cho các tài khoản có quyền Quản trị hoặc truy cập Audit Log.
- **Session Timeout:** Tự động đăng xuất sau 15 phút không hoạt động để tránh rủi ro tại máy trạm bác sĩ.

## 4. Nhật ký Giám sát (Audit Logging)
- Hệ thống ghi lại:
  - Ai đã xem hồ sơ nào?
  - Ai đã phê duyệt bản thảo AI?
  - Nội dung gốc vs Nội dung đã sửa (Diff).
- Log được lưu trữ tại phân vùng riêng, không cho phép xóa/sửa.

## 5. Phòng chống Hallucination (Safety Layer)
- Áp dụng kỹ thuật **Self-Correction** và **Cross-check** với dữ liệu gốc từ HIS để cảnh báo bác sĩ nếu AI sinh ra thông tin sai lệch về lâm sàng (vd: sai liều thuốc).
