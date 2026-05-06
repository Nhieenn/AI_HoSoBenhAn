# HƯỚNG DẪN TRIỂN KHAI HỆ THỐNG VIMEDAI (DEMO)

Tài liệu này hướng dẫn cách thiết lập và chạy hệ thống ViMedAI cho buổi demo 13:30.

## 1. Yêu cầu hệ thống
- **Node.js**: v18.0.0 hoặc mới hơn.
- **Python**: v3.9 hoặc mới hơn.
- **Cổng dịch vụ**: 
  - Frontend: `3006`
  - Backend (AI Engine): `8001`

## 2. Cài đặt & Khởi chạy Frontend (Next.js)
1. Giải nén source code.
2. Mở terminal tại thư mục gốc và chạy:
   ```bash
   npm install
   npm run build
   npm start -- -p 3006
   ```
3. Truy cập: `http://localhost:3006`

## 3. Cài đặt & Khởi chạy Backend (AI Engine)
1. Di chuyển vào thư mục backend: `cd ai_engine` (hoặc đứng ở gốc).
2. Tạo môi trường ảo và cài đặt thư viện:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```
3. Khởi chạy server FastAPI:
   ```bash
   python main.py
   ```
   *Lưu ý: Server sẽ lắng nghe tại cổng 8001.*

## 4. Cấu hình Reverse Proxy (Nginx)
Nếu sử dụng Domain, vui lòng cấu hình Nginx trỏ về `localhost:3006`.
Dữ liệu AI được xử lý thông qua API nội bộ giữa Frontend và Backend.

---
*Người chuẩn bị: Đội ngũ phát triển ViMedAI*
