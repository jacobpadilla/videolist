import os
import hashlib
import configparser
import ffmpeg

THUMB_DIR = os.path.abspath('static/thumbs')
CONFIG_PATH = 'config/settings.ini'

def load_thumbnail_time(config_path=CONFIG_PATH) -> int:
    config = configparser.ConfigParser()
    config.read(config_path)
    raw_value = config.get('general', 'thumbnail_time', fallback='300')
    time_str = raw_value.split(';')[0].strip()  # Remove any comment
    return int(time_str)


def get_thumb_filename(video_path: str) -> str:
    # Create a unique ID using a hash of the full file path
    video_hash = hashlib.md5(video_path.encode('utf-8')).hexdigest()
    return f"{video_hash}.jpg"

def get_thumb_path(video_path: str) -> str:
    return os.path.join(THUMB_DIR, get_thumb_filename(video_path))

from utils.metadata import extract_metadata  # Add this import at the top

def generate_thumbnail(video_path: str, force: bool = False) -> str:
    os.makedirs(THUMB_DIR, exist_ok=True)
    thumb_path = get_thumb_path(video_path)

    if not force and os.path.exists(thumb_path):
        return thumb_path  # Already cached

    configured_time = load_thumbnail_time()
    duration = extract_metadata(video_path).get('duration', 0)

    # Use the smaller of configured time or half the duration
    seek_time = min(configured_time, int(duration // 2)) if duration > 0 else configured_time

    try:
        (
            ffmpeg
            .input(video_path, ss=seek_time)
            .filter('scale', 320, -1)  # Resize thumbnail width to 320px, keep aspect
            .output(thumb_path, vframes=1)
            .overwrite_output()
            .run(quiet=True)
        )
        return thumb_path
    except ffmpeg.Error as e:
        print(f"Failed to generate thumbnail for {video_path}: {e}")
        return None
