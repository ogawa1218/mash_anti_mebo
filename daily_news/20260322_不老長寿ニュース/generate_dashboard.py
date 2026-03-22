#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""不老長寿ニュース ダッシュボード生成スクリプト｜2026-03-22"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR
FONT_PATH = "/home/user/mash_anti_mebo/note/scripts/NotoSansJP-VF.ttf"

DATE = "2026.03.22"
NEWS = [
    {
        "category": "🧬 不老長寿",
        "cat_color": "#8b5cf6",
        "title": "老化は「生物システムの連携崩壊」",
        "summary": "老化を単一の欠陥ではなく複数システムの協調喪失として捉える新パラダイムが2026年に主流化。単一サプリより組み合わせ介入が有望。",
        "source": "EurekAlert! / Frontiers, 2026",
        "stars": "★★★",
    },
    {
        "category": "🧬 不老長寿",
        "cat_color": "#8b5cf6",
        "title": "ラパマイシン、ヒト試験で筋肉量維持を確認",
        "summary": "老化抑制薬ラパマイシンの低用量間欠投与が免疫強化と筋肉量維持に効果。動物実験から人間への翻訳が進む。",
        "source": "査読論文・2025〜2026臨床試験",
        "stars": "★★★",
    },
    {
        "category": "⚖️ ダイエット",
        "cat_color": "#ef4444",
        "title": "断食IFはカロリー制限と同等——コクラン結論",
        "summary": "22RCT・2,000人を分析したコクランレビューが「断食ダイエットは普通の食事制限と統計的に差がない」と結論。続かなかったのは意志の問題ではない。",
        "source": "Cochrane / Rutgers大学, 2026年2月",
        "stars": "★★★",
    },
    {
        "category": "⚖️ ダイエット",
        "cat_color": "#ef4444",
        "title": "腸内細菌Turicibacterが肥満を抑制",
        "summary": "Cell Metabolismに掲載。Turicibacter菌が産生する脂質が有害セラミドを低下させ体重増加を抑制。肥満者はこの菌が少ない傾向。",
        "source": "University of Utah / Cell Metabolism, 2026年1月",
        "stars": "★★★",
    },
    {
        "category": "🥗 食事",
        "cat_color": "#22c55e",
        "title": "腸内細菌が多様な人ほどリバウンドしない",
        "summary": "腸内多様性が改善した参加者ほど減量成果が大きく、終了後も体重が戻りにくい。短鎖脂肪酸がGLP-1を活性化するメカニズムが関与。",
        "source": "University of Colorado Anschutz, 2026",
        "stars": "★★☆",
    },
]

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('file://" + FONT_PATH + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:900px;overflow:hidden;background:#f0f4f8;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
)

def build_html():
    header = (
        "<div style='width:100%;height:80px;background:linear-gradient(135deg,#22c55e,#16a34a);"
        "display:flex;align-items:center;justify-content:space-between;padding:0 40px;'>"
        "<div style='font-size:26px;font-weight:900;color:#fff;letter-spacing:1px;'>🌿 不老長寿ニュース｜" + DATE + "</div>"
        "<div style='font-size:14px;color:rgba(255,255,255,.85);'>Longevity Navigator × マーシー</div>"
        "</div>"
    )

    cards = ""
    for i, n in enumerate(NEWS):
        if i < 4:
            w = "610px"
            left = str(20 + (i % 2) * 640) + "px"
            top = str(100 + (i // 2) * 200) + "px"
            h = "175px"
        else:
            w = "1240px"
            left = "20px"
            top = "505px"
            h = "165px"

        cards += (
            "<div style='position:absolute;left:" + left + ";top:" + top + ";width:" + w + ";"
            "height:" + h + ";background:#fff;border-radius:14px;padding:18px 22px;"
            "box-shadow:0 2px 12px rgba(0,0,0,.07);overflow:hidden;'>"
            "<div style='display:inline-block;background:" + n["cat_color"] + ";color:#fff;"
            "font-size:12px;font-weight:700;padding:3px 12px;border-radius:20px;'>" + n["category"] + "</div>"
            "<div style='position:absolute;top:18px;right:20px;font-size:16px;color:#f59e0b;letter-spacing:2px;'>" + n["stars"] + "</div>"
            "<div style='font-size:19px;font-weight:800;color:#1a1a1a;margin-top:9px;line-height:1.35;'>" + n["title"] + "</div>"
            "<div style='font-size:13px;color:#6b7280;margin-top:7px;line-height:1.6;'>" + n["summary"] + "</div>"
            "<div style='position:absolute;bottom:11px;right:20px;font-size:11px;color:#9ca3af;'>" + n["source"] + "</div>"
            "</div>"
        )

    footer = (
        "<div style='position:absolute;bottom:0;width:100%;height:52px;background:#fff;"
        "border-top:2px solid #f0f4f8;display:flex;align-items:center;justify-content:space-between;padding:0 40px;'>"
        "<div style='font-size:14px;font-weight:800;color:#22c55e;'>マーシー｜100kg→68kg｜Sub3達成</div>"
        "<div style='font-size:12px;color:#9ca3af;'>毎朝更新・世界最先端の健康研究をお届け | note.com/longevity_navi</div>"
        "</div>"
    )

    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        + header + cards + footer
        + "</body></html>"
    )

if __name__ == "__main__":
    print("不老長寿ニュース ダッシュボード生成開始...")
    html = build_html()
    tmp = ARTICLE_DIR / "_tmp_dashboard.html"
    out = OUTPUT_DIR / "dashboard_20260322.png"
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto("file://" + str(tmp))
        page.wait_for_timeout(1000)
        page.screenshot(path=str(out), full_page=False)
        browser.close()
    tmp.unlink(missing_ok=True)
    print("✅ 完了: " + str(out))
