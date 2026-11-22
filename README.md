# Stickman Explainer Video Generator Skill

An autonomous, high-retention video production skill that creates both **Phone/Reel Shorts (720x1600)** and **Laptop/Long-Form videos (1920x1080)** at 60 FPS, pairing editorial stick-figure illustrations with rich 2D background details, synchronized voice narration, and ducked royalty-free background music.

Designed to run in any directory, generating finished deliverables (videos, social captions with 5 hashtags, and 1920x1080 thumbnails) while automatically purging intermediate scratch files.

---

## ⚡ Key Highlights

- **⚡ Dual Video Formats & Dedicated Separate Short Images**:
  - **Phone / Short / Reel (720 x 1600)**: Native **9:16 vertical full-height artwork** with large, prominent characters filling the mobile canvas. Zero small images, zero black bars.
  - **Laptop / Long-Form (1920 x 1080)**: 16:9 widescreen cinematic framing with rich 2D environmental details.
  - **Separate Short Images**: In long-form projects, the companion short **generates its own dedicated 9:16 vertical images** (`short_slide_*.png`), never reusing or letterboxing 16:9 widescreen images!
- **🚨 Mandatory Hook Formula (Name First, Then Imagine)**:
  - **Sentence 1**: Spoken uppercase name of the law/phenomenon (e.g., `THE PRATFALL EFFECT.` or `THE SUNK COST FALLACY.`). The video and narration start with the name!
  - **Sentence 2**: Immediately follows with the scenario starting with `"Imagine a guy..."`, `"Imagine you..."`, or `"Imagine if you..."`.
  - **Negative Constraint**: Zero named fictional characters (banned: *"Leo walked into the office..."*). Never start with "Imagine" before stating the name.
- **⏱️ High-Retention Pacing (Mostly 3s, Sometimes 2s)**:
  - Slides stay on screen for mostly **~3.0 seconds**, dipping to **~2.0 seconds** for fast surprise beats or punchlines (target average ~2.8s–3.2s).
  - In long-form after 2 minutes, slides stay on screen for **5.0 to 6.0 seconds** for deep exposition.
- **🎵 Dynamic Background Music Rotation (12 Tracks)**:
  - Curated library of 12 royalty-free instrumental tracks in `audio/music/` (`curious`, `investigation`, `mystery`, `sneaky`, `playful`, `quirky`, `upbeat`, `reflective`, `deep_mystery`, `thoughtful`, `light`, `comedy`).
  - Automatically matches topic mood and rotates tracks using `topics/completed_topics.json` history to prevent back-to-back repeats.
- **🎨 Rich 2D Background Details**:
  - Backgrounds feature stylized, charming 2D environmental elements: mid-century bookshelves, framed wall art, modern potted plants, stylish floor lamps, cozy desks, office whiteboards, and subtle city skylines in fine ink lines with muted earthy neutrals.
- **🖼️ 1920x1080 YouTube Thumbnail**: Automatically generates a high-CTR, dramatic widescreen thumbnail featuring the topic name in the exact same editorial stick-figure webcomic art style.
- **🎁 Automatic Companion Short**: Producing a 10-minute long-form video automatically renders an accompanying 720x1600 Short (`out/<slug>-short.mp4`) from the opening hook.
- **📝 Social Captions + Exactly 5 Hashtags**: Every generated video automatically produces an engaging caption accompanied by exactly 5 targeted hashtags (`<slug>-caption.txt`).
- **🧹 Zero-Clutter Auto-Cleanup**: The directory where the agent is run is where deliverables are saved. All intermediate scratch files (`build/`, `voice/`, `images/`, `out_frames/`, raw WAVs) are automatically deleted upon completion.
- **🎙️ Dual Audio Engine**: Natural conversational TTS voiceover combined with ducked background music (-26 dB) and mastered to -14.0 LUFS.

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
│   ├── image_prompt_template.md      # Flow prompt formula (720x1600 & 1920x1080)
│   └── style_presets.json            # Style presets with rich 2D background details
├── engine/
│   └── slideshow.js                  # Browser 60fps rendering engine (centered + cream fill)
├── tools/                            # Production toolchain
│   ├── cli.py                        # Unified command-line interface
│   ├── metadata.py                   # Caption + 5 hashtags generator
│   ├── cleanup.py                    # Automatic scratch file cleanup utility
│   ├── check.py                      # Pacing validation (mostly ~3s, sometimes ~2s)
│   ├── extract_short.py              # Automatic companion short generator (720x1600)
│   ├── prompts.py                    # Slide prompt compiler (1920x1080, 720x1600 & thumbnail)
│   ├── voice.py                      # TTS generator & Whisper word-clock alignment
│   ├── mix.py                        # Dynamic music rotation across 12 tracks & ducking (-26dB)
│   ├── build.py                      # HTML web player generator (full cream fill, no black bars)
│   ├── render.py                     # Parallel Playwright frame capturer + FFmpeg
│   └── topics.py                     # Topic queue & deduplication manager
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

## 🚀 Quickstart & Prerequisites

### 1. Requirements

- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **FFmpeg**: Installed and accessible in your system PATH
- **Google Flow MCP**: Configured in your agent environment (for `flow_agent_images`)

### 2. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium
```

---

## 🛠️ CLI Quick Reference

```bash
# 1. Create a Phone Short project (720x1600)
python tools/cli.py new my-short --mode short

# 2. Create a Laptop Long-Form project (1920x1080)
python tools/cli.py new my-deepdive --mode long

# 3. Compile prompts (16:9 + thumbnail for long, centered for phone)
python tools/cli.py prompts <slug>

# 4. Generate TTS voiceover and Whisper word timestamps
python tools/cli.py tts <slug> --voice Charon

# 5. Validate timing & pacing rules (mostly ~3s, sometimes ~2s)
python tools/cli.py check <slug>

# 6. 1-Command Autonomous Production
# - Generates primary video + companion short (if long) + thumbnail (if long)
# - Rotates background music dynamically from 12 curated tracks
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
