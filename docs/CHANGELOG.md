# Changelog — AI_HoSoBenhAn

## [2026-05-04] — Project Setup
### Added
- Khởi tạo cấu trúc thư mục dự án (docs, .gemini, .cursorrules).
- Thiết lập bộ quy tắc dự án (RULES.md, .cursorrules, .gemini/rules.md).
- Hoàn thiện tài liệu cơ bản (ARCHITECTURE.md, DATABASE.md, SECURITY.md, API_CONTRACTS.md).

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
