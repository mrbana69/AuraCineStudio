"""
AuraCineStudio Polish Module
Sound design layering, music ducking, VFX curves, and color grading.
"""
from polish.sound_designer import apply_audio_enhancements
from polish.vfx_colorist import apply_visual_polish

__all__ = ["apply_audio_enhancements", "apply_visual_polish"]
