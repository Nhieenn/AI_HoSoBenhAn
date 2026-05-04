# Kiến Trúc Hệ Thống — ViMedAI
Cập nhật: 04/05/2026

## 1. Tổng Quan
ViMedAI là một hệ thống AI hỗ trợ ghi chép y tế tiếng Việt, được thiết kế để triển khai **On-premise** nhằm đảm bảo an toàn dữ liệu bệnh nhân (PHI). Hệ thống sử dụng kiến trúc Hybrid kết hợp giữa Web Management và AI Inference Engine chuyên biệt.

## 2. Tech Stack Đề Xuất
### Frontend & Management API
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **State Management:** React Query / Zustand
- **UI:** Tailwind CSS + ShadcnUI (Giao diện hiện đại, tối ưu cho bác sĩ)

### AI Inference Engine (Backend Services)
- **Framework:** FastAPI (Python) - Phù hợp nhất cho xử lý AI và GPU.
- **AI Models:**
  - LLM: PhoGPT-7B hoặc tương đương (Fine-tuned cho y khoa).
  - NER/De-id: Spacy hoặc Transformer-based (mô hình Sidecar chuyên biệt).
- **RAG Engine:** LangChain / LlamaIndex.
- **Vector Database:** ChromaDB hoặc Milvus (Triển khai On-premise).

### Persistence & Infrastructure
- **Database:** PostgreSQL (Lưu trữ metadata, users, audit logs).
- **ORM:** Prisma.
- **Cache & Queue:** Redis (Quản lý các tác vụ AI chạy ngầm).
- **Deployment:** Docker & Docker Compose (Dễ dàng triển khai trên hạ tầng máy chủ bệnh viện).

## 3. Cấu Trúc Thư Mục
```
/
├── prisma/               # Database schema & migrations
├── docs/                 # Tài liệu Technical Design
├── src/
│   ├── app/              # Next.js pages & API routes
│   ├── components/       # UI components (Review UI, Dashboard)
│   ├── lib/              # Core logic (Auth, Encryption, DB client)
│   ├── services/         # Integration with AI Engine & HIS
│   └── types/            # TypeScript interfaces
├── ai-engine/            # (Python) FastAPI Service
│   ├── models/           # Local LLM & NER weights
│   ├── core/             # Logic De-id, RAG, Generation
│   └── main.py           # API entry point for AI tasks
└── docker-compose.yml    # Orchestration
```

## 4. Sơ Đồ Luồng Dữ Liệu Tổng Thể (Data Flow)
1.  **Input:** HIS đẩy dữ liệu thô (free-text hoặc cấu trúc) qua API.
2.  **De-id:** `ai-engine` nhận text -> Tự động ẩn danh PHI -> Lưu bản lưu ẩn danh.
3.  **Process:**
    *   **NER:** Trích xuất thực thể y khoa.
    *   **RAG:** Tìm kiếm phác đồ/template tương ứng trong Vector DB.
    *   **Generation:** LLM tổng hợp nháp dựa trên dữ liệu đã ẩn danh và tri thức RAG.
4.  **Safety:** Lớp kiểm soát kiểm tra mâu thuẫn lâm sàng và hallucination.
5.  **Review:** Nháp hiển thị trên Web UI để Bác sĩ chỉnh sửa/phê duyệt.
6.  **Output:** Sau khi duyệt, hệ thống gỡ bỏ mã giả danh (Re-identify) và đẩy về HIS/EHR.

## 5. Các Service Bên Ngoài
- **HIS/PACS/LIS:** Hệ thống thông tin bệnh viện hiện có (Tích hợp qua HL7/FHIR).
- **Local GPU Node:** Hạ tầng máy chủ nội bộ phục vụ Inference.
- *Lưu ý: Không sử dụng API ngoài (OpenAI/Cloud) để bảo mật tuyệt đối.*
