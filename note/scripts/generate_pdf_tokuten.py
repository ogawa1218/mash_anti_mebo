#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E判定逆転30日プログラム - 特典PDF 3本 生成スクリプト
背景：アイボリー (#F8F4E8)
アクセント：オレンジ (#FF6D00) × 水色 (#38bdf8)
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent / "pdf_bonus"
OUTPUT_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────
# 共通CSS
# ─────────────────────────────────────────
SHARED_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap');

@page { size: A4; margin: 14mm 18mm 16mm 18mm; }

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Noto Sans JP', sans-serif;
  background: #F8F4E8;
  color: #1a1a2e;
  font-size: 10.5pt;
  line-height: 1.85;
}

/* ── COVER ── */
.cover {
  background: #1a1a2e;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 50px 40px;
  page-break-after: always;
}
.cover-badge {
  background: #FF6D00;
  color: #fff;
  padding: 5px 22px;
  border-radius: 20px;
  font-size: 9pt;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 28px;
  display: inline-block;
}
.cover-num {
  font-size: 11pt;
  color: #38bdf8;
  font-weight: 700;
  margin-bottom: 12px;
  letter-spacing: 2px;
}
.cover-title {
  font-size: 26pt;
  font-weight: 900;
  line-height: 1.4;
  color: #fff;
  margin-bottom: 10px;
}
.cover-title span { color: #FF6D00; }
.cover-subtitle {
  font-size: 12pt;
  color: #38bdf8;
  line-height: 1.7;
  margin-bottom: 40px;
}
.cover-divider {
  width: 56px; height: 3px;
  background: linear-gradient(to right, #FF6D00, #38bdf8);
  margin: 0 auto 32px;
  border-radius: 2px;
}
.cover-stats {
  display: flex;
  gap: 32px;
  margin-bottom: 40px;
}
.cover-stat {
  text-align: center;
}
.cover-stat .num { font-size: 22pt; font-weight: 900; color: #FF6D00; }
.cover-stat .label { font-size: 8pt; color: #9ca3af; margin-top: 2px; }
.cover-author { font-size: 10pt; color: #6b7280; margin-top: 8px; }
.cover-author span { color: #38bdf8; }

/* ── SECTION HEADER ── */
.sec-header {
  border-left: 5px solid #FF6D00;
  padding-left: 14px;
  margin: 28px 0 16px;
}
.sec-header h2 {
  font-size: 15pt;
  font-weight: 900;
  color: #1a1a2e;
}
.sec-header .sub {
  font-size: 9pt;
  color: #6b7280;
  margin-top: 3px;
}

.sec-header-blue {
  border-left: 5px solid #38bdf8;
  padding-left: 14px;
  margin: 28px 0 16px;
}
.sec-header-blue h2 {
  font-size: 14pt;
  font-weight: 900;
  color: #1a1a2e;
}

/* ── PART LABEL ── */
.part-label {
  display: inline-block;
  background: #FF6D00;
  color: #fff;
  padding: 4px 16px;
  border-radius: 4px;
  font-size: 9pt;
  font-weight: 700;
  margin-bottom: 6px;
  letter-spacing: 0.5px;
}
.part-label-blue {
  display: inline-block;
  background: #38bdf8;
  color: #1a1a2e;
  padding: 4px 16px;
  border-radius: 4px;
  font-size: 9pt;
  font-weight: 700;
  margin-bottom: 6px;
}

/* ── DARK BOX ── */
.dark-box {
  background: #1a1a2e;
  color: #fff;
  border-radius: 12px;
  padding: 20px 24px;
  margin: 16px 0;
}
.dark-box .label {
  font-size: 8.5pt;
  color: #38bdf8;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 8px;
}
.dark-box .value {
  font-size: 17pt;
  font-weight: 900;
  color: #FF6D00;
  line-height: 1.3;
}
.dark-box .desc {
  font-size: 9pt;
  color: #9ca3af;
  margin-top: 6px;
  line-height: 1.6;
}

/* ── HIGHLIGHT BOXES ── */
.hl-orange {
  background: #FFF4E8;
  border-left: 4px solid #FF6D00;
  padding: 14px 18px;
  border-radius: 0 8px 8px 0;
  margin: 14px 0;
  font-size: 10.5pt;
  line-height: 1.8;
}
.hl-blue {
  background: #EBF8FF;
  border-left: 4px solid #38bdf8;
  padding: 14px 18px;
  border-radius: 0 8px 8px 0;
  margin: 14px 0;
  font-size: 10.5pt;
  line-height: 1.8;
}
.hl-dark {
  background: #1a1a2e;
  color: #fff;
  padding: 18px 22px;
  border-radius: 10px;
  margin: 18px 0;
  font-size: 12pt;
  font-weight: 700;
  line-height: 1.7;
  text-align: center;
}
.hl-dark span { color: #FF6D00; }

/* ── TABLE ── */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 14px 0;
  font-size: 9.5pt;
}
thead tr { background: #1a1a2e; }
thead th {
  color: #fff;
  padding: 10px 13px;
  text-align: left;
  font-weight: 700;
  font-size: 9pt;
}
thead th:first-child { border-radius: 8px 0 0 0; }
thead th:last-child  { border-radius: 0 8px 0 0; }
tbody tr:nth-child(even) { background: #F0EBD8; }
tbody tr:nth-child(odd)  { background: #FAFAF5; }
tbody td {
  padding: 10px 13px;
  border-bottom: 1px solid #D4C9A8;
  color: #1a1a2e;
  vertical-align: top;
}

/* ── CHECKLIST ── */
.checklist { list-style: none; margin: 12px 0; }
.checklist li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 16px;
  margin-bottom: 8px;
  background: #FAFAF5;
  border-radius: 8px;
  border: 1.5px solid #D4C9A8;
  font-size: 10.5pt;
  line-height: 1.7;
}
.cb {
  width: 20px; height: 20px; min-width: 20px;
  border: 2px solid #FF6D00;
  border-radius: 4px;
  display: inline-block;
  margin-top: 2px;
}
.cb-blue {
  width: 20px; height: 20px; min-width: 20px;
  border: 2px solid #38bdf8;
  border-radius: 4px;
  display: inline-block;
  margin-top: 2px;
}

/* ── STEP ── */
.step {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 14px;
  padding: 14px 16px;
  background: #FAFAF5;
  border-radius: 10px;
  border: 1.5px solid #D4C9A8;
}
.step-num {
  background: #FF6D00;
  color: #fff;
  width: 34px; height: 34px; min-width: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 13pt;
}
.step-body h4 {
  font-size: 11pt;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 5px;
}
.step-body p {
  font-size: 9.5pt;
  color: #5a5a7a;
  line-height: 1.75;
}

/* ── TYPE BADGE ── */
.badge { display: inline-block; padding: 3px 11px; border-radius: 12px; font-size: 8.5pt; font-weight: 700; }
.badge-a { background: #FFE4D0; color: #c2410c; }
.badge-b { background: #D0EAFF; color: #0369a1; }
.badge-c { background: #D0FFE4; color: #15803d; }
.badge-d { background: #FFD0E4; color: #9d174d; }
.badge-e { background: #E4D0FF; color: #6d28d9; }

/* ── MAERCY MESSAGE ── */
.maercy {
  background: #1a1a2e;
  color: #e5e7eb;
  border-radius: 14px;
  padding: 22px 26px 20px;
  margin: 20px 0;
  position: relative;
}
.maercy::before {
  content: "マーシーより";
  position: absolute;
  top: -13px; left: 22px;
  background: #FF6D00;
  color: #fff;
  padding: 4px 14px;
  border-radius: 12px;
  font-size: 8.5pt;
  font-weight: 700;
}
.maercy p { font-size: 10.5pt; line-height: 1.9; }

/* ── TIMELINE ── */
.timeline { padding-left: 28px; margin: 14px 0; position: relative; }
.timeline::before {
  content: '';
  position: absolute; left: 10px; top: 8px; bottom: 8px;
  width: 2px; background: #D4C9A8;
}
.tl-item {
  position: relative;
  margin-bottom: 14px;
  padding: 13px 16px;
  background: #FAFAF5;
  border-radius: 8px;
  border: 1.5px solid #D4C9A8;
}
.tl-item::before {
  content: '';
  position: absolute;
  left: -22px; top: 16px;
  width: 12px; height: 12px;
  background: #FF6D00;
  border-radius: 50%;
  border: 2px solid #F8F4E8;
}
.tl-title { font-size: 10.5pt; font-weight: 700; color: #FF6D00; margin-bottom: 7px; }

/* ── WRITE SPACE ── */
.write-space {
  border: 1.5px solid #D4C9A8;
  border-radius: 8px;
  padding: 14px 16px;
  min-height: 64px;
  background: #fff;
  margin: 8px 0;
}
.write-line {
  border-bottom: 1px solid #D4C9A8;
  min-height: 32px;
  margin-bottom: 10px;
}

/* ── RECORD CARD ── */
.record-card {
  background: #FAFAF5;
  border: 1.5px solid #D4C9A8;
  border-radius: 12px;
  padding: 14px 18px;
  margin-bottom: 14px;
  page-break-inside: avoid;
}
.record-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 1px solid #D4C9A8;
  margin-bottom: 12px;
}
.rc-day { font-size: 15pt; font-weight: 900; color: #FF6D00; }
.rc-date { font-size: 9pt; color: #6b7280; }
.rc-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  font-size: 9.5pt;
}
.rc-label { color: #6b7280; font-weight: 700; width: 100px; min-width: 100px; }
.rc-input { border-bottom: 1px solid #D4C9A8; flex: 1; min-height: 22px; }
.rc-options { display: flex; gap: 14px; flex-wrap: wrap; }
.rc-opt { display: flex; align-items: center; gap: 6px; font-size: 9pt; }
.rc-circle { width: 14px; height: 14px; border-radius: 50%; border: 1.5px solid #D4C9A8; display: inline-block; }

/* ── REVIEW CARD ── */
.review-card {
  background: #fff;
  border: 2px solid #FF6D00;
  border-radius: 14px;
  padding: 22px 24px;
  margin: 16px 0;
  page-break-inside: avoid;
}
.review-card-title {
  font-size: 13pt;
  font-weight: 900;
  color: #FF6D00;
  margin-bottom: 18px;
  padding-bottom: 10px;
  border-bottom: 1px solid #F0EBD8;
}
.review-q { font-size: 9.5pt; font-weight: 700; color: #1a1a2e; margin-bottom: 6px; margin-top: 14px; }

/* ── DIVIDER ── */
.divider {
  height: 2px;
  background: linear-gradient(to right, #FF6D00 0%, #38bdf8 50%, transparent 100%);
  margin: 20px 0;
  border-radius: 2px;
}

/* ── PAGE BREAK ── */
.pb { page-break-after: always; }

/* ── FOOTER ── */
.footer {
  text-align: center;
  font-size: 8pt;
  color: #9ca3af;
  margin-top: 20px;
  padding-top: 10px;
  border-top: 1px solid #D4C9A8;
}

/* ── EMERGENCY BOX ── */
.emergency {
  background: #1a1a2e;
  border-radius: 14px;
  padding: 22px 26px;
  margin: 20px 0;
}
.emergency-title {
  font-size: 13pt;
  font-weight: 900;
  color: #FF6D00;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.emergency-steps { list-style: none; }
.emergency-steps li {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 10px 0;
  border-bottom: 1px solid #2d3748;
  color: #e5e7eb;
  font-size: 10.5pt;
}
.emergency-steps li:last-child { border-bottom: none; }
.e-num {
  background: #FF6D00;
  color: #fff;
  width: 28px; height: 28px; min-width: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 11pt;
  margin-top: 1px;
}

/* ── GRID 2COL ── */
.grid2 { display: flex; gap: 14px; margin: 14px 0; }
.grid2 > * { flex: 1; }

/* ── LEVEL BOX ── */
.level-box {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  border: 1.5px solid #D4C9A8;
  margin-bottom: 10px;
  background: #FAFAF5;
  align-items: flex-start;
  page-break-inside: avoid;
}
.level-dot {
  width: 16px; height: 16px; min-width: 16px;
  border-radius: 50%;
  margin-top: 4px;
}
.level-body strong { font-size: 10.5pt; font-weight: 700; display: block; margin-bottom: 4px; }
.level-body p { font-size: 9pt; color: #5a5a7a; line-height: 1.7; }

/* ── LETTER PAGE ── */
.letter-page {
  background: #fff;
  border: 2px solid #D4C9A8;
  border-radius: 16px;
  padding: 30px 32px;
  margin: 20px 0;
  min-height: 300px;
}
.letter-page .greeting { font-size: 11pt; font-weight: 700; margin-bottom: 16px; color: #6b7280; }
.letter-area { min-height: 200px; }
.letter-line { border-bottom: 1px solid #D4C9A8; min-height: 34px; margin-bottom: 4px; }
.letter-sig { text-align: right; font-size: 10pt; color: #6b7280; margin-top: 16px; }
"""

# ─────────────────────────────────────────
# PDF① 夜食対策表
# ─────────────────────────────────────────
def html_pdf1():
    return f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8">
<style>{SHARED_CSS}</style>
</head><body>

<!-- ══ COVER ══ -->
<div class="cover">
  <span class="cover-badge">E判定逆転30日プログラム｜特典PDF ①</span>
  <div class="cover-num">TOKUTEN PDF 01</div>
  <h1 class="cover-title">夜食<span>対策</span>表</h1>
  <p class="cover-subtitle">意志力ゼロで「夜の崩れ」を止める<br>状況別・完全対処マニュアル</p>
  <div class="cover-divider"></div>
  <div class="cover-stats">
    <div class="cover-stat"><div class="num">5</div><div class="label">欲求タイプ</div></div>
    <div class="cover-stat"><div class="num">3</div><div class="label">分プロトコル</div></div>
    <div class="cover-stat"><div class="num">30+</div><div class="label">置き換え食品</div></div>
  </div>
  <p class="cover-author">Longevity Navigator ／ <span>マーシー｜−32kg × サブ3</span></p>
</div>

<!-- ══ P2 はじめに ══ -->
<div class="pb">
  <div class="sec-header"><h2>このPDFの使い方</h2><p class="sub">読み込む必要はありません。困ったときに開くリファレンスです。</p></div>
  <p>このPDFは、<strong>「夜食を食べたくなった瞬間」に開くためのもの</strong>です。スマホのホーム画面に保存、または印刷してキッチンに貼るのが最も効果的な活用法です。</p>
  <br>
  <table>
    <thead><tr><th>パート</th><th>内容</th><th>使うタイミング</th></tr></thead>
    <tbody>
      <tr><td><strong>PART 1</strong></td><td>夜食欲求の正体</td><td>「なぜ食べたくなるか」を理解したいとき</td></tr>
      <tr><td><strong>PART 2</strong></td><td>状況別・対処マップ</td><td>「今夜食べたい」と思った瞬間</td></tr>
      <tr><td><strong>PART 3</strong></td><td>置き換えフード完全リスト</td><td>「何を食べればいいか」迷ったとき</td></tr>
    </tbody>
  </table>
  <div class="hl-orange"><strong>ルール：</strong>完璧にやろうとしなくていいです。このシートを開いた時点で、すでに一歩踏み留まっています。それだけで十分です。</div>

  <div class="divider"></div>
  <div class="sec-header"><h2>PART 1　夜食欲求の正体を知る</h2><p class="sub">意志力の問題ではなく、ホルモンと環境の問題です</p></div>
  <p>夜に食欲が増すのは体の設計上、当然のことです。理由は4つあります。</p>
  <br>
  <div class="step">
    <div class="step-num">1</div>
    <div class="step-body">
      <h4>コルチゾールの蓄積</h4>
      <p>日中のストレスでコルチゾール（ストレスホルモン）が蓄積されます。コルチゾールは高カロリー食（脂質＋糖質の組み合わせ）への欲求を強く引き起こします。忙しい日ほど夜の食欲が強いのはこのためです。</p>
    </div>
  </div>
  <div class="step">
    <div class="step-num">2</div>
    <div class="step-body">
      <h4>グレリンの上昇（睡眠不足）</h4>
      <p>睡眠6時間未満でグレリン（食欲促進ホルモン）が24%増加、レプチン（満腹ホルモン）が18%減少します（Spiegel et al., 2004）。睡眠が少ない夜ほど夜食欲求が強くなる直接の原因です。</p>
    </div>
  </div>
  <div class="step">
    <div class="step-num">3</div>
    <div class="step-body">
      <h4>血糖値の底打ち</h4>
      <p>夕食後3〜4時間で血糖値が下降し「軽い低血糖状態」になります。脳はエネルギー不足と判断し緊急食欲信号を送ります。夜10〜11時の「甘いものが無性に欲しい」の正体です。</p>
    </div>
  </div>
  <div class="step">
    <div class="step-num">4</div>
    <div class="step-body">
      <h4>習慣の自動起動（条件反射）</h4>
      <p>「帰宅→ソファ→お菓子」が習慣化されると、帰宅しただけで食欲回路が起動します。これはパブロフの条件反射と同じメカニズムです。食べたいのではなく、ルーティンが勝手に動いているだけです。</p>
    </div>
  </div>

  <div class="hl-dark"><span>意志力で止めようとするから止まらない。</span><br>原因がわかれば、仕組みで対処できます。</div>
  <div class="footer">E判定逆転30日プログラム｜特典PDF① 夜食対策表　／　Longevity Navigator</div>
</div>

<!-- ══ P3 欲求タイプ診断 ══ -->
<div class="pb">
  <div class="sec-header"><h2>今夜の欲求はどのタイプ？</h2><p class="sub">タイプによって対処法が変わります</p></div>
  <table>
    <thead><tr><th>タイプ</th><th>特徴・サイン</th><th>主な原因</th></tr></thead>
    <tbody>
      <tr>
        <td><span class="badge badge-a">A ストレス食い</span></td>
        <td>イライラ・もやもやしている。甘い・脂っこいものが欲しい</td>
        <td>コルチゾール蓄積</td>
      </tr>
      <tr>
        <td><span class="badge badge-b">B 習慣食い</span></td>
        <td>特に食べたいわけじゃないが手が動く。帰宅後の流れで</td>
        <td>条件反射・習慣の自動起動</td>
      </tr>
      <tr>
        <td><span class="badge badge-c">C 本物の空腹</span></td>
        <td>胃がキュルキュル言っている。何でも食べたい</td>
        <td>夕食量が少なかった</td>
      </tr>
      <tr>
        <td><span class="badge badge-d">D 口寂しい</span></td>
        <td>何かを口に入れたいだけ。退屈・手持ち無沙汰</td>
        <td>刺激不足・習慣</td>
      </tr>
      <tr>
        <td><span class="badge badge-e">E 睡眠不足型</span></td>
        <td>眠いのに目が冴えている。甘いものを強烈に求めている</td>
        <td>グレリン上昇・睡眠不足</td>
      </tr>
    </tbody>
  </table>
  <div class="hl-blue"><strong>本物の空腹かどうかの確認法：</strong><br>「ブロッコリーが食べたいか」と自問してください。何でもいいから食べたいなら本物の空腹。チョコやポテチなど特定のものだけ食べたいなら、別タイプの欲求です。</div>

  <div class="divider"></div>
  <div class="sec-header"><h2>PART 2　状況別・対処マップ</h2></div>

  <div style="margin-bottom:14px;">
    <span class="badge badge-a" style="font-size:10pt;padding:5px 14px;margin-bottom:8px;display:inline-block;">タイプ A　ストレス食い</span>
    <div class="timeline">
      <div class="tl-item">
        <div class="tl-title">まず3分やること</div>
        <p>① スマホを伏せて置く<br>② 4-7-8呼吸を3回（4秒吸う→7秒止める→8秒で吐く）<br>③ 「今夜のストレスの原因」を1行メモに書く<br>→ 呼吸でコルチゾールが低下。メモで感情を外に出す。</p>
      </div>
      <div class="tl-item">
        <div class="tl-title">それでも食べたい場合</div>
        <p>PART 3「Aタイプ向け」置き換えリストから選ぶ</p>
      </div>
      <div class="tl-item">
        <div class="tl-title">環境チェック</div>
        <p>視界にお菓子が見えていないか確認 → 見えている場合は棚の奥に移動</p>
      </div>
    </div>
  </div>

  <div style="margin-bottom:14px;">
    <span class="badge badge-b" style="font-size:10pt;padding:5px 14px;margin-bottom:8px;display:inline-block;">タイプ B　習慣食い</span>
    <div class="timeline">
      <div class="tl-item">
        <div class="tl-title">まず10分やること</div>
        <p>① 歯を磨く（これだけで食べる気が大幅に低下します）<br>② 部屋を暗くして横になる<br>③ スマホを寝室と別の部屋に置く<br>→ 帰宅→ソファ→お菓子の連鎖の「きっかけ」を断ち切る</p>
      </div>
      <div class="tl-item">
        <div class="tl-title">明日以降の設計改善</div>
        <p>帰宅後すぐ着替えてシャワーを浴びるルーティンを挿入する → 従来の条件反射を書き換える</p>
      </div>
    </div>
  </div>
  <div class="footer">E判定逆転30日プログラム｜特典PDF① 夜食対策表　／　Longevity Navigator</div>
</div>

<!-- ══ P4 タイプC〜E ══ -->
<div class="pb">
  <div style="margin-bottom:14px;">
    <span class="badge badge-c" style="font-size:10pt;padding:5px 14px;margin-bottom:8px;display:inline-block;">タイプ C　本物の空腹</span>
    <div class="timeline">
      <div class="tl-item">
        <div class="tl-title">まず確認</div>
        <p>水を200ml飲む → 20分待つ。それでも空腹なら本物の空腹として食べてOK。</p>
      </div>
      <div class="tl-item">
        <div class="tl-title">食べるときのルール</div>
        <p>PART 3「Cタイプ向け」から選ぶ。食べる量は「手のひら1杯分」を目安に。</p>
      </div>
    </div>
  </div>

  <div style="margin-bottom:14px;">
    <span class="badge badge-d" style="font-size:10pt;padding:5px 14px;margin-bottom:8px;display:inline-block;">タイプ D　口寂しい</span>
    <div class="timeline">
      <div class="tl-item">
        <div class="tl-title">まず試すこと（カロリーゼロ）</div>
        <p>① 強炭酸水を飲む（ウィルキンソン推奨）<br>② キシリトールガムを噛む<br>③ ハーブティーを淹れる（準備の時間で欲求が収まることも）</p>
      </div>
      <div class="tl-item">
        <div class="tl-title">それでも口寂しい場合</div>
        <p>PART 3「Dタイプ向け」から選ぶ。食べることを責めない。カロリーへの影響を最小化しながら欲求を満たすことが目標。</p>
      </div>
    </div>
  </div>

  <div style="margin-bottom:14px;">
    <span class="badge badge-e" style="font-size:10pt;padding:5px 14px;margin-bottom:8px;display:inline-block;">タイプ E　睡眠不足型</span>
    <div class="timeline">
      <div class="tl-item">
        <div class="tl-title">今夜の最優先事項：寝ること</div>
        <p>睡眠不足型の夜食欲求は、食べても解消されません。グレリンは睡眠によってしか正常化しないからです。</p>
      </div>
      <div class="tl-item">
        <div class="tl-title">今すぐやること</div>
        <p>① スマホを別の部屋に置く<br>② 部屋の照明を最も暗い設定にする<br>③ 布団に入る（眠れなくてもOK。横になるだけでいい）</p>
      </div>
      <div class="tl-item">
        <div class="tl-title">どうしても眠れない場合</div>
        <p>ホットミルク1杯（トリプトファンが睡眠促進）またはバナナ1/2本を食べてから就寝してください。</p>
      </div>
    </div>
  </div>
  <div class="footer">E判定逆転30日プログラム｜特典PDF① 夜食対策表　／　Longevity Navigator</div>
</div>

<!-- ══ P5 置き換えリスト ══ -->
<div class="pb">
  <div class="sec-header"><h2>PART 3　置き換えフード完全リスト</h2><p class="sub">3基準：低GI ／ 高タンパク or 高食物繊維 ／ コンビニで買える</p></div>

  <div class="part-label">タイプA ストレス食い向け</div>
  <table>
    <thead><tr><th>食べたいもの</th><th>置き換え</th><th>理由</th></tr></thead>
    <tbody>
      <tr><td>ポテチ</td><td><strong>素焼きミックスナッツ（一握り・約30g）</strong></td><td>血糖値スパイクなし。良質な脂質</td></tr>
      <tr><td>チョコ</td><td><strong>カカオ72%以上のチョコ（2〜3片）</strong></td><td>ポリフェノールで抗ストレス効果</td></tr>
      <tr><td>アイス</td><td><strong>冷凍ブルーベリー（50g）</strong></td><td>自然な甘み・低GI・抗酸化物質豊富</td></tr>
      <tr><td>スナック菓子</td><td><strong>焼き海苔（3〜4枚）</strong></td><td>低カロリー・ミネラル豊富・咀嚼満足感</td></tr>
      <tr><td>揚げ物</td><td><strong>ゆで卵1個＋からし少量</strong></td><td>タンパク質で10分後に食欲が落ち着く</td></tr>
    </tbody>
  </table>

  <div class="part-label">タイプB 習慣食い向け</div>
  <table>
    <thead><tr><th>置き換え</th><th>おすすめ商品・作り方</th><th>効果</th></tr></thead>
    <tbody>
      <tr><td><strong>強炭酸水</strong></td><td>ウィルキンソン炭酸水（レモン）</td><td>口の刺激を代替。食欲抑制</td></tr>
      <tr><td><strong>ハーブティー</strong></td><td>カモミール or ペパーミントティー</td><td>副交感神経優位・食欲抑制</td></tr>
      <tr><td><strong>スルメ（細く）</strong></td><td>細く裂いて1〜2本</td><td>咀嚼回数多く満足感高い・低カロリー</td></tr>
      <tr><td><strong>寒天ゼリー</strong></td><td>砂糖不使用の寒天ゼリー</td><td>カロリーほぼゼロ・食べた感あり</td></tr>
      <tr><td><strong>キシリトールガム</strong></td><td>どの銘柄でも可</td><td>噛む行為への欲求を直接満たす</td></tr>
    </tbody>
  </table>

  <div class="part-label">タイプC 本物の空腹向け</div>
  <table>
    <thead><tr><th>食品</th><th>量の目安</th><th>選ぶ理由</th></tr></thead>
    <tbody>
      <tr><td><strong>ギリシャヨーグルト</strong></td><td>100〜150g</td><td>高タンパク・腹持ちが良い</td></tr>
      <tr><td><strong>ゆで卵</strong></td><td>1〜2個</td><td>タンパク質で空腹を素早く満たす</td></tr>
      <tr><td><strong>豆腐（冷奴）</strong></td><td>1/2丁</td><td>低カロリー・高タンパク</td></tr>
      <tr><td><strong>納豆</strong></td><td>1パック</td><td>発酵食品・腸内環境にも良い</td></tr>
      <tr><td><strong>バナナ</strong></td><td>1/2本</td><td>素早いエネルギー補給・半分で止める</td></tr>
    </tbody>
  </table>

  <div class="grid2">
    <div>
      <div class="part-label">タイプD 口寂しい向け</div>
      <ul class="checklist" style="margin-top:8px;">
        <li><div class="cb"></div>強炭酸水（最優先）</li>
        <li><div class="cb"></div>スルメ（咀嚼欲求を直接満たす）</li>
        <li><div class="cb"></div>焼き海苔（低カロリー）</li>
        <li><div class="cb"></div>キシリトールガム</li>
        <li><div class="cb"></div>お茶を淹れる（準備時間で欲求消化）</li>
      </ul>
    </div>
    <div>
      <div class="part-label badge-e" style="background:#E4D0FF;color:#6d28d9;">タイプE 睡眠不足型向け</div>
      <ul class="checklist" style="margin-top:8px;">
        <li><div class="cb-blue"></div>ホットミルク200ml（トリプトファン）</li>
        <li><div class="cb-blue"></div>バナナ1/2本（マグネシウム）</li>
        <li><div class="cb-blue"></div>カモミールティー（GABA作用）</li>
      </ul>
      <div class="hl-blue" style="font-size:9pt;margin-top:8px;"><strong>最優先は「寝ること」です。</strong></div>
    </div>
  </div>
  <div class="footer">E判定逆転30日プログラム｜特典PDF① 夜食対策表　／　Longevity Navigator</div>
</div>

<!-- ══ P6 緊急プロトコル＋環境設計 ══ -->
<div class="pb">
  <div class="emergency">
    <div class="emergency-title">⚡ 緊急時3分プロトコル</div>
    <ul class="emergency-steps">
      <li><div class="e-num">1</div><div><strong>水を1杯飲む（30秒）</strong><br><span style="font-size:9pt;color:#9ca3af;">空腹感の多くは脱水です。水200mlで血糖値も少し安定します。</span></div></li>
      <li><div class="e-num">2</div><div><strong>歯を磨く（1分）</strong><br><span style="font-size:9pt;color:#9ca3af;">歯磨き後の食欲は心理的に大幅に低下します。これだけで解決することも多い。</span></div></li>
      <li><div class="e-num">3</div><div><strong>4-7-8呼吸を3回（1分30秒）</strong><br><span style="font-size:9pt;color:#9ca3af;">4秒吸う→7秒止める→8秒で吐く。コルチゾールが下がり食欲への切迫感が和らぎます。</span></div></li>
      <li><div class="e-num">4</div><div><strong>それでも食べたいなら置き換えリストから選ぶ</strong><br><span style="font-size:9pt;color:#9ca3af;">ここまでやって食べるなら、それは本物の欲求。責めずに置き換えを。</span></div></li>
    </ul>
  </div>

  <div class="sec-header"><h2>今週やること：環境設計チェックリスト</h2><p class="sub">一度やれば、毎晩の意志力が不要になります</p></div>

  <p style="font-weight:700;margin-bottom:8px;">▶ 買い物リスト（置き換えフードの備蓄）</p>
  <ul class="checklist">
    <li><div class="cb"></div>素焼きミックスナッツ（大袋。小分けして保存）</li>
    <li><div class="cb"></div>カカオ70%以上チョコレート</li>
    <li><div class="cb"></div>ウィルキンソン強炭酸水（ケース買い推奨）</li>
    <li><div class="cb"></div>ギリシャヨーグルト（複数個ストック）</li>
    <li><div class="cb"></div>カモミールティー or ハーブティー</li>
    <li><div class="cb"></div>ゆで卵（週初めに5個まとめてゆでておく）</li>
  </ul>

  <p style="font-weight:700;margin:14px 0 8px;">▶ 冷蔵庫の配置変え</p>
  <ul class="checklist">
    <li><div class="cb"></div>目線の高さ → ゆで卵・ギリシャヨーグルト・野菜を置く</li>
    <li><div class="cb"></div>目線より上 → チョコ・ナッツ（食べてもいいが見えにくく）</li>
    <li><div class="cb"></div>冷凍庫の一番奥・一番下 → アイス類を移動</li>
  </ul>

  <p style="font-weight:700;margin:14px 0 8px;">▶ リビングの整理</p>
  <ul class="checklist">
    <li><div class="cb"></div>テーブルの上：食べ物をゼロにする</li>
    <li><div class="cb"></div>炭酸水をリビングのすぐ手の届く場所に置く</li>
    <li><div class="cb"></div>お菓子のストックをリビングから別の部屋へ移動</li>
  </ul>

  <div class="maercy">
    <p>環境を変えるのに意志力は要りません。最初の10分だけ集中してください。棚を整理して、冷蔵庫を並び替えて、炭酸水を買ってくる。それだけで、毎晩の「戦い」がなくなります。<br><br>僕は環境を変えた週から、夜食を一切我慢せずにほぼゼロになりました。意志は使っていません。環境が自動的に行動を変えてくれたからです。</p>
  </div>
  <div class="footer">E判定逆転30日プログラム｜特典PDF① 夜食対策表　／　Longevity Navigator</div>
</div>

</body></html>"""


# ─────────────────────────────────────────
# PDF② 崩れ復帰チェックシート
# ─────────────────────────────────────────
def html_pdf2():
    return f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8">
<style>{SHARED_CSS}</style>
</head><body>

<!-- ══ COVER ══ -->
<div class="cover">
  <span class="cover-badge">E判定逆転30日プログラム｜特典PDF ②</span>
  <div class="cover-num">TOKUTEN PDF 02</div>
  <h1 class="cover-title">崩れ<span>復帰</span><br>チェックシート</h1>
  <p class="cover-subtitle">「また失敗した」を「データが取れた」に変える<br>72時間リセットガイド</p>
  <div class="cover-divider"></div>
  <div class="cover-stats">
    <div class="cover-stat"><div class="num">72</div><div class="label">時間で戻る</div></div>
    <div class="cover-stat"><div class="num">7</div><div class="label">セクション</div></div>
    <div class="cover-stat"><div class="num">0</div><div class="label">自己嫌悪</div></div>
  </div>
  <p class="cover-author">Longevity Navigator ／ <span>マーシー｜−32kg × サブ3</span></p>
</div>

<!-- ══ P2 はじめに ══ -->
<div class="pb">
  <div class="sec-header"><h2>このシートを使う前に</h2></div>
  <div class="hl-dark"><span>崩れたことは、失敗ではありません。</span></div>
  <p>意志が弱かったわけでも、プログラムが終わったわけでも、あなたがダメな人間なわけでもありません。特定のコンディションと環境が重なったとき、人間は誰でも崩れます。僕も今でも崩れます。</p>
  <br>
  <p>このシートの目的は「反省して気合を入れ直すこと」ではありません。<strong>「なぜ崩れたかのデータを取り、次の設計を1つだけ変えること」</strong>です。</p>
  <br>
  <table>
    <thead><tr><th>セクション</th><th>内容</th><th>所要時間</th></tr></thead>
    <tbody>
      <tr><td>SECTION 1</td><td>崩れの記録</td><td>2分</td></tr>
      <tr><td>SECTION 2</td><td>原因分析チェック</td><td>3分</td></tr>
      <tr><td>SECTION 3</td><td>深刻度の確認</td><td>30秒</td></tr>
      <tr><td>SECTION 4</td><td>感情の処理（重い場合のみ）</td><td>5分</td></tr>
      <tr><td>SECTION 5</td><td>72時間リセットプロトコル</td><td>実行するだけ</td></tr>
      <tr><td>SECTION 6</td><td>崩れパターン分析（繰り返し使用）</td><td>5分</td></tr>
      <tr><td>SECTION 7</td><td>再スタートガイド（1週間以上崩れた場合）</td><td>5分</td></tr>
    </tbody>
  </table>
  <div class="footer">E判定逆転30日プログラム｜特典PDF② 崩れ復帰チェックシート　／　Longevity Navigator</div>
</div>

<!-- ══ P3 SECTION1〜3 ══ -->
<div class="pb">
  <div class="sec-header"><h2>SECTION 1　崩れの記録（2分）</h2><p class="sub">感情は書かなくていいです。事実だけ書きます。</p></div>
  <div class="record-card">
    <div class="record-card-header">
      <span style="font-weight:900;font-size:12pt;color:#FF6D00;">記録日</span>
      <span style="color:#6b7280;font-size:9.5pt;">　　　年　　月　　日</span>
    </div>
    <div class="rc-row"><div class="rc-label">何を食べましたか？</div><div class="rc-input"></div></div>
    <div class="rc-row"><div class="rc-label">何時頃ですか？</div><div class="rc-input"></div></div>
    <div class="rc-row">
      <div class="rc-label">食べた量</div>
      <div class="rc-options">
        <div class="rc-opt"><div class="rc-circle"></div>少し</div>
        <div class="rc-opt"><div class="rc-circle"></div>普通</div>
        <div class="rc-opt"><div class="rc-circle"></div>多め</div>
        <div class="rc-opt"><div class="rc-circle"></div>かなり多い</div>
      </div>
    </div>
  </div>

  <div class="sec-header"><h2>SECTION 2　崩れの原因分析（3分）</h2><p class="sub">当てはまるものに✓をつけてください（複数可）</p></div>
  <div class="grid2">
    <div>
      <p style="font-weight:700;margin-bottom:8px;color:#FF6D00;">▶ コンディション系</p>
      <ul class="checklist">
        <li><div class="cb"></div>睡眠が6時間未満だった</li>
        <li><div class="cb"></div>仕事・人間関係でストレスが高かった</li>
        <li><div class="cb"></div>体調が優れなかった</li>
        <li><div class="cb"></div>疲労度が特に高い1日だった</li>
      </ul>
      <p style="font-weight:700;margin:12px 0 8px;color:#38bdf8;">▶ 習慣・トリガー系</p>
      <ul class="checklist">
        <li><div class="cb-blue"></div>帰宅後の習慣でつい食べた</li>
        <li><div class="cb-blue"></div>テレビ・スマホを見ながら食べた</li>
        <li><div class="cb-blue"></div>「今日だけいいや」と思った</li>
        <li><div class="cb-blue"></div>最初の1口が止まらなかった</li>
      </ul>
    </div>
    <div>
      <p style="font-weight:700;margin-bottom:8px;color:#FF6D00;">▶ 環境系</p>
      <ul class="checklist">
        <li><div class="cb"></div>家に「崩れの原因」食品があった</li>
        <li><div class="cb"></div>コンビニや飲食店に立ち寄った</li>
        <li><div class="cb"></div>視界に食べ物があった</li>
        <li><div class="cb"></div>飲み会・外食があった</li>
      </ul>
      <p style="font-weight:700;margin:12px 0 8px;color:#38bdf8;">▶ その他</p>
      <ul class="checklist">
        <li><div class="cb-blue"></div>夕食の量が少なかった（本物の空腹）</li>
        <li><div class="cb-blue"></div>理由がわからない</li>
        <li><div class="cb-blue"></div>その他：<div class="rc-input" style="flex:1;margin-left:8px;"></div></li>
      </ul>
    </div>
  </div>

  <div class="sec-header"><h2>SECTION 3　深刻度の確認（30秒）</h2></div>
  <div class="level-box"><div class="level-dot" style="background:#22c55e;"></div><div class="level-body"><strong>レベル1：1回、置き換えできないものを食べた</strong><p>→ 気にしなくてOK。次の食事だけ整えましょう。このシートの残りは読まなくていいです。</p></div></div>
  <div class="level-box"><div class="level-dot" style="background:#FF6D00;"></div><div class="level-body"><strong>レベル2：夜食を複数回食べた（1日）</strong><p>→ SECTION 5の72時間プロトコルを実行してください。</p></div></div>
  <div class="level-box"><div class="level-dot" style="background:#ef4444;"></div><div class="level-body"><strong>レベル3：2〜3日連続で崩れている</strong><p>→ SECTION 4の「感情処理」から始めてください。</p></div></div>
  <div class="level-box"><div class="level-dot" style="background:#7c3aed;"></div><div class="level-body"><strong>レベル4：1週間以上崩れ続けている</strong><p>→ SECTION 7の「再スタートガイド」を使用してください。</p></div></div>
  <div class="footer">E判定逆転30日プログラム｜特典PDF② 崩れ復帰チェックシート　／　Longevity Navigator</div>
</div>

<!-- ══ P4 SECTION4〜5 ══ -->
<div class="pb">
  <div class="sec-header"><h2>SECTION 4　感情の処理</h2><p class="sub">感情が重い場合のみ。行動より先に感情を処理します。</p></div>
  <div class="review-card">
    <p style="font-size:9.5pt;color:#5a5a7a;margin-bottom:14px;">自己嫌悪が強い場合は、行動より先に感情を処理します。以下の質問に、思ったことをそのまま書いてください。正解はありません。</p>
    <div class="review-q">Q1. 今、自分に対してどんな言葉が浮かびますか？</div>
    <div class="write-space"><div class="write-line"></div><div class="write-line"></div></div>
    <div class="review-q">Q2. もし親友が同じ状況だったら、あなたは何と言いますか？</div>
    <div class="write-space"><div class="write-line"></div><div class="write-line"></div></div>
    <div class="review-q">Q3. Q2の言葉を、今の自分に言ってみてください。（頭の中だけでOK）</div>
    <div class="hl-blue" style="margin-top:10px;font-size:9.5pt;">自分に厳しすぎる人は、他人には優しい言葉をかけられるのに自分にだけ残酷になります。あなたが親友に言える言葉は、あなた自身にも言っていい言葉です。</div>
  </div>

  <div class="sec-header"><h2>SECTION 5　72時間リセットプロトコル</h2><p class="sub">崩れた翌日から72時間、この順番で動いてください。</p></div>

  <div class="part-label">崩れた当日（夜）</div>
  <ul class="checklist" style="margin-top:8px;">
    <li><div class="cb"></div>これ以上食べるのをやめる（「今日はもう終わり」ではなく「今夜はここで止める」）</li>
    <li><div class="cb"></div>歯を磨く</li>
    <li><div class="cb"></div>炭酸水か白湯を1杯飲む</li>
    <li><div class="cb"></div>就寝時間を通常より30分早める</li>
    <li><div class="cb"></div>「明日の朝食に何を食べるか」だけ決めておく（例：卵2個と味噌汁）</li>
  </ul>

  <div class="part-label" style="margin-top:16px;">翌朝（D+1）</div>
  <ul class="checklist" style="margin-top:8px;">
    <li><div class="cb"></div>体重計に乗る（増えていてもOK。多くは水分の重さ。脂肪は2〜3日後に正確な値が出ます）</li>
    <li><div class="cb"></div>SECTION 1〜2の記録を書く（まだの場合）</li>
    <li><div class="cb"></div>朝食を「食べる順番ルール」で食べる（野菜orタンパク→最後に炭水化物）</li>
    <li><div class="cb"></div>水を500ml飲む（午前中）</li>
    <li><div class="cb"></div>いつも通りの1日を過ごす（特別なことは何もしなくてOK）</li>
  </ul>

  <div class="part-label" style="margin-top:16px;">翌々日（D+2）</div>
  <ul class="checklist" style="margin-top:8px;">
    <li><div class="cb"></div>昨日の食事は整えられたか確認 → NoならYes今日の昼食だけ整える</li>
    <li><div class="cb"></div>就寝時間を守れたか確認 → Noなら今夜だけ30分早く寝る</li>
    <li><div class="cb"></div>体が重ければ15分だけ歩く（運動ではなく気分転換として）</li>
    <li><div class="cb"></div>置き換えフードの在庫を確認・補充する</li>
  </ul>

  <div class="part-label" style="margin-top:16px;">72時間後（D+3）</div>
  <ul class="checklist" style="margin-top:8px;">
    <li><div class="cb"></div>SECTION 6の「崩れパターン分析」を記入する</li>
    <li><div class="cb"></div>設計の改善点を1つだけ決める（例：チョコを棚の奥に移動する）</li>
    <li><div class="cb"></div><strong>「戻れた」と自分に言う</strong></li>
    <li><div class="cb"></div>次の1週間を始める</li>
  </ul>
  <div class="footer">E判定逆転30日プログラム｜特典PDF② 崩れ復帰チェックシート　／　Longevity Navigator</div>
</div>

<!-- ══ P5 SECTION6〜7＋手紙 ══ -->
<div class="pb">
  <div class="sec-header"><h2>SECTION 6　崩れパターン分析</h2><p class="sub">繰り返し使用してください。5回分記録するとパターンが見えます。</p></div>
  <table>
    <thead><tr><th>#</th><th>日付</th><th>曜日</th><th>睡眠時間</th><th>ストレス度</th><th>主な原因</th><th>戻るまでの日数</th></tr></thead>
    <tbody>
      <tr><td style="color:#FF6D00;font-weight:700;">1</td><td></td><td></td><td></td><td>高 / 中 / 低</td><td></td><td></td></tr>
      <tr><td style="color:#FF6D00;font-weight:700;">2</td><td></td><td></td><td></td><td>高 / 中 / 低</td><td></td><td></td></tr>
      <tr><td style="color:#FF6D00;font-weight:700;">3</td><td></td><td></td><td></td><td>高 / 中 / 低</td><td></td><td></td></tr>
      <tr><td style="color:#FF6D00;font-weight:700;">4</td><td></td><td></td><td></td><td>高 / 中 / 低</td><td></td><td></td></tr>
      <tr><td style="color:#FF6D00;font-weight:700;">5</td><td></td><td></td><td></td><td>高 / 中 / 低</td><td></td><td></td></tr>
    </tbody>
  </table>
  <div class="review-q">5回分記録できたら書いてください</div>
  <div class="write-space">
    <p style="font-size:9pt;color:#6b7280;margin-bottom:6px;">崩れやすい曜日・時間帯：</p><div class="write-line"></div>
    <p style="font-size:9pt;color:#6b7280;margin:10px 0 6px;">崩れる前日・当日の共通点：</p><div class="write-line"></div>
    <p style="font-size:9pt;color:#6b7280;margin:10px 0 6px;">最速で戻れたときにやっていたこと：</p><div class="write-line"></div>
  </div>

  <div class="sec-header"><h2>SECTION 7　再スタートガイド</h2><p class="sub">1週間以上崩れ続けている場合</p></div>
  <div class="step">
    <div class="step-num">1</div>
    <div class="step-body"><h4>今日を「Day 1」に設定し直す</h4><p>これまでの崩れをすべてリセット。帳消し。ゼロからのスタートです。</p></div>
  </div>
  <div class="step">
    <div class="step-num">2</div>
    <div class="step-body"><h4>Week 1の「睡眠を整える」だけに戻る</h4><p>食事も運動も今週は全部手放す。就寝時間を固定することだけをやります。</p></div>
  </div>
  <div class="step">
    <div class="step-num">3</div>
    <div class="step-body"><h4>3日間だけ就寝時間を守る</h4><p>3日間続けられたら、食事の順番を再開する。それ以上は求めない。</p></div>
  </div>
  <div class="step">
    <div class="step-num">4</div>
    <div class="step-body"><h4>また崩れてもOK → またSTEP 1に戻るだけ</h4><p>このループに終わりはありません。何度でも戻ってきていいです。</p></div>
  </div>

  <div class="divider"></div>
  <p style="font-weight:700;margin-bottom:10px;">自分への手紙</p>
  <div class="letter-page">
    <p class="greeting">未来の自分から、今日の自分へ</p>
    <div class="letter-area">
      <div class="letter-line"></div><div class="letter-line"></div>
      <div class="letter-line"></div><div class="letter-line"></div>
      <div class="letter-line"></div><div class="letter-line"></div>
    </div>
    <p class="letter-sig">未来のあなたより</p>
  </div>
  <div class="footer">E判定逆転30日プログラム｜特典PDF② 崩れ復帰チェックシート　／　Longevity Navigator</div>
</div>

</body></html>"""


# ─────────────────────────────────────────
# PDF③ 30日記録シート
# ─────────────────────────────────────────
def make_day_card(day: int, week: int) -> str:
    return f"""
<div class="record-card">
  <div class="record-card-header">
    <span class="rc-day">Day {day}</span>
    <span class="rc-date">　　　月　　日（　　）　Week {week}</span>
  </div>
  <div class="rc-row">
    <div class="rc-label">就寝時間</div>
    <div class="rc-input"></div>
    <span style="font-size:9pt;color:#6b7280;margin:0 6px;">時</span>
    <div class="rc-input" style="max-width:40px;"></div>
    <span style="font-size:9pt;color:#6b7280;">分</span>
  </div>
  <div class="rc-row">
    <div class="rc-label">睡眠時間</div>
    <div class="rc-input" style="max-width:50px;"></div>
    <span style="font-size:9pt;color:#6b7280;margin-left:4px;">時間</span>
  </div>
  <div class="rc-row">
    <div class="rc-label">夜食</div>
    <div class="rc-options">
      <div class="rc-opt"><div class="rc-circle"></div>なし ◎</div>
      <div class="rc-opt"><div class="rc-circle"></div>置き換えた ○</div>
      <div class="rc-opt"><div class="rc-circle"></div>少し食べた △</div>
      <div class="rc-opt"><div class="rc-circle"></div>崩れた ×</div>
    </div>
  </div>
  <div class="rc-row">
    <div class="rc-label">食べる順番</div>
    <div class="rc-options">
      <div class="rc-opt"><div class="rc-circle"></div>意識した ◎</div>
      <div class="rc-opt"><div class="rc-circle"></div>だいたい ○</div>
      <div class="rc-opt"><div class="rc-circle"></div>できなかった ×</div>
    </div>
  </div>
  <div class="rc-row"><div class="rc-label">今日のひとこと</div><div class="rc-input"></div></div>
</div>"""


def make_week_review(week: int, days: str) -> str:
    colors = {1: "#FF6D00", 2: "#38bdf8", 3: "#22c55e", 4: "#a855f7"}
    c = colors.get(week, "#FF6D00")
    return f"""
<div class="review-card" style="border-color:{c};">
  <div class="review-card-title" style="color:{c};">Week {week} レビュー　（Day {days} 終了後）</div>
  <div class="grid2">
    <div>
      <div class="review-q">就寝時間を守れた日数</div>
      <div style="display:flex;align-items:center;gap:8px;margin:6px 0;">
        <div class="write-space" style="min-height:30px;width:50px;padding:6px;text-align:center;"></div>
        <span style="font-size:10pt;">日 / 7日</span>
      </div>
    </div>
    <div>
      <div class="review-q">夜食を食べなかった日数</div>
      <div style="display:flex;align-items:center;gap:8px;margin:6px 0;">
        <div class="write-space" style="min-height:30px;width:50px;padding:6px;text-align:center;"></div>
        <span style="font-size:10pt;">日 / 7日</span>
      </div>
    </div>
  </div>
  <div class="review-q">今週、一番うまくいったことは？</div>
  <div class="write-space"><div class="write-line"></div></div>
  <div class="review-q">今週、一番難しかったことは？</div>
  <div class="write-space"><div class="write-line"></div></div>
  <div class="review-q">来週、1つだけ変えるとしたら何ですか？</div>
  <div class="write-space"><div class="write-line"></div></div>
  <div class="review-q">今週の自分へのひとこと（10点満点で　　　点）</div>
  <div class="write-space"><div class="write-line"></div></div>
</div>"""


def html_pdf3():
    # Day cards: 4 per page
    pages_html = ""
    day = 1
    for week in range(1, 5):
        days_in_week = range(day, day + 7)
        # 2 pages of day cards per week (4 cards/page → actually we do 3-4 per page)
        week_cards = "".join(make_day_card(d, week) for d in days_in_week)
        pages_html += f"""
<div class="pb">
  <div class="sec-header-blue"><h2>Week {week}　Day {day}〜{day+6}</h2></div>
  {week_cards}
  <div class="footer">E判定逆転30日プログラム｜特典PDF③ 30日記録シート　／　Longevity Navigator</div>
</div>"""
        pages_html += f"""
<div class="pb">
  {make_week_review(week, f'{day}〜{day+6}')}
  <div class="footer">E判定逆転30日プログラム｜特典PDF③ 30日記録シート　／　Longevity Navigator</div>
</div>"""
        day += 7

    # Day 29-30
    pages_html += f"""
<div class="pb">
  <div class="sec-header-blue"><h2>最終週　Day 29・30</h2></div>
  {make_day_card(29, 5)}{make_day_card(30, 5)}
  <div class="footer">E判定逆転30日プログラム｜特典PDF③ 30日記録シート　／　Longevity Navigator</div>
</div>"""

    return f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8">
<style>{SHARED_CSS}</style>
</head><body>

<!-- ══ COVER ══ -->
<div class="cover">
  <span class="cover-badge">E判定逆転30日プログラム｜特典PDF ③</span>
  <div class="cover-num">TOKUTEN PDF 03</div>
  <h1 class="cover-title">30日<span>記録</span>シート</h1>
  <p class="cover-subtitle">毎晩30秒。データが貯まるほど<br>崩れにくくなる記録メソッド</p>
  <div class="cover-divider"></div>
  <div class="cover-stats">
    <div class="cover-stat"><div class="num">30</div><div class="label">日間記録</div></div>
    <div class="cover-stat"><div class="num">4</div><div class="label">週次レビュー</div></div>
    <div class="cover-stat"><div class="num">30</div><div class="label">秒/日</div></div>
  </div>
  <p class="cover-author">Longevity Navigator ／ <span>マーシー｜−32kg × サブ3</span></p>
</div>

<!-- ══ P2 開始前チェック ══ -->
<div class="pb">
  <div class="sec-header"><h2>記録の目的</h2></div>
  <div class="grid2">
    <div class="dark-box">
      <div class="label">目的 ①</div>
      <div class="value" style="font-size:13pt;">崩れパターンを発見する</div>
      <div class="desc">記録を続けると「睡眠が短い日の翌夜は必ず崩れる」などのパターンが見えます。パターンがわかれば先手で設計できます。</div>
    </div>
    <div class="dark-box">
      <div class="label">目的 ②</div>
      <div class="value" style="font-size:13pt;">意識する習慣をつくる</div>
      <div class="desc">毎晩30秒の記録行為が「今日の自分を観察する」習慣を作ります。記録することで翌日の行動が自然と変わります。</div>
    </div>
  </div>
  <div class="hl-orange"><strong>記録のルール：</strong>毎晩30秒。完璧じゃなくていい。空白が続いても戻ってきていい。途中で止まっても、また開けばいいだけです。</div>

  <div class="sec-header"><h2>開始前チェックシート　現在地の確認</h2><p class="sub">プログラム開始日に記入。30日後に見返します。</p></div>
  <div class="review-card">
    <div class="review-card-title">スタート時点の記録　　　　年　　月　　日</div>
    <div class="grid2">
      <div>
        <div class="review-q">体重（任意）</div>
        <div style="display:flex;align-items:center;gap:6px;margin:6px 0;">
          <div class="write-space" style="min-height:30px;width:70px;padding:6px;"></div>
          <span>kg</span>
        </div>
      </div>
      <div>
        <div class="review-q">腹囲（任意）</div>
        <div style="display:flex;align-items:center;gap:6px;margin:6px 0;">
          <div class="write-space" style="min-height:30px;width:70px;padding:6px;"></div>
          <span>cm</span>
        </div>
      </div>
    </div>
    <div class="review-q">現在、夜食を食べている頻度</div>
    <div class="rc-options" style="margin:8px 0;">
      <div class="rc-opt"><div class="rc-circle"></div>ほぼ毎日</div>
      <div class="rc-opt"><div class="rc-circle"></div>週4〜5日</div>
      <div class="rc-opt"><div class="rc-circle"></div>週2〜3日</div>
      <div class="rc-opt"><div class="rc-circle"></div>たまに</div>
    </div>
    <div class="review-q">現在の平均就寝時間</div>
    <div style="display:flex;align-items:center;gap:6px;margin:6px 0;">
      <div class="write-space" style="min-height:30px;width:50px;padding:6px;"></div>
      <span>時頃</span>
      <span style="margin-left:16px;">睡眠時間：</span>
      <div class="write-space" style="min-height:30px;width:50px;padding:6px;"></div>
      <span>時間</span>
    </div>
    <div class="review-q">今、一番やめたい夜の習慣は？</div>
    <div class="write-space"><div class="write-line"></div></div>
    <div class="review-q">30日後、どんな自分になっていたいですか？</div>
    <div class="write-space"><div class="write-line"></div><div class="write-line"></div></div>
  </div>
  <div class="footer">E判定逆転30日プログラム｜特典PDF③ 30日記録シート　／　Longevity Navigator</div>
</div>

{pages_html}

<!-- ══ 崩れパターン集計 ══ -->
<div class="pb">
  <div class="sec-header"><h2>崩れパターン集計表</h2><p class="sub">崩れた日の記録を一覧にすることで、自分だけのパターンを発見します</p></div>
  <table>
    <thead><tr><th>#</th><th>日付</th><th>曜日</th><th>時間帯</th><th>睡眠時間</th><th>ストレス</th><th>主な原因</th><th>復帰日数</th></tr></thead>
    <tbody>
      {"".join(f'<tr><td style="color:#FF6D00;font-weight:700;">{i}</td><td></td><td></td><td></td><td></td><td>高/中/低</td><td></td><td></td></tr>' for i in range(1,9))}
    </tbody>
  </table>
  <div class="review-card" style="margin-top:16px;">
    <div class="review-card-title">パターン分析</div>
    <div class="review-q">崩れやすい曜日・時間帯</div>
    <div class="write-space"><div class="write-line"></div></div>
    <div class="review-q">崩れる前の共通点（睡眠不足・ストレス・外食など）</div>
    <div class="write-space"><div class="write-line"></div></div>
    <div class="review-q">最速で戻れたときにやっていたこと</div>
    <div class="write-space"><div class="write-line"></div></div>
    <div class="review-q">次の30日で改善する「設計の1点」</div>
    <div class="write-space"><div class="write-line"></div></div>
  </div>
  <div class="footer">E判定逆転30日プログラム｜特典PDF③ 30日記録シート　／　Longevity Navigator</div>
</div>

<!-- ══ 30日後の振り返り ══ -->
<div class="pb">
  <div class="sec-header"><h2>30日後の振り返りシート</h2></div>
  <div class="review-card">
    <div class="review-card-title">ゴール時点の記録　　　　年　　月　　日</div>
    <div class="grid2">
      <div>
        <div class="review-q">体重（任意）</div>
        <div style="display:flex;align-items:center;gap:6px;margin:6px 0;">
          <div class="write-space" style="min-height:30px;width:60px;padding:6px;"></div>
          <span>kg（開始時比</span>
          <div class="write-space" style="min-height:30px;width:50px;padding:6px;"></div>
          <span>kg）</span>
        </div>
      </div>
      <div>
        <div class="review-q">腹囲（任意）</div>
        <div style="display:flex;align-items:center;gap:6px;margin:6px 0;">
          <div class="write-space" style="min-height:30px;width:60px;padding:6px;"></div>
          <span>cm（開始時比</span>
          <div class="write-space" style="min-height:30px;width:50px;padding:6px;"></div>
          <span>cm）</span>
        </div>
      </div>
    </div>
    <div class="review-q">夜食を食べた日数（30日合計）</div>
    <div style="display:flex;align-items:center;gap:6px;margin:6px 0;">
      <div class="write-space" style="min-height:30px;width:50px;padding:6px;"></div>
      <span>日 / 30日</span>
    </div>
    <div class="review-q">30日前と比べて、変わったと感じることを3つ</div>
    <div class="write-space">
      <p style="font-size:9pt;color:#6b7280;">①</p><div class="write-line"></div>
      <p style="font-size:9pt;color:#6b7280;margin-top:8px;">②</p><div class="write-line"></div>
      <p style="font-size:9pt;color:#6b7280;margin-top:8px;">③</p><div class="write-line"></div>
    </div>
    <div class="review-q">30日間で一番つらかったのはいつですか？そのときどう乗り越えましたか？</div>
    <div class="write-space"><div class="write-line"></div><div class="write-line"></div></div>
    <div class="review-q">30日前の自分に声をかけるとしたら？</div>
    <div class="write-space"><div class="write-line"></div><div class="write-line"></div></div>
    <div class="review-q">30日後の自分を10点満点で評価してください（　　　点）　その理由：</div>
    <div class="write-space"><div class="write-line"></div></div>
  </div>
  <div class="footer">E判定逆転30日プログラム｜特典PDF③ 30日記録シート　／　Longevity Navigator</div>
</div>

<!-- ══ 次の30日＋マーシーより ══ -->
<div class="pb">
  <div class="sec-header"><h2>次の30日への設計改善シート</h2><p class="sub">30日のデータをもとに、次の30日の設計を更新します</p></div>
  <div class="review-card">
    <div class="review-q">続けること（うまくいっていたこと）</div>
    <div class="write-space">
      <p style="font-size:9pt;color:#6b7280;">① </p><div class="write-line"></div>
      <p style="font-size:9pt;color:#6b7280;margin-top:8px;">② </p><div class="write-line"></div>
    </div>
    <div class="review-q">やめること（効果がなかった・続けられなかったこと）</div>
    <div class="write-space">
      <p style="font-size:9pt;color:#6b7280;">① </p><div class="write-line"></div>
      <p style="font-size:9pt;color:#6b7280;margin-top:8px;">② </p><div class="write-line"></div>
    </div>
    <div class="review-q">次の30日で新たに試すこと（1つだけ）</div>
    <div class="write-space"><div class="write-line"></div></div>
    <div class="review-q">次の30日の目標（数字ではなく「行動」で設定）</div>
    <div class="write-space"><div class="write-line"></div><div class="write-line"></div></div>
  </div>

  <div class="maercy" style="margin-top:20px;">
    <p>30日間、記録してくれてありがとうございます。<br><br>
    完璧じゃなくてよかった。空白のページがあってよかった。崩れた記録があってよかった。<br>
    そのすべてが、あなただけのデータです。<br><br>
    このシートの記録は、証拠です。30日間、あなたが本気で向き合った証拠。<br><br>
    次の30日も、またこのシートを使ってください。2冊目を開くとき、1冊目を見返してみてください。きっと気づきます。<strong style="color:#FF6D00;">「あの頃より、少しだけ変わってる」</strong>と。<br><br>
    それが、すべてです。</p>
  </div>
  <div class="footer">E判定逆転30日プログラム｜特典PDF③ 30日記録シート　／　Longevity Navigator</div>
</div>

</body></html>"""


# ─────────────────────────────────────────
# PDF生成メイン
# ─────────────────────────────────────────
async def create_pdf(html: str, output_path: Path, label: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html, wait_until="networkidle", timeout=60000)
        await page.pdf(
            path=str(output_path),
            format="A4",
            print_background=True,
            margin={"top": "14mm", "bottom": "16mm", "left": "18mm", "right": "18mm"},
        )
        await browser.close()
    print(f"✅ {label} → {output_path}")


async def main():
    print("📄 特典PDF生成開始...")
    tasks = [
        create_pdf(html_pdf1(), OUTPUT_DIR / "tokuten_01_yashoku_taisaku.pdf",    "PDF① 夜食対策表"),
        create_pdf(html_pdf2(), OUTPUT_DIR / "tokuten_02_kuzure_fukki.pdf",        "PDF② 崩れ復帰チェックシート"),
        create_pdf(html_pdf3(), OUTPUT_DIR / "tokuten_03_30nichi_kiroku.pdf",      "PDF③ 30日記録シート"),
    ]
    for t in tasks:
        await t
    print(f"\n🎉 全3本の特典PDFを生成しました")
    print(f"📁 出力先: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
