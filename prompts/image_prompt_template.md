# Image Prompt Template & Style Presets

This file defines the exact prompt formula and visual DNA used when generating slide images in the **Editorial Stick-Figure Explainer Comic** style through the Google Flow MCP server (`flow_agent_images`).

---

## The Default Prompt Formula

Every slide prompt is constructed by integrating the **Top Title Header**, the **Central Subject**, and the **Bottom Caption**:

```text
Modern 2D editorial webcomic explainer illustration, 1:1 square canvas on a warm off-white cream background (#FBF6EF). At the top center, bold comic book title: "{top_title}". In the center: {subject}. At the bottom center, bold comic book caption: "{bottom_caption}". Stylized stick-figure characters with oversized round white heads, dot eyes, expressive eyebrows, thin black stick limbs, wearing solid color shirts (red, yellow, green, blue). Thick uniform black ink outlines, flat 2D coloring with zero gradients, soft gray ground shadows, clean comic typography, crisp lines, 1:1 square aspect ratio.
```

---

## Primary Style Preset (Extracted Style)

### `editorial_stick_comic` (Default)
> "Modern 2D editorial webcomic explainer illustration on a warm off-white cream background (#FBF6EF). Features stylized stick-figure characters with oversized pure white round heads, simple dot eyes, expressive minimalist eyebrows and mouths, rounded bean-shaped torsos, thin black stick limbs, and small oval white hands and feet. Thick, uniform, slightly hand-drawn black ink outlines with rounded line ends. Flat 2D coloring with zero gradients, using muted earthy neutrals for props and furniture, desaturated light gray silhouettes for background crowd figures, and bold solid primary accent colors (red #DC2626, yellow #EAB308, green #16A34A, blue #2563EB) for character shirts or large flat circular halos behind spotlight characters. Minimalist soft oval gray ground shadows underneath characters and objects, expressive comic motion lines, clean comic layout."

---

## Detailed Visual DNA (For AI Agent Replication)

### 1. Canvas & Framing
- **Canvas Aspect Ratio**: 1:1 Square (1080x1080), vertically centered in 9:16 mobile frame with solid black letterbox bars (`#000000`).
- **Canvas Background**: Warm off-white parchment cream (`#FBF6EF` / `#F6F4EC`).
- **Top Zone**: Centered bold uppercase comic title (e.g. `SURROUNDED BY IDIOTS`) in black ink with comic sans / hand-drawn comic lettering.
- **Center Zone**: The main character action, props, furniture, speech bubbles, and thought bubbles.
- **Bottom Zone**: 1 or 2 lines of bold uppercase punchy caption text, with keywords colored in primary red (`#DC2626`), yellow (`#EAB308`), green (`#16A34A`), or blue (`#2563EB`).

### 2. Character Design Rules
- **Head**: Oversized, smooth white circle; no ears, no nose, no hair (unless required for a specific archetype like the Greek physician Hippocrates who has a gray beard and toga, or round spectacles on the analytical Blue character).
- **Face**: Minimalist black dot/oval eyes, short angled eyebrows, and simple curved or straight line mouths to communicate distinct emotional states (furious, overjoyed, relaxed, analytical, confused).
- **Body**: Simple rounded bean-shaped torso. Characters wear plain solid shirts in primary colors:
  - **Red**: Driven, aggressive, urgent, results-focused (`#DC2626`).
  - **Yellow**: Enthusiastic, chaotic, spontaneous, energetic (`#EAB308`).
  - **Green**: Calm, passive, conflict-avoidant, patient (`#16A34A`).
  - **Blue**: Analytical, meticulous, methodical, fact-driven (`#2563EB`).
- **Limbs**: Thin, uniform solid black stick arms and stick legs with small oval white hands/mittens and small oval white shoes.
- **Secondary Characters**: Drawn in the same style but filled with flat, neutral white or desaturated warm gray silhouettes so they never compete with focal characters.

### 3. Comic Storytelling Elements (In-Image Text & Props)
- **Speech Bubbles**: Rounded white speech bubbles with black outlines and comic dialogue (e.g., `"WHATEVER YOU GUYS DECIDE"`, `"SMALL TALK" [crossed out with red diagonal line]`, `"WHY?"`).
- **Thought Bubbles**: Bubbly cloud outlines showing icons or text (e.g., beach/mountain/city icons, `"WHY ARE MY FRIENDS LIKE THIS?"`, `"IDIOT"`).
- **Labeled Props & Diagrams**:
  - Laptops showing flight maps with route pins, or spreadsheets with columns `"PRICE | DISTANCE | WEATHER"`.
  - Wall clocks / stopwatches ticking in red.
  - Desk calendars with red X marks over two weeks.
  - Book covers with clear legible titles.
  - Signposts (`"CHANGE"`) and rainclouds (`"CONFLICT"`).
  - Four open colored boxes (red, yellow, green, blue).

### 4. Linework & Shading
- **Outlines**: Medium-thick black ink strokes with rounded caps and hand-drawn comic smoothness.
- **Interior Shading**: Flat 2D cel style only. Soft, semi-transparent warm-gray elliptical ground shadows underneath characters and furniture. No 3D lighting, specular highlights, or airbrushed gradients.
- **Halos**: Large, flat solid-color circular backdrops (red, yellow, green, blue) directly behind the character in spotlight scenes.

---

## Scene-Specific Sub-Presets

### 1. `stick_comic_spotlight` (Personality Type Spotlight)
> "Modern 2D editorial stick-figure webcomic illustration on warm off-white cream background (#FBF6EF). Single main character centered in front of a large flat solid-colored circular halo backdrop (red, yellow, green, or blue). Labeled symbolic props, bold top title, bold bottom caption with colored keyword."

### 2. `stick_comic_interior` (Living Room / Office)
> "Modern 2D editorial stick-figure webcomic illustration on warm off-white cream background (#FBF6EF). Flat 2D interior room with beige walls, living room sofa, coffee table, laptop showing clear interface, four stick friends in colored shirts interacting."

### 3. `stick_comic_group` (Four-Way Clashing Scene)
> "Modern 2D editorial stick-figure webcomic illustration on warm off-white cream background (#FBF6EF). Four distinct stick figures in red, yellow, green, and blue shirts pointing or arguing, comic emotion lines, bold top title, bold bottom punchy caption."
