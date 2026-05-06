# CHANGELOG

## [Unreleased] - 2026-05-06
### Added
- **Vector Database Integration (Phase 2):** Khởi tạo và tích hợp ChromaDB (`vector_db/`) để thay thế bộ máy TF-IDF tĩnh.
- **Data Ingestion Pipeline (`ai_engine/core/ingestor.py`):** 
  - Khả năng đọc, băm nhỏ (chunking) file PDF Y khoa thực tế.
  - Tự động trích xuất Tên Bệnh từ tiêu đề PDF và gán vào thẻ `metadata["disease"]`.
- **Hệ AI Nhúng Đa Ngôn Ngữ:** Áp dụng model `keepitreal/vietnamese-sbert` để nhúng văn bản (Embedding) sang hệ tọa độ không gian Vector đa chiều.
- **Mass Data Ingestion:** Nạp thành công toàn bộ **1.251 bệnh lý nội khoa** từ `knowledge_base.json` vào ChromaDB thông qua script `ingest_full_kb.py`, chuẩn bị cho Demo.
- Thêm các kịch bản Demo (`scratch/demo_pdf_parser.py`, `scratch/generate_mock_pdf.py`).

### Changed
- **`ai_engine/core/rag.py`:** Chuyển đổi cấu trúc `BaseRetriever` sang dùng `ChromaRetriever` làm mặc định, trả về đầy đủ metadata trong Citations.
- **`ai_engine/core/generator.py`:**
  - Chuyển logic truy xuất Tên Bệnh: Ưu tiên đọc từ `metadata["disease"]` thay vì dùng split chuỗi thủ công.
  - Xóa bỏ điểm yếu "Tam sao thất bản": Thay vì chỉ query RAG bằng các triệu chứng bị NER lọc sót, hệ thống giờ đây query bằng **nguyên văn lời kể của bệnh nhân** (raw reason) để đảm bảo không rớt chữ.
  - Tối ưu hóa luật (Rule) "Suy tim" để bớt độ nhạy, bắt buộc phải có kèm triệu chứng *khó thở* và *tĩnh mạch* / *phù*.
- Cập nhật `.gitignore` để không push các thư mục dữ liệu lớn (`vector_db/`, `ai_engine/models/`) lên Git.

### Fixed
- Lỗi hiển thị nguyên câu văn dài thay vì tên bệnh khi kết quả RAG không có định dạng dấu `:`.
- Lỗi AI đoán sai bệnh ("Suy thượng thận", "Trật khuỷu tay") do quá trình trích xuất NER (PhoBERT) bỏ sót keyword quan trọng như "mắt lồi", "tay run".

## [Phase 1 POC] - 2026-05-04
- Khởi tạo kiến trúc Frontend (Next.js) và Backend (FastAPI).
- Tích hợp mô hình PhoBERT-base-v2 (Zero-shot) cho module bóc tách thực thể.
- Xây dựng hệ thống sinh Bệnh án theo Template.
