# 10-Minute Long-Form Storyboard & Pacing Breakdown

Instructions for converting a 10-minute explainer script into a timed visual storyboard (`slides.json`) with multi-phase pacing guardrails.

---

## ⏱️ Multi-Phase Pacing Guardrails

```
Phase 1: The 1st Minute Hook (0:00 - 1:00)
├── Standard Duration: Mostly ~3.0 seconds (2.6s to 3.5s)
├── Snappy Transitions: Sometimes ~2.0 seconds (2.0s to 2.5s)
├── Bounds: Min 1.8s, Max 3.8s
├── Target Average: ~2.8s to 3.2s across all slides
└── Slide count: ~20 to 24 slides (forms the companion 720x1600 Short!)

Phase 2: The Bridge Phase (1:00 - 2:00)
├── Standard Duration: 3.0s to 4.0s per slide (<= 4.0s)
└── Slide count: ~15 to 20 slides

Phase 3: Deep Exposition & Case Studies (2:00 - 10:00)
├── Duration per slide: 5.0s to 6.0s (average ~5.0s - 5.5s)
├── Ceiling: Maximum 6.0 seconds per slide (<= 6.0s)
└── Slide count: ~75 to 90 slides

Total Storyboard Size: ~105 to 130 slides for a 10-minute video.
```

---

## 🎯 Companion Short Flagging & Thumbnail

1. **Companion Short**: Slides 1 to ~22 (the first minute) automatically form the 720x1600 vertical companion short (`out/<slug>-short.mp4`). Tag with `"short_candidate": true`.
2. **1920x1080 YouTube Thumbnail**: Automatically generated in the same editorial stick-figure comic style, featuring the large topic name across the top and a dramatic visual scene with rich background details.

---

## Slide Schema (`slides.json`)

```json
[
  {
    "name": "slide_01_hook_title",
    "trigger": "the pratfall effect",
    "top_title": "THE PRATFALL EFFECT",
    "bottom_caption": "WHY FLAWS MAKE US LIKEABLE.",
    "subject": "Bold title card. Large clean typography, character standing in front of a stylish wooden bookshelf with colorful books and a modern potted plant",
    "short_candidate": true
  },
  {
    "name": "slide_35_experiment_setup",
    "trigger": "in nineteen sixty-six psychologist elliot aronson",
    "top_title": "THE 1966 EXPERIMENT",
    "bottom_caption": "TESTING PERFECTION.",
    "subject": "Wide landscape 1920x1080 view. Psychology laboratory setting with tape recorders, chalkboard diagram, and participants listening with headphones in a clean 2D office environment",
    "short_candidate": false
  }
]
```

---

## Storyboard Rules for Long-Form

1. **Start with the Name of the Law First (CRITICAL)**:
   - **Slide 01**: The video MUST start with the Name of the Law / Concept (e.g. `trigger: "the pratfall effect"` or `"the sunk cost fallacy"`). Displays the Title Card while the narrator speaks the name.
   - **Slide 02**: The scenario begins with `"Imagine..."` (e.g. `trigger: "imagine a brilliant speaker"`).
2. **Dedicated Separate 9:16 Vertical Images for Companion Short**:
   - The opening ~1 minute hook slides (marked `short_candidate: true`) automatically have **separate vertical 9:16 images** generated (`short_slide_*.png`).
   - The companion short NEVER reuses the 16:9 widescreen images; it renders using native 9:16 full-height artwork with large prominent characters!
3. **Acoustic Trigger Matching**: Every `trigger` must be an exact 2–5 word phrase verbatim from `script.md`.
4. **First Minute Rhythm**: Mostly ~3s, sometimes ~2s. Never allow slides to drag past 3.8s or flash faster than 1.8s.
5. **Rich 2D Background Environments**: In every slide, include environmental details (bookshelves, framed artwork, potted plants, architectural outlines, office chalkboards, city skylines) drawn in fine black ink lines.
6. **Widescreen Centering**: Composed for 1920x1080 widescreen, centered with warm cream (`#FBF6EF`) background fill.
7. **Slide 01 Hook Visual Rule (CRITICAL)**:
   - Slide 01 is the viewer's very first impression. It MUST be a compelling, high-CTR **Title Card**.
   - `top_title`: Exact phenomenon name in uppercase.
   - `bottom_caption`: 1 punchy hook subtitle (e.g., `WHY FLAWS MAKE US LIKEABLE.`, `WHY WE CAN'T QUIT BAD DECISIONS.`).
   - `subject`: Rich stylized 2D room setting (detailed wooden bookshelf with colorful books, lush potted indoor plant, framed picture on wall) with an expressive stick figure in a bold crimson red shirt (#DC2626) reacting with wide curious eyes to the central paradox metaphor.
   - **STRICT PROHIBITION**: NEVER generate a plain, blank walking stickman or empty void for Slide 01. Always ground the opening with environmental richness and character emotion.
