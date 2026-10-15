"""
AuraCineStudio Sensors Module
Parallel sensing engines: Music/Audio, Speech VAD, Optical Motion, and Quality Analysis.
"""
from sensors.music_engine import process_soundtrack
from sensors.speech_vad import process_speech
from sensors.motion_detector import detect_camera_motion
from sensors.quality_filter import inspect_footage_parallel, inspect_clip_quality

__all__ = [
    "process_soundtrack",
    "process_speech",
    "detect_camera_motion",
    "inspect_footage_parallel",
    "inspect_clip_quality"
]
