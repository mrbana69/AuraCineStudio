"""
AuraCineStudio WFP Inspector & Reverse Engineering Tool
Inspects and unpacks Wondershare Filmora (.wfp) archives to discover schemas,
internal timeline tracks, and media metadata structures.
"""
import sys
import json
import zipfile
from pathlib import Path
from core.logger import AuraLogger

def inspect_wfp_blueprint(wfp_file: str, output_folder: str = "cache/wfp_inspected") -> Dict:
    out_path = Path(output_folder)
    out_path.mkdir(exist_ok=True, parents=True)
    wfp_path = Path(wfp_file)

    if not wfp_path.exists():
        AuraLogger.log("error", f"WFP file not found: {wfp_file}")
        return {}

    AuraLogger.log("conform", f"Decompressing and reverse-engineering .wfp: {wfp_path.name}...")

    manifest = []
    try:
        with zipfile.ZipFile(wfp_path, "r") as archive:
            archive.extractall(out_path)
            manifest = archive.namelist()
    except zipfile.BadZipFile:
        AuraLogger.log("warn", "File is not a zip container (legacy pure XML project format).")
        with open(wfp_path, "r", encoding="utf-8", errors="ignore") as f:
            (out_path / "legacy_project.xml").write_text(f.read(), encoding="utf-8")
        return {"type": "legacy_xml", "extracted_to": str(out_path)}

    json_structures = {}
    for json_file in out_path.rglob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as jf:
                data = json.load(jf)
                json_structures[json_file.name] = list(data.keys()) if isinstance(data, dict) else f"Array[{len(data)}]"
        except Exception:
            pass

    summary = {
        "source_wfp": wfp_path.name,
        "files_count": len(manifest),
        "manifest": manifest,
        "json_keys_discovered": json_structures
    }

    AuraLogger.log("success", f"WFP structure unpacked to {out_path.resolve()} ({len(manifest)} internal files).")
    return summary

if __name__ == "__main__":
    if len(sys.argv) > 1:
        res = inspect_wfp_blueprint(sys.argv[1])
        print(json.dumps(res, indent=2))
    else:
        print("Usage: python inspect_wfp.py <project.wfp>")
