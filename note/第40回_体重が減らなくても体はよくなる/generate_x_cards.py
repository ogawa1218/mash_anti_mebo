#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第40回 X投稿用カード画像 10枚生成スクリプト（図解版）
体重が変わらなくても体の中は変わっている
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
HASHTAG = "#第40回 体重と体の改善"

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;background:#0d1b2a;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
    ".num{position:absolute;top:28px;right:48px;font-size:20px;font-weight:700;color:#334155;}"
    ".author{position:absolute;bottom:20px;left:48px;font-size:17px;font-weight:400;color:#334155;}"
    ".series{position:absolute;bottom:20px;right:48px;font-size:17px;font-weight:700;color:#FF6D00;}"
)

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]

TWEETS = [
    "先週も体重変わらなかった。\n夜食を減らした。歩いた。\nなのに数字はゼロ。\n「また失敗した」\nそういう朝、何回経験しましたか？\n僕は100kgのころ、週3回は味わっていました。",
    "体重が動かない本当の原因は\n「意志が弱い」ことではありません。\n見ていた「指標」が間違っていただけです。\n同じ1kgでも水分・脂肪・筋肉で意味が全然違う。\n体重計はその内訳を教えてくれません。",
    "英国大規模研究（UKPDS）が示すこと。\n体重が大きく変わらなくても\n食事・生活習慣を変えれば\nHbA1cは改善する。\n体重が動かない＝失敗ではない。\n見る場所を変えれば、続けられるようになる。",
    "糖尿病予備軍が見るべき4つの数字。\n①腹囲：内臓脂肪を直接反映\n②食後眠気：血糖改善のサイン\n③夕食後10分歩く：血糖スパイクを抑える\n④睡眠：食欲ホルモンを安定させる\n体重より正直に「変化」を教えてくれる。",
    "腹囲1cmの意味を知っていますか？\n体重が1gも変わらなくても\n腹囲が1〜2cm縮めば\n内臓脂肪が減っているサインです。\n内臓脂肪減少→インスリンの効きが改善\n→血糖コントロールが改善し始める。",
    "忙しい会社員が最初にやるべき順番。\n1）甘い飲み物を水かお茶に変える（最優先）\n2）夜食を週5→週3回にする\n3）夕食後10分歩く\n4）週3日だけ30分早く寝る\n全部いっぺんにやらなくていい。",
    "今週の月曜から始めること。\n【ステップ1だけ】\n甘い飲み物を水かお茶に変える。\n缶コーヒー→無糖 / スポーツドリンク→水\n1週間で食後眠気が減ってきたら\n血糖が安定し始めた証拠です。",
    "8勝6敗でいい。これが僕の基準。\n食べすぎ→次の食事を軽くするだけ\n歩けない→翌日10分歩くだけ\n体重増→腹囲と睡眠を確認するだけ\n自分を責める時間は0秒でいい。\n次の1手だけ考える。",
    "食後の眠気が「血糖スパイク」のサイン。\n血糖急上昇→インスリン大量分泌\n→血糖急降下→眠気・だるさ\nこれが「食後のあの眠さ」の正体。\n逆に言えば食後眠気が減ってきた＝\n血糖が安定してきた証拠。体重より先に変わる。",
    "今夜やること、1つだけ。\n夕食後に10分歩いて\n寝る前にお腹まわりを1回測って記録する。\n体重計は明日の朝でいい。\n今日はこの1つだけ。\nhttps://note.com/longevity_navi\n#ダイエット #メタボ #糖尿病予備軍",
]


def wrap(content, num_str):
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        + content
        + f"<p class='num'>{num_str}</p>"
        + "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        + f"<p class='series'>{HASHTAG}</p>"
        + "</body></html>"
    )


def card_01():
    content = (
        "<div style='position:absolute;left:56px;top:60px;font-size:36px;font-weight:900;"
        "color:#9ca3af;'>共感</div>"
        "<div style='position:absolute;left:56px;top:120px;right:56px;'>"
        "<div style='font-size:34px;font-weight:900;color:#fff;line-height:1.5;margin-bottom:32px;'>"
        "先週も体重が動かなかった朝の話</div>"
        # タイムライン
        + "".join([
            f"<div style='display:flex;align-items:center;margin-bottom:20px;'>"
            f"<div style='width:120px;font-size:18px;color:#6b7280;flex-shrink:0;'>{time}</div>"
            f"<div style='width:12px;height:12px;border-radius:50%;background:{color};"
            f"flex-shrink:0;margin-right:16px;'></div>"
            f"<div style='font-size:22px;font-weight:700;color:#fff;'>{event}</div>"
            f"</div>"
            for time, event, color in [
                ("夕食", "夜食を我慢した。少し歩いた", "#4ade80"),
                ("就寝前", "「明日こそ体重が減るはず」", "#38bdf8"),
                ("翌朝", "体重計→200g増えていた", "#ef4444"),
                ("朝7時", "「また失敗した」と落ち込む", "#ef4444"),
                ("その夜", "崩れる → また増える", "#ef4444"),
            ]
        ]) +
        "<div style='margin-top:24px;background:#1e3a5f;border-radius:12px;padding:16px 24px;"
        "border-left:4px solid #FF6D00;font-size:20px;color:#FF6D00;font-weight:700;'>"
        "このループの原因は「指標」にあった</div>"
        "</div>"
    )
    return wrap(content, "1/10")


def card_02():
    content = (
        "<div style='position:absolute;left:56px;top:60px;font-size:36px;font-weight:900;"
        "color:#9ca3af;'>原因</div>"
        "<div style='position:absolute;left:56px;top:120px;right:56px;'>"
        "<div style='font-size:34px;font-weight:900;color:#fff;line-height:1.4;margin-bottom:28px;'>"
        "体重計が教えてくれないこと</div>"
        "<div style='display:flex;gap:24px;margin-bottom:24px;'>"
        + "".join([
            f"<div style='flex:1;background:#1e3a5f;border-radius:12px;padding:20px;text-align:center;'>"
            f"<div style='font-size:40px;font-weight:900;color:{color};'>{icon}</div>"
            f"<div style='font-size:20px;font-weight:700;color:#fff;margin-top:8px;'>{label}</div>"
            f"<div style='font-size:15px;color:#9ca3af;margin-top:6px;'>{desc}</div>"
            f"</div>"
            for icon, label, desc, color in [
                ("💧", "水分", "1〜2kg動く", "#38bdf8"),
                ("🔥", "脂肪", "ゆっくり変化", "#FF6D00"),
                ("💪", "筋肉", "増えると体重増", "#4ade80"),
            ]
        ]) +
        "</div>"
        "<div style='background:#2d1515;border:2px solid #ef4444;border-radius:12px;"
        "padding:18px 24px;font-size:22px;color:#fff;font-weight:700;'>"
        "体重計はこの内訳を教えてくれない。<span style='color:#ef4444;'>だから「体重だけ」では正確に判断できない。</span>"
        "</div></div>"
    )
    return wrap(content, "2/10")


def card_03():
    content = (
        "<div style='position:absolute;left:56px;top:60px;font-size:36px;font-weight:900;"
        "color:#9ca3af;'>解決策</div>"
        "<div style='position:absolute;left:56px;top:120px;right:56px;'>"
        "<div style='font-size:30px;font-weight:900;color:#fff;margin-bottom:24px;'>"
        "UKPDS研究（英国・大規模糖尿病研究）が示すこと</div>"
        "<div style='display:flex;gap:32px;margin-bottom:24px;'>"
        "<div style='flex:1;background:#0d2035;border:2px solid #ef4444;border-radius:14px;"
        "padding:24px;text-align:center;'>"
        "<div style='font-size:22px;color:#ef4444;font-weight:700;margin-bottom:12px;'>これまでの思い込み</div>"
        "<div style='font-size:26px;font-weight:900;color:#fff;'>体重が変わらない<br>＝失敗</div>"
        "</div>"
        "<div style='display:flex;align-items:center;font-size:48px;color:#555;'>→</div>"
        "<div style='flex:1;background:#0d2a0d;border:2px solid #4ade80;border-radius:14px;"
        "padding:24px;text-align:center;'>"
        "<div style='font-size:22px;color:#4ade80;font-weight:700;margin-bottom:12px;'>研究が示す事実</div>"
        "<div style='font-size:26px;font-weight:900;color:#fff;'>体重変化がなくても<br>HbA1cは改善する</div>"
        "</div></div>"
        "<div style='background:#1e3a5f;border-radius:12px;padding:16px 24px;"
        "font-size:20px;color:#38bdf8;font-weight:700;'>"
        "見る場所を変えるだけで、続けられるようになる。</div>"
        "</div>"
    )
    return wrap(content, "3/10")


def card_04():
    items = [
        ("①", "お腹まわり（腹囲）", "男性85cm基準。内臓脂肪を直接反映", "#8b5cf6"),
        ("②", "食後の体調", "眠気が減った＝血糖改善のサイン", "#38bdf8"),
        ("③", "歩いた量", "夕食後10分○×記録で十分", "#4ade80"),
        ("④", "睡眠", "崩れると食欲ホルモンが暴れる", "#f59e0b"),
    ]
    cards_html = "".join([
        f"<div style='background:#1e3a5f;border-radius:12px;border-left:5px solid {color};"
        f"padding:16px 20px;display:flex;align-items:center;gap:16px;'>"
        f"<span style='font-size:36px;font-weight:900;color:{color};width:40px;'>{num}</span>"
        f"<div><div style='font-size:22px;font-weight:800;color:#fff;'>{title}</div>"
        f"<div style='font-size:17px;color:#9ca3af;margin-top:4px;'>{desc}</div></div>"
        f"</div>"
        for num, title, desc, color in items
    ])
    content = (
        "<div style='position:absolute;left:56px;top:60px;font-size:36px;font-weight:900;"
        "color:#9ca3af;'>仕組み</div>"
        "<div style='position:absolute;left:56px;top:120px;right:56px;'>"
        "<div style='font-size:30px;font-weight:900;color:#fff;margin-bottom:20px;'>"
        "糖尿病予備軍が見るべき4つの数字</div>"
        "<div style='display:flex;flex-direction:column;gap:14px;'>"
        + cards_html + "</div></div>"
    )
    return wrap(content, "4/10")


def card_05():
    content = (
        "<div style='position:absolute;left:56px;top:60px;font-size:36px;font-weight:900;"
        "color:#9ca3af;'>効果</div>"
        "<div style='position:absolute;left:56px;top:120px;right:56px;'>"
        "<div style='font-size:30px;font-weight:900;color:#fff;margin-bottom:24px;'>"
        "腹囲1cmが縮んだときの意味</div>"
        "<div style='display:flex;gap:24px;margin-bottom:20px;'>"
        "<div style='flex:1;background:#2d0a0a;border:2px solid #ef4444;border-radius:14px;"
        "padding:24px;'>"
        "<div style='font-size:22px;color:#ef4444;font-weight:700;margin-bottom:12px;'>体重が変わらない週</div>"
        "<div style='font-size:60px;font-weight:900;color:#ef4444;text-align:center;'>±0 kg</div>"
        "<div style='font-size:18px;color:#9ca3af;margin-top:8px;text-align:center;'>「また失敗した」と思いがち</div>"
        "</div>"
        "<div style='flex:1;background:#0a2d0a;border:2px solid #4ade80;border-radius:14px;"
        "padding:24px;'>"
        "<div style='font-size:22px;color:#4ade80;font-weight:700;margin-bottom:12px;'>でも腹囲は…</div>"
        "<div style='font-size:60px;font-weight:900;color:#4ade80;text-align:center;'>-1 cm</div>"
        "<div style='font-size:18px;color:#9ca3af;margin-top:8px;text-align:center;'>内臓脂肪が減っているサイン</div>"
        "</div></div>"
        "<div style='background:#1e3a5f;border-radius:12px;padding:16px 24px;"
        "font-size:20px;color:#38bdf8;font-weight:700;'>"
        "内臓脂肪↓ → インスリンの効き改善 → 血糖コントロール改善</div>"
        "</div>"
    )
    return wrap(content, "5/10")


def card_06():
    steps = [
        ("1", "甘い飲み物を減らす", "最優先。液体糖分は最速で血糖を上げる", "#ef4444"),
        ("2", "夜食を週5→週3回", "ゼロにしない。2回減らすだけ", "#f97316"),
        ("3", "夕食後10分歩く", "食後歩行は血糖スパイクを抑える", "#4ade80"),
        ("4", "週3日30分早く寝る", "毎日じゃなくていい", "#38bdf8"),
    ]
    content = (
        "<div style='position:absolute;left:56px;top:60px;font-size:36px;font-weight:900;"
        "color:#9ca3af;'>設計</div>"
        "<div style='position:absolute;left:56px;top:120px;right:56px;'>"
        "<div style='font-size:30px;font-weight:900;color:#fff;margin-bottom:20px;'>"
        "忙しい会社員が最初にやるべき順番</div>"
        "<table style='width:100%;border-collapse:collapse;'>"
        "<thead><tr style='background:#0d2035;'>"
        "<th style='padding:12px 16px;color:#9ca3af;font-size:18px;text-align:left;width:60px;'>順</th>"
        "<th style='padding:12px 16px;color:#9ca3af;font-size:18px;text-align:left;'>行動</th>"
        "<th style='padding:12px 16px;color:#9ca3af;font-size:18px;text-align:left;'>なぜ</th>"
        "</tr></thead><tbody>"
        + "".join([
            f"<tr style='background:#122840;border-bottom:1px solid #1e3a5f;'>"
            f"<td style='padding:14px 16px;text-align:center;'>"
            f"<span style='display:inline-block;width:36px;height:36px;border-radius:50%;"
            f"background:{color};color:#fff;font-size:18px;font-weight:900;line-height:36px;'>{num}</span></td>"
            f"<td style='padding:14px 16px;font-size:20px;font-weight:700;color:#fff;'>{action}</td>"
            f"<td style='padding:14px 16px;font-size:17px;color:#9ca3af;'>{why}</td>"
            f"</tr>"
            for num, action, why, color in steps
        ]) +
        "</tbody></table>"
        "</div>"
    )
    return wrap(content, "6/10")


def card_07():
    step_items = [
        ("缶コーヒー（砂糖入り）", "無糖コーヒー・ブラック", "#38bdf8"),
        ("スポーツドリンク", "水・麦茶", "#38bdf8"),
        ("ジュース・甘いお茶", "緑茶・ほうじ茶", "#38bdf8"),
    ]
    content = (
        "<div style='position:absolute;left:56px;top:60px;font-size:36px;font-weight:900;"
        "color:#9ca3af;'>実践</div>"
        "<div style='position:absolute;left:56px;top:120px;right:56px;'>"
        "<div style='font-size:30px;font-weight:900;color:#FF6D00;margin-bottom:8px;'>"
        "ステップ1だけ今週やる</div>"
        "<div style='font-size:22px;color:#fff;font-weight:700;margin-bottom:24px;'>"
        "「甘い飲み物を水かお茶に変える」</div>"
        "<div style='display:flex;flex-direction:column;gap:14px;margin-bottom:20px;'>"
        + "".join([
            f"<div style='display:flex;align-items:center;gap:16px;'>"
            f"<div style='flex:1;background:#2d1515;border-radius:10px;padding:14px 20px;"
            f"font-size:20px;color:#ef4444;font-weight:700;'>✗ {before}</div>"
            f"<div style='font-size:28px;color:#555;'>→</div>"
            f"<div style='flex:1;background:#0a2d0a;border-radius:10px;padding:14px 20px;"
            f"font-size:20px;color:#4ade80;font-weight:700;'>✓ {after}</div>"
            f"</div>"
            for before, after, color in step_items
        ]) +
        "</div>"
        "<div style='background:#1e3a5f;border-radius:10px;padding:14px 20px;"
        "font-size:19px;color:#38bdf8;font-weight:700;'>"
        "1週間後、食後眠気が減ってきたら血糖安定のサインです。</div>"
        "</div>"
    )
    return wrap(content, "7/10")


def card_08():
    cases = [
        ("食べすぎた日", "次の食事を軽くする", "#ef4444", "#4ade80"),
        ("歩けなかった日", "翌日10分歩く", "#f97316", "#4ade80"),
        ("体重が増えた朝", "腹囲と睡眠を確認する", "#f59e0b", "#38bdf8"),
    ]
    content = (
        "<div style='position:absolute;left:56px;top:60px;font-size:36px;font-weight:900;"
        "color:#9ca3af;'>復帰</div>"
        "<div style='position:absolute;left:56px;top:120px;right:56px;'>"
        "<div style='font-size:34px;font-weight:900;color:#fff;margin-bottom:24px;'>"
        "8勝6敗でいい ― 崩れた日のリカバリー</div>"
        "<div style='display:flex;flex-direction:column;gap:16px;'>"
        + "".join([
            f"<div style='display:flex;align-items:center;gap:16px;'>"
            f"<div style='background:#2d0a0a;border:2px solid {lc};border-radius:10px;"
            f"padding:14px 20px;width:340px;font-size:20px;font-weight:700;color:#fff;'>{trigger}</div>"
            f"<div style='font-size:32px;color:#555;'>→</div>"
            f"<div style='flex:1;background:#051a05;border:2px solid {rc};border-radius:10px;"
            f"padding:14px 20px;font-size:20px;font-weight:700;color:#fff;'>{action}</div>"
            f"</div>"
            for trigger, action, lc, rc in cases
        ]) +
        "</div>"
        "<div style='margin-top:20px;background:#1e3a5f;border-radius:10px;padding:14px 20px;"
        "font-size:20px;color:#4ade80;font-weight:700;'>"
        "自分を責める時間は0秒でいい。次の1手だけ考える。</div>"
        "</div>"
    )
    return wrap(content, "8/10")


def card_09():
    content = (
        "<div style='position:absolute;left:56px;top:60px;font-size:36px;font-weight:900;"
        "color:#9ca3af;'>深掘り</div>"
        "<div style='position:absolute;left:56px;top:120px;right:56px;'>"
        "<div style='font-size:30px;font-weight:900;color:#fff;margin-bottom:20px;'>"
        "食後の眠気が「血糖スパイク」のサインである理由</div>"
        "<div style='display:flex;align-items:center;gap:0;margin-bottom:20px;'>"
        + "".join([
            f"<div style='text-align:center;padding:16px 0;'>"
            f"<div style='background:{bg};border-radius:10px;padding:16px 20px;width:220px;"
            f"font-size:19px;font-weight:700;color:#fff;line-height:1.4;'>{label}</div>"
            f"</div>"
            + (f"<div style='font-size:28px;color:#555;padding:0 4px;'>→</div>" if arrow else "")
            for label, bg, arrow in [
                ("血糖値が\n急上昇", "#ef4444", True),
                ("インスリンが\n大量分泌", "#f97316", True),
                ("血糖値が\n急降下", "#ef4444", True),
                ("食後の眠気・\nだるさ", "#8b5cf6", False),
            ]
        ]) +
        "</div>"
        "<div style='background:#0a2d0a;border:2px solid #4ade80;border-radius:12px;"
        "padding:16px 24px;font-size:20px;color:#4ade80;font-weight:700;'>"
        "逆に言えば「食後眠気が減ってきた」= 血糖が安定してきた証拠。体重より先に変わる。</div>"
        "<div style='margin-top:12px;font-size:17px;color:#6b7280;'>"
        "出典：Colberg SR et al. Exercise and type 2 diabetes. Diabetes Care, 2010.</div>"
        "</div>"
    )
    return wrap(content, "9/10")


def card_10():
    content = (
        "<div style='position:absolute;left:56px;top:60px;font-size:36px;font-weight:900;"
        "color:#9ca3af;'>今夜やること</div>"
        "<div style='position:absolute;left:56px;top:120px;right:56px;'>"
        "<div style='font-size:34px;font-weight:900;color:#FF6D00;margin-bottom:24px;'>"
        "今夜やること、1つだけ</div>"
        "<div style='display:flex;flex-direction:column;gap:16px;margin-bottom:28px;'>"
        + "".join([
            f"<div style='background:#1e3a5f;border-radius:12px;padding:18px 24px;"
            f"display:flex;align-items:center;gap:16px;'>"
            f"<span style='width:36px;height:36px;border-radius:50%;background:#4ade80;"
            f"color:#000;font-size:20px;font-weight:900;display:flex;align-items:center;"
            f"justify-content:center;flex-shrink:0;'>✓</span>"
            f"<span style='font-size:22px;font-weight:700;color:#fff;'>{text}</span>"
            f"</div>"
            for text in [
                "夕食後に10分歩く",
                "寝る前にお腹まわりを1回測って記録する",
                "体重計は明日の朝でいい",
            ]
        ]) +
        "</div>"
        "<div style='background:linear-gradient(90deg,#FF6D00,#f97316);border-radius:12px;"
        "padding:18px 24px;text-align:center;font-size:22px;font-weight:900;color:#fff;'>"
        "詳しくはnoteで → note.com/longevity_navi</div>"
        "</div>"
    )
    return wrap(content, "10/10")


CARD_FUNCS = [
    card_01, card_02, card_03, card_04, card_05,
    card_06, card_07, card_08, card_09, card_10
]


def render(html, fname):
    tmp = ARTICLE_DIR / "_tmp_xcard.html"
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


if __name__ == "__main__":
    print("第40回 X投稿カード画像（図解版）生成開始...\n")
    for i, func in enumerate(CARD_FUNCS):
        html = func()
        fname = "x_post_" + str(i + 1).zfill(2) + ".png"
        render(html, fname)
        print(f"✅ {fname}  [{CARD_TAGS[i]}]")
    print("\n✅ 全10枚完了。保存先: " + str(OUTPUT_DIR))
