"""
AuraCineStudio Sound Designer
Injects foley sound design (whooshes, risers, sub-booms) and generates audio ducking envelopes
to keep music at -18dB during voice passages and full 0dB on climax drops.
"""
from pathlib import Path
from typing import Dict, Any, List

from core.logger import AuraLogger
from core.config import STUDIO_CONFIG

def apply_audio_enhancements(blueprint: Dict[str, Any], sfx_dir: Path) -> Dict[str, Any]:
    """
    Scans the timeline cuts, attaches directional whooshes to transitions,
    and formats the audio track ducking envelope.
    """
    AuraLogger.log("sound", "Generating 3D sound design, foley layers, and ducking envelopes...")
    
    cuts = blueprint.get("cuts", [])
    sfx_cues = list(blueprint.get("sound_design", []))
    ducking_envelope = []

    for cut in cuts:
        # 1. Whoosh injection on transitions
        trans = cut.get("transition_out", "")
        if "WHIP" in trans or "MATCH" in trans:
            whoosh_time = round(cut["end"] - 0.18, 2)
            sfx_cues.append({
                "time": whoosh_time,
                "sfx": "whoosh_directional.wav",
                "volume": -5.0,
                "role": "TRANSITION_WHOOSH"
            })

        # 2. Ducking schedule on dialog A-roll
        if cut.get("has_speech_aroll"):
            ducking_envelope.append({
                "start": cut["start"],
                "end": cut["end"],
                "target_db": STUDIO_CONFIG.DUCKING_DB,
                "fade_frames": 6
            })

    # Sort SFX by timestamp
    sfx_cues.sort(key=lambda x: x["time"])

    blueprint["sound_design_polished"] = {
        "sfx_events": sfx_cues,
        "ducking_envelope": ducking_envelope,
        "total_sfx_count": len(sfx_cues)
    }

    AuraLogger.log("success", f"Sound design polished: {len(sfx_cues)} SFX cues, {len(ducking_envelope)} ducking windows.")
    return blueprint
