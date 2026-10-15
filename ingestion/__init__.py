"""
AuraCineStudio Ingestion Module
Handles heavy footage ingestion, fast proxy generation, and audio stream extraction.
"""
from ingestion.proxy_generator import generate_work_proxies, ingest_single_clip

__all__ = ["generate_work_proxies", "ingest_single_clip"]
