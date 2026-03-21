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
HASHTAG = "#第 間食の置き換え設計"

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
    """帰宅して冷蔵庫を開ける。
チーズかまぼこ1本、ビールと一緒に。

「1本だけ」のはずが3本。
空袋をゴミの奥に隠す。

100kgだった頃、毎晩これだった。
月+1.5kg。年間12万円。

止められないのは意志が弱いからじゃなかった。

↓続き（2/10）""",

    """裁判官の判決データを調べた研究がある。

午前中の仮釈放承認率：65%
夕方：ほぼ0%

裁判官でさえ夕方は正しい判断ができなくなる。

これが「判断疲労」。
夕方に「食べない」と決められないのは当然。

意志の問題じゃない。設計の問題。

↓続き（3/10）""",

    """間食を「止める」のをやめた。
代わりに「置き換える」ことにした。

3つだけ決めた：
① 15時に先手の間食を固定
② 帰宅3分ルール
③ 22時以降、選択肢ゼロ

我慢はゼロ。設計だけ。
これで月12,000円→2,400円になった。

↓続き（4/10）""",

    """コーネル大学のワンシンク博士の実験。

お菓子の容器を透明→不透明に変えただけで
消費量が30%減った。

意志力を鍛える必要はない。
見えなくするだけで食べなくなる。

環境を変えれば行動が変わる。
これが「置き換え設計」の科学的根拠。

↓続き（5/10）""",

    """置き換え設計を始めて起きたこと：

❌ BEFORE
・コンビニ間食 月12,000円
・帰宅後のビール＋つまみ 週5
・22時以降 毎晩300kcal

✅ AFTER
・ナッツ30g＋コーヒー 月2,400円
・帰宅直後のつまみ 週1
・22時以降 ほぼゼロ

我慢は1回もしてない。

↓続き（6/10）""",

    """STEP 1｜15時固定間食の実装

300kcal 400円のコンビニスイーツを
150kcal 80円のナッツ30g＋ブラックコーヒーに。

デスクの引き出しに小分けナッツ常備。
最初の2週間だけ15時にアラーム設定。

これだけで夕方の暴走スイッチが消えた。

↓続き（7/10）""",

    """帰宅3分ルール。

靴を脱ぐ→部屋着に着替える
→コップ1杯の水→ミントガムを噛む

ポイントは「キッチンに立ち寄らない動線」を作ること。

玄関にミントガム。
着替えはリビング側に。

冷蔵庫を開ける前に3分稼ぐだけで夜が変わる。

↓続き（8/10）""",

    """これだけやっても崩れる日はある。
僕も月に4〜5回は崩れる。

崩れた夜のルール：
① 反省しない。計算しない。寝る
② 翌朝は普通に朝食を食べる
③ 翌日の15時にナッツ＋コーヒーを予定通りやる

8勝6敗でOK。
翌日の15時にリセット完了。

↓続き（9/10）""",

    """判断疲労の研究で面白いのは、
「食事をした直後に承認率が回復する」こと。

つまり15時にナッツを食べるのは
空腹を満たすだけじゃなく、
判断力を回復させる効果もある。

「先手の間食」は二重の意味で効く。
空腹対策＋判断力リチャージ。

↓続き（10/10）""",

    """【まとめ｜間食の置き換え設計】

✅ 15時にナッツ30g＋コーヒー
✅ 帰宅3分ルール（着替え→水→ミント）
✅ 22時以降は味噌汁・ヨーグルト・炭酸水だけ

今日やること1つだけ：
→ コンビニで小分けナッツを1袋買う

詳しくはnoteに書きました👇
https://note.com/mash_anti_metabo""",
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]


# ═══════════════════════════════════════════════════
# カード1：共感（タイムライン型：帰宅後の崩れパターン）
# ═══════════════════════════════════════════════════
def card_01():
    accent = "#38bdf8"
    events = [
        ("19:00", "帰宅。靴を脱ぐ", "#f59e0b"),
        ("19:01", "冷蔵庫を開ける", "#f59e0b"),
        ("19:03", "ビール＋チーズかまぼこ1本目", "#ef4444"),
        ("19:15", "気づけば3本目", "#ef4444"),
        ("19:20", "空袋をゴミの奥に隠す", "#ef4444"),
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
        "<div class='title'>100kgだった頃の毎晩。帰宅20分の記録</div>"
        "<div style='position:absolute;left:56px;top:152px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:76px;right:56px;padding:16px 24px;"
        "background:rgba(239,68,68,.12);border-left:4px solid #ef4444;border-radius:0 8px 8px 0;'>"
        "<span style='font-size:26px;font-weight:800;color:#ef4444;'>月+1.5kg。年間12万円。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:12px;'>止められないのは意志が弱いからじゃなかった</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード2：原因（判断疲労フロー図）
# ═══════════════════════════════════════════════════
def card_02():
    accent = "#38bdf8"
    steps = [
        ("① 午前：判断力100%", "#4ade80"),
        ("② 仕事で100回の判断", "#f59e0b"),
        ("③ 夕方：判断力ほぼ0%", "#ef4444"),
        ("④ 「食べない」と決められない", "#ef4444"),
        ("⑤ 冷蔵庫を開ける→崩れる", "#ef4444"),
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
        "<div class='title'>裁判官でさえ夕方は判断を間違える</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:66px;display:flex;align-items:center;gap:12px;'>"
        "<div style='font-size:22px;color:#38bdf8;font-weight:700;'>📄 Danziger et al., PNAS, 2011</div>"
        "<div style='font-size:18px;color:#9ca3af;'>仮釈放承認率 午前65%→夕方ほぼ0%</div>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード3：解決策（横3列ステップカード）
# ═══════════════════════════════════════════════════
def card_03():
    accent = "#FF6D00"
    cards_data = [
        ("STEP 1", "15時に先手の\n間食を固定", "夕方の空腹を消す", "#FF6D00", "ナッツ30g＋コーヒー"),
        ("STEP 2", "帰宅3分ルール", "動線で夜を変える", "#38bdf8", "着替え→水→ミント"),
        ("STEP 3", "22時以降\n選択肢ゼロ", "見えなければ食べない", "#4ade80", "味噌汁・ヨーグルト・炭酸水"),
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
        "<div class='title'>間食は「止める」のではなく「置き換える」</div>"
        "<div style='position:absolute;left:40px;top:160px;right:40px;display:flex;align-items:stretch;'>"
        + html_cards + "</div>"
        "<div style='position:absolute;left:56px;bottom:76px;'>"
        "<span style='font-size:24px;font-weight:700;color:#FF6D00;'>我慢ゼロ。設計だけ。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:12px;'>月12,000円→2,400円に</span>"
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
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>4/10</div>"
        "<div class='title'>なぜ「置き換え」が効くのか？2つの科学的根拠</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>"
        # 研究カード1
        "<div style='background:#111d2e;border:2px solid #38bdf8;border-radius:14px;padding:22px;margin-bottom:16px;'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>"
        "<div style='background:#38bdf8;color:#000;font-size:14px;font-weight:800;padding:4px 12px;border-radius:6px;'>根拠①</div>"
        "<div style='font-size:18px;color:#38bdf8;font-weight:700;'>判断疲労（Decision Fatigue）</div></div>"
        "<div style='font-size:22px;color:#fff;font-weight:700;margin-bottom:4px;'>判断力は有限。先に決めれば消耗しない</div>"
        "<div style='font-size:16px;color:#9ca3af;'>Danziger et al., PNAS, 2011</div>"
        "</div>"
        # 研究カード2
        "<div style='background:#111d2e;border:2px solid #4ade80;border-radius:14px;padding:22px;'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>"
        "<div style='background:#4ade80;color:#000;font-size:14px;font-weight:800;padding:4px 12px;border-radius:6px;'>根拠②</div>"
        "<div style='font-size:18px;color:#4ade80;font-weight:700;'>環境設計の力</div></div>"
        "<div style='font-size:22px;color:#fff;font-weight:700;margin-bottom:4px;'>容器を不透明にするだけで消費量 -30%</div>"
        "<div style='font-size:16px;color:#9ca3af;'>Wansink, Environment and Behavior, 2006</div>"
        "</div>"
        "</div>"
        "<div style='position:absolute;left:56px;bottom:70px;'>"
        "<span style='font-size:22px;font-weight:700;color:#FF6D00;'>意志力を鍛えるのではなく、環境を変える</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード5：効果（Before/After比較パネル）
# ═══════════════════════════════════════════════════
def card_05():
    accent = "#4ade80"
    before = [
        "コンビニ間食 月12,000円",
        "帰宅後ビール＋つまみ 週5",
        "22時以降 毎晩300kcal",
        "月+1.5kgペース",
    ]
    after = [
        "ナッツ＋コーヒー 月2,400円",
        "帰宅直後のつまみ 週1",
        "22時以降 ほぼゼロ",
        "月-1kgペースに逆転",
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
        "<div class='title'>置き換え設計で起きた変化｜我慢は1回もしてない</div>"
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
        "<span style='font-size:44px;font-weight:900;color:#FF6D00;'>-9,600円/月</span>"
        "<span style='font-size:20px;color:#9ca3af;'>間食コスト80%削減</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード6：設計（15時固定間食テーブル）
# ═══════════════════════════════════════════════════
def card_06():
    accent = "#38bdf8"
    rows = [
        ("項目", "BEFORE", "AFTER"),
        ("食べるもの", "コンビニスイーツ", "ナッツ30g＋ブラックコーヒー"),
        ("カロリー", "300kcal", "150kcal"),
        ("コスト", "400円/日", "80円/日"),
        ("月間コスト", "12,000円", "2,400円"),
        ("夕方の空腹", "毎日限界突破", "ほぼなし"),
    ]
    header = rows[0]
    data = rows[1:]
    h = (
        "<div style='display:flex;background:#1e3a5f;border-radius:10px 10px 0 0;padding:14px 16px;'>"
        "<div style='flex:1;font-size:20px;font-weight:800;color:#fff;'>" + header[0] + "</div>"
        "<div style='flex:2;font-size:20px;font-weight:800;color:#ef4444;'>" + header[1] + "</div>"
        "<div style='flex:2;font-size:20px;font-weight:800;color:#4ade80;'>" + header[2] + "</div>"
        "</div>"
    )
    body = ""
    for i, (item, bef, aft) in enumerate(data):
        bg = "#111d2e" if i % 2 == 0 else "#0d1b2a"
        body += (
            "<div style='display:flex;background:" + bg + ";padding:14px 16px;"
            "border-bottom:1px solid #1e3a5f;'>"
            "<div style='flex:1;font-size:20px;font-weight:700;color:#fff;'>" + item + "</div>"
            "<div style='flex:2;font-size:18px;color:#fca5a5;'>" + bef + "</div>"
            "<div style='flex:2;font-size:18px;color:#86efac;'>" + aft + "</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>6/10</div>"
        "<div class='title'>STEP 1｜15時固定間食の置き換え設計</div>"
        "<div style='position:absolute;left:40px;top:148px;right:40px;"
        "border:2px solid #1e3a5f;border-radius:12px;overflow:hidden;'>"
        + h + body + "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;'>"
        "<span style='font-size:22px;color:#FF6D00;font-weight:700;'>デスクの引き出しにナッツ常備。</span>"
        "<span style='font-size:18px;color:#9ca3af;'>最初の2週間だけ15時アラーム</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード7：実践（帰宅3分ルール 縦フロー型）
# ═══════════════════════════════════════════════════
def card_07():
    accent = "#FF6D00"
    steps = [
        ("🚪", "靴を脱いだら", "キッチンに立ち寄らず部屋着に着替え", "#FF6D00"),
        ("💧", "着替えたら", "コップ1杯の水を飲む", "#38bdf8"),
        ("🍃", "水を飲んだら", "ミントガムを噛む", "#4ade80"),
    ]
    items = ""
    for i, (icon, label, detail, col) in enumerate(steps):
        items += (
            "<div style='display:flex;align-items:center;gap:16px;margin-bottom:12px;'>"
            "<div style='min-width:56px;height:56px;background:" + col + ";border-radius:14px;"
            "display:flex;align-items:center;justify-content:center;font-size:28px;'>" + icon + "</div>"
            "<div style='flex:1;background:#111d2e;border:2px solid " + col + ";border-radius:12px;padding:16px 20px;'>"
            "<div style='font-size:24px;font-weight:800;color:#fff;'>" + label + "</div>"
            "<div style='font-size:18px;color:#9ca3af;margin-top:4px;'>" + detail + "</div>"
            "</div></div>"
        )
        if i < len(steps) - 1:
            items += "<div style='margin-left:24px;font-size:24px;color:#555;margin-bottom:6px;'>↓</div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>7/10</div>"
        "<div class='title'>STEP 2｜帰宅3分ルールで冷蔵庫直行を止める</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;'>"
        "<span style='font-size:24px;font-weight:700;color:#FF6D00;'>ビール＋つまみ 週5→週1。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:8px;'>動線を変えたら勝手に減った</span>"
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
        ("崩れた夜…", "飲み会・出張・我慢できなかった日", "#ef4444", "#1a0a0a"),
        ("❌ やらないこと", "翌日の食事を抜く＝反動で再崩れ", "#ef4444", "#111d2e"),
        ("✅ その夜は寝る", "反省も計算もしない。とにかく寝る", "#f59e0b", "#111d2e"),
        ("✅ 翌朝普通に食べる", "朝食を食べて血糖値を安定させる", "#38bdf8", "#111d2e"),
        ("✅ 翌日15時にリセット", "ナッツ＋コーヒーを予定通りやる", "#4ade80", "#111d2e"),
    ]
    items = ""
    for i, (title, sub, col, bg) in enumerate(steps):
        items += (
            "<div style='background:" + bg + ";border-left:4px solid " + col + ";"
            "border-radius:0 10px 10px 0;padding:12px 20px;margin-bottom:6px;'>"
            "<div style='font-size:24px;font-weight:800;color:" + col + ";'>" + title + "</div>"
            "<div style='font-size:16px;color:#9ca3af;margin-top:2px;'>" + sub + "</div>"
            "</div>"
        )
        if i < len(steps) - 1:
            items += "<div style='text-align:left;margin-left:20px;font-size:18px;color:#555;'>↓</div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>8/10</div>"
        "<div class='title'>崩れた日のリカバリー手順</div>"
        "<div style='position:absolute;left:56px;top:140px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:68px;'>"
        "<span style='font-size:32px;font-weight:900;color:#FF6D00;'>8勝6敗でOK。翌日の15時にリセット完了。</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード9：深掘り（判断力回復のCSSグラフ）
# ═══════════════════════════════════════════════════
def card_09():
    accent = "#38bdf8"
    bars = [
        ("9時", "90%", "90", "#4ade80"),
        ("12時", "70%", "70", "#4ade80"),
        ("15時前", "30%", "30", "#ef4444"),
        ("15時\n(間食後)", "65%", "65", "#38bdf8"),
        ("18時", "50%", "50", "#f59e0b"),
    ]
    bar_html = ""
    for label, pct, height, col in bars:
        label_html = label.replace("\n", "<br>")
        bar_html += (
            "<div style='display:flex;flex-direction:column;align-items:center;flex:1;'>"
            "<div style='font-size:16px;font-weight:700;color:" + col + ";margin-bottom:6px;'>" + pct + "</div>"
            "<div style='width:60px;height:" + str(int(height) * 3) + "px;background:" + col + ";"
            "border-radius:8px 8px 0 0;'></div>"
            "<div style='font-size:16px;color:#9ca3af;margin-top:8px;text-align:center;line-height:1.3;'>" + label_html + "</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>9/10</div>"
        "<div class='title'>15時の間食は判断力もリチャージする</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>"
        "<div style='font-size:20px;color:#9ca3af;margin-bottom:12px;'>判断力の推移（イメージ）</div>"
        "<div style='display:flex;align-items:flex-end;height:300px;gap:16px;padding:0 40px;'>"
        + bar_html + "</div></div>"
        "<div style='position:absolute;left:56px;bottom:70px;background:#111d2e;"
        "border:2px solid #38bdf8;border-radius:10px;padding:14px 24px;'>"
        "<span style='font-size:20px;font-weight:800;color:#38bdf8;'>食事で判断力が回復 →</span>"
        "<span style='font-size:20px;color:#fff;margin-left:8px;'>先手の間食＝空腹対策＋判断力リチャージ</span>"
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
        ("15時にナッツ30g＋コーヒー", "夕方の暴走スイッチを先に消す", "#FF6D00"),
        ("帰宅3分ルール", "着替え→水→ミントで冷蔵庫直行を止める", "#38bdf8"),
        ("22時以降は3択だけ", "味噌汁・ヨーグルト・炭酸水", "#4ade80"),
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
        "<div class='title'>間食の置き換え設計｜まとめ</div>"
        "<div style='position:absolute;left:56px;top:152px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:40px;bottom:76px;right:40px;"
        "background:linear-gradient(135deg,rgba(255,109,0,.15),rgba(255,109,0,.05));"
        "border:2px solid #FF6D00;border-radius:14px;padding:20px 28px;"
        "display:flex;align-items:center;justify-content:space-between;'>"
        "<div>"
        "<div style='font-size:28px;font-weight:900;color:#FF6D00;'>今日やること1つだけ。</div>"
        "<div style='font-size:18px;color:#9ca3af;margin-top:4px;'>コンビニで小分けナッツを1袋買う。</div>"
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

