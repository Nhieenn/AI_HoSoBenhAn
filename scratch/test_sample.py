import json
import random
with open('clean_knowledge_base.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

valid_diseases = [d for d in data if len(d.get('metadata', {}).get('title', '')) > 2]
samples = random.sample(valid_diseases, 5)

for s in samples:
    title = s['metadata'].get('title', '')
    print(f"- Bệnh: {title}")
    print(f"  Triệu chứng: {s['content'][:150]}...\n")
