"""Validation gate: verifies slide images, word triggers, and timing constraints.
Enforces the retention pacing rule:
- Mostly 3 seconds, sometimes 2 seconds (range 1.8s - 3.8s, target average ~2.8s - 3.2s)
- Long-form deep dive (after 2 minutes): 5.0s to 6.0s (hard cap <= 6.0s)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from common import load_json, probe_duration
except ImportError:
    from tools.common import load_json, probe_duration


def check_project(pdir):
    pdir = Path(pdir)
    cfg = load_json(pdir / 'film.json')
    slides = load_json(pdir / 'slides.json')
    words_file = pdir / 'voice/words.json'
    
    errors, warnings = [], []
    
    # 1. Check audio
    narration_path = pdir / 'voice/narration.wav'
    if not narration_path.exists():
        errors.append("voice/narration.wav is missing. Run voice acquisition first.")
        dur = 0.0
    else:
        dur = probe_duration(narration_path)
        
    # Determine video mode: short vs long
    fmt = cfg.get('format', '720:1600')
    mode = cfg.get('mode', 'long' if fmt in ('16:9', '1920:1080', 'laptop', 'long') or dur > 180 else 'short')
    is_long = (mode == 'long' or fmt in ('16:9', '1920:1080', 'laptop') or dur > 180)
        
    # 2. Check words & timeline pacing
    words_data = load_json(words_file) if words_file.exists() else []
    if not words_data:
        warnings.append("voice/words.json not generated. Slide triggers will rely on approximate fallback.")
        all_words = []
    else:
        all_words = [x.get('w', '').lower() for x in words_data]

    # Calculate phrase timestamps & slide durations
    def norm(w):
        return ''.join(c for c in (w or '').lower() if c.isalnum())

    nwords = [{'k': norm(x.get('w', '')), 's': x.get('s', 0.0)} for x in words_data]

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

    timeline = []
    prev_time = 0.0
    for s in slides:
        t = s.get('time')
        if t is None:
            t = find_phrase_time(s.get('trigger', ''))
        if t is None or t < prev_time:
            t = prev_time
        timeline.append({'name': s['name'], 'start': t})
        prev_time = t

    # Check slide durations
    # Rules:
    # 1. First minute (or Short mode):
    #    - Mostly 3s, sometimes 2s (range: 1.8s to 3.8s)
    #    - Warn if < 1.8s (too fast/rushed)
    #    - Warn/violation if > 3.8s (dragging on too long)
    # 2. Long mode after 2 minutes:
    #    - 5.0s to 6.0s (hard cap <= 6.0s)
    pacing_violations = []
    first_min_durations = []

    for i in range(len(timeline)):
        start = timeline[i]['start']
        end = timeline[i + 1]['start'] if i + 1 < len(timeline) else dur
        duration = max(0.0, end - start)
        timeline[i]['duration'] = duration
        
        if start < 60.0 or not is_long:
            first_min_durations.append(duration)
            if duration < 1.8:
                warnings.append(
                    f"Slide '{timeline[i]['name']}' at {start:.1f}s lasts {duration:.1f}s (too short; target ~3s, sometimes ~2s, min 1.8s)."
                )
            elif duration > 3.8:
                pacing_violations.append(
                    f"Slide '{timeline[i]['name']}' at {start:.1f}s lasts {duration:.1f}s (> 3.8s; target ~3s, sometimes ~2s)."
                )
        else:
            if start < 120.0:
                max_allowed = 4.0
                phase_label = "minute 1 to 2 [bridge phase]"
            else:
                max_allowed = 6.0
                phase_label = "after 2 mins [deep-dive phase]"

            if duration > max_allowed:
                pacing_violations.append(
                    f"Slide '{timeline[i]['name']}' at {start:.1f}s lasts {duration:.1f}s (> {max_allowed:.1f}s max in {phase_label})."
                )

    # 3. Check slide images
    img_dir = pdir / 'images'
    for i, s in enumerate(slides):
        name = s['name']
        found = list(img_dir.glob(f"{name}.*")) if img_dir.exists() else []
        if not found:
            warnings.append(f"Slide '{name}' has no image file in images/ ({name}.png/.jpg).")
            
        trig = s.get('trigger', '')
        if trig and all_words:
            first_word = trig.split()[0].lower()
            if not any(first_word in w for w in all_words):
                warnings.append(f"Slide '{name}' trigger phrase '{trig}' not heard in spoken narration.")

    for pv in pacing_violations:
        warnings.append(f"[PACING] {pv}")

    # Check average duration in 1st minute / short
    avg_str = ""
    if first_min_durations:
        avg_dur = sum(first_min_durations) / len(first_min_durations)
        avg_str = f" | avg duration: {avg_dur:.2f}s ({len(first_min_durations)} slides, target ~2.8s-3.2s)"
        if avg_dur < 2.4:
            warnings.append(f"Average duration ({avg_dur:.2f}s) is too fast. Target is mostly 3s, sometimes 2s (~2.8s-3.2s avg).")
        elif avg_dur > 3.6:
            warnings.append(f"Average duration ({avg_dur:.2f}s) is too slow. Target is mostly 3s, sometimes 2s (~2.8s-3.2s avg).")
                
    mode_str = f"Long-Form 1920x1080 ({dur / 60:.1f} min)" if is_long else f"Short/Reel 720x1600 ({dur:.1f}s)"
    print(f"\n[Check] Validating '{cfg.get('slug', pdir.name)}' [{mode_str}]:")
    print(f"Total Slides: {len(slides)} | Audio Duration: {dur:.1f}s{avg_str}")
    for w in warnings:
        print(f"  [WARN]  {w}")
    for e in errors:
        print(f"  [ERROR] {e}")
        
    if not errors and not pacing_violations:
        print("  [SUCCESS] All critical checks and pacing rules passed (mostly 3s, sometimes 2s).")
    elif not errors:
        print("  [PASSED WITH PACING WARNINGS] Audio and images exist; review pacing warnings above.")
    return len(errors) == 0
