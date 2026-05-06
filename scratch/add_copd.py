import json
import os

kb_path = "d:\\AI_HoSoBenhAn\\knowledge_base.json"
with open(kb_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data.append({
    "content": "Bệnh phổi tắc nghẽn mãn tính (COPD): Bệnh phổi tắc nghẽn mãn tính (COPD) là một bệnh viêm phổi mãn tính gây tắc nghẽn luồng khí từ phổi. Các triệu chứng bao gồm khó thở, ho, tạo đờm (khạc đờm) và thở khò khè. Bệnh thường do tiếp xúc lâu dài với các chất khí kích thích hoặc hạt vật chất, thường là từ khói thuốc lá. Triệu chứng: khó thở kéo dài, tăng lên khi gắng sức, ho nhiều, khạc đờm nhầy màu đục đặc biệt vào buổi sáng sớm, thở khò khè, tức ngực nhẹ. Sụt cân, mệt mỏi.",
    "metadata": {
        "source": "YouMed",
        "url": "https://youmed.vn/tin-tuc/benh-phoi-tac-nghen-man-tinh-copd/",
        "scrapedAt": "2026-05-06T12:00:00Z"
    }
})

with open(kb_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Added COPD to KB. Total items:", len(data))
