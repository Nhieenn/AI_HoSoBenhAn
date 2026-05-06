HỌC VIỆN QUÂN Y

TÀI LIỆU PHÂN TÍCH NGHIỆP VỤ

BA Document

Hệ thống AI Tạo Sinh Chuyên Biệt

cho Ngôn Ngữ và Thuật Ngữ Y Khoa Tiếng Việt

Phiên bản: 1.0  |  Ngày: 04/05/2026

Đơn vị: Học viện Quân y

# MỤC LỤC

# 1. TỔNG QUAN DỰ ÁN

| Tên dự án | Hệ thống AI Tạo Sinh Y Khoa Tiếng Việt (ViMedAI) |
| --- | --- |
| Phiên bản tài liệu | 1.0 |
| Ngày tạo | 04/05/2026 |
| Đơn vị đề xuất | Học viện Quân y |
| Loại dự án | Nghiên cứu – Phát triển – Triển khai |
| Thời gian dự kiến | 12–24 tháng (Giai đoạn 1) |

## 1.1 Tóm tắt điều hành

Dự án xây dựng một hệ thống AI tạo sinh chuyên biệt cho ngôn ngữ và thuật ngữ y khoa tiếng Việt, nhằm tối ưu hóa quy trình ghi chép và báo cáo y tế. Hệ thống không thay thế bác sĩ viết bệnh án, mà hoạt động như một công cụ hỗ trợ soạn thảo có kiểm soát: đề xuất nháp, tiền điền biểu mẫu, chuẩn hóa cấu trúc báo cáo, mở rộng/giải nghĩa viết tắt và trích xuất khái niệm lâm sàng.

Kiến trúc được chọn là Hybrid SFT + Modular RAG + Sidecar IE/De-identification, triển khai on-premise để đảm bảo an toàn dữ liệu bệnh nhân.

# 2. BỐI CẢNH NGHIỆP VỤ

## 2.1 Vấn đề hiện tại

| # | Vấn đề | Tác động |
| --- | --- | --- |
| 1 | Bác sĩ tốn nhiều thời gian ghi chép bệnh án thủ công | Giảm thời gian khám chữa bệnh, tăng tải trọng hành chính |
| 2 | Thiếu nhất quán trong cách diễn đạt thuật ngữ và viết tắt giữa các bác sĩ, khoa, phòng | Khó tổng hợp dữ liệu thứ cấp cho nghiên cứu và kiểm định chất lượng |
| 3 | Viết tắt nội viện không có từ điển chuẩn hóa | Nguy cơ hiểu nhầm khi bàn giao ca, hội chẩn liên khoa |
| 4 | Cấu trúc báo cáo chẩn đoán hình ảnh không đồng nhất | Khó trích xuất dữ liệu tự động, khó so sánh ca bệnh theo chuỗi thời gian |
| 5 | Thiếu hạ tầng NLP y tế đặc thù cho tiếng Việt | Không thể tận dụng công nghệ AI sẵn có của quốc tế |

## 2.2 Cơ hội

* Nghiên cứu năm 2025 (Bui et al.) chứng minh fine-tune LLM tiếng Việt y khoa bằng LoRA/QLoRA với ~337.000 cặp dữ liệu cải thiện đáng kể chất lượng.
* Công nghệ PEFT (LoRA/QLoRA) cho phép huấn luyện trên hạ tầng GPU cục bộ với chi phí hợp lý.
* Bộ dữ liệu công khai (MIMIC-IV, VinDr-CXR) có thể dùng để bootstrap trước khi có dữ liệu nội bộ đủ lớn.
* Tiết kiệm thời gian ghi chép ước tính đến ~40% theo các nghiên cứu quốc tế.
# 3. CÁC BÊN LIÊN QUAN (STAKEHOLDERS)

## 3.1 Ma trận Stakeholders

| Stakeholder | Vai trò | Quyền lợi/Quan tâm chính | Mức độ ảnh hưởng |
| --- | --- | --- | --- |
| Ban Giám đốc Bệnh viện | Sponsor, phê duyệt ngân sách | Hiệu quả vận hành, tuân thủ pháp lý, an toàn bệnh nhân | Rất cao |
| Bác sĩ điều trị | Người dùng cuối chính | Tiết kiệm thời gian, độ tin cậy của nháp, không tăng gánh nặng kiểm tra | Rất cao |
| Bác sĩ chẩn đoán hình ảnh | Người dùng cuối (radiology) | Chuẩn hóa báo cáo, tốc độ | Cao |
| Điều dưỡng/Hành chính | Người dùng tiền điền biểu mẫu | Độ chính xác dữ liệu hành chính | Trung bình |
| Phòng Công nghệ thông tin | Triển khai và vận hành | Bảo mật, tích hợp HIS, hiệu năng | Cao |
| Phòng Pháp chế/Đạo đức | Tuân thủ pháp luật | Bảo vệ dữ liệu bệnh nhân, trách nhiệm pháp lý | Rất cao |
| Nhóm nghiên cứu/AI | Phát triển mô hình | Chất lượng dữ liệu, infrastructure, benchmark | Cao |
| Bệnh nhân | Người chịu tác động gián tiếp | An toàn thông tin cá nhân, chất lượng hồ sơ | Cao |
| Cơ quan quản lý nhà nước | Giám sát, phê duyệt | Tuân thủ luật KCB, bảo vệ dữ liệu cá nhân | Cao |

# 4. MỤC TIÊU NGHIỆP VỤ

## 4.1 Mục tiêu chiến lược

| Mã | Mục tiêu | Chỉ số đo lường | Mốc thời gian |
| --- | --- | --- | --- |
| BG-01 | Giảm thời gian ghi chép bệnh án hành chính và cấu trúc | Thời gian hoàn thành tài liệu giảm ≥ 20% so với baseline | Cuối Giai đoạn 2 (Assisted Mode) |
| BG-02 | Tăng tính nhất quán thuật ngữ và cấu trúc văn bản y tế | Tỷ lệ viết tắt không chuẩn trong bệnh án giảm ≥ 50% | Cuối Giai đoạn 1 |
| BG-03 | Tạo nền dữ liệu có cấu trúc cho nghiên cứu và kiểm định chất lượng | Volume dữ liệu cấu trúc hóa tăng; có thể truy vấn tự động | 24 tháng |
| BG-04 | Đảm bảo an toàn bệnh nhân và tuân thủ bảo mật dữ liệu | Không sự cố rò rỉ PHI; không hallucination nghiêm trọng trong ca triển khai | Từ ngày đầu pilot |
| BG-05 | Xây dựng năng lực nội bộ về AI y tế tiếng Việt | Có đội ngũ vận hành và phát triển mô hình in-house | 24 tháng |

## 4.2 Lưu ý – Không phải mục tiêu

> KHÔNG phải mục tiêu của Giai đoạn 1: Thay thế hoàn toàn bác sĩ trong viết bệnh án, triển khai sinh progress note tự do trên mọi chuyên khoa, hoặc ra quyết định lâm sàng tự động.

# 5. PHẠM VI DỰ ÁN

## 5.1 Trong phạm vi (In Scope)

| # | Chức năng | Giai đoạn ưu tiên |
| --- | --- | --- |
| 1 | Chuẩn hóa thuật ngữ y khoa (4 lớp: đồng nghĩa, viết tắt, hình thức, section) | Giai đoạn 1 |
| 2 | Ẩn danh dữ liệu PHI (De-identification): loại bỏ hoặc mã hóa thông tin định danh bệnh nhân nhằm đảm bảo bảo mật | Giai đoạn 1 – Bắt buộc |
| 3 | Trích xuất khái niệm lâm sàng (NER): nhận diện và trích xuất thực thể y khoa từ văn bản lâm sàng | Giai đoạn 1 |
| 4 | Giải nghĩa và mở rộng viết tắt nội viện: hỗ trợ hiểu và chuẩn hóa các viết tắt chuyên môn trong bệnh viện | Giai đoạn 1 |
| 5 | Cấu trúc hóa báo cáo chẩn đoán hình ảnh: chuyển dữ liệu thô sang định dạng báo cáo chuẩn hóa | Giai đoạn 1 – Use case ưu tiên |
| 6 | Sinh nháp discharge summary: tạo bản tóm tắt xuất viện tự động để bác sĩ chỉnh sửa | Giai đoạn 1 – Use case ưu tiên |
| 7 | Tiền điền tự động phần hành chính và trường facts: hỗ trợ điền trước các trường hành chính và clinical facts | Giai đoạn 1 |
| 8 | RAG nội bộ (phác đồ, mẫu biểu, từ điển thuật ngữ) | Giai đoạn 1 |
| 9 | Vòng duyệt bác sĩ (Assisted Mode): cho phép bác sĩ xem xét, chỉnh sửa và phê duyệt nội dung do AI tạo | Giai đoạn 2 |
| 10 | Audit log và active learning: ghi lại lịch sử thao tác hệ thống và cải thiện mô hình dựa trên phản hồi người dùng | Liên tục |

## 5.2 Ngoài phạm vi (Out Of Scope)

| Hạng mục | Lý do |
| --- | --- |
| Sinh progress note tự do đa chuyên khoa | Giai đoạn sau; rủi ro an toàn cao |
| Ra quyết định lâm sàng tự động | Ngoài phạm vi AI hỗ trợ có kiểm soát |
| Ứng dụng di động bệnh nhân | Không thuộc phạm vi dự án này |
| Dịch thuật đa ngôn ngữ | Ngoài scope tiếng Việt Giai đoạn 1 |
| Tích hợp thiết bị y tế (IoT/monitor) | Hạ tầng riêng, scope khác |
| Pretraining LLM từ đầu | Chi phí quá cao; không khả thi trong 12–24 tháng |
| Phân tích ảnh y khoa trực tiếp (vision model) | Giai đoạn sau |

# 6. YÊU CẦU NGHIỆP VỤ (BUSINESS REQUIREMENTS)

## BR-01: Chuẩn hóa thuật ngữ và viết tắt

Hệ thống phải chuẩn hóa 4 lớp biến thể ngôn ngữ trong văn bản y tế tiếng Việt:

* Đồng nghĩa khái niệm: Ánh xạ thuật ngữ thuần Việt, Hán-Việt, tiếng Anh và viết tắt về cùng canonical term.
* Viết tắt nội viện: Giải nghĩa viết tắt theo từ điển nội bộ, theo khoa/phòng và theo ngữ cảnh section.
* Biến thể hình thức: Chuẩn hóa có dấu/không dấu, đơn vị đo, ký tự đặc biệt, biểu thức số-chữ.
* Ngôn ngữ section: Phân biệt vai trò ngữ nghĩa của cùng một cụm từ khi xuất hiện ở section khác nhau.
Điều kiện chấp nhận: Accuracy giải nghĩa viết tắt nhóm nguy cơ cao ≥ 0,95.

## BR-02: Bảo vệ thông tin cá nhân bệnh nhân (PHI)

Mọi dữ liệu bệnh nhân phải được de-identify trước khi vào bất kỳ tác vụ downstream nào. Không có dữ liệu định danh nào được truyền ra ngoài network bệnh viện.

Điều kiện chấp nhận: Recall PHI ≥ 0,99 trên nhóm PHI nguy cơ cao; 0 sự cố rò rỉ dữ liệu.

## BR-03: Hỗ trợ sinh nháp có kiểm soát

Hệ thống hỗ trợ bác sĩ bằng cách sinh nháp ghi chép/báo cáo. Bác sĩ luôn là người phê duyệt cuối cùng trước khi lưu vào hồ sơ chính thức.

Điều kiện chấp nhận: Hallucination nghiêm trọng ở trường bắt buộc = 0; tỷ lệ bác sĩ chấp nhận nháp cải thiện qua các chu kỳ.

## BR-04: Truy nguyên và minh bạch đầu ra

Mọi nội dung trong output có thể truy nguyên về nguồn tài liệu tham chiếu (phác đồ, hướng dẫn, mẫu biểu). Bác sĩ biết đoạn nào do AI sinh, đoạn nào lấy từ nguồn nào.

## BR-05: Tích hợp với hệ thống HIS hiện tại

Hệ thống nhận đầu vào từ HIS và xuất kết quả về HIS/EHR theo chuẩn dữ liệu bệnh viện mà không yêu cầu thay đổi workflow hiện tại của bác sĩ.

# 7. YÊU CẦU CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

## 7.1 Module Chuẩn hóa và Xử lý văn bản

| Mã | Yêu cầu | Mức độ ưu tiên |
| --- | --- | --- |
| FR-NORM-01 | Hệ thống chuẩn hóa Unicode, đơn vị đo, dấu câu và ký tự đặc biệt trong văn bản tiếng Việt y khoa | Must Have |
| FR-NORM-02 | Hệ thống tự động phân đoạn section bệnh án (hành chính, bệnh sử, tiền sử, khám, CLS, chẩn đoán, KHĐT) | Must Have |
| FR-NORM-03 | Hệ thống tra cứu và mở rộng viết tắt theo từ điển nội bộ và ngữ cảnh section | Must Have |
| FR-NORM-04 | Hệ thống cảnh báo khi gặp viết tắt chưa có trong từ điển, cho phép bác sĩ bổ sung | Should Have |
| FR-NORM-05 | Hệ thống cho phép quản trị viên cập nhật từ điển viết tắt nội viện theo khoa/phòng | Must Have |

## 7.2 Module De-identification

| Mã | Yêu cầu | Mức độ ưu tiên |
| --- | --- | --- |
| FR-DEID-01 | Tự động phát hiện và mask 8 nhóm PHI: tên, ngày sinh, địa chỉ, SĐT, CMND/CCCD, số BHYT, số hồ sơ, thông tin định danh khác | Must Have |
| FR-DEID-02 | De-identification hoạt động trước mọi tác vụ: huấn luyện, inference, lưu trữ | Must Have |
| FR-DEID-03 | Pseudonymization nhất quán trong cùng một dataset (cùng bệnh nhân → cùng pseudonym) | Must Have |
| FR-DEID-04 | Báo cáo audit log chi tiết mỗi thực thể bị mask | Must Have |
| FR-DEID-05 | Không mask nhầm giá trị lâm sàng hợp lệ (số xét nghiệm, chỉ số sinh tồn) | Must Have |

## 7.3 Module NER – Trích xuất khái niệm lâm sàng

| Mã | Yêu cầu | Mức độ ưu tiên |
| --- | --- | --- |
| FR-NER-01 | Nhận dạng thực thể: bệnh lý, triệu chứng, thuốc, liều dùng, xét nghiệm, kết quả, thủ thuật, giải phẫu | Must Have |
| FR-NER-02 | Gán nhãn entity type và confidence score cho mỗi thực thể | Must Have |
| FR-NER-03 | Trích xuất đúng bối cảnh phủ định ("không sốt", "chưa dùng aspirin") | Should Have |
| FR-NER-04 | Liên kết thực thể với ontology chuẩn (ICD, SNOMED nếu có) | Should Have |

## 7.4 Module Sinh nháp

| Mã | Yêu cầu | Mức độ ưu tiên |
| --- | --- | --- |
| FR-GEN-01 | Sinh nháp discharge summary từ thông tin đầu vào cấu trúc | Must Have |
| FR-GEN-02 | Cấu trúc hóa báo cáo chẩn đoán hình ảnh từ free-text mô tả | Must Have |
| FR-GEN-03 | Tiền điền tự động các trường hành chính và facts có thể kiểm chứng | Must Have |
| FR-GEN-04 | Gắn cờ uncertainty khi thông tin đầu vào mơ hồ hoặc thiếu | Must Have |
| FR-GEN-05 | Để trống trường thông tin không có trong đầu vào, không tự bịa | Must Have |
| FR-GEN-06 | Hỗ trợ template theo khoa/phòng có thể tùy chỉnh | Should Have |

## 7.5 Module RAG – Truy hồi và neo đầu ra

| Mã | Yêu cầu | Mức độ ưu tiên |
| --- | --- | --- |
| FR-RAG-01 | Lưu trữ và lập chỉ mục: phác đồ điều trị, hướng dẫn chuyên môn, mẫu biểu, từ điển thuật ngữ, quy ước bệnh viện | Must Have |
| FR-RAG-02 | Truy hồi tài liệu liên quan theo query và rerank theo relevance | Must Have |
| FR-RAG-03 | Gắn citation nguồn tài liệu vào output | Must Have |
| FR-RAG-04 | Thông báo rõ khi không tìm thấy tài liệu phù hợp | Must Have |
| FR-RAG-05 | Cập nhật kho chỉ mục khi có phiên bản tài liệu mới | Must Have |

## 7.6 Module Kiểm soát an toàn đầu ra

| Mã | Yêu cầu | Mức độ ưu tiên |
| --- | --- | --- |
| FR-SAFE-01 | Kiểm tra PHI trong output trước khi hiển thị cho người dùng | Must Have |
| FR-SAFE-02 | Phát hiện và gắn cờ mâu thuẫn nội bộ trong nháp | Must Have |
| FR-SAFE-03 | Chặn output có hallucination nghiêm trọng ở trường bắt buộc | Must Have |
| FR-SAFE-04 | Ước lượng và hiển thị mức độ bất định (uncertainty) | Must Have |
| FR-SAFE-05 | Output chỉ được lưu vào EHR sau khi bác sĩ phê duyệt | Must Have |

## 7.7 Module Workflow Bác sĩ

| Mã | Yêu cầu | Mức độ ưu tiên |
| --- | --- | --- |
| FR-WF-01 | Hiển thị nháp với phân biệt rõ nội dung AI sinh / nội dung từ nguồn | Must Have |
| FR-WF-02 | Cho phép bác sĩ chỉnh sửa trực tiếp trên nháp | Must Have |
| FR-WF-03 | Bác sĩ có thể Phê duyệt / Từ chối / Yêu cầu sinh lại | Must Have |
| FR-WF-04 | Ghi lại diff giữa nháp gốc và bản được duyệt cho active learning | Must Have |
| FR-WF-05 | Hỗ trợ Silent Mode: sinh nháp ngầm không hiển thị trong workflow thật | Should Have |

## 7.8 Module Audit & Bảo mật

| Mã | Yêu cầu | Mức độ ưu tiên |
| --- | --- | --- |
| FR-AUD-01 | Ghi log toàn bộ: generate, edit, approve, reject, block – với timestamp và user ID | Must Have |
| FR-AUD-02 | Log không thể xóa hoặc sửa bởi bất kỳ user thông thường nào | Must Have |
| FR-AUD-03 | Phân quyền theo vai trò (RBAC): Bác sĩ, Điều dưỡng, Quản trị, Nhà nghiên cứu | Must Have |
| FR-AUD-04 | Không truyền dữ liệu bệnh nhân ra ngoài network bệnh viện | Must Have |

# 8. YÊU CẦU PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS)

## 8.1 Hiệu năng

| Mã | Yêu cầu | Ngưỡng mục tiêu |
| --- | --- | --- |
| NFR-PERF-01 | Latency sinh nháp discharge summary | ≤ vài giây (P95 < 15 giây) |
| NFR-PERF-02 | Latency de-identification trên văn bản ≤ 1.000 token | < 2 giây |
| NFR-PERF-03 | Số người dùng đồng thời (concurrent) | ≥ 50 |
| NFR-PERF-04 | VRAM tối đa trong inference với model 7B | ≤ 20 GB |
| NFR-PERF-05 | Uptime hệ thống trong giờ làm việc | ≥ 99% |

## 8.2 Độ chính xác (chỉ số tối thiểu trước pilot)

| Module | Chỉ số | Ngưỡng |
| --- | --- | --- |
| De-identification | Recall PHI nhóm nguy cơ cao | ≥ 0,99 |
| NER lâm sàng | F1 macro | ≥ 0,90 |
| Giải nghĩa viết tắt nguy cơ cao | Accuracy | ≥ 0,95 |
| Hallucination nghiêm trọng | Rate | = 0 ở trường bắt buộc |
| RAG Faithfulness | Score | ≥ ngưỡng nội bộ đã định |

## 8.3 Bảo mật

* Toàn bộ hệ thống triển khai on-premise hoặc trong private network bệnh viện.
* Dữ liệu huấn luyện phải được de-identify trước khi sử dụng.
* Mã hóa dữ liệu at-rest và in-transit.
* Xác thực đa yếu tố cho tài khoản quản trị.
* Audit log lưu giữ ≥ 5 năm.
## 8.4 Khả năng bảo trì và mở rộng

* Cho phép cập nhật từ điển viết tắt mà không cần retrain mô hình.
* Cho phép cập nhật kho chỉ mục RAG không downtime.
* Pipeline fine-tune có thể chạy lại với dữ liệu mới mỗi quý.
* Hỗ trợ mở rộng sang chuyên khoa mới bằng cấu hình (không cần viết lại core).
# 9. QUY TRÌNH NGHIỆP VỤ (BUSINESS PROCESS FLOWS)

## 9.1 Quy trình hiện tại (As-Is)

* Bác sĩ khám bệnh → Ghi chép tay / đánh máy vào HIS
* Sử dụng viết tắt tự do, không chuẩn hóa
* Không có kiểm tra nhất quán thuật ngữ
* Lưu bệnh án vào HIS → Không có audit trail nội dung AI
## 9.2 Quy trình tương lai – Radiology Report (To-Be, Use case 1)

* Bước 1: Bác sĩ hình ảnh nhập mô tả free-text hoặc diễn giải
* Bước 2a: De-identification check (không có PHI trong radiology note)
* Bước 2b: NER trích xuất phát hiện, cấu trúc hóa FINDINGS
* Bước 2c: RAG truy hồi template báo cáo chuyên khoa
* Bước 2d: LLM sinh nháp FINDINGS + IMPRESSION có cấu trúc
* Bước 2e: Safety layer kiểm tra hallucination và mâu thuẫn
* Bước 3: Nháp hiển thị cho bác sĩ, có highlight citation nguồn
* Bước 4: Bác sĩ duyệt / chỉnh sửa / phê duyệt
* Bước 5: Audit log ghi diff; output lưu vào HIS/PACS
## 9.3 Quy trình tương lai – Discharge Summary (To-Be, Use case 2)

* Bước 1: Bác sĩ yêu cầu sinh discharge summary cho ca bệnh
* Bước 2: Hệ thống thu thập đầu vào từ HIS: thông tin nhập viện, diễn biến, xét nghiệm, thuốc, chẩn đoán
* Bước 3a: De-identification tất cả PHI
* Bước 3b: NER trích xuất danh sách vấn đề, thuốc, thủ thuật
* Bước 3c: Normalization chuẩn hóa thuật ngữ và viết tắt
* Bước 3d: RAG truy hồi template discharge theo khoa
* Bước 3e: LLM sinh nháp 6 section chuẩn
* Bước 3f: Safety layer: PHI check, hallucination check, consistency check
* Bước 4: Hiển thị nháp với cờ bất định ở các trường cần xác nhận
* Bước 5: Bác sĩ phê duyệt, hệ thống lưu và tạo audit log
# 10. YÊU CẦU DỮ LIỆU

## 10.1 Nguồn dữ liệu đầu vào

| Nguồn | Loại | Vai trò | Yêu cầu xử lý |
| --- | --- | --- | --- |
| Bệnh án nội bộ đã ẩn danh | Văn bản lâm sàng | Fine-tuning, RAG index, active learning | De-identification bắt buộc |
| Từ điển viết tắt nội viện | Bảng tra cứu | Normalization, abbreviation expansion | Xây dựng theo khoa/phòng |
| Phác đồ điều trị, hướng dẫn chuyên môn | Tài liệu chuẩn | RAG kho nội bộ | Version control |
| Mẫu biểu, template báo cáo | Cấu trúc | RAG kho nội bộ | Phân loại theo khoa |
| Corpus công khai (MIMIC-IV, VinDr-CXR) | Văn bản lâm sàng | Bootstrap pretraining | Tuân thủ license |
| Dữ liệu hỏi-đáp tiếng Việt y khoa (Bui et al.) | Instruction pairs | Fine-tuning instruction | Open access |

## 10.2 Yêu cầu quản lý dữ liệu

* De-identification: 100% dữ liệu bệnh nhân phải được ẩn danh trước khi dùng.
* Version control: Tất cả tài liệu RAG có phiên bản và ngày hiệu lực.
* Retention: Audit log lưu ≥ 5 năm; dữ liệu huấn luyện theo chính sách lưu giữ bệnh viện.
* Lineage: Có thể truy vết mỗi output về training data và tài liệu retrieval.
* Consent: Quy trình đạo đức và pháp chế phê duyệt trước khi dùng dữ liệu nội bộ.
# 11. GIAO DIỆN VÀ TÍCH HỢP HỆ THỐNG

## 11.1 Tích hợp đầu vào

| Hệ thống | Giao thức | Dữ liệu trao đổi |
| --- | --- | --- |
| HIS (Hospital Information System) | HL7 v2 / FHIR R4 | Thông tin nhập viện, xét nghiệm, chẩn đoán, thuốc |
| PACS (Picture Archiving) | DICOM / API nội bộ | Metadata ảnh chẩn đoán, báo cáo radiology |
| LIS (Laboratory Information System) | HL7 / API | Kết quả xét nghiệm |

## 11.2 Tích hợp đầu ra

| Hệ thống | Giao thức | Dữ liệu trao đổi |
| --- | --- | --- |
| HIS/EHR | FHIR R4 / API | Discharge summary, bệnh án đã phê duyệt |
| PACS | DICOM SR / API | Báo cáo radiology có cấu trúc |
| Audit System | Syslog / Database | Log mọi thao tác người dùng và hệ thống |

# 12. GIẢ ĐỊNH VÀ RÀNG BUỘC

## 12.1 Giả định

| # | Giả định |
| --- | --- |
| 1 | Bệnh viện có hạ tầng GPU on-premise tối thiểu (1 GPU ≥ 20 GB VRAM) cho inference |
| 2 | Có nguồn dữ liệu bệnh án nội bộ đủ đa dạng và có thể được ẩn danh hợp pháp |
| 3 | Bác sĩ đồng ý tham gia pilot và cung cấp phản hồi |
| 4 | Phòng pháp chế có thể xây dựng legal-compliance matrix trong vòng 60 ngày đầu |
| 5 | HIS hiện tại hỗ trợ tích hợp API hoặc HL7 |

## 12.2 Ràng buộc

| # | Ràng buộc | Nguồn gốc |
| --- | --- | --- |
| 1 | Toàn bộ xử lý dữ liệu bệnh nhân phải on-premise | Bảo mật / pháp lý |
| 2 | Bác sĩ bắt buộc phê duyệt trước khi lưu bất kỳ output nào | An toàn lâm sàng |
| 3 | Không huấn luyện từ đầu (from scratch) trong Giai đoạn 1 | Ràng buộc nguồn lực |
| 4 | Phải có ethical approval trước khi dùng dữ liệu bệnh nhân | Đạo đức nghiên cứu |
| 5 | Model size ≤ 8B tham số trong Giai đoạn 1 | Hạ tầng GPU nội bộ |

# 13. RỦI RO NGHIỆP VỤ

| Mã | Rủi ro | Xác suất | Mức độ tác động | Biện pháp giảm thiểu |
| --- | --- | --- | --- | --- |
| R-01 | Thiếu dữ liệu nội bộ đạt chuẩn (không đủ sạch, không đủ đa dạng) | Cao | Rất cao | Bắt đầu thu thập và ẩn danh ngay từ tháng 1; dùng corpus công khai để bootstrap |
| R-02 | Viết tắt nội viện mơ hồ gây giải nghĩa sai → nguy cơ lâm sàng | Cao | Rất cao | Xây từ điển viết tắt nội bộ theo khoa trước khi pilot; quy tắc "để trống nếu không chắc" |
| R-03 | Hallucination ở trường thông tin quan trọng (thuốc, dị ứng) | Trung bình | Rất cao | Safety layer bắt buộc; bác sĩ phê duyệt; test set kiểm tra trước pilot |
| R-04 | Bác sĩ lệ thuộc thụ động vào nháp, giảm kiểm tra | Trung bình | Cao | Training bác sĩ; đo số lỗi được phát hiện bởi bác sĩ; đánh dấu nháp là "đề xuất" |
| R-05 | Khoảng trống pháp lý Việt Nam chưa rõ ràng | Trung bình | Cao | Workstream pháp chế độc lập; không triển khai rộng khi chưa có compliance matrix |
| R-06 | Hạ tầng GPU không đủ tải production | Thấp | Trung bình | Ước tính VRAM trước; dự phòng cloud private nếu cần |
| R-07 | Chất lượng mô hình giảm sau fine-tune mới (catastrophic forgetting) | Trung bình | Cao | Regression test sau mỗi chu kỳ huấn luyện; rollback tự động nếu F1 giảm |

# 14. LỘ TRÌNH VÀ MỐC TRIỂN KHAI

## 14.1 Lộ trình 12–24 tháng

| Giai đoạn | Thời gian | Hoạt động chính | Milestone |
| --- | --- | --- | --- |
| Khởi động | T1–T2 | Chọn use case đầu, phê duyệt governance, bắt đầu thu thập dữ liệu | Phê duyệt ethical; bắt đầu xây từ điển viết tắt |
| Dữ liệu | T2–T5 | Thu thập nguồn công khai; ẩn danh dữ liệu nội bộ; xây từ điển thuật ngữ | Dataset v1 ready; abbreviation dictionary v1 |
| Mô hình – GĐ1 | T4–T7 | Baseline sidecar encoder cho de-id và IE | De-id Recall ≥ 0,99; NER F1 ≥ 0,90 |
| Mô hình – GĐ2 | T6–T10 | DAPT + SFT LLM tiếng Việt y khoa; tích hợp RAG nội bộ | Mô hình draft v1; RAG index v1 |
| Đánh giá offline | T9–T11 | Offline evaluation và failure analysis trên test set chuẩn | Báo cáo hallucination rate; benchmark report |
| Silent Mode | T11–T14 | Hệ thống sinh nháp ngầm, so sánh với bệnh án thật | Silent mode report; QA review |
| Assisted Mode | T14–T17 | Bác sĩ nhìn thấy nháp, chỉnh sửa, phê duyệt | Tỷ lệ chấp nhận ≥ mục tiêu; thời gian ghi chép giảm |
| Hardening | T17–T19 | Bảo mật, audit, tối ưu hiệu năng, legal compliance | Security audit passed |
| Mở rộng | T19–T23 | Thêm chuyên khoa thứ hai | Specialty #2 pilot |
| Quyết định triển khai | T23–T24 | Review toàn bộ; quyết định triển khai rộng hoặc dừng | Go/No-Go decision |

## 14.2 Bốn điểm quyết định quan trọng (Decision Gates)

| Gate | Điều kiện để tiếp tục |
| --- | --- |
| Gate 1 | Có được tập dữ liệu nội bộ đã ẩn danh đủ sạch và đủ đa dạng |
| Gate 2 | Sidecar de-identification và NER đạt ngưỡng tin cậy để đưa vào pipeline thật |
| Gate 3 | Trong Silent Mode, mô hình giảm thời gian ghi chép mà không tăng lỗi lâm sàng |
| Gate 4 | Trong Assisted Mode, bác sĩ chấp nhận hệ thống như công cụ hỗ trợ thật sự |

# 15. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)

## 15.1 Tiêu chí kỹ thuật (trước pilot lâm sàng)

| Tiêu chí | Ngưỡng bắt buộc |
| --- | --- |
| De-identification Recall PHI nhóm nguy cơ cao | ≥ 0,99 |
| NER F1 macro | ≥ 0,90 |
| Accuracy viết tắt nhóm nguy cơ cao | ≥ 0,95 |
| Hallucination nghiêm trọng ở trường bắt buộc | = 0 |
| PHI không rò rỉ trong output | 100% |

## 15.2 Tiêu chí vận hành (sau Assisted Mode)

| Tiêu chí | Ngưỡng mục tiêu |
| --- | --- |
| Thời gian hoàn tất tài liệu (discharge summary) | Giảm ≥ 20% so với baseline |
| Tỷ lệ bác sĩ chấp nhận nháp (không từ chối hoàn toàn) | ≥ 60% sau 3 tháng |
| Số chỉnh sửa lớn (major edit) trên mỗi nháp | Giảm dần qua các chu kỳ |
| Latency đầu-cuối P95 | ≤ 15 giây |
| Uptime trong giờ làm việc | ≥ 99% |

# 16. BẢNG CHÚ GIẢI THUẬT NGỮ

| Thuật ngữ | Định nghĩa |
| --- | --- |
| LLM | Large Language Model – Mô hình ngôn ngữ lớn |
| SFT | Supervised Fine-Tuning – Tinh chỉnh có giám sát |
| PEFT | Parameter-Efficient Fine-Tuning – Tinh chỉnh hiệu quả tham số |
| LoRA/QLoRA | Phương pháp PEFT giảm số tham số cần huấn luyện |
| RAG | Retrieval-Augmented Generation – Sinh văn bản có tăng cường truy hồi |
| NER | Named Entity Recognition – Nhận dạng thực thể có tên |
| PHI | Protected Health Information – Thông tin sức khỏe được bảo vệ |
| De-identification | Ẩn danh hóa – loại bỏ/che PHI khỏi văn bản |
| Hallucination | Lỗi mô hình sinh ra thông tin sai không có cơ sở từ đầu vào |
| EHR/HIS | Electronic Health Record / Hospital Information System |
| DAPT | Domain-Adaptive Pre-Training – Tiền huấn luyện thích nghi miền |
| FHIR | Fast Healthcare Interoperability Resources – Chuẩn trao đổi dữ liệu y tế |
| RBAC | Role-Based Access Control – Kiểm soát truy cập theo vai trò |
| On-premise | Triển khai tại cơ sở, không dùng cloud công cộng |
| Active Learning | Học chủ động – dùng phản hồi người dùng để cải thiện mô hình |
| Faithfulness | Mức độ output trung thành với tài liệu nguồn được truy hồi |
| Silent Mode | Chế độ hệ thống sinh nháp ngầm, không hiển thị cho bác sĩ trong workflow thật |
| Assisted Mode | Chế độ bác sĩ nhìn thấy nháp và phê duyệt |

Tài liệu này sẽ được cập nhật khi có thay đổi về yêu cầu, phạm vi hoặc ràng buộc. Mọi thay đổi cần được phê duyệt bởi các bên liên quan chính.

