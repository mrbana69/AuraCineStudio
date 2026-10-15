"""
AuraCineStudio Proxy Generator
Generates lightweight 360p video proxies and 16kHz mono audio streams using FFmpeg.
Prevents memory crashes on high-res 4K/ProRes/HEVC footage during agent sensing.
"""
import os
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.logger import AuraLogger
from core.config import STUDIO_CONFIG

VALID_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi", ".mkv"}

def ingest_single_clip(video_path: Path, output_dir: Path) -> Dict[str, Any]:
    """
    Extracts 16kHz mono wav and 360p ultrafast proxy for a single clip.
    """
    stem = video_path.stem
    proxy_video = output_dir / f"{stem}_proxy360p.mp4"
    audio_wav = output_dir / f"{stem}_audio16k.wav"

    # 1. Extract 16kHz mono WAV (only ~1MB/min, ultra-light for speech/audio engines)
    if not audio_wav.exists():
        cmd_audio = [
            "ffmpeg", "-y", "-i", str(video_path),
            "-vn", "-ac", "1", "-ar", str(STUDIO_CONFIG.AUDIO_MONO_SPEECH_SR),
            str(audio_wav)
        ]
        try:
            subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        except Exception as e:
            AuraLogger.log("warn", f"Could not extract audio for {video_path.name}: {e}")

    # 2. Generate 360p 24fps ultrafast proxy for computer vision & optical flow
    if not proxy_video.exists():
        cmd_proxy = [
            "ffmpeg", "-y", "-i", str(video_path),
            "-vf", f"scale=-2:{STUDIO_CONFIG.PROXY_HEIGHT}",
            "-r", str(STUDIO_CONFIG.PROXY_FPS),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30",
            "-an",
            str(proxy_video)
        ]
        try:
            subprocess.run(cmd_proxy, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        except Exception as e:
            AuraLogger.log("warn", f"Could not generate proxy for {video_path.name}: {e}")

    return {
        "original_file": str(video_path),
        "proxy_file": str(proxy_video) if proxy_video.exists() else str(video_path),
        "audio_file": str(audio_wav) if audio_wav.exists() else None
    }

def generate_work_proxies(footage_dir: str, cache_dir: str, max_workers: int = 4) -> Tuple[List[str], List[str], List[Dict[str, Any]]]:
    """
    Discovers all videos in footage_dir and runs proxy generation in parallel.
    Returns: (list_of_proxies, list_of_audios, clip_mappings)
    """
    footage_path = Path(footage_dir)
    cache_path = Path(cache_dir) / "proxies"
    cache_path.mkdir(parents=True, exist_ok=True)

    if not footage_path.exists():
        AuraLogger.log("error", f"Footage directory not found: {footage_dir}")
        return [], [], []

    video_files = [p for p in footage_path.rglob("*") if p.is_file() and p.suffix.lower() in VALID_EXTENSIONS]
    if not video_files:
        AuraLogger.log("warn", f"No video files found in {footage_dir}")
        return [], [], []

    AuraLogger.log("ingest", f"Discovered {len(video_files)} video assets. Dispatching parallel proxy pipeline...")

    mappings = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(ingest_single_clip, vf, cache_path): vf for vf in video_files}
        for future in as_completed(futures):
            res = future.result()
            mappings.append(res)
            AuraLogger.log("ingest", f"Ingested & proxied: {Path(res['original_file']).name}")

    proxies = [m["proxy_file"] for m in mappings if m.get("proxy_file")]
    audios = [m["audio_file"] for m in mappings if m.get("audio_file")]

    AuraLogger.log("success", f"Ingestion complete: {len(proxies)} proxies, {len(audios)} audio streams ready.")
    return proxies, audios, mappings
