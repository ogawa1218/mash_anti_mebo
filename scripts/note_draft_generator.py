#!/usr/bin/env python3
"""
note記事自動生成スクリプト

使い方:
    python scripts/note_draft_generator.py "トピック名"

例:
    python scripts/note_draft_generator.py "夜に崩れる人ほど、最初に変えるべきは睡眠だった"
"""

import sys
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv
import anthropic

# .envファイルを読み込み
load_dotenv()

def generate_note_article(topic: str) -> dict:
    """
    トピックを指定すると、note記事の完全な下書きを生成

    Args:
        topic: 記事のトピック（例：「夜に崩れる人ほど、最初に変えるべきは睡眠だった」）

    Returns:
        dict: 記事データ（title, content, infographic_prompts, thumbnail_prompts, x_post, x_thread, standfm）
    """
    client = anthropic.Anthropic()

    prompt = f"""
以下のトピックでnote記事を執筆してください。

【トピック】
{topic}

【必須ルール】
1. ペルソナ：30〜40代、健診E判定メタボ男性、夜食/間食で崩れやすい
2. 著者：マーシー（100kg→68kg、8年維持、サブ3ランナー）
3. コアメッセージ：意志力ではなく仕組みで変える
4. 文字数：5000字前後
5. 見出しに番号を振る（1. 2. 3. ...）
6. 8構成要素を含める：
   - 問題提起（感情から入る）
   - 共感
   - ベネフィット
   - 結論
   - 理由・事例
   - 行動手順
   - まとめ
   - CTA（次のステップ）

【記事構成】
## 1. [問題提起の見出し]
（導入・共感）

## 2. [科学的説明の見出し]
（理由・根拠）

## 3. [実体験ストーリーの見出し]
（著者の体験）

## 4. [ベネフィットの見出し]
（得られる変化）

## 5. [行動手順の見出し]
（今日からできること）

## 6. [核心メッセージの見出し]
（仕組みで変える）

## 7. まとめ：[まとめの見出し]
（今日やること）

## 8. 次のステップ：さらに深く学びたい方へ
（CTA）

【出力形式】
以下のJSON形式で出力してください（コードブロックなし）：

{{
  "title": "記事タイトル（数字含む・30文字以内）",
  "content": "記事本文（Markdown形式・見出しに番号付き）",
  "infographic_positions": [
    "図解①の挿入位置（章番号と見出し）",
    "図解②の挿入位置",
    "図解③の挿入位置"
  ],
  "infographic_prompts": [
    "図解①のプロンプト（Nano Banana Pro用・1280x720px・日本語）",
    "図解②のプロンプト",
    "図解③のプロンプト"
  ],
  "thumbnail_prompts": [
    "サムネイルプロンプトA（1280x670px・黒背景・3行コピー）",
    "サムネイルプロンプトB",
    "サムネイルプロンプトC"
  ],
  "x_post": "X告知文（140字以内・フック→ベネフィット→CTA）",
  "x_thread": [
    "1/10投稿文",
    "2/10投稿文",
    "3/10投稿文",
    "4/10投稿文",
    "5/10投稿文",
    "6/10投稿文",
    "7/10投稿文",
    "8/10投稿文",
    "9/10投稿文",
    "10/10投稿文（まとめ＋noteリンク誘導）"
  ],
  "standfm": "stand.fm概要欄（タイトル・概要・要点4つ・ハッシュタグ）"
}}

【重要】
- 中学生でもわかる言葉で書く
- 感情語を使う（「怖かった」「諦めかけていた」など）
- 出典は1つ以上明記する
- 免責事項を末尾に含める
- 図解プロンプトは具体的に（色指定・レイアウト指定含む）
"""

    print(f"📝 記事生成中... トピック: {topic}")

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )

    # テキストブロックを取得
    text_block = next(b for b in response.content if b.type == "text")
    json_str = text_block.text.strip()

    # コードブロックを削除（もし含まれていれば）
    json_str = json_str.replace("```json", "").replace("```", "").strip()

    print("✅ 記事生成完了")

    # JSONパース
    return json.loads(json_str)


def save_article(data: dict, topic: str, output_dir: Path):
    """
    生成された記事を整形して保存

    Args:
        data: 記事データ
        topic: トピック名（ファイル名に使用）
        output_dir: 出力先ディレクトリ
    """
    # 出力ディレクトリを作成
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. 記事本文
    content_path = output_dir / "記事本文.md"
    with open(content_path, "w", encoding="utf-8") as f:
        f.write(f"# {data['title']}\n\n")
        f.write(data['content'])
        f.write("\n\n---\n\n")
        f.write("**Longevity Navigator（不老長寿ナビゲーター）**\n")
        f.write("100kg→68kgを8年間維持中 | サブ3ランナー | 30〜40代メタボ逆転を仕組みで支援\n\n")
        f.write("📝 note：https://note.com/longevity_navi\n")
        f.write("🎙️ Podcast：準備中\n")
        f.write("🐦 X（Twitter）：@longevity_navi\n")
    print(f"✅ 記事本文を保存: {content_path}")

    # 2. 図解プロンプト
    infographic_path = output_dir / "図解プロンプト.md"
    with open(infographic_path, "w", encoding="utf-8") as f:
        f.write("# 図解プロンプト\n\n")
        f.write("## 挿入位置\n\n")
        for i, pos in enumerate(data.get('infographic_positions', []), 1):
            f.write(f"- 図解{i:02d}: {pos}\n")
        f.write("\n---\n\n")
        for i, prompt in enumerate(data.get('infographic_prompts', []), 1):
            f.write(f"## 図解{i:02d}\n\n")
            f.write(f"### プロンプト\n\n```\n{prompt}\n```\n\n")
            f.write("---\n\n")
    print(f"✅ 図解プロンプトを保存: {infographic_path}")

    # 3. サムネイルプロンプト
    thumbnail_path = output_dir / "サムネイルプロンプト.md"
    with open(thumbnail_path, "w", encoding="utf-8") as f:
        f.write("# サムネイルプロンプト（3案）\n\n")
        labels = ["A", "B", "C"]
        for i, prompt in enumerate(data.get('thumbnail_prompts', []), 0):
            if i < len(labels):
                f.write(f"## 案{labels[i]}\n\n")
                f.write(f"### プロンプト\n\n```\n{prompt}\n```\n\n")
                f.write("---\n\n")
    print(f"✅ サムネイルプロンプトを保存: {thumbnail_path}")

    # 4. X告知文
    x_path = output_dir / "X告知文.md"
    with open(x_path, "w", encoding="utf-8") as f:
        f.write("# X告知文\n\n")
        f.write("## 1投稿版\n\n")
        f.write(f"{data.get('x_post', '')}\n\n")
        f.write("[note URL]\n\n")
        f.write("---\n\n")
        f.write("## 10連スレッド版\n\n")
        for i, tweet in enumerate(data.get('x_thread', []), 1):
            f.write(f"### {i}/10\n\n")
            f.write(f"{tweet}\n\n")
            if i == 10:
                f.write("[note URL]\n\n")
            f.write("---\n\n")
    print(f"✅ X告知文を保存: {x_path}")

    # 5. stand.fm概要欄
    standfm_path = output_dir / "standfm概要欄.md"
    with open(standfm_path, "w", encoding="utf-8") as f:
        f.write("# stand.fm 概要欄\n\n")
        f.write(data.get('standfm', ''))
        f.write("\n\n---\n\n")
        f.write("📝 詳しくはnoteで全文公開中：\n")
        f.write("https://note.com/longevity_navi\n")
    print(f"✅ stand.fm概要欄を保存: {standfm_path}")

    # 6. 設定メモ
    meta_path = output_dir / "設定メモ.md"
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write("# 設定メモ\n\n")
        f.write(f"**作成日:** {datetime.date.today().strftime('%Y年%m月%d日')}\n")
        f.write(f"**トピック:** {topic}\n")
        f.write(f"**タイトル:** {data['title']}\n\n")
        f.write("## noteに投稿する手順\n\n")
        f.write("1. `記事本文.md` をコピー\n")
        f.write("2. noteのエディタにペースト\n")
        f.write("3. Nano Banana Proで図解を生成\n")
        f.write("4. 図解を挿入位置に配置\n")
        f.write("5. サムネイルを設定\n")
        f.write("6. タグを設定：#ダイエット #メタボ #健康診断 #食事管理 #習慣化\n")
        f.write("7. プレビュー確認\n")
        f.write("8. 公開ボタンをクリック\n\n")
        f.write("## X告知の手順\n\n")
        f.write("1. noteのURLを取得\n")
        f.write("2. `X告知文.md` の [note URL] を実際のURLに置き換え\n")
        f.write("3. 1投稿版を投稿\n")
        f.write("4. （余力があれば）10連スレッドを投稿\n")
    print(f"✅ 設定メモを保存: {meta_path}")

    print(f"\n🎉 すべてのファイルを保存完了: {output_dir}")


def main():
    """
    メイン処理
    """
    # コマンドライン引数からトピックを取得
    if len(sys.argv) < 2:
        print("❌ エラー: トピックを指定してください")
        print("使い方: python scripts/note_draft_generator.py \"トピック名\"")
        print("例: python scripts/note_draft_generator.py \"夜に崩れる人ほど、最初に変えるべきは睡眠だった\"")
        sys.exit(1)

    topic = sys.argv[1]

    # 出力先ディレクトリを決定（日付ベース）
    today = datetime.date.today().strftime("%Y%m%d")
    safe_topic = topic[:30].replace(' ', '_').replace('　', '_').replace('/', '_').replace('\\', '_')
    output_dir = Path(f"note/{today}_{safe_topic}")

    try:
        # 記事を生成
        data = generate_note_article(topic)

        # ファイルに保存
        save_article(data, topic, output_dir)

        print("\n✨ 完了！次のステップ:")
        print(f"1. {output_dir} フォルダを確認")
        print("2. `記事本文.md` をnoteにコピペ")
        print("3. 図解を生成して挿入")
        print("4. 公開！")

    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
