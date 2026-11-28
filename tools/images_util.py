"""Image dimension & aspect-ratio normalizer.
Enforces exact pixel resolutions without clipping or distorting artwork:
- Short / Companion Short slides (9:16): 1080 x 1920 pixels
- Long-Form slides (16:9): 1920 x 1024 pixels
- Long-Form Thumbnails (16:9): 1920 x 1080 pixels
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from common import load_json
except ImportError:
    from tools.common import load_json

CREAM_BG = (251, 246, 239)  # #FBF6EF


def get_target_resolution(aspect_ratio, is_thumbnail=False, mode='short'):
    """Returns exact target (width, height) pixels for a slide prompt."""
    if is_thumbnail:
        return (1920, 1080)
    ar = str(aspect_ratio or '').lower()
    if ar in ('9:16', '720:1600', '1080:1920', 'short', 'vertical'):
        return (1080, 1920)
    if ar in ('16:9', '1920:1024', '1920:1080', 'long', 'landscape'):
        return (1920, 1024)
    if ar in ('1:1', 'square'):
        return (1080, 1080)
    return (1920, 1024) if mode == 'long' else (1080, 1920)


def fit_image_to_target(img_path, target_w, target_h, bg_rgb=CREAM_BG):
    """Resizes and centers an image cleanly to (target_w, target_h) with warm cream fill."""
    img_path = Path(img_path)
    if not img_path.exists():
        return False

    with Image.open(img_path) as im:
        if im.size == (target_w, target_h) and im.mode == 'RGB':
            return False  # Already exact dimensions

        src = im.convert('RGB')
        # Scale proportionally so it fits cleanly inside (target_w, target_h) without clipping text or characters,
        # or if aspect ratio is within 2% of target, resize cleanly to fill.
        src_ratio = src.width / max(1, src.height)
        tgt_ratio = target_w / max(1, target_h)
        if abs(src_ratio - tgt_ratio) / tgt_ratio <= 0.03:
            out = src.resize((target_w, target_h), Image.Resampling.LANCZOS)
        else:
            out = ImageOps.pad(src, (target_w, target_h), method=Image.Resampling.LANCZOS, color=bg_rgb, centering=(0.5, 0.5))

        out.save(img_path, format='PNG' if img_path.suffix.lower() == '.png' else 'JPEG', quality=95)
        return True


def normalize_project_images(pdir):
    """Normalizes all slide images in pdir/images/ to their exact target dimensions."""
    pdir = Path(pdir)
    img_dir = pdir / 'images'
    if not img_dir.exists():
        return 0

    cfg_file = pdir / 'film.json'
    cfg = load_json(cfg_file) if cfg_file.exists() else {}
    fmt = cfg.get('format', '9:16')
    mode = cfg.get('mode', 'long' if fmt in ('16:9', '1920:1080', '1920:1024', 'laptop', 'long') else 'short')

    prompts_file = pdir / 'prompts.json'
    prompt_map = {}
    if prompts_file.exists():
        for item in load_json(prompts_file):
            prompt_map[item['name']] = item

    changed = 0
    for ext in ('*.png', '*.jpg', '*.jpeg'):
        for f in img_dir.glob(ext):
            stem = f.stem
            p_info = prompt_map.get(stem, {})
            is_thumb = (p_info.get('type') == 'thumbnail' or 'thumbnail' in stem.lower())
            if is_thumb:
                tw, th = 1920, 1080
            elif p_info.get('target_width') and p_info.get('target_height'):
                tw, th = int(p_info['target_width']), int(p_info['target_height'])
            elif stem.startswith('short_') or p_info.get('type') == 'companion_short':
                tw, th = 1080, 1920
            else:
                ar = p_info.get('aspect_ratio', '16:9' if mode == 'long' else '9:16')
                tw, th = get_target_resolution(ar, is_thumbnail=False, mode=mode)

            if fit_image_to_target(f, tw, th):
                changed += 1
                print(f" -> Normalized {f.name} -> {tw}x{th}")

    if changed:
        print(f"[Images] Normalized {changed} image file(s) to exact target resolution.")
    return changed


if __name__ == '__main__':
    if len(sys.argv) > 1:
        normalize_project_images(sys.argv[1])
