# Longevity Navigator｜Podcast台本 → note公開セット一括生成

このコマンドは、ポッドキャスト台本テキスト1本から
**note公開に必要な全素材を一括で自動生成**します。

## 生成物一覧

| # | 成果物 | 用途 |
|---|---|---|
| 0 | 記事目次（構成設計） | 記事の骨格。感情導線の設計図 |
| 1 | note記事全文（約5000字） | noteに貼り付けて公開 |
| 2 | サムネイルプロンプト | Nano Banana Proに入力 |
| 3 | 図解プロンプト＋挿入位置マップ | Nano Banana Proに入力 |
| 4 | noteタグ提案 | note投稿設定で使用 |

---

## ブランド設定（全生成物に一貫して適用）

```
著者：マーシー
実績：100kg → 68kg（-32kg）、サブ3ランナー、健診E判定 → 基準値クリア
コアメッセージ：意志力ではなく仕組みで変わる

ペルソナ：田中 健二（42歳）
  - 管理職・年収650万・妻と子2人
  - 健診E判定が3年連続。E判定を家族に見せずに捨てたことがある
  - 夜食・間食がやめられない。「また崩れた…」の自己嫌悪ループ
  - 「俺だけじゃない」と諦めかけている。でも本当は変わりたい
  - スマホで「健診 Eランク」を検索してこの記事に辿り着いた
  - 「また綺麗事を言うんでしょ」と最初は冷めている

ペルソナが動く3つのトリガー：
  ① この人、俺より酷い状況だったのに変われた（希望）
  ② 具体的な方法が書いてある（再現性）
  ③ 数字が出てる（信頼）

ブランドカラー：
  背景     #000000（黒）
  オレンジ #FF6D00（強調・CTA）
  水色     #38bdf8（科学・データ）
  緑       #4ade80（効果・ポジティブ）
  白       #FFFFFF（メインテキスト）

フォント：Noto Sans JP Black（太いゴシック体）
テイスト：Appleのミニマリズム。黒背景。余白重視。
```

---

## 実行手順

台本テキストが貼り付けられたら、以下を**この順番で**実行する。

---

### STEP 1：台本を分析する + 前回記事を特定する（出力しない・内部処理）

**1-A. 台本から以下の要素を抽出・整理する。**

```
抽出リスト：
  - テーマ（1行で）
  - ペルソナが「これ自分だ」と感じる感情フック（台本内から抜き出す）
  - コアメッセージ（1行）
  - 主要ポイント（3〜6個・箇条書き）
  - 科学的根拠（論文名・著者・掲載誌・データがあれば）
  - 実体験エピソード（マーシー自身の話）
  - 崩れた時の復帰方法（台本に含まれる場合）
  - 記事カテゴリ：睡眠 / 食事 / 運動 / 習慣化 / ニュース
  - 今回の回数（N回目）
```

**1-B. 前回の記事を自動特定する（記事フッターに使用）**

以下の手順で前回記事の情報を取得する：

1. `C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note\` 内の `第*回_*` フォルダを一覧取得（Glob tool使用）
2. 回数が「今回のN-1」に該当するフォルダを特定
3. そのフォルダ内の本文mdファイルのタイトル行（`# `で始まる行）を読み取る
4. 記事カテゴリ（睡眠 / 食事 / 運動 / 習慣化 / ニュース）を判定して「〇〇編」とする
5. 取得した `前回のタイトル` と `前回のテーマ編` を SECTION 1 フッターに埋め込む

この分析結果は出力せず、STEP 2〜5の生成に使う。

---

### STEP 2：記事目次を設計する（SECTION 0として出力）

**【目次設計の最重要原則】**

ペルソナ（田中 健二・42歳）は記事の冒頭で「どうせまた綺麗事だろ」と思っている。
最初の数行で「この人は俺のことを分かっている」と感じさせなければ、読み続けてもらえない。
だから目次は、**感情の流れ**を設計するものだと考える。

```
感情の流れ設計図（全記事共通の骨格）：

フェーズ1「共感」
  → 読者が「これ自分だ」と思う場面から始める
  → 状況説明ではなく、感情の描写から入る
  → 例：「また今日も…」という罪悪感、空袋を見る自己嫌悪

フェーズ2「問題の正体」
  → 「意志が弱いからじゃない」と解放する
  → 科学的な原因を中学生でも分かる言葉で説明
  → 読者が「そういうことか」と膝を打つ

フェーズ3「結論を先に見せる」
  → 全体の答えを早めに提示（結論ファースト）
  → 「3ステップで変わる」など、ゴールが見える安心感
  → 読者が「続きを読めば分かる」と思える

フェーズ4「実践手順」
  → 各ステップを1つずつ、具体的に
  → 禁止ではなく追加・置き換え・固定
  → 完璧でなくていい、1つだけでいい

フェーズ5「崩れた時の戻り方」
  → 必ず入れる。これが他記事との最大差別化
  → 「8勝6敗でOK」の思想
  → 自己嫌悪を切り、翌朝の行動に変換する

フェーズ6「まとめ＋今日1つの実践」
  → 3点に絞って整理
  → 「全部じゃなくて1つだけ」でOKとする
  → CTAで次の記事・Podcastへ誘導
```

**出力フォーマット：**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 SECTION 0｜記事目次（構成設計）
━━━━━━━━━━━━━━━━━━━━━━━━━━

【タイトル案（3案）】
案A：[数字＋感情語＋意外性の型]
案B：[読者に直接語りかける型]
案C：[結果を先に見せる型]
推奨：[どれかを推奨し理由を1行で]

【記事目次】

## 1. [感情フックの見出し]
　→ 設計意図：[ペルソナのどの感情に刺さるか1行で]

## 2. [問題の正体を暴く見出し]
　→ 設計意図：[なぜここでこの話をするか]

## 3. [結論・全体像の見出し]
　→ 設計意図：[読者にどんな安心感を与えるか]

## 4. [科学的根拠の見出し]
　→ 設計意図：[信頼性をどう担保するか]

## 5. [ステップ1の見出し]
　→ 設計意図：[最初の行動を何にするか・なぜそれか]

## 6. [ステップ2の見出し]
　→ 設計意図：

## 7. [ステップ3の見出し]（あれば）
　→ 設計意図：

## 8. [崩れた日の戻り方]
　→ 設計意図：[自己嫌悪をどう切り替えるか]

## 9. まとめ＋今日からの実践3つ
　→ 設計意図：読者が「これだけやれば大丈夫」と感じる締め

【感情導線の確認チェック】
- [ ] 冒頭が「状況説明」ではなく「感情」から始まっているか
- [ ] 「意志が弱い」ではなく「仕組みの問題」に転換されているか
- [ ] 崩れた時の復帰手順が入っているか
- [ ] CTAが末尾にあるか（過去記事 or Podcast）
```

---

### STEP 3：note記事全文を生成する（SECTION 1として出力）

STEP 2で設計した目次の構成・感情導線に従い、約5000字の記事本文を生成する。

**【記事執筆の品質基準】**

```
文体・トーン：
  - 中学生でも分かる言葉で書く（専門用語は必ず解説する）
  - 断定的・命令調は避ける（「〜です」「〜します」）
  - 体験談は一人称（「私も」「僕も」）で書く
  - 共感ワード：「また今日も」「どうせ」「わかっていても」「なのに」

感情描写のルール：
  - 「before→after」より先に「感情の変化」を書く
    ❌「体重100kg→70kgになりました」
    ⭕「100kgだった頃、鏡を見るのが怖かった。今は毎朝楽しみになった」
  - ペルソナの「裏の感情」に触れる
    恐怖・悔しさ・諦め・疑心・期待・嫉妬 のいずれか

マーシーの実体験ルール：
  - 各ステップに必ず実体験エピソードを入れる
  - 数字を使う（「400円が150円になった」「11時の空腹が12時半まで持つ」）
  - 失敗談も入れる（「私も全部失敗しました」）

科学的根拠のルール：
  - 必ず1つ以上の具体的な出典を明記する
    ❌「ある研究によると」
    ⭕「2011年、イスラエルの研究チーム（Danziger et al., PNAS掲載）によれば」
  - 出典は末尾にまとめて記載する

構成のルール：
  - 崩れた時の復帰手順セクションを必ず入れる
  - 「8勝6敗でOK」の思想を必ず伝える
  - CTAには過去記事リンクと次回予告を入れる
  - 末尾に免責事項を入れる

禁止事項：
  - 「〜しなければなりません」「〜すべきです」（上から目線NG）
  - 「簡単です」「誰でもできます」（軽率な約束NG）
  - 根拠のない断言（「必ず痩せます」等）
```

**出力フォーマット：**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 SECTION 1｜note記事全文（約5000字）
━━━━━━━━━━━━━━━━━━━━━━━━━━

# [タイトル]

## 1. [見出し]

[本文...]

---

（各セクションを目次の構成通りに展開）

---

【出典】
- [論文1]
- [論文2]

---

▼ 前回の記事（[前回のテーマ編]）
「[前回のタイトル]」

▼ Podcastで"聴く"バージョン
🎙️ 日本を元気にする健康習慣ラジオ ― E判定からの逆転 ―

マーシー｜-30kg×サブ3｜健診Eメタボ脱出
100kg→68kgを8年間維持中 | サブ3ランナー | 30〜40代メタボ逆転を仕組みで支援

📝 note：https://note.com/mash_anti_metabo
🎙️ Podcast：https://stand.fm/channels/6965ee968d01e8272cb34e15
🐦 X（Twitter）：@MASH_Remotion18

---

【免責事項】
この記事は個人の体験に基づく情報共有です。
医療行為・診断・治療を目的としたものではありません。
健康状態に不安がある方は医師にご相談ください。
```

---

### STEP 4：サムネイル生成スクリプトを出力する（SECTION 2として出力）

STEP 2で決定したタイトルと感情フックを元に、**HTML/CSS + Playwright** 方式の `generate_thumbnail.py` を生成する。
棒人間などのSVGイラストは使わない。テキストを主役にしたミニマルデザイン。

**サムネイルの設計原則：**
- 背景は必ず黒（#000000）
- 左上にオレンジのアクセントバー（幅72px・高さ6px・#FF6D00）
- テキスト3〜4行構成：line1・line2（白 #FFFFFF・86px）、line3（オレンジ #FF6D00・96px）、sub（グレー #666666・36px）
- 左寄せ。余白重視のAppleミニマル
- 著者情報は左下に小さく（マーシー｜100kg→68kg｜Sub3）
- シリーズ番号は右下に大きく（①②③… の丸数字）
- SVGイラスト・棒人間・装飾図形は一切入れない

**変数として記事ごとに変えるもの：**
- `LINE1`：1行目テキスト（最大10文字程度）
- `LINE2`：2行目テキスト（最大10文字程度）
- `LINE3`：3行目テキスト・オレンジ色（最大10文字程度）
- `SUB`：サブテキスト（最大20文字程度・なければ空文字）
- `NUM`：シリーズ番号の丸数字（⑨⑩など）
- `OUTPUT_FNAME`：出力ファイル名（例：`サムネイル_第9回.png`）

**出力フォーマット：**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
📸 SECTION 2｜generate_thumbnail.py
━━━━━━━━━━━━━━━━━━━━━━━━━━

[以下のテンプレートにこの回の内容を当てはめて、完全なPythonスクリプトを出力する]
```

**テンプレート（各回の内容を埋めて完全なスクリプトとして出力すること）：**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第N回 サムネイル高品質生成スクリプト
HTML/CSS + Playwright（Chromiumヘッドレス）版
サイズ: 1280×670px
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images"
OUTPUT_DIR.mkdir(exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

LINE1        = "[1行目テキスト]"
LINE2        = "[2行目テキスト]"
LINE3        = "[3行目テキスト（オレンジ）]"
SUB          = "[サブテキスト（不要なら空文字）]"
NUM          = "[丸数字]"
OUTPUT_FNAME = "サムネイル_第N回.png"

THUMBNAIL_HTML = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@font-face {{
  font-family: 'NotoSansJP';
  src: url('{FONT}');
  font-weight: 100 900;
}}
* {{ margin:0; padding:0; box-sizing:border-box;
     -webkit-font-smoothing:antialiased; }}
body {{
  width:1280px; height:670px; overflow:hidden;
  background:#000000; position:relative;
  font-family:'NotoSansJP','Meiryo',sans-serif;
}}
.accent {{
  position:absolute;
  left:80px; top:72px;
  width:72px; height:6px;
  background:#FF6D00;
  border-radius:3px;
  box-shadow:0 0 18px rgba(255,109,0,.7);
}}
.copy {{
  position:absolute;
  left:80px; top:108px;
}}
.line1 {{
  display:block;
  font-size:86px; font-weight:900;
  color:#FFFFFF; line-height:1.18;
  letter-spacing:-2px;
}}
.line2 {{
  display:block;
  font-size:86px; font-weight:900;
  color:#FFFFFF; line-height:1.18;
  letter-spacing:-2px;
}}
.line3 {{
  display:block;
  font-size:96px; font-weight:900;
  color:#FF6D00; line-height:1.2;
  margin-top:14px; letter-spacing:-2px;
  text-shadow:
    0 0 50px rgba(255,109,0,.6),
    0 0 100px rgba(255,109,0,.28),
    0 0 160px rgba(255,109,0,.12);
}}
.sub {{
  display:block;
  font-size:36px; font-weight:500;
  color:#666666; line-height:1.4;
  margin-top:20px; letter-spacing:.5px;
}}
.author {{
  position:absolute;
  bottom:26px; left:80px;
  font-size:22px; font-weight:400;
  color:#555555; letter-spacing:.3px;
}}
.num {{
  position:absolute;
  bottom:16px; right:60px;
  font-size:80px; font-weight:900;
  color:#FF6D00;
  text-shadow:0 0 30px rgba(255,109,0,.45);
}}
</style></head><body>

<div class="accent"></div>

<div class="copy">
  <span class="line1">{{LINE1}}</span>
  <span class="line2">{{LINE2}}</span>
  <span class="line3">{{LINE3}}</span>
  {{% if SUB %}}<span class="sub">{{SUB}}</span>{{% endif %}}
</div>

<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="num">{{NUM}}</p>

</body></html>"""

if __name__ == "__main__":
    print(f"第N回 サムネイル生成開始 (HTML/CSS + Playwright)...\n")

    out = OUTPUT_DIR / OUTPUT_FNAME
    tmp = ARTICLE_DIR / "_tmp_thumb.html"

    tmp.write_text(THUMBNAIL_HTML, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page    = browser.new_page(viewport={{"width": 1280, "height": 670}})
        page.goto(f"file:///{tmp.as_posix()}")
        page.wait_for_timeout(900)
        page.screenshot(path=str(out), full_page=False)
        browser.close()

    tmp.unlink(missing_ok=True)

    print(f"✅ {OUTPUT_FNAME}")
    print(f"保存先: {out}")
```

注意：テンプレート内の `{LINE1}` 等はPythonのf-string変数として実際の文字列に置き換えること。`{% if SUB %}` 部分はSUBが空の場合はそのタグごと削除すること。

---

### STEP 5：図解プロンプト＋挿入位置マップを生成する（SECTION 3として出力）

STEP 3で生成した記事の構成に沿って、5〜6枚の図解を設計する。

**図解の種類と使い分け：**

| 種類 | 用途 | 背景色 |
|---|---|---|
| 全体像カード型 | ステップ・手順の全体像 | ダークネイビー #1A2A3A |
| Before/After型 | 変化・改善の比較 | 上下2分割 |
| フロー図型 | 手順・順番の可視化 | ダークネイビー #1A2A3A |
| メカニズム図型 | 科学的仕組みの説明 | 時間軸グラデーション |
| 比較表型 | NG例 vs OK例 | 左赤（#FF1744） 右水色 |
| 復帰フロー型 | 崩れた時の戻り方 | 暗→明グラデーション |

**設計ルール：**
- 記事の感情導線に沿って挿入位置を決める
- 1枚で「このセクションの要点が分かる」内容にする
- テキストは短く・大きく・明確に

**出力フォーマット：**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
🗺️ SECTION 3｜図解挿入位置マップ＋プロンプト
━━━━━━━━━━━━━━━━━━━━━━━━━━
サイズ：1280×720px

【挿入位置マップ】
| 図解 | 挿入位置（セクション名） | 種類 | 役割 |
|---|---|---|---|
...

---
### 図解① [タイトル]
【挿入位置】[セクション名]の[前/後/中]

[プロンプト本文]
---
```

各プロンプト本文の必須要素：
- 「日本語インフォグラフィック画像を作成してください。」で始める
- 「日本語テキストを正確に表示すること。」で終える
- 背景色・テキストカラー（16進数）
- レイアウト構造（カード横並び・上下2段・フロー図など）

---

### STEP 6：noteタグを提案する（SECTION 4として出力）

```
固定タグ（毎回必ず含める3個）：
  #ダイエット　#メタボ　#習慣化

カテゴリ別追加タグ（2〜3個選択）：
  睡眠系：     #睡眠　#睡眠不足　#不眠
  食事系：     #食事管理　#健康診断　#血糖値
  運動系：     #運動習慣　#筋トレ　#ウォーキング
  朝食・間食：  #食事管理　#間食　#朝食
  ニュース系：  #最新研究　#栄養学　#健康科学
  全体習慣系：  #健康診断　#健康習慣　#ライフスタイル
```

**出力フォーマット：**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️ SECTION 4｜noteタグ提案
━━━━━━━━━━━━━━━━━━━━━━━━━━

#ダイエット #メタボ #習慣化 #[追加タグ] #[追加タグ] #[追加タグ]

選定理由：[1〜2行で説明]
```

---

### STEP 6.5：X投稿スレッド10本 + カード画像スクリプトを生成する（SECTION 5として出力）

STEP 3で生成した記事の内容を元に、X（Twitter）投稿スレッド10本と、各投稿に対応するカード画像生成スクリプトを生成する。

**X投稿スレッドの設計原則：**

| 番号 | 役割 | アクセントカラー | 内容 |
|---|---|---|---|
| 1 | 共感フック | 水色 #38bdf8 | ペルソナの「これ自分だ」感情から始める |
| 2 | 原因 | 水色 #38bdf8 | 問題の正体（意志ではなく仕組み） |
| 3 | 解決策 | オレンジ #FF6D00 | 記事のコアメッセージ |
| 4 | 仕組み | 水色 #38bdf8 | 科学的・実践的な根拠 |
| 5 | 効果 | 緑 #4ade80 | 見た目・数値への効果 |
| 6 | 設計 | 水色 #38bdf8 | 続ける仕組みの具体設計 |
| 7 | 実践 | オレンジ #FF6D00 | 具体的な行動プロトコル |
| 8 | 復帰 | 緑 #4ade80 | 崩れた日の戻り方 |
| 9 | 深掘り | 水色 #38bdf8 | 記事テーマに関連した追加知識 |
| 10 | CTA | オレンジ #FF6D00 | 今夜やること1つ＋noteリンク |

**各投稿のルール：**
- 140文字以内（スレッドなので改行含む）
- 末尾に「↓続き（N+1/10）」または「noteで詳細👇 https://note.com/mash_anti_metabo」
- 断定調より体験談・問いかけで共感を先に取る

**カード画像の設計原則：**
- サイズ：1280×720px
- 左上：タグピル（役割名・アクセントカラー背景・黒テキスト）
- 右上：N/10（投稿番号）
- メインテキスト3行：msg1・msg2（白 #FFFFFF・76px）、orange（オレンジ #FF6D00・62px）
- サブテキスト：28px・グレー #555555
- 左下：マーシー｜100kg→68kg｜Sub3
- 右下：#第N回 [テーマ]（アクセントカラー）

**出力フォーマット：**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
🐦 SECTION 5｜X投稿スレッド10本 + generate_x_cards.py
━━━━━━━━━━━━━━━━━━━━━━━━━━

【X投稿スレッド】

投稿1/10｜[タグ]
```
[140文字以内のツイート本文]
```

投稿2/10｜[タグ]
```
[140文字以内のツイート本文]
```

...（10本分）

---

【generate_x_cards.py】
[以下のテンプレートに各回の内容を当てはめた、完全なPythonスクリプト]
```

**generate_x_cards.py テンプレート：**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第N回 X投稿用カード画像 10枚生成スクリプト"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

HASHTAG = "#第N回 [テーマ]"

X_POSTS = [
    {"idx":1,  "accent":"#38bdf8", "tag":"共感",       "msg1":"[1行目]", "msg2":"[2行目]", "orange":"[オレンジ行]", "sub":"[サブ]",
     "tweet":"[ツイート本文1]"},
    {"idx":2,  "accent":"#38bdf8", "tag":"原因",       "msg1":"[1行目]", "msg2":"[2行目]", "orange":"[オレンジ行]", "sub":"[サブ]",
     "tweet":"[ツイート本文2]"},
    {"idx":3,  "accent":"#FF6D00", "tag":"解決策",     "msg1":"[1行目]", "msg2":"[2行目]", "orange":"[オレンジ行]", "sub":"[サブ]",
     "tweet":"[ツイート本文3]"},
    {"idx":4,  "accent":"#38bdf8", "tag":"仕組み",     "msg1":"[1行目]", "msg2":"[2行目]", "orange":"[オレンジ行]", "sub":"[サブ]",
     "tweet":"[ツイート本文4]"},
    {"idx":5,  "accent":"#4ade80", "tag":"効果",       "msg1":"[1行目]", "msg2":"[2行目]", "orange":"[オレンジ行]", "sub":"[サブ]",
     "tweet":"[ツイート本文5]"},
    {"idx":6,  "accent":"#38bdf8", "tag":"設計",       "msg1":"[1行目]", "msg2":"[2行目]", "orange":"[オレンジ行]", "sub":"[サブ]",
     "tweet":"[ツイート本文6]"},
    {"idx":7,  "accent":"#FF6D00", "tag":"実践",       "msg1":"[1行目]", "msg2":"[2行目]", "orange":"[オレンジ行]", "sub":"[サブ]",
     "tweet":"[ツイート本文7]"},
    {"idx":8,  "accent":"#4ade80", "tag":"復帰",       "msg1":"[1行目]", "msg2":"[2行目]", "orange":"[オレンジ行]", "sub":"[サブ]",
     "tweet":"[ツイート本文8]"},
    {"idx":9,  "accent":"#38bdf8", "tag":"深掘り",     "msg1":"[1行目]", "msg2":"[2行目]", "orange":"[オレンジ行]", "sub":"[サブ]",
     "tweet":"[ツイート本文9]"},
    {"idx":10, "accent":"#FF6D00", "tag":"今夜やること","msg1":"[1行目]", "msg2":"[2行目]", "orange":"[オレンジ行]", "sub":"[サブ]",
     "tweet":"[ツイート本文10]"},
]

def make_card_html(card: dict) -> str:
    accent = card["accent"]
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@font-face {{font-family:'NotoSansJP';src:url('{FONT}');font-weight:100 900;}}
*{{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}}
body{{width:1280px;height:720px;overflow:hidden;background:#000000;position:relative;
  font-family:'NotoSansJP','Meiryo',sans-serif;}}
.tag{{position:absolute;left:72px;top:56px;background:{accent};color:#000000;
  font-size:26px;font-weight:800;padding:6px 22px;border-radius:22px;letter-spacing:1px;}}
.num{{position:absolute;top:62px;right:72px;font-size:26px;font-weight:700;color:#333333;}}
.copy{{position:absolute;left:72px;top:146px;}}
.msg1{{display:block;font-size:76px;font-weight:900;color:#FFFFFF;line-height:1.2;letter-spacing:-2px;}}
.msg2{{display:block;font-size:76px;font-weight:900;color:#FFFFFF;line-height:1.2;letter-spacing:-2px;}}
.orange{{display:block;font-size:62px;font-weight:900;color:#FF6D00;line-height:1.3;margin-top:14px;
  letter-spacing:-1px;text-shadow:0 0 40px rgba(255,109,0,.55),0 0 80px rgba(255,109,0,.22);}}
.sub{{display:block;font-size:28px;font-weight:400;color:#555555;line-height:1.5;margin-top:18px;letter-spacing:.3px;}}
.author{{position:absolute;bottom:28px;left:72px;font-size:20px;font-weight:400;color:#404040;}}
.series{{position:absolute;bottom:28px;right:72px;font-size:20px;font-weight:700;color:{accent};}}
</style></head><body>
<div class="tag">{card['tag']}</div>
<div class="num">{card['idx']}/10</div>
<div class="copy">
  <span class="msg1">{card['msg1']}</span>
  <span class="msg2">{card['msg2']}</span>
  <span class="orange">{card['orange']}</span>
  <span class="sub">{card['sub']}</span>
</div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="series">{HASHTAG}</p>
</body></html>"""

def save_tweets(posts):
    out = OUTPUT_DIR / "x_posts.md"
    lines = ["# 第N回 X投稿スレッド（10本）\n\n"]
    for p in posts:
        lines += [f"## 投稿{p['idx']}/10｜{p['tag']}\n\n```\n{p['tweet'].strip()}\n```\n\n"]
        lines += [f"![カード{p['idx']}](x_post_{p['idx']:02d}.png)\n\n---\n\n"]
    out.write_text("".join(lines), encoding="utf-8")
    print(f"✅ X投稿テキスト保存: {out.name}")

if __name__ == "__main__":
    print("第N回 X投稿カード画像 生成開始...\n")
    tmp = ARTICLE_DIR / "_tmp_xcard.html"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for card in X_POSTS:
            html  = make_card_html(card)
            fname = f"x_post_{card['idx']:02d}.png"
            out   = OUTPUT_DIR / fname
            tmp.write_text(html, encoding="utf-8")
            page = browser.new_page(viewport={"width":1280,"height":720})
            page.goto(f"file:///{tmp.as_posix()}")
            page.wait_for_timeout(600)
            page.screenshot(path=str(out), full_page=False)
            page.close()
            print(f"✅ {fname}  [{card['tag']}]")
        browser.close()
    tmp.unlink(missing_ok=True)
    save_tweets(X_POSTS)
    print(f"\n全10枚完了。保存先: {OUTPUT_DIR}")
```

注意：テンプレート内の `[1行目]` 等は記事内容に合わせた実際のテキストに置き換えること。`HASHTAG` は `#第N回 [テーマ]` 形式で設定すること。

---

### STEP 7：ファイル保存と一覧出力

全SECTIONの出力が完了したら、以下の手順でファイルに保存し、一覧を表示する。

**7-1. フォルダ名の生成**

SECTION 0で推奨したタイトル案から、フォルダ名を生成する：
- 形式：`第N回_[タイトルの要約（30文字以内）]`
- 例：`第6回_運動ゼロの40代がトイレで1回だけで変わった科学的理由`

**7-2. フォルダ作成**

```bash
mkdir -p "第N回_[フォルダ名]"
```

**7-3. 各ファイルの保存**

以下のファイルをWrite toolで保存する：

| # | ファイル名 | 内容 |
|---|---|---|
| 1 | 第N回_記事目次.md | SECTION 0の内容 |
| 2 | 第N回_[タイトル].md | SECTION 1の内容（本文） |
| 3 | generate_thumbnail.py | SECTION 2の内容（実行可能なPythonスクリプト） |
| 4 | 第N回_図解プロンプト.md | SECTION 3の内容 |
| 5 | 第N回_noteタグ.md | SECTION 4の内容 |
| 6 | generate_x_cards.py | SECTION 5の内容（X投稿カード10枚生成スクリプト） |

**7-4. 保存完了の報告**

ファイル保存が完了したら、以下の形式で一覧を出力する：

```
完了しました！

以下のフォルダに全ファイルを保存しました：

**📁 第N回_[フォルダ名]**

```
C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note\第N回_[フォルダ名]\
```

## 保存ファイル一覧

| # | ファイル名 | 内容 |
|---|---|---|
| 1 | 第N回_記事目次.md | 記事の構成設計・感情導線の設計図 |
| 2 | 第N回_[タイトル].md | note記事本文（約5,000字） |
| 3 | generate_thumbnail.py | サムネイル生成スクリプト（python3 -X utf8 generate_thumbnail.py で実行） |
| 4 | 第N回_図解プロンプト.md | 図解5〜6枚分のプロンプト＋挿入位置マップ |
| 5 | 第N回_noteタグ.md | note投稿時のタグ提案 |
| 6 | generate_x_cards.py | X投稿カード10枚生成スクリプト（python3 -X utf8 generate_x_cards.py で実行） |

記事はnoteにコピペして公開できる状態です。
- サムネイル：`python3 -X utf8 generate_thumbnail.py` → `images/サムネイル_第N回.png`
- X投稿カード：`python3 -X utf8 generate_x_cards.py` → `images/x_posts/x_post_01〜10.png` + `x_posts.md`
- 図解：Nano Banana Proに各プロンプトを入力
```

---

## 出力の最終順序

以下の順序で全セクションを**1つの返答にまとめて**出力する：

```
SECTION 0｜記事目次（構成設計）
     ↓
SECTION 1｜note記事全文（約5000字）
     ↓
SECTION 2｜generate_thumbnail.py
     ↓
SECTION 3｜図解挿入位置マップ＋プロンプト（5〜6枚）
     ↓
SECTION 4｜noteタグ提案
     ↓
SECTION 5｜X投稿スレッド10本 + generate_x_cards.py
     ↓
STEP 7｜ファイル保存＋一覧出力
```

---

## 出力前の品質チェック（必ず確認）

**記事について**
- [ ] 冒頭は「状況説明」ではなく「感情の描写」から始まっているか
- [ ] 「意志が弱い」→「仕組みの問題」への転換が入っているか
- [ ] マーシーの実体験エピソードが各ステップに入っているか（数字付き）
- [ ] 科学的出典が1つ以上、著者・掲載誌付きで入っているか
- [ ] 崩れた時の復帰手順セクションが入っているか
- [ ] 「8勝6敗でOK」の思想が伝わっているか
- [ ] CTAと免責事項が末尾に入っているか
- [ ] 文字数が約5000字か（大幅に少ない場合は加筆する）

**ビジュアルについて**
- [ ] generate_thumbnail.py の変数（LINE1/LINE2/LINE3/SUB/NUM/OUTPUT_FNAME）が記事内容に合わせて正しく設定されているか
- [ ] サムネイル背景は黒（#000000）か
- [ ] SVGイラスト・棒人間が含まれていないか（テキスト主役デザイン）
- [ ] 図解は全て1280×720pxか
- [ ] 各図解プロンプトが「日本語インフォグラフィック〜」で始まり「正確に表示すること。」で終わるか
- [ ] タグは5〜6個（固定3＋追加2〜3）か

**X投稿について**
- [ ] X投稿スレッドが10本あるか
- [ ] 各投稿が140文字以内か（スレッド形式なので改行含む概算でOK）
- [ ] 投稿1が感情フック（「また今日も〜」「〜できなかった」等）から始まっているか
- [ ] 投稿10にnoteリンク（https://note.com/mash_anti_metabo）が含まれているか
- [ ] generate_x_cards.py の X_POSTS 変数が10本分設定されているか
- [ ] HASHTAG 変数が `#第N回 [テーマ]` 形式で設定されているか

**ファイル保存について**
- [ ] SECTION 0-5の出力が完了してから保存を開始する
- [ ] フォルダ名は既存の命名規則に従う（第N回_タイトル要約）
- [ ] 各ファイルのパスは絶対パスで指定する
- [ ] 保存完了後は必ず一覧表を出力する

---

## 使い方

```
/podcast-to-note-assets

[ここにポッドキャスト台本テキストをそのまま貼り付ける]
```

台本は丸ごとコピペでOK。形式・長さは問わない。
生成物は全て1回の返答に収まるように出力する。
