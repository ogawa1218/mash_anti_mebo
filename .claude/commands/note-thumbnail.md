# Longevity Navigator｜サムネイル職人｜noteサムネイル自動生成

このコマンドは、note記事タイトル・テーマを受け取り、
**HTML/CSS + Playwright** でクリック率特化のnoteサムネイルPNGを自動生成します。

---

## 出力仕様

| 項目 | 値 |
|---|---|
| サイズ | 1280×670px |
| 背景 | 完全な黒（#000000） |
| 保存先 | `note/images/YYYYMMDD_[topic]/thumbnail.png` |

---

## 実行手順

### STEP 1｜入力を受け取る

引数がある場合：その引数をタイトル/テーマとして使う
引数がない場合：最新のdrafts/YYYYMMDD_*.mdのタイトルを読み込む

---

### STEP 2｜3行コピーを生成

記事タイトル・テーマから以下を生成する：

```
行1（白・大）：感情フック or 問いかけ（20文字以内）
行2（白・中）：ベネフィット or 裏切り（20文字以内）
行3（オレンジ・大・太）：結論ワード or 行動ワード（15文字以内）
```

**コピー生成のルール：**
- ペルソナ：30〜40代メタボ男性、健診E判定、夜に崩れやすい
- 感情語を優先：「また夜に食べた」「続かない」「やめられない」
- 数字を入れると強い：「-32kg」「8年維持」「30日」
- 疑問形も有効：「なぜ夜に崩れるのか？」
- 3行で完結した意味になること（1行だけでは意味不明にしない）

**良い例（睡眠テーマ）：**
```
行1：夜に崩れる人ほど
行2：最初に変えるべきは
行3：「睡眠」だった。
```

**良い例（間食テーマ）：**
```
行1：意志力で間食を
行2：止めようとしてるから
行3：止まらない。
```

---

### STEP 3｜Pythonスクリプトを実行

**スクリプトパス：**
`C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note\scripts\illustrate_hq.py`

スクリプトが存在しない場合、または`--mode thumbnail`オプションが未対応の場合は、
以下の仕様でサムネイル専用のPythonスクリプトをインラインで生成・実行する。

**サムネイル生成スクリプト（インライン）：**

```python
"""
Longevity Navigator | noteサムネイル生成スクリプト
HTML/CSS + Playwright でPNG出力（1280x670px）
"""

import os, sys, datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

FONT_URL = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
BASE_DIR = Path(r"C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note")
IMAGES_DIR = BASE_DIR / "images"

def build_html(line1, line2, line3, episode_num=""):
    num_html = ("<div style='position:absolute;bottom:40px;right:50px;"
                "font-size:48px;font-weight:900;color:#f97316;"
                "font-family:NotoSansJP;'>" + episode_num + "</div>") if episode_num else ""

    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        "@font-face{font-family:'NotoSansJP';src:url('" + FONT_URL + "');}"
        "*{margin:0;padding:0;box-sizing:border-box;}"
        "body{width:1280px;height:670px;background:#000000;overflow:hidden;"
        "font-family:'NotoSansJP',sans-serif;position:relative;display:flex;"
        "align-items:center;justify-content:center;}"
        ".noise{position:absolute;inset:0;opacity:0.03;"
        "background-image:url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256'"
        " xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E"
        "%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'"
        " stitchTiles='stitch'/%3E%3C/filter%3E"
        "%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E"
        "%3C/svg%3E\");}"
        ".accent-line{position:absolute;left:0;top:0;width:6px;height:100%;"
        "background:linear-gradient(180deg,#f97316 0%,#fb923c 50%,transparent 100%);}"
        ".copy-wrap{text-align:left;padding:0 80px;z-index:1;width:100%;}"
        ".line1{font-size:56px;font-weight:700;color:#ffffff;line-height:1.3;"
        "letter-spacing:-0.02em;}"
        ".line2{font-size:56px;font-weight:700;color:#ffffff;line-height:1.3;"
        "letter-spacing:-0.02em;}"
        ".line3{font-size:72px;font-weight:900;color:#f97316;line-height:1.2;"
        "letter-spacing:-0.03em;margin-top:8px;"
        "text-shadow:0 0 40px rgba(249,115,22,0.5);}"
        ".profile{position:absolute;bottom:40px;left:50px;}"
        ".profile-name{font-size:22px;font-weight:700;color:#ffffff;}"
        ".profile-sub{font-size:16px;color:#9ca3af;margin-top:4px;}"
        "</style></head><body>"
        "<div class='noise'></div>"
        "<div class='accent-line'></div>"
        "<div class='copy-wrap'>"
        "<div class='line1'>" + line1 + "</div>"
        "<div class='line2'>" + line2 + "</div>"
        "<div class='line3'>" + line3 + "</div>"
        "</div>"
        "<div class='profile'>"
        "<div class='profile-name'>マーシー</div>"
        "<div class='profile-sub'>100kg→68kg(-32kg)｜Sub3</div>"
        "</div>"
        + num_html +
        "</body></html>"
    )

def generate_thumbnail(line1, line2, line3, topic, episode_num=""):
    today = datetime.date.today().strftime("%Y%m%d")
    safe_topic = topic[:20].replace(" ","_").replace("　","_")
    folder = IMAGES_DIR / (today + "_" + safe_topic)
    folder.mkdir(parents=True, exist_ok=True)
    html_path = folder / "thumbnail.html"
    png_path  = folder / "thumbnail.png"

    html_content = build_html(line1, line2, line3, episode_num)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width":1280,"height":670})
        page.goto("file:///" + str(html_path).replace("\\","/"))
        page.wait_for_timeout(800)
        page.screenshot(path=str(png_path))
        browser.close()

    print("✅ 生成完了：" + str(png_path))
    return str(png_path)

if __name__ == "__main__":
    # 引数：line1 line2 line3 topic [episode_num]
    args = sys.argv[1:]
    if len(args) < 4:
        print("Usage: python note_thumbnail.py line1 line2 line3 topic [episode_num]")
        sys.exit(1)
    generate_thumbnail(args[0], args[1], args[2], args[3],
                       args[4] if len(args) > 4 else "")
```

スクリプトを `note/scripts/note_thumbnail.py` として保存してから実行する。

**実行コマンド：**
```bash
python3 -X utf8 "C:\Users\masas\product\2nd-Brain\04_アウトプット\Longevity\note\scripts\note_thumbnail.py" \
  "[行1]" "[行2]" "[行3]" "[トピック名]" "[エピソード番号（省略可）]"
```

---

### STEP 4｜バリエーションを2案追加生成（任意）

3行コピーのパターンを変えて合計3案生成する：
- **案A（問いかけ型）**：「なぜ〜？」で始まる
- **案B（結果型）**：数字を入れる（例：-32kg、30日）
- **案C（共感型）**：「また〜た」「続かない」などの感情語

3案すべてのPNGを生成し、最後にマーシーが選べるようにする。

---

### STEP 5｜完了サマリーを表示

```
サムネイル生成完了：YYYY-MM-DD

生成ファイル：
・thumbnail.png（案A：問いかけ型）
・thumbnail_b.png（案B：結果型）
・thumbnail_c.png（案C：共感型）

保存先：note/images/YYYYMMDD_[topic]/

コピー内容（案A）：
  行1：[テキスト]
  行2：[テキスト]
  行3：[テキスト]（オレンジ）

次のアクション：
・3案の中から1枚を選んでnoteにアップロード
・noteのサムネイル設定でアップロードすればOK
```

---

## デザインシステム（サムネイル専用）

### カラーパレット
```
背景：           #000000（純黒・Appleミニマル）
テキスト行1・2：  #ffffff（白）
テキスト行3：     #f97316（オレンジ強調）
サブテキスト：    #9ca3af（グレー）
アクセントライン：#f97316（左端縦ライン）
グロー：         rgba(249,115,22,0.5)
```

### タイポグラフィ
```
行1・2：Noto Sans JP / font-weight:700 / 56px
行3：   Noto Sans JP / font-weight:900 / 72px
名前：  Noto Sans JP / font-weight:700 / 22px
実績：  Noto Sans JP / font-weight:400 / 16px
```

### 固定要素（全サムネイル共通）
```
左端縦ライン：オレンジグラデーション（6px幅）
左下：マーシー / 100kg→68kg(-32kg)｜Sub3
右下：エピソード番号（①②③… ※省略可）
```

---

## 注意事項

- Playwrightがインストールされていること（`pip install playwright` + `playwright install chromium`）
- フォントパス `C:/Windows/Fonts/NotoSansJP-VF.ttf` が存在すること
- 3行コピーは各20文字以内に収めること（はみ出し防止）
- エピソード番号は記事の通し番号（第5回なら「⑤」）
- 生成失敗時はHTMLファイルをブラウザで開いて確認すること
