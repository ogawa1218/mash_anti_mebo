#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 図解生成スクリプト（HTML/CSS + Playwright 強化版）
5枚の図解を一括生成 | 1280×720px
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
# 図解①  運動ゼロの悪循環ループ（円形フロー）
# ─────────────────────────────────────────────
def fig1():
    steps = [
        ("①", "運動しなきゃ\nと思う",         "top:60px;left:50%;transform:translateX(-50%)"),
        ("②", "ジムを検討\n→面倒で断念",      "top:220px;right:80px"),
        ("③", "罪悪感で\nストレス食い",        "bottom:130px;right:100px"),
        ("④", "体重が増え\nさらに動けない",    "bottom:130px;left:100px"),
        ("⑤", "自己嫌悪\n「俺には無理」",     "top:220px;left:80px"),
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
        + "<div class='title'>なぜ運動ゼロから抜け出せないのか</div>"
        + cards
        + "<div class='center'><div class='center-main'>動けない<br>ループ</div>"
        + "<div class='center-sub'>↻ 繰り返す</div></div>"
        + "<div class='caption'>問題は意志の弱さではなく「ジムしかない」という思い込み</div>"
        + "</body></html>"
    )
    render(html, "図解①_運動ゼロの悪循環ループ.png")

# ─────────────────────────────────────────────
# 図解②  歩くだけ3ステップ全体像（横3列カード）
# ─────────────────────────────────────────────
def fig2():
    cols = [
        ("#FF6D00", "STEP 1", "食後10分\nウォーク", "血糖値スパイクを\n抑制する", "#38bdf8", "昼食後にオフィス周り\n1周するだけ"),
        ("#38bdf8", "STEP 2", "1駅手前を\n週3回", "帰宅ルートに\n組み込む", "#38bdf8", "判断不要・時間固定\n達成感自動"),
        ("#4ade80", "STEP 3", "今より\n+1,500歩", "歩数計で\n可視化する", "#4ade80", "スマホで今の歩数を\n確認→+1,500歩"),
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
        + "<div class='title'>「歩くだけ」で体が変わる3ステップ</div>"
        + cards
        + "</body></html>"
    )
    render(html, "図解②_歩くだけ3ステップ全体像.png")

# ─────────────────────────────────────────────
# 図解③  食後ウォーク NG vs OK 比較
# ─────────────────────────────────────────────
def fig3():
    ng_items = ["食後すぐデスクに戻る", "血糖値がドカンと急上昇", "30分後に急降下→強い眠気", "15時にお菓子を食べてしまう", "夜の間食も止まらない"]
    ok_items = ["食後10分だけ歩く", "血糖値の上昇が穏やかに", "午後の眠気が軽くなる", "15時のお菓子欲求が激減", "夜の間食も自然に減る"]

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

    ng_col = make_col(ng_items, "#ef4444", "❌  食後すぐ座る", "→", "left:20px")
    ok_col = make_col(ok_items, "#4ade80", "✅  食後10分ウォーク", "→", "right:20px")

    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#080d14;}"
        + ".title{position:absolute;top:14px;left:50%;transform:translateX(-50%);"
        + "font-size:32px;font-weight:900;color:#fff;white-space:nowrap;}"
        + ".caption{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);"
        + "font-size:20px;color:#9ca3af;white-space:nowrap;}"
        + ".divider{position:absolute;left:638px;top:80px;width:4px;height:580px;background:#1e293b;}"
        + "</style></head><body>"
        + "<div class='title'>食後の10分で1日が変わる</div>"
        + ng_col + ok_col
        + "<div class='divider'></div>"
        + "<div class='caption'>出典：Buffey et al., Sports Medicine, 2022</div>"
        + "</body></html>"
    )
    render(html, "図解③_食後ウォークNGvsOK.png")

# ─────────────────────────────────────────────
# 図解④  歩数アップ実践早見表（テーブル）
# ─────────────────────────────────────────────
def fig4():
    rows = [
        ("食後10分ウォーク",     "約1,000歩",  "約10分",   "毎日の昼食後"),
        ("1駅手前ウォーク",      "約1,200歩",  "約15分",   "帰宅時・週3回"),
        ("1つ先のコンビニ",      "約300歩",    "約3分",    "朝の買い物時"),
        ("階段を使う",           "約200歩",    "約2分",    "2〜3階まで"),
        ("駐車場を遠くにする",   "約400歩",    "約5分",    "買い物時"),
    ]
    header = (
        "<div style='display:grid;grid-template-columns:240px 1fr 1fr 1fr;"
        "background:#1e3a5f;border-radius:12px 12px 0 0;padding:0;'>"
        "<div style='padding:14px 16px;font-size:22px;font-weight:900;color:#fff;'>やること</div>"
        "<div style='padding:14px 16px;font-size:22px;font-weight:900;color:#FF6D00;'>歩数</div>"
        "<div style='padding:14px 16px;font-size:22px;font-weight:900;color:#38bdf8;'>時間</div>"
        "<div style='padding:14px 16px;font-size:22px;font-weight:900;color:#4ade80;'>タイミング</div>"
        "</div>"
    )
    body = ""
    for i, (action, steps, time, timing) in enumerate(rows):
        bg = "#0d1b2a" if i % 2 == 0 else "#111f2e"
        body += (
            "<div style='display:grid;grid-template-columns:240px 1fr 1fr 1fr;background:" + bg + ";'>"
            "<div style='padding:13px 16px;font-size:21px;font-weight:700;color:#fff;border-right:1px solid #1e3a5f;'>" + action + "</div>"
            "<div style='padding:13px 16px;font-size:20px;color:#fbbf84;border-right:1px solid #1e3a5f;'>" + steps + "</div>"
            "<div style='padding:13px 16px;font-size:20px;color:#7dd3fc;border-right:1px solid #1e3a5f;'>" + time + "</div>"
            "<div style='padding:13px 16px;font-size:20px;color:#86efac;'>" + timing + "</div>"
            "</div>"
        )
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#0d1b2a;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px 40px;}"
        + ".title{font-size:32px;font-weight:900;color:#fff;margin-bottom:18px;text-align:center;}"
        + ".table-wrap{width:1200px;border-radius:12px;overflow:hidden;border:1px solid #1e3a5f;}"
        + ".note{font-size:22px;font-weight:700;color:#FF6D00;margin-top:16px;text-align:center;}"
        + "</style></head><body>"
        + "<div class='title'>+1,500歩の足し方 早見表</div>"
        + "<div class='table-wrap'>" + header + body + "</div>"
        + "<div class='note'>どれか1〜2つの組み合わせで +1,500歩は達成できる</div>"
        + "</body></html>"
    )
    render(html, "図解④_歩数アップ実践早見表.png")

# ─────────────────────────────────────────────
# 図解⑤  崩れた日の復帰フロー（縦型3ステップ）
# ─────────────────────────────────────────────
def fig5():
    steps = [
        ("#ef4444", "その日は何もしない", "反省も後悔もしない。ただ寝る"),
        ("#38bdf8", "翌日、いつもの時間に歩く", "それだけでリセット完了。気合いは不要"),
        ("#4ade80", "2日休んだら3日目に10分だけ", "10分歩けたら、もう戻れている"),
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
        + "<div class='top'><div class='top-label'>歩けなかった日…</div>"
        + "<div class='top-sub'>雨の日・飲み会の日・体調が悪い日・疲れた夜</div></div>"
        + cards
        + "<div class='bottom'>"
        + "<div class='bottom-main'>8勝6敗でOK。週4日歩けたら十分です</div>"
        + "<div class='bottom-sub'>体は責めるほど変わらない。歩くほど変わる</div>"
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

