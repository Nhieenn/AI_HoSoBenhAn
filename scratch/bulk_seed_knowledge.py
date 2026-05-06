import requests

API_URL = "http://localhost:8001/rag/index"

medical_library = [
    # KHOA MẮT
    {"content": "Viêm kết mạc (Đau mắt đỏ): Mắt đỏ, cộm như có cát, chảy nước mắt, có nhiều rỉ (ghèn). Thị lực thường không giảm.", "source": "Phác đồ Nhãn khoa"},
    {"content": "Đục thủy tinh thể: Thị lực giảm từ từ, nhìn mờ như có màn sương, không đau nhức. Thường gặp ở người già.", "source": "Phác đồ Nhãn khoa"},
    
    # KHOA TIM MẠCH
    {"content": "Suy tim: Khó thở khi gắng sức, sau đó khó thở cả khi nghỉ ngơi. Phù chân, gan to, tĩnh mạch cổ nổi.", "source": "Tim mạch học lâm sàng"},
    {"content": "Cơn đau thắt ngực ổn định: Đau thắt sau xương ức khi gắng sức, giảm khi nghỉ hoặc dùng Nitroglycerin.", "source": "Phác đồ Tim mạch"},
    
    # KHOA TIÊU HÓA (MỞ RỘNG)
    {"content": "Viêm tụy cấp: Đau bụng dữ dội vùng trên rốn, đau lan ra sau lưng, nôn nhiều. Bụng chướng, ấn đau thượng vị.", "source": "Phác đồ Ngoại khoa"},
    {"content": "Xơ gan: Hội chứng suy tế bào gan (vàng da, sao mạch, lòng bàn tay son) và hội chứng tăng áp lực tĩnh mạch cửa (cổ trướng, tuần hoàn bàng hệ).", "source": "Bệnh học Nội khoa"},
    
    # KHOA TRUYỀN NHIỄM (MỞ RỘNG)
    {"content": "Sốt rét: Cơn sốt điển hình qua 3 giai đoạn: Rét run - Sốt nóng - Vã mồ hôi. Có yếu tố dịch tễ vùng sốt rét.", "source": "Phác đồ Truyền nhiễm"},
    
    # CƠ XƯƠNG KHỚP (ĐÃ CÓ)
    {"content": "Thoát vị đĩa đệm: Đau lan dọc dây thần kinh tọa, tê bì chân, yếu cơ.", "source": "Ngoại thần kinh"}
]

print("--- STARTING BULK INDEXING MEDICAL LIBRARY ---")
for item in medical_library:
    try:
        response = requests.post(API_URL, json=item)
        if response.status_code == 200:
            print(f"Indexed: {item['source']}")
    except:
        pass
print("--- BULK INDEXING COMPLETE ---")
