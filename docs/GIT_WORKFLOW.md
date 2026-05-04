# Quy chuẩn làm việc với Git — ViMedAI
Cập nhật: 04/05/2026

Tài liệu này quy định cách quản lý mã nguồn, đặt tên nhánh, commit message và gắn thẻ (tag) cho dự án ViMedAI. Mọi thành viên và AI Agent **PHẢI** tuân thủ quy trình này để đảm bảo tính nhất quán.

## 1. Chiến lược phân nhánh (Branching Strategy)
Dự án áp dụng mô hình phân nhánh dựa trên tính năng (Feature Branch Workflow):

- **`main`**: Nhánh chính (Production). Code trên nhánh này phải luôn ổn định, đã qua kiểm duyệt và sẵn sàng để deploy. KHÔNG bao giờ commit trực tiếp lên `main`.
- **`feature/*`**: Nhánh để phát triển tính năng hoặc module mới.
  - *Định dạng:* `feature/<tên-tính-năng-hoặc-module>`
  - *Ví dụ:* `feature/module-1-normalization`, `feature/deid-ner-integration`
- **`fix/*` / `hotfix/*`**: Nhánh dùng để sửa lỗi.
  - *Ví dụ:* `fix/deid-regex-bug`, `hotfix/login-crash`
- **`docs/*`**: Nhánh dùng riêng cho việc cập nhật tài liệu.

## 2. Quy chuẩn Commit Message (Conventional Commits)
Mọi commit message phải tuân theo chuẩn cấu trúc sau:
`<type>(<scope>): <mô tả ngắn gọn>`

### Các `<type>` được phép sử dụng:
- **`feat`**: Thêm một tính năng/module mới (vd: `feat(module1): add normalization logic`)
- **`fix`**: Sửa lỗi mã nguồn (vd: `fix(deid): fix regex pattern for phone numbers`)
- **`docs`**: Chỉ thay đổi tài liệu (vd: `docs: update architecture diagram`)
- **`refactor`**: Sửa đổi code nhưng không thay đổi chức năng (vd: `refactor(api): restructure dictionary endpoints`)
- **`test`**: Thêm hoặc sửa test case (vd: `test(ai-engine): add unit test for NER`)
- **`chore`**: Cập nhật cấu hình build, dependencies (vd: `chore: update next.js to 14.2.3`)

### Quy tắc bổ sung cho Commit:
- Viết bằng tiếng Anh.
- Viết thường (lowercase) ở đầu câu, không dùng dấu chấm câu ở cuối.
- Dùng thì hiện tại (ví dụ: dùng `add` thay vì `added` hay `adds`).

## 3. Quy trình làm việc (Workflow)
1. **Khởi tạo nhánh:** Trước khi bắt đầu task, tạo nhánh mới từ `main` (hoặc `develop` nếu có):
   `git checkout -b feature/tên-chức-năng`
2. **Code & Kiểm chứng:** Tuân thủ 4 bước Verification (Build, Type, Functional, Security) trước khi commit.
3. **Commit:** Nhóm các thay đổi có ý nghĩa vào một commit sử dụng Conventional Commits.
4. **Merge & Tag:** Khi một Module hoặc Milestone hoàn thành, merge vào nhánh chính và tạo Tag:
   `git tag -a v<version>-<module> -m "Mô tả hoàn thành"`
   *(Ví dụ: `git tag -a v0.1.0-module1 -m "Module 1 Completed"`)*

Tuân thủ nghiêm ngặt quy trình này sẽ giúp việc review code và quản lý phiên bản của ViMedAI trở nên dễ dàng và an toàn hơn.
