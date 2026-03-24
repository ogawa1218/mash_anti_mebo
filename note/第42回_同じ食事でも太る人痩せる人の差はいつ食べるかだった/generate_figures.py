#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第42回 図解PNG自動生成スクリプト
テーマ：食べる時間と体の変化（時間栄養学）
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


def fig1():
    """体内時計と代謝フロー（24時間タイムライン）"""
    slots = [
        ("06:00", "#4ade80", "朝食", "インスリン感受性 最高", "エネルギーとして使われやすい"),
        ("12:00", "#38bdf8", "昼食", "代謝活発・燃焼モード", "最も太りにくい時間帯"),
        ("18:00", "#FF6D00", "夕食推奨", "代謝が落ち始める", "早めに食べ終えるのが理想"),
        ("22:00", "#ef4444", "BMAL1ピーク", "脂肪合成酵素が増加", "同じカロリーでも脂肪になりやすい"),
    ]
    slots_html = ""
    for i, (time, color, label, sub1, sub2) in enumerate(slots):
        left = 56 + i * 295
        slots_html += (
            f"<div style='position:absolute;top:160px;left:{left}px;width:265px;"
            "background:#1e3a5f;border-radius:12px;padding:20px;text-align:center;'>"
            f"<div style='font-size:36px;font-weight:900;color:{color};'>{time}</div>"
            f"<div style='font-size:20px;font-weight:700;color:#e2e8f0;margin-top:8px;'>{label}</div>"
            f"<div style='font-size:14px;color:#9ca3af;margin-top:8px;'>{sub1}</div>"
            f"<div style='font-size:14px;color:{color};margin-top:4px;'>{sub2}</div>"
            "</div>"
        )
        if i < 3:
            arrow_left = left + 268
            slots_html += (
                f"<div style='position:absolute;top:218px;left:{arrow_left}px;"
                "font-size:32px;color:#444;'>→</div>"
            )
    bmal_bar = (
        "<div style='position:absolute;top:440px;left:56px;right:56px;'>"
        "<div style='font-size:16px;color:#9ca3af;margin-bottom:8px;'>BMAL1活性（脂肪合成酵素）</div>"
        "<div style='width:100%;height:32px;background:#1e3a5f;border-radius:8px;overflow:hidden;position:relative;'>"
        "<div style='position:absolute;left:0;top:0;width:30%;height:100%;background:#4ade8040;'></div>"
        "<div style='position:absolute;left:30%;top:0;width:30%;height:100%;background:#38bdf840;'></div>"
        "<div style='position:absolute;left:60%;top:0;width:20%;height:100%;background:#FF6D0060;'></div>"
        "<div style='position:absolute;left:80%;top:0;width:20%;height:100%;background:#ef444490;'></div>"
        "<div style='position:absolute;left:0;top:0;right:0;bottom:0;display:flex;align-items:center;"
        "justify-content:space-around;font-size:13px;color:#e2e8f0;'>"
        "<span>低</span><span>低</span><span>中</span><span style='color:#ef4444;font-weight:900;'>高 ↑↑</span>"
        "</div></div>"
        "<div style='font-size:13px;color:#ef4444;margin-top:6px;text-align:right;'>22時以降は脂肪合成モード</div>"
        "</div>"
    )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:40px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>体内時計と食事タイミング</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>「いつ食べるか」で体への影響が変わる</div></div>"
        + slots_html + bmal_bar +
        "<div style='position:absolute;bottom:20px;left:56px;font-size:14px;color:#3a3a3a;'>"
        "マーシー｜100kg→68kg｜Sub3　Hatori et al. Cell Metabolism 2012</div>"
        "</body></html>"
    )


def fig2():
    """NGパターン vs OKパターン比較"""
    ng_items = [
        "22時〜23時に夕食",
        "BMAL1ピーク前後に食べる",
        "インスリン感受性が低い時間帯",
        "食後すぐ就寝",
        "内臓脂肪が蓄積しやすい",
    ]
    ok_items = [
        "19〜20時に夕食を終える",
        "BMAL1ピーク前に消化完了",
        "インスリン感受性が高い時間帯に食べる",
        "食後3〜4時間で就寝",
        "同じ食事でも太りにくい",
    ]
    ng_html = ""
    ok_html = ""
    for i, item in enumerate(ng_items):
        top = 160 + i * 88
        ng_html += (
            f"<div style='position:absolute;top:{top}px;left:40px;right:20px;"
            "background:#2a1a1a;border-radius:8px;padding:14px 20px;"
            "border-left:4px solid #ef4444;'>"
            f"<div style='font-size:18px;color:#ef4444;'>✗ {item}</div>"
            "</div>"
        )
    for i, item in enumerate(ok_items):
        top = 160 + i * 88
        ok_html += (
            f"<div style='position:absolute;top:{top}px;left:20px;right:40px;"
            "background:#1a2a1a;border-radius:8px;padding:14px 20px;"
            "border-left:4px solid #4ade80;'>"
            f"<div style='font-size:18px;color:#4ade80;'>✓ {item}</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:40px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>夜型食事 vs 時間設計食事</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>「いつ食べるか」を変えるだけで結果が変わる</div></div>"
        "<div style='position:absolute;top:110px;left:0;width:640px;height:100%;'>"
        "<div style='position:absolute;top:0;left:56px;font-size:22px;font-weight:700;color:#ef4444;'>❌ 夜型（変えない）</div>"
        + ng_html + "</div>"
        "<div style='position:absolute;top:0;left:0;width:2px;height:100%;background:#333;left:640px;'></div>"
        "<div style='position:absolute;top:110px;left:640px;width:640px;height:100%;'>"
        "<div style='position:absolute;top:0;left:20px;font-size:22px;font-weight:700;color:#4ade80;'>✅ 時間設計（変えた）</div>"
        + ok_html + "</div>"
        "<div style='position:absolute;bottom:20px;left:56px;font-size:14px;color:#3a3a3a;'>"
        "マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>"
    )


def fig3():
    """食べる時間3ルール カードグリッド"""
    rules = [
        ("ルール①", "就寝3〜4時間前に食べ終える", "23時就寝 → 19〜20時が理想", "#38bdf8"),
        ("ルール②", "朝食を起床後1時間以内に食べる", "体内時計リセット＋BMAL1正常化", "#4ade80"),
        ("ルール③", "22時以降は食べない", "BMAL1ピーク前に食事を終わらせる", "#FF6D00"),
    ]
    cards_html = ""
    for i, (num, title, sub, color) in enumerate(rules):
        left = 56 + i * 395
        cards_html += (
            f"<div style='position:absolute;top:160px;left:{left}px;width:360px;height:340px;"
            "background:#1e3a5f;border-radius:16px;padding:32px;'>"
            f"<div style='font-size:20px;font-weight:700;color:{color};letter-spacing:2px;'>{num}</div>"
            f"<div style='font-size:26px;font-weight:900;color:#e2e8f0;margin-top:16px;line-height:1.4;'>{title}</div>"
            f"<div style='font-size:16px;color:#9ca3af;margin-top:20px;line-height:1.6;'>{sub}</div>"
            f"<div style='position:absolute;bottom:0;left:0;width:100%;height:4px;background:{color};border-radius:0 0 16px 16px;'></div>"
            "</div>"
        )
    note = (
        "<div style='position:absolute;top:540px;left:56px;right:56px;"
        "background:#1a1a2a;border-radius:10px;padding:16px 24px;"
        "border:1px solid #38bdf840;'>"
        "<div style='font-size:18px;color:#38bdf8;'>💡 まず1つだけ始めるなら「ルール③　22時以降は食べない」</div>"
        "</div>"
    )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:40px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>食べる時間3ルール</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>意志力ゼロ。タイミングの設計だけで変わる。</div></div>"
        + cards_html + note +
        "<div style='position:absolute;bottom:20px;left:56px;font-size:14px;color:#3a3a3a;'>"
        "マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>"
    )


def fig4():
    """食事時間帯早見表（就寝時刻別）"""
    rows = [
        ("22時就寝", "18〜19時", "20時まで", "21時以降NG"),
        ("23時就寝", "19〜20時", "21時まで", "22時以降NG"),
        ("24時就寝", "20〜21時", "22時まで", "23時以降NG"),
        ("1時就寝",  "21〜22時", "23時まで", "24時以降NG"),
    ]
    header_html = (
        "<div style='position:absolute;top:130px;left:56px;right:56px;"
        "display:grid;grid-template-columns:220px 1fr 1fr 1fr;gap:8px;'>"
        "<div style='font-size:16px;font-weight:700;color:#9ca3af;padding:12px;'>就寝時刻</div>"
        "<div style='font-size:16px;font-weight:700;color:#4ade80;padding:12px;'>理想の夕食時間</div>"
        "<div style='font-size:16px;font-weight:700;color:#FF6D00;padding:12px;'>ギリギリライン</div>"
        "<div style='font-size:16px;font-weight:700;color:#ef4444;padding:12px;'>BMAL1ゾーン</div>"
        "</div>"
    )
    rows_html = ""
    for i, (bedtime, ideal, limit, danger) in enumerate(rows):
        top = 190 + i * 108
        bg = "#1e3a5f" if i % 2 == 0 else "#162a4a"
        rows_html += (
            f"<div style='position:absolute;top:{top}px;left:56px;right:56px;"
            f"background:{bg};border-radius:8px;padding:16px;'>"
            "display:grid;grid-template-columns:220px 1fr 1fr 1fr;gap:8px;'>"
            f"<div style='display:grid;grid-template-columns:220px 1fr 1fr 1fr;gap:8px;'>"
            f"<div style='font-size:22px;font-weight:700;color:#e2e8f0;'>{bedtime}</div>"
            f"<div style='font-size:22px;font-weight:700;color:#4ade80;'>{ideal}</div>"
            f"<div style='font-size:22px;font-weight:700;color:#FF6D00;'>{limit}</div>"
            f"<div style='font-size:22px;font-weight:700;color:#ef4444;'>{danger}</div>"
            "</div></div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:40px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>就寝時刻別・食事タイミング早見表</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>自分の生活リズムに合わせて逆算する</div></div>"
        + header_html + rows_html +
        "<div style='position:absolute;bottom:20px;left:56px;font-size:14px;color:#3a3a3a;'>"
        "マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>"
    )


def fig5():
    """リカバリーフロー（崩れた日の翌日対策）"""
    steps = [
        ("夜遅く食べてしまった", "#ef4444", "❌", "22時以降に食事"),
        ("自己嫌悪に0秒使う", "#9ca3af", "→", "気にしない"),
        ("翌朝の朝食を軽めに", "#38bdf8", "✓", "果物・ヨーグルト程度"),
        ("昼食でしっかり食べる", "#4ade80", "✓", "インスリン感受性が高い時間"),
        ("翌夜は早めに食べ終える", "#FF6D00", "✓", "リセット完了"),
    ]
    steps_html = ""
    for i, (label, color, mark, sub) in enumerate(steps):
        top = 160 + i * 102
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
    note = (
        "<div style='position:absolute;top:0;right:56px;font-size:18px;font-weight:700;color:#4ade80;'>"
        "8勝6敗でOK</div>"
    )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:40px;left:56px;right:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#4ade80;'>崩れた日のリカバリーフロー</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>遅くなっても翌日に補正できる。自己嫌悪は不要。</div>"
        + note + "</div>"
        + steps_html +
        "<div style='position:absolute;bottom:20px;left:56px;font-size:14px;color:#3a3a3a;'>"
        "マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>"
    )


FIGURES = [
    ("fig_01_体内時計と代謝フロー.png", fig1),
    ("fig_02_NGvsOK比較.png",           fig2),
    ("fig_03_3ルールカード.png",         fig3),
    ("fig_04_食事時間帯早見表.png",      fig4),
    ("fig_05_リカバリーフロー.png",      fig5),
]


if __name__ == "__main__":
    print("第42回 図解生成開始 (HTML/CSS + Playwright)...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for fname, generator in FIGURES:
            html = generator()
            tmp  = ARTICLE_DIR / "_tmp_fig.html"
            tmp.write_text(html, encoding="utf-8")
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(f"file:///{tmp.as_posix()}")
            page.wait_for_timeout(800)
            out = OUTPUT_DIR / fname
            page.screenshot(path=str(out), full_page=False)
            page.close()
            tmp.unlink(missing_ok=True)
            print(f"✅ {fname}")
        browser.close()

    print(f"\n保存先: {OUTPUT_DIR}")
    print("生成完了: 5枚")
