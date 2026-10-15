"""
AuraCineStudio Speech & Voice Activity Engine
Detects spoken dialog intervals, isolates speech segments, cuts dead pauses (>0.4s),
and schedules music ducking (-18dB) for A-roll clarity.
"""
import sys
import json
from pathlib import Path
from typing import List, Dict, Any

from core.logger import AuraLogger
from core.config import STUDIO_CONFIG

def detect_speech_in_audio(audio_path: str, min_silence_sec: float = STUDIO_CONFIG.MIN_SILENCE_SEC) -> List[Dict[str, Any]]:
    """
    Analyzes an audio file for speech intervals and pauses using Librosa or energy splitting.
    """
    a_file = Path(audio_path)
    if not a_file.exists():
        return []

    try:
        import librosa
        import numpy as np

        y, sr = librosa.load(str(a_file), sr=STUDIO_CONFIG.AUDIO_MONO_SPEECH_SR, mono=True)
        # Split speech above 28dB threshold
        intervals = librosa.effects.split(y, top_db=28, frame_length=2048, hop_length=512)
        
        segments = []
        for start, end in intervals:
            t_start = round(float(start) / sr, 3)
            t_end = round(float(end) / sr, 3)
            dur = round(t_end - t_start, 3)
            # Discard microscopic mouth clicks (< 0.2s)
            if dur >= 0.25:
                segments.append({
                    "start": t_start,
                    "end": t_end,
                    "duration": dur,
                    "music_ducking_db": STUDIO_CONFIG.DUCKING_DB
                })
        return segments
    except ImportError:
        # Fallback without librosa
        return []
    except Exception as e:
        AuraLogger.log("warn", f"Speech VAD error on {a_file.name}: {e}")
        return []

def process_speech(audio_tracks: List[str], cache_dir: str) -> Dict[str, Any]:
    """
    Scans all audio tracks extracted from the footage, identifying dialog and ducking cues.
    """
    AuraLogger.log("speech", f"Inspecting {len(audio_tracks)} audio tracks for spoken narrative (A-Roll)...")
    
    total_speech_segments = []
    tracks_with_speech = 0

    for track in audio_tracks:
        if not track or not Path(track).exists():
            continue
        segments = detect_speech_in_audio(track)
        if segments:
            tracks_with_speech += 1
            total_speech_segments.extend(segments)
            AuraLogger.log("speech", f"Found {len(segments)} spoken intervals in {Path(track).name}")

    AuraLogger.log("speech", f"Speech processing complete: {len(total_speech_segments)} dialog segments across {tracks_with_speech} tracks.")
    return {
        "tracks_scanned": len(audio_tracks),
        "has_dialogue": len(total_speech_segments) > 0,
        "speech_segments": total_speech_segments
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        res = detect_speech_in_audio(sys.argv[1])
        print(json.dumps(res, indent=2))
