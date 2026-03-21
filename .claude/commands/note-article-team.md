# Longevity Navigator｜noteコンテンツ制作チーム｜全素材一括生成

このコマンドは、Podcast台本（またはテーマ）から**note公開に必要な全素材を内製エージェントチームで一括生成**します。
図解・サムネイル・Xカードはすべて **HTML/CSS + Playwright** で直接生成します（外部ツール不要）。

---

## エージェントチーム構成

```
┌────────────────────────────────────────────────────┐
│           note コンテンツ制作チーム                  │
│                                                    │
│  🔍 Phase 0: 分析エージェント（台本解析・回数特定）  │
│                    ↓                               │
│  ✍️  Phase 1: 記事生成エージェント（直列）           │
│       ├─ note記事全文（5000字）                    │
│       └─ X投稿スレッド10本テキスト                  │
│                    ↓                               │
│  🎨 Phase 2: ビジュアル生成チーム（並列実行）        │
│       ├─ 🖼️  図解職人エージェント（5枚PNG）          │
│       ├─ 📸 サムネイル職人エージェント（1枚PNG）     │
│       └─ 🐦 X投稿職人エージェント（10枚PNG）        │
│                    ↓                               │
│  💾 Phase 3: 保存・完了レポートエージェント          │
└────────────────────────────────────────────────────┘
```

---

## 入力形式

```
/note-article-team

[ここにPodcast台本 または テーマ名 を貼り付ける]
```

- **台本がある場合**：そのままペースト → 台本を元に生成
- **テーマのみの場合**：例「外食でも太らない方法」→ 台本なしで記事・図解を直接生成

---

## 実行手順

---

### ─── Phase 0：分析エージェント ───

#### 0-1. 回数・前回記事を特定する（出力しない）

1. `C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note\` の `第*回_*` フォルダをGlobで一覧取得
2. 最大回数+1 = 今回の回数（N）と決定
3. 前回フォルダ内のmdファイルのタイトル行（`# `）を読み取る
4. 前回のカテゴリ（睡眠・食事・運動・習慣化・ニュース）を判定

#### 0-2. 台本・テーマを分析する（出力しない）

台本または入力テーマから以下を抽出：
```
- テーマ（1行）
- 感情フック（「これ自分だ」と思う場面）
- コアメッセージ（1行）
- 主要ポイント（3〜6個）
- 実体験エピソード
- 科学的根拠（台本にあれば）
- 記事カテゴリ
- 丸数字エピソード番号（⑨⑩…）
```

---

### ─── Phase 1：記事生成エージェント ───

#### 1-1. note記事全文（約5000字）

以下の品質基準で生成する：

**感情導線（必須）：**
```
フェーズ1「共感」→ フェーズ2「問題の正体」→ フェーズ3「結論先出し」
→ フェーズ4「実践手順」→ フェーズ5「崩れた時の戻り方」→ フェーズ6「まとめ+CTA」
```

**記事執筆ルール：**
- 冒頭は「感情の描写」から（状況説明NG）
- 「意志が弱い」→「仕組みの問題」への転換を入れる
- マーシーの実体験エピソードを各ステップに入れる（数字付き）
- 科学的出典を1つ以上：著者・掲載誌・年を明記する
- 崩れた時の復帰手順セクションを必ず入れる
- 「8勝6敗でOK」の思想を伝える
- 末尾：前回記事リンク・Podcast案内・プロフィール・免責事項

**フォーマット：**
```
# [タイトル]
## 1. [見出し]
...
【出典】
▼ 前回の記事（[カテゴリ]編）
「[前回タイトル]」
▼ Podcast...
【免責事項】
```

#### 1-2. X投稿スレッド10本テキスト

| 番号 | 役割 | アクセント |
|---|---|---|
| 1 | 共感フック | 水色 |
| 2 | 原因 | 水色 |
| 3 | 解決策 | オレンジ |
| 4 | 仕組み | 水色 |
| 5 | 効果 | 緑 |
| 6 | 設計 | 水色 |
| 7 | 実践 | オレンジ |
| 8 | 復帰 | 緑 |
| 9 | 深掘り | 水色 |
| 10 | CTA | オレンジ（noteリンク含む） |

各140文字以内。投稿1は感情フックから始める。投稿10にhttps://note.com/mash_anti_metabo を入れる。

---

### ─── Phase 2：ビジュアル生成チーム（並列） ───

**Phase 2の3タスクは独立しているため、3つのスクリプトを順次作成・実行する。**

---

#### 2-1. 図解職人エージェント → generate_figures.py

**生成する図解：5枚（1280×720px）**

記事の感情導線に沿って以下の5種類を設計・生成する：

| 図解 | 種類 | 挿入位置 |
|---|---|---|
| ① | フロー図（問題ループ） | セクション2の後 |
| ② | カードグリッド（3〜4ステップ全体像） | セクション3の後 |
| ③ | NG vs OK比較表 | セクション4の後 |
| ④ | 実践早見表（表形式） | ステップ後 |
| ⑤ | 復帰フロー（縦型3ステップ） | 崩れた日セクションの後 |

**デザインシステム（全図解共通）：**
```python
BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('file:///C:/Windows/Fonts/NotoSansJP-VF.ttf');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;font-family:'NJ','Meiryo',sans-serif;position:relative;}"
)
背景色：#0d1b2a（ダーク紺）
オレンジ強調：#FF6D00
水色データ：#38bdf8
緑ポジティブ：#4ade80
赤NG：#ef4444
テキスト白：#ffffff
テキスト薄：#9ca3af
カードBG：#1e3a5f または #0d2035
```

**スクリプト構造（記事内容に合わせて各figN関数を実装する）：**

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

def fig1(): ... # 図解①（問題ループ）
def fig2(): ... # 図解②（ステップ全体像）
def fig3(): ... # 図解③（NG vs OK）
def fig4(): ... # 図解④（実践早見表）
def fig5(): ... # 図解⑤（復帰フロー）

if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5()
    print("全5枚完了。保存先: " + str(OUTPUT_DIR))
```

スクリプトを `generate_figures.py` として保存してから `python3 -X utf8 generate_figures.py` で実行する。

---

#### 2-2. サムネイル職人エージェント → generate_thumbnail.py

**サムネイル仕様：1280×670px / 黒背景 #000000**

記事タイトル・テーマから3行コピーを生成：
```
行1（白・86px）：感情フック（10文字以内）
行2（白・86px）：ベネフィット or 裏切り（10文字以内）
行3（オレンジ・96px）：結論ワード（10文字以内）
SUB：サブテキスト（グレー・36px）
NUM：エピソード丸数字（右下・オレンジ）
```

**スクリプト構造：**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第N回 サムネイル生成スクリプト"""
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
SUB          = "[サブテキスト]"
NUM          = "[丸数字]"
OUTPUT_FNAME = "サムネイル_第N回.png"

THUMBNAIL_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
@font-face { font-family:'NotoSansJP'; src:url('""" + """[FONT]""" + """'); font-weight:100 900; }
*{ margin:0; padding:0; box-sizing:border-box; -webkit-font-smoothing:antialiased; }
body{ width:1280px; height:670px; overflow:hidden; background:#000000; position:relative;
  font-family:'NotoSansJP','Meiryo',sans-serif; }
.accent{ position:absolute; left:80px; top:72px; width:72px; height:6px;
  background:#FF6D00; border-radius:3px; box-shadow:0 0 18px rgba(255,109,0,.7); }
.copy{ position:absolute; left:80px; top:108px; }
.line1{ display:block; font-size:86px; font-weight:900; color:#FFFFFF; line-height:1.18; letter-spacing:-2px; }
.line2{ display:block; font-size:86px; font-weight:900; color:#FFFFFF; line-height:1.18; letter-spacing:-2px; }
.line3{ display:block; font-size:96px; font-weight:900; color:#FF6D00; line-height:1.2;
  margin-top:14px; letter-spacing:-2px;
  text-shadow:0 0 50px rgba(255,109,0,.6),0 0 100px rgba(255,109,0,.28); }
.sub{ display:block; font-size:36px; font-weight:500; color:#666666; line-height:1.4; margin-top:20px; }
.author{ position:absolute; bottom:26px; left:80px; font-size:22px; font-weight:400; color:#555555; }
.num{ position:absolute; bottom:16px; right:60px; font-size:80px; font-weight:900; color:#FF6D00;
  text-shadow:0 0 30px rgba(255,109,0,.45); }
</style></head><body>
<div class="accent"></div>
<div class="copy">
  <span class="line1">[LINE1]</span>
  <span class="line2">[LINE2]</span>
  <span class="line3">[LINE3]</span>
  <span class="sub">[SUB]</span>
</div>
<p class="author">マーシー｜100kg→68kg｜Sub3</p>
<p class="num">[NUM]</p>
</body></html>"""

if __name__ == "__main__":
    out = OUTPUT_DIR / OUTPUT_FNAME
    tmp = ARTICLE_DIR / "_tmp_thumb.html"
    tmp.write_text(THUMBNAIL_HTML, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 670})
        page.goto("file:///" + str(tmp).replace("\\", "/"))
        page.wait_for_timeout(900)
        page.screenshot(path=str(out), full_page=False)
        browser.close()
    tmp.unlink(missing_ok=True)
    print("OK: " + str(out))
```

`[FONT]`, `[LINE1]`〜`[NUM]` を記事内容で埋めて、`generate_thumbnail.py` として保存・実行する。

---

#### 2-3. X投稿職人エージェント → generate_x_cards.py

**Xカード仕様：1280×720px / 黒背景**

1-2で生成したスレッド10本テキストを使ってカード画像10枚を生成する。

**スクリプト構造：**

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

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]
TWEETS = ["[ツイート1]", ..., "[ツイート10]"]

# 各カードは card_NN() 関数として実装。カードの役割に応じた図解レイアウトを使う。
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
CARD_FUNCS = [card_01, ..., card_10]
# render(html, fname) → Playwright で PNG 保存
```

**重要：**
- テキストのみのフラットカードは禁止。各カードに図解要素（タイムライン、フロー図、比較表、グラフ等）を入れる。
- 左上のタグピル（「共感」「原因」等の役割ラベル）は入れない。
参考実装：`note/第9回_*/generate_x_cards.py`
`generate_x_cards.py` として保存・実行する。

---

### ─── Phase 3：保存・完了レポートエージェント ───

#### 3-1. フォルダ作成・ファイル保存

フォルダ名：`第N回_[タイトル要約（30文字以内）]`

```
C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note\第N回_[フォルダ名]\
├── 第N回_記事目次.md
├── 第N回_[タイトル].md          ← 記事全文
├── generate_thumbnail.py        ← 実行済み
├── generate_figures.py          ← 実行済み
├── generate_x_cards.py          ← 実行済み
├── 第N回_noteタグ.md
└── images/
    ├── サムネイル_第N回.png
    ├── 図解①〜⑤.png
    └── x_posts/
        ├── x_post_01〜10.png
        └── x_posts.md           ← X投稿テキスト10本
```

#### 3-2. 完了レポートを出力

```
━━━━━━━━━━━━━━━━━━━━━━━
✅ 第N回 全素材生成完了：YYYY-MM-DD
━━━━━━━━━━━━━━━━━━━━━━━

📁 第N回_[フォルダ名]

生成物：
  📝 note記事（約5000字）
  📸 サムネイル（1枚・PNG）
  🖼️  図解（5枚・PNG）
  🐦 Xカード（10枚・PNG）+ テキスト

マーシーがやること：
  1. 記事をnoteにコピペ → サムネイルをアップロード
  2. 図解をセクションに挿入（挿入位置は記事内に記載）
  3. Xカードをimages/x_posts/x_posts.md のテキストと一緒に予約投稿
━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 品質チェックリスト（保存前に確認）

**記事：**
- [ ] 冒頭が感情描写から始まっているか
- [ ] 「意志の問題→仕組みの問題」への転換が入っているか
- [ ] 実体験エピソードに数字が入っているか
- [ ] 科学的出典（著者・掲載誌・年）が1つ以上入っているか
- [ ] 崩れた時の復帰セクションが入っているか
- [ ] 約5000字になっているか

**ビジュアル：**
- [ ] サムネイル：黒背景・3行コピー・エピソード番号・実際にPNG生成済みか
- [ ] 図解5枚：すべてPNG生成済みか
- [ ] Xカード10枚：すべてPNG生成済みか

---

## 注意事項

- Playwrightがインストールされていること（`pip install playwright` + `playwright install chromium`）
- フォントパス `C:/Windows/Fonts/NotoSansJP-VF.ttf` が存在すること
- 生成に失敗した場合はHTMLファイルをブラウザで開いて確認する
- スクリプト内でf-stringを使う場合はCSS `{}` との競合に注意（文字列結合を推奨）
