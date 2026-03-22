#!/bin/bash
# 不老長寿・健康ニュース自動収集スクリプト
# 毎朝6時（朝版）・夕方17時（夕版）に実行
# 使用方法: ./collect_health_news.sh [朝|夕]

set -euo pipefail

# 引数チェック
SESSION="${1:-朝}"
DATE=$(date +%Y%m%d)
TIME_LABEL="${SESSION}"  # 朝 or 夕

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT_DIR="${PROJECT_DIR}/daily_news/${DATE}_${TIME_LABEL}"

mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/health_news_${DATE}_${TIME_LABEL}.md"

echo "=== 不老長寿・健康ニュース収集開始: $(date '+%Y-%m-%d %H:%M') ==="
echo "出力先: $OUTPUT_FILE"

# Claude CLIでニュース収集・翻訳・Podcast候補選定を実行
claude --dangerously-skip-permissions -p "
今日（$(date '+%Y年%m月%d日')）の${SESSION}の不老長寿・健康ニュース収集タスクです。

## タスク

WebSearchツールを使って、以下のテーマに関する最新の世界の研究・ニュースを10件収集し、日本語に翻訳してまとめてください。

### 収集テーマ
- 長寿・アンチエイジング研究（NMN、ラパマイシン、セノリティクスなど）
- 栄養学・食事法（断食、地中海食、ケトジェニックなど）
- 睡眠科学（睡眠の質、概日リズムなど）
- 運動科学（筋トレ、HIIT、ゾーン2トレーニングなど）
- メタボリズム・代謝研究
- GLP-1・肥満研究
- 脳・認知機能・メンタルヘルス
- 腸内細菌・マイクロバイオーム
- ホルモン最適化
- バイオマーカー・予防医学

## 出力フォーマット

以下のMarkdown形式で出力してください：

---

# 🌟 不老長寿・健康ニュース ${DATE} ${TIME_LABEL}版

収集日時: $(date '+%Y年%m月%d日 %H:%M')

---

## 📰 今日のヘルスニュース TOP10

### 1. [タイトル（日本語）]
- **原題**: [英語原題]
- **発信元**: [メディア/ジャーナル名・年]
- **カテゴリ**: [栄養/睡眠/運動/長寿/代謝/その他]
- **概要**: [200字程度の日本語要約]
- **マーシー視点**: [30〜40代メタボ男性への応用ポイント1〜2行]

（2〜10番も同様）

---

## 🎙️ Podcastネタ候補 TOP3

上記10件の中から、Podcast台本に最適な3件を選び、その理由と台本構成案を記載。

### 候補1: [タイトル]
- **選定理由**: [なぜPodcastに適しているか]
- **想定タイトル案**: [「〇〇〇〇〇」のような台本タイトル3案]
- **構成メモ**: [オープニング → 本題 → まとめの流れを3〜4行で]
- **ターゲット共感ポイント**: [田中健二（42歳メタボ管理職）が「それ自分だ！」と思うポイント]

### 候補2: [同上]

### 候補3: [同上]

---

## 📌 今週のトレンドメモ
[10件を横断して見えるトレンド・キーワードを3〜5点箇条書き]

---
" > "$OUTPUT_FILE"

echo "=== 収集完了: $(date '+%Y-%m-%d %H:%M') ==="
echo "ファイル: $OUTPUT_FILE"

# 完了通知（terminal-notifier / notify-send があれば）
if command -v notify-send &>/dev/null; then
    notify-send "健康ニュース収集完了" "${DATE} ${TIME_LABEL}版 → ${OUTPUT_DIR}"
fi
