
import torch
import torch.nn as nn
from pathlib import Path
from typing import Optional

class SimpleHead(nn.Module):
    # a tiny head if backbone is feature extractor returning (N, C)
    def __init__(self, in_ch=512):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(in_ch, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(256, 1)
        )

    def forward(self, x):
        return self.mlp(x).squeeze(1)

class HeuristicModel(nn.Module):
    '''
    Fallback model that computes a simple score from per-frame statistics.
    DO NOT use in production, it's only to keep the app functional without real weights.
    '''
    def __init__(self):
        super().__init__()
        self.bias = nn.Parameter(torch.tensor(0.0))
        self.scale = nn.Parameter(torch.tensor(1.0))

    @torch.no_grad()
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (N, C, H, W) normalized frames
        # Simple temporal artifact proxy: high-frequency energy approximated via Sobel-like ops
        sobel_x = x[:, :, :, 1:] - x[:, :, :, :-1]
        sobel_y = x[:, :, 1:, :] - x[:, :, :-1, :]
        hf = (sobel_x.abs().mean(dim=(1,2,3)) + sobel_y.abs().mean(dim=(1,2,3))) / 2.0
        logits = self.scale * (hf - 0.25) + self.bias
        return logits

def load_model(model_path: str) -> Optional[nn.Module]:
    p = Path(model_path)
    if p.exists():
        try:
            model = torch.jit.load(str(p), map_location="cpu")
            model.eval()
            return model
        except Exception:
            # try to load state dict
            try:
                state = torch.load(str(p), map_location="cpu")
                # Expecting a dict with 'backbone_out' channels; adapt as needed
                model = SimpleHead(in_ch=512)
                model.load_state_dict(state)
                model.eval()
                return model
            except Exception:
                pass
    # fallback
    fallback = HeuristicModel()
    fallback.eval()
    return fallback
