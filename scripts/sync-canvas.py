"""Validate and normalise v1/canvas.json.

Usage:
  python3 scripts/sync-canvas.py          # validate, seed defaults, rewrite file
  python3 scripts/sync-canvas.py --check  # validate only (used on pull requests)
"""
import json
import os
import re
import sys

CANVAS_FILE = "v1/canvas.json"
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
REQUIRED_FIELDS = ("title", "videoUrl", "thumbUrl")
URL_FIELDS = ("videoUrl", "thumbUrl")

# Seed entries. They are only added when missing, so edits made to
# v1/canvas.json (by maintainers or contributors) are never overwritten.
SAMPLE_CANVAS = {
    "jfKfPfyJRdk": {
        "title": "Lofi Hip Hop Radio",
        "videoUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "thumbUrl": "https://i.ytimg.com/vi/jfKfPfyJRdk/hqdefault.jpg",
    },
    "4xDzrJKXOOY": {
        "title": "Synthwave Radio",
        "videoUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "thumbUrl": "https://i.ytimg.com/vi/4xDzrJKXOOY/hqdefault.jpg",
    },
}


def _reject_duplicates(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key: {key!r}")
        seen[key] = value
    return seen


def load_catalog():
    """Load the catalog. A missing file is fine; a broken one is an error."""
    if not os.path.exists(CANVAS_FILE):
        return {}
    with open(CANVAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=_reject_duplicates)


def validate(catalog):
    errors = []
    if not isinstance(catalog, dict):
        return ["top level must be a JSON object keyed by videoId"]
    for video_id, entry in catalog.items():
        if not VIDEO_ID_RE.match(video_id):
            errors.append(f"{video_id!r}: not a valid 11-character videoId")
        if not isinstance(entry, dict):
            errors.append(f"{video_id!r}: entry must be an object")
            continue
        for field in REQUIRED_FIELDS:
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{video_id!r}: '{field}' must be a non-empty string")
            elif field in URL_FIELDS and not value.startswith("https://"):
                errors.append(f"{video_id!r}: '{field}' must be an https:// URL")
    return errors


def main():
    check_only = "--check" in sys.argv[1:]

    try:
        catalog = load_catalog()
    except (ValueError, OSError) as exc:
        # Never fall back to an empty catalog here: that would wipe every
        # community entry on the next automated commit.
        print(f"ERROR: cannot read {CANVAS_FILE}: {exc}", file=sys.stderr)
        return 1

    if not check_only and isinstance(catalog, dict):
        for video_id, entry in SAMPLE_CANVAS.items():
            catalog.setdefault(video_id, entry)

    errors = validate(catalog)
    if errors:
        print(f"ERROR: {CANVAS_FILE} is invalid:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    if check_only:
        print(f"{CANVAS_FILE} is valid. Total canvases: {len(catalog)}")
        return 0

    os.makedirs(os.path.dirname(CANVAS_FILE), exist_ok=True)
    tmp_file = CANVAS_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp_file, CANVAS_FILE)

    print(f"Canvas catalog updated. Total active canvases: {len(catalog)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
