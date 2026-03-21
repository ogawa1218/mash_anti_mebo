#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "images" / "thumbnails"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_URL = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
PORTRAIT_PATH = Path(
    r"C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note\Image\portrait_marcy.png"
)

VARIANTS = [
    {
        "suffix": "a",
        "line1": "卵を先に食べると",
        "line2": "本当に痩せるのか？",
        "line3": "科学で検証",
    },
    {
        "suffix": "b",
        "line1": "朝の卵2〜3個で",
        "line2": "10時の暴走は",
        "line3": "止まるのか",
    },
    {
        "suffix": "c",
        "line1": "卵は痩せ薬じゃない",
        "line2": "でも朝の食欲設計には",
        "line3": "かなり強い",
    },
]


def portrait_data_uri() -> str:
    if not PORTRAIT_PATH.exists():
        return ""
    data = base64.b64encode(PORTRAIT_PATH.read_bytes()).decode("ascii")
    return "data:image/png;base64," + data


def build_html(line1: str, line2: str, line3: str, portrait_uri: str) -> str:
    portrait = ""
    portrait_css = ""
    if portrait_uri:
        portrait = (
            "<div class='portrait-wrap'>"
            "<img class='portrait-img' src='" + portrait_uri + "'>"
            "</div>"
        )
        portrait_css = (
            ".portrait-wrap{position:absolute;right:0;top:0;width:540px;height:100%;"
            "overflow:hidden;mask-image:linear-gradient(to right,transparent 0%,rgba(0,0,0,.35) 18%,black 42%,black 100%);}"
            ".portrait-img{width:100%;height:100%;object-fit:cover;object-position:center top;"
            "filter:contrast(1.05) brightness(.84) saturate(.9);}"
        )

    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        "@font-face{font-family:'NJ';src:url('" + FONT_URL + "');font-weight:100 900;}"
        "*{margin:0;padding:0;box-sizing:border-box;}"
        "body{width:1280px;height:670px;overflow:hidden;background:#000;position:relative;"
        "font-family:'NJ','Yu Gothic UI',sans-serif;color:#fff;}"
        ".bg{position:absolute;inset:0;background:"
        "radial-gradient(circle at 18% 18%,rgba(56,189,248,.16),transparent 28%),"
        "radial-gradient(circle at 78% 30%,rgba(255,109,0,.22),transparent 32%),"
        "linear-gradient(180deg,#050505 0%,#000 100%);}"
        ".grid{position:absolute;inset:0;opacity:.08;background-image:"
        "linear-gradient(rgba(255,255,255,.08) 1px,transparent 1px),"
        "linear-gradient(90deg,rgba(255,255,255,.08) 1px,transparent 1px);"
        "background-size:48px 48px;}"
        ".accent{position:absolute;left:0;top:0;width:8px;height:100%;"
        "background:linear-gradient(180deg,#ff6d00 0%,#38bdf8 100%);}"
        ".wrap{position:absolute;left:74px;top:0;width:720px;height:100%;display:flex;"
        "flex-direction:column;justify-content:center;z-index:2;}"
        ".eyebrow{font-size:20px;font-weight:800;letter-spacing:.16em;color:#9ca3af;margin-bottom:18px;}"
        ".line1,.line2{font-size:60px;line-height:1.24;font-weight:800;letter-spacing:-.03em;}"
        ".line3{font-size:82px;line-height:1.14;font-weight:900;letter-spacing:-.04em;color:#ff6d00;"
        "text-shadow:0 0 36px rgba(255,109,0,.32);margin-top:12px;}"
        ".badge{position:absolute;top:42px;right:42px;border:1px solid rgba(255,255,255,.18);"
        "border-radius:999px;padding:10px 16px;font-size:18px;font-weight:700;color:#d1d5db;"
        "background:rgba(255,255,255,.04);backdrop-filter:blur(10px);z-index:3;}"
        ".footer{position:absolute;left:52px;bottom:34px;z-index:3;}"
        ".footer-name{font-size:24px;font-weight:800;}"
        ".footer-sub{font-size:16px;color:#9ca3af;margin-top:4px;}"
        ".note{position:absolute;right:44px;bottom:32px;font-size:18px;color:#d1d5db;z-index:3;}"
        + portrait_css
        + "</style></head><body>"
        "<div class='bg'></div>"
        "<div class='grid'></div>"
        "<div class='accent'></div>"
        + portrait
        + "<div class='badge'>第15回｜朝食設計</div>"
        "<div class='wrap'>"
        "<div class='eyebrow'>EGG BREAKFAST</div>"
        "<div class='line1'>" + line1 + "</div>"
        "<div class='line2'>" + line2 + "</div>"
        "<div class='line3'>" + line3 + "</div>"
        "</div>"
        "<div class='footer'><div class='footer-name'>マーシー</div>"
        "<div class='footer-sub'>100kg→68kg(-32kg)｜Sub3 Runner</div></div>"
        "<div class='note'>意志力ではなく、仕組みで変える</div>"
        "</body></html>"
    )


def render(html: str, out_path: Path) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 670})
        page.set_content(html)
        page.wait_for_timeout(900)
        page.screenshot(path=str(out_path))
        browser.close()


def main() -> None:
    portrait_uri = portrait_data_uri()
    for variant in VARIANTS:
        html = build_html(
            variant["line1"],
            variant["line2"],
            variant["line3"],
            portrait_uri,
        )
        html_path = OUTPUT_DIR / f"thumbnail_{variant['suffix']}.html"
        png_path = OUTPUT_DIR / f"thumbnail_{variant['suffix']}.png"
        html_path.write_text(html, encoding="utf-8")
        render(html, png_path)


if __name__ == "__main__":
    main()


