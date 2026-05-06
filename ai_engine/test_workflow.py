from core.workflow import WorkflowEngine

def test_workflow_engine():
    engine = WorkflowEngine()
    
    # 1. Test Create Draft
    original_text = "Bệnh nhân bị viêm họng, cho uống Paracetamol."
    draft_id = engine.create_draft(original_text, {"department": "General"})
    assert draft_id in engine.drafts
    assert engine.drafts[draft_id]["status"] == "DRAFT"
    
    # 2. Test Review & Approve without change
    engine.review_draft(draft_id, "APPROVED")
    assert engine.drafts[draft_id]["status"] == "APPROVED"
    res = engine.process_approved_draft(draft_id)
    assert res["feedback_recorded"] == False
    
    # 3. Test Review with changes (Active Learning)
    original_text_2 = "Chẩn đoán: Sốt xuất huyết. Xử trí: Truyền dịch."
    draft_id_2 = engine.create_draft(original_text_2)
    
    updated_text = "Chẩn đoán: Sốt xuất huyết Dengue. Xử trí: Truyền dịch tĩnh mạch."
    engine.review_draft(draft_id_2, "APPROVED", updated_text)
    
    res_2 = engine.process_approved_draft(draft_id_2)
    assert res_2["feedback_recorded"] == True
    assert len(engine.feedbacks) == 1
    
    feedback = res_2["feedback"]
    assert "Dengue" in str(feedback["changes"])
    assert "tĩnh mạch" in str(feedback["changes"])
    
    # 4. Test Silent Mode
    def dummy_generator(text):
        return f"Generated: {text}"
        
    silent_res = engine.generate_silent(dummy_generator, "Test Data")
    assert silent_res["is_silent"] == True
    assert silent_res["generated_text"] == "Generated: Test Data"
    
if __name__ == "__main__":
    test_workflow_engine()
    print("All Workflow tests passed!")
