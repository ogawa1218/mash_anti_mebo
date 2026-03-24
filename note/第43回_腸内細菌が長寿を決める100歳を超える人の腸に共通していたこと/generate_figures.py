#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第43回 図解PNG自動生成スクリプト
テーマ：腸内細菌と不老長寿（時間栄養学）
HTML/CSS + Playwright（Chromiumヘッドレス）版
サイズ: 1280×720px × 5枚
"""

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
    "body{width:1280px;height:720px;overflow:hidden;background:#0d1b2a;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
)


def render(html, fname):
    tmp = ARTICLE_DIR / "_tmp_fig.html"
    out = OUTPUT_DIR / fname
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(f"file:///{tmp.as_posix()}")
        page.wait_for_timeout(800)
        page.screenshot(path=str(out), full_page=False)
        browser.close()
    tmp.unlink(missing_ok=True)
    print(f"✅ {fname}")


def fig1():
    """腸活ループ問題フロー（問題の正体を可視化）"""
    steps = [
        ("食物繊維不足", "発酵食品を食べない", "#ef4444"),
        ("善玉菌が減る", "悪玉菌が優勢になる", "#FF6D00"),
        ("酪酸が作られない", "腸管バリアが低下", "#FF6D00"),
        ("慢性炎症が続く", "老化が加速する", "#ef4444"),
    ]
    steps_html = ""
    for i, (label, desc, color) in enumerate(steps):
        left = 40 + i * 305
        steps_html += (
            f"<div style='position:absolute;top:180px;left:{left}px;width:270px;"
            "background:#1e3a5f;border-radius:12px;padding:20px;text-align:center;'>"
            f"<div style='font-size:24px;font-weight:900;color:{color};line-height:1.3;'>{label}</div>"
            f"<div style='font-size:14px;color:#9ca3af;margin-top:8px;'>{desc}</div>"
            "</div>"
        )
        if i < 3:
            arrow_left = left + 272
            steps_html += (
                f"<div style='position:absolute;top:216px;left:{arrow_left}px;"
                "font-size:28px;color:#444;'>→</div>"
            )
    # 解決矢印
    steps_html += (
        "<div style='position:absolute;top:400px;left:56px;right:56px;"
        "background:#1a2a1a;border-radius:12px;padding:20px 32px;"
        "border:1px solid #4ade8040;display:flex;align-items:center;gap:24px;'>"
        "<div style='font-size:28px;font-weight:900;color:#4ade80;'>解決策</div>"
        "<div style='font-size:18px;color:#e2e8f0;'>"
        "水溶性食物繊維（大麦・海藻）＋発酵食品（納豆・味噌）を毎日摂る"
        "</div></div>"
    )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:40px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#ef4444;'>「腸活してるのに変わらない」の正体</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>ヨーグルトだけでは不十分。菌＋餌のセットが必要。</div></div>"
        + steps_html +
        "<div style='position:absolute;bottom:20px;left:56px;font-size:14px;color:#3a3a3a;'>"
        "マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>"
    )


def fig2():
    """腸活3ステップ横カードグリッド"""
    steps = [
        ("Step 1", "納豆＋玉ねぎ", "シンバイオティクス", "善玉菌＋その餌を同時投入", "#4ade80"),
        ("Step 2", "大麦2割混ぜ", "β-グルカン補給", "酪酸産生菌の餌を増やす", "#38bdf8"),
        ("Step 3", "食後15分歩く", "腸内多様性UP", "蠕動運動活発化＋フローラ多様化", "#FF6D00"),
    ]
    cards_html = ""
    for i, (num, title, tag, sub, color) in enumerate(steps):
        left = 56 + i * 395
        cards_html += (
            f"<div style='position:absolute;top:150px;left:{left}px;width:360px;height:360px;"
            "background:#1e3a5f;border-radius:16px;padding:32px;'>"
            f"<div style='font-size:18px;font-weight:700;color:{color};letter-spacing:2px;'>{num}</div>"
            f"<div style='font-size:30px;font-weight:900;color:#e2e8f0;margin-top:16px;'>{title}</div>"
            f"<div style='margin-top:16px;padding:8px 16px;background:{color}20;"
            f"border-radius:20px;display:inline-block;'>"
            f"<span style='font-size:16px;font-weight:700;color:{color};'>{tag}</span></div>"
            f"<div style='font-size:16px;color:#9ca3af;margin-top:16px;line-height:1.6;'>{sub}</div>"
            f"<div style='position:absolute;bottom:0;left:0;width:100%;height:4px;"
            f"background:{color};border-radius:0 0 16px 16px;'></div>"
            "</div>"
        )
    note_html = (
        "<div style='position:absolute;top:548px;left:56px;right:56px;"
        "background:#1a1a2a;border-radius:10px;padding:14px 24px;border:1px solid #38bdf840;'>"
        "<div style='font-size:18px;color:#38bdf8;'>"
        "💡 全部やらなくていい。今日は1つだけ選んでください。</div>"
        "</div>"
    )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:40px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>今夜から始める腸活3ステップ</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>意志力ゼロ。食事の仕組みを変えるだけ。</div></div>"
        + cards_html + note_html +
        "<div style='position:absolute;bottom:20px;left:56px;font-size:14px;color:#3a3a3a;'>"
        "マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>"
    )


def fig3():
    """NG腸活 vs OK腸活比較表"""
    ng_items = [
        "ヨーグルトだけ食べる",
        "2〜3日でやめてしまう",
        "味噌汁を沸騰させて溶く",
        "食物繊維をほとんど食べない",
        "運動なし・ストレス放置",
    ]
    ok_items = [
        "ヨーグルト＋バナナ・はちみつ",
        "2週間続けて初めて入口",
        "火を止めてから味噌を溶く",
        "大麦・海藻・きのこを毎日",
        "食後15分のウォーキング習慣",
    ]
    ng_html = ""
    ok_html = ""
    for i, item in enumerate(ng_items):
        top = 150 + i * 92
        ng_html += (
            f"<div style='position:absolute;top:{top}px;left:36px;right:16px;"
            "background:#2a1a1a;border-radius:8px;padding:14px 20px;"
            "border-left:4px solid #ef4444;'>"
            f"<div style='font-size:18px;color:#ef4444;'>✗ {item}</div>"
            "</div>"
        )
    for i, item in enumerate(ok_items):
        top = 150 + i * 92
        ok_html += (
            f"<div style='position:absolute;top:{top}px;left:16px;right:36px;"
            "background:#1a2a1a;border-radius:8px;padding:14px 20px;"
            "border-left:4px solid #4ade80;'>"
            f"<div style='font-size:18px;color:#4ade80;'>✓ {item}</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:40px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>NG腸活 vs OK腸活</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>「変わらない」理由はここにある。</div></div>"
        "<div style='position:absolute;top:110px;left:0;width:640px;height:100%;'>"
        "<div style='position:absolute;top:0;left:56px;font-size:22px;font-weight:700;color:#ef4444;'>❌ NG（変わらない）</div>"
        + ng_html + "</div>"
        "<div style='position:absolute;top:0;left:640px;width:2px;height:100%;background:#333;'></div>"
        "<div style='position:absolute;top:110px;left:640px;width:640px;height:100%;'>"
        "<div style='position:absolute;top:0;left:16px;font-size:22px;font-weight:700;color:#4ade80;'>✅ OK（変わる）</div>"
        + ok_html + "</div>"
        "<div style='position:absolute;bottom:20px;left:56px;font-size:14px;color:#3a3a3a;'>"
        "マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>"
    )


def fig4():
    """腸活食品早見表（食品×菌種対応）"""
    header_html = (
        "<div style='position:absolute;top:130px;left:56px;right:56px;"
        "display:grid;grid-template-columns:200px 1fr 1fr 1fr;gap:8px;'>"
        "<div style='font-size:16px;font-weight:700;color:#9ca3af;padding:12px;'>食品</div>"
        "<div style='font-size:16px;font-weight:700;color:#4ade80;padding:12px;'>プロ/プレ</div>"
        "<div style='font-size:16px;font-weight:700;color:#38bdf8;padding:12px;'>対象菌</div>"
        "<div style='font-size:16px;font-weight:700;color:#FF6D00;padding:12px;'>効果</div>"
        "</div>"
    )
    rows = [
        ("納豆", "プロバイオティクス", "ビフィズス菌・乳酸菌", "善玉菌を直接補給"),
        ("玉ねぎ", "プレバイオティクス", "ビフィズス菌", "オリゴ糖で善玉菌を育てる"),
        ("大麦", "プレバイオティクス", "酪酸産生菌", "β-グルカンで酪酸を増やす"),
        ("味噌・ぬか漬け", "プロバイオティクス", "乳酸菌・酵母菌", "腸内多様性を高める"),
        ("海藻・きのこ", "プレバイオティクス", "酪酸産生菌全般", "水溶性食物繊維を補給"),
    ]
    rows_html = ""
    for i, (food, type_, target, effect) in enumerate(rows):
        top = 188 + i * 96
        bg = "#1e3a5f" if i % 2 == 0 else "#162a4a"
        rows_html += (
            f"<div style='position:absolute;top:{top}px;left:56px;right:56px;"
            f"background:{bg};border-radius:8px;padding:16px;'>"
            "<div style='display:grid;grid-template-columns:200px 1fr 1fr 1fr;gap:8px;'>"
            f"<div style='font-size:20px;font-weight:700;color:#e2e8f0;'>{food}</div>"
            f"<div style='font-size:16px;color:#4ade80;'>{type_}</div>"
            f"<div style='font-size:16px;color:#38bdf8;'>{target}</div>"
            f"<div style='font-size:16px;color:#FF6D00;'>{effect}</div>"
            "</div></div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:40px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>腸活食品早見表</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>どの食品がどの菌に効くか、一目でわかる</div></div>"
        + header_html + rows_html +
        "<div style='position:absolute;bottom:20px;left:56px;font-size:14px;color:#3a3a3a;'>"
        "マーシー｜100kg→68kg｜Sub3　京丹後長寿コホート研究・東京工科大学2023</div>"
        "</body></html>"
    )


def fig5():
    """リカバリーフロー（崩れた日の戻り方）"""
    steps = [
        ("腸活できなかった", "#ef4444", "❌", "ついヨーグルトも忘れた"),
        ("自己嫌悪に0秒使う", "#9ca3af", "→", "腸活は完璧主義と相性が悪い"),
        ("翌朝、納豆を食べる", "#38bdf8", "✓", "たった1つのアクション"),
        ("その日の夜、大麦を炊く", "#4ade80", "✓", "リズムを取り戻す"),
        ("リセット完了", "#FF6D00", "✓", "8勝6敗でOK。それで十分"),
    ]
    steps_html = ""
    for i, (label, color, mark, sub) in enumerate(steps):
        top = 150 + i * 102
        steps_html += (
            f"<div style='position:absolute;top:{top}px;left:56px;right:56px;"
            "background:#1e3a5f;border-radius:10px;padding:16px 24px;"
            f"border-left:6px solid {color};display:flex;align-items:center;gap:20px;'>"
            f"<div style='font-size:32px;font-weight:900;color:{color};width:40px;'>{mark}</div>"
            "<div style='flex:1;'>"
            f"<div style='font-size:22px;font-weight:700;color:#e2e8f0;'>{label}</div>"
            f"<div style='font-size:15px;color:#9ca3af;margin-top:4px;'>{sub}</div>"
            "</div></div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:40px;left:56px;right:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#4ade80;'>崩れた日のリカバリーフロー</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>"
        "完璧主義を捨てる。翌朝の1つが全てをリセットする。</div>"
        "<div style='position:absolute;top:0;right:0;font-size:18px;font-weight:700;color:#4ade80;'>"
        "8勝6敗でOK</div>"
        "</div>"
        + steps_html +
        "<div style='position:absolute;bottom:20px;left:56px;font-size:14px;color:#3a3a3a;'>"
        "マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>"
    )


FIGURES = [
    ("fig_01_問題ループフロー.png",   fig1),
    ("fig_02_腸活3ステップカード.png", fig2),
    ("fig_03_NGvsOK比較.png",        fig3),
    ("fig_04_腸活食品早見表.png",     fig4),
    ("fig_05_リカバリーフロー.png",   fig5),
]


if __name__ == "__main__":
    print("第43回 図解生成開始 (HTML/CSS + Playwright)...\n")
    for fname, generator in FIGURES:
        render(generator(), fname)
    print(f"\n保存先: {OUTPUT_DIR}")
    print("生成完了: 5枚")
