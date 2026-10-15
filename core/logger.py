"""
AuraCineStudio Troupe Logger
Provides standardized terminal logging formatted per virtual post-production department.
"""
import sys
from datetime import datetime

class AuraLogger:
    # Role-based colored badges for terminal
    ROLES = {
        "director": ("\033[95m[🎬 SHOWRUNNER]\033[0m", "[SHOWRUNNER]"),
        "music": ("\033[94m[🎵 MUSIC SUPERVISOR]\033[0m", "[MUSIC SUPERVISOR]"),
        "speech": ("\033[96m[✂️ LEAD EDITOR / SPEECH]\033[0m", "[SPEECH CUTTER]"),
        "vision": ("\033[92m[🔍 VISUAL SCOUT]\033[0m", "[VISUAL SCOUT]"),
        "sound": ("\033[93m[🎛️ SOUND DESIGNER]\033[0m", "[SOUND DESIGNER]"),
        "vfx": ("\033[91m[✨ VFX & COLORIST]\033[0m", "[VFX & COLORIST]"),
        "conform": ("\033[97m[🏗️ MASTER CONFORMER]\033[0m", "[MASTER CONFORMER]"),
        "ingest": ("\033[90m[⚡ INGESTION]\033[0m", "[INGESTION]"),
        "success": ("\033[92m[✓ SUCCESS]\033[0m", "[SUCCESS]"),
        "warn": ("\033[93m[⚠ WARNING]\033[0m", "[WARNING]"),
        "error": ("\033[91m[✗ ERROR]\033[0m", "[ERROR]"),
    }

    @classmethod
    def log(cls, role: str, message: str):
        badge_color, badge_plain = cls.ROLES.get(role.lower(), (f"[{role.upper()}]", f"[{role.upper()}]"))
        # Check if terminal supports ANSI
        if sys.stdout.isatty():
            print(f"{badge_color} {message}")
        else:
            print(f"{badge_plain} {message}")

    @classmethod
    def header(cls, title: str):
        border = "=" * 65
        print(f"\n\033[1;97m{border}")
        print(f"  🎬 {title.upper()}")
        print(f"{border}\033[0m\n")

    @classmethod
    def section(cls, step: str, title: str):
        print(f"\n\033[1;36m▶ [{step}] {title}...\033[0m")
