# Stickman Explainer Video Generator Skill

An autonomous, high-retention video production skill that creates both **1-minute vertical Shorts (1080x1920)** and **10-minute horizontal explainer videos (1920x1080)** at 60 FPS, pairing editorial stick-figure illustrations with synchronized voice narration and ducked royalty-free background music.

Designed to run in any directory, generating finished deliverables (videos, social captions with 5 hashtags, and 16:9 thumbnails) while automatically purging intermediate scratch files.

---

## ⚡ Key Highlights

- **⚡ Dual Video Modes**:
  - **Short Mode (9:16, 1080x1920)**: High-velocity 1-minute explainer shorts with slide transitions every 2.0 to 4.0 seconds.
  - **Long-Form Mode (16:9, 1920x1080)**: Comprehensive 10-minute deep dives with dual-phase pacing and real-world case studies.
- **🎁 Automatic Companion Short**: Producing a 10-minute long-form video automatically renders an accompanying 1-minute 9:16 Short (`out/<slug>-short.mp4`) from the opening hook in the same run.
- **🖼️ 16:9 YouTube Thumbnail**: Automatically generates a high-CTR, dramatic widescreen thumbnail featuring the topic name in the exact same editorial stick-figure webcomic art style.
- **📝 Social Captions + Exactly 5 Hashtags**: Every generated video automatically produces an engaging, curiosity-driven caption accompanied by exactly 5 targeted hashtags (`<slug>-caption.txt`).
- **🧹 Zero-Clutter Auto-Cleanup**: The directory where the agent is run is where deliverables are saved. All intermediate scratch files (`build/`, `voice/`, `images/`, `out_frames/`, raw WAVs) are automatically deleted upon completion, leaving only clean finished deliverables.
- **🎨 Editorial Webcomic Visual DNA**: Minimalist round heads, expressive dot eyes/brows, bean torsos, clean stick limbs, solid bold primary color accents (red, yellow, green, blue), warm off-white cream background (`#FBF6EF`), top headline titles, and bottom captions.
- **⏱️ Retention Pacing Guardrails**:
  - *Short*: All slides strictly **2.0s to 4.0s** (hard cap at 4.0s).
  - *Long-Form*: First 2 minutes strictly **2.0s to 4.0s** (fast visual hook); after 2 minutes, slides are allowed to stay on screen for **5.0 to 6.0 seconds** (hard cap at 6.0s).
- **🎙️ Dual Audio Engine**: Natural conversational TTS voiceover (Gemini Studio TTS or custom audio) combined with ducked background music (-26 dB) and mastered to -14.0 LUFS.
- **🧠 Zero-Duplicate Topic Management**: Built-in queue (`topics/example_topics.json`) and completed registry (`topics/completed_topics.json`).

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
│   ├── storyboard_prompt.md          # Short slide breakdown (25-30 slides)
│   ├── storyboard_long_prompt.md     # Long slide breakdown (~120 slides, dual pacing)
│   ├── image_prompt_template.md      # Flow prompt formula (1:1 and 16:9)
│   └── style_presets.json            # Style presets (editorial webcomic)
├── engine/
│   └── slideshow.js                  # Browser 60fps rendering engine
├── tools/                            # Production toolchain
│   ├── cli.py                        # Unified command-line interface
│   ├── metadata.py                   # Caption + 5 hashtags generator
│   ├── cleanup.py                    # Automatic scratch file cleanup utility
│   ├── check.py                      # Pacing validation (dual-phase rules)
│   ├── extract_short.py              # Automatic companion short generator
│   ├── prompts.py                    # Slide prompt compiler (1:1, 16:9 & thumbnail)
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
# 1. Create a 1-minute Short project
python tools/cli.py new my-short --mode short

# 2. Create a 10-minute Long-Form project
python tools/cli.py new my-deepdive --mode long

# 3. Generate speech audio & Whisper word timestamps
python tools/cli.py tts my-deepdive --voice Charon

# 4. Compile prompts (16:9 + thumbnail for long, 1:1 for short)
python tools/cli.py prompts my-deepdive

# 5. Generate / view caption + 5 hashtags
python tools/cli.py caption my-deepdive

# 6. Validate timing & dual-phase pacing rules
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
