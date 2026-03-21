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
HASHTAG = "#第 ミトコンドリア"
FIXED_TAGS = "\n\n#ダイエット #メタボ #習慣化 #運動習慣 #Longevity"

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
    "「最近、疲れやすくなった」\n「階段で息が上がる」\n「回復が遅い」\n\n40代、こう感じていませんか？\n\n実はこれ、歳のせいだけじゃない。あなたの細胞の中の「エンジン」が劣化しているサインです。\n\n↓続き（2/10）" + FIXED_TAGS,
    "そのエンジンの名前は「ミトコンドリア」。\n\n中学の理科で習ったやつ。細胞の中でエネルギーを作る工場。\n\n30代から機能が落ち始める。代謝が落ちる。脂肪が燃えにくくなる。疲れやすくなる。\n\nこれが「老化」の正体の一つ。\n\n↓続き（3/10）" + FIXED_TAGS,
    "でも、このミトコンドリアは「再起動」できる。\n\n方法は運動。しかも「ゆるい運動」が最強。\n\n会話できるギリギリのペースで歩く。これだけで細胞レベルの若返りが始まる。\n\n↓続き（4/10）" + FIXED_TAGS,
    "2011年、カナダの研究チームがPNASに発表。\n\n運動を続けたマウスの老化が逆転した。ミトコンドリアの数と機能が回復。\n\nさらに2017年のMayo Clinic研究では、12週間の運動で高齢者のミトコンドリア機能が69%改善。\n\n↓続き（5/10）" + FIXED_TAGS,
    "僕は32歳・100kgの時、5分歩くだけで息切れしていた。\n\n3ヶ月後、30分歩いても平気になった。体重だけじゃ説明できない変化だった。\n\n今思うと、ミトコンドリアが活性化された瞬間だったと理解している。\n\n↓続き（6/10）" + FIXED_TAGS,
    "最も効果的な運動は「ゾーン2トレーニング」。\n\n・早歩き（少し息が上がる程度）\n・軽いジョギング\n・自転車をゆるく漕ぐ\n\n10分からでOK。追い込む必要なし。「ゆるく長く」が黄金ルール。\n\n↓続き（7/10）" + FIXED_TAGS,
    "続ける仕組みはif-then設計。\n\n「もし昼休みになったら→10分速歩き」\n「もし駅に着いたら→1駅手前で降りる」\n\nもう一つ。運動ウェアを前日に玄関に置く。意志力に頼らず、環境で行動を変える。\n\n↓続き（8/10）" + FIXED_TAGS,
    "「3日サボってしまった…」\n\n大丈夫。ミトコンドリアは習慣的な刺激の積み重ねで変わる。3日休んでも再開すればまた動く。\n\n復帰if-then：「もし昨日やらなかったら→翌朝5分だけ歩く」\n\n8勝6敗でOK。\n\n↓続き（9/10）" + FIXED_TAGS,
    "運動は「カロリーを燃やすもの」じゃない。\n\n「細胞を若返らせるもの」。\n\nこの認識の転換が、運動を「やらなきゃ」から「やりたい」に変えてくれる。\n\nミトコンドリアは、あなたが動き出すのを待っている。\n\n↓続き（10/10）" + FIXED_TAGS,
    "今夜やること1つだけ。\n\n「明日の朝、10分だけ速歩きする」と決める。\n\nできたらボーナス。できなくても翌日やればいい。\n\nミトコンドリアの若返りは今日始まる。\n\n詳しくはnoteで全文公開中\nhttps://note.com/mash_anti_metabo" + FIXED_TAGS,
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]


def card_01():
    """共感: タイムライン型"""
    items = [
        ("7:00", "朝起きてもダルい", "#ef4444"),
        ("12:00", "ランチ後に猛烈な眠気", "#ef4444"),
        ("15:00", "3階まで階段で息切れ", "#FF6D00"),
        ("19:00", "帰宅したら何もする気力なし", "#ef4444"),
        ("23:00", "「歳だから仕方ない」と諦める", "#ef4444"),
    ]
    items_html = ""
    for i, (time, event, color) in enumerate(items):
        top = 160 + i * 90
        items_html += (
            "<div style='position:absolute;top:" + str(top) + "px;left:120px;right:56px;"
            "display:flex;align-items:center;gap:20px;'>"
            "<div style='font-size:22px;font-weight:700;color:#9ca3af;width:80px;'>" + time + "</div>"
            "<div style='width:16px;height:16px;border-radius:50%;background:" + color + ";flex-shrink:0;"
            "box-shadow:0 0 12px " + color + "60;'></div>"
            "<div style='flex:1;background:#1e3a5f;border-radius:10px;padding:14px 20px;"
            "font-size:20px;font-weight:600;color:#e2e8f0;'>" + event + "</div>"
            "</div>"
        )
        if i < 4:
            items_html += (
                "<div style='position:absolute;top:" + str(top + 50) + "px;left:208px;"
                "width:2px;height:40px;background:#1e3a5f;'></div>"
            )
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        "<div class='num'>1/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>40代の1日、心当たりありませんか？</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>それ、「歳のせい」じゃないかもしれない。</div>"
        "</div>"
        + items_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p>"
        "</body></html>")


def card_02():
    """原因: フロー図型"""
    steps = [
        ("30代〜", "ミトコンドリア\n機能低下開始", "#38bdf8"),
        ("代謝↓", "脂肪が\n燃えにくくなる", "#FF6D00"),
        ("疲労↑", "疲れやすく\n回復が遅い", "#ef4444"),
        ("老化加速", "細胞レベルで\n劣化が進む", "#ef4444"),
    ]
    steps_html = ""
    for i, (label, desc, color) in enumerate(steps):
        left = 56 + i * 300
        steps_html += (
            "<div style='position:absolute;top:240px;left:" + str(left) + "px;width:260px;'>"
            "<div style='background:#1e3a5f;border-radius:14px;padding:24px;border-top:4px solid " + color + ";"
            "text-align:center;height:160px;display:flex;flex-direction:column;justify-content:center;'>"
            "<div style='font-size:20px;font-weight:800;color:" + color + ";'>" + label + "</div>"
            "<div style='font-size:16px;color:#e2e8f0;margin-top:8px;white-space:pre-line;'>" + desc + "</div>"
            "</div></div>"
        )
        if i < 3:
            steps_html += (
                "<div style='position:absolute;top:310px;left:" + str(left + 268) + "px;"
                "font-size:28px;font-weight:900;color:#4a5568;'>→</div>"
            )
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        "<div class='num'>2/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>「疲れやすさ」の正体</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>ミトコンドリア＝細胞のエンジン。30代から劣化が始まる。</div>"
        "</div>"
        + steps_html +
        "<div style='position:absolute;bottom:60px;left:56px;right:56px;"
        "background:#162d4a;border-radius:12px;padding:16px 24px;text-align:center;'>"
        "<span style='font-size:18px;color:#9ca3af;'>ミトコンドリアの機能</span>"
        "<span style='font-size:18px;font-weight:800;color:#38bdf8;'> = </span>"
        "<span style='font-size:18px;font-weight:800;color:#fff;'>生物学的な若さ</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p>"
        "</body></html>")


def card_03():
    """解決策: 横3列ステップカード"""
    cards = [
        ("STEP 1", "ゾーン2運動", "話せるペースで歩く", "#38bdf8"),
        ("STEP 2", "スイッチON", "PGC-1α活性化", "#FF6D00"),
        ("STEP 3", "細胞若返り", "ミトコンドリア再生", "#4ade80"),
    ]
    cards_html = ""
    for i, (step, title, sub, color) in enumerate(cards):
        left = 56 + i * 400
        cards_html += (
            "<div style='position:absolute;top:200px;left:" + str(left) + "px;width:360px;height:300px;"
            "background:#1e3a5f;border-radius:16px;padding:28px;border-top:4px solid " + color + ";'>"
            "<div style='font-size:14px;font-weight:700;color:" + color + ";letter-spacing:2px;'>" + step + "</div>"
            "<div style='font-size:32px;font-weight:900;color:#fff;margin-top:16px;'>" + title + "</div>"
            "<div style='width:40px;height:3px;background:" + color + ";margin:20px 0;border-radius:2px;'></div>"
            "<div style='font-size:20px;color:#e2e8f0;'>" + sub + "</div>"
            "</div>"
        )
        if i < 2:
            cards_html += (
                "<div style='position:absolute;top:330px;left:" + str(left + 370) + "px;"
                "font-size:28px;font-weight:900;color:#9ca3af;'>→</div>"
            )
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        "<div class='num'>3/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>「ゆるい運動」が最強の若返り法</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>追い込む必要なし。細胞レベルで変わる仕組み。</div>"
        "</div>"
        + cards_html +
        "<div style='position:absolute;bottom:36px;left:56px;font-size:14px;color:#4a5568;'>"
        "Hood et al. 2019, Journal of Physiology</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#FF6D00;'>" + HASHTAG + "</p>"
        "</body></html>")


def card_04():
    """仕組み: 番号バッジ付きカード＋出典バッジ"""
    facts = [
        ("1", "運動でミトコンドリアが増殖", "PGC-1αスイッチで工場が増える", "Safdar et al. 2011, PNAS", "#38bdf8"),
        ("2", "壊れたミトコンドリアを掃除", "ミトファジーで古い部品を分解・再利用", "大隅良典 2016 ノーベル賞", "#38bdf8"),
        ("3", "12週間で機能69%改善", "高齢者ほど改善幅が大きかった", "Robinson et al. 2017, Cell Metabolism", "#FF6D00"),
    ]
    facts_html = ""
    for i, (num, title, sub, source, color) in enumerate(facts):
        top = 170 + i * 170
        facts_html += (
            "<div style='position:absolute;top:" + str(top) + "px;left:56px;right:56px;"
            "display:flex;align-items:center;gap:24px;'>"
            "<div style='width:64px;height:64px;border-radius:50%;background:" + color + ";"
            "display:flex;align-items:center;justify-content:center;flex-shrink:0;"
            "font-size:28px;font-weight:900;color:#fff;'>" + num + "</div>"
            "<div style='flex:1;background:#1e3a5f;border-radius:14px;padding:20px 24px;'>"
            "<div style='font-size:22px;font-weight:800;color:#fff;'>" + title + "</div>"
            "<div style='font-size:15px;color:#9ca3af;margin-top:4px;'>" + sub + "</div>"
            "<div style='display:inline-block;background:#162d4a;border-radius:8px;padding:4px 12px;"
            "font-size:12px;color:#6b7280;margin-top:8px;'>" + source + "</div>"
            "</div></div>"
        )
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        "<div class='num'>4/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>科学が証明した3つの事実</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>ミトコンドリア×運動の研究データ</div>"
        "</div>"
        + facts_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p>"
        "</body></html>")


def card_05():
    """効果: Before/After比較パネル"""
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        "<div class='num'>5/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#4ade80;'>100kg→68kg 体感の変化</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>体重だけじゃ説明できない変化があった。</div>"
        "</div>"
        # Before
        "<div style='position:absolute;top:150px;left:56px;width:560px;height:420px;"
        "background:#1e3a5f;border-radius:16px;padding:28px;border-top:4px solid #ef4444;'>"
        "<div style='font-size:18px;font-weight:700;color:#ef4444;letter-spacing:2px;'>BEFORE｜100kg</div>"
        "<div style='margin-top:20px;display:flex;flex-direction:column;gap:16px;'>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#ef4444;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>5分歩くだけで息切れ</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#ef4444;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>朝起きても体がダルい</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#ef4444;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>階段2階分で膝に手をつく</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#ef4444;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>「太ってるから当然」と諦め</div></div>"
        "</div>"
        "<div style='position:absolute;bottom:20px;left:28px;font-size:64px;font-weight:900;color:rgba(239,68,68,.15);'>BEFORE</div>"
        "</div>"
        # After
        "<div style='position:absolute;top:150px;right:56px;width:560px;height:420px;"
        "background:#1e3a5f;border-radius:16px;padding:28px;border-top:4px solid #4ade80;'>"
        "<div style='font-size:18px;font-weight:700;color:#4ade80;letter-spacing:2px;'>AFTER｜68kg</div>"
        "<div style='margin-top:20px;display:flex;flex-direction:column;gap:16px;'>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#4ade80;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>30分歩いても平気</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#4ade80;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>朝の体の軽さが別人</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#4ade80;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>フルマラソン サブ3達成</div></div>"
        "<div style='display:flex;align-items:center;gap:12px;'>"
        "<div style='width:8px;height:8px;border-radius:50%;background:#4ade80;'></div>"
        "<div style='font-size:20px;color:#e2e8f0;'>ミトコンドリアが再起動した</div></div>"
        "</div>"
        "<div style='position:absolute;bottom:20px;right:28px;font-size:64px;font-weight:900;color:rgba(74,222,128,.15);'>AFTER</div>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#4ade80;'>" + HASHTAG + "</p>"
        "</body></html>")


def card_06():
    """設計: テーブル型"""
    rows = [
        ("早歩き", "話せるギリギリ", "10-30分", "毎日OK", "#4ade80"),
        ("ジョギング", "鼻呼吸ギリ", "20-40分", "週3-4回", "#38bdf8"),
        ("自転車", "平地ゆるく", "20-40分", "週2-3回", "#38bdf8"),
        ("筋トレ", "スクワット等", "15-20分", "週2回", "#FF6D00"),
    ]
    rows_html = ""
    for name, intensity, dur, freq, color in rows:
        rows_html += (
            "<tr>"
            "<td style='padding:14px 20px;font-size:18px;font-weight:700;color:" + color + ";"
            "border-bottom:1px solid #1e3a5f;'>" + name + "</td>"
            "<td style='padding:14px 20px;font-size:16px;color:#e2e8f0;border-bottom:1px solid #1e3a5f;'>" + intensity + "</td>"
            "<td style='padding:14px 20px;font-size:16px;color:#e2e8f0;border-bottom:1px solid #1e3a5f;'>" + dur + "</td>"
            "<td style='padding:14px 20px;font-size:16px;color:#e2e8f0;border-bottom:1px solid #1e3a5f;'>" + freq + "</td>"
            "</tr>"
        )
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "table{width:calc(100% - 112px);position:absolute;top:170px;left:56px;border-collapse:collapse;}"
        "th{padding:12px 20px;font-size:14px;font-weight:700;color:#FF6D00;text-align:left;"
        "border-bottom:2px solid #FF6D00;letter-spacing:1px;background:#0d2035;}"
        "</style></head><body>"
        "<div class='num'>6/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>ゾーン2 実践メニュー</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>「話せるペース」で続ける。追い込みは逆効果。</div>"
        "</div>"
        "<table><tr><th>種目</th><th>強度</th><th>時間</th><th>頻度</th></tr>"
        + rows_html + "</table>"
        "<div style='position:absolute;bottom:80px;left:56px;right:56px;"
        "background:linear-gradient(90deg,rgba(74,222,128,.1),rgba(74,222,128,.05));"
        "border:1px solid #4ade80;border-radius:12px;padding:16px 24px;text-align:center;'>"
        "<span style='font-size:20px;font-weight:800;color:#4ade80;'>初心者は「早歩き10分×週3回」から</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p>"
        "</body></html>")


def card_07():
    """実践: 縦フロー型"""
    steps = [
        ("1", "if-thenを1つ決める", "「もし昼休みになったら\n→10分速歩き」", "#FF6D00"),
        ("2", "環境を準備する", "運動ウェアを前日の夜に\n玄関に置く", "#FF6D00"),
        ("3", "10分だけやる", "完璧じゃなくていい\n動いた事実が全て", "#4ade80"),
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
            "<div style='font-size:16px;color:#9ca3af;margin-top:6px;white-space:pre-line;'>" + sub + "</div>"
            "</div></div>"
        )
        if i < 2:
            steps_html += (
                "<div style='position:absolute;top:" + str(top + 100) + "px;left:83px;"
                "width:2px;height:60px;background:#1e3a5f;'></div>"
            )
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        "<div class='num'>7/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>意志力ゼロで続ける3ステップ</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>if-then設計×環境設計で「気合い」を外す</div>"
        "</div>"
        + steps_html +
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#FF6D00;'>" + HASHTAG + "</p>"
        "</body></html>")


def card_08():
    """復帰: リカバリーフロー"""
    steps = [
        ("崩れた日", "「今日はできなかった...」", "#ef4444"),
        ("翌朝5分だけ歩く", "ゼロをイチにするだけでOK", "#FF6D00"),
        ("ループに戻る", "8勝6敗で十分", "#4ade80"),
    ]
    steps_html = ""
    for i, (title, sub, color) in enumerate(steps):
        left = 56 + i * 400
        steps_html += (
            "<div style='position:absolute;top:240px;left:" + str(left) + "px;width:360px;'>"
            "<div style='background:#1e3a5f;border-radius:16px;padding:28px;border-top:4px solid " + color + ";"
            "text-align:center;height:200px;display:flex;flex-direction:column;justify-content:center;'>"
            "<div style='font-size:26px;font-weight:800;color:" + color + ";'>" + title + "</div>"
            "<div style='font-size:18px;color:#e2e8f0;margin-top:12px;'>" + sub + "</div>"
            "</div></div>"
        )
        if i < 2:
            steps_html += (
                "<div style='position:absolute;top:325px;left:" + str(left + 370) + "px;"
                "font-size:28px;font-weight:900;color:#9ca3af;'>→</div>"
            )
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        "<div class='num'>8/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#4ade80;'>崩れても大丈夫。戻り方はこれ。</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>3日休んでも、再開すればミトコンドリアは応えてくれる。</div>"
        "</div>"
        + steps_html +
        "<div style='position:absolute;bottom:60px;left:56px;right:56px;"
        "background:linear-gradient(90deg,rgba(74,222,128,.1),rgba(74,222,128,.05));"
        "border:1px solid #4ade80;border-radius:12px;padding:18px 24px;text-align:center;'>"
        "<span style='font-size:22px;font-weight:800;color:#4ade80;'>if-then復帰：「もし昨日やらなかったら → 翌朝5分だけ歩く」</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#4ade80;'>" + HASHTAG + "</p>"
        "</body></html>")


def card_09():
    """深掘り: CSSグラフ＋説明カード"""
    bars = [
        ("運動なし", "15", "15%", "#ef4444"),
        ("週1回", "35", "35%", "#FF6D00"),
        ("週2-3回", "55", "55%", "#38bdf8"),
        ("週4回+", "69", "69%", "#4ade80"),
    ]
    bars_html = ""
    for i, (label, width_pct, display, color) in enumerate(bars):
        top = 200 + i * 100
        bars_html += (
            "<div style='position:absolute;top:" + str(top) + "px;left:56px;right:56px;'>"
            "<div style='font-size:16px;font-weight:700;color:#9ca3af;margin-bottom:8px;'>" + label + "</div>"
            "<div style='background:#0d2035;border-radius:8px;height:44px;position:relative;overflow:hidden;'>"
            "<div style='background:linear-gradient(90deg," + color + "," + color + "80);height:100%;"
            "width:" + width_pct + "%;border-radius:8px;'></div>"
            "<div style='position:absolute;right:12px;top:10px;font-size:18px;font-weight:800;color:#fff;'>"
            + display + "</div></div></div>"
        )
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        "<div class='num'>9/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#38bdf8;'>運動頻度とミトコンドリア改善率</div>"
        "<div style='font-size:16px;color:#9ca3af;margin-top:6px;'>週2-3回で十分な効果。「毎日」じゃなくていい。</div>"
        "</div>"
        + bars_html +
        "<div style='position:absolute;bottom:60px;left:56px;right:56px;"
        "background:#162d4a;border-radius:12px;padding:14px 24px;display:flex;justify-content:space-between;'>"
        "<span style='font-size:14px;color:#9ca3af;'>Robinson et al. 2017, Cell Metabolism</span>"
        "<span style='font-size:14px;color:#4ade80;font-weight:700;'>今から始める人が最も得をする</span>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#38bdf8;'>" + HASHTAG + "</p>"
        "</body></html>")


def card_10():
    """CTA: チェックリスト＋CTAボックス"""
    checks = [
        ("ミトコンドリアは30代から劣化する", True),
        ("「ゆるい運動」が最強の若返り法", True),
        ("ゾーン2 = 話せるペースで歩くだけ", True),
        ("12週間で機能69%改善のデータ", True),
        ("if-then設計で仕組みにする", True),
        ("8勝6敗でOK。崩れても戻れる", True),
    ]
    checks_html = ""
    for i, (text, checked) in enumerate(checks):
        top = 160 + i * 56
        mark = "&#x2705;" if checked else "&#x2B1C;"
        checks_html += (
            "<div style='position:absolute;top:" + str(top) + "px;left:56px;right:400px;"
            "display:flex;align-items:center;gap:12px;'>"
            "<div style='font-size:24px;'>" + mark + "</div>"
            "<div style='font-size:20px;color:#e2e8f0;font-weight:600;'>" + text + "</div>"
            "</div>"
        )
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS + "</style></head><body>"
        "<div class='num'>10/10</div>"
        "<div style='position:absolute;top:44px;left:56px;'>"
        "<div style='font-size:32px;font-weight:900;color:#FF6D00;'>今夜やること、1つだけ。</div>"
        "</div>"
        + checks_html +
        # CTAボックス
        "<div style='position:absolute;top:160px;right:56px;width:320px;height:380px;"
        "background:linear-gradient(180deg,#FF6D00,#e65100);border-radius:16px;padding:28px;"
        "display:flex;flex-direction:column;justify-content:center;text-align:center;'>"
        "<div style='font-size:20px;font-weight:700;color:rgba(255,255,255,.8);'>今夜の1アクション</div>"
        "<div style='font-size:28px;font-weight:900;color:#fff;margin-top:16px;line-height:1.4;'>"
        "明日の朝<br>10分だけ<br>速歩きする</div>"
        "<div style='width:60px;height:3px;background:rgba(255,255,255,.4);margin:20px auto;border-radius:2px;'></div>"
        "<div style='font-size:16px;color:rgba(255,255,255,.7);'>できたらボーナス<br>できなくても翌日やればいい</div>"
        "<div style='margin-top:20px;background:rgba(255,255,255,.15);border-radius:10px;padding:12px;'>"
        "<div style='font-size:14px;color:#fff;font-weight:700;'>noteで全文公開中</div>"
        "</div>"
        "</div>"
        "<div style='position:absolute;bottom:60px;left:56px;'>"
        "<div style='font-size:16px;color:#9ca3af;'>ミトコンドリアは、あなたが動き出すのを待っている。</div>"
        "</div>"
        "<p class='author'>マーシー｜100kg→68kg｜Sub3</p>"
        "<p class='series' style='color:#FF6D00;'>" + HASHTAG + "</p>"
        "</body></html>")


CARD_FUNCS = [card_01, card_02, card_03, card_04, card_05,
              card_06, card_07, card_08, card_09, card_10]


def render(html, fname):
    tmp = ARTICLE_DIR / "_tmp_xcard.html"
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


def save_tweets():
    out = OUTPUT_DIR / "x_posts.md"
    lines = ["# 第 X投稿スレッド（10本）\n\n"]
    for i, tweet in enumerate(TWEETS):
        tag = CARD_TAGS[i]
        lines.append(
            "## 投稿" + str(i+1) + "/10｜" + tag + "\n\n```\n" + tweet.strip() + "\n```\n\n"
            "![カード" + str(i+1) + "](x_post_" + str(i+1).zfill(2) + ".png)\n\n---\n\n"
        )
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

