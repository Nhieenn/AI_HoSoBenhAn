__HỌC VIỆN QUÂN Y__

──────────

__TÀI LIỆU PHÂN TÍCH NGHIỆP VỤ__

*BUSINESS ANALYSIS DOCUMENT*

__Hệ thống AI Tạo Sinh Chuyên Biệt__

__cho Ngôn Ngữ và Thuật Ngữ Y Khoa Tiếng Việt__

__\(ViMedAI\)__

__Phiên bản 2\.0__

Ngày: 05/05/2026

Đơn vị: Học viện Quân y

# __MỤC LỤC__

__1\. TỔNG QUAN DỰ ÁN__	__3__

1\.1 Tóm tắt điều hành	3

__2\. BỐI CẢNH NGHIỆP VỤ__	__4__

2\.1 Vấn đề hiện tại	4

2\.2 Cơ hội	4

__3\. CÁC BÊN LIÊN QUAN \(STAKEHOLDERS\)__	__5__

3\.1 Ma trận Stakeholders	5

__4\. MỤC TIÊU NGHIỆP VỤ__	__6__

4\.1 Mục tiêu chiến lược	6

4\.2 Lưu ý – Không phải mục tiêu	6

__5\. PHẠM VI DỰ ÁN__	__7__

5\.1 Trong phạm vi \(In Scope\)	7

5\.2 Ngoài phạm vi \(Out Of Scope\)	7

__6\. YÊU CẦU NGHIỆP VỤ \(BUSINESS REQUIREMENTS\)__	__8__

BR\-01: Chuẩn hóa thuật ngữ và viết tắt	8

BR\-02: Bảo vệ thông tin cá nhân bệnh nhân \(PHI\)	8

BR\-03: Hỗ trợ sinh nháp có kiểm soát	8

BR\-04: Truy nguyên và minh bạch đầu ra	8

BR\-05: Tích hợp với hệ thống HIS hiện tại	8

BR\-06: Báo cáo minh bạch theo chuẩn quốc tế \(MỚI\)	9

__7\. YÊU CẦU CHỨC NĂNG \(FUNCTIONAL REQUIREMENTS\)__	__10__

7\.1 Module Chuẩn hóa và Xử lý văn bản	10

7\.2 Module De\-identification	10

7\.3 Module NER – Trích xuất khái niệm lâm sàng	10

7\.4 Module Sinh nháp	11

7\.5 Module RAG – Truy hồi và neo đầu ra	11

7\.6 Module Kiểm soát an toàn đầu ra	12

7\.7 Module Workflow Bác sĩ	12

7\.8 Module Audit, Bảo mật và Báo cáo minh bạch	13

7\.9 Module Huấn luyện mô hình \(MỚI\)	13

__8\. YÊU CẦU PHI CHỨC NĂNG \(NON\-FUNCTIONAL REQUIREMENTS\)__	__14__

8\.1 Hiệu năng	14

8\.2 Độ chính xác	14

8\.3 Bảo mật	14

8\.4 Khả năng bảo trì và mở rộng	15

8\.5 Tính minh bạch và tuân thủ chuẩn báo cáo \(MỚI\)	15

__9\. QUY TRÌNH NGHIỆP VỤ \(BUSINESS PROCESS FLOWS\)__	__15__

9\.1 Quy trình hiện tại \(As\-Is\)	15

9\.2 Quy trình tương lai – Radiology Report \(To\-Be, Use case 1\)	15

9\.3 Quy trình tương lai – Discharge Summary \(To\-Be, Use case 2\)	16

__10\. YÊU CẦU DỮ LIỆU__	__17__

10\.1 Nguồn dữ liệu đầu vào	17

10\.2 Yêu cầu quản lý dữ liệu	17

__11\. GIAO DIỆN VÀ TÍCH HỢP HỆ THỐNG__	__18__

11\.1 Tích hợp đầu vào	18

11\.2 Tích hợp đầu ra	18

__12\. GIẢ ĐỊNH VÀ RÀNG BUỘC__	__18__

12\.1 Giả định	18

12\.2 Ràng buộc	19

__13\. RỦI RO NGHIỆP VỤ__	__20__

__14\. LỘ TRÌNH VÀ MỐC TRIỂN KHAI__	__21__

14\.1 Lộ trình 12–24 tháng	21

14\.2 Bốn điểm quyết định quan trọng \(Decision Gates\)	22

__15\. TIÊU CHÍ CHẤP NHẬN \(ACCEPTANCE CRITERIA\)__	__22__

15\.1 Tiêu chí kỹ thuật \(trước pilot lâm sàng\)	22

15\.2 Tiêu chí vận hành \(sau Assisted Mode\)	23

__16\. BẢNG CHÚ GIẢI THUẬT NGỮ__	__23__

# __1\. TỔNG QUAN DỰ ÁN__

__Hạng mục__

__Nội dung__

Tên dự án

Hệ thống AI Tạo Sinh Y Khoa Tiếng Việt \(ViMedAI\)

Phiên bản tài liệu

2\.0

Ngày tạo

05/05/2026

Đơn vị đề xuất

Học viện Quân y

Loại dự án

Nghiên cứu – Phát triển – Triển khai

Thời gian dự kiến

12–24 tháng \(Giai đoạn 1\)

Cơ sở tham chiếu

Báo cáo nghiên cứu khả thi: Ứng dụng AI tạo sinh chuyên biệt cho ngôn ngữ và thuật ngữ y khoa tiếng Việt

## __1\.1 Tóm tắt điều hành__

Dự án xây dựng một hệ thống AI tạo sinh chuyên biệt cho ngôn ngữ và thuật ngữ y khoa tiếng Việt, nhằm tối ưu hóa quy trình ghi chép và báo cáo y tế\. Hệ thống không thay thế bác sĩ viết bệnh án, mà hoạt động như một công cụ hỗ trợ soạn thảo có kiểm soát: đề xuất nháp, tiền điền biểu mẫu, chuẩn hóa cấu trúc báo cáo, mở rộng/giải nghĩa viết tắt và trích xuất khái niệm lâm sàng\.

Kiến trúc được chọn là Hybrid SFT \+ Modular RAG \+ Sidecar IE/De\-identification, triển khai on\-premise để đảm bảo an toàn dữ liệu bệnh nhân\. Pipeline huấn luyện gồm ba bước theo thứ tự: Continued Pretraining \(DAPT\) trên y khoa tiếng Việt → Supervised Fine\-Tuning \(SFT\) bằng LoRA/QLoRA → Modular RAG nội bộ với rerank, citation và faithfulness check\.

Phiên bản 2\.0 cập nhật và bổ sung so với phiên bản 1\.0 các nội dung: lớp chuẩn hóa thứ 5 \(Khuôn mẫu báo cáo\); BR\-06 mới về báo cáo minh bạch theo chuẩn quốc tế \(Model Card, Data Sheet, CONSORT\-AI/SPIRIT\-AI\); 02 giả định mới về thiếu corpus viết tắt và khung pháp lý Việt Nam; Acceptance Criteria cho BR\-04 và BR\-05; mở rộng bảng nguồn dữ liệu; quy định rõ Modular RAG; bổ sung yêu cầu credentialed access cho MIMIC; và các sửa đổi khác để đảm bảo tính nhất quán với báo cáo nghiên cứu khả thi gốc\.

# __2\. BỐI CẢNH NGHIỆP VỤ__

## __2\.1 Vấn đề hiện tại__

__\#__

__Vấn đề__

__Tác động__

1

Bác sĩ tốn nhiều thời gian ghi chép bệnh án thủ công

Giảm thời gian khám chữa bệnh, tăng tải trọng hành chính

2

Thiếu nhất quán trong cách diễn đạt thuật ngữ và viết tắt giữa các bác sĩ, khoa, phòng

Khó tổng hợp dữ liệu thứ cấp cho nghiên cứu và kiểm định chất lượng

3

Viết tắt nội viện không có từ điển chuẩn hóa

Nguy cơ hiểu nhầm khi bàn giao ca, hội chẩn liên khoa

4

Cấu trúc báo cáo chẩn đoán hình ảnh không đồng nhất

Khó trích xuất dữ liệu tự động, khó so sánh ca bệnh theo chuỗi thời gian

5

Thiếu hạ tầng NLP y tế đặc thù cho tiếng Việt

Không thể tận dụng công nghệ AI sẵn có của quốc tế

## __2\.2 Cơ hội__

- Nghiên cứu năm 2025 \(Bui et al\.\) chứng minh fine\-tune LLM tiếng Việt y khoa bằng LoRA/QLoRA với ~337\.000 cặp dữ liệu cải thiện đáng kể chất lượng theo BertScore, Rouge\-L và đánh giá bằng LLM\.
- Công nghệ PEFT \(LoRA/QLoRA\) cho phép huấn luyện trên hạ tầng GPU cục bộ với chi phí hợp lý\.
- Bộ dữ liệu công khai \(MIMIC\-IV, MIMIC\-CXR, MIMIC\-IV\-Note, VinDr\-CXR, PadChest\) có thể dùng để bootstrap trước khi có dữ liệu nội bộ đủ lớn\.
- Tiết kiệm thời gian ghi chép theo các nghiên cứu quốc tế có thể đạt đến ~40% trong điều kiện lý tưởng\. Tuy nhiên, các nghiên cứu này cũng cảnh báo về sai lệch sự thật, hallucination, giảm chất lượng ở ca phức tạp và niềm tin của bác sĩ\. Do đó, mục tiêu nội bộ của dự án \(BG\-01\) đặt thận trọng ở mức ≥ 20%\.

# __3\. CÁC BÊN LIÊN QUAN \(STAKEHOLDERS\)__

## __3\.1 Ma trận Stakeholders__

__Stakeholder__

__Vai trò__

__Quyền lợi/Quan tâm chính__

__Mức độ ảnh hưởng__

Ban Giám đốc Bệnh viện / Học viện

Sponsor, phê duyệt ngân sách

Hiệu quả vận hành, tuân thủ pháp lý, an toàn bệnh nhân

Rất cao

Bác sĩ điều trị

Người dùng cuối chính

Tiết kiệm thời gian, độ tin cậy của nháp, không tăng gánh nặng kiểm tra

Rất cao

Bác sĩ chẩn đoán hình ảnh

Người dùng cuối \(radiology\)

Chuẩn hóa báo cáo, tốc độ

Cao

Điều dưỡng/Hành chính

Người dùng tiền điền biểu mẫu

Độ chính xác dữ liệu hành chính

Trung bình

Phòng Công nghệ thông tin

Triển khai và vận hành

Bảo mật, tích hợp HIS, hiệu năng

Cao

Phòng Pháp chế/Đạo đức

Tuân thủ pháp luật

Bảo vệ dữ liệu bệnh nhân, trách nhiệm pháp lý

Rất cao

Nhóm nghiên cứu/AI

Phát triển mô hình

Chất lượng dữ liệu, infrastructure, benchmark

Cao

Bệnh nhân

Người chịu tác động gián tiếp

An toàn thông tin cá nhân, chất lượng hồ sơ

Cao

Cơ quan quản lý nhà nước

Giám sát, phê duyệt \(external regulator\)

Tuân thủ luật KCB, bảo vệ dữ liệu cá nhân

Cao

# __4\. MỤC TIÊU NGHIỆP VỤ__

## __4\.1 Mục tiêu chiến lược__

__Mã__

__Mục tiêu__

__Chỉ số đo lường__

__Mốc thời gian__

BG\-01

Giảm thời gian ghi chép bệnh án hành chính và cấu trúc

Thời gian hoàn thành tài liệu giảm ≥ 20% so với baseline \(mục tiêu thận trọng so với mức ~40% trong nghiên cứu quốc tế\)

Cuối Giai đoạn 2 \(Assisted Mode\)

BG\-02

Tăng tính nhất quán thuật ngữ và cấu trúc văn bản y tế

Tỷ lệ viết tắt không chuẩn trong bệnh án giảm ≥ 50%

Cuối Giai đoạn 1

BG\-03

Tạo nền dữ liệu có cấu trúc cho nghiên cứu và kiểm định chất lượng

Volume dữ liệu cấu trúc hóa tăng; có thể truy vấn tự động

24 tháng

BG\-04

Đảm bảo an toàn bệnh nhân và tuân thủ bảo mật dữ liệu

Không sự cố rò rỉ PHI; không hallucination nghiêm trọng trong ca triển khai

Từ ngày đầu pilot

BG\-05

Xây dựng năng lực nội bộ về AI y tế tiếng Việt

Có đội ngũ vận hành và phát triển mô hình in\-house

24 tháng

## __4\.2 Lưu ý – Không phải mục tiêu__

__*Lưu ý: *__*KHÔNG phải mục tiêu của Giai đoạn 1: Thay thế hoàn toàn bác sĩ trong viết bệnh án; triển khai sinh progress note tự do trên mọi chuyên khoa; hoặc ra quyết định lâm sàng tự động\.*

# __5\. PHẠM VI DỰ ÁN__

## __5\.1 Trong phạm vi \(In Scope\)__

__\#__

__Chức năng__

__Giai đoạn ưu tiên__

1

Chuẩn hóa thuật ngữ y khoa \(5 lớp: đồng nghĩa, viết tắt, hình thức, section, khuôn mẫu báo cáo\)

Giai đoạn 1

2

Ẩn danh dữ liệu PHI \(De\-identification\): loại bỏ hoặc mã hóa thông tin định danh bệnh nhân

Giai đoạn 1 – Bắt buộc

3

Trích xuất khái niệm lâm sàng \(NER\): nhận diện và trích xuất thực thể y khoa

Giai đoạn 1

4

Giải nghĩa và mở rộng viết tắt nội viện theo từ điển nội bộ và ngữ cảnh section

Giai đoạn 1

5

Cấu trúc hóa báo cáo chẩn đoán hình ảnh: chuyển dữ liệu thô sang định dạng FHIR/DICOM SR chuẩn

Giai đoạn 1 – Use case ưu tiên

6

Sinh nháp discharge summary có section cố định để bác sĩ chỉnh sửa

Giai đoạn 1 – Use case ưu tiên

7

Tiền điền tự động phần hành chính và trường facts có thể kiểm chứng

Giai đoạn 1

8

RAG nội bộ \(phác đồ, mẫu biểu, từ điển thuật ngữ\) – kiến trúc Modular/Advanced RAG

Giai đoạn 1

9

Vòng duyệt bác sĩ \(Assisted Mode\): xem xét, chỉnh sửa và phê duyệt nội dung do AI tạo

Giai đoạn 2

10

Audit log và active learning: ghi lại lịch sử thao tác và cải thiện mô hình từ phản hồi

Liên tục

11

Báo cáo minh bạch \(Model Card, Data Sheet, framework CONSORT\-AI/SPIRIT\-AI\)

Giai đoạn 1 – Bắt buộc

## __5\.2 Ngoài phạm vi \(Out Of Scope\)__

__Hạng mục__

__Lý do__

Sinh progress note tự do đa chuyên khoa

Giai đoạn sau; rủi ro an toàn cao

Ra quyết định lâm sàng tự động

Ngoài phạm vi AI hỗ trợ có kiểm soát

Ứng dụng di động bệnh nhân

Không thuộc phạm vi dự án này

Dịch thuật đa ngôn ngữ

Ngoài scope tiếng Việt Giai đoạn 1

Tích hợp thiết bị y tế \(IoT/monitor\)

Hạ tầng riêng, scope khác

Pretraining LLM từ đầu \(from scratch\)

Chi phí quá cao; không khả thi trong 12–24 tháng; không có bằng chứng ưu thế so với DAPT\+SFT

Phân tích ảnh y khoa trực tiếp \(vision model thuần\)

Giai đoạn sau; chỉ nhận metadata báo cáo từ PACS

# __6\. YÊU CẦU NGHIỆP VỤ \(BUSINESS REQUIREMENTS\)__

## __BR\-01: Chuẩn hóa thuật ngữ và viết tắt__

Hệ thống phải chuẩn hóa 5 lớp biến thể ngôn ngữ trong văn bản y tế tiếng Việt:

- __Đồng nghĩa khái niệm: __Ánh xạ thuật ngữ thuần Việt, Hán\-Việt, tiếng Anh và viết tắt về cùng canonical term\.
- __Viết tắt nội viện: __Giải nghĩa viết tắt theo từ điển nội bộ, theo khoa/phòng và theo ngữ cảnh section\.
- __Biến thể hình thức: __Chuẩn hóa có dấu/không dấu, đơn vị đo, ký tự đặc biệt, biểu thức số\-chữ\.
- __Ngôn ngữ section: __Phân biệt vai trò ngữ nghĩa của cùng một cụm từ khi xuất hiện ở section khác nhau \(hành chính, bệnh sử, khám, CLS, chẩn đoán, KHĐT\)\.
- __Khuôn mẫu báo cáo: __Quản lý câu mẫu, template và boilerplate theo khoa/phòng để tránh sinh văn bản lặp hoặc bỏ sót thông tin có điều kiện\.

__*Điều kiện chấp nhận: *__*Accuracy giải nghĩa viết tắt nhóm nguy cơ cao ≥ 0,95; tỷ lệ áp dụng đúng template theo khoa ≥ 95%\.*

## __BR\-02: Bảo vệ thông tin cá nhân bệnh nhân \(PHI\)__

Mọi dữ liệu bệnh nhân phải được de\-identify trước khi vào bất kỳ tác vụ downstream nào\. Không có dữ liệu định danh nào được truyền ra ngoài network bệnh viện\.

__*Điều kiện chấp nhận: *__*Recall PHI ≥ 0,99 trên nhóm PHI nguy cơ cao; 0 sự cố rò rỉ dữ liệu\.*

## __BR\-03: Hỗ trợ sinh nháp có kiểm soát__

Hệ thống hỗ trợ bác sĩ bằng cách sinh nháp ghi chép/báo cáo\. Bác sĩ luôn là người phê duyệt cuối cùng trước khi lưu vào hồ sơ chính thức\.

__*Điều kiện chấp nhận: *__*Hallucination nghiêm trọng ở trường bắt buộc = 0; tỷ lệ bác sĩ chấp nhận nháp cải thiện qua các chu kỳ\.*

## __BR\-04: Truy nguyên và minh bạch đầu ra__

Mọi nội dung trong output có thể truy nguyên về nguồn tài liệu tham chiếu \(phác đồ, hướng dẫn, mẫu biểu\)\. Bác sĩ biết đoạn nào do AI sinh, đoạn nào lấy từ nguồn nào\.

__*Điều kiện chấp nhận: *__*Tỷ lệ output có gắn citation đầy đủ ≥ 95%; audit log ghi đủ provenance \(training data, retrieval doc id\) cho mỗi output có thể truy vấn được\.*

## __BR\-05: Tích hợp với hệ thống HIS hiện tại__

Hệ thống nhận đầu vào từ HIS và xuất kết quả về HIS/EHR theo chuẩn dữ liệu bệnh viện mà không yêu cầu thay đổi workflow hiện tại của bác sĩ\.

__*Điều kiện chấp nhận: *__*100% input/output trao đổi qua chuẩn FHIR R4 hoặc HL7 v2; không yêu cầu thay đổi UI HIS hiện tại; UAT với ≥ 5 bác sĩ xác nhận workflow không bị gián đoạn\.*

## __BR\-06: Báo cáo minh bạch theo chuẩn quốc tế__

Mỗi phiên bản mô hình triển khai phải có tài liệu minh bạch theo các framework quốc tế công nhận\. Mỗi pilot/đánh giá lâm sàng phải tuân thủ checklist báo cáo phù hợp\.

- Mỗi phiên bản model phải có Model Card mô tả: dữ liệu huấn luyện, đánh giá, hạn chế, các use case được/không được hỗ trợ\.
- Mỗi dataset huấn luyện hoặc RAG corpus phải có Data Sheet mô tả: nguồn, kích thước, quá trình ẩn danh, license\.
- Mỗi đánh giá lâm sàng tiền cứu phải tuân thủ CONSORT\-AI \(cho thử nghiệm\) hoặc SPIRIT\-AI \(cho protocol\)\.
- Audit trail và provenance log phải được giữ lại theo chính sách lưu trữ\.

__*Điều kiện chấp nhận: *__*100% phiên bản model triển khai có Model Card; 100% dataset có Data Sheet; pilot lâm sàng có protocol theo SPIRIT\-AI được phê duyệt trước khi bắt đầu\.*

# __7\. YÊU CẦU CHỨC NĂNG \(FUNCTIONAL REQUIREMENTS\)__

## __7\.1 Module Chuẩn hóa và Xử lý văn bản__

__Mã__

__Yêu cầu__

__Mức độ ưu tiên__

FR\-NORM\-01

Hệ thống chuẩn hóa Unicode, đơn vị đo, dấu câu và ký tự đặc biệt trong văn bản tiếng Việt y khoa

Must Have

FR\-NORM\-02

Hệ thống tự động phân đoạn section bệnh án \(hành chính, bệnh sử, tiền sử, khám, CLS, chẩn đoán, KHĐT\)

Must Have

FR\-NORM\-03

Hệ thống tra cứu và mở rộng viết tắt theo từ điển nội bộ và ngữ cảnh section

Must Have

FR\-NORM\-04

Hệ thống cảnh báo khi gặp viết tắt chưa có trong từ điển, cho phép bác sĩ bổ sung

Should Have

FR\-NORM\-05

Hệ thống cho phép quản trị viên cập nhật từ điển viết tắt nội viện theo khoa/phòng

Must Have

FR\-NORM\-06

Hệ thống quản lý kho khuôn mẫu báo cáo \(template/boilerplate\) theo khoa, phát hiện và cảnh báo sai lệch khi nháp không khớp template chuẩn

Must Have

## __7\.2 Module De\-identification__

__Mã__

__Yêu cầu__

__Mức độ ưu tiên__

FR\-DEID\-01

Tự động phát hiện và mask 8 nhóm PHI áp dụng theo bối cảnh Việt Nam: tên, ngày sinh, địa chỉ, SĐT, CMND/CCCD, số BHYT, số hồ sơ, thông tin định danh khác \(Ghi chú: 8 nhóm là diễn giải áp dụng – nguồn quốc tế tham chiếu HIPAA/GDPR và nguyên tắc tối thiểu hóa dữ liệu\)

Must Have

FR\-DEID\-02

De\-identification hoạt động trước mọi tác vụ downstream: huấn luyện, inference, lưu trữ

Must Have

FR\-DEID\-03

Pseudonymization nhất quán trong cùng một dataset \(cùng bệnh nhân → cùng pseudonym\)

Must Have

FR\-DEID\-04

Báo cáo audit log chi tiết mỗi thực thể bị mask

Must Have

FR\-DEID\-05

Không mask nhầm giá trị lâm sàng hợp lệ \(số xét nghiệm, chỉ số sinh tồn\)

Must Have

## __7\.3 Module NER – Trích xuất khái niệm lâm sàng__

__Mã__

__Yêu cầu__

__Mức độ ưu tiên__

FR\-NER\-01

Nhận dạng thực thể: bệnh lý, triệu chứng, thuốc, liều dùng, xét nghiệm, kết quả, thủ thuật, giải phẫu

Must Have

FR\-NER\-02

Gán nhãn entity type và confidence score cho mỗi thực thể

Must Have

FR\-NER\-03

Trích xuất đúng bối cảnh phủ định \("không sốt", "chưa dùng aspirin"\)

Should Have

FR\-NER\-04

Liên kết thực thể với ontology chuẩn \(ICD, SNOMED nếu có\)

Should Have

## __7\.4 Module Sinh nháp__

__Mã__

__Yêu cầu__

__Mức độ ưu tiên__

FR\-GEN\-01

Sinh nháp discharge summary từ thông tin đầu vào cấu trúc, có 6 section chuẩn cố định

Must Have

FR\-GEN\-02

Cấu trúc hóa báo cáo chẩn đoán hình ảnh từ free\-text mô tả, output tuân thủ FHIR R4/DICOM SR

Must Have

FR\-GEN\-03

Tiền điền tự động các trường hành chính và facts có thể kiểm chứng

Must Have

FR\-GEN\-04

Gắn cờ uncertainty khi thông tin đầu vào mơ hồ hoặc thiếu

Must Have

FR\-GEN\-05

Để trống trường thông tin không có trong đầu vào, không tự bịa \(rule "để trống nếu không chắc"\)

Must Have

FR\-GEN\-06

Hỗ trợ template theo khoa/phòng có thể tùy chỉnh, được quản lý ở module 7\.1

Should Have

## __7\.5 Module RAG – Truy hồi và neo đầu ra__

Kiến trúc RAG bắt buộc là Modular/Advanced RAG với rerank, citation và faithfulness check\. Không sử dụng kiến trúc Naïve RAG cho use case nguy cơ cao như EHR summarization và discharge generation\.

__Mã__

__Yêu cầu__

__Mức độ ưu tiên__

FR\-RAG\-01

Lưu trữ và lập chỉ mục: phác đồ điều trị, hướng dẫn chuyên môn, mẫu biểu, từ điển thuật ngữ, quy ước bệnh viện

Must Have

FR\-RAG\-02

Truy hồi tài liệu liên quan theo query và rerank theo relevance \(Modular RAG có rerank stage\)

Must Have

FR\-RAG\-03

Gắn citation nguồn tài liệu vào mỗi đoạn output

Must Have

FR\-RAG\-04

Thông báo rõ khi không tìm thấy tài liệu phù hợp \(no\-result handling\)

Must Have

FR\-RAG\-05

Cập nhật kho chỉ mục khi có phiên bản tài liệu mới \(không downtime\)

Must Have

FR\-RAG\-06

Faithfulness check: kiểm tra mỗi câu trong output có thực sự được hỗ trợ bởi tài liệu retrieval

Must Have

## __7\.6 Module Kiểm soát an toàn đầu ra__

__Mã__

__Yêu cầu__

__Mức độ ưu tiên__

FR\-SAFE\-01

Kiểm tra PHI trong output trước khi hiển thị cho người dùng

Must Have

FR\-SAFE\-02

Phát hiện và gắn cờ mâu thuẫn nội bộ trong nháp

Must Have

FR\-SAFE\-03

Chặn output có hallucination nghiêm trọng ở trường bắt buộc \(thuốc, dị ứng, liều\)

Must Have

FR\-SAFE\-04

Ước lượng và hiển thị mức độ bất định \(uncertainty\) ở các trường rủi ro

Must Have

FR\-SAFE\-05

Output chỉ được lưu vào EHR sau khi bác sĩ phê duyệt

Must Have

## __7\.7 Module Workflow Bác sĩ__

__Mã__

__Yêu cầu__

__Mức độ ưu tiên__

FR\-WF\-01

Hiển thị nháp với phân biệt rõ nội dung AI sinh / nội dung từ nguồn \(color coding hoặc icon\)

Must Have

FR\-WF\-02

Cho phép bác sĩ chỉnh sửa trực tiếp trên nháp

Must Have

FR\-WF\-03

Bác sĩ có thể Phê duyệt / Từ chối / Yêu cầu sinh lại

Must Have

FR\-WF\-04

Ghi lại diff giữa nháp gốc và bản được duyệt cho active learning

Must Have

FR\-WF\-05

Hỗ trợ Silent Mode: sinh nháp ngầm không hiển thị trong workflow thật

Should Have

## __7\.8 Module Audit, Bảo mật và Báo cáo minh bạch__

__Mã__

__Yêu cầu__

__Mức độ ưu tiên__

FR\-AUD\-01

Ghi log toàn bộ: generate, edit, approve, reject, block – với timestamp và user ID

Must Have

FR\-AUD\-02

Log không thể xóa hoặc sửa bởi bất kỳ user thông thường nào \(immutable\)

Must Have

FR\-AUD\-03

Phân quyền theo vai trò \(RBAC\): Bác sĩ, Điều dưỡng, Quản trị, Nhà nghiên cứu

Must Have

FR\-AUD\-04

Không truyền dữ liệu bệnh nhân ra ngoài network bệnh viện

Must Have

FR\-AUD\-05

Sinh và lưu Model Card cho mỗi phiên bản mô hình triển khai \(kết nối với BR\-06\)

Must Have

FR\-AUD\-06

Sinh và lưu Data Sheet cho mỗi dataset huấn luyện và RAG corpus

Must Have

FR\-AUD\-07

Tài liệu hóa đánh giá lâm sàng theo CONSORT\-AI/SPIRIT\-AI

Must Have

## __7\.9 Module Huấn luyện mô hình__

Pipeline huấn luyện 3 bước theo thứ tự, đảm bảo bám sát kiến trúc Hybrid được khuyến nghị bởi báo cáo nghiên cứu khả thi gốc\.

__Mã__

__Yêu cầu__

__Mức độ ưu tiên__

FR\-TRAIN\-01

Continued Pretraining \(DAPT\) trên corpus y khoa tiếng Việt công khai và tài liệu nội bộ đã ẩn danh, sử dụng LLM nền có năng lực tiếng Việt hoặc đa ngữ làm backbone

Must Have

FR\-TRAIN\-02

Supervised Fine\-Tuning \(SFT\) bằng LoRA/QLoRA trên cặp "đầu vào hành chính/lâm sàng → ghi chú/báo cáo chuẩn"

Must Have

FR\-TRAIN\-03

Pipeline fine\-tune có thể chạy lại với dữ liệu mới mỗi quý \(chu kỳ tái huấn luyện\)

Must Have

FR\-TRAIN\-04

Regression test sau mỗi chu kỳ huấn luyện; rollback tự động nếu chỉ số chính \(F1, hallucination rate\) suy giảm

Must Have

FR\-TRAIN\-05

Model size ≤ 8B tham số trong Giai đoạn 1 \(ràng buộc hạ tầng GPU nội bộ\)

Must Have

# __8\. YÊU CẦU PHI CHỨC NĂNG \(NON\-FUNCTIONAL REQUIREMENTS\)__

## __8\.1 Hiệu năng__

__Mã__

__Yêu cầu__

__Ngưỡng mục tiêu__

NFR\-PERF\-01

Latency sinh nháp discharge summary

≤ vài giây \(P95 < 15 giây\)

NFR\-PERF\-02

Latency de\-identification trên văn bản ≤ 1\.000 token

< 2 giây

NFR\-PERF\-03

Số người dùng đồng thời \(concurrent\) – ước lượng nội bộ theo quy mô Học viện Quân y

≥ 50 \(yêu cầu sizing GPU theo NFR\-PERF\-04 phải tương thích\)

NFR\-PERF\-04

VRAM tối đa trong inference với model 7B \(sử dụng quantization 4\-bit/8\-bit; con số là ước lượng nội bộ tham chiếu nghiên cứu PEFT\)

≤ 20 GB cho 1 instance; nếu concurrent ≥ 50 cần dự phòng nhiều instance

NFR\-PERF\-05

Uptime hệ thống trong giờ làm việc

≥ 99%

## __8\.2 Độ chính xác \(chỉ số tối thiểu trước pilot\)__

__Module__

__Chỉ số__

__Ngưỡng__

De\-identification

Recall PHI nhóm nguy cơ cao

≥ 0,99

NER lâm sàng

F1 macro

≥ 0,90

Giải nghĩa viết tắt nguy cơ cao

Accuracy

≥ 0,95

Hallucination nghiêm trọng

Rate ở trường bắt buộc

= 0

RAG Faithfulness

Score

≥ ngưỡng nội bộ đã định

Section segmentation

Accuracy

≥ 0,90

## __8\.3 Bảo mật__

- Toàn bộ hệ thống triển khai on\-premise hoặc trong private network bệnh viện\.
- Dữ liệu huấn luyện phải được de\-identify trước khi sử dụng\.
- Mã hóa dữ liệu at\-rest và in\-transit\.
- Xác thực đa yếu tố cho tài khoản quản trị\.
- Audit log lưu giữ ≥ 5 năm\.
- Nguyên tắc tham chiếu HIPAA/GDPR: tối thiểu hóa dữ liệu, giới hạn mục đích, kiểm soát truy cập theo vai trò\.

## __8\.4 Khả năng bảo trì và mở rộng__

- Cho phép cập nhật từ điển viết tắt mà không cần retrain mô hình\.
- Cho phép cập nhật kho chỉ mục RAG không downtime\.
- Pipeline fine\-tune có thể chạy lại với dữ liệu mới mỗi quý\.
- Hỗ trợ mở rộng sang chuyên khoa mới bằng cấu hình \(không cần viết lại core\)\.

## __8\.5 Tính minh bạch và tuân thủ chuẩn báo cáo__

- Mỗi phiên bản model triển khai có Model Card công bố nội bộ\.
- Mỗi dataset huấn luyện có Data Sheet đính kèm\.
- Mỗi pilot lâm sàng tiền cứu có protocol theo SPIRIT\-AI; báo cáo kết quả theo CONSORT\-AI\.
- Hệ thống cho phép truy vết \(lineage\) mỗi output về training data và tài liệu retrieval đã sử dụng\.

# __9\. QUY TRÌNH NGHIỆP VỤ \(BUSINESS PROCESS FLOWS\)__

## __9\.1 Quy trình hiện tại \(As\-Is\)__

- Bác sĩ khám bệnh → Ghi chép tay hoặc đánh máy trực tiếp vào HIS, thường mất 10–20 phút mỗi ca cho phần hành chính và bệnh án\.
- Sử dụng viết tắt tự do, không chuẩn hóa: cùng một viết tắt có thể có nghĩa khác nhau ở các khoa khác nhau, gây khó khăn khi bàn giao ca và hội chẩn liên khoa\.
- Không có kiểm tra nhất quán thuật ngữ: cùng một bệnh hoặc thuật ngữ có thể xuất hiện dưới nhiều biến thể \(Việt/Anh/Hán\-Việt/viết tắt\) trong cùng một bệnh án\.
- Báo cáo chẩn đoán hình ảnh không đồng nhất về cấu trúc giữa các bác sĩ và giữa các ca, gây khó cho phân tích thứ cấp\.
- Discharge summary thường được viết vào cuối ca làm việc, có thể bị thiếu thông tin hoặc copy\-paste từ ca trước → nguy cơ sai sót lâm sàng\.
- Lưu bệnh án vào HIS → Không có audit trail nội dung, không có khả năng truy vết nguồn của các kết luận trong bệnh án\.

## __9\.2 Quy trình tương lai – Radiology Report \(To\-Be, Use case 1\)__

- Bước 1: Bác sĩ hình ảnh nhập mô tả free\-text hoặc diễn giải
- Bước 2a: De\-identification check \(kiểm tra không có PHI trong radiology note\)
- Bước 2b: NER trích xuất phát hiện, cấu trúc hóa FINDINGS
- Bước 2c: RAG truy hồi template báo cáo chuyên khoa \(Modular RAG có rerank\)
- Bước 2d: LLM sinh nháp FINDINGS \+ IMPRESSION có cấu trúc, output tuân thủ FHIR R4/DICOM SR
- Bước 2e: Safety layer kiểm tra hallucination, mâu thuẫn và faithfulness
- Bước 3: Nháp hiển thị cho bác sĩ, có highlight citation nguồn
- Bước 4: Bác sĩ duyệt / chỉnh sửa / phê duyệt
- Bước 5: Audit log ghi diff; output lưu vào HIS/PACS theo chuẩn DICOM SR

## __9\.3 Quy trình tương lai – Discharge Summary \(To\-Be, Use case 2\)__

- Bước 1: Bác sĩ yêu cầu sinh discharge summary cho ca bệnh
- Bước 2: Hệ thống thu thập đầu vào từ HIS qua FHIR R4: thông tin nhập viện, diễn biến, xét nghiệm, thuốc, chẩn đoán
- Bước 3a: De\-identification toàn bộ PHI
- Bước 3b: NER trích xuất danh sách vấn đề, thuốc, thủ thuật
- Bước 3c: Normalization chuẩn hóa thuật ngữ và viết tắt theo 5 lớp \(BR\-01\)
- Bước 3d: Modular RAG truy hồi template discharge theo khoa, có rerank
- Bước 3e: LLM sinh nháp 6 section chuẩn
- Bước 3f: Safety layer: PHI check, hallucination check, consistency check, faithfulness check
- Bước 4: Hiển thị nháp với cờ bất định ở các trường cần xác nhận
- Bước 5: Bác sĩ phê duyệt, hệ thống lưu vào EHR và tạo audit log có provenance đầy đủ

# __10\. YÊU CẦU DỮ LIỆU__

## __10\.1 Nguồn dữ liệu đầu vào__

__Nguồn__

__Loại__

__Vai trò__

__Yêu cầu xử lý__

Bệnh án nội bộ đã ẩn danh

Văn bản lâm sàng

Fine\-tuning, RAG index, active learning

De\-identification bắt buộc; ethical approval

Từ điển viết tắt nội viện

Bảng tra cứu

Normalization, abbreviation expansion

Xây dựng theo khoa/phòng từ đầu \(xem Giả định 6\)

Phác đồ điều trị, hướng dẫn chuyên môn

Tài liệu chuẩn

RAG kho nội bộ

Version control, ngày hiệu lực

Mẫu biểu, template báo cáo, khuôn mẫu boilerplate

Cấu trúc

RAG kho nội bộ, chuẩn hóa lớp 5

Phân loại theo khoa, có versioning

MIMIC\-IV \(>520\.000 lượt nhập viện\)

EHR công khai \(US\)

Domain\-adaptive pretraining, benchmark

Credentialed access PhysioNet bắt buộc; tuân thủ DUA

MIMIC\-IV\-Note \(>2,6 triệu ghi chú; 331\.000 discharge\)

Clinical notes

DAPT, tóm tắt, discharge generation

Credentialed access PhysioNet

MIMIC\-CXR \(227\.835 imaging studies\)

Radiology reports \+ ảnh

Use case 1: structuring radiology

Credentialed access PhysioNet

VinDr\-CXR \(>100\.000 CXR Việt Nam\)

Imaging \+ report

Use case 1: structuring radiology, thuật ngữ ngực\-phổi tiếng Việt

Open dataset đã ẩn danh; tuân thủ license

Longitudinal\-MIMIC \(26\.625 BN longitudinal\)

EHR longitudinal

Học tiền điền có ngữ cảnh thời gian

Credentialed access PhysioNet

PadChest \(>160\.000 ảnh, 67k BN\)

Imaging \+ report

Mở rộng miền radiology, đa dạng từ vựng

Academic license

Bui et al\. 2025 \(~337\.000 cặp prompt\-response y khoa tiếng Việt\)

Instruction pairs

SFT instruction tuning tiếng Việt y khoa

Open access; bài báo Comput Methods Programs Biomed 2025

## __10\.2 Yêu cầu quản lý dữ liệu__

- De\-identification: 100% dữ liệu bệnh nhân phải được ẩn danh trước khi dùng cho bất kỳ tác vụ nào \(huấn luyện, RAG, lưu trữ, chia sẻ\)\.
- Version control: Tất cả tài liệu RAG có phiên bản và ngày hiệu lực\.
- Retention: Audit log lưu ≥ 5 năm; dữ liệu huấn luyện theo chính sách lưu giữ bệnh viện\.
- Lineage: Có thể truy vết mỗi output về training data và tài liệu retrieval đã sử dụng\.
- Consent: Quy trình đạo đức và pháp chế phê duyệt trước khi dùng dữ liệu nội bộ\.
- Credentialing: Truy cập MIMIC family yêu cầu PhysioNet credentialing \(CITI training \+ DUA\); cần được cấp trước khi bắt đầu giai đoạn dữ liệu\.
- Data Sheet: Mỗi dataset có Data Sheet mô tả: nguồn, kích thước, quy trình ẩn danh, license, hạn chế \(theo BR\-06\)\.

# __11\. GIAO DIỆN VÀ TÍCH HỢP HỆ THỐNG__

## __11\.1 Tích hợp đầu vào__

__Hệ thống__

__Giao thức__

__Dữ liệu trao đổi__

HIS \(Hospital Information System\)

HL7 v2 / FHIR R4

Thông tin nhập viện, xét nghiệm, chẩn đoán, thuốc

PACS \(Picture Archiving\)

DICOM / API nội bộ

Metadata ảnh chẩn đoán, báo cáo radiology

LIS \(Laboratory Information System\)

HL7 / API

Kết quả xét nghiệm

## __11\.2 Tích hợp đầu ra__

__Hệ thống__

__Giao thức__

__Dữ liệu trao đổi__

HIS/EHR

FHIR R4 / API

Discharge summary, bệnh án đã phê duyệt

PACS

DICOM SR / FHIR R4 / API

Báo cáo radiology có cấu trúc, FHIR\-compliant

Audit System

Syslog / Database

Log mọi thao tác người dùng và hệ thống

# __12\. GIẢ ĐỊNH VÀ RÀNG BUỘC__

## __12\.1 Giả định__

__\#__

__Giả định__

1

Bệnh viện/Học viện có hạ tầng GPU on\-premise tối thiểu 1 GPU ≥ 20 GB VRAM cho inference; nếu concurrent ≥ 50 cần dự phòng nhiều instance hoặc GPU bộ nhớ cao hơn\.

2

Có nguồn dữ liệu bệnh án nội bộ đủ đa dạng và có thể được ẩn danh hợp pháp\.

3

Bác sĩ đồng ý tham gia pilot và cung cấp phản hồi\.

4

Phòng pháp chế có thể xây dựng legal\-compliance matrix trong vòng 60 ngày đầu\.

5

HIS hiện tại hỗ trợ tích hợp API hoặc HL7/FHIR R4\.

6

Từ điển viết tắt nội viện sẽ phải được xây dựng từ đầu vì không có nguồn công khai đáng tin cậy về tần suất viết tắt trong bệnh án tiếng Việt – đây là deliverable bắt buộc của giai đoạn dữ liệu\.

7

Khung pháp lý Việt Nam cho AI y tế chưa có chi tiết áp dụng được trực tiếp; legal\-compliance matrix nội bộ phải được xây dựng và phê duyệt trong dự án, tham chiếu nguyên tắc HIPAA/GDPR\.

8

Tổ chức triển khai có thể hoàn tất PhysioNet credentialing \(CITI training \+ DUA\) cho team cần dùng MIMIC family trước giai đoạn dữ liệu\.

9

Nghiên cứu Bui et al\. 2025 và các nguồn quốc tế phản ánh đúng xu hướng kỹ thuật áp dụng cho tiếng Việt; tuy nhiên benchmark chuyển giao sang môi trường lâm sàng bệnh viện cần được kiểm chứng riêng\.

## __12\.2 Ràng buộc__

__\#__

__Ràng buộc__

__Nguồn gốc__

1

Toàn bộ xử lý dữ liệu bệnh nhân phải on\-premise hoặc trong private network bệnh viện

Bảo mật / pháp lý

2

Bác sĩ bắt buộc phê duyệt trước khi lưu bất kỳ output nào

An toàn lâm sàng

3

Không huấn luyện từ đầu \(from scratch\) trong Giai đoạn 1

Ràng buộc nguồn lực, không có bằng chứng ưu thế

4

Phải có ethical approval trước khi dùng dữ liệu bệnh nhân

Đạo đức nghiên cứu

5

Model size ≤ 8B tham số trong Giai đoạn 1

Hạ tầng GPU nội bộ

6

RAG bắt buộc kiến trúc Modular/Advanced; không sử dụng Naïve RAG cho use case nguy cơ cao

An toàn lâm sàng \(BR\-04\)

7

Mỗi phiên bản model phải có Model Card; mỗi dataset phải có Data Sheet

Tuân thủ chuẩn báo cáo \(BR\-06\)

# __13\. RỦI RO NGHIỆP VỤ__

__Mã__

__Rủi ro__

__Xác suất__

__Mức độ tác động__

__Biện pháp giảm thiểu__

R\-01

Thiếu dữ liệu nội bộ đạt chuẩn \(không đủ sạch, không đủ đa dạng\) – liên quan Giả định 2

Cao

Rất cao

Bắt đầu thu thập và ẩn danh ngay từ tháng 1; dùng corpus công khai \(MIMIC family, VinDr\-CXR, PadChest\) để bootstrap

R\-02

Viết tắt nội viện mơ hồ gây giải nghĩa sai → nguy cơ lâm sàng – liên quan Giả định 6

Cao

Rất cao

Xây từ điển viết tắt nội bộ theo khoa trước khi pilot; quy tắc "để trống nếu không chắc" \(FR\-GEN\-05\)

R\-03

Hallucination ở trường thông tin quan trọng \(thuốc, dị ứng\)

Trung bình

Rất cao

Safety layer bắt buộc \(FR\-SAFE\-03\); bác sĩ phê duyệt; test set kiểm tra trước pilot

R\-04

Bác sĩ lệ thuộc thụ động vào nháp, giảm kiểm tra

Trung bình

Cao

Training bác sĩ; đo số lỗi được phát hiện bởi bác sĩ; đánh dấu nháp là "đề xuất"

R\-05

Khoảng trống pháp lý Việt Nam chưa rõ ràng – liên quan Giả định 7

Trung bình

Cao

Workstream pháp chế độc lập; không triển khai rộng khi chưa có compliance matrix

R\-06

Hạ tầng GPU không đủ tải production khi mở rộng concurrent users \(NFR\-PERF\-03 ≥ 50\)

Trung bình

Trung bình

Sizing cẩn thận giai đoạn pilot; benchmark tải thực tế; dự phòng nhiều GPU instance hoặc cloud private

R\-07

Chất lượng mô hình giảm sau fine\-tune mới \(catastrophic forgetting\)

Trung bình

Cao

Regression test sau mỗi chu kỳ huấn luyện \(FR\-TRAIN\-04\); rollback tự động nếu F1 giảm

R\-08

Không hoàn tất PhysioNet credentialing kịp thời cho team – liên quan Giả định 8

Thấp

Trung bình

Bắt đầu thủ tục CITI training và DUA ngay từ tháng 1; có team backup

R\-09

Triển khai mô hình không có Model Card/Data Sheet → vi phạm BR\-06

Thấp

Cao

Tự động hóa sinh Model Card trong CI/CD; kiểm tra pre\-deployment bắt buộc

# __14\. LỘ TRÌNH VÀ MỐC TRIỂN KHAI__

## __14\.1 Lộ trình 12–24 tháng__

__Giai đoạn__

__Thời gian__

__Hoạt động chính__

__Milestone / Decision Gate__

Khởi động

T1–T2

Chọn use case đầu, phê duyệt governance, bắt đầu thu thập dữ liệu, khởi động PhysioNet credentialing

Phê duyệt ethical; bắt đầu xây từ điển viết tắt

Dữ liệu

T2–T5

Thu thập nguồn công khai \(MIMIC family, VinDr\-CXR, PadChest\); ẩn danh dữ liệu nội bộ; xây từ điển thuật ngữ

Dataset v1 ready; abbreviation dictionary v1; Data Sheet cho mỗi dataset → Gate 1

Mô hình – GĐ1

T4–T7

Baseline sidecar encoder cho de\-id và IE

De\-id Recall ≥ 0,99; NER F1 ≥ 0,90 → Gate 2

Mô hình – GĐ2

T6–T10

DAPT \+ SFT LLM tiếng Việt y khoa \(FR\-TRAIN\); tích hợp Modular RAG nội bộ

Mô hình draft v1; RAG index v1; Model Card v1

Đánh giá offline

T9–T11

Offline evaluation và failure analysis trên test set chuẩn

Báo cáo hallucination rate; benchmark report

Silent Mode

T11–T14

Hệ thống sinh nháp ngầm, so sánh với bệnh án thật

Silent mode report; QA review → Gate 3

Assisted Mode

T14–T17

Bác sĩ nhìn thấy nháp, chỉnh sửa, phê duyệt; protocol theo SPIRIT\-AI

Tỷ lệ chấp nhận ≥ mục tiêu; thời gian ghi chép giảm → Gate 4

Hardening

T17–T19

Bảo mật, audit, tối ưu hiệu năng, legal compliance

Security audit passed; legal\-compliance matrix v1\.0

Mở rộng

T19–T23

Thêm chuyên khoa thứ hai

Specialty \#2 pilot; Model Card v2

Quyết định triển khai

T23–T24

Review toàn bộ; quyết định triển khai rộng hoặc dừng; báo cáo CONSORT\-AI

Go/No\-Go decision

## __14\.2 Bốn điểm quyết định quan trọng \(Decision Gates\)__

__Gate__

__Điều kiện để tiếp tục__

__Vị trí trong roadmap__

Gate 1

Có được tập dữ liệu nội bộ đã ẩn danh đủ sạch và đủ đa dạng; mỗi dataset có Data Sheet

Cuối giai đoạn Dữ liệu \(T5\)

Gate 2

Sidecar de\-identification và NER đạt ngưỡng tin cậy để đưa vào pipeline thật

Cuối Mô hình – GĐ1 \(T7\)

Gate 3

Trong Silent Mode, mô hình giảm thời gian ghi chép mà không tăng lỗi lâm sàng

Cuối Silent Mode \(T14\)

Gate 4

Trong Assisted Mode, bác sĩ chấp nhận hệ thống như công cụ hỗ trợ thật sự

Cuối Assisted Mode \(T17\)

# __15\. TIÊU CHÍ CHẤP NHẬN \(ACCEPTANCE CRITERIA\)__

## __15\.1 Tiêu chí kỹ thuật \(trước pilot lâm sàng\)__

__Tiêu chí__

__Ngưỡng bắt buộc__

De\-identification Recall PHI nhóm nguy cơ cao

≥ 0,99

NER F1 macro

≥ 0,90

Accuracy viết tắt nhóm nguy cơ cao

≥ 0,95

Hallucination nghiêm trọng ở trường bắt buộc

= 0

PHI không rò rỉ trong output

100%

Section segmentation accuracy

≥ 0,90

RAG Faithfulness score

≥ ngưỡng nội bộ đã định

Tỷ lệ output có gắn citation đầy đủ

≥ 95%

Mỗi model triển khai có Model Card; mỗi dataset có Data Sheet

100%

## __15\.2 Tiêu chí vận hành \(sau Assisted Mode\)__

__Tiêu chí__

__Ngưỡng mục tiêu__

Thời gian hoàn tất tài liệu \(discharge summary\)

Giảm ≥ 20% so với baseline

Tỷ lệ bác sĩ chấp nhận nháp \(không từ chối hoàn toàn\)

≥ 60% sau 3 tháng

Số chỉnh sửa lớn \(major edit\) trên mỗi nháp

Giảm dần qua các chu kỳ

Latency đầu\-cuối P95

≤ 15 giây

Uptime trong giờ làm việc

≥ 99%

Pilot lâm sàng có protocol theo SPIRIT\-AI và báo cáo theo CONSORT\-AI

100%

# __16\. BẢNG CHÚ GIẢI THUẬT NGỮ__

__Thuật ngữ__

__Định nghĩa__

LLM

Large Language Model – Mô hình ngôn ngữ lớn

SFT

Supervised Fine\-Tuning – Tinh chỉnh có giám sát

DAPT

Domain\-Adaptive Pre\-Training – Tiền huấn luyện thích nghi miền

PEFT

Parameter\-Efficient Fine\-Tuning – Tinh chỉnh hiệu quả tham số

LoRA/QLoRA

Phương pháp PEFT giảm số tham số cần huấn luyện

RAG

Retrieval\-Augmented Generation – Sinh văn bản có tăng cường truy hồi

Modular RAG / Advanced RAG

Kiến trúc RAG có rerank, citation, faithfulness check; phù hợp use case nguy cơ cao

Naïve RAG

RAG cơ bản chỉ retrieve\+generate, không có rerank/check; KHÔNG dùng cho clinical use case

NER

Named Entity Recognition – Nhận dạng thực thể có tên

PHI

Protected Health Information – Thông tin sức khỏe được bảo vệ

De\-identification

Ẩn danh hóa – loại bỏ/che PHI khỏi văn bản

Pseudonymization

Thay PHI bằng định danh giả nhất quán theo bệnh nhân

Hallucination

Lỗi mô hình sinh ra thông tin sai không có cơ sở từ đầu vào

Faithfulness

Mức độ output trung thành với tài liệu nguồn được truy hồi

EHR/HIS

Electronic Health Record / Hospital Information System

FHIR

Fast Healthcare Interoperability Resources – Chuẩn trao đổi dữ liệu y tế \(HL7 FHIR R4\)

DICOM SR

DICOM Structured Reporting – Chuẩn báo cáo có cấu trúc cho radiology

RBAC

Role\-Based Access Control – Kiểm soát truy cập theo vai trò

On\-premise

Triển khai tại cơ sở, không dùng cloud công cộng

Active Learning

Học chủ động – dùng phản hồi người dùng để cải thiện mô hình

Silent Mode

Chế độ hệ thống sinh nháp ngầm, không hiển thị cho bác sĩ trong workflow thật

Assisted Mode

Chế độ bác sĩ nhìn thấy nháp và phê duyệt

Model Card

Tài liệu minh bạch mô tả mô hình: dữ liệu, đánh giá, hạn chế, use case

Data Sheet

Tài liệu mô tả dataset: nguồn, kích thước, ẩn danh, license

CONSORT\-AI

Checklist báo cáo kết quả thử nghiệm lâm sàng có AI \(mở rộng CONSORT\)

SPIRIT\-AI

Checklist protocol thử nghiệm lâm sàng có AI \(mở rộng SPIRIT\)

PhysioNet credentialing

Quy trình cấp quyền truy cập dữ liệu MIMIC: hoàn tất CITI training \+ ký Data Use Agreement

MIMIC

Medical Information Mart for Intensive Care – Bộ dữ liệu EHR công khai có kiểm soát của MIT/BIDMC

VinDr\-CXR

Bộ dữ liệu X\-quang ngực mở của Việt Nam \(>100\.000 ảnh từ 2 bệnh viện\)

HIPAA / GDPR

Khung pháp lý bảo vệ dữ liệu sức khỏe của Hoa Kỳ / Liên minh Châu Âu, dùng làm tham chiếu nguyên tắc

*Tài liệu này sẽ được cập nhật khi có thay đổi về yêu cầu, phạm vi hoặc ràng buộc\.*

*Mọi thay đổi cần được phê duyệt bởi các bên liên quan chính\.*

