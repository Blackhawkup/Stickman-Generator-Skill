#!/usr/bin/env python3
"""Unified CLI for the Timed Slideshow Explainer system.

Supports both 1-minute vertical Shorts (9:16) and 10-minute long-form explainer videos (16:9).
When rendering a long-form video, an autonomous companion Short (first ~60s hook) is automatically generated.
Saves deliverables to the working directory where the agent is run and cleans up intermediate scratch files.

Commands:
  python tools/cli.py new <slug> [--mode short|long] [--format 16:9|9:16|1:1] [--dir <path>]
  python tools/cli.py prompts <project>
  python tools/cli.py tts <project> [--voice Charon]
  python tools/cli.py voice <project> <audio.wav>
  python tools/cli.py images <project>
  python tools/cli.py mix <project>
  python tools/cli.py check <project>
  python tools/cli.py build <project>
  python tools/cli.py preview <project>
  python tools/cli.py render <project>
  python tools/cli.py extract-short <project>
  python tools/cli.py caption <project>
  python tools/cli.py thumbnail <project>
  python tools/cli.py auto <project> [--voice Charon] [--keep-temp]
  python tools/cli.py topics [next|list|completed]
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
    # 1. Exact path
    p = Path(name).expanduser()
    if p.is_dir() and (p / 'film.json').exists():
        return p.resolve()
    # 2. Relative to current working directory
    cwd_p = Path.cwd() / name
    if (cwd_p / 'film.json').exists():
        return cwd_p.resolve()
    # 3. Running directly inside project folder
    if (Path.cwd() / 'film.json').exists() and name in ('.', Path.cwd().name):
        return Path.cwd().resolve()
    # 4. Standard projects directory
    p = PROJECTS_DIR / name
    if (p / 'film.json').exists():
        return p.resolve()
    die(f"Cannot find project '{name}'. Expected folder with film.json at {p} or {cwd_p}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('help', '-h', '--help'):
        print(__doc__)
        return

    cmd = sys.argv[1]
    rest = sys.argv[2:]
    parser = argparse.ArgumentParser(prog=f"cli.py {cmd}")

    if cmd == 'new':
        parser.add_argument('slug')
        parser.add_argument('--mode', default='short', choices=['short', 'long'], help="Video mode: short (~1m) or long (~10m)")
        parser.add_argument('--format', choices=['16:9', '9:16', '1:1'], help="Aspect ratio (defaults to 16:9 for long, 9:16 for short)")
        parser.add_argument('--dir', help="Custom destination directory (defaults to current working directory or projects/)")
        args = parser.parse_args(rest)
        
        if args.dir:
            dest = Path(args.dir).expanduser() / args.slug
        elif Path.cwd().name == 'slideshow-workflow':
            dest = PROJECTS_DIR / args.slug
        else:
            dest = Path.cwd() / args.slug

        if dest.exists():
            die(f"Project '{args.slug}' already exists at {dest}")
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copytree(TEMPLATES_DIR, dest, dirs_exist_ok=True)
        
        cfg = load_json(dest / 'film.json')
        cfg['slug'] = args.slug
        cfg['mode'] = args.mode
        cfg['format'] = args.format if args.format else ('16:9' if args.mode == 'long' else '9:16')
        save_json(dest / 'film.json', cfg)
        for d in ('images', 'voice', 'out', 'build'):
            (dest / d).mkdir(exist_ok=True)
        print(f"\n[Project Created] {dest}")
        print(f"Mode: {cfg['mode'].upper()} | Format: {cfg['format']}")

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

    elif cmd == 'caption':
        parser.add_argument('project')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        cfg = load_json(pdir / 'film.json')
        slug = cfg.get('slug', pdir.name)
        topic_name = cfg.get('topic', cfg.get('title', slug.replace('-', ' ').title()))
        script_file = pdir / 'script.md'
        script_text = script_file.read_text(encoding='utf-8') if script_file.exists() else ""
        mode = cfg.get('mode', 'short')
        import metadata
        res = metadata.save_metadata(pdir, topic_name, slug, script_text=script_text, mode=mode)
        print("\n" + res['full_text'])

    elif cmd in ('preview', 'render'):
        parser.add_argument('project')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        import check, mix, build, render
        build.build_page(pdir)
        mix.mix_audio(pdir)
        if not check.check_project(pdir):
            print("\n[Notice] Proceeding despite warnings...")
        cfg = load_json(pdir / 'film.json')
        slug = cfg.get('slug', pdir.name)
        is_long = (cfg.get('mode') == 'long' or cfg.get('format') == '16:9')
        out_dir = pdir / 'out'
        out_dir.mkdir(exist_ok=True)
        
        if cmd == 'preview':
            render.export_video(pdir, out_dir / 'preview.mp4', preview=True)
        else:
            filename = f"{slug}-long.mp4" if is_long else f"{slug}.mp4"
            render.export_video(pdir, out_dir / filename, preview=False)

    elif cmd == 'extract-short':
        parser.add_argument('project')
        parser.add_argument('--max-duration', type=float, default=72.0)
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        import extract_short
        extract_short.extract_short(pdir, max_duration=args.max_duration)

    elif cmd == 'images':
        parser.add_argument('project')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        script = Path(__file__).resolve().parent / 'generate_all_slides.mjs'
        import subprocess
        subprocess.check_call(['node', str(script), str(pdir)])

    elif cmd == 'thumbnail':
        parser.add_argument('project')
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        import thumbnail
        cfg = load_json(pdir / 'film.json')
        topic_name = cfg.get('topic', cfg.get('title', pdir.name.replace('-', ' ').title()))
        thumbnail.build_and_save_thumbnail(pdir, topic_name=topic_name)

    elif cmd == 'auto':
        parser.add_argument('project')
        parser.add_argument('--voice', default='Charon')
        parser.add_argument('--keep-temp', action='store_true', help="Keep intermediate scratch files (build/, voice/, images/)")
        args = parser.parse_args(rest)
        pdir = resolve_project(args.project)
        cfg = load_json(pdir / 'film.json')
        slug = cfg.get('slug', pdir.name)
        topic_name = cfg.get('topic', cfg.get('title', slug.replace('-', ' ').title()))
        is_long = (cfg.get('mode') == 'long' or cfg.get('format') == '16:9')
        script_path = Path(__file__).resolve().parent / 'generate_all_slides.mjs'
        import prompts, voice, mix, build, check, render, subprocess, metadata, cleanup

        mode_title = "10-MINUTE LONG FORM" if is_long else "1-MINUTE SHORT"
        print(f"\n============================================================")
        print(f"[Auto Pipeline] Production: {slug} [{mode_title}]")
        print(f"Working Directory: {pdir}")
        print(f"============================================================")
        
        print("\n[Step 1/7] Compiling Prompts (Including Thumbnail for Long Form)...")
        prompts.build_prompts(pdir)

        print("\n[Step 2/7] Generating Narration & Clocks...")
        files = voice.tts_generate(pdir, voice=args.voice)
        voice.align_and_lock_voice(pdir, files)

        print("\n[Step 3/7] Generating Artwork & Thumbnail via Google Flow...")
        subprocess.check_call(['node', str(script_path), str(pdir)])

        print("\n[Step 4/7] Mixing Soundtrack & Ducking Music...")
        mix.mix_audio(pdir)

        print("\n[Step 5/7] Building Viewer & Validating Pacing...")
        build.build_page(pdir)
        if not check.check_project(pdir):
            print("\n[Notice] Proceeding despite warnings...")

        print("\n[Step 6/7] Rendering Primary 60fps MP4...")
        out_dir = pdir / 'out'
        out_dir.mkdir(exist_ok=True)
        
        script_file = pdir / 'script.md'
        script_text = script_file.read_text(encoding='utf-8') if script_file.exists() else ""
        
        if is_long:
            out_mp4 = out_dir / f"{slug}-long.mp4"
            render.export_video(pdir, out_mp4, preview=False)
            
            # Step 7a: Automatically extract and render companion Short!
            print("\n[Step 7/7] Automatically Extracting & Rendering Companion 1-Minute Short (9:16)...")
            import extract_short
            short_mp4 = out_dir / f"{slug}-short.mp4"
            extract_short.extract_short(pdir, short_mp4)
            
            # Step 7b: Generate & verify 1920x1080 High-CTR YouTube Thumbnail
            print("\n[Step 7b] Generating 1920x1080 High-CTR YouTube Thumbnail...")
            import thumbnail
            thumb_dest = thumbnail.build_and_save_thumbnail(pdir, topic_name=topic_name)
            
            # Metadata & Captions + 5 Hashtags
            metadata.save_metadata(pdir, topic_name, slug, script_text=script_text, mode='long', video_path=out_mp4, thumbnail_path=thumb_dest)
        else:
            thumb_dest = None
            out_mp4 = out_dir / f"{slug}.mp4"
            render.export_video(pdir, out_mp4, preview=False)
            
            # Metadata & Captions + 5 Hashtags
            metadata.save_metadata(pdir, topic_name, slug, script_text=script_text, mode='short', video_path=out_mp4)

        # Record in completed topics ledger
        from common import probe_duration
        import topics
        slides = load_json(pdir / 'slides.json')
        dur = probe_duration(out_mp4) if out_mp4.exists() else 0.0
        topics.mark_completed(
            topic_name,
            slug=slug,
            title=cfg.get('title', topic_name.upper()),
            duration=dur,
            slides=len(slides),
            video_path=out_mp4,
            music=cfg.get('music'),
            thumbnail=thumb_dest if (thumb_dest and Path(thumb_dest).exists()) else None
        )

        # Step 8: Clean up intermediate scratch files (preserving only deliverables)
        cleanup.cleanup_project(pdir, keep_temp=args.keep_temp)

        print(f"\n============================================================")
        print(f"[Auto Pipeline] Production Finished for '{slug}'!")
        print(f"All scratch files deleted. Final deliverables ready in {pdir}:")
        if is_long:
            print(f"  ★ Master Video:     {slug}-long.mp4 (16:9, ~10m)")
            print(f"  ★ Companion Short:  {slug}-short.mp4 (9:16, ~1m)")
            print(f"  ★ Video Thumbnail:  {slug}-thumbnail.png (16:9)")
        else:
            print(f"  ★ Finished Short:   {slug}.mp4 (9:16, ~1m)")
        print(f"  ★ Social Caption:   {slug}-caption.txt (with 5 targeted hashtags)")
        print(f"  ★ Metadata Record:  {slug}-metadata.json")
        print(f"  ★ Topics Ledger:    Updated topics/completed_topics.json")
        print(f"============================================================")

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
