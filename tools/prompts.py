"""Compiles slides.json into Flow MCP prompts using customizable prompt templates."""
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
    
    project_title = cfg.get('title', 'SURROUNDED BY IDIOTS').upper()
    
    out_prompts = []
    for s in slides:
        subject = s.get('subject', '').strip().rstrip('.')
        top_title = s.get('top_title', project_title)
        bottom_caption = s.get('bottom_caption', s.get('caption', ''))
        
        # Build Flow prompt
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
        prompt = " ".join(prompt_parts)
        
        out_prompts.append({
            'name': s['name'],
            'trigger': s.get('trigger', ''),
            'top_title': top_title,
            'bottom_caption': bottom_caption,
            'prompt': prompt,
            'caption': bottom_caption
        })
        
    save_json(pdir / 'prompts.json', out_prompts)
    print(f"\n[Prompts] Generated {len(out_prompts)} prompts -> {pdir / 'prompts.json'}")
    print(f"Applied style preset: '{preset.get('name', preset_key)}'")
    for p in out_prompts:
        print(f" - [{p['name']}]: {p['prompt'][:90]}...")
    return out_prompts
