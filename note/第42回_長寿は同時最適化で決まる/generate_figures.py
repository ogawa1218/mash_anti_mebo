#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第42回 図解生成スクリプト（HTML/CSS + Playwright 強化版）
図解5枚：
  ①「魔法の1手」ループ（失敗の円形フロー）
  ② 同時最適化の4要素（横4列カード）
  ③ NG vs OK 比較表
  ④ 実践早見表（4指標テーブル）
  ⑤ 崩れた日の復帰フロー（縦型4ステップ）
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images"
OUTPUT_DIR.mkdir(exist_ok=True)
FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;font-family:'NJ','Meiryo',sans-serif;position:relative;}"
)

def render(html, fname):
    tmp = ARTICLE_DIR / "_tmp_fig.html"
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
    print("OK: " + fname)

# ──────────────────────────────────────────────────────────
# 図解① 「魔法の1手」失敗ループ（円形フロー）
# ──────────────────────────────────────────────────────────
def fig1():
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:40px;left:60px;font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;}}
.subtitle{{position:absolute;top:84px;left:60px;font-size:20px;font-weight:500;color:#9ca3af;}}

/* 中央の「→」ループ */
.loop-wrap{{
  position:absolute;left:50%;top:50%;
  transform:translate(-50%,-48%);
  width:640px;height:480px;
}}

/* 各ステップのカード（5個を円形に配置） */
.step{{
  position:absolute;
  width:170px;padding:14px 10px;border-radius:12px;
  font-size:18px;font-weight:700;color:#fff;
  text-align:center;line-height:1.4;
  border:2px solid rgba(255,255,255,.1);
}}
.s1{{background:#1e3a5f;top:0;left:50%;transform:translateX(-50%);}}
.s2{{background:#2d1f4e;top:110px;right:0;}}
.s3{{background:#4a1a1a;bottom:110px;right:20px;}}
.s4{{background:#3a1a0a;bottom:110px;left:20px;}}
.s5{{background:#1a3a1a;top:110px;left:0;}}

/* 矢印ラベル */
.arrow{{position:absolute;font-size:15px;font-weight:600;color:#9ca3af;text-align:center;}}
.a12{{top:90px;right:30px;}}
.a23{{bottom:200px;right:10px;}}
.a34{{bottom:80px;left:50%;transform:translateX(-50%);}}
.a45{{bottom:200px;left:10px;}}
.a51{{top:90px;left:30px;}}

/* 中央の警告 */
.center{{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:150px;height:150px;border-radius:50%;
  background:rgba(239,68,68,.15);border:2px solid #ef4444;
  display:flex;align-items:center;justify-content:center;
  flex-direction:column;text-align:center;
}}
.center .icon{{font-size:36px;}}
.center .label{{font-size:14px;font-weight:700;color:#ef4444;margin-top:6px;}}

/* 右下の解決策 */
.solution{{
  position:absolute;bottom:30px;right:40px;
  background:rgba(56,189,248,.1);border:1.5px solid #38bdf8;
  border-radius:10px;padding:14px 20px;max-width:320px;
}}
.solution .sol-title{{font-size:16px;font-weight:700;color:#38bdf8;margin-bottom:6px;}}
.solution .sol-body{{font-size:14px;font-weight:500;color:#e2e8f0;line-height:1.6;}}

/* 著者 */
.author{{position:absolute;bottom:20px;left:40px;font-size:16px;color:#3a3a3a;font-weight:400;}}
</style></head><body>

<div class="title">①「魔法の1手」 ─ 失敗が繰り返される理由</div>
<div class="subtitle">なぜ「これだけやれば」は続かないのか</div>

<div class="loop-wrap">
  <div class="step s1">最新の方法<br>を試す</div>
  <div class="step s2">1〜3週間<br>で効果</div>
  <div class="step s3">反動・<br>リバウンド</div>
  <div class="step s4">自己嫌悪<br>ループ</div>
  <div class="step s5">継続<br>困難</div>

  <div class="arrow a12">↘ 短期効果</div>
  <div class="arrow a23">↓ 崩れる</div>
  <div class="arrow a34">← 戻る</div>
  <div class="arrow a45">↑ 疲弊</div>
  <div class="arrow a51">↗ 諦め</div>

  <div class="center">
    <div class="icon">🔄</div>
    <div class="label">無限<br>ループ</div>
  </div>
</div>

<div class="solution">
  <div class="sol-title">✅ 抜け出す方法</div>
  <div class="sol-body">1つだけ変えるのをやめる。<br>炎症・代謝・睡眠・継続の<br>4つを同時に少しずつ整える</div>
</div>

<div class="author">マーシー｜100kg→68kg｜Sub3</div>
</body></html>"""
    render(html, "図解①_魔法の1手ループ.png")

# ──────────────────────────────────────────────────────────
# 図解② 同時最適化の4要素（横4列カード）
# ──────────────────────────────────────────────────────────
def fig2():
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:60px;font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;}}
.subtitle{{position:absolute;top:82px;left:60px;font-size:20px;font-weight:500;color:#9ca3af;}}

.cards{{
  position:absolute;top:140px;left:40px;right:40px;
  display:flex;gap:24px;
}}
.card{{
  flex:1;border-radius:16px;padding:28px 20px;
  border:1.5px solid rgba(255,255,255,.08);
  display:flex;flex-direction:column;align-items:center;text-align:center;
}}
.card .icon{{font-size:44px;margin-bottom:14px;}}
.card .name{{font-size:22px;font-weight:900;color:#fff;margin-bottom:10px;}}
.card .desc{{font-size:14px;font-weight:500;color:#9ca3af;line-height:1.6;}}
.card .trigger{{
  margin-top:14px;font-size:13px;font-weight:600;
  padding:6px 12px;border-radius:20px;
}}

.c1{{background:#0d2035;}}
.c1 .trigger{{background:rgba(239,68,68,.15);color:#ef4444;}}
.c2{{background:#1a2010;}}
.c2 .trigger{{background:rgba(74,222,128,.15);color:#4ade80;}}
.c3{{background:#1e1a30;}}
.c3 .trigger{{background:rgba(56,189,248,.15);color:#38bdf8;}}
.c4{{background:#2a1800;}}
.c4 .trigger{{background:rgba(255,109,0,.15);color:#FF6D00;}}

/* 中央の→連動 */
.connector{{
  position:absolute;top:50%;transform:translateY(-50%);
  font-size:28px;color:#444;z-index:10;
}}

.bottom-note{{
  position:absolute;bottom:28px;left:0;right:0;text-align:center;
  font-size:18px;font-weight:700;color:#FF6D00;
}}
.author{{position:absolute;bottom:20px;left:40px;font-size:16px;color:#3a3a3a;font-weight:400;}}
</style></head><body>

<div class="title">② 同時最適化の4要素 ─ 4本足の椅子</div>
<div class="subtitle">1つだけ直しても他が崩れると戻る。4つを同時に少しずつ整える</div>

<div class="cards">
  <div class="card c1">
    <div class="icon">🔥</div>
    <div class="name">① 炎症</div>
    <div class="desc">慢性炎症が<br>すべての根っこ。<br>睡眠・食事・運動・<br>ストレスが複合的に作用</div>
    <div class="trigger">TNF-α / IL-6</div>
  </div>
  <div class="card c2">
    <div class="icon">⚡</div>
    <div class="name">② 代謝</div>
    <div class="desc">血糖・脂質・<br>体脂肪は連動する。<br>体重だけ見ると<br>実態を見逃す</div>
    <div class="trigger">腹囲で判断</div>
  </div>
  <div class="card c3">
    <div class="icon">🌙</div>
    <div class="name">③ 睡眠/食事</div>
    <div class="desc">「何を食べるか」より<br>「いつ食べるか」。<br>夜遅い食事が<br>翌日の行動を崩す</div>
    <div class="trigger">就寝3時間前まで</div>
  </div>
  <div class="card c4">
    <div class="icon">📅</div>
    <div class="name">④ 行動継続</div>
    <div class="desc">知識より運用。<br>「先に決める」だけで<br>実行率が3倍に<br>（Gollwitzer, 1999）</div>
    <div class="trigger">事前固定が最強</div>
  </div>
</div>

<div class="bottom-note">4本の足を同時に少しずつ伸ばす ─ これが8年リバウンドしない戦略</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
</body></html>"""
    render(html, "図解②_4要素の全体像.png")

# ──────────────────────────────────────────────────────────
# 図解③ NG vs OK 比較表
# ──────────────────────────────────────────────────────────
def fig3():
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:60px;font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;}}
.subtitle{{position:absolute;top:82px;left:60px;font-size:20px;font-weight:500;color:#9ca3af;}}

.panels{{
  position:absolute;top:136px;left:40px;right:40px;bottom:60px;
  display:flex;gap:32px;
}}
.panel{{flex:1;border-radius:16px;padding:32px 28px;display:flex;flex-direction:column;gap:18px;}}
.ng{{background:rgba(127,29,29,.25);border:1.5px solid #ef4444;}}
.ok{{background:rgba(20,83,45,.25);border:1.5px solid #4ade80;}}

.panel-header{{display:flex;align-items:center;gap:14px;margin-bottom:8px;}}
.panel-header .badge{{
  font-size:28px;font-weight:900;padding:6px 16px;border-radius:8px;
}}
.ng .badge{{background:#ef4444;color:#fff;}}
.ok .badge{{background:#4ade80;color:#0d1b2a;}}
.panel-header .title-text{{font-size:22px;font-weight:900;color:#fff;}}

.row{{display:flex;align-items:flex-start;gap:12px;}}
.row .icon{{font-size:20px;flex-shrink:0;margin-top:2px;}}
.row .text{{font-size:17px;font-weight:500;color:#e2e8f0;line-height:1.5;}}
.row .sub{{font-size:14px;color:#9ca3af;margin-top:2px;}}

.divider{{width:2px;background:rgba(255,255,255,.1);border-radius:1px;}}

.author{{position:absolute;bottom:18px;left:40px;font-size:16px;color:#3a3a3a;font-weight:400;}}
.vs{{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-size:36px;font-weight:900;color:#666;
  background:#0d1b2a;padding:8px 14px;border-radius:8px;z-index:10;
}}
</style></head><body>

<div class="title">③ NG vs OK ─ 戦略の違いがすべてを決める</div>
<div class="subtitle">意志の差ではなく、設計の差</div>

<div class="panels">
  <div class="panel ng">
    <div class="panel-header">
      <div class="badge">NG</div>
      <div class="title-text">「魔法の1手」戦略</div>
    </div>
    <div class="row"><div class="icon">✗</div><div class="text">糖質制限「だけ」を全力でやる<div class="sub">→ 3週間で効果、4週間後にリバウンド</div></div></div>
    <div class="row"><div class="icon">✗</div><div class="text">睡眠が崩れたまま食事制限を強化<div class="sub">→ コルチゾール↑、レプチン↓、夜に止まらない</div></div></div>
    <div class="row"><div class="icon">✗</div><div class="text">「空いた時間に運動する」<div class="sub">→ 忙しい週は必ず空き時間が消える</div></div></div>
    <div class="row"><div class="icon">✗</div><div class="text">崩れた日に「全部やり直し」と力む<div class="sub">→ 2〜3日でまた崩れる</div></div></div>
    <div class="row"><div class="icon">✗</div><div class="text">体重だけを追いかける<div class="sub">→ 内臓脂肪が残っていても数字に騙される</div></div></div>
  </div>

  <div class="panel ok">
    <div class="panel-header">
      <div class="badge">OK</div>
      <div class="title-text">「同時最適化」戦略</div>
    </div>
    <div class="row"><div class="icon">✓</div><div class="text">4要素をそれぞれ20%ずつ整える<div class="sub">→ 良い連鎖が生まれ、維持しやすい</div></div></div>
    <div class="row"><div class="icon">✓</div><div class="text">まず睡眠時刻を固定してから食事制限へ<div class="sub">→ 準備できた状態で制限すると続く</div></div></div>
    <div class="row"><div class="icon">✓</div><div class="text">週4枠をカレンダーに先に入れる<div class="sub">→ 会議と同格に扱い、迷わない</div></div></div>
    <div class="row"><div class="icon">✓</div><div class="text">崩れた翌朝は「就寝時刻だけ戻す」<div class="sub">→ 8勝6敗でOK。1つ戻れば他も戻る</div></div></div>
    <div class="row"><div class="icon">✓</div><div class="text">腹囲・睡眠時刻・活動量・飲酒で見る<div class="sub">→ 体重より正直な4指標</div></div></div>
  </div>
</div>

<div class="vs">VS</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
</body></html>"""
    render(html, "図解③_NG_vs_OK比較表.png")

# ──────────────────────────────────────────────────────────
# 図解④ 実践早見表（4指標テーブル）
# ──────────────────────────────────────────────────────────
def fig4():
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:60px;font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;}}
.subtitle{{position:absolute;top:82px;left:60px;font-size:20px;font-weight:500;color:#9ca3af;}}

.table-wrap{{
  position:absolute;top:140px;left:60px;right:60px;
}}
table{{width:100%;border-collapse:collapse;}}
thead tr{{background:#1e3a5f;}}
thead th{{
  padding:16px 20px;font-size:18px;font-weight:700;color:#38bdf8;
  text-align:left;border-bottom:2px solid #38bdf8;
}}
tbody tr{{border-bottom:1px solid rgba(255,255,255,.06);}}
tbody tr:nth-child(odd){{background:rgba(255,255,255,.03);}}
tbody tr:hover{{background:rgba(56,189,248,.06);}}
tbody td{{padding:20px 20px;font-size:17px;color:#e2e8f0;vertical-align:middle;}}
.indicator{{font-weight:900;color:#fff;}}
.method{{color:#9ca3af;}}
.freq{{
  display:inline-block;padding:4px 12px;border-radius:20px;
  font-size:14px;font-weight:700;
  background:rgba(255,109,0,.15);color:#FF6D00;
}}
.reason{{font-size:14px;color:#64748b;margin-top:4px;}}

.note-box{{
  position:absolute;bottom:30px;left:60px;right:60px;
  background:rgba(74,222,128,.08);border:1.5px solid #4ade80;
  border-radius:12px;padding:16px 24px;
  font-size:16px;font-weight:600;color:#4ade80;text-align:center;
}}
.author{{position:absolute;bottom:18px;left:40px;font-size:16px;color:#3a3a3a;font-weight:400;}}
</style></head><body>

<div class="title">④ 生物学的年齢を追う ─ 実践早見表（4指標）</div>
<div class="subtitle">高価な機器は不要。この4つを週単位で記録するだけでいい</div>

<div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>指標</th>
        <th>測り方</th>
        <th>頻度</th>
        <th>なぜ重要か</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><div class="indicator">🎯 腹囲</div></td>
        <td><div class="method">朝起きてすぐ、へその高さで測る</div></td>
        <td><div class="freq">週1回</div></td>
        <td><div class="reason">内臓脂肪・代謝の最も信頼できる簡易指標</div></td>
      </tr>
      <tr>
        <td><div class="indicator">🌙 睡眠時刻</div></td>
        <td><div class="method">就寝・起床の時刻をメモ or アプリ記録</div></td>
        <td><div class="freq">毎日</div></td>
        <td><div class="reason">炎症・食欲・翌日の行動すべてに影響</div></td>
      </tr>
      <tr>
        <td><div class="indicator">🚶 活動量</div></td>
        <td><div class="method">スマホの歩数 or 運動時間を確認</div></td>
        <td><div class="freq">毎日</div></td>
        <td><div class="reason">代謝・ミトコンドリア機能の維持に直結</div></td>
      </tr>
      <tr>
        <td><div class="indicator">🍺 飲酒回数</div></td>
        <td><div class="method">週に何回飲んだかを記録</div></td>
        <td><div class="freq">週1回</div></td>
        <td><div class="reason">睡眠の質・肝臓・炎症マーカーへの影響大</div></td>
      </tr>
    </tbody>
  </table>
</div>

<div class="note-box">
  悪化していなければ合格 ✓　少しでも改善していれば大成功 ✓✓
</div>

<div class="author">マーシー｜100kg→68kg｜Sub3</div>
</body></html>"""
    render(html, "図解④_実践早見表.png")

# ──────────────────────────────────────────────────────────
# 図解⑤ 崩れた日の復帰フロー（縦型4ステップ）
# ──────────────────────────────────────────────────────────
def fig5():
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:60px;font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;}}
.subtitle{{position:absolute;top:82px;left:60px;font-size:20px;font-weight:500;color:#9ca3af;}}

.flow{{
  position:absolute;top:140px;left:80px;right:80px;
  display:flex;flex-direction:column;gap:0;
}}

.step-row{{display:flex;align-items:center;gap:24px;}}
.step-num{{
  width:56px;height:56px;border-radius:50%;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-size:24px;font-weight:900;color:#0d1b2a;
}}
.step-card{{
  flex:1;border-radius:12px;padding:18px 24px;
  border:1.5px solid rgba(255,255,255,.08);
}}
.step-title{{font-size:20px;font-weight:900;color:#fff;margin-bottom:4px;}}
.step-body{{font-size:15px;font-weight:500;color:#9ca3af;line-height:1.5;}}
.step-badge{{
  display:inline-block;margin-top:6px;padding:3px 10px;border-radius:20px;
  font-size:13px;font-weight:700;
}}

.s1 .step-num{{background:#38bdf8;}}
.s1 .step-card{{background:#0d2035;}}
.s1 .step-badge{{background:rgba(56,189,248,.2);color:#38bdf8;}}

.s2 .step-num{{background:#a78bfa;}}
.s2 .step-card{{background:#160d2a;}}
.s2 .step-badge{{background:rgba(167,139,250,.2);color:#a78bfa;}}

.s3 .step-num{{background:#4ade80;}}
.s3 .step-card{{background:#0d2010;}}
.s3 .step-badge{{background:rgba(74,222,128,.2);color:#4ade80;}}

.s4 .step-num{{background:#FF6D00;}}
.s4 .step-card{{background:#2a1000;}}
.s4 .step-badge{{background:rgba(255,109,0,.2);color:#FF6D00;}}

.arrow-down{{
  text-align:center;font-size:24px;color:#444;
  padding:4px 0;margin-left:80px;
}}

.bottom-msg{{
  position:absolute;bottom:24px;left:0;right:0;text-align:center;
  font-size:20px;font-weight:900;color:#FF6D00;
}}
.author{{position:absolute;bottom:20px;left:40px;font-size:16px;color:#3a3a3a;font-weight:400;}}
</style></head><body>

<div class="title">⑤ 崩れた日の翌朝リセット ─ 4ステップ</div>
<div class="subtitle">全部を取り戻そうとしない。1つ戻せば他も戻る</div>

<div class="flow">
  <div class="step-row s1">
    <div class="step-num">1</div>
    <div class="step-card">
      <div class="step-title">体重計に乗らない</div>
      <div class="step-body">崩れた翌日の体重は水分・食事内容で必ず増える。数字で自己嫌悪になるだけ。</div>
      <div class="step-badge">1〜2日後に乗ればOK</div>
    </div>
  </div>
  <div class="arrow-down">↓</div>
  <div class="step-row s2">
    <div class="step-num">2</div>
    <div class="step-card">
      <div class="step-title">朝食は普通に食べる</div>
      <div class="step-body">「昨日の分を取り戻そう」と制限しない。空腹が強すぎると夜にまた崩れる。</div>
      <div class="step-badge">制限しない・普通に食べる</div>
    </div>
  </div>
  <div class="arrow-down">↓</div>
  <div class="step-row s3">
    <div class="step-num">3</div>
    <div class="step-card">
      <div class="step-title">5分だけ体を動かす</div>
      <div class="step-body">ストレッチでも、その場歩きでもOK。「動いた」という事実が次の行動を引き出す。</div>
      <div class="step-badge">ストレッチ・散歩5分でOK</div>
    </div>
  </div>
  <div class="arrow-down">↓</div>
  <div class="step-row s4">
    <div class="step-num">4</div>
    <div class="step-card">
      <div class="step-title">就寝時刻だけ戻す</div>
      <div class="step-body">食事・運動・体重は後でいい。今夜の寝る時刻だけを昨日より30分前にする。</div>
      <div class="step-badge">これだけでリズムが戻る</div>
    </div>
  </div>
</div>

<div class="bottom-msg">8勝6敗でOK ─ 崩れることより、戻れないことが本当の失敗</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
</body></html>"""
    render(html, "図解⑤_崩れた日の復帰フロー.png")


if __name__ == "__main__":
    print("第42回 図解5枚 生成開始...\n")
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))
