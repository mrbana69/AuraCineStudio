"""
AuraCineStudio - Master CLI Orchestrator
Virtual Post-Production Troupe Controller for Antigravity.
Coordinates Ingestion, Parallel Sensing, Hybrid Signature Decision, Polish, and Master Conform.
"""
import sys
import argparse
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.logger import AuraLogger
from core.config import STUDIO_CONFIG
from core.state_manager import SessionState
from ingestion.proxy_generator import generate_work_proxies
from sensors.music_engine import process_soundtrack
from sensors.speech_vad import process_speech
from sensors.quality_filter import inspect_footage_parallel
from decision.hybrid_signature_engine import HybridSignatureEngine
from polish.sound_designer import apply_audio_enhancements
from polish.vfx_colorist import apply_visual_polish
from conform.wfp_builder import build_wfp_project
from conform.edl_exporter import export_edl_timeline

def run_studio(
    footage_dir: str,
    music_track: str,
    mode: str = "highlight",
    output_name: str = "aura_master_edit",
    template_wfp: str = None,
    export_edl: bool = True
) -> str:
    """
    Executes end-to-end post-production pipeline across the virtual troupe.
    """
    AuraLogger.header("AuraCineStudio - Virtual Post-Production Crew")
    AuraLogger.log("director", f"Session mode: {mode.upper()} | Output target: {output_name}")

    session = SessionState.create_new(output_name)
    AuraLogger.log("director", f"Session initialized: {session.session_id}")

    # 1. INGESTION
    AuraLogger.section("1/5", "Ingestion & Low-Latency Proxy Pipeline")
    proxies, audio_streams, clip_mappings = generate_work_proxies(
        footage_dir=footage_dir,
        cache_dir=str(session.base_dir)
    )
    if not proxies:
        AuraLogger.log("error", f"No valid footage could be processed in {footage_dir}. Halting production.")
        return ""

    # 2. SENSING (PARALLEL DEPARTMENTS)
    AuraLogger.section("2/5", "Parallel Sensing Reparti (Music, Speech VAD, Optical Vision)")
    music_meta = process_soundtrack(music_track, str(session.base_dir))
    speech_meta = process_speech(audio_streams, str(session.base_dir))
    vision_catalog = inspect_footage_parallel(proxies, str(session.base_dir))

    session.save_audio_map(music_meta)
    session.save_speech_map(speech_meta)
    session.save_visual_catalog({"clips": vision_catalog})

    # 3. DECISION ENGINE (SHOWRUNNER)
    AuraLogger.section("3/5", "Showrunner: Orchestrating 'Hybrid Kinetic Cinema' Signature")
    target_duration = 60.0 if mode == "highlight" else sum(c.get("duration", 4.0) for c in vision_catalog)
    engine = HybridSignatureEngine(
        vision_catalog=vision_catalog,
        audio_data=music_meta,
        speech_data=speech_meta
    )
    raw_blueprint = engine.generate_timeline(target_duration=target_duration, mode=mode)
    session.save_blueprint(raw_blueprint)

    # 4. POLISH (SFX & VFX)
    AuraLogger.section("4/5", "Sound Design & Visual Polish (Foley, Ducking, Ramping, LUTs)")
    polished_audio = apply_audio_enhancements(raw_blueprint, STUDIO_CONFIG.SFX_DIR)
    final_blueprint = apply_visual_polish(polished_audio, STUDIO_CONFIG.LUTS_DIR)
    session.save_polished_plan(final_blueprint)

    # 5. CONFORM & MASTER COMPILATION
    AuraLogger.section("5/5", "Master Conformer: Compiling Wondershare Filmora (.wfp) Master")
    out_dir = STUDIO_CONFIG.OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_wfp = str(out_dir / f"{output_name}.wfp")
    
    template_file = template_wfp or str(STUDIO_CONFIG.TEMPLATE_WFP)
    final_wfp_path = build_wfp_project(
        blueprint=final_blueprint,
        template_wfp=template_file,
        output_wfp=out_wfp,
        media_folder=footage_dir
    )

    if export_edl:
        out_edl = str(out_dir / f"{output_name}.edl")
        export_edl_timeline(final_blueprint, out_edl, fps=STUDIO_CONFIG.DEFAULT_FPS)

    AuraLogger.header("Production Completed Successfully")
    AuraLogger.log("conform", f"Filmora Master Ready: {final_wfp_path}")
    return final_wfp_path

def main():
    parser = argparse.ArgumentParser(description="AuraCineStudio - Virtual Post-Production Crew")
    parser.add_argument("--footage", required=True, help="Directory containing raw camera footage")
    parser.add_argument("--music", default="assets/soundtrack.mp3", help="Path to soundtrack audio file")
    parser.add_argument("--mode", default="highlight", choices=["highlight", "full"], help="Edit mode: 60s highlight or full long-form")
    parser.add_argument("--out", default="master_edit", help="Output project name")
    parser.add_argument("--template", default=None, help="Optional existing Filmora .wfp template")
    parser.add_argument("--no-edl", action="store_true", help="Skip secondary EDL export")

    args = parser.parse_args()
    run_studio(
        footage_dir=args.footage,
        music_track=args.music,
        mode=args.mode,
        output_name=args.out,
        template_wfp=args.template,
        export_edl=not args.no_edl
    )

if __name__ == "__main__":
    main()
