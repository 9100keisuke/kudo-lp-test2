import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFilter

BASE = Path(__file__).parent

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # 1. Book cover PNG
        page = await browser.new_page(viewport={"width": 600, "height": 850})
        await page.goto(f"file://{BASE / 'book-cover-un.html'}")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=str(BASE / "book-cover-un.png"))
        await page.close()
        print("✓ book-cover-un.png (600x850)")

        # 2. 3D Mockup HTML
        mockup_html = BASE / "mockup-temp.html"
        mockup_html.write_text(f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:800; height:700; background: transparent; display:flex; align-items:center; justify-content:center; }}
.scene {{ perspective: 1200px; display:flex; align-items:center; justify-content:center; width:800px; height:700px; }}
.book {{ position:relative; transform-style:preserve-3d; transform: rotateY(-25deg) rotateX(5deg); }}
.book .front {{ position:relative; z-index:2; }}
.book .front img {{ width:360px; height:510px; display:block; border-radius:2px; box-shadow: 0 0 0 1px rgba(0,0,0,0.05); }}
.book .spine {{ position:absolute; top:0; left:0; width:40px; height:510px; background: linear-gradient(90deg, #c9a84c, #b8860b, #a07508); transform: rotateY(90deg) translateX(-20px) translateZ(180px); border-radius:0; }}
.book .back {{ position:absolute; top:0; left:0; width:360px; height:510px; background: linear-gradient(135deg, #f5f0e8, #ede4d8); transform: translateZ(-40px); border-radius:2px; }}
.shadow {{ position:absolute; bottom:-30px; left:50%; transform:translateX(-50%); width:320px; height:20px; background:radial-gradient(ellipse, rgba(0,0,0,0.2) 0%, transparent 70%); filter:blur(10px); }}
</style></head><body>
<div class="scene">
  <div class="book">
    <div class="front"><img src="file://{BASE / 'book-cover-un.png'}"></div>
    <div class="spine"></div>
    <div class="back"></div>
  </div>
  <div class="shadow"></div>
</div></body></html>""")

        page2 = await browser.new_page(viewport={"width": 800, "height": 700})
        await page2.goto(f"file://{mockup_html}")
        await page2.wait_for_timeout(2000)
        await page2.screenshot(path=str(BASE / "book-mockup-3d.png"), omit_background=True)
        await page2.close()
        print("✓ book-mockup-3d.png (800x700, transparent)")

        # 3. Header/FV image (for Pattern A)
        header_html = BASE / "header-fv-temp.html"
        header_html.write_text(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&family=Noto+Serif+JP:wght@700;900&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1200; height:628; overflow:hidden; }}
.fv {{
  width:1200px; height:628px;
  background: linear-gradient(135deg, #fffdf7 0%, #f5f0ff 50%, #ede4ff 100%);
  display:flex; align-items:center; position:relative; overflow:hidden;
  font-family:'Noto Sans JP',sans-serif; color:#1a1a2e; padding:0 60px;
}}
.fv::before {{ content:''; position:absolute; top:0; left:0; right:0; bottom:0;
  background:radial-gradient(ellipse at 30% 50%, rgba(184,134,11,0.06) 0%, transparent 60%); }}
.left {{ flex:1; position:relative; z-index:1; padding-right:40px; }}
.tag {{ display:inline-block; background:rgba(184,134,11,0.08); border:1px solid rgba(184,134,11,0.15);
  border-radius:100px; padding:6px 18px; font-size:11px; color:#b8860b; letter-spacing:0.2em; font-weight:700; margin-bottom:20px; }}
h1 {{ font-family:'Noto Serif JP',serif; font-size:44px; font-weight:900; line-height:1.35; margin-bottom:16px; }}
.gold {{ color:#b8860b; }}
.sub {{ font-size:15px; color:rgba(26,26,46,0.55); line-height:1.8; margin-bottom:24px; }}
.cta {{ display:inline-block; background:#b8860b; color:#fff; font-weight:900; font-size:16px; padding:14px 36px; border-radius:100px; box-shadow:0 8px 30px rgba(184,134,11,0.25); }}
.author-row {{ display:flex; align-items:center; gap:12px; margin-top:20px; }}
.author-photo {{ width:50px; height:50px; border-radius:50%; object-fit:cover; object-position:center top; border:2px solid rgba(184,134,11,0.15); }}
.author-name {{ font-weight:700; font-size:13px; color:#b8860b; }}
.author-title {{ font-size:10px; color:rgba(26,26,46,0.4); }}
.right {{ flex-shrink:0; position:relative; z-index:1; }}
.right img {{ max-height:480px; filter:drop-shadow(12px 12px 30px rgba(0,0,0,0.12)); }}
.orb1 {{ position:absolute; width:200px; height:200px; border-radius:50%; background:rgba(180,130,200,0.06); filter:blur(60px); top:-40px; right:200px; }}
.orb2 {{ position:absolute; width:150px; height:150px; border-radius:50%; background:rgba(184,134,11,0.05); filter:blur(50px); bottom:20px; left:100px; }}
.dot {{ position:absolute; width:4px; height:4px; border-radius:50%; background:rgba(184,134,11,0.15); }}
</style></head><body>
<div class="fv">
  <div class="orb1"></div><div class="orb2"></div>
  <div class="dot" style="top:80px;left:150px;"></div>
  <div class="dot" style="top:200px;right:400px;width:3px;height:3px;"></div>
  <div class="dot" style="bottom:100px;left:300px;width:5px;height:5px;"></div>
  <div class="left">
    <div class="tag">Harvard Neuroscience × Luck Design</div>
    <h1>なぜ、<span class="gold">真面目な人</span>ほど<br>運が悪くなるのか？</h1>
    <p class="sub">脳が"正解"を探すほど、人生のチャンスは見えなくなる。<br>正解探しをやめた人から、「なぜかうまくいく」が始まる。</p>
    <div class="cta">無料で詳細を受け取る</div>
    <div class="author-row">
      <img src="file://{BASE / 'author-keisuke.webp'}" class="author-photo">
      <div>
        <p class="author-name">工藤圭介</p>
        <p class="author-title">ハーバード大学 脳神経科学プログラム修了</p>
      </div>
    </div>
  </div>
  <div class="right">
    <img src="file://{BASE / 'book-cover-un.png'}">
  </div>
</div></body></html>""")

        page3 = await browser.new_page(viewport={"width": 1200, "height": 628})
        await page3.goto(f"file://{header_html}")
        await page3.wait_for_timeout(2000)
        await page3.screenshot(path=str(BASE / "header-fv-a.png"))
        await page3.close()
        print("✓ header-fv-a.png (1200x628)")

        await browser.close()

    # Convert to webp
    for name in ["book-cover-un.png", "book-mockup-3d.png", "header-fv-a.png"]:
        img = Image.open(BASE / name)
        webp_name = name.replace(".png", ".webp")
        img.save(BASE / webp_name, "WEBP", quality=90)
        print(f"✓ {webp_name}")

    # Cleanup temp HTML
    for f in ["mockup-temp.html", "header-fv-temp.html"]:
        (BASE / f).unlink(missing_ok=True)

    print("\nAll assets generated!")

asyncio.run(main())
