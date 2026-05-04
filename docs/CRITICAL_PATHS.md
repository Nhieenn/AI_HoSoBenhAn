# Critical Paths — ViMedAI

## 1. Luồng Tóm tắt xuất viện (Discharge Summary Flow)
Đây là luồng nghiệp vụ quan trọng nhất, kết hợp nhiều module AI.
- **Bước 1:** Nhận dữ liệu từ HIS (`/api/documents/ingest`).
- **Bước 2:** Chạy Sidecar De-identification (`ai-engine/core/deid.py`).
- **Bước 3:** NER trích xuất thực thể lâm sàng (`ai-engine/core/ner.py`).
- **Bước 4:** RAG tìm kiếm template & phác đồ (`ai-engine/core/rag.py`).
- **Bước 5:** LLM sinh nháp (`ai-engine/core/generator.py`).
- **Bước 6:** Bác sĩ review và duyệt trên UI (`src/app/drafts/[id]/page.tsx`).
- **Bước 7:** Đồng bộ dữ liệu sạch về HIS.

## 2. Luồng Bảo vệ dữ liệu (PHI Protection Path)
Đảm bảo không có dữ liệu thật nào bị rò rỉ.
- **File quan trọng:** 
  - `src/lib/encryption.ts` (Mã hóa lưu trữ).
  - `ai-engine/core/deid.py` (Logic mask thông tin).
- **Quy tắc:** Mọi dữ liệu đi vào AI Engine phải qua hàm `mask_phi()` trước.

## 3. Danh sách PROTECTED FILES (KHÔNG ĐƯỢC SỬA TÙY TIỆN)
- `src/lib/auth.ts`: Logic xác thực đa tầng.
- `ai-engine/core/deid.py`: Module ẩn danh cốt lõi.
- `prisma/schema.prisma`: Cấu trúc DB y khoa.
- `src/middleware.ts`: Chặn truy cập trái phép cấp mạng.
