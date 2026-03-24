#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第41回 図解生成スクリプト（HTML/CSS + Playwright 強化版）
stand.fm 第31話「就寝前の入浴が『睡眠の質』を劇的に変える」対応
図解① 深部体温フロー（入浴→温まる→放熱→眠気）
図解② NG vs OK 比較（誤解3パターン vs 正解）
図解③ 3コツカードグリッド（温度/タイミング/入浴後の流れ）
図解④ 5日間チェック表（テーブル型）
図解⑤ リカバリーフロー（入れなかった日の翌朝3手）
"""

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
    "body{width:1280px;height:720px;overflow:hidden;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
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


# ── 図解① 深部体温フロー ─────────────────────────────────────
def fig1():
    steps = [
        ("🛁", "#38bdf8", "入浴（38〜40℃）", "10〜15分"),
        ("🔥", "#FF6D00", "深部体温が上昇", "体が温まる"),
        ("💨", "#4ade80", "体から熱が放熱", "手足が温かくなる"),
        ("📉", "#38bdf8", "深部体温が低下", "就寝1〜2時間後"),
        ("😴", "#4ade80", "自然な眠気が来る", "スムーズな入眠"),
    ]
    cards = ""
    for i, (icon, color, title, sub) in enumerate(steps):
        arrow = "" if i == len(steps) - 1 else (
            f'<div style="position:absolute;right:-34px;top:50%;transform:translateY(-50%);'
            f'font-size:32px;color:#555;z-index:10;">▶</div>'
        )
        cards += f"""
        <div style="position:relative;background:#0d2035;border:2px solid {color};
                    border-radius:12px;padding:28px 20px;text-align:center;
                    width:200px;flex-shrink:0;">
          <div style="font-size:44px;margin-bottom:12px;">{icon}</div>
          <div style="font-size:20px;font-weight:900;color:{color};line-height:1.3;
                      margin-bottom:8px;">{title}</div>
          <div style="font-size:15px;color:#9ca3af;">{sub}</div>
          {arrow}
        </div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
    {BASE_CSS}
    body{{background:#0d1b2a;}}
    .hdr{{position:absolute;left:64px;top:40px;}}
    .badge{{display:inline-block;background:#38bdf8;color:#000;font-size:14px;
            font-weight:900;padding:4px 14px;border-radius:20px;margin-bottom:12px;}}
    .ttl{{font-size:38px;font-weight:900;color:#fff;letter-spacing:-1px;}}
    .row{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
          display:flex;gap:36px;align-items:center;}}
    .src{{position:absolute;bottom:24px;right:48px;font-size:14px;color:#444;}}
    </style></head><body>
    <div class="hdr">
      <div class="badge">図解①｜メカニズム</div>
      <div class="ttl">湯船が眠りを変える「深部体温フロー」</div>
    </div>
    <div class="row">{cards}</div>
    <div class="src">Haghayegh et al., Sleep Medicine Reviews 2019</div>
    </body></html>"""
    render(html, "図解①_深部体温フロー.png")


# ── 図解② NG vs OK 比較 ──────────────────────────────────────
def fig2():
    ng_items = [
        ("❌", "寝る直前に入る", "体がまだ熱いまま就寝"),
        ("❌", "熱すぎるお湯（43℃+）", "交感神経が興奮→覚醒"),
        ("❌", "シャワーで代替", "全身温まりにくく体温変化が弱い"),
    ]
    ok_items = [
        ("✅", "就寝1〜2時間前に入る", "体温が下がる時間を確保"),
        ("✅", "38〜40℃でゆっくり", "副交感神経優位→リラックス"),
        ("✅", "湯船に10〜15分", "全身温まり→放熱→自然な眠気"),
    ]
    def card(items, color, label):
        rows = "".join(
            f'<div style="display:flex;align-items:flex-start;gap:14px;margin-bottom:18px;">'
            f'<span style="font-size:26px;flex-shrink:0;">{ic}</span>'
            f'<div><div style="font-size:20px;font-weight:900;color:{color};">{t}</div>'
            f'<div style="font-size:15px;color:#9ca3af;margin-top:4px;">{s}</div></div></div>'
            for ic, t, s in items
        )
        return f"""
        <div style="background:#0d2035;border:2px solid {color};border-radius:16px;
                    padding:32px 36px;width:520px;">
          <div style="font-size:22px;font-weight:900;color:{color};
                      margin-bottom:24px;letter-spacing:1px;">{label}</div>
          {rows}
        </div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
    {BASE_CSS}
    body{{background:#0d1b2a;}}
    .hdr{{position:absolute;left:64px;top:36px;}}
    .badge{{display:inline-block;background:#FF6D00;color:#fff;font-size:14px;
            font-weight:900;padding:4px 14px;border-radius:20px;margin-bottom:12px;}}
    .ttl{{font-size:36px;font-weight:900;color:#fff;letter-spacing:-1px;}}
    .panels{{position:absolute;top:160px;left:64px;display:flex;gap:36px;}}
    </style></head><body>
    <div class="hdr">
      <div class="badge">図解②｜誤解vs正解</div>
      <div class="ttl">やりがちな3つの誤解と、正しい入浴設計</div>
    </div>
    <div class="panels">
      {card(ng_items, "#ef4444", "❌ よくある誤解")}
      {card(ok_items, "#4ade80", "✅ 効く入浴3原則")}
    </div>
    </body></html>"""
    render(html, "図解②_NGvsOK比較.png")


# ── 図解③ 3コツカードグリッド ────────────────────────────────
def fig3():
    cards_data = [
        ("#38bdf8", "コツ①", "温度と時間を固定",
         "38〜40℃", "10〜15分",
         "長く・熱くしすぎない", "気持ちよく入れる温度から"),
        ("#FF6D00", "コツ②", "就寝1〜2時間前に入る",
         "23時就寝 → 21〜22時入浴", "",
         "「帰ったらすぐ入る」ルールで固定", "タイミングが一番大事"),
        ("#4ade80", "コツ③", "入浴後の流れを設計",
         "✅ 軽いストレッチ", "✅ 照明を暗くする",
         "✅ ノンカフェイン飲料", "❌ スマホは眠りの邪魔"),
    ]
    cards_html = ""
    for color, badge, title, l1, l2, l3, l4 in cards_data:
        cards_html += f"""
        <div style="background:#0d2035;border-top:4px solid {color};
                    border-radius:12px;padding:28px 28px;width:340px;">
          <div style="display:inline-block;background:{color};color:#000;
                      font-size:13px;font-weight:900;padding:3px 12px;
                      border-radius:20px;margin-bottom:14px;">{badge}</div>
          <div style="font-size:22px;font-weight:900;color:#fff;
                      margin-bottom:18px;line-height:1.3;">{title}</div>
          <div style="font-size:17px;color:{color};font-weight:700;
                      margin-bottom:8px;">{l1}</div>
          {"" if not l2 else f'<div style="font-size:17px;color:{color};font-weight:700;margin-bottom:14px;">{l2}</div>'}
          <div style="font-size:15px;color:#9ca3af;line-height:1.7;">{l3}<br>{l4}</div>
        </div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
    {BASE_CSS}
    body{{background:#0d1b2a;}}
    .hdr{{position:absolute;left:64px;top:36px;}}
    .badge{{display:inline-block;background:#38bdf8;color:#000;font-size:14px;
            font-weight:900;padding:4px 14px;border-radius:20px;margin-bottom:12px;}}
    .ttl{{font-size:36px;font-weight:900;color:#fff;}}
    .row{{position:absolute;top:160px;left:64px;display:flex;gap:32px;}}
    </style></head><body>
    <div class="hdr">
      <div class="badge">図解③｜実践コツ</div>
      <div class="ttl">「疲れていてもできる」入浴3コツ</div>
    </div>
    <div class="row">{cards_html}</div>
    </body></html>"""
    render(html, "図解③_3コツカードグリッド.png")


# ── 図解④ 5日間チェック表 ──────────────────────────────────
def fig4():
    rows_html = ""
    for d in range(1, 6):
        bg = "#0d2035" if d % 2 == 1 else "#0a1828"
        rows_html += f"""
        <tr style="background:{bg};">
          <td style="padding:16px 24px;font-size:18px;font-weight:900;
                     color:#38bdf8;width:80px;text-align:center;">Day{d}</td>
          <td style="padding:16px 24px;font-size:17px;color:#9ca3af;text-align:center;">
            □ 就寝1〜2時間前に入れた</td>
          <td style="padding:16px 24px;font-size:17px;color:#9ca3af;text-align:center;">
            □ 38〜40℃ / 10〜15分</td>
          <td style="padding:16px 24px;font-size:17px;color:#9ca3af;text-align:center;">
            □ 寝つきの変化（◎/○/△）</td>
        </tr>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
    {BASE_CSS}
    body{{background:#0d1b2a;}}
    .hdr{{position:absolute;left:64px;top:36px;}}
    .badge{{display:inline-block;background:#4ade80;color:#000;font-size:14px;
            font-weight:900;padding:4px 14px;border-radius:20px;margin-bottom:12px;}}
    .ttl{{font-size:36px;font-weight:900;color:#fff;}}
    .wrap{{position:absolute;top:148px;left:64px;right:64px;}}
    table{{width:100%;border-collapse:collapse;border-radius:12px;overflow:hidden;}}
    th{{background:#1e3a5f;padding:14px 24px;font-size:16px;font-weight:900;
        color:#38bdf8;text-align:center;}}
    .note{{position:absolute;bottom:24px;left:64px;font-size:15px;color:#555;}}
    </style></head><body>
    <div class="hdr">
      <div class="badge">図解④｜5日間トライアル</div>
      <div class="ttl">5日間チェック表 ― 寝つきの変化を記録する</div>
    </div>
    <div class="wrap">
      <table>
        <tr>
          <th>日</th>
          <th>タイミング</th>
          <th>温度・時間</th>
          <th>寝つき</th>
        </tr>
        {rows_html}
      </table>
    </div>
    <div class="note">「昨日より少し早く眠れた」感覚が出たら前進のサイン</div>
    </body></html>"""
    render(html, "図解④_5日間チェック表.png")


# ── 図解⑤ リカバリーフロー ───────────────────────────────────
def fig5():
    steps = [
        ("#ef4444", "入れなかった夜", "シャワーで終わった", "自己嫌悪に0秒使う"),
        ("#FF6D00", "翌朝のアクション", "朝シャワーを3〜5分長めに", "「今日、機会があれば入る」設定"),
        ("#4ade80", "翌夜：再スタート", "38〜40℃、10〜15分", "8勝6敗でいい。続きから始める"),
    ]
    steps_html = ""
    for i, (color, title, l1, l2) in enumerate(steps):
        connector = "" if i == len(steps) - 1 else (
            f'<div style="width:4px;height:32px;background:linear-gradient({color},#FF6D00);'
            f'margin:0 auto;opacity:0.5;"></div>')
        steps_html += f"""
        <div style="background:#0d2035;border-left:6px solid {color};
                    border-radius:8px;padding:18px 24px;">
          <div style="font-size:20px;font-weight:900;color:{color};margin-bottom:6px;">{title}</div>
          <div style="font-size:16px;color:#fff;margin-bottom:4px;">→ {l1}</div>
          <div style="font-size:14px;color:#9ca3af;">{l2}</div>
        </div>{connector}"""

    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
    {BASE_CSS}
    body{{background:#0d1b2a;}}
    .hdr{{position:absolute;left:64px;top:36px;}}
    .badge{{display:inline-block;background:#ef4444;color:#fff;font-size:14px;
            font-weight:900;padding:4px 14px;border-radius:20px;margin-bottom:12px;}}
    .ttl{{font-size:36px;font-weight:900;color:#fff;}}
    .col{{position:absolute;top:148px;left:200px;right:200px;}}
    .tagline{{position:absolute;bottom:24px;left:64px;right:64px;text-align:center;
              font-size:20px;font-weight:900;color:#4ade80;}}
    </style></head><body>
    <div class="hdr">
      <div class="badge">図解⑤｜リカバリー</div>
      <div class="ttl">入れなかった日の翌朝リカバリーフロー</div>
    </div>
    <div class="col">{steps_html}</div>
    <div class="tagline">8勝6敗でいい ― 次の1手だけ考える</div>
    </body></html>"""
    render(html, "図解⑤_リカバリーフロー.png")


if __name__ == "__main__":
    print("第41回 図解5枚 生成開始...\n")
    fig1(); fig2(); fig3(); fig4(); fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))
