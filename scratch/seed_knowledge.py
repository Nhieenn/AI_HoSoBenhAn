import requests

API_URL = "http://localhost:8001/rag/index"

# Kiến thức từ Phác đồ điều trị của Bộ Y tế
knowledge_base = [
    {
        "content": "Sốt xuất huyết Dengue: Sốt cao đột ngột, liên tục từ 2-7 ngày. Triệu chứng kèm theo: Đau đầu, đau hốc mắt, đau cơ khớp, phát ban, dấu hiệu xuất huyết (chấm xuất huyết dưới da, chảy máu cam). Cận lâm sàng: Tiểu cầu giảm, Hematocrit tăng.",
        "source": "Phác đồ Bộ Y Tế 2023"
    },
    {
        "content": "Viêm loét dạ dày tá tràng: Đau vùng thượng vị, thường liên quan đến bữa ăn (đau khi đói hoặc ngay sau khi ăn). Có thể kèm buồn nôn, ợ hơi, ợ chua. Điều trị bằng kháng sinh (nếu có HP) và thuốc ức chế bơm Proton (PPI).",
        "source": "Hướng dẫn lâm sàng nội khoa"
    },
    {
        "content": "Thoái hóa khớp: Đau khớp kiểu cơ học, cứng khớp buổi sáng ngắn (< 30 phút). Có tiếng lục khục, lạo xạo khi cử động khớp. Thường gặp ở người cao tuổi (> 60 tuổi).",
        "source": "Phác đồ Cơ Xương Khớp - BV Bạch Mai"
    },
    {
        "content": "Thoát vị đĩa đệm cột sống: Đau lan dọc theo đường đi của dây thần kinh (đau thần kinh tọa), kèm tê bì, yếu cơ, hạn chế vận động. Chẩn đoán xác định bằng MRI cột sống.",
        "source": "Hướng dẫn chẩn đoán Ngoại thần kinh"
    }
]

for item in knowledge_base:
    try:
        response = requests.post(API_URL, json=item)
        print(f"Indexing: {item['content'][:50]}... -> {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
