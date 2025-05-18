# videolist
This is a simple, lightweight Flask web app for browsing and watching your home video collection. It scans a local directory for video files (like `.mkv`, `.mp4`, etc.), generates thumbnails, extracts metadata (duration, resolution, codec), and presents everything in a responsive, mobile-friendly web interface.

---

## 🚀 Features

- 📁 Scans a configurable folder for video files
- 🖼️ Generates thumbnails using `ffmpeg`
- 🧠 Displays video metadata: duration, resolution, codec
- 🌐 Plays videos directly in the browser (when supported)
- 📱 Responsive layout via Bootstrap 5
- 🛠️ Fully configurable via a simple `settings.ini` file

---

## 🧩 Requirements

- Python 3.7+
- `ffmpeg` installed and in your system's PATH  
  _(You can install it via [ffmpeg.org](https://ffmpeg.org/download.html), `brew install ffmpeg`, or your system package manager.)_

---

## ⚙️ Configuration (`settings.ini`)

```ini
[general]
video_folder = /your/path/to/videos
supported_extensions = .mkv,.mp4,.avi,.mov
thumbnail_time = 300
