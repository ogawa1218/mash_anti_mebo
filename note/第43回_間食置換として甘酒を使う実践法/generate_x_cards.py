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
HASHTAG = "#第43回 甘酒間食置換"

TWEETS = [
    """午後3時。会議が終わった。
気づいたらコンビニでポテチとチョコを握ってレジに並んでいた。

「今日だけ。明日からやめる」
何回言いましたか。

僕は100kgだった頃、週5でこれをやってました。
間食代だけで月1万円。

意志が弱いんじゃなかった。
↓続き（2/10）""",

    """甘いもの欲が止まらない本当の原因。

昼食後に血糖値が急上昇→急降下する。
この「血糖クラッシュ」が15〜17時の
強烈な空腹と甘味欲を引き起こす。
（Ludwig, JAMA 2002）

我慢で消える問題じゃない。
「置き換え先」を用意するかどうかで決まる。
↓続き（3/10）""",

    """答えは「プロテインより甘酒」ではなく
"間食置換として甘酒を設計する"。

筋トレ後→プロテイン一択
15〜17時の間食→甘酒100mlで置換

勝負は「何を飲むか」じゃない。
「どこで何を置き換えるか」。

目的で分ければ両方使ってOK。
↓続き（4/10）""",

    """甘酒置換のメリット3つ。

①甘味欲をゼロにしなくていい
→完全禁止は反動が大きい。中間地点が最強

②ルール化しやすい
→「16時に100ml」の1行で運用できる

③夜のドカ食い予防
→血糖クラッシュを緩めて帰宅後の爆食を減らす

我慢ゼロで夜の崩れが消える仕組み。
↓続き（5/10）""",

    """甘酒の失敗パターンは4つだけ。

❌ コップになみなみ200ml超
❌ 夜11時に「追加」で飲む
❌ チョコと併用（体にいいからと油断）
❌ 量も時間もバラバラ

全部に共通するのは
「健康っぽい追加カロリー」になること。

逆に言えば、ここを固定すれば勝てる。
↓続き（6/10）""",

    """そのまま使える甘酒置換ルール4つ。

① 量を固定：1回100〜150ml
② 時間を固定：15〜17時
③ 単体で終える：お菓子併用禁止
④ 週単位で評価：8勝6敗で合格

紙パック100mlをそのまま飲むのがコツ。
コップに注ぐと「もう少し…」が始まる。
物理的に量を制限する。
↓続き（7/10）""",

    """コスト比較がエグい。

以前の間食：
ポテチ+チョコ+菓子パン＝1日400〜500円
→月10,000円超

甘酒置換後：
1回100〜150円
→月3,000〜4,500円

月5,000円以上浮く。年間6万円。
しかも腹囲も減る。一石二鳥。
↓続き（8/10）""",

    """崩れた日の翌日リセットは2つだけ。

1️⃣ 甘酒を1本買い足す
→ストック切れ＝仕組みの故障

2️⃣ 翌日の15〜17時に1回だけ甘酒に戻す
→「全部やり直し」は禁止

8勝6敗でOK。
1回の成功が次の1週間を作る。
↓続き（9/10）""",

    """プロテインとの共存ルール。

筋トレ後→プロテイン（たんぱく質確保）
15〜17時→甘酒100ml（間食暴走対策）

目的が違えば競合しない。
「どちらが上か」ではなく
「いつ・何を・なぜ使うか」。

両方使ってOKです。
↓続き（10/10）""",

    """今日の行動は1つだけ。

今日か明日の15〜17時に
甘酒100mlを1回だけ試してください。
お菓子なし、単体で。

この「1回の成功」が次の1週間を作ります。

詳しくはnoteで👇
https://note.com/mash_anti_metabo""",
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;background:#0d1b2a;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
    ".num{position:absolute;top:44px;right:56px;font-size:22px;font-weight:700;color:#444;}"
    ".author{position:absolute;bottom:22px;left:56px;font-size:18px;font-weight:400;color:#3a3a3a;}"
    ".series{position:absolute;bottom:22px;right:56px;font-size:18px;font-weight:700;}"
)

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


def card_01():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#38bdf8;}}
.timeline{{position:absolute;top:110px;left:80px;bottom:70px;right:56px;}}
.tl-line{{position:absolute;left:28px;top:0;bottom:0;width:3px;background:rgba(255,255,255,.1);border-radius:2px;}}
.tl-item{{position:relative;margin-bottom:28px;padding-left:72px;}}
.tl-dot{{position:absolute;left:18px;top:6px;width:22px;height:22px;border-radius:50%;}}
.tl-time{{font-size:16px;font-weight:700;color:#9ca3af;margin-bottom:4px;}}
.tl-text{{font-size:19px;font-weight:700;color:#fff;line-height:1.4;}}
.tl-sub{{font-size:14px;color:#64748b;margin-top:2px;}}
.dot-orange{{background:#FF6D00;box-shadow:0 0 10px rgba(255,109,0,.5);}}
.dot-blue{{background:#38bdf8;box-shadow:0 0 10px rgba(56,189,248,.5);}}
.dot-red{{background:#ef4444;box-shadow:0 0 10px rgba(239,68,68,.5);}}
.dot-gray{{background:#6b7280;}}
.dot-green{{background:#4ade80;box-shadow:0 0 10px rgba(74,222,128,.5);}}
.series{{color:#38bdf8;}}
</style></head><body>
<div class="main-title">午後3時、気づいたらポテチを握っていた</div>
<div class="num">1/10</div>
<div class="timeline">
  <div class="tl-line"></div>
  <div class="tl-item"><div class="tl-dot dot-orange"></div><div class="tl-time">15:00</div><div class="tl-text">会議終了。「疲れた…何か甘いもの」</div><div class="tl-sub">コンビニに吸い込まれる</div></div>
  <div class="tl-item"><div class="tl-dot dot-blue"></div><div class="tl-time">15:05</div><div class="tl-text">ポテチ＋チョコ＝400円</div><div class="tl-sub">「今日だけ。明日からやめる」</div></div>
  <div class="tl-item"><div class="tl-dot dot-red"></div><div class="tl-time">21:00</div><div class="tl-text">帰宅後さらにアイス追加</div><div class="tl-sub">夕食後なのに止まらない</div></div>
  <div class="tl-item"><div class="tl-dot dot-gray"></div><div class="tl-time">23:00</div><div class="tl-text">自己嫌悪。「また崩れた…」</div><div class="tl-sub">これを週5で繰り返す。月1万円消失</div></div>
  <div class="tl-item"><div class="tl-dot dot-green"></div><div class="tl-time">解決策</div><div class="tl-text">15時に甘酒100mlを「置換」で入れる</div><div class="tl-sub">我慢ではなく置き換え。月5,000円浮く</div></div>
</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""


def card_02():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#38bdf8;}}
.flow{{position:absolute;top:110px;left:56px;right:56px;bottom:70px;display:flex;flex-direction:column;justify-content:center;gap:0;}}
.step-row{{display:flex;align-items:center;gap:16px;}}
.step-box{{flex:1;border-radius:12px;padding:18px 20px;border:1.5px solid rgba(255,255,255,.08);}}
.s1{{background:#1e3a5f;}}
.s2{{background:#2d1f4e;}}
.s3{{background:#4a1a1a;}}
.s4{{background:#0d2010;}}
.step-title{{font-size:20px;font-weight:900;color:#fff;margin-bottom:4px;}}
.step-desc{{font-size:14px;color:#9ca3af;line-height:1.5;}}
.arrow-d{{text-align:center;font-size:24px;color:#444;padding:6px 0;}}
.source{{position:absolute;bottom:60px;right:56px;font-size:13px;color:#444;background:rgba(56,189,248,.08);padding:4px 12px;border-radius:20px;}}
.series{{color:#38bdf8;}}
</style></head><body>
<div class="main-title">なぜ15時に甘いものが止まらないのか</div>
<div class="num">2/10</div>
<div class="flow">
  <div class="step-row"><div class="step-box s1"><div class="step-title">🍚 昼食後 → 血糖値が急上昇</div><div class="step-desc">炭水化物中心の昼食で血糖スパイクが起きる</div></div></div>
  <div class="arrow-d">↓</div>
  <div class="step-row"><div class="step-box s2"><div class="step-title">📉 14〜15時 → 血糖クラッシュ</div><div class="step-desc">急上昇の反動で血糖値が急降下。強い空腹感と甘味欲が発生</div></div></div>
  <div class="arrow-d">↓</div>
  <div class="step-row"><div class="step-box s3"><div class="step-title">🍫 15〜17時 → コンビニへ直行</div><div class="step-desc">ポテチ＋チョコ＋菓子パン。「意志が弱い」のではなく血糖の問題</div></div></div>
  <div class="arrow-d">↓</div>
  <div class="step-row"><div class="step-box s4"><div class="step-title">✅ 解決：甘酒100mlで血糖を緩やかに補給</div><div class="step-desc">クラッシュを緩め、夜の過食トリガーを弱める</div></div></div>
</div>
<div class="source">Ludwig DS, JAMA, 2002</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""


def card_03():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#FF6D00;}}
.cards{{position:absolute;top:110px;left:56px;right:56px;display:flex;gap:20px;}}
.card{{flex:1;border-radius:14px;padding:24px 20px;display:flex;flex-direction:column;align-items:center;text-align:center;border:1.5px solid rgba(255,255,255,.08);}}
.c1{{background:#0d2035;}}
.c2{{background:#2a1000;}}
.c3{{background:#0d2010;}}
.card .icon{{font-size:44px;margin-bottom:12px;}}
.card .name{{font-size:22px;font-weight:900;color:#fff;margin-bottom:8px;}}
.card .purpose{{font-size:14px;font-weight:600;padding:4px 12px;border-radius:20px;margin-bottom:14px;}}
.c1 .purpose{{background:rgba(56,189,248,.15);color:#38bdf8;}}
.c2 .purpose{{background:rgba(255,109,0,.15);color:#FF6D00;}}
.c3 .purpose{{background:rgba(74,222,128,.15);color:#4ade80;}}
.card .desc{{font-size:14px;color:#9ca3af;line-height:1.6;}}
.card .timing{{margin-top:auto;padding-top:14px;font-size:13px;font-weight:700;color:#fff;border-top:1px solid rgba(255,255,255,.06);width:100%;}}
.bottom{{position:absolute;bottom:30px;left:0;right:0;text-align:center;font-size:19px;font-weight:900;color:#FF6D00;}}
.series{{color:#FF6D00;}}
</style></head><body>
<div class="main-title">目的で使い分ける ─ 二択問題にしない</div>
<div class="num">3/10</div>
<div class="cards">
  <div class="card c1"><div class="icon">💪</div><div class="name">プロテイン</div><div class="purpose">筋量維持</div><div class="desc">筋トレ後のたんぱく質確保。<br>20〜30g摂れる。<br>甘酒では代替不可。</div><div class="timing">⏰ 筋トレ後・朝食時</div></div>
  <div class="card c2"><div class="icon">🍶</div><div class="name">甘酒（置換）</div><div class="purpose">間食暴走対策</div><div class="desc">100〜150mlで甘味欲を整える。<br>血糖クラッシュを緩め<br>夜の過食を予防。</div><div class="timing">⏰ 15〜17時</div></div>
  <div class="card c3"><div class="icon">🤝</div><div class="name">両方使う</div><div class="purpose">タイミングで分離</div><div class="desc">目的が違えば競合しない。<br>筋トレ後→プロテイン<br>15時→甘酒</div><div class="timing">⏰ 使い分けるだけ</div></div>
</div>
<div class="bottom">「どちらが上か」ではなく「いつ・何を・なぜ使うか」</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""


def card_04():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#38bdf8;}}
.cards{{position:absolute;top:110px;left:56px;right:56px;bottom:70px;display:flex;flex-direction:column;gap:16px;}}
.sci-card{{flex:1;border-radius:12px;padding:16px 20px;border:1.5px solid rgba(56,189,248,.2);background:#0d2035;display:flex;gap:18px;align-items:center;}}
.badge{{width:44px;height:44px;border-radius:10px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:900;color:#fff;}}
.b1{{background:#38bdf8;color:#0d1b2a;}}
.b2{{background:#4ade80;color:#0d1b2a;}}
.b3{{background:#FF6D00;}}
.content{{flex:1;}}
.finding{{font-size:17px;font-weight:700;color:#fff;line-height:1.4;margin-bottom:4px;}}
.detail{{font-size:13px;color:#9ca3af;line-height:1.5;}}
.series{{color:#38bdf8;}}
</style></head><body>
<div class="main-title">間食置換が効く3つの理由</div>
<div class="num">4/10</div>
<div class="cards">
  <div class="sci-card"><div class="badge b1">①</div><div class="content"><div class="finding">甘味欲をゼロにしなくていい</div><div class="detail">完全禁止→反動で爆食。甘酒は「ゼロか100か」を避ける中間地点。我慢している感覚がないから続く。</div></div></div>
  <div class="sci-card"><div class="badge b2">②</div><div class="content"><div class="finding">「16時に100ml」の1行でルール化完了</div><div class="detail">量・時間・種類が決まっている→毎回悩まない。悩まないことが続く秘訣。再現性が高い。</div></div></div>
  <div class="sci-card"><div class="badge b3">③</div><div class="content"><div class="finding">夜のドカ食い予防に直結</div><div class="detail">血糖クラッシュ（15〜17時）を甘酒で緩めると、帰宅後の爆食トリガーが弱まる。（Ludwig, JAMA 2002）</div></div></div>
</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""


def card_05():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#4ade80;}}
.panels{{position:absolute;top:110px;left:56px;right:56px;bottom:70px;display:flex;gap:24px;}}
.panel{{flex:1;border-radius:16px;padding:24px 20px;display:flex;flex-direction:column;gap:14px;}}
.before{{background:rgba(127,29,29,.2);border:1.5px solid #ef4444;}}
.after{{background:rgba(20,83,45,.2);border:1.5px solid #4ade80;}}
.ph{{display:flex;align-items:center;gap:12px;margin-bottom:6px;}}
.ph .badge{{font-size:20px;font-weight:900;padding:5px 12px;border-radius:8px;}}
.before .badge{{background:#ef4444;color:#fff;}}
.after .badge{{background:#4ade80;color:#0d1b2a;}}
.ph .pt{{font-size:18px;font-weight:900;color:#fff;}}
.item{{display:flex;gap:10px;align-items:flex-start;}}
.icon{{font-size:18px;flex-shrink:0;}}
.item-text{{font-size:15px;font-weight:600;color:#e2e8f0;line-height:1.4;}}
.item-sub{{font-size:12px;color:#64748b;margin-top:2px;}}
.result-bar{{margin-top:auto;padding:10px 14px;border-radius:10px;font-size:16px;font-weight:700;text-align:center;}}
.before .result-bar{{background:rgba(239,68,68,.15);color:#ef4444;}}
.after .result-bar{{background:rgba(74,222,128,.15);color:#4ade80;}}
.series{{color:#4ade80;}}
</style></head><body>
<div class="main-title">Before/After ─ 間食のコストと量が激変</div>
<div class="num">5/10</div>
<div class="panels">
  <div class="panel before">
    <div class="ph"><div class="badge">BEFORE</div><div class="pt">コンビニ間食</div></div>
    <div class="item"><div class="icon">✗</div><div class="item-text">ポテチ＋チョコ＋菓子パン<div class="item-sub">→ 1日400〜500円、月10,000円超</div></div></div>
    <div class="item"><div class="icon">✗</div><div class="item-text">カロリー500〜700kcal<div class="item-sub">→ 夕食1食分のカロリーが間食で消える</div></div></div>
    <div class="item"><div class="icon">✗</div><div class="item-text">血糖スパイク→クラッシュ→夜食<div class="item-sub">→ 間食が夜の暴食を誘発する悪循環</div></div></div>
    <div class="item"><div class="icon">✗</div><div class="item-text">「今日だけ」を週5で繰り返す<div class="item-sub">→ 自己嫌悪ループ</div></div></div>
    <div class="result-bar">年間12万円＋体重増加</div>
  </div>
  <div class="panel after">
    <div class="ph"><div class="badge">AFTER</div><div class="pt">甘酒置換</div></div>
    <div class="item"><div class="icon">✓</div><div class="item-text">甘酒100ml（紙パック1本）<div class="item-sub">→ 1回100〜150円、月3,000〜4,500円</div></div></div>
    <div class="item"><div class="icon">✓</div><div class="item-text">カロリー約76kcal<div class="item-sub">→ お菓子の1/7〜1/9のカロリー</div></div></div>
    <div class="item"><div class="icon">✓</div><div class="item-text">血糖を緩やかに補給→夜の崩れ減<div class="item-sub">→ 帰宅後の爆食トリガーが弱まる</div></div></div>
    <div class="item"><div class="icon">✓</div><div class="item-text">ルール化されて悩まない<div class="item-sub">→ 8勝6敗で合格</div></div></div>
    <div class="result-bar">年間6万円節約＋腹囲減少</div>
  </div>
</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""


def card_06():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#38bdf8;}}
.table-wrap{{position:absolute;top:110px;left:56px;right:56px;bottom:70px;}}
table{{width:100%;border-collapse:collapse;}}
thead tr{{background:#1e3a5f;}}
thead th{{padding:14px 16px;font-size:16px;font-weight:700;color:#38bdf8;text-align:left;border-bottom:2px solid #38bdf8;}}
tbody tr{{border-bottom:1px solid rgba(255,255,255,.06);}}
tbody tr:nth-child(odd){{background:rgba(255,255,255,.02);}}
tbody td{{padding:18px 16px;font-size:15px;color:#e2e8f0;vertical-align:middle;}}
.rule-name{{font-weight:900;color:#fff;font-size:17px;}}
.rule-detail{{color:#9ca3af;font-size:13px;margin-top:3px;}}
.badge{{display:inline-block;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:700;background:rgba(255,109,0,.15);color:#FF6D00;}}
.series{{color:#38bdf8;}}
</style></head><body>
<div class="main-title">甘酒置換ルール ─ 実践早見表</div>
<div class="num">6/10</div>
<div class="table-wrap">
  <table>
    <thead><tr><th>ルール</th><th>内容</th><th>コツ</th></tr></thead>
    <tbody>
      <tr><td><div class="rule-name">① 量を固定</div></td><td>1回 100〜150ml<div class="rule-detail">紙パック1本。おかわり禁止</div></td><td><div class="badge">物理的に制限</div></td></tr>
      <tr><td><div class="rule-name">② 時間を固定</div></td><td>15〜17時<div class="rule-detail">夜食なら就寝2時間前まで</div></td><td><div class="badge">血糖クラッシュ対策</div></td></tr>
      <tr><td><div class="rule-name">③ 単体で終える</div></td><td>お菓子併用禁止<div class="rule-detail">置換なので追加しない</div></td><td><div class="badge">追加カロリー防止</div></td></tr>
      <tr><td><div class="rule-name">④ 週単位で評価</div></td><td>8勝6敗で合格<div class="rule-detail">崩れた翌日に戻せばOK</div></td><td><div class="badge">完璧より継続</div></td></tr>
    </tbody>
  </table>
</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""


def card_07():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#FF6D00;}}
.content{{position:absolute;top:110px;left:56px;right:56px;bottom:70px;display:flex;gap:36px;}}
.chart-area{{flex:1;display:flex;flex-direction:column;gap:24px;justify-content:center;}}
.chart-row{{}}
.chart-label{{font-size:15px;font-weight:700;color:#fff;margin-bottom:8px;}}
.chart-bar-wrap{{display:flex;align-items:center;gap:12px;}}
.chart-bar{{height:44px;border-radius:0 8px 8px 0;display:flex;align-items:center;padding:0 14px;font-size:16px;font-weight:700;color:#fff;}}
.bar-ng{{background:#ef4444;width:100%;}}
.bar-ok{{background:#4ade80;color:#0d1b2a;width:40%;}}
.bar-save{{background:#FF6D00;width:60%;margin-top:20px;}}
.divider{{width:1px;background:rgba(255,255,255,.08);}}
.tips-area{{width:300px;display:flex;flex-direction:column;gap:14px;justify-content:center;}}
.tip-card{{border-radius:12px;padding:14px 16px;border:1px solid rgba(255,255,255,.08);}}
.t1{{background:#0d2035;}}
.t2{{background:#2a1000;}}
.tip-title{{font-size:15px;font-weight:700;margin-bottom:4px;}}
.t1 .tip-title{{color:#38bdf8;}}
.t2 .tip-title{{color:#FF6D00;}}
.tip-body{{font-size:13px;color:#9ca3af;line-height:1.6;}}
.series{{color:#FF6D00;}}
</style></head><body>
<div class="main-title">コスト比較 ─ 月5,000円以上浮く</div>
<div class="num">7/10</div>
<div class="content">
  <div class="chart-area">
    <div class="chart-row"><div class="chart-label">❌ コンビニ間食（以前）</div><div class="chart-bar-wrap"><div class="chart-bar bar-ng">月10,000円超</div></div></div>
    <div class="chart-row"><div class="chart-label">✅ 甘酒置換（現在）</div><div class="chart-bar-wrap"><div class="chart-bar bar-ok">月3,000〜4,500円</div></div></div>
    <div class="chart-row"><div class="chart-bar-wrap"><div class="chart-bar bar-save">💰 月5,000円以上の節約</div></div></div>
    <div style="font-size:14px;color:#64748b;margin-top:12px;">年間6万円。しかも腹囲も減る。一石二鳥。</div>
  </div>
  <div class="divider"></div>
  <div class="tips-area">
    <div class="tip-card t1"><div class="tip-title">📊 カロリー比較</div><div class="tip-body">ポテチ+チョコ+菓子パン<br>= 500〜700kcal<br><br>甘酒100ml<br>= 約76kcal<br><br>1/7〜1/9のカロリー</div></div>
    <div class="tip-card t2"><div class="tip-title">⚡ 運用のコツ</div><div class="tip-body">紙パック100mlを箱買い。<br>デスクに3本常備。<br>「買いに行く手間」を<br>先に消しておく。</div></div>
  </div>
</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""


def card_08():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#4ade80;}}
.crash-label{{position:absolute;top:100px;left:56px;background:rgba(239,68,68,.15);border:1.5px solid #ef4444;border-radius:8px;padding:8px 16px;font-size:16px;font-weight:700;color:#ef4444;}}
.steps{{position:absolute;top:170px;left:56px;right:56px;display:flex;gap:24px;}}
.step{{flex:1;border-radius:14px;padding:28px 20px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px;}}
.s1{{background:#0d2035;border:1.5px solid rgba(56,189,248,.2);}}
.s2{{background:#2a1000;border:1.5px solid rgba(255,109,0,.2);}}
.step-num{{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;}}
.n1{{background:#38bdf8;color:#0d1b2a;}}
.n2{{background:#FF6D00;color:#fff;}}
.step-icon{{font-size:36px;}}
.step-title{{font-size:20px;font-weight:900;color:#fff;line-height:1.3;}}
.step-detail{{font-size:14px;color:#9ca3af;line-height:1.6;}}
.result-box{{position:absolute;bottom:28px;left:56px;right:56px;background:rgba(74,222,128,.08);border:1.5px solid #4ade80;border-radius:12px;padding:16px 24px;text-align:center;}}
.result-box .r-title{{font-size:20px;font-weight:900;color:#4ade80;}}
.result-box .r-sub{{font-size:14px;color:#9ca3af;margin-top:4px;}}
.series{{color:#4ade80;}}
</style></head><body>
<div class="main-title">崩れた日の翌日リセット ─ 2つだけ</div>
<div class="num">8/10</div>
<div class="crash-label">⚠️ コンビニに寄った / お菓子を食べた / 甘酒を切らしていた</div>
<div class="steps">
  <div class="step s1"><div class="step-num n1">1</div><div class="step-icon">🍶</div><div class="step-title">甘酒を<br>1本買い足す</div><div class="step-detail">ストック切れ＝仕組みの故障。<br>帰り道のコンビニかスーパーで<br>1本だけ買う。<br>物理的に「ない」をなくす。</div></div>
  <div class="step s2"><div class="step-num n2">2</div><div class="step-icon">⏰</div><div class="step-title">翌日15〜17時に<br>1回だけ戻す</div><div class="step-detail">全部やり直す必要なし。<br>「1回の成功」が<br>次の1週間を作る。<br>この1回がリズムを復旧させる。</div></div>
</div>
<div class="result-box">
  <div class="r-title">8勝6敗でOK ─ 1回戻せば他も戻る</div>
  <div class="r-sub">崩れることが失敗ではない。戻れないことが本当の失敗</div>
</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""


def card_09():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#38bdf8;}}
.content-area{{position:absolute;top:110px;left:56px;right:56px;bottom:70px;display:flex;gap:32px;}}
.left{{flex:1;display:flex;flex-direction:column;gap:16px;}}
.right{{flex:1;display:flex;flex-direction:column;gap:16px;}}

.nutrient-card{{border-radius:12px;padding:16px 18px;border:1px solid rgba(255,255,255,.08);background:#0d2035;}}
.n-title{{font-size:16px;font-weight:700;color:#38bdf8;margin-bottom:8px;}}
.n-body{{font-size:14px;color:#9ca3af;line-height:1.6;}}

.timing-card{{border-radius:12px;padding:16px 18px;border:1px solid rgba(255,255,255,.08);background:#2a1000;}}
.t-title{{font-size:16px;font-weight:700;color:#FF6D00;margin-bottom:8px;}}
.t-body{{font-size:14px;color:#9ca3af;line-height:1.6;}}

.source-badge{{display:inline-block;margin-top:6px;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:600;background:rgba(56,189,248,.1);color:#38bdf8;}}
.series{{color:#38bdf8;}}
</style></head><body>
<div class="main-title">プロテインとの共存 ─ 目的で使い分ける</div>
<div class="num">9/10</div>
<div class="content-area">
  <div class="left">
    <div class="nutrient-card">
      <div class="n-title">💪 プロテインの役割</div>
      <div class="n-body">
        ・筋トレ後のたんぱく質補給<br>
        ・1回で20〜30gのたんぱく質<br>
        ・筋量維持に不可欠<br>
        ・甘酒では代替できない領域<br><br>
        ⏰ タイミング：筋トレ後・朝食時
      </div>
    </div>
    <div class="nutrient-card">
      <div class="n-title">📊 米麹甘酒100mlの中身</div>
      <div class="n-body">
        エネルギー：約76kcal<br>
        糖質：約17g<br>
        たんぱく質：約1.7g<br>
        ビタミンB1・B2・B6<br>
        アミノ酸・オリゴ糖
      </div>
    </div>
  </div>
  <div class="right">
    <div class="timing-card">
      <div class="t-title">🍶 甘酒の役割</div>
      <div class="t-body">
        ・間食暴走の置換ツール<br>
        ・甘味欲をゼロにせず整える<br>
        ・血糖クラッシュを緩める<br>
        ・夜の過食トリガーを弱める<br><br>
        ⏰ タイミング：15〜17時
      </div>
    </div>
    <div class="timing-card">
      <div class="t-title">🤝 両立ルール</div>
      <div class="t-body">
        目的が違えば競合しない。<br>
        筋トレ後 → プロテイン<br>
        15〜17時 → 甘酒100ml<br><br>
        「どちらが上か」ではなく<br>
        「いつ・何を・なぜ」で決める
      </div>
      <div class="source-badge">Jakubowicz et al., Steroids, 2012</div>
    </div>
  </div>
</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""


def card_10():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#FF6D00;}}
.checklist{{position:absolute;top:110px;left:56px;right:56px;display:flex;flex-direction:column;gap:16px;}}
.check-item{{display:flex;gap:18px;align-items:center;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:16px 20px;}}
.check-badge{{width:40px;height:40px;border-radius:10px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:900;}}
.cb1{{background:#38bdf8;color:#0d1b2a;}}
.cb2{{background:#4ade80;color:#0d1b2a;}}
.cb3{{background:#a78bfa;color:#fff;}}
.check-text{{}}
.check-title{{font-size:18px;font-weight:700;color:#fff;}}
.check-sub{{font-size:14px;color:#9ca3af;margin-top:3px;}}
.cta-box{{position:absolute;bottom:24px;left:56px;right:56px;background:linear-gradient(135deg,rgba(255,109,0,.2) 0%,rgba(255,109,0,.08) 100%);border:2px solid #FF6D00;border-radius:16px;padding:20px 28px;display:flex;justify-content:space-between;align-items:center;}}
.cta-left{{}}
.cta-main{{font-size:22px;font-weight:900;color:#FF6D00;}}
.cta-sub{{font-size:15px;color:#9ca3af;margin-top:6px;}}
.cta-right{{background:#FF6D00;border-radius:10px;padding:10px 20px;font-size:16px;font-weight:900;color:#fff;text-align:center;}}
.series{{color:#FF6D00;}}
</style></head><body>
<div class="main-title">今日からできる実践 ─ 1つだけ選ぶ</div>
<div class="num">10/10</div>
<div class="checklist">
  <div class="check-item"><div class="check-badge cb1">1</div><div class="check-text"><div class="check-title">今日の15〜17時に甘酒100mlを1回だけ試す</div><div class="check-sub">お菓子なし・単体で。この「1回の成功」が次の1週間を作る</div></div></div>
  <div class="check-item"><div class="check-badge cb2">2</div><div class="check-text"><div class="check-title">甘酒を3本買ってデスクに常備する</div><div class="check-sub">「ないから買えない」をなくす。仕組みの第一歩</div></div></div>
  <div class="check-item"><div class="check-badge cb3">3</div><div class="check-text"><div class="check-title">1週間の間食代を計算してみる</div><div class="check-sub">ポテチ+チョコ+菓子パンの合計が見えると動きやすい</div></div></div>
</div>
<div class="cta-box">
  <div class="cta-left"><div class="cta-main">詳細はnoteで全文公開中 👇</div><div class="cta-sub">note.com/mash_anti_metabo ｜ 5,000字・科学的根拠付き</div></div>
  <div class="cta-right">今すぐ<br>読む</div>
</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""


CARD_FUNCS = [card_01, card_02, card_03, card_04, card_05,
              card_06, card_07, card_08, card_09, card_10]

def save_tweets():
    out = OUTPUT_DIR / "x_posts.md"
    lines = ["# 第43回 X投稿スレッド（10本）\n\n"]
    for i, tweet in enumerate(TWEETS):
        tag = CARD_TAGS[i]
        fname = "x_post_" + str(i+1).zfill(2) + ".png"
        lines.append(
            "## 投稿" + str(i+1) + "/10｜" + tag + "\n\n```\n" + tweet.strip() + "\n```\n\n"
            "![カード" + str(i+1) + "](" + fname + ")\n\n---\n\n"
        )
    out.write_text("".join(lines), encoding="utf-8")
    print("✅ x_posts.md 保存完了")

if __name__ == "__main__":
    print("第43回 X投稿カード画像（図解版）生成開始...\n")
    for i, func in enumerate(CARD_FUNCS):
        html = func()
        fname = "x_post_" + str(i+1).zfill(2) + ".png"
        render(html, fname)
        print("✅ " + fname + "  [" + CARD_TAGS[i] + "]")
    save_tweets()
    print("\n全10枚完了。保存先: " + str(OUTPUT_DIR))
