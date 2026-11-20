"""Validation gate: verifies slide images, word triggers, and timing constraints."""
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

    # Check slide durations (rule: no slide > 4.0s)
    pacing_violations = []
    for i in range(len(timeline)):
        start = timeline[i]['start']
        end = timeline[i + 1]['start'] if i + 1 < len(timeline) else dur
        duration = max(0.0, end - start)
        timeline[i]['duration'] = duration
        if duration > 4.0:
            pacing_violations.append(f"Slide '{timeline[i]['name']}' lasts {duration:.1f}s (> 4.0s maximum allowed).")

    # 3. Check slide images
    img_dir = pdir / 'images'
    for i, s in enumerate(slides):
        name = s['name']
        found = list(img_dir.glob(f"{name}.*")) if img_dir.exists() else []
        if not found:
            warnings.append(f"Slide '{name}' has no image file in images/ ({name}.png/.jpg).")
            
        # Check trigger word
        trig = s.get('trigger', '')
        if trig and all_words:
            first_word = trig.split()[0].lower()
            if not any(first_word in w for w in all_words):
                warnings.append(f"Slide '{name}' trigger phrase '{trig}' not heard in spoken narration.")

    for pv in pacing_violations:
        warnings.append(f"[PACING] {pv}")
                
    print(f"\n[Check] Validating '{cfg.get('slug', pdir.name)}':")
    print(f"Total Slides: {len(slides)} | Audio Duration: {dur:.1f}s")
    for w in warnings:
        print(f"  [WARN]  {w}")
    for e in errors:
        print(f"  [ERROR] {e}")
        
    if not errors:
        print("  [SUCCESS] All critical checks passed.")
    return len(errors) == 0
