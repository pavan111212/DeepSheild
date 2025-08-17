
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PredictResponse
from .services.inference import predict_on_video_bytes
from .config import APP_VERSION

app = FastAPI(title="deepShield API", version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"version": APP_VERSION}

@app.post("/api/v1/predict", response_model=PredictResponse)
async def predict(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".webm")):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    data = await file.read()
    try:
        result = predict_on_video_bytes(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
