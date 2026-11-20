"""Downloads curated royalty-free explainer background tracks and builds music_catalog.json."""
import json, time, urllib.request
from pathlib import Path

music_dir = Path('slideshow-workflow/audio/music')
music_dir.mkdir(parents=True, exist_ok=True)

tracks = [
    ('curious', 'Scheming%20Weasel%20faster.mp3', 'Curious and mischievous pizzicato strings, ideal for cognitive biases and psychology paradoxes.'),
    ('investigation', 'Investigations.mp3', 'Thoughtful investigative detective vibraphone and bass, perfect for scientific studies.'),
    ('mystery', 'Hidden%20Agenda.mp3', 'Subtle tense mystery with ticking rhythm, great for surprising plot twists.'),
    ('sneaky', 'Sneaky%20Snitch.mp3', 'Playful tip-toe bassoon and clarinet, ideal for funny human flaws and mistakes.'),
    ('playful', 'Fluffing%20a%20Duck.mp3', 'Lighthearted bouncy cartoon comedy, great for everyday awkward situations.'),
    ('quirky', 'Quirky%20Dog.mp3', 'Fun, off-beat, energetic acoustic rhythm with upbeat whistling.'),
    ('upbeat', 'Carefree.mp3', 'Warm, cheerful, positive acoustic guitar and bells, ideal for hopeful conclusions.'),
    ('reflective', 'Opportunity%20Walks.mp3', 'Smooth, introspective, calm walking tempo for thoughtful reflections.'),
    ('tech_intrigue', 'Cipher.mp3', 'Modern subtle electronic pulse, great for data, tech, and spreadsheets.'),
    ('deep_mystery', 'Comfortable%20Mystery.mp3', 'Soft low-key detective jazz bass, ideal for deep unexplained questions.'),
    ('thoughtful', 'The%20Builder.mp3', 'Steady productive acoustic beat, great for step-by-step explanations.'),
    ('light', 'Wallpaper.mp3', 'Neutral gentle ambient background, stays out of the way of spoken voice.'),
    ('comedy', 'Monkeys%20Spinning%20Monkeys.mp3', 'Wild whimsical fun rhythm, great for chaotic group dynamics.'),
    ('suspense', 'Danse%20Morialta.mp3', 'Gradually rising tension, great for escalation and conflict.'),
    ('smooth_groove', 'Fretless.mp3', 'Relaxed subtle groove, modern clean presentation.')
]

catalog = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

print(f"[Music] Downloading {len(tracks)} curated royalty-free tracks to {music_dir}...")
for slug, filename, desc in tracks:
    target_path = music_dir / f'{slug}.mp3'
    if target_path.exists() and target_path.stat().st_size > 50000:
        print(f" -> Already cached: {slug}.mp3 ({target_path.stat().st_size // 1024} KB)")
        catalog.append({'id': slug, 'file': str(target_path.as_posix()), 'mood': slug, 'description': desc, 'recommended_db': -26})
        continue
    url = f"https://incompetech.com/music/royalty-free/mp3-royaltyfree/{filename}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            target_path.write_bytes(data)
            print(f" -> Downloaded {slug}.mp3 ({len(data) // 1024} KB)")
            catalog.append({'id': slug, 'file': str(target_path.as_posix()), 'mood': slug, 'description': desc, 'recommended_db': -26})
        time.sleep(0.3)
    except Exception as e:
        print(f" [!] Error downloading {slug} from {url}: {e}")

catalog_path = music_dir / 'music_catalog.json'
catalog_path.write_text(json.dumps(catalog, indent=2), encoding='utf-8')
print(f"\n[Success] Music catalog created: {len(catalog)} tracks saved to {catalog_path}")
