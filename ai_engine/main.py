from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from core.normalization import Normalizer
from core.deid import DeIdentifier
from core.ner import ClinicalNER
from core.generator import ClinicalGenerator
from core.rag import ClinicalRAG
from core.safety import SafetyChecker

app = FastAPI(title="ViMedAI Inference Engine")
normalizer = Normalizer()
deidentifier = DeIdentifier()
ner_engine = ClinicalNER()
generator = ClinicalGenerator()
rag_engine = ClinicalRAG()
safety_checker = SafetyChecker()

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

class SafetyCheckResponse(BaseModel):
    is_safe: bool
    phi_warnings: list[str]
    hallucination_warnings: list[str]

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
            draft_entities=request.draft_entities
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
