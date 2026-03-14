#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第8回 X投稿用インフォグラフィックカード 10枚生成スクリプト
HTML/CSS + Playwright（Chromiumヘッドレス）版
サイズ: 1280×720px
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

# ============================================================
# X投稿テキスト（10本）
# ============================================================
TWEETS = [
    {
        "idx": 1,
        "tag": "共感",
        "tweet": (
            "「今日こそやる」と思いながら、\n"
            "メニューを考えているうちに1時間が過ぎてソファに倒れ込む。\n\n"
            "100kgだった頃の自分がまさにそうでした。\n\n"
            "これ、意志の弱さじゃないです。\n設計のミスです。\n\n"
            "↓続きを読む（2/10）"
        ),
    },
    {
        "idx": 2,
        "tag": "原因",
        "tweet": (
            "「今日は何をやるか」を毎回考えなければいけない。\n\n"
            "これが運動を止める最大の原因。\n\n"
            "スタンフォード大の心理学者が示した「選択のパラドックス」。\n"
            "選択肢が増えるほど、人は決断できなくなる。\n\n"
            "運動も同じ。\n\n"
            "↓解決策（3/10）"
        ),
    },
    {
        "idx": 3,
        "tag": "解決策",
        "tweet": (
            "解決策はシンプル。\n\n"
            "「迷ったらバーピー」と決めるだけ。\n\n"
            "種目を1つに絞ると、始める前の決断コストがゼロになる。\n"
            "ジム不要・器具不要・自宅の小スペースで完結。\n\n"
            "週3回・8分から始める。\n\n"
            "↓なぜバーピーか（4/10）"
        ),
    },
    {
        "idx": 4,
        "tag": "仕組み",
        "tweet": (
            "バーピー1種目の中に\n"
            "・スクワット（下半身）\n"
            "・腕立て（上半身）\n"
            "・プランク（体幹）\n"
            "・ジャンプ（心肺）\n\n"
            "が入っている。\n\n"
            "4種目分の刺激が1種目で取れる。\n\n"
            "↓見た目が変わる理由（5/10）"
        ),
    },
    {
        "idx": 5,
        "tag": "効果",
        "tweet": (
            "見た目を変えるには2種類の刺激が必要。\n\n"
            "①大きな筋肉への刺激（脚・お尻・胸）\n"
            "②心拍を上げる代謝刺激（EPOC）\n\n"
            "バーピーはこの2つを同時に取れる数少ない種目。\n\n"
            "私が68kgを8年間キープできているのも\nこの組み合わせが土台にある。\n\n"
            "↓段階化の設計（6/10）"
        ),
    },
    {
        "idx": 6,
        "tag": "設計",
        "tweet": (
            "バーピーはきつい。\nだから最初から標準形を目指さない。\n\n"
            "レベル1：ノージャンプ・ノープッシュアップ\n"
            "レベル2：ノージャンプ・プッシュアップあり\n"
            "レベル3：ジャンプあり（標準形）\n\n"
            "同じ種目のまま成長できる。\n「種目を迷う」必要がない。\n\n"
            "↓具体的なプロトコル（7/10）"
        ),
    },
    {
        "idx": 7,
        "tag": "実践",
        "tweet": (
            "具体的にはこれだけ。\n\n"
            "【フェーズ1（1〜2週目）】\n"
            "20秒バーピー → 40秒休憩 × 8セット = 8分\n\n"
            "【フェーズ2（3〜6週目）】\n"
            "30秒バーピー → 30秒休憩 × 10セット\n\n"
            "毎日やらなくていい。週3回で十分。\n\n"
            "↓崩れた日の戻り方（8/10）"
        ),
    },
    {
        "idx": 8,
        "tag": "復帰",
        "tweet": (
            "忙しくて動けなかった日の対処法は1つ。\n\n"
            "負荷を落とすだけ。\nレベルを1つ下げる。\n"
            "それでもきつければ5分歩くだけでいい。\n\n"
            "「やらなかった」と「ゼロにした」は違う。\n\n"
            "8勝6敗で十分。続いているなら勝ち。\n\n"
            "↓睡眠との連動（9/10）"
        ),
    },
    {
        "idx": 9,
        "tag": "睡眠×運動",
        "tweet": (
            "見落とされがちなポイント。\n\n"
            "バーピーの質を決める意外な要素がある。\n前日の睡眠。\n\n"
            "寝不足でやるとフォームが崩れやすく、\n回復も遅れる。\n\n"
            "攻める日の価値は、前日の夜が決める。\n"
            "HIITと睡眠はセットで考える。\n\n"
            "↓今夜やること（10/10）"
        ),
    },
    {
        "idx": 10,
        "tag": "今夜やること",
        "tweet": (
            "まず今夜だけ試してみてください。\n\n"
            "20秒バーピー → 40秒休憩 × 4セット\n（ノージャンプOK）\n\n"
            "終わったら一言だけメモ。\n「今日は、やった。」\n\n"
            "その4セットが、見た目を変える最初の1歩です。\n\n"
            "詳細はnoteで👇\nhttps://note.com/mash_anti_metabo"
        ),
    },
]


# ============================================================
# 共通ベーステンプレート（__BODY__を各カードで置換）
# ============================================================
def base_html(body_content: str, accent: str, tag: str, idx: int) -> str:
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@font-face {
  font-family:'NotoSansJP';
  src:url('""" + FONT + """');
  font-weight:100 900;
}
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}
body{
  width:1280px;height:720px;overflow:hidden;
  background:#0a0a0a;position:relative;
  font-family:'NotoSansJP','Meiryo',sans-serif;
}
.tag{
  position:absolute;left:56px;top:44px;
  background:""" + accent + """;color:#000;
  font-size:24px;font-weight:800;
  padding:5px 20px;border-radius:20px;
  letter-spacing:1px;
}
.num{
  position:absolute;top:50px;right:56px;
  font-size:24px;font-weight:700;
  color:#333;letter-spacing:1px;
}
.author{
  position:absolute;bottom:22px;left:56px;
  font-size:18px;font-weight:400;color:#3a3a3a;
}
.series{
  position:absolute;bottom:22px;right:56px;
  font-size:18px;font-weight:700;color:""" + accent + """;
}
</style></head><body>
<div class="tag">""" + tag + """</div>
<div class="num">""" + str(idx) + """/10</div>
""" + body_content + """
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series">#第8回 バーピー</p>
</body></html>"""


# ============================================================
# カード1：悪循環フローチャート（共感）
# ============================================================
def card1() -> str:
    body = """
<style>
.flow-wrap{position:absolute;left:56px;top:100px;right:56px;bottom:60px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;}
.flow-title{font-size:38px;font-weight:900;color:#fff;margin-bottom:28px;letter-spacing:-1px;}
.flow-step{width:560px;background:#161616;border:2px solid #38bdf8;border-radius:16px;padding:16px 28px;text-align:center;}
.flow-step-label{font-size:14px;font-weight:700;color:#38bdf8;letter-spacing:2px;margin-bottom:4px;}
.flow-step-text{font-size:28px;font-weight:900;color:#fff;letter-spacing:-0.5px;}
.flow-arrow{font-size:28px;color:#38bdf8;line-height:1;padding:4px 0;}
.flow-end{width:560px;background:#1a0a0a;border:2px solid #FF6D00;border-radius:16px;padding:16px 28px;text-align:center;}
.flow-end-label{font-size:14px;font-weight:700;color:#FF6D00;letter-spacing:2px;margin-bottom:4px;}
.flow-end-text{font-size:28px;font-weight:900;color:#FF6D00;}
.flow-badge{position:absolute;right:56px;top:100px;text-align:right;}
.flow-badge-line1{font-size:22px;font-weight:400;color:#555;}
.flow-badge-line2{font-size:48px;font-weight:900;color:#fff;letter-spacing:-1px;line-height:1.1;}
.flow-badge-line3{font-size:22px;font-weight:400;color:#555;margin-top:4px;}
</style>
<div class="flow-wrap">
  <div class="flow-title">あなたの"続かない"悪循環</div>
  <div class="flow-step">
    <div class="flow-step-label">STEP 1</div>
    <div class="flow-step-text">「今日こそやるぞ」</div>
  </div>
  <div class="flow-arrow">↓</div>
  <div class="flow-step">
    <div class="flow-step-label">STEP 2</div>
    <div class="flow-step-text">メニューを考え始める…</div>
  </div>
  <div class="flow-arrow">↓</div>
  <div class="flow-step">
    <div class="flow-step-label">STEP 3</div>
    <div class="flow-step-text">1時間が経過する</div>
  </div>
  <div class="flow-arrow">↓</div>
  <div class="flow-end">
    <div class="flow-end-label">結果</div>
    <div class="flow-end-text">「もう今日はいいや」</div>
  </div>
</div>
<div class="flow-badge">
  <div class="flow-badge-line1">これは</div>
  <div class="flow-badge-line2">意志の問題<br>じゃない</div>
  <div class="flow-badge-line3">設計のミスだ</div>
</div>
"""
    return base_html(body, "#38bdf8", "共感", 1)


# ============================================================
# カード2：選択肢比較（原因）
# ============================================================
def card2() -> str:
    body = """
<style>
.cmp-wrap{position:absolute;left:56px;top:100px;right:56px;bottom:60px;display:flex;align-items:stretch;gap:24px;}
.cmp-col{flex:1;display:flex;flex-direction:column;gap:16px;}
.cmp-head{border-radius:14px;padding:14px 20px;text-align:center;}
.cmp-head-ng{background:#200808;border:2px solid #ff4444;}
.cmp-head-ok{background:#082008;border:2px solid #4ade80;}
.cmp-head-icon{font-size:36px;line-height:1;}
.cmp-head-label{font-size:26px;font-weight:900;margin-top:6px;}
.cmp-head-ng .cmp-head-label{color:#ff4444;}
.cmp-head-ok .cmp-head-label{color:#4ade80;}
.cmp-head-sub{font-size:15px;color:#555;margin-top:4px;}
.cmp-item{background:#161616;border-radius:12px;padding:12px 18px;display:flex;align-items:center;gap:12px;}
.cmp-dot-ng{width:10px;height:10px;border-radius:50%;background:#ff4444;flex-shrink:0;}
.cmp-dot-ok{width:10px;height:10px;border-radius:50%;background:#4ade80;flex-shrink:0;}
.cmp-item-text{font-size:20px;font-weight:700;color:#ccc;}
.cmp-result{position:absolute;bottom:68px;left:56px;right:56px;text-align:center;}
.cmp-result-text{font-size:26px;font-weight:900;color:#38bdf8;letter-spacing:-0.5px;}
.cmp-title{position:absolute;left:56px;right:56px;top:106px;text-align:center;font-size:32px;font-weight:900;color:#fff;margin-bottom:16px;}
</style>
<div class="cmp-title">選択肢の数が行動を止める</div>
<div class="cmp-wrap" style="top:158px;">
  <div class="cmp-col">
    <div class="cmp-head cmp-head-ng">
      <div class="cmp-head-icon">✗</div>
      <div class="cmp-head-label">多い選択肢</div>
      <div class="cmp-head-sub">スタンフォード大の研究</div>
    </div>
    <div class="cmp-item"><div class="cmp-dot-ng"></div><div class="cmp-item-text">今日の種目を選ぶ</div></div>
    <div class="cmp-item"><div class="cmp-dot-ng"></div><div class="cmp-item-text">器具を選ぶ</div></div>
    <div class="cmp-item"><div class="cmp-dot-ng"></div><div class="cmp-item-text">次の種目を考える</div></div>
    <div class="cmp-item"><div class="cmp-dot-ng"></div><div class="cmp-item-text">→ 決断疲れ → 停止</div></div>
  </div>
  <div class="cmp-col">
    <div class="cmp-head cmp-head-ok">
      <div class="cmp-head-icon">✓</div>
      <div class="cmp-head-label">1種目に絞る</div>
      <div class="cmp-head-sub">バーピーだけ</div>
    </div>
    <div class="cmp-item"><div class="cmp-dot-ok"></div><div class="cmp-item-text">決断コスト ゼロ</div></div>
    <div class="cmp-item"><div class="cmp-dot-ok"></div><div class="cmp-item-text">器具不要</div></div>
    <div class="cmp-item"><div class="cmp-dot-ok"></div><div class="cmp-item-text">次の種目なし</div></div>
    <div class="cmp-item"><div class="cmp-dot-ok"></div><div class="cmp-item-text">→ すぐ動ける</div></div>
  </div>
</div>
"""
    return base_html(body, "#38bdf8", "原因", 2)


# ============================================================
# カード3：解決策3カード（解決策）
# ============================================================
def card3() -> str:
    body = """
<style>
.sol-title{position:absolute;left:56px;top:102px;right:56px;font-size:52px;font-weight:900;color:#FF6D00;letter-spacing:-2px;text-shadow:0 0 40px rgba(255,109,0,.5);}
.sol-sub{position:absolute;left:56px;top:172px;font-size:26px;font-weight:400;color:#666;}
.sol-cards{position:absolute;left:56px;top:236px;right:56px;display:flex;gap:20px;}
.sol-card{flex:1;background:#111;border-radius:18px;padding:28px 20px;text-align:center;border:1px solid #222;}
.sol-card-icon{font-size:44px;line-height:1;margin-bottom:14px;}
.sol-card-title{font-size:24px;font-weight:900;color:#FF6D00;margin-bottom:10px;letter-spacing:-0.5px;}
.sol-card-body{font-size:18px;font-weight:400;color:#888;line-height:1.6;}
.sol-card-val{font-size:36px;font-weight:900;color:#fff;margin-bottom:6px;letter-spacing:-1px;}
.sol-bottom{position:absolute;left:56px;bottom:60px;right:56px;text-align:center;font-size:22px;font-weight:700;color:#555;}
</style>
<div class="sol-title">迷ったらバーピー。</div>
<div class="sol-sub">決断コストをゼロにする唯一の方法</div>
<div class="sol-cards">
  <div class="sol-card">
    <div class="sol-card-icon">🏠</div>
    <div class="sol-card-title">自宅完結</div>
    <div class="sol-card-body">ジム不要<br>器具不要<br>小スペースで可</div>
  </div>
  <div class="sol-card">
    <div class="sol-card-icon">⏱</div>
    <div class="sol-card-title">週3回・8分</div>
    <div class="sol-card-val">8<span style="font-size:20px">分</span></div>
    <div class="sol-card-body">フェーズ1の<br>総運動時間</div>
  </div>
  <div class="sol-card">
    <div class="sol-card-icon">🧠</div>
    <div class="sol-card-title">決断コスト</div>
    <div class="sol-card-val" style="color:#FF6D00;">ゼロ</div>
    <div class="sol-card-body">「何をやるか」<br>を考えない</div>
  </div>
</div>
"""
    return base_html(body, "#FF6D00", "解決策", 3)


# ============================================================
# カード4：バーピー4フェーズ分解（仕組み）
# ============================================================
def card4() -> str:
    body = """
<style>
.mech-title{position:absolute;left:56px;top:102px;font-size:36px;font-weight:900;color:#fff;letter-spacing:-1px;}
.mech-sub{position:absolute;left:56px;top:150px;font-size:22px;color:#555;}
.mech-grid{position:absolute;left:56px;top:196px;right:56px;bottom:62px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:16px;}
.mech-cell{background:#111;border-radius:16px;padding:20px 24px;display:flex;align-items:center;gap:18px;border:1px solid #222;}
.mech-icon{font-size:44px;line-height:1;flex-shrink:0;}
.mech-info{}
.mech-part{font-size:15px;font-weight:700;color:#38bdf8;letter-spacing:1px;margin-bottom:4px;}
.mech-name{font-size:26px;font-weight:900;color:#fff;letter-spacing:-0.5px;}
.mech-muscle{font-size:16px;color:#555;margin-top:4px;}
.mech-badge{position:absolute;right:56px;top:102px;background:#0d1f2d;border:2px solid #38bdf8;border-radius:16px;padding:10px 20px;text-align:center;}
.mech-badge-num{font-size:52px;font-weight:900;color:#38bdf8;line-height:1;}
.mech-badge-label{font-size:15px;color:#38bdf8;letter-spacing:1px;}
</style>
<div class="mech-title">1種目で4種目分の刺激</div>
<div class="mech-sub">バーピー1動作の中に入っているもの</div>
<div class="mech-badge">
  <div class="mech-badge-num">×4</div>
  <div class="mech-badge-label">の刺激</div>
</div>
<div class="mech-grid">
  <div class="mech-cell">
    <div class="mech-icon">🦵</div>
    <div class="mech-info">
      <div class="mech-part">PHASE 1</div>
      <div class="mech-name">スクワット</div>
      <div class="mech-muscle">大腿四頭筋・臀筋・ハム</div>
    </div>
  </div>
  <div class="mech-cell">
    <div class="mech-icon">💪</div>
    <div class="mech-info">
      <div class="mech-part">PHASE 2</div>
      <div class="mech-name">腕立て</div>
      <div class="mech-muscle">胸・肩・上腕三頭筋</div>
    </div>
  </div>
  <div class="mech-cell">
    <div class="mech-icon">🏋</div>
    <div class="mech-info">
      <div class="mech-part">PHASE 3</div>
      <div class="mech-name">体幹プランク</div>
      <div class="mech-muscle">腹筋・脊柱起立筋</div>
    </div>
  </div>
  <div class="mech-cell">
    <div class="mech-icon">❤️</div>
    <div class="mech-info">
      <div class="mech-part">PHASE 4</div>
      <div class="mech-name">ジャンプ有酸素</div>
      <div class="mech-muscle">心肺機能・代謝向上</div>
    </div>
  </div>
</div>
"""
    return base_html(body, "#38bdf8", "仕組み", 4)


# ============================================================
# カード5：2本の柱→見た目変化（効果）
# ============================================================
def card5() -> str:
    body = """
<style>
.eff-title{position:absolute;left:56px;top:102px;font-size:38px;font-weight:900;color:#fff;letter-spacing:-1px;}
.eff-sub{position:absolute;left:56px;top:152px;font-size:20px;color:#555;}
.eff-cols{position:absolute;left:56px;top:200px;right:56px;height:340px;display:flex;gap:20px;}
.eff-col{flex:1;background:#0d1a0d;border:2px solid #4ade80;border-radius:18px;padding:24px 20px;}
.eff-col-icon{font-size:36px;line-height:1;margin-bottom:10px;}
.eff-col-title{font-size:24px;font-weight:900;color:#4ade80;margin-bottom:12px;letter-spacing:-0.5px;}
.eff-col-body{font-size:17px;color:#888;line-height:1.7;}
.eff-col-tag{display:inline-block;background:#4ade8022;border:1px solid #4ade80;border-radius:8px;padding:3px 10px;font-size:13px;font-weight:700;color:#4ade80;margin-top:10px;}
.eff-result{position:absolute;left:56px;bottom:65px;right:56px;display:flex;align-items:center;justify-content:center;gap:20px;}
.eff-arrow{font-size:32px;color:#4ade80;}
.eff-result-box{background:#0f2a0f;border:2px solid #4ade80;border-radius:16px;padding:14px 32px;text-align:center;}
.eff-result-text{font-size:28px;font-weight:900;color:#4ade80;letter-spacing:-0.5px;}
.eff-result-sub{font-size:14px;color:#555;margin-top:4px;}
.eff-keep{font-size:18px;color:#555;text-align:center;}
.eff-keep-num{font-size:38px;font-weight:900;color:#fff;letter-spacing:-1px;}
</style>
<div class="eff-title">見た目を変える2つの刺激</div>
<div class="eff-sub">バーピーはこの2つを同時に取れる数少ない種目</div>
<div class="eff-cols">
  <div class="eff-col">
    <div class="eff-col-icon">🦴</div>
    <div class="eff-col-title">① 筋刺激</div>
    <div class="eff-col-body">脚・お尻・胸の大きな筋肉へアプローチ。体脂肪を落としながら筋肉がしぼまないための刺激。</div>
    <div class="eff-col-tag">大筋群を使う</div>
  </div>
  <div class="eff-col">
    <div class="eff-col-icon">🔥</div>
    <div class="eff-col-title">② 代謝刺激</div>
    <div class="eff-col-body">心拍を上げることで、運動後も代謝が高い状態が続く（EPOC効果）。アフターバーンが起きる。</div>
    <div class="eff-col-tag">EPOC効果</div>
  </div>
</div>
<div class="eff-result">
  <div style="text-align:center;">
    <div class="eff-keep">68kgを</div>
    <div class="eff-keep-num">8年間</div>
    <div class="eff-keep">キープ中</div>
  </div>
  <div class="eff-arrow">←</div>
  <div class="eff-result-box">
    <div class="eff-result-text">この組み合わせが土台</div>
    <div class="eff-result-sub">100kg → 68kg (-32kg) 達成</div>
  </div>
</div>
"""
    return base_html(body, "#4ade80", "効果", 5)


# ============================================================
# カード6：レベル5段階バー（設計）
# ============================================================
def card6() -> str:
    body = """
<style>
.lv-title{position:absolute;left:56px;top:102px;font-size:38px;font-weight:900;color:#fff;letter-spacing:-1px;}
.lv-sub{position:absolute;left:56px;top:152px;font-size:20px;color:#555;}
.lv-list{position:absolute;left:56px;top:200px;right:56px;display:flex;flex-direction:column;gap:14px;}
.lv-row{display:flex;align-items:center;gap:16px;}
.lv-badge{width:100px;flex-shrink:0;text-align:center;}
.lv-badge-num{font-size:14px;font-weight:700;letter-spacing:1px;}
.lv-badge-circle{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:900;margin:0 auto 4px;}
.lv-bar-wrap{flex:1;background:#1a1a1a;border-radius:8px;height:44px;position:relative;overflow:hidden;}
.lv-bar{height:100%;border-radius:8px;display:flex;align-items:center;padding-left:16px;transition:width .3s;}
.lv-bar-text{font-size:16px;font-weight:700;color:#000;white-space:nowrap;}
.lv-desc{width:240px;flex-shrink:0;font-size:14px;color:#555;line-height:1.4;}
</style>
<div class="lv-title">最初から標準形を目指さない</div>
<div class="lv-sub">同じ種目のまま段階的に成長できる</div>
<div class="lv-list">
  <div class="lv-row">
    <div class="lv-badge"><div class="lv-badge-circle" style="background:#38bdf8;color:#000;">1</div><div class="lv-badge-num" style="color:#38bdf8;">LEVEL</div></div>
    <div class="lv-bar-wrap"><div class="lv-bar" style="width:20%;background:#38bdf8;"><span class="lv-bar-text">20%</span></div></div>
    <div class="lv-desc">ノージャンプ・ノープッシュアップ<br><span style="color:#38bdf8;">→ 運動ゼロから始める人</span></div>
  </div>
  <div class="lv-row">
    <div class="lv-badge"><div class="lv-badge-circle" style="background:#60c8f0;color:#000;">2</div><div class="lv-badge-num" style="color:#60c8f0;">LEVEL</div></div>
    <div class="lv-bar-wrap"><div class="lv-bar" style="width:40%;background:#60c8f0;"><span class="lv-bar-text">40%</span></div></div>
    <div class="lv-desc">ノージャンプ・プッシュアップあり<br><span style="color:#60c8f0;">→ 少し慣れてきた人</span></div>
  </div>
  <div class="lv-row">
    <div class="lv-badge"><div class="lv-badge-circle" style="background:#FF6D00;color:#000;">3</div><div class="lv-badge-num" style="color:#FF6D00;">LEVEL</div></div>
    <div class="lv-bar-wrap"><div class="lv-bar" style="width:60%;background:#FF6D00;"><span class="lv-bar-text">60%</span></div></div>
    <div class="lv-desc">ジャンプあり（標準形）<br><span style="color:#FF6D00;">→ 2〜3週間続いた人</span></div>
  </div>
  <div class="lv-row">
    <div class="lv-badge"><div class="lv-badge-circle" style="background:#ff8c30;color:#000;">4</div><div class="lv-badge-num" style="color:#ff8c30;">LEVEL</div></div>
    <div class="lv-bar-wrap"><div class="lv-bar" style="width:80%;background:#ff8c30;"><span class="lv-bar-text">80%</span></div></div>
    <div class="lv-desc">テンポ・回数アップ<br><span style="color:#ff8c30;">→ 標準形に慣れた人</span></div>
  </div>
  <div class="lv-row">
    <div class="lv-badge"><div class="lv-badge-circle" style="background:#ffaa50;color:#000;">5</div><div class="lv-badge-num" style="color:#ffaa50;">LEVEL</div></div>
    <div class="lv-bar-wrap"><div class="lv-bar" style="width:100%;background:#ffaa50;"><span class="lv-bar-text">100%</span></div></div>
    <div class="lv-desc">休憩を短くする<br><span style="color:#ffaa50;">→ さらに負荷を上げたい人</span></div>
  </div>
</div>
"""
    return base_html(body, "#38bdf8", "設計", 6)


# ============================================================
# カード7：タイマーグリッド（実践）
# ============================================================
def card7() -> str:
    body = """
<style>
.prot-title{position:absolute;left:56px;top:102px;font-size:36px;font-weight:900;color:#fff;letter-spacing:-1px;}
.prot-wrap{position:absolute;left:56px;top:158px;right:56px;bottom:62px;display:flex;gap:28px;}
.prot-phase{flex:1;display:flex;flex-direction:column;gap:10px;}
.prot-phase-head{background:#1a0e00;border:2px solid #FF6D00;border-radius:12px;padding:10px 16px;display:flex;justify-content:space-between;align-items:center;}
.prot-phase-name{font-size:16px;font-weight:700;color:#FF6D00;letter-spacing:1px;}
.prot-phase-total{font-size:22px;font-weight:900;color:#fff;}
.prot-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;flex:1;}
.prot-on{background:#FF6D00;border-radius:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:6px;}
.prot-off{background:#1a1a1a;border:1px solid #333;border-radius:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:6px;}
.prot-sec{font-size:20px;font-weight:900;color:#000;line-height:1;}
.prot-sec-off{font-size:20px;font-weight:900;color:#555;line-height:1;}
.prot-label{font-size:10px;font-weight:700;color:#000;letter-spacing:0.5px;margin-top:2px;}
.prot-label-off{font-size:10px;font-weight:700;color:#333;letter-spacing:0.5px;margin-top:2px;}
.prot-sets{background:#111;border-radius:10px;padding:8px;text-align:center;}
.prot-sets-num{font-size:28px;font-weight:900;color:#FF6D00;}
.prot-sets-label{font-size:12px;color:#555;}
</style>
<div class="prot-title">週3回・このセット数だけやる</div>
<div class="prot-wrap">
  <div class="prot-phase">
    <div class="prot-phase-head">
      <span class="prot-phase-name">PHASE 1｜1〜2週目</span>
      <span class="prot-phase-total">= 8分</span>
    </div>
    <div class="prot-grid">
      <div class="prot-on"><div class="prot-sec">20</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">40</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on"><div class="prot-sec">20</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">40</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on"><div class="prot-sec">20</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">40</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on"><div class="prot-sec">20</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">40</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on"><div class="prot-sec">20</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">40</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on"><div class="prot-sec">20</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">40</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on"><div class="prot-sec">20</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">40</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on"><div class="prot-sec">20</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">40</div><div class="prot-label-off">秒 OFF</div></div>
    </div>
    <div class="prot-sets"><div class="prot-sets-num">8セット</div><div class="prot-sets-label">× 週3回</div></div>
  </div>
  <div class="prot-phase">
    <div class="prot-phase-head">
      <span class="prot-phase-name">PHASE 2｜3〜6週目</span>
      <span class="prot-phase-total">= 10分</span>
    </div>
    <div class="prot-grid">
      <div class="prot-on" style="background:#ff8c30;"><div class="prot-sec">30</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">30</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on" style="background:#ff8c30;"><div class="prot-sec">30</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">30</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on" style="background:#ff8c30;"><div class="prot-sec">30</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">30</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on" style="background:#ff8c30;"><div class="prot-sec">30</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">30</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on" style="background:#ff8c30;"><div class="prot-sec">30</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">30</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on" style="background:#ff8c30;"><div class="prot-sec">30</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">30</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on" style="background:#ff8c30;"><div class="prot-sec">30</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">30</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on" style="background:#ff8c30;"><div class="prot-sec">30</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">30</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on" style="background:#ff8c30;"><div class="prot-sec">30</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">30</div><div class="prot-label-off">秒 OFF</div></div>
      <div class="prot-on" style="background:#ff8c30;"><div class="prot-sec">30</div><div class="prot-label">秒 ON</div></div>
      <div class="prot-off"><div class="prot-sec-off">30</div><div class="prot-label-off">秒 OFF</div></div>
    </div>
    <div class="prot-sets"><div class="prot-sets-num" style="color:#ff8c30;">10セット</div><div class="prot-sets-label">× 週3回</div></div>
  </div>
</div>
"""
    return base_html(body, "#FF6D00", "実践", 7)


# ============================================================
# カード8：崩れた日のフロー（復帰）
# ============================================================
def card8() -> str:
    body = """
<style>
.rec-title{position:absolute;left:56px;top:102px;font-size:38px;font-weight:900;color:#fff;letter-spacing:-1px;}
.rec-sub{position:absolute;left:56px;top:152px;font-size:20px;color:#555;}
.rec-wrap{position:absolute;left:56px;top:202px;right:56px;bottom:62px;display:flex;align-items:flex-start;gap:0;}
.rec-flow{flex:1;display:flex;flex-direction:column;align-items:center;gap:0;}
.rec-q{background:#1a1a1a;border:2px solid #4ade80;border-radius:16px;padding:14px 24px;text-align:center;width:340px;}
.rec-q-label{font-size:13px;font-weight:700;color:#4ade80;letter-spacing:1px;margin-bottom:4px;}
.rec-q-text{font-size:22px;font-weight:900;color:#fff;}
.rec-arr{font-size:24px;color:#4ade80;padding:4px 0;}
.rec-branch{display:flex;gap:16px;width:100%;}
.rec-yes{flex:1;display:flex;flex-direction:column;align-items:center;gap:0;}
.rec-no{flex:1;display:flex;flex-direction:column;align-items:center;gap:0;}
.rec-label-yn{font-size:13px;font-weight:700;letter-spacing:1px;padding:2px 0;}
.rec-action{border-radius:14px;padding:12px 16px;text-align:center;width:100%;}
.rec-action-text{font-size:17px;font-weight:700;line-height:1.5;}
.rec-win{position:absolute;right:56px;top:202px;width:280px;background:#0d1f0d;border:2px solid #4ade80;border-radius:20px;padding:24px;text-align:center;}
.rec-win-icon{font-size:44px;margin-bottom:10px;}
.rec-win-title{font-size:20px;font-weight:700;color:#4ade80;margin-bottom:10px;}
.rec-win-text{font-size:15px;color:#666;line-height:1.6;}
.rec-win-stat{font-size:36px;font-weight:900;color:#fff;margin-top:12px;letter-spacing:-1px;}
.rec-win-stat-label{font-size:14px;color:#555;}
</style>
<div class="rec-title">崩れた日の正しい戻り方</div>
<div class="rec-sub">「ゼロにしない」だけが唯一のルール</div>
<div class="rec-wrap">
  <div class="rec-flow">
    <div class="rec-q">
      <div class="rec-q-label">QUESTION</div>
      <div class="rec-q-text">今日、動けそうか？</div>
    </div>
    <div class="rec-arr">↓</div>
    <div class="rec-branch">
      <div class="rec-yes">
        <div class="rec-label-yn" style="color:#4ade80;">YES</div>
        <div class="rec-action" style="background:#0d200d;border:1px solid #4ade80;">
          <div class="rec-action-text" style="color:#4ade80;">レベルを<br>1つ下げる</div>
        </div>
        <div class="rec-arr">↓</div>
        <div class="rec-action" style="background:#111;border:1px solid #333;width:100%;">
          <div class="rec-action-text" style="color:#ccc;font-size:14px;">Lv3→Lv2<br>Lv2→Lv1<br>で続ける</div>
        </div>
      </div>
      <div class="rec-no">
        <div class="rec-label-yn" style="color:#ff4444;">NO</div>
        <div class="rec-action" style="background:#200808;border:1px solid #ff4444;">
          <div class="rec-action-text" style="color:#ff4444;">5分歩く<br>だけでいい</div>
        </div>
        <div class="rec-arr">↓</div>
        <div class="rec-action" style="background:#111;border:1px solid #333;width:100%;">
          <div class="rec-action-text" style="color:#ccc;font-size:14px;">近所を一周<br>でも十分<br>ゼロにしない</div>
        </div>
      </div>
    </div>
  </div>
  <div style="width:28px;"></div>
  <div class="rec-win">
    <div class="rec-win-icon">🏆</div>
    <div class="rec-win-title">続いている＝勝ち</div>
    <div class="rec-win-text">2024年メタ分析<br>（Fournier T et al.）<br><br>1日抜けても習慣の強度にはほとんど影響しない</div>
    <div class="rec-win-stat">8勝6敗</div>
    <div class="rec-win-stat-label">で十分。ゼロにしなければ勝ち。</div>
  </div>
</div>
"""
    return base_html(body, "#4ade80", "復帰", 8)


# ============================================================
# カード9：睡眠×運動比較（睡眠×運動）
# ============================================================
def card9() -> str:
    body = """
<style>
.slp-title{position:absolute;left:56px;top:102px;font-size:38px;font-weight:900;color:#fff;letter-spacing:-1px;}
.slp-sub{position:absolute;left:56px;top:152px;font-size:20px;color:#555;}
.slp-cols{position:absolute;left:56px;top:202px;right:56px;height:360px;display:flex;gap:20px;}
.slp-col{flex:1;border-radius:18px;padding:24px 20px;display:flex;flex-direction:column;gap:12px;}
.slp-col-ng{background:#180808;border:2px solid #ff4444;}
.slp-col-ok{background:#081020;border:2px solid #38bdf8;}
.slp-col-head{display:flex;align-items:center;gap:12px;}
.slp-col-icon{font-size:36px;}
.slp-col-info{}
.slp-col-title{font-size:22px;font-weight:900;}
.slp-col-ng .slp-col-title{color:#ff4444;}
.slp-col-ok .slp-col-title{color:#38bdf8;}
.slp-col-sleep{font-size:14px;color:#555;margin-top:2px;}
.slp-item{display:flex;align-items:flex-start;gap:10px;}
.slp-dot-ng{width:8px;height:8px;border-radius:50%;background:#ff4444;flex-shrink:0;margin-top:6px;}
.slp-dot-ok{width:8px;height:8px;border-radius:50%;background:#38bdf8;flex-shrink:0;margin-top:6px;}
.slp-item-text{font-size:17px;color:#aaa;line-height:1.5;}
.slp-bottom{position:absolute;left:56px;bottom:62px;right:56px;background:#0d1520;border:2px solid #38bdf8;border-radius:14px;padding:14px 28px;display:flex;align-items:center;gap:20px;}
.slp-bottom-icon{font-size:28px;}
.slp-bottom-text{font-size:20px;font-weight:700;color:#38bdf8;letter-spacing:-0.5px;}
.slp-bottom-sub{font-size:14px;color:#555;margin-top:2px;}
</style>
<div class="slp-title">攻める日の価値は前日の睡眠が決める</div>
<div class="slp-sub">HIITと睡眠はセットで考える</div>
<div class="slp-cols">
  <div class="slp-col slp-col-ng">
    <div class="slp-col-head">
      <div class="slp-col-icon">😴</div>
      <div class="slp-col-info">
        <div class="slp-col-title">寝不足の翌日</div>
        <div class="slp-col-sleep">睡眠 5時間以下</div>
      </div>
    </div>
    <div class="slp-item"><div class="slp-dot-ng"></div><div class="slp-item-text">フォームが雑になりやすい</div></div>
    <div class="slp-item"><div class="slp-dot-ng"></div><div class="slp-item-text">回復が遅れる</div></div>
    <div class="slp-item"><div class="slp-dot-ng"></div><div class="slp-item-text">集中力が続かない</div></div>
    <div class="slp-item"><div class="slp-dot-ng"></div><div class="slp-item-text">ケガのリスクが上がる</div></div>
    <div class="slp-item"><div class="slp-dot-ng"></div><div class="slp-item-text">同じ負荷でも苦しい</div></div>
  </div>
  <div class="slp-col slp-col-ok">
    <div class="slp-col-head">
      <div class="slp-col-icon">😊</div>
      <div class="slp-col-info">
        <div class="slp-col-title">十分な睡眠の翌日</div>
        <div class="slp-col-sleep">睡眠 7時間以上</div>
      </div>
    </div>
    <div class="slp-item"><div class="slp-dot-ok"></div><div class="slp-item-text">動きのキレが違う</div></div>
    <div class="slp-item"><div class="slp-dot-ok"></div><div class="slp-item-text">回復が早い</div></div>
    <div class="slp-item"><div class="slp-dot-ok"></div><div class="slp-item-text">集中してセットをこなせる</div></div>
    <div class="slp-item"><div class="slp-dot-ok"></div><div class="slp-item-text">フォームを維持できる</div></div>
    <div class="slp-item"><div class="slp-dot-ok"></div><div class="slp-item-text">同じ負荷が楽に感じる</div></div>
  </div>
</div>
<div class="slp-bottom">
  <div class="slp-bottom-icon">💡</div>
  <div>
    <div class="slp-bottom-text">バーピーの質を上げたければ、前日の夜から準備する</div>
    <div class="slp-bottom-sub">睡眠の整え方は第7回の記事で詳しく解説</div>
  </div>
</div>
"""
    return base_html(body, "#38bdf8", "睡眠×運動", 9)


# ============================================================
# カード10：今夜やること チェックリスト（CTA）
# ============================================================
def card10() -> str:
    body = """
<style>
.cta-title{position:absolute;left:56px;top:102px;font-size:52px;font-weight:900;color:#FF6D00;letter-spacing:-2px;text-shadow:0 0 40px rgba(255,109,0,.4);}
.cta-sub{position:absolute;left:56px;top:172px;font-size:24px;color:#666;}
.cta-checklist{position:absolute;left:56px;top:224px;right:380px;display:flex;flex-direction:column;gap:14px;}
.cta-item{background:#111;border-radius:14px;padding:16px 20px;display:flex;align-items:center;gap:16px;}
.cta-num{width:36px;height:36px;border-radius:50%;background:#FF6D00;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:900;color:#000;flex-shrink:0;}
.cta-text{font-size:20px;font-weight:700;color:#ccc;line-height:1.4;}
.cta-box{position:absolute;right:56px;top:224px;width:300px;background:#130800;border:2px solid #FF6D00;border-radius:20px;padding:28px 24px;text-align:center;}
.cta-box-tonight{font-size:16px;font-weight:700;color:#FF6D00;letter-spacing:2px;margin-bottom:8px;}
.cta-box-num{font-size:72px;font-weight:900;color:#fff;line-height:1;letter-spacing:-3px;}
.cta-box-unit{font-size:22px;font-weight:700;color:#FF6D00;}
.cta-box-detail{font-size:14px;color:#555;margin-top:10px;line-height:1.6;}
.cta-box-ok{background:#FF6D0022;border:1px solid #FF6D00;border-radius:8px;padding:6px 12px;margin-top:12px;font-size:14px;font-weight:700;color:#FF6D00;}
.cta-note{position:absolute;left:56px;bottom:62px;right:56px;text-align:center;font-size:18px;color:#444;}
.cta-note-url{color:#FF6D00;font-weight:700;}
</style>
<div class="cta-title">今夜だけ。</div>
<div class="cta-sub">まず1回やってみる。それだけでいい。</div>
<div class="cta-checklist">
  <div class="cta-item">
    <div class="cta-num">1</div>
    <div class="cta-text">スマホのタイマーをセット<br><span style="color:#555;font-size:15px;">20秒 → 40秒 × 4セット</span></div>
  </div>
  <div class="cta-item">
    <div class="cta-num">2</div>
    <div class="cta-text">ノージャンプ版でOK<br><span style="color:#555;font-size:15px;">飛ばなくていい。立つ→伏せるだけ</span></div>
  </div>
  <div class="cta-item">
    <div class="cta-num">3</div>
    <div class="cta-text">終わったら一言メモ<br><span style="color:#4ade80;font-size:15px;">「今日は、やった。」</span></div>
  </div>
  <div class="cta-item">
    <div class="cta-num">4</div>
    <div class="cta-text">詳細はnoteで確認<br><span style="color:#555;font-size:15px;">note.com/mash_anti_metabo</span></div>
  </div>
</div>
<div class="cta-box">
  <div class="cta-box-tonight">TODAY</div>
  <div class="cta-box-num">4</div>
  <div class="cta-box-unit">セット</div>
  <div class="cta-box-detail">20秒バーピー<br>↓<br>40秒休憩<br>× 4セット</div>
  <div class="cta-box-ok">ノージャンプOK</div>
</div>
"""
    return base_html(body, "#FF6D00", "今夜やること", 10)


# ============================================================
# X投稿テキスト保存
# ============================================================
def save_tweets(tweets: list[dict]) -> None:
    out = OUTPUT_DIR / "x_posts.md"
    lines = ["# 第8回 X投稿スレッド（10本）\n\n"]
    for t in tweets:
        lines.append(f"## 投稿{t['idx']}/10｜{t['tag']}\n\n")
        lines.append("```\n")
        lines.append(t["tweet"].strip() + "\n")
        lines.append("```\n\n")
        lines.append(f"![カード{t['idx']}](x_post_{t['idx']:02d}.png)\n\n---\n\n")
    out.write_text("".join(lines), encoding="utf-8")
    print(f"X投稿テキスト保存: {out.name}")


# ============================================================
# メイン
# ============================================================
CARD_FUNCS = [card1, card2, card3, card4, card5, card6, card7, card8, card9, card10]

if __name__ == "__main__":
    print("第8回 X投稿インフォグラフィックカード 生成開始...\n")

    tmp = ARTICLE_DIR / "_tmp_xcard.html"

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for i, (fn, tweet) in enumerate(zip(CARD_FUNCS, TWEETS), 1):
            html  = fn()
            fname = f"x_post_{i:02d}.png"
            out   = OUTPUT_DIR / fname

            tmp.write_text(html, encoding="utf-8")
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(f"file:///{tmp.as_posix()}")
            page.wait_for_timeout(700)
            page.screenshot(path=str(out), full_page=False)
            page.close()

            print(f"  {fname}  [{tweet['tag']}]")

        browser.close()

    tmp.unlink(missing_ok=True)
    save_tweets(TWEETS)

    print(f"\n全10枚完了。保存先: {OUTPUT_DIR}")
