"""
AuraCineStudio VFX & Colorist Module
Applies speed ramping curve definitions, defogging / contrast recovery instructions,
and LUT color transforms (Apple Log / Flat -> Rec.709).
"""
import subprocess
from pathlib import Path
from typing import Dict, Any, List

from core.logger import AuraLogger
from core.config import STUDIO_CONFIG

def apply_visual_polish(blueprint: Dict[str, Any], luts_dir: Path) -> Dict[str, Any]:
    """
    Attaches VFX keyframes (speed ramping, punch zooms, de-haze, LUT references)
    to each timeline slot for the NLE/WFP compiler.
    """
    AuraLogger.log("vfx", "Compiling visual polish (Speed ramping, punch zooms, LUT color transforms)...")
    
    cuts = blueprint.get("cuts", [])
    lut_file = luts_dir / "AppleLog_to_Rec709.cube"
    has_lut = lut_file.exists()

    for cut in cuts:
        block = cut.get("block", "")

        # 1. Punch Zoom VFX
        if cut.get("vfx") == "PUNCH_ZOOM_112":
            cut["scale_keyframes"] = [
                {"frame": 0, "scale": 112.0},
                {"frame": 6, "scale": 100.0, "easing": "ease_out_cubic"}
            ]

        # 2. Slow Push-In VFX
        elif cut.get("vfx") == "SLOW_PUSH_IN_104":
            cut["scale_keyframes"] = [
                {"frame": 0, "scale": 100.0},
                {"frame": int(cut["duration"] * 30), "scale": 104.0, "easing": "linear"}
            ]

        # 3. Speed Ramping Curve Translation
        curve = cut.get("speed_curve")
        if curve == "180_100_220":
            cut["speed_ramping_envelope"] = [
                {"point": 0.0, "speed": 1.8},
                {"point": 0.45, "speed": 1.0},
                {"point": 0.85, "speed": 2.2}
            ]

        # 4. Color Grading LUT
        if has_lut:
            cut["color_profile"] = {
                "lut_path": str(lut_file),
                "contrast": 1.08,
                "saturation": 1.05
            }

    AuraLogger.log("success", f"Visual polish applied across {len(cuts)} timeline cuts.")
    return blueprint

def defog_clip_ffmpeg(input_clip: str, output_clip: str):
    """
    Command line helper to remove veiling glare/fog from venue lights using FFmpeg curves.
    """
    vf_filter = (
        "curves=all='0/0 0.18/0.08 0.5/0.46 0.85/0.88 1/0.95',"
        "eq=contrast=1.18:brightness=-0.03:saturation=1.12:gamma=0.92,"
        "unsharp=lx=5:ly=5:la=0.6"
    )
    cmd = [
        "ffmpeg", "-y", "-i", input_clip,
        "-vf", vf_filter,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "copy",
        output_clip
    ]
    subprocess.run(cmd, check=True)
