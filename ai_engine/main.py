from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from core.normalization import Normalizer
from core.deid import DeIdentifier
from core.ner import ClinicalNER

app = FastAPI(title="ViMedAI Inference Engine")
normalizer = Normalizer()
deidentifier = DeIdentifier()
ner_engine = ClinicalNER()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
