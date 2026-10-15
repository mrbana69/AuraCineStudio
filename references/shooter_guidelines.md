# AuraCineStudio - DoP Field Shooter Protocol

> **"Garbage In, Garbage Out"**: La troupe di post-produzione è efficace quanto la qualità del girato grezzo che riceve.
> Questo protocollo garantisce che ogni inquadratura alimenti direttamente gli algoritmi di Optical Flow, Speed Ramping, Audio Slicing e LUT Color Grading della troupe.

---

## 1. I 4 Comandamenti Tecnici sul Campo

### A. Risoluzione & Framerate (Fisso a 60 FPS)
* **Standard Raccomandato**: `1080p @ 60 FPS` (oppure `4K @ 60 FPS`).
* **Perché**: I 60 frame al secondo permettono alla troupe VFX di applicare uno slow-motion fluido al 50% (24/30 FPS) e curve di speed ramping senza scatti o artefatti di interpolazione.
* **Per risparmiare spazio**: Se lo spazio è limitato, usa `1080p @ 60 FPS` in H.265 (HEVC). Sui social il 4K viene ricompresso a 1080p dai server.

### B. Blocco Messa a Fuoco ed Esposizione (AE/AF Lock)
* **Errore Comune**: Lasciare autofocus ed esposizione automatica attivi mentre ci si muove nel locale. L'obiettivo "pompa" avanti e indietro e la luminosità sfarfalla.
* **Soluzione**: Prima di iniziare il movimento, tocca sul soggetto/punto luminoso chiave e tieni premuto per attivare il **blocco AE/AF**.
* **Sottoesposizione manuale**: Nei locali con luci forti, abbassa l'esposizione di `-0.7` o `-1.0 EV`. I neri tornano profondi e i faretti non bruciano in macchie bianche.

### C. Pulizia Fisica della Lente (Anti-Nebbia)
* **La Causa #1 dell'alone lattiginoso**: Il grasso delle dita sulla lente agisce come un prisma diffusore nei locali bui con faretti diretti.
* **Soluzione**: Pulisci sempre la lente con un panno in microfibra o cotone con un movimento circolare prima di ogni sessione.

### D. La Regola dell'80/20 sugli Obiettivi
* **80% del Girato su 1x (e 2x/3x)**: È il sensore principale con la massima luminosità, tenuta agli alti ISO al buio e prospettiva naturale sui volti.
* **20% su 0.5x (Ultra-Wide)**: **Mai** usarlo come lente di default o per primi piani (deforma i volti e genera rumore a grana grossa). Usalo solo per inquadrature dal basso in mezzo alla folla che salta, sopra la torta o per transizioni whip a corto raggio.

---

## 2. Tecniche di Ripresa per il Montaggio Intelligente

### La Regola dei "3 Secondi di Coda" (Handle Buffers)
* Premi REC $\rightarrow$ resta immobile per 2 secondi $\rightarrow$ esegui il movimento fluido (pan, camminata o rotazione) $\rightarrow$ resta immobile per 2 secondi $\rightarrow$ premi STOP.
* **Perché**: La troupe usa i primi e gli ultimi fotogrammi per calcolare le code di dissolvenza, gli optical match-cut e le accelerazioni dello speed ramping.

### Movimenti Direzionali Concordi (Match-Cut)
* Se fai movimenti di camera su più clip, mantieni la stessa direzione (es. tutti `PAN_RIGHT` da sinistra a destra, oppure movimenti a spinta in avanti `Push-In`).
* Il modulo `motion_detector.py` allineerà automaticamente clip con vettori concordanti creando transizioni continue a 360°.

### Transizioni di Occultamento sul Campo (Wipe Naturale)
* Fai terminare un'inquadratura coprendo l'obiettivo con una spalla, una schiena o una bottiglia (lo schermo diventa per un attimo scuro).
* Inizia il clip successivo partendo dallo stesso ostacolo scuro e scoprendo la nuova scena. L'agente riconoscerà il calo di luce e collegherà i due clip a costo zero.

---

## 3. Checklist per Eventi, Feste e Viaggi

| Tipo di Shot | Cosa Inquadrare | Movimento Camera | Ruolo nella Troupe |
| :--- | :--- | :--- | :--- |
| **1. Establishing** | Location, allestimento, skyline | Movimento lento laterale o tilt | Intro & Tonal Suspense (Fase 2) |
| **2. Macro Dettagli** | Bicchieri, scarpe, abito, candele | Micro push-in o statico a fuoco | Staccato hyper-cuts & Foley (Fase 1 & 3) |
| **3. Azione / A-Roll** | Risate spontanee, dialoghi, balli | Orbita a 45° o seguire il passo | Corpo cinetico & Dialoghi ducked (Fase 3) |
| **4. Climax / Hype** | Salto, stappo spumante, fontane | Crash zoom rapido o shake mirato | The Climax Drop (Fase 5) |

---

## 4. Preset Blackmagic Camera (Riprese Pro)

* **Codec**: H.265 (HEVC) o Apple ProRes 422 HQ
* **Color Space**: Apple Log (o Flat)
* **Frame Rate**: 60 FPS costante
* **Shutter Angle**: $180^\circ$ (1/120s a 60 FPS per motion blur naturale)
* **White Balance**: Fisso a 3200K–4000K (Tungsteno) nei locali al chiuso
* **Zebre**: 95% attivo per controllare le alte luci
