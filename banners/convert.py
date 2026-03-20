"""HTMLバナーをPNGに変換するスクリプト（Playwright使用）"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BANNERS = [
    ("pattern-a-meta.html", 1200, 628),
    ("pattern-a-ig.html", 1080, 1080),
    ("pattern-b-meta.html", 1200, 628),
    ("pattern-b-ig.html", 1080, 1080),
    ("pattern-c-meta.html", 1200, 628),
    ("pattern-c-ig.html", 1080, 1080),
]

async def main():
    base = Path(__file__).parent
    out = base / "png"
    out.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for filename, w, h in BANNERS:
            page = await browser.new_page(viewport={"width": w, "height": h})
            await page.goto(f"file://{base / filename}")
            await page.wait_for_timeout(2000)  # フォント読み込み待ち
            png_name = filename.replace(".html", ".png")
            await page.screenshot(path=str(out / png_name))
            await page.close()
            print(f"✓ {png_name} ({w}x{h})")
        await browser.close()

asyncio.run(main())
