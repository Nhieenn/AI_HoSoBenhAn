import os
import PyPDF2
import chromadb
from chromadb.utils import embedding_functions

def ingest_pdf(pdf_path: str, collection_name: str = "vimedai_knowledge"):
    print("="*60)
    print(" 🚀 DATA INGESTION PIPELINE - CHUYỂN PDF VÀO VECTOR DB")
    print("="*60)
    print(f"\n[1] Bắt đầu đọc file PDF: {pdf_path}")
    
    # 1. Đọc PDF
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        print(f" -> Trích xuất thành công {len(text)} ký tự.")
    except Exception as e:
        print(f"Lỗi đọc PDF: {e}")
        return
    
    # 2. Băm nhỏ văn bản (Chunking)
    # Băm nhỏ (Chunking) theo Tiêu đề Bệnh (Header Extraction)
    print("\n[2] Băm nhỏ (Chunking) văn bản và Trích xuất Metadata...")
    
    import re
    lines = text.split('\n')
    chunks = []
    metadatas = []
    current_disease = "Bệnh lý Nội khoa"
    
    current_chunk_words = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Kiểm tra tiêu đề bệnh (VD: 1. BENH LY NOI TIET - DAI THAO DUONG TYPE 2)
        match = re.match(r"^\d+\.\s+.*?-\s+(.*)", line)
        if match:
            # Lưu chunk hiện tại (nếu có) trước khi chuyển sang bệnh mới
            if len(" ".join(current_chunk_words).strip()) > 10:
                chunks.append(" ".join(current_chunk_words))
                metadatas.append({"source": "PhacDo_NoiKhoa", "disease": current_disease})
                current_chunk_words = []
                
            # Cập nhật tên bệnh mới
            current_disease = match.group(1).strip()
            current_chunk_words.extend(line.split())
        else:
            current_chunk_words.extend(line.split())
            
            # Cắt chunk nếu đủ dài (50 chữ)
            if len(current_chunk_words) >= 50:
                chunks.append(" ".join(current_chunk_words))
                metadatas.append({"source": "PhacDo_NoiKhoa", "disease": current_disease})
                # Overlap: giữ lại 10 chữ cuối
                current_chunk_words = current_chunk_words[-10:]
                
    # Lưu nốt chunk cuối cùng
    if current_chunk_words and len(" ".join(current_chunk_words).strip()) > 10:
        chunks.append(" ".join(current_chunk_words))
        metadatas.append({"source": "PhacDo_NoiKhoa", "disease": current_disease})
            
    print(f" -> Đã băm thành {len(chunks)} khối (chunks) kèm theo Tag Tên Bệnh.")
    
    # 3. Kết nối ChromaDB
    # Đảm bảo database luôn nằm ở ổ D để không làm tràn ổ C
    db_path = r"d:\AI_HoSoBenhAn\vector_db"
    os.makedirs(db_path, exist_ok=True)
    
    print(f"\n[3] Kết nối ChromaDB tại ổ D ({db_path})...")
    client = chromadb.PersistentClient(path=db_path)
    
    # Dùng sentence-transformers embedding (sẽ tự động tải model về)
    print(" -> Khởi tạo AI Nhúng (Embedding Model: vietnamese-sbert)...")
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="keepitreal/vietnamese-sbert")
    
    # Xóa collection cũ nếu có để nạp lại từ đầu cho sạch
    try:
        client.delete_collection(name=collection_name)
    except:
        pass
        
    collection = client.create_collection(
        name=collection_name, 
        embedding_function=sentence_transformer_ef
    )
    
    # 4. Nhúng (Embed) và lưu vào DB
    print("\n[4] Đang nhúng (Embedding) vào Vector DB (Có thể mất vài phút tải Model lần đầu)...")
    
    ids = [f"pdf_chunk_{i}" for i in range(len(chunks))]
    # metadatas đã được tạo tự động ở vòng lặp băm nhỏ bên trên
    
    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    
    print("\n✅ HOÀN TẤT NẠP DỮ LIỆU VÀO CƠ SỞ DỮ LIỆU VECTOR!")
    print("="*60)

if __name__ == "__main__":
    pdf_path = r"d:\AI_HoSoBenhAn\ai_engine\data\PhacDo_NoiKhoa_Demo.pdf"
    if os.path.exists(pdf_path):
        ingest_pdf(pdf_path)
    else:
        print(f"Không tìm thấy file: {pdf_path}")
