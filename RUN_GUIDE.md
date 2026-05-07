# Hướng dẫn khởi động hệ thống ViMedAI (Bản Demo)

Để hệ thống hoạt động đầy đủ tính năng (Dashboard, Trích xuất NER, Truy vấn RAG, Sinh bệnh án), người dùng (Sếp/BA) cần chạy đồng thời 2 thành phần (Backend và Frontend) ở 2 Terminal (Cửa sổ dòng lệnh) khác nhau.

---

## 1. Khởi động Lõi AI Backend (Inference Engine)
Thành phần này chứa các mô hình AI (PhoBERT) và Cơ sở dữ liệu Vector RAG. Nó chịu trách nhiệm trích xuất triệu chứng và trả về chẩn đoán.

- **Mở Terminal 1** tại gốc dự án (`d:\AI_HoSoBenhAn` hoặc thư mục bạn vừa clone về).
- **Lệnh thực hiện:** (Bắt buộc phải truy cập vào thư mục `ai_engine` trước khi chạy)
  ```powershell
  cd ai_engine
  python -m uvicorn main:app --reload --port 8000
  ```
- **Lưu ý:** Lần chạy đầu tiên sẽ mất khoảng 1-2 phút để tải mô hình `PhoBERT-base-v2` và nạp dữ liệu từ `vector_db`. Khi màn hình hiện `Application startup complete` là thành công.
- **Địa chỉ API:** `http://localhost:8000/docs` (Swagger UI để test API trực tiếp).

*(Lưu ý cực kỳ quan trọng nếu clone sang máy mới: Vì file Vector DB rất nặng không đẩy lên Git, bạn cần nạp lại 1000 bệnh vào DB bằng cách mở Terminal thứ 3 và chạy lệnh: `python scratch/ingest_full_kb.py` trước khi test).*

---

## 2. Khởi động Frontend (Giao diện người dùng Web)
Thành phần này cung cấp giao diện Dashboard và trình soạn thảo bệnh án để Bác sĩ tương tác.

- **Mở Terminal 2** (Giữ nguyên Terminal 1 đang chạy Backend) tại gốc dự án.
- **Cài đặt thư viện (Chỉ chạy lần đầu):**
  ```powershell
  npm install
  ```
- **Lệnh khởi động:**
  ```powershell
  npm run dev
  ```
- **Địa chỉ truy cập Web:** Mở trình duyệt và vào `http://localhost:3000`

---

### Các lưu ý Quan trọng cho buổi Showcase (Demo):
1. **Thứ tự:** BẮT BUỘC phải chờ Terminal 1 (Backend AI) báo `Application startup complete` thì mới lên Web test tính năng sinh bệnh án. Nếu không, Web sẽ báo "Lỗi kết nối Inference Engine".
2. **Kịch bản Demo:** 
   - Đóng vai "Bác sĩ Hùng".
   - Vào danh sách bệnh nhân chờ, test 1 ca "Nhồi máu cơ tim" (để show tính năng Cấp cứu).
   - Test 1 ca "Đau nhức vùng ngực, lan ra sau lưng..." hoặc "Run tay, chậm chạp" (để show tính năng RAG - Bệnh Parkinson/Đa bệnh lý).
3. **Cảnh báo tính năng:** Nhấn mạnh với Sếp rằng đây là "Bộ khung luồng chạy (Architecture Pipeline)". Backend đang chạy bằng If/Else giả lập. Trí thông minh thật sự (Local LLM) sẽ được cắm vào ở Giai đoạn 2 sau khi có máy chủ GPU.

*Chúc dự án thành công rực rỡ!*
