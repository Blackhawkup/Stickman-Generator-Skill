# Storyboard & Slide Breakdown Prompt

Use this prompt to convert an approved explainer script into a sequential slide timeline with exact audio trigger words, titles, captions, and visual scene prompts.

---

## Instructions for the Model

Analyze the approved narration script. Break it down into sequential visual slides.

### STRICT PACING RULES (MANDATORY):
- **NO image may stay on screen for more than 4.0 seconds.**
- **Slide Duration Target**: Every slide must stay on screen for between **2, 3, and 4 seconds** (ideal sweet spot: 2.5 to 3.5 seconds).
- **Slide Count**: For a 55–65 second short video, break the script down into **18 to 22 sequential slides**.
- **Every visual beat must trigger on a specific 3-5 word phrase in the spoken audio.**
- Never let a character or background linger statically past 4 seconds; change camera angle, character reaction, speech bubble, or prop detail to keep visual momentum high.

### For each slide, define:
1. `name`: Unique short identifier (e.g. `slide_01_intro`, `slide_02_planning`, `slide_10_red_results`).
2. `trigger`: The exact 3-5 word phrase in the audio where this slide cuts in.
3. `top_title`: The top bold comic header (default: the main topic title, e.g. `"SURROUNDED BY IDIOTS"`).
4. `bottom_caption`: 1 to 2 lines of punchy, uppercase summary text for the bottom of the slide (e.g., `"PLANNING A WEEKEND TRIP."`, `"BOOK IT TONIGHT."`, `"RED. RESULTS NOT SMALL TALK."`).
5. `accent_color`: (Optional) The primary accent color for keywords or halos (`red`, `yellow`, `green`, `blue`).
6. `subject`: A detailed visual description of the central comic artwork (characters, colored shirts, facial expressions, speech bubbles, thought bubbles, props, furniture).
7. `transition`: `"cut"` (instant cut matching the reference video) or `"fade"`.

---

## Storyboard JSON Schema

```json
[
  {
    "name": "slide_01_intro",
    "trigger": "Surrounded by idiots",
    "top_title": "SURROUNDED BY IDIOTS",
    "bottom_caption": "",
    "subject": "Four stylized stick figures in red, yellow, green, and blue shirts pointing angrily at each other in a circle on an off-white cream background",
    "transition": "cut"
  },
  {
    "name": "slide_02_planning",
    "trigger": "Imagine four friends",
    "top_title": "SURROUNDED BY IDIOTS",
    "bottom_caption": "PLANNING A WEEKEND TRIP.",
    "accent_color": "red",
    "subject": "Four stick figure friends (wearing red, yellow, green, and blue shirts) sitting on a living room sofa around a wooden coffee table with a laptop showing a travel flight map route with an airplane and pin",
    "transition": "cut"
  }
]
```
