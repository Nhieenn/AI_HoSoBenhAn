# Project Rules — AI_HoSoBenhAn

# Văn bản này là QUY TẮC BẮT BUỘC. AI Agent PHẢI đọc trước khi code.

## NGUYÊN TẮC TUYỆT ĐỐI

1. KHÔNG BAO GIỜ xoá hoặc viết lại code đang hoạt động mà không hỏi trước
2. KHÔNG BAO GIỜ dùng raw SQL — chỉ dùng ORM (Prisma/Sequelize/TypeORM)
3. KHÔNG BAO GIỜ skip validation đầu vào ở bất kỳ API nào
4. KHÔNG BAO GIỜ hardcode credentials, tokens, secrets
5. PHẢI đọc CRITICAL_PATHS.md trước khi sửa bất kỳ file backend nào
6. PHẢI đọc DATABASE.md trước khi thêm/sửa bảng hoặc quan hệ
7. PHẢI chạy build test trước khi báo "hoàn thành"

## PROTECTED FILES — KHÔNG ĐƯỢC SỬA

### System Core & Auth (QC Pass: 2026-05-04)
- src/lib/auth.ts          ← Luồng xác thực
- src/middleware.ts         ← Middleware bảo mật
- prisma/schema.prisma     ← Chỉ sửa khi được yêu cầu rõ ràng
- nginx.conf               ← Cấu hình reverse proxy

### Module 1: Chuẩn hóa & Xử lý văn bản (QC Pass: 2026-05-05)
- ai_engine/core/normalization.py

### Module 2: Ẩn danh dữ liệu / De-identification (QC Pass: 2026-05-05)
- ai_engine/core/deid.py

### Module 3: Trích xuất khái niệm lâm sàng / NER (QC Pass: 2026-05-05)
- ai_engine/core/ner.py

### Module 4: Sinh nháp / Generation (QC Pass: 2026-05-05)
- ai_engine/core/generator.py

### Module 5: Truy hồi và Neo đầu ra / RAG (QC Pass: 2026-05-05)
- ai_engine/core/rag.py

### Module 6: Kiểm soát an toàn và Workflow (QC Pass: 2026-05-05)
- ai_engine/core/safety.py
- ai_engine/core/workflow.py

### Module 7: Audit và Bảo mật (QC Pass: 2026-05-05)
- ai_engine/core/audit.py

### AI Inference Engine Entry (QC Pass: 2026-05-05)
- ai_engine/main.py

# Cập nhật danh sách này khi có thêm file critical

## QUY TẮC KHI CODE

1. Chỉ sửa đúng file và đúng function được yêu cầu
2. KHÔNG refactor, rename, hoặc "cải thiện" code khác
3. KHÔNG xoá comment hoặc code "không dùng"
4. Nếu thấy code "có vấn đề" → BÁO cho user, KHÔNG tự sửa
5. Trước khi code: liệt kê file sẽ sửa → chờ xác nhận

## TRƯỚC KHI BẮT ĐẦU SESSION

1. Đọc RULES.md (file này)
2. Đọc docs/ARCHITECTURE.md
3. Đọc docs/CRITICAL_PATHS.md nếu sửa backend
4. Đọc docs/DATABASE.md nếu liên quan database
5. Đọc docs/GIT_WORKFLOW.md để tuân thủ quy tắc quản lý mã nguồn
6. Chủ động đọc REQUIREMENTS.md và CHANGELOG.md để nắm bắt bối cảnh và yêu cầu chi tiết

# Codex sẽ xem xét kết quả của bạn khi bạn hoàn tất.
