"""
AuraCineStudio Core Module
Houses configuration, multi-agent logging, and state management.
"""
from core.config import STUDIO_CONFIG
from core.logger import AuraLogger
from core.state_manager import SessionState

__all__ = ["STUDIO_CONFIG", "AuraLogger", "SessionState"]
