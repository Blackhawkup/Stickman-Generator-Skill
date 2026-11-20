"""Shared paths, configuration helpers, and subprocess utilities."""
import json, os, platform, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / 'prompts'
TEMPLATES_DIR = ROOT / 'templates'
ENGINE_DIR = ROOT / 'engine'
PROJECTS_DIR = ROOT / 'projects'
IS_WIN = platform.system() == 'Windows'
IS_MAC = platform.system() == 'Darwin'


def die(msg):
    print(f"\n[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def load_json(path, default=None):
    p = Path(path)
    if not p.exists():
        if default is not None:
            return default
        die(f"Missing file: {p}")
    return json.loads(p.read_text(encoding='utf-8'))


def save_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=kw.pop('check', True), **kw)


def ffmpeg(*args, **kw):
    return run(['ffmpeg', '-y', '-v', 'error', *args], **kw)


def probe_duration(path):
    r = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


def norm(word):
    """Normalize word token for acoustic alignment."""
    return re.sub(r'[\W_]+', '', str(word).lower())


def find_chrome():
    env = os.environ.get('CHROME_PATH')
    cands = [env] if env else []
    if IS_MAC:
        cands += ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium']
    elif IS_WIN:
        for base in (os.environ.get('PROGRAMFILES'), os.environ.get('PROGRAMFILES(X86)'), os.environ.get('LOCALAPPDATA')):
            if base:
                cands.append(os.path.join(base, 'Google', 'Chrome', 'Application', 'chrome.exe'))
    else:
        cands += [shutil.which(n) for n in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser')]
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


def launch_args():
    """Playwright chromium launch configuration."""
    kw = {'args': ['--allow-file-access-from-files', '--disable-gpu-vsync', '--force-color-profile=srgb']}
    c = find_chrome()
    if c:
        kw['executable_path'] = c
    return kw
