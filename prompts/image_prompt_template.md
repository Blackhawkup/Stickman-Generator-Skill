# Image Prompt Template & Style Presets

This file defines the exact prompt formula and visual DNA used when generating slide images in the **Editorial Stick-Figure Explainer Comic** style through the Google Flow MCP server (`flow_agent_images`).

Supports:
- **Phone / Short / Reel**: **720 x 1600** (centered canvas with matching warm cream `#FBF6EF` fill)
- **Laptop / Long-Form**: **1920 x 1080** (16:9 widescreen with rich 2D background details)
- **Long-Form Thumbnail**: **1920 x 1080** (clickable high-CTR YouTube thumbnail featuring the topic name)

---

## The Prompt Formulas

### 1. Phone / Short / Reel Formula (720 x 1600 Canvas)
Used for vertical explainer shorts on phone screens (720x1600) with centered artwork seamlessly blending into the warm off-white cream background (`#FBF6EF`):
```text
Modern 2D editorial webcomic explainer illustration on a warm off-white cream background (#FBF6EF). Vertical composition centered on warm cream parchment background (#FBF6EF). At the top center, bold black comic book title: "{top_title}". In the center: {subject}. At the bottom center, bold comic book caption: "{bottom_caption}". Rich stylized 2D background details (cozy room interior, detailed bookshelf, framed wall pictures, potted indoor plants, stylish floor lamp, or desk setup) drawn in fine black ink lines and muted earthy neutrals. Stylized stick-figure characters with oversized round white heads, dot eyes, expressive eyebrows, thin black stick limbs, wearing solid bold primary color shirts (red #DC2626, yellow #EAB308, green #16A34A, blue #2563EB). Thick uniform black ink outlines on characters, flat 2D coloring with zero gradients, soft gray ground shadows, clean comic typography, crisp lines, centered subject seamlessly blending into the warm cream background fill.
```

### 2. Laptop / Long-Form Formula (1920 x 1080 Canvas)
Used for 10-minute long-form explainer videos (1920x1080 horizontal) on laptops and widescreen monitors:
```text
Modern 2D editorial webcomic explainer illustration on a warm off-white cream background (#FBF6EF). 1920x1080 widescreen landscape canvas (16:9 aspect ratio), wide cinematic framing, centered subject. At the top center, bold black comic book title: "{top_title}". In the wide center composition: {subject}. At the bottom center, bold comic book caption: "{bottom_caption}". Rich stylized 2D background details (subtle room architectural outlines, bookshelves with colorful book spines, framed artwork on walls, modern potted plants, desk lamps, or distant city skyline silhouettes) drawn in fine black ink lines with muted earthy neutral colors (slate gray, soft taupe, olive green, warm wood). Stylized stick-figure characters with oversized round white heads, dot eyes, expressive eyebrows, thin black stick limbs, wearing solid bold primary color shirts (red #DC2626, yellow #EAB308, green #16A34A, blue #2563EB). Thick uniform black ink outlines on characters, flat 2D coloring with zero gradients, soft gray ground shadows, clean comic typography, crisp lines, 16:9 landscape aspect ratio, subject centered with generous breathing room matching background color.
```

### 3. YouTube Thumbnail Formula (1920 x 1080)
```text
Modern 2D editorial webcomic explainer illustration on a warm off-white cream background (#FBF6EF). 1920x1080 widescreen landscape YouTube thumbnail. In huge bold comic typography across the top center: "{topic}". In the center: Dramatic high-contrast visual scene with rich stylized 2D background environment (detailed office or laboratory background, chalkboard with arrows, bookshelf, dramatic spotlight). Stylized stick-figure character with oversized round white head, shocked wide dot eyes and open mouth, wearing a bright solid crimson red shirt (#DC2626), frozen in disbelief facing a giant dilemma or metaphorical paradox. Thick uniform black ink outlines, flat 2D coloring with zero gradients, soft gray ground shadow, clean negative space, dramatic YouTube thumbnail composition, clickable, 16:9 landscape aspect ratio (1920x1080).
```

---

## Detailed Visual DNA

### 1. Canvas & Centering
- **Phone / Short / Reel**: 720x1600. The image and characters stay perfectly centered, and the surrounding canvas is filled with the exact same warm cream color (`#FBF6EF`). No black bars, no harsh borders.
- **Laptop / Long-Form**: 1920x1080 widescreen. Clean landscape composition with warm cream canvas fill.
- **Top Zone**: Centered bold uppercase comic headline title in black ink.
- **Center Zone**: The main character action, expressive interactions, and props.
- **Bottom Zone**: 1 or 2 lines of bold punchy comic book caption.

### 2. Rich 2D Background Details
- Every image includes charming, stylized 2D background elements drawn in fine black ink lines:
  - **Indoor Environments**: Mid-century wooden bookshelves filled with books, framed artwork on walls, lush potted indoor plants (fiddle-leaf fig, monstera), modern floor lamps, clean desks with laptops and mugs, wall clocks, patterned rugs.
  - **Offices / Analysis Labs**: Glass partitions with subtle office textures, chalkboards with flowcharts and arrows, corkboards with sticky notes.
  - **Outdoor Scenes**: Distant city skyline silhouettes, soft rolling hills, stylized grass tufts, whimsical clouds in the warm cream sky, street lamps, café awnings.
- **Background Palette**: Muted earthy neutrals (slate gray, soft taupe, olive green, warm wood brown) so the background is visually rich while the primary-colored characters remain the clear focal point.

### 3. Character Design
- **Head**: Oversized, smooth white circle; dot eyes, expressive eyebrows, and simple line mouths communicating clear emotions (shock, fury, joy, analysis, confusion).
- **Body**: Simple rounded bean-shaped torso wearing solid primary color shirts:
  - **Red**: Urgent, aggressive, results-focused (`#DC2626`).
  - **Yellow**: Enthusiastic, energetic, chaotic (`#EAB308`).
  - **Green**: Calm, passive, conflict-avoidant (`#16A34A`).
  - **Blue**: Analytical, methodical, fact-driven (`#2563EB`).
- **Limbs**: Thin uniform black stick limbs with small oval white hands and shoes.
- **Shading**: Flat 2D cel style with soft, semi-transparent warm-gray oval ground shadows.
