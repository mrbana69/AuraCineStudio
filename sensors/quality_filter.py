"""
AuraCineStudio Visual Quality & Frame Culling Inspector
Performs AI culling: filters blurry/shaky footage using Laplacian variance,
detects luminance spikes (sparklers, cake candles, flash lights), and flags low-contrast veiling haze.
"""
import sys
import json
from pathlib import Path
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.logger import AuraLogger
from core.config import STUDIO_CONFIG
from sensors.motion_detector import detect_camera_motion

def inspect_clip_quality(proxy_clip_path: str) -> Dict[str, Any]:
    """
    Inspects sharpness, luminance variance, sparks/candles, and motion direction.
    """
    p_path = Path(proxy_clip_path)
    base_result = {
        "proxy_file": str(p_path),
        "source_file": p_path.name.replace("_proxy360p", ""),
        "blur_score": 120.0,
        "is_blurry": False,
        "has_sparks": False,
        "has_veiling_haze": False,
        "dominant_motion": "STATIC",
        "energy_score": 0.5,
        "best_action_in": 0.5,
        "duration": 4.0
    }

    if not p_path.exists():
        return base_result

    try:
        import cv2
        import numpy as np

        cap = cv2.VideoCapture(str(p_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or STUDIO_CONFIG.DEFAULT_FPS
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = float(total_frames / fps) if total_frames > 0 else 4.0

        blur_scores = []
        luminance_vals = []
        max_lum_jump = 0.0
        prev_lum = None
        frame_idx = 0

        # Sample every 5th frame for high performance
        while cap.isOpened() and frame_idx < fps * 15:
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            if frame_idx % 5 == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # 1. Laplacian Sharpness Variance
                laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
                blur_scores.append(laplacian_var)

                # 2. Mean Luminance & Flash/Spark Detection
                mean_lum = float(np.mean(gray))
                luminance_vals.append(mean_lum)
                if prev_lum is not None:
                    jump = abs(mean_lum - prev_lum)
                    if jump > max_lum_jump:
                        max_lum_jump = jump
                prev_lum = mean_lum

            frame_idx += 1
        cap.release()

        avg_blur = float(np.mean(blur_scores)) if blur_scores else 120.0
        avg_lum = float(np.mean(luminance_vals)) if luminance_vals else 100.0
        
        # Motion detection
        motion_meta = detect_camera_motion(str(p_path))
        
        # Veiling haze: low dark channel contrast (black level too bright)
        has_haze = avg_lum > 140.0 and avg_blur < 90.0
        has_sparks = max_lum_jump > STUDIO_CONFIG.LUMINANCE_FLASH_DELTA

        is_blurry = avg_blur < STUDIO_CONFIG.BLUR_LAPLACIAN_THRESHOLD

        return {
            "proxy_file": str(p_path),
            "source_file": p_path.name.replace("_proxy360p", ""),
            "blur_score": round(avg_blur, 1),
            "is_blurry": is_blurry,
            "has_sparks": has_sparks,
            "has_veiling_haze": has_haze,
            "dominant_motion": motion_meta.get("dominant_motion", "STATIC"),
            "energy_score": motion_meta.get("motion_energy", 0.5),
            "best_action_in": 0.5 if not has_sparks else 1.0,
            "duration": round(duration, 2)
        }

    except ImportError:
        return base_result
    except Exception as e:
        AuraLogger.log("warn", f"Quality check error on {p_path.name}: {e}")
        return base_result

def inspect_footage_parallel(proxy_clips: List[str], cache_dir: str, max_workers: int = 4) -> List[Dict[str, Any]]:
    """
    Runs multi-threaded quality and optical flow sensing across all proxy clips.
    """
    AuraLogger.log("vision", f"Scouting {len(proxy_clips)} footage clips in parallel (Sharpness, Motion, Sparks)...")
    
    catalog = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(inspect_clip_quality, p): p for p in proxy_clips}
        for future in as_completed(futures):
            res = future.result()
            catalog.append(res)
            status = "BLURRY/DISCARD" if res["is_blurry"] else f"{res['dominant_motion']} (Score: {res['blur_score']})"
            if res.get("has_sparks"):
                status += " [💥 SPARKS/CLIMAX DETECTED]"
            AuraLogger.log("vision", f"Clip evaluated: {Path(res['source_file']).name} -> {status}")

    valid_clips = [c for c in catalog if not c["is_blurry"]]
    AuraLogger.log("success", f"Visual scouting complete: {len(valid_clips)}/{len(catalog)} clips cleared for final cut.")
    return catalog

if __name__ == "__main__":
    if len(sys.argv) > 1:
        res = inspect_clip_quality(sys.argv[1])
        print(json.dumps(res, indent=2))
