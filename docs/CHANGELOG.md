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
