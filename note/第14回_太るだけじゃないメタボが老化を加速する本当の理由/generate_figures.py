#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 図解生成スクリプト（HTML/CSS + Playwright）"""
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
    "body{width:1280px;height:720px;overflow:hidden;font-family:'NJ','Meiryo',sans-serif;position:relative;}"
)

def render(html, fname):
    tmp = ARTICLE_DIR / "_tmp_fig.html"
    out = OUTPUT_DIR / fname
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.goto("file:///" + str(tmp).replace("\\", "/"))
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(out), full_page=False)
        b.close()
    tmp.unlink(missing_ok=True)
    print("OK: " + fname)


def fig1():
    """図解①：内臓脂肪と慢性炎症ループ（円形フロー）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "body{background:#0d1b2a;}</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;'>"
        "<div style='font-size:14px;font-weight:700;color:#FF6D00;letter-spacing:2px;'>FIGURE 01</div>"
        "<div style='font-size:32px;font-weight:900;color:#fff;margin-top:4px;'>内臓脂肪 → 慢性炎症ループ</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>Inflammaging（インフラメイジング）の正体</div></div>"
        # 上：内臓脂肪
        "<div style='position:absolute;top:140px;left:420px;width:440px;'>"
        "<div style='background:#1e3a5f;border:2px solid #ef4444;border-radius:16px;padding:20px;text-align:center;'>"
        "<div style='font-size:24px;font-weight:800;color:#ef4444;'>内臓脂肪（火元）</div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>TNF-α / IL-6 / CRP を24時間分泌</div></div></div>"
        # 矢印→右
        "<div style='position:absolute;top:225px;left:880px;font-size:32px;color:#ef4444;'>&#x2193;</div>"
        # 右：炎症物質が全身へ
        "<div style='position:absolute;top:250px;right:56px;width:360px;'>"
        "<div style='background:#1e3a5f;border:2px solid #FF6D00;border-radius:16px;padding:20px;text-align:center;'>"
        "<div style='font-size:22px;font-weight:800;color:#FF6D00;'>炎症物質が全身を巡る</div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>血管・臓器にダメージ蓄積</div></div></div>"
        # 矢印↓
        "<div style='position:absolute;top:360px;right:200px;font-size:32px;color:#FF6D00;'>&#x2193;</div>"
        # 下：4つのダメージ
        "<div style='position:absolute;top:390px;left:56px;right:56px;display:flex;gap:16px;'>"
        "<div style='flex:1;background:#0d2035;border-radius:12px;padding:16px;text-align:center;border-top:3px solid #ef4444;'>"
        "<div style='font-size:16px;font-weight:700;color:#ef4444;'>心臓病</div>"
        "<div style='font-size:13px;color:#9ca3af;margin-top:4px;'>動脈硬化</div></div>"
        "<div style='flex:1;background:#0d2035;border-radius:12px;padding:16px;text-align:center;border-top:3px solid #FF6D00;'>"
        "<div style='font-size:16px;font-weight:700;color:#FF6D00;'>糖尿病</div>"
        "<div style='font-size:13px;color:#9ca3af;margin-top:4px;'>インスリン抵抗性</div></div>"
        "<div style='flex:1;background:#0d2035;border-radius:12px;padding:16px;text-align:center;border-top:3px solid #38bdf8;'>"
        "<div style='font-size:16px;font-weight:700;color:#38bdf8;'>認知症</div>"
        "<div style='font-size:13px;color:#9ca3af;margin-top:4px;'>脳の炎症</div></div>"
        "<div style='flex:1;background:#0d2035;border-radius:12px;padding:16px;text-align:center;border-top:3px solid #8b5cf6;'>"
        "<div style='font-size:16px;font-weight:700;color:#8b5cf6;'>老化加速</div>"
        "<div style='font-size:13px;color:#9ca3af;margin-top:4px;'>テロメア短縮</div></div></div>"
        # 左：悪循環矢印
        "<div style='position:absolute;top:250px;left:56px;width:360px;'>"
        "<div style='background:#1e3a5f;border:2px solid #ef4444;border-radius:16px;padding:20px;text-align:center;'>"
        "<div style='font-size:22px;font-weight:800;color:#ef4444;'>さらに脂肪が増える</div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>代謝低下 → 太りやすい体に</div></div></div>"
        "<div style='position:absolute;top:225px;left:380px;font-size:32px;color:#ef4444;'>&#x2191;</div>"
        # 下部：解決策バー
        "<div style='position:absolute;bottom:36px;left:56px;right:56px;'>"
        "<div style='background:linear-gradient(90deg,rgba(74,222,128,.15),rgba(74,222,128,.05));border:2px solid #4ade80;"
        "border-radius:16px;padding:16px 32px;text-align:center;'>"
        "<span style='font-size:20px;font-weight:800;color:#4ade80;'>解決策：内臓脂肪を減らす → 炎症が鎮まる → 老化が遅くなる</span></div></div>"
        "</body></html>")
    render(html, "図解①_内臓脂肪と慢性炎症ループ.png")


def fig2():
    """図解②：メタボ治療と老化の関係（横3列カード）"""
    cards = [
        ("STEP 1", "内臓脂肪を減らす", "炎症の火元を断つ", "腹囲85cm以上が目安", "#ef4444"),
        ("STEP 2", "慢性炎症が下がる", "CRP・IL-6が低下", "体の修復が進み始める", "#FF6D00"),
        ("STEP 3", "老化が遅くなる", "4大リスクが下がる", "メタボ治療=老化治療", "#4ade80"),
    ]
    cards_html = ""
    for i, (step, title, sub1, sub2, color) in enumerate(cards):
        left = 56 + i * 400
        cards_html += (
            "<div style='position:absolute;top:170px;left:" + str(left) + "px;width:360px;height:340px;"
            "background:#1e3a5f;border-radius:16px;padding:28px;border-top:4px solid " + color + ";'>"
            "<div style='font-size:14px;font-weight:700;color:" + color + ";letter-spacing:2px;'>" + step + "</div>"
            "<div style='font-size:28px;font-weight:900;color:#fff;margin-top:16px;line-height:1.3;'>" + title + "</div>"
            "<div style='width:40px;height:3px;background:" + color + ";margin:20px 0;'></div>"
            "<div style='font-size:18px;color:#e2e8f0;'>" + sub1 + "</div>"
            "<div style='font-size:16px;color:#9ca3af;margin-top:8px;'>" + sub2 + "</div></div>")
        if i < 2:
            cards_html += (
                "<div style='position:absolute;top:320px;left:" + str(left + 370) + "px;"
                "font-size:28px;font-weight:900;color:#9ca3af;'>→</div>")
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "body{background:#0d1b2a;}</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;'>"
        "<div style='font-size:14px;font-weight:700;color:#FF6D00;letter-spacing:2px;'>FIGURE 02</div>"
        "<div style='font-size:32px;font-weight:900;color:#fff;margin-top:4px;'>メタボを治す ＝ 老化を遅らせる</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>内臓脂肪→慢性炎症→老化の因果関係</div></div>"
        + cards_html +
        "<div style='position:absolute;bottom:36px;right:56px;font-size:14px;color:#4a5568;'>"
        "Franceschi et al. 2018, Nature Reviews Endocrinology</div></body></html>")
    render(html, "図解②_メタボ治療と老化の関係.png")


def fig3():
    """図解③：CANTOS試験の結果（データ可視化）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "body{background:#0d1b2a;}</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;'>"
        "<div style='font-size:14px;font-weight:700;color:#FF6D00;letter-spacing:2px;'>FIGURE 03</div>"
        "<div style='font-size:32px;font-weight:900;color:#fff;margin-top:4px;'>CANTOS試験：炎症を下げるだけで心臓病が減った</div></div>"
        # メインデータ
        "<div style='position:absolute;top:140px;left:56px;width:560px;height:420px;"
        "background:#0d2035;border-radius:16px;padding:32px;'>"
        "<div style='font-size:16px;font-weight:700;color:#38bdf8;letter-spacing:2px;'>STUDY DATA</div>"
        "<div style='font-size:22px;font-weight:700;color:#fff;margin-top:12px;'>対象：10,061人（心臓発作歴あり）</div>"
        "<div style='font-size:22px;font-weight:700;color:#fff;margin-top:8px;'>期間：3.7年（中央値）</div>"
        "<div style='margin-top:24px;'>"
        # バーグラフ
        "<div style='margin-bottom:16px;'>"
        "<div style='font-size:14px;color:#9ca3af;margin-bottom:6px;'>プラセボ群（炎症そのまま）</div>"
        "<div style='background:#1e3a5f;border-radius:8px;height:48px;position:relative;'>"
        "<div style='background:#ef4444;height:100%;width:100%;border-radius:8px;'></div>"
        "<div style='position:absolute;right:12px;top:12px;font-size:18px;font-weight:800;color:#fff;'>100%</div></div></div>"
        "<div style='margin-bottom:16px;'>"
        "<div style='font-size:14px;color:#9ca3af;margin-bottom:6px;'>カナキヌマブ群（炎症を抑制）</div>"
        "<div style='background:#1e3a5f;border-radius:8px;height:48px;position:relative;'>"
        "<div style='background:#4ade80;height:100%;width:85%;border-radius:8px;'></div>"
        "<div style='position:absolute;right:12px;top:12px;font-size:18px;font-weight:800;color:#fff;'>85%</div></div></div>"
        "</div>"
        "<div style='background:#162d4a;border-radius:10px;padding:14px 20px;margin-top:12px;'>"
        "<span style='font-size:18px;font-weight:800;color:#4ade80;'>心臓発作リスク 15%低下</span>"
        "<span style='font-size:14px;color:#9ca3af;margin-left:12px;'>コレステロール値は変化なし</span></div></div>"
        # 右パネル：意義
        "<div style='position:absolute;top:140px;right:56px;width:560px;height:420px;"
        "background:#0d2035;border-radius:16px;padding:32px;'>"
        "<div style='font-size:16px;font-weight:700;color:#FF6D00;letter-spacing:2px;'>SIGNIFICANCE</div>"
        "<div style='font-size:24px;font-weight:900;color:#fff;margin-top:12px;line-height:1.4;'>"
        "炎症そのものが<br>心臓病の原因だと<br>初めて臨床で証明</div>"
        "<div style='width:60px;height:3px;background:#FF6D00;margin:24px 0;'></div>"
        "<div style='font-size:16px;color:#e2e8f0;line-height:1.7;'>"
        "従来の常識：<br>"
        "<span style='color:#ef4444;'>「コレステロールを下げれば防げる」</span><br><br>"
        "新たな視点：<br>"
        "<span style='color:#4ade80;'>「炎症を下げなければ不十分」</span></div>"
        "<div style='position:absolute;bottom:20px;right:20px;font-size:13px;color:#4a5568;'>"
        "Ridker et al. 2017, NEJM</div></div>"
        # 下部
        "<div style='position:absolute;bottom:36px;left:56px;'>"
        "<div style='font-size:14px;color:#4a5568;'>CANTOS: Canakinumab Anti-inflammatory Thrombosis Outcomes Study</div></div>"
        "</body></html>")
    render(html, "図解③_CANTOS試験の結果.png")


def fig4():
    """図解④：抗炎症4つの戦略早見表（テーブル型）"""
    rows = [
        ("内臓脂肪を減らす", "腹囲85cm以上は要注意", "体重5%減でCRP低下", "#ef4444"),
        ("オメガ3脂肪酸", "サバ・イワシ・サーモン・くるみ", "週2-3回の青魚", "#38bdf8"),
        ("超加工食品を減らす", "菓子パン・スナック・清涼飲料水", "1日1つ減らすだけ", "#FF6D00"),
        ("ゾーン2運動", "話せるペースで歩く", "週2-3回 10分から", "#4ade80"),
    ]
    rows_html = ""
    for name, detail, action, color in rows:
        rows_html += (
            "<tr>"
            "<td style='padding:18px 20px;font-size:20px;font-weight:700;color:" + color + ";"
            "border-bottom:1px solid #1e3a5f;'>" + name + "</td>"
            "<td style='padding:18px 20px;font-size:16px;color:#e2e8f0;border-bottom:1px solid #1e3a5f;'>" + detail + "</td>"
            "<td style='padding:18px 20px;font-size:16px;color:#e2e8f0;border-bottom:1px solid #1e3a5f;'>" + action + "</td>"
            "</tr>")
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "body{background:#0d1b2a;}"
        "table{width:calc(100% - 112px);position:absolute;top:140px;left:56px;border-collapse:collapse;}"
        "th{padding:14px 20px;font-size:14px;font-weight:700;color:#FF6D00;text-align:left;"
        "border-bottom:2px solid #FF6D00;letter-spacing:1px;background:#0d2035;}"
        "</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;'>"
        "<div style='font-size:14px;font-weight:700;color:#FF6D00;letter-spacing:2px;'>FIGURE 04</div>"
        "<div style='font-size:32px;font-weight:900;color:#fff;margin-top:4px;'>抗炎症 4つの戦略</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>薬でもサプリでもない。生活習慣が最強の抗炎症法。</div></div>"
        "<table><tr><th>戦略</th><th>具体的な内容</th><th>始め方</th></tr>"
        + rows_html + "</table>"
        "<div style='position:absolute;bottom:60px;left:56px;right:56px;display:flex;gap:20px;'>"
        "<div style='flex:1;background:#162d4a;border-radius:12px;padding:16px 20px;border-left:4px solid #4ade80;'>"
        "<div style='font-size:16px;font-weight:700;color:#4ade80;'>まず1つだけ</div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>超加工食品を1つ減らすことから</div></div>"
        "<div style='flex:1;background:#162d4a;border-radius:12px;padding:16px 20px;border-left:4px solid #FF6D00;'>"
        "<div style='font-size:16px;font-weight:700;color:#FF6D00;'>核心</div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>メタボを治す = 老化を遅らせる</div></div></div>"
        "</body></html>")
    render(html, "図解④_抗炎症4つの戦略早見表.png")


def fig5():
    """図解⑤：崩れた日の復帰フロー"""
    steps = [
        ("1", "食べすぎた日", "「飲み会でつい...」「疲れてコンビニ弁当...」", "#ef4444"),
        ("2", "翌朝の1食を軽くする", "ゆで卵＋サラダだけでOK。全リセット不要", "#FF6D00"),
        ("3", "ループに戻る", "8勝6敗で十分。6割で炎症は下がる", "#4ade80"),
    ]
    steps_html = ""
    for i, (num, title, sub, color) in enumerate(steps):
        top = 150 + i * 185
        steps_html += (
            "<div style='position:absolute;top:" + str(top) + "px;left:56px;right:56px;"
            "display:flex;align-items:center;gap:24px;'>"
            "<div style='width:72px;height:72px;border-radius:50%;background:" + color + ";"
            "display:flex;align-items:center;justify-content:center;flex-shrink:0;"
            "font-size:32px;font-weight:900;color:#fff;'>" + num + "</div>"
            "<div style='flex:1;background:#1e3a5f;border-radius:14px;padding:22px 28px;"
            "border-left:4px solid " + color + ";'>"
            "<div style='font-size:24px;font-weight:800;color:#fff;'>" + title + "</div>"
            "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>" + sub + "</div></div></div>")
        if i < 2:
            steps_html += (
                "<div style='position:absolute;top:" + str(top + 100) + "px;left:83px;"
                "width:2px;height:70px;background:#1e3a5f;'></div>")
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "body{background:#0d1b2a;}</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;'>"
        "<div style='font-size:14px;font-weight:700;color:#FF6D00;letter-spacing:2px;'>FIGURE 05</div>"
        "<div style='font-size:32px;font-weight:900;color:#fff;margin-top:4px;'>崩れた日の復帰フロー</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>8勝6敗でOK。翌朝の1食で戻る。</div></div>"
        + steps_html +
        "<div style='position:absolute;bottom:36px;right:56px;font-size:14px;color:#4a5568;'>"
        "第 慢性炎症×抗炎症生活</div></body></html>")
    render(html, "図解⑤_崩れた日の復帰フロー.png")


if __name__ == "__main__":
    print("第 図解5枚 生成開始...\n")
    fig1(); fig2(); fig3(); fig4(); fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))

