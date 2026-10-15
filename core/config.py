"""
AuraCineStudio Global Configuration
Defines default processing parameters, thresholds, and role specifications.
"""
from pathlib import Path

class StudioConfig:
    # Processing Defaults
    DEFAULT_FPS: float = 30.0
    HIGH_FPS_TARGET: float = 60.0
    AUDIO_SAMPLE_RATE: int = 44100
    AUDIO_MONO_SPEECH_SR: int = 16000
    PROXY_HEIGHT: int = 360
    PROXY_FPS: int = 24
    
    # Sound Design Defaults
    DUCKING_DB: float = -18.0
    MIN_SILENCE_SEC: float = 0.4
    DEAD_STOP_FRAMES: int = 12
    DEAD_STOP_DURATION_SEC: float = 0.45
    LOW_PASS_CUTOFF_HZ: int = 300
    
    # Visual Quality Thresholds
    BLUR_LAPLACIAN_THRESHOLD: float = 100.0
    MOTION_SAMPLE_INTERVAL_FRAMES: int = 4
    LUMINANCE_FLASH_DELTA: float = 40.0
    
    # Speed Ramping Presets (Percentages: In / Mid / Out)
    HOURGLASS_RAMP: str = "180_100_220"
    FAST_SNAP_RAMP: str = "200_100_200"
    
    # Default Paths
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent
    CACHE_DIR: Path = ROOT_DIR / "cache"
    OUTPUT_DIR: Path = ROOT_DIR / "output"
    ASSETS_DIR: Path = ROOT_DIR / "assets"
    SFX_DIR: Path = ASSETS_DIR / "sfx"
    LUTS_DIR: Path = ASSETS_DIR / "luts"
    TEMPLATE_WFP: Path = ASSETS_DIR / "template.wfp"

STUDIO_CONFIG = StudioConfig()
