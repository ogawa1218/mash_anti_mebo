#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第42回 サムネイル高品質生成スクリプト
stand.fm 第42話「食べる時間で体は変わる ― 同じ食事でも太る人・痩せる人の差」対応
HTML/CSS + Playwright（Chromiumヘッドレス）版
サイズ: 1280×670px
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images"
OUTPUT_DIR.mkdir(exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

LINE1        = "同じ食事でも"
LINE2        = "太る人と"
LINE3        = "痩せる人"
SUB          = "差は「いつ食べるか」だった"
NUM          = "㊷"
OUTPUT_FNAME = "サムネイル_第42回.png"

THUMBNAIL_HTML = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@font-face {{
  font-family: 'NotoSansJP';
  src: url('{FONT}');
  font-weight: 100 900;
}}
* {{ margin:0; padding:0; box-sizing:border-box;
     -webkit-font-smoothing:antialiased; }}
body {{
  width:1280px; height:670px; overflow:hidden;
  background:#000000; position:relative;
  font-family:'NotoSansJP','Meiryo',sans-serif;
}}
.accent {{
  position:absolute;
  left:80px; top:72px;
  width:72px; height:6px;
  background:#38bdf8;
  border-radius:3px;
  box-shadow:0 0 18px rgba(56,189,248,.7);
}}
.copy {{
  position:absolute;
  left:80px; top:108px;
}}
.line1 {{
  display:block;
  font-size:86px; font-weight:900;
  color:#FFFFFF; line-height:1.18;
  letter-spacing:-2px;
}}
.line2 {{
  display:block;
  font-size:86px; font-weight:900;
  color:#FFFFFF; line-height:1.18;
  letter-spacing:-2px;
}}
.line3 {{
  display:block;
  font-size:96px; font-weight:900;
  color:#38bdf8; line-height:1.2;
  margin-top:14px; letter-spacing:-2px;
  text-shadow:
    0 0 50px rgba(56,189,248,.6),
    0 0 100px rgba(56,189,248,.28),
    0 0 160px rgba(56,189,248,.12);
}}
.sub {{
  display:block;
  font-size:36px; font-weight:500;
  color:#666666; line-height:1.4;
  margin-top:20px; letter-spacing:.5px;
}}
.author {{
  position:absolute;
  bottom:26px; left:80px;
  font-size:22px; font-weight:400;
  color:#555555; letter-spacing:.3px;
}}
.num {{
  position:absolute;
  bottom:16px; right:60px;
  font-size:80px; font-weight:900;
  color:#38bdf8;
  text-shadow:0 0 30px rgba(56,189,248,.45);
}}
</style></head><body>

<div class="accent"></div>

<div class="copy">
  <span class="line1">{LINE1}</span>
  <span class="line2">{LINE2}</span>
  <span class="line3">{LINE3}</span>
  <span class="sub">{SUB}</span>
</div>

<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="num">{NUM}</p>

</body></html>"""

if __name__ == "__main__":
    print("第42回 サムネイル生成開始 (HTML/CSS + Playwright)...\n")

    out = OUTPUT_DIR / OUTPUT_FNAME
    tmp = ARTICLE_DIR / "_tmp_thumb.html"

    tmp.write_text(THUMBNAIL_HTML, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page    = browser.new_page(viewport={"width": 1280, "height": 670})
        page.goto(f"file:///{tmp.as_posix()}")
        page.wait_for_timeout(900)
        page.screenshot(path=str(out), full_page=False)
        browser.close()

    tmp.unlink(missing_ok=True)

    print(f"✅ {OUTPUT_FNAME}")
    print(f"保存先: {out}")
