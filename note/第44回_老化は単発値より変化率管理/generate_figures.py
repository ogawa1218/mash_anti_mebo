#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第44回 図解生成スクリプト（HTML/CSS + Playwright 強化版）
テーマ：老化は単発値より変化率管理
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
    """図解①：単発値 vs 変化率（左右比較）"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:56px;font-size:32px;font-weight:900;color:#fff;}}
.title span{{color:#FF6D00;}}
.container{{display:flex;gap:40px;position:absolute;top:110px;left:56px;right:56px;bottom:60px;}}
.panel{{flex:1;border-radius:18px;padding:36px;position:relative;}}
.panel-ng{{background:rgba(239,68,68,.12);border:2px solid #ef4444;}}
.panel-ok{{background:rgba(74,222,128,.10);border:2px solid #4ade80;}}
.panel-label{{font-size:22px;font-weight:900;margin-bottom:18px;}}
.label-ng{{color:#ef4444;}}
.label-ok{{color:#4ade80;}}
.panel h3{{font-size:26px;font-weight:800;color:#fff;margin-bottom:20px;}}
.item{{display:flex;align-items:center;margin-bottom:16px;}}
.icon{{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;margin-right:14px;flex-shrink:0;}}
.icon-ng{{background:rgba(239,68,68,.25);color:#ef4444;}}
.icon-ok{{background:rgba(74,222,128,.2);color:#4ade80;}}
.item-text{{font-size:20px;color:#d1d5db;line-height:1.5;}}
.item-text strong{{color:#fff;}}
.result{{position:absolute;bottom:28px;left:36px;right:36px;padding:14px;border-radius:10px;text-align:center;font-size:20px;font-weight:700;}}
.result-ng{{background:rgba(239,68,68,.15);color:#ef4444;}}
.result-ok{{background:rgba(74,222,128,.12);color:#4ade80;}}
.footer{{position:absolute;bottom:18px;right:56px;font-size:16px;color:#555;}}
</style></head><body>
<div class="title">単発値 vs <span>変化率</span>｜どちらが将来を予測するか</div>
<div class="container">
  <div class="panel panel-ng">
    <div class="panel-label label-ng">✗ 単発値で判断</div>
    <h3>1回の数字で安心</h3>
    <div class="item"><div class="icon icon-ng">①</div><div class="item-text">健診1回「セーフ」→ <strong>油断</strong></div></div>
    <div class="item"><div class="icon icon-ng">②</div><div class="item-text">3か月ダラけて<strong>生活崩壊</strong></div></div>
    <div class="item"><div class="icon icon-ng">③</div><div class="item-text">翌年<strong>E判定に逆戻り</strong></div></div>
    <div class="item"><div class="icon icon-ng">④</div><div class="item-text">「もうダメだ…」→ <strong>自己嫌悪</strong></div></div>
    <div class="result result-ng">数字の点しか見ていない</div>
  </div>
  <div class="panel panel-ok">
    <div class="panel-label label-ok">✓ 変化率で管理</div>
    <h3>傾きの方向を追う</h3>
    <div class="item"><div class="icon icon-ok">①</div><div class="item-text">週単位で<strong>傾き</strong>を確認</div></div>
    <div class="item"><div class="icon icon-ok">②</div><div class="item-text">小さな改善を<strong>同時に積む</strong></div></div>
    <div class="item"><div class="icon icon-ok">③</div><div class="item-text">体重横ばいでも<strong>腹囲は減少</strong></div></div>
    <div class="item"><div class="icon icon-ok">④</div><div class="item-text">「先週よりマシ」→ <strong>継続</strong></div></div>
    <div class="result result-ok">6〜12か月で傾きが変わる</div>
  </div>
</div>
<div class="footer">Belsky et al., PNAS 2015（Dunedin Study）</div>
</body></html>"""
    render(html, "図解①_単発値vs変化率.png")


def fig2():
    """図解②：3つの実務ポイント（横3列カード）"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:56px;font-size:32px;font-weight:900;color:#fff;}}
.title span{{color:#38bdf8;}}
.cards{{display:flex;gap:32px;position:absolute;top:120px;left:56px;right:56px;}}
.card{{flex:1;background:#1e3a5f;border-radius:18px;padding:32px 28px;position:relative;border-top:4px solid;}}
.card:nth-child(1){{border-color:#FF6D00;}}
.card:nth-child(2){{border-color:#38bdf8;}}
.card:nth-child(3){{border-color:#4ade80;}}
.num{{font-size:48px;font-weight:900;margin-bottom:12px;}}
.card:nth-child(1) .num{{color:#FF6D00;}}
.card:nth-child(2) .num{{color:#38bdf8;}}
.card:nth-child(3) .num{{color:#4ade80;}}
.card h3{{font-size:24px;font-weight:800;color:#fff;margin-bottom:16px;line-height:1.3;}}
.card p{{font-size:18px;color:#9ca3af;line-height:1.7;}}
.card p strong{{color:#fff;}}
.arrow{{position:absolute;top:260px;font-size:36px;color:#555;}}
.arrow1{{left:398px;}}
.arrow2{{left:828px;}}
.bottom{{position:absolute;bottom:36px;left:56px;right:56px;background:rgba(255,109,0,.08);border:1px solid rgba(255,109,0,.3);border-radius:14px;padding:20px 32px;text-align:center;}}
.bottom p{{font-size:22px;font-weight:700;color:#FF6D00;}}
.footer{{position:absolute;bottom:14px;right:56px;font-size:14px;color:#444;}}
</style></head><body>
<div class="title">研究を実務に翻訳する<span>3つのポイント</span></div>
<div class="cards">
  <div class="card">
    <div class="num">01</div>
    <h3>派手な一発を<br>追いすぎない</h3>
    <p>サプリで一時的に数値改善しても<strong>土台が崩れていたら意味なし</strong>。一発逆転思考は研究が最も否定。</p>
  </div>
  <div class="card">
    <div class="num">02</div>
    <h3>小さい改善を<br>同時に積む</h3>
    <p>睡眠を少し整える。食後に少し歩く。夜食を少し減らす。<strong>「少しずつ×同時に」</strong>が最前線の戦略。</p>
  </div>
  <div class="card">
    <div class="num">03</div>
    <h3>週次・月次で<br>傾きを確認</h3>
    <p>1日単位で一喜一憂しない。<strong>「今週は先週よりマシか」</strong>。この問いだけで十分。</p>
  </div>
</div>
<span class="arrow arrow1">→</span>
<span class="arrow arrow2">→</span>
<div class="bottom">
  <p>完璧な健康生活ではなく「悪化しない仕組み」を作る</p>
</div>
</body></html>"""
    render(html, "図解②_3つの実務ポイント.png")


def fig3():
    """図解③：NG vs OK 比較表"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:56px;font-size:32px;font-weight:900;color:#fff;}}
.title span{{color:#FF6D00;}}
.table-wrap{{position:absolute;top:110px;left:56px;right:56px;}}
table{{width:100%;border-collapse:separate;border-spacing:0 8px;}}
th{{font-size:18px;font-weight:700;padding:14px 20px;text-align:left;}}
th:nth-child(1){{color:#9ca3af;width:30%;}}
th:nth-child(2){{color:#ef4444;width:35%;}}
th:nth-child(3){{color:#4ade80;width:35%;}}
td{{padding:16px 20px;font-size:19px;color:#d1d5db;}}
tr.row{{background:#0d2035;border-radius:10px;}}
tr.row td:first-child{{border-radius:10px 0 0 10px;font-weight:700;color:#fff;}}
tr.row td:last-child{{border-radius:0 10px 10px 0;}}
.ng{{color:#ef4444;}}
.ok{{color:#4ade80;}}
.badge{{display:inline-block;padding:3px 10px;border-radius:6px;font-size:14px;font-weight:700;margin-right:6px;}}
.badge-ng{{background:rgba(239,68,68,.2);color:#ef4444;}}
.badge-ok{{background:rgba(74,222,128,.15);color:#4ade80;}}
.footer{{position:absolute;bottom:18px;left:56px;font-size:16px;color:#555;}}
</style></head><body>
<div class="title">体重停滞期の判断｜<span>NG vs OK</span></div>
<div class="table-wrap">
<table>
<tr><th>チェック項目</th><th><span class="badge badge-ng">✗</span> NGパターン</th><th><span class="badge badge-ok">✓</span> OKパターン</th></tr>
<tr class="row"><td>体重</td><td class="ng">毎日測って一喜一憂</td><td class="ok">週2回測って平均で判断</td></tr>
<tr class="row"><td>腹囲</td><td class="ng">測っていない</td><td class="ok">週1回へその高さで計測</td></tr>
<tr class="row"><td>睡眠</td><td class="ng">夜更かしが増えている</td><td class="ok">就寝時刻が安定している</td></tr>
<tr class="row"><td>活動量</td><td class="ng">歩数が毎月減っている</td><td class="ok">歩数 or 運動時間を記録</td></tr>
<tr class="row"><td>評価方法</td><td class="ng">1回の数字で安心 or 絶望</td><td class="ok">「先週よりマシか」で判断</td></tr>
<tr class="row"><td>停滞期の判断</td><td class="ng">体重が動かない＝失敗</td><td class="ok">腹囲が減っていれば継続</td></tr>
</table>
</div>
<div class="footer">マーシー実体験：体重横ばい3か月でも腹囲95cm→91cm</div>
</body></html>"""
    render(html, "図解③_NG vs OK比較表.png")


def fig4():
    """図解④：実践早見表（4指標ダッシュボード）"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:56px;font-size:32px;font-weight:900;color:#fff;}}
.title span{{color:#38bdf8;}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:24px;position:absolute;top:110px;left:56px;right:56px;}}
.card{{background:#1e3a5f;border-radius:16px;padding:28px 24px;border-left:5px solid;}}
.card:nth-child(1){{border-color:#FF6D00;}}
.card:nth-child(2){{border-color:#38bdf8;}}
.card:nth-child(3){{border-color:#4ade80;}}
.card:nth-child(4){{border-color:#a78bfa;}}
.card-title{{font-size:28px;font-weight:900;color:#fff;margin-bottom:10px;}}
.card-freq{{font-size:16px;font-weight:700;padding:4px 12px;border-radius:20px;display:inline-block;margin-bottom:14px;}}
.card:nth-child(1) .card-freq{{background:rgba(255,109,0,.15);color:#FF6D00;}}
.card:nth-child(2) .card-freq{{background:rgba(56,189,248,.15);color:#38bdf8;}}
.card:nth-child(3) .card-freq{{background:rgba(74,222,128,.12);color:#4ade80;}}
.card:nth-child(4) .card-freq{{background:rgba(167,139,250,.15);color:#a78bfa;}}
.card-how{{font-size:18px;color:#9ca3af;line-height:1.6;}}
.card-how strong{{color:#fff;}}
.bottom-bar{{position:absolute;bottom:32px;left:56px;right:56px;display:flex;gap:20px;align-items:center;justify-content:center;}}
.tip{{background:rgba(255,109,0,.08);border:1px solid rgba(255,109,0,.3);border-radius:12px;padding:14px 28px;}}
.tip p{{font-size:20px;font-weight:700;color:#FF6D00;text-align:center;}}
.footer{{position:absolute;bottom:10px;right:56px;font-size:14px;color:#444;}}
</style></head><body>
<div class="title">4指標ダッシュボード｜<span>これだけ追う</span></div>
<div class="grid">
  <div class="card">
    <div class="card-title">体重</div>
    <div class="card-freq">週2〜3回</div>
    <div class="card-how"><strong>朝起きてすぐ</strong>測定<br>週の平均で先月と比較</div>
  </div>
  <div class="card">
    <div class="card-title">腹囲</div>
    <div class="card-freq">週1回</div>
    <div class="card-how"><strong>へその高さ</strong>で計測<br>体重より先に内臓脂肪を反映</div>
  </div>
  <div class="card">
    <div class="card-title">睡眠</div>
    <div class="card-freq">毎日ざっくり</div>
    <div class="card-how"><strong>就寝・起床時刻</strong>を記録<br>夜更かし頻度の変化を見る</div>
  </div>
  <div class="card">
    <div class="card-title">活動量</div>
    <div class="card-freq">毎日</div>
    <div class="card-how"><strong>歩数 or 運動時間</strong><br>月単位の傾きで評価する</div>
  </div>
</div>
<div class="bottom-bar">
  <div class="tip"><p>毎日完璧に記録しない。週で傾きを見る。</p></div>
</div>
</body></html>"""
    render(html, "図解④_実践早見表.png")


def fig5():
    """図解⑤：崩れた日の復帰フロー（縦型3ステップ）"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
body{{background:#0d1b2a;}}
.title{{position:absolute;top:36px;left:56px;font-size:32px;font-weight:900;color:#fff;}}
.title span{{color:#4ade80;}}
.flow{{position:absolute;top:110px;left:50%;transform:translateX(-50%);width:700px;}}
.step{{display:flex;align-items:flex-start;margin-bottom:12px;position:relative;}}
.step-num{{width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900;flex-shrink:0;margin-right:24px;}}
.step:nth-child(1) .step-num{{background:rgba(239,68,68,.2);color:#ef4444;border:2px solid #ef4444;}}
.step:nth-child(3) .step-num{{background:rgba(255,109,0,.15);color:#FF6D00;border:2px solid #FF6D00;}}
.step:nth-child(5) .step-num{{background:rgba(74,222,128,.15);color:#4ade80;border:2px solid #4ade80;}}
.step-content{{background:#1e3a5f;border-radius:14px;padding:22px 28px;flex:1;}}
.step-content h3{{font-size:22px;font-weight:800;color:#fff;margin-bottom:8px;}}
.step-content p{{font-size:18px;color:#9ca3af;line-height:1.5;}}
.step-content p strong{{color:#fff;}}
.connector{{display:flex;align-items:center;justify-content:center;margin:4px 0 4px 16px;}}
.connector .arrow-down{{font-size:32px;font-weight:900;}}
.step:nth-child(1) ~ .connector .arrow-down{{color:#FF6D00;}}
.c1 .arrow-down{{color:#FF6D00;}}
.c2 .arrow-down{{color:#4ade80;}}
.badge-box{{position:absolute;bottom:36px;left:50%;transform:translateX(-50%);background:rgba(74,222,128,.08);border:2px solid rgba(74,222,128,.3);border-radius:16px;padding:18px 48px;text-align:center;}}
.badge-box p{{font-size:24px;font-weight:900;color:#4ade80;}}
.badge-box span{{font-size:16px;color:#9ca3af;display:block;margin-top:6px;}}
.footer{{position:absolute;bottom:12px;right:56px;font-size:14px;color:#444;}}
</style></head><body>
<div class="title">崩れた日の<span>復帰フロー</span></div>
<div class="flow">
  <div class="step">
    <div class="step-num">1</div>
    <div class="step-content">
      <h3>崩れた日（歩けなかった）</h3>
      <p>「全部やり直し」は<strong>禁止</strong>。<br>崩れること自体は失敗ではない。</p>
    </div>
  </div>
  <div class="connector c1"><span class="arrow-down">↓</span></div>
  <div class="step">
    <div class="step-num">2</div>
    <div class="step-content">
      <h3>カレンダーを翌日にスライド</h3>
      <p>予定を<strong>消さない。移すだけ</strong>。<br>移動するだけで「仕組み」は生きている。</p>
    </div>
  </div>
  <div class="connector c2"><span class="arrow-down">↓</span></div>
  <div class="step">
    <div class="step-num">3</div>
    <div class="step-content">
      <h3>翌日の食後10分だけ歩く</h3>
      <p><strong>1回戻せば</strong>、他も自然に戻る。<br>完璧に戻す必要はない。</p>
    </div>
  </div>
</div>
<div class="badge-box">
  <p>8勝6敗でOK</p>
  <span>崩れることより「戻れないこと」が本当の失敗</span>
</div>
</body></html>"""
    render(html, "図解⑤_崩れた日の復帰フロー.png")


if __name__ == "__main__":
    print("第44回 図解5枚 生成開始...\n")
    fig1(); fig2(); fig3(); fig4(); fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))
