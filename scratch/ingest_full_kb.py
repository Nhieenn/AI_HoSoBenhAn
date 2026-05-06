import os
import json
import chromadb
from chromadb.utils import embedding_functions

def ingest_full_kb():
    print("="*60)
    print(" 🚀 KÍCH HOẠT CHIẾN DỊCH NẠP 1.251 BỆNH VÀO CHROMADB")
    print("="*60)
    
    kb_path = r"d:\AI_HoSoBenhAn\clean_knowledge_base.json"
    if not os.path.exists(kb_path):
        print(f"Lỗi: Không tìm thấy {kb_path}")
        return
        
    # 1. Đọc file JSON
    print(f"\n[1] Đang đọc siêu tệp Tri thức (1.7MB)...")
    with open(kb_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f" -> Đã đọc thành công {len(data)} bản ghi bệnh lý.")
    
    # 2. Xử lý Metadata
    print("\n[2] Đang tách Tên Bệnh và tạo Metadata...")
    chunks = []
    metadatas = []
    ids = []
    
    for i, item in enumerate(data):
        content = item.get("content", "")
        if not content: continue
        
        # Lấy tên bệnh (phần trước dấu hai chấm)
        parts = content.split(":")
        disease_name = parts[0].strip() if len(parts) > 1 else "Bệnh lý Nội khoa"
        
        meta = item.get("metadata", {})
        meta["disease"] = disease_name
        # Ép kiểu dữ liệu để ChromaDB không báo lỗi
        clean_meta = {}
        for k, v in meta.items():
            if isinstance(v, (str, int, float, bool)):
                clean_meta[k] = v
            else:
                clean_meta[k] = str(v)
                
        chunks.append(content)
        metadatas.append(clean_meta)
        ids.append(f"kb_disease_{i}")
        
    # 3. Kết nối ChromaDB
    db_path = r"d:\AI_HoSoBenhAn\vector_db"
    print(f"\n[3] Kết nối ChromaDB tại ổ D ({db_path})...")
    client = chromadb.PersistentClient(path=db_path)
    
    print(" -> Khởi tạo AI Nhúng (vietnamese-sbert)...")
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="keepitreal/vietnamese-sbert")
    
    collection_name = "vimedai_knowledge"
    try:
        client.delete_collection(name=collection_name)
    except:
        pass
        
    collection = client.create_collection(name=collection_name, embedding_function=ef)
    
    # 4. Nạp hàng loạt vào Vector DB
    print("\n[4] Đang bơm 1.251 bệnh vào Không gian Toán học Đa chiều (Vector Space)...")
    print(" -> Quá trình này sẽ chia thành nhiều đợt để tránh nghẽn RAM.")
    
    batch_size = 300
    total_added = 0
    for i in range(0, len(chunks), batch_size):
        end = min(i + batch_size, len(chunks))
        collection.add(
            documents=chunks[i:end],
            metadatas=metadatas[i:end],
            ids=ids[i:end]
        )
        total_added += (end - i)
        print(f"    + Tiến độ: {total_added}/{len(chunks)} bệnh đã được nhúng Vector...")
        
    print("\n✅ HOÀN TẤT CHIẾN DỊCH! AI ĐÃ SẴN SÀNG CHẨN ĐOÁN MỌI BỆNH!")
    print("="*60)

if __name__ == "__main__":
    ingest_full_kb()
