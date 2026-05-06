# 🚀 CHIẾN DỊCH DEMO VIMEDAI (13:30 - 06/05/2026)

Dưới đây là danh sách nhiệm vụ chi tiết để hoàn thiện hệ thống và triển khai cho khách hàng/QC kiểm thử.

## 1. Dashboard & UI/UX (Đã hoàn thiện)
- [x] Sửa lỗi đồ họa: Icon KPI bị to quá cỡ.
- [x] Sửa lỗi bố cục: Loại bỏ lặp Sidebar/Topbar.
- [x] Khôi phục Sidebar/Topbar chuẩn Quân y (Navy/Gold).
- [x] Đồng bộ bảng Audit Logs theo phong cách v2.
- [x] Fix bug SyntaxError & 404 trang Discharge.
- [x] Khôi phục CSS Editor, Pipeline và Panels.
- [x] **MỚI**: Tích hợp thanh điều hướng nổi (DemoNav) hỗ trợ chuyển module nhanh.

## 2. Module Discharge & Radiology (Cốt lõi)
- [x] Logic sinh nháp AI (NER, RAG, Generation).
- [x] Nút **"Phê duyệt & Lưu HIS"**: Đồng bộ EHR & Ghi Audit Log.
- [x] Safety Gates: PHI Check, Hallucination & Faithfulness score.
- [x] **Nâng cấp Radiology**: DICOM Viewer (Simulated) & AI Findings Table.
- [x] **Bổ sung ngữ cảnh**: Tính năng nhập thêm triệu chứng lâm sàng bằng nút `+`.
- [x] **Điều hướng Breadcrumbs**: Chuyển đổi Breadcrumbs thành liên kết & tối ưu hiệu ứng phản hồi.
- [x] **Phản hồi nút bấm**: Tối ưu hiệu ứng hover/active cho các nút Sinh lại, Từ chối, Phê duyệt.

## 3. Mockup & Tính năng bổ trợ (Theo yêu cầu BA)
- [x] **Hàng đợi nhập (Queue)**: Giao diện bảng danh sách bệnh nhân chờ xử lý thời gian thực.
- [x] **Hồ sơ bệnh nhân**: Trang quản lý danh sách bệnh nhân tập trung.
- [x] **Thư viện Tri thức**: Giao diện tra cứu phác đồ điều trị (RAG Source).
- [x] **Audit System**: Trang nhật ký hệ thống minh bạch.

## 4. Triển khai & Kiểm thử (Hạn chót: 11:30)
- [x] **Build Production**: Chạy `npm run build` để tối ưu mã nguồn (Đã hoàn thành - Exit code 0).
- [ ] **Kích hoạt Service**:
    - [ ] Khởi chạy Frontend ở chế độ Production: `npm start -- -p 3006`.
    - [ ] Khởi chạy Backend AI Engine (venv_prod): `python ai_engine/main.py`.
- [ ] **Công bố Tên miền (Public URL)**:
    - [ ] Thiết lập Cloudflare Tunnel (cloudflared) để QC/Tester truy cập từ xa.
    - [ ] Gửi URL chính thức cho ban dự án.
- [ ] **QC & Dry Run**:
    - [ ] Bàn giao cho QC kiểm tra luồng chính (Happy Path).
    - [ ] Chạy thử kịch bản demo: Dashboard -> Queue -> Editor -> Audit.

---
*Ghi chú: Mọi tính năng giao diện đã được đồng bộ với Mockup v2 mới nhất của công ty.*
*Trạng thái: [ ] Chưa làm | [/] Đang làm | [x] Hoàn thành*
