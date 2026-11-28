---
name: stickman-generator
description: Zero-input autonomous end-to-end production of stick-figure explainer slideshow videos in both Phone/Reels (1080x1920, 9:16 vertical) and Laptop/Long-Form (1920x1024 16:9 images on 1920x1080 HD video) formats. Features always-on word-highlighted synced subtitles on every video, automatic selection of the catchiest uncompleted topic without repeats, synchronized voice narration, editorial webcomic styling with rich 2D background details, dynamic modern ambient music rotation across 12 tracks, strict retention pacing (mostly ~3s, sometimes ~2s; 5-6s after 2m in long form), mandatory Name-First then Imagine hook architecture, automatic companion 9:16 short generation, social captions with 5 hashtags, 1920x1080 YouTube thumbnail generation, and automatic cleanup of intermediate scratch files. Use when asked to generate, script, storyboard, render, or produce stickman explainer shorts or long-form slideshow videos.
---

# Stickman Slideshow Explainer Generator

A streamlined, 100% autonomous explainer video production system that automatically selects the catchiest unproduced topic, synchronizes editorial stick-figure comic illustrations with voice narration, dynamic word-highlighted subtitles, and ducked background music—requiring **zero user inputs** throughout the pipeline.

Supports two distinct production modes:
1. **Phone / Short / Reel Mode**: **1080 x 1920 pixels (`9:16` vertical portrait)** video and images, synced word-highlighted subtitles, and matching warm cream background (`#FBF6EF`). Zero black bars.
2. **Laptop / Long-Form Mode**: **1920 x 1080 (`16:9` widescreen)** video with **1920 x 1024 (`16:9`)** artwork, synced subtitles, which **automatically generates a companion 1080x1920 (`9:16`) Short** from the opening hook and a matching **1920x1080 YouTube thumbnail**!

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

## 🎨 Visual DNA, Canvas & Synced Subtitles

### 1. Canvas Dimensions & Exact Image Resolutions
| Mode | Video Canvas Dimensions | Image Resolution & Aspect Ratio | Layout & Background Fill |
|---|---|---|---|
| **Phone / Short / Reel** | **1080 x 1920** (`9:16` Vertical) | **1080 x 1920** (`9:16` Vertical) | Full-height vertical portrait; warm cream (`#FBF6EF`) seamless fill |
| **Companion Short (Long-Form)** | **1080 x 1920** (`9:16` Vertical) | **1080 x 1920** (`9:16` Vertical) | Generated **SEPARATELY** as dedicated `1080x1920` (`9:16`) vertical images (`short_slide_*.png`) |
| **Laptop / Long-Form** | **1920 x 1080** (`16:9` Widescreen) | **1920 x 1024** (`16:9` Landscape) | Centered `1920x1024` artwork inside `1920x1080` HD canvas with warm cream (`#FBF6EF`) fill |
| **YouTube Thumbnail** | **1920 x 1080** (`16:9` Widescreen) | **1920 x 1080** (`16:9` Landscape) | High-contrast dramatic thumbnail with large topic title |

> [!IMPORTANT]
> **Exact Dimensions & Separate Short Artwork**:
> - **Shorts (`9:16`)**: Generated and normalized to exact **1080 × 1920 pixels (`9:16` vertical)**. Characters and scenes fill the tall portrait screen without shrinking or black bars.
> - **Long-Form (`16:9`)**: Slide images are generated and normalized to exact **1920 × 1024 pixels (`16:9` landscape)**, leaving clean cream margins at the bottom of the 1920x1080 HD frame for synced subtitles.
> - **Companion Short**: NEVER reuses 16:9 widescreen images; separate `1080x1920` (`9:16`) images are always generated specifically for the companion short.

### 2. Always-On Synced Subtitles
- **Every generated video** (Short, Long-Form, and Companion Short) includes **word-highlighted phrase subtitles** automatically synced to `voice/words.json`.
- Rendered deterministically at 60 FPS inside `engine/slideshow.js` in a high-contrast slate pill (`rgba(15, 23, 42, 0.90)`) with white text and bright yellow (`#FACC15`) active spoken word highlighting.
- Automatically positioned in the mobile safe zone (`bottom: 11%` on `1080x1920`) and bottom subtitle zone (`bottom: 30px` on `1920x1080`).

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
# Auto-pick the catchiest uncompleted topic and initialize project
python tools/cli.py new --mode short            # 1080x1920 (9:16 vertical)
python tools/cli.py new --mode long             # 1920x1080 HD video (1920x1024 16:9 images)

# Or specify an explicit slug
python tools/cli.py new my-short --mode short
python tools/cli.py new my-deepdive --mode long

# Inspect catchiest available topic (zero repeats against completed_topics.json)
python tools/cli.py topics next

# Compile prompts (1920x1024 16:9 + 1920x1080 thumbnail + 1080x1920 companion short; or 1080x1920 short)
python tools/cli.py prompts <slug>

# Generate TTS voiceover and Whisper word timestamps (powers synced subtitles)
python tools/cli.py tts <slug> --voice Charon

# Validate timing & pacing rules (mostly ~3s, sometimes ~2s)
python tools/cli.py check <slug>

# Generate dedicated 1920x1080 High-CTR YouTube Thumbnail
python tools/cli.py thumbnail <slug>

# 1-Command Autonomous Production
# - Generates narration + artwork + enforces exact 1080x1920 / 1920x1024 resolutions
# - Renders subtitled primary video + companion 1080x1920 short (if long) + 1920x1080 thumbnail (if long)
# - Generates social caption + 5 hashtags
# - Cleans up all intermediate scratch files automatically
# - Updates topics/completed_topics.json
python tools/cli.py auto <slug>
```

---

## 🤖 Zero-Input Autonomous Production Protocol (Strict Requirement)

The agent MUST operate **100% automatically with zero user questions or confirmations** once the user asks for a Short or Long-Form video:

1. **Determine Mode & Directory**:
   - Infer **Short Mode** (`1080x1920`, `9:16`) or **Long-Form Mode** (`1920x1080` video with `1920x1024` `16:9` images) from the user prompt. Default to `short` if unspecified.
   - Run directly in the active working directory where the user executes the agent.
2. **Automatically Pick the Catchiest Uncompleted Topic (No User Prompt Needed)**:
   - Run `python tools/cli.py new --mode <short|long>` (without asking the user for a topic!). It automatically scores and picks the catchiest uncompleted topic via `topics.get_best_topic()`, verified against `topics/completed_topics.json` so there are zero repeats.
   - If the user named a specific topic, verify it isn't a repeat; if `example_topics.json` is empty, immediately brainstorm a highly catchy psychology/paradox concept, add it via `tools/topics.py add`, and proceed immediately without pausing.
3. **Draft Script Immediately (Zero Approval Loops)**:
   - Short Mode: Follow `prompts/script_prompt.md`.
   - Long-Form Mode: Follow `prompts/script_long_prompt.md`.
   - **Enforce**: Sentence 1 = `[TITLE].`, Sentence 2 = `Imagine [a guy / you / if you]...` (no named fiction characters).
4. **Storyboard Automatically**:
   - Enforce mostly ~3s, sometimes ~2s (~20-25 slides in minute 1; 5–6s after minute 2 in long form).
   - Slide 01 MUST be a rich Title Card (never a plain walking stickman).
5. **Execute Auto Pipeline**: Run `python tools/cli.py auto <slug>`.
   - Produces subtitled MP4 video(s), companion `1080x1920` short (if long), `1920x1080` thumbnail (if long), and caption + 5 hashtags.
   - Automatically normalizes all images to exact `1080x1920` (short) and `1920x1024` (long).
   - Automatically purges scratch folders (`build/`, `voice/`, `images/`).
   - Automatically updates `topics/completed_topics.json`.
6. **Deliver Final Product**: Present clickable links to the finished subtitled MP4(s), thumbnail image (for long-form), and social caption + 5 hashtags.
