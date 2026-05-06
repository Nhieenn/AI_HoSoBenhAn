import json
from core.ner import ClinicalNER

ner = ClinicalNER()

text = "Bệnh nhân nam 65 tuổi, tiền sử hút thuốc lá 30 bao-năm. Bệnh nhân đi khám vì tình trạng khó thở kéo dài nhiều tháng nay, khó thở tăng lên rõ rệt khi leo cầu thang hoặc gắng sức. Gần đây bệnh nhân ho nhiều, khạc đờm nhầy màu đục đặc biệt vào buổi sáng sớm. Nghe phổi có tiếng thở khò khè, tức ngực nhẹ."

entities = ner.extract_entities(text)
print(json.dumps(entities, ensure_ascii=False, indent=2))
