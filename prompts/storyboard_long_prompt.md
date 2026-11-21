# 10-Minute Long-Form Storyboard & Pacing Breakdown

Instructions for converting a 10-minute explainer script into a timed visual storyboard (`slides.json`) with multi-phase pacing guardrails.

---

## ⏱️ Multi-Phase Pacing Guardrails

```
Phase 1: The 1st Minute Hook (0:00 - 1:00)
├── Ceiling: Every slide must stay on screen for LESS than 3.0 seconds (< 3.0s)
├── Average: ~2.0 seconds on average across all slides
├── Range: 1.2s to 2.8s per slide
└── Slide count: ~28 to 32 slides (forms the companion 720x1600 Short!)

Phase 2: The Bridge Phase (1:00 - 2:00)
├── Ceiling: Maximum 4.0 seconds per slide (<= 4.0s)
├── Average: ~3.0s per slide
└── Slide count: ~18 to 22 slides

Phase 3: Deep Exposition & Case Studies (2:00 - 10:00)
├── Duration per slide: 5.0s to 6.0s (average ~4.8s - 5.5s)
├── Ceiling: Maximum 6.0 seconds per slide (<= 6.0s)
└── Slide count: ~80 to 95 slides

Total Storyboard Size: ~125 to 150 slides for a 10-minute video.
```

---

## 🎯 Companion Short Flagging & Thumbnail

1. **Companion Short**: Slides 1 to ~30 (the first minute) automatically form the 720x1600 vertical companion short (`out/<slug>-short.mp4`). Tag with `"short_candidate": true`.
2. **1920x1080 YouTube Thumbnail**: Automatically generated in the same editorial stick-figure comic style, featuring the large topic name across the top and a dramatic visual scene with rich background details.

---

## Slide Schema (`slides.json`)

```json
[
  {
    "name": "slide_01_hook_title",
    "trigger": "the sunk cost fallacy",
    "top_title": "THE SUNK COST FALLACY",
    "bottom_caption": "WHY WE CAN'T LET GO.",
    "subject": "Bold title card. Large clean typography, character standing in front of a stylish wooden bookshelf with colorful books and a modern potted plant",
    "short_candidate": true
  },
  {
    "name": "slide_35_concorde_project",
    "trigger": "the supersonic concorde airliner",
    "top_title": "THE CONCORDE DISASTER",
    "bottom_caption": "BILLIONS IN THE SKY.",
    "subject": "Wide landscape 1920x1080 view. Two government officials in black suits standing on an airstrip looking at a sleek supersonic passenger jet, airport hangar and control tower in the background, stacks of cash flying into the jet engine",
    "short_candidate": false
  }
]
```

---

## Storyboard Rules for Long-Form

1. **Acoustic Trigger Matching**: Every `trigger` must be an exact 2–5 word phrase verbatim from `script.md`.
2. **First Minute Velocity**: Keep transitions fast (`< 3.0s`, avg `~2.0s`) during the initial 60 seconds to lock in audience retention.
3. **Rich 2D Background Environments**: In every slide, include environmental details (bookshelves, framed artwork, potted plants, architectural outlines, office chalkboards, city skylines) drawn in fine black ink lines.
4. **Widescreen Centering**: Composed for 1920x1080, centered with warm cream (`#FBF6EF`) background fill.
