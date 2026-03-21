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
HASHTAG = "#第 体重計習慣"
FIXED_TAGS = "\n\n#ダイエット #メタボ #習慣化 #体重管理 #健康診断"

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
    "風呂上がり、体重計を横目で素通りした。\n\n「乗ったら増えてるかも」\n「見ないほうが、心はラク」\n\n100kgだった頃、3ヶ月間乗れなかった。\n3ヶ月後に恐る恐る乗ったら、5kg増えてた。\n\n見なかった代償は、見た時より大きかった。\n\n\u2193続き（2/10）" + FIXED_TAGS,
    "体重計が怖いのは、弱さじゃない。\n\nハードルが高すぎるだけ。\n\n「測って\u2192記録して\u2192分析して\u2192食事見直し」\nこの5ステップを全部セットで考えてる。\n\nそりゃ怖い。\n1つ目の「測る」にすら辿り着けない。\n\n\u2193続き（3/10）" + FIXED_TAGS,
    "結論。体重計に乗り続けるには2つだけ。\n\n\u2460 if-thenプランニング\n「トイレの後に、乗る」と決めるだけ\n\n\u2461 ハードルを極限まで下げる\n「乗るだけ。記録もいらない」\n\nこの2つで、測ることが\u201c努力\u201dじゃなくなる。\n\n\u2193続き（4/10）" + FIXED_TAGS,
    "if-thenプランニングの研究結果。\n\n「もしXしたら、Yする」と決めるだけで\n目標達成率が2\u301c3倍に。\n\n94研究のメタ分析で効果量d=0.65\n（Gollwitzer & Sheeran 2006）\n\n「明日から測ろう」は目標。\n「トイレの後に測る」は計画。\n\n\u2193続き（5/10）" + FIXED_TAGS,
    "毎日測るだけで痩せやすくなる。\n\n\u274c 測定しない群\n\u2192 変化なし\n\n\u2705 毎日計測群（6ヶ月）\n\u2192 -6.1kg\n\n\u2705 週1回群（同期間）\n\u2192 -3.7kg\n\n差は2.4kg。やったことは「測っただけ」。\n（Steinberg 2015）\n\n\u2193続き（6/10）" + FIXED_TAGS,
    "ハードルを極限まで下げるレベル設計。\n\nLv.1 乗るだけ（3秒）\u2190 ここから\nLv.2 数字を見る（5秒）\nLv.3 メモする（15秒）\nLv.4 一言書く（30秒）\n\n最初の7日間はLv.1でOK。\n「乗った」という事実だけを積む。\n\n\u2193続き（7/10）" + FIXED_TAGS,
    "明日からやること、3ステップ。\n\n\u2460 if-thenを1つ決める\n「トイレの後に、乗る」\n\n\u2461 7日間レベル1\n乗るだけ。記録しない。\n\n\u2462 8日目にレベルを1つ上げる\n無理ならLv.1を続けてOK。\n\n紙に書いて体重計の横に貼る。\n\n\u2193続き（8/10）" + FIXED_TAGS,
    "増えてた日、普通にある。\n\nリカバリーもif-thenで設計する。\n\n「増えていたら\u21923秒待って\u2192観測完了と言う」\n\n\u2460 3秒待つ（反射的に責めない）\n\u2461 「観測完了」と声に出す\n\u2462 翌朝もう1回乗る\n\n8勝6敗でOK。戻れたら勝ち。\n\n\u2193続き（9/10）" + FIXED_TAGS,
    "100kgで3ヶ月乗れなかった僕が変われた理由。\n\n最初の2週間、乗るだけだった。\n記録もしない。数字も見ない。\n\n2週間後、自然と数字を見るようになった。\n3週間後、メモを始めた。\n\nハードルを下げるのは手抜きじゃない。\n「入口を広くする」こと。\n\n\u2193続き（10/10）" + FIXED_TAGS,
    "【まとめ\uff5c体重計に乗り続ける仕組み】\n\n\u2705 if-then\uff1a「トイレの後に、乗る」\n\u2705 Lv.1\uff1a乗るだけ。記録すらいらない\n\u2705 崩れた日\uff1a「観測完了」で戻る\n\n体重計の横に紙を1枚貼ってください。\n\n詳しくはnoteに書きました\nhttps://note.com/mash_anti_metabo" + FIXED_TAGS,
]

CARD_TAGS = ["共感", "原因", "解決策", "仕組み", "効果",
             "設計", "実践", "復帰", "深掘り", "今夜やること"]

ACCENT_COLORS = ["#38bdf8", "#38bdf8", "#FF6D00", "#38bdf8", "#4ade80",
                 "#38bdf8", "#FF6D00", "#4ade80", "#38bdf8", "#FF6D00"]


def card_01():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".timeline{position:absolute;top:120px;left:56px;right:56px;}"
        ".tl-row{display:flex;align-items:center;gap:16px;margin-bottom:14px;}"
        ".tl-time{font-size:16px;font-weight:800;color:#38bdf8;min-width:80px;text-align:right;}"
        ".tl-bar{width:6px;height:48px;border-radius:3px;}"
        ".tl-text{font-size:18px;color:#d4d6db;font-weight:500;line-height:1.5;}"
        ".b1{background:#38bdf8;} .b2{background:#f59e0b;} .b3{background:#ef4444;} .b4{background:#9ca3af;}"
        "</style></head><body>"
        "<div class='num'>1/10</div>"
        "<div class='title'>体重計を横目で素通りした夜</div>"
        "<div class='timeline'>"
        "<div class='tl-row'><span class='tl-time'>月曜</span><div class='tl-bar b1'></div><span class='tl-text'>「今週こそ測ろう」と決意する</span></div>"
        "<div class='tl-row'><span class='tl-time'>火曜</span><div class='tl-bar b1'></div><span class='tl-text'>朝バタバタで忘れる</span></div>"
        "<div class='tl-row'><span class='tl-time'>水曜</span><div class='tl-bar b2'></div><span class='tl-text'>夜食べすぎた。「明日は怖い」</span></div>"
        "<div class='tl-row'><span class='tl-time'>木曜</span><div class='tl-bar b3'></div><span class='tl-text'>風呂上がり、体重計を素通り</span></div>"
        "<div class='tl-row'><span class='tl-time'>金曜</span><div class='tl-bar b3'></div><span class='tl-text'>「週末から測ればいいか」</span></div>"
        "<div class='tl-row'><span class='tl-time'>日曜夜</span><div class='tl-bar b4'></div><span class='tl-text'>「結局また測れなかった…」</span></div>"
        "<div class='tl-row'><span class='tl-time'>3ヶ月後</span><div class='tl-bar b3'></div><span class='tl-text'>恐る恐る乗ったら+5kg。</span></div>"
        "</div>"
        "<div class='author'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "<div class='series' style='color:#38bdf8;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_02():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".flow{position:absolute;top:120px;left:80px;}"
        ".fstep{display:flex;align-items:center;gap:16px;margin-bottom:8px;}"
        ".fbox{background:#1e3a5f;border:2px solid #38bdf8;border-radius:12px;padding:14px 20px;"
        "font-size:16px;font-weight:700;color:#38bdf8;min-width:200px;text-align:center;}"
        ".farrow{font-size:24px;color:#FF6D00;font-weight:900;margin:0 8px;}"
        ".fresult{background:#1e3a5f;border:2px solid #ef4444;border-radius:12px;padding:14px 20px;"
        "font-size:16px;font-weight:700;color:#ef4444;min-width:200px;text-align:center;}"
        ".msg{position:absolute;bottom:120px;left:80px;right:80px;background:rgba(255,109,0,0.1);"
        "border:2px solid #FF6D00;border-radius:14px;padding:20px 32px;text-align:center;"
        "font-size:22px;font-weight:800;color:#FF6D00;line-height:1.6;}"
        "</style></head><body>"
        "<div class='num'>2/10</div>"
        "<div class='title'>ハードルが高すぎる問題</div>"
        "<div class='flow'>"
        "<div class='fstep'><div class='fbox'>\u2460 測る</div><span class='farrow'>\u2192</span>"
        "<div class='fbox'>\u2461 記録する</div><span class='farrow'>\u2192</span>"
        "<div class='fbox'>\u2462 分析する</div><span class='farrow'>\u2192</span>"
        "<div class='fbox'>\u2463 食事見直す</div><span class='farrow'>\u2192</span>"
        "<div class='fbox'>\u2464 運動増やす</div></div>"
        "<div style='margin:24px 0 0 0;text-align:center;'>"
        "<div class='fresult' style='display:inline-block;'>\u274c 5ステップを全部考えるから「測る」にすら辿り着けない</div>"
        "</div>"
        "</div>"
        "<div class='msg'>問題は意志の弱さじゃない。<br>ハードルが高すぎること。</div>"
        "<div class='author'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "<div class='series' style='color:#38bdf8;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_03():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:28px;font-weight:900;color:#fff;}"
        ".cards{position:absolute;top:110px;left:56px;display:flex;gap:28px;}"
        ".card{width:360px;padding:28px 24px;border-radius:16px;}"
        ".c1{background:#0d2035;border:2px solid #38bdf8;}"
        ".c2{background:#0d2035;border:2px solid #FF6D00;}"
        ".c3{background:#0d2035;border:2px solid #4ade80;}"
        ".cnum{font-size:40px;font-weight:900;margin-bottom:8px;}"
        ".cn1{color:#38bdf8;} .cn2{color:#FF6D00;} .cn3{color:#4ade80;}"
        ".ctitle{font-size:20px;font-weight:800;color:#fff;margin-bottom:12px;}"
        ".cbody{font-size:15px;color:#9ca3af;line-height:1.7;}"
        ".cbody strong{color:#fff;}"
        ".arrow-r{font-size:32px;color:#FF6D00;font-weight:900;position:absolute;top:280px;}"
        ".ar1{left:428px;} .ar2{left:816px;}"
        "</style></head><body>"
        "<div class='num'>3/10</div>"
        "<div class='title'>体重計に乗り続ける2つの仕組み</div>"
        "<div class='cards'>"
        "<div class='card c1'>"
        "<div class='cnum cn1'>01</div>"
        "<div class='ctitle'>if-then\u30d7\u30e9\u30f3\u30cb\u30f3\u30b0</div>"
        "<div class='cbody'><strong>\u300c\u30c8\u30a4\u30ec\u306e\u5f8c\u306b\u3001\u4e57\u308b\u300d</strong><br>"
        "\u3044\u3064\u30fb\u4f55\u3092\u3059\u308b\u304b\u3092<br>\u4e8b\u524d\u306b\u6c7a\u3081\u308b\u3060\u3051</div>"
        "</div>"
        "<div class='card c2'>"
        "<div class='cnum cn2'>02</div>"
        "<div class='ctitle'>\u30cf\u30fc\u30c9\u30eb\u3092<br>\u6975\u9650\u307e\u3067\u4e0b\u3052\u308b</div>"
        "<div class='cbody'><strong>Lv.1\uff1a\u4e57\u308b\u3060\u3051\uff083\u79d2\uff09</strong><br>"
        "\u8a18\u9332\u3082\u30b3\u30e1\u30f3\u30c8\u3082\u4e0d\u8981</div>"
        "</div>"
        "<div class='card c3'>"
        "<div class='cnum cn3'>\u2192</div>"
        "<div class='ctitle'>\u81ea\u52d5\u3067<br>\u7d9a\u304f\u8a08\u6e2c\u7fd2\u6163</div>"
        "<div class='cbody'>\u6bce\u65e5\u8a08\u6e2c\u7fa4\u306f<br>6\u30f6\u6708\u3067<strong>-6.1kg</strong></div>"
        "</div>"
        "</div>"
        "<div class='arrow-r ar1'>\u00d7</div>"
        "<div class='arrow-r ar2'>\u2192</div>"
        "<div class='author'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "<div class='series' style='color:#FF6D00;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_04():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".content{position:absolute;top:110px;left:56px;right:56px;}"
        ".item{background:#1e3a5f;border-radius:14px;padding:22px 28px;margin-bottom:16px;"
        "display:flex;align-items:center;gap:20px;}"
        ".inum{font-size:36px;font-weight:900;color:#38bdf8;min-width:48px;text-align:center;}"
        ".itext{font-size:18px;color:#d4d6db;font-weight:600;line-height:1.6;}"
        ".itext strong{color:#fff;}"
        ".src{position:absolute;bottom:80px;left:56px;background:#0d2035;border:1px solid #38bdf8;"
        "border-radius:8px;padding:10px 20px;font-size:14px;color:#38bdf8;}"
        ".effect{position:absolute;bottom:80px;right:56px;background:rgba(74,222,128,0.1);"
        "border:1px solid #4ade80;border-radius:8px;padding:10px 20px;"
        "font-size:16px;font-weight:700;color:#4ade80;}"
        "</style></head><body>"
        "<div class='num'>4/10</div>"
        "<div class='title'>if-then\u30d7\u30e9\u30f3\u30cb\u30f3\u30b0\u306e\u79d1\u5b66</div>"
        "<div class='content'>"
        "<div class='item'><div class='inum'>1</div><div class='itext'>X\u304c\u8d77\u304d\u305f\u3089\u3001Y\u3092\u3059\u308b\u3002<br><strong>\u305f\u3063\u305f\u3053\u308c\u3060\u3051\u3092\u4e8b\u524d\u306b\u6c7a\u3081\u308b</strong></div></div>"
        "<div class='item'><div class='inum'>2</div><div class='itext'>X\u304c\u8d77\u304d\u305f\u77ac\u9593\u3001\u8133\u304c\u81ea\u52d5\u7684\u306bY\u3092\u601d\u3044\u51fa\u3059\u3002<br><strong>\u610f\u5fd7\u529b\u3092\u4f7f\u308f\u305a\u306b\u884c\u52d5\u304c\u8d77\u52d5</strong></div></div>"
        "<div class='item'><div class='inum'>3</div><div class='itext'>\u4f8b\uff1a<strong>\u300c\u30c8\u30a4\u30ec\u306e\u5f8c\u306b\u3001\u4f53\u91cd\u8a08\u306b\u4e57\u308b\u300d</strong><br>\u6bce\u671d\u8003\u3048\u305a\u306b\u4e57\u308c\u308b\u3088\u3046\u306b\u306a\u308b</div></div>"
        "</div>"
        "<div class='src'>Gollwitzer & Sheeran 2006\uff5c94\u7814\u7a76\u30e1\u30bf\u5206\u6790</div>"
        "<div class='effect'>\u52b9\u679c\u91cf d=0.65\uff5c\u5b9f\u884c\u7387 2\u301c3\u500d</div>"
        "<div class='author'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "<div class='series' style='color:#38bdf8;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_05():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".compare{position:absolute;top:110px;left:56px;display:flex;gap:32px;}"
        ".panel{width:560px;padding:28px 24px;border-radius:16px;}"
        ".ng{background:rgba(239,68,68,0.08);border:2px solid #ef4444;}"
        ".ok{background:rgba(74,222,128,0.08);border:2px solid #4ade80;}"
        ".phead{font-size:22px;font-weight:900;margin-bottom:20px;text-align:center;}"
        ".phn{color:#ef4444;} .pho{color:#4ade80;}"
        ".prow{font-size:17px;color:#d4d6db;margin-bottom:14px;line-height:1.6;font-weight:500;}"
        ".prow strong{color:#fff;}"
        ".big{font-size:48px;font-weight:900;text-align:center;margin-top:16px;}"
        ".bn{color:#ef4444;} .bo{color:#4ade80;}"
        "</style></head><body>"
        "<div class='num'>5/10</div>"
        "<div class='title'>\u6bce\u65e5\u6e2c\u308b\u3060\u3051\u3067\u75e9\u305b\u3084\u3059\u304f\u306a\u308b</div>"
        "<div class='compare'>"
        "<div class='panel ng'>"
        "<div class='phead phn'>\u2717 \u6e2c\u5b9a\u3057\u306a\u3044\u7fa4</div>"
        "<div class='prow'>\u2022 \u73fe\u72b6\u304c\u898b\u3048\u306a\u3044</div>"
        "<div class='prow'>\u2022 \u4e0d\u5b89\u3060\u3051\u304c\u5897\u5927</div>"
        "<div class='prow'>\u2022 \u5909\u5316\u306b\u6c17\u3065\u3051\u306a\u3044</div>"
        "<div class='big bn'>-3.7kg</div>"
        "<div style='text-align:center;font-size:14px;color:#666;'>\u9031\u00d71\u56de\u8a08\u6e2c\u7fa4</div>"
        "</div>"
        "<div class='panel ok'>"
        "<div class='phead pho'>\u2713 \u6bce\u65e5\u8a08\u6e2c\u7fa4</div>"
        "<div class='prow'>\u2022 \u89b3\u6e2c\u306e\u89e3\u50cf\u5ea6\u304c\u4e0a\u304c\u308b</div>"
        "<div class='prow'>\u2022 \u884c\u52d5\u3068\u7d50\u679c\u304c\u3064\u306a\u304c\u308b</div>"
        "<div class='prow'>\u2022 \u5c0f\u3055\u306a\u6210\u529f\u306b\u6c17\u3065\u3051\u308b</div>"
        "<div class='big bo'>-6.1kg</div>"
        "<div style='text-align:center;font-size:14px;color:#666;'>Steinberg 2015\uff5c6\u30f6\u6708</div>"
        "</div>"
        "</div>"
        "<div class='author'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "<div class='series' style='color:#4ade80;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_06():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        "table{position:absolute;top:110px;left:56px;border-collapse:separate;border-spacing:0;"
        "width:1168px;border-radius:14px;overflow:hidden;}"
        "th{background:#1e3a5f;color:#38bdf8;font-size:17px;font-weight:800;padding:16px 18px;"
        "text-align:center;border-bottom:2px solid #2a4a6f;}"
        "td{background:#0d2035;color:#d4d6db;font-size:16px;font-weight:500;padding:18px 18px;"
        "text-align:center;border-bottom:1px solid #1a3050;line-height:1.4;}"
        "tr:last-child td{border-bottom:none;}"
        ".lv{font-size:20px;font-weight:900;}"
        ".l1{color:#4ade80;} .l2{color:#38bdf8;} .l3{color:#FF6D00;} .l4{color:#f59e0b;}"
        ".rec{background:rgba(74,222,128,0.08) !important;}"
        ".badge{display:inline-block;background:#4ade80;color:#0d1b2a;font-size:12px;"
        "font-weight:900;padding:2px 8px;border-radius:5px;margin-left:6px;}"
        "</style></head><body>"
        "<div class='num'>6/10</div>"
        "<div class='title'>\u30cf\u30fc\u30c9\u30eb\u3092\u6975\u9650\u307e\u3067\u4e0b\u3052\u308b\u30ec\u30d9\u30eb\u8a2d\u8a08</div>"
        "<table>"
        "<tr><th>Lv</th><th>\u3084\u308b\u3053\u3068</th><th>\u6642\u9593</th><th>\u8a18\u9332</th><th>\u671f\u9593\u306e\u76ee\u5b89</th></tr>"
        "<tr class='rec'><td><span class='lv l1'>1</span><span class='badge'>\u63a8\u5968</span></td>"
        "<td>\u4e57\u308b\u3060\u3051\u3002\u4ee5\u4e0a\u3002</td><td>3\u79d2</td><td>\u4e0d\u8981</td><td>7\u301c14\u65e5</td></tr>"
        "<tr><td><span class='lv l2'>2</span></td><td>\u6570\u5b57\u3092\u898b\u308b</td><td>5\u79d2</td><td>\u4e0d\u8981</td><td>2\u301c3\u9031\u76ee</td></tr>"
        "<tr><td><span class='lv l3'>3</span></td><td>\u30e1\u30e2\u3059\u308b</td><td>15\u79d2</td><td>\u6570\u5b57\u306e\u307f</td><td>3\u301c4\u9031\u76ee</td></tr>"
        "<tr><td><span class='lv l4'>4</span></td><td>\u8a18\u9332\uff0b\u4e00\u8a00</td><td>30\u79d2</td><td>\u6570\u5b57\uff0b\u4e00\u8a00</td><td>1\u30f6\u6708\u76ee\u301c</td></tr>"
        "</table>"
        "<div class='author'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "<div class='series' style='color:#38bdf8;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_07():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".steps{position:absolute;top:110px;left:56px;display:flex;flex-direction:column;gap:12px;}"
        ".step{display:flex;align-items:center;gap:20px;width:1100px;}"
        ".snum{width:56px;height:56px;border-radius:50%;display:flex;align-items:center;"
        "justify-content:center;font-size:26px;font-weight:900;flex-shrink:0;}"
        ".sn1{background:#FF6D00;color:#fff;}"
        ".sn2{background:#38bdf8;color:#0d1b2a;}"
        ".sn3{background:#4ade80;color:#0d1b2a;}"
        ".sbox{flex:1;background:#1e3a5f;border-radius:14px;padding:20px 24px;"
        "border:1px solid #2a4a6f;}"
        ".stitle{font-size:20px;font-weight:800;color:#fff;margin-bottom:6px;}"
        ".sdesc{font-size:15px;color:#9ca3af;line-height:1.6;}"
        ".conn{width:2px;height:16px;background:#FF6D00;margin-left:27px;}"
        "</style></head><body>"
        "<div class='num'>7/10</div>"
        "<div class='title'>\u660e\u65e5\u304b\u3089\u306e\u8a2d\u8a08\uff1a3\u30b9\u30c6\u30c3\u30d7</div>"
        "<div class='steps'>"
        "<div class='step'><div class='snum sn1'>1</div>"
        "<div class='sbox'><div class='stitle'>if-then\u30921\u3064\u6c7a\u3081\u308b</div>"
        "<div class='sdesc'>\u300c\u30c8\u30a4\u30ec\u306e\u5f8c\u306b\u3001\u4e57\u308b\u300d\u3002\u7d19\u306b\u66f8\u3044\u3066\u4f53\u91cd\u8a08\u306e\u6a2a\u306b\u8cbc\u308b\u3002</div></div></div>"
        "<div class='conn'></div>"
        "<div class='step'><div class='snum sn2'>2</div>"
        "<div class='sbox'><div class='stitle'>\u6700\u521d\u306e7\u65e5\u9593\u306fLv.1</div>"
        "<div class='sdesc'>\u4e57\u308b\u3060\u3051\u3002\u6570\u5b57\u3092\u898b\u306a\u304f\u3066\u3082\u3044\u3044\u3002\u8a18\u9332\u3057\u306a\u304f\u3066\u3044\u3044\u3002</div></div></div>"
        "<div class='conn'></div>"
        "<div class='step'><div class='snum sn3'>3</div>"
        "<div class='sbox'><div class='stitle'>8\u65e5\u76ee\u4ee5\u964d\u3001\u30ec\u30d9\u30eb\u30921\u3064\u4e0a\u3052\u308b</div>"
        "<div class='sdesc'>\u7121\u7406\u306a\u3089Lv.1\u7d9a\u884c\u3067OK\u3002\u81ea\u5206\u306e\u30da\u30fc\u30b9\u3067\u4e0a\u3052\u308c\u3070\u3044\u3044\u3002</div></div></div>"
        "</div>"
        "<div class='author'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "<div class='series' style='color:#FF6D00;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_08():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:28px;font-weight:900;color:#fff;}"
        ".trigger{position:absolute;top:100px;left:56px;right:56px;background:rgba(239,68,68,0.1);"
        "border:2px solid #ef4444;border-radius:14px;padding:14px 24px;text-align:center;"
        "font-size:18px;font-weight:700;color:#ef4444;}"
        ".flow{position:absolute;top:180px;left:56px;display:flex;flex-direction:column;"
        "align-items:center;gap:8px;width:1168px;}"
        ".arrow-d{font-size:24px;color:#FF6D00;font-weight:900;}"
        ".fstep{width:700px;padding:20px 28px;border-radius:14px;display:flex;align-items:center;gap:20px;}"
        ".f1{background:#1e3a5f;border:2px solid #f59e0b;}"
        ".f2{background:#1e3a5f;border:2px solid #FF6D00;}"
        ".f3{background:#1e3a5f;border:2px solid #4ade80;}"
        ".fnum{font-size:32px;font-weight:900;min-width:44px;text-align:center;}"
        ".fn1{color:#f59e0b;} .fn2{color:#FF6D00;} .fn3{color:#4ade80;}"
        ".ftitle{font-size:18px;font-weight:800;color:#fff;}"
        ".fdesc{font-size:14px;color:#9ca3af;}"
        ".result{margin-top:8px;background:rgba(74,222,128,0.1);border:2px solid #4ade80;"
        "border-radius:14px;padding:14px 28px;text-align:center;"
        "font-size:20px;font-weight:900;color:#4ade80;}"
        "</style></head><body>"
        "<div class='num'>8/10</div>"
        "<div class='title'>\u5d29\u308c\u305f\u65e5\u306e\u30ea\u30ab\u30d0\u30ea\u30fc if-then</div>"
        "<div class='trigger'>\u26a0 \u4f53\u91cd\u304c\u6628\u65e5\u3088\u308a+1kg\u5897\u3048\u3066\u3044\u305f</div>"
        "<div class='flow'>"
        "<div class='arrow-d'>\u2193</div>"
        "<div class='fstep f1'><div class='fnum fn1'>1</div>"
        "<div><div class='ftitle'>3\u79d2\u5f85\u3064</div><div class='fdesc'>\u53cd\u5c04\u7684\u306b\u8cac\u3081\u306a\u3044\u3002\u00b11-2kg\u306f\u6c34\u5206\u5909\u52d5\u3002</div></div></div>"
        "<div class='arrow-d'>\u2193</div>"
        "<div class='fstep f2'><div class='fnum fn2'>2</div>"
        "<div><div class='ftitle'>\u300c\u89b3\u6e2c\u5b8c\u4e86\u300d\u3068\u58f0\u306b\u51fa\u3059</div><div class='fdesc'>\u8a55\u4fa1\u30b3\u30e1\u30f3\u30c8\u3092\u5c01\u3058\u308b\u3002</div></div></div>"
        "<div class='arrow-d'>\u2193</div>"
        "<div class='fstep f3'><div class='fnum fn3'>3</div>"
        "<div><div class='ftitle'>\u7fcc\u671d\u3082\u30461\u56de\u4e57\u308b</div><div class='fdesc'>\u9023\u7d9a\u6027\u3092\u5207\u3089\u306a\u3044\u3002</div></div></div>"
        "<div class='result'>8\u52dd6\u6557\u3067\u6210\u529f\u3002\u5b8c\u74a7\u3092\u76ee\u6307\u3055\u306a\u3044\u3002</div>"
        "</div>"
        "<div class='author'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "<div class='series' style='color:#4ade80;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_09():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:28px;font-weight:900;color:#fff;}"
        ".content{position:absolute;top:110px;left:56px;right:56px;}"
        ".phase{display:flex;align-items:center;gap:20px;margin-bottom:18px;}"
        ".plabel{min-width:100px;font-size:15px;font-weight:700;color:#9ca3af;text-align:right;}"
        ".pbar-bg{flex:1;height:40px;background:#1a3050;border-radius:8px;position:relative;overflow:hidden;}"
        ".pbar{height:100%;border-radius:8px;display:flex;align-items:center;padding-left:16px;"
        "font-size:15px;font-weight:800;color:#0d1b2a;}"
        ".b1{background:#ef4444;width:15%;} .b2{background:#f59e0b;width:35%;}"
        ".b3{background:#38bdf8;width:60%;} .b4{background:#4ade80;width:85%;}"
        ".note{margin-top:8px;font-size:14px;color:#555;text-align:right;}"
        ".msg{position:absolute;bottom:100px;left:56px;right:56px;background:rgba(255,109,0,0.1);"
        "border:2px solid #FF6D00;border-radius:14px;padding:20px 32px;text-align:center;"
        "font-size:20px;font-weight:800;color:#FF6D00;line-height:1.6;}"
        "</style></head><body>"
        "<div class='num'>9/10</div>"
        "<div class='title'>\u50d5\u304c100kg\u304b\u3089\u5909\u308f\u308c\u305f\u8ecc\u8de1</div>"
        "<div class='content'>"
        "<div class='phase'><span class='plabel'>\u6700\u521d\u306e2\u9031\u9593</span>"
        "<div class='pbar-bg'><div class='pbar b1'>Lv.1 \u4e57\u308b\u3060\u3051</div></div></div>"
        "<div class='phase'><span class='plabel'>3\u9031\u76ee</span>"
        "<div class='pbar-bg'><div class='pbar b2'>Lv.2 \u6570\u5b57\u3092\u898b\u308b</div></div></div>"
        "<div class='phase'><span class='plabel'>4\u9031\u76ee</span>"
        "<div class='pbar-bg'><div class='pbar b3'>Lv.3 \u30e1\u30e2\u3059\u308b</div></div></div>"
        "<div class='phase'><span class='plabel'>1\u30f6\u6708\u76ee\u301c</span>"
        "<div class='pbar-bg'><div class='pbar b4'>Lv.4 \u8a18\u9332\uff0b\u300c\u89b3\u6e2c\u5b8c\u4e86\u300d</div></div></div>"
        "<div class='note'>\u203b \u5404\u30ec\u30d9\u30eb\u306e\u671f\u9593\u306f\u500b\u4eba\u5dee\u3042\u308a\u3002\u7121\u7406\u306b\u4e0a\u3052\u306a\u304f\u3066OK\u3002</div>"
        "</div>"
        "<div class='msg'>\u30cf\u30fc\u30c9\u30eb\u3092\u4e0b\u3052\u308b\u306e\u306f\u624b\u629c\u304d\u3058\u3083\u306a\u3044\u3002<br>\u300c\u5165\u53e3\u3092\u5e83\u304f\u3059\u308b\u300d\u3053\u3068\u3002</div>"
        "<div class='author'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "<div class='series' style='color:#38bdf8;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_10():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".checks{position:absolute;top:120px;left:56px;}"
        ".check{display:flex;align-items:center;gap:16px;margin-bottom:20px;}"
        ".cbox{width:36px;height:36px;border-radius:8px;background:#4ade80;display:flex;"
        "align-items:center;justify-content:center;font-size:20px;font-weight:900;color:#0d1b2a;}"
        ".ctext{font-size:20px;font-weight:700;color:#d4d6db;line-height:1.5;}"
        ".ctext strong{color:#fff;}"
        ".cta{position:absolute;bottom:100px;left:56px;right:56px;background:#FF6D00;"
        "border-radius:16px;padding:24px 40px;text-align:center;}"
        ".cta-main{font-size:22px;font-weight:900;color:#fff;margin-bottom:8px;}"
        ".cta-sub{font-size:16px;color:rgba(255,255,255,0.8);}"
        "</style></head><body>"
        "<div class='num'>10/10</div>"
        "<div class='title'>\u4eca\u591c\u3084\u308b\u3053\u3068\uff1a\u7d19\u30921\u679a\u8cbc\u308b\u3060\u3051</div>"
        "<div class='checks'>"
        "<div class='check'><div class='cbox'>\u2713</div><div class='ctext'>if-then\uff1a<strong>\u300c\u30c8\u30a4\u30ec\u306e\u5f8c\u306b\u3001\u4e57\u308b\u300d</strong></div></div>"
        "<div class='check'><div class='cbox'>\u2713</div><div class='ctext'>Lv.1\uff1a<strong>\u4e57\u308b\u3060\u3051\u3002\u8a18\u9332\u3059\u3089\u3044\u3089\u306a\u3044</strong></div></div>"
        "<div class='check'><div class='cbox'>\u2713</div><div class='ctext'>\u5d29\u308c\u305f\u65e5\uff1a<strong>\u300c\u89b3\u6e2c\u5b8c\u4e86\u300d\u3067\u623b\u308b</strong></div></div>"
        "<div class='check'><div class='cbox'>\u2713</div><div class='ctext'>7\u65e5\u9593\u3001\u4e57\u308b\u3060\u3051\u3067<strong>100\u70b9</strong></div></div>"
        "</div>"
        "<div class='cta'>"
        "<div class='cta-main'>\u8a73\u3057\u304f\u306fnote\u306b\u66f8\u304d\u307e\u3057\u305f</div>"
        "<div class='cta-sub'>https://note.com/mash_anti_metabo</div>"
        "</div>"
        "<div class='author'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "<div class='series' style='color:#FF6D00;'>" + HASHTAG + "</div>"
        "</body></html>")


CARD_FUNCS = [card_01, card_02, card_03, card_04, card_05,
              card_06, card_07, card_08, card_09, card_10]


def render_card(html, fname):
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
        render_card(html, fname)
        print("✅ " + fname + "  [" + CARD_TAGS[i] + "]")
    save_tweets()
    print("\n全10枚完了。保存先: " + str(OUTPUT_DIR))

