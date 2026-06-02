from pathlib import Path
import subprocess

def has_audio(video_path: str) -> bool:
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=index",
        "-of", "csv=p=0",
        str(video_path)
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return bool(result.stdout.strip())
#

def extract_audio_bytes(video_path: str) -> bytes:

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-vn",               # убрать видео
        "-acodec", "pcm_s16le",
        "-ar", "16000",      # стандарт для ASR
        "-ac", "1",          # mono
        "-f", "wav",
        "pipe:1"             # вывод в stdout
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    
    return result.stdout
#

def video_verify(path: str) -> bool:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                path
            ],
            capture_output=True,
            text=True,
            check=True
        )

        return bool(result.stdout.strip())
    #
    except:
        return False
    #
#