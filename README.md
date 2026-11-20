# Stickman Explainer Video Generator Skill

An autonomous, high-retention video production skill that creates both **1-minute vertical Shorts (1080x1920)** and **10-minute horizontal explainer videos (1920x1080)** at 60 FPS, pairing editorial stick-figure illustrations with synchronized voice narration and ducked royalty-free background music.

When generating a 10-minute long-form video, the pipeline **automatically extracts and renders an autonomous 1-minute vertical Short** from the opening hook!

---

## ⚡ Key Highlights

- **⚡ Dual Video Modes**:
  - **Short Mode (9:16, 1080x1920)**: High-velocity 1-minute explainer shorts with slide changes every 2.0 to 4.0 seconds.
  - **Long-Form Mode (16:9, 1920x1080)**: Comprehensive 10-minute deep dives with dual-phase pacing and real-world case studies.
- **🎁 Automatic Companion Short**: Producing a 10-minute long-form video automatically renders an accompanying 1-minute 9:16 Short (`out/<slug>-short.mp4`) in the same run.
- **🎨 Editorial Webcomic Visual DNA**: Minimalist round heads, expressive dot eyes/brows, bean torsos, clean stick limbs, solid bold primary color accents (red, yellow, green, blue), warm off-white cream background (`#FBF6EF`), top headline titles, and bottom captions.
- **⏱️ Retention Pacing Guardrails**:
  - *Short*: All slides strictly **2.0s to 4.0s** (hard cap at 4.0s).
  - *Long-Form*: First 2 minutes strictly **2.0s to 4.0s** (fast visual hook); after 2 minutes, slides are allowed to stay on screen for **5.0 to 6.0 seconds** (hard cap at 6.0s).
- **🎙️ Dual Audio Engine**: Natural conversational TTS voiceover (Gemini Studio TTS or custom audio) combined with ducked background music (-26 dB) and mastered to -14.0 LUFS.
- **🧠 Zero-Duplicate Topic Management**: Built-in queue (`topics/example_topics.json`) and completed registry (`topics/completed_topics.json`).
- **🖼️ Google Flow MCP Ready**: Builds tailored image prompts for 1:1 square canvas (Shorts) and 16:9 widescreen canvas (Long-form).

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
│   ├── check.py                      # Pacing validation (dual-phase rules)
│   ├── extract_short.py              # Automatic companion short generator
│   ├── prompts.py                    # Slide prompt compiler (1:1 & 16:9)
│   ├── voice.py                      # TTS generator & Whisper word-clock alignment
│   ├── mix.py                        # Audio ducking (-26dB) & LUFS mastering
│   ├── build.py                      # HTML web player generator
│   ├── render.py                     # Parallel Playwright frame capturer + FFmpeg
│   ├── flow_driver.py                # Google Flow MCP execution helper
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
├── examples/                         # Verified reference outputs
│   └── sunk-cost-fallacy/            # Canonical 30-slide 60fps project
└── projects/                         # Active working directory for new shorts
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
# 1. Create a 1-minute Short project (9:16 vertical)
python tools/cli.py new my-short --mode short

# 2. Create a 10-minute Long-Form project (16:9 widescreen)
python tools/cli.py new my-deepdive --mode long

# 3. Generate speech audio & Whisper word timestamps
python tools/cli.py tts my-deepdive --voice Charon

# 4. Compile image prompts for Google Flow (16:9 for long, 1:1 for short)
python tools/cli.py prompts my-deepdive

# 5. Mix ducked background music with voiceover
python tools/cli.py mix my-deepdive --music audio/music/curious.mp3

# 6. Validate timing & dual-phase pacing rules
#    (<= 4.0s in first 2 mins, <= 6.0s after 2 mins)
python tools/cli.py check my-deepdive

# 7. One-command automated production pipeline
#    When run on a long-form project, it produces BOTH:
#    - out/<slug>-long.mp4 (1920x1080, 16:9, ~10m)
#    - out/<slug>-short.mp4 (1080x1920, 9:16, ~1m)
python tools/cli.py auto my-deepdive --voice Charon
```

---

## 📜 10-Minute Long-Form Script Arc

When producing a 10-minute video, the script follows this 7-part architecture:
1. **0:00 – 1:00 (The Viral Hook Short)**: Title Card + *"Imagine..."* everyday scenario. Engineered to stand alone as the companion Short.
2. **1:00 – 2:00 (The Bridge to Depth)**: Escalation from personal choice to corporate/societal stakes + thesis roadmap. Pacing remains fast (<= 4.0s).
3. **2:00 – 4:00 (The Science & Origin)**: The researchers, experimental methodology, and counter-intuitive data. (Pacing relaxed to 4–6s).
4. **4:00 – 6:30 (Real-World Case Studies)**: Deep dive into 2–3 historical blunders (e.g. Concorde fallacy, Kodak, mountaineering).
5. **6:30 – 8:30 (Everyday Modern Traps)**: Career, relationship, and financial subscription traps.
6. **8:30 – 9:30 (Actionable Mental Models)**: Clean Slate / Stranger Test, Zero-Based Thinking, exit rules.
7. **9:30 – 10:00 (Philosophical Synthesis)**: Final takeaway and memorable closing punchline.

---

## 📄 License

MIT License. Free for personal and commercial content creation.
