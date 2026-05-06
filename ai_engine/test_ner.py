import sys
import os

# Add the current directory to sys.path to import core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.ner import ClinicalNER

def test_ner_extraction():
    ner = ClinicalNER()
    
    test_text = """
    Bệnh nhân nam, 45 tuổi. 
    Tiền sử: Tăng huyết áp 5 năm, đái tháo đường type 2.
    Hiện tại: Bệnh nhân không sốt, không ho, có đau đầu nhẹ.
    Chỉ định cận lâm sàng: Xét nghiệm Glucose máu, HbA1c, siêu âm tim.
    Điều trị: Paracetamol 500mg uống 2 lần/ngày. Amlodipin 5mg.
    """
    
    print("Original Text:")
    print(test_text)
    print("-" * 40)
    
    entities = ner.extract_entities(test_text)
    
    print("Extracted Entities:")
    for ent in entities:
        neg = "[NEGATED] " if ent["is_negative"] else ""
        ontology_str = f" (Ontology: {ent['ontology']})" if ent['ontology'] else ""
        print(f"- {neg}{ent['type']}: '{ent['text']}' at [{ent['start']}:{ent['end']}]{ontology_str}")
        
    print("-" * 40)
    
    # Assertions for verification
    types_found = [e["type"] for e in entities]
    texts_found = [e["text"].lower() for e in entities]
    
    # Check if all types are extracted
    assert "DISEASE" in types_found
    assert "SYMPTOM" in types_found
    assert "TEST" in types_found
    assert "DRUG" in types_found
    assert "DOSAGE" in types_found
    assert "PROCEDURE" in types_found
    
    # Check negation for "sốt" and "ho"
    sot_entity = next((e for e in entities if e["text"].lower() == "sốt"), None)
    assert sot_entity is not None
    assert sot_entity["is_negative"] is True
    
    ho_entity = next((e for e in entities if e["text"].lower() == "ho"), None)
    assert ho_entity is not None
    assert ho_entity["is_negative"] is True
    
    # Check non-negation for "đau đầu"
    daudau_entity = next((e for e in entities if e["text"].lower() == "đau đầu"), None)
    assert daudau_entity is not None
    assert daudau_entity["is_negative"] is False
    
    # Check ontology linkage
    tha_entity = next((e for e in entities if e["text"].lower() == "tăng huyết áp"), None)
    assert tha_entity is not None
    assert tha_entity["ontology"] == {"code": "I10", "system": "ICD-10"}
    
    print("All NER tests passed!")

if __name__ == "__main__":
    test_ner_extraction()
