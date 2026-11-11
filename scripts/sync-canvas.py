import json
import os
import urllib.request

CANVAS_FILE = "v1/canvas.json"
os.makedirs("v1", exist_ok=True)

# Curated high-res loop canvas sources for popular hits
SAMPLE_CANVAS = {
  "jfKfPfyJRdk": {
    "title": "Lofi Hip Hop Radio",
    "videoUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "thumbUrl": "https://i.ytimg.com/vi/jfKfPfyJRdk/hqdefault.jpg"
  },
  "4xDzrJKXOOY": {
    "title": "Synthwave Radio",
    "videoUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "thumbUrl": "https://i.ytimg.com/vi/4xDzrJKXOOY/hqdefault.jpg"
  }
}

existing = {}
if os.path.exists(CANVAS_FILE):
    try:
        with open(CANVAS_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
    except Exception:
        existing = {}

existing.update(SAMPLE_CANVAS)

with open(CANVAS_FILE, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=2)

print(f"Canvas catalog updated. Total active canvases: {len(existing)}")
