"""
AuraCineStudio Wondershare Filmora (.wfp) Builder
Compiles the polished multi-track decision timeline into a native Filmora project package (.wfp).
Handles ZIP unpacking/repacking, asset path resolution, and track injection.
"""
import os
import json
import zipfile
import shutil
from pathlib import Path
from typing import Dict, Any, List

from core.logger import AuraLogger
from core.config import STUDIO_CONFIG

def build_wfp_project(blueprint: Dict[str, Any], template_wfp: str, output_wfp: str, media_folder: str) -> str:
    """
    Constructs a valid .wfp project file linking original high-resolution footage.
    """
    AuraLogger.log("conform", f"Compiling timeline into Filmora .wfp master: {Path(output_wfp).name}...")
    
    out_file = Path(output_wfp)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = STUDIO_CONFIG.CACHE_DIR / "wfp_compile_tmp"

    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)

    template_path = Path(template_wfp)
    cuts = blueprint.get("cuts", [])
    sfx_events = blueprint.get("sound_design_polished", {}).get("sfx_events", [])

    # Case A: Template .wfp exists
    if template_path.exists() and zipfile.is_zipfile(template_path):
        AuraLogger.log("conform", f"Unpacking base template: {template_path.name}")
        with zipfile.ZipFile(template_path, "r") as z_in:
            z_in.extractall(temp_dir)

        # Locate timeline JSON inside extracted archive
        timeline_json = next(temp_dir.rglob("*timeline*.json"), None) or next(temp_dir.rglob("*.json"), None)
        if timeline_json and timeline_json.exists():
            with open(timeline_json, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception:
                    data = {}

            # Inject our signature sequence metadata
            data["signature_hybrid_meta"] = {
                "style": blueprint.get("signature_style", "HYBRID_KINETIC_CINEMA"),
                "total_cuts": len(cuts),
                "target_duration": blueprint.get("target_duration", 60.0),
                "cuts": cuts
            }

            with open(timeline_json, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    # Case B: Synthesize clean Filmora WFP structure from scratch
    else:
        AuraLogger.log("conform", "No external template provided. Synthesizing native WFP directory structure...")
        (temp_dir / "WSVEFolder").mkdir(parents=True, exist_ok=True)
        (temp_dir / "ProjectFolder" / "Medias").mkdir(parents=True, exist_ok=True)
        (temp_dir / "Timeline").mkdir(parents=True, exist_ok=True)
        (temp_dir / "Effects").mkdir(parents=True, exist_ok=True)

        project_info = {
            "version": "13.0.0",
            "canvas": {
                "width": 1080 if blueprint.get("mode") == "highlight" else 1920,
                "height": 1920 if blueprint.get("mode") == "highlight" else 1080,
                "aspect_ratio": "9:16" if blueprint.get("mode") == "highlight" else "16:9",
                "fps": 30.0
            },
            "created_by": "AuraCineStudio"
        }
        with open(temp_dir / "WSVEFolder" / "project_info.json", "w", encoding="utf-8") as f:
            json.dump(project_info, f, indent=2)

        # Medias manifest
        media_path = Path(media_folder).resolve()
        medias_info = {
            "media_root": str(media_path),
            "total_assets": len(cuts),
            "media_list": [
                {
                    "id": f"media_{i}",
                    "path": str((media_path / c["source"]).resolve()) if not Path(c["source"]).is_absolute() else c["source"],
                    "in_point": c.get("in_point", 0.0),
                    "duration": c.get("duration", 2.0)
                }
                for i, c in enumerate(cuts)
            ]
        }
        with open(temp_dir / "ProjectFolder" / "Medias" / "medias_info.json", "w", encoding="utf-8") as f:
            json.dump(medias_info, f, indent=2)

        # Timeline track sequence
        timeline_data = {
            "sequence_name": blueprint.get("signature_style", "HYBRID_KINETIC_CINEMA"),
            "target_duration": blueprint.get("target_duration", 60.0),
            "tracks": {
                "video_track_1": cuts,
                "audio_sfx_track": sfx_events
            }
        }
        with open(temp_dir / "Timeline" / "timeline.json", "w", encoding="utf-8") as f:
            json.dump(timeline_data, f, indent=2)

    # Re-pack as valid zip .wfp container
    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as z_out:
        for file in temp_dir.rglob("*"):
            if file.is_file():
                z_out.write(file, arcname=file.relative_to(temp_dir))

    # Clean up temp
    shutil.rmtree(temp_dir, ignore_errors=True)
    AuraLogger.log("success", f"Master .wfp ready for Filmora: {out_file.resolve()}")
    return str(out_file)
