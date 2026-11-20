---
name: stickman-generator
description: Autonomous end-to-end production of stick-figure explainer slideshow videos in both 1-minute Shorts (9:16) and 10-minute Long-Form (16:9) formats, featuring synchronized voice narration, editorial webcomic styling, ducked royalty-free background music, dual-phase pacing guardrails, automatic companion short generation, social captions with 5 hashtags, 16:9 YouTube thumbnail generation, and automatic cleanup of intermediate scratch files. Use when asked to generate, script, storyboard, render, or produce stickman explainer shorts or long-form slideshow videos.
---

# Stickman Slideshow Explainer Generator

A streamlined, high-speed autonomous explainer video production system that synchronizes editorial stick-figure comic illustrations with voice narration and ducked background music.

Supports two distinct production modes:
1. **Short Mode**: 1-minute viral vertical short (9:16, 1080x1920, 60fps).
2. **Long-Form Mode**: 10-minute comprehensive deep dive (16:9, 1920x1080, 60fps), which **automatically generates a companion 1-minute vertical short** from the opening hook and a matching **16:9 YouTube thumbnail**!

---

## 🎯 When to Use This Skill

Activate this skill when:
- Asked to **"generate a clip"**, **"create an explainer short"**, **"make a 10 min video"**, or **"make a video on [Topic]"**.
- Producing timed visual slideshow explainers on psychology, cognitive biases, paradoxes, productivity laws, or human behavior.
- Generating editorial webcomic stick-figure artwork via Google Flow (`flow_agent_images`).
- Generating social media captions with exactly 5 targeted hashtags.
- Generating 16:9 YouTube thumbnails in the editorial stick-figure comic art style.
- Automatically cleaning up intermediate scratch files so only final deliverables remain in the execution directory.

---

## ⚡ Core Operating Guardrails

### 1. Working Directory & Automatic Scratch Cleanup
- **Save Location**: The directory where the agent is run is the exact directory where all project files and deliverables are created.
- **Automatic Post-Production Cleanup**: After video rendering, all intermediate scratch files and folders (`build/`, `voice/`, `images/`, `out_frames/`, temporary audio WAVs) are **automatically deleted**.
- **Preserved Deliverables**:
  1. Primary Video (`<slug>.mp4` or `<slug>-long.mp4`)
  2. Companion Short for long-form (`<slug>-short.mp4`)
  3. 16:9 YouTube Thumbnail for long-form (`<slug>-thumbnail.png`)
  4. Social Media Caption + 5 Hashtags (`<slug>-caption.txt`)
  5. Metadata Record (`<slug>-metadata.json`)
  6. Updated Topic Ledger (`topics/completed_topics.json`)

---

### 2. Social Captions & Exactly 5 Hashtags
Every completed video automatically generates:
- **Engaging Caption**: Hooky, curiosity-driven summary of the psychological paradox/concept with a conversational question prompt.
- **Exactly 5 Hashtags**: 5 high-impact, topic-relevant hashtags (e.g. `#{Topic} #Psychology #HumanBehavior #Mindset #LifeHacks`).
- Saved directly to `<slug>-caption.txt` and `<slug>-metadata.json`.

---

### 3. YouTube Thumbnail for Long-Form Videos
When generating a 10-minute long-form video (16:9):
- A dedicated **16:9 widescreen thumbnail** is generated in the **exact same editorial stick-figure webcomic art style**.
- **Topic Name**: Prominently displayed in huge, bold black comic typography across the top center.
- **Focal Character**: Oversized round white head, shocked/wide dot eyes, wearing a bold solid primary red shirt (`#DC2626`).
- **Dramatic Visual Metaphor**: High-contrast, clickable visual scene representing the concept (e.g. throwing bags of cash into a burning incinerator, standing at a cliff edge, or looking at a giant ticking trap).
- **Canvas**: Clean warm parchment cream (`#FBF6EF`), flat 2D coloring, soft gray ground shadow, 16:9 aspect ratio.
- Saved as `<slug>-thumbnail.png`.

---

### 4. Pacing Guardrails (By Mode)

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

### 5. Resolution & Aspect Ratios

| Mode | Video Dimensions | Flow Image Prompt Aspect Ratio | Canvas Layout |
|---|---|---|---|
| **Short** | 1080x1920 (9:16 Vertical) | `1:1` Square (`1080x1080`) | Centered square canvas with clean letterbox |
| **Long-Form** | 1920x1080 (16:9 Horizontal) | `16:9` Landscape (`1920x1080`) | Full bleed widescreen canvas (`#FBF6EF`) |
| **Thumbnail** | 1920x1080 (16:9 Horizontal) | `16:9` Landscape (`1920x1080`) | High-contrast YouTube thumbnail with bold title |

---

### 6. Visual DNA (Editorial Webcomic Style)
- **Head**: Oversized smooth white circle with dot eyes, minimal eyebrows, and expressive mouths.
- **Torso**: Bean/pear-shaped torso wearing plain white or a bold solid primary shirt (Red, Yellow, Green, Blue).
- **Limbs**: Thin, uniform black stick limbs with small oval white hands and shoes.
- **Canvas**: Warm off-white parchment cream background (`#FBF6EF` / `#F6F4EC`).
- **Layout**: Centered action with clean top zone (for headline title) and bottom zone (for captions). No bare pencil sketches; always crisp ink outlines, flat 2D cel colors, and soft gray ground shadows.

---

### 7. Dual Audio Engine & Ducking
- Spoken narration mastered to **-14.0 LUFS** integrated loudness.
- Background music auto-selected from `audio/music/` and ducked to **-26.0 dB** behind voice.
- Ambient bed seamlessly loops across any duration (from 1 minute to 10+ minutes).

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

# Compile prompts (1:1 for short, 16:9 + thumbnail for long)
python tools/cli.py prompts <slug>

# Generate TTS voiceover and Whisper word timestamps
python tools/cli.py tts <slug> --voice Charon

# Generate/view caption + 5 hashtags
python tools/cli.py caption <slug>

# Validate timing & pacing rules
python tools/cli.py check <slug>

# 1-Command Autonomous Production
# - Generates primary video + companion short (if long) + thumbnail (if long)
# - Generates social caption + 5 hashtags
# - Cleans up all intermediate scratch files automatically
# - Updates topics/completed_topics.json
python tools/cli.py auto <slug>
```

---

## 🚀 Autonomous Production Protocol

When the user asks for a video:
1. **Determine Mode & Directory**:
   - Short Mode (`--mode short`) vs Long-Form Mode (`--mode long`).
   - Run in the current working directory where the user executes the agent.
2. **Fetch Topic**: Run `python tools/cli.py topics next` and confirm it is uncompleted.
3. **Draft Script**:
   - For Short: Use `prompts/script_prompt.md`.
   - For Long-Form: Use `prompts/script_long_prompt.md`.
4. **Storyboard**:
   - For Short: 25–30 slides (`prompts/storyboard_prompt.md`), all `<= 4.0s`.
   - For Long-Form: 115–140 slides (`prompts/storyboard_long_prompt.md`), `<= 4.0s` in first 2 mins, `<= 6.0s` after 2 mins.
5. **Execute Auto Pipeline**: Run `python tools/cli.py auto <slug>`.
   - Produces video(s), caption + 5 hashtags, and thumbnail (for long).
   - Automatically purges scratch folders (`build/`, `voice/`, `images/`).
   - Updates `topics/completed_topics.json`.
6. **Deliver**: Present clickable links to the finished MP4(s), thumbnail image, and caption text.
