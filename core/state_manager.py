"""
AuraCineStudio Session State Manager
Handles contract storage and interchange between the virtual troupe departments.
"""
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

from core.config import STUDIO_CONFIG

class SessionState:
    def __init__(self, session_id: str, base_cache_dir: Optional[Path] = None):
        self.session_id = session_id
        self.base_dir = (base_cache_dir or STUDIO_CONFIG.CACHE_DIR) / "runs" / session_id
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.audio_map_path = self.base_dir / "audio_map.json"
        self.speech_map_path = self.base_dir / "speech_map.json"
        self.visual_catalog_path = self.base_dir / "visual_catalog.json"
        self.blueprint_path = self.base_dir / "decision_blueprint.json"
        self.polished_plan_path = self.base_dir / "polished_timeline.json"
        self.meta_path = self.base_dir / "session_meta.json"

    @classmethod
    def create_new(cls, project_name: str = "project") -> "SessionState":
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in project_name)
        session_id = f"{safe_name}_{timestamp}"
        session = cls(session_id)
        session._save_meta({"created_at": timestamp, "project_name": project_name})
        return session

    def _save_meta(self, meta: Dict[str, Any]):
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

    def save_json(self, target_path: Path, data: Any):
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_json(self, target_path: Path) -> Optional[Any]:
        if not target_path.exists():
            return None
        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Convenience methods for troupe contracts
    def save_audio_map(self, data: Dict[str, Any]):
        self.save_json(self.audio_map_path, data)

    def load_audio_map(self) -> Optional[Dict[str, Any]]:
        return self.load_json(self.audio_map_path)

    def save_speech_map(self, data: Dict[str, Any]):
        self.save_json(self.speech_map_path, data)

    def load_speech_map(self) -> Optional[Dict[str, Any]]:
        return self.load_json(self.speech_map_path)

    def save_visual_catalog(self, data: Dict[str, Any]):
        self.save_json(self.visual_catalog_path, data)

    def load_visual_catalog(self) -> Optional[Dict[str, Any]]:
        return self.load_json(self.visual_catalog_path)

    def save_blueprint(self, data: Dict[str, Any]):
        self.save_json(self.blueprint_path, data)

    def load_blueprint(self) -> Optional[Dict[str, Any]]:
        return self.load_json(self.blueprint_path)

    def save_polished_plan(self, data: Dict[str, Any]):
        self.save_json(self.polished_plan_path, data)

    def load_polished_plan(self) -> Optional[Dict[str, Any]]:
        return self.load_json(self.polished_plan_path)
