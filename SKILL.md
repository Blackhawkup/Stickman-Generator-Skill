---
name: stickman-generator
description: Autonomous end-to-end production of stick-figure explainer slideshow videos in both Phone/Reels (720x1600) and Laptop/Long-Form (1920x1080) formats, featuring synchronized voice narration, editorial webcomic styling with rich 2D background details, dynamic royalty-free background music rotation across 12 catalog tracks, strict retention pacing (mostly ~3s, sometimes ~2s; 5-6s after 2m in long form), mandatory "Imagine..." hook architecture, automatic companion short generation, social captions with 5 hashtags, 1920x1080 YouTube thumbnail generation, and automatic cleanup of intermediate scratch files. Use when asked to generate, script, storyboard, render, or produce stickman explainer shorts or long-form slideshow videos.
---

# Stickman Slideshow Explainer Generator

A streamlined, high-speed autonomous explainer video production system that synchronizes editorial stick-figure comic illustrations with voice narration and ducked background music.

Supports two distinct production modes:
1. **Phone / Short / Reel Mode**: **720 x 1600** vertical video, centered with matching warm cream background fill (`#FBF6EF`). Zero black bars.
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

## 🚨 Mandatory Hook Architecture (Non-Negotiable)

Every script (both Short and Long-Form) MUST start with this EXACT 2-sentence opening:
1. **Sentence 1**: The Topic Title in uppercase followed by a period (e.g. `THE PRATFALL EFFECT.` or `THE SUNK COST FALLACY.`).
2. **Sentence 2**: MUST start with `"Imagine a guy..."`, `"Imagine you..."`, or `"Imagine if you..."`:
   - *"Imagine a brilliant speaker in a sharp suit walks onto a stage, delivers a flawless presentation, and then spills hot coffee all over his shirt."*
   - *"Imagine you buy a forty-dollar ticket to a movie, and thirty minutes in, it's completely unwatchable."*
3. **STRICT NEGATIVE CONSTRAINT**: NEVER start with fictional character names (e.g. *"Leo walked into the office..."*, *"David was a manager..."*). NEVER start with creator filler like *"Hey guys"* or unrelated rhetorical questions.

---

## ⏱️ Pacing & Timing Rules

### 1. The Opening / Shorts Pacing (Mostly 3s, Sometimes 2s)
- **Standard Duration**: Mostly **around 3.0 seconds** (2.6s to 3.5s) so viewers can absorb the comic art, props, and captions.
- **Snappy Transitions**: Sometimes **around 2.0 seconds** (1.8s to 2.4s) for quick punchy reveals, surprise beats, or sudden realization cuts.
- **Bounds**: Minimum 1.8 seconds (avoid frantic 1s flashes), maximum ceiling 3.8 seconds (never drag).
- **Target Average**: **~2.8s to 3.2s** across all slides in a short (~20 to 25 slides per ~60–75s video).

### 2. Subsequent Minutes (Long-Form Mode)
- **Minute 1:00 – 2:00 (Bridge Phase)**: Transitions every **3.0s to 4.0s** (hard cap `<= 4.0s`).
- **Minute 2:00 – 10:00 (Deep Exposition & Case Studies)**: Images are allowed to stay on screen for **5.0 to 6.0 seconds** (average ~5.0s–5.5s, hard cap `<= 6.0s`) to let complex studies, methodologies, and mental models breathe.
- **Automated Validation**: Run `python tools/cli.py check <slug>`. The auditor enforces these pacing bounds.

---

## 🎵 Dynamic Background Music Rotation (12 Tracks)

Never repeat the same background music track across videos:
- Curated library of 12 royalty-free instrumental tracks in `audio/music/`:
  `curious`, `investigation`, `mystery`, `sneaky`, `playful`, `quirky`, `upbeat`, `reflective`, `deep_mystery`, `thoughtful`, `light`, `comedy`.
- When set to `"music": "auto"` (the default), `mix.py` automatically maps the topic theme and mood to track candidates while inspecting `topics/completed_topics.json` to prevent back-to-back repeats.
- Narration is mastered to **-14.0 LUFS** with music dynamically ducked to **-26.0 dB** behind speech.

---

## 🎨 Visual DNA, Canvas & Centering

### 1. Canvas Dimensions & Zero Black Bars
| Mode | Canvas Dimensions | Layout & Background Fill | Flow Aspect Ratio |
|---|---|---|---|
| **Phone / Short / Reel** | **720 x 1600** (Vertical) | Centered artwork; entire screen filled with warm cream (`#FBF6EF`) | `1:1` (Centered) |
| **Laptop / Long-Form** | **1920 x 1080** (Widescreen 16:9) | Full 16:9 cinematic framing with warm cream (`#FBF6EF`) | `16:9` |
| **YouTube Thumbnail** | **1920 x 1080** (Widescreen 16:9) | High-contrast dramatic thumbnail with large topic title | `16:9` |

> [!IMPORTANT]
> The image stays in the center and the entire rest of the frame is filled with the exact same warm cream background color (`#FBF6EF`). Zero black bars, zero harsh borders.

### 2. Slide 01 Opening Rule (Title Card)
- **Slide 01** is the viewer's very first impression. It MUST be a compelling, high-CTR **Title Card**.
- `top_title`: Exact phenomenon name in uppercase.
- `bottom_caption`: 1 punchy hook subtitle (e.g. `WHY FLAWS MAKE US LIKEABLE.`, `WHY WE CAN'T LET GO.`).
- `subject`: Rich stylized 2D room setting (wooden bookshelf, potted indoor plant, framed picture) with an expressive stick figure in a bold primary shirt reacting with wide curious eyes.
- **STRICT PROHIBITION**: NEVER generate a plain, blank walking stickman or empty void for Slide 01.

### 3. Rich 2D Background Details
- Every image includes charming 2D background details drawn in fine black ink lines:
  * Mid-century wooden bookshelves with colorful books, framed wall art, modern potted indoor plants (fiddle-leaf fig, monstera), stylish floor lamps, cozy desks with laptops and mugs, wall clocks, patterned rugs.
  * Offices/Labs: Glass partitions, chalkboards with flowcharts and arrows, corkboards with notes.
  * Outdoor: Stylized clouds in the warm cream sky, soft rolling hills, distant city skyline silhouettes, lampposts.
- Background palette uses muted earthy neutrals (slate gray, soft taupe, olive green, warm wood) keeping the primary-colored characters as the clear focal point.

---

## 🧹 Working Directory & Automatic Scratch Cleanup
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

# Validate timing & pacing rules (mostly ~3s, sometimes ~2s)
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
   - **Enforce**: Sentence 1 = `[TITLE].`, Sentence 2 = `Imagine [a guy / you / if you]...` (no named fiction characters).
4. **Storyboard**:
   - Enforce mostly ~3s, sometimes ~2s (~20-25 slides in a short).
   - In long form, slides after minute 2 stay for 5–6 seconds.
   - Slide 01 MUST be a rich Title Card (never a plain walking stickman).
5. **Execute Auto Pipeline**: Run `python tools/cli.py auto <slug>`.
   - Produces video(s), caption + 5 hashtags, and thumbnail (for long).
   - Automatically purges scratch folders (`build/`, `voice/`, `images/`).
   - Updates `topics/completed_topics.json`.
6. **Deliver**: Present clickable links to the finished MP4(s), thumbnail image, and caption text.
