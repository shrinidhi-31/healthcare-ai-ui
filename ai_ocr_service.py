from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import easyocr
import numpy as np
import cv2
import uvicorn

app = FastAPI(title="MedVerify AI/OCR Service", version="1.0.0")

# Initialize EasyOCR
print("Loading EasyOCR model...")
reader = easyocr.Reader(['en'], gpu=False)
print("AI Service Ready!")

class SymptomRequest(BaseModel):
    symptoms: List[str]
    duration: Optional[str] = None
    age: Optional[int] = None

class SummarizeRequest(BaseModel):
    ocr_text: str

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0", "ocr_loaded": True}

@app.post("/internal/ocr/extract")
async def extract_ocr(file: UploadFile = File(...)):
    """Extract text from medical documents/prescriptions"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(400, "Could not decode image")
    
    results = reader.readtext(img)
    texts = [text for bbox, text, conf in results]
    full_text = " ".join(texts)
    
    # Check for emergency keywords (matches MedVerify alert system)
    emergency_keywords = ["chest pain", "difficulty breathing", "severe bleeding", 
                         "heart attack", "stroke", "unconscious", "emergency"]
    contains_emergency = any(kw in full_text.lower() for kw in emergency_keywords)
    
    return {
        "extracted_text": full_text,
        "word_count": len(texts),
        "confidence": round(sum(conf for bbox, text, conf in results) / len(results), 3) if results else 0,
        "contains_emergency_keywords": contains_emergency
    }

@app.post("/internal/triage/analyze")
async def analyze_symptoms(request: SymptomRequest):
    """Analyze symptoms and determine severity - matches MedVerify alert severity levels"""
    symptoms_lower = [s.lower() for s in request.symptoms]
    
    # HIGH severity (matches alert system)
    emergency_symptoms = ["chest pain", "difficulty breathing", "shortness of breath", 
                         "severe bleeding", "unconscious", "heart attack", "stroke"]
    high_urgency = [s for s in symptoms_lower if s in emergency_symptoms]
    
    if high_urgency:
        return {
            "severity": "HIGH",
            "reason": f"{', '.join(high_urgency)} detected",
            "recommendation": "Seek immediate medical attention. Call emergency services."
        }
    
    # MEDIUM severity
    medium_symptoms = ["fever", "vomiting", "diarrhea", "severe headache", "injury", "cough"]
    medium_urgency = [s for s in symptoms_lower if s in medium_symptoms]
    
    if medium_urgency:
        return {
            "severity": "MEDIUM",
            "reason": f"{', '.join(medium_urgency)} reported",
            "recommendation": "Consult a physician within 24-48 hours"
        }
    
    # LOW severity
    return {
        "severity": "LOW",
        "reason": "Non-urgent symptoms reported",
        "recommendation": "Monitor symptoms. Schedule routine appointment if needed."
    }

@app.post("/internal/report/summarize")
async def summarize_report(request: SummarizeRequest):
    """Summarize medical reports after OCR"""
    text = request.ocr_text.lower()
    
    # Simple extraction (can be enhanced)
    findings = []
    if "bp" in text or "blood pressure" in text:
        findings.append("Blood pressure mentioned")
    if "sugar" in text or "glucose" in text:
        findings.append("Blood sugar mentioned")
    if "medication" in text or "prescribed" in text:
        findings.append("Medications prescribed")
    
    return {
        "summary": f"Medical report analysis: {request.ocr_text[:200]}...",
        "key_findings": findings if findings else ["No specific findings extracted"],
        "abnormalities": ["Possible abnormal values detected"] if "abnormal" in text else []
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)