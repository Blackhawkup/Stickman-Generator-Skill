"""High-speed frame-by-frame renderer using Playwright CDP and FFmpeg pipes.
Supports 1920x1080 (laptop / long form) and 720x1600 (phone / short / reel).
"""
import asyncio, base64, os, subprocess, tempfile
from pathlib import Path
from common import launch_args, run, die, load_json


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


async def open_page(browser, html_path, W, H):
    errs = []
    ctx = await browser.new_context(viewport={'width': W, 'height': H})
    pg = await ctx.new_page()
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    await pg.goto(Path(html_path).resolve().as_uri())
    
    # Wait for all slide images and clocks to be ready
    for _ in range(600):
        if errs:
            break
        if await pg.evaluate('window.__READY===true'):
            break
        await asyncio.sleep(0.1)
    if errs:
        die("Slideshow page encountered an error:\n  " + "\n  ".join(errs))
    cdp = await ctx.new_cdp_session(pg)
    return pg, cdp, errs


async def capture_frame(cdp, W, H, scale=1.0):
    args = {'format': 'png', 'optimizeForSpeed': True, 'captureBeyondViewport': False}
    if scale != 1.0:
        args['clip'] = {'x': 0, 'y': 0, 'width': W, 'height': H, 'scale': scale}
    res = await cdp.send('Page.captureScreenshot', args)
    return base64.b64decode(res['data'])


async def render_worker(browser, html_path, W, H, scale, fps, frames, segment_path, crf):
    pg, cdp, _ = await open_page(browser, html_path, W, H)
    ff = subprocess.Popen([
        'ffmpeg', '-y', '-v', 'error',
        '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'png', '-i', '-',
        '-c:v', 'libx264', '-preset', 'faster', '-crf', str(crf),
        '-pix_fmt', 'yuv420p', str(segment_path)
    ], stdin=subprocess.PIPE)
    
    for i in frames:
        t = i / fps
        await pg.evaluate(f'window.__seek({t:.4f})')
        ff.stdin.write(await capture_frame(cdp, W, H, scale))
        
    ff.stdin.close()
    ff.wait()
    await pg.close()


async def render_slideshow(pdir, out_mp4, fps=60, scale=1.0, crf=16, audio_path=None):
    from playwright.async_api import async_playwright
    pdir = Path(pdir)
    cfg = load_json(pdir / 'film.json')
    fmt = cfg.get('format', '720:1600')
    W, H = get_dimensions(fmt)
    html_path = pdir / 'build/page.html'
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(**launch_args())
        pg, _, _ = await open_page(browser, html_path, W, H)
        dur = await pg.evaluate('window.CLOCK.dur || 30.0')
        await pg.close()
        
        total_frames = round(dur * fps)
        n_workers = max(1, min(int(os.environ.get('WB_WORKERS', '0')) or max(1, (os.cpu_count() or 4) // 2), 6))
        print(f"\n[Render] Rendering {total_frames} frames ({dur:.1f}s, {W}x{H}) at {fps} fps across {n_workers} workers...")
        
        with tempfile.TemporaryDirectory(dir=str(pdir / 'build')) as tmp:
            segs, jobs = [], []
            for k in range(n_workers):
                seg = Path(tmp) / f"seg_{k:02d}.mp4"
                segs.append(seg)
                frame_range = range(total_frames * k // n_workers, total_frames * (k + 1) // n_workers)
                jobs.append(render_worker(browser, html_path, W, H, scale, fps, frame_range, seg, crf))
                
            await asyncio.gather(*jobs)
            await browser.close()
            
            # Concat segments
            lst = Path(tmp) / 'list.txt'
            lst.write_text(''.join(f"file '{s.as_posix()}'\n" for s in segs), encoding='utf-8')
            
            args = ['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(lst)]
            if audio_path and Path(audio_path).exists():
                args += ['-i', str(audio_path), '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '256k', '-shortest']
            else:
                args += ['-map', '0:v']
            args += ['-c:v', 'copy', '-movflags', '+faststart', str(out_mp4)]
            run(args)
            
    print(f"\n[Success] Final Video Rendered: {out_mp4} ({dur:.1f} s, {W}x{H})")


def export_video(pdir, out_mp4, fps=60, preview=False):
    pdir = Path(pdir)
    audio = pdir / 'voice/mix.wav'
    if not audio.exists():
        audio = pdir / 'voice/narration.wav'
    scale = 0.5 if preview else 1.0
    crf = 24 if preview else 16
    fps = 30 if preview else fps
    Path(out_mp4).parent.mkdir(exist_ok=True, parents=True)
    asyncio.run(render_slideshow(pdir, out_mp4, fps=fps, scale=scale, crf=crf, audio_path=audio))
