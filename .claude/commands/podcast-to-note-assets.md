# Longevity Navigator｜Podcast台本 → note公開セット一括生成

このコマンドは、ポッドキャスト台本テキスト1本から
**note公開に必要な全素材を一括で自動生成**します。

## 生成物一覧

| # | 成果物 | 用途 |
|---|---|---|
| 0 | 本番台本（改善反映済み） | Podcast収録用の完成台本 |
| 1 | 記事目次（構成設計） | 記事の骨格。感情導線の設計図 |
| 2 | note記事全文（約5000字） | noteに貼り付けて公開（図解挿入マーカー付き） |
| 3 | generate_thumbnail.py | サムネイルPNG自動生成 |
| 4 | generate_figures.py | 図解5枚PNG自動生成（HTML/CSS + Playwright） |
| 5 | noteタグ提案 | note投稿設定で使用 |
| 6 | stand.fm概要欄 | Podcast概要欄テキスト |
| 7 | generate_x_cards.py | X投稿カード10枚PNG自動生成 |

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

Podcast台本の固定テンプレート：

【オープニング（毎回固定）】
お疲れさまです、マーシーです。
元気ですかー？絶好調ですかー？
今日も聴いてくれてありがとうございます。
私はもともと、健康診断E判定のメタボでした。そこから食事・睡眠・運動を見直して100㎏から-32kg、今は68kg、そしてサブ3ランナーです。
現在はフルマラソン2時間50分切り通称サブエガを目指して日々トレーニングしています。
この番組では、その実体験と世界の最新研究をつなぎながら、日本を元気にするための健康習慣を"今日の1歩"まで落として、熱を込めて届けています。
では早速、日本を元気にする健康習慣ラジオ、やっていきましょう！

【エンディング（毎回固定・[変数]部分のみ差し替え）】
さあ、今日の1歩です。
[その回の具体的な1アクション]
全部やらなくていい。今日はこの1つだけ。
この1つが、明日のあなたを少しだけ変えます。

noteでは、今日話した内容をさらに深掘りして全文公開しています。
概要欄にリンクを貼っておくので、ぜひ読んでみてください。

あと、感想やコメント、めちゃくちゃ励みになります。
「やってみた」の一言だけでも、本当に嬉しいです。
あなたの声が、次の放送の燃料になります。

それでは、今日も最後まで聴いてくれてありがとうございました。
あなたの健康を、意志力じゃなく、仕組みで変える。
日本を元気にする健康習慣ラジオ、マーシーでした。
また次回！絶好調でいきましょう！

※この番組は個人の体験に基づく健康情報の共有です。
治療中の方や服薬中の方は、主治医の指示を優先してください。
```

---

## 実行手順

台本テキストが貼り付けられたら、以下を**この順番で**実行する。

---

### STEP 0：台本の構成確認 + 3つの改善案 → 本番台本の確定

**0-1. 台本の構成を整理して「確認用台本」を提示する**

貼り付けられた台本テキストを以下の観点で整理し、構成を可視化する：
- 全体の流れ（導入→共感→本題→実践→まとめ）
- 各セクションの時間配分（目安）
- 科学的根拠の有無・出典の正確性
- ペルソナ（田中 健二・42歳）に刺さる感情フックがあるか
- 「8勝6敗でOK」の思想が含まれているか

**0-2. 3つの改善案を提示する**

以下の3観点から具体的な改善案を提案する：

```
改善案①：感情フックの強化
  → 冒頭の共感度を上げる具体的な修正案

改善案②：科学的根拠・具体性の補強
  → データ・論文・数値を追加する箇所と内容

改善案③：構成・テンポの最適化
  → セクションの順序入れ替え、冗長な箇所のカット、不足の補完
```

**0-3. 改善を反映した「本番台本」を確定する**

3つの改善案をすべて反映した本番用台本を生成する。
この本番台本をSTEP 1以降の全素材生成のベースとして使う。

**出力フォーマット：**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎙️ STEP 0｜台本確認＋改善
━━━━━━━━━━━━━━━━━━━━━━━━━━

【構成確認】
| セクション | 内容 | 時間目安 |
|---|---|---|
...

【改善案①：感情フックの強化】
[具体的な修正内容]

【改善案②：科学的根拠の補強】
[具体的な追加内容]

【改善案③：構成・テンポの最適化】
[具体的な変更内容]

---

【本番台本（改善反映済み）】
[完全な本番用台本テキスト]
```

**0-4. 本番台本をファイルに保存する**

改善を反映した本番台本を `第N回_本番台本.md` としてフォルダに保存する（STEP 7で他ファイルと一緒に保存）。
元の台本と改善ポイントも含め、以下のフォーマットで保存：

```
# 第N回 本番台本（改善反映済み）

## 改善ポイント
- 改善①：[内容]
- 改善②：[内容]
- 改善③：[内容]

---

## 本番台本

[改善反映済みの完全な台本テキスト]
```

**重要：** STEP 0の出力（本番台本）が確認されてから、STEP 1以降に進む。
ただし、ユーザーが「確認不要」「そのまま進めて」と言った場合は、改善を反映した本番台本をそのまま使ってSTEP 1に進む。

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

図解挿入マーカーのルール：
  - 各セクションの末尾（`---` の直前）に図解の挿入位置を明示する
  - フォーマット：`> 📊【図解N挿入】図解N_ファイル名.png`
  - 5枚の図解を適切なセクションに配置する（STEP 5の図解と対応させる）
  - noteに貼り付ける際に、このマーカーの位置に画像を挿入する目印となる

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

### STEP 5：図解生成スクリプトを作成・実行する（SECTION 3として出力）

STEP 3で生成した記事の構成に沿って、5枚の図解を **HTML/CSS + Playwright** で直接PNG生成する。
Nano Banana Proなどの外部ツールは使わない。スクリプト1本で5枚すべて生成する。

**図解の種類と使い分け：**

| 図解 | 種類 | 挿入位置 |
|---|---|---|
| ① | フロー図（問題ループ） | セクション2の後 |
| ② | カードグリッド（3〜4ステップ全体像） | セクション3の後 |
| ③ | NG vs OK比較表 | セクション4の後 |
| ④ | 実践早見表（表形式） | ステップ後 |
| ⑤ | 復帰フロー（縦型3ステップ） | 崩れた日セクションの後 |

**デザインシステム（全図解共通）：**
```
背景色：#0d1b2a（ダーク紺）
オレンジ強調：#FF6D00
水色データ：#38bdf8
緑ポジティブ：#4ade80
赤NG：#ef4444
テキスト白：#ffffff
テキスト薄：#9ca3af
カードBG：#1e3a5f または #0d2035
```

**スクリプト構造（参考実装：`note/第9回_*/generate_figures.py`）：**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第N回 図解生成スクリプト（HTML/CSS + Playwright 強化版）"""
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

def fig1(): ... # 図解①（問題ループ・円形フロー）
def fig2(): ... # 図解②（ステップ全体像・横3列カード）
def fig3(): ... # 図解③（NG vs OK比較表・左右2列）
def fig4(): ... # 図解④（実践早見表・テーブル）
def fig5(): ... # 図解⑤（復帰フロー・縦型3ステップ）

if __name__ == "__main__":
    print("第N回 図解5枚 生成開始...\n")
    fig1(); fig2(); fig3(); fig4(); fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))
```

**重要：**
- 各 `figN()` 関数は記事内容に合わせた完全なHTML文字列を組み立てて `render()` に渡すこと
- 第9回の `generate_figures.py` を参考実装として使うこと
- スクリプトを `generate_figures.py` として保存してから `python3 -X utf8 generate_figures.py` で実行し、5枚のPNGを生成すること

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

### STEP 6.3：stand.fm概要欄を生成する（SECTION 4.5として出力）

STEP 3で生成した記事の内容を元に、stand.fm（Podcast）の概要欄テキストを生成する。

**概要欄の構成（固定フォーマット）：**

```
# stand.fm 概要欄 ― 第N回

## タイトル
[記事タイトルと同じ]

---

## 概要

[ペルソナの感情から入る冒頭 3〜5行]

[マーシーの体験 2〜3行]

[コアメッセージ 1〜2行（太字）]

---

## 今回の内容

✅ **[セクション1の要約]**
→ [具体的な内容1行]

✅ **[セクション2の要約]**
→ [具体的な内容1行]

✅ **[セクション3の要約]**
→ [具体的な内容1行]

✅ **[セクション4の要約]**
→ [具体的な内容1行]

✅ **[崩れた日のリカバリー]**
→ [具体的な内容1行]

---

## 今日からできること（1つだけでOK）

1. **[実践1]**
2. **[実践2]**
3. **[実践3]**

全部やらなくていい。今日は1つだけ。

---

📝 詳しくはnoteで全文公開中：
https://note.com/mash_anti_metabo

🎙️ 日本を元気にする健康習慣ラジオ ― E判定からの逆転 ―
マーシー｜100kg→68kg（-32kg）を8年間維持中｜サブ3ランナー
30〜40代メタボ逆転を仕組みで支援

#ダイエット #メタボ #習慣化 #[記事テーマに合わせたタグ3〜4個]
```

**概要欄の品質基準：**
- 冒頭は「感情」から始める（状況説明ではない）
- 「今回の内容」は箇条書き5項目以内
- 科学的根拠は著者名・年を添える
- マーシーの具体的な数字（コスト差・効果の差）を入れる
- 末尾にnoteリンクとハッシュタグ

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

**カード画像の設計原則（図解スタイル）：**
- サイズ：1280×720px
- 背景：ダークネイビー #0d1b2a（図解と統一）
- 右上：N/10（投稿番号）
- **左上のタグピル（「共感」「原因」等）は入れない**
- **テキストのみのフラットデザインは禁止。各カードに図解要素を入れる**
- 左下：マーシー｜100kg→68kg｜Sub3
- 右下：#第N回 [テーマ]（アクセントカラー）

**カードごとの図解レイアウト（番号別）：**

| カード | レイアウト | 視覚要素 |
|---|---|---|
| 1 共感 | タイムライン型 | 時刻＋カラーバー＋イベント列 |
| 2 原因 | フロー図型 | ステップカード＋矢印＋ループ表現 |
| 3 解決策 | 横3列ステップカード | 色分け枠＋矢印で接続 |
| 4 仕組み | 番号付きカード | アクセント色の番号バッジ＋出典バッジ |
| 5 効果 | Before/After比較 | 左赤パネル（✗）vs 右緑パネル（✓）＋数値 |
| 6 設計 | テーブル型 | ヘッダー行＋データ行＋列色分け |
| 7 実践 | 縦フロー型 | 丸番号＋枠付きステップカード＋接続線 |
| 8 復帰 | リカバリーフロー | 赤→緑のグラデーション＋ステップカード |
| 9 深掘り | データ可視化型 | CSSグラフ＋説明カード＋出典バッジ |
| 10 CTA | チェックリスト＋CTA | チェックバッジ＋CTAボックス |

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

**generate_x_cards.py テンプレート（図解版）：**

各カードは個別の `card_NN()` 関数として実装し、カードの役割に応じた図解レイアウトを使う。
テキストのみのフラットカードは禁止。必ず視覚構造（タイムライン、フロー図、比較表、グラフ等）を入れる。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第N回 X投稿用カード画像 10枚生成スクリプト（図解版）"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
HASHTAG = "#第N回 [テーマ]"

# ── 共通CSS ──────────────────────────────────────
BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;background:#0d1b2a;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
    ".num{position:absolute;top:44px;right:56px;font-size:22px;font-weight:700;color:#444;}"
    ".author{position:absolute;bottom:22px;left:56px;font-size:18px;font-weight:400;color:#3a3a3a;}"
    ".series{position:absolute;bottom:22px;right:56px;font-size:18px;font-weight:700;}"
    ".title{position:absolute;left:56px;top:96px;font-size:36px;font-weight:900;color:#fff;"
    "letter-spacing:-1px;}"
)

# ── ツイートテキスト ──────────────────────────────
TWEETS = [
    "[ツイート本文1]",
    "[ツイート本文2]",
    # ... 10本分
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]

# ── 各カード関数（記事内容に合わせて実装） ─────────
# card_01(): 共感 → タイムライン型（時刻＋バー＋イベント）
# card_02(): 原因 → フロー図（ステップカード＋矢印）
# card_03(): 解決策 → 横3列ステップカード（色枠＋矢印）
# card_04(): 仕組み → 番号バッジ付きカード＋出典バッジ
# card_05(): 効果 → Before/After比較パネル（赤✗ vs 緑✓）
# card_06(): 設計 → テーブル型（ヘッダー＋データ行＋列色分け）
# card_07(): 実践 → 縦フロー型（丸番号＋枠カード＋接続線）
# card_08(): 復帰 → リカバリーフロー（赤→緑グラデーション）
# card_09(): 深掘り → CSSグラフ＋説明カード＋出典バッジ
# card_10(): CTA → チェックリスト＋CTAボックス

# 実装例は第9回 generate_x_cards.py を参照。
# 各 card_NN() 関数は完全なHTML文字列を返す。

CARD_FUNCS = [card_01, card_02, card_03, card_04, card_05,
              card_06, card_07, card_08, card_09, card_10]

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

def save_tweets():
    out = OUTPUT_DIR / "x_posts.md"
    lines = ["# 第N回 X投稿スレッド（10本）\n\n"]
    for i, tweet in enumerate(TWEETS):
        tag = CARD_TAGS[i]
        lines.append(
            "## 投稿" + str(i+1) + "/10｜" + tag + "\n\n```\n" + tweet.strip() + "\n```\n\n"
            "![カード" + str(i+1) + "](x_post_" + str(i+1).zfill(2) + ".png)\n\n---\n\n"
        )
    out.write_text("".join(lines), encoding="utf-8")

if __name__ == "__main__":
    print("第N回 X投稿カード画像（図解版）生成開始...\n")
    for i, func in enumerate(CARD_FUNCS):
        html = func()
        fname = "x_post_" + str(i+1).zfill(2) + ".png"
        render(html, fname)
        print("✅ " + fname + "  [" + CARD_TAGS[i] + "]")
    save_tweets()
    print("\n全10枚完了。保存先: " + str(OUTPUT_DIR))
```

注意：
- 各 `card_NN()` 関数は記事内容に合わせた図解HTMLを返すこと
- 第9回の `generate_x_cards.py` を参考実装として使うこと
- テキストのみのフラットカードは禁止。必ず図解要素を入れること
- `HASHTAG` は `#第N回 [テーマ]` 形式で設定すること

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
| 1 | 第N回_本番台本.md | STEP 0の改善反映済み台本 |
| 2 | 第N回_記事目次.md | SECTION 0の内容 |
| 3 | 第N回_[タイトル].md | SECTION 1の内容（本文・図解挿入マーカー付き） |
| 4 | generate_thumbnail.py | サムネイル生成スクリプト |
| 5 | generate_figures.py | 図解5枚生成スクリプト |
| 6 | 第N回_noteタグ.md | SECTION 4の内容 |
| 7 | 第N回_standfm概要欄.md | stand.fm概要欄テキスト |
| 8 | generate_x_cards.py | X投稿カード10枚生成スクリプト |

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
| 1 | 第N回_本番台本.md | STEP 0の改善反映済みPodcast台本 |
| 2 | 第N回_記事目次.md | 記事の構成設計・感情導線の設計図 |
| 3 | 第N回_[タイトル].md | note記事本文（約5,000字・図解挿入マーカー付き） |
| 4 | generate_thumbnail.py | サムネイル生成スクリプト |
| 5 | generate_figures.py | 図解5枚生成スクリプト |
| 6 | 第N回_noteタグ.md | note投稿時のタグ提案 |
| 7 | 第N回_standfm概要欄.md | stand.fm概要欄テキスト |
| 8 | generate_x_cards.py | X投稿カード10枚生成スクリプト |

全画像は自動生成済みです：
- サムネイル：`images/サムネイル_第N回.png`
- 図解5枚：`images/図解①〜⑤_*.png`
- Xカード10枚：`images/x_posts/x_post_01〜10.png` + `x_posts.md`
```

---

## 出力の最終順序

以下の順序で全セクションを**1つの返答にまとめて**出力する：

```
SECTION 0｜記事目次（構成設計）
     ↓
SECTION 1｜note記事全文（約5000字）
     ↓
SECTION 2｜generate_thumbnail.py → サムネイルPNG生成
     ↓
SECTION 3｜generate_figures.py → 図解5枚PNG生成
     ↓
SECTION 4｜noteタグ提案
     ↓
SECTION 5｜X投稿スレッド10本 + generate_x_cards.py → Xカード10枚PNG生成
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
- [ ] generate_figures.py が5枚のPNGを正常に生成したか
- [ ] 図解は全て1280×720pxか
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
