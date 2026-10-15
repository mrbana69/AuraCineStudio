"""
AuraCineStudio Optical Flow Motion Detector
Calculates camera trajectory vectors (PAN_LEFT, PAN_RIGHT, TILT_UP, TILT_DOWN, STATIC)
using Farneback Dense Optical Flow to enable directional match-cuts (Sam Kolder style).
"""
import sys
import json
from pathlib import Path
from typing import Dict, Any

from core.logger import AuraLogger
from core.config import STUDIO_CONFIG

def detect_camera_motion(video_path: str, max_duration_sec: float = 4.0) -> Dict[str, Any]:
    """
    Computes dense optical flow across the first few seconds of a video clip.
    Returns dominant motion vector, velocity, and intensity.
    """
    v_path = Path(video_path)
    if not v_path.exists():
        return {"dominant_motion": "STATIC", "intensity": 0.0, "file": v_path.name}

    try:
        import cv2
        import numpy as np

        cap = cv2.VideoCapture(str(v_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or STUDIO_CONFIG.DEFAULT_FPS
        max_frames = int(fps * max_duration_sec)

        ret, prev_frame = cap.read()
        if not ret or prev_frame is None:
            cap.release()
            return {"dominant_motion": "STATIC", "intensity": 0.0, "file": v_path.name}

        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        flow_x, flow_y = [], []
        frame_idx = 0

        while cap.isOpened() and frame_idx < max_frames:
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            if frame_idx % STUDIO_CONFIG.MOTION_SAMPLE_INTERVAL_FRAMES == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Compute Farneback Optical Flow
                flow = cv2.calcOpticalFlowFarneback(
                    prev_gray, gray, None,
                    pyr_scale=0.5, levels=3, winsize=15,
                    iterations=3, poly_n=5, poly_sigma=1.2, flags=0
                )
                flow_x.append(float(np.mean(flow[..., 0])))
                flow_y.append(float(np.mean(flow[..., 1])))
                prev_gray = gray

            frame_idx += 1
        cap.release()

        mean_x = float(np.mean(flow_x)) if flow_x else 0.0
        mean_y = float(np.mean(flow_y)) if flow_y else 0.0
        intensity = float(np.sqrt(mean_x**2 + mean_y**2))

        # Classification threshold
        motion_thresh = 0.4
        if abs(mean_x) > abs(mean_y):
            if mean_x < -motion_thresh:
                motion = "PAN_LEFT"
            elif mean_x > motion_thresh:
                motion = "PAN_RIGHT"
            else:
                motion = "STATIC"
        else:
            if mean_y < -motion_thresh:
                motion = "TILT_UP"
            elif mean_y > motion_thresh:
                motion = "TILT_DOWN"
            else:
                motion = "STATIC"

        return {
            "file": v_path.name,
            "dominant_motion": motion,
            "intensity_x": round(mean_x, 2),
            "intensity_y": round(mean_y, 2),
            "motion_energy": round(min(intensity / 3.0, 1.0), 2)
        }

    except ImportError:
        return {"dominant_motion": "STATIC", "intensity": 0.0, "file": v_path.name}
    except Exception as e:
        AuraLogger.log("warn", f"Optical flow calculation error on {v_path.name}: {e}")
        return {"dominant_motion": "STATIC", "intensity": 0.0, "file": v_path.name}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        res = detect_camera_motion(sys.argv[1])
        print(json.dumps(res, indent=2))
