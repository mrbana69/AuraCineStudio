# AuraCineStudio - Sound Design & Audio Architecture

Audio is 50% of the visual perception in cinematic filmmaking. In AuraCineStudio, audio is not a passive backing track; it drives the visual edit.

---

## 1. The 4 Phases of Audio Suspense

```
[Ritmo Standard] ──> [1. Il Vuoto / Low-Pass] ──> [2. Il Tonal Drone] ──> [3. Risoluzione / Drop]
   Tagli veloci       Audio di colpo filtrato        Pitch sale (Riser)        Impatto visivo + Audio pieno
   (1-2s a clip)      Micro-silenzio (0.3s)          Nessun taglio (2-4s)      Flash / Glitch / Bass Hit
```

1. **Audio Low-Pass Filter & Micro-Mute**:
   - Right before a suspense moment, high frequencies are cut abruptly with a 24dB/oct low-pass filter below 300 Hz, or audio is muted for 10-15 frames (0.3s - 0.5s) to reset ear attention.
2. **The Tonal Drone / Riser**:
   - A continuous 50-100 Hz drone or pitch-shifted riser builds tension.
   - During this window, visual editing slows down: long steady shots or slow push-in (100% $\rightarrow$ 104% over 3s).
3. **The Dead Stop**:
   - Exactly 12 frames (0.4s) before the drop: total silence.
4. **The Drop / Climax Hit**:
   - Bass punches back at 100% volume with a sub-boom impact, accompanied visually by a 2-frame white flash and punch-zoom (112%).

---

## 2. Audio Ducking Guidelines

* **Voiceover / Spoken Dialog (A-Roll)**: Background music ducks to `-18 dB` with a 6-frame smooth ease curve whenever speech is active.
* **Pause / B-Roll Windows**: Music returns to `0 dB` during pauses greater than `0.6s`.
