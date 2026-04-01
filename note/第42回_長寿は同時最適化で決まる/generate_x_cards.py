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
HASHTAG = "#第42回 同時最適化"

# ── ツイートテキスト ──────────────────────────────────────
TWEETS = [
    """健診E判定3年連続。
「今度こそ」と糖質制限を始めた。3週間で-2kg。
「これだ！」と思った。

4週間後にはスタートより+1.5kg。

意志が弱いんじゃない。
「1つだけ変える」戦略が人体に合ってないだけ。
↓続き（2/10）""",

    """なぜ「魔法の1手」は続かないか。

4本足の椅子を想像して。
1本だけ伸ばしても椅子は不安定。

人体も同じ。
糖質制限「だけ」→睡眠崩れると夜中の食欲が爆発
運動「だけ」→炎症が高いと回復が遅れて継続できない

1つ直しても他が崩れると全部戻る。
↓続き（3/10）""",

    """解決策は「同時最適化」。

炎症・代謝・睡眠食事・行動継続。
4つを同時に、それぞれ20%ずつ整える。

1つ全力でやるより4つを少しずつの方が
楽で続くしリバウンドしにくい。

理由は「良い連鎖」にある。
↓続き（4/10）""",

    """良い連鎖の仕組み：

睡眠が少し整う
→翌日の食欲コントロールが楽になる
→夜の暴食が減る
→翌朝の運動意欲が上がる
→睡眠の質が上がる

悪い連鎖と同じように良い連鎖もある。
これを意図的に作るのが同時最適化。

（López-Otín et al., Nature Aging 2022）
↓続き（5/10）""",

    """「1つだけ全力」vs「4つを20%ずつ」

❌ 糖質制限のみ
→3週間効果→4週間後リバウンド→前より重い

✅ 睡眠+食事時間+軽運動+就寝固定を20%ずつ
→8年リバウンドなし（僕の実績）

派手さはゼロ。でもこれが一番強い。
↓続き（6/10）""",

    """生物学的年齢は「今何歳相当」より
「変化速度（傾き）」で見る。

追うべき4指標：
・腹囲（週1回・朝起きてすぐ）
・睡眠時刻（就寝・起床を記録）
・活動量（歩数or運動時間）
・飲酒回数（週何回）

悪化してなければ合格。
少しでも改善すれば大成功。
↓続き（7/10）""",

    """食事制限は「準備ができた状態」でやること。

この状態で極端な制限→失敗しやすい：
・睡眠が崩れている
・仕事ストレスが強い
・過去に反動食いを繰り返してきた

正しい順番：
①睡眠時刻を固定する
②夜の食事を前倒しにする
③その後で緩やかに制限
↓続き（8/10）""",

    """崩れた日の翌朝リセット4ステップ。

1️⃣ 体重計に乗らない（2日後でOK）
2️⃣ 朝食は普通に食べる（制限しない）
3️⃣ 5分だけ体を動かす（ストレッチでOK）
4️⃣ 就寝時刻だけ戻す

「全部取り戻そう」とするとまた崩れる。
8勝6敗でOK。
↓続き（9/10）""",

    """運動継続で最も効くのは「事前固定」。

空いたらやる → ほぼ負け
先に枠を取る → 勝ち

推奨：週4枠×20〜30分
+予備日1枠をカレンダーに固定

種目は何でもOK。速歩・自重・ストレッチ。
「迷わないこと」が最優先。

これを10年固定して8年リバウンドなし。
↓続き（10/10）""",

    """今日の行動は1つだけ。

今夜の就寝時刻を決めて
コメントで宣言してください。

（例：23:00就寝、22:45就寝）

ここが整うと明日の行動が整う。
できなかった日は翌日スライドでOK。

詳しくはnoteで👇
https://note.com/mash_anti_metabo""",
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]

# ── 共通CSS ──────────────────────────────────────
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

# ──────────────────────────────────────────────────────────
# カード01：共感 ─ タイムライン型（E判定からの失敗ストーリー）
# ──────────────────────────────────────────────────────────
def card_01():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#38bdf8;}}

.timeline{{position:absolute;top:110px;left:80px;bottom:70px;right:56px;}}
.tl-line{{position:absolute;left:28px;top:0;bottom:0;width:3px;background:rgba(255,255,255,.1);border-radius:2px;}}

.tl-item{{position:relative;margin-bottom:32px;padding-left:72px;}}
.tl-dot{{
  position:absolute;left:18px;top:6px;
  width:22px;height:22px;border-radius:50%;flex-shrink:0;
}}
.tl-time{{font-size:16px;font-weight:700;color:#9ca3af;margin-bottom:4px;}}
.tl-text{{font-size:20px;font-weight:700;color:#fff;line-height:1.4;}}
.tl-sub{{font-size:15px;color:#64748b;margin-top:2px;}}

.dot-orange{{background:#FF6D00;box-shadow:0 0 10px rgba(255,109,0,.5);}}
.dot-blue{{background:#38bdf8;box-shadow:0 0 10px rgba(56,189,248,.5);}}
.dot-red{{background:#ef4444;box-shadow:0 0 10px rgba(239,68,68,.5);}}
.dot-gray{{background:#6b7280;}}
.dot-green{{background:#4ade80;box-shadow:0 0 10px rgba(74,222,128,.5);}}

.series{{color:#38bdf8;}}
</style></head><body>
<div class="main-title">「今度こそ」が崩れ続けた理由</div>
<div class="num">1/10</div>

<div class="timeline">
  <div class="tl-line"></div>

  <div class="tl-item">
    <div class="tl-dot dot-orange"></div>
    <div class="tl-time">健診当日</div>
    <div class="tl-text">E判定。3年連続。封筒を黙って捨てた。</div>
    <div class="tl-sub">「今度こそ変わる」と決意</div>
  </div>

  <div class="tl-item">
    <div class="tl-dot dot-blue"></div>
    <div class="tl-time">翌日〜3週間</div>
    <div class="tl-text">糖質制限を開始。-2kg達成。</div>
    <div class="tl-sub">「これだ！ついに見つけた方法」</div>
  </div>

  <div class="tl-item">
    <div class="tl-dot dot-red"></div>
    <div class="tl-time">4週間後</div>
    <div class="tl-text">リバウンド。開始前より+1.5kg。</div>
    <div class="tl-sub">「また失敗した…。俺には無理なのか」</div>
  </div>

  <div class="tl-item">
    <div class="tl-dot dot-gray"></div>
    <div class="tl-time">以降、繰り返し</div>
    <div class="tl-text">断食・ジム・走り込み。全部同じパターン。</div>
    <div class="tl-sub">「意志が弱いのか？」と自問し続けた</div>
  </div>

  <div class="tl-item">
    <div class="tl-dot dot-green"></div>
    <div class="tl-time">8年後（現在）</div>
    <div class="tl-text">100kg→68kg、8年リバウンドなし。</div>
    <div class="tl-sub">違いは意志ではなく「戦略」だった</div>
  </div>
</div>

<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""

# ──────────────────────────────────────────────────────────
# カード02：原因 ─ 4本足の椅子フロー図
# ──────────────────────────────────────────────────────────
def card_02():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#38bdf8;}}

.chair-wrap{{
  position:absolute;top:110px;left:56px;right:56px;bottom:70px;
  display:flex;align-items:center;gap:40px;
}}
.chair-visual{{
  width:340px;flex-shrink:0;
  display:flex;flex-direction:column;align-items:center;
  gap:12px;
}}
.chair-top{{
  width:280px;height:60px;background:#4a4a4a;border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-size:20px;font-weight:900;color:#fff;
}}
.legs{{display:flex;gap:40px;height:140px;align-items:flex-start;}}
.leg{{
  width:56px;height:130px;border-radius:4px;
  display:flex;align-items:center;justify-content:center;
  font-size:13px;font-weight:700;color:#fff;
  writing-mode:vertical-rl;text-orientation:mixed;
}}
.l1{{background:#ef4444;height:130px;}}
.l2{{background:#38bdf8;height:70px;/* 短い足 */}}
.l3{{background:#4ade80;height:90px;/* 短い足 */}}
.l4{{background:#FF6D00;height:50px;/* 最も短い */}}

.chair-label{{font-size:15px;font-weight:600;color:#9ca3af;text-align:center;}}

.arrow-mid{{font-size:48px;color:#444;flex-shrink:0;}}

.result-box{{
  flex:1;
}}
.result-title{{font-size:22px;font-weight:900;color:#ef4444;margin-bottom:20px;}}
.result-items{{display:flex;flex-direction:column;gap:14px;}}
.r-item{{
  background:rgba(239,68,68,.08);border-left:3px solid #ef4444;
  padding:12px 16px;border-radius:0 8px 8px 0;
}}
.r-item .cause{{font-size:18px;font-weight:700;color:#fff;}}
.r-item .effect{{font-size:14px;color:#9ca3af;margin-top:4px;}}

.ok-hint{{
  margin-top:20px;
  background:rgba(74,222,128,.08);border-left:3px solid #4ade80;
  padding:12px 16px;border-radius:0 8px 8px 0;
  font-size:16px;font-weight:600;color:#4ade80;
}}

.series{{color:#38bdf8;}}
</style></head><body>
<div class="main-title">なぜ「1つだけ変える」は続かないのか</div>
<div class="num">2/10</div>

<div class="chair-wrap">
  <div class="chair-visual">
    <div class="chair-top">あなたの健康</div>
    <div class="legs">
      <div class="leg l1">炎症</div>
      <div class="leg l2">代謝</div>
      <div class="leg l3">睡眠<br>食事</div>
      <div class="leg l4">継続</div>
    </div>
    <div class="chair-label">足の長さがバラバラ<br>= 不安定 = すぐ倒れる</div>
  </div>

  <div class="arrow-mid">→</div>

  <div class="result-box">
    <div class="result-title">✗ 1つだけ頑張ると…</div>
    <div class="result-items">
      <div class="r-item">
        <div class="cause">糖質制限「だけ」</div>
        <div class="effect">→ 睡眠が崩れていると夜中の食欲が爆発</div>
      </div>
      <div class="r-item">
        <div class="cause">運動「だけ」</div>
        <div class="effect">→ 炎症が高いと回復が遅れて継続できない</div>
      </div>
      <div class="r-item">
        <div class="cause">食事管理「だけ」</div>
        <div class="effect">→ ストレス強い期間は翌日の意志力がゼロ</div>
      </div>
    </div>
    <div class="ok-hint">✅ 解決策：4本足を同時に少しずつ伸ばす</div>
  </div>
</div>

<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""

# ──────────────────────────────────────────────────────────
# カード03：解決策 ─ 横3列ステップカード（良い連鎖）
# ──────────────────────────────────────────────────────────
def card_03():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#FF6D00;}}

.steps{{
  position:absolute;top:110px;left:56px;right:56px;
  display:flex;align-items:stretch;gap:0;
}}
.step{{
  flex:1;border-radius:0;padding:24px 18px;
  display:flex;flex-direction:column;align-items:center;text-align:center;
  position:relative;
}}
.step:first-child{{border-radius:16px 0 0 16px;}}
.step:last-child{{border-radius:0 16px 16px 0;}}

.s1{{background:#1e3a5f;border:1.5px solid #38bdf8;border-right:none;}}
.s2{{background:#1a2a10;border:1.5px solid #4ade80;border-left:none;border-right:none;}}
.s3{{background:#2a1000;border:1.5px solid #FF6D00;border-left:none;}}

.arrow-sep{{
  width:30px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-size:32px;color:#555;
  position:relative;z-index:2;
}}

.step-icon{{font-size:40px;margin-bottom:10px;}}
.step-label{{font-size:14px;font-weight:600;padding:4px 12px;border-radius:20px;margin-bottom:12px;}}
.s1 .step-label{{background:rgba(56,189,248,.2);color:#38bdf8;}}
.s2 .step-label{{background:rgba(74,222,128,.2);color:#4ade80;}}
.s3 .step-label{{background:rgba(255,109,0,.2);color:#FF6D00;}}

.step-title{{font-size:22px;font-weight:900;color:#fff;margin-bottom:10px;line-height:1.3;}}
.step-desc{{font-size:14px;color:#9ca3af;line-height:1.6;}}
.step-chain{{
  margin-top:14px;padding:8px 12px;border-radius:8px;
  font-size:13px;font-weight:600;
  background:rgba(255,255,255,.05);color:#e2e8f0;
}}

.bottom{{
  position:absolute;bottom:30px;left:0;right:0;text-align:center;
  font-size:20px;font-weight:900;color:#FF6D00;
}}
.series{{color:#FF6D00;}}
</style></head><body>
<div class="main-title">同時最適化 ─ 良い連鎖を意図的に作る</div>
<div class="num">3/10</div>

<div class="steps">
  <div class="step s1">
    <div class="step-icon">🌙</div>
    <div class="step-label">STEP 1</div>
    <div class="step-title">睡眠時刻を<br>固定する</div>
    <div class="step-desc">まずここだけ。<br>就寝・起床を<br>30分以内の誤差に</div>
    <div class="step-chain">→ 翌日の食欲コントロールが楽になる</div>
  </div>
  <div class="arrow-sep">→</div>
  <div class="step s2">
    <div class="step-icon">🍽️</div>
    <div class="step-label">STEP 2</div>
    <div class="step-title">食事時間を<br>前倒しにする</div>
    <div class="step-desc">就寝3時間前<br>までに食事を終える。<br>カロリー計算より先</div>
    <div class="step-chain">→ 夜の暴食が減る。翌朝スッキリ起きられる</div>
  </div>
  <div class="arrow-sep">→</div>
  <div class="step s3">
    <div class="step-icon">📅</div>
    <div class="step-label">STEP 3</div>
    <div class="step-title">運動枠を<br>先に固定する</div>
    <div class="step-desc">週4枠×20分を<br>カレンダーに先入れ。<br>種目は何でもOK</div>
    <div class="step-chain">→ 睡眠の質が上がる。良い連鎖が完成</div>
  </div>
</div>

<div class="bottom">1つ良くなると他も上がる ─ これが同時最適化の力</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""

# ──────────────────────────────────────────────────────────
# カード04：仕組み ─ 科学的根拠カード（番号バッジ＋出典）
# ──────────────────────────────────────────────────────────
def card_04():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#38bdf8;}}

.cards{{
  position:absolute;top:110px;left:56px;right:56px;bottom:70px;
  display:flex;flex-direction:column;gap:20px;
}}
.sci-card{{
  flex:1;border-radius:12px;padding:18px 20px;
  border:1.5px solid rgba(56,189,248,.2);background:#0d2035;
  display:flex;gap:20px;align-items:center;
}}
.badge{{
  width:48px;height:48px;border-radius:10px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-size:22px;font-weight:900;color:#fff;
}}
.b1{{background:#ef4444;}}
.b2{{background:#38bdf8;}}
.b3{{background:#4ade80;color:#0d1b2a;}}

.content{{flex:1;}}
.finding{{font-size:18px;font-weight:700;color:#fff;line-height:1.4;margin-bottom:6px;}}
.detail{{font-size:14px;color:#9ca3af;line-height:1.5;}}
.source{{
  display:inline-block;margin-top:6px;padding:2px 10px;border-radius:20px;
  font-size:12px;font-weight:600;
  background:rgba(56,189,248,.1);color:#38bdf8;
}}

.series{{color:#38bdf8;}}
</style></head><body>
<div class="main-title">科学が証明する「同時最適化」の根拠</div>
<div class="num">4/10</div>

<div class="cards">
  <div class="sci-card">
    <div class="badge b1">🔥</div>
    <div class="content">
      <div class="finding">炎症マーカーが高い人は10年後の代謝疾患リスクが約2.3倍</div>
      <div class="detail">炎症は睡眠・食事・運動・ストレスが複合的に絡む。1つだけ変えても戻りやすい。</div>
      <div class="source">López-Otín et al., Nature Aging, 2022</div>
    </div>
  </div>

  <div class="sci-card">
    <div class="badge b2">🌙</div>
    <div class="content">
      <div class="finding">同カロリーでも「食べる時間帯」を変えるだけで体重・代謝・炎症に差が出る</div>
      <div class="detail">「何を食べるか」より「いつ食べるか」。就寝3時間前までが目安。</div>
      <div class="source">Hatori et al., Cell Metabolism, 2012</div>
    </div>
  </div>

  <div class="sci-card">
    <div class="badge b3">📅</div>
    <div class="content">
      <div class="finding">「いつ・どこで・どうやって」を事前に決めた群は行動完遂率が約3倍</div>
      <div class="detail">「空いたらやる」ではほぼ負け。先に枠を固定するだけで継続率が劇的に変わる。</div>
      <div class="source">Gollwitzer PM, American Psychologist, 1999</div>
    </div>
  </div>
</div>

<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""

# ──────────────────────────────────────────────────────────
# カード05：効果 ─ Before/After比較パネル
# ──────────────────────────────────────────────────────────
def card_05():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#4ade80;}}

.panels{{
  position:absolute;top:110px;left:56px;right:56px;bottom:70px;
  display:flex;gap:24px;
}}
.panel{{flex:1;border-radius:16px;padding:28px 24px;display:flex;flex-direction:column;gap:16px;}}
.before{{background:rgba(127,29,29,.2);border:1.5px solid #ef4444;}}
.after{{background:rgba(20,83,45,.2);border:1.5px solid #4ade80;}}

.ph{{display:flex;align-items:center;gap:14px;margin-bottom:8px;}}
.ph .badge{{font-size:22px;font-weight:900;padding:6px 14px;border-radius:8px;}}
.before .badge{{background:#ef4444;color:#fff;}}
.after .badge{{background:#4ade80;color:#0d1b2a;}}
.ph .pt{{font-size:20px;font-weight:900;color:#fff;}}

.item{{display:flex;gap:12px;align-items:flex-start;}}
.icon{{font-size:20px;flex-shrink:0;}}
.item-text{{font-size:16px;font-weight:600;color:#e2e8f0;line-height:1.4;}}
.item-sub{{font-size:13px;color:#64748b;margin-top:2px;}}

.result-bar{{
  margin-top:auto;padding:12px 16px;border-radius:10px;
  font-size:17px;font-weight:700;text-align:center;
}}
.before .result-bar{{background:rgba(239,68,68,.15);color:#ef4444;}}
.after .result-bar{{background:rgba(74,222,128,.15);color:#4ade80;}}

.series{{color:#4ade80;}}
</style></head><body>
<div class="main-title">「1つ全力」vs「4つ同時最適化」の現実</div>
<div class="num">5/10</div>

<div class="panels">
  <div class="panel before">
    <div class="ph">
      <div class="badge">BEFORE</div>
      <div class="pt">魔法の1手</div>
    </div>
    <div class="item"><div class="icon">✗</div><div class="item-text">糖質制限3週間で-2kg<div class="item-sub">→ 4週間後にリバウンド、+1.5kg</div></div></div>
    <div class="item"><div class="icon">✗</div><div class="item-text">断食を試みるが空腹で3日で断念<div class="item-sub">→ 反動でその後2日間食べ続ける</div></div></div>
    <div class="item"><div class="icon">✗</div><div class="item-text">ジム通い2ヶ月で挫折<div class="item-sub">→ 「忙しくて行けない」が積み重なる</div></div></div>
    <div class="item"><div class="icon">✗</div><div class="item-text">やるたびに自己嫌悪が増える<div class="item-sub">→ 「俺には無理」と諦めかける</div></div></div>
    <div class="result-bar">8年間で何度も繰り返した</div>
  </div>

  <div class="panel after">
    <div class="ph">
      <div class="badge">AFTER</div>
      <div class="pt">同時最適化</div>
    </div>
    <div class="item"><div class="icon">✓</div><div class="item-text">睡眠時刻を30分早めるだけ<div class="item-sub">→ 翌日の食欲が自然に落ち着く</div></div></div>
    <div class="item"><div class="icon">✓</div><div class="item-text">食事を就寝3時間前までに終える<div class="item-sub">→ 夜の暴食がじわじわ減っていく</div></div></div>
    <div class="item"><div class="icon">✓</div><div class="item-text">週4枠をカレンダーに先固定<div class="item-sub">→ 忙しくても「予約済み」で守れる</div></div></div>
    <div class="item"><div class="icon">✓</div><div class="item-text">崩れた翌日は就寝時刻だけ戻す<div class="item-sub">→ 8勝6敗で8年維持できている</div></div></div>
    <div class="result-bar">100kg→68kg、8年リバウンドなし</div>
  </div>
</div>

<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""

# ──────────────────────────────────────────────────────────
# カード06：設計 ─ 4指標テーブル型
# ──────────────────────────────────────────────────────────
def card_06():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#38bdf8;}}

.table-wrap{{position:absolute;top:110px;left:56px;right:56px;bottom:80px;}}
table{{width:100%;border-collapse:collapse;height:100%;}}
thead tr{{background:#1e3a5f;}}
thead th{{
  padding:14px 16px;font-size:17px;font-weight:700;color:#38bdf8;
  text-align:left;border-bottom:2px solid #38bdf8;
}}
tbody tr{{border-bottom:1px solid rgba(255,255,255,.06);}}
tbody tr:nth-child(odd){{background:rgba(255,255,255,.02);}}
tbody td{{padding:18px 16px;font-size:16px;color:#e2e8f0;vertical-align:middle;}}
.indicator{{font-weight:900;color:#fff;font-size:18px;}}
.freq-badge{{
  display:inline-block;padding:3px 10px;border-radius:20px;
  font-size:13px;font-weight:700;
  background:rgba(255,109,0,.15);color:#FF6D00;
}}
.why{{font-size:13px;color:#64748b;margin-top:3px;}}

.note-box{{
  position:absolute;bottom:20px;left:56px;right:56px;
  background:rgba(74,222,128,.08);border:1.5px solid #4ade80;
  border-radius:10px;padding:12px 20px;
  font-size:16px;font-weight:700;color:#4ade80;text-align:center;
}}
.series{{color:#38bdf8;}}
</style></head><body>
<div class="main-title">生物学的年齢の「傾き」を追う4指標</div>
<div class="num">6/10</div>

<div class="table-wrap">
  <table>
    <thead><tr>
      <th>指標</th><th>測り方</th><th>頻度</th><th>なぜ重要か</th>
    </tr></thead>
    <tbody>
      <tr>
        <td><div class="indicator">🎯 腹囲</div></td>
        <td>朝起きてすぐ、へその高さ</td>
        <td><div class="freq-badge">週1回</div></td>
        <td><div class="why">体重より内臓脂肪を正確に反映</div></td>
      </tr>
      <tr>
        <td><div class="indicator">🌙 睡眠時刻</div></td>
        <td>就寝・起床をメモorアプリ</td>
        <td><div class="freq-badge">毎日</div></td>
        <td><div class="why">炎症・食欲・翌日の行動すべてに影響</div></td>
      </tr>
      <tr>
        <td><div class="indicator">🚶 活動量</div></td>
        <td>スマホ歩数 or 運動時間</td>
        <td><div class="freq-badge">毎日</div></td>
        <td><div class="why">代謝・ミトコンドリア機能の維持</div></td>
      </tr>
      <tr>
        <td><div class="indicator">🍺 飲酒回数</div></td>
        <td>週何回飲んだかを記録</td>
        <td><div class="freq-badge">週1回</div></td>
        <td><div class="why">睡眠の質・肝臓・炎症に直撃</div></td>
      </tr>
    </tbody>
  </table>
</div>

<div class="note-box">悪化してなければ合格 ✓　少しでも改善すれば大成功 ✓✓</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""

# ──────────────────────────────────────────────────────────
# カード07：実践 ─ 縦フロー型（食事制限の正しい順番）
# ──────────────────────────────────────────────────────────
def card_07():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#FF6D00;}}

.flow{{
  position:absolute;top:110px;left:80px;right:80px;bottom:70px;
  display:flex;flex-direction:column;gap:0;
}}
.step-row{{display:flex;align-items:center;gap:20px;}}
.step-num{{
  width:50px;height:50px;border-radius:50%;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-size:20px;font-weight:900;
}}
.step-card{{
  flex:1;border-radius:10px;padding:14px 18px;
  display:flex;justify-content:space-between;align-items:center;
}}
.step-left{{}}
.step-title{{font-size:18px;font-weight:900;color:#fff;}}
.step-sub{{font-size:14px;color:#9ca3af;margin-top:4px;}}
.step-result{{
  font-size:13px;font-weight:600;padding:4px 10px;border-radius:20px;flex-shrink:0;margin-left:10px;
}}

.s1 .step-num{{background:#38bdf8;color:#0d1b2a;}}
.s1 .step-card{{background:#0d2035;border:1px solid rgba(56,189,248,.2);}}
.s1 .step-result{{background:rgba(56,189,248,.15);color:#38bdf8;}}

.s2 .step-num{{background:#a78bfa;color:#fff;}}
.s2 .step-card{{background:#160d2a;border:1px solid rgba(167,139,250,.2);}}
.s2 .step-result{{background:rgba(167,139,250,.15);color:#a78bfa;}}

.s3 .step-num{{background:#4ade80;color:#0d1b2a;}}
.s3 .step-card{{background:#0d2010;border:1px solid rgba(74,222,128,.2);}}
.s3 .step-result{{background:rgba(74,222,128,.15);color:#4ade80;}}

.s4 .step-num{{background:#FF6D00;color:#fff;}}
.s4 .step-card{{background:#2a1000;border:1px solid rgba(255,109,0,.2);}}
.s4 .step-result{{background:rgba(255,109,0,.15);color:#FF6D00;}}

.arrow-down{{text-align:left;margin-left:65px;font-size:22px;color:#333;padding:4px 0;}}

.ng-box{{
  position:absolute;top:110px;right:56px;width:260px;
  background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.3);
  border-radius:10px;padding:14px 16px;
}}
.ng-title{{font-size:15px;font-weight:700;color:#ef4444;margin-bottom:8px;}}
.ng-item{{font-size:13px;color:#9ca3af;margin-bottom:5px;}}

.series{{color:#FF6D00;}}
</style></head><body>
<div class="main-title">食事制限「準備OKチェック」+ 正しい順番</div>
<div class="num">7/10</div>

<div class="flow">
  <div class="step-row s1">
    <div class="step-num">1</div>
    <div class="step-card">
      <div class="step-left">
        <div class="step-title">睡眠時刻を固定する</div>
        <div class="step-sub">就寝・起床を30分以内の誤差に。まずここだけ。</div>
      </div>
      <div class="step-result">最優先</div>
    </div>
  </div>
  <div class="arrow-down">↓</div>
  <div class="step-row s2">
    <div class="step-num">2</div>
    <div class="step-card">
      <div class="step-left">
        <div class="step-title">夜の食事を前倒しにする</div>
        <div class="step-sub">就寝3時間前までに食事終了を目標に。</div>
      </div>
      <div class="step-result">次のステップ</div>
    </div>
  </div>
  <div class="arrow-down">↓</div>
  <div class="step-row s3">
    <div class="step-num">3</div>
    <div class="step-card">
      <div class="step-left">
        <div class="step-title">体が落ち着いたら緩やかに制限</div>
        <div class="step-sub">睡眠と食事時間が安定してから食事量を調整。</div>
      </div>
      <div class="step-result">準備OK後</div>
    </div>
  </div>
  <div class="arrow-down">↓</div>
  <div class="step-row s4">
    <div class="step-num">4</div>
    <div class="step-card">
      <div class="step-left">
        <div class="step-title">崩れたら制限を弱めて継続優先</div>
        <div class="step-sub">「一番強い方法」より「一番続く方法」を選ぶ。</div>
      </div>
      <div class="step-result">継続が最優先</div>
    </div>
  </div>
</div>

<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""

# ──────────────────────────────────────────────────────────
# カード08：復帰 ─ リカバリーフロー（崩れた日4ステップ）
# ──────────────────────────────────────────────────────────
def card_08():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#4ade80;}}

.crash-label{{
  position:absolute;top:100px;left:56px;
  background:rgba(239,68,68,.15);border:1.5px solid #ef4444;
  border-radius:8px;padding:8px 16px;
  font-size:16px;font-weight:700;color:#ef4444;
}}

.steps{{
  position:absolute;top:160px;left:56px;right:56px;
  display:flex;gap:16px;
}}
.step{{
  flex:1;border-radius:12px;padding:20px 16px;
  display:flex;flex-direction:column;align-items:center;text-align:center;
  gap:10px;
}}
.s1{{background:#0d2035;border:1px solid rgba(56,189,248,.2);}}
.s2{{background:#160d2a;border:1px solid rgba(167,139,250,.2);}}
.s3{{background:#0d2010;border:1px solid rgba(74,222,128,.2);}}
.s4{{background:#2a1000;border:1px solid rgba(255,109,0,.2);}}

.step-num{{
  width:44px;height:44px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:18px;font-weight:900;color:#0d1b2a;
}}
.n1{{background:#38bdf8;}}
.n2{{background:#a78bfa;}}
.n3{{background:#4ade80;}}
.n4{{background:#FF6D00;}}

.step-icon{{font-size:28px;}}
.step-title{{font-size:16px;font-weight:900;color:#fff;line-height:1.3;}}
.step-detail{{font-size:13px;color:#9ca3af;line-height:1.5;}}

/* 矢印 */
.arrow{{
  display:flex;align-items:center;justify-content:center;
  font-size:28px;color:#333;flex-shrink:0;
  align-self:center;
}}

.result-box{{
  position:absolute;bottom:24px;left:56px;right:56px;
  background:rgba(74,222,128,.08);border:1.5px solid #4ade80;
  border-radius:12px;padding:14px 24px;text-align:center;
}}
.result-box .r-title{{font-size:20px;font-weight:900;color:#4ade80;}}
.result-box .r-sub{{font-size:14px;color:#9ca3af;margin-top:4px;}}

.series{{color:#4ade80;}}
</style></head><body>
<div class="main-title">崩れた日の翌朝リセット ─ この4つだけ</div>
<div class="num">8/10</div>

<div class="crash-label">⚠️ 崩れた翌朝、「全部取り戻そう」は禁止</div>

<div class="steps">
  <div class="step s1">
    <div class="step-num n1">1</div>
    <div class="step-icon">⚖️</div>
    <div class="step-title">体重計に<br>乗らない</div>
    <div class="step-detail">水分・食事で必ず増える。数字で自己嫌悪になるだけ。1〜2日後でOK</div>
  </div>
  <div class="step s2">
    <div class="step-num n2">2</div>
    <div class="step-icon">🍳</div>
    <div class="step-title">朝食は<br>普通に食べる</div>
    <div class="step-detail">「昨日の分を取り戻そう」と制限しない。空腹が強すぎると夜また崩れる</div>
  </div>
  <div class="step s3">
    <div class="step-num n3">3</div>
    <div class="step-icon">🧘</div>
    <div class="step-title">5分だけ<br>体を動かす</div>
    <div class="step-detail">ストレッチ・その場歩きでOK。「動いた」事実が次の行動を引き出す</div>
  </div>
  <div class="step s4">
    <div class="step-num n4">4</div>
    <div class="step-icon">🌙</div>
    <div class="step-title">就寝時刻<br>だけ戻す</div>
    <div class="step-detail">食事・運動は後でいい。今夜の寝る時刻だけを昨日より30分前に</div>
  </div>
</div>

<div class="result-box">
  <div class="r-title">8勝6敗でOK ─ 1つ戻せば他も戻る</div>
  <div class="r-sub">崩れることが失敗ではない。戻れないことが本当の失敗</div>
</div>

<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""

# ──────────────────────────────────────────────────────────
# カード09：深掘り ─ 事前固定の効果（横棒グラフ比較）
# ──────────────────────────────────────────────────────────
def card_09():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#38bdf8;}}

.content{{position:absolute;top:110px;left:56px;right:56px;bottom:70px;display:flex;gap:40px;}}

.chart-area{{flex:1;display:flex;flex-direction:column;gap:28px;justify-content:center;}}
.chart-row{{}}
.chart-label{{font-size:16px;font-weight:700;color:#fff;margin-bottom:8px;}}
.chart-bar-wrap{{display:flex;align-items:center;gap:12px;}}
.chart-bar{{height:44px;border-radius:0 8px 8px 0;display:flex;align-items:center;padding:0 14px;font-size:16px;font-weight:700;color:#fff;}}
.chart-val{{font-size:16px;font-weight:700;color:#9ca3af;}}

.bar-ng{{background:#ef4444;width:28%;}}
.bar-ok{{background:#4ade80;color:#0d1b2a;width:100%;}}

.divider{{width:1px;background:rgba(255,255,255,.08);}}

.tips-area{{width:320px;display:flex;flex-direction:column;gap:16px;justify-content:center;}}
.tip-card{{
  border-radius:12px;padding:16px 18px;
  border:1px solid rgba(255,255,255,.08);
}}
.t1{{background:#0d2035;}}
.t2{{background:#2a1000;}}
.tip-title{{font-size:16px;font-weight:700;margin-bottom:6px;}}
.t1 .tip-title{{color:#38bdf8;}}
.t2 .tip-title{{color:#FF6D00;}}
.tip-body{{font-size:14px;color:#9ca3af;line-height:1.6;}}

.source-note{{
  position:absolute;bottom:22px;right:56px;
  font-size:13px;color:#444;
}}
.series{{color:#38bdf8;}}
</style></head><body>
<div class="main-title">「事前固定」が運動継続率を3倍にする</div>
<div class="num">9/10</div>

<div class="content">
  <div class="chart-area">
    <div class="chart-row">
      <div class="chart-label">❌ 「空いたらやる」方式</div>
      <div class="chart-bar-wrap">
        <div class="chart-bar bar-ng">28%</div>
        <div class="chart-val">継続率</div>
      </div>
    </div>
    <div class="chart-row">
      <div class="chart-label">✅ 「先に枠を固定」方式</div>
      <div class="chart-bar-wrap">
        <div class="chart-bar bar-ok">91%</div>
        <div class="chart-val">継続率</div>
      </div>
    </div>
    <div style="font-size:14px;color:#64748b;margin-top:8px;">
      出典：Gollwitzer PM, American Psychologist, 1999<br>
      「実施意図理論」─ 事前に決めた群は約3倍の行動完遂率
    </div>
  </div>

  <div class="divider"></div>

  <div class="tips-area">
    <div class="tip-card t1">
      <div class="tip-title">📅 推奨スケジュール</div>
      <div class="tip-body">
        週4枠 × 20〜30分<br>
        ＋ 予備日1枠<br>
        カレンダーに先入れ<br>
        （会議と同格に扱う）
      </div>
    </div>
    <div class="tip-card t2">
      <div class="tip-title">⚡ 種目のルール</div>
      <div class="tip-body">
        何でもOK。<br>
        速歩・自重・ジョグ・ストレッチ。<br>
        「迷わないこと」が最優先。<br>
        完璧より継続。
      </div>
    </div>
  </div>
</div>

<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""

# ──────────────────────────────────────────────────────────
# カード10：CTA ─ チェックリスト＋CTAボックス
# ──────────────────────────────────────────────────────────
def card_10():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.main-title{{position:absolute;top:42px;left:56px;font-size:28px;font-weight:900;color:#fff;}}
.num{{color:#FF6D00;}}

.checklist{{
  position:absolute;top:110px;left:56px;right:56px;
  display:flex;flex-direction:column;gap:16px;
}}
.check-item{{
  display:flex;gap:18px;align-items:center;
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);
  border-radius:12px;padding:16px 20px;
}}
.check-badge{{
  width:40px;height:40px;border-radius:10px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-size:18px;font-weight:900;
}}
.cb1{{background:#38bdf8;color:#0d1b2a;}}
.cb2{{background:#4ade80;color:#0d1b2a;}}
.cb3{{background:#a78bfa;color:#fff;}}

.check-text{{}}
.check-title{{font-size:18px;font-weight:700;color:#fff;}}
.check-sub{{font-size:14px;color:#9ca3af;margin-top:3px;}}

.cta-box{{
  position:absolute;bottom:24px;left:56px;right:56px;
  background:linear-gradient(135deg,rgba(255,109,0,.2) 0%,rgba(255,109,0,.08) 100%);
  border:2px solid #FF6D00;border-radius:16px;
  padding:20px 28px;
  display:flex;justify-content:space-between;align-items:center;
}}
.cta-left{{}}
.cta-main{{font-size:22px;font-weight:900;color:#FF6D00;}}
.cta-sub{{font-size:15px;color:#9ca3af;margin-top:6px;}}
.cta-right{{
  background:#FF6D00;border-radius:10px;padding:10px 20px;
  font-size:16px;font-weight:900;color:#fff;text-align:center;
}}

.series{{color:#FF6D00;}}
</style></head><body>
<div class="main-title">今日からできる実践 ─ 1つだけ選ぶ</div>
<div class="num">10/10</div>

<div class="checklist">
  <div class="check-item">
    <div class="check-badge cb1">1</div>
    <div class="check-text">
      <div class="check-title">今夜の就寝時刻を今すぐ決める</div>
      <div class="check-sub">例：23:00就寝。コメントで宣言するとさらに効果大（Gollwitzer 1999）</div>
    </div>
  </div>
  <div class="check-item">
    <div class="check-badge cb2">2</div>
    <div class="check-text">
      <div class="check-title">今週の運動枠を4つカレンダーに入れる</div>
      <div class="check-sub">種目は後で決めてOK。「先に入れること」が9割</div>
    </div>
  </div>
  <div class="check-item">
    <div class="check-badge cb3">3</div>
    <div class="check-text">
      <div class="check-title">腹囲を今朝計って記録する</div>
      <div class="check-sub">数値より「計った」事実が大事。変化の傾きを追い始める第一歩</div>
    </div>
  </div>
</div>

<div class="cta-box">
  <div class="cta-left">
    <div class="cta-main">詳細はnoteで全文公開中 👇</div>
    <div class="cta-sub">note.com/mash_anti_metabo ｜ 5,000字・科学的根拠付き</div>
  </div>
  <div class="cta-right">今すぐ<br>読む</div>
</div>

<div class="author">マーシー｜100kg→68kg｜Sub3</div>
<div class="series">{HASHTAG}</div>
</body></html>"""

# ── カード関数リスト ──────────────────────────────────────
CARD_FUNCS = [card_01, card_02, card_03, card_04, card_05,
              card_06, card_07, card_08, card_09, card_10]

def save_tweets():
    out = OUTPUT_DIR / "x_posts.md"
    lines = ["# 第42回 X投稿スレッド（10本）\n\n"]
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
    print("第42回 X投稿カード画像（図解版）生成開始...\n")
    for i, func in enumerate(CARD_FUNCS):
        html = func()
        fname = "x_post_" + str(i+1).zfill(2) + ".png"
        render(html, fname)
        print("✅ " + fname + "  [" + CARD_TAGS[i] + "]")
    save_tweets()
    print("\n全10枚完了。保存先: " + str(OUTPUT_DIR))
