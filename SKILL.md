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

## 🚨 Mandatory Opening Architecture: Name First, Then Imagine (Non-Negotiable)

The video and spoken narration MUST start with the NAME of the law or concept, NOT the hypothetical scenario.
The sequence is strictly: **NAME OF THE THING FIRST, THEN THE IMAGINE PART**.

1. **Sentence 1 (The VERY FIRST Words Spoken)**:
   The narrator speaks the exact name of the law/phenomenon in UPPERCASE followed by a period:
   - `THE PRATFALL EFFECT.`
   - `THE SUNK COST FALLACY.`
   - `PARKINSON'S LAW.`
   - `THE SPOTLIGHT EFFECT.`
   *Crucial*: The narrator MUST speak this name out loud as the very first sentence. The video starts with the Title Card displaying this name.
2. **Sentence 2 (The VERY NEXT Words Spoken - Scenario Begins)**:
   Immediately AFTER the name is stated, the very next sentence begins the scenario with **"Imagine"**:
   - *"Imagine a brilliant speaker in a sharp suit walks onto a stage, delivers a flawless presentation, and then spills hot coffee all over his shirt."*
   - *"Imagine you buy a forty-dollar ticket to a movie, and twenty minutes in, it's completely unwatchable."*
3. **STRICT NEGATIVE CONSTRAINTS**:
   - NEVER start the video with "Imagine..." before stating the name of the law.
   - NEVER use named fiction characters (e.g. *"Leo walked into the office..."*, *"David was a manager..."*).
   - NEVER save the name of the law for the middle or end of the video.

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

## 🎵 Sophisticated Explainer Audio & Dynamic Music Rotation

Never use annoying cartoon meme tracks or repetitive loops:
- Curated library of modern, calm, sophisticated explainer instrumental tracks in `audio/music/`:
  * `clean_soul`: Smooth, modern Rhodes piano lo-fi chillhop groove (habits, everyday life, psychology).
  * `deliberate_thought`: Minimalist, intellectual marimba and subtle acoustic pulse (scientific studies, data, experiments).
  * `perspectives`: Neutral, elegant modern documentary acoustic flow (10-minute long-form deep dives, history, multi-part cases).
  * `thoughtful`: Steady, productive acoustic rhythm (Parkinson's Law, time management, productivity).
  * `reflective`: Calm introspective walking tempo with Rhodes chords (philosophical takeaways, mindsets).
  * `heartwarming`: Gentle uplifting acoustic warmth and piano (breakthroughs, actionable insights).
  * `light`: Ultra-clean subtle ambient background that stays completely out of the way of spoken voice.
  * `deep_mystery`: Low-key noir detective jazz bass for unresolved paradoxes.
  * `composed`: Procedurally synthesized lush harmonic ambient pad with warm reverb. Infinite length, zero ear fatigue.
- **Zero Cartoon Comedy**: Wacky cartoon tracks (`comedy`, `playful`, `sneaky`, `quirky`) are removed from rotation.
- **Seamless Crossfade Looping**: Audio loops with an equal-power 2.5s crossfade, eliminating abrupt cuts or glitches over 10-minute videos.
- **Loudness Balance**: Narration mastered to **-14.0 LUFS** with music ducked to **-29.0 dB** so it sits softly in the background.

---

## 🖼️ Mandatory 1920x1080 High-CTR YouTube Thumbnail

For every long-format video, a dedicated 1920x1080 YouTube thumbnail **MUST ALWAYS be generated and used**:
- **Design Formula**:
  * Large, bold comic book headline title across the top: `"{TOPIC TITLE}"`.
  * High-contrast red accent hook/warning banner (`#DC2626`).
  * Centered expressive stick-figure character in crimson red shirt (#DC2626) reacting in shock/disbelief to the core dilemma.
  * Warm cream parchment background (`#FBF6EF`) with 2D bookshelf, desk, and subtle spotlighting.
- **Automatic Generation**:
  * Generated and preserved at `<project>/<slug>-thumbnail.png`.
  * Can be created directly via `python tools/cli.py thumbnail <slug>` or during `cli.py auto`.
- **Where the Thumbnail is Used**:
  * **Deliverable**: Saved directly in project root ready for YouTube upload.
  * **Metadata**: Linked in `<slug>-metadata.json` under `"thumbnail_path"`.
  * **Ledger**: Recorded in `topics/completed_topics.json` under `"thumbnail"`.
  * **Web Player**: Embedded in `build/page.html` as the pre-play poster.
  * **Deliverable Presentation**: The agent MUST present a clickable link and image preview to the user upon completion.

---

## 🎨 Visual DNA, Canvas & Separate Short Images

### 1. Canvas Dimensions & Dedicated Vertical 9:16 Generation
| Mode | Canvas Dimensions | Layout & Background Fill | Flow Aspect Ratio |
|---|---|---|---|
| **Phone / Short / Reel** | **720 x 1600** (Vertical) | Native 9:16 full-height composition; warm cream (`#FBF6EF`) fill | `9:16` (Full Height) |
| **Companion Short (Long-Form)** | **720 x 1600** (Vertical) | Generated **SEPARATELY** as dedicated 9:16 vertical images (`short_slide_*.png`) | `9:16` (Full Height) |
| **Laptop / Long-Form** | **1920 x 1080** (Widescreen 16:9) | Full 16:9 cinematic framing with warm cream (`#FBF6EF`) | `16:9` |
| **YouTube Thumbnail** | **1920 x 1080** (Widescreen 16:9) | High-contrast dramatic thumbnail with large topic title | `16:9` |

> [!IMPORTANT]
> **No Small Images in Shorts**: All short images are generated in native **9:16 vertical** aspect ratio with large, prominent characters occupying the tall frame. In long-form projects, the companion short NEVER reuses the 16:9 widescreen images; separate vertical 9:16 images are generated specifically for the short. Zero small images, zero black bars.

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

# Generate dedicated 1920x1080 High-CTR YouTube Thumbnail
python tools/cli.py thumbnail <slug>

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
