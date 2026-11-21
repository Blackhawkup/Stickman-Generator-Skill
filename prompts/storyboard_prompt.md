# Storyboard & Slide Trigger Breakdown (Shorts)

Instructions for breaking down a 1-minute narration script into timed visual slides (`slides.json`).

---

## ⏱️ Retention Pacing Rules (Strict)

```
1st Minute Pacing Rules:
├── Ceiling: Every slide must stay on screen for LESS than 3.0 seconds (< 3.0s)
├── Average: ~2.0 seconds on average across all slides
├── Range: 1.2s to 2.8s per slide
└── Slide Count: 28 to 32 slides for a ~60-second video
```

---

## Slide Schema (`slides.json`)

```json
[
  {
    "name": "slide_01_hook_title",
    "trigger": "the sunk cost fallacy",
    "top_title": "THE SUNK COST FALLACY",
    "bottom_caption": "WHY WE CAN'T LET GO.",
    "subject": "Bold title card. Centered character with bright red shirt, detailed office background with bookshelf and potted plant"
  },
  {
    "name": "slide_02_vip_ticket",
    "trigger": "imagine you buy a forty dollar ticket",
    "top_title": "THE SUNK COST FALLACY",
    "bottom_caption": "A 40 DOLLAR MISTAKE.",
    "subject": "A stick-figure holding a gold VIP movie ticket with a bright yellow shirt, cozy living room background with sofa and lamp"
  }
]
```

---

## Rules for Slide Generation

1. **Duration Constraint**: Never allow a slide to last `>= 3.0s` in the first minute.
2. **Acoustic Trigger Matching**: Every `trigger` must be an exact 2–5 word phrase verbatim from `script.md`.
3. **Rich 2D Background**: Include environmental cues in `subject` (e.g. bookshelves, framed art, plants, desks, city windows).
4. **Resolution**: Outputs at **720x1600** for phone/reels, centered with warm cream (`#FBF6EF`) background fill.
