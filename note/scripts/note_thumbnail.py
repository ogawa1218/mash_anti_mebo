"""
Longevity Navigator | noteサムネイル生成スクリプト
HTML/CSS + Playwright でPNG出力（1280x670px）
ポートレート画像を右側に配置し、左エッジをグラデーションでフェード
使い方:
  python3 -X utf8 note_thumbnail.py line1 line2 line3 topic [episode_num] [suffix]
"""

import sys, datetime, base64
from pathlib import Path
from playwright.sync_api import sync_playwright

FONT_URL = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
BASE_DIR = Path(r"C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note")
IMAGES_DIR = BASE_DIR / "images"
PORTRAIT_PATH = Path(r"C:/Users/masas/portrait_marcy.png")


def load_portrait_base64():
    if PORTRAIT_PATH.exists():
        with open(PORTRAIT_PATH, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return ""


def build_html(line1, line2, line3, episode_num="", portrait_data=""):
    num_html = (
        "<div style='position:absolute;bottom:40px;right:44px;"
        "font-size:44px;font-weight:900;color:#f97316;"
        "font-family:NotoSansJP;letter-spacing:-0.02em;'>"
        + episode_num + "</div>"
    ) if episode_num else ""

    portrait_html = ""
    if portrait_data:
        portrait_html = (
            "<div class='portrait-wrap'>"
            "<img class='portrait-img' src='" + portrait_data + "'>"
            "</div>"
        )

    portrait_css = ""
    if portrait_data:
        portrait_css = (
            ".portrait-wrap{"
            "position:absolute;right:0;top:0;height:100%;width:580px;"
            "overflow:hidden;"
            "-webkit-mask-image:linear-gradient(to right,transparent 0%,"
            "rgba(0,0,0,0.15) 8%,rgba(0,0,0,0.6) 20%,black 36%,black 100%);"
            "mask-image:linear-gradient(to right,transparent 0%,"
            "rgba(0,0,0,0.15) 8%,rgba(0,0,0,0.6) 20%,black 36%,black 100%);}"
            ".portrait-img{"
            "width:100%;height:100%;"
            "object-fit:cover;object-position:center top;"
            "filter:contrast(1.08) brightness(0.88) saturate(0.9);}"
        )

    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        "@font-face{font-family:'NotoSansJP';src:url('" + FONT_URL + "');}"
        "*{margin:0;padding:0;box-sizing:border-box;}"
        "body{width:1280px;height:670px;background:#000000;overflow:hidden;"
        "font-family:'NotoSansJP',sans-serif;position:relative;}"
        ".accent-line{position:absolute;left:0;top:0;width:6px;height:100%;"
        "background:linear-gradient(180deg,#f97316 0%,#fb923c 50%,transparent 100%);}"
        ".copy-wrap{position:absolute;top:0;left:0;width:730px;height:100%;"
        "display:flex;flex-direction:column;justify-content:center;"
        "padding:0 70px 0 76px;z-index:2;}"
        ".line1{font-size:54px;font-weight:700;color:#ffffff;line-height:1.35;"
        "letter-spacing:-0.02em;}"
        ".line2{font-size:54px;font-weight:700;color:#ffffff;line-height:1.35;"
        "letter-spacing:-0.02em;}"
        ".line3{font-size:68px;font-weight:900;color:#f97316;line-height:1.2;"
        "letter-spacing:-0.03em;margin-top:14px;"
        "text-shadow:0 0 40px rgba(249,115,22,0.55);}"
        ".profile{position:absolute;bottom:38px;left:50px;z-index:3;}"
        ".profile-name{font-size:21px;font-weight:700;color:#ffffff;}"
        ".profile-sub{font-size:15px;color:#9ca3af;margin-top:4px;}"
        + portrait_css
        + "</style></head><body>"
        "<div class='accent-line'></div>"
        + portrait_html
        + "<div class='copy-wrap'>"
        "<div class='line1'>" + line1 + "</div>"
        "<div class='line2'>" + line2 + "</div>"
        "<div class='line3'>" + line3 + "</div>"
        "</div>"
        "<div class='profile'>"
        "<div class='profile-name'>マーシー</div>"
        "<div class='profile-sub'>100kg&#x2192;68kg(-32kg)&#xFF5C;Sub3</div>"
        "</div>"
        + num_html
        + "</body></html>"
    )


def generate_thumbnail(line1, line2, line3, topic, episode_num="", suffix=""):
    today = datetime.date.today().strftime("%Y%m%d")
    safe_topic = topic[:20].replace(" ", "_").replace("\u3000", "_")
    folder = IMAGES_DIR / (today + "_" + safe_topic)
    folder.mkdir(parents=True, exist_ok=True)

    fname = "thumbnail" + (("_" + suffix) if suffix else "")
    html_path = folder / (fname + ".html")
    png_path = folder / (fname + ".png")

    portrait_data = load_portrait_base64()
    html_content = build_html(line1, line2, line3, episode_num, portrait_data)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 670})
        page.goto("file:///" + str(html_path).replace("\\", "/"))
        page.wait_for_timeout(1000)
        page.screenshot(path=str(png_path))
        browser.close()

    print("OK: " + str(png_path))
    return str(png_path)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 4:
        print("Usage: note_thumbnail.py line1 line2 line3 topic [episode_num] [suffix]")
        sys.exit(1)
    generate_thumbnail(
        args[0], args[1], args[2], args[3],
        args[4] if len(args) > 4 else "",
        args[5] if len(args) > 5 else "",
    )
