import os

def demo_pdf_chunking(pdf_path: str):
    """
    KỊCH BẢN MÔ PHỎNG: Cắt file PDF Phác đồ Điều trị Nội khoa thành các 'Chunk' 
    để nạp vào Vector Database cho AI học ở Giai đoạn 2.
    
    (Thực tế chúng ta sẽ dùng thư viện PyMuPDF hoặc Langchain để cắt)
    """
    print("="*60)
    print(" [SNEAK PEEK PHASE 2] BĂM NHỎ TÀI LIỆU PDF CHO AI HỌC")
    print("="*60)
    
    # 1. Giả lập AI đang đọc 1 cuốn sách PDF Nội khoa dày 1000 trang
    print(f"\n[1] Đang đọc file PDF: '{pdf_path}'...")
    print("... Trích xuất chữ thành công (Loại bỏ hình ảnh, Header, Footer).")
    
    # Giả lập trang sách nội khoa
    pdf_text = """
    Trang 154 - Phác đồ điều trị Nhồi máu cơ tim cấp.
    Triệu chứng lâm sàng: Bệnh nhân có cơn đau thắt ngực điển hình, đau sau xương ức, 
    cảm giác bóp nghẹt, lan lên cằm hoặc vai trái. Đau kéo dài trên 20 phút, 
    không đáp ứng với Nitroglycerin. Vã mồ hôi, khó thở, hoảng hốt.
    Cận lâm sàng: Điện tâm đồ có ST chênh lên. Men tim Troponin T hoặc I tăng cao.
    Điều trị: Thở oxy, giảm đau bằng Morphine, thuốc chống đông máu. Cần can thiệp
    mạch vành qua da (PCI) cấp cứu trong vòng 120 phút.
    """
    
    # 2. Băm nhỏ văn bản (Chunking) với Overlap
    print("\n[2] Đang băm nhỏ (Chunking) dữ liệu để AI dễ tiêu hóa...")
    chunk_size = 50 # Chữ
    overlap = 10 # Chữ chồng lấp để không mất ngữ cảnh
    
    words = pdf_text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
            
    # 3. Kết quả sẽ đẩy vào Vector Database
    print("\n[3] Kết quả các khối (Chunks) sẽ được đưa vào Vector Database (Ổ D):")
    for idx, c in enumerate(chunks):
        print(f"  👉 Chunk {idx+1}: '{c} ...'")
        
    print("\n✅ Đây là cách chúng ta sẽ nhồi vài GB sách PDF vào não AI ở Giai đoạn 2!")

if __name__ == "__main__":
    demo_pdf_chunking("Phac_Do_Noi_Khoa_Bach_Mai_2023.pdf")
