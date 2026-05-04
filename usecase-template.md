```
## Module: Quản Lý Người Dùng

### UC-01: Đăng nhập hệ thống
- Ưu tiên: MUST
- Actor: Admin, Nhân viên
- Mô tả: Người dùng nhập email + mật khẩu để truy cập hệ thống
- Luồng chính:
  1. Nhập email + password
  2. Hệ thống xác thực
  3. Redirect về Dashboard theo role
- Luồng ngoại lệ:
  - Sai mật khẩu 5 lần → khoá 15 phút
  - Tài khoản bị disable → thông báo liên hệ admin

### UC-02: Quản lý CRUD nhân viên
- Ưu tiên: MUST
- Actor: Admin
- Mô tả: Thêm/sửa/xoá/xem danh sách nhân viên
- Dữ liệu: Họ tên, email, SĐT, phòng ban, chức vụ, trạng thái
- Phân trang: 20 bản ghi/trang, có search + filter
```
