# AuraCineStudio 🎬

> **Elite Virtual Post-Production Crew & "Hybrid Kinetic Cinema" Engine for Antigravity**

AuraCineStudio trasforma Antigravity in una troupe cinematografica autonoma di post-produzione.
Mentre il DoP / Field Shooter (l'utente) si concentra unicamente sulla cattura del girato grezzo sul campo, la troupe virtuale esegue in parallelo ingestion a bassa latenza, sensing audio/visivo, composizione di regia e conforming finale in progetti pronti per **Wondershare Filmora** (`.wfp`) e standard CMX 3600 EDL.

---

## 🌟 La Nostra Firma: "Hybrid Kinetic Cinema"

AuraCineStudio unifica 5 pilastri della grammatica cinematografica e del montaggio moderno in una metodologia integrata:

1. **In Media Res Hype-Hook**: Apertura ad alta ritenzione (0–2.8s) con micro-stacchi sui punti di massima energia, stacco atmosferico e *The Dead Stop* (silenzio d'aria pre-drop).
2. **Kinetic Optical Flow**: Match-cut direzionali su vettori di movimento concordanti (`PAN_RIGHT` $\rightarrow$ `PAN_RIGHT`) e curve di velocità a clessidra (`180%` $\rightarrow$ `100%` $\rightarrow$ `220%`).
3. **Diegetic Foley Architecture**: Sound design tridimensionale iper-realistico, sub-bass impact booms sui beat primari e whoosh direzionali calibrati su ogni transizione.
4. **Rhythmic Staccato Hyper-Cuts**: Micro-sequenze dinamiche da 6–8 frame sincronizzate sugli accenti percussivi secondari (snare/timbal).
5. **Atmospheric Tonal Suspense**: Dilatazione temporale con tonal drones, filtri passa-basso (<300 Hz), slow-motion fluido a 60fps e stacchi continui con J-cut/L-cut asimmetrici.

---

## 🏗️ Architettura del Repository

```plaintext
AuraCineStudio/
├── .gitignore
├── README.md                          # Documentazione e showcase della troupe
├── SKILL.md                          # Direttive operative per Antigravity CLI
├── studio.py                         # Master CLI orchestrator
├── requirements.txt
│
├── core/
│   ├── config.py                     # Costanti, soglie e percorsi globali
│   ├── logger.py                     # Logger multi-agente con badge di reparto
│   └── state_manager.py              # Gestione sessioni e salvataggio JSON intermedi
│
├── ingestion/
│   └── proxy_generator.py            # FFmpeg: audio mono 16kHz + proxy 360p ultra-rapidi
│
├── sensors/
│   ├── music_engine.py               # Spettrometria dinamica, kick/snare, finestre di suspense
│   ├── speech_vad.py                 # Riconoscimento vocale, taglio silenzi e ducking
│   ├── motion_detector.py            # Farneback Optical Flow & vettori di camera
│   └── quality_filter.py             # Laplacian sharpness, blur check, luminance bursts
│
├── decision/
│   └── hybrid_signature_engine.py    # Showrunner: formula ibrida per Reel 60s e Long-Form
│
├── polish/
│   ├── sound_designer.py             # Layering foley, whoosh direzionali e ducking (-18dB)
│   └── vfx_colorist.py               # Curve speed ramp, punch zoom e LUT Rec.709
│
├── conform/
│   ├── wfp_builder.py                # Compilatore archivio Wondershare Filmora (.wfp)
│   └── edl_exporter.py               # Esportatore standard CMX 3600 EDL
│
├── tools/
│   ├── download_reference.py         # Downloader yt-dlp per Reel/Shorts da IG e YouTube
│   ├── inspect_wfp.py                # Reverse-engineering file .wfp
│   └── extract_recipe.py             # Estrattore ricette di montaggio da reference
│
├── references/
│   ├── shooter_guidelines.md         # Protocollo di ripresa DoP (smartphone / Blackmagic)
│   ├── architecture.md               # Specifiche della pipeline e contratti dati
│   └── sound_design_guide.md         # Manuale di sound design e tonal suspense
│
└── assets/
    ├── sfx/                          # whoosh_snap.wav, whoosh_directional.wav, sub_boom_impact.wav
    ├── luts/                         # AppleLog_to_Rec709.cube
    └── template.wfp                  # Template di base Filmora
```

---

## 🚀 Guida Rapida

### 1. Installazione Dipendenze
```bash
pip install -r requirements.txt
```
*(Assicurati che `ffmpeg` sia installato e presente nel PATH di sistema).*

### 2. Esecuzione Highlight da 60 Secondi (Reel / TikTok)
```bash
py studio.py --footage ./footage/ --music ./audio/track.mp3 --mode highlight --out mio_reel
```

### 3. Esecuzione Video Completo Long-Form (Multi-Capitolo)
```bash
py studio.py --footage ./footage/ --music ./audio/track.mp3 --mode full --out video_completo
```

### 4. Studio di Trend (Download & Extraction)
```bash
py tools/download_reference.py "https://www.instagram.com/reel/xyz..."
py tools/extract_recipe.py cache/references/xyz.mp4 recipes/xyz_recipe.json
```

---

## 📜 Licenza
MIT License - Realizzato per produzioni cinematografiche e social ad altissimo impatto.
