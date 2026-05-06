# Database Schema — ViMedAI
Cập nhật: 04/05/2026

## 1. Quy Tắc Thiết Kế
- **Bảo mật:** Dữ liệu PHI (Tên, SĐT...) phải được mã hóa ở mức ứng dụng trước khi lưu (AES-256).
- **Soft Delete:** Sử dụng `deletedAt` cho mọi bảng quan trọng.
- **Audit Trail:** Mọi thay đổi dữ liệu lâm sàng phải được ghi log ID người thực hiện.

## 2. Các Bảng Dữ Liệu

### Bảng: `User` (Nhân viên y tế)
| Cột | Type | Constraint | Mô tả |
| --- | --- | --- | --- |
| id | String | PK, cuid() | |
| username | String | UNIQUE | |
| password | String | | Bcrypt hash |
| role | Enum | DOCTOR, ADMIN, NURSE, RESEARCHER | Phân quyền RBAC |
| departmentId | String | FK | Khoa/Phòng làm việc |

### Bảng: `MedicalRecord` (Hồ sơ gốc từ HIS)
| Cột | Type | Constraint | Mô tả |
| --- | --- | --- | --- |
| id | String | PK | ID đồng bộ từ HIS |
| rawContent | Text | | Nội dung thô chưa xử lý |
| deidentifiedContent | Text | | Nội dung sau khi qua module De-id |
| patientIdHash | String | INDEX | Mã bệnh nhân đã được hash |
| status | Enum | PENDING, PROCESSED, ERROR | Trạng thái xử lý AI |

### Bảng: `AIDraft` (Bản thảo do AI sinh)
| Cột | Type | Constraint | Mô tả |
| --- | --- | --- | --- |
| id | String | PK | |
| recordId | String | FK | Liên kết MedicalRecord |
| content | Json | | Chứa 6 section tóm tắt xuất viện |
| doctorId | String | FK | Bác sĩ phụ trách review |
| status | Enum | DRAFT, APPROVED, REJECTED | |
| version | Int | DEFAULT 1 | |

### Bảng: `NormalizationDict` (Từ điển viết tắt/thuật ngữ)
| Cột | Type | Constraint | Mô tả |
| --- | --- | --- | --- |
| id | String | PK | |
| abbr | String | INDEX | Từ viết tắt (vd: BN) |
| fullText | String | | Nghĩa đầy đủ (vd: Bệnh nhân) |
| category | Enum | DRUG, SYMPTOM, ADMIN | Loại thuật ngữ |
| departmentId | String | FK (Nullable) | Dùng chung hoặc theo khoa |

### Bảng: `AuditLog` (Nhật ký hệ thống)
| Cột | Type | Constraint | Mô tả |
| --- | --- | --- | --- |
| id | String | PK | |
| userId | String | FK | Người thực hiện |
| action | String | | LOGIN, GENERATE, EDIT, APPROVE |
| targetId | String | | ID của object bị tác động |
| diff | Json | | Thay đổi trước và sau khi Edit |

## 3. Sơ Đồ Quan Hệ
- `User` (1) ── (N) `AIDraft` (Bác sĩ quản lý bản thảo)
- `MedicalRecord` (1) ── (N) `AIDraft` (Một hồ sơ có thể có nhiều phiên bản nháp)
- `Department` (1) ── (N) `User`
- `Department` (1) ── (N) `NormalizationDict` (Từ điển theo khoa)

## 4. Quy Tắc Migration
1. Không thay đổi schema trực tiếp trên DB production.
2. Mọi script migration phải nằm trong folder `prisma/migrations`.
3. Kiểm tra tính tương thích ngược (Backward compatibility) trước khi deploy.
