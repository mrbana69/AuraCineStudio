"""
AuraCineStudio Universal Music & Audio Engine
Performs spectral decomposition, onset detection, transient tracking, and suspense-dip identification.
Agnostic across all genres (urban, techno, cinematic, rock, pop, acoustic).
"""
import sys
import json
from pathlib import Path
from typing import Dict, Any, List

from core.logger import AuraLogger
from core.config import STUDIO_CONFIG

def process_soundtrack(audio_path: str, cache_dir: str, fps: float = STUDIO_CONFIG.DEFAULT_FPS) -> Dict[str, Any]:
    """
    Analyzes soundtrack audio file and outputs comprehensive rhythm and suspense markers.
    """
    a_path = Path(audio_path)
    if not a_path.exists():
        AuraLogger.log("warn", f"Audio file not found: {audio_path}. Creating fallback audio markers.")
        return _fallback_audio_markers(60.0, fps)

    AuraLogger.log("music", f"Analyzing soundtrack dynamics: {a_path.name}...")

    try:
        import librosa
        import numpy as np

        # Load audio in mono
        y, sr = librosa.load(str(a_path), sr=STUDIO_CONFIG.AUDIO_SAMPLE_RATE, mono=True)
        total_duration = float(len(y) / sr)
        hop_length = int(sr / fps)

        # 1. Harmonic / Percussive Separation (HPSS)
        # Separates melodic bed from rhythmic transients without hardcoded frequencies
        y_harmonic, y_percussive = librosa.effects.hpss(y)

        # 2. Universal Onset Envelope
        onset_env = librosa.onset.onset_strength(y=y_percussive, sr=sr, hop_length=hop_length)
        if np.max(onset_env) > 0:
            onset_norm = (onset_env - np.min(onset_env)) / (np.max(onset_env) - np.min(onset_env))
        else:
            onset_norm = onset_env

        # 3. Dynamic Peak Picking (Hierarchical Beats)
        # Primary Peaks (KICK / Major scene cuts): > 80th percentile
        thresh_p = float(np.percentile(onset_norm, 80))
        primary_peaks = librosa.util.peak_pick(
            onset_norm,
            pre_max=3, post_max=3,
            pre_avg=4, post_avg=4,
            delta=thresh_p * 0.35,
            wait=int(fps * 0.25)
        )

        # Secondary Peaks (SNARE / Accent VFX): > 60th percentile
        thresh_s = float(np.percentile(onset_norm, 60))
        secondary_peaks = librosa.util.peak_pick(
            onset_norm,
            pre_max=2, post_max=2,
            pre_avg=3, post_avg=3,
            delta=thresh_s * 0.25,
            wait=int(fps * 0.12)
        )

        # 4. Universal Suspense Windows (Tonal Dips & Drones)
        # Low energy periods (> 0.8s) followed by energetic surge
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        rms_norm = (rms - np.min(rms)) / (np.max(rms) - np.min(rms) + 1e-6)
        low_thresh = float(np.percentile(rms_norm, 25))

        suspense_zones = []
        in_dip = False
        dip_start = 0.0

        for idx, energy in enumerate(rms_norm):
            t = round(idx / fps, 3)
            if energy < low_thresh and not in_dip:
                in_dip = True
                dip_start = t
            elif energy >= low_thresh and in_dip:
                in_dip = False
                dur = round(t - dip_start, 3)
                if dur >= 0.8:
                    suspense_zones.append({
                        "start_sec": dip_start,
                        "resolution_sec": t,
                        "duration_sec": dur,
                        "type": "TONAL_SUSPENSE_HOLD"
                    })

        # 5. Timeline Markers Assembly
        timeline_markers = []
        for p in primary_peaks:
            t = round(float(p) / fps, 3)
            timeline_markers.append({
                "time_sec": t,
                "frame": int(p),
                "strength": round(float(onset_norm[p]), 2),
                "priority": "HIGH",
                "action": "SCENE_CUT"
            })

        for s in secondary_peaks:
            t = round(float(s) / fps, 3)
            if not any(abs(m["time_sec"] - t) < 0.1 for m in timeline_markers):
                timeline_markers.append({
                    "time_sec": t,
                    "frame": int(s),
                    "strength": round(float(onset_norm[s]), 2),
                    "priority": "MEDIUM",
                    "action": "ACCENT_VFX"
                })

        timeline_markers.sort(key=lambda x: x["time_sec"])

        # Compute BPM
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(tempo[0] if isinstance(tempo, np.ndarray) else tempo)

        res = {
            "audio_file": a_path.name,
            "fps": fps,
            "duration_sec": round(total_duration, 2),
            "bpm": round(bpm, 1),
            "suspense_zones": suspense_zones,
            "timeline_markers": timeline_markers
        }
        AuraLogger.log("music", f"BPM: {res['bpm']} | {len(timeline_markers)} rhythmic transients | {len(suspense_zones)} suspense zones identified.")
        return res

    except ImportError:
        AuraLogger.log("warn", "librosa not installed, using fallback algorithmic pacing markers.")
        return _fallback_audio_markers(60.0, fps)
    except Exception as e:
        AuraLogger.log("error", f"Audio analysis error: {e}. Falling back to default markers.")
        return _fallback_audio_markers(60.0, fps)

def _fallback_audio_markers(duration: float, fps: float) -> Dict[str, Any]:
    """Generates standard cinematic rhythmic pacing when raw spectral analysis is unavailable."""
    markers = []
    # Rhythmic cuts every ~1.2 to 2.4 seconds with accents
    t = 0.0
    while t < duration:
        t += 1.4
        markers.append({
            "time_sec": round(t, 2),
            "frame": int(t * fps),
            "strength": 0.85,
            "priority": "HIGH",
            "action": "SCENE_CUT"
        })
    return {
        "audio_file": "fallback",
        "fps": fps,
        "duration_sec": duration,
        "bpm": 120.0,
        "suspense_zones": [{"start_sec": 3.0, "resolution_sec": 9.5, "duration_sec": 6.5, "type": "TONAL_SUSPENSE_HOLD"}],
        "timeline_markers": markers
    }

if __name__ == "__main__":
    if len(sys.argv) > 2:
        out = process_soundtrack(sys.argv[1], sys.argv[2])
        print(json.dumps(out, indent=2))
