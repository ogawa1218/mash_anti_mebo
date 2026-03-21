#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 X投稿用カード画像 10枚生成スクリプト（図解版）
各カードがテキストだけでなく、視覚的な図解・構造を持つデザイン。
タグピル（共感・原因等）は入れない。
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
HASHTAG = "#第 朝リセット"

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;background:#0d1b2a;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
    ".num{position:absolute;top:44px;right:56px;font-size:22px;font-weight:700;color:#444;}"
    ".author{position:absolute;bottom:22px;left:56px;font-size:18px;font-weight:400;color:#3a3a3a;}"
    ".series{position:absolute;bottom:22px;right:56px;font-size:18px;font-weight:700;}"
    ".title{position:absolute;left:56px;top:96px;font-size:36px;font-weight:900;color:#fff;"
    "letter-spacing:-1px;}"
)

TWEETS = [
    """100kgだった頃の朝。
缶コーヒー＋菓子パン2個。
「朝食は食べてる。偉い」と思ってた。

でも11時にはチョコが空。
昼は牛丼大盛りを5分で流し込む。
夜は「今日くらいいいか」。

翌朝、体重計で自己嫌悪。
原因は夜じゃなかった。朝だった。

↓続き（2/10）""",

    """菓子パン＋缶コーヒーの朝食。
糖質だけが一気に入る。

血糖値が急上昇→急降下。
この急降下が11時の「甘いもの欲しい」の正体。

夕方には判断力がゼロ。
コンビニに吸い込まれる。

夜の崩れは、朝で仕込まれていた。

↓続き（3/10）""",

    """朝食を変えて夜の食欲が減った方法。

① 最初の3口をたんぱく質にする
② 菓子パンを禁止せず2点セット化
③ 朝食を3パターン固定する

菓子パンを捨てなくていい。
足すだけ。
我慢ゼロ。設計だけ。

↓続き（4/10）""",

    """なぜ朝の3口で夜まで変わるのか。

①セカンドミール効果（Wolever, 1991）
朝に低GI食を摂ると昼食後の血糖値まで穏やかになる。

②朝のたんぱく質→夜の食欲ホルモン低下（Leidy, 2013）
朝のたんぱく質で夜のグレリンが有意に低下。

朝の3口が12時間後に効く。

↓続き（5/10）""",

    """朝食を変えて起きたこと：

❌ BEFORE
・11時にチョコ→空
・15時にお菓子 週5
・夜は毎日崩壊

✅ AFTER
・11時の空腹が12時半まで持つ
・15時のお菓子 週5→週2
・夜の崩壊が激減

チョコ代だけで月3,000円の節約。

↓続き（6/10）""",

    """STEP 2｜菓子パンを禁止しない。

菓子パンだけ → 菓子パン＋ゆで卵
おにぎりだけ → おにぎり＋味噌汁＋卵
トーストだけ → トースト＋チーズ＋ゆで卵

量は変えない。足すだけ。
「禁止で止める」は3日で終わる。
「足して変える」は3ヶ月続く。

↓続き（7/10）""",

    """STEP 3｜朝食を3パターンに固定する。

A（最短2分）：ゆで卵2個＋バナナ半分＋コーヒー
B（和風5分）：納豆ごはん小＋味噌汁＋海苔
C（コンビニ）：ゆで卵＋ヨーグルト＋おにぎり

前日の夜に「明日はA」と決めるだけ。
迷いがゼロになると判断力が夜まで持つ。

↓続き（8/10）""",

    """それでも朝が崩れる日はある。
僕も月3〜4回は菓子パン単独になる。

崩れた朝のルール：
① 責めない
② 昼の最初の1口を主菜にする
③ 15時にナッツ＋コーヒー

朝が崩れても昼でリセット完了。
8勝6敗でOK。

↓続き（9/10）""",

    """セカンドミール効果の面白い点。

朝食は「朝だけに効く」んじゃない。
昼・夕方・夜まで連鎖的に影響する。

朝に糖質単独で乱高下させると、
その波が1日中続く。

逆に朝でゆるやかにスタートすれば、
1日を通して食欲が安定しやすくなる。

↓続き（10/10）""",

    """【まとめ｜朝リセット3ステップ】

✅ 最初の3口をたんぱく質に
✅ 菓子パンを禁止せず足すだけ
✅ 朝食を3パターン固定

今夜やること1つだけ：
→ ゆで卵を2個、茹でてください

あなたは意志が弱いんじゃない。
朝の設計を変えるだけで夜が変わる。

詳しくはnoteに書きました👇
https://note.com/mash_anti_metabo""",
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]


# ═══════════════════════════════════════════════════
# カード1：共感（朝→夜タイムライン）
# ═══════════════════════════════════════════════════
def card_01():
    accent = "#38bdf8"
    events = [
        ("7:00", "菓子パン2個＋缶コーヒー", "#f59e0b"),
        ("11:00", "デスクのチョコが空に", "#ef4444"),
        ("12:00", "牛丼大盛り5分で完食", "#ef4444"),
        ("15:00", "また甘いもの", "#ef4444"),
        ("19:00", "判断力ゼロ→ドカ食い", "#ef4444"),
    ]
    items = ""
    for time, text, col in events:
        items += (
            "<div style='display:flex;align-items:center;margin-bottom:14px;'>"
            "<div style='min-width:80px;height:48px;background:" + col + ";border-radius:10px;"
            "display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;color:#000;'>" + time + "</div>"
            "<div style='width:4px;height:40px;background:" + col + ";border-radius:2px;margin:0 16px;'></div>"
            "<div style='font-size:24px;font-weight:600;color:#d1d5db;'>" + text + "</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>1/10</div>"
        "<div class='title'>100kgだった頃の1日。崩れは朝から始まっていた</div>"
        "<div style='position:absolute;left:56px;top:152px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:76px;right:56px;padding:16px 24px;"
        "background:rgba(239,68,68,.12);border-left:4px solid #ef4444;border-radius:0 8px 8px 0;'>"
        "<span style='font-size:26px;font-weight:800;color:#ef4444;'>「朝食は食べてるから偉い」と思っていた。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:12px;'>原因は夜じゃなかった</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード2：原因（血糖値フロー図）
# ═══════════════════════════════════════════════════
def card_02():
    accent = "#38bdf8"
    steps = [
        ("① 菓子パン＋缶コーヒー", "#f59e0b"),
        ("② 血糖値が急上昇", "#ef4444"),
        ("③ 急降下→強い空腹", "#ef4444"),
        ("④ 11時にチョコ→昼に早食い", "#ef4444"),
        ("⑤ 夕方判断力ゼロ→夜崩壊", "#ef4444"),
    ]
    items = ""
    for i, (text, col) in enumerate(steps):
        items += (
            "<div style='display:flex;align-items:center;margin-bottom:6px;'>"
            "<div style='background:#1e3a5f;border:2px solid " + col + ";border-radius:10px;"
            "padding:10px 20px;font-size:24px;font-weight:700;color:#fff;flex:1;'>" + text + "</div></div>"
        )
        if i < len(steps) - 1:
            items += "<div style='text-align:center;font-size:28px;color:" + col + ";margin:2px 0 2px 40px;'>↓</div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>2/10</div>"
        "<div class='title'>夜に崩れる原因は「朝の設計ミス」だった</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:66px;display:flex;align-items:center;gap:12px;'>"
        "<div style='font-size:22px;color:#4ade80;font-weight:700;'>✅ 解決：</div>"
        "<div style='font-size:20px;color:#9ca3af;'>朝の最初の3口を変えるだけで連鎖が止まる</div>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード3：解決策（横3列ステップ）
# ═══════════════════════════════════════════════════
def card_03():
    accent = "#FF6D00"
    cards_data = [
        ("STEP 1", "最初の3口を\nたんぱく質に", "午前の食欲を安定", "#FF6D00", "ゆで卵・納豆"),
        ("STEP 2", "菓子パンを\n2点セット化", "禁止より組み合わせ", "#38bdf8", "＋ゆで卵で足す"),
        ("STEP 3", "朝食を\n3パターン固定", "迷いゼロ＝判断力温存", "#4ade80", "前日の夜に決める"),
    ]
    html_cards = ""
    for i, (step, title, sub, col, ex) in enumerate(cards_data):
        title_html = title.replace("\n", "<br>")
        html_cards += (
            "<div style='flex:1;background:#111d2e;border:2px solid " + col + ";"
            "border-radius:14px;padding:24px 20px;text-align:center;'>"
            "<div style='font-size:20px;font-weight:800;color:" + col + ";margin-bottom:8px;'>" + step + "</div>"
            "<div style='font-size:28px;font-weight:900;color:#fff;margin-bottom:6px;line-height:1.3;'>" + title_html + "</div>"
            "<div style='font-size:18px;color:" + col + ";margin-bottom:12px;'>" + sub + "</div>"
            "<div style='font-size:16px;color:#666;'>" + ex + "</div>"
            "</div>"
        )
        if i < 2:
            html_cards += "<div style='display:flex;align-items:center;font-size:36px;color:#fff;padding:0 8px;'>→</div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>3/10</div>"
        "<div class='title'>朝の最初の3口を変えるだけ。我慢ゼロ</div>"
        "<div style='position:absolute;left:40px;top:160px;right:40px;display:flex;align-items:stretch;'>"
        + html_cards + "</div>"
        "<div style='position:absolute;left:56px;bottom:76px;'>"
        "<span style='font-size:24px;font-weight:700;color:#FF6D00;'>菓子パンを捨てなくていい。足すだけ。</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード4：仕組み（科学的根拠カード）
# ═══════════════════════════════════════════════════
def card_04():
    accent = "#38bdf8"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>4/10</div>"
        "<div class='title'>なぜ朝の3口で夜まで変わるのか</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>"
        "<div style='background:#111d2e;border:2px solid #38bdf8;border-radius:14px;padding:22px;margin-bottom:16px;'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>"
        "<div style='background:#38bdf8;color:#000;font-size:14px;font-weight:800;padding:4px 12px;border-radius:6px;'>根拠①</div>"
        "<div style='font-size:18px;color:#38bdf8;font-weight:700;'>セカンドミール効果</div></div>"
        "<div style='font-size:22px;color:#fff;font-weight:700;margin-bottom:4px;'>朝の低GI食が昼食後の血糖値まで穏やかにする</div>"
        "<div style='font-size:16px;color:#9ca3af;'>Wolever TM et al., Am J Clin Nutr, 1991</div>"
        "</div>"
        "<div style='background:#111d2e;border:2px solid #4ade80;border-radius:14px;padding:22px;'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>"
        "<div style='background:#4ade80;color:#000;font-size:14px;font-weight:800;padding:4px 12px;border-radius:6px;'>根拠②</div>"
        "<div style='font-size:18px;color:#4ade80;font-weight:700;'>朝たんぱく質→夜グレリン低下</div></div>"
        "<div style='font-size:22px;color:#fff;font-weight:700;margin-bottom:4px;'>朝のたんぱく質で夜の空腹ホルモンが有意に低下</div>"
        "<div style='font-size:16px;color:#9ca3af;'>Leidy HJ et al., Am J Clin Nutr, 2013</div>"
        "</div>"
        "</div>"
        "<div style='position:absolute;left:56px;bottom:70px;'>"
        "<span style='font-size:22px;font-weight:700;color:#FF6D00;'>朝の3口が、12時間後の夜食欲求に影響する</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード5：効果（Before/After比較）
# ═══════════════════════════════════════════════════
def card_05():
    accent = "#4ade80"
    before = ["11時にチョコが空", "15時のお菓子 週5", "夜は毎日崩壊", "チョコ代 月3,000円"]
    after = ["11時の空腹→12時半まで持つ", "15時のお菓子 週2に", "夜の崩壊が激減", "チョコ代ほぼゼロ"]
    left = ""
    for b in before:
        left += "<div style='display:flex;align-items:center;margin-bottom:12px;'><span style='color:#ef4444;font-size:22px;margin-right:8px;'>✗</span><span style='font-size:22px;color:#fca5a5;'>" + b + "</span></div>"
    right = ""
    for a in after:
        right += "<div style='display:flex;align-items:center;margin-bottom:12px;'><span style='color:#4ade80;font-size:22px;margin-right:8px;'>✓</span><span style='font-size:22px;color:#86efac;'>" + a + "</span></div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>5/10</div>"
        "<div class='title'>朝の最初の3口を変えて起きた変化</div>"
        "<div style='position:absolute;left:40px;top:152px;right:40px;display:flex;gap:24px;'>"
        "<div style='flex:1;background:rgba(239,68,68,.08);border:2px solid rgba(239,68,68,.3);"
        "border-radius:14px;padding:24px;'>"
        "<div style='font-size:24px;font-weight:800;color:#ef4444;margin-bottom:16px;text-align:center;'>❌ BEFORE</div>"
        + left + "</div>"
        "<div style='flex:1;background:rgba(74,222,128,.08);border:2px solid rgba(74,222,128,.3);"
        "border-radius:14px;padding:24px;'>"
        "<div style='font-size:24px;font-weight:800;color:#4ade80;margin-bottom:16px;text-align:center;'>✅ AFTER</div>"
        + right + "</div></div>"
        "<div style='position:absolute;left:56px;bottom:72px;display:flex;align-items:baseline;gap:16px;'>"
        "<span style='font-size:44px;font-weight:900;color:#FF6D00;'>たった3口</span>"
        "<span style='font-size:20px;color:#9ca3af;'>ゆで卵1個から始めた</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード6：設計（2点セット化テーブル）
# ═══════════════════════════════════════════════════
def card_06():
    accent = "#38bdf8"
    rows = [
        ("菓子パンだけ", "菓子パン＋ゆで卵"),
        ("おにぎりだけ", "おにぎり＋味噌汁＋卵"),
        ("トーストだけ", "トースト＋チーズ＋ゆで卵"),
        ("何も食べない", "無糖ヨーグルト＋バナナ半分"),
    ]
    header = (
        "<div style='display:flex;background:#1e3a5f;border-radius:10px 10px 0 0;padding:14px 16px;'>"
        "<div style='flex:1;font-size:22px;font-weight:800;color:#ef4444;'>❌ BEFORE（単独）</div>"
        "<div style='flex:1;font-size:22px;font-weight:800;color:#4ade80;'>✅ AFTER（2点セット）</div>"
        "</div>"
    )
    body = ""
    for i, (bef, aft) in enumerate(rows):
        bg = "#111d2e" if i % 2 == 0 else "#0d1b2a"
        body += (
            "<div style='display:flex;background:" + bg + ";padding:16px;"
            "border-bottom:1px solid #1e3a5f;'>"
            "<div style='flex:1;font-size:22px;color:#fca5a5;'>" + bef + "</div>"
            "<div style='flex:1;font-size:22px;color:#86efac;font-weight:600;'>" + aft + "</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>6/10</div>"
        "<div class='title'>STEP 2｜菓子パンを禁止しない。足すだけ</div>"
        "<div style='position:absolute;left:40px;top:148px;right:40px;"
        "border:2px solid #1e3a5f;border-radius:12px;overflow:hidden;'>"
        + header + body + "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;'>"
        "<span style='font-size:24px;color:#FF6D00;font-weight:700;'>「禁止で止める」は3日で終わる。</span>"
        "<span style='font-size:20px;color:#9ca3af;'>「足して変える」は3ヶ月続く</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード7：実践（朝食3パターン縦フロー）
# ═══════════════════════════════════════════════════
def card_07():
    accent = "#FF6D00"
    patterns = [
        ("A", "最短2分", "ゆで卵2個＋バナナ半分＋コーヒー", "#FF6D00"),
        ("B", "和風5分", "納豆ごはん小＋味噌汁＋海苔", "#38bdf8"),
        ("C", "コンビニ", "ゆで卵＋ヨーグルト＋おにぎり1個", "#4ade80"),
    ]
    items = ""
    for label, time, detail, col in patterns:
        items += (
            "<div style='display:flex;align-items:center;gap:16px;margin-bottom:16px;'>"
            "<div style='min-width:64px;height:64px;background:" + col + ";border-radius:14px;"
            "display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900;color:#000;'>" + label + "</div>"
            "<div style='flex:1;background:#111d2e;border:2px solid " + col + ";border-radius:12px;padding:18px 20px;'>"
            "<div style='font-size:18px;color:" + col + ";font-weight:700;margin-bottom:4px;'>" + time + "</div>"
            "<div style='font-size:24px;font-weight:800;color:#fff;'>" + detail + "</div>"
            "</div></div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>7/10</div>"
        "<div class='title'>STEP 3｜朝食を3パターン固定して迷いを消す</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;'>"
        "<span style='font-size:24px;font-weight:700;color:#FF6D00;'>前日の夜に「明日はA」と決めるだけ。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:8px;'>迷いゼロ＝判断力が夜まで持つ</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード8：復帰（リカバリーフロー）
# ═══════════════════════════════════════════════════
def card_08():
    accent = "#4ade80"
    steps = [
        ("菓子パン単独の朝…", "出張・締め切り・バタバタした日", "#ef4444", "#1a0a0a"),
        ("❌ やらないこと", "自分を責める＝血糖値は下がらない", "#ef4444", "#111d2e"),
        ("✅ 昼の最初の1口を主菜に", "焼き魚・鶏・卵。ここでリセット開始", "#38bdf8", "#111d2e"),
        ("✅ 15時にナッツ＋コーヒー", "間食設計（第11回）と連動でリセット完了", "#4ade80", "#111d2e"),
    ]
    items = ""
    for i, (title, sub, col, bg) in enumerate(steps):
        items += (
            "<div style='background:" + bg + ";border-left:4px solid " + col + ";"
            "border-radius:0 10px 10px 0;padding:14px 20px;margin-bottom:8px;'>"
            "<div style='font-size:24px;font-weight:800;color:" + col + ";'>" + title + "</div>"
            "<div style='font-size:17px;color:#9ca3af;margin-top:3px;'>" + sub + "</div>"
            "</div>"
        )
        if i < len(steps) - 1:
            items += "<div style='text-align:left;margin-left:20px;font-size:20px;color:#555;'>↓</div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>8/10</div>"
        "<div class='title'>崩れた朝のリカバリー手順</div>"
        "<div style='position:absolute;left:56px;top:140px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:68px;'>"
        "<span style='font-size:32px;font-weight:900;color:#FF6D00;'>8勝6敗でOK。昼の1口でリセット完了。</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード9：深掘り（セカンドミール効果の波形イメージ）
# ═══════════════════════════════════════════════════
def card_09():
    accent = "#38bdf8"
    bars_ng = [
        ("朝", "95", "#ef4444"),
        ("10時", "30", "#ef4444"),
        ("昼後", "90", "#ef4444"),
        ("15時", "25", "#ef4444"),
        ("夕方", "20", "#ef4444"),
    ]
    bars_ok = [
        ("朝", "60", "#4ade80"),
        ("10時", "55", "#4ade80"),
        ("昼後", "65", "#4ade80"),
        ("15時", "50", "#38bdf8"),
        ("夕方", "45", "#38bdf8"),
    ]

    def make_bars(bars, label, col, left):
        bar_html = ""
        for t, h, c in bars:
            bar_html += (
                "<div style='display:flex;flex-direction:column;align-items:center;flex:1;'>"
                "<div style='width:40px;height:" + str(int(h) * 2) + "px;background:" + c + ";"
                "border-radius:6px 6px 0 0;'></div>"
                "<div style='font-size:14px;color:#9ca3af;margin-top:6px;'>" + t + "</div>"
                "</div>"
            )
        return (
            "<div style='position:absolute;left:" + left + ";top:148px;width:560px;'>"
            "<div style='font-size:20px;font-weight:800;color:" + col + ";margin-bottom:12px;text-align:center;'>" + label + "</div>"
            "<div style='font-size:14px;color:#666;margin-bottom:8px;text-align:center;'>血糖値イメージ（高↑ 低↓）</div>"
            "<div style='display:flex;align-items:flex-end;height:200px;gap:8px;padding:0 20px;'>"
            + bar_html + "</div></div>"
        )

    ng = make_bars(bars_ng, "❌ 糖質単独（乱高下）", "#ef4444", "40px")
    ok = make_bars(bars_ok, "✅ たんぱく質ファースト（安定）", "#4ade80", "680px")

    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>9/10</div>"
        "<div class='title'>セカンドミール効果｜朝が昼・夜まで影響する</div>"
        + ng + ok +
        "<div style='position:absolute;left:56px;bottom:70px;background:#111d2e;"
        "border:2px solid #38bdf8;border-radius:10px;padding:14px 24px;'>"
        "<span style='font-size:20px;font-weight:800;color:#38bdf8;'>朝でゆるやかにスタート →</span>"
        "<span style='font-size:20px;color:#fff;margin-left:8px;'>1日を通して食欲が安定しやすくなる</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード10：CTA（チェックリスト＋CTAボックス）
# ═══════════════════════════════════════════════════
def card_10():
    accent = "#FF6D00"
    checks = [
        ("最初の3口をたんぱく質に", "ゆで卵・納豆・ヨーグルト", "#FF6D00"),
        ("菓子パンを禁止せず足すだけ", "単独→2点セット化", "#38bdf8"),
        ("朝食を3パターン固定", "前日の夜に決めるだけ", "#4ade80"),
    ]
    items = ""
    for title, desc, col in checks:
        items += (
            "<div style='display:flex;align-items:flex-start;margin-bottom:16px;gap:14px;'>"
            "<div style='min-width:36px;height:36px;background:" + col + ";border-radius:8px;"
            "display:flex;align-items:center;justify-content:center;font-size:20px;color:#000;font-weight:900;'>✓</div>"
            "<div>"
            "<div style='font-size:22px;font-weight:800;color:" + col + ";'>" + title + "</div>"
            "<div style='font-size:20px;color:#d1d5db;margin-top:4px;'>" + desc + "</div>"
            "</div></div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>10/10</div>"
        "<div class='title'>朝リセット3ステップ｜まとめ</div>"
        "<div style='position:absolute;left:56px;top:152px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:40px;bottom:76px;right:40px;"
        "background:linear-gradient(135deg,rgba(255,109,0,.15),rgba(255,109,0,.05));"
        "border:2px solid #FF6D00;border-radius:14px;padding:20px 28px;"
        "display:flex;align-items:center;justify-content:space-between;'>"
        "<div>"
        "<div style='font-size:28px;font-weight:900;color:#FF6D00;'>今夜やること1つだけ。</div>"
        "<div style='font-size:18px;color:#9ca3af;margin-top:4px;'>ゆで卵を2個、茹でてください。</div>"
        "</div>"
        "<div style='font-size:16px;color:#FF6D00;font-weight:700;white-space:nowrap;'>noteで詳細 →</div>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


CARD_FUNCS = [card_01, card_02, card_03, card_04, card_05,
              card_06, card_07, card_08, card_09, card_10]


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


def save_tweets():
    out = OUTPUT_DIR / "x_posts.md"
    lines = ["# 第 X投稿スレッド（10本）\n\n"]
    for i, tweet in enumerate(TWEETS):
        tag = CARD_TAGS[i]
        lines.append(
            "## 投稿" + str(i+1) + "/10｜" + tag + "\n\n```\n" + tweet.strip() + "\n```\n\n"
            "![カード" + str(i+1) + "](x_post_" + str(i+1).zfill(2) + ".png)\n\n---\n\n"
        )
    out.write_text("".join(lines), encoding="utf-8")
    print("✅ X投稿テキスト保存: " + out.name)


if __name__ == "__main__":
    print("第 X投稿カード画像（図解版）生成開始...\n")
    for i, func in enumerate(CARD_FUNCS):
        html = func()
        fname = "x_post_" + str(i+1).zfill(2) + ".png"
        render(html, fname)
        print("✅ " + fname + "  [" + CARD_TAGS[i] + "]")
    save_tweets()
    print("\n全10枚完了。保存先: " + str(OUTPUT_DIR))

