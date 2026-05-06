# BÁO CÁO TIẾN ĐỘ DỰ ÁN VIMED-AI (GIAI ĐOẠN POC)

**Cập nhật lần cuối:** Hôm nay
**Mục đích:** Đánh giá tình trạng dự án hiện tại, tóm tắt các giới hạn kỹ thuật và làm cơ sở (context) cho các phiên làm việc tiếp theo với AI hoặc trình bày với Ban Giám đốc (BA/Sếp).

---

## 1. NHỮNG THÀNH TỰU ĐÃ ĐẠT ĐƯỢC (ACHIEVED)

Hệ thống đã chứng minh được tính khả thi (Proof of Concept) của quy trình chẩn đoán tự động hoàn toàn không có sự can thiệp của con người, bao gồm:

- **Hoàn thiện Kiến trúc Pipeline (4 Bước):**
  - (1) Trích xuất thực thể NER.
  - (2) Truy hồi kiến thức Vector RAG.
  - (3) Rào chắn an toàn (Safety Gates).
  - (4) Sinh bệnh án tự động (Generator).
- **Tích hợp hệ thống:** Kết nối mượt mà giữa Frontend (Next.js) và Lõi AI Backend (FastAPI) qua Proxy, giải quyết triệt để lỗi CORS và sai lệch cổng (Port 8000).
- **Xây dựng CSDL Kiến thức (Vector Database):** Cào, lọc rác SEO và vector hóa thành công 1.251 bệnh lý từ YouMed/SBB vào ChromaDB (dùng mô hình nhúng `vietnamese-sbert`).
- **Triển khai Cơ chế An toàn (Hallucination Prevention):** Hệ thống đã biết "nhận ngu" - tự động văng lỗi `[CHƯA RÕ CHẨN ĐOÁN]` khi dữ liệu RAG mâu thuẫn với triệu chứng, tuyệt đối không chẩn đoán bừa để bảo vệ sinh mạng bệnh nhân.
- **Sẵn sàng triển khai (Staging):** Nhánh `demo` đã được dọn dẹp sạch sẽ (loại bỏ các file Models/DB nặng), sẵn sàng cho Sếp clone về server nội bộ.

---

## 2. NHỮNG HẠN CHẾ HIỆN TẠI (LIMITATIONS)

Đây là các điểm yếu cố hữu của phiên bản POC hiện tại do thiếu hụt tài nguyên:

- **Tầng Sinh văn bản (Generator) đang giả lập:** Do chưa có Server GPU, hệ thống chưa thể chạy các Mô hình Ngôn ngữ Lớn (LLM) thực thụ. Hiện tại đang phải dùng mã code cứng (Rule-based If/Else) để đánh giá kết quả từ RAG, dẫn đến thiếu linh hoạt.
- **Nhận diện thực thể (NER) còn hạn chế:** NER hiện đang phụ thuộc nhiều vào Regex (Từ khóa). Nếu người dùng nhập các từ khóa không có sẵn trong thư viện (VD: "chậm chạp", "run lắc"), hệ thống sẽ không trích xuất được triệu chứng để đưa vào RAG.
- **Chất lượng dữ liệu RAG chưa đạt chuẩn Y khoa:** Dữ liệu hiện tại cào từ các trang web đại chúng (YouMed, SBB). Nhiều bài báo không mô tả triệu chứng hoặc viết lan man, khiến Vector Search bị mất phương hướng (VD: vụ án U nang buồng trứng xoắn).

---

## 3. KHÚC MẮC & VẤN ĐỀ CẦN XEM XÉT (BOTTLENECKS & CONSIDERATIONS)

Để dự án chuyển từ POC sang Production (Thực tế), chúng ta bắt buộc phải giải quyết 3 bài toán sau:

### 3.1. Nút thắt Phần cứng vs. Yêu cầu Bảo mật (Hardware Bottleneck)

- **Vấn đề:** BA yêu cầu 100% On-Premise (Local), tuyệt đối không dùng API ngoài (như OpenAI) để bảo vệ PHI (Dữ liệu y tế cá nhân).
- **Giải pháp:** Bắt buộc phải triển khai Local LLM (Ollama / vLLM chạy mô hình PhoGPT-7B hoặc Llama-3).
- **Yêu cầu:** Đề xuất Ban Giám đốc cấp máy chủ nội bộ có Card đồ họa (GPU - Tối thiểu Nvidia RTX 3090/4090 hoặc A100) để đảm bảo tốc độ phản hồi < 2 giây.

### 3.2. Nút thắt Thuật toán Tìm kiếm (Lexical vs Semantic)

- **Vấn đề:** Thuật toán Vector hiện tại dễ bị đánh lừa bởi từ vựng trùng lặp. (VD: "Ngón cái và ngón trỏ khép mở" ưu tiên tìm ra bệnh *Viêm khớp ngón tay* thay vì *Parkinson*).
- **Giải pháp:** Cần Fine-tune lại mô hình Embedding riêng cho Y khoa, đồng thời áp dụng kiến trúc Hybrid Search (Kết hợp Vector Search + Keyword Search truyền thống).

### 3.3. Chất lượng Dữ liệu Đầu vào (Garbage In -> Garbage Out)

- **Vấn đề:** AI không thể chẩn đoán đúng nếu đọc sách sai.
- **Giải pháp:** Dừng sử dụng dữ liệu web đại chúng. Yêu cầu Bệnh viện cung cấp bộ **Phác đồ Điều trị chuẩn của Bộ Y Tế** để AI học lại. Đồng thời, cần nguồn lực Bác sĩ nội trú hỗ trợ gán nhãn (Labeling) 5,000 bệnh án cũ để tinh chỉnh (Fine-tune) văn phong của AI.

---

## 4. CHIẾN LƯỢC CÀO VÀ LỌC DỮ LIỆU (DATA INGESTION PIPELINE)
Để phục vụ yêu cầu đa dạng hóa bệnh lý, team đã xây dựng một Pipeline xử lý dữ liệu tự động:
- **Thu thập (Scraping):** Cào toàn bộ 1.251 bệnh lý nội/ngoại khoa từ 2 trang bách khoa Y tế (YouMed và SBB).
- **Vấn đề "Rác SEO":** Đa số các bài viết trên mạng chứa 70% là câu chữ quảng cáo, dẫn dắt (SEO) và chỉ 30% là kiến thức y khoa thực sự (Triệu chứng, Nguyên nhân). Nếu đưa trực tiếp vào AI, AI sẽ bị "nhiễu" và mất tập trung.
- **Khử nhiễu (Cleaning):** Áp dụng thuật toán bóc tách Regex (`clean_kb.py`) để vứt bỏ toàn bộ các câu rác (VD: *"Cùng bác sĩ tìm hiểu nhé"*, *"Bài viết này mang đến..."*). Chỉ chắt lọc và giữ lại phần lõi chứa Triệu chứng (Core Symptoms).
- **Kết quả:** Vector DB hiện tại chứa những "viên nén tri thức" đậm đặc, giúp hệ thống RAG so khớp ngữ nghĩa (Semantic Search) chính xác và nhanh hơn rất nhiều.

---

## 5. BẢN CHẤT CỦA NHÁNH DEMO HIỆN TẠI (THE NATURE OF THIS DEMO)
Cần quán triệt rõ tinh thần với BA và Sếp trước buổi trình diễn (Showcase):
- **Bản chất nhánh `demo`:** Đây là một **"Bộ Khung Xương" (Architecture Pipeline)**. Nhiệm vụ của nó là chứng minh đường ống xử lý dữ liệu (Từ lúc nhập liệu -> Kiểm duyệt bảo mật -> RAG tìm kiếm -> Sinh bệnh án tự động) hoạt động trơn tru, khép kín và an toàn 100% On-Premise.
- **Không phải là "Bách khoa toàn thư" (Chưa phải lúc):** Buổi demo KHÔNG dùng để "thách đố" AI các ca bệnh siêu khó nằm ngoài kịch bản. Lý do: Bộ não sinh văn bản (Generator) đang chạy bằng thuật toán giả lập tạm thời (Rule-based), chưa có Mô hình Ngôn ngữ Lớn (LLM) thực thụ do giới hạn máy chủ hiện tại không có GPU.
- **Thông điệp chiến lược (Key Takeaway):** Khi trình bày, cần nhấn mạnh với Sếp: *"Hạ tầng và Kiến trúc đã xây xong và rất vững chắc. Sự thông minh của AI ở Giai đoạn 2 phụ thuộc hoàn toàn vào việc Bệnh viện cấp **Phác đồ Điều trị chuẩn** (để thay thế dữ liệu web) và cấp **Máy chủ GPU** (để cắm Local LLM vào tầng Generator)."*
