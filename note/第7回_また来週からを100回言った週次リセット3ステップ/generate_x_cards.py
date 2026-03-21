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
HASHTAG = "#第 週次リセット"

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

TWEETS = [
    """月曜に「今週こそは」と決める。
火曜に崩れる。
水曜に「もう今週はいいや」。
金曜に体重計を見て落ち込む。

「また来週から」

これ、何回言いましたか？
僕は100回以上言いました。100kgの頃の話です。

↓続き（2/10）""",

    """崩れるのは普通です。

忙しい30〜40代で、
週5日完璧に食事をコントロールできる人のほうが珍しい。

問題は「崩れたこと」じゃない。
「崩れた後にどう戻すかが決まっていないこと」が問題だった。

設計があれば、崩れても戻せます。

↓続き（3/10）""",

    """平日崩れを止めた方法はシンプル。

毎晩1分、翌日の食事を先に決める。

・朝：何を食べるか
・昼：主菜を何にするか
・夜：崩れた時の予備プラン

これだけ。
先に決めてあるから、疲れた日でも迷わない。

↓続き（4/10）""",

    """なぜ「先決め」が効くのか。

心理学者ゴルヴィッツァーの研究（1999）によると、
「いつ・何をするか」を事前に決めた人は
目標達成率が2〜3倍に上がる。

これを Implementation Intentions（実行意図）と呼ぶ。

「健康的に食べよう」より「昼は鶏定食」のほうが実行される。

↓続き（5/10）""",

    """先決めを始めてから起きた変化。

・平日の崩れが週3〜4日→1〜2日に
・帰宅後のつまみ食いが激減
・朝の判断ストレスがゼロに
・3ヶ月で-6kg

やったことは毎晩1分の先決め。それだけ。
100kgから68kgへの-32kgは、こういう小さな習慣の積み上げ。

↓続き（6/10）""",

    """崩れやすい日を先に知っておく。

週の最初に1分、崩れポイントを3つ書く。
・火曜＝会議続きで昼が遅れる
・木曜＝残業で22時帰宅
・金曜＝同僚と外食

反省じゃなく予測。
予測できる崩れは対策できる。

↓続き（7/10）""",

    """対策は1行で十分。

・残業日→味噌汁＋卵＋小ごはん
・外食日→最初に主菜を決める
・昼遅れの日→16時にゆで卵を挟む

複雑にしないほうが現場で使える。
100kgの頃はExcelで完璧な計画を作って水曜に崩壊してた。
今は1行。それが8年続いてる。

↓続き（8/10）""",

    """崩れた日は普通にある。

やらないこと：
「昨日崩れたから今日は食べない」

やること：
次の食事で主菜→副菜→主食に戻す。

100点を狙わなくていい。
70点で戻る。8勝6敗でOK。

↓続き（9/10）""",

    """平日に崩れやすい3つの原因。

①判断の先送り→疲れた脳が楽な選択に流れる
②完璧主義→1回崩れたら全部投げる
③記録のズレ→体重だけ見て行動を見ない

解決は全部同じ。
「先に決めておく」こと。
判断を減らすだけで、崩れにくくなる。

↓続き（10/10）""",

    """【まとめ｜崩れない週次リセット】

✅ 崩れるのは普通。設計があれば戻せる
✅ 反省より「先決め」が効く
✅ 毎晩1分、翌日の食事を先に決める

今夜、寝る前に1分だけ。
→「明日の朝・昼・夜の最初の1手」を決める

あなたは意志が弱いんじゃない。忙しいだけ。

詳しくはnoteに書きました👇
https://note.com/mash_anti_metabo""",
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]


# ═══════════════════════════════════════════════════
# カード1：共感（週次ループ タイムライン）
# ═══════════════════════════════════════════════════
def card_01():
    accent = "#38bdf8"
    days = [
        ("月", "「今週こそ完璧にやる」", "#4ade80"),
        ("火", "会議続き。昼食抜き", "#f59e0b"),
        ("水", "残業→22時にラーメン", "#ef4444"),
        ("木", "「もう今週はいいや」", "#ef4444"),
        ("金", "体重計を見て落ち込む", "#ef4444"),
    ]
    items = ""
    for day, text, col in days:
        items += (
            "<div style='display:flex;align-items:center;margin-bottom:14px;'>"
            "<div style='min-width:56px;height:56px;background:" + col + ";border-radius:12px;"
            "display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:900;color:#000;'>" + day + "</div>"
            "<div style='width:4px;height:40px;background:" + col + ";border-radius:2px;margin:0 16px;'></div>"
            "<div style='font-size:24px;font-weight:600;color:#d1d5db;'>" + text + "</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>1/10</div>"
        "<div class='title'>「また今週もダメだった」を何回繰り返しただろう</div>"
        "<div style='position:absolute;left:56px;top:152px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:76px;right:56px;padding:16px 24px;"
        "background:rgba(239,68,68,.12);border-left:4px solid #ef4444;border-radius:0 8px 8px 0;'>"
        "<span style='font-size:26px;font-weight:800;color:#ef4444;'>「また来週から」を100回言った。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:12px;'>問題は意志じゃなく、設計がなかったこと</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード2：原因（崩れループ フロー図）
# ═══════════════════════════════════════════════════
def card_02():
    accent = "#38bdf8"
    steps = [
        ("① 崩れる（火〜水）", "#1e3a5f"),
        ("② 自己嫌悪が始まる", "#1e3a5f"),
        ("③ 「今週はもういいや」", "#1e3a5f"),
        ("④ 週末に体重を見て後悔", "#1e3a5f"),
        ("⑤ 「来週こそ…」→①に戻る", "#1e3a5f"),
    ]
    items = ""
    for i, (text, bg) in enumerate(steps):
        items += (
            "<div style='display:flex;align-items:center;margin-bottom:6px;'>"
            "<div style='background:" + bg + ";border:2px solid #ef4444;border-radius:10px;"
            "padding:10px 20px;font-size:24px;font-weight:700;color:#fff;flex:1;'>" + text + "</div></div>"
        )
        if i < len(steps) - 1:
            items += "<div style='text-align:center;font-size:28px;color:#ef4444;margin:2px 0 2px 40px;'>↓</div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>2/10</div>"
        "<div class='title'>崩れるのは失敗じゃない。戻し方がないだけ</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:66px;display:flex;align-items:center;gap:12px;'>"
        "<div style='font-size:28px;color:#4ade80;font-weight:700;'>✅ 解決策：</div>"
        "<div style='font-size:22px;color:#9ca3af;'>「崩れた後の戻し方」を先に決めておく</div>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード3：解決策（3ステップカード 横3列）
# ═══════════════════════════════════════════════════
def card_03():
    accent = "#FF6D00"
    cards = [
        ("STEP 1", "崩れポイントを予測", "週の最初に3つ書く", "#FF6D00", "反省じゃなく予測"),
        ("STEP 2", "1行の回避策", "複雑にしない", "#38bdf8", "残業日→味噌汁＋卵"),
        ("STEP 3", "毎晩1分の先決め", "翌日の最初の1手", "#4ade80", "朝＝納豆ごはん"),
    ]
    html = ""
    for i, (step, title, sub, col, ex) in enumerate(cards):
        html += (
            "<div style='flex:1;background:#111d2e;border:2px solid " + col + ";"
            "border-radius:14px;padding:24px 20px;text-align:center;'>"
            "<div style='font-size:20px;font-weight:800;color:" + col + ";margin-bottom:8px;'>" + step + "</div>"
            "<div style='font-size:30px;font-weight:900;color:#fff;margin-bottom:6px;'>" + title + "</div>"
            "<div style='font-size:18px;color:" + col + ";margin-bottom:12px;'>" + sub + "</div>"
            "<div style='font-size:16px;color:#666;'>" + ex + "</div>"
            "</div>"
        )
        if i < 2:
            html += "<div style='display:flex;align-items:center;font-size:36px;color:#fff;padding:0 8px;'>→</div>"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>3/10</div>"
        "<div class='title'>毎晩1分、翌日の食事を先に決めるだけでいい</div>"
        "<div style='position:absolute;left:40px;top:160px;right:40px;display:flex;align-items:stretch;'>"
        + html + "</div>"
        "<div style='position:absolute;left:56px;bottom:76px;'>"
        "<span style='font-size:24px;font-weight:700;color:#FF6D00;'>カロリー計算なし。完璧な計画なし。</span>"
        "<span style='font-size:20px;color:#9ca3af;margin-left:12px;'>先に決めるだけ</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード4：仕組み（科学的根拠 + 番号カード）
# ═══════════════════════════════════════════════════
def card_04():
    accent = "#38bdf8"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>4/10</div>"
        "<div class='title'>なぜ「先決め」が効くのか</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>"
        # 研究カード
        "<div style='background:#111d2e;border:2px solid #38bdf8;border-radius:14px;padding:24px;margin-bottom:20px;'>"
        "<div style='font-size:20px;color:#38bdf8;font-weight:700;margin-bottom:8px;'>📄 Implementation Intentions（実行意図）</div>"
        "<div style='font-size:24px;color:#fff;font-weight:700;margin-bottom:6px;'>「いつ・何をするか」を事前に決めた人は</div>"
        "<div style='font-size:42px;color:#FF6D00;font-weight:900;margin-bottom:6px;'>目標達成率が 2〜3倍</div>"
        "<div style='font-size:18px;color:#9ca3af;'>Gollwitzer PM, American Psychologist, 1999</div>"
        "</div>"
        # 比較
        "<div style='display:flex;gap:16px;'>"
        "<div style='flex:1;background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.3);border-radius:10px;padding:16px;'>"
        "<div style='font-size:20px;font-weight:800;color:#ef4444;margin-bottom:8px;'>❌ 曖昧な決意</div>"
        "<div style='font-size:18px;color:#fca5a5;'>「健康的に食べよう」</div>"
        "<div style='font-size:16px;color:#666;margin-top:4px;'>→ 夜に判断疲れで崩れる</div>"
        "</div>"
        "<div style='flex:1;background:rgba(74,222,128,.08);border:1px solid rgba(74,222,128,.3);border-radius:10px;padding:16px;'>"
        "<div style='font-size:20px;font-weight:800;color:#4ade80;margin-bottom:8px;'>✅ 具体的な先決め</div>"
        "<div style='font-size:18px;color:#86efac;'>「昼は鶏の定食にする」</div>"
        "<div style='font-size:16px;color:#666;margin-top:4px;'>→ 迷わず実行できる</div>"
        "</div>"
        "</div>"
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
    before = [
        "平日3〜4日崩れる",
        "帰宅後つまみ食い",
        "毎朝「何食べよう」で迷う",
        "週末に自己嫌悪",
    ]
    after = [
        "崩れは週1〜2日に",
        "つまみ食い激減",
        "朝の判断ストレスゼロ",
        "3ヶ月で-6kg",
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
        "<div class='title'>毎晩1分の先決めで起きた変化</div>"
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
        "<span style='font-size:48px;font-weight:900;color:#FF6D00;'>-6kg / 3ヶ月</span>"
        "<span style='font-size:20px;color:#9ca3af;'>やったことは毎晩1分の先決めだけ</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード6：設計（崩れポイント予測テーブル）
# ═══════════════════════════════════════════════════
def card_06():
    accent = "#38bdf8"
    rows = [
        ("火曜", "会議続きで昼が遅れる", "16時にゆで卵を挟む"),
        ("水曜", "飲み会の予定あり", "最初に主菜を決める"),
        ("木曜", "残業で22時帰宅", "味噌汁＋卵＋小ごはん"),
        ("金曜", "同僚と外食", "主菜→副菜→主食の順"),
    ]
    header = (
        "<div style='display:flex;background:#1e3a5f;border-radius:10px 10px 0 0;padding:12px 16px;'>"
        "<div style='flex:1;font-size:20px;font-weight:800;color:#fff;'>曜日</div>"
        "<div style='flex:2;font-size:20px;font-weight:800;color:#ef4444;'>崩れポイント</div>"
        "<div style='flex:2;font-size:20px;font-weight:800;color:#4ade80;'>1行の回避策</div>"
        "</div>"
    )
    body = ""
    for i, (day, point, action) in enumerate(rows):
        bg = "#111d2e" if i % 2 == 0 else "#0d1b2a"
        body += (
            "<div style='display:flex;background:" + bg + ";padding:14px 16px;"
            "border-bottom:1px solid #1e3a5f;'>"
            "<div style='flex:1;font-size:22px;font-weight:700;color:#fff;'>" + day + "</div>"
            "<div style='flex:2;font-size:18px;color:#fca5a5;'>" + point + "</div>"
            "<div style='flex:2;font-size:18px;color:#86efac;'>" + action + "</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>6/10</div>"
        "<div class='title'>崩れポイント予測＋1行回避策テーブル</div>"
        "<div style='position:absolute;left:40px;top:148px;right:40px;"
        "border:2px solid #1e3a5f;border-radius:12px;overflow:hidden;'>"
        + header + body + "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;'>"
        "<span style='font-size:22px;color:#FF6D00;font-weight:700;'>反省じゃなく予測。</span>"
        "<span style='font-size:18px;color:#9ca3af;'>予測できる崩れは対策できる</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード7：実践（先決めシート型）
# ═══════════════════════════════════════════════════
def card_07():
    accent = "#FF6D00"
    meals = [
        ("🌅 朝食", "何を食べるか", "納豆ごはん＋味噌汁", "#FF6D00"),
        ("☀️ 昼食", "主菜を何に", "焼き魚定食 or 鶏グリル", "#38bdf8"),
        ("🌙 夜食", "崩れた時の予備", "味噌汁＋卵＋小ごはん", "#4ade80"),
    ]
    items = ""
    for icon, label, example, col in meals:
        items += (
            "<div style='background:#111d2e;border:2px solid " + col + ";border-radius:12px;"
            "padding:18px 24px;margin-bottom:12px;display:flex;align-items:center;gap:16px;'>"
            "<div style='font-size:28px;'>" + icon + "</div>"
            "<div style='flex:1;'>"
            "<div style='font-size:24px;font-weight:800;color:#fff;'>" + label + "</div>"
            "<div style='font-size:18px;color:#666;margin-top:4px;'>例：" + example + "</div>"
            "</div>"
            "<div style='font-size:20px;color:" + col + ";font-weight:700;'>決める</div>"
            "</div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>7/10</div>"
        "<div class='title'>寝る前1分の「先決めシート」</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:72px;'>"
        "<span style='font-size:24px;font-weight:700;color:#FF6D00;'>決めてあるだけで、翌日の判断コストがゼロになる</span>"
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
        ("崩れた日の夜…", "会食・残業・睡眠不足で食べすぎた", "#ef4444", "#1a0a0a"),
        ("❌ やらないこと", "翌日の食事を抜く＝反動で再崩れ", "#ef4444", "#111d2e"),
        ("✅ 翌朝は普通に食べる", "納豆ごはん＋味噌汁でリセット", "#38bdf8", "#111d2e"),
        ("✅ 次の食事で順番を戻す", "主菜→副菜→主食で1食分戻す", "#4ade80", "#111d2e"),
    ]
    items = ""
    for i, (title, sub, col, bg) in enumerate(steps):
        border = "#ef4444" if i <= 1 else col
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
        "<div class='title'>崩れた日の70点リカバリー</div>"
        "<div style='position:absolute;left:56px;top:148px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:68px;'>"
        "<span style='font-size:32px;font-weight:900;color:#FF6D00;'>100点を狙わなくていい。70点で戻る。</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード9：深掘り（3原因の構造図）
# ═══════════════════════════════════════════════════
def card_09():
    accent = "#38bdf8"
    causes = [
        ("①", "判断の先送り", "疲れた脳が楽な選択に流れる", "#ef4444"),
        ("②", "完璧主義", "1回崩れたら全部投げてしまう", "#f59e0b"),
        ("③", "記録のズレ", "体重だけ見て行動を見ない", "#38bdf8"),
    ]
    items = ""
    for num, title, desc, col in causes:
        items += (
            "<div style='display:flex;align-items:flex-start;margin-bottom:20px;'>"
            "<div style='min-width:52px;height:52px;background:" + col + ";border-radius:12px;"
            "display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900;color:#000;'>" + num + "</div>"
            "<div style='margin-left:16px;'>"
            "<div style='font-size:28px;font-weight:800;color:#fff;'>" + title + "</div>"
            "<div style='font-size:20px;color:#9ca3af;margin-top:4px;'>" + desc + "</div>"
            "</div></div>"
        )
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>9/10</div>"
        "<div class='title'>平日に崩れやすい3つの原因</div>"
        "<div style='position:absolute;left:56px;top:152px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:56px;bottom:70px;background:#111d2e;"
        "border:2px solid #4ade80;border-radius:10px;padding:14px 24px;'>"
        "<span style='font-size:22px;font-weight:800;color:#4ade80;'>解決は全部同じ →</span>"
        "<span style='font-size:22px;color:#fff;margin-left:8px;'>「先に決めておく」こと</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:" + accent + ";'>" + HASHTAG + "</p>"
        "</body></html>"
    )


# ═══════════════════════════════════════════════════
# カード10：CTA（まとめチェックリスト）
# ═══════════════════════════════════════════════════
def card_10():
    accent = "#FF6D00"
    checks = [
        ("崩れるのは普通", "設計があれば戻せる", "#38bdf8"),
        ("反省より先決め", "崩れポイントを予測＋1行回避策", "#FF6D00"),
        ("毎晩1分の先決め", "翌日の朝・昼・夜の最初の1手", "#4ade80"),
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
        "<div class='title'>崩れない週次リセット｜まとめ</div>"
        "<div style='position:absolute;left:56px;top:152px;right:56px;'>" + items + "</div>"
        "<div style='position:absolute;left:40px;bottom:76px;right:40px;"
        "background:linear-gradient(135deg,rgba(255,109,0,.15),rgba(255,109,0,.05));"
        "border:2px solid #FF6D00;border-radius:14px;padding:20px 28px;"
        "display:flex;align-items:center;justify-content:space-between;'>"
        "<div>"
        "<div style='font-size:28px;font-weight:900;color:#FF6D00;'>今夜、寝る前に1分だけ。</div>"
        "<div style='font-size:18px;color:#9ca3af;margin-top:4px;'>明日の朝・昼・夜の最初の1手を決める。</div>"
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

