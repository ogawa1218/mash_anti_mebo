#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 サムネイル高品質生成スクリプト
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

LINE1        = "疲れやすいのは"
LINE2        = "歳のせいじゃない。"
LINE3        = "細胞のせいだった。"
SUB          = "ミトコンドリア×ゾーン2で若返る運動科学"
NUM          = "\u2466"
OUTPUT_FNAME = "サムネイル_第13回.png"

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
  background:#FF6D00;
  border-radius:3px;
  box-shadow:0 0 18px rgba(255,109,0,.7);
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
  color:#FF6D00; line-height:1.2;
  margin-top:14px; letter-spacing:-2px;
  text-shadow:
    0 0 50px rgba(255,109,0,.6),
    0 0 100px rgba(255,109,0,.28),
    0 0 160px rgba(255,109,0,.12);
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
  color:#FF6D00;
  text-shadow:0 0 30px rgba(255,109,0,.45);
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
    print("第 サムネイル生成開始 (HTML/CSS + Playwright)...\n")

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

    print(f"OK: {OUTPUT_FNAME}")
    print(f"保存先: {out}")


