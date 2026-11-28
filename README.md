# Stickman Explainer Video Generator Skill

A 100% autonomous, zero-input, high-retention video production skill that creates both **Phone/Reel Shorts (1080x1920, 9:16)** and **Laptop/Long-Form videos (1920x1080 HD with 1920x1024 16:9 slides)** at 60 FPS, pairing editorial stick-figure illustrations with **always-on word-highlighted subtitles**, rich 2D background details, synchronized voice narration, and ducked royalty-free background music.

Designed to run completely automatically without user prompts—picking the catchiest unproduced topic, generating finished deliverables (videos with burned-in subtitles, social captions with 5 hashtags, and 1920x1080 thumbnails) in the active directory while automatically purging intermediate scratch files.

---

## ⚡ Key Highlights

- **⚡ Dual Video Formats & Exact Pixel Dimensions**:
  - **Phone / Short / Reel (`9:16` Vertical)**: **1080 × 1920 pixels** (`9:16` vertical) images and 60fps video with large, prominent characters filling the mobile canvas. Zero small images, zero black bars.
  - **Laptop / Long-Form (`16:9` Widescreen)**: **1920 × 1024 pixels** (`16:9` landscape) slides rendered cleanly inside a **1920 × 1080** HD canvas with rich 2D environmental details and warm cream (`#FBF6EF`) fill.
  - **Separate Short Images**: In long-form projects, the companion short **generates its own dedicated 1080×1920 (`9:16`) vertical images** (`short_slide_*.png`), never reusing or letterboxing 16:9 widescreen images!
- **💬 Always-On Word-Synced Subtitles**:
  - Every generated video (Short, Long-Form, and Companion Short) renders **crisp, high-contrast phrase subtitles** with real-time yellow word highlighting (`#FACC15`) in an ink-bordered slate pill (`rgba(15, 23, 42, 0.90)`), aligned deterministically to Faster-Whisper word timestamps.
- **🤖 Zero-Input Autonomous Execution**:
  - Needs **zero user input** throughout production: automatically scores and selects the **catchiest uncompleted topic** (`python tools/cli.py topics next`), writes script + storyboard, generates narration + artwork, normalizes resolutions, renders with subtitles, extracts companion short + thumbnail (if long), cleans up temp files, and updates the topic ledger.
- **🚨 Mandatory Hook Formula (Name First, Then Imagine)**:
  - **Sentence 1**: Spoken uppercase name of the law/phenomenon (e.g., `THE PRATFALL EFFECT.` or `THE SUNK COST FALLACY.`). The video and narration start with the name!
  - **Sentence 2**: Immediately follows with the scenario starting with `"Imagine a guy..."`, `"Imagine you..."`, or `"Imagine if you..."`.
  - **Negative Constraint**: Zero named fictional characters (banned: *"Leo walked into the office..."*). Never start with "Imagine" before stating the name.
- **⏱️ High-Retention Pacing (Mostly 3s, Sometimes 2s)**:
  - Slides stay on screen for mostly **~3.0 seconds**, dipping to **~2.0 seconds** for fast surprise beats or punchlines (target average ~2.8s–3.2s).
  - In long-form after 2 minutes, slides stay on screen for **5.0 to 6.0 seconds** for deep exposition.
- **🎵 Sophisticated Explainer Audio & Dynamic Music Rotation**:
  - Curated library of modern, calm explainer instrumental tracks: `clean_soul` (chill Rhodes lo-fi), `deliberate_thought` (documentary marimba & pulse), `perspectives` (modern documentary acoustic flow), `thoughtful` (productive acoustic beat), `reflective` (introspective Rhodes chords), `heartwarming` (uplifting acoustic guitar), `light` (ambient minimal), and `composed` (procedural harmonic ambient pad).
  - **Zero Cartoon Comedy**: Wacky cartoon/meme tracks banished from rotation.
  - **Seamless 2.5s Crossfade Looping**: Eliminates harsh cuts or glitches across 10-minute videos. Ducked to **-29.0 dB** behind narration.
- **🖼️ Mandatory 1920x1080 YouTube Thumbnail**:
  - Automatically generates an eye-catching, high-CTR 16:9 widescreen thumbnail featuring the uppercase topic title, crimson red hook badge, and expressive editorial stick-figure illustration (`<slug>-thumbnail.png`).
  - Recorded in `<slug>-metadata.json` and `completed_topics.json`. Dedicated CLI command: `python tools/cli.py thumbnail <slug>`.
- **🎁 Automatic Companion Short**: Producing a 10-minute long-form video automatically renders an accompanying **1080×1920 (`9:16`)** Short (`out/<slug>-short.mp4`) from the opening hook with synced subtitles.
- **📝 Social Captions + Exactly 5 Hashtags**: Every generated video automatically produces an engaging caption accompanied by exactly 5 targeted hashtags (`<slug>-caption.txt`).
- **🧹 Zero-Clutter Auto-Cleanup**: The directory where the agent is run is where deliverables are saved. All intermediate scratch files (`build/`, `voice/`, `images/`, `out_frames/`, raw WAVs) are automatically deleted upon completion.
- **🎙️ Dual Audio Engine**: Natural conversational TTS voiceover combined with ducked background music (-29 dB) and mastered to -14.0 LUFS.

---

## 📂 Architecture & Directory Layout

```
Stickman-Generator-Skill/
├── SKILL.md                          # Primary agent skill instructions & rules
├── README.md                         # Public documentation & setup guide
├── requirements.txt                  # Python dependencies
├── package.json                      # Node metadata & scripts
├── prompts/                          # User-editable prompts & styling
│   ├── topic_prompt.md               # Topic discovery & psychological angle
│   ├── script_prompt.md              # 1-minute short script formula (Mandatory Imagine hook)
│   ├── script_long_prompt.md         # 10-minute long-form script formula (7 acts)
│   ├── storyboard_prompt.md          # Short slide breakdown (mostly ~3s, sometimes ~2s)
│   ├── storyboard_long_prompt.md     # Long slide breakdown (~130 slides, multi-phase pacing)
│   ├── image_prompt_template.md      # Flow prompt formula (1080x1920 & 1920x1024)
│   └── style_presets.json            # Style presets with rich 2D background details
├── engine/
│   └── slideshow.js                  # Browser 60fps rendering engine + word-synced subtitles
├── tools/                            # Production toolchain
│   ├── cli.py                        # Unified zero-input command-line interface
│   ├── images_util.py                # Exact dimension enforcer (1080x1920 & 1920x1024)
│   ├── metadata.py                   # Caption + 5 hashtags generator
│   ├── thumbnail.py                  # 1920x1080 High-CTR YouTube Thumbnail generator
│   ├── cleanup.py                    # Automatic scratch file cleanup utility
│   ├── check.py                      # Pacing validation (mostly ~3s, sometimes ~2s)
│   ├── extract_short.py              # Automatic companion short generator (1080x1920, 9:16)
│   ├── prompts.py                    # Slide prompt compiler (1920x1024, 1080x1920 & thumbnail)
│   ├── voice.py                      # TTS generator with retry & Whisper word-clock alignment
│   ├── mix.py                        # Sophisticated music selection & crossfade looping (-29dB)
│   ├── build.py                      # HTML web player generator (subtitles + cream fill)
│   ├── render.py                     # Parallel Playwright frame capturer + FFmpeg
│   └── topics.py                     # Catchiest-topic selector & deduplication manager
├── topics/
│   ├── example_topics.json           # Queue of viral ideas waiting to be made
│   ├── completed_topics.json         # Permanent ledger of finished videos & tracks used
│   └── README.md                     # Topic management guide
├── audio/
│   └── music/                        # Curated royalty-free music library (12 tracks)
│       ├── music_catalog.json        # Mood tags & track definitions
│       └── *.mp3                     # Instrumental audio tracks
├── templates/
│   └── film.json                     # Project manifest template
└── examples/                         # Verified reference outputs
    └── sunk-cost-fallacy/            # Canonical project reference
```

---

## 🚀 Complete Installation & Setup Guide

### 1. Prerequisites

Ensure the following tools are installed on your system:
- **Git**
- **Python 3.10 or higher**
- **Node.js 18.0 or higher**
- **FFmpeg** installed and available in your system `PATH`:
  - **Windows**: `winget install Gyan.FFmpeg` (then restart your terminal)
  - **macOS**: `brew install ffmpeg`
  - **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install ffmpeg`
- **Google Flow MCP** (`flow-mcp`) configured and signed in to Google Flow (for AI comic artwork via `flow_agent_images`).

---

### 2. Clone & Install as an Antigravity Skill

Install globally so the skill is available in **any project or directory**:

#### Windows (PowerShell)
```powershell
git clone https://github.com/Blackhawkup/Stickman-Generator-Skill.git "$env:USERPROFILE\.gemini\config\skills\stickman-generator"
cd "$env:USERPROFILE\.gemini\config\skills\stickman-generator"
```

#### macOS / Linux
```bash
git clone https://github.com/Blackhawkup/Stickman-Generator-Skill.git ~/.gemini/config/skills/stickman-generator
cd ~/.gemini/config/skills/stickman-generator
```

*(Optional workspace-only install: clone into `<your-workspace>/.agents/skills/stickman-generator` instead.)*

---

### 3. Install Python Dependencies & Chromium

Inside the cloned skill folder, create/activate a virtual environment (recommended) and install dependencies:

#### Windows (PowerShell)
```powershell
python -m venv "$env:USERPROFILE\WhiteboardFilms\.tools\venv"
& "$env:USERPROFILE\WhiteboardFilms\.tools\venv\Scripts\python.exe" -m pip install -r requirements.txt
& "$env:USERPROFILE\WhiteboardFilms\.tools\venv\Scripts\playwright.exe" install chromium
```

#### macOS / Linux
```bash
python3 -m venv ~/WhiteboardFilms/.tools/venv
source ~/WhiteboardFilms/.tools/venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

*(Note: `tools/cli.py` automatically detects `~/WhiteboardFilms/.tools/venv` whenever invoked with system `python`. You can override that path with `WHITEBOARD_HOME` or install `requirements.txt` into your active environment directly.)*

---

### 4. Configure Gemini TTS Key & Google Flow

1. **Gemini API Key (for Voice Narration TTS)**:
   - Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).
   - Set it as an environment variable `GEMINI_API_KEY`:
     - **Windows**: `setx GEMINI_API_KEY "your_api_key_here"`
     - **macOS/Linux**: `export GEMINI_API_KEY="your_api_key_here"` (add to `~/.zshrc` or `~/.bashrc`)
   - *Or* save the key directly in `~/.flow-mcp/gemini-key` (Windows: `%USERPROFILE%\.flow-mcp\gemini-key`).
2. **Google Flow Artwork (`flow-mcp`)**:
   - Ensure your `flow-mcp` Chrome window is running and signed in to Google Flow.
   - `tools/generate_all_slides.mjs` automatically looks for `~/flow-mcp/dist/flow.js` (or set `FLOW_MCP_PATH` to point to `flow.js`).
   - When running via Antigravity, the agent can also invoke the `flow_agent_images` MCP tool directly.

---

## ▶️ How to Run It

### Option A: Zero-Input Autonomous Mode (Recommended — Inside Antigravity)

Open any empty or target output folder in Antigravity and simply prompt:

* **To make a 1-Minute Vertical Short (`1080x1920`, `9:16`)**:
  > *"Generate a stickman short video"*
* **To make a 10-Minute Long-Form Video (`1920x1080` video, `1920x1024` slides, + companion short + thumbnail)**:
  > *"Generate a 10 minute long-form stickman video"*
* **To request a specific topic**:
  > *"Make a short on The Spotlight Effect"* or *"Make a long-form video on Parkinson's Law"*

**Zero user input is required after your prompt.** The agent will automatically:
1. Score and pick the catchiest unproduced topic from `topics/example_topics.json` (verifying zero repeats against `topics/completed_topics.json`).
2. Write the script (`Name First -> Imagine...`) and paced storyboard (`slides.json`).
3. Generate TTS voice narration + Faster-Whisper word-level timestamps.
4. Generate editorial stickman artwork via Flow and enforce exact `1080x1920` (short) or `1920x1024` (long) dimensions.
5. Select aesthetic ambient background music, apply a 2.5s crossfade loop, and mix audio (`-14.0 LUFS` voice / `-29.0 dB` music).
6. Render 60fps MP4(s) with **always-on synced word-highlighted subtitles**.
7. Extract the companion `1080x1920` vertical Short and render the `1920x1080` YouTube thumbnail (for long-form).
8. Generate `<slug>-caption.txt` (caption + 5 hashtags), update `completed_topics.json`, and **delete all scratch folders**.

### Option B: CLI Quick Reference (Manual / Scripted Runs)

```bash
# 1. Auto-pick the catchiest uncompleted topic & create a Short (1080x1920, 9:16)
python tools/cli.py new --mode short

# 2. Auto-pick the catchiest uncompleted topic & create a Long-Form project (1920x1024 images, 1920x1080 video)
python tools/cli.py new --mode long

# (Or provide an explicit slug: python tools/cli.py new my-topic --mode short)

# 3. Compile prompts (1920x1024 16:9 + thumbnail + 1080x1920 companion short for long; 1080x1920 9:16 for short)
python tools/cli.py prompts <slug>

# 4. Generate TTS voiceover and Whisper word timestamps (powers word-highlighted subtitles)
python tools/cli.py tts <slug> --voice Charon

# 5. Validate timing & pacing rules (mostly ~3s, sometimes ~2s)
python tools/cli.py check <slug>

# 6. Generate dedicated 1920x1080 YouTube Thumbnail (for long-form videos)
python tools/cli.py thumbnail <slug>

# 7. 1-Command Autonomous Production
# - Normalizes image resolutions (1080x1920 short / 1920x1024 long)
# - Renders subtitled primary video + subtitled companion short (if long) + thumbnail (if long)
# - Selects aesthetic lo-fi / ambient documentary soundtrack & crossfades
# - Generates social caption + 5 hashtags
# - Cleans up all intermediate scratch files automatically
# - Updates topics/completed_topics.json
python tools/cli.py auto <slug>
```

---

## 🎯 Topic Deduplication System

- **Inspect Next Topic**:
  ```bash
  python tools/cli.py topics next
  ```
- **List All Candidate Topics**:
  ```bash
  python tools/cli.py topics list
  ```
- **Inspect Completed Production Ledger**:
  ```bash
  python tools/cli.py topics completed
  ```
- **Add Your Own Topic**:
  ```bash
  python tools/topics.py add "The Pygmalion Effect" --category "Social Psychology" --scenario "Higher expectations lead to an increase in performance"
  ```
