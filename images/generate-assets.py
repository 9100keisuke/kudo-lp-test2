import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image

BASE = Path(__file__).parent

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # 1. Book cover PNG
        page = await browser.new_page(viewport={"width": 600, "height": 850})
        await page.goto(f"file://{BASE / 'book-cover-un.html'}")
        await page.wait_for_timeout(3000)
        await page.screenshot(path=str(BASE / "book-cover-un.png"))
        await page.close()
        print("✓ book-cover-un.png (600x850)")

        # 2. 3D Mockup - realistic with page edges, gloss, thick spine
        mockup_html = BASE / "mockup-temp.html"
        mockup_html.write_text(f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:900px; height:750px; background:transparent; display:flex; align-items:center; justify-content:center; }}

.scene {{
  perspective: 1800px;
  display:flex; align-items:center; justify-content:center;
  width:900px; height:750px;
}}

.book {{
  position:relative;
  transform-style: preserve-3d;
  transform: rotateY(-28deg) rotateX(4deg);
}}

/* Front cover */
.front {{
  position:relative; z-index:3;
  width:380px; height:538px;
  border-radius: 1px 4px 4px 1px;
  overflow: hidden;
  box-shadow: 2px 0 8px rgba(0,0,0,0.08);
}}
.front img {{
  width:100%; height:100%; display:block; object-fit:cover;
}}
/* Subtle gloss reflection on front */
.front::after {{
  content:''; position:absolute; inset:0;
  background: linear-gradient(
    120deg,
    transparent 30%,
    rgba(255,255,255,0.08) 45%,
    rgba(255,255,255,0.15) 50%,
    rgba(255,255,255,0.08) 55%,
    transparent 70%
  );
  pointer-events: none;
}}

/* Spine - thick & realistic */
.spine {{
  position:absolute; top:0; left:0;
  width:42px; height:538px;
  background: linear-gradient(90deg,
    #7a5c10 0%, #8b6914 10%, #b8860b 35%, #c9a84c 55%, #b8860b 75%, #8b6914 95%, #7a5c10 100%
  );
  transform-origin: left center;
  transform: rotateY(-90deg);
  box-shadow: inset -2px 0 6px rgba(0,0,0,0.25), inset 2px 0 4px rgba(255,255,255,0.08);
}}

/* Spine text */
.spine::after {{
  content: 'なぜ、真面目な人ほど運が悪くなるのか？  工藤圭介';
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%) rotate(90deg);
  white-space: nowrap;
  font-family: sans-serif; font-size: 11px; font-weight: 600;
  color: rgba(255,255,255,0.8);
  letter-spacing: 0.08em;
}}

/* Page edges (bottom) - visible below front cover */
.pages-bottom {{
  position:absolute; bottom:-12px; left:2px;
  width:376px; height:12px;
  background: repeating-linear-gradient(
    90deg,
    #f5f0e6 0px, #f5f0e6 1.5px,
    #ebe3d3 1.5px, #ebe3d3 3px
  );
  box-shadow: 0 2px 4px rgba(0,0,0,0.08);
  border-radius: 0 0 2px 2px;
  z-index: 2;
}}

/* Page edges (right side) - visible on the open side */
.pages-right {{
  position:absolute; top:2px; right:-10px;
  width:10px; height:534px;
  background: repeating-linear-gradient(
    0deg,
    #f5f0e6 0px, #f5f0e6 1.5px,
    #e8e0d0 1.5px, #e8e0d0 3px
  );
  box-shadow: 2px 0 4px rgba(0,0,0,0.06);
  border-radius: 0 2px 2px 0;
  z-index: 2;
}}

/* Back cover */
.back {{
  position:absolute; top:0; left:-42px;
  width:380px; height:538px;
  background: linear-gradient(135deg, #ede8dd, #e0d8cc);
  transform-origin: right center;
  transform: translateZ(0px);
  border-radius: 4px 1px 1px 4px;
  z-index: 0;
}}

/* Realistic shadow on surface */
.shadow {{
  position:absolute;
  bottom: -50px; left: 50%;
  transform: translateX(-45%) rotateX(80deg);
  width: 360px; height: 60px;
  background: radial-gradient(ellipse at center, rgba(0,0,0,0.18) 0%, rgba(0,0,0,0.06) 40%, transparent 70%);
  filter: blur(12px);
  z-index: 0;
}}
</style></head><body>
<div class="scene">
  <div class="book">
    <div class="front"><img src="file://{BASE / 'book-cover-un.png'}"></div>
    <div class="spine"></div>
    <div class="pages-right"></div>
    <div class="pages-bottom"></div>
    <div class="back"></div>
  </div>
  <div class="shadow"></div>
</div></body></html>""")

        page2 = await browser.new_page(viewport={"width": 900, "height": 750})
        await page2.goto(f"file://{mockup_html}")
        await page2.wait_for_timeout(3000)
        await page2.screenshot(path=str(BASE / "book-mockup-3d.png"), omit_background=True)
        await page2.close()
        print("✓ book-mockup-3d.png (900x750, transparent)")

        await browser.close()

    # Convert to webp
    for name in ["book-cover-un.png", "book-mockup-3d.png"]:
        img = Image.open(BASE / name)
        webp_name = name.replace(".png", ".webp")
        img.save(BASE / webp_name, "WEBP", quality=92)
        print(f"✓ {webp_name}")

    # Cleanup temp HTML
    for f in ["mockup-temp.html"]:
        (BASE / f).unlink(missing_ok=True)

    print("\nAll assets generated!")

asyncio.run(main())
