"""Project Cleanup Utility:
Moves final deliverables (MP4 videos, thumbnail PNG, caption TXT, metadata JSON)
directly to the active directory where the agent is run, and deletes all intermediate
scratch directories (build/, voice/, images/, temp wavs), leaving only clean finished files.
"""
import os, shutil
from pathlib import Path


def cleanup_project(pdir, target_dir=None, keep_temp=False):
    """Deletes intermediate scratch files, keeping only final deliverables and updating topic list."""
    pdir = Path(pdir).resolve()
    target_dir = Path(target_dir).resolve() if target_dir else pdir

    if keep_temp:
        print(f"\n[Cleanup] --keep-temp flag active. Retaining intermediate scratch files in {pdir}")
        return

    print(f"\n[Cleanup] Cleaning intermediate scratch files for '{pdir.name}'...")

    # 1. Collect all final deliverables from out/ and pdir/
    deliverables = []
    
    # Final video(s)
    out_dir = pdir / 'out'
    if out_dir.exists():
        for mp4 in out_dir.glob('*.mp4'):
            dest = target_dir / mp4.name
            if mp4.resolve() != dest.resolve():
                shutil.copy2(mp4, dest)
                print(f" -> Preserved deliverable: {dest.name}")
            deliverables.append(dest)

    # Caption and metadata files
    for ext in ('*-caption.txt', '*-metadata.json', '*thumbnail*.png'):
        for f in pdir.glob(ext):
            dest = target_dir / f.name
            if f.resolve() != dest.resolve():
                shutil.copy2(f, dest)
                print(f" -> Preserved deliverable: {dest.name}")
            deliverables.append(dest)

    # 2. Delete intermediate scratch folders
    scratch_folders = ['build', 'voice', 'images', 'out_frames', 'out']
    for folder in scratch_folders:
        fpath = pdir / folder
        if fpath.exists() and fpath.is_dir():
            try:
                shutil.rmtree(fpath)
                print(f" -> Deleted temporary folder: {folder}/")
            except Exception as e:
                print(f" [!] Warning removing {folder}: {e}")

    # 3. Clean up intermediate json and temp files in pdir if target_dir is outside pdir
    if pdir != target_dir:
        try:
            shutil.rmtree(pdir)
            print(f" -> Cleaned temporary project directory: {pdir}")
        except Exception as e:
            pass

    print(f"\n[Cleanup] Complete! Only final deliverables retained in: {target_dir}")
    for d in deliverables:
        print(f"   ★ {d.name}")
    return deliverables
