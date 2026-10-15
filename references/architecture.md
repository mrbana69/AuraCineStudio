# AuraCineStudio - Architecture & Virtual Troupe Specifications

AuraCineStudio operates as an elite virtual post-production studio with strict separation of concerns, asynchronous event/artifact bus, and multi-core parallel sensing.

```mermaid
flowchart TD
    User["🎥 Field Shooter / DoP (User)"] --> Ingest["⚡ Ingestion Engineer\n(360p Proxies + 16kHz Mono Audio)"]
    
    subgraph Sensing ["Parallel Sensing Reparti"]
        Ingest --> Music["🎵 Music Supervisor\n(Spectral Flux, Beat Drops, Suspense Dips)"]
        Ingest --> Speech["✂️ Speech Cutter / VAD\n(Dialogue intervals, Dead Pauses >0.4s)"]
        Ingest --> Vision["🔍 Visual Scout\n(Laplacian Sharpness, Farneback Optical Flow)"]
    end
    
    Music --> Bus[("Artifact Bus\n(audio_map.json / visual_catalog.json)")]
    Speech --> Bus
    Vision --> Bus
    
    Bus --> Showrunner["🎬 Showrunner Director\n(Hybrid Kinetic Cinema Decision Engine)"]
    
    subgraph Polish ["Finishing & Polish"]
        Showrunner --> Sound["🎛️ Sound Designer\n(Ducking -18dB, Whooshes, Sub-Booms)"]
        Showrunner --> VFX["✨ VFX & Colorist\n(Hourglass Ramping, Punch Zoom, LUTs)"]
    end
    
    Sound --> Conform["🏗️ Master Conformer\n(WFP Compiler / EDL Exporter)"]
    VFX --> Conform
    
    Conform --> Master[("🎬 Wondershare Filmora (.wfp)\nLinked to Original 4K/ProRes Media")]
```

---

## The 5 Editing Schools in the Hybrid Signature

1. **Kesia Production**: 
   - Hyper-hook in media res (0.0s – 2.8s)
   - The Dead Stop vacuum (12 frames absolute silence before drop)
   - Climax party energy
2. **Sam Kolder / JR Alli**:
   - Directional optical flow matching (`PAN_RIGHT` $\rightarrow$ `PAN_RIGHT`)
   - Hourglass speed ramping (`180%` $\rightarrow$ `100%` $\rightarrow$ `220%`)
3. **Benn TK / Daniel Schiffer**:
   - Diegetic foley audio reinforcement
   - Directional whooshes on seamless transitions
   - Sub-bass impact booms on drops
4. **Edgar Wright**:
   - Staccato micro-cuts on macro details (6–8 frames)
5. **High-End Wedding Cinema**:
   - Tonal suspense dilation
   - Low-pass filters (<300 Hz)
   - Asymmetric J-cuts and L-cuts on emotional speeches

---

## Artifact Contracts Schema

| File Name | Producer | Consumer | Purpose |
| :--- | :--- | :--- | :--- |
| `audio_map.json` | `Music Supervisor` | `Showrunner` | Transients, BPM, drops, and suspense dips |
| `speech_map.json` | `Speech Cutter` | `Showrunner / Sound` | Dialog intervals, ducking trigger windows |
| `visual_catalog.json` | `Visual Scout` | `Showrunner` | Sharpness scores, motion vectors, spark triggers |
| `decision_blueprint.json` | `Showrunner` | `Sound & VFX Polish` | Timeline slots, source in/out points, speed curves |
| `polished_timeline.json` | `Sound & VFX` | `Master Conformer` | SFX track, ducking schedule, punch zooms |
