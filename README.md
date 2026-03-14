# Longevity Navigator - note記事自動生成システム

## 🚀 セットアップ（初回のみ）

### 1. 必要なパッケージをインストール

```bash
cd /c/Users/masas/product/2nd-Brain/04_アウトプット/Longevity

# Pythonパッケージをインストール
pip3 install anthropic python-dotenv --break-system-packages
```

### 2. APIキーを設定

```bash
# .envファイルを作成
cp .env.example .env

# エディタで.envを開いて、APIキーを設定
# ANTHROPIC_API_KEY=sk-ant-... （あなたのClaude APIキー）
```

**Claude APIキーの取得方法：**
1. https://console.anthropic.com/ にアクセス
2. 「API Keys」から新しいキーを作成
3. `.env`ファイルに貼り付け

---

## 📝 使い方

### 基本的な使い方

```bash
cd /c/Users/masas/product/2nd-Brain/04_アウトプット/Longevity

# 記事を生成
python3 scripts/note_draft_generator.py "トピック名"
```

### 例：第5回記事を生成

```bash
python3 scripts/note_draft_generator.py "寝つきが悪い人のための5つのコツ"
```

### 生成されるファイル

```
note/20260309_寝つきが悪い人のための5つのコツ/
├── 記事本文.md                  ← noteにコピペする
├── 図解プロンプト.md            ← Nano Banana Proで生成
├── サムネイルプロンプト.md      ← Nano Banana Proで生成
├── X告知文.md                   ← Xに投稿
├── standfm概要欄.md             ← stand.fmに投稿
└── 設定メモ.md                  ← 作業手順
```

---

## 🎨 note投稿の手順

### ステップ1：記事を生成
```bash
python3 scripts/note_draft_generator.py "トピック名"
```

### ステップ2：図解を生成
1. Genspark（https://www.genspark.com/）にアクセス
2. 「Nano Banana Pro」を選択
3. `図解プロンプト.md`の内容をコピペ
4. 生成された画像をダウンロード

### ステップ3：noteに投稿
1. `記事本文.md`の内容をコピー
2. noteのエディタにペースト
3. 図解を挿入
4. サムネイルを設定
5. タグを設定：`#ダイエット #メタボ #健康診断 #食事管理 #習慣化`
6. プレビュー確認
7. 公開ボタンをクリック

### ステップ4：Xで告知
1. noteのURLを取得
2. `X告知文.md`の [note URL] を実際のURLに置き換え
3. 1投稿版を投稿
4. （余力があれば）10連スレッドを投稿

---

## ⏱️ 所要時間

- **記事生成**：2分（自動）
- **図解生成**：10分（Nano Banana Proで手動）
- **note投稿**：5分
- **X告知**：3分

**合計：約20分で1本公開完了**

---

## 🔧 トラブルシューティング

### エラー: `ModuleNotFoundError: No module named 'anthropic'`

パッケージがインストールされていません。

```bash
pip3 install anthropic python-dotenv --break-system-packages
```

### エラー: `anthropic.AuthenticationError`

APIキーが設定されていないか、間違っています。

```bash
# .envファイルを確認
cat .env

# 正しいAPIキーが設定されているか確認
# ANTHROPIC_API_KEY=sk-ant-...
```

### エラー: `JSONDecodeError`

Claude APIのレスポンスがJSON形式でない可能性があります。
もう一度実行してください。

```bash
python3 scripts/note_draft_generator.py "トピック名"
```

---

## 📂 ディレクトリ構成

```
04_アウトプット/Longevity/
├── README.md                    ← このファイル
├── CLAUDE.md                    ← プロジェクト設計書
├── .env                         ← APIキー（git管理外）
├── .env.example                 ← APIキーのテンプレート
├── .gitignore                   ← .envを除外
├── scripts/
│   └── note_draft_generator.py  ← 記事自動生成スクリプト
└── note/
    ├── 第1回_*.md
    ├── 第2回_*.md
    ├── 第3回_*.md
    ├── 第4回_夜に崩れる人ほど最初に変えるべきは睡眠だった/
    │   ├── 記事本文.md
    │   ├── 図解プロンプト10枚.md
    │   ├── サムネイルプロンプト3案.md
    │   ├── X告知文.md
    │   └── standfm概要欄.md
    └── 20260309_*/                ← 新規生成された記事
```

---

## 🎯 次のステップ

1. **APIキーを設定**（まだの場合）
2. **テスト実行**：第5回記事を生成してみる
3. **noteに投稿**：実際に公開してみる
4. **反応を確認**：PV、スキ、コメントをチェック

---

## 📞 サポート

問題が発生した場合は、以下を確認してください：
1. `.env`ファイルが正しく設定されているか
2. Pythonパッケージがインストールされているか
3. インターネット接続が正常か

---

**作成日：** 2026年3月9日
**最終更新：** 2026年3月9日
