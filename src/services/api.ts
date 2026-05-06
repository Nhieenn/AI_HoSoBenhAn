const API_BASE_URL = '/api/proxy';

// MODULE 1: Normalization
export const normalizeText = async (text: string) => {
  const res = await fetch(`${API_BASE_URL}/normalize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return res.json();
};

// MODULE 2: De-identification
export const deidentifyText = async (text: string) => {
  const res = await fetch(`${API_BASE_URL}/deidentify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return res.json();
};

// MODULE 3: NER Extraction
export const extractEntities = async (text: string) => {
  const res = await fetch(`${API_BASE_URL}/extract`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return res.json();
};

// MODULE 4: Generation
export const generateDischarge = async (patientData: any, entities: any[], department: string) => {
  const res = await fetch(`${API_BASE_URL}/generate/discharge`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ patient_data: patientData, entities, department })
  });
  return res.json();
};

export const generateRadiology = async (rawFindings: string, entities: any[], department: string) => {
  const res = await fetch(`${API_BASE_URL}/generate/radiology`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ raw_findings: rawFindings, entities, department })
  });
  return res.json();
};

// MODULE 5: RAG Retrieve
export const retrieveContext = async (query: string, top_k: number = 3) => {
  const res = await fetch(`${API_BASE_URL}/rag/retrieve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, top_k })
  });
  return res.json();
};

// MODULE 6: Safety Check
export const checkSafety = async (draftText: string, originalEntities: any[], draftEntities: any[], patientData: any = null) => {
  const res = await fetch(`${API_BASE_URL}/safe/check`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      draft_text: draftText, 
      original_entities: originalEntities, 
      draft_entities: draftEntities, 
      patient_data: patientData 
    })
  });
  return res.json();
};

export const checkFaithfulness = async (generatedText: string, context: string) => {
  const res = await fetch(`${API_BASE_URL}/rag/faithfulness`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ generated_text: generatedText, context })
  });
  return res.json();
};

// MODULE 7: Audit
export const logAudit = async (userId: string, action: string, targetId: string, details: any = null) => {
  const res = await fetch(`${API_BASE_URL}/audit/log`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, action, target_id: targetId, details })
  });
  return res.json();
};

// MODULE 8: Active Learning & Fine-tuning
export const saveTrainingData = async (instruction: string, inputText: string, outputText: string) => {
  const res = await fetch(`${API_BASE_URL}/training/active-learning/save`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ instruction, input_text: inputText, output_text: outputText })
  });
  return res.json();
};

export const extractDiff = async (originalText: string, editedText: string) => {
  const res = await fetch(`${API_BASE_URL}/training/active-learning/diff`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ original_text: originalText, edited_text: editedText })
  });
  return res.json();
};

export const approveReport = async (id: string, originalText: string, finalReport: string) => {
  // 1. Save for Active Learning (Module 8)
  await saveTrainingData("Chỉnh sửa báo cáo y khoa", originalText, finalReport);
  // 2. Log Audit (Module 7)
  return await logAudit("BSHUNG", "APPROVE_REPORT", id, { report_length: finalReport.length });
};

export const startFinetune = async (datasetPath: string, modelId: string = "vinai/PhoGPT-7B") => {
  const res = await fetch(`${API_BASE_URL}/training/finetune/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ dataset_path: datasetPath, model_id: modelId })
  });
  return res.json();
};

export const getModelCard = async () => {
  const res = await fetch(`${API_BASE_URL}/audit/model-card`);
  return res.json();
};

export const getAuditLogs = async () => {
  const res = await fetch(`${API_BASE_URL}/audit/logs`);
  return res.json();
};
