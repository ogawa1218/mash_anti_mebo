#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第40回 図解生成スクリプト（HTML/CSS + Playwright 強化版）
体重が変わらなくても体の中は変わっている ― 糖尿病予備軍が本当に見るべき4つの数字
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
    "body{width:1280px;height:720px;overflow:hidden;font-family:'NJ','Meiryo',sans-serif;"
    "background:#0d1b2a;position:relative;}"
)

def render(html, fname):
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
    print("✅ " + fname)


def fig1():
    """図解①：体重だけ見るループ（円形フロー・問題の構造）"""
    steps = [
        ("体重が動かない", "#ef4444"),
        ("やる気が落ちる", "#f97316"),
        ("その夜に崩れる", "#ef4444"),
        ("また増える", "#ef4444"),
        ("また落ち込む", "#f97316"),
    ]
    cards = ""
    import math
    cx, cy, r = 640, 350, 200
    for i, (text, color) in enumerate(steps):
        angle = math.radians(-90 + i * 72)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        cards += (
            f"<div style='position:absolute;left:{x-90}px;top:{y-32}px;width:180px;height:64px;"
            f"background:{color};border-radius:12px;display:flex;align-items:center;"
            f"justify-content:center;font-size:22px;font-weight:800;color:#fff;text-align:center;"
            f"line-height:1.3;'>{text}</div>"
        )
    arrows = ""
    for i in range(5):
        a1 = math.radians(-90 + i * 72 + 36)
        ax = cx + r * math.cos(a1)
        ay = cy + r * math.sin(a1)
        arrows += (
            f"<div style='position:absolute;left:{ax-10}px;top:{ay-10}px;"
            f"font-size:28px;color:#555;'>→</div>"
        )

    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;font-size:32px;font-weight:900;color:#fff;'>①</div>"
        "<div style='position:absolute;top:36px;left:100px;font-size:28px;font-weight:700;color:#9ca3af;'>"
        "体重だけ見ていると、このループから抜けられない</div>"
        + cards + arrows +
        "<div style='position:absolute;top:316px;left:580px;font-size:20px;font-weight:700;"
        "color:#ef4444;background:rgba(239,68,68,.15);padding:8px 18px;border-radius:8px;'>"
        "負のループ</div>"
        "<p style='position:absolute;bottom:20px;left:56px;font-size:16px;color:#374151;'>"
        "マーシー｜100kg→68kg｜Sub3</p>"
        "<p style='position:absolute;bottom:20px;right:56px;font-size:16px;font-weight:700;color:#FF6D00;'>"
        "#第40回 体重と体の改善</p>"
        "</body></html>"
    )
    render(html, "図解①_体重だけ見るループ.png")


def fig2():
    """図解②：体重と内臓脂肪の違い（NG vs OK 左右比較）"""
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;font-size:32px;font-weight:900;color:#fff;'>②</div>"
        "<div style='position:absolute;top:36px;left:100px;font-size:28px;font-weight:700;color:#9ca3af;'>"
        "体重は「結果の一部」に過ぎない</div>"
        # 左パネル NG
        "<div style='position:absolute;left:40px;top:100px;width:560px;height:540px;"
        "background:linear-gradient(160deg,#2d0a0a,#1a0505);border:2px solid #ef4444;"
        "border-radius:20px;padding:36px;'>"
        "<div style='font-size:36px;font-weight:900;color:#ef4444;margin-bottom:20px;'>✗ 体重だけ見る</div>"
        "<div style='font-size:22px;color:#f87171;line-height:2;'>"
        "• 水分増減で1〜2kg動く<br>• 筋肉が増えても数字が増える<br>• 内臓脂肪は反映されにくい<br>"
        "• 朝と夜で1〜2kg差がある<br>• 動かないと「失敗」と感じる</div>"
        "<div style='margin-top:30px;background:#3d0808;border-radius:12px;padding:18px;'>"
        "<div style='font-size:20px;color:#ef4444;font-weight:700;'>結果：</div>"
        "<div style='font-size:24px;color:#fff;font-weight:800;margin-top:8px;'>数字に一喜一憂して続かない</div>"
        "</div></div>"
        # 右パネル OK
        "<div style='position:absolute;left:680px;top:100px;width:560px;height:540px;"
        "background:linear-gradient(160deg,#0a2d0a,#051a05);border:2px solid #4ade80;"
        "border-radius:20px;padding:36px;'>"
        "<div style='font-size:36px;font-weight:900;color:#4ade80;margin-bottom:20px;'>✓ 4つで見る</div>"
        "<div style='font-size:22px;color:#86efac;line-height:2;'>"
        "• 腹囲：内臓脂肪を直接反映<br>• 食後眠気：血糖改善のサイン<br>• 歩数：食後血糖抑制の証拠<br>"
        "• 睡眠：食欲ホルモンを安定させる<br>• 週1回測定でOK</div>"
        "<div style='margin-top:30px;background:#083d08;border-radius:12px;padding:18px;'>"
        "<div style='font-size:20px;color:#4ade80;font-weight:700;'>結果：</div>"
        "<div style='font-size:24px;color:#fff;font-weight:800;margin-top:8px;'>体重が動かない週も「前進」とわかる</div>"
        "</div></div>"
        "<p style='position:absolute;bottom:20px;left:56px;font-size:16px;color:#374151;'>"
        "マーシー｜100kg→68kg｜Sub3</p>"
        "<p style='position:absolute;bottom:20px;right:56px;font-size:16px;font-weight:700;color:#FF6D00;'>"
        "#第40回 体重と体の改善</p>"
        "</body></html>"
    )
    render(html, "図解②_体重と内臓脂肪の違い.png")


def fig3():
    """図解③：4つのチェック項目（カードグリッド）"""
    items = [
        ("①", "お腹まわり（腹囲）", "週1〜2回・朝起きてすぐ測定\n男性85cm・女性90cmが基準\n1mm縮んでも前進", "#8b5cf6"),
        ("②", "食後の体調", "食後30〜60分の眠気をチェック\n「眠気が減った」＝血糖改善のサイン\n体重より先に変化が出る", "#38bdf8"),
        ("③", "歩いた量", "「夕食後10分歩いたか」○×記録\n食後歩行は血糖スパイクを抑える\n万歩計より○×で続けやすい", "#4ade80"),
        ("④", "睡眠", "寝る・起きる時間を大きくずらさない\n睡眠崩れ→グレリン増加→食欲暴走\n「何時に寝たか」1行メモでOK", "#f59e0b"),
    ]
    cards = ""
    positions = [
        ("40px", "100px"), ("680px", "100px"),
        ("40px", "390px"), ("680px", "390px"),
    ]
    for (item, pos) in zip(items, positions):
        num, title, desc, color = item
        left, top = pos
        desc_html = desc.replace("\n", "<br>")
        cards += (
            f"<div style='position:absolute;left:{left};top:{top};width:560px;height:260px;"
            f"background:#1e3a5f;border-radius:16px;border-left:6px solid {color};padding:24px 28px;'>"
            f"<div style='font-size:52px;font-weight:900;color:{color};float:left;margin-right:16px;line-height:1;'>{num}</div>"
            f"<div><div style='font-size:26px;font-weight:800;color:#fff;margin-bottom:12px;'>{title}</div>"
            f"<div style='font-size:18px;color:#9ca3af;line-height:1.8;'>{desc_html}</div></div>"
            f"</div>"
        )
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;font-size:32px;font-weight:900;color:#fff;'>③</div>"
        "<div style='position:absolute;top:36px;left:100px;font-size:28px;font-weight:700;color:#9ca3af;'>"
        "糖尿病予備軍が見るべき4つのチェック項目</div>"
        + cards +
        "<p style='position:absolute;bottom:20px;left:56px;font-size:16px;color:#374151;'>"
        "マーシー｜100kg→68kg｜Sub3</p>"
        "<p style='position:absolute;bottom:20px;right:56px;font-size:16px;font-weight:700;color:#FF6D00;'>"
        "#第40回 体重と体の改善</p>"
        "</body></html>"
    )
    render(html, "図解③_4つのチェック項目.png")


def fig4():
    """図解④：忙しい会社員4ステップ早見表（テーブル型）"""
    rows = [
        ("1", "甘い飲み物を減らす", "ジュース→水・お茶", "液体糖分は最速で血糖を上げる", "#ef4444"),
        ("2", "夜食の回数を減らす", "週5回→週3回", "ゼロにしない。2回減らすだけ", "#f97316"),
        ("3", "夕食後10分歩く", "コンビニ往復でOK", "食後歩行は血糖スパイクを抑える", "#4ade80"),
        ("4", "週3日30分早く寝る", "毎日じゃなくていい", "睡眠安定→翌日の食欲が落ち着く", "#38bdf8"),
    ]
    rows_html = ""
    for step, action, how, why, color in rows:
        rows_html += (
            f"<tr>"
            f"<td style='padding:18px 16px;text-align:center;'>"
            f"<span style='display:inline-block;width:44px;height:44px;border-radius:50%;"
            f"background:{color};color:#fff;font-size:22px;font-weight:900;"
            f"line-height:44px;text-align:center;'>{step}</span></td>"
            f"<td style='padding:18px 16px;font-size:22px;font-weight:800;color:#fff;'>{action}</td>"
            f"<td style='padding:18px 16px;font-size:19px;color:#4ade80;font-weight:600;'>{how}</td>"
            f"<td style='padding:18px 16px;font-size:17px;color:#9ca3af;'>{why}</td>"
            f"</tr>"
        )
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        "table{width:1180px;border-collapse:collapse;}"
        "th{padding:14px 16px;font-size:18px;font-weight:700;color:#9ca3af;text-align:left;"
        "background:#0d2035;border-bottom:2px solid #1e3a5f;}"
        "tr:nth-child(even){background:#0d2035;}"
        "tr:nth-child(odd){background:#122840;}"
        "</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;font-size:32px;font-weight:900;color:#fff;'>④</div>"
        "<div style='position:absolute;top:36px;left:100px;font-size:28px;font-weight:700;color:#9ca3af;'>"
        "忙しい会社員がまずやる順番</div>"
        "<div style='position:absolute;top:96px;left:50px;width:1180px;'>"
        "<table>"
        "<thead><tr>"
        "<th style='width:70px;'>順番</th>"
        "<th>行動</th>"
        "<th>具体的に</th>"
        "<th>なぜその順番か</th>"
        "</tr></thead>"
        "<tbody>" + rows_html + "</tbody>"
        "</table>"
        "<div style='margin-top:20px;background:#1a3a1a;border-radius:12px;padding:16px 24px;"
        "border-left:4px solid #4ade80;font-size:20px;color:#4ade80;font-weight:700;'>"
        "💡 全部やらなくていい。今週は「1番だけ」から始めよう。</div>"
        "</div>"
        "<p style='position:absolute;bottom:20px;left:56px;font-size:16px;color:#374151;'>"
        "マーシー｜100kg→68kg｜Sub3</p>"
        "<p style='position:absolute;bottom:20px;right:56px;font-size:16px;font-weight:700;color:#FF6D00;'>"
        "#第40回 体重と体の改善</p>"
        "</body></html>"
    )
    render(html, "図解④_忙しい会社員4ステップ.png")


def fig5():
    """図解⑤：8勝6敗リカバリーフロー（縦型3ステップ）"""
    cases = [
        ("食べすぎた日", "次の食事を軽くする", "罰ゲームの断食はしない。1食軽くするだけ", "#ef4444", "#4ade80"),
        ("歩けなかった日", "翌日10分歩く", "「昨日サボった分を今日30分」はやらない", "#f97316", "#4ade80"),
        ("体重が増えた朝", "腹囲と睡眠を確認する", "体重だけで判断しない。4つの指標で見る", "#f59e0b", "#38bdf8"),
    ]
    cards_html = ""
    for i, (trigger, action, note, left_color, right_color) in enumerate(cases):
        top = 110 + i * 185
        cards_html += (
            f"<div style='position:absolute;left:40px;top:{top}px;width:580px;height:155px;"
            f"background:#1a0505;border:2px solid {left_color};border-radius:14px;"
            f"display:flex;align-items:center;justify-content:center;flex-direction:column;'>"
            f"<div style='font-size:20px;color:{left_color};font-weight:700;margin-bottom:6px;'>崩れパターン</div>"
            f"<div style='font-size:26px;font-weight:900;color:#fff;'>{trigger}</div>"
            f"</div>"
            f"<div style='position:absolute;left:648px;top:{top + 55}px;font-size:40px;color:#555;'>→</div>"
            f"<div style='position:absolute;left:700px;top:{top}px;width:540px;height:155px;"
            f"background:#051a05;border:2px solid {right_color};border-radius:14px;padding:20px 24px;'>"
            f"<div style='font-size:20px;color:{right_color};font-weight:700;margin-bottom:6px;'>次の1手</div>"
            f"<div style='font-size:24px;font-weight:900;color:#fff;margin-bottom:8px;'>{action}</div>"
            f"<div style='font-size:16px;color:#9ca3af;'>{note}</div>"
            f"</div>"
        )
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;font-size:32px;font-weight:900;color:#fff;'>⑤</div>"
        "<div style='position:absolute;top:36px;left:100px;font-size:28px;font-weight:700;color:#9ca3af;'>"
        "8勝6敗でいい ― 崩れた日のリカバリーフロー</div>"
        + cards_html +
        "<div style='position:absolute;bottom:56px;left:40px;right:40px;"
        "background:linear-gradient(90deg,rgba(74,222,128,.15),rgba(56,189,248,.15));"
        "border-radius:12px;padding:14px 24px;border:1px solid #1e3a5f;'>"
        "<span style='font-size:22px;font-weight:900;color:#4ade80;'>自分を責める時間は0秒でいい。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:16px;'>次の1手だけを考える。</span>"
        "</div>"
        "<p style='position:absolute;bottom:20px;left:56px;font-size:16px;color:#374151;'>"
        "マーシー｜100kg→68kg｜Sub3</p>"
        "<p style='position:absolute;bottom:20px;right:56px;font-size:16px;font-weight:700;color:#FF6D00;'>"
        "#第40回 体重と体の改善</p>"
        "</body></html>"
    )
    render(html, "図解⑤_8勝6敗リカバリーフロー.png")


if __name__ == "__main__":
    print("第40回 図解5枚 生成開始...\n")
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    print("\n✅ 全5枚完了。保存先: " + str(OUTPUT_DIR))
