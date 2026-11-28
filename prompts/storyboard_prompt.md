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

1. **Start with the Name of the Law First (CRITICAL)**:
   - **Slide 01**: The video MUST start with the Name of the Law / Concept (e.g. `trigger: "the pratfall effect"` or `"the sunk cost fallacy"`). Displays the high-CTR Title Card while the narrator speaks the name.
   - **Slide 02**: The scenario begins with `"Imagine..."` (e.g. `trigger: "imagine a brilliant speaker"` or `"imagine you buy"`).
2. **1080x1920 (9:16 Vertical) Image Composition (Large Prominent Figures)**:
   - Generated as **1080x1920** vertical images (`9:16` aspect ratio) with large, prominent stick figures filling the tall mobile frame.
   - Characters and props must be large, bold, and expressive (never tiny, shrunken, or floating in empty space).
3. **Pacing Balance**: Keep most slides at **~3 seconds**, using **~2 seconds** selectively for quick surprise beats, sudden realizations, or punchy text reveals.
4. **Acoustic Trigger Matching**: Every `trigger` must be an exact 2–5 word phrase verbatim from `script.md`.
5. **Rich 2D Background Details**: Include environmental cues in `subject` (tall bookshelves, hanging plants, framed art, modern desks, floor lamps).
6. **Slide 01 Hook Title Card Rule**:
   - Slide 01 is the viewer's very first impression. It MUST be a compelling, high-CTR **Title Card**.
   - `top_title`: Exact phenomenon name in uppercase.
   - `bottom_caption`: 1 punchy hook subtitle (e.g., `WHY FLAWS MAKE US LIKEABLE.`, `WHY WE CAN'T QUIT BAD DECISIONS.`).
   - `subject`: Rich stylized 2D room setting (detailed wooden bookshelf with colorful books, lush potted indoor monstera plant, framed picture on wall) with an expressive stick figure in a bold crimson red shirt (#DC2626) reacting with wide curious eyes to the central paradox metaphor.
   - **STRICT PROHIBITION**: NEVER generate a plain, blank walking stickman or empty void for Slide 01. Always ground the opening with environmental richness and character emotion.
