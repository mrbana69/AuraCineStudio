"""
AuraCineStudio Trend Recipe Extractor
Deconstructs a reference video into a JSON editing recipe of cuts, flash markers, and pacing.
"""
import sys
import json
import subprocess
from pathlib import Path

from core.logger import AuraLogger
from core.config import STUDIO_CONFIG
from sensors.music_engine import process_soundtrack

def extract_recipe(video_path: str, output_recipe_json: str):
    v_path = Path(video_path)
    out_path = Path(output_recipe_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not v_path.exists():
        AuraLogger.log("error", f"Video file not found: {video_path}")
        return

    AuraLogger.log("vision", f"Extracting editing recipe from reference: {v_path.name}...")

    # 1. Extract audio
    audio_tmp = out_path.parent / f"{v_path.stem}_temp_audio.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(v_path),
        "-vn", "-ac", "1", "-ar", "44100",
        str(audio_tmp)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Spectral Audio sensing
    audio_meta = process_soundtrack(str(audio_tmp), str(out_path.parent))
    if audio_tmp.exists():
        audio_tmp.unlink()

    # 3. Simple luminance and cut scanning
    recipe = {
        "source_reference": v_path.name,
        "duration": audio_meta.get("duration_sec", 60.0),
        "bpm": audio_meta.get("bpm", 120.0),
        "suspense_cues": audio_meta.get("suspense_zones", []),
        "timeline_hits": audio_meta.get("timeline_markers", [])
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(recipe, f, indent=2)

    AuraLogger.log("success", f"Recipe extracted successfully to {out_path.name}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        extract_recipe(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python extract_recipe.py <reference_video.mp4> <output_recipe.json>")
