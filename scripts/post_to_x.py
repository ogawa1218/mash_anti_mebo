#!/usr/bin/env python3
"""
X投稿支援スクリプト

使い方:
    python scripts/post_to_x.py note/20260310_トピック名/ --url https://note.com/longevity_navi/n/xxxxx

機能:
    - X告知文を読み込み
    - noteURLを自動挿入
    - 投稿テキストを1つずつ表示
    - コピペしやすい形式で出力
"""

import sys
import argparse
from pathlib import Path
import time

def load_x_posts(note_dir: Path, note_url: str):
    """
    X告知文を読み込み、noteURLを挿入

    Args:
        note_dir: noteディレクトリのパス
        note_url: noteのURL

    Returns:
        dict: {
            'single': 1投稿版,
            'thread': [1/10, 2/10, ..., 10/10]
        }
    """
    x_file = note_dir / "X告知文.md"

    if not x_file.exists():
        print(f"❌ エラー: {x_file} が見つかりません")
        sys.exit(1)

    with open(x_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1投稿版を抽出
    single_match = content.split("## 1投稿版")[1].split("---")[0]
    single_post = single_match.strip().replace("[note URL]", note_url)

    # 10連スレッドを抽出
    thread_section = content.split("## 10連スレッド版")[1]
    thread_posts = []

    for i in range(1, 11):
        marker = f"### {i}/10"
        if marker in thread_section:
            start = thread_section.find(marker) + len(marker)
            end = thread_section.find("---", start)
            if end == -1:
                end = len(thread_section)

            post = thread_section[start:end].strip()
            # 最後の投稿にnoteURL挿入
            if i == 10:
                post = post.replace("[note URL]", note_url)

            thread_posts.append(post)

    return {
        'single': single_post,
        'thread': thread_posts
    }

def display_single_post(post: str):
    """1投稿版を表示"""
    print("\n" + "="*60)
    print("📝 1投稿版（すぐに投稿したい場合はこれをコピペ）")
    print("="*60)
    print()
    print(post)
    print()
    print("文字数:", len(post), "文字")
    print("="*60)

def display_thread_posts(posts: list, interactive: bool = False):
    """10連スレッドを表示"""
    print("\n" + "="*60)
    print("📝 10連スレッド版（時間があればこちらを投稿）")
    print("="*60)

    for i, post in enumerate(posts, 1):
        print(f"\n【{i}/10】")
        print("-" * 60)
        print(post)
        print("-" * 60)
        print(f"文字数: {len(post)} 文字")

        if interactive and i < len(posts):
            input("\n⏎ Enterキーを押すと次の投稿を表示...")

    print("\n" + "="*60)
    print("✨ 全10投稿の表示が完了しました")
    print("="*60)

def save_posts_to_file(posts_data: dict, output_path: Path):
    """投稿内容をテキストファイルに保存"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("X投稿テキスト（コピペ用）\n")
        f.write("="*60 + "\n\n")

        f.write("【1投稿版】\n")
        f.write("-"*60 + "\n")
        f.write(posts_data['single'] + "\n")
        f.write("-"*60 + "\n")
        f.write(f"文字数: {len(posts_data['single'])} 文字\n\n")

        f.write("="*60 + "\n")
        f.write("【10連スレッド版】\n")
        f.write("="*60 + "\n\n")

        for i, post in enumerate(posts_data['thread'], 1):
            f.write(f"\n【{i}/10】\n")
            f.write("-"*60 + "\n")
            f.write(post + "\n")
            f.write("-"*60 + "\n")
            f.write(f"文字数: {len(post)} 文字\n\n")

    print(f"\n📄 投稿テキストを保存: {output_path}")

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='X投稿支援スクリプト')
    parser.add_argument('note_dir', help='noteディレクトリのパス（例: note/20260310_トピック名/）')
    parser.add_argument('--url', required=True, help='noteのURL（例: https://note.com/longevity_navi/n/xxxxx）')
    parser.add_argument('--interactive', '-i', action='store_true', help='対話モード（1つずつEnterで進む）')
    parser.add_argument('--save', '-s', action='store_true', help='投稿テキストをファイルに保存')

    args = parser.parse_args()

    note_dir = Path(args.note_dir)

    if not note_dir.exists():
        print(f"❌ エラー: {note_dir} が見つかりません")
        sys.exit(1)

    # X投稿を読み込み
    print(f"📖 X告知文を読み込み中... {note_dir}")
    posts = load_x_posts(note_dir, args.url)

    # 1投稿版を表示
    display_single_post(posts['single'])

    # 10連スレッドを表示
    display_thread_posts(posts['thread'], interactive=args.interactive)

    # ファイルに保存（オプション）
    if args.save:
        output_path = note_dir / "X投稿テキスト_コピペ用.txt"
        save_posts_to_file(posts, output_path)

    print("\n✨ 完了！")
    print("\n次のステップ:")
    print("1. 上記のテキストをコピー")
    print("2. Xを開く（https://x.com/compose/post）")
    print("3. ペーストして投稿")
    print("\n💡 ヒント:")
    print("- 1投稿版：すぐに投稿したい場合")
    print("- 10連スレッド版：時間があれば（エンゲージメント高い）")

if __name__ == "__main__":
    main()
