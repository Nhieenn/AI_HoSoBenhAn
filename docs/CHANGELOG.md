# Changelog — AI_HoSoBenhAn

## [2026-05-05] — Module 4: Sinh nháp (Generation)
### Added
- **UC-GEN-01 & UC-GEN-02**: Sinh cấu trúc Tóm tắt xuất viện và Báo cáo CĐHA bằng Template-based Generation (Mock LLM).
- **UC-GEN-03 (Auto-fill)**: Điền tự động các thực thể (bệnh, triệu chứng, thuốc, xét nghiệm) và thông tin hành chính vào form mẫu. Loại bỏ các thực thể có bối cảnh phủ định.
- **UC-GEN-04 (Uncertainty)**: Tự động đánh dấu cờ `[UNCERTAIN]` hoặc `[CẢNH BÁO]` đối với hồ sơ thiếu dữ liệu chẩn đoán/kết luận.
- **UC-GEN-05**: Hỗ trợ bộ template khác nhau cho từng chuyên khoa (General, Cardiology, XRay).
- Thêm 2 API POST `/generate/discharge` và `/generate/radiology` trong Inference Engine.
### Files changed
- `ai_engine/main.py` (MODIFIED)
- `ai_engine/core/generator.py` (NEW) ⚠️ PROTECTED
- `ai_engine/test_generator.py` (NEW)

## [2026-05-05] — Module 3: Trích xuất khái niệm lâm sàng (NER)
### Added
- **UC-NER-01**: Nhận dạng 6 loại thực thể y khoa (DISEASE, SYMPTOM, DRUG, DOSAGE, TEST, PROCEDURE) bằng rule-based Regex và Dictionary.
- **UC-NER-02**: Logic phân tích bối cảnh phủ định ("không", "chưa") trong phạm vi mệnh đề, phân tách tự động theo dấu câu để bảo vệ các thực thể khẳng định đi kèm.
- **UC-NER-03**: Map tự động thực thể trích xuất với mã tiêu chuẩn Ontology (ICD-10, LOINC, ATC) dựa trên từ điển mô phỏng.
- Tích hợp endpoint POST `/extract` vào Inference Engine để frontend/backend giao tiếp xử lý NER.
### Files changed
- `ai_engine/main.py` (MODIFIED)
- `ai_engine/core/ner.py` (NEW) ⚠️ PROTECTED
- `ai_engine/test_ner.py` (NEW)

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
- `prisma/schema.prisma` (MODIFIED)
- `src/services/aiService.ts` (MODIFIED)
- `src/services/recordService.ts` (NEW)
- `src/app/api/documents/ingest/route.ts` (NEW)
- `src/app/api/documents/[id]/status/route.ts` (NEW)

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
- `prisma/schema.prisma` (MODIFIED — thêm model NormalizationDict, Department)
- `ai_engine/main.py` (NEW) ⚠️ PROTECTED
- `ai_engine/core/normalization.py` (NEW) ⚠️ PROTECTED
- `src/services/aiService.ts` (NEW)
- `src/services/dictionaryService.ts` (NEW)
- `src/app/api/ai/normalize/route.ts` (NEW)
- `src/app/api/admin/dictionary/route.ts` (NEW)

## [2026-05-04] — Project Setup
### Added
- Khởi tạo cấu trúc thư mục dự án (docs, .gemini, .cursorrules).
- Thiết lập bộ quy tắc dự án (RULES.md, .cursorrules, .gemini/rules.md).
- Hoàn thiện tài liệu cơ bản (ARCHITECTURE.md, DATABASE.md, SECURITY.md, API_CONTRACTS.md).

## [2026-04-12] — Module Partner (Mẫu)
### Added
- API CRUD /api/partners (GET, POST, PUT, DELETE).
- Trang danh sách partners với phân trang + search.
- Form thêm/sửa partner với Zod validation.
### Security
- Thêm input validation cho tất cả field.
- Rate limiting 30 req/phút cho API partner.
### Files changed
- `src/app/api/partners/route.ts` (NEW)
- `src/app/dashboard/partners/page.tsx` (NEW)
- `prisma/schema.prisma` (MODIFIED — thêm model Partner)
- `docs/DATABASE.md` (UPDATED)

## [2026-04-10] — Module Auth (Mẫu)
### Added
- Login/Logout with JWT.
- Middleware auth check.
- Role-based access control.
### Files changed
- `src/lib/auth.ts` (NEW) ⚠️ PROTECTED
- `src/middleware.ts` (NEW) ⚠️ PROTECTED
