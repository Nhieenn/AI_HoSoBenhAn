# Hướng dẫn khởi động hệ thống ViMedAI

Để hệ thống hoạt động đầy đủ tính năng (Dashboard, Editor, AI Diagnosis, RAG), bạn cần chạy đồng thời 2 thành phần sau:

## 1. Khởi động AI Backend (Inference Engine)
Thành phần này xử lý các tác vụ thông minh: trích xuất triệu chứng, tra cứu phác đồ và sinh bệnh án.

- **Thư mục:** Gốc dự án (`d:\AI_HoSoBenhAn`)
- **Lệnh thực hiện:**
  ```powershell
  python ai_engine/main.py
  ```
- **Địa chỉ:** `http://localhost:8001` (Kiểm tra tại `http://localhost:8001/docs`)

## 2. Khởi động Frontend (Giao diện người dùng)
Thành phần này cung cấp giao diện Dashboard và trình soạn thảo bệnh án.

- **Thư mục:** Gốc dự án (`d:\AI_HoSoBenhAn`)
- **Lệnh thực hiện:**
  ```powershell
  npm run dev
  ```
  *Hoặc để chạy đúng cổng 3006 như phiên làm việc này:*
  ```powershell
  npx next dev -p 3006
  ```
- **Địa chỉ:** `http://localhost:3006`

---

### Các lưu ý quan trọng cho buổi Test:
1. **Thứ tự:** Nên chạy Backend trước để Frontend có thể kết nối ngay khi tải trang.
2. **Dữ liệu:** Không xóa file `knowledge_base.json` vì đây là nơi chứa kiến thức y khoa để AI tra cứu.
3. **Quyền hạn:** Đăng nhập mặc định đang là **Bác sĩ Nguyễn V. Hùng** để bạn có thể test tính năng "Chỉnh sửa dữ liệu thô (HIS)".
4. **Lỗi 500:** Nếu gặp lỗi này khi sinh bệnh án, hãy kiểm tra xem Terminal chạy Python có đang bị treo không.

*Chúc bạn có một buổi làm việc hiệu quả!*
