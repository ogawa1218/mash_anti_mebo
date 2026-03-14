#!/usr/bin/env python3
"""
note記事作成ワークフロー（全自動）

使い方:
    python scripts/create_article.py "トピック名" [--skip-images]

機能:
    1. 記事を自動生成（Claude API）
    2. 図解・サムネイルを自動生成（Gemini API）※オプション
    3. X投稿準備（手動投稿用テキスト出力）

全自動で記事作成が完了します！
"""

import sys
import argparse
import subprocess
from pathlib import Path
import datetime

def run_command(command: list, description: str):
    """
    コマンドを実行

    Args:
        command: 実行するコマンド（リスト形式）
        description: 処理の説明
    """
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ エラーが発生しました:")
        print(result.stderr)
        return False

    print(result.stdout)
    return True

def find_latest_note_dir(base_dir: Path, topic: str):
    """
    最新のnoteディレクトリを探す

    Args:
        base_dir: noteディレクトリのベース
        topic: トピック名

    Returns:
        Path: 見つかったディレクトリ
    """
    # 日付ベースのディレクトリを探す
    today = datetime.date.today().strftime("%Y%m%d")
    safe_topic = topic[:30].replace(' ', '_').replace('　', '_').replace('/', '_').replace('\\', '_')

    pattern = f"{today}_{safe_topic}"

    for item in base_dir.iterdir():
        if item.is_dir() and item.name.startswith(pattern):
            return item

    return None

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='note記事作成ワークフロー（全自動）')
    parser.add_argument('topic', help='記事のトピック（例: "寝つきが悪い人のための5つのコツ"）')
    parser.add_argument('--skip-images', action='store_true', help='画像生成をスキップ（プロンプトのみ生成）')
    parser.add_argument('--note-url', help='noteのURL（既に投稿済みの場合、X投稿準備に使用）')

    args = parser.parse_args()

    topic = args.topic
    base_dir = Path("note")

    print("="*60)
    print("🎨 note記事作成ワークフロー（全自動）")
    print("="*60)
    print(f"📝 トピック: {topic}")
    print(f"📅 作成日: {datetime.date.today().strftime('%Y年%m月%d日')}")
    print("="*60)

    # ステップ1: 記事を生成
    success = run_command(
        ['python', 'scripts/note_draft_generator.py', topic],
        "ステップ1: 記事を生成中..."
    )

    if not success:
        print("\n❌ 記事生成に失敗しました")
        sys.exit(1)

    # 生成されたディレクトリを探す
    note_dir = find_latest_note_dir(base_dir, topic)

    if not note_dir:
        print("\n❌ 生成されたディレクトリが見つかりません")
        sys.exit(1)

    print(f"\n✅ 記事が生成されました: {note_dir}")

    # ステップ2: 画像を生成（オプション）
    if not args.skip_images:
        print("\n" + "="*60)
        print("⚠️  画像生成について")
        print("="*60)
        print("画像生成には数分かかる場合があります。")
        print("スキップする場合は Ctrl+C を押してください。")
        print("="*60)

        try:
            import time
            print("\n5秒後に開始...")
            time.sleep(5)

            success = run_command(
                ['python', 'scripts/generate_images.py', str(note_dir)],
                "ステップ2: 画像を生成中..."
            )

            if not success:
                print("\n⚠️  画像生成に失敗しましたが、続行します")
                print("手動でNano Banana Proを使って生成してください")
        except KeyboardInterrupt:
            print("\n⏭️  画像生成をスキップしました")
            print("後で手動で生成できます:")
            print(f"    python scripts/generate_images.py {note_dir}")
    else:
        print("\n⏭️  画像生成をスキップしました（--skip-imagesオプション）")

    # ステップ3: X投稿準備（note URLが指定されている場合）
    if args.note_url:
        success = run_command(
            ['python', 'scripts/post_to_x.py', str(note_dir), '--url', args.note_url, '--save'],
            "ステップ3: X投稿準備中..."
        )

        if not success:
            print("\n⚠️  X投稿準備に失敗しましたが、続行します")
    else:
        print("\n" + "="*60)
        print("📝 ステップ3: X投稿準備")
        print("="*60)
        print("noteに記事を投稿したら、以下のコマンドでX投稿を準備してください:")
        print(f"    python scripts/post_to_x.py {note_dir} --url https://note.com/longevity_navi/n/xxxxx")
        print("="*60)

    # 完了メッセージ
    print("\n" + "="*60)
    print("🎉 完了！")
    print("="*60)
    print(f"\n📁 生成されたファイル: {note_dir}")
    print("\n次のステップ:")
    print("1. 記事本文.md をnoteにコピペ")

    if args.skip_images:
        print("2. 図解プロンプト.md を使ってNano Banana Proで画像生成")
        print("   → https://www.genspark.com/")
    else:
        print("2. images/ フォルダ内の画像をnote記事に挿入")

    print("3. noteに投稿")
    print("4. 投稿URLを取得")

    if not args.note_url:
        print(f"5. X投稿準備:")
        print(f"   python scripts/post_to_x.py {note_dir} --url [noteのURL]")

    print("\n✨ お疲れ様でした！")

if __name__ == "__main__":
    main()
