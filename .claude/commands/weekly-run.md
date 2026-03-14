# Longevity Navigator｜週次ワークフロー｜全エージェント一括実行

このコマンドは、コンテンツ制作の**全工程を週次で自動実行**するコーディネーターです。
各スキルを順番に呼び出し、1週間分のコンテンツ素材を一括生成します。

---

## 実行フロー

```
/weekly-run
    │
    ├─ Phase 1：情報収集
    │   ├─ /fetch-research → 新しい研究トピック収集（1〜2件）
    │   └─ /trend-hunt    → 世界バズTop3を発掘・翻案
    │
    ├─ Phase 2：コンテンツ生成
    │   ├─ /content-batch → X投稿10本 + note記事1〜2本
    │   └─ /podcast-script→ Podcast台本 + 概要欄（1本）
    │
    ├─ Phase 3：素材生成
    │   └─ /illustrate    → 図解PNG生成（note用 + X用）
    │
    └─ Phase 4：週次レポート出力
```

---

## 実行手順

### STEP 1｜実行前チェック

以下を確認してから開始する：
- `note/research_stock.md` の最新状態を把握
- 前回の `/weekly-run` からの差分（新しいトピックがあるか）
- 今週の推奨テーマ（活用度★★★★★未使用のものを優先）

---

### STEP 2｜Phase 1：情報収集（並行実行）

**2-1. 新しい研究を収集**
`/fetch-research` を実行。
- 引数なし → デフォルトリストから未収集のトピックを1〜2件選ぶ
- 収集済みの場合はスキップしてPhase 2へ

**2-2. バズコンテンツを発掘**
`/trend-hunt` を実行。
- 世界の健康・長寿ジャンルのトレンドTop3を収集
- マーシー版に翻案

---

### STEP 3｜Phase 2：コンテンツ生成

**3-1. X投稿10本 + note記事を生成**
`/content-batch` を実行。
- `research_stock.md` から全トピックのX投稿を生成
- ★★★★★トピックをnote記事に展開

**3-2. Podcast台本を生成**
`/podcast-script` を実行。
- 今週最も旬なトピック or 最新のnote記事を元に
- 台本（2,500〜3,500字）+ 概要欄を生成

---

### STEP 4｜Phase 3：図解生成

`/illustrate` を実行。
- 今週のnote記事から図解5枚（note用・X用）を生成
- Podcast用サムネイル（正方形1080×1080）を1枚生成

---

### STEP 5｜週次レポートを出力・保存

**保存パス：**
`C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note\weekly_report_YYYYMMDD.md`

**レポートフォーマット：**

```markdown
# 週次レポート｜YYYY-MM-DD（第〇週）

## 今週生成した素材

### 研究収集（/fetch-research）
- [トピック名]：Obsidian保存済み

### バズ翻案（/trend-hunt）
- 1位：[コンテンツ名]（[媒体]）
- 2位：[コンテンツ名]（[媒体]）
- 3位：[コンテンツ名]（[媒体]）

### X投稿（/content-batch）
- 生成本数：10本
- 推奨投稿順：[1位→2位→...]
- バッチファイル：content_batches/batch_YYYYMMDD.md

### note記事（/content-batch）
- [タイトル1]（[字数]字）→ note/drafts/YYYYMMDD_[].md
- [タイトル2]（[字数]字）→ note/drafts/YYYYMMDD_[].md

### Podcast台本（/podcast-script）
- [エピソードタイトル]（想定[〇〇]分）
- 台本：Podcast/台本/YYYYMMDD_[].md
- 概要欄：Podcast/stand.fm概要欄/YYYYMMDD_[].md

### 図解（/illustrate）
- 生成枚数：〇枚
- 保存先：images/YYYYMMDD_[topic]/

---

## 今週の投稿スケジュール案

| 曜日 | 媒体 | コンテンツ |
|---|---|---|
| 月曜 21:00 | X | [投稿1] |
| 火曜 20:00 | note | [記事タイトル] |
| 水曜 21:00 | X | [投稿2] |
| 木曜 21:00 | stand.fm | [Podcastエピソード] |
| 金曜 21:00 | X | [投稿3〜4] |
| 土曜 21:00 | X | [投稿5] |
| 日曜 20:00 | X | [投稿6（反応まとめ or 新投稿）] |

---

## KPI目標（今週）

- noteスキ目標：[〇件]
- Xインプレッション目標：[〇回]
- Podcastリスナー目標：[〇人]

---

## 来週の推奨テーマ

1. [未使用★★★★★トピック]
2. [トレンドハントから]
3. [読者反応から]

---
*生成日：YYYY-MM-DD｜Claude Code自動生成*
```

---

### STEP 6｜完了サマリーを表示

```
週次ワークフロー完了：YYYY-MM-DD

生成した素材：
・研究ノート：[N]件（Obsidian保存済み）
・バズ翻案：3件（trend_hunt_YYYYMMDD.md）
・X投稿：10本（batch_YYYYMMDD.md）
・note記事：[N]本（drafts/に保存）
・Podcast台本：1本（Podcast/台本/に保存）
・図解PNG：[N]枚（images/に保存）

週次レポート：weekly_reports/weekly_report_YYYYMMDD.md

次のアクション（マーシーがやること）：
1. batch_YYYYMMDD.md を開いて投稿スケジュールを確認
2. note記事の下書きを加筆・修正して公開
3. Podcast台本を読んで収録
4. 図解をnote記事 / X投稿に挿入
```

---

## スキップ条件

以下の場合は該当フェーズをスキップして続行する：
- `/fetch-research` → 今週すでに実行済み → スキップ
- `/trend-hunt` → 今週すでに実行済み → スキップ
- `/illustrate` → Playwrightエラーの場合 → スキップして報告

---

## 注意事項

- 1回の実行で全フェーズを完走する（途中で止まらない）
- エラーが発生しても他のフェーズは継続する
- 生成物はすべて必ずファイルに保存してから報告する
- マーシーへの確認は最後のサマリー表示時のみ
