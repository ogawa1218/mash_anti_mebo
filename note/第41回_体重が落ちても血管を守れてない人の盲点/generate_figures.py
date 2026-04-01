#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第41回 図解5枚 生成スクリプト（HTML/CSS + Playwright 強化版）"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images"
OUTPUT_DIR.mkdir(exist_ok=True)
FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;background:#0d1b2a;}"
)

def render(html, fname):
    tmp = ARTICLE_DIR / "_tmp_fig.html"
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
    print("OK: " + fname)

def fig1():
    """図解①：夜更かしと食欲のループ（円形フロー）"""
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".title{position:absolute;top:30px;left:0;right:0;text-align:center;"
        "font-size:36px;font-weight:900;color:#fff;letter-spacing:-1px;}"
        ".sub{position:absolute;top:82px;left:0;right:0;text-align:center;"
        "font-size:20px;color:#9ca3af;}"
        ".node{position:absolute;border-radius:40px;"
        "display:flex;align-items:center;justify-content:center;"
        "font-size:18px;font-weight:700;text-align:center;line-height:1.4;color:#fff;}"
        ".center-box{position:absolute;width:260px;height:80px;border:3px solid #38bdf8;"
        "border-radius:12px;display:flex;align-items:center;justify-content:center;"
        "font-size:20px;font-weight:900;color:#38bdf8;text-align:center;line-height:1.4;}"
        ".footer{position:absolute;bottom:14px;left:0;right:0;text-align:center;"
        "font-size:13px;color:#374151;}"
        "</style></head><body>"
        "<div class='title'>\u591c\u66f4\u304b\u3057\u304c\u80a5\u6e80\u3092\u52a0\u901f\u3055\u305b\u308b\u30eb\u30fc\u30d7</div>"
        "<div class='sub'>\u610f\u5fd7\u529b\u3067\u65ad\u3061\u5207\u308b\u3088\u308a\u300c\u5c31\u5bdd\u6642\u523b\u306e\u8a2d\u8a08\u300d\u3067\u8131\u51fa\u3059\u308b</div>"
        # Node 1: 夜更かし (top center)
        "<div class='node' style='background:#ef4444;width:190px;height:72px;top:148px;left:545px;'>"
        "\u591c\u66f4\u304b\u3057<br>23\u6642\u4ee5\u964d</div>"
        # Arrow 1→2
        "<div style='position:absolute;top:220px;left:758px;font-size:26px;color:#6b7280;"
        "transform:rotate(40deg);'>\u2193</div>"
        # Node 2: 食欲増加 (right)
        "<div class='node' style='background:#f97316;width:190px;height:72px;top:290px;left:920px;'>"
        "\u98df\u6b32\u5897\u52a0<br>\u30b0\u30ec\u30ea\u30f3\u2191</div>"
        # Arrow 2→3
        "<div style='position:absolute;top:400px;left:980px;font-size:26px;color:#6b7280;'>\u2193</div>"
        # Node 3: 夜食 (bottom right)
        "<div class='node' style='background:#eab308;width:190px;height:72px;top:460px;left:860px;'>"
        "\u591c\u98df\u30fb\u9593\u98df<br>\u30ab\u30ed\u30ea\u30fc\u5897</div>"
        # Arrow 3→4
        "<div style='position:absolute;top:502px;left:720px;font-size:26px;color:#6b7280;'>\u2190</div>"
        # Node 4: 翌日疲れ (bottom center)
        "<div class='node' style='background:#dc2626;width:190px;height:72px;top:460px;left:445px;'>"
        "\u7fcc\u65e5\u75b2\u308c<br>\u4f53\u91cd\u5897\u52a0</div>"
        # Arrow 4→5
        "<div style='position:absolute;top:502px;left:320px;font-size:26px;color:#6b7280;'>\u2190</div>"
        # Node 5: 運動中断 (bottom left)
        "<div class='node' style='background:#b91c1c;width:190px;height:72px;top:460px;left:100px;'>"
        "\u904b\u52d5\u4e2d\u65ad<br>\u4ee3\u8b1d\u4f4e\u4e0b</div>"
        # Arrow 5→1
        "<div style='position:absolute;top:340px;left:148px;font-size:26px;color:#6b7280;"
        "transform:rotate(-50deg);'>\u2191</div>"
        # Center box
        "<div class='center-box' style='top:324px;left:510px;'>"
        "\u3053\u306e\u30eb\u30fc\u30d7\u3092<br>\u8a2d\u8a08\u3067\u65ad\u3061\u5207\u308b</div>"
        "<div class='footer'>\u7b2c41\u56de\uff5cLongevity Navigator \u00d7 \u30de\u30fc\u30b7\u30fc</div>"
        "</body></html>"
    )
    render(html, "\u56f3\u89e3\u2460_\u591c\u66f4\u304b\u3057\u3068\u98df\u6b32\u306e\u30eb\u30fc\u30d7.png")

def fig2():
    """図解②：4軸評価（カードグリッド）"""
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".title{position:absolute;top:28px;left:0;right:0;text-align:center;"
        "font-size:38px;font-weight:900;color:#fff;}"
        ".sub{position:absolute;top:82px;left:0;right:0;text-align:center;"
        "font-size:20px;color:#9ca3af;}"
        ".card{position:absolute;width:262px;height:210px;border-radius:16px;"
        "display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;}"
        ".card-num{font-size:46px;font-weight:900;}"
        ".card-title{font-size:26px;font-weight:900;color:#fff;}"
        ".card-sub{font-size:16px;color:rgba(255,255,255,.65);text-align:center;line-height:1.4;}"
        ".arr{position:absolute;top:195px;font-size:36px;color:#374151;font-weight:900;}"
        ".bottom{position:absolute;bottom:28px;left:80px;right:80px;"
        "background:#1e2a3a;border:2px solid #38bdf8;border-radius:12px;"
        "padding:18px;text-align:center;font-size:20px;color:#fff;font-weight:700;}"
        ".footer{position:absolute;bottom:8px;left:0;right:0;text-align:center;"
        "font-size:13px;color:#374151;}"
        "</style></head><body>"
        "<div class='title'>\u4f53\u91cd\u8a081\u3064\u304b\u30894\u8ef8\u8a55\u4fa1\u3078</div>"
        "<div class='sub'>\u505c\u6ede\u3057\u3066\u3082\u300c\u3069\u3053\u304b\u304c\u524d\u9032\u3057\u3066\u3044\u308b\u300d\u304c\u7d99\u7d9a\u306e\u9375</div>"
        # Card 1: 体重
        "<div class='card' style='background:#1e3a5f;top:148px;left:40px;'>"
        "<div class='card-num' style='color:#38bdf8;'>\u2460</div>"
        "<div class='card-title'>\u4f53\u3000\u91cd</div>"
        "<div class='card-sub'>\u6bce\u671d\u540c\u3058\u6642\u9593\u5e2f<br>\u8d77\u5e8a\u5f8c</div>"
        "</div>"
        "<div class='arr' style='left:316px;'>\u2192</div>"
        # Card 2: 血圧
        "<div class='card' style='background:#1a3a2a;top:148px;left:370px;'>"
        "<div class='card-num' style='color:#4ade80;'>\u2461</div>"
        "<div class='card-title'>\u8840\u3000\u5727</div>"
        "<div class='card-sub'>\u8d77\u5e8a\u5f8c30\u5206\u4ee5\u5185<br>\u5bb6\u5ead\u7528\u8840\u5727\u8a08</div>"
        "</div>"
        "<div class='arr' style='left:646px;'>\u2192</div>"
        # Card 3: 腹囲
        "<div class='card' style='background:#2d1b00;top:148px;left:700px;'>"
        "<div class='card-num' style='color:#FF6D00;'>\u2462</div>"
        "<div class='card-title'>\u8179\u3000\u56f2</div>"
        "<div class='card-sub'>\u90311\u56de\u5540\u7e4a\u308a<br>\u540c\u3058\u6642\u9593\u5e2f\u306b</div>"
        "</div>"
        "<div class='arr' style='left:976px;'>\u2192</div>"
        # Card 4: 活動量
        "<div class='card' style='background:#1a1a3e;top:148px;left:1030px;'>"
        "<div class='card-num' style='color:#a78bfa;'>\u2463</div>"
        "<div class='card-title'>\u6d3b\u52d5\u91cf</div>"
        "<div class='card-sub'>\u6b69\u6570 or \u904b\u52d5\u6642\u9593<br>\u6bce\u65e5\u8a18\u9332</div>"
        "</div>"
        # Bottom message
        "<div class='bottom'>"
        "\u4f53\u91cd\u304c\u505c\u6ede\u3057\u3066\u3082\u3001\u8840\u5727\u30fb\u8179\u56f2\u30fb\u6d3b\u52d5\u91cf\u306e\u3069\u308c\u304b\u304c\u6539\u5584\u3057\u3066\u3044\u308c\u3070"
        "<span style='color:#4ade80;font-size:24px;'>\u300c\u305d\u308c\u306f\u524d\u9032\u300d</span></div>"
        "<div class='footer'>\u7b2c41\u56de\uff5cLongevity Navigator \u00d7 \u30de\u30fc\u30b7\u30fc</div>"
        "</body></html>"
    )
    render(html, "\u56f3\u89e3\u2461_4\u8ef8\u8a55\u4fa1\u3068\u6e2c\u5b9a\u65b9\u6cd5.png")

def fig3():
    """図解③：NG vs OK比較（体重のみ vs 複合KPI）"""
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".title{position:absolute;top:28px;left:0;right:0;text-align:center;"
        "font-size:38px;font-weight:900;color:#fff;}"
        ".panel{position:absolute;width:560px;height:460px;border-radius:16px;padding:28px;}"
        ".panel-title{font-size:30px;font-weight:900;margin-bottom:20px;}"
        ".item{font-size:19px;margin-bottom:14px;display:flex;align-items:flex-start;gap:10px;"
        "color:#d1d5db;line-height:1.4;}"
        ".badge{font-size:20px;font-weight:900;min-width:28px;}"
        ".result{border-radius:8px;padding:14px;margin-top:12px;"
        "font-size:18px;font-weight:700;text-align:center;}"
        ".footer{position:absolute;bottom:14px;left:0;right:0;text-align:center;"
        "font-size:13px;color:#374151;}"
        "</style></head><body>"
        "<div class='title'>\u4f53\u91cd\u306e\u307f vs 4\u8ef8\u8a55\u4fa1\uff1a\u7d99\u7d9a\u7387\u306e\u9055\u3044</div>"
        # NG panel
        "<div class='panel' style='background:#1f0a0a;border:2px solid #ef4444;top:90px;left:36px;'>"
        "<div class='panel-title' style='color:#ef4444;'>\u2717 \u4f53\u91cd\u306e\u307f\u8ffd\u8de1</div>"
        "<div class='item'><span class='badge' style='color:#ef4444;'>\u2717</span>"
        "\u505c\u6ede\uff1d\u5931\u6557\u3068\u5224\u65ad\u3055\u308c\u3084\u3059\u3044</div>"
        "<div class='item'><span class='badge' style='color:#ef4444;'>\u2717</span>"
        "\u6570\u5024\u306b\u30e2\u30c1\u30d9\u30fc\u30b7\u30e7\u30f3\u3092\u5de6\u53f3\u3055\u308c\u308b</div>"
        "<div class='item'><span class='badge' style='color:#ef4444;'>\u2717</span>"
        "\u8840\u7ba1\u30ea\u30b9\u30af\u6539\u5584\u3092\u898b\u9003\u3059</div>"
        "<div class='item'><span class='badge' style='color:#ef4444;'>\u2717</span>"
        "\u30ea\u30d0\u30a6\u30f3\u30c9\u5f8c\u306e\u81ea\u5df1\u5acc\u60aa\u304c\u5927\u304d\u3044</div>"
        "<div class='result' style='background:#2d1010;color:#ef4444;'>"
        "3\u56de\u306b1\u56de\u306f\u632b\u6298\u3057\u3066\u30ea\u30d0\u30a6\u30f3\u30c9</div>"
        "</div>"
        # OK panel
        "<div class='panel' style='background:#0a1f0a;border:2px solid #4ade80;top:90px;left:684px;'>"
        "<div class='panel-title' style='color:#4ade80;'>\u2713 4\u8ef8\u8a55\u4fa1\u3067\u8ffd\u8de1</div>"
        "<div class='item'><span class='badge' style='color:#4ade80;'>\u2713</span>"
        "\u505c\u6ede\u3067\u3082\u300c\u8840\u5727\u304c\u4e0b\u304c\u3063\u305f\u300d\u3067\u524d\u9032\u78ba\u8a8d</div>"
        "<div class='item'><span class='badge' style='color:#4ade80;'>\u2713</span>"
        "\u3069\u3053\u304b\u306e\u8ef8\u304c\u6539\u5584\u3059\u308c\u3070\u7d9a\u3051\u3089\u308c\u308b</div>"
        "<div class='item'><span class='badge' style='color:#4ade80;'>\u2713</span>"
        "\u8840\u7ba1\u30ea\u30b9\u30af\u306e\u5909\u5316\u3092\u5b9f\u611f\u3067\u304d\u308b</div>"
        "<div class='item'><span class='badge' style='color:#4ade80;'>\u2713</span>"
        "\u5d29\u308c\u305f\u5f8c\u3082\u623b\u308a\u3084\u3059\u3044\u8a2d\u8a08\u306b\u306a\u308b</div>"
        "<div class='result' style='background:#0a2d0a;color:#4ade80;'>"
        "\u300c\u524d\u9032\u306e\u8a3c\u62e0\u300d\u304c\u7d99\u7d9a\u306e\u71c3\u6599\u306b\u306a\u308b</div>"
        "</div>"
        "<div class='footer'>\u7b2c41\u56de\uff5cLongevity Navigator \u00d7 \u30de\u30fc\u30b7\u30fc</div>"
        "</body></html>"
    )
    render(html, "\u56f3\u89e3\u2462_\u4f53\u91cd\u306e\u307f KPI vs \u8907\u5408KPI.png")

def fig4():
    """図解④：5ステップ早見表（テーブル型）"""
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".title{position:absolute;top:24px;left:0;right:0;text-align:center;"
        "font-size:36px;font-weight:900;color:#fff;}"
        "table{position:absolute;top:88px;left:40px;width:1200px;"
        "border-collapse:collapse;}"
        "th{background:#1e3a5f;color:#38bdf8;font-size:18px;font-weight:700;"
        "padding:12px 18px;text-align:left;border-bottom:2px solid #38bdf8;}"
        "td{font-size:17px;color:#e5e7eb;padding:13px 18px;"
        "border-bottom:1px solid #1e293b;line-height:1.5;}"
        "tr:nth-child(odd) td{background:#0f1f30;}"
        "tr:nth-child(even) td{background:#0d1b2a;}"
        ".badge{display:inline-block;background:#FF6D00;color:#fff;"
        "font-size:14px;font-weight:900;padding:2px 10px;border-radius:8px;margin-right:8px;}"
        ".footer{position:absolute;bottom:14px;left:0;right:0;text-align:center;"
        "font-size:13px;color:#374151;}"
        "</style></head><body>"
        "<div class='title'>\u4eca\u65e5\u304b\u3089\u59cb\u3081\u308b5\u30b9\u30c6\u30c3\u30d7\u8a2d\u8a08</div>"
        "<table>"
        "<tr><th>\u30b9\u30c6\u30c3\u30d7</th><th>\u5185\u5bb9</th>"
        "<th>\u30bf\u30a4\u30df\u30f3\u30b0</th><th>\u6240\u8981\u6642\u9593</th></tr>"
        "<tr><td><span class='badge'>1</span>\u5c31\u5bdd\u6642\u523b\u306e\u4e0b\u9650</td>"
        "<td>23:30\u3092\u8d85\u3048\u305f\u3089\u30b9\u30af\u30ed\u30fc\u30eb\u505c\u6b62\u30fb\u5c31\u5bdd</td>"
        "<td>\u6bce\u665a</td><td>\u6c7a\u3081\u308b\u3060\u3051</td></tr>"
        "<tr><td><span class='badge'>2</span>\u591c\u306e\u98df\u884c\u52d5\u3092\u56fa\u5b9a</td>"
        "<td>21\u6642\u4ee5\u964d\u306f\u30ab\u30ed\u30ea\u30fc\u98f2\u6599\u306a\u3057\u3002\u7518\u3044\u3082\u306e\u306f\u7fd4\u671d\u3078</td>"
        "<td>21\u6642\u4ee5\u964d</td><td>0\u5206\uff08\u30eb\u30fc\u30eb\u5316\uff09</td></tr>"
        "<tr><td><span class='badge'>3</span>\u904b\u52d5\u3092\u4e88\u7d04\u5316</td>"
        "<td>\u90314\u67a0\u00d720\u301e30\u5206\u3092\u30ab\u30ec\u30f3\u30c0\u30fc\u56fa\u5b9a\u5165\u529b</td>"
        "<td>\u4eca\u65e5\u4e2d\u306b\u8a2d\u5b9a</td><td>3\u5206\uff08\u30ab\u30ec\u30f3\u30c0\u30fc\u64cd\u4f5c\uff09</td></tr>"
        "<tr><td><span class='badge'>4</span>\u7b4b\u30c8\u30ec\u6700\u5c0f\u69cb\u6210</td>"
        "<td>\u30b9\u30af\u30ef\u30c3\u30c815\u56de\uff0b\u30d7\u30c3\u30b7\u30e5\u30a2\u30c3\u30d710\u56de\u306e2\u7a2e\u76ee\u3060\u3051</td>"
        "<td>\u904b\u52d5\u67a0\u306e\u4e2d</td><td>10\u5206</td></tr>"
        "<tr><td><span class='badge'>5</span>\u90311\u30ec\u30d3\u30e5\u30fc</td>"
        "<td>4\u8ef8\uff08\u4f53\u91cd\u30fb\u8840\u5727\u30fb\u8179\u56f2\u30fb\u6d3b\u52d5\u91cf\uff09\u306e\u6539\u5584\u3092\u78ba\u8a8d</td>"
        "<td>\u9031\u672b</td><td>5\u5206</td></tr>"
        "</table>"
        "<div class='footer'>\u7b2c41\u56de\uff5cLongevity Navigator \u00d7 \u30de\u30fc\u30b7\u30fc</div>"
        "</body></html>"
    )
    render(html, "\u56f3\u89e3\u2463_5\u30b9\u30c6\u30c3\u30d7\u65e9\u898b\u8868.png")

def fig5():
    """図解⑤：崩れた週の復帰フロー（縦型3ステップ）"""
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        ".title{position:absolute;top:24px;left:0;right:0;text-align:center;"
        "font-size:36px;font-weight:900;color:#fff;}"
        ".sub{position:absolute;top:76px;left:0;right:0;text-align:center;"
        "font-size:19px;color:#9ca3af;}"
        ".step{position:absolute;width:820px;height:118px;border-radius:16px;"
        "left:230px;display:flex;align-items:center;padding:0 28px;gap:20px;}"
        ".step-num{font-size:46px;font-weight:900;min-width:56px;text-align:center;}"
        ".step-title{font-size:24px;font-weight:900;margin-bottom:6px;}"
        ".step-desc{font-size:16px;color:rgba(255,255,255,.78);line-height:1.45;}"
        ".arr{position:absolute;left:620px;font-size:32px;color:#6b7280;}"
        ".bottom-badge{position:absolute;bottom:22px;left:230px;width:820px;"
        "background:#1e293b;border-radius:8px;padding:12px;text-align:center;"
        "font-size:19px;color:#4ade80;font-weight:700;}"
        ".footer{position:absolute;bottom:4px;left:0;right:0;text-align:center;"
        "font-size:13px;color:#374151;}"
        "</style></head><body>"
        "<div class='title'>\u5d29\u308c\u305f\u9031\u306e\u300c\u6700\u4f4e\u30e9\u30a4\u30f3\u300d\u5fa9\u5e30\u30d5\u30ed\u30fc</div>"
        "<div class='sub'>\u5b8c\u74a7\u306b\u623b\u3055\u306a\u304f\u3066\u3044\u3044\u3002\u6700\u4f4e\u30e9\u30a4\u30f3\u306b\u623b\u3059\u3060\u3051\u3067OK</div>"
        # Step 1
        "<div class='step' style='background:#2d1010;border:2px solid #ef4444;top:118px;'>"
        "<div class='step-num' style='color:#ef4444;'>1</div>"
        "<div style='flex:1;'>"
        "<div class='step-title' style='color:#ef4444;'>\u5d29\u308c\u305f\uff01\u5168\u505c\u6b62\u30e2\u30fc\u30c9</div>"
        "<div class='step-desc'>\u98f2\u307f\u4f1a\u30fb\u6b8b\u696d\u30fb\u5bb6\u65cf\u306e\u4f53\u8abf\u4e0d\u826f\u3067\u5168\u90e8\u5d29\u308c\u305f\u72b6\u614b<br>"
        "\u2192 \u81ea\u5df1\u5acc\u60aa\u306b\u5165\u3089\u306a\u3044\u3002\u4ed5\u7d44\u307f\u306e\u554f\u984c\u3001\u610f\u5fd7\u306e\u554f\u984c\u3058\u3083\u306a\u3044</div>"
        "</div>"
        "</div>"
        "<div class='arr' style='top:248px;'>\u2193</div>"
        # Step 2
        "<div class='step' style='background:#2d1f00;border:2px solid #f59e0b;top:294px;'>"
        "<div class='step-num' style='color:#f59e0b;'>2</div>"
        "<div style='flex:1;'>"
        "<div class='step-title' style='color:#f59e0b;'>\u6700\u4f4e\u30e9\u30a4\u30f3\u3092\u78ba\u8a8d\u3059\u308b</div>"
        "<div class='step-desc'>\u300c\u7fd4\u671d10\u5206\u306e\u30a6\u30a9\u30fc\u30ad\u30f3\u30b0\u3060\u3051\u300d\u300c\u671d\u98df\u3092\u305f\u3093\u3071\u304f\u8caa\u30d5\u30a1\u30fc\u30b9\u30c8\u306b\u623b\u3059\u300d<br>"
        "\u2192 1\u3064\u3060\u3051\u9078\u3093\u3067\u5b9f\u884c\u3002\u5168\u90e8\u623b\u305d\u3046\u3068\u3057\u306a\u3044</div>"
        "</div>"
        "</div>"
        "<div class='arr' style='top:424px;'>\u2193</div>"
        # Step 3
        "<div class='step' style='background:#0a1f0a;border:2px solid #4ade80;top:470px;'>"
        "<div class='step-num' style='color:#4ade80;'>3</div>"
        "<div style='flex:1;'>"
        "<div class='step-title' style='color:#4ade80;'>7\u5206\u3067\u30ea\u30b9\u30bf\u30fc\u30c8 \u2192 \u7fd4\u9031\u3078</div>"
        "<div class='step-desc'>20\u5206\u304c\u7121\u7406\u306a\u30897\u5206\u30027\u5206\u304c\u7121\u7406\u306a\u3089\u30b9\u30af\u30ef\u30c3\u30c83\u56de\u3060\u3051<br>"
        "\u2192\u300c\u6b62\u3081\u306a\u304b\u3063\u305f\u300d\u3068\u3044\u3046\u4e8b\u5b9f\u304c\u7fd4\u9031\u306e\u571f\u53f0\u306b\u306a\u308b</div>"
        "</div>"
        "</div>"
        "<div class='bottom-badge'>8\u52dd6\u6557\u3067OK\uff5c\u5d29\u308c\u305f\u5f8c\u306b\u623b\u308c\u308b\u304b\u3001\u304c\u672c\u5f53\u306e\u5b9f\u529b</div>"
        "<div class='footer'>\u7b2c41\u56de\uff5cLongevity Navigator \u00d7 \u30de\u30fc\u30b7\u30fc</div>"
        "</body></html>"
    )
    render(html, "\u56f3\u89e3\u2464_\u5d29\u308c\u305f\u9031\u306e\u5fa9\u5e30\u30d5\u30ed\u30fc.png")

if __name__ == "__main__":
    print("第41回 図解5枚 生成開始...\n")
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))
