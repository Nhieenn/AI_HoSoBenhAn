import json
from core.rag import ClinicalRAG

rag = ClinicalRAG()
symptoms = "khó thở, ho, khạc đờm, khò khè, tức ngực"
query = symptoms

res = rag.retrieve_context(query)
with open('out_rag.txt', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
