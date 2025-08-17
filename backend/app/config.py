
import os

MODEL_THRESHOLD = float(os.getenv("MODEL_THRESHOLD", "0.5"))
FRAME_COUNT = int(os.getenv("FRAME_COUNT", "16"))
MODEL_PATH = os.getenv("MODEL_PATH", "weights/model.pt")
APP_VERSION = "1.0.0"
