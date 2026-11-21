"""Audio mixing: voice narration + ambient musical bed + -14 LUFS loudness mastering.
Marker drawing sounds have been completely removed.
"""
import json, re, subprocess
from pathlib import Path
import numpy as np
from scipy import signal
from common import load_json, run, ffmpeg, IS_WIN

SR = 48000
MIDI = lambda m: 440.0 * 2 ** ((m - 69) / 12.0)
rng = np.random.default_rng(3)


def ffmpeg_decode(path, channels=1):
    r = run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ac', str(channels), '-ar', str(SR), '-'], capture_output=True)
    return np.frombuffer(r.stdout, np.float32).copy()


def _pad(freqs, dur, vel):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for f in freqs:
        for det in (-6, 0, 6):
            ff = f * 2 ** (det / 1200.0)
            x += sum(np.sin(2 * np.pi * ff * k * t + k) / k ** 1.8 for k in (1, 2, 3)) / 3
    e = np.ones(n)
    na = min(n, int(0.9 * SR))
    nr = min(n, int(1.2 * SR))
    e[:na] = np.sin(np.linspace(0, np.pi / 2, na)) ** 2
    e[-nr:] *= np.cos(np.linspace(0, np.pi / 2, nr)) ** 2
    return x * e * vel / len(freqs) ** 0.7


def _pluck(f, dur, vel, bright=0.8):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ratios = [1, 2, 3, 4.2]
    amps = [1.0, 0.42 * bright, 0.2 * bright, 0.1 * bright]
    taus = [0.55, 0.32, 0.2, 0.12]
    x = sum(a * np.sin(2 * np.pi * f * r * t + 0.3 * i) * np.exp(-t / (tau * dur / 1.2)) for i, (r, a, tau) in enumerate(zip(ratios, amps, taus)))
    return x * np.minimum(1, t / 0.003) * vel * 0.5


def composed_ambient_bed(N, key=50, bpm=84):
    """Synthesizes a soft, harmonic ambient backing track."""
    out = np.zeros((N + SR * 3, 2))
    beat, bar = 60 / bpm, 240 / bpm
    triads = [(0, 4, 7), (7, 11, 14), (9, 12, 16), (5, 9, 12)]

    def put(sig, t, pan=0.0):
        i = int(t * SR)
        if i >= out.shape[0]:
            return
        s = sig[:out.shape[0] - i]
        out[i:i + len(s), 0] += s * (1 - max(0, pan))
        out[i:i + len(s), 1] += s * (1 + min(0, pan))

    t, k = 0.0, 0
    while t < N / SR:
        tri = [key + x for x in triads[k % 4]]
        put(_pad([MIDI(n) for n in tri], bar + 0.6, 0.22), t)
        up = [n + 12 for n in tri] + [tri[0] + 24]
        for i, idx in enumerate([0, 1, 2, 1, 0, 1, 2, 3]):
            put(_pluck(MIDI(up[idx]), 1.1, 0.2 * (1.0 if i % 4 == 0 else 0.7)), t + i * beat / 2, -0.15 if i % 2 else 0.15)
        t += bar
        k += 1
    x = out[:N]
    ir = rng.standard_normal(int(1.3 * SR)) * np.exp(-6.9 * np.arange(int(1.3 * SR)) / (1.2 * SR))
    for c in range(2):
        wet = signal.fftconvolve(x[:, c], ir, 'full')[:N]
        x[:, c] = x[:, c] * 0.88 + wet / (np.abs(ir).max() * 40)
    return x


def measure_lufs(path):
    null_dev = 'NUL' if IS_WIN else '-'
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-af', 'ebur128=framelog=quiet', '-f', 'null', null_dev], capture_output=True, text=True)
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r.stderr)[-1])


def auto_select_music(pdir, topic_str=""):
    """Selects an ambient music track dynamically from the 12 curated tracks:
    curious, investigation, mystery, sneaky, playful, quirky, upbeat, reflective, deep_mystery, thoughtful, light, comedy.
    Avoids recently used tracks in completed_topics.json and matches topic mood.
    """
    catalog_path = Path(__file__).resolve().parent.parent / 'audio' / 'music' / 'music_catalog.json'
    catalog = load_json(catalog_path) if catalog_path.exists() else []
    all_tracks = [t['id'] for t in catalog] if catalog else [
        'curious', 'investigation', 'mystery', 'sneaky', 'playful', 'quirky',
        'upbeat', 'reflective', 'deep_mystery', 'thoughtful', 'light', 'comedy'
    ]
    
    # Check completed topics for recently used tracks
    topics_file = Path(__file__).resolve().parent.parent / 'topics' / 'completed_topics.json'
    completed = load_json(topics_file) if topics_file.exists() else []
    recent_tracks = [x.get('music') for x in completed[-4:] if x.get('music')]
    
    # Analyze topic/script keywords for mood
    search_text = (topic_str or "").lower()
    pdir = Path(pdir)
    if not search_text:
        film_file = pdir / 'film.json'
        if film_file.exists():
            cfg = load_json(film_file)
            search_text = (cfg.get('topic') or cfg.get('title') or cfg.get('slug') or '').lower()
        script_file = pdir / 'script.md'
        if script_file.exists():
            search_text += " " + script_file.read_text(encoding='utf-8')[:300].lower()
            
    # Mood candidate mappings
    candidates = []
    if any(k in search_text for k in ('bias', 'fallacy', 'paradox', 'trick', 'irrational', 'brain', 'illusion', 'sunk cost', 'spotlight')):
        candidates = ['curious', 'sneaky', 'quirky', 'thoughtful']
    elif any(k in search_text for k in ('study', 'experiment', 'research', 'evidence', 'scientist', 'test', 'data', 'laboratory')):
        candidates = ['investigation', 'thoughtful', 'deep_mystery']
    elif any(k in search_text for k in ('mystery', 'secret', 'hidden', 'dark', 'unexplained', 'bizarre', 'strange')):
        candidates = ['mystery', 'deep_mystery', 'investigation']
    elif any(k in search_text for k in ('funny', 'humor', 'embarrass', 'clumsy', 'mistake', 'awkward', 'spill', 'pratfall', 'laugh', 'coffee')):
        candidates = ['playful', 'comedy', 'quirky', 'sneaky']
    elif any(k in search_text for k in ('growth', 'lesson', 'decision', 'mindset', 'life', 'habit', 'relationship', 'future', 'success')):
        candidates = ['reflective', 'upbeat', 'light', 'thoughtful']
    else:
        candidates = ['curious', 'thoughtful', 'reflective', 'investigation', 'playful', 'quirky']
        
    # Filter out recent tracks to ensure dynamic rotation
    fresh_candidates = [c for c in candidates if c not in recent_tracks and c in all_tracks]
    if fresh_candidates:
        chosen = fresh_candidates[0]
    else:
        fresh_all = [t for t in all_tracks if t not in recent_tracks]
        chosen = fresh_all[0] if fresh_all else candidates[0]
        
    print(f"[Music] Dynamic auto-selected soundtrack track: '{chosen}' (matching mood, avoiding recent repeats: {recent_tracks})")
    return chosen


def resolve_music_path(music_spec):
    if not music_spec or music_spec == 'none':
        return None
    if music_spec == 'composed':
        return 'composed'
    lib_dir = Path(__file__).resolve().parent.parent / 'audio' / 'music'
    cand1 = lib_dir / f"{music_spec}.mp3"
    if cand1.exists():
        return cand1
    cand2 = Path(music_spec).expanduser()
    if cand2.exists():
        return cand2
    return None


def mix_audio(pdir, target_lufs=-14.0):
    pdir = Path(pdir)
    cfg = load_json(pdir / 'film.json')
    narration_path = pdir / 'voice/narration.wav'
    if not narration_path.exists():
        print("[Mix] Warning: No voice/narration.wav found. Skipping audio mix.")
        return
        
    vo = ffmpeg_decode(narration_path)
    N = len(vo)
    
    out = np.zeros((N, 2), np.float32)
    out[:, 0] += vo
    out[:, 1] += vo
    
    music_spec = cfg.get('music', 'auto')
    if music_spec in ('auto', 'dynamic', None, ''):
        chosen_track = auto_select_music(pdir)
        cfg['music'] = chosen_track
        save_json(pdir / 'film.json', cfg)
        music_spec = chosen_track
        
    m_target = resolve_music_path(music_spec)
    
    if m_target:
        if m_target == 'composed':
            bed = composed_ambient_bed(N)
        else:
            raw = ffmpeg_decode(m_target, 2).reshape(-1, 2)
            bed = np.vstack([raw] * (N // len(raw) + 1))[:N]
            
        # Sidechain voice ducking
        fade = np.ones(N, np.float32)
        fi, fo = min(N, int(0.6 * SR)), min(N, int(2.5 * SR))
        fade[:fi] = np.linspace(0, 1, fi)
        fade[N - fo:] = np.linspace(1, 0, fo)
        win = int(0.25 * SR)
        venv = signal.fftconvolve(np.abs(vo), np.ones(win) / win, mode='same')
        venv = venv / (venv.max() + 1e-9)
        duck = 1 - 0.55 * np.clip(venv * 6, 0, 1)
        win2 = int(0.12 * SR)
        duck = signal.fftconvolve(duck, np.ones(win2) / win2, mode='same')
        
        music_vol_db = cfg.get('music_db', -26)
        bed = bed * (fade * duck)[:, None] * 10 ** (music_vol_db / 20) / (np.sqrt(np.mean(bed ** 2)) + 1e-9)
        out += bed.astype(np.float32)
        
    out /= max(1.0, np.abs(out).max() / 0.95)
    
    vdir = pdir / 'voice'
    tmp = vdir / '_mix_pre.wav'
    run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', '-', '-c:a', 'pcm_s24le', str(tmp)], input=out.tobytes())
    
    gain = target_lufs - measure_lufs(tmp)
    final_out = vdir / 'mix.wav'
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(tmp), '-af', f'volume={gain:.2f}dB,alimiter=limit=0.84:level=false:attack=3:release=40', '-ar', str(SR), '-c:a', 'pcm_s24le', str(final_out)])
    tmp.unlink()
    
    final_lufs = measure_lufs(final_out)
    print(f"\n[Mix] Final soundtrack mastered at {final_lufs:.1f} LUFS -> {final_out}")
    return final_out
