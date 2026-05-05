# Changelog

All notable changes to the ViMedAI project will be documented in this file.

## [Unreleased]

### Added
- **Module 3: Trích xuất khái niệm lâm sàng (NER)** (`ai_engine/core/ner.py`, `ai_engine/test_ner.py`)
  - **UC-NER-01**: Nhận dạng 6 loại thực thể y khoa (DISEASE, SYMPTOM, DRUG, DOSAGE, TEST, PROCEDURE) bằng rule-based Regex và Dictionary.
  - **UC-NER-02**: Logic phân tích bối cảnh phủ định ("không", "chưa") trong phạm vi mệnh đề, phân tách tự động theo dấu câu để bảo vệ các thực thể khẳng định đi kèm.
  - **UC-NER-03**: Map tự động thực thể trích xuất với mã tiêu chuẩn Ontology (ICD-10, LOINC, ATC) dựa trên từ điển mô phỏng.
- Tích hợp endpoint POST `/extract` vào Inference Engine (`ai_engine/main.py`) để frontend/backend giao tiếp xử lý NER.
