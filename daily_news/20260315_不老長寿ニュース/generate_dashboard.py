#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
不老長寿ニュース ダッシュボード生成スクリプト
2026年03月15日版
HTML/CSS + Playwright（1280×900px）
デザイン：ライトグレー背景 + グリーン/オレンジ健康系UI
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR
FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

DATE = "2026年03月15日"
DAY_OF_WEEK = "土曜日"

NEWS = [
    {
        "cat": "🧬 不老長寿",
        "cat_color": "#8b5cf6",
        "title": "ビタミンD3で生物学的老化が約3年分巻き戻る",
        "source": "Am J Clin Nutr, 2025年5月",
        "summary": "ビタミンD3の毎日補給がDNAメチル化時計で約3年分の若返り効果。安価で手軽に始められる。",
        "stars": "★★★",
    },
    {
        "cat": "⚖️ ダイエット",
        "cat_color": "#ef4444",
        "title": "次世代GLP-1薬レタトルチドで体重-28.7%",
        "source": "Eli Lilly Phase III, 2025-2026",
        "summary": "三重受容体作動薬レタトルチド12mgで68週間で-28.7%。現行セマグルチドの約16%を大幅に上回る。",
        "stars": "★★☆",
    },
    {
        "cat": "💊 サプリ",
        "cat_color": "#f59e0b",
        "title": "NMNとNRがNAD+を約2倍に増加（ヒト試験）",
        "source": "NAD+ Precursor Comparison Trial, 2026",
        "summary": "14日間のNMN/NR補給で血中NAD+が約2倍に。腸内細菌を介した短鎖脂肪酸増加も確認。",
        "stars": "★★★",
    },
    {
        "cat": "🧬 不老長寿",
        "cat_color": "#8b5cf6",
        "title": "細胞の部分的リプログラミングで老化遺伝子を逆転",
        "source": "Partial Cellular Reprogramming Study, 2025",
        "summary": "老齢マウスに7ヶ月間の周期的処置で腎臓・肝臓の老化関連遺伝子が有意に低下。",
        "stars": "★★☆",
    },
    {
        "cat": "⚖️ ダイエット",
        "cat_color": "#ef4444",
        "title": "中年期の減量が脳の炎症を増加させるリスク",
        "source": "ScienceDaily / Hypothalamus Study, 2025",
        "summary": "中年マウスで減量後に視床下部の炎症増加。代謝は改善。ゆるやかな減量が重要。",
        "stars": "★★★",
    },
]

PODCAST_TOPIC = "「急に痩せるな」が科学的に正しかった話"
PODCAST_SUMMARY = "中年期の急激ダイエットは脳に炎症リスク。月1kgのゆるやか減量が正解。"

def build_news_cards():
    cards = ""
    for i, n in enumerate(NEWS):
        stars_html = ""
        for ch in n["stars"]:
            if ch == "★":
                stars_html += "<span style='color:#FF6D00;'>★</span>"
            elif ch == "☆":
                stars_html += "<span style='color:#ccc;'>☆</span>"

        cards += (
            "<div style='background:#ffffff;border-radius:12px;padding:20px 24px;"
            "box-shadow:0 1px 4px rgba(0,0,0,0.06);'>"
            "  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>"
            "    <span style='display:inline-block;padding:3px 10px;border-radius:20px;"
            f"     background:{n['cat_color']}22;color:{n['cat_color']};font-size:13px;font-weight:700;'>"
            f"     {n['cat']}</span>"
            f"   <span style='font-size:16px;letter-spacing:2px;'>{stars_html}</span>"
            "  </div>"
            f" <div style='font-size:17px;font-weight:800;color:#1a1a1a;margin-bottom:6px;line-height:1.4;'>{n['title']}</div>"
            f" <div style='font-size:12px;color:#888;margin-bottom:8px;'>{n['source']}</div>"
            f" <div style='font-size:13.5px;color:#444;line-height:1.6;'>{n['summary']}</div>"
            "</div>"
        )
    return cards

def build_html():
    cards = build_news_cards()

    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
        "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
        "body{width:1280px;height:900px;overflow:hidden;background:#f0f0f0;"
        "font-family:'NJ','Meiryo',sans-serif;position:relative;padding:36px 40px;}"
        "</style></head><body>"

        # ── ヘッダー ──
        "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;'>"
        "  <div>"
        "    <div style='font-size:28px;font-weight:900;color:#1a1a1a;'>"
        "      🌿 不老長寿ニュース</div>"
        f"   <div style='font-size:14px;color:#666;margin-top:4px;'>{DATE}（{DAY_OF_WEEK}）｜世界最先端の研究を毎朝5本ピックアップ</div>"
        "  </div>"
        "  <div style='display:flex;gap:8px;'>"
        "    <span style='padding:4px 12px;border-radius:20px;background:#22c55e22;color:#22c55e;font-size:12px;font-weight:700;'>健康</span>"
        "    <span style='padding:4px 12px;border-radius:20px;background:#FF6D0022;color:#FF6D00;font-size:12px;font-weight:700;'>ダイエット</span>"
        "    <span style='padding:4px 12px;border-radius:20px;background:#8b5cf622;color:#8b5cf6;font-size:12px;font-weight:700;'>不老長寿</span>"
        "  </div>"
        "</div>"

        # ── ニュースカード5枚（グリッド） ──
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px;'>"
        + cards +
        "</div>"

        # ── Podcastメモ ──
        "<div style='background:linear-gradient(135deg,#FF6D00 0%,#ff9a44 100%);border-radius:12px;"
        "padding:18px 24px;color:#fff;display:flex;align-items:center;gap:20px;'>"
        "  <div style='font-size:36px;'>🎙️</div>"
        "  <div>"
        f"   <div style='font-size:15px;font-weight:800;margin-bottom:4px;'>今日のPodcastネタ：{PODCAST_TOPIC}</div>"
        f"   <div style='font-size:13px;opacity:0.9;line-height:1.5;'>{PODCAST_SUMMARY}</div>"
        "  </div>"
        "</div>"

        # ── フッター ──
        "<div style='position:absolute;bottom:16px;left:40px;right:40px;display:flex;"
        "justify-content:space-between;align-items:center;'>"
        "  <div style='font-size:12px;color:#999;'>収集者：Claude Code × マーシー</div>"
        "  <div style='font-size:12px;color:#999;'>Longevity Navigator Daily</div>"
        "</div>"

        "</body></html>"
    )


if __name__ == "__main__":
    print("不老長寿ニュース ダッシュボード生成開始...\n")

    html = build_html()
    tmp = ARTICLE_DIR / "_tmp_dashboard.html"
    out = OUTPUT_DIR / "20260315_dashboard.png"

    tmp.write_text(html, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto("file:///" + str(tmp).replace("\\", "/"))
        page.wait_for_timeout(900)
        page.screenshot(path=str(out), full_page=False)
        browser.close()

    tmp.unlink(missing_ok=True)

    print("✅ 20260315_dashboard.png")
    print(f"保存先: {out}")
