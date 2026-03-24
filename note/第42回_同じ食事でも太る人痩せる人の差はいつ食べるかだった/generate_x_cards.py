#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第42回 X投稿用カード画像 10枚生成スクリプト（図解版）"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
HASHTAG = "#第42回 食べる時間と体の変化"
FIXED_TAGS = "\n\n#ダイエット #メタボ #習慣化 #食事管理 #血糖値 #健康診断"

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
    "同僚と同じ定食を食べた。\nカロリーも量も同じ。\n\nなのに、なぜか自分だけ太る。\n\n「体質の差かな」と思ってた。\n\n違った。\n差は「いつ食べたか」にあった。\n\n↓続き（2/10）" + FIXED_TAGS,
    "夜遅く食べると太る科学的理由。\n\n「BMAL1（ビーマルワン）」という体内時計遺伝子がある。\n\n夜10時〜深夜2時に活性化し、脂肪合成酵素が増える。\n\n同じカロリーでも、この時間帯に食べると脂肪になりやすい。\n\n↓続き（3/10）" + FIXED_TAGS,
    "食べる時間「3ルール」。\n\n① 夕食は就寝3〜4時間前に終える\n② 朝食は起床後1時間以内に食べる\n③ 22時以降は食べない\n\n食べる内容を変えなくていい。\n食べる時間を変えるだけ。\n\n↓続き（4/10）" + FIXED_TAGS,
    "なぜ「インスリン感受性」が昼夜で変わるのか。\n\n朝〜昼：感受性 高い → エネルギーになりやすい\n夜：感受性 低い → 脂肪として蓄積されやすい\n\n体が「夜は休む」と判断するから起こる自然な変化。\n\nSutton et al. Cell Metabolism 2018\n\n↓続き（5/10）" + FIXED_TAGS,
    "研究が示した「食べる時間」の数字。\n\nHatori et al. 2012（Cell Metabolism誌）\n同カロリーで8時間制限したマウスは\n\n✅ 体重が有意に低い\n✅ 体脂肪が少ない\n✅ 代謝疾患が少ない\n\n「何を食べるか」だけじゃなく「いつ食べるか」が代謝を変える。\n\n↓続き（6/10）" + FIXED_TAGS,
    "「遅くなりやすい」を防ぐ時間設計。\n\n23時就寝 → 19〜20時に食べ終える\n24時就寝 → 20〜21時に食べ終える\n\nコツは「帰宅したらすぐ着替えてすぐ食べる」。\n\n帰宅→着替え→食事を「習慣のセット」にする。\n考えないで動ける設計が勝つ。\n\n↓続き（7/10）" + FIXED_TAGS,
    "今夜からの実装プロトコル。\n\nStep1：今夜の夕食時間を30分早める\nStep2：22時以降は食べないルールを1つ設ける\nStep3：空腹なら水か温かい飲み物に変える\n\n「全部やらなくていい」\n\nまずStep1だけでいい。\n30分前倒しするだけで体は変わり始める。\n\n↓続き（8/10）" + FIXED_TAGS,
    "遅くなった日の翌朝にやること。\n\n→ 自己嫌悪に0秒使う\n→ 翌朝の朝食を少し軽めにする\n→ 昼食でしっかり食べる（インスリン感受性が高い）\n\n「絶対に遅く食べない」じゃなくていい。\n「翌日に補正できる」が続く。\n\n8勝6敗でいい。\n\n↓続き（9/10）" + FIXED_TAGS,
    "「朝食を抜けばいいんじゃ？」は誤解。\n\n朝食抜き→空腹強い→昼・夜に過食\n→体内時計が乱れやすい\n\n目指すのは「抜く」じゃなく「前にずらす」こと。\n\n食事を早めに終わらせて、翌朝しっかり食べる。\nこの循環が体内時計を整える。\n\n↓続き（10/10）" + FIXED_TAGS,
    "今夜やること、1つだけ。\n\n夕食を、いつもより30分だけ早く始める。\n\nそれだけ。\n\n食べる時間を変えると、同じ食事でも体への影響が変わる。\n翌朝の感覚が変わる。\n\nnoteで全文公開中\nhttps://note.com/mash_anti_metabo" + FIXED_TAGS,
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]
ACCENT_COLORS = ["#38bdf8", "#38bdf8", "#FF6D00", "#38bdf8", "#4ade80",
                 "#38bdf8", "#FF6D00", "#4ade80", "#38bdf8", "#FF6D00"]


def make_card(n, tweet, tag, accent):
    lines = tweet.split("\n")
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
        ("同じ定食・同じカロリー", "なのに自分だけ太る", "#ef4444"),
        ("体質の差？", "違った。時間の差だった", "#FF6D00"),
        ("BMAL1遺伝子", "夜10時〜深夜2時に脂肪合成↑", "#38bdf8"),
        ("食べる時間", "「いつ食べるか」が体を変える", "#4ade80"),
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
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>同じ食事でも太る人・痩せる人の差</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>体質じゃない。「いつ食べるか」の差だった。</div></div>"
        + items_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p></body></html>"
    )


def card_05():
    cols = [
        ("時間制限なし", "好きな時間に食べた", "#ef4444", "体重増加\n代謝疾患あり"),
        ("8時間制限", "食べる時間を絞った", "#4ade80", "体重低い\n代謝疾患なし"),
    ]
    cols_html = ""
    for i, (title, sub, color, result) in enumerate(cols):
        left = 80 + i * 560
        cols_html += (
            f"<div style='position:absolute;top:160px;left:{left}px;width:500px;"
            "background:#1e3a5f;border-radius:16px;padding:32px;text-align:center;'>"
            f"<div style='font-size:28px;font-weight:900;color:{color};'>{title}</div>"
            f"<div style='font-size:18px;color:#9ca3af;margin-top:12px;'>{sub}</div>"
            "<div style='margin-top:32px;padding:20px;background:#0d1b2a;border-radius:10px;'>"
            + "".join(
                f"<div style='font-size:22px;font-weight:700;color:{color};margin:8px 0;'>{r}</div>"
                for r in result.split("\n")
            ) +
            "</div></div>"
        )
    note_html = (
        "<div style='position:absolute;top:520px;left:80px;right:80px;"
        "background:#1a1a2a;border-radius:10px;padding:16px 24px;border:1px solid #38bdf840;'>"
        "<div style='font-size:18px;color:#38bdf8;'>"
        "同じカロリーで差が出た ＝ 「いつ食べるか」が代謝を変える</div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>"
        "Hatori et al. Cell Metabolism 2012</div>"
        "</div>"
    )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>5/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#4ade80;'>研究が示した「食べる時間」の差</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>同じカロリー・異なる食べる時間帯。8週間後の結果。</div></div>"
        + cols_html + note_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#4ade80;'>" + HASHTAG + "</p></body></html>"
    )


def render_cards():
    generators = [
        card_01,
        lambda: make_card(2, TWEETS[1], CARD_TAGS[1], ACCENT_COLORS[1]),
        lambda: make_card(3, TWEETS[2], CARD_TAGS[2], ACCENT_COLORS[2]),
        lambda: make_card(4, TWEETS[3], CARD_TAGS[3], ACCENT_COLORS[3]),
        card_05,
        lambda: make_card(6, TWEETS[5], CARD_TAGS[5], ACCENT_COLORS[5]),
        lambda: make_card(7, TWEETS[6], CARD_TAGS[6], ACCENT_COLORS[6]),
        lambda: make_card(8, TWEETS[7], CARD_TAGS[7], ACCENT_COLORS[7]),
        lambda: make_card(9, TWEETS[8], CARD_TAGS[8], ACCENT_COLORS[8]),
        lambda: make_card(10, TWEETS[9], CARD_TAGS[9], ACCENT_COLORS[9]),
    ]

    print("第42回 X投稿カード生成開始...\n")
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
