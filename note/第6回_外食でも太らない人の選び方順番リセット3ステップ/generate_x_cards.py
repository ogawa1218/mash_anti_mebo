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
HASHTAG = "#第 外食の順番リセット"

# ── 共通CSS ──────────────────────────────────────
BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;background:#0d1b2a;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
    ".tag{position:absolute;left:56px;top:40px;color:#000;font-size:22px;"
    "font-weight:800;padding:5px 18px;border-radius:18px;letter-spacing:1px;}"
    ".num{position:absolute;top:44px;right:56px;font-size:22px;font-weight:700;color:#444;}"
    ".author{position:absolute;bottom:22px;left:56px;font-size:18px;font-weight:400;color:#3a3a3a;}"
    ".series{position:absolute;bottom:22px;right:56px;font-size:18px;font-weight:700;}"
    ".title{position:absolute;left:56px;top:96px;font-size:36px;font-weight:900;color:#fff;"
    "letter-spacing:-1px;}"
)

# ── ツイートデータ ──────────────────────────────────
TWEETS = [
    """残業後の22時。
疲れた頭で駅前に出て、目に入った丼を頼む。
食べ終えた後の自己嫌悪、つらいですよね。

これ、意志が弱いんじゃないんです。
「主食から決める」という設計ミスが原因でした。

↓続き（2/10）""",

    """主食（丼・麺）から食べ始めると何が起きるか。

血糖値が急上昇→急降下。
「もう少し食べたい」という衝動が出る。
追加注文→帰宅後のつまみ食い→自己嫌悪。

このループ、根性論では止まりません。
最初の1手を変えるだけで切れます。

↓続き（3/10）""",

    """外食崩れを止めた1つの変化。

主食から決める→主菜から決める

「今日は何でたんぱく質を取るか？」を最初に決める。
副菜を1つ足して、主食を最後に調整する。

主菜→副菜→主食。
この順番を固定するだけです。

↓続き（4/10）""",

    """なぜ食べる順番で変わるのか。

①主菜（たんぱく質）先→満足感が出て追加注文が減る
②副菜を足す→食べるスピードが落ちて勢い食いを防ぐ
③主食を最後に→量を必要分だけ調整できる

2015年Diabetes Care の研究でも食べる順番が食後血糖値に有意な影響を与えることが示されています。

↓続き（5/10）""",

    """順番を変えてから僕に起きた変化。

・帰宅後のつまみ食いがほぼゼロに
・翌朝のむくみが激減
・朝食が食べられるようになった
・午後の眠気が軽くなった
・3ヶ月で-8kg

やったことは「主菜から決める」だけ。
100kgから68kgになるまで、この習慣を続けました。

↓続き（6/10）""",

    """疲れた夜の外食設計はシンプルに。

主菜の選び方：
焼き魚・刺身・鶏グリル・卵系・赤身肉

副菜の足し方：
サラダ・おひたし・味噌汁1杯でもOK

主食の調整：
小盛り・替え玉なし・丼→定食化

最初に「何でたんぱく質を取るか」だけ決める。
あとは自然についてきます。

↓続き（7/10）""",

    """今夜から使える外食の鉄則。

店に入ったら最初に1つだけ決める。
「今日は、何でたんぱく質を取るか？」

焼き魚→決定。
次に副菜。
最後に主食の量。

これだけ。
全部完璧にやらなくていい。
「主菜から決める」1点だけ守れれば十分です。

↓続き（8/10）""",

    """崩れた日は、普通にあります。

会食で飲みすぎた。
残業でラーメン食べた。
それで終わりじゃない。

「昨日崩れたから今日は食べない」は逆効果。
空腹で夜を迎えるとまた崩れます。

次の食事で主菜→副菜→主食に戻すだけ。
8勝6敗でOK。続けることが全てです。

↓続き（9/10）""",

    """22時に外食で崩れやすい理由は脳にあります。

1日中判断を繰り返した脳は夜になると「省エネモード」に。
省エネモードの脳が選ぶのは「最も簡単な選択」。
＝目に入ったもの＝炭水化物。

これを「決断疲れ（Decision Fatigue）」と呼びます。
意志が弱いのではなく、脳が疲れているだけ。
だから「最初の選択だけ固定する」設計が効くんです。

↓続き（10/10）""",

    """【まとめ｜外食で太らない人の選び方】

✅ 崩れる原因は意志じゃなく「主食から決める」設計ミス
✅ 主菜→副菜→主食の順番を固定するだけでいい
✅ 崩れたら次の食事でリセット。ゼロにしない

今夜の外食で1つだけ試す。
→「主菜を先に決める」

体は責めるほど変わらない。整えるほど変わります。

詳しくはnoteに書きました👇
https://note.com/mash_anti_metabo""",
]


# ═══════════════════════════════════════════════════
# カード1：共感シナリオ（タイムライン型）
# ═══════════════════════════════════════════════════
def card_01():
    accent = "#38bdf8"
    steps = [
        ("22:00", "残業終了。頭ぼんやり", "#ef4444"),
        ("22:05", "目に入った丼屋に入店", "#ef4444"),
        ("22:20", "食べ終わる。満腹…", "#f59e0b"),
        ("23:00", "帰宅。なぜか口寂しい", "#ef4444"),
        ("23:30", "冷蔵庫を開けてしまう", "#ef4444"),
        ("23:50", "自己嫌悪…「明日から本気で」", "#ef4444"),
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
        "<div class='tag' style='background:" + accent + ";'>共感</div>"
        "<div class='num'>1/10</div>"
        "<div class='title'>残業後の22時。いつも同じ崩れ方をしていた</div>"
        "<div style='position:absolute;left:56px;top:152px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:80px;right:56px;padding:18px 24px;"
        "background:rgba(239,68,68,.12);border-left:4px solid #ef4444;border-radius:0 8px 8px 0;'>"
        "<span style='font-size:26px;font-weight:800;color:#ef4444;'>問題は意志じゃなかった。</span>"
        "<span style='font-size:22px;color:#9ca3af;margin-left:12px;'>「最初の1手」が間違っていた</span>"
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
        ("① 主食から注文", "#1e3a5f"),
        ("② 血糖値が急上昇", "#1e3a5f"),
        ("③ 急降下→追加注文", "#1e3a5f"),
        ("④ 帰宅後つまみ食い", "#1e3a5f"),
        ("⑤ 自己嫌悪→翌日も崩れる", "#1e3a5f"),
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
        "<div class='tag' style='background:" + accent + ";'>原因</div>"
        "<div class='num'>2/10</div>"
        "<div class='title'>外食崩れの悪循環ループ</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:66px;display:flex;align-items:center;gap:12px;'>"
        "<div style='font-size:38px;'>🔄</div>"
        "<div style='font-size:22px;color:#ef4444;font-weight:700;'>このループは根性論では止まらない</div>"
        "<div style='font-size:20px;color:#9ca3af;'>→ 最初の1手を変えれば切れる</div>"
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
        ("STEP 1", "主菜を決める", "たんぱく質の土台", "#FF6D00", "焼き魚・刺身・鶏グリル"),
        ("STEP 2", "副菜を足す", "勢い食いを防ぐ", "#38bdf8", "サラダ・汁物1杯でOK"),
        ("STEP 3", "主食を調整", "量の適正化", "#4ade80", "小盛り・替え玉なし"),
    ]
    cards_html = ""
    for i, (step, title, sub, col, ex) in enumerate(cards_data):
        cards_html += (
            "<div style='flex:1;background:#111d2e;border:2px solid " + col + ";"
            "border-radius:14px;padding:24px 20px;text-align:center;'>"
            "<div style='font-size:20px;font-weight:800;color:" + col + ";margin-bottom:8px;'>" + step + "</div>"
            "<div style='font-size:32px;font-weight:900;color:#fff;margin-bottom:6px;'>" + title + "</div>"
            "<div style='font-size:18px;color:" + col + ";margin-bottom:12px;'>" + sub + "</div>"
            "<div style='font-size:16px;color:#666;'>" + ex + "</div>"
            "</div>"
        )
        if i < 2:
            cards_html += "<div style='display:flex;align-items:center;font-size:36px;color:#fff;padding:0 8px;'>→</div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='tag' style='background:" + accent + ";'>解決策</div>"
        "<div class='num'>3/10</div>"
        "<div class='title'>主菜→副菜→主食。この順番を固定するだけ</div>"
        "<div style='position:absolute;left:40px;top:160px;right:40px;display:flex;align-items:stretch;'>"
        + cards_html + "</div>"
        "<div style='position:absolute;left:56px;bottom:76px;'>"
        "<span style='font-size:24px;font-weight:700;color:#FF6D00;'>カロリー計算なし。禁止食なし。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:12px;'>順番を変えるだけ</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード4：仕組み（3理由カード＋出典バッジ）
# ═══════════════════════════════════════════════════
def card_04():
    accent = "#38bdf8"
    reasons = [
        ("①", "主菜でたんぱく質の土台", "満足感が出て追加注文が減る", "#FF6D00"),
        ("②", "副菜で食べるペースを落とす", "勢い食い・早食いを防止", "#38bdf8"),
        ("③", "主食を最後に量を調整", "「小盛りでいいかな」が自然に選べる", "#4ade80"),
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
        "<div class='tag' style='background:" + accent + ";'>仕組み</div>"
        "<div class='num'>4/10</div>"
        "<div class='title'>なぜ順番を変えるだけで結果が変わるのか</div>"
        "<div style='position:absolute;left:56px;top:152px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:70px;background:#111d2e;"
        "border:1px solid #38bdf8;border-radius:8px;padding:10px 20px;display:inline-flex;align-items:center;gap:10px;'>"
        "<span style='font-size:18px;color:#38bdf8;font-weight:700;'>📄 出典</span>"
        "<span style='font-size:16px;color:#9ca3af;'>Shukla et al., Diabetes Care, 2015</span>"
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
        "帰宅後つまみ食い",
        "翌朝のむくみ",
        "朝食が食べられない",
        "午後に強烈な眠気",
    ]
    after = [
        "つまみ食いほぼゼロ",
        "むくみ激減",
        "朝食が自然に食べられる",
        "午後の眠気が軽い",
    ]
    left = ""
    for b in before:
        left += "<div style='display:flex;align-items:center;margin-bottom:12px;'><span style='color:#ef4444;font-size:22px;margin-right:8px;'>✗</span><span style='font-size:22px;color:#fca5a5;'>" + b + "</span></div>"
    right = ""
    for a in after:
        right += "<div style='display:flex;align-items:center;margin-bottom:12px;'><span style='color:#4ade80;font-size:22px;margin-right:8px;'>✓</span><span style='font-size:22px;color:#86efac;'>" + a + "</span></div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='tag' style='background:" + accent + ";'>効果</div>"
        "<div class='num'>5/10</div>"
        "<div class='title'>順番を変えてから3ヶ月で起きた変化</div>"
        "<div style='position:absolute;left:40px;top:152px;right:40px;display:flex;gap:24px;'>"
        # Before
        "<div style='flex:1;background:rgba(239,68,68,.08);border:2px solid rgba(239,68,68,.3);"
        "border-radius:14px;padding:24px;'>"
        "<div style='font-size:24px;font-weight:800;color:#ef4444;margin-bottom:16px;text-align:center;'>❌ BEFORE</div>"
        + left +
        "</div>"
        # After
        "<div style='flex:1;background:rgba(74,222,128,.08);border:2px solid rgba(74,222,128,.3);"
        "border-radius:14px;padding:24px;'>"
        "<div style='font-size:24px;font-weight:800;color:#4ade80;margin-bottom:16px;text-align:center;'>✅ AFTER</div>"
        + right +
        "</div>"
        "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;display:flex;align-items:baseline;gap:16px;'>"
        "<span style='font-size:48px;font-weight:900;color:#FF6D00;'>-8kg / 3ヶ月</span>"
        "<span style='font-size:20px;color:#9ca3af;'>やったことは「主菜から決める」だけ</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード6：設計（シーン別テーブル）
# ═══════════════════════════════════════════════════
def card_06():
    accent = "#38bdf8"
    rows = [
        ("定食屋", "焼き魚・しょうが焼き", "おひたし・小鉢", "ご飯小盛り"),
        ("居酒屋", "刺身盛り・鶏グリル", "海藻サラダ", "シメは半分"),
        ("ラーメン屋", "ゆで卵を追加", "メンマ先食い", "替え玉なし"),
        ("コンビニ", "サラダチキン・卵", "野菜惣菜を追加", "おにぎり1個"),
    ]
    header = (
        "<div style='display:flex;background:#1e3a5f;border-radius:10px 10px 0 0;padding:12px 16px;'>"
        "<div style='flex:1.2;font-size:20px;font-weight:800;color:#fff;'>外食シーン</div>"
        "<div style='flex:1.5;font-size:20px;font-weight:800;color:#FF6D00;'>主菜</div>"
        "<div style='flex:1.5;font-size:20px;font-weight:800;color:#38bdf8;'>副菜</div>"
        "<div style='flex:1.2;font-size:20px;font-weight:800;color:#4ade80;'>主食</div>"
        "</div>"
    )
    body = ""
    for i, (scene, main, side, staple) in enumerate(rows):
        bg = "#111d2e" if i % 2 == 0 else "#0d1b2a"
        body += (
            "<div style='display:flex;background:" + bg + ";padding:14px 16px;"
            "border-bottom:1px solid #1e3a5f;'>"
            "<div style='flex:1.2;font-size:20px;font-weight:700;color:#fff;'>" + scene + "</div>"
            "<div style='flex:1.5;font-size:18px;color:#e5e7eb;'>" + main + "</div>"
            "<div style='flex:1.5;font-size:18px;color:#e5e7eb;'>" + side + "</div>"
            "<div style='flex:1.2;font-size:18px;color:#e5e7eb;'>" + staple + "</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='tag' style='background:" + accent + ";'>設計</div>"
        "<div class='num'>6/10</div>"
        "<div class='title'>外食シーン別 順番リセット早見表</div>"
        "<div style='position:absolute;left:40px;top:148px;right:40px;"
        "border:2px solid #1e3a5f;border-radius:12px;overflow:hidden;'>"
        + header + body +
        "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;'>"
        "<span style='font-size:22px;color:#FF6D00;font-weight:700;'>最初に「何でたんぱく質を取るか」だけ決める。</span>"
        "<span style='font-size:18px;color:#9ca3af;'>あとは自然についてきます</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード7：実践（ステップフロー縦型）
# ═══════════════════════════════════════════════════
def card_07():
    accent = "#FF6D00"
    steps = [
        ("STEP 1", "主菜を決める", "「今日は何でたんぱく質を取るか？」", "#FF6D00"),
        ("STEP 2", "副菜を1つ足す", "汁物1杯でもOK。ゼロか1かが大事", "#38bdf8"),
        ("STEP 3", "主食を最後に調整", "小盛り・替え玉なし・定食化", "#4ade80"),
    ]
    items = ""
    for i, (step, title, desc, col) in enumerate(steps):
        items += (
            "<div style='display:flex;align-items:center;gap:20px;'>"
            "<div style='min-width:100px;text-align:center;'>"
            "<div style='font-size:18px;font-weight:800;color:" + col + ";'>" + step + "</div>"
            "<div style='width:44px;height:44px;margin:8px auto;background:" + col + ";"
            "border-radius:50%;display:flex;align-items:center;justify-content:center;"
            "font-size:22px;font-weight:900;color:#000;'>" + str(i+1) + "</div>"
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
        "<div class='tag' style='background:" + accent + ";'>実践</div>"
        "<div class='num'>7/10</div>"
        "<div class='title'>今夜から使える外食の鉄則</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;'>"
        "<span style='font-size:24px;font-weight:700;color:#FF6D00;'>完璧にやらなくていい。</span>"
        "<span style='font-size:20px;color:#9ca3af;'>まず1回、主菜から決めてみる</span>"
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
        ("崩れた夜…", "会食・深夜ラーメン・止まらなかった", "#ef4444", "#1a0a0a"),
        ("✅ 自己嫌悪をやめる", "「次の食事で戻す」に切り替え", "#fff", "#111d2e"),
        ("✅ 翌朝食を抜かない", "空腹で夜を迎えると再崩れする", "#38bdf8", "#111d2e"),
        ("✅ 次の外食で主菜から", "1回順番通りに選べたらリセット完了", "#4ade80", "#111d2e"),
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
        "<div class='tag' style='background:" + accent + ";'>復帰</div>"
        "<div class='num'>8/10</div>"
        "<div class='title'>崩れた日のリカバリー設計</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:68px;'>"
        "<span style='font-size:32px;font-weight:900;color:#FF6D00;'>8勝6敗でOK。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:8px;'>続けることが全てです</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード9：深掘り（科学メカニズム図）
# ═══════════════════════════════════════════════════
def card_09():
    accent = "#38bdf8"
    # 時間軸グラフ風
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='tag' style='background:" + accent + ";'>深掘り</div>"
        "<div class='num'>9/10</div>"
        "<div class='title'>22時に崩れやすい科学的な理由</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>"
        # 判断力グラフ（簡易CSS棒グラフ）
        "<div style='margin-bottom:20px;'>"
        "<div style='font-size:18px;color:#9ca3af;margin-bottom:8px;'>⏰ 判断力の推移（Decision Fatigue）</div>"
        "<div style='display:flex;align-items:flex-end;gap:6px;height:120px;'>"
        # 朝〜夜の棒
        "<div style='flex:1;display:flex;flex-direction:column;align-items:center;'>"
        "<div style='width:100%;height:110px;background:linear-gradient(to top,#4ade80,#22c55e);border-radius:6px 6px 0 0;'></div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>8時</div></div>"
        "<div style='flex:1;display:flex;flex-direction:column;align-items:center;'>"
        "<div style='width:100%;height:90px;background:linear-gradient(to top,#38bdf8,#0ea5e9);border-radius:6px 6px 0 0;'></div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>12時</div></div>"
        "<div style='flex:1;display:flex;flex-direction:column;align-items:center;'>"
        "<div style='width:100%;height:60px;background:linear-gradient(to top,#f59e0b,#d97706);border-radius:6px 6px 0 0;'></div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>17時</div></div>"
        "<div style='flex:1;display:flex;flex-direction:column;align-items:center;'>"
        "<div style='width:100%;height:25px;background:linear-gradient(to top,#ef4444,#dc2626);border-radius:6px 6px 0 0;'></div>"
        "<div style='font-size:14px;color:#fff;margin-top:4px;font-weight:700;'>22時</div></div>"
        "</div>"
        "</div>"
        # 説明カード
        "<div style='display:flex;gap:16px;margin-top:20px;'>"
        "<div style='flex:1;background:#111d2e;border:1px solid #333;border-radius:10px;padding:16px;'>"
        "<div style='font-size:20px;font-weight:800;color:#ef4444;'>22時の脳</div>"
        "<div style='font-size:17px;color:#9ca3af;margin-top:6px;'>省エネモード→「最も簡単な選択」=炭水化物</div>"
        "</div>"
        "<div style='flex:1;background:#111d2e;border:1px solid #333;border-radius:10px;padding:16px;'>"
        "<div style='font-size:20px;font-weight:800;color:#4ade80;'>対策</div>"
        "<div style='font-size:17px;color:#9ca3af;margin-top:6px;'>判断を1つに減らす→「主菜から決める」だけ固定</div>"
        "</div>"
        "</div>"
        "</div>"
        "<div style='position:absolute;left:56px;bottom:68px;background:#111d2e;"
        "border:1px solid #38bdf8;border-radius:8px;padding:10px 20px;display:inline-flex;align-items:center;gap:10px;'>"
        "<span style='font-size:16px;color:#38bdf8;font-weight:700;'>📄</span>"
        "<span style='font-size:15px;color:#9ca3af;'>Danziger et al., PNAS, 2011</span>"
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
        ("崩れる原因", "意志じゃなく「主食から決める」設計ミス", "#38bdf8"),
        ("解決策", "主菜→副菜→主食の順番を固定するだけ", "#FF6D00"),
        ("崩れたら", "次の食事でリセット。ゼロにしない", "#4ade80"),
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
        "<div class='tag' style='background:" + accent + ";'>今夜やること</div>"
        "<div class='num'>10/10</div>"
        "<div class='title'>外食で太らない人の選び方｜まとめ</div>"
        "<div style='position:absolute;left:56px;top:152px;right:56px;'>" + items + "</div>"
        # CTA box
        "<div style='position:absolute;left:40px;bottom:76px;right:40px;"
        "background:linear-gradient(135deg,rgba(255,109,0,.15),rgba(255,109,0,.05));"
        "border:2px solid #FF6D00;border-radius:14px;padding:20px 28px;"
        "display:flex;align-items:center;justify-content:space-between;'>"
        "<div>"
        "<div style='font-size:28px;font-weight:900;color:#FF6D00;'>今夜、主菜を先に決める。</div>"
        "<div style='font-size:18px;color:#9ca3af;margin-top:4px;'>体は責めるほど変わらない。整えるほど変わる。</div>"
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

