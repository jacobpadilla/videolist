import subprocess
import json
import os

def extract_metadata(video_path: str) -> dict:
    if not os.path.exists(video_path):
        return {}

    try:
        # Run ffprobe to get video metadata as JSON
        result = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                video_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"ffprobe error: {result.stderr}")
            return {}

        info = json.loads(result.stdout)

        # Extract basic info
        format_info = info.get('format', {})
        streams = info.get('streams', [])

        video_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})

        return {
            'duration': float(format_info.get('duration', 0)),
            'codec': video_stream.get('codec_name', 'unknown'),
            'width': video_stream.get('width'),
            'height': video_stream.get('height'),
        }

    except Exception as e:
        print(f"Metadata extraction failed for {video_path}: {e}")
        return {}
