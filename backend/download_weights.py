
'''
Attempts to fetch a public pretrained DeepFake detection model and save it to weights/model.pt.
This is optional — the app will run a heuristic fallback if unavailable.

You can replace the URLs with your preferred model (TorchScript recommended).
'''
import os
from pathlib import Path
import urllib.request

TARGET = Path(__file__).parent / "weights" / "model.pt"
TARGET.parent.mkdir(parents=True, exist_ok=True)

CANDIDATE_URLS = [
    # TODO: Replace with your curated, legal-to-redistribute model URLs.
    # Example placeholders (may require auth / may change):
    # "https://example.com/deepfake_xception_ffpp.torchscript",
]

def try_download(url: str) -> bool:
    try:
        print(f"Downloading: {url}")
        urllib.request.urlretrieve(url, TARGET)
        print(f"Saved to: {TARGET}")
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False

def main():
    if TARGET.exists():
        print("Weights already exist. Skipping.")
        return
    for url in CANDIDATE_URLS:
        if try_download(url):
            return
    print("No weights downloaded. The API will use the heuristic fallback model.")

if __name__ == '__main__':
    main()
