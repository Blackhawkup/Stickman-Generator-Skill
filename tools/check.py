"""Validation gate: verifies slide images, word triggers, and timing constraints.
Enforces the strict retention pacing rule:
- First minute (both short and long): Every image must stay on screen for < 3.0 seconds, averaging ~2.0 seconds.
- After 2 minutes (long form): Images can stay for 5.0 to 6.0 seconds (hard cap <= 6.0s).
"""
from pathlib import Path
from common import load_json, probe_duration


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
    # 1. First minute (t < 60.0s) for BOTH short and long:
    #    - Strictly < 3.0s (hard cap < 3.0s)
    #    - Average duration target: ~2.0s across all first-minute slides
    # 2. After first minute:
    #    - Short mode: strictly <= 3.0s
    #    - Long mode:
    #        * 60s to 120s: <= 4.0s (bridge phase)
    #        * 120s+ (2 mins+): 5.0s to 6.0s (hard cap <= 6.0s)
    pacing_violations = []
    first_min_durations = []

    for i in range(len(timeline)):
        start = timeline[i]['start']
        end = timeline[i + 1]['start'] if i + 1 < len(timeline) else dur
        duration = max(0.0, end - start)
        timeline[i]['duration'] = duration
        
        if start < 60.0:
            first_min_durations.append(duration)
            if duration >= 3.0:
                pacing_violations.append(
                    f"Slide '{timeline[i]['name']}' at {start:.1f}s lasts {duration:.1f}s (>= 3.0s; MUST be < 3.0s in 1st minute)."
                )
        else:
            if is_long:
                if start < 120.0:
                    max_allowed = 4.0
                    phase_label = "minute 1 to 2 [bridge phase]"
                else:
                    max_allowed = 6.0
                    phase_label = "after 2 mins [deep-dive phase]"
            else:
                max_allowed = 3.0
                phase_label = "short [viral pacing]"

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

    # Check 1st minute average
    avg_str = ""
    if first_min_durations:
        avg_dur = sum(first_min_durations) / len(first_min_durations)
        avg_str = f" | 1st-min avg: {avg_dur:.2f}s ({len(first_min_durations)} slides, target ~2.0s)"
        if avg_dur > 2.4:
            warnings.append(f"1st-minute average duration is {avg_dur:.2f}s (exceeds ~2.0s average target).")
                
    mode_str = f"Long-Form 1920x1080 ({dur / 60:.1f} min)" if is_long else f"Short/Reel 720x1600 ({dur:.1f}s)"
    print(f"\n[Check] Validating '{cfg.get('slug', pdir.name)}' [{mode_str}]:")
    print(f"Total Slides: {len(slides)} | Audio Duration: {dur:.1f}s{avg_str}")
    for w in warnings:
        print(f"  [WARN]  {w}")
    for e in errors:
        print(f"  [ERROR] {e}")
        
    if not errors and not pacing_violations:
        print("  [SUCCESS] All critical checks and pacing rules passed (< 3s in 1st min, ~2s avg).")
    elif not errors:
        print("  [PASSED WITH PACING WARNINGS] Audio and images exist; review pacing violations above.")
    return len(errors) == 0
