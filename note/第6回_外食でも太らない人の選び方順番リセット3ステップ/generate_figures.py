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
# 図解①  外食崩れのループ（円形フロー）
# ─────────────────────────────────────────────
def fig1():
    steps = [
        ("①", "判断力ゼロで\n店に入る",    "top:60px;left:50%;transform:translateX(-50%)"),
        ("②", "主食から\n注文する",         "top:220px;right:80px"),
        ("③", "血糖値が\n急上昇→急降下",   "bottom:130px;right:100px"),
        ("④", "帰宅後に\nつまみ食い",      "bottom:130px;left:100px"),
        ("⑤", "自己嫌悪\n翌日も崩れる",    "top:220px;left:80px"),
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
        + "<div class='title'>なぜ外食で毎回崩れるのか</div>"
        + cards
        + "<div class='center'><div class='center-main'>毎晩の<br>ループ</div>"
        + "<div class='center-sub'>↻ 繰り返す</div></div>"
        + "<div class='caption'>意志の問題ではなく、最初の1手が間違っていた</div>"
        + "</body></html>"
    )
    render(html, "図解①_外食崩れのループ.png")

# ─────────────────────────────────────────────
# 図解②  主菜→副菜→主食 3ステップ全体像
# ─────────────────────────────────────────────
def fig2():
    cols = [
        ("#FF6D00", "STEP 1", "主菜を決める", "たんぱく質の\n土台をつくる", "#38bdf8", "焼き魚・刺身\n鶏グリル・卵系"),
        ("#38bdf8", "STEP 2", "副菜を1つ足す", "勢い食いを\n防ぐ", "#38bdf8", "サラダ・おひたし\n味噌汁1杯でもOK"),
        ("#4ade80", "STEP 3", "主食を最後に\n調整する", "量を必要分\nだけ選ぶ", "#4ade80", "小盛り・替え玉なし\n丼→定食化"),
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
        + "<div class='title'>外食で崩れない「順番リセット」3ステップ</div>"
        + cards
        + "</body></html>"
    )
    render(html, "図解②_順番リセット3ステップ.png")

# ─────────────────────────────────────────────
# 図解③  主食スタートNG vs 主菜スタートOK
# ─────────────────────────────────────────────
def fig3():
    ng_items = ["主食（丼・麺）から注文", "血糖値が急上昇→急降下", "追加注文の衝動が増える", "帰宅後のつまみ食い", "翌朝むくみ・重だるさ"]
    ok_items = ["主菜（たんぱく質）を先に注文", "血糖値の急上昇が緩やかに", "満足感が出て追加注文が減る", "帰宅後のつまみ食いが激減", "翌朝の体が軽い"]

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

    ng_col = make_col(ng_items, "#ef4444", "❌  主食スタート", "→", "left:20px")
    ok_col = make_col(ok_items, "#4ade80", "✅  主菜スタート", "→", "right:20px")

    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#080d14;}"
        + ".title{position:absolute;top:14px;left:50%;transform:translateX(-50%);"
        + "font-size:32px;font-weight:900;color:#fff;white-space:nowrap;}"
        + ".caption{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);"
        + "font-size:20px;color:#9ca3af;white-space:nowrap;}"
        + ".divider{position:absolute;left:638px;top:80px;width:4px;height:580px;background:#1e293b;}"
        + "</style></head><body>"
        + "<div class='title'>最初の1手が結果を決める</div>"
        + ng_col + ok_col
        + "<div class='divider'></div>"
        + "<div class='caption'>変えるのは意志力ではなく順番だけ</div>"
        + "</body></html>"
    )
    render(html, "図解③_NGvsOK比較.png")

# ─────────────────────────────────────────────
# 図解④  外食シーン別 順番リセット早見表
# ─────────────────────────────────────────────
def fig4():
    rows = [
        ("定食屋",   "焼き魚・しょうが焼き",    "おひたし・小鉢",       "ご飯 小盛り"),
        ("居酒屋",   "刺身盛り・鶏グリル",       "海藻サラダ",           "シメは半分"),
        ("ラーメン屋","ゆで卵を追加",            "海苔・メンマを先食い",  "替え玉なし"),
        ("コンビニ", "サラダチキン・ゆで卵",     "野菜惣菜を追加",       "おにぎり1個まで"),
        ("会食",     "魚料理・肉料理から",        "サラダを先に取る",     "ご飯は少量で"),
    ]
    header = (
        "<div style='display:grid;grid-template-columns:180px 1fr 1fr 1fr;"
        "background:#1e3a5f;border-radius:12px 12px 0 0;padding:0;'>"
        "<div style='padding:14px 16px;font-size:22px;font-weight:900;color:#fff;'>外食シーン</div>"
        "<div style='padding:14px 16px;font-size:22px;font-weight:900;color:#FF6D00;'>主菜</div>"
        "<div style='padding:14px 16px;font-size:22px;font-weight:900;color:#38bdf8;'>副菜</div>"
        "<div style='padding:14px 16px;font-size:22px;font-weight:900;color:#4ade80;'>主食</div>"
        "</div>"
    )
    body = ""
    for i, (scene, main, side, carb) in enumerate(rows):
        bg = "#0d1b2a" if i % 2 == 0 else "#111f2e"
        body += (
            "<div style='display:grid;grid-template-columns:180px 1fr 1fr 1fr;background:" + bg + ";'>"
            "<div style='padding:13px 16px;font-size:21px;font-weight:700;color:#fff;border-right:1px solid #1e3a5f;'>" + scene + "</div>"
            "<div style='padding:13px 16px;font-size:20px;color:#fbbf84;border-right:1px solid #1e3a5f;'>" + main + "</div>"
            "<div style='padding:13px 16px;font-size:20px;color:#7dd3fc;border-right:1px solid #1e3a5f;'>" + side + "</div>"
            "<div style='padding:13px 16px;font-size:20px;color:#86efac;'>" + carb + "</div>"
            "</div>"
        )
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS
        + "body{background:#0d1b2a;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px 40px;}"
        + ".title{font-size:32px;font-weight:900;color:#fff;margin-bottom:18px;text-align:center;}"
        + ".table-wrap{width:1200px;border-radius:12px;overflow:hidden;border:1px solid #1e3a5f;}"
        + "</style></head><body>"
        + "<div class='title'>外食シーン別 順番リセット早見表</div>"
        + "<div class='table-wrap'>" + header + body + "</div>"
        + "</body></html>"
    )
    render(html, "図解④_外食シーン別早見表.png")

# ─────────────────────────────────────────────
# 図解⑤  崩れた日の翌日リセットフロー
# ─────────────────────────────────────────────
def fig5():
    steps = [
        ("#ef4444", "自己嫌悪をやめる", '"また崩れた"じゃなく"次の食事で戻す"に切り替える'),
        ("#38bdf8", "翌朝食を抜かない",  "空腹のまま夜を迎えると再崩れしやすくなる"),
        ("#4ade80", "次の外食で主菜から選ぶ", "1回順番通りに選べたらリセット完了"),
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
        + "<div class='top'><div class='top-label'>崩れた日の夜…</div>"
        + "<div class='top-sub'>会食でドカ食い・深夜ラーメン・止まらなかった夜</div></div>"
        + cards
        + "<div class='bottom'>"
        + "<div class='bottom-main'>8勝6敗でOK。続けることが全てです</div>"
        + "<div class='bottom-sub'>体は責めるほど変わらない。整えるほど変わる</div>"
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

