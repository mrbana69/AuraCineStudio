"""
AuraCineStudio Reference Media Downloader
Downloads reference video trends from YouTube (Shorts & Videos) and Instagram (Reels & Posts)
using yt-dlp to extract editing pacing, rhythm, and sound design recipes.
"""
import sys
import subprocess
from pathlib import Path
from core.logger import AuraLogger
from core.config import STUDIO_CONFIG

def download_reference_media(url: str, output_folder: str = "cache/references") -> Path:
    """
    Downloads reference video using yt-dlp Python API or subprocess CLI.
    """
    out_dir = Path(output_folder)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_template = str(out_dir / "%(id)s.%(ext)s")

    AuraLogger.log("ingest", f"Fetching reference video from URL: {url}...")

    # Method 1: Python module yt_dlp
    try:
        import yt_dlp
        ydl_opts = {
            "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best",
            "outtmpl": out_template,
            "quiet": True,
            "no_warnings": True,
            "merge_output_format": "mp4"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except ImportError:
        # Method 2: Fallback to CLI execution
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--no-playlist",
            "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", out_template,
            url
        ]
        subprocess.run(cmd, check=True)

    # Locate downloaded mp4
    mp4_files = sorted(out_dir.glob("*.mp4"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not mp4_files:
        raise FileNotFoundError(f"Download failed or no mp4 found in {output_folder}")

    target = mp4_files[0]
    AuraLogger.log("success", f"Reference asset downloaded: {target.name}")
    return target

if __name__ == "__main__":
    if len(sys.argv) > 1:
        download_reference_media(sys.argv[1])
    else:
        print("Usage: python download_reference.py <YOUTUBE_OR_INSTAGRAM_URL>")
