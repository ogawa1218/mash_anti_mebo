#!/usr/bin/env node
/**
 * md-to-note.mjs
 * Markdownのnote記事をnote.com貼り付け用HTMLに変換し、クリップボードにコピーする
 *
 * 使い方:
 *   node scripts/md-to-note.mjs <markdownファイルパス>
 *
 * 例:
 *   node scripts/md-to-note.mjs src/app/content/20260320-cinnamon-honey/note-article.md
 */

import { readFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import { resolve, basename } from 'path';

// ---- シンプルなMarkdown→HTML変換 ----
function mdToHtml(md) {
  let html = md;

  // フロントマター除去（---で囲まれたブロック）
  html = html.replace(/^---[\s\S]*?---\n/, '');

  // 水平線（先に処理しないと見出しと干渉する）
  html = html.replace(/^---$/gm, '<hr>');

  // 見出し h1〜h4
  html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

  // コードブロック（```...```）
  html = html.replace(/```[\w]*\n([\s\S]*?)```/g, (_, code) => {
    const escaped = code.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return `<pre><code>${escaped}</code></pre>`;
  });

  // インラインコード
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // 太字 **text**
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

  // 斜体 *text*（太字処理後）
  html = html.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');

  // テーブル（Markdown table）
  html = html.replace(/((?:^\|.+\|\n)+)/gm, (block) => {
    const rows = block.trim().split('\n');
    if (rows.length < 2) return block;
    const headerCols = rows[0].split('|').filter((c) => c.trim() !== '');
    // 2行目はセパレーター行（|---|---|）なのでスキップ
    const bodyRows = rows.slice(2);
    const thead = '<thead><tr>' + headerCols.map((c) => `<th>${c.trim()}</th>`).join('') + '</tr></thead>';
    const tbody = '<tbody>' + bodyRows.map((row) => {
      const cols = row.split('|').filter((c) => c.trim() !== '');
      return '<tr>' + cols.map((c) => `<td>${c.trim()}</td>`).join('') + '</tr>';
    }).join('') + '</tbody>';
    return `<table>${thead}${tbody}</table>`;
  });

  // 順序なしリスト（ネスト非対応、シンプル版）
  html = html.replace(/((?:^[-*] .+\n?)+)/gm, (block) => {
    const items = block.trim().split('\n').map((line) => {
      return `<li>${line.replace(/^[-*] /, '')}</li>`;
    });
    return `<ul>${items.join('')}</ul>`;
  });

  // 順序ありリスト
  html = html.replace(/((?:^\d+[).] .+\n?)+)/gm, (block) => {
    const items = block.trim().split('\n').map((line) => {
      return `<li>${line.replace(/^\d+[).] /, '')}</li>`;
    });
    return `<ol>${items.join('')}</ol>`;
  });

  // イタリック体（免責など）*text*
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // 段落変換（連続する空行で区切られたテキストをpタグに）
  const blocks = html.split(/\n{2,}/);
  html = blocks.map((block) => {
    block = block.trim();
    if (!block) return '';
    // すでにHTMLタグで始まっていれば段落化しない
    if (/^<(h[1-6]|ul|ol|li|table|pre|hr|blockquote)/.test(block)) return block;
    // 改行を<br>に変換してpタグで包む
    return `<p>${block.replace(/\n/g, '<br>')}</p>`;
  }).join('\n\n');

  return html;
}

// ---- クリップボードへコピー ----
function copyToClipboard(text) {
  try {
    // Linux: xclip or xsel
    try {
      execSync('which xclip', { stdio: 'ignore' });
      execSync('xclip -selection clipboard', { input: text, stdio: ['pipe', 'ignore', 'ignore'] });
      return 'xclip';
    } catch {}
    try {
      execSync('which xsel', { stdio: 'ignore' });
      execSync('xsel --clipboard --input', { input: text, stdio: ['pipe', 'ignore', 'ignore'] });
      return 'xsel';
    } catch {}
    // macOS
    try {
      execSync('which pbcopy', { stdio: 'ignore' });
      execSync('pbcopy', { input: text, stdio: ['pipe', 'ignore', 'ignore'] });
      return 'pbcopy';
    } catch {}
    return null;
  } catch {
    return null;
  }
}

// ---- メイン処理 ----
const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('使い方: node scripts/md-to-note.mjs <markdownファイルパス>');
  console.error('例:     node scripts/md-to-note.mjs src/app/content/20260320-cinnamon-honey/note-article.md');
  process.exit(1);
}

const inputPath = resolve(args[0]);
if (!existsSync(inputPath)) {
  console.error(`ファイルが見つかりません: ${inputPath}`);
  process.exit(1);
}

const md = readFileSync(inputPath, 'utf-8');

// フッターの著者プロフィール・免責ブロックを除去（note本文外のメタ情報）
const cleanedMd = md
  .replace(/^\*本記事は.*\*$/gm, '') // 免責（イタリック行）
  .replace(/^---\s*\n\n\*\*著者：.*/s, ''); // 著者プロフィール以降

const html = mdToHtml(cleanedMd);

// HTMLファイルとして保存（オプション）
const outputPath = inputPath.replace(/\.md$/, '.html');

// 標準出力にHTMLを表示
console.log('\n' + '='.repeat(60));
console.log(`📄 ${basename(inputPath)} → note貼り付け用HTML`);
console.log('='.repeat(60) + '\n');
console.log(html);
console.log('\n' + '='.repeat(60));

// クリップボードにコピー
const clipTool = copyToClipboard(html);
if (clipTool) {
  console.log(`\n✅ HTMLをクリップボードにコピーしました（${clipTool}）`);
  console.log('   note.com の記事編集画面でHTMLモードを開いて貼り付けてください。');
} else {
  console.log('\n⚠️  クリップボードへの自動コピーは環境非対応です（xclip/xsel/pbcopy が必要）。');
  console.log('   上記のHTMLをコピーして、noteのHTMLモードに貼り付けてください。');
}
console.log('='.repeat(60) + '\n');
