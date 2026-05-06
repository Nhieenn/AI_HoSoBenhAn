import json

try:
    with open('knowledge_base.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total entries: {len(data)}")
    
    malaria_entries = []
    for item in data:
        if 'sốt rét' in json.dumps(item, ensure_ascii=False).lower():
            malaria_entries.append(item)
            
    with open('scratch/kb_sot_ret.json', 'w', encoding='utf-8') as f:
        json.dump(malaria_entries, f, ensure_ascii=False, indent=2)

    print(f"Found {len(malaria_entries)} entries related to 'sốt rét'. Results written to scratch/kb_sot_ret.json")

except Exception as e:
    print("Error:", e)
