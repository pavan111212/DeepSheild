
import cv2
import numpy as np
from typing import List

def sample_frames_from_video_bytes(data: bytes, num_frames: int = 16) -> List[np.ndarray]:
    # Write to temp buffer
    import tempfile, os
    fd, tmp_path = tempfile.mkstemp(suffix=".mp4")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)

        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            raise ValueError("Could not open video")
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
        idxs = np.linspace(0, max(frame_count - 1, 0), num_frames).astype(int)

        frames = []
        wanted = set(idxs.tolist())
        i = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if i in wanted:
                frames.append(frame)
            i += 1

        cap.release()
        if len(frames) == 0:
            raise ValueError("No frames extracted")
        return frames
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

def preprocess_frames(frames: List[np.ndarray], size: int = 224):
    # center-crop to square then resize to size x size; normalize to [-1,1]
    processed = []
    for img in frames:
        h, w = img.shape[:2]
        side = min(h, w)
        y0 = (h - side) // 2
        x0 = (w - side) // 2
        crop = img[y0:y0+side, x0:x0+side]
        resized = cv2.resize(crop, (size, size), interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        norm = (rgb - 0.5) / 0.5  # to [-1,1]
        processed.append(norm.transpose(2,0,1))  # C,H,W
    return np.stack(processed, axis=0)  # N,C,H,W
