#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第41回 X投稿用カード画像 10枚生成スクリプト（図解版）"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
HASHTAG = "#\u7b2c41\u56de \u8840\u7ba1\u3092\u5b88\u308b\u6e1b\u91cf"

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;background:#0d1b2a;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
    ".num{position:absolute;top:28px;right:44px;font-size:20px;font-weight:700;color:#374151;}"
    ".author{position:absolute;bottom:18px;left:44px;font-size:16px;font-weight:400;color:#374151;}"
    ".series{position:absolute;bottom:18px;right:44px;font-size:16px;font-weight:700;}"
    ".title{position:absolute;left:44px;top:72px;font-size:32px;font-weight:900;color:#fff;"
    "letter-spacing:-1px;}"
)

TWEETS = [
    "\u5065\u8a3a\u3092\u7d42\u3048\u305f\u5e30\u308a\u9053\u3001\u305f\u3081\u606f\u3092\u3064\u3044\u305f\u7d4c\u9a13\u306f\u3042\u308a\u307e\u3059\u304b\u3002\n\n\u300c\u307e\u305f\u4eca\u5e74\u3082E\u5224\u5b9a\u2026\u300d\n\u300c\u4f53\u91cd\u306f\u843d\u3068\u3057\u305f\u306e\u306b\u3001\u306a\u3093\u3067\u5909\u308f\u3089\u306a\u3044\u306e\u304b\u300d\n\n\u5b9f\u306f\u3001\u4f53\u91cd\u8a08\u3060\u3051\u3092\u898b\u3066\u3044\u308b\u3068\u672c\u8cea\u3092\u5916\u3057\u3084\u3059\u3044\u3002\n\n\u2193\u7d9a\u304d\uff082/10\uff09",
    "\u540c\u3058\u0033kg\u6e1b\u3067\u3082\u5dee\u304c\u51fa\u308b\u7406\u7531\u3002\n\n\u30fb\u7761\u7720\u0035\u6642\u9593\u30fb\u904b\u52d5\u30bc\u30ed\n\u2192 \u4f53\u91cd\u6e1b\u3067\u3082\u8840\u5727\u307b\u307c\u5909\u308f\u3089\u305a\n\n\u30fb\u7761\u7720\u0037\u6642\u9593\u30fb\u9031\u0033\u56de\u904b\u52d5\n\u2192 \u4f53\u91cd\uff0b\u8840\u7ba1\u30ea\u30b9\u30af\u304c\u6539\u5584\n\n\u300c\u4f55kg\u6e1b\u3063\u305f\u304b\u300d\u3060\u3051\u3067\u306f\u672c\u5f53\u306e\u5909\u5316\u306f\u898b\u3048\u306a\u3044\u3002\n\n\u2193\u7d9a\u304d\uff083/10\uff09",
    "\u4f53\u91cd\u8a08\u306b\u300c3\u3064\u300d\u8ffd\u52a0\u3059\u308b\u3060\u3051\u3067\u7d99\u7d9a\u529b\u304c\u5909\u308f\u308b\u3002\n\n\u2460\u8840\u5727\uff08\u671d\u30fb\u8d77\u5e8a\u5f8c30\u5206\uff09\n\u2461\u8179\u56f2\uff08\u9031\u0031\u56de\uff09\n\u2462\u6d3b\u52d5\u91cf\uff08\u6b69\u6570 or \u904b\u52d5\u6642\u9593\uff09\n\n\u4f53\u91cd\u304c\u505c\u6ede\u3057\u3066\u3082\u4ed6\u306e\u3069\u308c\u304b\u304c\u524d\u9032\u3057\u3066\u3044\u308c\u3070\u300c\u524d\u9032\u4e2d\u300d\u3002\n\n\u2193\u7d9a\u304d\uff084/10\uff09",
    "\u6700\u65b0\u7814\u7a76\u304c\u793a\u30593\u3064\u306e\u4e8b\u5b9f\u3002\n\n\u2460SELECT\u8a66\u9a13\uff08NEJM,2023\uff09\n \u4ecb\u5165\u3067\u5fc3\u8840\u7ba1\u30a4\u30d9\u30f3\u30c8\u304c\u7d0420\uff05\u6e1b\u5c11\n\n\u2461Tasali et al.\uff08JAMA IM,2022\uff09\n \u7761\u7720\u5ef6\u9577\u2192\u81ea\u7136\u306b270kcal/\u65e5\u6e1b\u5c11\n\n\u2462\u904b\u52d5\u4ecb\u5165RCT\uff082024-25\uff09\n \u6709\u6c27\u30fb\u7b4b\u30c8\u30ec\u3067\u8139\u6a5f\u80fd\u6307\u6a19\u3082\u6539\u5584\n\n\u2193\u7d9a\u304d\uff085/10\uff09",
    "\u300c\u591c\u66f4\u304b\u3057\u300d\u3092\u3084\u3081\u308b\u3060\u3051\u3067\u98df\u6b32\u304c\u843d\u3061\u7740\u304f\u3002\n\n\u7761\u7720\u4e0d\u8db3\u2192\u30b0\u30ec\u30ea\u30f3\u2191\u2192\u98df\u6b32\u5897\u52a0\u2192\u591c\u98df\n\u3053\u308c\u304c\u6bce\u6669\u306e\u30eb\u30fc\u30d7\u3002\n\n\u610f\u5fd7\u3067\u6b62\u3081\u3088\u3046\u3068\u3057\u3066\u3082\u9650\u754c\u304c\u3042\u308b\u3002\n\u8a2d\u8a08\u3067\u6b62\u3081\u308b\u3002\n\n\u300c23:30\u5c31\u5bdd\u30eb\u30fc\u30eb\u300d\u3092\u4eca\u591c\u304b\u3089\u6c7a\u3081\u308b\u3060\u3051\u3002\n\n\u2193\u7d9a\u304d\uff086/10\uff09",
    "\u904b\u52d5\u7d99\u7d9a\u7387\u3092\u4e0a\u3052\u308b\u552f\u4e00\u306e\u65b9\u6cd5\u3002\n\n\u300c\u6c17\u304c\u5411\u3044\u305f\u3089\u3084\u308b\u300d\u2192 \u307b\u307c\u3084\u3089\u306a\u3044\n\u300c\u6c7a\u307e\u3063\u305f\u6897\u306b\u4e88\u7d04\u300d\u2192 \u610f\u5fd7\u4e0d\u8981\u3067\u3084\u308b\n\n\u90314\u6897\u00d720\u5206\u3092\u30ab\u30ec\u30f3\u30c0\u30fc\u306b\u5165\u308c\u308b\u3060\u3051\u3002\n\u4eca\u9031\u4e2d\u306b\u6765\u9031\u5206\u3092\u5165\u308c\u308b\u306e\u304c\u6700\u521d\u306e1\u30a2\u30af\u30b7\u30e7\u30f3\u3002\n\n\u2193\u7d9a\u304d\uff087/10\uff09",
    "\u6700\u5c0f\u69cb\u6210\u306e5\u30b9\u30c6\u30c3\u30d7\u3002\n\n1. 23:30\u5c31\u5bdd\u30eb\u30fc\u30eb\u8a2d\u5b9a\n2. 21\u6642\u4ee5\u964d\u30ab\u30ed\u30ea\u30fc\u98f2\u6599\u306a\u3057\n3. \u90314\u6897\u3092\u4eca\u65e5\u30ab\u30ec\u30f3\u30c0\u30fc\u306b\u5165\u308c\u308b\n4. \u30b9\u30af\u30ef\u30c3\u30c815\u56de\uff0b\u30d7\u30c3\u30b7\u30e5\u30a2\u30c3\u30d710\u56de\n5. \u9031\u672b5\u5206\u30664\u8ef8\u30ec\u30d3\u30e5\u30fc\n\n\u5168\u90e8\u3084\u3089\u306a\u304f\u3066\u3044\u3044\u3002\u4eca\u65e5\u306f1\u3064\u3060\u3051\u3002\n\n\u2193\u7d9a\u304d\uff088/10\uff09",
    "\u5d29\u308c\u305f\u9031\u306f\u5fc5\u305a\u6765\u308b\u3002\u305d\u306e\u6642\u306e\u305f\u3081\u306b\u3002\n\n\u5d29\u308c\u305f \u2192\u300c\u6700\u4f4e\u30e9\u30a4\u30f3\u306b\u623b\u3059\u300d\u3060\u3051\n\n\u30fb\u7fd4\u671d10\u5206\u30a6\u30a9\u30fc\u30ad\u30f3\u30b0\u3060\u3051\n\u30fb\u671d\u98df\u3092\u305f\u3093\u3071\u304f\u8caa\u30d5\u30a1\u30fc\u30b9\u30c8\u306b\u623b\u3059\n\u30fb\u30b9\u30af\u30ef\u30c3\u30c83\u56de\u3060\u3051\n\n\u300c\u6b62\u3081\u306a\u304b\u3063\u305f\u300d\u304c\u7fd4\u9031\u306e\u571f\u53f0\u306b\u306a\u308b\u3002\n8\u52dd6\u6557\u3067OK\u3002\n\n\u2193\u7d9a\u304d\uff089/10\uff09",
    "\u904b\u52d5\u306f\u300c\u898b\u305f\u76ee\u300d\u3060\u3051\u3067\u306a\u304f\u300c\u81d3\u5668\u300d\u3092\u5b88\u308b\u3002\n\n2024\uff5e25\u5e74\u306e\u7814\u7a76\u3067\u3001\n\u6709\u6c27\uff0b\u7b4b\u30c8\u30ec\u306e\u7d99\u7d9a\u304c\u8139\u6a5f\u80fd\u6307\u6a19\u3092\u6539\u5584\u3057\u305fRCT\u304c\u8907\u6570\u5831\u544a\u3002\n\n\u300c\u30c0\u30a4\u30a8\u30c3\u30c8\uff1d\u898b\u305f\u76ee\u300d\u304b\u3089\n\u300c\u30c0\u30a4\u30a8\u30c3\u30c8\uff1d10\u5e74\u5f8c\u306e\u81d3\u5668\u3092\u5b88\u308b\u6295\u8cc7\u300d\u306b\u5909\u3048\u308b\u3068\u7d99\u7d9a\u306e\u7406\u7531\u304c\u5909\u308f\u308b\u3002\n\n\u2193\u7d9a\u304d\uff0810/10\uff09",
    "\u4eca\u591c\u3084\u308b\u3053\u30681\u3064\u3060\u3051\u3002\n\n\u6765\u9031\u5206\u306e\u904b\u52d54\u6897\u3092\u30ab\u30ec\u30f3\u30c0\u30fc\u306b\u5165\u308c\u308b\u3002\n\n\u4f53\u91cd\u8a08\u3060\u3051\u3067\u81ea\u5206\u3092\u8a55\u4fa1\u3059\u308b\u306e\u3092\u3084\u3081\u305f\u65e5\u304c\u672c\u5f53\u306e\u5909\u5316\u306e\u59cb\u307e\u308a\u3002\n\n\u8840\u7ba1\u3092\u5b88\u308b\u6e1b\u91cf\u306e\u5168\u30b9\u30c6\u30c3\u30d7\u306fnote\u3067\u25bc\nhttps://note.com/mash_anti_metabo\n\n#\u4e0d\u8001\u9577\u5bff #\u5065\u5eb7 #\u30c0\u30a4\u30a8\u30c3\u30c8 #\u6700\u65b0\u7814\u7a76 #Longevity",
]

CARD_TAGS = ["\u5171\u611f", "\u539f\u56e0", "\u89e3\u6c7a\u7b56", "\u4ed5\u7d44\u307f", "\u52b9\u679c",
             "\u8a2d\u8a08", "\u5b9f\u8df5", "\u5fa9\u5e30", "\u6df1\u6398\u308a", "\u4eca\u591c\u3084\u308b\u3053\u3068"]

ACCENT_COLORS = ["#38bdf8","#38bdf8","#FF6D00","#38bdf8","#4ade80",
                 "#38bdf8","#FF6D00","#4ade80","#38bdf8","#FF6D00"]

def render(html, fname):
    tmp = ARTICLE_DIR / "_tmp_xcard.html"
    out = OUTPUT_DIR / fname
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto("file:///" + str(tmp).replace("\\", "/"))
        page.wait_for_timeout(800)
        page.screenshot(path=str(out), full_page=False)
        browser.close()
    tmp.unlink(missing_ok=True)

def card_common_header(num_str, tag, accent):
    return (
        "<div class='num'>" + num_str + "</div>"
        "<div class='author'>\u30de\u30fc\u30b7\u30fc\uff5c100kg\u219268kg\uff5cSub3</div>"
        "<div class='series' style='color:" + accent + ";'>" + HASHTAG + "</div>"
    )

def card_01():
    """共感：タイムライン型"""
    c = ACCENT_COLORS[0]
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".tl-item{position:absolute;left:120px;display:flex;align-items:flex-start;gap:20px;}"
        ".tl-dot{width:20px;height:20px;border-radius:50%;margin-top:4px;flex-shrink:0;}"
        ".tl-line{position:absolute;left:129px;width:2px;background:#374151;}"
        ".tl-time{font-size:18px;color:#9ca3af;min-width:72px;margin-top:3px;}"
        ".tl-text{font-size:20px;color:#e5e7eb;line-height:1.5;}"
        ".tl-emo{font-size:22px;font-weight:900;margin-top:4px;}"
        "</style></head><body>"
        + card_common_header("1/10", CARD_TAGS[0], c) +
        "<div class='title' style='color:" + c + ";'>\u4e00\u5e74\u3067\u4e00\u756a\u8f9b\u3044\u65e5</div>"
        "<div class='tl-line' style='top:130px;height:420px;'></div>"
        # Item 1
        "<div class='tl-item' style='top:130px;'>"
        "<div class='tl-dot' style='background:#ef4444;'></div>"
        "<div><div class='tl-time'>9:00 AM</div>"
        "<div class='tl-text'>\u5065\u8a3a\u7d50\u679c\u3092\u5c01\u7b52\u3067\u53d7\u3051\u53d6\u308b</div>"
        "</div></div>"
        # Item 2
        "<div class='tl-item' style='top:225px;'>"
        "<div class='tl-dot' style='background:#f97316;'></div>"
        "<div><div class='tl-time'>9:05 AM</div>"
        "<div class='tl-text'>\u958b\u5c01\u2026\u300c\u307e\u305fE\u5224\u5b9a\u300d<br>"
        "<span class='tl-emo' style='color:#ef4444;'>\u300c\u3084\u3063\u3066\u308b\u306e\u306b\u3001\u306a\u3093\u3067\u2026\u300d</span></div>"
        "</div></div>"
        # Item 3
        "<div class='tl-item' style='top:345px;'>"
        "<div class='tl-dot' style='background:#eab308;'></div>"
        "<div><div class='tl-time'>9:10 AM</div>"
        "<div class='tl-text'>\u4f53\u91cd\u6b04\u3060\u3051\u5c11\u3057\u4e0b\u304c\u3063\u305f<br>"
        "<span style='color:#9ca3af;'>\u8840\u5727\u30fb\u8179\u56f2\u306f\u307b\u307c\u540c\u3058\u2026</span></div>"
        "</div></div>"
        # Item 4
        "<div class='tl-item' style='top:450px;'>"
        "<div class='tl-dot' style='background:" + c + ";'></div>"
        "<div><div class='tl-time'>?</div>"
        "<div class='tl-text' style='color:" + c + ";font-weight:700;'>"
        "\u8a55\u4fa1\u8ef8\u304c\u305a\u308c\u3066\u3044\u308b\u3060\u3051\u304b\u3082</div>"
        "</div></div>"
        "</body></html>"
    )
    return html

def card_02():
    """原因：フロー図型"""
    c = ACCENT_COLORS[1]
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".flow-card{position:absolute;height:88px;border-radius:12px;"
        "display:flex;align-items:center;padding:0 20px;}"
        ".flow-title{font-size:20px;font-weight:900;}"
        ".flow-sub{font-size:15px;color:rgba(255,255,255,.65);margin-top:4px;}"
        ".flow-arr{position:absolute;font-size:28px;color:#374151;}"
        "</style></head><body>"
        + card_common_header("2/10", CARD_TAGS[1], c) +
        "<div class='title' style='color:" + c + ";'>\u540c\u3058\u0033kg\u6e1b\u3067\u3082\u5dee\u304c\u51fa\u308b</div>"
        # Left column (NG)
        "<div style='position:absolute;top:130px;left:44px;font-size:16px;color:#ef4444;font-weight:700;'>\u2717 \u7761\u7720\u0035\u6642\u9593\u30fb\u904b\u52d5\u30bc\u30ed</div>"
        "<div class='flow-card' style='background:#1f1010;border:2px solid #ef4444;top:162px;left:44px;width:520px;'>"
        "<div><div class='flow-title' style='color:#ef4444;'>\u4f53\u91cd -3kg</div>"
        "<div class='flow-sub'>\u8840\u5727\uff1a\u307b\u307c\u5909\u5316\u306a\u3057</div></div></div>"
        "<div class='flow-arr' style='top:268px;left:44px;'>\u2193</div>"
        "<div class='flow-card' style='background:#1f1010;border:1px solid #374151;top:304px;left:44px;width:520px;'>"
        "<div><div class='flow-title' style='color:#9ca3af;'>\u7b4b\u8089\u3082\u843d\u3061\u308b\u30fb\u30ea\u30d0\u30a6\u30f3\u30c9\u30ea\u30b9\u30af\u2191</div>"
        "<div class='flow-sub'>\u8840\u7ba1\u30ea\u30b9\u30af\u306f\u6539\u5584\u3055\u308c\u306a\u3044</div></div></div>"
        # Right column (OK)
        "<div style='position:absolute;top:130px;left:640px;font-size:16px;color:#4ade80;font-weight:700;'>\u2713 \u7761\u7720\u0037\u6642\u9593\u30fb\u9031\u0033\u56de\u904b\u52d5</div>"
        "<div class='flow-card' style='background:#0a1f0a;border:2px solid #4ade80;top:162px;left:640px;width:520px;'>"
        "<div><div class='flow-title' style='color:#4ade80;'>\u4f53\u91cd -3kg</div>"
        "<div class='flow-sub'>\u8840\u5727\uff1a\u6539\u5584\u30fb\u8179\u56f2\u6e1b\u5c11</div></div></div>"
        "<div class='flow-arr' style='top:268px;left:640px;'>\u2193</div>"
        "<div class='flow-card' style='background:#0a1f0a;border:1px solid #4ade80;top:304px;left:640px;width:520px;'>"
        "<div><div class='flow-title' style='color:#4ade80;'>\u7b4b\u8089\u7dad\u6301\u30fb\u4f53\u8102\u80aa\u6e1b\u5c11</div>"
        "<div class='flow-sub'>\u8840\u7ba1\u30ea\u30b9\u30af\u3082\u4f4e\u4e0b</div></div></div>"
        # Bottom
        "<div style='position:absolute;bottom:48px;left:44px;right:44px;"
        "background:#1e2a3a;border-radius:8px;padding:12px;text-align:center;"
        "font-size:19px;color:" + c + ";font-weight:700;'>"
        "4\u8ef8\u3067\u8a55\u4fa1\u3059\u308b\u3068\u300c\u672c\u5f53\u306e\u5909\u5316\u300d\u304c\u898b\u3048\u308b</div>"
        "</body></html>"
    )
    return html

def card_03():
    """解決策：横3列ステップカード"""
    c = ACCENT_COLORS[2]
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".step-card{position:absolute;width:340px;height:270px;border-radius:16px;"
        "display:flex;flex-direction:column;align-items:center;"
        "justify-content:center;gap:10px;padding:20px;}"
        ".s-num{font-size:52px;font-weight:900;}"
        ".s-title{font-size:24px;font-weight:900;color:#fff;text-align:center;}"
        ".s-detail{font-size:16px;text-align:center;line-height:1.5;}"
        ".arrow-mid{position:absolute;top:278px;font-size:34px;color:#374151;font-weight:900;}"
        "</style></head><body>"
        + card_common_header("3/10", CARD_TAGS[2], c) +
        "<div class='title' style='color:" + c + ";'>\u8a55\u4fa1\u8ef8\u3092\u00b33\u3064\u300d\u8ffd\u52a0\u3059\u308b\u3060\u3051</div>"
        "<div class='step-card' style='background:#1e3a5f;top:130px;left:44px;'>"
        "<div class='s-num' style='color:#38bdf8;'>\u2460</div>"
        "<div class='s-title'>\u8840\u3000\u5727</div>"
        "<div class='s-detail' style='color:#9ca3af;'>\u6bce\u671d\u8d77\u5e8a\u5f8c30\u5206<br>130mmHg\u4ee5\u4e0b\u76ee\u6a19</div>"
        "</div>"
        "<div class='arrow-mid' style='left:393px;'>\u2192</div>"
        "<div class='step-card' style='background:#1a3a2a;top:130px;left:470px;'>"
        "<div class='s-num' style='color:#4ade80;'>\u2461</div>"
        "<div class='s-title'>\u8179\u3000\u56f2</div>"
        "<div class='s-detail' style='color:#9ca3af;'>\u9031\u00b11\u56de<br>\u540c\u3058\u6642\u9593\u5e2f\u306b\u8a08\u6e2c</div>"
        "</div>"
        "<div class='arrow-mid' style='left:819px;'>\u2192</div>"
        "<div class='step-card' style='background:#2d1b00;top:130px;left:896px;'>"
        "<div class='s-num' style='color:#FF6D00;'>\u2462</div>"
        "<div class='s-title'>\u6d3b\u52d5\u91cf</div>"
        "<div class='s-detail' style='color:#9ca3af;'>\u6b69\u6570\u307e\u305f\u306f<br>\u9031\u306e\u904b\u52d5\u6642\u9593</div>"
        "</div>"
        "<div style='position:absolute;bottom:48px;left:44px;right:44px;"
        "background:#2d1b00;border:2px solid " + c + ";border-radius:10px;"
        "padding:14px;text-align:center;font-size:20px;color:" + c + ";font-weight:700;'>"
        "\u4f53\u91cd\u505c\u6ede\u3067\u3082\u300c\u8840\u5727\u304c\u4e0b\u304c\u3063\u305f\u300d\u306f\u524d\u9032</div>"
        "</body></html>"
    )
    return html

def card_04():
    """仕組み：番号付きカード"""
    c = ACCENT_COLORS[3]
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".rcard{position:absolute;left:44px;width:1192px;border-radius:12px;"
        "display:flex;align-items:center;padding:16px 24px;gap:20px;}"
        ".rnum{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;"
        "justify-content:center;font-size:22px;font-weight:900;color:#fff;flex-shrink:0;}"
        ".rtitle{font-size:20px;font-weight:900;margin-bottom:4px;}"
        ".rsub{font-size:16px;color:#9ca3af;line-height:1.4;}"
        ".src-badge{display:inline-block;background:#1e293b;border:1px solid #374151;"
        "color:#9ca3af;font-size:12px;padding:2px 8px;border-radius:6px;margin-left:8px;}"
        "</style></head><body>"
        + card_common_header("4/10", CARD_TAGS[3], c) +
        "<div class='title' style='color:" + c + ";'>\u6700\u65b0\u7814\u7a76\u304c\u793a\u30593\u3064\u306e\u5909\u5316</div>"
        "<div class='rcard' style='background:#1e3a5f;top:130px;'>"
        "<div class='rnum' style='background:#38bdf8;'>1</div>"
        "<div><div class='rtitle' style='color:#38bdf8;'>\u8a55\u4fa1\u8ef8\u304c\u300ckg\u300d\u304b\u3089\u300c\u5fc3\u8840\u7ba1\u30a4\u30d9\u30f3\u30c8\u300d\u3078"
        "<span class='src-badge'>SELECT\u8a66\u9a13 NEJM 2023</span></div>"
        "<div class='rsub'>\u4ecb\u5165\u306b\u3088\u308a\u5fc3\u8840\u7ba1\u30a4\u30d9\u30f3\u30c8\u7d04<b style='color:#38bdf8;'>20\uff05\u6e1b\u5c11</b>\u3002\u300c\u4f55kg\u843d\u3061\u305f\u304b\u300d\u3060\u3051\u3067\u306a\u304f\u8840\u7ba1\u3092\u5b88\u308c\u305f\u304b\u304c\u8a55\u4fa1\u57fa\u6e96\u306b</div>"
        "</div></div>"
        "<div class='rcard' style='background:#1a3a2a;top:258px;'>"
        "<div class='rnum' style='background:#4ade80;'>2</div>"
        "<div><div class='rtitle' style='color:#4ade80;'>\u7761\u7720\u5ef6\u9577\u3067\u81ea\u7136\u306b270kcal/\u65e5\u6e1b"
        "<span class='src-badge'>Tasali et al. JAMA IM 2022</span></div>"
        "<div class='rsub'>\u7761\u7720\u6642\u9593\u3092\u5ef6\u3070\u3059\u3060\u3051\u3067\u98df\u6b32\u304c\u81ea\u7136\u306b\u843d\u3061\u7740\u304f\u3002\u610f\u5fd7\u4e0d\u8981\u3002\u5c31\u5bdd\u8a2d\u8a08\u304c\u5148</div>"
        "</div></div>"
        "<div class='rcard' style='background:#2d1b00;top:386px;'>"
        "<div class='rnum' style='background:#FF6D00;'>3</div>"
        "<div><div class='rtitle' style='color:#FF6D00;'>\u904b\u52d5\u3067\u8139\u6a5f\u80fd\u6307\u6a19\u3082\u6539\u5584"
        "<span class='src-badge'>RCT 2024-2025</span></div>"
        "<div class='rsub'>\u6709\u6c27\uff0b\u7b4b\u30c8\u30ec\u306e\u7d99\u7d9a\u3067\u8139\u6a5f\u80fd\u6307\u6a19\u6539\u5584\u3002\u904b\u52d5\u306f\u81d3\u5668\u3092\u5b88\u308b\u300c\u81d3\u5668\u4fdd\u8b77\u884c\u52d5\u300d\u3067\u3082\u3042\u308b</div>"
        "</div></div>"
        "</body></html>"
    )
    return html

def card_05():
    """効果：Before/After比較パネル"""
    c = ACCENT_COLORS[4]
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".panel{position:absolute;width:555px;height:430px;border-radius:16px;padding:24px;}"
        ".p-title{font-size:28px;font-weight:900;margin-bottom:16px;}"
        ".p-item{font-size:18px;margin-bottom:12px;display:flex;gap:10px;line-height:1.4;}"
        ".badge{font-size:20px;min-width:24px;}"
        "</style></head><body>"
        + card_common_header("5/10", CARD_TAGS[4], c) +
        "<div class='title' style='color:" + c + ";'>\u7761\u7720\u8a2d\u8a08\u524d vs \u5f8c</div>"
        # Before
        "<div class='panel' style='background:#1f0a0a;border:2px solid #ef4444;top:108px;left:36px;'>"
        "<div class='p-title' style='color:#ef4444;'>\u2717 \u7761\u7720\u5d29\u58ca\u4e2d</div>"
        "<div class='p-item'><span class='badge' style='color:#ef4444;'>\u2192</span>"
        "<span style='color:#d1d5db;'>\u5e73\u65e5\u6bce\u65e55\u6642\u9593\u4ee5\u4e0b</span></div>"
        "<div class='p-item'><span class='badge' style='color:#ef4444;'>\u2192</span>"
        "<span style='color:#d1d5db;'>\u591c11\u6642\u3001\u304a\u83d3\u5b50\u306b\u624b\u304c\u4f38\u3073\u308b</span></div>"
        "<div class='p-item'><span class='badge' style='color:#ef4444;'>\u2192</span>"
        "<span style='color:#d1d5db;'>\u7d61\u3093\u3067\u3082\u7fd4\u65e5\u306f\u30c0\u30eb\u304f\u904b\u52d5\u6253\u5207\u308c</span></div>"
        "<div class='p-item'><span class='badge' style='color:#ef4444;'>\u2192</span>"
        "<span style='color:#d1d5db;'>\u98f3\u3093\u3067\u3082\u98f2\u307f\u8fc7\u304e\u304c\u6b62\u307e\u3089\u306a\u3044</span></div>"
        "<div style='background:#2d1010;border-radius:8px;padding:12px;margin-top:8px;"
        "font-size:17px;color:#ef4444;text-align:center;font-weight:700;'>"
        "\u5168\u65bd\u7b56\u304c\u5d29\u308c\u308b\u30eb\u30fc\u30d7</div>"
        "</div>"
        # After
        "<div class='panel' style='background:#0a1f0a;border:2px solid " + c + ";top:108px;left:689px;'>"
        "<div class='p-title' style='color:" + c + ";'>\u2713 23:30\u5c31\u5bdd\u30eb\u30fc\u30eb\u5f8c</div>"
        "<div class='p-item'><span class='badge' style='color:" + c + ";'>\u2192</span>"
        "<span style='color:#d1d5db;'>\u7761\u73502\u6642\u9593\u5897\u3067\u7761\u8cea\u5b89\u5b9a</span></div>"
        "<div class='p-item'><span class='badge' style='color:" + c + ";'>\u2192</span>"
        "<span style='color:#d1d5db;'>\u591c11\u6642\u306e\u304a\u83d3\u5b50\u885d\u52d5\u304c\u81ea\u7136\u306b\u843d\u3061\u7740\u304f</span></div>"
        "<div class='p-item'><span class='badge' style='color:" + c + ";'>\u2192</span>"
        "<span style='color:#d1d5db;'>\u7fd4\u671d\u306e\u904b\u52d5\u6800\u304c\u7d9a\u304f\u3088\u3046\u306b\u306a\u308b</span></div>"
        "<div class='p-item'><span class='badge' style='color:" + c + ";'>\u2192</span>"
        "<span style='color:#d1d5db;'>\u98f3\u7832\u306e\u98f2\u307f\u9077\u304e\u307e\u3067\u6e1b\u308b</span></div>"
        "<div style='background:#0a2d0a;border-radius:8px;padding:12px;margin-top:8px;"
        "font-size:17px;color:" + c + ";text-align:center;font-weight:700;'>"
        "\u610f\u5fd7\u4e0d\u8981\u3002\u7761\u7720\u8a2d\u8a08\u304c\u5168\u90e8\u3092\u6b63\u3059</div>"
        "</div>"
        "</body></html>"
    )
    return html

def card_06():
    """設計：テーブル型"""
    c = ACCENT_COLORS[5]
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "table{position:absolute;top:116px;left:36px;width:1208px;border-collapse:collapse;}"
        "th{background:#1e3a5f;color:#38bdf8;font-size:18px;font-weight:700;"
        "padding:12px 16px;text-align:left;border-bottom:2px solid #38bdf8;}"
        "td{font-size:17px;color:#e5e7eb;padding:12px 16px;border-bottom:1px solid #1e293b;"
        "line-height:1.5;}"
        "tr:nth-child(odd) td{background:#0f1f30;}"
        "tr:nth-child(even) td{background:#0d1b2a;}"
        ".badge{display:inline-block;color:#fff;"
        "font-size:14px;font-weight:900;padding:2px 10px;border-radius:8px;margin-right:6px;}"
        "</style></head><body>"
        + card_common_header("6/10", CARD_TAGS[5], c) +
        "<div class='title' style='color:" + c + ";'>\u9031\u00b14\u6897\u00d720\u5206\u30ea\u30ba\u30e0\u30d7\u30e9\u30f3</div>"
        "<table>"
        "<tr><th>\u66dc\u65e5</th><th>\u904b\u52d5\u5185\u5bb9</th><th>\u6642\u9593</th><th>\u5834\u6240</th></tr>"
        "<tr><td><span class='badge' style='background:#38bdf8;'>\u6708</span></td>"
        "<td>\u6709\u6c27\uff1a\u30a6\u30a9\u30fc\u30ad\u30f3\u30b020\u5206</td><td>20\u5206</td><td>\u901a\u52e4\u9014\u4e2d\u306e\u9060\u56de\u308a</td></tr>"
        "<tr><td><span class='badge' style='background:#4ade80;'>\u6c34</span></td>"
        "<td>\u7b4b\u30c8\u30ec\uff1a\u30b9\u30af\u30ef\u30c3\u30c815\u56de\uff0b\u30d7\u30c3\u30b7\u30e5\u30a2\u30c3\u30d710\u56de</td><td>10\u5206</td><td>\u6606\u4f11\u307f\u30fb\u5c45\u5ba4</td></tr>"
        "<tr><td><span class='badge' style='background:#FF6D00;'>\u91d1</span></td>"
        "<td>\u6709\u6c27\uff1a\u30b8\u30e7\u30ae\u30f320\u5206</td><td>20\u5206</td><td>\u8fd1\u6240\u516c\u5712\u30fb\u901a\u52e4\u9014</td></tr>"
        "<tr><td><span class='badge' style='background:#a78bfa;'>\u571f</span></td>"
        "<td>\u30b3\u30f3\u30dc\uff1a\u6709\u6c27\uff0b\u7b4b\u30c8\u30ec30\u5206</td><td>30\u5206</td><td>\u81ea\u5b85\u307e\u305f\u306f\u30b8\u30e0</td></tr>"
        "</table>"
        "<div style='position:absolute;bottom:48px;left:36px;right:36px;"
        "background:#2d1b00;border:2px solid " + c + ";border-radius:10px;"
        "padding:12px;text-align:center;font-size:18px;color:" + c + ";font-weight:700;'>"
        "\u4eca\u65e5\u4e2d\u306b\u30ab\u30ec\u30f3\u30c0\u30fc\u306b\u5165\u308c\u308b\u3060\u3051\u3002\u6790\u308c\u305f\u65e5\u306f\u7fd4\u65e5\u306b\u30b9\u30e9\u30a4\u30c9OK</div>"
        "</body></html>"
    )
    return html

def card_07():
    """実践：縦フロー型"""
    c = ACCENT_COLORS[6]
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".vcard{position:absolute;left:100px;width:1080px;height:82px;border-radius:12px;"
        "display:flex;align-items:center;padding:0 20px;gap:18px;}"
        ".vnum{width:48px;height:48px;border-radius:50%;display:flex;align-items:center;"
        "justify-content:center;font-size:22px;font-weight:900;color:#fff;flex-shrink:0;}"
        ".vcon{flex:1;}"
        ".vtitle{font-size:19px;font-weight:900;color:#fff;}"
        ".vsub{font-size:14px;color:#9ca3af;margin-top:2px;}"
        ".varr{position:absolute;left:640px;font-size:24px;color:#374151;}"
        "</style></head><body>"
        + card_common_header("7/10", CARD_TAGS[6], c) +
        "<div class='title' style='color:" + c + ";'>\u6700\u5c0f\u69cb\u6210\u00b75\u30b9\u30c6\u30c3\u30d7</div>"
        "<div class='vcard' style='background:#1e3a5f;top:120px;'>"
        "<div class='vnum' style='background:#38bdf8;'>1</div>"
        "<div class='vcon'><div class='vtitle'>\u5c31\u5bdd\u6642\u523b\u306e\u4e0b\u9650\u8a2d\u5b9a</div>"
        "<div class='vsub'>23:30\u4ee5\u964d\u306f\u30b9\u30af\u30ed\u30fc\u30eb\u505c\u6b62\u30fb\u5c31\u5bdd</div></div></div>"
        "<div class='varr' style='top:214px;'>\u2193</div>"
        "<div class='vcard' style='background:#1a3a2a;top:226px;'>"
        "<div class='vnum' style='background:#4ade80;'>2</div>"
        "<div class='vcon'><div class='vtitle'>21\u6642\u4ee5\u964d\u30ab\u30ed\u30ea\u30fc\u98f2\u6599\u306a\u3057</div>"
        "<div class='vsub'>\u7518\u3044\u3082\u306e\u306f\u7fd4\u671d\u3078\u30b9\u30e9\u30a4\u30c9</div></div></div>"
        "<div class='varr' style='top:320px;'>\u2193</div>"
        "<div class='vcard' style='background:#2d1b00;top:332px;'>"
        "<div class='vnum' style='background:#FF6D00;'>3</div>"
        "<div class='vcon'><div class='vtitle'>\u9031\u00b14\u6897\u3092\u4eca\u65e5\u30ab\u30ec\u30f3\u30c0\u30fc\u306b\u5165\u308c\u308b</div>"
        "<div class='vsub'>20\uff5e30\u5206\u306e\u904b\u52d5\u6800\u3002\u4eca\u65e5\u4e2d\u306b\u8a2d\u5b9a\u5b8c\u4e86</div></div></div>"
        "<div class='varr' style='top:426px;'>\u2193</div>"
        "<div class='vcard' style='background:#1e3a5f;top:438px;'>"
        "<div class='vnum' style='background:#38bdf8;'>4</div>"
        "<div class='vcon'><div class='vtitle'>\u30b9\u30af\u30ef\u30c3\u30c815\u56de\uff0b\u30d7\u30c3\u30b7\u30e5\u30a2\u30c3\u30d710\u56de</div>"
        "<div class='vsub'>2\u7a2e\u76ee\u3060\u3051\u3002\u6700\u5c0f\u69cb\u6210\u3067\u5b8c\u7be7\u3092\u512a\u5148</div></div></div>"
        "<div class='varr' style='top:532px;'>\u2193</div>"
        "<div class='vcard' style='background:#1a3a2a;top:544px;'>"
        "<div class='vnum' style='background:#4ade80;'>5</div>"
        "<div class='vcon'><div class='vtitle'>\u9031\u672b5\u5206\u30664\u8ef8\u30ec\u30d3\u30e5\u30fc</div>"
        "<div class='vsub'>\u4f53\u91cd\u30fb\u8840\u5727\u30fb\u8179\u56f2\u30fb\u6d3b\u52d5\u91cf\u306e\u3069\u308c\u304b\u304c\u6539\u5584\u3067\u300c\u524d\u9032\u300d</div></div></div>"
        "</body></html>"
    )
    return html

def card_08():
    """復帰：リカバリーフロー"""
    c = ACCENT_COLORS[7]
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".rflow{position:absolute;left:80px;width:1120px;border-radius:14px;"
        "padding:18px 24px;display:flex;align-items:center;gap:18px;}"
        ".rf-num{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;"
        "justify-content:center;font-size:24px;font-weight:900;color:#fff;flex-shrink:0;}"
        ".rf-title{font-size:22px;font-weight:900;margin-bottom:4px;}"
        ".rf-sub{font-size:15px;line-height:1.45;}"
        ".rf-arr{position:absolute;left:620px;font-size:28px;color:#6b7280;}"
        "</style></head><body>"
        + card_common_header("8/10", CARD_TAGS[7], c) +
        "<div class='title' style='color:" + c + ";'>\u5d29\u308c\u305f\u9031\u306e\u6700\u4f4e\u30e9\u30a4\u30f3\u8a2d\u8a08</div>"
        "<div class='rflow' style='background:#2d1010;border:2px solid #ef4444;top:120px;'>"
        "<div class='rf-num' style='background:#ef4444;'>1</div>"
        "<div><div class='rf-title' style='color:#ef4444;'>\u5d29\u308c\u305f\uff01\u5168\u505c\u6b62\u30e2\u30fc\u30c9</div>"
        "<div class='rf-sub' style='color:#9ca3af;'>\u81ea\u5df1\u5448\u60aa\u306b\u5165\u3089\u306a\u3044\u3002\u4ed5\u7d44\u307f\u306e\u554f\u984c\u3001\u610f\u5fd7\u306e\u554f\u984c\u3058\u3083\u306a\u3044</div>"
        "</div></div>"
        "<div class='rf-arr' style='top:243px;'>\u2193</div>"
        "<div class='rflow' style='background:#2d1f00;border:2px solid #f59e0b;top:280px;'>"
        "<div class='rf-num' style='background:#f59e0b;'>2</div>"
        "<div><div class='rf-title' style='color:#f59e0b;'>\u6700\u4f4e\u30e9\u30a4\u30f3\u3092\u78ba\u8a8d\u3059\u308b</div>"
        "<div class='rf-sub' style='color:#9ca3af;'>"
        "\u30fb\u7fd4\u671d10\u5206\u30a6\u30a9\u30fc\u30ad\u30f3\u30b0\u3060\u3051\u3000\u30fb\u671d\u98df\u3092\u305f\u3093\u3071\u304f\u8caa\u30d5\u30a1\u30fc\u30b9\u30c8\u306b\u623b\u3059\u3000\u30fb\u30b9\u30af\u30ef\u30c3\u30c83\u56de\u3060\u3051</div>"
        "</div></div>"
        "<div class='rf-arr' style='top:403px;'>\u2193</div>"
        "<div class='rflow' style='background:#0a1f0a;border:2px solid " + c + ";top:440px;'>"
        "<div class='rf-num' style='background:" + c + ";'>3</div>"
        "<div><div class='rf-title' style='color:" + c + ";'>7\u5206\u3067\u30ea\u30b9\u30bf\u30fc\u30c8 \u2192 \u7fd4\u9031\u3078</div>"
        "<div class='rf-sub' style='color:#9ca3af;'>20\u5206\u304c\u7121\u7406\u306a\u30897\u5206\u3002\u300c\u6b62\u3081\u306a\u304b\u3063\u305f\u300d\u304c\u7fd4\u9031\u306e\u571f\u53f0\u306b\u306a\u308b</div>"
        "</div></div>"
        "<div style='position:absolute;bottom:22px;left:80px;width:1120px;"
        "text-align:center;font-size:20px;color:" + c + ";font-weight:700;'>"
        "8\u52dd6\u6557\u3067OK\uff5c\u5d29\u308c\u305f\u5f8c\u306b\u623b\u308c\u308b\u304b\u304c\u672c\u5f53\u306e\u5b9f\u529b</div>"
        "</body></html>"
    )
    return html

def card_09():
    """深掘り：CSSグラフ+説明カード"""
    c = ACCENT_COLORS[8]
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".bar-wrap{position:absolute;left:60px;top:120px;width:580px;}"
        ".bar-label{font-size:16px;color:#9ca3af;margin-bottom:4px;}"
        ".bar-row{display:flex;align-items:center;gap:10px;margin-bottom:14px;}"
        ".bar-bg{width:460px;height:36px;background:#1e2a3a;border-radius:6px;overflow:hidden;}"
        ".bar-fill{height:36px;border-radius:6px;display:flex;align-items:center;"
        "padding-left:10px;font-size:14px;font-weight:700;color:#fff;}"
        ".bar-val{font-size:16px;font-weight:700;color:#e5e7eb;min-width:48px;}"
        ".note-card{position:absolute;top:120px;left:700px;width:520px;border-radius:14px;"
        "padding:24px;}"
        ".nc-title{font-size:22px;font-weight:900;margin-bottom:12px;}"
        ".nc-item{font-size:16px;margin-bottom:10px;display:flex;gap:10px;line-height:1.4;}"
        "</style></head><body>"
        + card_common_header("9/10", CARD_TAGS[8], c) +
        "<div class='title' style='color:" + c + ";'>\u904b\u52d5\u304c\u81d3\u5668\u3092\u5b88\u308b\u30c7\u30fc\u30bf</div>"
        # Bar chart
        "<div class='bar-wrap'>"
        "<div class='bar-label'>\u7d50\u679c\u306e\u5dee\uff08\u904b\u52d5\u7d99\u7d9a\u6709 vs \u7121\uff09</div>"
        "<div class='bar-row'>"
        "<span style='font-size:15px;color:#9ca3af;min-width:100px;'>\u4f53\u91cd\u6e1b\u5c11</span>"
        "<div class='bar-bg'><div class='bar-fill' style='width:85%;background:#38bdf8;'>-8.2%</div></div>"
        "</div><div class='bar-row'>"
        "<span style='font-size:15px;color:#9ca3af;min-width:100px;'>\u8840\u5727\u6539\u5584</span>"
        "<div class='bar-bg'><div class='bar-fill' style='width:72%;background:#4ade80;'>-6.3 mmHg</div></div>"
        "</div><div class='bar-row'>"
        "<span style='font-size:15px;color:#9ca3af;min-width:100px;'>\u8139\u6a5f\u80fd\u6307\u6a19</span>"
        "<div class='bar-bg'><div class='bar-fill' style='width:60%;background:#FF6D00;'>\u6539\u5584\u7b4b</div></div>"
        "</div><div class='bar-row'>"
        "<span style='font-size:15px;color:#9ca3af;min-width:100px;'>\u4f53\u8102\u80aa\u7387</span>"
        "<div class='bar-bg'><div class='bar-fill' style='width:78%;background:#a78bfa;'>-3.1%</div></div>"
        "</div>"
        "<div style='margin-top:12px;font-size:13px;color:#6b7280;'>\u51fa\u5178\uff1aRCT\u7dcf\u5408\uff082024\uff5e2025\u5e74\uff09\u3088\u308a\u7b46\u8005\u5f15\u7528</div>"
        "</div>"
        # Note card
        "<div class='note-card' style='background:#1e3a5f;border:2px solid " + c + ";'>"
        "<div class='nc-title' style='color:" + c + ";'>\u904b\u52d5\u306e\u76ee\u7684\u3092\u5c45\u3048\u308b</div>"
        "<div class='nc-item'><span style='color:#ef4444;'>\u2717</span>"
        "<span style='color:#d1d5db;'>\u898b\u305f\u76ee\u3060\u3051\u3092\u76ee\u6a19\u306b\u3059\u308b\u2026\u505c\u6ede\u3067\u632b\u6298</span></div>"
        "<div class='nc-item'><span style='color:" + c + ";'>\u2713</span>"
        "<span style='color:#d1d5db;'>10\u5e74\u5f8c\u306e\u81d3\u5668\u3092\u5b88\u308b\u300c\u6295\u8cc7\u300d\u3068\u601d\u3046</span></div>"
        "<div class='nc-item'><span style='color:" + c + ";'>\u2713</span>"
        "<span style='color:#d1d5db;'>\u904b\u52d5\u6bce\u56de\u304c\u300c\u81d3\u5668\u3078\u306e\u6a4f\u91d1\u300d\u306b\u306a\u308b</span></div>"
        "<div style='margin-top:12px;font-size:16px;color:" + c + ";font-weight:700;'>"
        "\u7d99\u7d9a\u306e\u7406\u7531\u304c\u5909\u308f\u308b\u3068\u6b62\u307e\u3089\u306a\u304f\u306a\u308b</div>"
        "</div>"
        "</body></html>"
    )
    return html

def card_10():
    """CTA：チェックリスト+CTAボックス"""
    c = ACCENT_COLORS[9]
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".check-item{position:absolute;left:60px;display:flex;align-items:flex-start;gap:18px;}"
        ".check-box{width:36px;height:36px;border-radius:8px;border:2px solid;"
        "display:flex;align-items:center;justify-content:center;"
        "font-size:20px;font-weight:900;flex-shrink:0;}"
        ".check-text{font-size:22px;font-weight:700;color:#e5e7eb;line-height:1.5;}"
        ".cta-box{position:absolute;left:60px;border-radius:16px;"
        "padding:22px 32px;}"
        "</style></head><body>"
        + card_common_header("10/10", CARD_TAGS[9], c) +
        "<div class='title' style='color:" + c + ";'>\u4eca\u591c\u3084\u308b\u3053\u30681\u3064\u3060\u3051</div>"
        "<div class='check-item' style='top:115px;'>"
        "<div class='check-box' style='border-color:" + c + ";color:" + c + ";'>\u2713</div>"
        "<div class='check-text'>\u6765\u9031\u5206\u306e\u904b\u52d5\u00b44\u6897\u3092\u30ab\u30ec\u30f3\u30c0\u30fc\u306b\u5165\u308c\u308b</div>"
        "</div>"
        "<div class='check-item' style='top:185px;'>"
        "<div class='check-box' style='border-color:#38bdf8;color:#38bdf8;'>\u2713</div>"
        "<div class='check-text'>\u660e\u671d\u304b\u3089\u8840\u5727\u3092\u8a08\u6e2c\u3059\u308b\uff08\u8d77\u5e8a\u5f8c30\u5206\uff09</div>"
        "</div>"
        "<div class='check-item' style='top:255px;'>"
        "<div class='check-box' style='border-color:#4ade80;color:#4ade80;'>\u2713</div>"
        "<div class='check-text'>23:30\u5c31\u5bdd\u30eb\u30fc\u30eb\u3092\u4eca\u591c\u304b\u3089\u8a2d\u5b9a\u3059\u308b</div>"
        "</div>"
        "<div class='cta-box' style='background:#2d1b00;border:2px solid " + c + ";top:340px;width:1160px;'>"
        "<div style='font-size:20px;color:#9ca3af;margin-bottom:8px;'>"
        "\u4f53\u91cd\u8a08\u3060\u3051\u3067\u81ea\u5206\u3092\u8a55\u4fa1\u3059\u308b\u306e\u3092\u3084\u3081\u305f\u65e5\u304c\u3001\u672c\u5f53\u306e\u5909\u5316\u306e\u59cb\u307e\u308a</div>"
        "<div style='font-size:22px;color:" + c + ";font-weight:900;'>"
        "\u8840\u7ba1\u3092\u5b88\u308b\u6e1b\u91cf\u306e\u5168\u30b9\u30c6\u30c3\u30d7\u306fnote\u3067\u25bc<br>"
        "<span style='font-size:18px;color:#9ca3af;'>https://note.com/mash_anti_metabo</span></div>"
        "</div>"
        "<div style='position:absolute;bottom:52px;left:60px;right:60px;text-align:center;"
        "font-size:16px;color:#374151;'>"
        "#\u4e0d\u8001\u9577\u5bff #\u5065\u5eb7 #\u30c0\u30a4\u30a8\u30c3\u30c8 #\u6700\u65b0\u7814\u7a76 #Longevity</div>"
        "</body></html>"
    )
    return html

CARD_FUNCS = [card_01, card_02, card_03, card_04, card_05,
              card_06, card_07, card_08, card_09, card_10]

def save_tweets():
    out = ARTICLE_DIR / "\u7b2c41\u56de_X\u6295\u7a3710\u672c.md"
    lines = ["# \u7b2c41\u56de X\u6295\u7a3f\u30b9\u30ec\u30c3\u30c9\uff0810\u672c\uff09\n\n"]
    for i, tweet in enumerate(TWEETS):
        tag = CARD_TAGS[i]
        fname = "x_post_" + str(i+1).zfill(2) + ".png"
        lines.append(
            "## \u6295\u7a3f" + str(i+1) + "/10\uff5c" + tag + "\n\n```\n" + tweet.strip() +
            "\n```\n\n![\u30ab\u30fc\u30c9" + str(i+1) + "](images/x_posts/" + fname + ")\n\n---\n\n"
        )
    out.write_text("".join(lines), encoding="utf-8")

if __name__ == "__main__":
    print("第41回 X投稿カード画像（図解版）生成開始...\n")
    for i, func in enumerate(CARD_FUNCS):
        html = func()
        fname = "x_post_" + str(i+1).zfill(2) + ".png"
        render(html, fname)
        print("✅ " + fname + "  [" + CARD_TAGS[i] + "]")
    save_tweets()
    print("\n全10枚完了。保存先: " + str(OUTPUT_DIR))
