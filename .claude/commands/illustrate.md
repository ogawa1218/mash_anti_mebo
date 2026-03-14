# Longevity Navigator｜イラストレーター｜図解PNG自動生成（強化版）

このコマンドは、記事テキストまたはX投稿文を受け取り、
**HTML/CSS + Playwright** で高品質な図解PNGを自動生成します。

## 出力先

| 用途 | サイズ | 保存先 |
|---|---|---|
| X投稿用 | 1280×720px | `images/YYYYMMDD_[topic]/x_[N].png` |
| noteヘッダー用 | 1280×670px | `images/YYYYMMDD_[topic]/note_header.png` |
| 正方形（汎用） | 1080×1080px | `images/YYYYMMDD_[topic]/square_[N].png` |

---

## 実行手順

### STEP 1｜入力を受け取る

引数がある場合：その引数をコンテンツとして使う
引数がない場合：最新の `note/batch_YYYYMMDD.md` を読み込む

入力の種類を判定：
- X投稿文（短文・箇条書き）→ X用インフォグラフィック
- note記事テキスト → note用図解セット（5枚）
- トピック名のみ → 研究データ図解

---

### STEP 2｜レイアウト種別を自動判定

コンテンツの構造を分析して最適なレイアウトを選ぶ：

| コンテンツの特徴 | レイアウト種別 |
|---|---|
| 「→」「だから」等の因果関係 | フロー図（縦型・横型） |
| A vs B の比較 | 比較表（左右2列） |
| 数値・%・統計 | データビジュアル（バー・プログレス） |
| 手順・ステップ | ステップカード（番号付き） |
| チェック項目 | チェックリスト |
| 時間・タイミング | タイマーグリッド |
| 選択肢・判断 | YES/NOフロー |
| 複数の柱・要素 | カードグリッド |

---

### STEP 3｜Pythonスクリプトを実行

**スクリプトパス：**
`C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note\scripts\illustrate_hq.py`

**実行コマンド：**
```bash
python3 -X utf8 "C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note\scripts\illustrate_hq.py" \
  --content "[コンテンツテキスト]" \
  --layout "[レイアウト種別]" \
  --topic "[トピック名]" \
  --size "x|note|square|all"
```

スクリプトが存在しない場合は、まずスクリプトを生成してから実行する。

---

### STEP 4｜生成確認・サマリー表示

```
図解生成完了：YYYY-MM-DD

生成ファイル：
・[ファイル名1]（[レイアウト種別] / [サイズ]）
・[ファイル名2]

レイアウト判定理由：[なぜそのレイアウトを選んだか]

次のアクション：
・X投稿時はx_[N].pngを添付
・note記事には note_header.png + 図解を挿入
```

---

## デザインシステム（全図解共通）

### カラーパレット
```
背景（ダーク）：  #1A2A3A
パネル：          #27292d または rgba(255,255,255,0.08)
オレンジ強調：    #f97316
水色データ：      #38bdf8
緑ポジティブ：    #4ade80
赤NG：            #ef4444
テキスト白：      #f0f1f3
テキスト薄：      #7a7e8a
```

### 強化エフェクト
- **グラスモーフィズム**：`backdrop-filter: blur(12px)` + 半透明背景
- **グラデーション**：多段・放射状・コニカル対応
- **光彩（Glow）**：`box-shadow: 0 0 20px rgba(249,115,22,0.4)`
- **SVGアイコン**：インライン埋め込み（Font Awesomeアイコンパス）
- **タイポグラフィ**：NotoSansJP-VF.ttf（可変フォント）

### フォント設定
```css
@font-face {
  font-family: 'NotoSansJP';
  src: url('file:///C:/Windows/Fonts/NotoSansJP-VF.ttf');
}
```

---

## 注意事項

- Playwrightがインストールされていること（`pip install playwright` + `playwright install chromium`）
- フォントパス `C:/Windows/Fonts/NotoSansJP-VF.ttf` が存在すること
- スクリプトにf-stringは使わない（CSS `{}` との競合を避けるため文字列結合で書く）
- 生成失敗時はHTMLファイルをブラウザで開いて確認すること
