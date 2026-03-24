#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第41回 X投稿用カード画像 10枚生成スクリプト（図解版）"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
HASHTAG = "#第41回 就寝前入浴"
FIXED_TAGS = "\n\n#ダイエット #メタボ #習慣化 #睡眠 #睡眠の質 #入浴"

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;background:#0d1b2a;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
    ".num{position:absolute;top:44px;right:56px;font-size:22px;font-weight:700;color:#444;}"
    ".author{position:absolute;bottom:22px;left:56px;font-size:18px;font-weight:400;color:#3a3a3a;}"
    ".series{position:absolute;bottom:22px;right:56px;font-size:18px;font-weight:700;}"
)

TWEETS = [
    "帰宅して、シャワー3分で終わらせた夜。\n\n布団に入っても眠れない。\n夜中に起きる。\n朝が重い。\n\n「疲れてるから仕方ない」\n\nそう思ってた。\nでも本当の原因は別にあった。\n\n↓続き（2/10）" + FIXED_TAGS,
    "シャワーで終わると眠れない理由。\n\n人は「深部体温が下がるとき」に眠気が来やすい。\n\nシャワーだけ→全身が温まらない\n→体温変化が起きない\n→眠気のスイッチが入りにくい\n\n湯船とシャワーの差は「体温の設計」の問題だ。\n\n↓続き（3/10）" + FIXED_TAGS,
    "睡眠を変えた「入浴3原則」。\n\n① 38〜40℃で10〜15分\n② 就寝1〜2時間前に入る\n③ 入浴後の流れを整える\n\nジムもサプリも器具もいらない。\n湯船があれば今夜から試せる。\n\n↓続き（4/10）" + FIXED_TAGS,
    "なぜ「就寝1〜2時間前」なのか。\n\n入浴→体が温まる\n↓\nお風呂を出たあと熱が逃げる\n↓\n深部体温が下がる\n↓\n自然な眠気が来る\n\nこの流れが完成するのに約1〜2時間かかる。\n\n直前に入ると、まだ熱いまま布団に入ることになる。\n\n↓続き（5/10）" + FIXED_TAGS,
    "研究が示した「湯船の数字」。\n\n2025年の観察研究（Sleep Health誌）では、就寝前に湯船に入った人は\n\n✅ 睡眠効率が高い\n✅ 夜中に起きる時間が短い\n✅「よく眠れなかった」割合が低い\n\n「気がする」じゃなく、客観的な指標が動いていた。\n\n↓続き（6/10）" + FIXED_TAGS,
    "「入れない日が続く」を防ぐ時間設計。\n\n23時就寝 → 21〜22時に入浴\n24時就寝 → 22〜23時に入浴\n\nコツは「帰宅したらすぐ脱ぐ」。\n\n帰宅→着替え→入浴の順を\n「習慣のセット」にする。\n考えないで動ける設計が勝つ。\n\n↓続き（7/10）" + FIXED_TAGS,
    "今夜からの実装プロトコル。\n\nStep1：お湯を38〜40℃に設定\nStep2：タイマーを10分セット\nStep3：スマホを浴室に持ち込まない\nStep4：出たら照明を少し暗くする\n\n「全部やらなくていい」\n\nまずStep1だけでいい。\n温度を1つ変えるだけで、体は変わり始める。\n\n↓続き（8/10）" + FIXED_TAGS,
    "入れなかった日の翌朝にやること。\n\n→ 自己嫌悪に0秒使う\n→ 朝シャワーを3〜5分長めに浴びる\n→「今日、機会があれば入る」設定にする\n\n「絶対入る」じゃなくていい。\n「機会があれば」くらいが続く。\n\n8勝6敗でいい。\nそれで十分に前進している。\n\n↓続き（9/10）" + FIXED_TAGS,
    "「熱いほど効く」は誤解。\n\n43℃以上のお湯は交感神経を刺激しやすく、むしろ覚醒方向に動く人が多い。\n\n研究で使われているのは40〜42.5℃が中心。\n個人差があるため「気持ちよく入れる温度」が正解。\n\n「熱い＝すごい」じゃない。\n「適温＋継続」が勝つ設計。\n\n↓続き（10/10）" + FIXED_TAGS,
    "今夜やること、1つだけ。\n\n就寝の1〜2時間前に、\n38〜40℃の湯船に10〜15分。\n\n睡眠が変わると、翌日の食欲・集中・活力が変わる。\n体重より先に、朝の感覚が変わる。\n\nnoteで全文公開中\nhttps://note.com/mash_anti_metabo" + FIXED_TAGS,
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]
ACCENT_COLORS = ["#38bdf8", "#38bdf8", "#FF6D00", "#38bdf8", "#4ade80",
                 "#38bdf8", "#FF6D00", "#4ade80", "#38bdf8", "#FF6D00"]


def make_card(n, tweet, tag, accent):
    lines = tweet.split("\n")
    # Strip hashtag block from display (last 2 lines are \n\n#tags)
    display_lines = []
    for line in lines:
        if line.startswith("#") and "ダイエット" in line:
            break
        display_lines.append(line)

    text_html = ""
    y = 120
    for line in display_lines:
        if line.strip() == "":
            y += 18
            continue
        size = 26 if len(line) > 30 else 30
        weight = 700
        color = "#e2e8f0"
        if line.startswith("✅") or line.startswith("→"):
            color = "#4ade80"
        elif "↓続き" in line:
            color = "#555"
            size = 20
        text_html += (
            f"<div style='position:absolute;top:{y}px;left:56px;right:80px;"
            f"font-size:{size}px;font-weight:{weight};color:{color};line-height:1.5;'>{line}</div>"
        )
        y += size * 1.6

    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        f"<div style='position:absolute;top:0;left:0;width:6px;height:100%;background:{accent};'></div>"
        f"<div style='position:absolute;top:44px;left:56px;font-size:18px;font-weight:700;"
        f"color:{accent};letter-spacing:2px;'>{tag}</div>"
        f"<div class='num'>{n}/10</div>"
        + text_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        f"<p class='series' style='color:{accent};'>" + HASHTAG + "</p></body></html>"
    )


def card_01():
    items = [
        ("シャワーだけ", "全身が温まらない", "#ef4444"),
        ("体温変化なし", "眠気のスイッチが入らない", "#ef4444"),
        ("布団に入っても眠れない", "夜中に起きる・朝が重い", "#FF6D00"),
        ("原因は「疲れ」じゃない", "体温設計の問題だった", "#38bdf8"),
    ]
    items_html = ""
    for i, (label, desc, color) in enumerate(items):
        top = 150 + i * 120
        items_html += (
            f"<div style='position:absolute;top:{top}px;left:56px;right:56px;"
            "display:flex;align-items:center;gap:20px;'>"
            f"<div style='width:16px;height:16px;border-radius:50%;background:{color};flex-shrink:0;"
            f"box-shadow:0 0 12px {color}60;'></div>"
            "<div style='flex:1;background:#1e3a5f;border-radius:10px;padding:16px 24px;'>"
            f"<div style='font-size:22px;font-weight:700;color:{color};'>{label}</div>"
            f"<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>{desc}</div></div></div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>1/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>シャワーで眠れない夜の正体</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>「疲れ」じゃなく「体温設計」の問題。</div></div>"
        + items_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p></body></html>"
    )


def card_03():
    rules = [
        ("① 温度", "38〜40℃（ぬるめでOK）", "#38bdf8"),
        ("② 時間", "10〜15分浸かる", "#4ade80"),
        ("③ タイミング", "就寝1〜2時間前", "#FF6D00"),
    ]
    html = ""
    for i, (num, desc, color) in enumerate(rules):
        top = 180 + i * 160
        html += (
            f"<div style='position:absolute;top:{top}px;left:56px;right:56px;"
            "background:#1e3a5f;border-radius:12px;padding:24px 32px;"
            f"border-left:6px solid {color};'>"
            f"<div style='font-size:28px;font-weight:900;color:{color};'>{num}</div>"
            f"<div style='font-size:22px;font-weight:500;color:#e2e8f0;margin-top:8px;'>{desc}</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>3/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>睡眠を変えた「入浴3原則」</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>これだけ。今夜から試せる。</div></div>"
        + html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#FF6D00;'>" + HASHTAG + "</p></body></html>"
    )


def card_04():
    steps = [
        ("入浴", "38〜40℃で10〜15分", "#38bdf8"),
        ("体が温まる", "深部体温が上昇", "#FF6D00"),
        ("熱が逃げる", "お風呂を出たあと放熱", "#4ade80"),
        ("眠気が来る", "深部体温低下＝自然な眠気", "#38bdf8"),
    ]
    html = ""
    for i, (label, desc, color) in enumerate(steps):
        left = 40 + i * 300
        html += (
            f"<div style='position:absolute;top:200px;left:{left}px;width:260px;"
            "background:#1e3a5f;border-radius:12px;padding:20px;text-align:center;'>"
            f"<div style='font-size:24px;font-weight:900;color:{color};'>{label}</div>"
            f"<div style='font-size:14px;color:#9ca3af;margin-top:8px;'>{desc}</div>"
            "</div>"
        )
        if i < 3:
            arrow_left = left + 268
            html += (
                f"<div style='position:absolute;top:230px;left:{arrow_left}px;"
                "font-size:32px;color:#444;'>→</div>"
            )
    html += (
        "<div style='position:absolute;top:430px;left:56px;right:56px;"
        "background:#1a2a1a;border-radius:10px;padding:16px 24px;"
        "border:1px solid #4ade8040;'>"
        "<div style='font-size:18px;color:#4ade80;'>⏱ 完成まで約1〜2時間</div>"
        "<div style='font-size:15px;color:#9ca3af;margin-top:4px;'>直前入浴は逆効果。熱いまま布団に入ることになる。</div>"
        "</div>"
    )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>4/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>深部体温が下がると眠くなる仕組み</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>Haghayegh et al. Sleep Medicine Reviews 2019</div></div>"
        + html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p></body></html>"
    )


def render_cards():
    generators = [
        card_01,
        lambda: make_card(2, TWEETS[1], CARD_TAGS[1], ACCENT_COLORS[1]),
        card_03,
        card_04,
        lambda: make_card(5, TWEETS[4], CARD_TAGS[4], ACCENT_COLORS[4]),
        lambda: make_card(6, TWEETS[5], CARD_TAGS[5], ACCENT_COLORS[5]),
        lambda: make_card(7, TWEETS[6], CARD_TAGS[6], ACCENT_COLORS[6]),
        lambda: make_card(8, TWEETS[7], CARD_TAGS[7], ACCENT_COLORS[7]),
        lambda: make_card(9, TWEETS[8], CARD_TAGS[8], ACCENT_COLORS[8]),
        lambda: make_card(10, TWEETS[9], CARD_TAGS[9], ACCENT_COLORS[9]),
    ]

    print("第41回 X投稿カード生成開始...\n")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for i, gen in enumerate(generators, 1):
            html = gen()
            tmp = ARTICLE_DIR / f"_tmp_card_{i:02d}.html"
            tmp.write_text(html, encoding="utf-8")
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(f"file:///{tmp.as_posix()}")
            page.wait_for_timeout(500)
            out = OUTPUT_DIR / f"x_post_{i:02d}.png"
            page.screenshot(path=str(out), full_page=False)
            page.close()
            tmp.unlink(missing_ok=True)
            print(f"✅ x_post_{i:02d}.png")
        browser.close()
    print(f"\n保存先: {OUTPUT_DIR}")


if __name__ == "__main__":
    render_cards()
