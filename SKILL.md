---
name: stickman-generator
description: Autonomous end-to-end production of 1-minute stick-figure explainer slideshow shorts with synchronized voice narration, editorial webcomic styling, ducked royalty-free background music, strict pacing guardrails (2.0s-4.0s), and topic deduplication. Use when asked to generate, script, storyboard, render, or produce stickman explainer shorts or timed slideshow videos.
---

# Stickman Slideshow Explainer Generator

A streamlined, high-speed autonomous explainer video production system that synchronizes editorial stick-figure comic illustrations with voice narration and ducked background music for YouTube Shorts, Instagram Reels, and TikTok.

---

## 🎯 When to Use This Skill

Activate this skill when:
- The user requests to **"generate a clip"**, **"create an explainer short"**, or **"make a video on [Topic]"**.
- Producing timed visual slideshow explainers on psychology, cognitive biases, paradoxes, productivity laws, or human behavior.
- Generating editorial webcomic stick-figure artwork via Google Flow (`flow_agent_images`).
- Synchronizing image slide transitions strictly to speech audio word clocks via Whisper.
- Ensuring strict pacing standards (**no slide on screen for more than 4.0 seconds**).

---

## ⚡ Core Operating Guardrails

Every generated video MUST adhere to these non-negotiable standards:

1. **Strict Slide Pacing (Retention Rule)**:
   - **Hard Ceiling**: No single slide may remain on screen for more than **4.0 seconds**.
   - **Target Duration**: **2.0 to 3.5 seconds** per slide.
   - **Slide Count**: For a 60–80 second short, always generate **25 to 30 slides**.
   - **Verification**: Run `python tools/cli.py check <slug>` before rendering. If any slide exceeds 4.0s, split the slide or add transition beats.

2. **Visual DNA (Editorial Comic Style)**:
   - **Head**: Oversized smooth white circle/oval with minimal dot eyes and simple expressive eyebrows/mouths. No ears, no nose, no hair.
   - **Body**: Simple rounded trapezoidal/bean torso. Main character wears either plain white or a single bold primary color shirt (Crimson Red, Warm Yellow, Leaf Green, or Cerulean Blue).
   - **Limbs**: Thin, uniform black stick arms/legs with small oval white hands and shoes.
   - **Canvas**: Clean warm off-white cream background (`#F6F4EC` / `#FBF6EF`). Never pure clinical white (`#FFFFFF`).
   - **Layout**: Centered character/props in middle 60%. Clean negative space at top (for title) and bottom (for captions). No bare pencil sketches; always finished comic ink lines with flat 2D cel coloring and soft gray oval ground shadows.

3. **Audio Mastering & Ducking**:
   - Spoken narration mastered to **-14.0 LUFS** integrated loudness.
   - Background music auto-selected from `audio/music/` and ducked to **-26.0 dB** behind voice.
   - Voice audio generated via Gemini Studio TTS (`Charon` or `Puck`) or user-supplied audio.

4. **Format & Rendering**:
   - **Aspect Ratio**: 9:16 vertical short (1080x1920).
   - **Frame Rate**: 60 FPS for fluid transitions and sharp text overlays.
   - **Transition Style**: Instant hard cuts (`transition: "cut"`, `fade_duration: 0.0s`), static camera (`ken_burns_zoom: 1.0`).

5. **Topic Deduplication**:
   - Always check `topics/completed_topics.json` before starting.
   - Never produce a topic that has already been completed.
   - Auto-log newly completed videos with title, duration, slide count, and file paths.

---

## 🏗️ Architecture & Directory Layout

```
stickman-generator/
├── SKILL.md                          # This agent reference guide
├── README.md                         # Public documentation & setup
├── requirements.txt                  # Python dependencies
├── package.json                      # Node scripts & metadata
├── prompts/                          # Extracted prompts & visual styling
│   ├── topic_prompt.md               # Topic discovery & psychological angle
│   ├── script_prompt.md              # 10-step spoken narration script formula
│   ├── storyboard_prompt.md          # Visual scene & trigger phrase breakdown
│   ├── image_prompt_template.md      # Flow prompt formula & negative rules
│   └── style_presets.json            # Visual style presets (editorial comic)
├── engine/
│   └── slideshow.js                  # Browser rendering engine (60fps canvas)
├── tools/                            # Execution tooling & CLI
│   ├── cli.py                        # Unified CLI (auto, new, tts, check, render)
│   ├── topics.py                     # Topic queue selector & deduplication
│   ├── prompts.py                    # Flow prompt builder from slides.json
│   ├── flow_driver.py                # Automated Google Flow MCP runner
│   ├── voice.py                      # TTS generation & Whisper word-clock alignment
│   ├── mix.py                        # Audio ducking & LUFS mastering
│   ├── build.py                      # HTML web player generator
│   ├── check.py                      # Pacing validation & duration audit
│   ├── render.py                     # 60fps Playwright + FFmpeg video renderer
│   └── common.py                     # Shared paths & execution helpers
├── topics/
│   ├── example_topics.json           # Queue of viral ideas waiting to be made
│   ├── completed_topics.json         # Permanent ledger of finished videos
│   └── README.md                     # Topics system instructions
├── audio/
│   └── music/                        # Curated royalty-free background tracks
│       ├── music_catalog.json        # Mood tags & track definitions
│       └── *.mp3                     # High-quality instrumental audio files
├── templates/
│   └── film.json                     # Default video project manifest
├── examples/                         # Verified canonical reference outputs
│   └── sunk-cost-fallacy/            # Complete 30-slide 60fps reference short
└── projects/                         # Active working directory for new shorts
```

---

## 🚀 Autonomous Production Workflow

When asked to generate a short, execute this sequence:

### Step 1: Select Topic & Check Deduplication
Run:
```bash
python tools/cli.py topics next
```
- Fetches the next topic from `topics/example_topics.json`.
- Confirms it does not exist in `topics/completed_topics.json`.
- Extracts `slug`, `topic`, `hook_scenario`, `core_concept`, and `researcher`.

### Step 2: Generate the Spoken Narration Script
Reference `prompts/script_prompt.md` to craft a ~220–250 word script (~60–75s duration) following the 10-step viral narrative arc:
1. **The relatable everyday hook** (0–6s)
2. **Escalation of commitment** (6–15s)
3. **The realization / breaking point** (15–25s)
4. **Naming the psychological paradox** (25–35s)
5. **The historical origin / researcher study** (35–48s)
6. **The underlying psychological mechanism** (48–58s)
7. **Everyday modern manifestations** (58–68s)
8. **The contrarian takeaway & punchline** (68–75s)

Save the script to `projects/<slug>/script.md`.

### Step 3: Generate Narration Audio & Word Clocks
Run TTS and Whisper word alignment:
```bash
python tools/cli.py tts <slug> --voice Charon
```
- Calls Gemini Studio TTS API to synthesize natural conversational speech.
- Runs `faster-whisper` (int8) to extract word-level timestamps (`voice/words.json`).
- Yields exact project duration and word clocks.

### Step 4: Storyboard with Strict Pacing (25–30 Slides)
Break the script into 25–30 visual slides following `prompts/storyboard_prompt.md`:
- Every slide maps to an exact acoustic `trigger` phrase in `script.md`.
- Ensure interval between consecutive trigger words is between **2.0s and 4.0s**.
- Each slide contains:
  * `title`: Uppercase context headline at the top (e.g., `"THE CONCORDE FALLACY"`).
  * `caption`: 3–6 word bottom caption (e.g., `"THROWING GOOD MONEY AFTER BAD"`).
  * `subject`: Detailed scene description following the visual DNA.
  * `props`: Minimalist everyday objects.
  * `style`: `"editorial_stick_comic"`.

Save to `projects/<slug>/slides.json`.

### Step 5: Build Image Generation Prompts
Run:
```bash
python tools/cli.py prompts <slug>
```
Compiles `prompts.json` applying the Editorial Webcomic DNA:
`"{subject}. Modern 2D editorial webcomic explainer illustration on a warm off-white cream background (#F6F4EC)..."`

### Step 6: Generate Images via Google Flow MCP
Invoke Google Flow MCP tool `flow_agent_images`:
- Pass prompt and aspect ratio `1:1`.
- Download generated slide images into `projects/<slug>/images/slide_01_hook.png` through `slide_30_...png`.

### Step 7: Mix Background Music with Audio Ducking
Select appropriate background music based on tone (e.g., `curious.mp3`, `mystery.mp3`, `upbeat.mp3`) and mix:
```bash
python tools/cli.py mix <slug> --music audio/music/curious.mp3 --music-gain-db -26.0 --target-lufs -14.0
```
Produces mastered dual-layer audio at `projects/<slug>/voice/mix.wav`.

### Step 8: Build Player & Validate Pacing Guardrails
Build web player and run validation:
```bash
python tools/cli.py build <slug>
python tools/cli.py check <slug>
```
`check.py` asserts:
- [x] All 25–30 slide images exist.
- [x] Every trigger phrase matches in `words.json`.
- [x] **Zero pacing violations (> 4.0s)**.
- [x] Audio mix exists and aligns with video duration.

### Step 9: Render 60 FPS MP4 Video
Render final video:
```bash
python tools/cli.py render <slug> --fps 60 --concurrency 8
```
- Playwright captures frame sequences in parallel.
- FFmpeg encodes high-bitrate H.264 video with AAC stereo audio into `projects/<slug>/out/<slug>.mp4`.

### Step 10: Auto-Log Completed Topic
Record completion into `topics/completed_topics.json`:
```bash
python tools/cli.py topics complete <slug> --duration <sec> --slides <count>
```

---

## ⚡ 1-Command Autonomous CLI Execution

To run all steps in a single automated pipeline:
```bash
python tools/cli.py auto <slug> --voice Charon --music curious.mp3
```

---

## 🛠️ CLI Quick Reference

| Command | Action |
|---|---|
| `python tools/cli.py topics next` | Get the next unproduced topic idea |
| `python tools/cli.py topics list` | List all available ideas in the queue |
| `python tools/cli.py topics completed` | View all finished videos |
| `python tools/cli.py new <slug> --format 9:16` | Initialize a new project directory |
| `python tools/cli.py tts <slug> --voice Charon` | Generate voiceover & Whisper timestamps |
| `python tools/cli.py prompts <slug>` | Generate Google Flow prompt manifest |
| `python tools/cli.py mix <slug> --music <file>` | Master voice and duck background music |
| `python tools/cli.py build <slug>` | Compile interactive HTML player |
| `python tools/cli.py check <slug>` | Audit timing, triggers, and <= 4.0s pacing |
| `python tools/cli.py preview <slug>` | Render fast 15fps video draft |
| `python tools/cli.py render <slug> --fps 60` | Render production 60fps MP4 short |
| `python tools/cli.py auto <slug>` | Run entire pipeline end-to-end |
