import os
from flask import Flask, render_template, send_from_directory, abort
from utils.file_scanner import load_settings, scan_video_files
from utils.thumbnailer import generate_thumbnail, get_thumb_filename
from utils.metadata import extract_metadata

app = Flask(__name__)
settings = load_settings()
VIDEO_FOLDER = settings['video_folder']
EXTENSIONS = settings['supported_extensions']
THUMB_FOLDER = os.path.abspath('static/thumbs')

# Global map of video ID (hash) to full file path
video_id_map = {}

@app.route('/')
def index():
    video_files = scan_video_files(VIDEO_FOLDER, EXTENSIONS)
    videos = []

    for path in video_files:
        filename = os.path.basename(path)

        # Generate thumbnail and get filename
        thumb_path = generate_thumbnail(path)
        if not thumb_path:
            continue  # skip if thumbnail generation failed

        thumb_filename = os.path.basename(thumb_path)
        video_id = os.path.splitext(thumb_filename)[0]
        video_id_map[video_id] = path  # Register for download route

        metadata = extract_metadata(path)

        videos.append({
            'name': filename,
            'thumb_url': f'/thumbs/{thumb_filename}',
            'video_url': f'/video/{video_id}',
            'duration': f"{int(metadata.get('duration', 0) // 60)} min",
            'resolution': f"{metadata.get('width')}x{metadata.get('height')}" if metadata.get('width') else "Unknown",
            'codec': metadata.get('codec', 'Unknown')
        })

    return render_template('index.html', videos=videos)

@app.route('/thumbs/<filename>')
def serve_thumb(filename):
    return send_from_directory(THUMB_FOLDER, filename)

@app.route('/video/<video_id>')
def serve_video(video_id):
    path = video_id_map.get(video_id)
    if path and os.path.exists(path):
        return send_from_directory(os.path.dirname(path), os.path.basename(path), as_attachment=False)

    abort(404)

if __name__ == '__main__':
    app.run(debug=True)
