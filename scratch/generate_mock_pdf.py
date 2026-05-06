import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def create_medical_pdf(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Thiết lập Font cơ bản (không cần Unicode font phức tạp nếu chỉ dùng Tiếng Việt cơ bản hoặc không dấu, 
    # nhưng để tốt nhất ta cứ xuất tiếng Việt nếu font chuẩn hỗ trợ, mặc định reportlab Helvetica ko hỗ trợ tiếng Việt có dấu tốt
    # Do đó, để nhanh chóng cho POC, tôi sẽ xuất nội dung tiếng Việt có dấu bằng cách dùng font mặc định nếu máy tính có, 
    # hoặc ta cứ viết tiếng Việt, reportlab có thể in ra chữ lỗi font tí cũng không sao vì AI đọc text.
    # Nhưng để an toàn tránh lỗi Unicode, ta dùng tiếng Việt chuẩn không dấu hoặc cài font.
    # Thôi ta cứ dùng string cơ bản)
    
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, y, "HƯỚNG DẪN CHẨN ĐOÁN VÀ ĐIỀU TRỊ BỆNH NỘI KHOA")
    
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(100, y, "BỘ Y TẾ - XUẤT BẢN NĂM 2024")
    
    y -= 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "1. BENH LY NOI TIET - DAI THAO DUONG TYPE 2")
    y -= 20
    c.setFont("Helvetica", 11)
    text1 = "Dai thao duong type 2 la benh ly noi tiet pho bien. Trieu chung bao gom: "
    text2 = "an nhieu, uong nhieu nuoc do khac, di tieu nhieu lan, sut can khong ro nguyen nhan."
    text3 = "Benh nhan thuong xuyen met moi. Dieu tri bang Metformin 500mg, an kieng, tap the duc."
    c.drawString(50, y, text1)
    y -= 15
    c.drawString(50, y, text2)
    y -= 15
    c.drawString(50, y, text3)

    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "2. BENH LY TIM MACH - SUY TIM MAN TINH")
    y -= 20
    c.setFont("Helvetica", 11)
    text4 = "Suy tim man tinh dac trung boi tinh trang tim khong the bom du mau."
    text5 = "Trieu chung lam sang: Kho tho khi nam dau thap, phu mem hai chi duoi, an lom."
    text6 = "Benh nhan cam thay met moi khi van dong nhe. Tinh mach co noi ro."
    text7 = "Dieu tri: Loi tieu Furosemide, thuoc uc che men chuyen ACE inhibitor."
    c.drawString(50, y, text4)
    y -= 15
    c.drawString(50, y, text5)
    y -= 15
    c.drawString(50, y, text6)
    y -= 15
    c.drawString(50, y, text7)
    
    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "3. BENH LY HO HAP - HEN PHE QUAN (ASTHMA)")
    y -= 20
    c.setFont("Helvetica", 11)
    text8 = "Hen phe quan la tinh trang viem man tinh duong tho."
    text9 = "Trieu chung: Ho keo dai dac biet ve dem hoac gan sang, kho khe, kho tho."
    text10 = "Nang nguc. Cac trieu chung thuong khoi phat khi tiep xuc di nguyen (phan hoa)."
    text11 = "Thuoc cat con: Salbutamol xit. Thuoc du phong: ICS/LABA."
    c.drawString(50, y, text8)
    y -= 15
    c.drawString(50, y, text9)
    y -= 15
    c.drawString(50, y, text10)
    y -= 15
    c.drawString(50, y, text11)

    c.save()

if __name__ == "__main__":
    os.makedirs(r"d:\AI_HoSoBenhAn\ai_engine\data", exist_ok=True)
    create_medical_pdf(r"d:\AI_HoSoBenhAn\ai_engine\data\PhacDo_NoiKhoa_Demo.pdf")
    print("Created PhacDo_NoiKhoa_Demo.pdf successfully!")
