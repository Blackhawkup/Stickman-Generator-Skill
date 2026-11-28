"""Companion Short Extractor:
Automatically extracts the opening ~1 minute hook from a 10-minute long-form explainer
and renders a vertical 720x1600 60fps Short (out/<slug>-short.mp4) formatted for phone/reels
with seamless warm cream background (#FBF6EF) fill.
"""
import asyncio, json, os, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from common import load_json, save_json, run, probe_duration, ENGINE_DIR, die
except ImportError:
    from tools.common import load_json, save_json, run, probe_duration, ENGINE_DIR, die
from render import render_slideshow


def extract_short(pdir, out_short_mp4=None, max_duration=65.0):
    pdir = Path(pdir)
    cfg = load_json(pdir / 'film.json')
    slides = load_json(pdir / 'slides.json')
    words_file = pdir / 'voice/words.json'
    words = load_json(words_file) if words_file.exists() else []
    
    slug = cfg.get('slug', pdir.name)
    out_dir = pdir / 'out'
    out_dir.mkdir(exist_ok=True, parents=True)
    if not out_short_mp4:
        out_short_mp4 = out_dir / f"{slug}-short.mp4"
    else:
        out_short_mp4 = Path(out_short_mp4)

    # 1. Determine which slides belong to the opening ~1 min Short
    short_slides = [s for s in slides if s.get('short_candidate') is True]
    
    if not short_slides:
        def norm(w):
            return ''.join(c for c in (w or '').lower() if c.isalnum())
        nwords = [{'k': norm(x.get('w', '')), 's': x.get('s', 0.0), 'e': x.get('e', 0.0)} for x in words]
        
        def find_phrase_time(phrase):
            if not phrase:
                return None
            tokens = [norm(t) for t in phrase.split() if norm(t)]
            if not tokens:
                return 0.0
            for i in range(len(nwords) - len(tokens) + 1):
                if all(nwords[i + j]['k'] == tokens[j] for j in range(len(tokens))):
                    return nwords[i]['s']
            for w in nwords:
                if w['k'] == tokens[0]:
                    return w['s']
            return None

        chosen = []
        for i, s in enumerate(slides):
            t = s.get('time')
            if t is None:
                t = find_phrase_time(s.get('trigger', ''))
            if t is not None and t > max_duration and len(chosen) >= 15:
                break
            chosen.append(s)
            if len(chosen) >= 32:
                break
        short_slides = chosen

    if not short_slides:
        short_slides = slides[:min(30, len(slides))]

    # Determine end time of the short
    last_slide_idx = slides.index(short_slides[-1])
    if last_slide_idx + 1 < len(slides):
        next_slide = slides[last_slide_idx + 1]
        next_t = next_slide.get('time')
        if next_t is None and words:
            tokens = [norm(t) for t in (next_slide.get('trigger', '')).split() if norm(t)]
            for i in range(len(nwords) - len(tokens) + 1):
                if all(nwords[i + j]['k'] == tokens[j] for j in range(len(tokens))):
                    next_t = nwords[i]['s']
                    break
        short_dur = min(max_duration, next_t if next_t and next_t > 30.0 else 60.0)
    else:
        short_dur = min(max_duration, 60.0)

    print(f"\n[Companion Short] Extracting opening hook short:")
    print(f" - Slides selected: {len(short_slides)} (slides 1 to {len(short_slides)})")
    print(f" - Short duration: {short_dur:.1f} seconds")

    # 2. Slice audio with fadeout
    bdir = pdir / 'build'
    bdir.mkdir(exist_ok=True, parents=True)
    full_audio = pdir / 'voice/mix.wav'
    if not full_audio.exists():
        full_audio = pdir / 'voice/narration.wav'
    
    short_audio = bdir / 'short_audio.wav'
    fade_start = max(0.0, short_dur - 0.6)
    run([
        'ffmpeg', '-y', '-v', 'error',
        '-ss', '0', '-t', f"{short_dur:.3f}",
        '-i', str(full_audio),
        '-af', f"afade=t=out:st={fade_start:.3f}:d=0.6",
        str(short_audio)
    ])

    # 3. Build vertical 1080x1920 (9:16) companion short viewer
    try:
        import images_util
        images_util.normalize_project_images(pdir)
    except Exception as e:
        print(f"[Companion Short] Note during image normalization: {e}")

    shutil.copy(ENGINE_DIR / 'slideshow.js', bdir / 'slideshow.js')
    
    # 1080x1920 (9:16) phone layout with matching cream background (#FBF6EF) and synced subtitles
    short_film = {
        'W': 1080,
        'H': 1920,
        'format': '9:16',
        'theme': {
            'background': '#FBF6EF',
            'font_family': "'Comic Sans MS', 'Comic Neue', cursive, sans-serif",
            'canvas_bg': '#FBF6EF'
        },
        'canvas': {
            'aspect_ratio': '9:16',
            'width': 1080,
            'height': 1920,
            'canvas_bg': '#FBF6EF',
            'border_radius': 0,
            'shadow': False,
            'blur_backdrop': False
        },
        'subtitles': cfg.get('subtitles', {'enabled': True}),
        'transitions': {'default_type': 'cut', 'fade_duration': 0.0, 'ken_burns_zoom': 1.0}
    }
    # Dedicated separate 1080x1920 (9:16) vertical images for companion short
    short_slides_built = []
    for s in short_slides:
        s_copy = dict(s)
        short_img_name = f"short_{s['name']}.png"
        short_img_path = pdir / 'images' / short_img_name
        if short_img_path.exists():
            s_copy['src'] = f"../images/{short_img_name}"
            print(f" -> Companion Short using dedicated 1080x1920 (9:16) image: {short_img_name}")
        else:
            s_copy['src'] = f"../images/{s['name']}.png"
        short_slides_built.append(s_copy)

    (bdir / 'film_short.js').write_text(f"window.FILM = {json.dumps(short_film, indent=2)};\n", encoding='utf-8')
    (bdir / 'slides_short.js').write_text(f"window.SLIDES = {json.dumps(short_slides_built, indent=2)};\n", encoding='utf-8')

    # Filter words for the short duration
    short_words = [w for w in words if w.get('e', 0.0) <= short_dur + 0.5]
    clocks_js = f"window.DUR = {short_dur:.3f};\nwindow.WORDS = {json.dumps(short_words)};\n"
    (bdir / 'clocks_short.js').write_text(clocks_js, encoding='utf-8')

    # HTML short page
    html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{cfg.get('title', 'Short')} - Companion Short</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #FBF6EF;
      font-family: 'Comic Sans MS', 'Comic Neue', cursive, sans-serif;
      user-select: none;
    }}
    #viewport {{
      position: absolute;
      inset: 0;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #FBF6EF;
    }}
    #slides-container {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      background: #FBF6EF;
    }}
  </style>
</head>
<body>
  <div id="viewport">
    <div id="slides-container"></div>
  </div>
  <script src="film_short.js"></script>
  <script src="slides_short.js"></script>
  <script src="clocks_short.js"></script>
  <script src="slideshow.js"></script>
</body>
</html>
"""
    short_html = bdir / 'page_short.html'
    short_html.write_text(html_content, encoding='utf-8')

    # 4. Render companion short MP4 (1080x1920, 9:16, 60fps)
    print(f"[Companion Short] Rendering vertical phone 1080x1920 (9:16) short ({short_dur:.1f}s) to {out_short_mp4}...")
    
    async def render_short():
        from playwright.async_api import async_playwright
        from common import launch_args
        import tempfile
        from render import open_page, render_worker
        
        fps = 60
        scale = 1.0
        crf = 16
        W, H = 1080, 1920
        total_frames = round(short_dur * fps)
        n_workers = max(1, min(int(os.environ.get('WB_WORKERS', '0')) or max(1, (os.cpu_count() or 4) // 2), 6))
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(**launch_args())
            with tempfile.TemporaryDirectory(dir=str(bdir)) as tmp:
                segs, jobs = [], []
                for k in range(n_workers):
                    seg = Path(tmp) / f"seg_{k:02d}.mp4"
                    segs.append(seg)
                    frame_range = range(total_frames * k // n_workers, total_frames * (k + 1) // n_workers)
                    jobs.append(render_worker(browser, short_html, W, H, scale, fps, frame_range, seg, crf))
                await asyncio.gather(*jobs)
                await browser.close()
                
                lst = Path(tmp) / 'list.txt'
                lst.write_text(''.join(f"file '{s.as_posix()}'\n" for s in segs), encoding='utf-8')
                
                args = [
                    'ffmpeg', '-y', '-v', 'error',
                    '-f', 'concat', '-safe', '0', '-i', str(lst),
                    '-i', str(short_audio),
                    '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
                    '-shortest', '-movflags', '+faststart',
                    str(out_short_mp4)
                ]
                run(args)

    asyncio.run(render_short())
    print(f"\n[Success] Companion Short Rendered: {out_short_mp4} ({short_dur:.1f}s, 720x1600, 60fps)")
    return out_short_mp4
