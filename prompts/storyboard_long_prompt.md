# 10-Minute Long-Form Storyboard & Pacing Breakdown

Instructions for converting a 10-minute explainer script into a timed visual storyboard (`slides.json`) with dual-phase pacing guardrails.

---

## ⏱️ Dual-Phase Pacing Guardrails

```
Phase 1: High-Retention Hook Window (0:00 - 2:00)
├── Duration per slide: Strictly 2.0s to 4.0s (average ~2.8s)
├── Maximum ceiling: 4.0 seconds (hard cap)
└── Slide count: ~30 to 35 slides

Phase 2: Deep Exposition & Case Studies (2:00 - 10:00)
├── Duration per slide: 4.0s to 6.0s (average ~4.8s)
├── Maximum ceiling: 6.0 seconds (hard cap)
└── Slide count: ~85 to 110 slides

Total Storyboard Size: ~115 to 145 slides for a 10-minute video.
```

---

## 🎯 Companion Short Flagging

The first minute of slides (typically slides 1 to ~20–25, covering timestamps `0.0s` to `~60–70s`) forms the **Autonomous Companion Short**.
- Tag each of these slides with `"short_candidate": true`.
- The pipeline will automatically slice these slides, audio, and words to generate a vertical 9:16 Short (`out/<slug>-short.mp4`) alongside the full 16:9 10-minute video (`out/<slug>-long.mp4`).

---

## Slide Schema (`slides.json`)

```json
[
  {
    "name": "slide_01_hook_title",
    "trigger": "the sunk cost fallacy",
    "top_title": "THE SUNK COST FALLACY",
    "bottom_caption": "WHY WE CAN'T LET GO.",
    "subject": "Bold title card. Large clean typography, character standing next to a giant question mark",
    "short_candidate": true
  },
  {
    "name": "slide_02_vip_ticket",
    "trigger": "imagine you buy a 40 dollar ticket",
    "top_title": "THE SUNK COST FALLACY",
    "bottom_caption": "A 40 DOLLAR MISTAKE.",
    "subject": "A cheerful stick-figure holding a gold VIP movie ticket with a bright yellow shirt",
    "short_candidate": true
  },
  {
    "name": "slide_35_concorde_project",
    "trigger": "the supersonic concorde airliner",
    "top_title": "THE CONCORDE DISASTER",
    "bottom_caption": "BILLIONS IN THE SKY.",
    "subject": "Wide landscape 16:9 view. Two government officials in black suits standing on an airstrip looking at a sleek supersonic passenger jet, stacks of cash flying into the jet engine",
    "short_candidate": false
  }
]
```

---

## Storyboard Rules for Long-Form

1. **Acoustic Trigger Matching**: Every `trigger` must be an exact 2–5 word phrase verbatim from `script.md`.
2. **Visual Progression**: Even during longer 4–6s slides in Phase 2, each slide must show a clear new concept, diagram, character action, or visual comparison.
3. **16:9 Landscape Framing**: Compose subjects for a widescreen 1920x1080 canvas:
   - Use the horizontal space: place contrasting characters on opposite sides (left vs right).
   - Use multi-element diagrams, charts with simple stick figure annotations, and detailed environmental backdrops (offices, courtrooms, airfields, laboratories).
4. **Validation Gate**: Run `python tools/cli.py check <slug>`. The auditor will automatically enforce:
   - `<= 4.0s` for all slides starting before `120.0s`.
   - `<= 6.0s` for all slides starting at or after `120.0s`.
