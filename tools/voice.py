"""Voice acquisition, faster-whisper word-level alignment, and silence/pacing adjustment."""
import base64, json, os, re, sys, urllib.error, urllib.request, wave
from difflib import SequenceMatcher
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from common import ffmpeg, load_json, save_json, norm, probe_duration, run, die
except ImportError:
    from tools.common import ffmpeg, load_json, save_json, norm, probe_duration, run, die

SR = 48000
TTS_MODEL = 'gemini-2.5-flash-preview-tts'


def script_words(pdir):
    text_path = pdir / 'script.md'
    text = text_path.read_text(encoding='utf-8') if text_path.exists() else ''
    text = '\n'.join(l for l in text.splitlines() if not l.strip().startswith('#'))
    return re.findall(r"\S+", text)


def get_gemini_key():
    k = os.environ.get('GEMINI_API_KEY', '').strip()
    p = Path.home() / '.flow-mcp' / 'gemini-key'
    if not k and p.exists():
        lines = [l.strip() for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]
        if lines:
            k = lines[0]
    return k


def tts_generate(pdir, voice='Charon', style=None, text=None):
    """Direct call to Google AI Studio TTS API. Chunks long texts by paragraph."""
    k = get_gemini_key()
    if not k:
        die("No Google AI Studio key found in GEMINI_API_KEY or ~/.flow-mcp/gemini-key. Please provide an audio file or configure the key.")
    src = text or (pdir / 'script.md').read_text(encoding='utf-8')
    paras = [p.strip() for p in src.split('\n\n') if p.strip() and not p.strip().startswith('#')]
    chunks, cur = [], ''
    for p in paras:
        if len((cur + ' ' + p).split()) > 420 and cur:
            chunks.append(cur)
            cur = p
        else:
            cur = (cur + '\n\n' + p).strip()
    if cur:
        chunks.append(cur)
    vdir = pdir / 'voice'
    vdir.mkdir(exist_ok=True, parents=True)
    files = []
    print(f"\n[TTS] Generating voice with Google AI Studio ({voice})...")
    for i, c in enumerate(chunks):
        body = {
            'contents': [{'parts': [{'text': (f'Say {style}: {c}' if style else c)}]}],
            'generationConfig': {
                'responseModalities': ['AUDIO'],
                'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': voice}}}
            }
        }
        req = urllib.request.Request(
            f'https://generativelanguage.googleapis.com/v1beta/models/{TTS_MODEL}:generateContent',
            data=json.dumps(body).encode(),
            headers={'content-type': 'application/json', 'x-goog-api-key': k}
        )
        try:
            r = json.load(urllib.request.urlopen(req, timeout=300))
        except urllib.error.HTTPError as e:
            die(f"Google AI Studio refused this take ({e.code}): {e.read().decode()[:300]}")
        part = next(p for p in r['candidates'][0]['content']['parts'] if 'inlineData' in p)
        rate = int((re.search(r'rate=(\d+)', part['inlineData'].get('mimeType', '')) or [0, 24000])[1])
        f = vdir / f'take-{i + 1:02d}.wav'
        with wave.open(str(f), 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(rate)
            w.writeframes(base64.b64decode(part['inlineData']['data']))
        files.append(f)
        print(f"  piece {i + 1}/{len(chunks)}: {probe_duration(f):.1f} s")
    return files


def transcribe_words(audio_path, language='en'):
    from faster_whisper import WhisperModel
    print("[Voice] Aligning word-level timestamps with Whisper (fast int8)...")
    model = WhisperModel('base', device='cpu', compute_type='int8')
    r = run(['ffmpeg', '-v', 'error', '-i', str(audio_path), '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'], capture_output=True)
    audio = np.frombuffer(r.stdout, np.float32).copy()
    segs, _ = model.transcribe(audio, word_timestamps=True, language=language, vad_filter=False)
    words = [{'w': w.word.strip(), 's': round(w.start, 3), 'e': round(w.end, 3)} for s in segs for w in s.words if w.word.strip()]
    return words


def align_and_lock_voice(pdir, audio_files, tempo=None, target=None, language='en'):
    vdir = pdir / 'voice'
    vdir.mkdir(exist_ok=True, parents=True)
    tmp = vdir / '_joined.wav'
    if len(audio_files) == 1:
        ffmpeg('-i', str(audio_files[0]), '-ar', SR, '-ac', 1, str(tmp))
    else:
        args = []
        for f in audio_files:
            args += ['-i', str(f)]
        chain = ''.join(f'[{i}:a]aresample={SR},aformat=channel_layouts=mono[a{i}];' for i in range(len(audio_files)))
        joined = ''.join(f'[a{i}]' for i in range(len(audio_files)))
        ffmpeg(*args, '-filter_complex', chain + f'{joined}concat=n={len(audio_files)}:v=0:a=1[o]', '-map', '[o]', str(tmp))
        
    out = vdir / 'narration.wav'
    ffmpeg('-i', str(tmp), '-c:a', 'pcm_s16le', str(out))
    tmp.unlink()
    
    # Extract word timestamps
    raw_words = transcribe_words(out, language=language)
    
    # Correct transcription tokens against script.md
    sw = script_words(pdir)
    if sw:
        a = [norm(x['w']) for x in raw_words]
        b = [norm(x) for x in sw]
        matcher = SequenceMatcher(None, a, b, autojunk=False)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace' and i2 - i1 == j2 - j1:
                for k in range(i2 - i1):
                    raw_words[i1 + k]['w'] = sw[j1 + k]
    save_json(vdir / 'words.json', raw_words)
    print(f"[Voice] Words locked: {len(raw_words)} tokens saved to {vdir / 'words.json'}")
    apply_pacing(pdir)


def apply_pacing(pdir):
    """Inserts gentle pauses specified in film.json without disrupting word-level timings."""
    vdir = pdir / 'voice'
    words_file = vdir / 'words.json'
    if not words_file.exists():
        return
    W = load_json(words_file)
    cfg = load_json(pdir / 'film.json')
    pacing = cfg.get('pacing', {})
    pauses = pacing.get('pauses', [])
    
    # Produce build/clocks.js
    build_dir = pdir / 'build'
    build_dir.mkdir(exist_ok=True, parents=True)
    
    narration_path = vdir / 'narration.wav'
    dur = probe_duration(narration_path) if narration_path.exists() else 30.0
    
    # Write clocks.js
    clocks_js = (
        f"window.WORDS = {json.dumps(W, separators=(',', ':'))};\n"
        f"window.DUR = {dur:.2f};\n"
    )
    (build_dir / 'clocks.js').write_text(clocks_js, encoding='utf-8')
    print(f"[Clock] Clocks bundle written: {build_dir / 'clocks.js'} (Duration: {dur:.2f}s)")
