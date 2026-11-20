#!/usr/bin/env python3
"""Unified CLI for the Timed Slideshow Explainer system.

Commands:
  python tools/cli.py new <slug> [--format 16:9|9:16|1:1]
  python tools/cli.py prompts <project>
  python tools/cli.py tts <project> [--voice Charon]
  python tools/cli.py voice <project> <audio.wav>
  python tools/cli.py images <project>
  python tools/cli.py mix <project>
  python tools/cli.py check <project>
  python tools/cli.py build <project>
  python tools/cli.py preview <project>
  python tools/cli.py render <project>
  python tools/cli.py auto <project> [--voice Charon]
"""
import argparse, json, os, platform, shutil, sys
from pathlib import Path

# Auto-reexec in venv if available
VENV_PY = Path(os.environ.get('WHITEBOARD_HOME', str(Path.home() / 'WhiteboardFilms'))) / '.tools' / 'venv' / ('Scripts/python.exe' if platform.system() == 'Windows' else 'bin/python')
if os.environ.get('_VENV_ACTIVE') != '1' and VENV_PY.exists():
    try:
        import faster_whisper
    except ImportError:
        import subprocess
        env = os.environ.copy()
        env['_VENV_ACTIVE'] = '1'
        sys.exit(subprocess.call([str(VENV_PY), str(Path(__file__).resolve())] + sys.argv[1:], env=env))

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, TEMPLATES_DIR, PROJECTS_DIR, load_json, save_json, die


def resolve_project(name):
    p = Path(name).expanduser()
    if p.is_dir() and (p / 'film.json').exists():
        return p.resolve()
    p = PROJECTS_DIR / name
    if (p / 'film.json').exists():
        return p
    die(f"Cannot find project '{name}'. Expected folder with film.json at {p}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('help', '-h', '--help'):
        print(__doc__)
        return

    cmd = sys.argv[1]
    rest = sys.argv[2:]
    parser = argparse.ArgumentParser(prog=f"cli.py {cmd}")

    if cmd == 'new':
        parser.add_argument('slug')
        parser.add_argument('--format', default='16:9', choices=['16:9', '9:16', '1:1'])
        args = parser.parse_args(rest)
        dest = PROJECTS_DIR / args.slug
        if dest.exists():
            die(f"Project '{args.slug}' already exists at {dest}")
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copytree(TEMPLATES_DIR, dest, dirs_exist_ok=True)
        cfg = load_json(dest / 'film.json')
        cfg['slug'] = args.slug
        cfg['format'] = args.format
        save_json(dest / 'film.json', cfg)
        for d in ('images', 'voice', 'out', 'build'):
            (dest / d).mkdir(exist_ok=True)
        print(f"\n[Project Created] {dest}")

    elif cmd == 'prompts':
        parser.add_argument('project')
        args = parser.parse_args(rest)
        import prompts
        prompts.build_prompts(resolve_project(args.project))

    elif cmd == 'intake':
        parser.add_argument('project')
        parser.add_argument('pairs', nargs='+')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        img_dir = pdir / 'images'
        img_dir.mkdir(exist_ok=True)
        for pair in args.pairs:
            name, path = pair.split('=', 1)
            src = Path(path).expanduser()
            if not src.exists():
                die(f"Image not found: {src}")
            dst = img_dir / f"{name}{src.suffix.lower()}"
            shutil.copy(src, dst)
            print(f" -> Imported {dst.name}")
        print(f"\n[Intake] Successfully imported {len(args.pairs)} images.")

    elif cmd == 'tts':
        parser.add_argument('project')
        parser.add_argument('--voice', default='Charon')
        parser.add_argument('--style', default='warm, confident YouTube explainer')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        import voice
        files = voice.tts_generate(pdir, voice=args.voice, style=args.style)
        voice.align_and_lock_voice(pdir, files)

    elif cmd == 'voice':
        parser.add_argument('project')
        parser.add_argument('audio', nargs='+')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        import voice
        voice.align_and_lock_voice(pdir, [Path(x).expanduser() for x in args.audio])

    elif cmd == 'mix':
        parser.add_argument('project')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        import mix
        mix.mix_audio(pdir)

    elif cmd == 'build':
        parser.add_argument('project')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        import build
        build.build_page(pdir)

    elif cmd == 'check':
        parser.add_argument('project')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        import check, build
        build.build_page(pdir)
        check.check_project(pdir)

    elif cmd in ('preview', 'render'):
        parser.add_argument('project')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        import check, mix, build, render
        build.build_page(pdir)
        mix.mix_audio(pdir)
        if not check.check_project(pdir):
            print("\n[Notice] Proceeding despite warnings...")
        slug = load_json(pdir / 'film.json').get('slug', pdir.name)
        out_dir = pdir / 'out'
        out_dir.mkdir(exist_ok=True)
        if cmd == 'preview':
            render.export_video(pdir, out_dir / 'preview.mp4', preview=True)
        else:
            render.export_video(pdir, out_dir / f"{slug}.mp4", preview=False)

    elif cmd == 'images':
        parser.add_argument('project')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        slug = load_json(pdir / 'film.json').get('slug', pdir.name)
        script = Path(__file__).resolve().parent / 'generate_all_slides.mjs'
        import subprocess
        subprocess.check_call(['node', str(script), slug])

    elif cmd == 'auto':
        parser.add_argument('project')
        parser.add_argument('--voice', default='Charon')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        slug = load_json(pdir / 'film.json').get('slug', pdir.name)
        script = Path(__file__).resolve().parent / 'generate_all_slides.mjs'
        import prompts, voice, mix, build, check, render, subprocess

        print(f"\n============================================================")
        print(f"[Auto Pipeline] Running autonomous production: {slug}")
        print(f"============================================================")
        print("\n[Step 1/6] Compiling Prompts...")
        prompts.build_prompts(pdir)

        print("\n[Step 2/6] Generating Narration & Clocks...")
        files = voice.tts_generate(pdir, voice=args.voice)
        voice.align_and_lock_voice(pdir, files)

        print("\n[Step 3/6] Generating Slide Images via Google Flow...")
        subprocess.check_call(['node', str(script), slug])

        print("\n[Step 4/6] Mixing Soundtrack & Ducking Music...")
        mix.mix_audio(pdir)

        print("\n[Step 5/6] Building Viewer & Validating Pacing...")
        build.build_page(pdir)
        if not check.check_project(pdir):
            print("\n[Notice] Proceeding despite warnings...")

        print("\n[Step 6/6] Rendering Final 60fps MP4...")
        out_dir = pdir / 'out'
        out_dir.mkdir(exist_ok=True)
        out_mp4 = out_dir / f"{slug}.mp4"
        render.export_video(pdir, out_mp4, preview=False)

        # Record in completed topics ledger
        from common import probe_duration
        import topics
        cfg = load_json(pdir / 'film.json')
        topic_name = cfg.get('topic', cfg.get('title', slug))
        slides = load_json(pdir / 'slides.json')
        dur = probe_duration(out_mp4) if out_mp4.exists() else 0.0
        topics.mark_completed(topic_name, slug=slug, title=cfg.get('title', topic_name.upper()), duration=dur, slides=len(slides), video_path=out_mp4)
        print(f"\n[Auto Pipeline] Complete! Final deliverable: {out_mp4}")

    elif cmd == 'topics':
        import topics
        subcmd = rest[0] if rest else 'list'
        if subcmd == 'next':
            nxt = topics.get_next_topic()
            print(json.dumps(nxt, indent=2) if nxt else json.dumps({'error': 'No more unproduced topics.'}))
        elif subcmd == 'completed':
            comp = topics.get_completed_topics()
            print(f"\n--- Completed Topics Ledger ({len(comp)} videos) ---")
            for i, c in enumerate(comp, 1):
                dur_str = f"({c.get('duration_seconds', 0):.1f}s, {c.get('slides_count', 0)} slides)" if 'duration_seconds' in c else ""
                print(f"{i:02d}. {c['topic']} {dur_str} -> {c.get('video_path', 'done')}")
        else:
            comp_set = {topics.norm_str(x.get('topic', '')) for x in topics.get_completed_topics()}
            pending = [x for x in topics.get_example_topics() if topics.norm_str(x.get('topic', '')) not in comp_set]
            print(f"\n--- Pending Candidate Topics ({len(pending)} available in example_topics.json) ---")
            for i, p in enumerate(pending, 1):
                print(f"{i:02d}. {p['topic']} [{p.get('category', 'General')}]")
                if p.get('core_concept'):
                    print(f"    Concept: {p['core_concept']}")

    else:
        die(f"Unknown command '{cmd}'. Run 'cli.py help' for usage.")


if __name__ == '__main__':
    main()
