"""Builds the HTML/JS slideshow viewer for Playwright rendering and live browser preview.
Supports 1920x1080 (laptop / long form) and 720x1600 (phone / short / reel) with centered canvas
and matching warm off-white cream (#FBF6EF) background fill.
"""
import json, shutil
from pathlib import Path
from common import load_json, save_json, ENGINE_DIR, die


def get_dimensions(fmt):
    """Resolves width and height for format."""
    f = str(fmt).lower()
    if f in ('720:1600', '720x1600', 'phone', 'short', 'reel', 'reels', '9:16'):
        return 720, 1600
    if f in ('16:9', '1920:1080', '1920x1080', 'laptop', 'long', 'desktop', 'wide'):
        return 1920, 1080
    if f in ('1:1', 'square'):
        return 1080, 1080
    return 720, 1600


def build_page(pdir):
    pdir = Path(pdir)
    cfg = load_json(pdir / 'film.json')
    slides = load_json(pdir / 'slides.json')
    
    fmt = cfg.get('format', '720:1600')
    W, H = get_dimensions(fmt)
    
    theme = cfg.get('theme', {})
    bg_color = theme.get('background', '#FBF6EF')
    font_fam = theme.get('font_family', "'Comic Sans MS', 'Comic Neue', cursive, sans-serif")
    
    canvas_cfg = cfg.get('canvas', {
        'aspect_ratio': 'custom',
        'width': W,
        'height': H,
        'canvas_bg': theme.get('canvas_bg', '#FBF6EF'),
        'border_radius': 0,
        'shadow': False,
        'blur_backdrop': False
    })
    
    bdir = pdir / 'build'
    bdir.mkdir(exist_ok=True, parents=True)
    
    # Copy slideshow engine
    shutil.copy(ENGINE_DIR / 'slideshow.js', bdir / 'slideshow.js')
    
    # Write film.js
    film_data = {
        'W': W,
        'H': H,
        'format': fmt,
        'theme': theme,
        'canvas': canvas_cfg,
        'transitions': cfg.get('transitions', {'default_type': 'cut', 'fade_duration': 0.0, 'ken_burns_zoom': 1.0})
    }
    (bdir / 'film.js').write_text(f"window.FILM = {json.dumps(film_data, indent=2)};\n", encoding='utf-8')
    
    # Write slides.js
    (bdir / 'slides.js').write_text(f"window.SLIDES = {json.dumps(slides, indent=2)};\n", encoding='utf-8')
    
    # Write page.html
    html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{cfg.get('title', 'Slideshow')}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: {W}px;
      height: {H}px;
      overflow: hidden;
      background: {bg_color};
      font-family: {font_fam};
      user-select: none;
    }}
    #viewport {{
      position: absolute;
      inset: 0;
      width: {W}px;
      height: {H}px;
      overflow: hidden;
      background: {bg_color};
    }}
    #slides-container {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      background: {bg_color};
    }}
  </style>
</head>
<body>
  <div id="viewport">
    <div id="slides-container"></div>
  </div>
  <script src="film.js"></script>
  <script src="slides.js"></script>
  <script src="clocks.js"></script>
  <script src="slideshow.js"></script>
</body>
</html>
"""
    (bdir / 'page.html').write_text(html_content, encoding='utf-8')
    print(f"[Build] Slideshow HTML canvas generated ({W}x{H}, background: {bg_color}) -> {bdir / 'page.html'}")
    return bdir / 'page.html'
