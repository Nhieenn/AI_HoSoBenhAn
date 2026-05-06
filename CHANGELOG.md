# CHANGELOG

## [Unreleased] - 2026-05-06
### Added
- **PROJECT_STATUS.md:** Tạo báo cáo tiến độ chi tiết, đánh giá thực trạng POC, giải thích kiến trúc Local LLM (On-Premise) và nút thắt dữ liệu RAG.
- **Quy tắc AI (RULES.md):** Bổ sung chỉ thị bắt buộc các AI Agent tương lai phải đọc `RUN_GUIDE.md` và `PROJECT_STATUS.md` trước khi thao tác.
- **Rule Đa bệnh lý (Multi-morbidity):** Bổ sung Expert Rule vào `generator.py` để chẩn đoán song song bệnh Parkinson (dựa trên "run lắc + chậm chạp") kết hợp cùng kết quả RAG.
- **Vector Database Integration (Phase 2):** Khởi tạo và tích hợp ChromaDB (`vector_db/`) để thay thế bộ máy TF-IDF tĩnh.
- **Data Ingestion Pipeline (`ai_engine/core/ingestor.py`):** 
  - Khả năng đọc, băm nhỏ (chunking) file PDF Y khoa thực tế.
  - Tự động trích xuất Tên Bệnh từ tiêu đề PDF và gán vào thẻ `metadata["disease"]`.
- **Hệ AI Nhúng Đa Ngôn Ngữ:** Áp dụng model `keepitreal/vietnamese-sbert` để nhúng văn bản (Embedding) sang không gian Vector.
- **Mass Data Ingestion:** Nạp thành công toàn bộ **1.251 bệnh lý nội/ngoại khoa** vào ChromaDB chuẩn bị cho Demo.
- Thêm các kịch bản Demo (`scratch/demo_pdf_parser.py`, `scratch/generate_mock_pdf.py`).

### Changed
- **Lọc rác SEO (Data Cleaning):** Cập nhật `clean_kb.py` sử dụng Regex để bóc tách và vứt bỏ phần văn bản quảng cáo, chỉ nạp "Triệu chứng" cốt lõi vào Vector DB nhằm tăng độ tinh khiết cho thuật toán RAG.
- **Hướng dẫn khởi động (RUN_GUIDE.md):** Cập nhật chi tiết luồng chạy Terminal, định vị port 8000 và kịch bản Test "Happy Path" cho BA/Sếp.
- **Từ điển NER (`ner.py`):** Bổ sung thêm cụm từ khóa lâm sàng (đau quặn, chậm chạp, vùng bụng dưới...).
- **`ai_engine/core/rag.py`:** Trả về đầy đủ metadata trong Citations.
- **`ai_engine/core/generator.py`:**
  - Chuyển logic truy xuất Tên Bệnh: Ưu tiên đọc từ `metadata["disease"]`.
  - Tối ưu hóa luật (Rule) "Suy tim" để bớt độ nhạy, bắt buộc phải có kèm triệu chứng *khó thở* và *tĩnh mạch* / *phù*.
- Cập nhật `.gitignore` để không push thư mục lớn (`vector_db/`, `ai_engine/models/`) lên Git.

### Fixed
- **Lỗi kết nối API:** Sửa proxy ở `src/app/api/proxy/[...path]/route.ts` trỏ đúng về Port `8000` của FastAPI, chấm dứt tình trạng Web báo lỗi Inference Engine.
- **Sửa lỗi Vector Mù:** Sửa lỗi hệ thống sinh văn bản bắt nhầm bệnh do thiếu RAG metadata.

## [Phase 1 POC] - 2026-05-04
- Khởi tạo kiến trúc Frontend (Next.js) và Backend (FastAPI).
- Tích hợp mô hình PhoBERT-base-v2 (Zero-shot) cho module bóc tách thực thể.
- Xây dựng hệ thống sinh Bệnh án theo Template.
