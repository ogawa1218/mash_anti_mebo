#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 図解生成スクリプト（HTML/CSS + Playwright）"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images"
OUTPUT_DIR.mkdir(exist_ok=True)
FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;font-family:'NJ','Meiryo',sans-serif;position:relative;}"
)

def render(html, fname):
    tmp = ARTICLE_DIR / "_tmp_fig.html"
    out = OUTPUT_DIR / fname
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto("file:///" + str(tmp).replace("\\", "/"))
        page.wait_for_timeout(800)
        page.screenshot(path=str(out), full_page=False)
        browser.close()
    tmp.unlink(missing_ok=True)
    print("OK: " + fname)


def fig1():
    """図解①：ミトコンドリア劣化ループ（円形フロー）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;}"
        "</style></head><body>"
        # タイトル
        "<div style='position:absolute;top:36px;left:56px;'>"
        "<div style='font-size:14px;font-weight:700;color:#FF6D00;letter-spacing:2px;'>FIGURE 01</div>"
        "<div style='font-size:32px;font-weight:900;color:#fff;margin-top:4px;'>ミトコンドリア劣化ループ</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>30代から始まる「疲れやすさ」の正体</div>"
        "</div>"
        # 中央のループ図
        # ステップ1（上）
        "<div style='position:absolute;top:150px;left:440px;width:400px;'>"
        "<div style='background:#1e3a5f;border:2px solid #ef4444;border-radius:16px;padding:20px 24px;text-align:center;'>"
        "<div style='font-size:22px;font-weight:800;color:#ef4444;'>30代からミトコンドリア劣化</div>"
        "<div style='font-size:15px;color:#9ca3af;margin-top:6px;'>エンジン性能が低下し始める</div>"
        "</div></div>"
        # 矢印 右下
        "<div style='position:absolute;top:262px;left:860px;font-size:36px;color:#ef4444;transform:rotate(45deg);'>→</div>"
        # ステップ2（右）
        "<div style='position:absolute;top:290px;right:56px;width:340px;'>"
        "<div style='background:#1e3a5f;border:2px solid #ef4444;border-radius:16px;padding:20px 24px;text-align:center;'>"
        "<div style='font-size:22px;font-weight:800;color:#ef4444;'>代謝低下・疲れやすい</div>"
        "<div style='font-size:15px;color:#9ca3af;margin-top:6px;'>脂肪が燃えにくくなる</div>"
        "</div></div>"
        # 矢印 下
        "<div style='position:absolute;top:410px;right:180px;font-size:36px;color:#ef4444;transform:rotate(90deg);'>→</div>"
        # ステップ3（下）
        "<div style='position:absolute;top:440px;left:440px;width:400px;'>"
        "<div style='background:#1e3a5f;border:2px solid #ef4444;border-radius:16px;padding:20px 24px;text-align:center;'>"
        "<div style='font-size:22px;font-weight:800;color:#ef4444;'>運動が辛い → やめる</div>"
        "<div style='font-size:15px;color:#9ca3af;margin-top:6px;'>「歳だから仕方ない」と諦める</div>"
        "</div></div>"
        # 矢印 左下
        "<div style='position:absolute;top:410px;left:400px;font-size:36px;color:#ef4444;transform:rotate(-90deg);'>→</div>"
        # ステップ4（左）
        "<div style='position:absolute;top:290px;left:56px;width:340px;'>"
        "<div style='background:#1e3a5f;border:2px solid #ef4444;border-radius:16px;padding:20px 24px;text-align:center;'>"
        "<div style='font-size:22px;font-weight:800;color:#ef4444;'>さらに劣化が加速</div>"
        "<div style='font-size:15px;color:#9ca3af;margin-top:6px;'>老化スピードが上がる</div>"
        "</div></div>"
        # 矢印 上
        "<div style='position:absolute;top:260px;left:190px;font-size:36px;color:#ef4444;transform:rotate(-45deg);'>→</div>"
        # 中央の解決策
        "<div style='position:absolute;bottom:40px;left:56px;right:56px;'>"
        "<div style='background:linear-gradient(90deg,rgba(34,197,94,.15),rgba(34,197,94,.05));border:2px solid #4ade80;border-radius:16px;padding:18px 32px;display:flex;align-items:center;justify-content:center;gap:20px;'>"
        "<div style='font-size:36px;'>&#x1F504;</div>"
        "<div>"
        "<div style='font-size:22px;font-weight:800;color:#4ade80;'>解決策：ゾーン2運動でループを断ち切る</div>"
        "<div style='font-size:15px;color:#9ca3af;margin-top:2px;'>ゆるい運動がミトコンドリアを再起動させる</div>"
        "</div></div></div>"
        "</body></html>")
    render(html, "図解①_ミトコンドリア劣化ループ.png")


def fig2():
    """図解②：ゾーン2×ミトコンドリア全体像（横3列カード）"""
    cards = [
        ("STEP 1", "ゾーン2運動", "話せるペースで10-40分", "息が上がるけど会話OK", "#38bdf8"),
        ("STEP 2", "PGC-1α活性化", "遺伝子スイッチON", "ミトコンドリア増殖を指令", "#FF6D00"),
        ("STEP 3", "細胞が若返る", "数が増える＋古いのを掃除", "代謝UP・疲れにくい体へ", "#4ade80"),
    ]
    cards_html = ""
    for i, (step, title, sub1, sub2, color) in enumerate(cards):
        left = 56 + i * 400
        cards_html += (
            "<div style='position:absolute;top:180px;left:" + str(left) + "px;width:360px;height:340px;"
            "background:#1e3a5f;border-radius:16px;padding:28px;border-top:4px solid " + color + ";'>"
            "<div style='font-size:14px;font-weight:700;color:" + color + ";letter-spacing:2px;'>" + step + "</div>"
            "<div style='font-size:28px;font-weight:900;color:#fff;margin-top:12px;line-height:1.3;'>" + title + "</div>"
            "<div style='width:40px;height:3px;background:" + color + ";margin:16px 0;border-radius:2px;'></div>"
            "<div style='font-size:18px;color:#e2e8f0;line-height:1.6;'>" + sub1 + "</div>"
            "<div style='font-size:16px;color:#9ca3af;margin-top:10px;line-height:1.6;'>" + sub2 + "</div>"
            "</div>"
        )
        if i < 2:
            cards_html += (
                "<div style='position:absolute;top:330px;left:" + str(left + 370) + "px;"
                "font-size:28px;font-weight:900;color:#9ca3af;'>→</div>"
            )

    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;}"
        "</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;'>"
        "<div style='font-size:14px;font-weight:700;color:#FF6D00;letter-spacing:2px;'>FIGURE 02</div>"
        "<div style='font-size:32px;font-weight:900;color:#fff;margin-top:4px;'>ゾーン2 → ミトコンドリア活性化の流れ</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>「ゆるい運動」が細胞を若返らせるメカニズム</div>"
        "</div>"
        + cards_html +
        "<div style='position:absolute;bottom:36px;right:56px;font-size:14px;color:#4a5568;'>"
        "出典: Hood et al. 2019, Journal of Physiology</div>"
        "</body></html>")
    render(html, "図解②_ゾーン2ミトコンドリア全体像.png")


def fig3():
    """図解③：運動の2つの効果比較（NG vs OK）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;}"
        "</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;'>"
        "<div style='font-size:14px;font-weight:700;color:#FF6D00;letter-spacing:2px;'>FIGURE 03</div>"
        "<div style='font-size:32px;font-weight:900;color:#fff;margin-top:4px;'>運動がミトコンドリアに与える2つの効果</div>"
        "</div>"
        # 左パネル：生合成
        "<div style='position:absolute;top:130px;left:56px;width:560px;height:440px;"
        "background:#0d2035;border-radius:16px;padding:32px;border-top:4px solid #38bdf8;'>"
        "<div style='font-size:16px;font-weight:700;color:#38bdf8;letter-spacing:2px;'>EFFECT 1</div>"
        "<div style='font-size:28px;font-weight:900;color:#fff;margin-top:8px;'>ミトコンドリア生合成</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>新しい工場が増える</div>"
        "<div style='width:100%;height:2px;background:#1e3a5f;margin:20px 0;'></div>"
        # ビフォーアフター
        "<div style='display:flex;gap:20px;margin-top:12px;'>"
        "<div style='flex:1;background:#1e3a5f;border-radius:12px;padding:16px;text-align:center;'>"
        "<div style='font-size:14px;color:#ef4444;font-weight:700;'>BEFORE</div>"
        "<div style='font-size:48px;margin:8px 0;'>&#x1F534;&#x1F534;</div>"
        "<div style='font-size:14px;color:#9ca3af;'>少ない・弱い</div>"
        "</div>"
        "<div style='display:flex;align-items:center;font-size:28px;color:#38bdf8;font-weight:900;'>→</div>"
        "<div style='flex:1;background:#1e3a5f;border-radius:12px;padding:16px;text-align:center;'>"
        "<div style='font-size:14px;color:#4ade80;font-weight:700;'>AFTER</div>"
        "<div style='font-size:48px;margin:8px 0;'>&#x1F7E2;&#x1F7E2;&#x1F7E2;&#x1F7E2;</div>"
        "<div style='font-size:14px;color:#9ca3af;'>数が増殖</div>"
        "</div></div>"
        "<div style='margin-top:16px;background:#162d4a;border-radius:8px;padding:12px 16px;'>"
        "<div style='font-size:15px;color:#e2e8f0;'>PGC-1αスイッチ → 細胞内で増殖開始</div>"
        "<div style='font-size:13px;color:#6b7280;margin-top:4px;'>Safdar et al. 2011, PNAS</div>"
        "</div>"
        "</div>"
        # 右パネル：ミトファジー
        "<div style='position:absolute;top:130px;right:56px;width:560px;height:440px;"
        "background:#0d2035;border-radius:16px;padding:32px;border-top:4px solid #4ade80;'>"
        "<div style='font-size:16px;font-weight:700;color:#4ade80;letter-spacing:2px;'>EFFECT 2</div>"
        "<div style='font-size:28px;font-weight:900;color:#fff;margin-top:8px;'>ミトファジー（掃除）</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>壊れた工場を除去・再利用</div>"
        "<div style='width:100%;height:2px;background:#1e3a5f;margin:20px 0;'></div>"
        # ビフォーアフター
        "<div style='display:flex;gap:20px;margin-top:12px;'>"
        "<div style='flex:1;background:#1e3a5f;border-radius:12px;padding:16px;text-align:center;'>"
        "<div style='font-size:14px;color:#ef4444;font-weight:700;'>BEFORE</div>"
        "<div style='font-size:48px;margin:8px 0;'>&#x1F534;&#x26A0;&#x1F534;&#x26A0;</div>"
        "<div style='font-size:14px;color:#9ca3af;'>壊れたまま蓄積</div>"
        "</div>"
        "<div style='display:flex;align-items:center;font-size:28px;color:#4ade80;font-weight:900;'>→</div>"
        "<div style='flex:1;background:#1e3a5f;border-radius:12px;padding:16px;text-align:center;'>"
        "<div style='font-size:14px;color:#4ade80;font-weight:700;'>AFTER</div>"
        "<div style='font-size:48px;margin:8px 0;'>&#x1F7E2;&#x1F7E2;&#x2728;</div>"
        "<div style='font-size:14px;color:#9ca3af;'>新品に入替</div>"
        "</div></div>"
        "<div style='margin-top:16px;background:#162d4a;border-radius:8px;padding:12px 16px;'>"
        "<div style='font-size:15px;color:#e2e8f0;'>オートファジーでダメージ品を分解・再構築</div>"
        "<div style='font-size:13px;color:#6b7280;margin-top:4px;'>大隅良典 2016 ノーベル賞</div>"
        "</div>"
        "</div>"
        # 下部バー
        "<div style='position:absolute;bottom:36px;left:56px;right:56px;'>"
        "<div style='background:linear-gradient(90deg,rgba(255,109,0,.15),rgba(255,109,0,.05));border:1px solid #FF6D00;"
        "border-radius:12px;padding:14px 24px;text-align:center;'>"
        "<span style='font-size:18px;font-weight:800;color:#FF6D00;'>結果：12週間で機能69%改善</span>"
        "<span style='font-size:14px;color:#9ca3af;margin-left:16px;'>Robinson et al. 2017, Cell Metabolism</span>"
        "</div></div>"
        "</body></html>")
    render(html, "図解③_運動の2つの効果比較.png")


def fig4():
    """図解④：ゾーン2実践早見表（テーブル型）"""
    rows = [
        ("早歩き", "話せるギリギリ", "10-30分", "毎日OK", "道具不要", "#4ade80"),
        ("軽いジョギング", "鼻呼吸ギリ", "20-40分", "週3-4回", "シューズのみ", "#38bdf8"),
        ("自転車", "平地ゆるく", "20-40分", "週2-3回", "自転車", "#38bdf8"),
        ("筋トレ（補助）", "スクワット等", "15-20分", "週2回", "自重OK", "#FF6D00"),
    ]
    rows_html = ""
    for name, intensity, duration, freq, equip, color in rows:
        rows_html += (
            "<tr>"
            "<td style='padding:16px 20px;font-size:18px;font-weight:700;color:" + color + ";border-bottom:1px solid #1e3a5f;'>" + name + "</td>"
            "<td style='padding:16px 20px;font-size:16px;color:#e2e8f0;border-bottom:1px solid #1e3a5f;'>" + intensity + "</td>"
            "<td style='padding:16px 20px;font-size:16px;color:#e2e8f0;border-bottom:1px solid #1e3a5f;'>" + duration + "</td>"
            "<td style='padding:16px 20px;font-size:16px;color:#e2e8f0;border-bottom:1px solid #1e3a5f;'>" + freq + "</td>"
            "<td style='padding:16px 20px;font-size:16px;color:#9ca3af;border-bottom:1px solid #1e3a5f;'>" + equip + "</td>"
            "</tr>"
        )
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;}"
        "table{width:calc(100% - 112px);position:absolute;top:140px;left:56px;border-collapse:collapse;}"
        "th{padding:14px 20px;font-size:14px;font-weight:700;color:#FF6D00;text-align:left;"
        "border-bottom:2px solid #FF6D00;letter-spacing:1px;background:#0d2035;}"
        "</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;'>"
        "<div style='font-size:14px;font-weight:700;color:#FF6D00;letter-spacing:2px;'>FIGURE 04</div>"
        "<div style='font-size:32px;font-weight:900;color:#fff;margin-top:4px;'>ゾーン2 実践早見表</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>「話せるペース」で続ける運動メニュー</div>"
        "</div>"
        "<table>"
        "<tr><th>種目</th><th>強度の目安</th><th>時間</th><th>頻度</th><th>必要なもの</th></tr>"
        + rows_html +
        "</table>"
        # 下部の補足
        "<div style='position:absolute;bottom:60px;left:56px;right:56px;display:flex;gap:20px;'>"
        "<div style='flex:1;background:#162d4a;border-radius:12px;padding:16px 20px;border-left:4px solid #4ade80;'>"
        "<div style='font-size:16px;font-weight:700;color:#4ade80;'>初心者おすすめ</div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>早歩き10分 × 週3回から</div>"
        "</div>"
        "<div style='flex:1;background:#162d4a;border-radius:12px;padding:16px 20px;border-left:4px solid #38bdf8;'>"
        "<div style='font-size:16px;font-weight:700;color:#38bdf8;'>判定基準</div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>最大心拍数の60-70% = 会話ギリギリ</div>"
        "</div>"
        "<div style='flex:1;background:#162d4a;border-radius:12px;padding:16px 20px;border-left:4px solid #FF6D00;'>"
        "<div style='font-size:16px;font-weight:700;color:#FF6D00;'>注意</div>"
        "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>追い込みすぎは逆効果</div>"
        "</div>"
        "</div>"
        "</body></html>")
    render(html, "図解④_ゾーン2実践早見表.png")


def fig5():
    """図解⑤：崩れた日の復帰フロー（縦型3ステップ）"""
    steps = [
        ("1", "崩れた日", "「今日はできなかった...」", "自己嫌悪が始まりそうになる", "#ef4444"),
        ("2", "翌朝5分だけ歩く", "ゼロをイチに変えるだけでOK", "完璧じゃなくていい。動いた事実が大事", "#FF6D00"),
        ("3", "ループに戻る", "8勝6敗で十分。ミトコンドリアは応えてくれる", "週2-3回の継続で細胞は若返り続ける", "#4ade80"),
    ]
    steps_html = ""
    for i, (num, title, sub1, sub2, color) in enumerate(steps):
        top = 150 + i * 185
        steps_html += (
            "<div style='position:absolute;top:" + str(top) + "px;left:56px;right:56px;height:160px;"
            "display:flex;align-items:center;gap:28px;'>"
            # 番号バッジ
            "<div style='width:72px;height:72px;border-radius:50%;background:" + color + ";"
            "display:flex;align-items:center;justify-content:center;flex-shrink:0;"
            "font-size:32px;font-weight:900;color:#fff;'>" + num + "</div>"
            # カード
            "<div style='flex:1;background:#1e3a5f;border-radius:16px;padding:20px 28px;"
            "border-left:4px solid " + color + ";'>"
            "<div style='font-size:24px;font-weight:800;color:#fff;'>" + title + "</div>"
            "<div style='font-size:16px;color:#e2e8f0;margin-top:6px;'>" + sub1 + "</div>"
            "<div style='font-size:14px;color:#9ca3af;margin-top:4px;'>" + sub2 + "</div>"
            "</div></div>"
        )
        if i < 2:
            steps_html += (
                "<div style='position:absolute;top:" + str(top + 162) + "px;left:83px;"
                "font-size:24px;color:#4a5568;'>|</div>"
            )

    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;}"
        "</style></head><body>"
        "<div style='position:absolute;top:36px;left:56px;'>"
        "<div style='font-size:14px;font-weight:700;color:#FF6D00;letter-spacing:2px;'>FIGURE 05</div>"
        "<div style='font-size:32px;font-weight:900;color:#fff;margin-top:4px;'>崩れた日の復帰フロー</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>8勝6敗でOK。翌朝5分で戻る。</div>"
        "</div>"
        + steps_html +
        "<div style='position:absolute;bottom:36px;right:56px;font-size:14px;color:#4a5568;'>"
        "第 ミトコンドリア×運動</div>"
        "</body></html>")
    render(html, "図解⑤_崩れた日の復帰フロー.png")


if __name__ == "__main__":
    print("第 図解5枚 生成開始...\n")
    fig1(); fig2(); fig3(); fig4(); fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))

