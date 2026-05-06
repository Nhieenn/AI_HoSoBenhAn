from ai_engine.core.ner import ClinicalNER

ner = ClinicalNER()
text = "Đau dạ dày dữ dội khi ăn cà chua"
entities = ner.extract_entities(text)

print(f"Text: {text}")
print(f"Entities found: {entities}")

if not entities:
    print("FAILED: No entities detected!")
else:
    print("SUCCESS: Entities detected.")
