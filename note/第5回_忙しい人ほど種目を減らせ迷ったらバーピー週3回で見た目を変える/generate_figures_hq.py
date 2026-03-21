#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 図解 高品質生成スクリプト
HTML/CSS + Playwright（Chromiumヘッドレス）版
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images"
OUTPUT_DIR.mkdir(exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

# ============================================================
# 共通CSS
# ============================================================
BASE = f"""
@font-face {{
  font-family: 'NotoSansJP';
  src: url('{FONT}');
  font-weight: 100 900;
}}
* {{ margin:0; padding:0; box-sizing:border-box;
     font-family:'NotoSansJP','Meiryo',sans-serif;
     -webkit-font-smoothing:antialiased; }}
:root {{
  --orange:#FF6D00; --orange-g:rgba(255,109,0,.35);
  --blue:#38bdf8;   --blue-g:rgba(56,189,248,.3);
  --green:#4ade80;  --green-g:rgba(74,222,128,.3);
  --red:#ef4444;    --red-g:rgba(239,68,68,.3);
  --navy:#1A2A3A;
  --panel:#27292d;  --panel2:#1e2431;
  --text:#FFFFFF;   --muted:#7a7e8a; --sub:#d4d6db;
  --border:rgba(255,255,255,.08);
}}
body {{
  width:1280px; height:720px; overflow:hidden;
  background:var(--navy); color:var(--text); position:relative;
}}
body::before {{
  content:''; position:absolute; inset:0; pointer-events:none;
  background-image:
    linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.018) 1px,transparent 1px);
  background-size:52px 52px;
}}
"""

# ============================================================
# 図解① バーピー1種目 vs 複数種目 比較
# ============================================================
HTML1 = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE}
h1{{position:absolute;top:18px;left:0;right:0;
    font-size:42px;font-weight:900;text-align:center;color:#FFFFFF;
    letter-spacing:-.3px;}}

/* 左半分 */
.left{{position:absolute;left:44px;top:80px;width:544px;bottom:72px;
       background:linear-gradient(145deg,#1e2a3a,#162030);
       border-radius:20px;border:1px solid rgba(255,109,0,.25);
       padding:22px 24px;
       box-shadow:0 20px 60px rgba(0,0,0,.4),
                  inset 0 1px 0 rgba(255,255,255,.05);}}
.left::before{{content:'';position:absolute;top:0;left:20px;right:20px;height:2px;
               background:linear-gradient(90deg,transparent,var(--orange),transparent);
               border-radius:2px;}}
.lbl-a{{font-size:22px;font-weight:800;color:var(--orange);margin-bottom:14px;
        text-shadow:0 0 20px var(--orange-g);}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;}}
.gc{{background:rgba(255,255,255,.05);border-radius:12px;padding:14px 16px;
     border-left:3px solid var(--blue);}}
.gc-icon{{font-size:26px;margin-bottom:6px;}}
.gc-name{{font-size:20px;font-weight:800;color:var(--blue);}}
.gc-note{{font-size:14px;color:var(--muted);margin-top:3px;}}
.left-bottom{{font-size:24px;font-weight:900;color:var(--orange);text-align:center;
              padding:10px 0;text-shadow:0 0 20px var(--orange-g);}}

/* 中央 = */
.eq{{position:absolute;left:50%;transform:translateX(-50%);top:50%;
     margin-top:-24px;width:56px;height:56px;
     display:flex;align-items:center;justify-content:center;
     font-size:40px;font-weight:900;color:rgba(255,255,255,.4);}}

/* 右半分 */
.right{{position:absolute;right:44px;top:80px;width:544px;bottom:72px;
        background:linear-gradient(145deg,#1a1d24,#14171e);
        border-radius:20px;border:1px solid rgba(255,255,255,.07);
        padding:22px 24px;}}
.lbl-b{{font-size:22px;font-weight:800;color:var(--muted);margin-bottom:14px;}}
.row-item{{display:flex;align-items:center;
           background:rgba(255,255,255,.03);border-radius:10px;
           padding:12px 16px;margin-bottom:10px;
           border:1px dashed rgba(99,102,110,.4);}}
.ri-name{{font-size:20px;font-weight:700;color:#9ca3af;flex:1;}}
.ri-tag{{font-size:14px;font-weight:600;color:var(--green);white-space:nowrap;
         text-shadow:0 0 10px var(--green-g);}}
.right-bottom{{font-size:17px;color:var(--muted);text-align:center;
               margin-top:12px;}}

/* フッター */
.foot{{position:absolute;bottom:16px;left:0;right:0;text-align:center;
       font-size:22px;font-weight:900;color:var(--orange);
       text-shadow:0 0 20px var(--orange-g);}}
</style></head><body>
<h1>バーピー1種目で、これだけ動く</h1>

<div class="left">
  <div class="lbl-a">バーピー 1種目</div>
  <div class="grid">
    <div class="gc">
      <div class="gc-icon">🦵</div>
      <div class="gc-name">下半身</div>
      <div class="gc-note">スクワット相当</div>
    </div>
    <div class="gc">
      <div class="gc-icon">💪</div>
      <div class="gc-name">上半身</div>
      <div class="gc-note">腕立て相当</div>
    </div>
    <div class="gc">
      <div class="gc-icon">🔥</div>
      <div class="gc-name">体幹</div>
      <div class="gc-note">プランク相当</div>
    </div>
    <div class="gc">
      <div class="gc-icon">❤️</div>
      <div class="gc-name">心肺</div>
      <div class="gc-note">有酸素相当</div>
    </div>
  </div>
  <div class="left-bottom">まとめて取れる</div>
</div>

<div class="eq">=</div>

<div class="right">
  <div class="lbl-b">従来のやり方 4種目</div>
  <div class="row-item">
    <span class="ri-name">スクワット</span>
    <span class="ri-tag">→ バーピーに含まれる</span>
  </div>
  <div class="row-item">
    <span class="ri-name">腕立て伏せ</span>
    <span class="ri-tag">→ バーピーに含まれる</span>
  </div>
  <div class="row-item">
    <span class="ri-name">プランク</span>
    <span class="ri-tag">→ バーピーに含まれる</span>
  </div>
  <div class="row-item">
    <span class="ri-name">有酸素運動（ジョギング等）</span>
    <span class="ri-tag">→ バーピーに含まれる</span>
  </div>
  <div class="right-bottom">それぞれ別に考える必要あり</div>
</div>

<div class="foot">迷ったらバーピー。それだけ決めておけばいい。</div>
</body></html>"""

# ============================================================
# 図解② 1週間の運動設計図（週間カレンダー型）
# ============================================================
HTML2 = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE}
h1{{position:absolute;top:14px;left:0;right:0;
    font-size:40px;font-weight:900;text-align:center;color:#FFFFFF;}}
.sub{{position:absolute;top:64px;left:0;right:0;
      font-size:20px;color:var(--muted);text-align:center;}}

/* カレンダー行 */
.cal{{position:absolute;top:104px;left:28px;right:28px;
      display:flex;gap:10px;height:410px;}}
.day{{flex:1;border-radius:16px;padding:16px 10px;
      display:flex;flex-direction:column;align-items:center;
      position:relative;}}

/* HIITデイ */
.hiit{{background:linear-gradient(180deg,#1e2a1a,#192218);
       border:1px solid rgba(255,109,0,.3);
       box-shadow:0 0 30px rgba(255,109,0,.08);}}
.hiit::before{{content:'';position:absolute;left:0;top:0;bottom:0;
               width:3px;background:var(--orange);border-radius:3px 0 0 3px;}}
.hiit-tag{{font-size:15px;font-weight:800;color:var(--orange);
           background:rgba(255,109,0,.12);border-radius:6px;
           padding:3px 8px;margin-bottom:10px;
           text-shadow:0 0 12px var(--orange-g);}}
.day-num{{font-size:42px;font-weight:900;color:#FFFFFF;line-height:1;margin-bottom:8px;}}
.hiit .day-num{{color:#FFFFFF;}}
.hiit-desc{{font-size:15px;font-weight:700;color:var(--blue);text-align:center;line-height:1.5;
            margin-top:auto;}}

/* 軽い運動デイ */
.light{{background:linear-gradient(180deg,#1a2420,#141c19);
        border:1px solid rgba(74,222,128,.15);}}
.light-tag{{font-size:15px;font-weight:700;color:var(--green);
            background:rgba(74,222,128,.08);border-radius:6px;
            padding:3px 8px;margin-bottom:10px;}}
.light .day-num{{color:#d4d6db;}}
.light-desc{{font-size:14px;color:var(--muted);text-align:center;margin-top:auto;line-height:1.5;}}

/* 回復デイ */
.rest{{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);}}
.rest-tag{{font-size:15px;font-weight:600;color:var(--muted);
           background:rgba(255,255,255,.04);border-radius:6px;
           padding:3px 8px;margin-bottom:10px;}}
.rest .day-num{{color:var(--muted);}}
.rest-desc{{font-size:14px;color:var(--muted);text-align:center;margin-top:auto;line-height:1.5;}}

/* 下部説明 */
.legend{{position:absolute;bottom:14px;left:28px;right:28px;
         display:flex;gap:24px;justify-content:center;}}
.leg{{display:flex;align-items:center;gap:10px;
      background:rgba(255,255,255,.04);border-radius:10px;
      padding:10px 20px;}}
.leg-dot{{width:12px;height:12px;border-radius:50%;flex-shrink:0;}}
.leg-title{{font-size:17px;font-weight:700;}}
.leg-desc{{font-size:15px;color:var(--sub);margin-left:4px;}}
</style></head><body>
<h1>1週間の運動設計図</h1>
<p class="sub">毎日の軽い動きが土台。週3回が加速装置。</p>

<div class="cal">
  <!-- 月 HIITデイ -->
  <div class="day hiit">
    <div class="hiit-tag">HIIT</div>
    <div class="day-num">月</div>
    <div class="hiit-desc">バーピー<br>8〜10分</div>
  </div>
  <!-- 火 軽い運動 -->
  <div class="day light">
    <div class="light-tag">軽い運動</div>
    <div class="day-num">火</div>
    <div class="light-desc">歩く・<br>階段</div>
  </div>
  <!-- 水 HIITデイ -->
  <div class="day hiit">
    <div class="hiit-tag">HIIT</div>
    <div class="day-num">水</div>
    <div class="hiit-desc">バーピー<br>8〜10分</div>
  </div>
  <!-- 木 軽い運動 -->
  <div class="day light">
    <div class="light-tag">軽い運動</div>
    <div class="day-num">木</div>
    <div class="light-desc">歩く・<br>階段</div>
  </div>
  <!-- 金 HIITデイ -->
  <div class="day hiit">
    <div class="hiit-tag">HIIT</div>
    <div class="day-num">金</div>
    <div class="hiit-desc">バーピー<br>8〜10分</div>
  </div>
  <!-- 土 回復 -->
  <div class="day rest">
    <div class="rest-tag">回復</div>
    <div class="day-num">土</div>
    <div class="rest-desc">ストレッチ<br>散歩</div>
  </div>
  <!-- 日 回復 -->
  <div class="day rest">
    <div class="rest-tag">回復</div>
    <div class="day-num">日</div>
    <div class="rest-desc">ストレッチ<br>散歩</div>
  </div>
</div>

<div class="legend">
  <div class="leg">
    <div class="leg-dot" style="background:var(--green);box-shadow:0 0 8px var(--green-g);"></div>
    <span class="leg-title" style="color:var(--green);">毎日の軽い運動</span>
    <span class="leg-desc">→ 習慣の土台をつくる</span>
  </div>
  <div class="leg">
    <div class="leg-dot" style="background:var(--orange);box-shadow:0 0 8px var(--orange-g);"></div>
    <span class="leg-title" style="color:var(--orange);">週3回のバーピー</span>
    <span class="leg-desc">→ 見た目を変える加速装置</span>
  </div>
</div>
</body></html>"""

# ============================================================
# 図解③ バーピー段階化レベル1〜5
# ============================================================
HTML3 = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE}
h1{{position:absolute;top:14px;left:0;right:0;
    font-size:40px;font-weight:900;text-align:center;color:#FFFFFF;}}
.sub{{position:absolute;top:62px;left:0;right:0;
      font-size:19px;color:var(--muted);text-align:center;}}

/* カード列 */
.cards{{position:absolute;top:100px;left:22px;right:22px;
        display:flex;gap:12px;height:504px;}}
.card{{flex:1;border-radius:16px;padding:22px 14px;
       display:flex;flex-direction:column;
       background:var(--panel);
       position:relative;overflow:hidden;}}
.card::before{{content:'';position:absolute;left:0;top:0;bottom:0;
               width:4px;border-radius:4px 0 0 4px;}}
/* Lv1-2 青系 */
.lv1,.lv2{{border:1px solid rgba(56,189,248,.2);}}
.lv1::before,.lv2::before{{background:var(--blue);}}
/* Lv3-5 オレンジ系 */
.lv3{{border:1px solid rgba(255,109,0,.3);background:#2d3244;}}
.lv3::before{{background:var(--orange);}}
.lv4,.lv5{{border:1px solid rgba(255,109,0,.2);}}
.lv4::before,.lv5::before{{background:var(--orange);}}

.lv-num{{font-size:28px;font-weight:900;margin-bottom:12px;}}
.lv1 .lv-num,.lv2 .lv-num{{color:var(--blue);text-shadow:0 0 20px var(--blue-g);}}
.lv3 .lv-num,.lv4 .lv-num,.lv5 .lv-num{{color:var(--orange);text-shadow:0 0 20px var(--orange-g);}}

.divider{{height:1px;background:rgba(255,255,255,.08);margin-bottom:14px;}}

.lv-title{{font-size:18px;font-weight:800;color:#FFFFFF;
           line-height:1.5;margin-bottom:12px;}}
.lv-desc{{font-size:15px;color:var(--muted);line-height:1.6;flex:1;}}
.lv-badge{{margin-top:14px;font-size:14px;font-weight:700;
           padding:5px 10px;border-radius:6px;text-align:center;}}
.lv1 .lv-badge{{color:var(--green);background:rgba(74,222,128,.1);}}
.lv3 .lv-badge{{color:var(--orange);background:rgba(255,109,0,.12);}}

/* 矢印 */
.arrow{{position:absolute;top:50%;transform:translateY(-50%);
        font-size:18px;color:var(--muted);opacity:.5;
        right:-8px;z-index:10;}}

/* フッター */
.foot{{position:absolute;bottom:14px;left:0;right:0;text-align:center;
       font-size:20px;font-weight:900;color:var(--orange);
       text-shadow:0 0 20px var(--orange-g);}}
</style></head><body>
<h1>バーピー段階化｜5つのレベル</h1>
<p class="sub">気合いではなく、今の自分に合うレベルを選ぶ</p>

<div class="cards">
  <div class="card lv1">
    <div class="lv-num">Lv.1</div>
    <div class="divider"></div>
    <div class="lv-title">ノージャンプ・ノープッシュアップ</div>
    <div class="lv-desc">運動ゼロから始める人向け</div>
    <div class="lv-badge">まずここから</div>
    <div class="arrow">›</div>
  </div>
  <div class="card lv2">
    <div class="lv-num">Lv.2</div>
    <div class="divider"></div>
    <div class="lv-title">ノージャンプ＋プッシュアップ</div>
    <div class="lv-desc">少し慣れてきた人向け</div>
    <div class="arrow">›</div>
  </div>
  <div class="card lv3">
    <div class="lv-num">Lv.3</div>
    <div class="divider"></div>
    <div class="lv-title">標準形（ジャンプあり）</div>
    <div class="lv-desc">2〜3週間続いた人向け</div>
    <div class="lv-badge">標準形</div>
    <div class="arrow">›</div>
  </div>
  <div class="card lv4">
    <div class="lv-num">Lv.4</div>
    <div class="divider"></div>
    <div class="lv-title">テンポアップ または回数アップ</div>
    <div class="lv-desc">標準形に慣れた人向け</div>
    <div class="arrow">›</div>
  </div>
  <div class="card lv5">
    <div class="lv-num">Lv.5</div>
    <div class="divider"></div>
    <div class="lv-title">休憩を短くする</div>
    <div class="lv-desc">さらに負荷を上げたい人向け</div>
  </div>
</div>

<div class="foot">何をやるかで迷わない。今の自分のレベルだけ選ぶ。</div>
</body></html>"""

# ============================================================
# 図解④ 崩れた日の戻り方フロー
# ============================================================
HTML4 = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE}
body{{background:linear-gradient(160deg,#060b12 0%,#1A2A3A 100%);}}

h1{{position:absolute;top:14px;left:0;right:0;
    font-size:38px;font-weight:900;text-align:center;color:#FFFFFF;}}
.sub{{position:absolute;top:62px;left:0;right:0;text-align:center;
      font-size:19px;font-weight:700;color:var(--orange);
      text-shadow:0 0 20px var(--orange-g);}}

/* トリガーノード */
.trigger{{position:absolute;left:50%;transform:translateX(-50%);
          top:104px;width:460px;height:60px;
          background:rgba(239,68,68,.1);border:2px solid var(--red);
          border-radius:30px;
          display:flex;align-items:center;justify-content:center;
          font-size:26px;font-weight:800;color:var(--red);
          box-shadow:0 0 28px var(--red-g);}}

/* 分岐メッセージ */
.branch-msg{{position:absolute;left:50%;transform:translateX(-50%);
             top:228px;width:600px;text-align:center;}}
.bm-main{{font-size:30px;font-weight:900;color:#FFFFFF;margin-bottom:6px;}}
.bm-sub{{font-size:17px;color:var(--muted);}}

/* 3択カード */
.opt{{position:absolute;top:378px;width:276px;height:116px;
      background:var(--panel);border-radius:14px;
      border:1px solid rgba(56,189,248,.22);
      display:flex;flex-direction:column;
      align-items:center;justify-content:center;gap:10px;
      box-shadow:0 12px 40px rgba(0,0,0,.4);}}
.o1{{left:110px;}} .o2{{left:502px;}} .o3{{left:894px;}}
.ot{{font-size:20px;font-weight:700;color:var(--blue);}}
.ob{{font-size:19px;font-weight:800;color:var(--green);
     text-shadow:0 0 12px var(--green-g);}}

/* ゴールノード */
.goal{{position:absolute;left:50%;transform:translateX(-50%);
       top:576px;width:620px;height:68px;
       background:linear-gradient(135deg,#14532d,#22c55e);
       border-radius:34px;
       display:flex;align-items:center;justify-content:center;
       font-size:23px;font-weight:900;color:#052e16;
       text-align:center;
       box-shadow:0 0 40px rgba(74,222,128,.35);}}

svg{{position:absolute;inset:0;width:1280px;height:720px;pointer-events:none;}}
</style></head><body>
<h1>崩れた日の"戻り方"</h1>
<p class="sub">ゼロにしなければ勝ち。負荷を落とすだけでいい。</p>

<div class="trigger">今日はバーピーがきつい</div>

<div class="branch-msg">
  <p class="bm-main">やめない。ただ落とす。</p>
  <p class="bm-sub">1日抜けても習慣強度にほぼ影響なし（メタ分析）</p>
</div>

<div class="opt o1">
  <div class="ot">Lv.1に落とす</div>
  <div class="ob">合格 ✓</div>
</div>
<div class="opt o2">
  <div class="ot">5分だけ歩く</div>
  <div class="ob">合格 ✓</div>
</div>
<div class="opt o3">
  <div class="ot">ストレッチだけやる</div>
  <div class="ob">合格 ✓</div>
</div>

<div class="goal">8勝6敗で十分。ゼロにしなければ勝ち ✓</div>

<svg xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ar" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#ef4444" opacity=".8"/></marker>
    <marker id="ab" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#38bdf8" opacity=".8"/></marker>
    <marker id="ag" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#4ade80"/></marker>
  </defs>
  <!-- trigger → branch-msg -->
  <line x1="640" y1="164" x2="640" y2="226" stroke="#ef4444" stroke-width="2.5" marker-end="url(#ar)" opacity=".8"/>
  <!-- branch-msg → 3 opts -->
  <line x1="640" y1="312" x2="248" y2="376" stroke="#38bdf8" stroke-width="2" opacity=".55" marker-end="url(#ab)"/>
  <line x1="640" y1="312" x2="640" y2="376" stroke="#38bdf8" stroke-width="2" opacity=".55" marker-end="url(#ab)"/>
  <line x1="640" y1="312" x2="1032" y2="376" stroke="#38bdf8" stroke-width="2" opacity=".55" marker-end="url(#ab)"/>
  <!-- 3 opts → goal -->
  <line x1="248" y1="494" x2="636" y2="574" stroke="#4ade80" stroke-width="2.5" marker-end="url(#ag)" opacity=".8"/>
  <line x1="640" y1="494" x2="640" y2="574" stroke="#4ade80" stroke-width="2.5" marker-end="url(#ag)" opacity=".8"/>
  <line x1="1032" y1="494" x2="644" y2="574" stroke="#4ade80" stroke-width="2.5" marker-end="url(#ag)" opacity=".8"/>
</svg>
</body></html>"""


# ============================================================
# 記事への画像埋め込み
# ============================================================
def embed_images_into_article():
    article_path = ARTICLE_DIR / "第5回_忙しい人ほど種目を減らせ迷ったらバーピー週3回で見た目を変える.md"
    output_path  = ARTICLE_DIR / "第5回_完成版（画像埋め込み済み）.md"

    replacements = [
        (
            "**【ここに図解①を挿入】**\n**バーピーで動く部位と複数種目との比較**",
            "![バーピーで動く部位と複数種目との比較](./images/図解①_バーピーvs複数種目比較.png)"
        ),
        (
            "**【ここに図解②を挿入】**\n**毎日の軽い運動 ＋ 週3回HIITの設計図**",
            "![毎日の軽い運動 ＋ 週3回HIITの設計図](./images/図解②_週間運動設計図.png)"
        ),
        (
            "**【ここに図解③を挿入】**\n**バーピー段階化レベル表（レベル1〜5）**",
            "![バーピー段階化レベル表（レベル1〜5）](./images/図解③_バーピー段階化レベル.png)"
        ),
        (
            "**【ここに図解④を挿入】**\n**崩れた日の戻り方フロー**",
            "![崩れた日の戻り方フロー](./images/図解④_崩れた日の戻り方フロー.png)"
        ),
    ]

    content = article_path.read_text(encoding="utf-8")
    for old, new in replacements:
        content = content.replace(old, new)
    output_path.write_text(content, encoding="utf-8")
    print(f"✅ 画像埋め込み完了: {output_path.name}")


# ============================================================
# メイン
# ============================================================
FIGURES = [
    (HTML1, "図解①_バーピーvs複数種目比較.png"),
    (HTML2, "図解②_週間運動設計図.png"),
    (HTML3, "図解③_バーピー段階化レベル.png"),
    (HTML4, "図解④_崩れた日の戻り方フロー.png"),
]

if __name__ == "__main__":
    print("第 高品質図解生成開始 (HTML/CSS + Playwright)...\n")

    tmp = ARTICLE_DIR / "_tmp.html"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        for html, fname in FIGURES:
            tmp.write_text(html, encoding="utf-8")
            page.goto(f"file:///{tmp.as_posix()}")
            page.wait_for_timeout(900)

            out = OUTPUT_DIR / fname
            page.screenshot(path=str(out), full_page=False)
            print(f"✅ {fname}")

        browser.close()

    tmp.unlink(missing_ok=True)

    print("\n記事への画像埋め込み中...")
    embed_images_into_article()

    print(f"\n全工程完了!")
    print(f"保存先: {OUTPUT_DIR}")


