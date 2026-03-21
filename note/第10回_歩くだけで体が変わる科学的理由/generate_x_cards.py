#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 X投稿用カード画像 10枚生成スクリプト（図解版）
各カードがテキストだけでなく、視覚的な図解・構造を持つデザイン。
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
HASHTAG = "#第 歩くだけで変わる"
FIXED_TAGS = "\n\n#ダイエット #メタボ #習慣化 #ウォーキング #運動習慣"

# ── 共通CSS ──────────────────────────────────────
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

# ── ツイートデータ ──────────────────────────────────
TWEETS = [
    """駅の階段を見て、ため息をつく。
「また今日もエスカレーターか」

100kgだった頃、2階に上がるだけで息が切れてた。
1日の歩数は2,000歩以下。
ジムの体験に行っても場違いで1回でやめた。

変われたのはジムに通えたからじゃない。
帰り道に15分歩いただけです。

↓続き（2/10）""",

    """運動ゼロから抜け出せない悪循環。

①運動しなきゃと思う
②ジムを検討→面倒で断念
③罪悪感でストレス食い
④体重が増えてさらに動けない
⑤自己嫌悪…

このループ、意志の問題じゃなかった。
「ジムしかない」という思い込みが原因でした。

↓続き（3/10）""",

    """歩くだけで体は変わる。

Lancet Public Health 2022年の大規模研究で判明：
+2,000歩/日で心血管死亡リスク約11%減。

時間にして約15〜20分。
ジムも走りもプロテインもいらない。
「歩くだけ」が科学的に最もラクで効く運動でした。

↓続き（4/10）""",

    """食後に10分歩くだけで血糖値が変わる。

Sports Medicine 2022年の研究：
食後2〜5分の軽い歩行で血糖値スパイクが有意に抑制。

つまり食後に10分歩けば：
・午後の眠気↓
・間食欲求↓
・脂肪蓄積↓

一石三鳥。散歩レベルでOKです。

↓続き（5/10）""",

    """食後ウォークで僕に起きた変化。

・15時のお菓子が週5→週2に
・午後の会議で眠くならなくなった
・夕方の空腹感が激減
・帰宅後のドカ食いが減った

やったことは昼食後にオフィスの周り1周。
10分もかからない。我慢じゃなく衝動が消えた。

↓続き（6/10）""",

    """1駅手前ウォークが最強な3つの理由。

①判断がいらない
→帰宅ルートに組み込むだけ

②時間が固定される
→「いつ歩くか」を迷わない

③達成感が自動で得られる
→家に着いた＝完了

週3回で月14,400歩追加。3ヶ月で1.5kg分の脂肪。

↓続き（7/10）""",

    """今日から始める+1,500歩の足し方。

食後10分ウォーク → 約1,000歩
1駅手前 → 約1,200歩
1つ先のコンビニ → 約300歩

どれか1つか2つでOK。
僕は2,000歩→3,500歩→5,000歩→8,000歩と増えた。
最初の目標はたった+1,500歩でした。

↓続き（8/10）""",

    """歩けない日は、普通にある。

雨の日。飲み会の日。疲れた日。
僕も週7日歩いてるわけじゃない。

週4日歩けたら十分。
8勝6敗でOK。

崩れたら翌日また歩くだけ。
100kgから68kgになれたのは
崩れるたびに翌日歩き始めたから。

↓続き（9/10）""",

    """歩数と健康の関係を数字で見る。

+2,000歩/日 → 心血管死亡リスク11%減
+4,000歩/日 → 全死亡リスク有意に低下
食後5分歩行 → 血糖値スパイク抑制

出典：
Paluch et al., Lancet Public Health 2022
Buffey et al., Sports Medicine 2022

↓続き（10/10）""",

    """【まとめ｜歩くだけで体が変わる3ステップ】

✅ 食後10分ウォーク → 血糖値安定・間食欲求↓
✅ 1駅手前を週3回 → 判断不要・達成感自動
✅ 今より+1,500歩 → スマホで現状確認→目標設定

今日、昼食後に10分だけ歩いてみてください。
歩くだけで、体は変わります。

詳しくはnoteに書きました👇
https://note.com/mash_anti_metabo""",
]


# ═══════════════════════════════════════════════════
# カード1：共感（タイムライン型）
# ═══════════════════════════════════════════════════
def card_01():
    accent = "#38bdf8"
    steps = [
        ("7:30", "駅の階段を見てため息", "#ef4444"),
        ("7:31", "エスカレーターに並ぶ", "#ef4444"),
        ("12:30", "昼食後すぐデスクに戻る", "#f59e0b"),
        ("15:00", "お菓子に手が伸びる", "#ef4444"),
        ("19:00", "帰宅→ソファで動かない", "#ef4444"),
        ("23:00", "「明日こそ運動しよう」", "#ef4444"),
    ]
    items = ""
    for time, text, col in steps:
        items += (
            "<div style='display:flex;align-items:center;margin-bottom:12px;'>"
            "<div style='width:80px;font-size:22px;font-weight:800;color:" + col + ";'>" + time + "</div>"
            "<div style='width:4px;height:36px;background:" + col + ";border-radius:2px;margin:0 16px;'></div>"
            "<div style='font-size:24px;font-weight:600;color:#d1d5db;'>" + text + "</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>1/10</div>"
        "<div class='title'>運動ゼロだった100kgの1日</div>"
        "<div style='position:absolute;left:56px;top:152px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:80px;right:56px;padding:18px 24px;"
        "background:rgba(239,68,68,.12);border-left:4px solid #ef4444;border-radius:0 8px 8px 0;'>"
        "<span style='font-size:26px;font-weight:800;color:#ef4444;'>1日2,000歩以下。</span>"
        "<span style='font-size:22px;color:#9ca3af;margin-left:12px;'>変われたのはジムじゃなく「歩いた」から</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード2：原因フロー図（循環ループ）
# ═══════════════════════════════════════════════════
def card_02():
    accent = "#38bdf8"
    steps = [
        ("① 運動しなきゃと思う", "#1e3a5f"),
        ("② ジムを検討→面倒で断念", "#1e3a5f"),
        ("③ 罪悪感でストレス食い", "#1e3a5f"),
        ("④ 体重が増えてさらに動けない", "#1e3a5f"),
        ("⑤ 自己嫌悪→「俺には無理」", "#1e3a5f"),
    ]
    items = ""
    for i, (text, bg) in enumerate(steps):
        items += (
            "<div style='display:flex;align-items:center;margin-bottom:6px;'>"
            "<div style='background:" + bg + ";border:2px solid #ef4444;border-radius:10px;"
            "padding:10px 20px;font-size:24px;font-weight:700;color:#fff;flex:1;'>" + text + "</div>"
        )
        if i < len(steps) - 1:
            items += "</div><div style='text-align:center;font-size:28px;color:#ef4444;margin:2px 0 2px 40px;'>↓</div>"
        else:
            items += "</div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>2/10</div>"
        "<div class='title'>運動ゼロの悪循環ループ</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:66px;display:flex;align-items:center;gap:12px;'>"
        "<div style='font-size:38px;'>🔄</div>"
        "<div style='font-size:22px;color:#ef4444;font-weight:700;'>「ジムしかない」という思い込みが原因</div>"
        "<div style='font-size:20px;color:#9ca3af;'>→ 歩くだけでループは切れる</div>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード3：解決策 3ステップカード（横3列）
# ═══════════════════════════════════════════════════
def card_03():
    accent = "#FF6D00"
    cards_data = [
        ("STEP 1", "食後10分\nウォーク", "血糖値スパイク抑制", "#FF6D00", "昼食後に散歩するだけ"),
        ("STEP 2", "1駅手前\n週3回", "帰宅ルートに組込み", "#38bdf8", "判断不要・達成感自動"),
        ("STEP 3", "今より\n+1,500歩", "歩数計で可視化", "#4ade80", "スマホで現状確認"),
    ]
    cards_html = ""
    for i, (step, title, sub, col, ex) in enumerate(cards_data):
        title_html = title.replace("\n", "<br>")
        cards_html += (
            "<div style='flex:1;background:#111d2e;border:2px solid " + col + ";"
            "border-radius:14px;padding:24px 20px;text-align:center;'>"
            "<div style='font-size:20px;font-weight:800;color:" + col + ";margin-bottom:8px;'>" + step + "</div>"
            "<div style='font-size:32px;font-weight:900;color:#fff;margin-bottom:6px;line-height:1.3;'>" + title_html + "</div>"
            "<div style='font-size:18px;color:" + col + ";margin-bottom:12px;'>" + sub + "</div>"
            "<div style='font-size:16px;color:#666;'>" + ex + "</div>"
            "</div>"
        )
        if i < 2:
            cards_html += "<div style='display:flex;align-items:center;font-size:36px;color:#fff;padding:0 8px;'>→</div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>3/10</div>"
        "<div class='title'>「歩くだけ」で体が変わる3ステップ</div>"
        "<div style='position:absolute;left:40px;top:160px;right:40px;display:flex;align-items:stretch;'>"
        + cards_html + "</div>"
        "<div style='position:absolute;left:56px;bottom:76px;'>"
        "<span style='font-size:24px;font-weight:700;color:#FF6D00;'>ジムも走りもプロテインもいらない。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:12px;'>歩くだけでいい</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード4：仕組み（科学的根拠カード＋出典バッジ）
# ═══════════════════════════════════════════════════
def card_04():
    accent = "#38bdf8"
    reasons = [
        ("①", "+2,000歩で死亡リスク11%減", "15〜20分歩くだけで心血管リスク低下", "#FF6D00"),
        ("②", "食後5分歩行で血糖値安定", "スパイクが穏やかに→眠気・間食↓", "#38bdf8"),
        ("③", "少しでも増やせば効果あり", "ゼロか100かではない。+500歩でも体は応える", "#4ade80"),
    ]
    items = ""
    for num, title, desc, col in reasons:
        items += (
            "<div style='display:flex;align-items:flex-start;margin-bottom:16px;'>"
            "<div style='min-width:52px;height:52px;background:" + col + ";border-radius:12px;"
            "display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900;color:#000;'>" + num + "</div>"
            "<div style='margin-left:16px;'>"
            "<div style='font-size:26px;font-weight:800;color:#fff;'>" + title + "</div>"
            "<div style='font-size:20px;color:#9ca3af;margin-top:4px;'>" + desc + "</div>"
            "</div></div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>4/10</div>"
        "<div class='title'>なぜ「歩くだけ」で体が変わるのか</div>"
        "<div style='position:absolute;left:56px;top:152px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:70px;display:flex;gap:12px;'>"
        "<div style='background:#111d2e;border:1px solid #38bdf8;border-radius:8px;padding:10px 20px;display:inline-flex;align-items:center;gap:10px;'>"
        "<span style='font-size:16px;color:#38bdf8;font-weight:700;'>📄</span>"
        "<span style='font-size:15px;color:#9ca3af;'>Paluch et al., Lancet Public Health, 2022</span>"
        "</div>"
        "<div style='background:#111d2e;border:1px solid #4ade80;border-radius:8px;padding:10px 20px;display:inline-flex;align-items:center;gap:10px;'>"
        "<span style='font-size:16px;color:#4ade80;font-weight:700;'>📄</span>"
        "<span style='font-size:15px;color:#9ca3af;'>Buffey et al., Sports Medicine, 2022</span>"
        "</div>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード5：効果 Before/After比較
# ═══════════════════════════════════════════════════
def card_05():
    accent = "#4ade80"
    before = [
        "15時のお菓子が週5回",
        "午後の会議で常に眠い",
        "夕方の空腹が止まらない",
        "帰宅後にドカ食い",
    ]
    after = [
        "お菓子が週2回に自然減",
        "午後も集中が持続",
        "夕方の空腹が激減",
        "帰宅後もコントロール可能",
    ]
    left = ""
    for b in before:
        left += "<div style='display:flex;align-items:center;margin-bottom:12px;'><span style='color:#ef4444;font-size:22px;margin-right:8px;'>✗</span><span style='font-size:22px;color:#fca5a5;'>" + b + "</span></div>"
    right = ""
    for a in after:
        right += "<div style='display:flex;align-items:center;margin-bottom:12px;'><span style='color:#4ade80;font-size:22px;margin-right:8px;'>✓</span><span style='font-size:22px;color:#86efac;'>" + a + "</span></div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>5/10</div>"
        "<div class='title'>食後ウォークで起きた変化</div>"
        "<div style='position:absolute;left:40px;top:152px;right:40px;display:flex;gap:24px;'>"
        "<div style='flex:1;background:rgba(239,68,68,.08);border:2px solid rgba(239,68,68,.3);"
        "border-radius:14px;padding:24px;'>"
        "<div style='font-size:24px;font-weight:800;color:#ef4444;margin-bottom:16px;text-align:center;'>❌ BEFORE</div>"
        + left +
        "</div>"
        "<div style='flex:1;background:rgba(74,222,128,.08);border:2px solid rgba(74,222,128,.3);"
        "border-radius:14px;padding:24px;'>"
        "<div style='font-size:24px;font-weight:800;color:#4ade80;margin-bottom:16px;text-align:center;'>✅ AFTER</div>"
        + right +
        "</div>"
        "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;display:flex;align-items:baseline;gap:16px;'>"
        "<span style='font-size:48px;font-weight:900;color:#FF6D00;'>昼食後10分だけ</span>"
        "<span style='font-size:20px;color:#9ca3af;'>我慢じゃなく衝動が消えた</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード6：設計（1駅手前の3つの強みテーブル）
# ═══════════════════════════════════════════════════
def card_06():
    accent = "#38bdf8"
    rows = [
        ("判断がいらない", "帰宅ルートに組込むだけ", "ジムは毎回「行くか行かないか」を判断する", "#FF6D00"),
        ("時間が固定される", "帰宅時間＝ウォーク時間", "「いつ歩くか」を考えなくていい", "#38bdf8"),
        ("達成感が自動", "家に着いた＝完了", "ゴールが明確。追加の判断不要", "#4ade80"),
    ]
    items = ""
    for title, point, detail, col in rows:
        items += (
            "<div style='display:flex;gap:16px;margin-bottom:14px;'>"
            "<div style='min-width:240px;background:#111d2e;border:2px solid " + col + ";"
            "border-radius:12px;padding:16px 20px;'>"
            "<div style='font-size:24px;font-weight:900;color:" + col + ";'>" + title + "</div>"
            "<div style='font-size:18px;color:#d1d5db;margin-top:6px;'>" + point + "</div>"
            "</div>"
            "<div style='flex:1;background:#0d2035;border-radius:12px;padding:16px 20px;"
            "display:flex;align-items:center;'>"
            "<div style='font-size:20px;color:#9ca3af;'>" + detail + "</div>"
            "</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>6/10</div>"
        "<div class='title'>1駅手前ウォークが最強な3つの理由</div>"
        "<div style='position:absolute;left:40px;top:148px;right:40px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;'>"
        "<span style='font-size:22px;color:#FF6D00;font-weight:700;'>週3回で月14,400歩追加。</span>"
        "<span style='font-size:18px;color:#9ca3af;'>3ヶ月で1.5kg分の脂肪に相当</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード7：実践（+1,500歩の足し方フロー）
# ═══════════════════════════════════════════════════
def card_07():
    accent = "#FF6D00"
    steps = [
        ("食後10分ウォーク", "約1,000歩", "昼食後にオフィス周り1周", "#FF6D00"),
        ("1駅手前ウォーク", "約1,200歩", "帰宅時に1駅手前で下車", "#38bdf8"),
        ("1つ先のコンビニ", "約300歩", "朝の買い物をちょっと遠くに", "#4ade80"),
    ]
    items = ""
    for i, (title, count, desc, col) in enumerate(steps):
        items += (
            "<div style='display:flex;align-items:center;gap:20px;'>"
            "<div style='min-width:100px;text-align:center;'>"
            "<div style='width:44px;height:44px;margin:0 auto;background:" + col + ";"
            "border-radius:50%;display:flex;align-items:center;justify-content:center;"
            "font-size:22px;font-weight:900;color:#000;'>" + str(i+1) + "</div>"
            "<div style='font-size:18px;font-weight:800;color:" + col + ";margin-top:6px;'>" + count + "</div>"
            "</div>"
            "<div style='flex:1;background:#111d2e;border:2px solid " + col + ";"
            "border-radius:12px;padding:18px 24px;'>"
            "<div style='font-size:30px;font-weight:900;color:#fff;'>" + title + "</div>"
            "<div style='font-size:20px;color:#9ca3af;margin-top:6px;'>" + desc + "</div>"
            "</div></div>"
        )
        if i < 2:
            items += "<div style='text-align:center;margin:6px 0;'><div style='width:4px;height:24px;background:#333;margin:0 auto;border-radius:2px;'></div></div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>7/10</div>"
        "<div class='title'>+1,500歩の足し方（どれか1〜2つでOK）</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;'>"
        "<span style='font-size:24px;font-weight:700;color:#FF6D00;'>全部やらなくていい。</span>"
        "<span style='font-size:20px;color:#9ca3af;'>1つ選んで今日からやってみる</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード8：復帰フロー
# ═══════════════════════════════════════════════════
def card_08():
    accent = "#4ade80"
    steps = [
        ("歩けなかった日…", "雨・飲み会・疲労・体調不良", "#ef4444", "#1a0a0a"),
        ("✅ その日は何もしない", "反省も後悔もしない。ただ寝る", "#fff", "#111d2e"),
        ("✅ 翌日いつもの時間に歩く", "それだけでリセット完了", "#38bdf8", "#111d2e"),
        ("✅ 2日休んだら10分だけ", "10分歩けたらもう戻れている", "#4ade80", "#111d2e"),
    ]
    items = ""
    for i, (title, sub, col, bg) in enumerate(steps):
        border = "#ef4444" if i == 0 else col
        items += (
            "<div style='background:" + bg + ";border-left:4px solid " + border + ";"
            "border-radius:0 10px 10px 0;padding:14px 20px;margin-bottom:8px;'>"
            "<div style='font-size:26px;font-weight:800;color:" + col + ";'>" + title + "</div>"
            "<div style='font-size:18px;color:#9ca3af;margin-top:4px;'>" + sub + "</div>"
            "</div>"
        )
        if i < len(steps) - 1:
            items += "<div style='text-align:left;margin-left:20px;font-size:20px;color:#555;'>↓</div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>8/10</div>"
        "<div class='title'>歩けなかった日のリカバリー設計</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:68px;'>"
        "<span style='font-size:32px;font-weight:900;color:#FF6D00;'>8勝6敗でOK。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:8px;'>週4日歩けたら十分です</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード9：深掘り（歩数と健康リスクの棒グラフ）
# ═══════════════════════════════════════════════════
def card_09():
    accent = "#38bdf8"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>9/10</div>"
        "<div class='title'>歩数と健康リスクの関係（科学データ）</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>"
        # 棒グラフ風
        "<div style='margin-bottom:20px;'>"
        "<div style='font-size:18px;color:#9ca3af;margin-bottom:8px;'>📊 1日の歩数増加と心血管死亡リスク低下率</div>"
        "<div style='display:flex;align-items:flex-end;gap:16px;height:180px;padding-left:20px;'>"
        # 棒
        "<div style='flex:1;display:flex;flex-direction:column;align-items:center;'>"
        "<div style='font-size:20px;font-weight:800;color:#f59e0b;margin-bottom:4px;'>-5%</div>"
        "<div style='width:100%;height:40px;background:linear-gradient(to top,#f59e0b,#d97706);border-radius:6px 6px 0 0;'></div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>+1,000歩</div></div>"
        "<div style='flex:1;display:flex;flex-direction:column;align-items:center;'>"
        "<div style='font-size:20px;font-weight:800;color:#38bdf8;margin-bottom:4px;'>-11%</div>"
        "<div style='width:100%;height:90px;background:linear-gradient(to top,#38bdf8,#0ea5e9);border-radius:6px 6px 0 0;'></div>"
        "<div style='font-size:16px;color:#fff;margin-top:6px;font-weight:700;'>+2,000歩</div></div>"
        "<div style='flex:1;display:flex;flex-direction:column;align-items:center;'>"
        "<div style='font-size:20px;font-weight:800;color:#4ade80;margin-bottom:4px;'>-17%</div>"
        "<div style='width:100%;height:135px;background:linear-gradient(to top,#4ade80,#22c55e);border-radius:6px 6px 0 0;'></div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>+4,000歩</div></div>"
        "<div style='flex:1;display:flex;flex-direction:column;align-items:center;'>"
        "<div style='font-size:20px;font-weight:800;color:#22c55e;margin-bottom:4px;'>-24%</div>"
        "<div style='width:100%;height:180px;background:linear-gradient(to top,#22c55e,#16a34a);border-radius:6px 6px 0 0;'></div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>+6,000歩</div></div>"
        "</div>"
        "</div>"
        # 追加データ
        "<div style='display:flex;gap:16px;margin-top:20px;'>"
        "<div style='flex:1;background:#111d2e;border:1px solid #333;border-radius:10px;padding:16px;'>"
        "<div style='font-size:20px;font-weight:800;color:#38bdf8;'>食後ウォーク効果</div>"
        "<div style='font-size:17px;color:#9ca3af;margin-top:6px;'>食後2〜5分歩くだけで血糖値スパイク有意に抑制</div>"
        "</div>"
        "<div style='flex:1;background:#111d2e;border:1px solid #333;border-radius:10px;padding:16px;'>"
        "<div style='font-size:20px;font-weight:800;color:#4ade80;'>最も重要なポイント</div>"
        "<div style='font-size:17px;color:#9ca3af;margin-top:6px;'>「少しでも増やせば効果がある」ゼロか100かではない</div>"
        "</div>"
        "</div>"
        "</div>"
        "<div style='position:absolute;left:56px;bottom:68px;display:flex;gap:12px;'>"
        "<div style='background:#111d2e;border:1px solid #38bdf8;border-radius:8px;padding:10px 16px;display:inline-flex;align-items:center;gap:8px;'>"
        "<span style='font-size:14px;color:#38bdf8;font-weight:700;'>📄</span>"
        "<span style='font-size:14px;color:#9ca3af;'>Paluch et al., Lancet Public Health, 2022</span>"
        "</div>"
        "<div style='background:#111d2e;border:1px solid #4ade80;border-radius:8px;padding:10px 16px;display:inline-flex;align-items:center;gap:8px;'>"
        "<span style='font-size:14px;color:#4ade80;font-weight:700;'>📄</span>"
        "<span style='font-size:14px;color:#9ca3af;'>Buffey et al., Sports Medicine, 2022</span>"
        "</div>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード10：CTA まとめチェックリスト
# ═══════════════════════════════════════════════════
def card_10():
    accent = "#FF6D00"
    checks = [
        ("STEP 1", "食後10分ウォーク → 血糖値安定・間食↓", "#FF6D00"),
        ("STEP 2", "1駅手前を週3回 → 判断不要・達成感自動", "#38bdf8"),
        ("STEP 3", "今より+1,500歩 → スマホで現状確認", "#4ade80"),
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
        "<div class='title'>歩くだけで体が変わる｜まとめ</div>"
        "<div style='position:absolute;left:56px;top:152px;right:56px;'>" + items + "</div>"
        # CTA box
        "<div style='position:absolute;left:40px;bottom:76px;right:40px;"
        "background:linear-gradient(135deg,rgba(255,109,0,.15),rgba(255,109,0,.05));"
        "border:2px solid #FF6D00;border-radius:14px;padding:20px 28px;"
        "display:flex;align-items:center;justify-content:space-between;'>"
        "<div>"
        "<div style='font-size:28px;font-weight:900;color:#FF6D00;'>今日、昼食後に10分だけ歩く。</div>"
        "<div style='font-size:18px;color:#9ca3af;margin-top:4px;'>歩くだけで、体は変わります。</div>"
        "</div>"
        "<div style='font-size:16px;color:#FF6D00;font-weight:700;white-space:nowrap;'>noteで詳細 →</div>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ── カード関数リスト ─────────────────────────────
CARD_FUNCS = [card_01, card_02, card_03, card_04, card_05,
              card_06, card_07, card_08, card_09, card_10]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]


def render(html: str, fname: str):
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
            "## 投稿" + str(i+1) + "/10｜" + tag + "\n\n```\n" + tweet.strip() + FIXED_TAGS + "\n```\n\n"
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

