---
name: aura-cine-studio
description: >-
  Elite multi-agent virtual post-production crew (AuraCineStudio) that edits cinematic videos and 60-second high-retention reels.
  Fuses 5 core cinematic disciplines: In media res hype-hooks, kinetic optical flow, diegetic foley sound design, rhythmic staccato hyper-cuts, and atmospheric tonal suspense.
  Use when the user asks to edit videos, create reels/shorts, compile a Wondershare Filmora (.wfp) project, analyze audio/music beats, detect camera motion, or orchestrate video production.
---

# AuraCineStudio (Virtual Post-Production Crew)

AuraCineStudio è un collettivo di post-produzione cinematografica multi-agente per Antigravity.
Il sistema applica la firma proprietaria **"Hybrid Kinetic Cinema"**, fondendo la cinetica di movimento, la suspense narrativa e l'impatto ritmico percussivo in un unico motore coerente.

---

## 1. Gerarchia dei Ruoli (Troupe Virtuale)

* **Field Shooter / DoP (User)**: Registra il girato grezzo a 1080p/4K 60fps seguendo il [Shooter Protocol](./references/shooter_guidelines.md) (buffer di 2s, blocco AE/AF, regola dell'80/20, pulizia della lente).
* **Ingestion Engineer**: Genera proxy leggeri a 360p e stream audio mono 16kHz per evitare sovraccarichi di memoria RAM su girati da 6GB+.
* **Reparti di Sensing (Paralleli)**:
  - `Music Supervisor`: Spettrometria dinamica, transitori primari (KICK) e secondari (SNARE), finestre di tonal suspense.
  - `Speech Cutter / VAD`: Traccia il parlato A-roll ed elimina le pause morte (>0.4s).
  - `Visual Scout`: Analizza i vettori di movimento (Optical Flow Farneback), elimina fotogrammi sfocati (Laplaciano) e rileva fontane pirotecniche/candele.
* **Showrunner Director**: Mappa la timeline master secondo la formula "Hybrid Kinetic Cinema".
* **Sound Designer & VFX Colorist**: Inietta foley sincronizzato, ducking della musica a -18dB sul parlato, curve di velocità a clessidra e profili LUT Rec.709.
* **Master Conformer**: Compila il file `.wfp` per Wondershare Filmora (e CMX 3600 EDL) collegando i media originali ad alta risoluzione.

---

## 2. Comandi Operativi CLI

### A. Reel / Highlight da 60 Secondi (High Retention)
Esegue la formula compressa: Hype Teaser (0–2.8s) $\rightarrow$ Tonal Suspense (2.8–10.5s) $\rightarrow$ Kinetic Flow (10.5–48s) $\rightarrow$ The Dead Stop (48–48.5s) $\rightarrow$ Climax Drop (48.5–56.5s) $\rightarrow$ Outro Reverb (56.5–60s).
```bash
py studio.py --footage ./footage/ --music ./audio/soundtrack.mp3 --mode highlight --out reel_master
```

### B. Video Completo Long-Form (Multi-Capitolo)
Struttura il girato a capitoli narrativi, con Cold Open energico da 20s, audio ducking automatico sul parlato A-roll a -18dB e B-roll agganciato su J-cut/L-cut.
```bash
py studio.py --footage ./footage/ --music ./audio/soundtrack.mp3 --mode full --out video_completo_master
```

### C. Download Reference Media (YouTube & Instagram)
Scarica qualsiasi reel o short di tendenza per studiarne la ricetta di montaggio:
```bash
py tools/download_reference.py "https://www.instagram.com/reel/xyz..."
py tools/extract_recipe.py cache/references/xyz.mp4 recipes/xyz_recipe.json
```

---

## 3. Regole di Direzione Inderogabili

1. **Mai processare file video completi >1GB direttamente in RAM**: estrai sempre proxy 360p via `ingestion/proxy_generator.py`.
2. **Concordance of Motion (Optical Flow)**: Non eseguire stacchi tra movimenti di camera opposti (es. `PAN_LEFT` seguito da `PAN_RIGHT`) senza una transizione Whip e un effetto sonoro Whoosh direzionale.
3. **The Dead Stop Mandate**: Prima di ogni climax o drop primario (la torta, il salto, il botto della bottiglia), applica tassativamente il Dead Stop: 12 frame (0.45s) di silenzio totale o filtro passa-basso a 250Hz.
4. **Dialogue Ducking Mandate**: La colonna sonora musicale deve abbassarsi automaticamente a `-18 dB` quando è presente voce attiva nell'A-Roll, risalendo a `0 dB` sulle pause e sui drop.

---

## 4. Riferimenti Dettagliati

* Per le linee guida di ripresa con smartphone o Blackmagic Camera, consulta: [DoP Field Shooter Protocol](./references/shooter_guidelines.md).
* Per le specifiche del bus eventi e schemi JSON: [Architecture & Contracts](./references/architecture.md).
* Per i parametri acustici di foley e tonal beats: [Sound Design Guide](./references/sound_design_guide.md).
