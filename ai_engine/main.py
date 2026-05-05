from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from core.normalization import Normalizer
from core.deid import DeIdentifier
from core.ner import ClinicalNER
from core.generator import ClinicalGenerator

app = FastAPI(title="ViMedAI Inference Engine")
normalizer = Normalizer()
deidentifier = DeIdentifier()
ner_engine = ClinicalNER()
generator = ClinicalGenerator()

class NormalizeRequest(BaseModel):
    text: str
    dictionary: Optional[Dict[str, str]] = None

class NormalizeResponse(BaseModel):
    full_text: str
    sections: Dict[str, str]
    unknown_abbreviations: list[str]

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

@app.get("/")
def read_root():
    return {"message": "ViMedAI Inference Engine is running"}

@app.post("/normalize", response_model=NormalizeResponse)
async def normalize_text(request: NormalizeRequest):
    try:
        result = normalizer.process(request.text, request.dictionary)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
