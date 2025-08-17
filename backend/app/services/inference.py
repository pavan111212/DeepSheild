
import torch
import numpy as np
from typing import Dict, Any
from ..config import MODEL_THRESHOLD, FRAME_COUNT, MODEL_PATH
from ..models.loader import load_model
from .video_utils import sample_frames_from_video_bytes, preprocess_frames

_model = None

def get_model():
    global _model
    if _model is None:
        _model = load_model(MODEL_PATH)
    return _model

def predict_on_video_bytes(data: bytes) -> Dict[str, Any]:
    frames = sample_frames_from_video_bytes(data, num_frames=FRAME_COUNT)
    arr = preprocess_frames(frames, size=224)  # N,C,H,W
    x = torch.from_numpy(arr)  # float32

    model = get_model()
    with torch.no_grad():
        logits = model(x)  # (N,) or (N,1)
        if logits.ndim > 1:
            logits = logits.squeeze(1)
        probs = torch.sigmoid(logits).cpu().numpy()

    score = float(np.mean(probs))
    label = "fake" if score >= MODEL_THRESHOLD else "real"
    per_frame = [{"idx": int(i), "score": float(s)} for i, s in enumerate(probs.tolist())]

    return {
        "label": label,
        "score": score,
        "threshold": MODEL_THRESHOLD,
        "frames_analyzed": len(per_frame),
        "per_frame": per_frame,
    }
