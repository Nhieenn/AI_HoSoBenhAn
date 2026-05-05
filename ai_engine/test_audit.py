from core.audit import AuditLogger, RBACManager, DataIsolator, TransparencyReporter

def test_audit_logger():
    logger = AuditLogger()
    log = logger.log_action("user123", "CREATE_DRAFT", "draft_999", {"ip": "10.0.0.5"})
    assert log["user_id"] == "user123"
    assert log["action"] == "CREATE_DRAFT"
    assert len(logger.get_logs()) == 1
    
    # Test immutable behavior (returns a copy)
    logs_copy = logger.get_logs()
    logs_copy[0]["action"] = "HACKED"
    assert logger.get_logs()[0]["action"] == "CREATE_DRAFT"

def test_rbac_manager():
    rbac = RBACManager()
    assert rbac.check_permission("DOCTOR", "approve_draft") == True
    assert rbac.check_permission("NURSE", "approve_draft") == False
    assert rbac.check_permission("ADMIN", "view_audit") == True
    assert rbac.check_permission("UNKNOWN", "view_audit") == False

def test_data_isolator():
    isolator = DataIsolator()
    assert isolator.verify_no_external_request("http://192.168.1.100/api") == True
    assert isolator.verify_no_external_request("http://10.0.0.5/api") == True
    assert isolator.verify_no_external_request("http://localhost:8080/api") == True
    assert isolator.verify_no_external_request("https://google.com/api") == False
    assert isolator.verify_no_external_request("https://aws.amazon.com/api") == False

def test_transparency_reporter():
    reporter = TransparencyReporter()
    model_card = reporter.generate_model_card()
    assert "version" in model_card
    assert model_card["model_name"] == "ViMedAI-Clinical-Generative"
    
    data_sheet = reporter.generate_data_sheet()
    assert "composition" in data_sheet
    
    protocol_ok = reporter.verify_clinical_protocol({
        "ai_intervention_description": "...",
        "human_ai_interaction": "...",
        "error_analysis_plan": "..."
    })
    assert protocol_ok["compliant"] == True
    
    protocol_fail = reporter.verify_clinical_protocol({
        "human_ai_interaction": "..."
    })
    assert protocol_fail["compliant"] == False
    assert "ai_intervention_description" in protocol_fail["missing_fields"]

if __name__ == "__main__":
    test_audit_logger()
    test_rbac_manager()
    test_data_isolator()
    test_transparency_reporter()
    print("All Audit and Security tests passed!")
