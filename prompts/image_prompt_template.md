# Image Prompt Template & Style Presets

This file defines the exact prompt formula and visual DNA used when generating slide images in the **Editorial Stick-Figure Explainer Comic** style through the Google Flow MCP server (`flow_agent_images`).

Supports both **1:1 Square (Vertical Shorts)** and **16:9 Widescreen (10-Minute Long-Form)** formats.

---

## The Prompt Formulas

### 1. Short-Form Formula (1:1 Square Canvas)
Used for 1-minute vertical Shorts (1080x1920) with a centered 1:1 square canvas:
```text
Modern 2D editorial webcomic explainer illustration on a warm off-white cream background (#FBF6EF). 1:1 square canvas. At the top center, bold black comic book title: "{top_title}". In the center: {subject}. At the bottom center, bold comic book caption: "{bottom_caption}". Stylized stick-figure characters with oversized round white heads, dot eyes, expressive eyebrows, thin black stick limbs, wearing solid color shirts (red, yellow, green, blue). Thick uniform black ink outlines, flat 2D coloring with zero gradients, soft gray ground shadows, clean comic typography, crisp lines, 1:1 square aspect ratio.
```

### 2. Long-Form Formula (16:9 Widescreen Canvas)
Used for 10-minute long-form explainer videos (1920x1080 horizontal):
```text
Modern 2D editorial webcomic explainer illustration on a warm off-white cream background (#FBF6EF). 16:9 widescreen landscape canvas, wide cinematic framing. At the top center, bold black comic book title: "{top_title}". In the wide landscape composition: {subject}. At the bottom center, bold comic book caption: "{bottom_caption}". Stylized stick-figure characters with oversized round white heads, dot eyes, expressive eyebrows, thin black stick limbs, wearing solid color shirts (red, yellow, green, blue). Thick uniform black ink outlines, flat 2D coloring with zero gradients, soft gray ground shadows, clean comic typography, crisp clean lines, 16:9 landscape aspect ratio, no clutter, wide breathing room.
```

---

## Primary Style Preset

### `editorial_stick_comic` (Default)
> "Modern 2D editorial webcomic explainer illustration on a warm off-white cream background (#FBF6EF). Features stylized stick-figure characters with oversized pure white round heads, simple dot eyes, expressive minimalist eyebrows and mouths, rounded bean-shaped torsos, thin black stick limbs, and small oval white hands and feet. Thick, uniform, slightly hand-drawn black ink outlines with rounded line ends. Flat 2D coloring with zero gradients, using muted earthy neutrals for props and furniture, desaturated light gray silhouettes for background crowd figures, and bold solid primary accent colors (red #DC2626, yellow #EAB308, green #16A34A, blue #2563EB) for character shirts or large flat circular halos behind spotlight characters. Minimalist soft oval gray ground shadows underneath characters and objects, expressive comic motion lines, clean comic layout."

---

## Detailed Visual DNA (For AI Agent Replication)

### 1. Canvas & Framing
- **Short Mode**: 1:1 Square (1080x1080), vertically centered in 9:16 mobile frame with solid black letterbox bars (`#000000`).
- **Long-Form Mode**: 16:9 Landscape (1920x1080), full bleed widescreen canvas on warm cream (`#FBF6EF` / `#F6F4EC`).
- **Top Zone**: Centered bold uppercase comic title (e.g. `THE SUNK COST FALLACY`, `CONCORDE DISASTER`) in black ink with comic lettering.
- **Center Zone**: The main character action, props, diagrams, speech bubbles, and comparisons.
- **Bottom Zone**: 1 or 2 lines of bold uppercase punchy caption text, with keywords emphasized.

### 2. Character Design Rules
- **Head**: Oversized, smooth white circle; no ears, no nose, no hair (unless required for a specific archetype like a bearded historical researcher or spectacles).
- **Face**: Minimalist black dot/oval eyes, short angled eyebrows, and simple curved or straight line mouths to communicate distinct emotional states (furious, overjoyed, relaxed, analytical, confused).
- **Body**: Simple rounded bean-shaped torso. Characters wear plain solid shirts in primary colors:
  - **Red**: Driven, aggressive, urgent, results-focused (`#DC2626`).
  - **Yellow**: Enthusiastic, chaotic, spontaneous, energetic (`#EAB308`).
  - **Green**: Calm, passive, conflict-avoidant, patient (`#16A34A`).
  - **Blue**: Analytical, meticulous, methodical, fact-driven (`#2563EB`).
- **Limbs**: Thin, uniform solid black stick arms and stick legs with small oval white hands/mittens and small oval shoes.
- **Secondary Characters**: Drawn in the same style but filled with flat, neutral white or desaturated warm gray silhouettes so they never compete with focal characters.

### 3. Comic Storytelling Elements (In-Image Text & Props)
- **Speech Bubbles**: Rounded white speech bubbles with black outlines and comic dialogue.
- **Thought Bubbles**: Bubbly cloud outlines showing icons or text.
- **Labeled Props & Diagrams**:
  - Research lab experiments with labeled control groups ("Group A: Full Price" vs "Group B: Discounted").
  - Aircraft blueprints, corporate boardrooms, stock charts trending down.
  - Wall clocks / stopwatches ticking in red.
  - Clean decision trees and mental model diagrams ("Stranger Test", "Zero-Based Thinking").

### 4. Linework & Shading
- **Outlines**: Medium-thick black ink strokes with rounded caps and hand-drawn comic smoothness.
- **Interior Shading**: Flat 2D cel style only. Soft, semi-transparent warm-gray elliptical ground shadows underneath characters and furniture. No 3D lighting, specular highlights, or airbrushed gradients.
- **Halos**: Large, flat solid-color circular backdrops directly behind the character in spotlight scenes.
