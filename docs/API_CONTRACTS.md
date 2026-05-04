# API Contracts — ViMedAI

## 1. Authentication
### POST `/api/auth/login`
- **Auth:** Public
- **Body:** `{ username, password }`
- **Response 200:** `{ token, user: { id, role, dept } }`

---

## 2. Document Processing
### POST `/api/documents/ingest`
- **Desc:** Nhận dữ liệu từ HIS và khởi chạy pipeline AI.
- **Auth:** Required (System/Admin)
- **Body:** `{ externalId, patientId, content, type: 'RADIOLOGY' | 'DISCHARGE' }`
- **Response 202:** `{ jobId, status: 'PROCESSING' }`

### GET `/api/documents/:id/status`
- **Desc:** Kiểm tra trạng thái xử lý AI.
- **Response 200:** `{ status: 'COMPLETED', draftId: '...' }`

---

## 3. AI Drafts (Bác sĩ Workflow)
### GET `/api/drafts`
- **Desc:** Lấy danh sách bản thảo cần duyệt.
- **Query:** `?deptId=...&status=DRAFT`
- **Response 200:** `{ data: AIDraft[] }`

### GET `/api/drafts/:id`
- **Desc:** Xem chi tiết bản thảo kèm trích dẫn RAG.
- **Response 200:** 
  ```json
  {
    "id": "...",
    "content": { "section_1": "...", "section_2": "..." },
    "citations": [ { "text": "...", "source": "Phác đồ BYT 2024" } ],
    "uncertainty_flags": [ { "field": "medication", "reason": "Dose unclear" } ]
  }
  ```

### PUT `/api/drafts/:id`
- **Desc:** Cập nhật bản thảo sau khi bác sĩ sửa.
- **Body:** `{ content: { ... }, status: 'APPROVED' | 'REJECTED' }`
- **Response 200:** `{ success: true }`

---

## 4. Dictionary Management
### GET `/api/admin/dictionary`
- **Query:** `?search=...&deptId=...`
- **Response 200:** `[ { abbr, fullText, ... } ]`

### POST `/api/admin/dictionary`
- **Body:** `{ abbr, fullText, departmentId, category }`
- **Response 201:** `{ success: true }`

---

## 5. RAG & Knowledge Base
### POST `/api/rag/upload-protocol`
- **Desc:** Upload phác đồ điều trị mới để index vào Vector DB.
- **Auth:** Admin
- **Body:** FormData (PDF/Docx file)
- **Response 200:** `{ indexed_nodes: 45 }`
