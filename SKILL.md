---
name: stickman-generator
description: Autonomous end-to-end production of stick-figure explainer slideshow videos in both 1-minute Shorts (9:16) and 10-minute Long-Form (16:9) formats, featuring synchronized voice narration, editorial webcomic styling, ducked royalty-free background music, dual-phase pacing guardrails, automatic companion short generation, and topic deduplication. Use when asked to generate, script, storyboard, render, or produce stickman explainer shorts or long-form slideshow videos.
---

# Stickman Slideshow Explainer Generator

A streamlined, high-speed autonomous explainer video production system that synchronizes editorial stick-figure comic illustrations with voice narration and ducked background music.

Supports two distinct production modes:
1. **Short Mode**: 1-minute viral vertical short (9:16, 1080x1920, 60fps).
2. **Long-Form Mode**: 10-minute comprehensive deep dive (16:9, 1920x1080, 60fps), which **automatically generates a companion 1-minute vertical short** from the opening hook!

---

## 🎯 When to Use This Skill

Activate this skill when:
- Asked to **"generate a clip"**, **"create an explainer short"**, **"make a 10 min video"**, or **"make a video on [Topic]"**.
- Producing timed visual slideshow explainers on psychology, cognitive biases, paradoxes, productivity laws, or human behavior.
- Generating editorial webcomic stick-figure artwork via Google Flow (`flow_agent_images`).
- Synchronizing slide transitions strictly to speech audio word clocks via Whisper.
- Enforcing retention pacing guardrails.

---

## ⚡ Core Operating Guardrails

### 1. Pacing Guardrails (By Mode)

#### A. Short Mode (~60–80 Seconds)
- **Duration**: 2.0s to 4.0s per slide (average ~2.5–3.5s).
- **Hard Ceiling**: No single slide may stay on screen for more than **4.0 seconds**.
- **Slide Count**: 25 to 30 slides per video.

#### B. Long-Form Mode (~10 Minutes / 600 Seconds)
- **Phase 1: High-Retention Hook Window (0:00 – 2:00)**:
  - Pacing is identical to the Short!
  - Slides stay for **2.0s to 4.0s** (hard ceiling: **<= 4.0s**).
  - Maximizes early retention and hooks the audience with fast visual transitions.
- **Phase 2: Deep Exposition & Case Studies (2:00 – 10:00)**:
  - Pacing is relaxed: images are allowed to stay on screen for **5.0 to 6.0 seconds** (average ~4.8s).
  - Hard ceiling: **<= 6.0s**.
  - Provides adequate breathing room for multi-character dialogues, historical case studies, and mental model diagrams.
- **Slide Count**: ~115 to 145 slides for the full 10-minute video.
- **Automated Validation**: Run `python tools/cli.py check <slug>`. The auditor enforces `<= 4.0s` for the first 2 minutes and `<= 6.0s` thereafter.

---

### 2. Resolution & Aspect Ratios

| Mode | Video Dimensions | Flow Image Prompt Aspect Ratio | Canvas Layout |
|---|---|---|---|
| **Short** | 1080x1920 (9:16 Vertical) | `1:1` Square (`1080x1080`) | Centered square canvas with clean letterbox |
| **Long-Form** | 1920x1080 (16:9 Horizontal) | `16:9` Landscape (`1920x1080`) | Full bleed widescreen canvas (`#FBF6EF`) |

---

### 3. Visual DNA (Editorial Webcomic Style)
- **Head**: Oversized smooth white circle with dot eyes, minimal eyebrows, and expressive mouths.
- **Torso**: Bean/pear-shaped torso wearing plain white or a bold solid primary shirt:
  - **Red**: Urgent, driven, aggressive, results-focused (`#DC2626`).
  - **Yellow**: Enthusiastic, chaotic, spontaneous, energetic (`#EAB308`).
  - **Green**: Calm, passive, conflict-avoidant, patient (`#16A34A`).
  - **Blue**: Analytical, meticulous, methodical, fact-driven (`#2563EB`).
- **Limbs**: Thin, uniform black stick limbs with small oval white hands and shoes.
- **Canvas**: Warm off-white parchment cream background (`#FBF6EF` / `#F6F4EC`).
- **Layout**: Centered action with clean top zone (for headline title) and bottom zone (for captions). No bare pencil sketches; always crisp ink outlines, flat 2D cel colors, and soft gray ground shadows.

---

### 4. Audio Mastering & Ducking
- Spoken narration mastered to **-14.0 LUFS** integrated loudness.
- Background music auto-selected from `audio/music/` and ducked to **-26.0 dB** behind voice.
- Ambient bed seamlessly loops across any duration (from 1 minute to 10+ minutes).

---

### 5. Automatic Companion Short Generation
When producing a **10-minute long-form video**, the pipeline **automatically extracts and renders an autonomous 1-minute vertical 9:16 Short** from the opening hook.
- Delivered simultaneously in `projects/<slug>/out/`:
  - `<slug>-long.mp4` (1920x1080, 16:9 widescreen, ~10m)
  - `<slug>-short.mp4` (1080x1920, 9:16 vertical short, ~1m)

---

## 📜 Script Architecture

### Short Script Formula (`prompts/script_prompt.md`)
~220–250 words (~60–75s) following a rapid 10-step sequence:
Hook -> Everyday scenario -> Escalation -> Paradox reveal -> Research origin -> Psychological mechanism -> Everyday traps -> Contrarian takeaway.

### 10-Minute Long-Form Script Formula (`prompts/script_long_prompt.md`)
~1300–1500 words (~10 minutes) across 7 structured acts:
1. **0:00 – 1:00 (The Viral Hook Short)**: Must start with Title Card + *"Imagine..."* (relatable dilemma). Designed to stand alone as the companion Short.
2. **1:00 – 2:00 (The Bridge to Depth)**: Escalation from personal choice to corporate/societal stakes + thesis roadmap.
3. **2:00 – 4:00 (The Science & Origin)**: The researchers, experimental methodology, and counter-intuitive data.
4. **4:00 – 6:30 (Real-World Case Studies)**: 2–3 deep historical blunders (e.g. Concorde fallacy, Kodak, mountaineering).
5. **6:30 – 8:30 (Everyday Modern Traps)**: Career, relationship, and financial subscription traps.
6. **8:30 – 9:30 (Actionable Mental Models)**: Clean Slate / Stranger Test, Zero-Based Thinking, exit rules.
7. **9:30 – 10:00 (Philosophical Synthesis)**: Final takeaway and memorable closing punchline.

---

## 🛠️ CLI Quick Reference

```bash
# Initialize a 1-minute Short (9:16 vertical)
python tools/cli.py new my-short --mode short

# Initialize a 10-minute Long-Form video (16:9 widescreen)
python tools/cli.py new my-deepdive --mode long

# Compile prompts for Google Flow (1:1 for short, 16:9 for long)
python tools/cli.py prompts <slug>

# Generate TTS voiceover and Whisper word timestamps
python tools/cli.py tts <slug> --voice Charon

# Mix ducked background music with voice
python tools/cli.py mix <slug>

# Validate timing & pacing rules (enforces 4s rule in first 2 mins, 6s thereafter)
python tools/cli.py check <slug>

# Manually extract companion short from a long-form project
python tools/cli.py extract-short <slug>

# 1-Command Autonomous Production
# - For short: produces out/<slug>.mp4
# - For long: produces out/<slug>-long.mp4 AND out/<slug>-short.mp4 automatically!
python tools/cli.py auto <slug>
```

---

## 🚀 Autonomous Production Protocol

When the user asks for a video:
1. **Determine Mode**:
   - If user asks for a "clip", "short", or "reels" -> use **Short Mode** (`--mode short`).
   - If user asks for a "10 min video", "long video", or "deep dive" -> use **Long-Form Mode** (`--mode long`).
2. **Fetch Topic**: Run `python tools/cli.py topics next` and confirm it is uncompleted.
3. **Draft Script**:
   - For Short: Use `prompts/script_prompt.md`.
   - For Long-Form: Use `prompts/script_long_prompt.md`.
4. **Storyboard**:
   - For Short: 25–30 slides (`prompts/storyboard_prompt.md`), all `<= 4.0s`.
   - For Long-Form: 115–140 slides (`prompts/storyboard_long_prompt.md`), `<= 4.0s` in first 2 mins, `<= 6.0s` after 2 mins. Tag opening ~20–25 slides with `"short_candidate": true`.
5. **Run Auto Pipeline**: Run `python tools/cli.py auto <slug>`.
6. **Deliver**: Provide direct links to the generated MP4 deliverables.
