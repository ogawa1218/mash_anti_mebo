"""
Longevity Navigator | 高品質図解生成スクリプト（強化版）
HTML/CSS + Playwright でPNG出力
強化ポイント：グラスモーフィズム / SVGアイコン / 多段グラデーション / 光彩 / 複数サイズ対応
使い方:
  python3 -X utf8 illustrate_hq.py --content "テキスト" --layout "flow" --topic "NMN" --size "x"
  python3 -X utf8 illustrate_hq.py --topic "睡眠" --size "all"
"""

import argparse
import os
import sys
import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

# =====================================================================
# 設定
# =====================================================================
BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / "images"
FONT_URL = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

SIZES = {
    "x":      (1280, 720),
    "note":   (1280, 670),
    "square": (1080, 1080),
}

COLORS = {
    "bg":       "#1A2A3A",
    "panel":    "#1e3248",
    "orange":   "#f97316",
    "blue":     "#38bdf8",
    "green":    "#4ade80",
    "red":      "#ef4444",
    "text":     "#f0f1f3",
    "muted":    "#7a7e8a",
    "border":   "#2d4a6b",
}

# =====================================================================
# 共通ベースHTML
# =====================================================================
def base_html(body: str, width: int, height: int) -> str:
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'>"
        "<style>"
        "@font-face { font-family: 'NotoSansJP'; src: url('" + FONT_URL + "'); }"
        "* { margin: 0; padding: 0; box-sizing: border-box; }"
        "body {"
        "  width: " + str(width) + "px; height: " + str(height) + "px;"
        "  background: " + COLORS["bg"] + ";"
        "  font-family: 'NotoSansJP', sans-serif;"
        "  color: " + COLORS["text"] + ";"
        "  overflow: hidden;"
        "  position: relative;"
        "}"
        # 背景グラデーション装飾
        ".bg-glow {"
        "  position: absolute; border-radius: 50%; filter: blur(80px); pointer-events: none;"
        "}"
        ".bg-glow-1 {"
        "  width: 400px; height: 400px;"
        "  background: radial-gradient(circle, rgba(249,115,22,0.15) 0%, transparent 70%);"
        "  top: -100px; right: -100px;"
        "}"
        ".bg-glow-2 {"
        "  width: 300px; height: 300px;"
        "  background: radial-gradient(circle, rgba(56,189,248,0.12) 0%, transparent 70%);"
        "  bottom: -80px; left: -80px;"
        "}"
        # グラスパネル
        ".glass {"
        "  background: rgba(255,255,255,0.05);"
        "  border: 1px solid rgba(255,255,255,0.1);"
        "  border-radius: 16px;"
        "  backdrop-filter: blur(12px);"
        "}"
        # オレンジ光彩
        ".glow-orange {"
        "  box-shadow: 0 0 24px rgba(249,115,22,0.35), 0 0 4px rgba(249,115,22,0.6);"
        "}"
        # 青光彩
        ".glow-blue {"
        "  box-shadow: 0 0 24px rgba(56,189,248,0.35), 0 0 4px rgba(56,189,248,0.6);"
        "}"
        # ブランドフッター
        ".brand {"
        "  position: absolute; bottom: 18px; left: 28px;"
        "  font-size: 13px; color: " + COLORS["muted"] + ";"
        "  display: flex; align-items: center; gap: 8px;"
        "}"
        ".brand-tag {"
        "  position: absolute; bottom: 18px; right: 28px;"
        "  font-size: 12px; color: " + COLORS["muted"] + ";"
        "}"
        # オレンジアクセントライン
        ".accent-line {"
        "  width: 48px; height: 4px; border-radius: 2px;"
        "  background: linear-gradient(90deg, " + COLORS["orange"] + ", " + COLORS["blue"] + ");"
        "  margin-bottom: 12px;"
        "}"
        # セクションラベル
        ".label {"
        "  font-size: 11px; font-weight: 700; letter-spacing: 2px;"
        "  text-transform: uppercase; color: " + COLORS["orange"] + ";"
        "  margin-bottom: 6px;"
        "}"
        "</style>"
        "</head><body>"
        "<div class='bg-glow bg-glow-1'></div>"
        "<div class='bg-glow bg-glow-2'></div>"
        + body +
        "<div class='brand'>マーシー｜-30kg × サブ3</div>"
        "<div class='brand-tag'>@longevity_navi</div>"
        "</body></html>"
    )

# =====================================================================
# SVGアイコン（インライン）
# =====================================================================
def icon_arrow_right(color="#f97316", size=20):
    return (
        "<svg width='" + str(size) + "' height='" + str(size) + "' viewBox='0 0 24 24' fill='none'>"
        "<path d='M5 12h14M12 5l7 7-7 7' stroke='" + color + "' stroke-width='2.5' stroke-linecap='round'/>"
        "</svg>"
    )

def icon_check(color="#4ade80", size=20):
    return (
        "<svg width='" + str(size) + "' height='" + str(size) + "' viewBox='0 0 24 24' fill='none'>"
        "<path d='M20 6L9 17l-5-5' stroke='" + color + "' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'/>"
        "</svg>"
    )

def icon_x_mark(color="#ef4444", size=20):
    return (
        "<svg width='" + str(size) + "' height='" + str(size) + "' viewBox='0 0 24 24' fill='none'>"
        "<path d='M18 6L6 18M6 6l12 12' stroke='" + color + "' stroke-width='2.5' stroke-linecap='round'/>"
        "</svg>"
    )

def icon_lightning(color="#f97316", size=20):
    return (
        "<svg width='" + str(size) + "' height='" + str(size) + "' viewBox='0 0 24 24' fill='none'>"
        "<path d='M13 2L3 14h9l-1 8 10-12h-9l1-8z' fill='" + color + "'/>"
        "</svg>"
    )

def icon_brain(color="#38bdf8", size=20):
    return (
        "<svg width='" + str(size) + "' height='" + str(size) + "' viewBox='0 0 24 24' fill='none'>"
        "<path d='M12 2C8 2 5 5 5 8c0 2 1 3.5 2 4.5V18h10v-5.5c1-1 2-2.5 2-4.5 0-3-3-6-7-6z' "
        "stroke='" + color + "' stroke-width='1.8' fill='none'/>"
        "<path d='M9 18v2h6v-2' stroke='" + color + "' stroke-width='1.8'/>"
        "</svg>"
    )

def icon_muscle(color="#4ade80", size=20):
    return (
        "<svg width='" + str(size) + "' height='" + str(size) + "' viewBox='0 0 24 24' fill='none'>"
        "<path d='M6 4c0 0 2-1 4 1l6 6c2 2 1 4 1 4s1 2-1 4l-3-3-3 1-2-2 1-3-3-3z' "
        "stroke='" + color + "' stroke-width='1.8' fill='none'/>"
        "</svg>"
    )

# =====================================================================
# レイアウト：フロー図（因果・ステップ）
# =====================================================================
def layout_flow(steps: list, title: str, subtitle: str = "", width: int = 1280, height: int = 720) -> str:
    n = len(steps)
    if n == 0:
        steps = ["ステップ1", "ステップ2", "ステップ3"]
        n = 3

    step_w = min(200, (width - 80 - (n - 1) * 40) // n)
    total_w = n * step_w + (n - 1) * 40
    start_x = (width - total_w) // 2

    body = (
        "<div style='padding: 40px 48px;'>"
        "<div class='label'>MECHANISM</div>"
        "<div class='accent-line'></div>"
        "<div style='font-size: 28px; font-weight: 900; margin-bottom: 8px; line-height: 1.3;'>" + title + "</div>"
    )
    if subtitle:
        body += "<div style='font-size: 15px; color: " + COLORS["muted"] + "; margin-bottom: 32px;'>" + subtitle + "</div>"
    else:
        body += "<div style='margin-bottom: 32px;'></div>"

    body += "<div style='display: flex; align-items: center; justify-content: center; gap: 0;'>"

    colors_cycle = [COLORS["blue"], COLORS["orange"], COLORS["green"], COLORS["blue"], COLORS["orange"]]

    for i, step in enumerate(steps):
        c = colors_cycle[i % len(colors_cycle)]
        body += (
            "<div class='glass' style='"
            "width: " + str(step_w) + "px; min-height: 160px;"
            "padding: 20px 16px; display: flex; flex-direction: column;"
            "align-items: center; justify-content: center; text-align: center;"
            "border-color: " + c + "40;"
            "box-shadow: 0 0 20px " + c + "22;"
            "'>"
            "<div style='width: 36px; height: 36px; border-radius: 50%;"
            "background: linear-gradient(135deg, " + c + ", " + c + "88);"
            "display: flex; align-items: center; justify-content: center;"
            "font-size: 16px; font-weight: 900; margin-bottom: 12px;'>"
            + str(i + 1) +
            "</div>"
            "<div style='font-size: 13px; font-weight: 700; line-height: 1.5;'>" + step + "</div>"
            "</div>"
        )
        if i < n - 1:
            body += (
                "<div style='margin: 0 4px;'>" + icon_arrow_right(COLORS["orange"], 28) + "</div>"
            )

    body += "</div></div>"
    return body

# =====================================================================
# レイアウト：比較表（NG vs OK）
# =====================================================================
def layout_compare(left_title: str, left_items: list, right_title: str, right_items: list,
                   title: str, width: int = 1280, height: int = 720) -> str:
    body = (
        "<div style='padding: 40px 48px;'>"
        "<div class='label'>COMPARISON</div>"
        "<div class='accent-line'></div>"
        "<div style='font-size: 28px; font-weight: 900; margin-bottom: 28px; line-height: 1.3;'>" + title + "</div>"
        "<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>"
    )

    # 左：NG
    body += (
        "<div class='glass' style='padding: 24px; border-color: " + COLORS["red"] + "33;"
        "box-shadow: 0 0 20px " + COLORS["red"] + "15;'>"
        "<div style='display: flex; align-items: center; gap: 10px; margin-bottom: 18px;'>"
        + icon_x_mark(COLORS["red"], 22) +
        "<span style='font-size: 16px; font-weight: 900; color: " + COLORS["red"] + ";'>" + left_title + "</span>"
        "</div>"
    )
    for item in left_items:
        body += (
            "<div style='display: flex; align-items: flex-start; gap: 8px; margin-bottom: 10px; font-size: 14px;'>"
            "<span style='color: " + COLORS["red"] + "; margin-top: 2px; flex-shrink: 0;'>✕</span>"
            "<span>" + item + "</span>"
            "</div>"
        )
    body += "</div>"

    # 右：OK
    body += (
        "<div class='glass' style='padding: 24px; border-color: " + COLORS["green"] + "33;"
        "box-shadow: 0 0 20px " + COLORS["green"] + "15;'>"
        "<div style='display: flex; align-items: center; gap: 10px; margin-bottom: 18px;'>"
        + icon_check(COLORS["green"], 22) +
        "<span style='font-size: 16px; font-weight: 900; color: " + COLORS["green"] + ";'>" + right_title + "</span>"
        "</div>"
    )
    for item in right_items:
        body += (
            "<div style='display: flex; align-items: flex-start; gap: 8px; margin-bottom: 10px; font-size: 14px;'>"
            "<span style='color: " + COLORS["green"] + "; margin-top: 2px; flex-shrink: 0;'>✓</span>"
            "<span>" + item + "</span>"
            "</div>"
        )
    body += "</div>"

    body += "</div></div>"
    return body

# =====================================================================
# レイアウト：データカード（数値強調）
# =====================================================================
def layout_data_cards(cards: list, title: str, subtitle: str = "", width: int = 1280, height: int = 720) -> str:
    """
    cards: [{"number": "21%", "unit": "低下", "label": "MetSリスク", "source": "2025年メタ分析"}, ...]
    """
    n = len(cards)
    colors_cycle = [COLORS["orange"], COLORS["blue"], COLORS["green"], COLORS["orange"]]

    body = (
        "<div style='padding: 40px 48px;'>"
        "<div class='label'>DATA</div>"
        "<div class='accent-line'></div>"
        "<div style='font-size: 28px; font-weight: 900; margin-bottom: 8px;'>" + title + "</div>"
    )
    if subtitle:
        body += "<div style='font-size: 15px; color: " + COLORS["muted"] + "; margin-bottom: 28px;'>" + subtitle + "</div>"
    else:
        body += "<div style='margin-bottom: 28px;'></div>"

    cols = min(n, 4)
    body += "<div style='display: grid; grid-template-columns: repeat(" + str(cols) + ", 1fr); gap: 16px;'>"

    for i, card in enumerate(cards):
        c = colors_cycle[i % len(colors_cycle)]
        body += (
            "<div class='glass' style='padding: 24px 20px; text-align: center;"
            "border-color: " + c + "44;"
            "box-shadow: 0 0 24px " + c + "20;'>"
            "<div style='font-size: 48px; font-weight: 900;"
            "background: linear-gradient(135deg, " + c + ", #ffffff88);"
            "-webkit-background-clip: text; -webkit-text-fill-color: transparent;"
            "line-height: 1;'>"
            + card.get("number", "—") +
            "</div>"
            "<div style='font-size: 14px; color: " + c + "; font-weight: 700; margin: 6px 0;'>"
            + card.get("unit", "") + " " + card.get("label", "") +
            "</div>"
            "<div style='font-size: 11px; color: " + COLORS["muted"] + "; margin-top: 8px;'>"
            + card.get("source", "") +
            "</div>"
            "</div>"
        )

    body += "</div></div>"
    return body

# =====================================================================
# レイアウト：プログレスバー（比較・段階）
# =====================================================================
def layout_progress(items: list, title: str, subtitle: str = "", width: int = 1280, height: int = 720) -> str:
    """
    items: [{"label": "睡眠あり", "value": 85, "color": "#4ade80"}, ...]
    """
    body = (
        "<div style='padding: 40px 48px;'>"
        "<div class='label'>COMPARISON</div>"
        "<div class='accent-line'></div>"
        "<div style='font-size: 28px; font-weight: 900; margin-bottom: 8px;'>" + title + "</div>"
    )
    if subtitle:
        body += "<div style='font-size: 15px; color: " + COLORS["muted"] + "; margin-bottom: 32px;'>" + subtitle + "</div>"
    else:
        body += "<div style='margin-bottom: 32px;'></div>"

    for item in items:
        v = item.get("value", 50)
        c = item.get("color", COLORS["orange"])
        body += (
            "<div style='margin-bottom: 20px;'>"
            "<div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>"
            "<span style='font-size: 15px; font-weight: 700;'>" + item.get("label", "") + "</span>"
            "<span style='font-size: 15px; font-weight: 900; color: " + c + ";'>" + str(v) + "%</span>"
            "</div>"
            "<div style='height: 14px; background: rgba(255,255,255,0.06); border-radius: 7px; overflow: hidden;'>"
            "<div style='height: 100%; width: " + str(v) + "%; border-radius: 7px;"
            "background: linear-gradient(90deg, " + c + "88, " + c + ");"
            "box-shadow: 0 0 12px " + c + "55;'></div>"
            "</div>"
            "<div style='font-size: 11px; color: " + COLORS["muted"] + "; margin-top: 4px;'>"
            + item.get("note", "") +
            "</div>"
            "</div>"
        )

    body += "</div>"
    return body

# =====================================================================
# レイアウト：チェックリスト（今夜やること等）
# =====================================================================
def layout_checklist(items: list, title: str, subtitle: str = "", width: int = 1280, height: int = 720) -> str:
    body = (
        "<div style='padding: 40px 48px;'>"
        "<div class='label'>ACTION LIST</div>"
        "<div class='accent-line'></div>"
        "<div style='font-size: 28px; font-weight: 900; margin-bottom: 8px;'>" + title + "</div>"
    )
    if subtitle:
        body += "<div style='font-size: 15px; color: " + COLORS["muted"] + "; margin-bottom: 28px;'>" + subtitle + "</div>"
    else:
        body += "<div style='margin-bottom: 28px;'></div>"

    for i, item in enumerate(items):
        done = item.get("done", False)
        c = COLORS["green"] if done else COLORS["orange"]
        body += (
            "<div class='glass' style='display: flex; align-items: center; gap: 16px;"
            "padding: 16px 20px; margin-bottom: 12px;"
            "border-color: " + c + "33;'>"
            "<div style='width: 32px; height: 32px; border-radius: 50%;"
            "border: 2px solid " + c + ";"
            "display: flex; align-items: center; justify-content: center; flex-shrink: 0;"
            "background: " + c + "15;'>"
            + (icon_check(COLORS["green"], 16) if done else
               "<span style='font-size: 13px; font-weight: 900; color: " + c + ";'>" + str(i + 1) + "</span>") +
            "</div>"
            "<div style='flex: 1;'>"
            "<div style='font-size: 15px; font-weight: 700; margin-bottom: 2px;'>" + item.get("text", "") + "</div>"
            "<div style='font-size: 12px; color: " + COLORS["muted"] + ";'>" + item.get("note", "") + "</div>"
            "</div>"
            "</div>"
        )

    body += "</div>"
    return body

# =====================================================================
# レイアウト：カードグリッド（3カード）
# =====================================================================
def layout_card_grid(cards: list, title: str, subtitle: str = "", width: int = 1280, height: int = 720) -> str:
    """
    cards: [{"icon": "⚡", "title": "タイトル", "body": "説明文", "tag": "タグ"}, ...]
    """
    colors_cycle = [COLORS["orange"], COLORS["blue"], COLORS["green"]]
    n = len(cards)
    cols = min(n, 3)

    body = (
        "<div style='padding: 40px 48px;'>"
        "<div class='label'>SOLUTION</div>"
        "<div class='accent-line'></div>"
        "<div style='font-size: 28px; font-weight: 900; margin-bottom: 8px;'>" + title + "</div>"
    )
    if subtitle:
        body += "<div style='font-size: 15px; color: " + COLORS["muted"] + "; margin-bottom: 28px;'>" + subtitle + "</div>"
    else:
        body += "<div style='margin-bottom: 28px;'></div>"

    body += "<div style='display: grid; grid-template-columns: repeat(" + str(cols) + ", 1fr); gap: 16px;'>"

    for i, card in enumerate(cards):
        c = colors_cycle[i % len(colors_cycle)]
        body += (
            "<div class='glass' style='padding: 24px 20px;"
            "border-color: " + c + "44;"
            "box-shadow: 0 0 20px " + c + "18;'>"
            "<div style='font-size: 32px; margin-bottom: 12px;'>" + card.get("icon", "●") + "</div>"
            "<div style='font-size: 16px; font-weight: 900; color: " + c + "; margin-bottom: 10px;'>"
            + card.get("title", "") +
            "</div>"
            "<div style='font-size: 13px; line-height: 1.7; color: " + COLORS["text"] + ";'>"
            + card.get("body", "") +
            "</div>"
        )
        if card.get("tag"):
            body += (
                "<div style='margin-top: 14px; display: inline-block;"
                "background: " + c + "22; border: 1px solid " + c + "55;"
                "border-radius: 20px; padding: 4px 12px;"
                "font-size: 11px; font-weight: 700; color: " + c + ";'>"
                + card["tag"] +
                "</div>"
            )
        body += "</div>"

    body += "</div></div>"
    return body

# =====================================================================
# テンプレート：デモ図解（トピック名から自動生成）
# =====================================================================
def auto_layout(topic: str, width: int, height: int) -> str:
    """トピック名から適切なデモ図解を自動生成"""
    topic_lower = topic.lower()

    if any(k in topic_lower for k in ["nmn", "nad", "サプリ", "クレアチン", "マグネシウム"]):
        cards = [
            {"number": "40%", "unit": "低下", "label": "40代のNAD+量", "source": "20代比・加齢により"},
            {"number": "250mg", "unit": "/日", "label": "推奨補充量", "source": "臨床研究より"},
            {"number": "12週", "unit": "継続", "label": "効果実感の目安", "source": "複数RCT共通"},
        ]
        return layout_data_cards(cards, topic + "の科学", "最新臨床研究が示すデータ", width, height)

    elif any(k in topic_lower for k in ["睡眠", "sleep"]):
        items = [
            {"label": "睡眠7時間以上：脂肪燃焼", "value": 85, "color": COLORS["green"], "note": "十分な睡眠でダイエット効果が最大化"},
            {"label": "睡眠6時間未満：脂肪燃焼", "value": 38, "color": COLORS["red"], "note": "睡眠不足で脂肪燃焼が55%減少（研究より）"},
            {"label": "睡眠規則性スコア", "value": 72, "color": COLORS["orange"], "note": "時間より「規則性」が死亡リスクを下げる"},
        ]
        return layout_progress(items, "睡眠とダイエットの関係", "睡眠を削ると脂肪ではなく筋肉が落ちる", width, height)

    elif any(k in topic_lower for k in ["筋トレ", "レジスタンス", "運動", "バーピー", "ゾーン2"]):
        steps = ["運動開始", "筋肉量増加", "GLUT4増加", "血糖安定化", "インスリン抵抗性改善", "代謝向上"]
        return layout_flow(steps, "運動で代謝が変わるメカニズム", "筋肉は体最大のグルコース倉庫", width, height)

    elif any(k in topic_lower for k in ["glp-1", "glp1", "セマグルチド", "薬"]):
        left_items = ["体重の45%が筋肉から消える", "運動なしは筋肉喪失が加速", "リバウンドリスクが高い", "基礎代謝が低下する"]
        right_items = ["週2〜3回の筋トレを組み合わせる", "たんぱく質1.6〜2.2g/kg確保", "ゾーン2有酸素を並行", "医師と相談しながら継続"]
        return layout_compare("薬だけの場合", left_items, "筋トレ併用の場合", right_items, "GLP-1薬と筋トレの組み合わせが鍵", width, height)

    elif any(k in topic_lower for k in ["オートファジー", "断食", "fasting"]):
        steps = ["最終食事", "12時間後：ケトン産生開始", "16時間後：オートファジー活性化", "18〜24時間：細胞掃除ピーク"]
        return layout_flow(steps, "断食とオートファジーのタイムライン", "意志力ではなく「時間設計」の話", width, height)

    else:
        cards = [
            {"icon": "🔬", "title": "研究エビデンス", "body": "査読済み論文・RCT・メタ分析に基づく最新知見", "tag": "2024-2025"},
            {"icon": "⚡", "title": "実践プロトコル", "body": "40代メタボ男性が今日から始められる具体的な手順", "tag": "即実践可"},
            {"icon": "📈", "title": "期待できる効果", "body": "血糖・体脂肪・認知機能・エネルギー代謝の改善", "tag": "8週以降"},
        ]
        return layout_card_grid(cards, topic, "最新研究を実践に変える", width, height)

# =====================================================================
# PNG出力
# =====================================================================
def render_png(html: str, output_path: Path, width: int, height: int):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.set_content(html)
        page.wait_for_timeout(800)
        page.screenshot(path=str(output_path), full_page=False)
        browser.close()
    print("生成: " + str(output_path))

# =====================================================================
# メイン
# =====================================================================
def main():
    parser = argparse.ArgumentParser(description="Longevity Navigator 図解生成（強化版）")
    parser.add_argument("--topic", default="longevity", help="トピック名")
    parser.add_argument("--layout", default="auto", help="レイアウト種別: auto/flow/compare/data/progress/checklist/grid")
    parser.add_argument("--content", default="", help="コンテンツテキスト（省略可）")
    parser.add_argument("--size", default="x", help="出力サイズ: x/note/square/all")
    parser.add_argument("--outdir", default="", help="出力ディレクトリ（省略時は自動）")
    args = parser.parse_args()

    today = datetime.date.today().strftime("%Y%m%d")
    safe_topic = args.topic[:20].replace(" ", "_").replace("　", "_")

    if args.outdir:
        out_dir = Path(args.outdir)
    else:
        out_dir = IMAGES_DIR / (today + "_" + safe_topic)
    out_dir.mkdir(parents=True, exist_ok=True)

    sizes_to_render = SIZES.keys() if args.size == "all" else [args.size]

    for size_key in sizes_to_render:
        if size_key not in SIZES:
            print("不明なサイズ: " + size_key)
            continue

        w, h = SIZES[size_key]
        body = auto_layout(args.topic, w, h)
        html = base_html(body, w, h)

        # HTMLデバッグ保存
        html_path = out_dir / ("debug_" + size_key + ".html")
        html_path.write_text(html, encoding="utf-8")

        # PNG出力
        png_path = out_dir / (safe_topic + "_" + size_key + ".png")
        render_png(html, png_path, w, h)

    print("完了: " + str(out_dir))

if __name__ == "__main__":
    main()
