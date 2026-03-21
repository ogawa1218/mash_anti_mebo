#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 X投稿用カード画像 10枚生成スクリプト（図解版）"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARTICLE_DIR = Path(__file__).parent
OUTPUT_DIR  = ARTICLE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
HASHTAG = "#第 慢性炎症"
FIXED_TAGS = "\n\n#ダイエット #メタボ #習慣化 #健康診断 #Longevity"

BASE_CSS = (
    "@font-face{font-family:'NJ';src:url('" + FONT + "');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}"
    "body{width:1280px;height:720px;overflow:hidden;background:#0d1b2a;"
    "font-family:'NJ','Meiryo',sans-serif;position:relative;}"
    ".num{position:absolute;top:44px;right:56px;font-size:22px;font-weight:700;color:#444;}"
    ".author{position:absolute;bottom:22px;left:56px;font-size:18px;font-weight:400;color:#3a3a3a;}"
    ".series{position:absolute;bottom:22px;right:56px;font-size:18px;font-weight:700;}"
)

TWEETS = [
    "健診でE判定。\n「お腹が出てるだけでしょ」と思った。\n\n実は内臓脂肪は、24時間炎症物質を出し続ける「工場」だった。\n\nこの炎症が、心臓病・糖尿病・認知症・老化——全部の共通原因だと分かっている。\n\n↓続き（2/10）" + FIXED_TAGS,
    "「Inflammaging（インフラメイジング）」\n\n炎症＋老化の造語。2018年にNature Reviews誌で体系化された。\n\n内臓脂肪からTNF-α、IL-6、CRPが24時間放出→全身を巡り臓器にダメージ→老化が加速。\n\n↓続き（3/10）" + FIXED_TAGS,
    "「メタボを治す＝老化を遅らせる」\n\nこれは比喩じゃない。科学的な因果関係。\n\n内臓脂肪を減らす→慢性炎症が下がる→心臓病・糖尿病・認知症・老化リスクが下がる。\n\nダイエットの意味が変わる。\n\n↓続き（4/10）" + FIXED_TAGS,
    "2017年、CANTOS試験（Ridker, NEJM）。\n\n1万人以上の大規模臨床試験。炎症を抑える薬で心臓発作リスクが15%低下。\n\nコレステロールは変えてない。炎症だけ下げた。\n\n炎症そのものが心臓病の原因だと初めて臨床で証明された。\n\n↓続き（5/10）" + FIXED_TAGS,
    "僕は32歳・100kgの時、高感度CRPが基準値超えだった。\n\n意味すら分かってなかった。\n\n68kgまで落とした後、CRPは基準値内に。疲れにくくなった。風邪を引かなくなった。関節痛が消えた。\n\n全部「炎症が下がった」サインだった。\n\n↓続き（6/10）" + FIXED_TAGS,
    "最も確実な「抗炎症」は生活習慣。\n\n1. 内臓脂肪を減らす\n2. オメガ3（青魚）を摂る\n3. 超加工食品を減らす\n4. ゾーン2運動\n\n薬でもサプリでもない。この4つが全て。\n\n↓続き（7/10）" + FIXED_TAGS,
    "続けるコツはif-then設計。\n\n「もしコンビニに入ったら→菓子パンじゃなくサラダチキン」\n「もし喉が渇いたら→ジュースじゃなく水」\n「もし魚の選択肢があったら→青魚を選ぶ」\n\n意志力ゼロ。仕組みで変える。\n\n↓続き（8/10）" + FIXED_TAGS,
    "「飲み会で食べすぎた...」\n\n大丈夫。慢性炎症は1回の暴食で致命的には悪化しない。\n\n復帰if-then：「もし昨日食べすぎたら→翌朝の1食だけ軽くする」\n\n8勝6敗でOK。6割で炎症は下がる。\n\n↓続き（9/10）" + FIXED_TAGS,
    "ダイエットの本当の目的は「見た目」じゃない。\n\n「体内の炎を鎮めること」。\n\nそう考えると、1kgの変化が持つ意味がまったく違って見える。\n\nメタボを治すことは、未来の自分を守ること。\n\n↓続き（10/10）" + FIXED_TAGS,
    "今夜やること1つだけ。\n\n「明日の食事から、超加工食品を1つ減らす」\n\n菓子パン→おにぎり。ジュース→水。それだけでいい。\n\nあなたの体内の炎を、少しずつ鎮めていこう。\n\nnoteで全文公開中\nhttps://note.com/mash_anti_metabo" + FIXED_TAGS,
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]


def card_01():
    items = [
        ("健診E判定", "「お腹が出てるだけ」と軽視", "#ef4444"),
        ("内臓脂肪", "24時間炎症物質を放出中", "#ef4444"),
        ("慢性炎症", "心臓病・糖尿病・認知症・老化の原因", "#FF6D00"),
        ("自覚なし", "痛みも熱もない。静かに進行する", "#ef4444"),
    ]
    items_html = ""
    for i, (label, desc, color) in enumerate(items):
        top = 180 + i * 110
        items_html += (
            "<div style='position:absolute;top:" + str(top) + "px;left:56px;right:56px;"
            "display:flex;align-items:center;gap:20px;'>"
            "<div style='width:16px;height:16px;border-radius:50%;background:" + color + ";flex-shrink:0;"
            "box-shadow:0 0 12px " + color + "60;'></div>"
            "<div style='flex:1;background:#1e3a5f;border-radius:10px;padding:16px 24px;'>"
            "<div style='font-size:22px;font-weight:700;color:" + color + ";'>" + label + "</div>"
            "<div style='font-size:16px;color:#9ca3af;margin-top:4px;'>" + desc + "</div></div></div>")
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>1/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>「お腹が出てるだけ」の裏側</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>メタボの本当の問題は「見た目」じゃない。</div></div>"
        + items_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p></body></html>")


def card_02():
    steps = [
        ("内臓脂肪", "TNF-α / IL-6 / CRP\nを24時間分泌", "#ef4444"),
        ("血液を巡る", "炎症物質が\n全身の臓器へ", "#FF6D00"),
        ("臓器にダメージ", "血管・脳・膵臓\nDNAを傷つける", "#ef4444"),
        ("老化が加速", "生物学的年齢が\n実年齢を超える", "#8b5cf6"),
    ]
    steps_html = ""
    for i, (label, desc, color) in enumerate(steps):
        left = 56 + i * 300
        steps_html += (
            "<div style='position:absolute;top:220px;left:" + str(left) + "px;width:268px;'>"
            "<div style='background:#1e3a5f;border-radius:14px;padding:20px;border-top:4px solid " + color + ";"
            "text-align:center;height:180px;display:flex;flex-direction:column;justify-content:center;'>"
            "<div style='font-size:20px;font-weight:800;color:" + color + ";'>" + label + "</div>"
            "<div style='font-size:15px;color:#e2e8f0;margin-top:8px;white-space:pre-line;'>" + desc + "</div></div></div>")
        if i < 3:
            steps_html += (
                "<div style='position:absolute;top:300px;left:" + str(left + 276) + "px;"
                "font-size:24px;font-weight:900;color:#4a5568;'>→</div>")
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>2/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>Inflammaging のメカニズム</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>炎症（Inflammation）＋ 老化（Aging）＝ 慢性炎症老化</div></div>"
        + steps_html +
        "<div style='position:absolute;bottom:60px;left:56px;right:56px;"
        "background:#162d4a;border-radius:12px;padding:14px 24px;text-align:center;'>"
        "<span style='font-size:16px;color:#9ca3af;'>Franceschi et al. 2018, Nature Reviews Endocrinology</span></div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p></body></html>")


def card_03():
    cards = [
        ("STEP 1", "内臓脂肪を減らす", "炎症の火元を断つ", "#ef4444"),
        ("STEP 2", "慢性炎症が下がる", "CRP・IL-6が低下", "#FF6D00"),
        ("STEP 3", "老化が遅くなる", "4大リスクが低下", "#4ade80"),
    ]
    cards_html = ""
    for i, (step, title, sub, color) in enumerate(cards):
        left = 56 + i * 400
        cards_html += (
            "<div style='position:absolute;top:200px;left:" + str(left) + "px;width:360px;height:260px;"
            "background:#1e3a5f;border-radius:16px;padding:28px;border-top:4px solid " + color + ";'>"
            "<div style='font-size:14px;font-weight:700;color:" + color + ";letter-spacing:2px;'>" + step + "</div>"
            "<div style='font-size:30px;font-weight:900;color:#fff;margin-top:16px;'>" + title + "</div>"
            "<div style='width:40px;height:3px;background:" + color + ";margin:20px 0;'></div>"
            "<div style='font-size:18px;color:#e2e8f0;'>" + sub + "</div></div>")
        if i < 2:
            cards_html += (
                "<div style='position:absolute;top:310px;left:" + str(left + 370) + "px;"
                "font-size:28px;font-weight:900;color:#9ca3af;'>→</div>")
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>3/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>メタボを治す ＝ 老化を遅らせる</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>比喩じゃない。科学的な因果関係。</div></div>"
        + cards_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#FF6D00;'>" + HASHTAG + "</p></body></html>")


def card_04():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>4/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>CANTOS試験が証明したこと</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>1万人超の大規模臨床試験（Ridker 2017, NEJM）</div></div>"
        # バーグラフ
        "<div style='position:absolute;top:160px;left:56px;right:56px;'>"
        "<div style='margin-bottom:24px;'>"
        "<div style='font-size:16px;color:#9ca3af;margin-bottom:8px;'>プラセボ群（炎症そのまま）</div>"
        "<div style='background:#1e3a5f;border-radius:8px;height:56px;position:relative;'>"
        "<div style='background:linear-gradient(90deg,#ef4444,#ef444480);height:100%;width:100%;border-radius:8px;'></div>"
        "<div style='position:absolute;right:16px;top:14px;font-size:22px;font-weight:800;color:#fff;'>100%</div></div></div>"
        "<div style='margin-bottom:24px;'>"
        "<div style='font-size:16px;color:#9ca3af;margin-bottom:8px;'>カナキヌマブ群（炎症を抑制）</div>"
        "<div style='background:#1e3a5f;border-radius:8px;height:56px;position:relative;'>"
        "<div style='background:linear-gradient(90deg,#4ade80,#4ade8080);height:100%;width:85%;border-radius:8px;'></div>"
        "<div style='position:absolute;right:16px;top:14px;font-size:22px;font-weight:800;color:#fff;'>85%</div></div></div></div>"
        # 結果ボックス
        "<div style='position:absolute;top:380px;left:56px;right:56px;"
        "background:linear-gradient(90deg,rgba(74,222,128,.12),rgba(74,222,128,.04));"
        "border:2px solid #4ade80;border-radius:16px;padding:24px 32px;text-align:center;'>"
        "<div style='font-size:28px;font-weight:900;color:#4ade80;'>心臓発作リスク 15%低下</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:8px;'>コレステロール値は変化なし。炎症だけ下げた結果。</div></div>"
        # 意義
        "<div style='position:absolute;top:510px;left:56px;right:56px;"
        "background:#162d4a;border-radius:12px;padding:18px 24px;display:flex;gap:24px;align-items:center;'>"
        "<div style='font-size:18px;font-weight:800;color:#FF6D00;flex-shrink:0;'>歴史的意義</div>"
        "<div style='font-size:16px;color:#e2e8f0;'>炎症そのものが心臓病の原因であると初めて臨床試験で証明された</div></div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p></body></html>")


def card_05():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>5/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#4ade80;'>CRPが基準値に戻った日</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>100kg→68kg。数値だけじゃない変化。</div></div>"
        # Before
        "<div style='position:absolute;top:150px;left:56px;width:560px;height:400px;"
        "background:#1e3a5f;border-radius:16px;padding:28px;border-top:4px solid #ef4444;'>"
        "<div style='font-size:18px;font-weight:700;color:#ef4444;letter-spacing:2px;'>BEFORE｜100kg</div>"
        "<div style='margin-top:20px;display:flex;flex-direction:column;gap:14px;'>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#ef4444;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>高感度CRP：基準値超え</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#ef4444;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>すぐ疲れる・風邪をひきやすい</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#ef4444;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>膝・腰の慢性的な痛み</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#ef4444;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>「ちょっと高いだけ」と放置</div></div></div>"
        "<div style='position:absolute;bottom:20px;left:28px;font-size:56px;font-weight:900;color:rgba(239,68,68,.12);'>BEFORE</div></div>"
        # After
        "<div style='position:absolute;top:150px;right:56px;width:560px;height:400px;"
        "background:#1e3a5f;border-radius:16px;padding:28px;border-top:4px solid #4ade80;'>"
        "<div style='font-size:18px;font-weight:700;color:#4ade80;letter-spacing:2px;'>AFTER｜68kg</div>"
        "<div style='margin-top:20px;display:flex;flex-direction:column;gap:14px;'>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#4ade80;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>CRP：基準値内に回復</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#4ade80;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>疲れにくくなった</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#4ade80;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>風邪をほとんどひかない</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#4ade80;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>関節痛が消えた</div></div></div>"
        "<div style='position:absolute;bottom:20px;right:28px;font-size:56px;font-weight:900;color:rgba(74,222,128,.12);'>AFTER</div></div>"
        "<div style='position:absolute;bottom:40px;left:56px;right:56px;text-align:center;'>"
        "<span style='font-size:18px;color:#9ca3af;'>全部「慢性炎症が下がった」サイン</span></div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#4ade80;'>" + HASHTAG + "</p></body></html>")


def card_06():
    rows = [
        ("内臓脂肪を減らす", "体重5%減でCRP低下", "#ef4444"),
        ("オメガ3（青魚）", "週2-3回サバ・イワシ", "#38bdf8"),
        ("超加工食品を減らす", "1日1つ減らすだけ", "#FF6D00"),
        ("ゾーン2運動", "週2-3回 10分から", "#4ade80"),
    ]
    rows_html = ""
    for name, action, color in rows:
        rows_html += (
            "<tr><td style='padding:18px 20px;font-size:20px;font-weight:700;color:" + color + ";"
            "border-bottom:1px solid #1e3a5f;'>" + name + "</td>"
            "<td style='padding:18px 20px;font-size:18px;color:#e2e8f0;border-bottom:1px solid #1e3a5f;'>" + action + "</td></tr>")
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        "table{width:calc(100% - 112px);position:absolute;top:170px;left:56px;border-collapse:collapse;}"
        "th{padding:14px 20px;font-size:14px;font-weight:700;color:#FF6D00;text-align:left;"
        "border-bottom:2px solid #FF6D00;background:#0d2035;}</style></head><body>"
        "<div class='num'>6/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>抗炎症 4つの戦略</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>薬でもサプリでもない。生活習慣が最強。</div></div>"
        "<table><tr><th>戦略</th><th>始め方</th></tr>" + rows_html + "</table>"
        "<div style='position:absolute;bottom:80px;left:56px;right:56px;"
        "background:linear-gradient(90deg,rgba(74,222,128,.1),rgba(74,222,128,.05));"
        "border:1px solid #4ade80;border-radius:12px;padding:18px 24px;text-align:center;'>"
        "<span style='font-size:22px;font-weight:800;color:#4ade80;'>まず1つだけ。超加工食品を1つ減らす。</span></div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p></body></html>")


def card_07():
    steps = [
        ("1", "if-thenを1つ決める", "「もしコンビニに入ったら\n→菓子パンでなくサラダチキン」", "#FF6D00"),
        ("2", "環境を整える", "冷蔵庫の目の高さにナッツ\nお菓子は棚の奥へ", "#FF6D00"),
        ("3", "今日1つだけ減らす", "全部やめなくていい\n1つ減らせば炎症は下がり始める", "#4ade80"),
    ]
    steps_html = ""
    for i, (num, title, sub, color) in enumerate(steps):
        top = 160 + i * 175
        steps_html += (
            "<div style='position:absolute;top:" + str(top) + "px;left:56px;right:56px;"
            "display:flex;align-items:center;gap:24px;'>"
            "<div style='width:72px;height:72px;border-radius:50%;background:" + color + ";"
            "display:flex;align-items:center;justify-content:center;flex-shrink:0;"
            "font-size:32px;font-weight:900;color:#fff;'>" + num + "</div>"
            "<div style='flex:1;background:#1e3a5f;border-radius:14px;padding:22px 28px;"
            "border-left:4px solid " + color + ";'>"
            "<div style='font-size:24px;font-weight:800;color:#fff;'>" + title + "</div>"
            "<div style='font-size:16px;color:#9ca3af;margin-top:6px;white-space:pre-line;'>" + sub + "</div></div></div>")
        if i < 2:
            steps_html += (
                "<div style='position:absolute;top:" + str(top + 100) + "px;left:83px;"
                "width:2px;height:60px;background:#1e3a5f;'></div>")
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>7/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>抗炎症生活を仕組みにする</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>if-then設計×環境設計で意志力を外す</div></div>"
        + steps_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#FF6D00;'>" + HASHTAG + "</p></body></html>")


def card_08():
    steps = [
        ("食べすぎた日", "「飲み会でつい...」", "#ef4444"),
        ("翌朝の1食を軽くする", "ゆで卵＋サラダだけでOK", "#FF6D00"),
        ("ループに戻る", "8勝6敗で十分", "#4ade80"),
    ]
    steps_html = ""
    for i, (title, sub, color) in enumerate(steps):
        left = 56 + i * 400
        steps_html += (
            "<div style='position:absolute;top:220px;left:" + str(left) + "px;width:360px;'>"
            "<div style='background:#1e3a5f;border-radius:16px;padding:28px;border-top:4px solid " + color + ";"
            "text-align:center;height:200px;display:flex;flex-direction:column;justify-content:center;'>"
            "<div style='font-size:26px;font-weight:800;color:" + color + ";'>" + title + "</div>"
            "<div style='font-size:18px;color:#e2e8f0;margin-top:12px;'>" + sub + "</div></div></div>")
        if i < 2:
            steps_html += (
                "<div style='position:absolute;top:305px;left:" + str(left + 370) + "px;"
                "font-size:28px;font-weight:900;color:#9ca3af;'>→</div>")
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>8/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#4ade80;'>崩れても大丈夫。戻り方はこれ。</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>1回の暴食で慢性炎症は致命的に悪化しない。</div></div>"
        + steps_html +
        "<div style='position:absolute;bottom:60px;left:56px;right:56px;"
        "background:linear-gradient(90deg,rgba(74,222,128,.1),rgba(74,222,128,.05));"
        "border:1px solid #4ade80;border-radius:12px;padding:18px 24px;text-align:center;'>"
        "<span style='font-size:22px;font-weight:800;color:#4ade80;'>if-then復帰：「もし食べすぎたら → 翌朝1食を軽くする」</span></div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#4ade80;'>" + HASHTAG + "</p></body></html>")


def card_09():
    damages = [
        ("心臓病", "動脈硬化を加速", "85", "#ef4444"),
        ("糖尿病", "インスリン抵抗性", "70", "#FF6D00"),
        ("認知症", "脳の炎症・アミロイドβ蓄積", "60", "#38bdf8"),
        ("老化加速", "テロメア短縮・DNA損傷", "90", "#8b5cf6"),
    ]
    bars_html = ""
    for i, (name, desc, pct, color) in enumerate(damages):
        top = 190 + i * 110
        bars_html += (
            "<div style='position:absolute;top:" + str(top) + "px;left:56px;right:56px;'>"
            "<div style='display:flex;align-items:center;gap:16px;margin-bottom:8px;'>"
            "<div style='font-size:18px;font-weight:700;color:" + color + ";width:100px;'>" + name + "</div>"
            "<div style='font-size:14px;color:#9ca3af;'>" + desc + "</div></div>"
            "<div style='background:#0d2035;border-radius:8px;height:40px;position:relative;overflow:hidden;'>"
            "<div style='background:linear-gradient(90deg," + color + "," + color + "60);height:100%;"
            "width:" + pct + "%;border-radius:8px;'></div></div></div>")
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>9/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>慢性炎症が引き起こす4つのダメージ</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>「1つの病気の原因」ではなく「老化そのものの主要ドライバー」</div></div>"
        + bars_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p></body></html>")


def card_10():
    checks = [
        ("内臓脂肪は炎症の「工場」"),
        ("慢性炎症が心臓病・糖尿病・認知症・老化の共通原因"),
        ("メタボを治す = 老化を遅らせる"),
        ("抗炎症は薬ではなく生活習慣"),
        ("if-then設計で仕組みにする"),
        ("8勝6敗でOK。崩れても戻れる"),
    ]
    checks_html = ""
    for i, text in enumerate(checks):
        top = 160 + i * 56
        checks_html += (
            "<div style='position:absolute;top:" + str(top) + "px;left:56px;right:400px;"
            "display:flex;align-items:center;gap:12px;'>"
            "<div style='font-size:24px;'>&#x2705;</div>"
            "<div style='font-size:20px;color:#e2e8f0;font-weight:600;'>" + text + "</div></div>")
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS + "</style></head><body>"
        "<div class='num'>10/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>今夜やること、1つだけ。</div></div>"
        + checks_html +
        "<div style='position:absolute;top:160px;right:56px;width:320px;height:380px;"
        "background:linear-gradient(180deg,#FF6D00,#e65100);border-radius:16px;padding:28px;"
        "display:flex;flex-direction:column;justify-content:center;text-align:center;'>"
        "<div style='font-size:20px;font-weight:700;color:rgba(255,255,255,.8);'>今夜の1アクション</div>"
        "<div style='font-size:28px;font-weight:900;color:#fff;margin-top:16px;line-height:1.4;'>"
        "超加工食品を<br>1つだけ<br>減らす</div>"
        "<div style='width:60px;height:3px;background:rgba(255,255,255,.4);margin:20px auto;'></div>"
        "<div style='font-size:16px;color:rgba(255,255,255,.7);'>菓子パン→おにぎり<br>ジュース→水</div>"
        "<div style='margin-top:20px;background:rgba(255,255,255,.15);border-radius:10px;padding:12px;'>"
        "<div style='font-size:14px;color:#fff;font-weight:700;'>noteで全文公開中</div></div></div>"
        "<div style='position:absolute;bottom:60px;left:56px;'>"
        "<span style='font-size:16px;color:#9ca3af;'>体内の炎を、少しずつ鎮めていこう。</span></div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#FF6D00;'>" + HASHTAG + "</p></body></html>")


CARD_FUNCS = [card_01, card_02, card_03, card_04, card_05,
              card_06, card_07, card_08, card_09, card_10]


def render(html, fname):
    tmp = ARTICLE_DIR / "_tmp_xcard.html"
    out = OUTPUT_DIR / fname
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.goto("file:///" + str(tmp).replace("\\", "/"))
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(out), full_page=False)
        b.close()
    tmp.unlink(missing_ok=True)


def save_tweets():
    out = OUTPUT_DIR / "x_posts.md"
    lines = ["# 第 X投稿スレッド（10本）\n\n"]
    for i, tweet in enumerate(TWEETS):
        tag = CARD_TAGS[i]
        lines.append(
            "## 投稿" + str(i+1) + "/10｜" + tag + "\n\n```\n" + tweet.strip() + "\n```\n\n"
            "![カード" + str(i+1) + "](x_post_" + str(i+1).zfill(2) + ".png)\n\n---\n\n")
    out.write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    print("第 X投稿カード画像（図解版）生成開始...\n")
    for i, func in enumerate(CARD_FUNCS):
        html = func()
        fname = "x_post_" + str(i+1).zfill(2) + ".png"
        render(html, fname)
        print("OK: " + fname + "  [" + CARD_TAGS[i] + "]")
    save_tweets()
    print("\n全10枚完了。保存先: " + str(OUTPUT_DIR))

