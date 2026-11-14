# HiFi Canvas Video Repository (`HiFi-canvas`)

Community mapping and CDN resolver for Spotify-style looping background video canvases in **[HiFi Music](https://github.com/saferill/HiFi)**.

---

## Overview

HiFi Canvas enhances the Now Playing screen with looping ambient video clips behind the playback controls and synchronized lyrics. 

To maintain high performance and avoid repository bloat:
* **Binary `.mp4` video files are NOT stored in Git.**
* This repository hosts only lightweight metadata mappings (`v1/canvas.json`) that point to high-bandwidth edge CDN streaming URLs.
* The repository size stays under 1 MB while serving thousands of high-definition video loops.

---

## Schema (`v1/canvas.json`)

```json
{
  "jfKfPfyJRdk": {
    "title": "Lofi Hip Hop Radio",
    "videoUrl": "https://storage.googleapis.com/.../loop.mp4",
    "thumbUrl": "https://i.ytimg.com/vi/jfKfPfyJRdk/hqdefault.jpg"
  },
  "4xDzrJKXOOY": {
    "title": "Synthwave Radio",
    "videoUrl": "https://storage.googleapis.com/.../loop.mp4",
    "thumbUrl": "https://i.ytimg.com/vi/4xDzrJKXOOY/hqdefault.jpg"
  }
}
```

---

## Player Behavior

1. When a track starts, the client checks `v1/canvas.json` for the song's `videoId`.
2. If mapped, ExoPlayer initializes a lightweight background video surface that loops seamlessly.
3. If the user is on mobile data and has enabled **Data Saver** in settings, canvas video playback is automatically skipped to conserve bandwidth.

---

## Contributing

To submit a canvas mapping for a track:
1. Fork this repository.
2. Add your entry to `v1/canvas.json` using a valid HTTPS video URL (portrait 9:16 aspect ratio preferred, 1080p maximum, under 5 MB).
3. Run `python3 scripts/sync-canvas.py --check` to validate the file (the same check runs automatically on your Pull Request).
4. Open a Pull Request.

Each entry key must be the track's 11-character `videoId`, and `title`, `videoUrl` and `thumbUrl` are all required (`videoUrl` / `thumbUrl` must be `https://`).

---

## License

Open-source under the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.html).
