# Stickman Explainer Video Generator Skill

An autonomous, high-retention video production skill that creates 1-minute vertical explainer slideshow shorts (1080x1920, 60fps) pairing editorial stick-figure illustrations with synchronized voice narration and ducked royalty-free background music.

Designed for AI agent environments (Antigravity, Claude Code) as well as developer CLI workflows.

---

## ⚡ Key Highlights

- **⚡ 1-Command Autonomous Production**: Generates full script, storyboard, AI art prompts, TTS audio, Whisper word clocks, ducked music mix, and 60fps video rendering end-to-end.
- **🎨 Editorial Webcomic Visual DNA**: Minimalist round heads, expressive dot eyes/brows, bean torsos, clean stick limbs, solid bold primary color accents, warm off-white cream background (#F6F4EC), top headline titles, and bottom captions.
- **⏱️ Strict Retention Pacing Guardrails**: Enforces slide transitions every **2.0 to 4.0 seconds** (never exceeding 4.0s). For a 60–80 second short, 25 to 30 slides are timed to precise word triggers.
- **🎙️ Dual Audio Engine**: Natural conversational TTS voiceover (Gemini Studio TTS or custom audio) combined with ducked background music (-26 dB) and mastered to -14.0 LUFS.
- **🧠 Zero-Duplicate Topic Management**: Built-in queue (	opics/example_topics.json) and completed registry (	opics/completed_topics.json) to guarantee topics are never repeated.
- **🖼️ Google Flow MCP Ready**: Pre-formatted image prompt builder tailored for Google Flow (low_agent_images).

---

## 📂 Architecture & Directory Layout

`
Stickman-Generator-Skill/
├── SKILL.md                          # Primary agent skill instructions & rules
├── README.md                         # Public documentation & setup guide
├── requirements.txt                  # Python dependencies
├── package.json                      # Node metadata & scripts
├── prompts/                          # User-editable prompts & styling
│   ├── topic_prompt.md               # Topic discovery & psychological angle
│   ├── script_prompt.md              # 10-step spoken narration script formula
│   ├── storyboard_prompt.md          # Visual scene & trigger phrase breakdown
│   ├── image_prompt_template.md      # Flow prompt formula & composition rules
│   └── style_presets.json            # Style presets (editorial webcomic)
├── engine/
│   └── slideshow.js                  # Browser 60fps rendering engine
├── tools/                            # Production toolchain
│   ├── cli.py                        # Unified command-line interface
│   ├── topics.py                     # Topic queue & deduplication manager
│   ├── prompts.py                    # Slide prompt compiler
│   ├── flow_driver.py                # Google Flow MCP execution helper
│   ├── voice.py                      # TTS generator & Whisper word-clock alignment
│   ├── mix.py                        # Audio ducking (-26dB) & LUFS mastering
│   ├── build.py                      # HTML web player generator
│   ├── check.py                      # Pacing validation & trigger audit
│   └── render.py                     # Parallel Playwright frame capturer + FFmpeg
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
`

---

## 🚀 Quickstart & Prerequisites

### 1. Requirements

- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **FFmpeg**: Installed and accessible in your system PATH
- **Google Flow MCP**: Configured in your agent environment (for low_agent_images)

### 2. Install Dependencies

`ash
# Python dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium
`

---

## 🤖 Using as an AI Agent Skill

This repository adheres to the standard Agent Skill specification (SKILL.md).

### Install into Antigravity or Claude Code:
Copy or link this folder into your skills directory:
`ash
# Antigravity
cp -r Stickman-Generator-Skill ~/.gemini/config/skills/stickman-generator

# Claude Code
cp -r Stickman-Generator-Skill ~/.claude/skills/stickman-generator
`

### Agent Trigger Phrases:
- *"generate a clip"* — Automatically picks the next unproduced topic from 	opics/example_topics.json, scripts it, storyboards 25–30 slides with <= 4.0s pacing, generates images, mixes ducked audio, renders the 60fps video, and logs the completion.
- *"generate a clip on [Topic]"* — Generates a video on a specific topic.

---

## 🛠️ CLI Quick Reference

`ash
# 1. Fetch next available topic from queue
python tools/cli.py topics next

# 2. Initialize a new project directory
python tools/cli.py new my-topic --format 9:16

# 3. Generate speech audio & Whisper word timestamps
python tools/cli.py tts my-topic --voice Charon

# 4. Compile image prompts for Google Flow
python tools/cli.py prompts my-topic

# 5. Mix ducked background music with voiceover
python tools/cli.py mix my-topic --music audio/music/curious.mp3

# 6. Build interactive HTML player
python tools/cli.py build my-topic

# 7. Validate timing & strict <= 4.0s pacing rule
python tools/cli.py check my-topic

# 8. Render production 60fps MP4 video
python tools/cli.py render my-topic --fps 60

# 9. One-command automated production pipeline
python tools/cli.py auto my-topic --voice Charon --music curious.mp3
`

---

## 🎨 Visual DNA Guide

Every slide image generated follows the **Editorial Webcomic** aesthetic:
- **Head**: Large, smooth white circle with dot eyes and expressive minimal eyebrows/mouth.
- **Torso**: Bean/pear-shaped torso wearing plain white or a bold solid primary accent shirt (red, yellow, green, or blue).
- **Limbs**: Thin uniform black ink stick arms and legs with small oval hands/feet.
- **Canvas**: Warm off-white cream background (#F6F4EC / #FBF6EF).
- **Composition**: Centered subject in middle 60%, leaving clean top margin for title overlay and bottom margin for captions.
- **No Artifacts**: Crisp clean 2D outlines, flat cel colors, soft gray ground oval shadow, zero 3D shading, zero gradients, zero unwanted text.

---

## 📄 License

MIT License. Free for personal and commercial content creation.
