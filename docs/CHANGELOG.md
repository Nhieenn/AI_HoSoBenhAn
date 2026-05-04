# Changelog — AI_HoSoBenhAn

## [2026-05-04] — Project Setup
### Added
- Khởi tạo cấu trúc thư mục dự án (docs, .gemini, .cursorrules).
- Thiết lập bộ quy tắc dự án (RULES.md, .cursorrules, .gemini/rules.md).
- Hoàn thiện tài liệu cơ bản (ARCHITECTURE.md, DATABASE.md, SECURITY.md, API_CONTRACTS.md).

## [2026-05-04] — Module 1: Chuẩn hóa và Xử lý văn bản (Normalization)
### Added
- Logic AI: Chuẩn hóa Unicode, đơn vị đo, phân đoạn Section bệnh án.
- Logic AI: Mở rộng viết tắt và phát hiện viết tắt mới chưa có trong từ điển.
- API Backend: Endpoint `/api/ai/normalize` để gọi Engine Python.
- Admin API: CRUD từ điển viết tắt tại `/api/admin/dictionary`.
### Security
- Input validation cơ bản cho các endpoint API.
- Đã cấu hình `.gitignore` để tránh rò rỉ file môi trường và cache.
### Files changed
- prisma/schema.prisma (MODIFIED — thêm model NormalizationDict, Department)
- ai_engine/main.py (NEW)
- ai_engine/core/normalization.py (NEW)
- src/services/aiService.ts (NEW)
- src/services/dictionaryService.ts (NEW)
- src/app/api/ai/normalize/route.ts (NEW)
- src/app/api/admin/dictionary/route.ts (NEW)

## [2026-05-04] — Module 2: Ẩn danh dữ liệu (De-identification)
### Added
- Bảng `DeidAuditLog` trong schema Prisma để lưu lịch sử ẩn danh.
- Tích hợp `AIService.deidentify(text)` kết nối với AI Engine.
- `RecordService`: Xử lý băm `patientId` (SHA-256) và thiết lập luồng xử lý bất đồng bộ (chạy nền).
- API Backend: Endpoint `/api/documents/ingest` (POST) tiếp nhận dữ liệu HIS và trả về mã `202 Accepted`.
- API Backend: Endpoint `/api/documents/[id]/status` (GET) kiểm tra trạng thái xử lý.
### Security
- Băm `patientId` chuẩn SHA-256 có hỗ trợ salt.
- Input validation bắt buộc (`externalId`, `patientId`, `content`, `type`).
- Xử lý mượt mà (Graceful Degradation) khi Database hoặc AI Engine mất kết nối, không làm treo ứng dụng.
### Files changed
- prisma/schema.prisma (MODIFIED)
- src/services/aiService.ts (MODIFIED)
- src/services/recordService.ts (NEW)
- src/app/api/documents/ingest/route.ts (NEW)
- src/app/api/documents/[id]/status/route.ts (NEW)

## [2026-04-12] — Module Partner (Mẫu)
### Added
- API CRUD /api/partners (GET, POST, PUT, DELETE)
- Trang danh sách partners với phân trang + search
- Form thêm/sửa partner với Zod validation
### Security
- Thêm input validation cho tất cả field
- Rate limiting 30 req/phút cho API partner
### Files changed
- src/app/api/partners/route.ts (NEW)
- src/app/dashboard/partners/page.tsx (NEW)
- prisma/schema.prisma (MODIFIED — thêm model Partner)
- docs/DATABASE.md (UPDATED)

## [2026-04-10] — Module Auth (Mẫu)
### Added
- Login/Logout with JWT
- Middleware auth check
- Role-based access control
### Files changed
- src/lib/auth.ts (NEW) ⚠️ PROTECTED
- src/middleware.ts (NEW) ⚠️ PROTECTED
