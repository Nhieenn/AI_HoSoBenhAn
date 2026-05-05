from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from core.normalization import Normalizer
from core.deid import DeIdentifier
from core.ner import ClinicalNER
from core.generator import ClinicalGenerator
from core.rag import ClinicalRAG
from core.safety import SafetyChecker
from core.workflow import WorkflowEngine
from core.audit import AuditLogger, RBACManager, DataIsolator, TransparencyReporter

app = FastAPI(title="ViMedAI Inference Engine")
normalizer = Normalizer()
deidentifier = DeIdentifier()
ner_engine = ClinicalNER()
generator = ClinicalGenerator()
rag_engine = ClinicalRAG()
safety_checker = SafetyChecker()
workflow_engine = WorkflowEngine()
audit_logger = AuditLogger()
rbac_manager = RBACManager()
data_isolator = DataIsolator()
transparency_reporter = TransparencyReporter()

class NormalizeRequest(BaseModel):
    text: str
    dictionary: Optional[Dict[str, str]] = None
    required_keys: Optional[list[str]] = None

class NormalizeResponse(BaseModel):
    full_text: str
    sections: Dict[str, str]
    unknown_abbreviations: list[str]
    compliance_warnings: Optional[list[str]] = None

class DeIdentifyRequest(BaseModel):
    text: str

class DeIdentifyResponse(BaseModel):
    masked_text: str
    audit_logs: list[Dict]

class NERRequest(BaseModel):
    text: str

class NERResponse(BaseModel):
    entities: list[Dict]

class GenerateDischargeRequest(BaseModel):
    patient_data: Dict[str, Any]
    entities: list[Dict]
    department: Optional[str] = "General"

class GenerateRadiologyRequest(BaseModel):
    raw_findings: str
    entities: list[Dict]
    department: Optional[str] = "XRay"

class GenerateResponse(BaseModel):
    generated_text: str

class RAGIndexRequest(BaseModel):
    content: str
    source: str = "Tài liệu Y khoa"
    metadata: Optional[Dict[str, Any]] = None

class RAGIndexResponse(BaseModel):
    document_id: str
    message: str

class RAGRetrieveRequest(BaseModel):
    query: str
    top_k: int = 3

class RAGRetrieveResponse(BaseModel):
    query: str
    combined_context: str
    citations: list[Dict]

class SafetyCheckRequest(BaseModel):
    draft_text: str
    original_entities: list[Dict]
    draft_entities: list[Dict]
    patient_data: Optional[Dict[str, Any]] = None

class SafetyCheckResponse(BaseModel):
    is_safe: bool
    phi_warnings: list[str]
    hallucination_warnings: list[str]
    conflict_warnings: Optional[list[str]] = None

class WorkflowCreateRequest(BaseModel):
    generated_text: str
    metadata: Optional[Dict[str, Any]] = None

class WorkflowReviewRequest(BaseModel):
    draft_id: str
    status: str
    updated_text: Optional[str] = None

class WorkflowSilentRequest(BaseModel):
    patient_data: Dict[str, Any]
    entities: list[Dict]
    department: Optional[str] = "General"
    type: str = "discharge" # or "radiology"
    raw_findings: Optional[str] = None

class AuditLogRequest(BaseModel):
    user_id: str
    action: str
    target_id: str
    details: Optional[Dict[str, Any]] = None

class RBACCheckRequest(BaseModel):
    role: str
    action: str

class UrlVerifyRequest(BaseModel):
    url: str

class ProtocolVerifyRequest(BaseModel):
    protocol_details: Dict[str, Any]

@app.get("/")
def read_root():
    return {"message": "ViMedAI Inference Engine is running"}

@app.post("/normalize", response_model=NormalizeResponse)
async def normalize_text(request: NormalizeRequest):
    try:
        result = normalizer.process(request.text, request.dictionary, request.required_keys)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/deidentify", response_model=DeIdentifyResponse)
async def deidentify_text(request: DeIdentifyRequest):
    try:
        result = deidentifier.process(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract", response_model=NERResponse)
async def extract_entities(request: NERRequest):
    try:
        entities = ner_engine.extract_entities(request.text)
        return {"entities": entities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/discharge", response_model=GenerateResponse)
async def generate_discharge(request: GenerateDischargeRequest):
    try:
        text = generator.generate_discharge_summary(request.patient_data, request.entities, request.department)
        return {"generated_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/radiology", response_model=GenerateResponse)
async def generate_radiology(request: GenerateRadiologyRequest):
    try:
        text = generator.generate_radiology_report(request.raw_findings, request.entities, request.department)
        return {"generated_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag/index", response_model=RAGIndexResponse)
async def index_document(request: RAGIndexRequest):
    try:
        doc_id = rag_engine.index_document(request.content, request.source, request.metadata)
        return {"document_id": doc_id, "message": "Document indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag/retrieve", response_model=RAGRetrieveResponse)
async def retrieve_context(request: RAGRetrieveRequest):
    try:
        result = rag_engine.retrieve_context(request.query, request.top_k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/safe/check", response_model=SafetyCheckResponse)
async def check_safety(request: SafetyCheckRequest):
    try:
        result = safety_checker.process_safety_check(
            draft_text=request.draft_text,
            original_entities=request.original_entities,
            draft_entities=request.draft_entities,
            patient_data=request.patient_data
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class FaithfulnessRequest(BaseModel):
    generated_text: str
    context: str

class FaithfulnessResponse(BaseModel):
    is_faithful: bool
    unsupported_claims: list[str]

@app.post("/rag/faithfulness", response_model=FaithfulnessResponse)
async def check_faithfulness(request: FaithfulnessRequest):
    try:
        result = rag_engine.check_faithfulness(request.generated_text, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow/draft/create")
async def workflow_create_draft(request: WorkflowCreateRequest):
    try:
        draft_id = workflow_engine.create_draft(request.generated_text, request.metadata)
        return {"draft_id": draft_id, "message": "Draft created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow/draft/review")
async def workflow_review_draft(request: WorkflowReviewRequest):
    try:
        # Update draft
        draft = workflow_engine.review_draft(request.draft_id, request.status, request.updated_text)
        
        # If approved, extract feedback
        feedback_result = None
        if draft["status"] == "APPROVED":
            feedback_result = workflow_engine.process_approved_draft(request.draft_id)
            
        return {"draft": draft, "feedback_processing": feedback_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow/generate/silent")
async def workflow_generate_silent(request: WorkflowSilentRequest):
    try:
        if request.type == "discharge":
            func = generator.generate_discharge_summary
            args = (request.patient_data, request.entities, request.department)
        elif request.type == "radiology":
            if not request.raw_findings:
                raise ValueError("raw_findings is required for radiology generation")
            func = generator.generate_radiology_report
            args = (request.raw_findings, request.entities, request.department)
        else:
            raise ValueError("Invalid type. Must be discharge or radiology")
            
        result = workflow_engine.generate_silent(func, *args)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audit/log")
async def audit_log(request: AuditLogRequest):
    try:
        log_entry = audit_logger.log_action(request.user_id, request.action, request.target_id, request.details)
        return {"message": "Log entry created", "log": log_entry}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audit/logs")
async def get_audit_logs():
    try:
        return {"logs": audit_logger.get_logs()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audit/check-permission")
async def audit_check_permission(request: RBACCheckRequest):
    try:
        has_permission = rbac_manager.check_permission(request.role, request.action)
        return {"role": request.role, "action": request.action, "has_permission": has_permission}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audit/verify-url")
async def audit_verify_url(request: UrlVerifyRequest):
    try:
        is_safe = data_isolator.verify_no_external_request(request.url)
        return {"url": request.url, "is_safe": is_safe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audit/model-card")
async def get_model_card():
    try:
        return transparency_reporter.generate_model_card()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audit/data-sheet")
async def get_data_sheet():
    try:
        return transparency_reporter.generate_data_sheet()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audit/verify-protocol")
async def verify_protocol(request: ProtocolVerifyRequest):
    try:
        return transparency_reporter.verify_clinical_protocol(request.protocol_details)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
