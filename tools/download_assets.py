import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def main():
    out_dir = Path("slideshow-workflow/projects/sunk-cost-fallacy/images")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp('http://127.0.0.1:9333')
        ctx = b.contexts[0]
        page = next((pg for pg in ctx.pages if 'flow.google.com' in pg.url), None)
        
        # Get unique images with /asb/
        urls = await page.evaluate("""() => {
            const seen = new Set();
            const list = [];
            for (const img of document.querySelectorAll('img[src*="/asb/"]')) {
                if (!seen.has(img.src)) {
                    seen.add(img.src);
                    list.push(img.src);
                }
            }
            return list;
        }""")
        
        print(f"Unique Flow image URLs found: {len(urls)}")
        for i, u in enumerate(urls):
            print(f"[{i}] {u[:65]}...")
            
        slide_names = [
            "slide_01_intro",
            "slide_02_ticket",
            "slide_03_miserable_cinema",
            "slide_04_trapped",
            "slide_05_psychology",
            "slide_06_brain_trap",
            "slide_07_bad_decisions",
            "slide_08_takeaway"
        ]
        
        # In Flow grid, top-left is newest, bottom-right is oldest.
        # Since we generated slide 1 first and slide 8 last, the oldest is slide 1!
        # So urls in reverse order correspond to slide 1 -> 8:
        ordered_urls = list(reversed(urls[:len(slide_names)])) if len(urls) >= len(slide_names) else urls
        
        for idx, u in enumerate(ordered_urls):
            name = slide_names[idx]
            target = out_dir / f"{name}.png"
            img_bytes = await page.evaluate(f"""async () => {{
                const res = await fetch('{u}');
                const buf = await res.arrayBuffer();
                return Array.from(new Uint8Array(buf));
            }}""")
            target.write_bytes(bytes(img_bytes))
            print(f" -> Successfully saved {name}.png ({len(img_bytes)} bytes)")

if __name__ == '__main__':
    asyncio.run(main())
