#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第44回 X投稿用カード画像 10枚生成スクリプト（図解版）
テーマ：老化は単発値より変化率管理
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
HASHTAG = "#第44回 変化率管理"

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;background:#0d1b2a;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
    ".num{position:absolute;top:44px;right:56px;font-size:22px;font-weight:700;color:#444;}"
    ".author{position:absolute;bottom:22px;left:56px;font-size:18px;font-weight:400;color:#3a3a3a;}"
    ".series{position:absolute;bottom:22px;right:56px;font-size:18px;font-weight:700;}"
)

TWEETS = [
    "去年の健診、血糖値がギリギリ「セーフ」だった。\n\n「もう大丈夫だろう」\n\n3か月ダラけた翌年、E判定に逆戻り。\nしかも前年より悪化。\n\n1回の数字は何も保証しない。\n大事なのは「どっちに動いているか」。\n\n↓続き（2/10）",

    "Dunedin Study（Belsky et al., PNAS 2015）。\n1,000人以上を38年追跡した結果：\n\n同じ38歳でも、生物学的な老化速度が\n速い人と遅い人で10年後の健康に大差。\n\n「今何歳相当か」の単発値より\n「悪化のスピードをどう抑えるか」が本質。\n\n↓続き（3/10）",

    "老化対策の最適解は3つ：\n\n①派手な一発を追わない\n②小さい改善を同時に積む\n③週次で傾きを確認\n\n「若返りの一発逆転」じゃなく\n「悪化の傾きを下げる設計」。\n\nこれが忙しい会社員の現実解。\n\n↓続き（4/10）",

    "高い検査の前に、まず4つだけ追う：\n\n・体重（週2〜3回・朝イチ）\n・腹囲（週1回・へその高さ）\n・睡眠時刻（毎日ざっくり）\n・活動量（歩数 or 運動時間）\n\n完璧に記録しない。\n週で傾きを見るだけ。\n\n↓続き（5/10）",

    "100kgから落とす過程で\n体重が3か月間まったく動かなかった。\n\n「もう効果ないんじゃ…」と挫折しかけた。\n\nでも腹囲は95cm→91cmに減っていた。\n最終的に78cmまで到達。\n\n体重だけ見てたら辞めてた。\n変化率で見るから続けられた。\n\n↓続き（6/10）",

    "体重が停滞しても、これが動いていれば勝ち：\n\n✓ 腹囲が少し減った\n✓ 夜更かしが減った\n✓ 歩く頻度が増えた\n✓ 間食回数が減った\n\n体重だけで自分を否定すると継続が切れる。\n行動の傾きを守った人が最後に勝つ。\n\n↓続き（7/10）",

    "傾きを変える3ステップ：\n\nSTEP1：固定ルール1つ\n→「夕食後10分歩く」だけ\n\nSTEP2：カレンダーに先入れ\n→ 会議と同じ扱い\n\nSTEP3：週1レビュー\n→ 8勝6敗で合格\n\n食後10分歩行で血糖ピークが下がる\n（Buffey et al., 2022）\n\n↓続き（8/10）",

    "崩れた日のリセットは2つだけ：\n\n①カレンダーを翌日にスライド（消さない）\n②翌日の食後に10分だけ歩く\n\n「全部やり直し」は禁止。\n1回戻せば他も自然に戻る。\n\n8勝6敗でOK。\n崩れることより戻れないことが本当の失敗。\n\n↓続き（9/10）",

    "Dunedin Study（2015）の教訓：\n\n老化速度が速い人の特徴は\n「1つの数値が悪い」じゃなく\n「複数の指標が同時にゆるく悪化」。\n\nだから逆も同じ。\n複数の指標を少しずつ同時に改善する。\nこれが最も再現性の高い戦略。\n\n↓続き（10/10）",

    "今日やること1つだけ：\n\n今夜の食後10分歩行を\nカレンダーに登録してください。\n毎日同じ時刻で固定。\n\n全部やらなくていい。\nこの1つが明日のあなたを変える。\n\nnoteで詳細👇\nhttps://note.com/mash_anti_metabo",
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]

ACCENT_COLORS = [
    "#38bdf8", "#38bdf8", "#FF6D00", "#38bdf8", "#4ade80",
    "#38bdf8", "#FF6D00", "#4ade80", "#38bdf8", "#FF6D00",
]


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
    """共感 → タイムライン型"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.title{{position:absolute;left:56px;top:56px;font-size:36px;font-weight:900;color:#fff;letter-spacing:-1px;}}
.timeline{{position:absolute;top:130px;left:100px;}}
.tl-item{{display:flex;align-items:flex-start;margin-bottom:20px;position:relative;}}
.tl-dot{{width:18px;height:18px;border-radius:50%;margin-right:24px;margin-top:6px;flex-shrink:0;}}
.tl-line{{position:absolute;left:8px;top:24px;width:2px;height:60px;background:#333;}}
.tl-year{{font-size:22px;font-weight:700;color:#38bdf8;width:100px;flex-shrink:0;}}
.tl-text{{font-size:22px;color:#d1d5db;line-height:1.5;}}
.tl-text strong{{color:#fff;}}
.tl-item:nth-child(1) .tl-dot{{background:#4ade80;}}
.tl-item:nth-child(2) .tl-dot{{background:#FF6D00;}}
.tl-item:nth-child(3) .tl-dot{{background:#ef4444;}}
.tl-item:nth-child(4) .tl-dot{{background:#ef4444;}}
.msg{{position:absolute;bottom:80px;left:56px;right:56px;background:rgba(56,189,248,.08);border:1px solid rgba(56,189,248,.3);border-radius:14px;padding:20px 32px;text-align:center;}}
.msg p{{font-size:24px;font-weight:700;color:#38bdf8;}}
</style></head><body>
<p class="num">1/10</p>
<div class="title">1回の「セーフ」は何も保証しない</div>
<div class="timeline">
  <div class="tl-item"><div class="tl-dot"></div><div class="tl-line"></div><div class="tl-year">去年</div><div class="tl-text">血糖値ギリギリ基準内 →<strong>「セーフ！」</strong></div></div>
  <div class="tl-item"><div class="tl-dot"></div><div class="tl-line"></div><div class="tl-year">3か月後</div><div class="tl-text">安心して<strong>夜食復活・運動サボり</strong></div></div>
  <div class="tl-item"><div class="tl-dot"></div><div class="tl-line"></div><div class="tl-year">翌年</div><div class="tl-text"><strong>E判定に逆戻り</strong>（前年より悪化）</div></div>
  <div class="tl-item"><div class="tl-dot"></div><div class="tl-year">教訓</div><div class="tl-text">数字の「点」ではなく<strong>「方向」</strong>を見る</div></div>
</div>
<div class="msg"><p>大事なのは「どっちに動いているか」</p></div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series" style="color:#38bdf8">#第44回 変化率管理</p>
</body></html>"""
    render(html, "x_post_01.png")


def card_02():
    """原因 → フロー図型"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.title{{position:absolute;left:56px;top:56px;font-size:34px;font-weight:900;color:#fff;}}
.flow{{position:absolute;top:130px;left:56px;right:56px;display:flex;align-items:center;justify-content:center;gap:16px;}}
.fbox{{background:#1e3a5f;border-radius:14px;padding:20px 24px;text-align:center;min-width:200px;}}
.fbox h4{{font-size:20px;font-weight:800;color:#38bdf8;margin-bottom:8px;}}
.fbox p{{font-size:17px;color:#9ca3af;line-height:1.5;}}
.fbox p strong{{color:#fff;}}
.arrow-r{{font-size:28px;color:#38bdf8;font-weight:900;}}
.study{{position:absolute;top:320px;left:56px;right:56px;background:#0d2035;border-radius:16px;padding:28px 36px;border-left:4px solid #38bdf8;}}
.study h3{{font-size:24px;font-weight:800;color:#fff;margin-bottom:10px;}}
.study p{{font-size:19px;color:#9ca3af;line-height:1.6;}}
.study p strong{{color:#38bdf8;}}
.badge{{position:absolute;bottom:80px;left:56px;background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.25);border-radius:8px;padding:8px 16px;font-size:15px;color:#38bdf8;}}
</style></head><body>
<p class="num">2/10</p>
<div class="title">なぜ「変化率」が将来リスクを決めるのか</div>
<div class="flow">
  <div class="fbox"><h4>同じ38歳</h4><p>暦年齢は<strong>同一</strong></p></div>
  <span class="arrow-r">→</span>
  <div class="fbox"><h4>老化速度：速い</h4><p>複数指標が<strong>悪化中</strong></p></div>
  <span class="arrow-r">→</span>
  <div class="fbox"><h4>10年後</h4><p>疾患リスク<strong>大幅上昇</strong></p></div>
</div>
<div class="study">
  <h3>Dunedin Study（Belsky et al., PNAS 2015）</h3>
  <p>1,000人以上を<strong>38年間追跡</strong>。生物学的年齢の変化速度が<br>将来の疾患リスク・死亡率と<strong>強く関連</strong>することを実証。</p>
</div>
<div class="badge">出典：Belsky DW. et al., PNAS, 2015</div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series" style="color:#38bdf8">#第44回 変化率管理</p>
</body></html>"""
    render(html, "x_post_02.png")


def card_03():
    """解決策 → 横3列ステップカード"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.title{{position:absolute;left:56px;top:56px;font-size:34px;font-weight:900;color:#fff;}}
.title span{{color:#FF6D00;}}
.cards{{display:flex;gap:28px;position:absolute;top:130px;left:56px;right:56px;bottom:100px;}}
.card{{flex:1;background:#1e3a5f;border-radius:16px;padding:28px 22px;border-top:4px solid;display:flex;flex-direction:column;}}
.card:nth-child(1){{border-color:#FF6D00;}}
.card:nth-child(2){{border-color:#38bdf8;}}
.card:nth-child(3){{border-color:#4ade80;}}
.card-num{{font-size:40px;font-weight:900;margin-bottom:10px;}}
.card:nth-child(1) .card-num{{color:#FF6D00;}}
.card:nth-child(2) .card-num{{color:#38bdf8;}}
.card:nth-child(3) .card-num{{color:#4ade80;}}
.card h3{{font-size:22px;font-weight:800;color:#fff;margin-bottom:14px;line-height:1.3;}}
.card p{{font-size:17px;color:#9ca3af;line-height:1.6;flex:1;}}
.card p strong{{color:#fff;}}
.arrow-h{{font-size:28px;color:#555;position:absolute;}}
.a1{{top:280px;left:410px;}}
.a2{{top:280px;left:835px;}}
.bottom{{position:absolute;bottom:28px;left:56px;right:56px;text-align:center;}}
.bottom p{{font-size:22px;font-weight:700;color:#FF6D00;}}
</style></head><body>
<p class="num">3/10</p>
<div class="title">老化対策の<span>最適解</span>は3つ</div>
<div class="cards">
  <div class="card"><div class="card-num">01</div><h3>派手な一発を<br>追わない</h3><p>サプリの一時的効果より<strong>生活の土台</strong>が先。一発逆転は研究が否定。</p></div>
  <div class="card"><div class="card-num">02</div><h3>小さい改善を<br>同時に積む</h3><p>「少しずつ×同時に」が<strong>最も再現性が高い</strong>戦略。</p></div>
  <div class="card"><div class="card-num">03</div><h3>週次で<br>傾きを確認</h3><p>「今週は先週より<strong>マシだったか</strong>」。この問いだけでOK。</p></div>
</div>
<span class="arrow-h a1">→</span>
<span class="arrow-h a2">→</span>
<div class="bottom"><p>「悪化の傾きを下げる設計」が最強の戦略</p></div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series" style="color:#FF6D00">#第44回 変化率管理</p>
</body></html>"""
    render(html, "x_post_03.png")


def card_04():
    """仕組み → 番号付きカード＋出典バッジ"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.title{{position:absolute;left:56px;top:56px;font-size:34px;font-weight:900;color:#fff;}}
.title span{{color:#38bdf8;}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;position:absolute;top:130px;left:56px;right:56px;}}
.item{{background:#1e3a5f;border-radius:14px;padding:24px;display:flex;align-items:flex-start;gap:16px;}}
.item-num{{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:900;flex-shrink:0;background:rgba(56,189,248,.15);color:#38bdf8;border:2px solid #38bdf8;}}
.item-text h4{{font-size:20px;font-weight:800;color:#fff;margin-bottom:6px;}}
.item-text p{{font-size:17px;color:#9ca3af;line-height:1.5;}}
.point{{position:absolute;bottom:80px;left:56px;right:56px;background:rgba(56,189,248,.06);border:1px solid rgba(56,189,248,.2);border-radius:14px;padding:18px 32px;text-align:center;}}
.point p{{font-size:22px;font-weight:700;color:#38bdf8;}}
</style></head><body>
<p class="num">4/10</p>
<div class="title"><span>4指標</span>だけ追えばいい</div>
<div class="grid">
  <div class="item"><div class="item-num">1</div><div class="item-text"><h4>体重</h4><p>週2〜3回・朝起きてすぐ</p></div></div>
  <div class="item"><div class="item-num">2</div><div class="item-text"><h4>腹囲</h4><p>週1回・へその高さで</p></div></div>
  <div class="item"><div class="item-num">3</div><div class="item-text"><h4>睡眠</h4><p>就寝・起床をざっくり記録</p></div></div>
  <div class="item"><div class="item-num">4</div><div class="item-text"><h4>活動量</h4><p>歩数 or 運動時間</p></div></div>
</div>
<div class="point"><p>毎日完璧に記録しない。週で傾きを見る。</p></div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series" style="color:#38bdf8">#第44回 変化率管理</p>
</body></html>"""
    render(html, "x_post_04.png")


def card_05():
    """効果 → Before/After比較"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.title{{position:absolute;left:56px;top:56px;font-size:34px;font-weight:900;color:#fff;}}
.title span{{color:#4ade80;}}
.panels{{display:flex;gap:32px;position:absolute;top:130px;left:56px;right:56px;bottom:90px;}}
.panel{{flex:1;border-radius:16px;padding:28px;}}
.panel-before{{background:rgba(239,68,68,.08);border:2px solid rgba(239,68,68,.3);}}
.panel-after{{background:rgba(74,222,128,.06);border:2px solid rgba(74,222,128,.3);}}
.panel-label{{font-size:22px;font-weight:900;margin-bottom:18px;}}
.label-b{{color:#ef4444;}}
.label-a{{color:#4ade80;}}
.stat{{margin-bottom:16px;}}
.stat-label{{font-size:16px;color:#9ca3af;margin-bottom:4px;}}
.stat-value{{font-size:32px;font-weight:900;}}
.val-b{{color:#ef4444;}}
.val-a{{color:#4ade80;}}
.stat-note{{font-size:15px;color:#666;margin-top:4px;}}
.msg{{position:absolute;bottom:28px;left:56px;right:56px;text-align:center;}}
.msg p{{font-size:20px;font-weight:700;color:#4ade80;}}
</style></head><body>
<p class="num">5/10</p>
<div class="title">体重が止まっても<span>腹囲は動いていた</span></div>
<div class="panels">
  <div class="panel panel-before">
    <div class="panel-label label-b">✗ 体重だけで判断</div>
    <div class="stat"><div class="stat-label">体重</div><div class="stat-value val-b">3か月横ばい</div><div class="stat-note">→「効果なし」で挫折</div></div>
    <div class="stat"><div class="stat-label">腹囲</div><div class="stat-value val-b">測っていない</div><div class="stat-note">→ 変化を見逃す</div></div>
    <div class="stat"><div class="stat-label">結果</div><div class="stat-value val-b">辞めていた</div></div>
  </div>
  <div class="panel panel-after">
    <div class="panel-label label-a">✓ 変化率で判断</div>
    <div class="stat"><div class="stat-label">体重</div><div class="stat-value val-a">3か月横ばい</div><div class="stat-note">→ 水分・食事の影響</div></div>
    <div class="stat"><div class="stat-label">腹囲</div><div class="stat-value val-a">95→91cm（-4cm）</div><div class="stat-note">→ 内臓脂肪は確実に減少</div></div>
    <div class="stat"><div class="stat-label">最終結果</div><div class="stat-value val-a">95→78cm</div></div>
  </div>
</div>
<div class="msg"><p>体重だけ見ていたら辞めていた。変化率で見るから続けられた。</p></div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series" style="color:#4ade80">#第44回 変化率管理</p>
</body></html>"""
    render(html, "x_post_05.png")


def card_06():
    """設計 → テーブル型"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.title{{position:absolute;left:56px;top:56px;font-size:34px;font-weight:900;color:#fff;}}
.title span{{color:#38bdf8;}}
.table-wrap{{position:absolute;top:130px;left:56px;right:56px;}}
table{{width:100%;border-collapse:separate;border-spacing:0 8px;}}
th{{font-size:18px;font-weight:700;padding:12px 20px;text-align:left;color:#9ca3af;}}
td{{padding:16px 20px;font-size:19px;color:#d1d5db;background:#0d2035;}}
tr td:first-child{{border-radius:10px 0 0 10px;font-weight:700;color:#fff;}}
tr td:last-child{{border-radius:0 10px 10px 0;}}
.check{{color:#4ade80;font-size:20px;}}
.cross{{color:#ef4444;font-size:20px;}}
.bottom{{position:absolute;bottom:80px;left:56px;right:56px;background:rgba(56,189,248,.06);border:1px solid rgba(56,189,248,.2);border-radius:12px;padding:16px;text-align:center;}}
.bottom p{{font-size:20px;font-weight:700;color:#38bdf8;}}
</style></head><body>
<p class="num">6/10</p>
<div class="title">体重停滞期の<span>チェックリスト</span></div>
<div class="table-wrap">
<table>
<tr><th>項目</th><th>改善あり？</th><th>判定</th></tr>
<tr><td>腹囲が少し減った</td><td>内臓脂肪は減っている</td><td><span class="check">✓ 継続</span></td></tr>
<tr><td>夜更かしが減った</td><td>食欲コントロール改善</td><td><span class="check">✓ 継続</span></td></tr>
<tr><td>歩く頻度が増えた</td><td>代謝の土台が動き始め</td><td><span class="check">✓ 継続</span></td></tr>
<tr><td>間食回数が減った</td><td>食行動の傾きが変化</td><td><span class="check">✓ 継続</span></td></tr>
<tr><td>全部横ばい or 悪化</td><td>戦略の見直しが必要</td><td><span class="cross">✗ 再設計</span></td></tr>
</table>
</div>
<div class="bottom"><p>体重だけで自分を否定すると、継続が切れる</p></div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series" style="color:#38bdf8">#第44回 変化率管理</p>
</body></html>"""
    render(html, "x_post_06.png")


def card_07():
    """実践 → 縦フロー型"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.title{{position:absolute;left:56px;top:56px;font-size:34px;font-weight:900;color:#fff;}}
.title span{{color:#FF6D00;}}
.steps{{position:absolute;top:130px;left:160px;right:160px;}}
.step{{display:flex;align-items:flex-start;margin-bottom:10px;}}
.step-badge{{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;flex-shrink:0;margin-right:22px;}}
.s1 .step-badge{{background:rgba(255,109,0,.15);color:#FF6D00;border:2px solid #FF6D00;}}
.s2 .step-badge{{background:rgba(56,189,248,.12);color:#38bdf8;border:2px solid #38bdf8;}}
.s3 .step-badge{{background:rgba(74,222,128,.12);color:#4ade80;border:2px solid #4ade80;}}
.step-card{{background:#1e3a5f;border-radius:14px;padding:18px 24px;flex:1;}}
.step-card h4{{font-size:22px;font-weight:800;color:#fff;margin-bottom:6px;}}
.step-card p{{font-size:17px;color:#9ca3af;line-height:1.4;}}
.step-card p strong{{color:#fff;}}
.conn{{margin:2px 0 2px 22px;font-size:24px;font-weight:900;color:#555;}}
.src{{position:absolute;bottom:80px;left:56px;background:rgba(255,109,0,.08);border:1px solid rgba(255,109,0,.2);border-radius:8px;padding:8px 16px;font-size:14px;color:#FF6D00;}}
</style></head><body>
<p class="num">7/10</p>
<div class="title">傾きを変える<span>3ステップ</span></div>
<div class="steps">
  <div class="step s1"><div class="step-badge">1</div><div class="step-card"><h4>固定ルール1つだけ作る</h4><p>「<strong>夕食後10分歩く</strong>」これだけ。食後歩行で血糖ピーク抑制。</p></div></div>
  <div class="conn">↓</div>
  <div class="step s2"><div class="step-badge">2</div><div class="step-card"><h4>カレンダーに先入れする</h4><p>「空いたらやる」→「<strong>先に予約して守る</strong>」。行動完遂率3倍。</p></div></div>
  <div class="conn">↓</div>
  <div class="step s3"><div class="step-badge">3</div><div class="step-card"><h4>週1レビューする</h4><p>守れた回数だけ見る。未達は責めない。<strong>8勝6敗で合格</strong>。</p></div></div>
</div>
<div class="src">Buffey et al., Sports Medicine 2022 / Gollwitzer 1999</div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series" style="color:#FF6D00">#第44回 変化率管理</p>
</body></html>"""
    render(html, "x_post_07.png")


def card_08():
    """復帰 → リカバリーフロー"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.title{{position:absolute;left:56px;top:56px;font-size:34px;font-weight:900;color:#fff;}}
.title span{{color:#4ade80;}}
.flow{{position:absolute;top:130px;left:120px;right:120px;}}
.fstep{{display:flex;align-items:center;margin-bottom:14px;}}
.fstep-icon{{width:56px;height:56px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900;margin-right:22px;flex-shrink:0;}}
.f1 .fstep-icon{{background:rgba(239,68,68,.15);color:#ef4444;border:2px solid #ef4444;}}
.f2 .fstep-icon{{background:rgba(255,109,0,.12);color:#FF6D00;border:2px solid #FF6D00;}}
.f3 .fstep-icon{{background:rgba(74,222,128,.12);color:#4ade80;border:2px solid #4ade80;}}
.fstep-card{{background:#1e3a5f;border-radius:14px;padding:20px 26px;flex:1;}}
.fstep-card h4{{font-size:22px;font-weight:800;color:#fff;margin-bottom:6px;}}
.fstep-card p{{font-size:17px;color:#9ca3af;}}
.fstep-card p strong{{color:#fff;}}
.fconn{{margin:2px 0 2px 24px;font-size:26px;font-weight:900;}}
.fc1{{color:#FF6D00;}}
.fc2{{color:#4ade80;}}
.badge{{position:absolute;bottom:70px;left:50%;transform:translateX(-50%);background:rgba(74,222,128,.08);border:2px solid rgba(74,222,128,.3);border-radius:16px;padding:18px 48px;text-align:center;}}
.badge p{{font-size:28px;font-weight:900;color:#4ade80;}}
.badge span{{font-size:16px;color:#9ca3af;display:block;margin-top:4px;}}
</style></head><body>
<p class="num">8/10</p>
<div class="title">崩れた日の<span>リセット手順</span></div>
<div class="flow">
  <div class="fstep f1"><div class="fstep-icon">!</div><div class="fstep-card"><h4>歩けなかった日</h4><p>「全部やり直し」は<strong>禁止</strong></p></div></div>
  <div class="fconn fc1">↓</div>
  <div class="fstep f2"><div class="fstep-icon">→</div><div class="fstep-card"><h4>カレンダーを翌日にスライド</h4><p>消さない。<strong>移すだけ</strong>。仕組みは生きている。</p></div></div>
  <div class="fconn fc2">↓</div>
  <div class="fstep f3"><div class="fstep-icon">✓</div><div class="fstep-card"><h4>翌日の食後に10分歩く</h4><p><strong>1回戻せば</strong>他も自然に戻る。</p></div></div>
</div>
<div class="badge"><p>8勝6敗でOK</p><span>崩れることより「戻れないこと」が本当の失敗</span></div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series" style="color:#4ade80">#第44回 変化率管理</p>
</body></html>"""
    render(html, "x_post_08.png")


def card_09():
    """深掘り → データ可視化型（CSSバー）"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.title{{position:absolute;left:56px;top:56px;font-size:34px;font-weight:900;color:#fff;}}
.title span{{color:#38bdf8;}}
.content{{position:absolute;top:130px;left:56px;right:56px;display:flex;gap:36px;}}
.chart-area{{flex:1;}}
.chart-title{{font-size:20px;font-weight:700;color:#9ca3af;margin-bottom:18px;}}
.bar-row{{display:flex;align-items:center;margin-bottom:14px;}}
.bar-label{{width:140px;font-size:17px;color:#d1d5db;font-weight:600;}}
.bar-track{{flex:1;height:28px;background:#0d2035;border-radius:8px;position:relative;overflow:hidden;}}
.bar-fill{{height:100%;border-radius:8px;display:flex;align-items:center;justify-content:flex-end;padding-right:10px;font-size:14px;font-weight:700;}}
.bar-slow{{background:linear-gradient(90deg,#4ade80,#22c55e);color:#fff;width:40%;}}
.bar-avg{{background:linear-gradient(90deg,#FF6D00,#f59e0b);color:#fff;width:65%;}}
.bar-fast{{background:linear-gradient(90deg,#ef4444,#dc2626);color:#fff;width:90%;}}
.explain{{flex:1;}}
.explain-card{{background:#1e3a5f;border-radius:14px;padding:24px;margin-bottom:16px;border-left:4px solid #38bdf8;}}
.explain-card h4{{font-size:20px;font-weight:800;color:#fff;margin-bottom:8px;}}
.explain-card p{{font-size:17px;color:#9ca3af;line-height:1.6;}}
.explain-card p strong{{color:#38bdf8;}}
.src{{position:absolute;bottom:80px;left:56px;background:rgba(56,189,248,.08);border:1px solid rgba(56,189,248,.2);border-radius:8px;padding:8px 16px;font-size:14px;color:#38bdf8;}}
</style></head><body>
<p class="num">9/10</p>
<div class="title">Dunedin Studyの<span>教訓</span></div>
<div class="content">
  <div class="chart-area">
    <div class="chart-title">10年後の疾患リスク（イメージ）</div>
    <div class="bar-row"><div class="bar-label">老化速度：遅い</div><div class="bar-track"><div class="bar-fill bar-slow">低</div></div></div>
    <div class="bar-row"><div class="bar-label">老化速度：普通</div><div class="bar-track"><div class="bar-fill bar-avg">中</div></div></div>
    <div class="bar-row"><div class="bar-label">老化速度：速い</div><div class="bar-track"><div class="bar-fill bar-fast">高</div></div></div>
    <div style="margin-top:24px;">
      <div class="bar-row"><div class="bar-label" style="color:#ef4444;">速い人の特徴</div></div>
      <div style="font-size:17px;color:#9ca3af;line-height:1.7;padding-left:4px;">
        ・体重横ばいでも腹囲↑<br>
        ・睡眠時間が少しずつ↓<br>
        ・歩数が毎月↓<br>
        ・血糖指標が年単位で↑
      </div>
    </div>
  </div>
  <div class="explain">
    <div class="explain-card">
      <h4>速い人の本質</h4>
      <p>1つの数値が悪いのではなく<strong>複数指標が同時にゆるく悪化</strong>している</p>
    </div>
    <div class="explain-card">
      <h4>逆転の戦略</h4>
      <p>複数の指標を<strong>少しずつ同時に改善</strong>する。これが最も再現性が高い。</p>
    </div>
  </div>
</div>
<div class="src">Belsky DW. et al., PNAS, 2015</div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series" style="color:#38bdf8">#第44回 変化率管理</p>
</body></html>"""
    render(html, "x_post_09.png")


def card_10():
    """CTA → チェックリスト＋CTAボックス"""
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE_CSS}
.title{{position:absolute;left:56px;top:56px;font-size:36px;font-weight:900;color:#fff;}}
.title span{{color:#FF6D00;}}
.checklist{{position:absolute;top:140px;left:100px;right:100px;}}
.check-item{{display:flex;align-items:center;margin-bottom:18px;}}
.check-box{{width:36px;height:36px;border-radius:8px;border:3px solid #FF6D00;display:flex;align-items:center;justify-content:center;font-size:20px;color:#FF6D00;margin-right:18px;flex-shrink:0;}}
.check-text{{font-size:22px;color:#d1d5db;line-height:1.4;}}
.check-text strong{{color:#fff;}}
.cta-box{{position:absolute;bottom:80px;left:100px;right:100px;background:linear-gradient(135deg,rgba(255,109,0,.12),rgba(255,109,0,.04));border:2px solid #FF6D00;border-radius:20px;padding:28px 36px;text-align:center;}}
.cta-box h3{{font-size:28px;font-weight:900;color:#FF6D00;margin-bottom:10px;}}
.cta-box p{{font-size:20px;color:#d1d5db;}}
.cta-box a{{color:#FF6D00;text-decoration:none;font-weight:700;}}
</style></head><body>
<p class="num">10/10</p>
<div class="title">今日やること<span>1つだけ</span></div>
<div class="checklist">
  <div class="check-item"><div class="check-box">1</div><div class="check-text"><strong>食後10分歩行</strong>をカレンダーに登録する</div></div>
  <div class="check-item"><div class="check-box">2</div><div class="check-text"><strong>腹囲</strong>をへその高さで測って記録する</div></div>
  <div class="check-item"><div class="check-box">3</div><div class="check-text">今週の<strong>体重を2回測って平均</strong>を出す</div></div>
</div>
<div class="cta-box">
  <h3>全部やらなくていい。今日は1つだけ。</h3>
  <p>noteで詳細 → note.com/mash_anti_metabo</p>
</div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series" style="color:#FF6D00">#第44回 変化率管理</p>
</body></html>"""
    render(html, "x_post_10.png")


CARD_FUNCS = [card_01, card_02, card_03, card_04, card_05,
              card_06, card_07, card_08, card_09, card_10]


def save_tweets():
    out = OUTPUT_DIR / "x_posts.md"
    lines = ["# 第44回 X投稿スレッド（10本）\n\n"]
    for i, tweet in enumerate(TWEETS):
        tag = CARD_TAGS[i]
        lines.append(
            f"## 投稿{i+1}/10｜{tag}\n\n```\n{tweet.strip()}\n```\n\n"
            f"![カード{i+1}](x_post_{str(i+1).zfill(2)}.png)\n\n---\n\n"
        )
    out.write_text("".join(lines), encoding="utf-8")
    print("OK: x_posts.md")


if __name__ == "__main__":
    print("第44回 Xカード10枚 生成開始...\n")
    for i, func in enumerate(CARD_FUNCS):
        print(f"  カード {i+1}/10 生成中...")
        func()
    save_tweets()
    print(f"\n全10枚＋ツイートmd完了。保存先: {OUTPUT_DIR}")
