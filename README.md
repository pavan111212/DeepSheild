
# deepShield — DeepFake Video Detection (Ready-to-Deploy)

A full-stack app to classify **DeepFake vs Real** on uploaded videos. It includes:

- **Backend**: FastAPI + PyTorch (frame sampling with OpenCV), probability score, per-frame insights, health checks.
- **Frontend**: React + Vite + TypeScript + Tailwind, modern UI/UX with drag-and-drop upload, progress, result cards.
- **Containerization**: Dockerfiles for backend and frontend + `docker-compose.yml`.
- **Weights**: Script to fetch a public pretrained DeepFake detection model. A *fallback* lightweight heuristic model is included so the app still runs even if weights can’t be fetched. (Replace with your preferred SOTA model for production.)

---

## Quick Start

### 1) One-command local dev (requires Node 18+, Python 3.10+, FFmpeg)
```bash
# 1. Backend
cd backend
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python download_weights.py  # Optional, fetches a pretrained model
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 2. Frontend
cd ../frontend
npm install
npm run dev  # opens http://localhost:5173
```

### 2) Docker (recommended for deployment)
```bash
# from the project root
docker compose up --build
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000/docs
```

> **Note**: The backend will gracefully fall back to a built-in heuristic model if pretrained weights are not present.

---

## Backend Overview

- **Endpoint**: `POST /api/v1/predict` with a `multipart/form-data` field `file` (video).
- **Response**:
```json
{
  "label": "fake" | "real",
  "score": 0.87,
  "threshold": 0.5,
  "frames_analyzed": 16,
  "per_frame": [ { "idx": 0, "score": 0.82 }, ... ]
}
```
- **Health**: `GET /health` and `GET /version`

### Model Handling
- If `backend/weights/model.pt` exists, it will be used (PyTorch). You can fetch one via `download_weights.py`.
- Otherwise, the system uses a **fallback heuristic** (statistical temporal inconsistencies). Useful for demos, **not** production.

### Frame Sampling
- Extracts ~16 evenly-spaced frames per video.
- Preprocessing: 224×224 center-crop, normalization.
- Aggregation: mean of per-frame logits to a single probability.

---

## Frontend Overview

- Drag-and-drop or click to upload.
- Shows a playable preview (client-side), upload progress, and results with confidence and frame insights.
- Clean, responsive UI built with Tailwind.

---

## Environment Variables

Copy `.env.example` to `.env` and adjust as needed.

- `API_BASE_URL` (frontend): defaults to `http://localhost:8000`.
- `MODEL_THRESHOLD` (backend): default 0.5.
- `FRAME_COUNT` (backend): default 16.

---

## Production Notes

- Replace the fallback with your chosen SOTA model.
- Consider GPU build images for speed (see comments in `Dockerfile.backend`).
- Put your own weights in `backend/weights/model.pt` (TorchScript or state_dict is fine if loader updated).

---

## License

MIT — see `LICENSE`.
