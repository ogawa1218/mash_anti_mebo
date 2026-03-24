#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第43回 X投稿用カード画像 10枚生成スクリプト（図解版）"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
HASHTAG = "#第43回 腸内細菌と長寿"

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
    "「腸活してるのに変わらない」\n\n毎日ヨーグルト食べてる。\nでも便秘は続くし、お腹は重い。\n\nそれ、やり方が半分しか合ってなかっただけです。\n\n「菌を入れる」だけじゃ足りない。\n「菌の餌」も一緒に入れないと定着しない。\n\n↓続き（2/10）\n\n#ダイエット #メタボ #習慣化 #不老長寿 #腸活 #健康診断",
    "なぜヨーグルトだけでは変わらないのか。\n\n腸内細菌は「競争」で生き残る。\n外から入った善玉菌は、餌がなければすぐに洗い流されてしまう。\n\n餌＝プレバイオティクス（食物繊維・オリゴ糖）\n\nヨーグルトにバナナかはちみつをプラスするだけで\n定着率が劇的に変わる。\n\n↓続き（3/10）\n\n#ダイエット #メタボ #習慣化 #不老長寿 #腸活",
    "今夜からできる腸活3ステップ。\n\n① 朝食：納豆＋玉ねぎ（300円・3分）\n② 主食：大麦2割混ぜ（食物繊維3〜4倍）\n③ 食後：15分ウォーキング\n\n全部やらなくていい。\n1つだけ選べばいい。\n\nそれで腸内細菌は動き始める。\n\n↓続き（4/10）\n\n#ダイエット #メタボ #腸活 #習慣化",
    "なぜ「大麦」が腸にいいのか。\n\n大麦にはβ-グルカンという水溶性食物繊維が豊富。\nこれが「酪酸産生菌」の大好物。\n\n酪酸産生菌→酪酸を産生→腸細胞のエネルギー源\n→腸管バリアが強化→慢性炎症が抑制される\n\n白米8割＋大麦2割に変えるだけ。\n\n↓続き（5/10）\n\n#ダイエット #メタボ #腸活 #習慣化",
    "100歳以上が全国平均2.8倍の地域がある。\n\n京都府京丹後市。大腸がん罹患率も半分以下。\n\nこの地域の長寿者の腸内細菌を調べたら\n酪酸産生菌が圧倒的に多かった。\n\n✅ 植物性食事中心\n✅ 食物繊維が豊富\n✅ 酪酸産生菌が多い\n\n（京丹後長寿コホート研究・内藤裕二氏 2015〜）\n\n↓続き（6/10）\n\n#ダイエット #メタボ #不老長寿 #腸活",
    "就寝時刻別・腸活タイムライン設計。\n\n23時就寝の場合：\n朝：納豆＋玉ねぎ → 善玉菌補給\n昼：大麦ご飯 → 酪酸産生菌の燃料補給\n夕：発酵食品（味噌汁）→ 多様性UP\n食後：15分歩く → 蠕動運動活発化\n\n食事を「腸への投資」と考えるとメニュー選びが変わる。\n\n↓続き（7/10）\n\n#ダイエット #メタボ #腸活 #習慣化",
    "今夜からの腸活実装プロトコル。\n\nStep1：白米に大麦2割を混ぜて炊く\nStep2：納豆を買いおきする（1週間分）\nStep3：玉ねぎをみじん切りにして納豆に混ぜる\nStep4：味噌は火を止めてから溶く\n\n「全部やらなくていい」\n\nまずStep1だけでいい。今夜から変えられる。\n\n↓続き（8/10）\n\n#ダイエット #メタボ #腸活 #習慣化",
    "腸活を忘れた翌朝にやること。\n\n→ 自己嫌悪に0秒使う\n→ 朝食に納豆を1つ食べる\n→ その日の夜、大麦ご飯に戻す\n\nそれだけ。\n\n8勝6敗でOK。\n週の6割できていれば腸内環境は整っていく。\n\n「完璧にやれなかった」じゃなく\n「翌朝また1つやった」が続く腸活の正解。\n\n↓続き（9/10）\n\n#ダイエット #メタボ #腸活 #習慣化",
    "100歳以上の高齢者の腸から\n「天然の抗生物質」が発見された。\n\nその名も「isoalloLCA産生菌」。\n\n胆汁酸を代謝して、病原菌を殺す\n強力な抗菌物質を自ら生成できる菌。\n\n腸内細菌は消化補助だけじゃない。\n体内で薬を作る「臓器」でもある。\n\n（Nature Digest 2022）\n\n↓続き（10/10）\n\n#ダイエット #メタボ #不老長寿 #腸活",
    "今夜やること、1つだけ。\n\n白米を炊くとき、大麦2割を混ぜる。\n\nそれだけ。\n\n腸内細菌が変わると、\n食欲が落ち着く。\n疲れにくくなる。\n10年後の老化速度が変わる。\n\nnoteで全文公開中\nhttps://note.com/mash_anti_metabo\n\n#ダイエット #メタボ #腸活 #不老長寿 #習慣化",
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]
ACCENT_COLORS = ["#38bdf8", "#38bdf8", "#FF6D00", "#38bdf8", "#4ade80",
                 "#38bdf8", "#FF6D00", "#4ade80", "#38bdf8", "#FF6D00"]


def render(html, fname):
    tmp = ARTICLE_DIR / "_tmp_xcard.html"
    out = OUTPUT_DIR / fname
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(f"file:///{tmp.as_posix()}")
        page.wait_for_timeout(800)
        page.screenshot(path=str(out), full_page=False)
        browser.close()
    tmp.unlink(missing_ok=True)


def card_01():
    """共感：タイムライン型（変わらない理由の可視化）"""
    items = [
        ("ヨーグルトだけ", "プロバイオティクスのみ", "#ef4444"),
        ("餌なし", "プレバイオティクス不足", "#ef4444"),
        ("菌が定着しない", "洗い流されてしまう", "#FF6D00"),
        ("変わらない腸活", "ループが続く", "#ef4444"),
    ]
    items_html = ""
    for i, (label, desc, color) in enumerate(items):
        top = 160 + i * 116
        items_html += (
            f"<div style='position:absolute;top:{top}px;left:56px;right:56px;"
            "display:flex;align-items:center;gap:20px;'>"
            f"<div style='width:16px;height:16px;border-radius:50%;background:{color};flex-shrink:0;"
            f"box-shadow:0 0 12px {color}60;'></div>"
            "<div style='flex:1;background:#1e3a5f;border-radius:10px;padding:14px 24px;'>"
            f"<div style='font-size:22px;font-weight:700;color:{color};'>{label}</div>"
            f"<div style='font-size:15px;color:#9ca3af;margin-top:4px;'>{desc}</div></div></div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>1/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>「腸活してるのに変わらない」の正体</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>菌を入れるだけでは足りない。餌とセットで初めて機能する。</div></div>"
        + items_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p></body></html>"
    )


def card_03():
    """解決策：横3列ステップカード"""
    steps = [
        ("Step 1", "納豆＋玉ねぎ", "300円・3分", "#4ade80"),
        ("Step 2", "大麦2割混ぜ", "食物繊維3〜4倍", "#38bdf8"),
        ("Step 3", "食後15分歩く", "腸内多様性UP", "#FF6D00"),
    ]
    html = ""
    for i, (num, title, sub, color) in enumerate(steps):
        left = 56 + i * 393
        html += (
            f"<div style='position:absolute;top:150px;left:{left}px;width:360px;height:360px;"
            "background:#1e3a5f;border-radius:16px;padding:28px;text-align:center;'>"
            f"<div style='font-size:20px;font-weight:700;color:{color};'>{num}</div>"
            f"<div style='font-size:30px;font-weight:900;color:#e2e8f0;margin-top:14px;'>{title}</div>"
            f"<div style='margin-top:16px;padding:6px 16px;background:{color}20;border-radius:20px;"
            "display:inline-block;'>"
            f"<span style='font-size:16px;font-weight:700;color:{color};'>{sub}</span></div>"
            f"<div style='position:absolute;bottom:0;left:0;width:100%;height:4px;"
            f"background:{color};border-radius:0 0 16px 16px;'></div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>3/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>今夜からできる腸活3ステップ</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>全部やらなくていい。1つだけ選べばいい。</div></div>"
        + html +
        "<div style='position:absolute;top:546px;left:56px;right:56px;"
        "background:#1a1a2a;border-radius:10px;padding:14px 24px;border:1px solid #FF6D0040;'>"
        "<div style='font-size:18px;color:#FF6D00;'>💡 まずStep 1「納豆＋玉ねぎ」から始めてみてください</div>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#FF6D00;'>" + HASHTAG + "</p></body></html>"
    )


def card_05():
    """効果：Before/After比較（一般的な人 vs 京丹後長寿者）"""
    cols = [
        ("一般的な人", "腸活なし・高脂質食事", "#ef4444",
         ["酪酸産生菌が少ない", "慢性炎症が進行", "老化が速い"]),
        ("京丹後の長寿者", "食物繊維豊富な植物食", "#4ade80",
         ["酪酸産生菌が豊富", "慢性炎症が抑制", "100歳超でも健康"]),
    ]
    cols_html = ""
    for i, (title, sub, color, points) in enumerate(cols):
        left = 56 + i * 592
        pts_html = "".join(
            f"<div style='font-size:18px;font-weight:700;color:{color};margin:10px 0;'>→ {p}</div>"
            for p in points
        )
        cols_html += (
            f"<div style='position:absolute;top:150px;left:{left}px;width:560px;"
            "background:#1e3a5f;border-radius:16px;padding:28px;'>"
            f"<div style='font-size:26px;font-weight:900;color:{color};'>{title}</div>"
            f"<div style='font-size:16px;color:#9ca3af;margin-top:8px;'>{sub}</div>"
            f"<div style='margin-top:24px;'>{pts_html}</div>"
            "</div>"
        )
    note_html = (
        "<div style='position:absolute;top:530px;left:56px;right:56px;"
        "background:#1a1a2a;border-radius:10px;padding:14px 24px;border:1px solid #4ade8040;'>"
        "<div style='font-size:16px;color:#4ade80;'>"
        "京丹後長寿コホート研究（京都府立医科大学・内藤裕二氏 2015年〜）"
        "</div></div>"
    )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>5/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#4ade80;'>100歳の腸 vs 現代の腸</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>腸内細菌の差が、老化速度の差になる。</div></div>"
        + cols_html + note_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#4ade80;'>" + HASHTAG + "</p></body></html>"
    )


def card_07():
    """実践：縦フロー型（腸活実装プロトコル）"""
    steps = [
        ("Step 1", "白米に大麦2割を混ぜて炊く", "#38bdf8"),
        ("Step 2", "納豆を週7パック買いおきする", "#38bdf8"),
        ("Step 3", "玉ねぎをみじん切りで納豆に混ぜる", "#4ade80"),
        ("Step 4", "味噌は火を止めてから溶く", "#FF6D00"),
    ]
    html = ""
    for i, (num, text, color) in enumerate(steps):
        top = 160 + i * 120
        html += (
            f"<div style='position:absolute;top:{top}px;left:56px;right:56px;"
            "background:#1e3a5f;border-radius:10px;padding:16px 24px;"
            f"border-left:6px solid {color};display:flex;align-items:center;gap:20px;'>"
            f"<div style='width:44px;height:44px;border-radius:50%;background:{color}20;"
            f"border:2px solid {color};display:flex;align-items:center;justify-content:center;"
            f"font-size:18px;font-weight:900;color:{color};flex-shrink:0;'>{i+1}</div>"
            "<div style='flex:1;'>"
            f"<div style='font-size:14px;font-weight:700;color:{color};'>{num}</div>"
            f"<div style='font-size:20px;font-weight:700;color:#e2e8f0;margin-top:4px;'>{text}</div>"
            "</div></div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>7/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>腸活実装プロトコル</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>まずStep 1だけでいい。今夜から変えられる。</div></div>"
        + html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#FF6D00;'>" + HASHTAG + "</p></body></html>"
    )


def card_09():
    """深掘り：データ可視化（ビフィズス菌の加齢変化グラフ）"""
    bars = [
        ("乳児", 95, "#4ade80"),
        ("20代", 50, "#38bdf8"),
        ("40代", 20, "#FF6D00"),
        ("60代",  5, "#ef4444"),
        ("長寿者", 45, "#4ade80"),
    ]
    bars_html = ""
    for i, (label, pct, color) in enumerate(bars):
        left = 100 + i * 230
        bar_h = int(pct * 3.2)
        bar_top = 420 - bar_h
        bars_html += (
            f"<div style='position:absolute;left:{left}px;top:{bar_top}px;"
            f"width:160px;height:{bar_h}px;background:{color}80;border-radius:6px 6px 0 0;"
            f"border-top:3px solid {color};'></div>"
            f"<div style='position:absolute;left:{left}px;top:430px;"
            "width:160px;text-align:center;'>"
            f"<div style='font-size:18px;font-weight:700;color:{color};'>{label}</div>"
            f"<div style='font-size:22px;font-weight:900;color:#e2e8f0;'>{pct}%</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>9/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>ビフィズス菌の加齢変化</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>"
        "乳児95%→60代5%。でも長寿者は取り戻していた。</div></div>"
        + bars_html +
        "<div style='position:absolute;top:130px;left:56px;width:2px;height:300px;"
        "background:#333;'></div>"
        "<div style='position:absolute;top:125px;left:64px;font-size:13px;color:#555;'>100%</div>"
        "<div style='position:absolute;top:218px;left:64px;font-size:13px;color:#555;'>50%</div>"
        "<div style='position:absolute;top:312px;left:64px;font-size:13px;color:#555;'>0%</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p></body></html>"
    )


def make_text_card(n, tweet, tag, accent):
    """テキスト主体のカード（2/4/6/8/10番用）"""
    lines = []
    for line in tweet.split("\n"):
        if line.startswith("#") and "ダイエット" in line:
            break
        lines.append(line)

    text_html = ""
    y = 120
    for line in lines:
        if line.strip() == "":
            y += 16
            continue
        size = 26 if len(line) > 28 else 30
        color = "#e2e8f0"
        if line.startswith("✅") or line.startswith("→"):
            color = "#4ade80"
        elif "↓続き" in line:
            color = "#555"
            size = 20
        elif line.startswith("（") and "）" in line:
            color = "#9ca3af"
            size = 18
        text_html += (
            f"<div style='position:absolute;top:{y}px;left:56px;right:80px;"
            f"font-size:{size}px;font-weight:700;color:{color};line-height:1.5;'>{line}</div>"
        )
        y += int(size * 1.6)

    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        f"<div style='position:absolute;top:0;left:0;width:6px;height:100%;background:{accent};'></div>"
        f"<div class='num'>{n}/10</div>"
        + text_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        f"<p class='series' style='color:{accent};'>" + HASHTAG + "</p></body></html>"
    )


CARD_FUNCS = [
    card_01,
    lambda: make_text_card(2,  TWEETS[1],  CARD_TAGS[1],  ACCENT_COLORS[1]),
    card_03,
    lambda: make_text_card(4,  TWEETS[3],  CARD_TAGS[3],  ACCENT_COLORS[3]),
    card_05,
    lambda: make_text_card(6,  TWEETS[5],  CARD_TAGS[5],  ACCENT_COLORS[5]),
    card_07,
    lambda: make_text_card(8,  TWEETS[7],  CARD_TAGS[7],  ACCENT_COLORS[7]),
    card_09,
    lambda: make_text_card(10, TWEETS[9],  CARD_TAGS[9],  ACCENT_COLORS[9]),
]


if __name__ == "__main__":
    print("第43回 X投稿カード画像（図解版）生成開始...\n")
    for i, func in enumerate(CARD_FUNCS):
        html = func()
        fname = f"x_post_{i+1:02d}.png"
        render(html, fname)
        print(f"✅ {fname}  [{CARD_TAGS[i]}]")
    print(f"\n全10枚完了。保存先: {OUTPUT_DIR}")
