"""Direct automation driver for Google Flow Chrome window via CDP."""
import asyncio, json, os, time
from pathlib import Path
from playwright.async_api import async_playwright

async def set_composer(page, aspect_ratio="1:1"):
    btn = page.locator('button.settings-trigger-button').first
    text = await btn.inner_text()
    target_label = "1:1" if aspect_ratio == "1:1" else ("16:9" if aspect_ratio == "16:9" else aspect_ratio)
    if target_label not in text:
        await btn.click()
        await asyncio.sleep(0.5)
        # Click Image if visible
        img_opt = page.locator('button:has-text("Image"), [role="menuitem"]:has-text("Image")').first
        if await img_opt.is_visible():
            await img_opt.click()
            await asyncio.sleep(0.3)
        # Click target aspect ratio
        ar_opt = page.locator(f'button:has-text("{target_label}"), [role="menuitem"]:has-text("{target_label}")').first
        if await ar_opt.is_visible():
            await ar_opt.click()
            await asyncio.sleep(0.3)
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.5)
    print(f"[Flow Driver] Composer status: {await btn.inner_text()}")

async def generate_and_download(page, prompt, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Existing media cards
    before_cards = await page.evaluate("() => [...document.querySelectorAll('flow-media-tile, flow-asset-card, .asset-card, img')].map(el => el.getAttribute('data-id') || el.src || el.id)")
    
    # Enter prompt
    box = page.locator('div.ProseMirror')
    await box.click()
    await page.keyboard.press("Control+A")
    await page.keyboard.press("Backspace")
    await box.type(prompt, delay=5)
    await asyncio.sleep(0.5)
    
    # Submit
    submit = page.locator('button:has-text("arrow_forward")').last
    await submit.click()
    print(" -> Prompt submitted. Waiting for generation...")
    
    # Wait for completion: look for a newly rendered image
    t0 = time.time()
    img_data_url = None
    while time.time() - t0 < 120:
        await asyncio.sleep(2.5)
        # Check if new media tile with image is present
        result = await page.evaluate("""() => {
            const imgs = [...document.querySelectorAll('img')].map(i => i.src).filter(s => s && s.includes('googleusercontent'));
            return imgs.length > 0 ? imgs[0] : null;
        }""")
        if result and result not in before_cards:
            img_data_url = result
            break
            
    if not img_data_url:
        # Fallback: take latest googleusercontent img
        img_data_url = await page.evaluate("() => [...document.querySelectorAll('img')].map(i => i.src).filter(s => s && s.includes('googleusercontent'))[0]")
        
    if not img_data_url:
        raise RuntimeError("No generated image found on page.")
        
    print(f" -> Found rendered asset: {img_data_url[:50]}...")
    img_bytes = await page.evaluate(f"""async () => {{
        const res = await fetch('{img_data_url}');
        const buf = await res.arrayBuffer();
        return Array.from(new Uint8Array(buf));
    }}""")
    output_path.write_bytes(bytes(img_bytes))
    print(f" -> Saved to {output_path} ({len(img_bytes)} bytes)")

async def run_batch(project_dir):
    pdir = Path(project_dir)
    prompts = json.loads((pdir / 'prompts.json').read_text(encoding='utf-8'))
    img_dir = pdir / 'images'
    img_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp('http://127.0.0.1:9333')
        ctx = b.contexts[0]
        page = next((pg for pg in ctx.pages if 'flow.google.com' in pg.url), None)
        if not page:
            raise RuntimeError("No Google Flow page open on CDP port 9333")
            
        current_ar = None
        for i, s in enumerate(prompts):
            name = s['name']
            ar = s.get('aspect_ratio', '9:16')
            out_file = img_dir / f"{name}.png"
            if out_file.exists():
                print(f"[{i+1}/{len(prompts)}] {name} already exists. Skipping.")
                continue
            if ar != current_ar:
                await set_composer(page, ar)
                current_ar = ar
            print(f"\n[{i+1}/{len(prompts)}] Generating [{ar}] {name}...")
            await generate_and_download(page, s['prompt'], out_file)
            await asyncio.sleep(1.5)

    try:
        import images_util
        images_util.normalize_project_images(pdir)
    except Exception as e:
        print(f"[Flow Driver] Note during dimension normalization: {e}")

if __name__ == '__main__':
    import sys
    proj = sys.argv[1] if len(sys.argv) > 1 else 'slideshow-workflow/projects/sunk-cost-fallacy'
    asyncio.run(run_batch(proj))
