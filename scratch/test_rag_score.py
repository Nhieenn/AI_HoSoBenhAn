import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_engine'))

from core.rag import ClinicalRAG
rag = ClinicalRAG()

text = "Bệnh nhân nam 65 tuổi, tiền sử hút thuốc lá 30 bao-năm. Bệnh nhân đi khám vì tình trạng khó thở kéo dài nhiều tháng nay, khó thở tăng lên rõ rệt khi leo cầu thang hoặc gắng sức. Gần đây bệnh nhân ho nhiều, khạc đờm nhầy màu đục đặc biệt vào buổi sáng sớm. Nghe phổi có tiếng thở khò khè, tức ngực nhẹ."
symptoms = "khó thở, ho"
query = f"{symptoms} {text}"

res = rag.retrieve_context(query)
print(res)
