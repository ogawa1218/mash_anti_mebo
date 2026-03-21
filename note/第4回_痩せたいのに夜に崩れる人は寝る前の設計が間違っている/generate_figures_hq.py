#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 図解 高品質生成スクリプト
HTML/CSS + Playwright（Chromiumヘッドレス）版
"""

import sys
import os
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
  --orange:#f97316; --orange-g:rgba(249,115,22,.35);
  --blue:#38bdf8;   --blue-g:rgba(56,189,248,.35);
  --green:#4ade80;  --green-g:rgba(74,222,128,.3);
  --red:#ef4444;    --red-g:rgba(239,68,68,.35);
  --bg:#0d1117; --panel:#161b22; --panel2:#1e2431;
  --text:#e2e8f0; --muted:#64748b; --border:rgba(255,255,255,.08);
}}
body {{
  width:1280px; height:720px; overflow:hidden;
  background:var(--bg); color:var(--text); position:relative;
}}
body::before {{
  content:''; position:absolute; inset:0; pointer-events:none;
  background-image:
    linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);
  background-size:48px 48px;
}}
"""

# ============================================================
# 図解① 寝る90分前ルール 3ステップ
# ============================================================
HTML1 = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE}
.wrap{{position:relative;width:1280px;height:720px;
       padding:32px 44px 18px;
       display:flex;flex-direction:column;}}
h1{{font-size:44px;font-weight:900;text-align:center;
    color:#f1f5f9;margin-bottom:8px;letter-spacing:-.5px;}}
.sub{{font-size:21px;color:var(--muted);text-align:center;margin-bottom:22px;}}
.row{{display:flex;gap:0;flex:1;align-items:center;}}
.arr{{font-size:44px;color:var(--orange);flex-shrink:0;width:58px;
      text-align:center;text-shadow:0 0 24px var(--orange-g);
      margin-bottom:52px;}}
.card{{flex:1;height:418px;
       background:linear-gradient(145deg,#1a2030,#141920);
       border-radius:20px;border:1px solid rgba(249,115,22,.2);
       padding:30px 26px 24px;
       display:flex;flex-direction:column;align-items:center;
       position:relative;
       box-shadow:0 20px 60px rgba(0,0,0,.45),
                  inset 0 1px 0 rgba(255,255,255,.05);}}
.card::before{{content:'';position:absolute;
               top:0;left:16px;right:16px;height:2px;
               background:linear-gradient(90deg,transparent,var(--orange),transparent);
               border-radius:2px;}}
.time{{font-size:56px;font-weight:900;color:var(--orange);line-height:1;
       margin-bottom:14px;
       text-shadow:0 0 30px var(--orange-g),0 0 60px rgba(249,115,22,.15);}}
hr{{width:75%;border:none;border-top:1px solid rgba(255,255,255,.09);margin:0 0 18px;}}
.ctitle{{font-size:30px;font-weight:800;color:#f1f5f9;
         text-align:center;margin-bottom:18px;}}
.cdesc{{font-size:20px;color:#94a3b8;text-align:center;line-height:1.85;}}
.foot{{font-size:24px;font-weight:700;color:var(--orange);text-align:center;
       padding:14px 0 2px;
       text-shadow:0 0 20px var(--orange-g);letter-spacing:.5px;}}
</style></head><body>
<div class="wrap">
  <h1>寝る90分前ルール｜3ステップ</h1>
  <p class="sub">睡眠は布団に入る瞬間では決まらない</p>
  <div class="row">
    <div class="card">
      <div class="time">90分前</div><hr>
      <div class="ctitle">光を落とす</div>
      <div class="cdesc">照明を1段暗く<br>スマホはナイトモード</div>
    </div>
    <div class="arr">→</div>
    <div class="card">
      <div class="time">60分前</div><hr>
      <div class="ctitle">食を締める</div>
      <div class="cdesc">追加カロリーを入れない<br>歯磨きがトリガー</div>
    </div>
    <div class="arr">→</div>
    <div class="card">
      <div class="time">20分前</div><hr>
      <div class="ctitle">脳を静かにする</div>
      <div class="cdesc">呼吸1分＋ストレッチ2分<br>＋明日の準備2分</div>
    </div>
  </div>
  <div class="foot">戦いは朝じゃない。寝る前に始まっている。</div>
</div></body></html>"""

# ============================================================
# 図解② 睡眠不足が太りやすくする3つのメカニズム
# ============================================================
HTML2 = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE}
h1{{position:absolute;top:20px;left:0;right:0;
    font-size:40px;font-weight:900;text-align:center;color:#f1f5f9;}}
.top-node{{position:absolute;left:50%;transform:translateX(-50%);
           top:76px;width:340px;height:64px;
           background:rgba(239,68,68,.12);border:2px solid var(--red);
           border-radius:32px;
           display:flex;align-items:center;justify-content:center;
           font-size:32px;font-weight:900;color:var(--red);
           box-shadow:0 0 30px var(--red-g);}}
.bc{{position:absolute;top:258px;width:290px;height:218px;
     background:linear-gradient(145deg,#1a2030,#141920);
     border:1px solid rgba(239,68,68,.22);border-radius:16px;
     padding:18px 20px;
     box-shadow:0 16px 48px rgba(0,0,0,.4);}}
.bc-l{{left:58px;}} .bc-m{{left:495px;}} .bc-r{{left:932px;}}
.bt{{font-size:23px;font-weight:800;color:var(--red);margin-bottom:10px;}}
.bdiv{{height:1px;background:rgba(255,255,255,.07);margin:4px 0 10px;}}
.bs{{font-size:19px;color:var(--text);margin-bottom:8px;line-height:1.5;}}
.br{{font-size:17px;color:var(--muted);line-height:1.55;}}
.bot-node{{position:absolute;left:50%;transform:translateX(-50%);
           top:580px;width:520px;height:64px;
           background:rgba(56,189,248,.1);border:2px solid var(--blue);
           border-radius:32px;
           display:flex;align-items:center;justify-content:center;
           font-size:25px;font-weight:800;color:var(--blue);
           box-shadow:0 0 28px var(--blue-g);}}
.cite{{position:absolute;bottom:12px;left:24px;font-size:15px;color:var(--muted);}}
svg{{position:absolute;inset:0;width:1280px;height:720px;pointer-events:none;}}
</style></head><body>
<h1>睡眠が崩れると、なぜ太るのか</h1>
<div class="top-node">睡眠不足</div>
<div class="bc bc-l">
  <div class="bt">① 食欲が暴走</div><div class="bdiv"></div>
  <div class="bs">レプチン↓　グレリン↑</div>
  <div class="br">甘い物・脂っこい物に<br>手が伸びる</div>
</div>
<div class="bc bc-m">
  <div class="bt">② 判断が雑になる</div><div class="bdiv"></div>
  <div class="bs">前頭前皮質の機能↓</div>
  <div class="br">菓子パン＞サラダチキン<br>を選ぶ</div>
</div>
<div class="bc bc-r">
  <div class="bt">③ 活動量が落ちる</div><div class="bdiv"></div>
  <div class="bs">だるい→動かない<br>→眠りが浅い</div>
  <div class="br">悪循環に入る</div>
</div>
<div class="bot-node">もっと頑張る前に、まず寝る。</div>
<p class="cite">Taheri S et al. PLoS Med. 2004</p>
<svg xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ar" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#ef4444" opacity=".85"/>
    </marker>
    <marker id="ab" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#38bdf8" opacity=".85"/>
    </marker>
  </defs>
  <line x1="640" y1="140" x2="207" y2="256" stroke="#ef4444" stroke-width="2.5" marker-end="url(#ar)" opacity=".8"/>
  <line x1="640" y1="140" x2="640" y2="256" stroke="#ef4444" stroke-width="2.5" marker-end="url(#ar)" opacity=".8"/>
  <line x1="640" y1="140" x2="1073" y2="256" stroke="#ef4444" stroke-width="2.5" marker-end="url(#ar)" opacity=".8"/>
  <line x1="207" y1="476" x2="638" y2="578" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#ab)" opacity=".75"/>
  <line x1="640" y1="476" x2="640" y2="578" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#ab)" opacity=".75"/>
  <line x1="1073" y1="476" x2="642" y2="578" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#ab)" opacity=".75"/>
</svg>
</body></html>"""

# ============================================================
# 図解③ 照明とメラトニンの比較
# ============================================================
HTML3 = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE}
body{{background:#09090f;}}
.wrap{{position:absolute;inset:0;display:flex;}}
.side{{flex:1;display:flex;flex-direction:column;
       align-items:center;padding:30px 36px;position:relative;}}
.ng{{background:linear-gradient(180deg,rgba(239,68,68,.12) 0%,rgba(239,68,68,.04) 100%);}}
.ok{{background:linear-gradient(180deg,rgba(56,189,248,.12) 0%,rgba(56,189,248,.04) 100%);}}
.div{{width:3px;background:linear-gradient(180deg,transparent,rgba(255,255,255,.25),transparent);flex-shrink:0;}}
.lbl{{font-size:25px;font-weight:800;margin-bottom:14px;text-align:center;}}
.ng .lbl{{color:var(--red);}} .ok .lbl{{color:var(--blue);}}
.main{{font-size:46px;font-weight:900;text-align:center;
       line-height:1.25;margin-bottom:26px;}}
.ng .main{{color:var(--red);text-shadow:0 0 40px var(--red-g);}}
.ok .main{{color:var(--blue);text-shadow:0 0 40px var(--blue-g);}}
.items{{width:100%;display:flex;flex-direction:column;gap:12px;margin-bottom:24px;}}
.item{{background:rgba(255,255,255,.04);border-radius:12px;
       padding:13px 18px;font-size:20px;line-height:1.5;border-left:3px solid;}}
.ng .item{{color:#fca5a5;border-color:var(--red);}}
.ok .item{{color:#7dd3fc;border-color:var(--blue);}}
.verdict{{font-size:27px;font-weight:900;text-align:center;margin-top:auto;
          padding:16px 24px;border-radius:12px;}}
.ng .verdict{{color:var(--red);background:rgba(239,68,68,.1);
              border:1px solid rgba(239,68,68,.3);}}
.ok .verdict{{color:var(--green);background:rgba(74,222,128,.08);
              border:1px solid rgba(74,222,128,.3);}}
.cite{{position:absolute;bottom:14px;left:24px;
       font-size:15px;color:var(--muted);}}
</style></head><body>
<div class="wrap">
  <div class="side ng">
    <p class="lbl">❌ 寝る直前まで明るい部屋</p>
    <p class="main">蛍光灯<br>全開</p>
    <div class="items">
      <div class="item">メラトニン分泌が約90分遅延</div>
      <div class="item">脳が「まだ昼だ」と判断</div>
      <div class="item">寝つきが悪く、睡眠の質が低下</div>
    </div>
    <div class="verdict">体内時計 90分ズレる</div>
  </div>
  <div class="div"></div>
  <div class="side ok">
    <p class="lbl">✅ 90分前に照明を落とす</p>
    <p class="main">間接照明<br>＋ナイトモード</p>
    <div class="items">
      <div class="item">メラトニンが自然に分泌開始</div>
      <div class="item">脳が「もう夜だ」と認識</div>
      <div class="item">スムーズに入眠できる</div>
    </div>
    <div class="verdict">自然な眠りのスイッチON</div>
  </div>
</div>
<p class="cite">Gooley JJ et al. J Clin Endocrinol Metab. 2011</p>
</body></html>"""

# ============================================================
# 図解④ 「食を締める」実践フロー
# ============================================================
HTML4 = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE}
h1{{position:absolute;top:22px;left:0;right:0;
    font-size:42px;font-weight:900;text-align:center;color:#f1f5f9;}}
.sub{{position:absolute;top:78px;left:0;right:0;
      font-size:20px;color:var(--muted);text-align:center;}}
/* ノード共通 */
.nd{{position:absolute;display:flex;flex-direction:column;
     align-items:center;justify-content:center;
     text-align:center;border-radius:50px;}}
/* Step1 */
.n1{{left:40px;top:298px;width:190px;height:88px;
     background:#1e2431;border:1px solid rgba(255,255,255,.12);
     font-size:23px;font-weight:700;color:#f1f5f9;}}
.n1s{{font-size:14px;color:var(--muted);margin-top:4px;}}
/* Step2 */
.n2{{left:288px;top:286px;width:196px;height:112px;border-radius:16px;
     background:linear-gradient(135deg,#c2410c,#f97316);
     font-size:26px;font-weight:900;color:#fff;
     box-shadow:0 0 40px rgba(249,115,22,.4);}}
.n2s{{font-size:14px;color:rgba(255,255,255,.75);margin-top:4px;}}
/* Route cards */
.rt{{position:absolute;width:280px;height:108px;
     background:linear-gradient(145deg,#1a2030,#141920);
     border-radius:14px;padding:16px 20px;
     display:flex;flex-direction:column;justify-content:center;}}
.ra{{left:572px;top:194px;border:1px solid rgba(74,222,128,.3);}}
.rb{{left:572px;top:400px;border:1px solid rgba(56,189,248,.3);}}
.rtl{{font-size:20px;font-weight:700;margin-bottom:6px;}}
.ra .rtl{{color:var(--green);}} .rb .rtl{{color:var(--blue);}}
.rts{{font-size:17px;color:var(--muted);line-height:1.5;}}
/* Goal */
.goal{{position:absolute;right:38px;top:284px;width:248px;height:116px;
       border-radius:16px;
       background:linear-gradient(135deg,#14532d,#22c55e);
       display:flex;flex-direction:column;
       align-items:center;justify-content:center;
       font-size:21px;font-weight:900;color:#052e16;
       line-height:1.6;text-align:center;
       box-shadow:0 0 40px rgba(74,222,128,.35);}}
svg{{position:absolute;inset:0;width:1280px;height:720px;pointer-events:none;}}
</style></head><body>
<h1>食を締める｜実践フロー</h1>
<p class="sub">我慢ではなく、締め時を「仕組み」で決める</p>
<div class="nd n1">
  <span>寝る60分前</span>
  <span class="n1s">時計を確認</span>
</div>
<div class="nd n2">
  <span>歯を磨く</span>
  <span class="n2s">これがトリガー</span>
</div>
<div class="rt ra">
  <div class="rtl">お腹が空いていない</div>
  <div class="rts">そのまま就寝準備へ</div>
</div>
<div class="rt rb">
  <div class="rtl">どうしても空腹が強い</div>
  <div class="rts">温かいノンカフェイン飲料1杯</div>
</div>
<div class="goal">今日の食事は<br>ここまで ✓</div>
<svg xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ao" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#f97316"/></marker>
    <marker id="ag" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#4ade80"/></marker>
    <marker id="ab2" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#38bdf8"/></marker>
    <marker id="aw" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="rgba(255,255,255,.7)"/></marker>
  </defs>
  <!-- n1 → n2 -->
  <line x1="230" y1="342" x2="286" y2="342" stroke="#f97316" stroke-width="3.5" marker-end="url(#ao)"/>
  <!-- n2 → route A (top) -->
  <path d="M 386 286 C 480 248 520 248 570 248"
        stroke="#4ade80" stroke-width="2.5" fill="none" marker-end="url(#ag)" opacity=".9"/>
  <!-- n2 → route B (bottom) -->
  <path d="M 386 398 C 480 454 520 454 570 454"
        stroke="#38bdf8" stroke-width="2.5" fill="none" marker-end="url(#ab2)" opacity=".9"/>
  <!-- route A → goal -->
  <path d="M 852 248 C 945 248 945 342 992 342"
        stroke="#4ade80" stroke-width="2.5" fill="none" marker-end="url(#aw)" opacity=".8"/>
  <!-- route B → goal -->
  <path d="M 852 454 C 945 454 945 342 992 342"
        stroke="#38bdf8" stroke-width="2.5" fill="none" marker-end="url(#aw)" opacity=".8"/>
</svg>
</body></html>"""

# ============================================================
# 図解⑤ 崩れた日の復帰フロー
# ============================================================
HTML5 = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE}
body{{background:linear-gradient(165deg,#060b12 0%,#0c1a2e 100%);}}
h1{{position:absolute;top:14px;left:0;right:0;
    font-size:38px;font-weight:900;text-align:center;color:#f1f5f9;}}
.sub{{position:absolute;top:62px;left:0;right:0;
      font-size:20px;font-weight:700;text-align:center;color:var(--orange);
      text-shadow:0 0 20px var(--orange-g);}}
.fail{{position:absolute;left:50%;transform:translateX(-50%);
       top:106px;width:490px;height:64px;
       background:rgba(239,68,68,.1);border:2px solid var(--red);
       border-radius:32px;
       display:flex;align-items:center;justify-content:center;
       font-size:27px;font-weight:800;color:var(--red);
       box-shadow:0 0 30px var(--red-g);}}
.msg{{position:absolute;left:50%;transform:translateX(-50%);
      top:222px;width:720px;text-align:center;}}
.msg-m{{font-size:30px;font-weight:900;color:#f1f5f9;margin-bottom:8px;}}
.msg-s{{font-size:18px;color:var(--muted);}}
.opt{{position:absolute;top:386px;width:274px;height:108px;
      background:linear-gradient(145deg,#1a2030,#141920);
      border:1px solid rgba(56,189,248,.25);border-radius:14px;
      display:flex;flex-direction:column;
      align-items:center;justify-content:center;gap:10px;
      box-shadow:0 12px 40px rgba(0,0,0,.4);}}
.o1{{left:118px;}} .o2{{left:503px;}} .o3{{left:888px;}}
.ot{{font-size:21px;font-weight:700;color:var(--blue);}}
.ob{{font-size:20px;font-weight:800;color:var(--green);
     text-shadow:0 0 15px var(--green-g);}}
.goal{{position:absolute;left:50%;transform:translateX(-50%);
       top:574px;width:610px;height:68px;
       background:linear-gradient(135deg,#14532d,#22c55e);
       border-radius:34px;
       display:flex;align-items:center;justify-content:center;
       font-size:24px;font-weight:900;color:#052e16;
       box-shadow:0 0 40px rgba(74,222,128,.35);
       text-align:center;}}
svg{{position:absolute;inset:0;width:1280px;height:720px;pointer-events:none;}}
</style></head><body>
<h1>崩れた日の"戻り方"</h1>
<p class="sub">完璧を目指さない。70点を長く続ける。</p>
<div class="fail">3ステップ全部できなかった</div>
<div class="msg">
  <p class="msg-m">自分を責めない。1つだけでOK</p>
  <p class="msg-s">1日抜けても習慣強度にほぼ影響なし（メタ分析）</p>
</div>
<div class="opt o1">
  <div class="ot">照明だけ暗くした</div>
  <div class="ob">合格 ✓</div>
</div>
<div class="opt o2">
  <div class="ot">夜食だけ回避した</div>
  <div class="ob">合格 ✓</div>
</div>
<div class="opt o3">
  <div class="ot">呼吸1分だけやった</div>
  <div class="ob">合格 ✓</div>
</div>
<div class="goal">8勝6敗で十分。ゼロにしなければ勝ち ✓</div>
<svg xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ar2" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#ef4444" opacity=".8"/></marker>
    <marker id="ag2" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,9 3.5,0 7" fill="#4ade80"/></marker>
  </defs>
  <!-- fail → msg -->
  <line x1="640" y1="170" x2="640" y2="220" stroke="#ef4444" stroke-width="2.5" marker-end="url(#ar2)" opacity=".75"/>
  <!-- msg → 3 opts -->
  <line x1="640" y1="308" x2="255" y2="384" stroke="#38bdf8" stroke-width="2" opacity=".55"/>
  <line x1="640" y1="308" x2="640" y2="384" stroke="#38bdf8" stroke-width="2" opacity=".55"/>
  <line x1="640" y1="308" x2="1025" y2="384" stroke="#38bdf8" stroke-width="2" opacity=".55"/>
  <!-- 3 opts → goal -->
  <line x1="255" y1="494" x2="638" y2="572" stroke="#4ade80" stroke-width="2.5" marker-end="url(#ag2)" opacity=".75"/>
  <line x1="640" y1="494" x2="640" y2="572" stroke="#4ade80" stroke-width="2.5" marker-end="url(#ag2)" opacity=".75"/>
  <line x1="1025" y1="494" x2="642" y2="572" stroke="#4ade80" stroke-width="2.5" marker-end="url(#ag2)" opacity=".75"/>
</svg>
</body></html>"""


# ============================================================
# 記事への画像埋め込み
# ============================================================
def embed_images_into_article():
    article_path = ARTICLE_DIR / "第4回_痩せたいのに夜に崩れる人は寝る前の設計が間違っている.md"
    output_path  = ARTICLE_DIR / "第4回_完成版（画像埋め込み済み）.md"

    replacements = [
        (
            "**【ここに図解①を挿入】**\n**寝る90分前ルール｜3ステップの全体像**",
            "![寝る90分前ルール｜3ステップの全体像](./images/図解①_寝る90分前ルール.png)"
        ),
        (
            "**【ここに図解②を挿入】**\n**睡眠不足が太りやすくする3つのメカニズム**",
            "![睡眠不足が太りやすくする3つのメカニズム](./images/図解②_睡眠不足メカニズム.png)"
        ),
        (
            "**【ここに図解③を挿入】**\n**就寝前の照明とメラトニンの関係（比較図）**",
            "![就寝前の照明とメラトニンの関係](./images/図解③_照明とメラトニン比較.png)"
        ),
        (
            "**【ここに図解④を挿入】**\n**「食を締める」実践フロー（歯磨きトリガー）**",
            "![「食を締める」実践フロー](./images/図解④_食を締める実践フロー.png)"
        ),
        (
            "**【ここに図解⑤を挿入】**\n**崩れた日の復帰フロー**",
            "![崩れた日の復帰フロー](./images/図解⑤_崩れた日の復帰フロー.png)"
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
    (HTML1, "図解①_寝る90分前ルール.png"),
    (HTML2, "図解②_睡眠不足メカニズム.png"),
    (HTML3, "図解③_照明とメラトニン比較.png"),
    (HTML4, "図解④_食を締める実践フロー.png"),
    (HTML5, "図解⑤_崩れた日の復帰フロー.png"),
]

if __name__ == "__main__":
    print("高品質図解生成開始 (HTML/CSS + Playwright)...\n")

    tmp = ARTICLE_DIR / "_tmp.html"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        for html, fname in FIGURES:
            tmp.write_text(html, encoding="utf-8")
            page.goto(f"file:///{tmp.as_posix()}")
            page.wait_for_timeout(900)   # フォント・レンダリング待機

            out = OUTPUT_DIR / fname
            page.screenshot(path=str(out), full_page=False)
            print(f"✅ {fname}")

        browser.close()

    tmp.unlink(missing_ok=True)

    print("\n記事への画像埋め込み中...")
    embed_images_into_article()

    print(f"\n全工程完了!")
    print(f"保存先: {OUTPUT_DIR}")


