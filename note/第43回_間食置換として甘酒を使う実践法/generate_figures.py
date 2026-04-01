#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第43回 図解生成スクリプト（HTML/CSS + Playwright 強化版）
図解5枚：
  ① 間食暴走ループ（円形フロー）
  ② 目的別使い分け（プロテインvs甘酒カード）
  ③ NG vs OK 比較表
  ④ 甘酒置換ルール実践早見表
  ⑤ 崩れた日の復帰フロー（縦型2ステップ）
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


def fig1():
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:40px;left:60px;font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;}}
.subtitle{{position:absolute;top:84px;left:60px;font-size:20px;font-weight:500;color:#9ca3af;}}

.loop-wrap{{
  position:absolute;left:50%;top:52%;transform:translate(-50%,-48%);
  width:680px;height:460px;
}}
.step{{
  position:absolute;width:180px;padding:14px 12px;border-radius:12px;
  font-size:17px;font-weight:700;color:#fff;text-align:center;line-height:1.4;
  border:2px solid rgba(255,255,255,.1);
}}
.s1{{background:#1e3a5f;top:0;left:50%;transform:translateX(-50%);}}
.s2{{background:#2d1f4e;top:100px;right:0;}}
.s3{{background:#4a1a1a;bottom:100px;right:20px;}}
.s4{{background:#3a1a0a;bottom:100px;left:20px;}}
.s5{{background:#1a3a1a;top:100px;left:0;}}

.arrow{{position:absolute;font-size:15px;font-weight:600;color:#9ca3af;text-align:center;}}
.a12{{top:80px;right:40px;}}
.a23{{bottom:190px;right:10px;}}
.a34{{bottom:70px;left:50%;transform:translateX(-50%);}}
.a45{{bottom:190px;left:10px;}}
.a51{{top:80px;left:40px;}}

.center{{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:140px;height:140px;border-radius:50%;
  background:rgba(239,68,68,.15);border:2px solid #ef4444;
  display:flex;align-items:center;justify-content:center;
  flex-direction:column;text-align:center;
}}
.center .icon{{font-size:32px;}}
.center .label{{font-size:14px;font-weight:700;color:#ef4444;margin-top:4px;}}

.solution{{
  position:absolute;bottom:30px;right:40px;
  background:rgba(56,189,248,.1);border:1.5px solid #38bdf8;
  border-radius:10px;padding:14px 20px;max-width:320px;
}}
.solution .sol-title{{font-size:16px;font-weight:700;color:#38bdf8;margin-bottom:6px;}}
.solution .sol-body{{font-size:14px;font-weight:500;color:#e2e8f0;line-height:1.6;}}
.author{{position:absolute;bottom:20px;left:40px;font-size:16px;color:#3a3a3a;font-weight:400;}}
</style></head><body>
<div class="title">① 15時の間食暴走ループ</div>
<div class="subtitle">なぜ「今日だけ」が毎日続くのか</div>
<div class="loop-wrap">
  <div class="step s1">15時<br>「疲れた…」</div>
  <div class="step s2">コンビニで<br>ポテチ＋チョコ</div>
  <div class="step s3">帰宅後<br>さらに夜食</div>
  <div class="step s4">自己嫌悪<br>「明日からやめる」</div>
  <div class="step s5">翌日また<br>15時に崩れる</div>
  <div class="arrow a12">↘ 衝動買い</div>
  <div class="arrow a23">↓ 血糖崩壊</div>
  <div class="arrow a34">← 過食</div>
  <div class="arrow a45">↑ 罪悪感</div>
  <div class="arrow a51">↗ リセット失敗</div>
  <div class="center">
    <div class="icon">🔄</div>
    <div class="label">毎日<br>ループ</div>
  </div>
</div>
<div class="solution">
  <div class="sol-title">✅ 断ち切る方法</div>
  <div class="sol-body">15〜17時に甘酒100mlを<br>「置換」で入れる。<br>我慢ではなく置き換え。</div>
</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
</body></html>"""
    render(html, "図解①_間食暴走ループ.png")


def fig2():
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:60px;font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;}}
.subtitle{{position:absolute;top:82px;left:60px;font-size:20px;font-weight:500;color:#9ca3af;}}

.cards{{
  position:absolute;top:140px;left:60px;right:60px;
  display:flex;gap:32px;
}}
.card{{
  flex:1;border-radius:16px;padding:28px 24px;
  display:flex;flex-direction:column;align-items:center;text-align:center;
  border:1.5px solid rgba(255,255,255,.08);
}}
.c1{{background:#0d2035;}}
.c2{{background:#2a1000;}}
.c3{{background:#0d2010;}}

.card .icon{{font-size:48px;margin-bottom:14px;}}
.card .name{{font-size:24px;font-weight:900;color:#fff;margin-bottom:10px;}}
.card .purpose{{
  font-size:15px;font-weight:600;padding:6px 14px;border-radius:20px;
  margin-bottom:16px;
}}
.c1 .purpose{{background:rgba(56,189,248,.15);color:#38bdf8;}}
.c2 .purpose{{background:rgba(255,109,0,.15);color:#FF6D00;}}
.c3 .purpose{{background:rgba(74,222,128,.15);color:#4ade80;}}

.card .desc{{font-size:15px;font-weight:500;color:#9ca3af;line-height:1.6;}}
.card .timing{{
  margin-top:auto;padding-top:16px;
  font-size:14px;font-weight:700;color:#fff;
  border-top:1px solid rgba(255,255,255,.06);
  width:100%;
}}

.bottom-note{{
  position:absolute;bottom:28px;left:0;right:0;text-align:center;
  font-size:18px;font-weight:700;color:#FF6D00;
}}
.author{{position:absolute;bottom:20px;left:40px;font-size:16px;color:#3a3a3a;font-weight:400;}}
</style></head><body>
<div class="title">② 目的別使い分け ─ プロテイン vs 甘酒</div>
<div class="subtitle">「どちらが上か」ではなく「いつ・何を・なぜ使うか」</div>
<div class="cards">
  <div class="card c1">
    <div class="icon">💪</div>
    <div class="name">プロテイン</div>
    <div class="purpose">筋量維持・たんぱく質確保</div>
    <div class="desc">筋トレ後の回復に最適。<br>たんぱく質が20〜30g摂れる。<br>甘酒では代替できない領域。</div>
    <div class="timing">⏰ 筋トレ後・朝食時</div>
  </div>
  <div class="card c2">
    <div class="icon">🍶</div>
    <div class="name">甘酒（置換用）</div>
    <div class="purpose">間食暴走対策・甘味欲の緩和</div>
    <div class="desc">100〜150mlで甘味欲を<br>ゼロにせず整える。<br>血糖クラッシュを緩め<br>夜の過食を予防。</div>
    <div class="timing">⏰ 15〜17時の間食タイム</div>
  </div>
  <div class="card c3">
    <div class="icon">🤝</div>
    <div class="name">両方使う</div>
    <div class="purpose">タイミングを分けて両立</div>
    <div class="desc">筋トレ後 → プロテイン<br>15〜17時 → 甘酒<br>目的が違えば競合しない。<br>両方使ってOK。</div>
    <div class="timing">⏰ 目的で使い分ける</div>
  </div>
</div>
<div class="bottom-note">勝負は「何を飲むか」ではなく「どこで何を置き換えるか」</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
</body></html>"""
    render(html, "図解②_目的別使い分け.png")


def fig3():
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:60px;font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;}}
.subtitle{{position:absolute;top:82px;left:60px;font-size:20px;font-weight:500;color:#9ca3af;}}

.panels{{
  position:absolute;top:130px;left:40px;right:40px;bottom:60px;
  display:flex;gap:28px;
}}
.panel{{flex:1;border-radius:16px;padding:28px 24px;display:flex;flex-direction:column;gap:16px;}}
.ng{{background:rgba(127,29,29,.25);border:1.5px solid #ef4444;}}
.ok{{background:rgba(20,83,45,.25);border:1.5px solid #4ade80;}}

.panel-header{{display:flex;align-items:center;gap:14px;margin-bottom:6px;}}
.panel-header .badge{{font-size:26px;font-weight:900;padding:6px 14px;border-radius:8px;}}
.ng .badge{{background:#ef4444;color:#fff;}}
.ok .badge{{background:#4ade80;color:#0d1b2a;}}
.panel-header .title-text{{font-size:20px;font-weight:900;color:#fff;}}

.row{{display:flex;align-items:flex-start;gap:10px;}}
.row .icon{{font-size:18px;flex-shrink:0;margin-top:2px;}}
.row .text{{font-size:16px;font-weight:500;color:#e2e8f0;line-height:1.5;}}
.row .sub{{font-size:13px;color:#9ca3af;margin-top:2px;}}

.vs{{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-size:34px;font-weight:900;color:#666;
  background:#0d1b2a;padding:8px 12px;border-radius:8px;z-index:10;
}}
.author{{position:absolute;bottom:18px;left:40px;font-size:16px;color:#3a3a3a;font-weight:400;}}
</style></head><body>
<div class="title">③ 甘酒の使い方 ─ NG vs OK</div>
<div class="subtitle">「体にいいから」で足し算すると失敗する</div>
<div class="panels">
  <div class="panel ng">
    <div class="panel-header">
      <div class="badge">NG</div>
      <div class="title-text">足し算パターン</div>
    </div>
    <div class="row"><div class="icon">✗</div><div class="text">コップになみなみ200ml以上<div class="sub">→ カロリー150kcal超。お菓子と変わらない</div></div></div>
    <div class="row"><div class="icon">✗</div><div class="text">夜11時に追加で飲む<div class="sub">→ 就寝前の追加カロリー＋血糖上昇</div></div></div>
    <div class="row"><div class="icon">✗</div><div class="text">甘酒＋チョコのセット<div class="sub">→ 「体にいいから」併用は置換の意味なし</div></div></div>
    <div class="row"><div class="icon">✗</div><div class="text">量も時間もバラバラ<div class="sub">→ ルールなし = 効果なし</div></div></div>
    <div class="row"><div class="icon">✗</div><div class="text">「飲む点滴」を鵜呑み<div class="sub">→ 過大評価は崩れの元</div></div></div>
  </div>
  <div class="panel ok">
    <div class="panel-header">
      <div class="badge">OK</div>
      <div class="title-text">置換パターン</div>
    </div>
    <div class="row"><div class="icon">✓</div><div class="text">100〜150mlに量を固定<div class="sub">→ 紙パック1本がちょうどいい</div></div></div>
    <div class="row"><div class="icon">✓</div><div class="text">15〜17時の間食タイムに固定<div class="sub">→ 血糖クラッシュを緩めて夜の過食を防ぐ</div></div></div>
    <div class="row"><div class="icon">✓</div><div class="text">単体で終える（お菓子なし）<div class="sub">→ 甘酒だけで甘味欲を整える</div></div></div>
    <div class="row"><div class="icon">✓</div><div class="text">同じ商品を同じ量で回す<div class="sub">→ ルール化された行動は続きやすい</div></div></div>
    <div class="row"><div class="icon">✓</div><div class="text">8勝6敗で合格<div class="sub">→ 崩れた翌日に戻せばOK</div></div></div>
  </div>
</div>
<div class="vs">VS</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
</body></html>"""
    render(html, "図解③_NG_vs_OK比較表.png")


def fig4():
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:60px;font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;}}
.subtitle{{position:absolute;top:82px;left:60px;font-size:20px;font-weight:500;color:#9ca3af;}}

.table-wrap{{position:absolute;top:130px;left:60px;right:60px;}}
table{{width:100%;border-collapse:collapse;}}
thead tr{{background:#1e3a5f;}}
thead th{{padding:14px 18px;font-size:17px;font-weight:700;color:#38bdf8;text-align:left;border-bottom:2px solid #38bdf8;}}
tbody tr{{border-bottom:1px solid rgba(255,255,255,.06);}}
tbody tr:nth-child(odd){{background:rgba(255,255,255,.03);}}
tbody td{{padding:18px;font-size:16px;color:#e2e8f0;vertical-align:middle;}}
.rule-name{{font-weight:900;color:#fff;font-size:18px;}}
.rule-detail{{color:#9ca3af;font-size:14px;margin-top:3px;}}
.badge{{
  display:inline-block;padding:4px 12px;border-radius:20px;
  font-size:13px;font-weight:700;
  background:rgba(255,109,0,.15);color:#FF6D00;
}}

.cost-box{{
  position:absolute;bottom:24px;left:60px;right:60px;
  display:flex;gap:20px;
}}
.cost-card{{
  flex:1;border-radius:12px;padding:14px 18px;text-align:center;
}}
.cost-ng{{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);}}
.cost-ok{{background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.3);}}
.cost-save{{background:rgba(255,109,0,.1);border:1px solid rgba(255,109,0,.3);}}
.cost-label{{font-size:14px;font-weight:600;margin-bottom:4px;}}
.cost-ng .cost-label{{color:#ef4444;}}
.cost-ok .cost-label{{color:#4ade80;}}
.cost-save .cost-label{{color:#FF6D00;}}
.cost-value{{font-size:22px;font-weight:900;color:#fff;}}

.author{{position:absolute;bottom:18px;left:40px;font-size:16px;color:#3a3a3a;font-weight:400;}}
</style></head><body>
<div class="title">④ 甘酒置換ルール ─ 実践早見表</div>
<div class="subtitle">この4つを固定するだけで間食暴走が止まる</div>
<div class="table-wrap">
  <table>
    <thead><tr><th>ルール</th><th>内容</th><th>ポイント</th></tr></thead>
    <tbody>
      <tr>
        <td><div class="rule-name">①量を固定</div></td>
        <td>1回 100〜150ml<div class="rule-detail">紙パック1本。おかわり禁止</div></td>
        <td><div class="badge">物理的に制限</div></td>
      </tr>
      <tr>
        <td><div class="rule-name">②時間を固定</div></td>
        <td>15〜17時の間食タイム<div class="rule-detail">夜食なら就寝2時間前まで</div></td>
        <td><div class="badge">血糖クラッシュ対策</div></td>
      </tr>
      <tr>
        <td><div class="rule-name">③単体で終える</div></td>
        <td>甘酒＋お菓子は禁止<div class="rule-detail">置換なので併用しない</div></td>
        <td><div class="badge">追加カロリー防止</div></td>
      </tr>
      <tr>
        <td><div class="rule-name">④週単位で評価</div></td>
        <td>8勝6敗で合格<div class="rule-detail">崩れた翌日に戻せばOK</div></td>
        <td><div class="badge">完璧より継続</div></td>
      </tr>
    </tbody>
  </table>
</div>
<div class="cost-box">
  <div class="cost-card cost-ng">
    <div class="cost-label">❌ 以前の間食代</div>
    <div class="cost-value">月10,000円超</div>
  </div>
  <div class="cost-card cost-ok">
    <div class="cost-label">✅ 甘酒置換後</div>
    <div class="cost-value">月3,000〜4,500円</div>
  </div>
  <div class="cost-card cost-save">
    <div class="cost-label">💰 月の節約額</div>
    <div class="cost-value">5,000円以上</div>
  </div>
</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
</body></html>"""
    render(html, "図解④_実践早見表.png")


def fig5():
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:60px;font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;}}
.subtitle{{position:absolute;top:82px;left:60px;font-size:20px;font-weight:500;color:#9ca3af;}}

.crash-label{{
  position:absolute;top:130px;left:60px;
  background:rgba(239,68,68,.15);border:1.5px solid #ef4444;
  border-radius:8px;padding:10px 18px;
  font-size:17px;font-weight:700;color:#ef4444;
}}

.flow{{
  position:absolute;top:200px;left:80px;right:80px;
  display:flex;flex-direction:column;gap:0;
}}
.step-row{{display:flex;align-items:center;gap:24px;}}
.step-num{{
  width:60px;height:60px;border-radius:50%;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-size:26px;font-weight:900;
}}
.step-card{{
  flex:1;border-radius:12px;padding:22px 28px;
  border:1.5px solid rgba(255,255,255,.08);
}}
.step-title{{font-size:22px;font-weight:900;color:#fff;margin-bottom:6px;}}
.step-body{{font-size:16px;font-weight:500;color:#9ca3af;line-height:1.5;}}
.step-badge{{
  display:inline-block;margin-top:8px;padding:4px 12px;border-radius:20px;
  font-size:14px;font-weight:700;
}}

.s1 .step-num{{background:#38bdf8;color:#0d1b2a;}}
.s1 .step-card{{background:#0d2035;}}
.s1 .step-badge{{background:rgba(56,189,248,.2);color:#38bdf8;}}

.s2 .step-num{{background:#FF6D00;color:#fff;}}
.s2 .step-card{{background:#2a1000;}}
.s2 .step-badge{{background:rgba(255,109,0,.2);color:#FF6D00;}}

.arrow-down{{text-align:center;font-size:28px;color:#444;padding:8px 0;margin-left:90px;}}

.result-box{{
  position:absolute;bottom:28px;left:60px;right:60px;
  background:rgba(74,222,128,.08);border:1.5px solid #4ade80;
  border-radius:12px;padding:16px 24px;text-align:center;
}}
.result-box .r-title{{font-size:22px;font-weight:900;color:#4ade80;}}
.result-box .r-sub{{font-size:15px;color:#9ca3af;margin-top:6px;}}
.author{{position:absolute;bottom:20px;left:40px;font-size:16px;color:#3a3a3a;font-weight:400;}}
</style></head><body>
<div class="title">⑤ 崩れた日の翌日リセット ─ 2つだけ</div>
<div class="subtitle">「全部やり直そう」は禁止。この2つだけで戻れる</div>

<div class="crash-label">⚠️ コンビニに寄ってしまった / お菓子を食べた / 甘酒を切らしていた</div>

<div class="flow">
  <div class="step-row s1">
    <div class="step-num">1</div>
    <div class="step-card">
      <div class="step-title">甘酒を1本買い足す</div>
      <div class="step-body">物理的にストックを切らさない。「ないから買えない」をなくす。帰り道のコンビニかスーパーで1本だけ。</div>
      <div class="step-badge">ストック確保 = 仕組みの復旧</div>
    </div>
  </div>
  <div class="arrow-down">↓</div>
  <div class="step-row s2">
    <div class="step-num">2</div>
    <div class="step-card">
      <div class="step-title">翌日の15〜17時に1回だけ甘酒に戻す</div>
      <div class="step-body">全部やり直す必要なし。「1回の成功」が次の1週間を作る。この1回がリズムを復旧させる。</div>
      <div class="step-badge">1回の成功 → 次の1週間</div>
    </div>
  </div>
</div>

<div class="result-box">
  <div class="r-title">8勝6敗でOK ─ 崩れることより、戻れないことが本当の失敗</div>
  <div class="r-sub">完璧を狙わない。1回戻せば、他も自然に戻ってくる</div>
</div>
<div class="author">マーシー｜100kg→68kg｜Sub3</div>
</body></html>"""
    render(html, "図解⑤_崩れた日の復帰フロー.png")


if __name__ == "__main__":
    print("第43回 図解5枚 生成開始...\n")
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))
