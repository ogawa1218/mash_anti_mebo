#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 図解生成スクリプト（HTML/CSS + Playwright 強化版）
5枚の図解を一括生成 | 1280×720px
テーマ：朝食を変えたら、夜食も間食も勝手に減った話
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
# 図解①  菓子パン朝食→夜崩れの連鎖ループ（フロー図）
# ─────────────────────────────────────────────
def fig1():
    steps = [
        ("①", "菓子パン単独\nの朝食",         "top:60px;left:50%;transform:translateX(-50%)"),
        ("②", "血糖値\n急上昇→急降下",        "top:220px;right:80px"),
        ("③", "11時にチョコ\n昼に早食い",      "bottom:130px;right:100px"),
        ("④", "15時にお菓子\n夕方判断力ゼロ",  "bottom:130px;left:100px"),
        ("⑤", "帰宅後ドカ食い\n夜「今日くらい」", "top:220px;left:80px"),
    ]
    cards = ""
    for num, label, pos in steps:
        label_html = label.replace("\n", "<br>")
        cards += (
            "<div style='position:absolute;" + pos + ";width:210px;background:#1e3a5f;"
            "border:2px solid #ef4444;border-radius:14px;padding:16px 14px;text-align:center;'>"
            "<div style='font-size:28px;font-weight:900;color:#ef4444;'>" + num + "</div>"
            "<div style='font-size:20px;font-weight:700;color:#fff;margin-top:6px;line-height:1.35;'>" + label_html + "</div>"
            "</div>"
        )
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#0d1b2a;}"
        + ".title{position:absolute;top:14px;left:50%;transform:translateX(-50%);"
        + "font-size:30px;font-weight:900;color:#fff;white-space:nowrap;}"
        + ".center{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);"
        + "text-align:center;}"
        + ".center-main{font-size:34px;font-weight:900;color:#ef4444;}"
        + ".center-sub{font-size:20px;color:#9ca3af;margin-top:6px;}"
        + ".caption{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);"
        + "font-size:20px;color:#9ca3af;white-space:nowrap;}"
        + "</style></head><body>"
        + "<div class='title'>菓子パン朝食が夜の崩れを仕込んでいた</div>"
        + cards
        + "<div class='center'><div class='center-main'>朝→夜の<br>崩れ連鎖</div>"
        + "<div class='center-sub'>↻ 毎日繰り返す</div></div>"
        + "<div class='caption'>夜を変えるには、朝を変える必要があった</div>"
        + "</body></html>"
    )
    render(html, "図解①_菓子パン朝食の崩れ連鎖.png")


# ─────────────────────────────────────────────
# 図解②  朝リセット3ステップ全体像（横3列カード）
# ─────────────────────────────────────────────
def fig2():
    cols = [
        ("#FF6D00", "STEP 1", "最初の3口を\nたんぱく質に", "午前の食欲を\nゆるやかに", "#38bdf8", "ゆで卵・納豆\nヨーグルト"),
        ("#38bdf8", "STEP 2", "菓子パンを\n2点セット化", "禁止より\n組み合わせ", "#38bdf8", "菓子パン＋ゆで卵\nおにぎり＋味噌汁"),
        ("#4ade80", "STEP 3", "朝食を\n3パターン固定", "迷いを消して\n判断力温存", "#4ade80", "A:最短 B:和風\nC:コンビニ"),
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
            "<div style='font-size:36px;font-weight:900;color:#fff;margin:14px 0;line-height:1.3;'>" + title_html + "</div>"
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
        + "<div class='title'>朝リセット3ステップ｜最初の3口を変えるだけ</div>"
        + cards
        + "</body></html>"
    )
    render(html, "図解②_朝リセット3ステップ.png")


# ─────────────────────────────────────────────
# 図解③  糖質単独 vs たんぱく質ファースト（NG vs OK）
# ─────────────────────────────────────────────
def fig3():
    ng_items = [
        "菓子パン＋缶コーヒーだけ",
        "血糖値が急上昇→急降下",
        "11時にチョコが止まらない",
        "昼に早食い→午後は眠気",
        "帰宅後は判断力ゼロ→崩壊",
    ]
    ok_items = [
        "ゆで卵→菓子パンの順で食べる",
        "血糖値の上がり方がゆるやか",
        "11時の空腹が12時半まで持つ",
        "昼食も落ち着いて選べる",
        "夕方の判断力が残る→夜も安定",
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

    ng_col = make_col(ng_items, "#ef4444", "❌  糖質単独の朝食", "→", "left:20px")
    ok_col = make_col(ok_items, "#4ade80", "✅  たんぱく質ファースト", "→", "right:20px")

    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#080d14;}"
        + ".title{position:absolute;top:14px;left:50%;transform:translateX(-50%);"
        + "font-size:32px;font-weight:900;color:#fff;white-space:nowrap;}"
        + ".caption{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);"
        + "font-size:20px;color:#9ca3af;white-space:nowrap;}"
        + ".divider{position:absolute;left:638px;top:80px;width:4px;height:580px;background:#1e293b;}"
        + "</style></head><body>"
        + "<div class='title'>朝の最初の3口が1日を決める</div>"
        + ng_col + ok_col
        + "<div class='divider'></div>"
        + "<div class='caption'>変えるのは食事量ではなく、食べる順番だけ</div>"
        + "</body></html>"
    )
    render(html, "図解③_糖質単独vsたんぱく質ファースト.png")


# ─────────────────────────────────────────────
# 図解④  朝食3パターン早見表（テーブル）
# ─────────────────────────────────────────────
def fig4():
    rows = [
        ("パターンA", "最短・2分",  "ゆで卵2個",        "バナナ半分",     "コーヒー（無糖）"),
        ("パターンB", "和風・5分",  "納豆",             "ごはん（小）",   "味噌汁＋海苔"),
        ("パターンC", "コンビニ",   "ゆで卵 or サラチキ", "おにぎり1個",   "無糖ヨーグルト"),
    ]
    header = (
        "<div style='display:grid;grid-template-columns:160px 140px 1fr 1fr 1fr;"
        "background:#1e3a5f;border-radius:12px 12px 0 0;padding:0;'>"
        "<div style='padding:16px;font-size:22px;font-weight:900;color:#fff;'>パターン</div>"
        "<div style='padding:16px;font-size:22px;font-weight:900;color:#9ca3af;'>所要時間</div>"
        "<div style='padding:16px;font-size:22px;font-weight:900;color:#FF6D00;'>たんぱく質</div>"
        "<div style='padding:16px;font-size:22px;font-weight:900;color:#38bdf8;'>糖質</div>"
        "<div style='padding:16px;font-size:22px;font-weight:900;color:#4ade80;'>プラスα</div>"
        "</div>"
    )
    body = ""
    colors = ["#FF6D00", "#38bdf8", "#4ade80"]
    for i, (pat, time, protein, carb, plus) in enumerate(rows):
        bg = "#0d1b2a" if i % 2 == 0 else "#111f2e"
        col = colors[i]
        body += (
            "<div style='display:grid;grid-template-columns:160px 140px 1fr 1fr 1fr;background:" + bg + ";'>"
            "<div style='padding:16px;font-size:22px;font-weight:800;color:" + col + ";border-right:1px solid #1e3a5f;'>" + pat + "</div>"
            "<div style='padding:16px;font-size:20px;color:#9ca3af;border-right:1px solid #1e3a5f;'>" + time + "</div>"
            "<div style='padding:16px;font-size:20px;color:#fbbf84;border-right:1px solid #1e3a5f;'>" + protein + "</div>"
            "<div style='padding:16px;font-size:20px;color:#7dd3fc;border-right:1px solid #1e3a5f;'>" + carb + "</div>"
            "<div style='padding:16px;font-size:20px;color:#86efac;'>" + plus + "</div>"
            "</div>"
        )
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#0d1b2a;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px 40px;}"
        + ".title{font-size:32px;font-weight:900;color:#fff;margin-bottom:18px;text-align:center;}"
        + ".table-wrap{width:1200px;border-radius:12px;overflow:hidden;border:1px solid #1e3a5f;}"
        + ".caption{font-size:22px;color:#FF6D00;font-weight:700;margin-top:22px;text-align:center;}"
        + ".sub{font-size:18px;color:#9ca3af;margin-top:8px;text-align:center;}"
        + "</style></head><body>"
        + "<div class='title'>朝食3パターン早見表｜前日に選ぶだけ</div>"
        + "<div class='table-wrap'>" + header + body + "</div>"
        + "<div class='caption'>迷いを消す＝判断力を温存する</div>"
        + "<div class='sub'>前日の夜に「明日はA」と決めるだけでOK</div>"
        + "</body></html>"
    )
    render(html, "図解④_朝食3パターン早見表.png")


# ─────────────────────────────────────────────
# 図解⑤  崩れた朝のリカバリーフロー（縦型3ステップ）
# ─────────────────────────────────────────────
def fig5():
    steps = [
        ("#ef4444", "朝が崩れたことを責めない", "責めても血糖値は下がらない。気持ちを切り替える"),
        ("#38bdf8", "昼食の最初の1口を主菜にする", "焼き魚・鶏・卵。ここでリセットが始まる"),
        ("#4ade80", "15時にナッツ＋コーヒーを入れる", "第11回の間食設計と連動。これでリセット完了"),
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
        + "<div class='top'><div class='top-label'>菓子パン単独になってしまった朝…</div>"
        + "<div class='top-sub'>出張・締め切り・子供の送り出しでバタバタした日</div></div>"
        + cards
        + "<div class='bottom'>"
        + "<div class='bottom-main'>8勝6敗でOK。昼の1口でリセット完了</div>"
        + "<div class='bottom-sub'>朝が崩れてもその日を諦めない。70点を3ヶ月続ける</div>"
        + "</div></body></html>"
    )
    render(html, "図解⑤_崩れた朝のリカバリー.png")


if __name__ == "__main__":
    print("第 図解5枚 生成開始...\n")
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))

