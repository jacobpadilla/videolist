import os
import configparser
from typing import List

def load_settings(config_path: str = 'config/settings.ini') -> dict:
    config = configparser.ConfigParser()
    config.read(config_path)

    video_folder = config.get('general', 'video_folder', fallback='.')
    extensions = config.get('general', 'supported_extensions', fallback='.mkv,.mp4,.avi,.mov')
    extension_list = [ext.strip().lower() for ext in extensions.split(',')]

    return {
        'video_folder': os.path.abspath(video_folder),
        'supported_extensions': extension_list,
    }

def scan_video_files(video_folder: str, extensions: List[str]) -> List[str]:
    video_files = []
    for root, dirs, files in os.walk(video_folder):
        for file in files:
            if file.startswith('.'):
                continue  # Skip hidden files
            ext = os.path.splitext(file)[1].lower()
            if ext in extensions:
                full_path = os.path.join(root, file)
                video_files.append(full_path)
    return sorted(video_files)

# Example usage
if __name__ == '__main__':
    settings = load_settings()
    videos = scan_video_files(settings['video_folder'], settings['supported_extensions'])
    for v in videos:
        print(v)
