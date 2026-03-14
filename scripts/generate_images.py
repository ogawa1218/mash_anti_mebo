#!/usr/bin/env python3
"""
図解・サムネイル自動生成スクリプト（Gemini API使用）

使い方:
    python scripts/generate_images.py note/20260310_トピック名/

生成されるもの:
    - 図解画像（1280x720px）
    - サムネイル画像（1280x670px）
"""

import sys
import json
import re
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import os

# .envファイルを読み込み
load_dotenv()

def setup_gemini():
    """Gemini APIの初期化"""
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ エラー: GOOGLE_API_KEYまたはGEMINI_API_KEYが設定されていません")
        print("".envファイルにAPIキーを設定してください")
        sys.exit(1)

    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-exp')

def generate_image(model, prompt: str, output_path: Path):
    """
    プロンプトから画像を生成

    Args:
        model: Gemini model
        prompt: 画像生成プロンプト
        output_path: 保存先パス
    """
    print(f"📸 画像生成中... {output_path.name}")

    # Gemini 2.0 Flash with Imagenで画像生成
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="image/png"
        )
    )

    # 画像を保存
    with open(output_path, 'wb') as f:
        f.write(response.parts[0].inline_data.data)

    print(f"✅ 保存完了: {output_path}")

def load_prompts(note_dir: Path):
    """
    noteディレクトリから図解・サムネイルプロンプトを読み込み

    Args:
        note_dir: noteディレクトリのパス

    Returns:
        dict: {
            'infographics': [プロンプト1, プロンプト2, ...],
            'thumbnails': [プロンプトA, プロンプトB, プロンプトC]
        }
    """
    infographic_file = note_dir / "図解プロンプト.md"
    thumbnail_file = note_dir / "サムネイルプロンプト.md"

    if not infographic_file.exists():
        print(f"❌ エラー: {infographic_file} が見つかりません")
        sys.exit(1)

    if not thumbnail_file.exists():
        print(f"❌ エラー: {thumbnail_file} が見つかりません")
        sys.exit(1)

    # 図解プロンプトを読み込み
    with open(infographic_file, 'r', encoding='utf-8') as f:
        infographic_content = f.read()

    # サムネイルプロンプトを読み込み
    with open(thumbnail_file, 'r', encoding='utf-8') as f:
        thumbnail_content = f.read()

    # プロンプトを抽出（```で囲まれた部分）
    infographic_prompts = re.findall(r'```\n(.*?)\n```', infographic_content, re.DOTALL)
    thumbnail_prompts = re.findall(r'```\n(.*?)\n```', thumbnail_content, re.DOTALL)

    return {
        'infographics': infographic_prompts,
        'thumbnails': thumbnail_prompts
    }

def main():
    """メイン処理"""
    if len(sys.argv) < 2:
        print("❌ エラー: noteディレクトリを指定してください")
        print("使い方: python scripts/generate_images.py note/20260310_トピック名/")
        sys.exit(1)

    note_dir = Path(sys.argv[1])

    if not note_dir.exists():
        print(f"❌ エラー: {note_dir} が見つかりません")
        sys.exit(1)

    # 画像保存用ディレクトリを作成
    images_dir = note_dir / "images"
    images_dir.mkdir(exist_ok=True)

    # Geminiモデルを初期化
    print("🤖 Gemini APIを初期化中...")
    model = setup_gemini()

    # プロンプトを読み込み
    print("📖 プロンプトを読み込み中...")
    prompts = load_prompts(note_dir)

    # 図解を生成
    print(f"\n📊 図解を生成中... ({len(prompts['infographics'])}枚)")
    for i, prompt in enumerate(prompts['infographics'], 1):
        output_path = images_dir / f"図解{i:02d}.png"
        try:
            generate_image(model, prompt, output_path)
        except Exception as e:
            print(f"⚠️  図解{i:02d}の生成に失敗: {e}")

    # サムネイルを生成
    print(f"\n🎨 サムネイルを生成中... ({len(prompts['thumbnails'])}枚)")
    labels = ['A', 'B', 'C']
    for i, prompt in enumerate(prompts['thumbnails']):
        if i < len(labels):
            output_path = images_dir / f"サムネイル_{labels[i]}.png"
            try:
                generate_image(model, prompt, output_path)
            except Exception as e:
                print(f"⚠️  サムネイル_{labels[i]}の生成に失敗: {e}")

    print(f"\n🎉 完了！画像は {images_dir} に保存されました")
    print("\n次のステップ:")
    print(f"1. {images_dir} フォルダを確認")
    print("2. 生成された画像をnote記事に挿入")
    print("3. サムネイルを設定")

if __name__ == "__main__":
    main()
