# Storyboard & Slide Trigger Breakdown (Shorts)

Instructions for breaking down a 1-minute narration script into timed visual slides (`slides.json`).

---

## ⏱️ Retention Pacing Rules (Mostly 3s, Sometimes 2s)

```
Slide Duration Guidelines:
├── Standard Duration: Around 3.0 seconds (2.6s to 3.5s) for most slides
├── Snappy Transitions: Sometimes around 2.0 seconds (2.0s to 2.5s) for quick punchy beats
├── Minimum Duration: 1.8 seconds (avoid rushed 1-second cuts)
├── Maximum Ceiling: 3.8 seconds (never drag beyond 3.8s)
├── Target Average: ~2.8s to 3.2s across all slides
└── Total Slide Count: ~20 to 25 slides for a ~60-75 second short
```

---

## Slide Schema (`slides.json`)

```json
[
  {
    "name": "slide_01_hook_title",
    "trigger": "the pratfall effect",
    "top_title": "THE PRATFALL EFFECT",
    "bottom_caption": "WHY FLAWS MAKE US LIKEABLE.",
    "subject": "Bold title card. Large clean typography, centered stick figure with bright red shirt, rich room background with bookshelf and indoor plant"
  },
  {
    "name": "slide_02_spilled_coffee",
    "trigger": "imagine a brilliant speaker",
    "top_title": "THE PRATFALL EFFECT",
    "bottom_caption": "A FLAWLESS PRESENTATION.",
    "subject": "A confident stick-figure in a sharp suit standing at a modern podium, auditorium stage background with subtle audience silhouettes"
  }
]
```

---

## Rules for Slide Generation

1. **Pacing Balance**: Keep most slides at **~3 seconds**, using **~2 seconds** selectively for quick surprise beats, sudden realizations, or punchy text reveals.
2. **Acoustic Trigger Matching**: Every `trigger` must be an exact 2–5 word phrase verbatim from `script.md`.
3. **Rich 2D Background**: Include environmental cues in `subject` (e.g. bookshelves, framed art, plants, desks, city windows).
4. **Resolution**: Outputs at **720x1600** for phone/reels, centered with warm cream (`#FBF6EF`) background fill.
5. **Slide 01 Hook Visual Rule (CRITICAL)**:
   - Slide 01 is the viewer's very first impression. It MUST be a compelling, high-CTR **Title Card**.
   - `top_title`: Exact phenomenon name in uppercase.
   - `bottom_caption`: 1 punchy hook subtitle (e.g., `WHY FLAWS MAKE US LIKEABLE.`, `WHY WE CAN'T QUIT BAD DECISIONS.`).
   - `subject`: Rich stylized 2D room setting (detailed wooden bookshelf with colorful books, lush potted indoor monstera plant, framed picture on wall) with an expressive stick figure in a bold crimson red shirt (#DC2626) reacting with wide curious eyes to the central paradox metaphor.
   - **STRICT PROHIBITION**: NEVER generate a plain, blank walking stickman or empty void for Slide 01. Always ground the opening with environmental richness and character emotion.
