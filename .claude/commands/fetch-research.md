# Longevity Navigator｜最新研究収集 → Obsidian・Memory保存

このコマンドは、健康・不老長寿・ダイエット領域の**世界最先端情報をWeb検索で自動収集**し、
X投稿・note記事の参考資料としてすぐ使える形で保存します。

## 保存先

| 保存先 | パス | 用途 |
|---|---|---|
| Obsidianノート | `2nd-Brain/06_リソース/Longevity_Research/` | 記事執筆時の参照元 |
| Claude Memory | `memory/research_stock.md` | 次回会話でのコンテキスト補完 |
| ストックリスト | `note/research_stock.md` | X投稿・note用ネタ一覧 |

---

## 実行手順

### STEP 1｜検索トピックを決める

引数がある場合：その引数をトピックとして使う
引数がない場合：以下のデフォルトトピックから未収集のものを選ぶ

```
デフォルトトピック（優先順）：
1. NMN・NAD+ 最新臨床研究（2024〜2025）
2. オートファジー × 断食 最新知見
3. GLP-1薬 × 筋肉喪失リスク
4. ゾーン2トレーニング × 脂肪燃焼
5. 睡眠最適化 × 代謝・長寿
6. 地中海食 × メタボリックシンドローム改善
7. 超加工食品 × 腸内細菌・肥満
8. クレアチン × 認知機能・老化
9. レジスタンストレーニング × 代謝改善
10. マグネシウム × 睡眠・インスリン抵抗性
```

---

### STEP 2｜Web検索で情報収集

以下の手順で検索する：

**検索クエリ例（日本語と英語の両方）：**
- `[トピック] 最新研究 2024 2025`
- `[topic] clinical trial 2024 2025 PubMed`
- `[topic] meta-analysis 2025`

収集する情報：
- 研究機関・著者名
- 発表年・掲載誌（PubMed・Nature・NEJM等）
- 主な結論（数値・%・具体的な効果量）
- ペルソナ（田中 健二42歳）への関連度
- X投稿・note記事への活用アイデア

---

### STEP 3｜Obsidianノートを作成・保存

**保存パス：**
`C:\Users\masas\product\2nd-Brain\06_リソース\Longevity_Research\YYYYMMDD_[トピック名].md`

**ノートフォーマット：**

```markdown
---
date: YYYY-MM-DD
topic: [トピック名]
tags: [longevity, research, 関連タグ]
source: [掲載誌・URL]
usedin: []
---

# [トピック名]｜最新研究メモ

## 要点（3行サマリー）
-
-
-

## 研究詳細

### 研究1
- **タイトル：**
- **著者・機関：**
- **掲載：**
- **結論：**
- **数値：**

### 研究2
（同形式で続ける）

## X投稿アイデア（140字以内×3案）

### 案1（数字フック型）
```
[ここにX投稿文]
```

### 案2（共感型）
```
[ここにX投稿文]
```

### 案3（意外性型）
```
[ここにX投稿文]
```

## note記事アイデア

- タイトル候補：
- 構成メモ：
- ペルソナへの刺さり方：

## 関連する過去記事

-

---
*収集日: YYYY-MM-DD｜Claude Code自動収集*
```

---

### STEP 4｜research_stock.md に追記

**パス：** `C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note\research_stock.md`

既存ファイルがある場合は先頭に追記（新しいものを上に）。
ない場合は新規作成。

**追記フォーマット：**

```markdown
## [YYYY-MM-DD]｜[トピック名]

**一言サマリー：** [30字以内]
**数値：** [最も印象的な数値・データポイント]
**活用度：** ★★★★☆（X向き）/ ★★★☆☆（note向き）
**Obsidianノート：** `06_リソース/Longevity_Research/YYYYMMDD_[トピック名].md`

---
```

---

### STEP 5｜Claude Memoryを更新

**パス：** `C:\Users\masas\.claude\projects\c--Users-masas-product-2nd-Brain-04--------Longevity-note\memory\research_stock.md`

既存ファイルがあれば更新、なければ新規作成。

**Memory フォーマット（frontmatter必須）：**

```markdown
---
name: 最新研究ストック
description: X投稿・note記事に使える最新健康・長寿研究のリスト
type: reference
---

# 最新研究ストック（直近収集分）

| 日付 | トピック | 一言サマリー | 活用度 |
|---|---|---|---|
| YYYY-MM-DD | [トピック] | [サマリー] | ★★★★☆ |
（最新10件のみ保持）

最終更新: YYYY-MM-DD
```

---

### STEP 6｜MEMORY.md のインデックスを更新

`C:\Users\masas\.claude\projects\c--Users-masas-product-2nd-Brain-04--------Longevity-note\memory\MEMORY.md` に
`research_stock.md` へのリンクがなければ追加する。

---

### STEP 7｜収集結果をサマリー表示

以下の形式でユーザーに報告する：

```
収集完了：[トピック名]

主な知見：
・[知見1]
・[知見2]
・[知見3]

保存ファイル：
・Obsidian: 06_リソース/Longevity_Research/YYYYMMDD_[トピック名].md
・ストック: note/research_stock.md（先頭に追記）
・Memory: memory/research_stock.md（更新）

X投稿候補（最有力）：
[140字以内のX投稿文]

次のおすすめトピック：[未収集の中で最も旬なもの]
```

---

## 注意事項

- 医療的断言はしない。「〜が示された」「〜の可能性がある」等の表現を使う
- 出典（著者・掲載誌・年）は必ず明記する
- PubMed・Nature・NEJM・Lancet等の査読済み論文を優先する
- ペルソナ（30〜45歳男性・メタボ・E判定）への関連度を必ず評価する
- 1回の実行で1〜3トピックまで（多すぎると質が落ちる）
