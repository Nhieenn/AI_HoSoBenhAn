import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_engine'))
from core.ner import ClinicalNER
from core.rag import ClinicalRAG

ner = ClinicalNER()
rag = ClinicalRAG()

text = "Tôi bị nóng hầm hập mấy bữa nay. Sáng dậy gập gối cứ kêu rột rột, đi cầu thang đau lan xuống tận bắp chân. À tôi cũng hay bị đầy chướng bụng, ợ chua nữa"
entities = ner.extract_entities(text)
symptoms = [e['text'] for e in entities if e['type'] == 'SYMPTOM']

query = ", ".join(symptoms)
res = rag.retrieve_context(query)

out = {
    "symptoms": symptoms,
    "top_citation": res['citations'][0] if res['citations'] else "None",
    "all_citations": [c['source'] + ": " + c['text_snippet'][:50] for c in res['citations']]
}

with open('out_viemtuy.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
