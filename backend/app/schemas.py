
from pydantic import BaseModel
from typing import List

class FrameScore(BaseModel):
  idx: int
  score: float

class PredictResponse(BaseModel):
  label: str
  score: float
  threshold: float
  frames_analyzed: int
  per_frame: List[FrameScore]
