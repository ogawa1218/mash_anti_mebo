#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 図解生成スクリプト（HTML/CSS + Playwright 強化版）
5枚の図解を一括生成 | 1280×720px
テーマ：間食は意志で止めない。置き換え設計で勝つ方法
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
    "body{width:1280px;height:720px;overflow:hidden;font-family:'NJ','Meiryo',sans-serif;position:relative;}"
)

def render(html: str, fname: str):
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

# ─────────────────────────────────────────────
# 図解①  間食崩れの悪循環ループ（円形フロー）
# ─────────────────────────────────────────────
def fig1():
    steps = [
        ("①", "夕方の空腹が\n限界に達する",   "top:60px;left:50%;transform:translateX(-50%)"),
        ("②", "帰宅→即\n冷蔵庫を開ける",      "top:220px;right:80px"),
        ("③", "「1本だけ」が\n3本になる",       "bottom:130px;right:100px"),
        ("④", "空袋を隠して\n自己嫌悪",         "bottom:130px;left:100px"),
        ("⑤", "翌日も同じ\nパターンに",         "top:220px;left:80px"),
    ]
    cards = ""
    for num, label, pos in steps:
        label_html = label.replace("\n", "<br>")
        cards += (
            "<div style='position:absolute;" + pos + ";width:200px;background:#1e3a5f;"
            "border:2px solid #ef4444;border-radius:14px;padding:16px 14px;text-align:center;'>"
            "<div style='font-size:28px;font-weight:900;color:#ef4444;'>" + num + "</div>"
            "<div style='font-size:22px;font-weight:700;color:#fff;margin-top:6px;line-height:1.35;'>" + label_html + "</div>"
            "</div>"
        )
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#0d1b2a;}"
        + ".title{position:absolute;top:14px;left:50%;transform:translateX(-50%);"
        + "font-size:30px;font-weight:900;color:#fff;white-space:nowrap;}"
        + ".center{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);"
        + "text-align:center;}"
        + ".center-main{font-size:36px;font-weight:900;color:#ef4444;}"
        + ".center-sub{font-size:20px;color:#9ca3af;margin-top:6px;}"
        + ".caption{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);"
        + "font-size:20px;color:#9ca3af;white-space:nowrap;}"
        + "</style></head><body>"
        + "<div class='title'>なぜ毎晩、間食が止まらないのか</div>"
        + cards
        + "<div class='center'><div class='center-main'>毎晩の<br>ループ</div>"
        + "<div class='center-sub'>↻ 繰り返す</div></div>"
        + "<div class='caption'>意志の問題ではなく、判断疲労＋環境設計の問題だった</div>"
        + "</body></html>"
    )
    render(html, "図解①_間食崩れのループ.png")

# ─────────────────────────────────────────────
# 図解②  置き換え設計 3ステップ全体像（横3列カード）
# ─────────────────────────────────────────────
def fig2():
    cols = [
        ("#FF6D00", "STEP 1", "15時に先手の\n間食を固定", "夕方の空腹を\n先に消す", "#38bdf8", "ナッツ30g\n＋ブラックコーヒー"),
        ("#38bdf8", "STEP 2", "帰宅3分ルール", "夜の崩れを\n動線で断つ", "#38bdf8", "着替え→水\n→ミントガム"),
        ("#4ade80", "STEP 3", "22時以降\n選択肢ゼロ", "見えないものは\n食べない", "#4ade80", "味噌汁・ヨーグルト\n・炭酸水だけ"),
    ]
    cards = ""
    arrow_x = [465, 835]
    for i, (color, step, title, sub, sub_color, ex) in enumerate(cols):
        x = 40 + i * 408
        title_html = title.replace("\n", "<br>")
        sub_html = sub.replace("\n", "<br>")
        ex_html = ex.replace("\n", "<br>")
        cards += (
            "<div style='position:absolute;left:" + str(x) + "px;top:100px;width:370px;height:530px;"
            "background:#0d2035;border:3px solid " + color + ";border-radius:18px;padding:30px 24px;text-align:center;'>"
            "<div style='font-size:28px;font-weight:900;color:" + color + ";letter-spacing:1px;'>" + step + "</div>"
            "<div style='font-size:38px;font-weight:900;color:#fff;margin:14px 0;line-height:1.3;'>" + title_html + "</div>"
            "<div style='font-size:22px;color:" + sub_color + ";line-height:1.4;margin-bottom:18px;'>" + sub_html + "</div>"
            "<div style='background:#0a1520;border-radius:10px;padding:14px;font-size:19px;color:#9ca3af;line-height:1.5;'>" + ex_html + "</div>"
            "</div>"
        )
    for ax in arrow_x:
        cards += (
            "<div style='position:absolute;left:" + str(ax) + "px;top:340px;"
            "font-size:56px;color:#fff;font-weight:900;'>→</div>"
        )
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#0d1b2a;}"
        + ".title{position:absolute;top:14px;left:50%;transform:translateX(-50%);"
        + "font-size:32px;font-weight:900;color:#fff;white-space:nowrap;}"
        + "</style></head><body>"
        + "<div class='title'>間食の「置き換え設計」3ステップ</div>"
        + cards
        + "</body></html>"
    )
    render(html, "図解②_置き換え設計3ステップ.png")

# ─────────────────────────────────────────────
# 図解③  我慢 vs 置き換え（NG vs OK比較）
# ─────────────────────────────────────────────
def fig3():
    ng_items = [
        "「間食をゼロにする」と決意",
        "夕方の空腹を我慢する",
        "帰宅後に限界が来る",
        "反動でドカ食い",
        "自己嫌悪→翌日さらに崩れる",
    ]
    ok_items = [
        "15時にナッツ30gを先に食べる",
        "夕方の空腹がそもそも来ない",
        "帰宅3分ルールで動線を変える",
        "22時以降は選択肢をゼロにする",
        "崩れても翌日15時にリセット完了",
    ]

    def make_col(items, color, label, icon, bg):
        rows = "".join(
            "<div style='padding:13px 18px;font-size:22px;font-weight:600;color:" + color + ";border-bottom:1px solid #1a1a2e;'>"
            + icon + " " + it + "</div>"
            for it in items
        )
        return (
            "<div style='position:absolute;" + bg + ";top:80px;width:590px;height:580px;"
            "background:#0d1b2a;border:3px solid " + color + ";border-radius:16px;overflow:hidden;'>"
            "<div style='background:" + color + ";padding:16px;text-align:center;"
            "font-size:30px;font-weight:900;color:#000;'>" + label + "</div>"
            + rows + "</div>"
        )

    ng_col = make_col(ng_items, "#ef4444", "❌  我慢で止める", "→", "left:20px")
    ok_col = make_col(ok_items, "#4ade80", "✅  設計で置き換える", "→", "right:20px")

    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#080d14;}"
        + ".title{position:absolute;top:14px;left:50%;transform:translateX(-50%);"
        + "font-size:32px;font-weight:900;color:#fff;white-space:nowrap;}"
        + ".caption{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);"
        + "font-size:20px;color:#9ca3af;white-space:nowrap;}"
        + ".divider{position:absolute;left:638px;top:80px;width:4px;height:580px;background:#1e293b;}"
        + "</style></head><body>"
        + "<div class='title'>間食は「止める」のではなく「置き換える」</div>"
        + ng_col + ok_col
        + "<div class='divider'></div>"
        + "<div class='caption'>意志力に頼る戦い方を変えるだけで結果が変わる</div>"
        + "</body></html>"
    )
    render(html, "図解③_我慢vs置き換え比較.png")

# ─────────────────────────────────────────────
# 図解④  間食コスト＆カロリー比較表（実践早見表）
# ─────────────────────────────────────────────
def fig4():
    rows = [
        ("15時の間食",  "コンビニスイーツ",   "300kcal・400円", "ナッツ30g＋コーヒー", "150kcal・80円"),
        ("帰宅直後",    "ビール＋チーズかまぼこ", "350kcal・500円", "水＋ミントガム",      "0kcal・20円"),
        ("22時以降",    "菓子パン＋アイス",    "500kcal・400円", "味噌汁 or ヨーグルト", "80kcal・50円"),
        ("月間合計",    "—",                   "約34,500kcal",   "—",                    "約6,900kcal"),
        ("月間コスト",  "—",                   "約39,000円",     "—",                    "約4,500円"),
    ]
    header = (
        "<div style='display:grid;grid-template-columns:140px 1fr 1fr 1fr 1fr;"
        "background:#1e3a5f;border-radius:12px 12px 0 0;padding:0;'>"
        "<div style='padding:12px 14px;font-size:18px;font-weight:900;color:#fff;'>タイミング</div>"
        "<div style='padding:12px 14px;font-size:18px;font-weight:900;color:#ef4444;'>BEFORE（何を）</div>"
        "<div style='padding:12px 14px;font-size:18px;font-weight:900;color:#ef4444;'>kcal・コスト</div>"
        "<div style='padding:12px 14px;font-size:18px;font-weight:900;color:#4ade80;'>AFTER（何に）</div>"
        "<div style='padding:12px 14px;font-size:18px;font-weight:900;color:#4ade80;'>kcal・コスト</div>"
        "</div>"
    )
    body = ""
    for i, (timing, bef_what, bef_cal, aft_what, aft_cal) in enumerate(rows):
        bg = "#0d1b2a" if i % 2 == 0 else "#111f2e"
        fw = "800" if i >= 3 else "600"
        body += (
            "<div style='display:grid;grid-template-columns:140px 1fr 1fr 1fr 1fr;background:" + bg + ";'>"
            "<div style='padding:11px 14px;font-size:18px;font-weight:700;color:#fff;border-right:1px solid #1e3a5f;'>" + timing + "</div>"
            "<div style='padding:11px 14px;font-size:17px;font-weight:" + fw + ";color:#fca5a5;border-right:1px solid #1e3a5f;'>" + bef_what + "</div>"
            "<div style='padding:11px 14px;font-size:17px;font-weight:" + fw + ";color:#fca5a5;border-right:1px solid #1e3a5f;'>" + bef_cal + "</div>"
            "<div style='padding:11px 14px;font-size:17px;font-weight:" + fw + ";color:#86efac;border-right:1px solid #1e3a5f;'>" + aft_what + "</div>"
            "<div style='padding:11px 14px;font-size:17px;font-weight:" + fw + ";color:#86efac;'>" + aft_cal + "</div>"
            "</div>"
        )
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#0d1b2a;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px 40px;}"
        + ".title{font-size:32px;font-weight:900;color:#fff;margin-bottom:18px;text-align:center;}"
        + ".table-wrap{width:1200px;border-radius:12px;overflow:hidden;border:1px solid #1e3a5f;}"
        + ".caption{font-size:20px;color:#FF6D00;font-weight:700;margin-top:18px;text-align:center;}"
        + "</style></head><body>"
        + "<div class='title'>間食の置き換え｜コスト＆カロリー早見表</div>"
        + "<div class='table-wrap'>" + header + body + "</div>"
        + "<div class='caption'>月間 -27,600kcal ＆ -34,500円の差</div>"
        + "</body></html>"
    )
    render(html, "図解④_間食コスト比較表.png")

# ─────────────────────────────────────────────
# 図解⑤  崩れた日の復帰フロー（縦型3ステップ）
# ─────────────────────────────────────────────
def fig5():
    steps = [
        ("#ef4444", "その夜は何もしない", "反省も計算もしない。とにかく寝る"),
        ("#38bdf8", "翌朝、普通に朝食を食べる", "絶食は逆効果。反動で再崩れの原因に"),
        ("#4ade80", "翌日15時にナッツ＋コーヒー", "予定通りやれたら、もうリセット完了"),
    ]
    cards = ""
    for i, (color, title, sub) in enumerate(steps):
        cards += (
            "<div style='width:1100px;background:#0d2035;border-left:6px solid " + color + ";"
            "border-radius:12px;padding:22px 30px;margin-bottom:18px;display:flex;align-items:center;gap:24px;'>"
            "<div style='font-size:44px;font-weight:900;color:" + color + ";min-width:50px;'>0" + str(i+1) + "</div>"
            "<div>"
            "<div style='font-size:32px;font-weight:900;color:#fff;margin-bottom:6px;'>✅ " + title + "</div>"
            "<div style='font-size:22px;color:#9ca3af;'>" + sub + "</div>"
            "</div></div>"
        )
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#0d1b2a;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px 80px;}"
        + ".top{text-align:center;margin-bottom:24px;}"
        + ".top-label{font-size:28px;font-weight:900;color:#ef4444;}"
        + ".top-sub{font-size:20px;color:#9ca3af;margin-top:6px;}"
        + ".bottom{text-align:center;margin-top:14px;}"
        + ".bottom-main{font-size:30px;font-weight:900;color:#FF6D00;}"
        + ".bottom-sub{font-size:20px;color:#9ca3af;margin-top:6px;}"
        + "</style></head><body>"
        + "<div class='top'><div class='top-label'>それでも食べてしまった夜…</div>"
        + "<div class='top-sub'>飲み会・出張・どうしても我慢できなかった日</div></div>"
        + cards
        + "<div class='bottom'>"
        + "<div class='bottom-main'>8勝6敗でOK。翌日の15時にリセット完了</div>"
        + "<div class='bottom-sub'>完璧を目指すから続かない。70点を3ヶ月続ければ体は変わる</div>"
        + "</div></body></html>"
    )
    render(html, "図解⑤_崩れた日の復帰フロー.png")

if __name__ == "__main__":
    print("第 図解5枚 生成開始...\n")
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))

