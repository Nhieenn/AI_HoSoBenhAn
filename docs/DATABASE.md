# Database Schema — AI_HoSoBenhAn
# Cập nhật: 04/05/2026

## Quy Tắc
- KHÔNG xoá cột đang có data — đánh dấu deprecated
- KHÔNG đổi tên bảng — chỉ thêm mới
- Mọi bảng PHẢI có: id, createdAt, updatedAt
- Soft delete: dùng cột deletedAt thay vì xoá thật
- Mọi migration phải test trên staging trước

## Bảng: User
| Cột         | Type     | Constraint     | Mô tả              |
|-------------|----------|----------------|---------------------|
| id          | String   | PK, cuid()     | ID tự động          |
| email       | String   | UNIQUE, NOT NULL| Email đăng nhập    |
| password    | String   | NOT NULL       | Bcrypt hash         |
| name        | String   |                | Họ tên              |
| role        | Enum     | DEFAULT 'USER' | ADMIN/MANAGER/USER  |
| status      | Enum     | DEFAULT 'ACTIVE'| ACTIVE/INACTIVE    |
| createdAt   | DateTime | DEFAULT now()  |                     |
| updatedAt   | DateTime | Auto update    |                     |

## Quan Hệ
User 1 ── N Transaction  (userId FK)
User 1 ── 1 Profile      (userId FK, UNIQUE)
Partner 1 ── N BankAccount (partnerId FK)
