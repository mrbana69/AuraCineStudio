"""
AuraCineStudio Universal EDL & XML Exporter
Generates standard CMX 3600 EDL and JSON timeline files for DaVinci Resolve, Premiere Pro, and Final Cut Pro.
"""
from pathlib import Path
from typing import Dict, Any

from core.logger import AuraLogger

def export_edl_timeline(blueprint: Dict[str, Any], output_path: str, fps: float = 30.0) -> str:
    """
    Exports CMX 3600 standard Edit Decision List (.edl).
    """
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    cuts = blueprint.get("cuts", [])
    title = blueprint.get("signature_style", "AURACINE_EDIT")
    
    def sec_to_tc(sec: float) -> str:
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        f = int(round((sec - int(sec)) * fps))
        return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"

    lines = [
        f"TITLE: {title}",
        "FCM: NON-DROP FRAME",
        ""
    ]

    for idx, cut in enumerate(cuts, start=1):
        reel = "AX"
        in_pt = cut.get("in_point", 0.0)
        dur = cut.get("duration", 2.0)
        src_in = sec_to_tc(in_pt)
        src_out = sec_to_tc(in_pt + dur)
        rec_in = sec_to_tc(cut.get("start", 0.0))
        rec_out = sec_to_tc(cut.get("end", dur))

        # CMX 3600 line format:
        # 001  AX       V     C        00:00:00:00 00:00:02:00 00:00:00:00 00:00:02:00
        lines.append(f"{idx:03d}  {reel:<8} V     C        {src_in} {src_out} {rec_in} {rec_out}")
        lines.append(f"* FROM CLIP NAME: {cut.get('source', 'unknown.mp4')}")
        lines.append(f"* EFFECT: {cut.get('block', 'CUT')} | SPEED: {cut.get('speed_multiplier', 1.0)}")
        lines.append("")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    AuraLogger.log("success", f"EDL timeline exported: {out_file.name}")
    return str(out_file)
