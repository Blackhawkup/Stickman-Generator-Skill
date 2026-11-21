# Stickman Explainer Video Generator Skill

An autonomous, high-retention video production skill that creates both **Phone/Reel Shorts (720x1600)** and **Laptop/Long-Form videos (1920x1080)** at 60 FPS, pairing editorial stick-figure illustrations with rich 2D background details, synchronized voice narration, and ducked royalty-free background music.

Designed to run in any directory, generating finished deliverables (videos, social captions with 5 hashtags, and 1920x1080 thumbnails) while automatically purging intermediate scratch files.

---

## ⚡ Key Highlights

- **⚡ Dual Video Formats**:
  - **Phone / Short / Reel (720 x 1600)**: Centered artwork with matching warm cream (`#FBF6EF`) background fill. Zero black bars.
  - **Laptop / Long-Form (1920 x 1080)**: 16:9 widescreen cinematic framing with rich 2D environmental details.
- **⏱️ High-Retention 1st Minute Pacing**:
  - In the 1st minute (both short and long), every image stays on screen for **less than 3 seconds** (`< 3.0s`), averaging **~2.0 seconds** (~30 slides per minute).
  - In long-form after 2 minutes, slides are allowed to stay on screen for **5.0 to 6.0 seconds** for deep exposition.
- **🎨 Rich 2D Background Details**:
  - In addition to the signature stick figures, backgrounds feature stylized, charming 2D environmental elements: mid-century bookshelves, framed wall art, modern potted plants, stylish floor lamps, cozy desks, office whiteboards, and subtle city skylines in fine ink lines with muted earthy neutrals.
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
│   ├── script_prompt.md              # 1-minute short script formula
│   ├── script_long_prompt.md         # 10-minute long-form script formula (7 acts)
│   ├── storyboard_prompt.md          # Short slide breakdown (< 3s pacing, ~2s avg)
│   ├── storyboard_long_prompt.md     # Long slide breakdown (~130 slides, multi-phase pacing)
│   ├── image_prompt_template.md      # Flow prompt formula (720x1600 & 1920x1080)
│   └── style_presets.json            # Style presets with rich 2D background details
├── engine/
│   └── slideshow.js                  # Browser 60fps rendering engine (centered + cream fill)
├── tools/                            # Production toolchain
│   ├── cli.py                        # Unified command-line interface
│   ├── metadata.py                   # Caption + 5 hashtags generator
│   ├── cleanup.py                    # Automatic scratch file cleanup utility
│   ├── check.py                      # Pacing validation (< 3s in 1st min, ~2s avg)
│   ├── extract_short.py              # Automatic companion short generator (720x1600)
│   ├── prompts.py                    # Slide prompt compiler (1920x1080, 720x1600 & thumbnail)
│   ├── voice.py                      # TTS generator & Whisper word-clock alignment
│   ├── mix.py                        # Audio ducking (-26dB) & LUFS mastering
│   ├── build.py                      # HTML web player generator
│   ├── render.py                     # Parallel Playwright frame capturer + FFmpeg
│   └── topics.py                     # Topic queue & deduplication manager
├── topics/
│   ├── example_topics.json           # Queue of viral ideas waiting to be made
│   ├── completed_topics.json         # Permanent ledger of finished videos
│   └── README.md                     # Topic management guide
├── audio/
│   └── music/                        # Curated royalty-free music library
│       ├── music_catalog.json        # Mood tags & track definitions
│       └── *.mp3                     # Instrumental audio tracks
├── templates/
│   └── film.json                     # Project manifest template
└── examples/                         # Verified reference outputs
    └── sunk-cost-fallacy/            # Canonical 30-slide 60fps project
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

# 3. Generate speech audio & Whisper word timestamps
python tools/cli.py tts my-deepdive --voice Charon

# 4. Compile prompts (1920x1080 + thumbnail for long, 720x1600 for short)
python tools/cli.py prompts my-deepdive

# 5. Generate / view caption + 5 hashtags
python tools/cli.py caption my-deepdive

# 6. Validate timing & pacing rules (< 3s in 1st min, ~2s avg)
python tools/cli.py check my-deepdive

# 7. One-command automated production pipeline
#    - Produces primary video + companion short (if long) + thumbnail (if long)
#    - Generates caption + 5 hashtags
#    - Automatically purges all intermediate scratch files
#    - Updates topics/completed_topics.json
python tools/cli.py auto my-deepdive --voice Charon
```

---

## 📄 License

MIT License. Free for personal and commercial content creation.
