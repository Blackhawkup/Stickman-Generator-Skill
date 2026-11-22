"""Autonomous 1920x1080 High-CTR YouTube Thumbnail Generator.

Produces clickable widescreen (16:9) YouTube thumbnails for long-form explainer videos in the
signature Editorial Stick-Figure Webcomic art style.

Features:
- Warm cream parchment background (#FBF6EF) matching the video aesthetic
- Huge, bold, high-contrast comic book headline title
- Eye-catching red accent badge / paradox subtitle
- Expressive editorial stick-figure illustration in crimson red shirt (#DC2626)
- Can composite with Flow AI illustrations or render autonomously with PIL
- Preserved directly at <project>/<slug>-thumbnail.png
"""
import json, os, shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from common import load_json, save_json, PROMPTS_DIR
except ImportError:
    from tools.common import load_json, save_json, PROMPTS_DIR


def get_font(size=72, bold=True):
    """Loads a high-quality clean font across Windows and Linux platforms."""
    font_candidates = [
        # Windows fonts
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/comicbd.ttf" if bold else "C:/Windows/Fonts/comic.ttf",
        "C:/Windows/Fonts/seguiui.ttf",
        # Linux / cross-platform
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for cand in font_candidates:
        if os.path.exists(cand):
            try:
                return ImageFont.truetype(cand, size)
            except Exception:
                continue
    return ImageFont.load_default()


def build_and_save_thumbnail(pdir, topic_name=None, subtitle=None, overwrite=True):
    """Generates and saves a 1920x1080 high-CTR YouTube thumbnail for long-form videos."""
    pdir = Path(pdir).resolve()
    cfg_file = pdir / 'film.json'
    cfg = load_json(cfg_file) if cfg_file.exists() else {}
    
    slug = cfg.get('slug', pdir.name)
    title = (topic_name or cfg.get('topic') or cfg.get('title') or slug.replace('-', ' ')).upper()
    
    slides_file = pdir / 'slides.json'
    slides = load_json(slides_file) if slides_file.exists() else []
    
    if not subtitle:
        if slides and slides[0].get('bottom_caption'):
            subtitle = slides[0]['bottom_caption']
        else:
            subtitle = "WHY WE CAN'T LET GO"
            
    out_thumb = pdir / f"{slug}-thumbnail.png"
    img_dir = pdir / 'images'
    
    # 1. Check if Flow AI already generated an illustrated thumbnail image
    flow_thumb_candidates = [
        img_dir / f"{slug}-thumbnail.png",
        img_dir / f"{slug}-thumbnail.jpeg",
        img_dir / f"{pdir.name}-thumbnail.png",
        img_dir / "thumbnail.png"
    ]
    
    base_img = None
    for cand in flow_thumb_candidates:
        if cand.exists():
            try:
                base_img = Image.open(cand).convert("RGBA")
                if base_img.size != (1920, 1080):
                    base_img = base_img.resize((1920, 1080), Image.Resampling.LANCZOS)
                print(f"[Thumbnail] Loaded existing Flow AI illustration: {cand.name}")
                break
            except Exception:
                pass

    # 2. If no AI base image exists, render high-contrast editorial stickman artwork
    if base_img is None:
        base_img = Image.new("RGBA", (1920, 1080), "#FBF6EF")
        draw = ImageDraw.Draw(base_img)
        
        # Subtle parchment vignette border
        draw.rectangle([20, 20, 1900, 1060], outline="#E5DCCE", width=4)
        
        # Stylized background 2D desk & bookshelf in fine black ink lines
        # Bookshelf on left
        draw.rectangle([120, 260, 480, 880], outline="#0F172A", width=5, fill="#F5EADB")
        for shelf_y in (440, 620, 800):
            draw.line([(120, shelf_y), (480, shelf_y)], fill="#0F172A", width=5)
            
        # Books on shelf
        book_colors = ["#DC2626", "#2563EB", "#16A34A", "#EAB308", "#0F172A", "#64748B"]
        bx = 140
        for i, col in enumerate(book_colors * 2):
            if bx > 440:
                break
            bw = 28 + (i % 3) * 8
            bh = 120 + (i % 4) * 12
            draw.rectangle([bx, 440 - bh, bx + bw, 440], fill=col, outline="#0F172A", width=3)
            bx += bw + 6

        # Desk on right
        draw.line([(960, 780), (1800, 780)], fill="#0F172A", width=6)
        draw.line([(1040, 780), (1040, 1000)], fill="#0F172A", width=6)
        draw.line([(1720, 780), (1720, 1000)], fill="#0F172A", width=6)

        # Indoor Monstera plant
        draw.arc([1600, 660, 1720, 780], 0, 360, fill="#16A34A", width=6)
        draw.rectangle([1630, 720, 1690, 780], fill="#E2B170", outline="#0F172A", width=4)

        # Center: Large expressive stick figure in crimson red shirt (#DC2626)
        cx, cy = 960, 520
        # Oval ground shadow
        draw.ellipse([cx - 160, cy + 340, cx + 160, cy + 390], fill="#E5DCCE")
        
        # Body (bean torso in red shirt)
        draw.rounded_rectangle([cx - 75, cy - 20, cx + 75, cy + 180], radius=35, fill="#DC2626", outline="#0F172A", width=7)
        
        # Legs
        draw.line([(cx - 35, cy + 180), (cx - 55, cy + 350)], fill="#0F172A", width=8)
        draw.line([(cx + 35, cy + 180), (cx + 55, cy + 350)], fill="#0F172A", width=8)
        # Shoes
        draw.ellipse([cx - 85, cy + 340, cx - 35, cy + 365], fill="#0F172A")
        draw.ellipse([cx + 35, cy + 340, cx + 85, cy + 365], fill="#0F172A")
        
        # Head (large white circle)
        draw.ellipse([cx - 110, cy - 240, cx + 110, cy - 20], fill="#FFFFFF", outline="#0F172A", width=8)
        
        # Shocked expressive face: wide dot eyes + open gasp mouth
        draw.ellipse([cx - 45, cy - 145, cx - 25, cy - 120], fill="#0F172A")
        draw.ellipse([cx + 25, cy - 145, cx + 45, cy - 120], fill="#0F172A")
        # Raised expressive eyebrows
        draw.arc([cx - 55, cy - 180, cx - 15, cy - 150], 200, 340, fill="#0F172A", width=6)
        draw.arc([cx + 15, cy - 180, cx + 55, cy - 150], 200, 340, fill="#0F172A", width=6)
        # Open mouth
        draw.ellipse([cx - 25, cy - 95, cx + 25, cy - 55], fill="#DC2626", outline="#0F172A", width=5)
        
        # Arms raised in disbelief / dilemma
        draw.line([(cx - 65, cy + 30), (cx - 160, cy - 30)], fill="#0F172A", width=8)
        draw.line([(cx - 160, cy - 30), (cx - 190, cy - 110)], fill="#0F172A", width=8)
        draw.line([(cx + 65, cy + 30), (cx + 160, cy - 30)], fill="#0F172A", width=8)
        draw.line([(cx + 160, cy - 30), (cx + 190, cy - 110)], fill="#0F172A", width=8)
        # Hands
        draw.ellipse([cx - 215, cy - 135, cx - 175, cy - 95], fill="#FFFFFF", outline="#0F172A", width=6)
        draw.ellipse([cx + 175, cy - 135, cx + 215, cy - 95], fill="#FFFFFF", outline="#0F172A", width=6)

    # 3. Overlay Bold High-Contrast Typography & Clickable Banner
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d_over = ImageDraw.Draw(overlay)
    
    # Title formatting (Bold Headline)
    font_title = get_font(size=96, bold=True)
    
    # Shadow and Title text
    bbox = d_over.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    # If title is wide, shrink font
    if tw > 1650:
        font_title = get_font(size=76, bold=True)
        bbox = d_over.textbbox((0, 0), title, font=font_title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
    tx = (1920 - tw) // 2
    ty = 60
    
    # Title background badge for maximum contrast
    pad_x, pad_y = 40, 20
    d_over.rounded_rectangle(
        [tx - pad_x, ty - pad_y, tx + tw + pad_x, ty + th + pad_y + 10],
        radius=18,
        fill=(251, 246, 239, 245),
        outline="#0F172A",
        width=6
    )
    # Deep shadow under text
    d_over.text((tx + 4, ty + 4), title, font=font_title, fill="#CBD5E1")
    # Main bold headline text
    d_over.text((tx, ty), title, font=font_title, fill="#0F172A")
    
    # Subtitle Badge (High-CTR Warning / Hook Badge)
    if subtitle:
        font_sub = get_font(size=44, bold=True)
        s_bbox = d_over.textbbox((0, 0), subtitle.upper(), font=font_sub)
        sw = s_bbox[2] - s_bbox[0]
        sh = s_bbox[3] - s_bbox[1]
        sx = (1920 - sw) // 2
        sy = 950
        
        # Red punchy banner at bottom
        d_over.rounded_rectangle(
            [sx - 35, sy - 14, sx + sw + 35, sy + sh + 16],
            radius=12,
            fill="#DC2626",
            outline="#0F172A",
            width=5
        )
        d_over.text((sx, sy), subtitle.upper(), font=font_sub, fill="#FFFFFF")

    # Composite layers
    final_thumb = Image.alpha_composite(base_img, overlay).convert("RGB")
    final_thumb.save(out_thumb, "PNG", quality=95)
    
    # Copy to images/ if exists
    if img_dir.exists():
        try:
            shutil.copy2(out_thumb, img_dir / f"{slug}-thumbnail.png")
        except Exception:
            pass

    print(f"\n[Thumbnail] High-CTR 1920x1080 YouTube Thumbnail Generated:")
    print(f" -> Deliverable: {out_thumb} (1920x1080, Ready for Upload)")
    return out_thumb
