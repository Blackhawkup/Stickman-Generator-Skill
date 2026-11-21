---
name: stickman-generator
description: Autonomous end-to-end production of stick-figure explainer slideshow videos in both Phone/Reels (720x1600) and Laptop/Long-Form (1920x1080) formats, featuring synchronized voice narration, editorial webcomic styling with rich 2D background details, ducked royalty-free background music, strict retention pacing (< 3s in 1st minute, ~2s average), automatic companion short generation, social captions with 5 hashtags, 1920x1080 YouTube thumbnail generation, and automatic cleanup of intermediate scratch files. Use when asked to generate, script, storyboard, render, or produce stickman explainer shorts or long-form slideshow videos.
---

# Stickman Slideshow Explainer Generator

A streamlined, high-speed autonomous explainer video production system that synchronizes editorial stick-figure comic illustrations with voice narration and ducked background music.

Supports two distinct production modes:
1. **Phone / Short / Reel Mode**: **720 x 1600** vertical video, centered with matching warm cream background fill.
2. **Laptop / Long-Form Mode**: **1920 x 1080** widescreen video (16:9), which **automatically generates a companion 720x1600 Short** from the opening hook and a matching **1920x1080 YouTube thumbnail**!

---

## 🎯 When to Use This Skill

Activate this skill when:
- Asked to **"generate a clip"**, **"create an explainer short"**, **"make a 10 min video"**, or **"make a video on [Topic]"**.
- Producing timed visual slideshow explainers on psychology, cognitive biases, paradoxes, productivity laws, or human behavior.
- Generating editorial webcomic stick-figure artwork via Google Flow (`flow_agent_images`) with rich 2D background details.
- Generating social media captions with exactly 5 targeted hashtags.
- Generating 1920x1080 YouTube thumbnails in the editorial stick-figure comic art style.
- Automatically cleaning up intermediate scratch files so only final deliverables remain in the execution directory.

---

## ⚡ Core Operating Guardrails

### 1. Pacing & Timing Rules

#### A. The 1st Minute Retention Rule (Both Short & Long-Form)
- **Ceiling**: Every single image in the first 60 seconds MUST stay on screen for **less than 3 seconds** (`< 3.0s`).
- **Average Duration**: **~2.0 seconds on average** across all slides in the first minute.
- **Slide Count**: ~28 to 32 slides in the opening 60 seconds.

#### B. Subsequent Minutes (Long-Form Mode)
- **Minute 1:00 – 2:00 (Bridge Phase)**: Transitions every **2.5s to 4.0s** (hard cap `<= 4.0s`).
- **Minute 2:00 – 10:00 (Deep Exposition & Case Studies)**: Images are allowed to stay on screen for **5.0 to 6.0 seconds** (average ~4.8s–5.5s, hard cap `<= 6.0s`) to let complex case studies, study methodologies, and mental models breathe.
- **Automated Validation**: Run `python tools/cli.py check <slug>`. The auditor enforces `< 3.0s` and checks the `~2.0s` average in the first minute, `<= 4.0s` before 2m, and `<= 6.0s` thereafter.

---

### 2. Resolution & Aspect Ratios

| Mode | Canvas Dimensions | Layout & Background Fill | Flow Aspect Ratio |
|---|---|---|---|
| **Phone / Short / Reel** | **720 x 1600** (Vertical) | Centered artwork; entire screen filled with warm cream (`#FBF6EF`) | `1:1` (Centered) |
| **Laptop / Long-Form** | **1920 x 1080** (Widescreen 16:9) | Full 16:9 cinematic framing with warm cream (`#FBF6EF`) | `16:9` |
| **YouTube Thumbnail** | **1920 x 1080** (Widescreen 16:9) | High-contrast dramatic thumbnail with large topic title | `16:9` |

> [!IMPORTANT]
> In all formats, the image stays in the center and the entire rest of the frame is filled with the exact same background color (`#FBF6EF` warm off-white cream). Zero black bars, zero harsh borders.

---

### 3. Visual DNA & Rich 2D Background Details
- **Characters**: Stylized stick figures with oversized round white heads, expressive dot eyes and eyebrows, rounded bean-shaped torsos, thin black stick limbs, wearing solid bold primary color shirts:
  - **Red**: Urgent, aggressive, results-focused (`#DC2626`).
  - **Yellow**: Enthusiastic, chaotic, spontaneous (`#EAB308`).
  - **Green**: Calm, passive, conflict-avoidant (`#16A34A`).
  - **Blue**: Analytical, meticulous, methodical (`#2563EB`).
- **Rich 2D Environmental Backgrounds**:
  - Scenes feature polished, charming 2D background details drawn in fine black ink lines:
    * Indoor: Mid-century wooden bookshelves with colorful book spines, framed wall art, modern potted indoor plants (fiddle-leaf fig, monstera), stylish floor lamps, cozy desks with laptops and mugs, wall clocks, patterned rugs.
    * Offices / Labs: Glass partitions, chalkboards with flowcharts and arrows, corkboards with notes.
    * Outdoor: Stylized clouds in the warm cream sky, soft rolling hills, distant city skyline silhouettes, lampposts.
  - Background palette uses muted earthy neutrals (slate gray, soft taupe, olive green, warm wood) so the environment looks rich and appealing while keeping the primary-colored stick figures as the clear focal point.
- **Linework & Shading**: Thick uniform black ink outlines on characters, fine outlines on backgrounds, flat 2D cel coloring, soft oval gray ground shadows.

---

### 4. Working Directory & Automatic Scratch Cleanup
- **Save Location**: The directory where the agent is run is the exact directory where all project files and deliverables are created.
- **Automatic Post-Production Cleanup**: After video rendering, all intermediate scratch files and folders (`build/`, `voice/`, `images/`, `out_frames/`, temporary audio WAVs) are **automatically deleted**.
- **Preserved Deliverables**:
  1. Primary Video (`<slug>.mp4` or `<slug>-long.mp4`)
  2. Companion Short for long-form (`<slug>-short.mp4`, 720x1600)
  3. 1920x1080 YouTube Thumbnail for long-form (`<slug>-thumbnail.png`)
  4. Social Media Caption + 5 Hashtags (`<slug>-caption.txt`)
  5. Metadata Record (`<slug>-metadata.json`)
  6. Updated Topic Ledger (`topics/completed_topics.json`)

---

### 5. Dual Audio Engine & Ducking
- Spoken narration mastered to **-14.0 LUFS** integrated loudness.
- Background music auto-selected from `audio/music/` and ducked to **-26.0 dB** behind voice.
- Ambient bed seamlessly loops across any duration (from 1 minute to 10+ minutes).

---

## 🛠️ CLI Quick Reference

```bash
# Initialize a Short (720x1600 phone format)
python tools/cli.py new my-short --mode short

# Initialize a 10-minute Long-Form video (1920x1080 widescreen)
python tools/cli.py new my-deepdive --mode long

# Compile prompts (16:9 + thumbnail for long, centered for phone)
python tools/cli.py prompts <slug>

# Generate TTS voiceover and Whisper word timestamps
python tools/cli.py tts <slug> --voice Charon

# Validate timing & pacing rules (< 3s in 1st min, ~2s avg)
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
   - Short Mode (`720x1600`) vs Long-Form Mode (`1920x1080`).
   - Run in the current working directory where the user executes the agent.
2. **Fetch Topic**: Run `python tools/cli.py topics next` and confirm it is uncompleted.
3. **Draft Script**:
   - For Short: Use `prompts/script_prompt.md`.
   - For Long-Form: Use `prompts/script_long_prompt.md`.
4. **Storyboard**:
   - Enforce `< 3.0s` per slide in the 1st minute, averaging `~2.0s` (~30 slides in minute 1).
   - In long form, slides after minute 2 stay for 5–6 seconds.
5. **Execute Auto Pipeline**: Run `python tools/cli.py auto <slug>`.
   - Produces video(s), caption + 5 hashtags, and thumbnail (for long).
   - Automatically purges scratch folders (`build/`, `voice/`, `images/`).
   - Updates `topics/completed_topics.json`.
6. **Deliver**: Present clickable links to the finished MP4(s), thumbnail image, and caption text.
