"""
AuraCineStudio Hybrid Signature Engine
Synthesizes 5 core cinematic post-production pillars into our proprietary signature:
1. In Media Res Hype-Hook: High-retention opening, staccato teaser cuts, and the Dead Stop pre-drop.
2. Kinetic Optical Flow: Directional vector match-cutting and hourglass speed ramping.
3. Diegetic Foley Architecture: Immersive foley sound design, sub-impacts, and directional whooshes.
4. Rhythmic Staccato Cuts: Rapid micro-cuts on macro details locked to secondary percussive hits.
5. Atmospheric Tonal Suspense: Tonal drone dilation, steep low-pass filtering, and asymmetric J/L-cuts.
"""
from typing import Dict, Any, List
from core.logger import AuraLogger
from core.config import STUDIO_CONFIG

class HybridSignatureEngine:
    def __init__(self, vision_catalog: List[Dict[str, Any]], audio_data: Dict[str, Any], speech_data: Dict[str, Any] = None):
        self.vision = [c for c in vision_catalog if not c.get("is_blurry", False)]
        if not self.vision:
            # Fallback if all flagged blurry
            self.vision = vision_catalog or [{"source_file": "default.mp4", "duration": 4.0}]
            
        self.audio = audio_data or {}
        self.speech = speech_data or {}
        self.fps = self.audio.get("fps", STUDIO_CONFIG.DEFAULT_FPS)

    def generate_timeline(self, target_duration: float = 60.0, mode: str = "highlight") -> Dict[str, Any]:
        """
        Dispatches to either high-retention 60s Reel or multi-chapter Long-Form Master.
        """
        if mode == "full":
            return self._build_longform_master(target_duration)
        return self._build_highlight_60s(target_duration)

    def _build_highlight_60s(self, target_duration: float = 60.0) -> Dict[str, Any]:
        AuraLogger.log("director", f"Orchestrating 60-second high-retention reel with 'Hybrid Kinetic Cinema'...")
        timeline = []
        sfx_events = []

        # 1. Pool Categorization
        spark_clips = [c for c in self.vision if c.get("has_sparks") or c.get("energy_score", 0) > 0.75]
        kinetic_pans = [c for c in self.vision if c.get("dominant_motion") in ["PAN_LEFT", "PAN_RIGHT"]]
        static_details = [c for c in self.vision if c.get("dominant_motion") == "STATIC"]

        curr_t = 0.0

        # ----------------------------------------------------
        # [FASE 1: HOOK HYPER-CUTS] (0.0s -> ~2.8s)
        # 3 micro-cuts (6-8 frames) on maximum action
        # ----------------------------------------------------
        hook_pool = (spark_clips + self.vision)[:3]
        for i, clip in enumerate(hook_pool):
            dur = 0.8
            timeline.append({
                "block": "HYPER_HOOK",
                "start": round(curr_t, 2),
                "end": round(curr_t + dur, 2),
                "duration": dur,
                "source": clip["source_file"],
                "in_point": clip.get("best_action_in", 0.0),
                "speed_multiplier": 1.4,
                "transition_out": "FLASH_WHITE_2_FRAMES" if i == 2 else "HARD_CUT"
            })
            sfx_events.append({"time": round(curr_t, 2), "sfx": "whoosh_snap.wav", "volume": -3.0})
            curr_t += dur

        # ----------------------------------------------------
        # [FASE 2: ATMOSPHERE & TONAL SUSPENSE] (2.8s -> ~10.5s)
        # Pacing dilates, tonal drone, low-pass 300Hz, slow push-in
        # ----------------------------------------------------
        suspense_cues = self.audio.get("suspense_zones", [])
        suspense_target = suspense_cues[0]["resolution_sec"] if suspense_cues else 10.5
        suspense_target = min(suspense_target, 12.0)

        while curr_t < suspense_target and static_details:
            clip = static_details.pop(0)
            dur = min(2.5, suspense_target - curr_t)
            timeline.append({
                "block": "ATMOSPHERE_SUSPENSE",
                "start": round(curr_t, 2),
                "end": round(curr_t + dur, 2),
                "duration": dur,
                "source": clip["source_file"],
                "in_point": 0.5,
                "speed_multiplier": 0.65,  # 60fps cinematic slow-mo
                "vfx": "SLOW_PUSH_IN_104",
                "audio_filter": "LOW_PASS_300HZ"
            })
            curr_t += dur

        # ----------------------------------------------------
        # [FASE 3: KINETIC FLOW & OPTICAL MATCH-CUTS] (~10.5s -> ~48.0s)
        # Directional continuity: PAN_RIGHT -> PAN_RIGHT with hourglass speed curves
        # ----------------------------------------------------
        drop_time = target_duration - 12.0
        last_motion = "PAN_RIGHT"

        while curr_t < (drop_time - 0.5) and kinetic_pans:
            matching = next((c for c in kinetic_pans if c.get("dominant_motion") == last_motion), kinetic_pans.pop(0))
            if matching in kinetic_pans:
                kinetic_pans.remove(matching)

            dur = 1.6
            timeline.append({
                "block": "KINETIC_FLOW",
                "start": round(curr_t, 2),
                "end": round(curr_t + dur, 2),
                "duration": dur,
                "source": matching["source_file"],
                "in_point": 0.3,
                "speed_curve": STUDIO_CONFIG.HOURGLASS_RAMP,
                "transition_out": "SEAMLESS_DIRECTIONAL_WHIP"
            })
            sfx_events.append({"time": round(curr_t + dur - 0.15, 2), "sfx": "whoosh_directional.wav", "volume": -5.0})
            last_motion = matching.get("dominant_motion", "PAN_RIGHT")
            curr_t += dur

        # ----------------------------------------------------
        # [FASE 4: THE DEAD STOP] (48.0s -> 48.5s)
        # Absolute silence / low-pass vacuum 12 frames pre-drop
        # ----------------------------------------------------
        timeline.append({
            "block": "DEAD_STOP_VACUUM",
            "start": round(drop_time - STUDIO_CONFIG.DEAD_STOP_DURATION_SEC, 2),
            "end": round(drop_time, 2),
            "duration": STUDIO_CONFIG.DEAD_STOP_DURATION_SEC,
            "source": spark_clips[0]["source_file"] if spark_clips else self.vision[0]["source_file"],
            "in_point": 0.0,
            "speed_multiplier": 0.3,
            "audio_override": "TOTAL_MUTE"
        })

        # ----------------------------------------------------
        # [FASE 5: CLIMAX DROP & FOLEY IMPACT] (48.5s -> ~56.5s)
        # Kick-snapping, 112% punch-zoom, flash white, sub-impact boom
        # ----------------------------------------------------
        curr_t = drop_time
        sfx_events.append({"time": round(curr_t, 2), "sfx": "sub_boom_impact.wav", "volume": 0.0})

        kicks = [k for k in self.audio.get("timeline_markers", []) if k["time_sec"] >= curr_t and k["time_sec"] <= (target_duration - 3.5)]
        for k in kicks:
            t = k["time_sec"]
            if t - curr_t < 0.5:
                continue
            clip = spark_clips.pop(0) if spark_clips else self.vision[0]
            timeline.append({
                "block": "CLIMAX_DROP",
                "start": round(curr_t, 2),
                "end": round(t, 2),
                "duration": round(t - curr_t, 2),
                "source": clip["source_file"],
                "in_point": 0.5,
                "vfx": "PUNCH_ZOOM_112" if k.get("priority") == "HIGH" else "NONE",
                "transition_in": "FLASH_WHITE_2_FRAMES" if curr_t == drop_time else "HARD_CUT"
            })
            curr_t = t

        # ----------------------------------------------------
        # [FASE 6: OUTRO GLOW & REVERB FADE] (~56.5s -> 60.0s)
        # ----------------------------------------------------
        timeline.append({
            "block": "OUTRO_GLOW",
            "start": round(curr_t, 2),
            "end": round(target_duration, 2),
            "duration": round(target_duration - curr_t, 2),
            "source": self.vision[-1]["source_file"],
            "in_point": 1.0,
            "speed_multiplier": 0.8,
            "vfx": "FADE_TO_BLACK"
        })

        AuraLogger.log("success", f"Blueprint calculated: {len(timeline)} cuts, {len(sfx_events)} sound design cues.")
        return {
            "signature_style": "HYBRID_KINETIC_CINEMA",
            "mode": "highlight",
            "target_duration": target_duration,
            "cuts": timeline,
            "sound_design": sfx_events
        }

    def _build_longform_master(self, target_duration: float) -> Dict[str, Any]:
        AuraLogger.log("director", "Orchestrating multi-chapter Long-Form Master with narrative progression...")
        
        # 1. Cold Open Teaser (20s)
        cold_open = self._build_highlight_60s(target_duration=20.0)["cuts"]

        # 2. Main Narrative Chapters with Speech A-Roll and B-Roll Overlay
        speech_intervals = self.speech.get("speech_segments", [])
        chapters = []
        
        # Assemble sequence covering footage
        curr_t = 20.0
        for i, clip in enumerate(self.vision):
            dur = min(clip.get("duration", 4.0), 6.0)
            has_voice = any(abs(s["start"] - curr_t) < dur for s in speech_intervals)
            chapters.append({
                "block": f"CHAPTER_{(i // 4) + 1}",
                "start": round(curr_t, 2),
                "end": round(curr_t + dur, 2),
                "duration": dur,
                "source": clip["source_file"],
                "in_point": clip.get("best_action_in", 0.0),
                "has_speech_aroll": has_voice,
                "music_ducking_db": STUDIO_CONFIG.DUCKING_DB if has_voice else 0.0,
                "transition_out": "J_CUT_BROLL" if has_voice else "DIRECTIONAL_DISSOLVE"
            })
            curr_t += dur

        return {
            "signature_style": "HYBRID_KINETIC_CINEMA",
            "mode": "full",
            "target_duration": round(curr_t, 2),
            "cold_open_teaser": cold_open,
            "cuts": cold_open + chapters,
            "sound_design": [{"time": 20.0, "sfx": "sub_boom_impact.wav", "volume": 0.0}]
        }
