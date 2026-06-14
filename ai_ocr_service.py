from fastapi import FastAPI

app = FastAPI(title="MedVerify AI/OCR Service")

@app.get("/")
def root():
    return {"message": "MedVerify AI/OCR Service is running!"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/docs")
def docs_redirect():
    return {"message": "Interactive API docs available at /docs"}