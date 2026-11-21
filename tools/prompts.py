"""Compiles slides.json into Flow MCP prompts using customizable prompt templates.
Supports:
- 1920x1080 widescreen landscape for laptop / long-form videos
- 720x1600 portrait canvas for phone / short / reel videos (centered with warm cream background #FBF6EF fill)
- Dedicated 1920x1080 high-CTR YouTube thumbnail prompt in the same art style
- Rich stylized 2D background details (furniture, bookshelves, indoor plants, architectural lines)
"""
from pathlib import Path
from common import load_json, save_json, PROMPTS_DIR, die


def build_prompts(project_dir):
    pdir = Path(project_dir)
    cfg = load_json(pdir / 'film.json')
    slides = load_json(pdir / 'slides.json')
    presets = load_json(PROMPTS_DIR / 'style_presets.json')
    
    preset_key = cfg.get('style_preset', 'editorial_stick_comic')
    preset = presets.get(preset_key, presets.get('editorial_stick_comic', {}))
    bg_color = preset.get('background', '#FBF6EF')
    
    project_title = cfg.get('title', pdir.name.replace('-', ' ')).upper()
    fmt = cfg.get('format', '720:1600')
    mode = cfg.get('mode', 'long' if fmt in ('16:9', '1920:1080', 'laptop', 'long') else 'short')
    is_long = (mode == 'long' or fmt in ('16:9', '1920:1080', 'laptop'))
    
    out_prompts = []
    for s in slides:
        subject = s.get('subject', '').strip().rstrip('.')
        top_title = s.get('top_title', project_title)
        bottom_caption = s.get('bottom_caption', s.get('caption', ''))
        
        # Build Flow prompt tailored for format
        if is_long:
            # 1920x1080 Widescreen Landscape formula for laptop & long form
            prompt_parts = [
                f"Modern 2D editorial webcomic explainer illustration on a warm off-white cream background ({bg_color}).",
                "1920x1080 widescreen landscape canvas (16:9 aspect ratio), wide cinematic framing, centered subject."
            ]
            if top_title:
                prompt_parts.append(f'At the top center, bold black comic book title: "{top_title}".')
            prompt_parts.append(f"In the wide center composition: {subject}.")
            if bottom_caption:
                prompt_parts.append(f'At the bottom center, bold comic book caption: "{bottom_caption}".')
            prompt_parts.append(
                f"Rich stylized 2D background details (subtle room architectural outlines, bookshelves with colorful book spines, framed artwork on walls, modern potted plants, desk lamps, or distant city skyline silhouettes) drawn in fine black ink lines with muted earthy neutral colors (slate gray, soft taupe, olive green, warm wood). "
                f"Stylized stick-figure characters with oversized round white heads, dot eyes, expressive eyebrows, thin black stick limbs, wearing solid bold primary color shirts (red #DC2626, yellow #EAB308, green #16A34A, blue #2563EB). "
                f"Thick uniform black ink outlines on characters, flat 2D coloring with zero gradients, soft gray ground shadows, clean comic typography, crisp lines, 16:9 landscape aspect ratio, subject centered with generous breathing room matching background color."
            )
            aspect_ratio = "16:9"
        else:
            # 720x1600 Phone / Short / Reel formula
            prompt_parts = [
                f"Modern 2D editorial webcomic explainer illustration on a warm off-white cream background ({bg_color}).",
                "Vertical composition centered on warm cream parchment background (#FBF6EF)."
            ]
            if top_title:
                prompt_parts.append(f'At the top center, bold black comic book title: "{top_title}".')
            prompt_parts.append(f"In the center: {subject}.")
            if bottom_caption:
                prompt_parts.append(f'At the bottom center, bold comic book caption: "{bottom_caption}".')
            prompt_parts.append(
                f"Rich stylized 2D background details (cozy room interior, detailed bookshelf, framed wall pictures, potted indoor plants, stylish floor lamp, or desk setup) drawn in fine black ink lines and muted earthy neutrals. "
                f"Stylized stick-figure characters with oversized round white heads, dot eyes, expressive eyebrows, thin black stick limbs, wearing solid bold primary color shirts (red #DC2626, yellow #EAB308, green #16A34A, blue #2563EB). "
                f"Thick uniform black ink outlines on characters, flat 2D coloring with zero gradients, soft gray ground shadows, clean comic typography, crisp lines, centered subject seamlessly blending into the warm cream background fill."
            )
            aspect_ratio = "1:1"  # Generated centered, displays seamlessly in 720x1600 frame

        prompt = " ".join(prompt_parts)
        
        out_prompts.append({
            'name': s['name'],
            'trigger': s.get('trigger', ''),
            'top_title': top_title,
            'bottom_caption': bottom_caption,
            'prompt': prompt,
            'caption': bottom_caption,
            'aspect_ratio': aspect_ratio,
            'short_candidate': s.get('short_candidate', False)
        })
        
    # If Long-Form: generate a dedicated 1920x1080 YouTube Thumbnail prompt in the same art style
    if is_long:
        thumb_name = f"{pdir.name}-thumbnail"
        thumb_prompt = (
            f"Modern 2D editorial webcomic explainer illustration on a warm off-white cream background ({bg_color}). "
            f"1920x1080 widescreen landscape YouTube thumbnail. In huge bold comic typography across the top center: \"{project_title}\". "
            f"In the center: Dramatic high-contrast visual scene with rich stylized 2D background environment (detailed office or laboratory background, chalkboard with arrows, bookshelf, dramatic spotlight). "
            f"Stylized stick-figure character with oversized round white head, shocked wide dot eyes and open mouth, wearing a bright solid crimson red shirt (#DC2626), frozen in disbelief facing a giant dilemma or metaphorical paradox. "
            f"Thick uniform black ink outlines, flat 2D coloring with zero gradients, soft gray ground shadow, clean negative space, dramatic YouTube thumbnail composition, clickable, 16:9 landscape aspect ratio (1920x1080)."
        )
        out_prompts.append({
            'name': thumb_name,
            'type': 'thumbnail',
            'top_title': project_title,
            'bottom_caption': 'WHY WE CANT LET GO',
            'prompt': thumb_prompt,
            'caption': 'THUMBNAIL',
            'aspect_ratio': '16:9'
        })
        print(f" -> Added 1920x1080 YouTube Thumbnail prompt: '{thumb_name}'")

    save_json(pdir / 'prompts.json', out_prompts)
    format_label = "1920x1080 Widescreen (Laptop / Long-Form)" if is_long else "720x1600 Centered (Phone / Short / Reel)"
    print(f"\n[Prompts] Generated {len(out_prompts)} prompts [{format_label}] -> {pdir / 'prompts.json'}")
    print(f"Applied style preset: '{preset.get('name', preset_key)}'")
    for p in out_prompts[:5]:
        print(f" - [{p['name']}]: {p['prompt'][:90]}...")
    if len(out_prompts) > 5:
        print(f"   ... and {len(out_prompts) - 5} more prompts.")
    return out_prompts
