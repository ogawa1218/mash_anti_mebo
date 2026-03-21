# Longevity Navigator｜おはよう｜今日のタスク + 最新ニュース収集

ユーザーが「おはよう」と言ったら、今日やるべきタスクを一覧表示し、
さらに**世界最先端の不老長寿・健康・ダイエットニュースを5本収集**してダッシュボード画像を生成する。

---

## PART A：今日のタスク表示

### STEP 1：今日の日付と曜日を確認する

現在の日付と曜日を取得する。

### STEP 2：ロードマップからタスクを読み取る

`C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\ROADMAP_2026.md` を読み、
今日の日付に該当するタスクを抽出する。

### STEP 3：進捗状況を確認する

以下を確認して、今日の状態を把握する：

1. **note記事の公開状況**：`note/第*回_*/` フォルダをGlobで一覧取得し、最新回数を特定
2. **素材の生成状況**：最新回のフォルダ内に `images/` があるか確認
3. **直近のgitログ**：`git log --oneline -5` で直近の作業内容を確認
4. **日誌の確認**：`daily_logs/` 内の直近ファイルを読み、前日の完了タスクを確認

### STEP 4：今日のタスクを表示する

以下のフォーマットで出力する：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
☀️ おはよう、マーシー！ YYYY年MM月DD日（曜日）
━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 現在の進捗
  note公開済み：第N回まで（素材完成：第M回まで）
  有料note：[状況]
  ローンチまで：あとX日（4/18）

📋 今日のタスク
  □ [タスク1]（所要時間）
  □ [タスク2]（所要時間）
  □ [タスク3]（所要時間）

⏱️ 合計所要時間：約XX分

💡 今日のポイント
  [その日の優先度が高いタスクについて一言アドバイス]

━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 表示のルール

- タスクはロードマップの該当日から取得する
- ロードマップに該当日がない場合は、週次ルーティン（月〜日）から曜日ベースで提案する
- 前日の日誌で未完了のタスクがあれば、今日に繰り越して表示する
- ローンチ日（4/18）までのカウントダウンを常に表示する
- 挨拶はフレンドリーに。朝の気分が上がるようなトーンで

### 曜日別デフォルトタスク（ロードマップに具体タスクがない日）

```
月曜：テーマ決定 + /podcast-script でPodcast台本生成（30分）
火曜：Podcast収録（15分）+ stand.fm公開（15分）
水曜：/note-article-team で全素材一括生成（30分）+ note公開（30分）
木曜：X投稿5本予約投稿（20分）+ いいね返し15件（10分）
金曜：研究収集 /fetch-research（20分）+ 翌週テーマ選定（10分）
土曜：KPI振り返り（15分）+ 有料note執筆（60分）
日曜：有料note執筆（60分）+ 翌週の準備（30分）
```

---

## PART B：最新ニュース収集 + ダッシュボード生成

PART Aのタスク表示が完了したら、続けて最新ニュース収集を実行する。

### STEP 5：最新ニュースを5本収集する

以下の手順で**世界最先端の不老長寿・健康・ダイエット情報**を収集する。

**5-1. WebSearchで検索する（3〜5回の検索を並列実行）**

```
検索クエリ例（英語メイン）：
- "longevity research 2025 2026 breakthrough"
- "anti-aging clinical trial latest results"
- "weight loss metabolism new study 2025 2026"
- "NMN NAD+ human trial results"
- "exercise health lifespan new research"
- "intermittent fasting metabolic health 2025 2026"
- "gut microbiome obesity latest"
- "sleep optimization longevity latest"
```

曜日ごとにテーマを変えてバリエーションを出す：
```
月曜：不老長寿（NMN / NAD+ / テロメア / セノリティクス）
火曜：食事・栄養（断食 / 地中海食 / 超加工食品 / 腸内細菌）
水曜：運動科学（ゾーン2 / 筋トレ / ウォーキング / HIIT）
木曜：睡眠・ストレス（概日リズム / コルチゾール / 瞑想）
金曜：ダイエット最前線（GLP-1薬 / 代謝 / 肥満研究）
土曜：サプリ・栄養素（ビタミンD / マグネシウム / クレアチン / オメガ3）
日曜：総合（その週の最も注目度が高い研究）
```

**5-2. 各記事から以下を抽出する（5本）**

```
各ニュースの抽出項目：
- タイトル（日本語訳・20文字以内）
- サマリー（日本語・2〜3行）
- 出典（著者・掲載誌・年）
- カテゴリ（🧬 不老長寿 / 🥗 食事 / 🏃 運動 / 😴 睡眠 / 💊 サプリ / ⚖️ ダイエット）
- マーシーのコンテンツへの活用度（★〜★★★）
- Podcast/note化のアイデア（1行）
```

---

### STEP 6：フォルダを作成してファイルを保存する

**6-1. フォルダ作成**

```
保存先：C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\daily_news\YYYYMMDD_不老長寿ニュース\
```

フォルダ名は日付ベース：`20260316_不老長寿ニュース`

**6-2. 保存ファイル一覧**

| # | ファイル名 | 内容 |
|---|---|---|
| 1 | `YYYYMMDD_ニュースまとめ.md` | 5本のニュース詳細（Markdown） |
| 2 | `YYYYMMDD_podcast_memo.md` | Podcast用メモ（ショートエピソード台本の素材） |
| 3 | `YYYYMMDD_x_posts.md` | X投稿用テキスト（5本・各ニュース1投稿） |
| 4 | `generate_dashboard.py` | ダッシュボードPNG生成スクリプト |

---

### STEP 7：ニュースまとめMarkdownを作成する

**`YYYYMMDD_ニュースまとめ.md` のフォーマット：**

```markdown
# 不老長寿ニュース｜YYYY年MM月DD日

> 世界最先端の不老長寿・健康・ダイエット研究を毎朝5本ピックアップ

---

## 1. [タイトル（日本語）]
**カテゴリ：** [絵文字] [カテゴリ名]
**出典：** [著者, 掲載誌, 年]
**活用度：** ★★★

[サマリー 2〜3行]

**マーシーのコンテンツへの活用：**
[Podcast/noteへの展開アイデア 1行]

---

## 2. [タイトル]
...（5本分繰り返し）

---

## 今日の注目（1本ピックアップ）

**[最も活用度が高いニュースのタイトル]**

[なぜこれが重要か・ペルソナ（田中 健二 42歳）にどう刺さるか・2〜3行で解説]

---

収集日：YYYY-MM-DD
収集者：Claude Code × マーシー
```

---

### STEP 8：Podcast用メモを作成する

**`YYYYMMDD_podcast_memo.md` のフォーマット：**

```markdown
# Podcast用メモ｜YYYY年MM月DD日

> 今日のニュースから、ショートエピソード（5〜8分）の素材をまとめます

## エピソードタイトル案
- 案A：[タイトル案]
- 案B：[タイトル案]

## 話す内容（箇条書き）
1. [導入：ペルソナの感情フック 1行]
2. [ニュースの要約：中学生でも分かる言葉で 2〜3行]
3. [マーシーの実体験との接続 1〜2行]
4. [今日の1歩：具体的なアクション 1行]

## 出典
- [論文/ニュースの出典情報]

## 注意
- これはメモです。実際の台本作成は `/podcast-script` を使用してください
```

---

### STEP 9：X投稿用テキストを作成する

**`YYYYMMDD_x_posts.md` のフォーマット：**

各ニュースから1投稿ずつ、計5本のX投稿テキストを作成する。

```markdown
# X投稿｜YYYY年MM月DD日ニュース

## 投稿1｜[カテゴリ]
```
[140文字以内のツイート]

#不老長寿 #健康 #ダイエット #最新研究 #Longevity
```

## 投稿2｜[カテゴリ]
...（5本分）
```

**X投稿のルール：**
- 140文字以内
- 冒頭は数字か驚きのファクトで始める
- 末尾に固定ハッシュタグ5つ：`#不老長寿 #健康 #ダイエット #最新研究 #Longevity`
- 1本だけnoteリンクを入れる（最も活用度が高いニュース）

---

### STEP 10：ダッシュボードPNGを生成する

**`generate_dashboard.py` を作成して実行する。**

ダッシュボードの仕様：

```
サイズ：1280×900px
背景：#f0f0f0（ライトグレー）

デザインシステム：
  メインカラー：#22c55e（緑・健康）
  サブカラー：#FF6D00（オレンジ・強調）
  カードBG：#ffffff（白）
  テキスト：#1a1a1a（ほぼ黒）
  サブテキスト：#6b7280（グレー）
  カテゴリバッジ色：
    🧬 不老長寿：#8b5cf6（紫）
    🥗 食事：#22c55e（緑）
    🏃 運動：#3b82f6（青）
    😴 睡眠：#6366f1（インディゴ）
    💊 サプリ：#f59e0b（アンバー）
    ⚖️ ダイエット：#ef4444（赤）

レイアウト：
  上部：ヘッダー（緑グラデーション帯）
    「不老長寿ニュース｜YYYY.MM.DD」
    「Longevity Navigator × マーシー」

  中央：ニュースカード5枚（2列グリッド + 1枚下部全幅）
    各カード：
      - 左上にカテゴリバッジ（丸角・色付き）
      - タイトル（太字・黒）
      - サマリー（2行・グレー）
      - 右下に出典（小さく・薄グレー）
      - 右上に活用度（★マーク）

  下部：フッター
    「マーシー｜100kg→68kg｜Sub3」
    「毎朝更新・世界最先端の健康研究をお届け」

フォント：Noto Sans JP（ゴシック体）
テイスト：清潔感・信頼感のあるヘルスケアUI
```

**generate_dashboard.py テンプレート：**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""不老長寿ニュース ダッシュボード生成スクリプト"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR
FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

# ── ニュースデータ（STEP 5で収集した内容を埋める）──
DATE = "YYYY.MM.DD"
NEWS = [
    {
        "category": "カテゴリ",
        "cat_color": "#カラーコード",
        "title": "タイトル",
        "summary": "サマリー2〜3行",
        "source": "出典",
        "stars": "★★★",
    },
    # ... 5本分
]

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:900px;overflow:hidden;background:#f0f0f0;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
)

def build_html():
    # ヘッダー
    header = (
        "<div style='width:100%;height:80px;background:linear-gradient(135deg,#22c55e,#16a34a);"
        "display:flex;align-items:center;justify-content:space-between;padding:0 40px;'>"
        "<div style='font-size:28px;font-weight:900;color:#fff;'>不老長寿ニュース｜" + DATE + "</div>"
        "<div style='font-size:16px;color:rgba(255,255,255,.8);'>Longevity Navigator × マーシー</div>"
        "</div>"
    )

    # ニュースカード
    cards = ""
    for i, n in enumerate(NEWS):
        # 上4枚は2列、5枚目は下部全幅
        if i < 4:
            w = "580px"
            left = str(20 + (i % 2) * 620) + "px"
            top = str(100 + (i // 2) * 195) + "px"
        else:
            w = "1240px"
            left = "20px"
            top = "490px"

        cards += (
            "<div style='position:absolute;left:" + left + ";top:" + top + ";width:" + w + ";"
            "height:175px;background:#fff;border-radius:12px;padding:20px 24px;"
            "box-shadow:0 2px 8px rgba(0,0,0,.06);overflow:hidden;'>"
            # カテゴリバッジ
            "<div style='display:inline-block;background:" + n["cat_color"] + ";color:#fff;"
            "font-size:13px;font-weight:700;padding:3px 12px;border-radius:12px;'>" + n["category"] + "</div>"
            # 活用度
            "<div style='position:absolute;top:20px;right:24px;font-size:14px;color:#f59e0b;'>" + n["stars"] + "</div>"
            # タイトル
            "<div style='font-size:22px;font-weight:800;color:#1a1a1a;margin-top:10px;line-height:1.3;'>" + n["title"] + "</div>"
            # サマリー
            "<div style='font-size:15px;color:#6b7280;margin-top:6px;line-height:1.5;'>" + n["summary"] + "</div>"
            # 出典
            "<div style='position:absolute;bottom:12px;right:24px;font-size:12px;color:#9ca3af;'>" + n["source"] + "</div>"
            "</div>"
        )

    # フッター
    footer = (
        "<div style='position:absolute;bottom:0;width:100%;height:50px;background:#fff;"
        "border-top:1px solid #e5e7eb;display:flex;align-items:center;justify-content:space-between;padding:0 40px;'>"
        "<div style='font-size:14px;font-weight:700;color:#22c55e;'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div style='font-size:13px;color:#9ca3af;'>毎朝更新・世界最先端の健康研究をお届け</div>"
        "</div>"
    )

    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        + header + cards + footer
        + "</body></html>"
    )

if __name__ == "__main__":
    print("不老長寿ニュース ダッシュボード生成開始...\n")
    html = build_html()
    tmp = ARTICLE_DIR / "_tmp_dashboard.html"
    out = OUTPUT_DIR / ("dashboard_" + DATE.replace(".", "") + ".png")
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto("file:///" + str(tmp).replace("\\", "/"))
        page.wait_for_timeout(800)
        page.screenshot(path=str(out), full_page=False)
        browser.close()
    tmp.unlink(missing_ok=True)
    print("✅ ダッシュボード生成完了: " + out.name)
```

**重要：**
- NEWS配列は STEP 5で収集した実際のニュースデータで埋めること
- カテゴリバッジの色はデザインシステムに従うこと
- スクリプトを保存してから `python -X utf8 generate_dashboard.py` で実行すること

---

### STEP 11：完了サマリーを表示する

PART A（タスク表示）とPART B（ニュース収集）の両方が完了したら、
以下を追加表示する：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 今日の不老長寿ニュース（5本）
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [カテゴリ] [タイトル]（★★★）
2. [カテゴリ] [タイトル]（★★☆）
3. [カテゴリ] [タイトル]（★★☆）
4. [カテゴリ] [タイトル]（★☆☆）
5. [カテゴリ] [タイトル]（★☆☆）

📁 保存先：daily_news/YYYYMMDD_不老長寿ニュース/
📊 ダッシュボード：dashboard_YYYYMMDD.png
📝 Podcast用メモ：YYYYMMDD_podcast_memo.md
🐦 X投稿5本：YYYYMMDD_x_posts.md

⭐ 今日の注目：[最も活用度が高いニュースのタイトル]
→ [1行でなぜ重要かを説明]

━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 実行順序まとめ

```
/ohayou
  ↓
PART A：今日のタスク表示（STEP 1〜4）
  ↓
PART B：最新ニュース収集（STEP 5〜11）
  ├── STEP 5：WebSearchで5本収集
  ├── STEP 6：フォルダ作成
  ├── STEP 7：ニュースまとめ.md 保存
  ├── STEP 8：Podcast用メモ 保存
  ├── STEP 9：X投稿テキスト 保存
  ├── STEP 10：ダッシュボードPNG生成
  └── STEP 11：完了サマリー表示
```
