"""Compiles slides.json into Flow MCP prompts using customizable prompt templates.
Supports 1:1 square canvas for Shorts and 16:9 widescreen canvas for 10-minute Long-Form videos.
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
    fmt = cfg.get('format', '9:16')
    mode = cfg.get('mode', 'long' if fmt == '16:9' else 'short')
    is_long = (mode == 'long' or fmt == '16:9')
    
    out_prompts = []
    for s in slides:
        subject = s.get('subject', '').strip().rstrip('.')
        top_title = s.get('top_title', project_title)
        bottom_caption = s.get('bottom_caption', s.get('caption', ''))
        
        # Build Flow prompt tailored for format
        if is_long:
            # 16:9 Widescreen Landscape formula
            prompt_parts = [
                f"Modern 2D editorial webcomic explainer illustration on a warm off-white cream background ({bg_color}).",
                "16:9 widescreen landscape canvas, wide cinematic framing."
            ]
            if top_title:
                prompt_parts.append(f'At the top center, bold black comic book title: "{top_title}".')
            prompt_parts.append(f"In the wide landscape composition: {subject}.")
            if bottom_caption:
                prompt_parts.append(f'At the bottom center, bold comic book caption: "{bottom_caption}".')
            prompt_parts.append(
                "Stylized stick-figure characters with oversized round white heads, dot eyes, expressive eyebrows, thin black stick limbs, wearing solid color shirts (red, yellow, green, blue). Thick uniform black ink outlines, flat 2D coloring with zero gradients, soft gray ground shadows, clean comic typography, crisp clean lines, 16:9 landscape aspect ratio, no clutter, wide breathing room."
            )
            aspect_ratio = "16:9"
        else:
            # 1:1 Square canvas formula for Shorts
            prompt_parts = [
                f"Modern 2D editorial webcomic explainer illustration on a warm off-white cream background ({bg_color}).",
                "1:1 square canvas."
            ]
            if top_title:
                prompt_parts.append(f'At the top center, bold black comic book title: "{top_title}".')
            prompt_parts.append(f"In the center: {subject}.")
            if bottom_caption:
                prompt_parts.append(f'At the bottom center, bold comic book caption: "{bottom_caption}".')
            prompt_parts.append(
                "Stylized stick-figure characters with oversized round white heads, dot eyes, expressive eyebrows, thin black stick limbs, wearing solid color shirts (red, yellow, green, blue). Thick uniform black ink outlines, flat 2D coloring with zero gradients, soft gray ground shadows, clean comic typography, crisp lines, 1:1 square aspect ratio."
            )
            aspect_ratio = "1:1"

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
        
    save_json(pdir / 'prompts.json', out_prompts)
    format_label = "16:9 Widescreen (Long-Form)" if is_long else "1:1 Square (Short)"
    print(f"\n[Prompts] Generated {len(out_prompts)} prompts [{format_label}] -> {pdir / 'prompts.json'}")
    print(f"Applied style preset: '{preset.get('name', preset_key)}'")
    for p in out_prompts[:5]:
        print(f" - [{p['name']}]: {p['prompt'][:90]}...")
    if len(out_prompts) > 5:
        print(f"   ... and {len(out_prompts) - 5} more slide prompts.")
    return out_prompts
