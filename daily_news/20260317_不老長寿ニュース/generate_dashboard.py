#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""不老長寿ニュース ダッシュボード生成スクリプト"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR
FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

# ── ニュースデータ ──
DATE = "2026.03.17"
NEWS = [
    {
        "category": "\U0001f957 \u98df\u4e8b",
        "cat_color": "#22c55e",
        "title": "\u8d85\u52a0\u5de5\u98df\u54c1\u3067\u5fc3\u81d3\u767a\u4f5c\u30fb\u8133\u5352\u4e2d\u30ea\u30b9\u30af47%\u5897",
        "summary": "63,000\u4eba\u4ee5\u4e0a\u306e\u5927\u898f\u6a21\u7814\u7a76\u3067\u5224\u660e\u3002\u690d\u7269\u6027\u98df\u54c1\u3067\u3082\u8d85\u52a0\u5de5\u306a\u3089\u5fc3\u8840\u7ba1\u4fdd\u8b77\u52b9\u679c\u304c\u6d88\u5931\u3002",
        "source": "ScienceDaily 2026\u5e742\u6708",
        "stars": "\u2605\u2605\u2605",
    },
    {
        "category": "\u2696\ufe0f \u30c0\u30a4\u30a8\u30c3\u30c8",
        "cat_color": "#ef4444",
        "title": "\u65ad\u98df\u3001\u30ab\u30ed\u30ea\u30fc\u540c\u3058\u306a\u3089\u4ee3\u8b1d\u52b9\u679c\u306a\u3057",
        "summary": "\u30c9\u30a4\u30c4\u306e\u6700\u65b0\u7814\u7a76\uff1a16:8\u65ad\u98df\u3067\u3082\u30ab\u30ed\u30ea\u30fc\u304c\u540c\u3058\u306a\u3089\u8840\u7cd6\u5024\u3082\u30a4\u30f3\u30b9\u30ea\u30f3\u3082\u5909\u308f\u3089\u306a\u3044\u3002",
        "source": "\u30c9\u30a4\u30c4\u4eba\u9593\u6804\u990a\u7814\u7a76\u6240 2025\u5e7412\u6708",
        "stars": "\u2605\u2605\u2605",
    },
    {
        "category": "\u2696\ufe0f \u30c0\u30a4\u30a8\u30c3\u30c8",
        "cat_color": "#ef4444",
        "title": "\u6642\u9593\u5236\u9650\u98df\u304cHbA1c\u3068\u7a7a\u8179\u6642\u8840\u7cd6\u3092\u6539\u5584",
        "summary": "RCT 8\u672c\u306e\u30e1\u30bf\u5206\u6790\u3067\u78ba\u8a8d\u3002\u30e1\u30bf\u30dc\uff0b\u524d\u7cd6\u5c3f\u75c5\u60a3\u8005\u3067\u5fc3\u8840\u7ba1\u6307\u6a19\u3082\u6539\u5584\u3002",
        "source": "IJMS 2025 / UC San Diego TIMET\u8a66\u9a13",
        "stars": "\u2605\u2605\u2606",
    },
    {
        "category": "\U0001f957 \u98df\u4e8b",
        "cat_color": "#22c55e",
        "title": "\u5730\u4e2d\u6d77\u98df\u304c\u8178\u5185\u7d30\u83cc\u3092\u6539\u5584\u3057\u708e\u75c7\u3092\u4f4e\u6e1b",
        "summary": "\u5584\u7389\u83cc\u304c\u5897\u52a0\u3057\u80a5\u6e80\u95a2\u9023\u75c5\u539f\u83cc\u304c\u6e1b\u5c11\u3002\u8107\u8cea\u7570\u5e38\u75c7\u30fb\u708e\u75c7\u30e1\u30c7\u30a3\u30a8\u30fc\u30bf\u30fc\u3082\u4f4e\u4e0b\u3002",
        "source": "Frontiers in Nutrition / BMC Medical Genomics 2024-2025",
        "stars": "\u2605\u2605\u2606",
    },
    {
        "category": "\U0001f48a \u30b5\u30d7\u30ea",
        "cat_color": "#f59e0b",
        "title": "\u30aa\u30e1\u30ac3\u306e\u6297\u708e\u75c7\u52b9\u679c\u306b\u65b0\u305f\u306a\u7591\u554f",
        "summary": "\u30d6\u30ea\u30b9\u30c8\u30eb\u5927\u5b66\uff1a\u30aa\u30e1\u30ac3\u304c\u4e00\u90e8\u306e\u708e\u75c7\u30de\u30fc\u30ab\u30fc\u3092\u4e0a\u6607\u3055\u305b\u308b\u53ef\u80fd\u6027\u3002\u901a\u8aac\u306b\u7591\u554f\u7b26\u3002",
        "source": "\u30d6\u30ea\u30b9\u30c8\u30eb\u5927\u5b66 2025\u5e746\u6708",
        "stars": "\u2605\u2605\u2606",
    },
]

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:900px;overflow:hidden;background:#f0f0f0;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
)

def build_html():
    header = (
        "<div style='width:100%;height:80px;background:linear-gradient(135deg,#22c55e,#16a34a);"
        "display:flex;align-items:center;justify-content:space-between;padding:0 40px;'>"
        "<div style='font-size:28px;font-weight:900;color:#fff;'>不老長寿ニュース｜" + DATE + "</div>"
        "<div style='font-size:16px;color:rgba(255,255,255,.8);'>Longevity Navigator × マーシー</div>"
        "</div>"
    )

    cards = ""
    for i, n in enumerate(NEWS):
        if i < 4:
            w = "580px"
            left = str(20 + (i % 2) * 620) + "px"
            top = str(100 + (i // 2) * 195) + "px"
        else:
            w = "1240px"
            left = "20px"
            top = "490px"

        cards += (
            "<div style='position:absolute;left:" + left + ";top:" + top + ";width:" + w + ";"
            "height:175px;background:#fff;border-radius:12px;padding:20px 24px;"
            "box-shadow:0 2px 8px rgba(0,0,0,.06);overflow:hidden;'>"
            "<div style='display:inline-block;background:" + n["cat_color"] + ";color:#fff;"
            "font-size:13px;font-weight:700;padding:3px 12px;border-radius:12px;'>" + n["category"] + "</div>"
            "<div style='position:absolute;top:20px;right:24px;font-size:14px;color:#f59e0b;'>" + n["stars"] + "</div>"
            "<div style='font-size:22px;font-weight:800;color:#1a1a1a;margin-top:10px;line-height:1.3;'>" + n["title"] + "</div>"
            "<div style='font-size:15px;color:#6b7280;margin-top:6px;line-height:1.5;'>" + n["summary"] + "</div>"
            "<div style='position:absolute;bottom:12px;right:24px;font-size:12px;color:#9ca3af;'>" + n["source"] + "</div>"
            "</div>"
        )

    footer = (
        "<div style='position:absolute;bottom:0;width:100%;height:50px;background:#fff;"
        "border-top:1px solid #e5e7eb;display:flex;align-items:center;justify-content:space-between;padding:0 40px;'>"
        "<div style='font-size:14px;font-weight:700;color:#22c55e;'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div style='font-size:13px;color:#9ca3af;'>毎朝更新・世界最先端の健康研究をお届け</div>"
        "</div>"
    )

    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        + header + cards + footer
        + "</body></html>"
    )

if __name__ == "__main__":
    print("不老長寿ニュース ダッシュボード生成開始...\n")
    html = build_html()
    tmp = ARTICLE_DIR / "_tmp_dashboard.html"
    out = OUTPUT_DIR / "dashboard_20260317.png"
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto("file:///" + str(tmp).replace("\\", "/"))
        page.wait_for_timeout(800)
        page.screenshot(path=str(out), full_page=False)
        browser.close()
    tmp.unlink(missing_ok=True)
    print("✅ ダッシュボード生成完了: " + out.name)
