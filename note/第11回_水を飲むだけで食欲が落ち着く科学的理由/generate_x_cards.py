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
HASHTAG = "#第 食前水ルール"
FIXED_TAGS = "\n\n#ダイエット #メタボ #習慣化 #食事管理 #水分補給"

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
    "18時、デスクに空のペットボトルが1本。\n「今日も全然飲んでなかった…」\n\nでも喉の渇きより先に、腹が減ってる。\nコンビニ弁当を5分で食べ切って、食後の罪悪感。\n\n100kgだった頃、毎日これを繰り返してた。\n原因は「水」だった。\n\n↓続き（2/10）",
    "夕食の食べ過ぎ、意志の弱さじゃなかった。\n\n①日中、水をほぼ飲まない\n②夕方、脱水を空腹と誤認\n③帰宅→即食事→勢い食い\n④罪悪感→翌日も同じ\n\n体が「食べろ」と誤信号を出してただけ。\n水不足が全ての始まりだった。\n\n↓続き（3/10）",
    "結論：食前に水300mlを飲むだけ。\n\nこれだけで食欲の暴走は抑えやすくなる。\n\n食事を変える前に、食事の「前」を変える。\n大きな努力の前に、小さな前処理。\n\n3ステップで仕組み化できます。\n\n↓続き（4/10）",
    "食前の水が効く科学的理由。\n\n①満腹シグナルが早まる\n→ 1食-75kcal（Davy 2008, JADA）\n\n②勢い食いにブレーキ\n→ 30秒のワンクッション\n\n③ニセの空腹を判定\n→ 水を飲んで5分待つだけ\n\n↓続き（5/10）",
    "食前水の効果、数字で見ると。\n\n❌ 水なし：脱水→誤認→5分で完食→罪悪感\n✅ 水あり：300ml→ゆっくり開始→適量で満足\n\n12週間で約2kg多く減量（Dennis 2010, Obesity誌）\n月に換算すると脂肪-300g。\n\n↓続き（6/10）",
    "食前水ルール、実践早見表。\n\nSTEP1：夕食前だけに固定\nSTEP2：食前15分に水300ml\nSTEP3：最初の3分ゆっくり食べる\n\n水分目安：体重×30ml/日\n（68kg→約2L、100kg→約3L）\n\n↓続き（7/10）",
    "今日からやること。\n\n①帰宅したら冷蔵庫の前で水300ml\n②30〜60秒かけてゆっくり飲む\n③最初の3分は味噌汁・サラダから\n\n300mlが多ければ200mlでOK。\n大事なのは量より「毎回やる」こと。\n\n↓続き（8/10）",
    "忘れた日、普通にある。\n\n外食で流れた。会食で飛んだ。\n疲れてそれどころじゃなかった。\n\n大丈夫。\n次の食事でまた水を飲む。\nそれでリセット完了。\n\n8勝6敗でOK。復帰力がすべて。\n\n↓続き（9/10）",
    "100kgだった頃の水分量を測ったら750ml。\n推奨量の半分以下だった。\n\n食前に水を入れ始めてから変わったこと：\n・勢い食いが消えた\n・食後の罪悪感が減った\n・おかわりが自然に不要になった\n\n↓続き（10/10）",
    "【まとめ｜食前水ルール3ステップ】\n\n✅ 食前300mlで満腹シグナル早める\n✅ 夕食前だけに固定する\n✅ 崩れたら翌日また飲むだけ\n\n7日間、1食だけ試してみてください。\n\n詳しくはnoteに書きました👇\nhttps://note.com/mash_anti_metabo",
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
        ".tl-time{font-size:16px;font-weight:800;color:#38bdf8;min-width:56px;text-align:right;}"
        ".tl-bar{width:6px;height:48px;border-radius:3px;}"
        ".tl-text{font-size:18px;color:#d4d6db;font-weight:500;line-height:1.5;}"
        ".b1{background:#38bdf8;} .b2{background:#f59e0b;} .b3{background:#ef4444;} .b4{background:#ef4444;} .b5{background:#9ca3af;}"
        "</style></head><body>"
        "<div class='num'>1/10</div>"
        "<div class='title'>18時、空のペットボトルが1本だけ。</div>"
        "<div class='timeline'>"
        "<div class='tl-row'><span class='tl-time'>9:00</span><div class='tl-bar b1'></div><span class='tl-text'>出社。コーヒー1杯。水はゼロ。</span></div>"
        "<div class='tl-row'><span class='tl-time'>12:00</span><div class='tl-bar b1'></div><span class='tl-text'>昼食。ペットボトル半分だけ。</span></div>"
        "<div class='tl-row'><span class='tl-time'>15:00</span><div class='tl-bar b2'></div><span class='tl-text'>口が乾く。でも会議で飲めない。</span></div>"
        "<div class='tl-row'><span class='tl-time'>18:00</span><div class='tl-bar b3'></div><span class='tl-text'>脱水→空腹と誤認。限界。</span></div>"
        "<div class='tl-row'><span class='tl-time'>18:30</span><div class='tl-bar b3'></div><span class='tl-text'>コンビニ弁当を5分で完食。</span></div>"
        "<div class='tl-row'><span class='tl-time'>19:00</span><div class='tl-bar b4'></div><span class='tl-text'>「やってしまった…」罪悪感。</span></div>"
        "<div class='tl-row'><span class='tl-time'>翌日</span><div class='tl-bar b5'></div><span class='tl-text'>「今日こそ抑えよう」→ また同じ。</span></div>"
        "</div>"
        "<div class='author'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div class='series' style='color:#38bdf8;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_02():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".flow{position:absolute;top:120px;left:80px;}"
        ".fstep{display:flex;align-items:center;gap:16px;margin-bottom:8px;}"
        ".fbox{background:#1e3a5f;border:2px solid #38bdf8;border-radius:12px;padding:14px 20px;"
        "font-size:17px;font-weight:700;color:#d4d6db;min-width:340px;}"
        ".farrow{font-size:24px;color:#ef4444;font-weight:900;margin-left:180px;margin-bottom:4px;}"
        ".floop{position:absolute;right:120px;top:180px;width:200px;height:300px;"
        "border:3px dashed #ef4444;border-left:none;border-radius:0 60px 60px 0;}"
        ".floop-text{position:absolute;right:80px;top:310px;font-size:16px;font-weight:800;color:#ef4444;}"
        "</style></head><body>"
        "<div class='num'>2/10</div>"
        "<div class='title'>食べ過ぎの原因 ── 意志じゃなく水不足</div>"
        "<div class='flow'>"
        "<div class='fstep'><div class='fbox'>① 日中、水をほとんど飲まない</div></div>"
        "<div class='farrow'>↓</div>"
        "<div class='fstep'><div class='fbox'>② 夕方、脱水を「空腹」と誤認</div></div>"
        "<div class='farrow'>↓</div>"
        "<div class='fstep'><div class='fbox'>③ 帰宅 → 即食事 → 勢い食い</div></div>"
        "<div class='farrow'>↓</div>"
        "<div class='fstep'><div class='fbox'>④ 食後の罪悪感「やってしまった…」</div></div>"
        "<div class='farrow'>↓</div>"
        "<div class='fstep'><div class='fbox'>⑤ 翌日「今日こそ」→ また同じ</div></div>"
        "</div>"
        "<div class='floop'></div>"
        "<div class='floop-text'>毎日ループ</div>"
        "<div class='author'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div class='series' style='color:#38bdf8;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_03():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".cards{position:absolute;top:130px;left:56px;right:56px;display:flex;gap:20px;}"
        ".card{flex:1;border-radius:14px;padding:28px 20px;text-align:center;}"
        ".c1{background:#1e3a5f;border-top:4px solid #38bdf8;}"
        ".c2{background:#1e3a5f;border-top:4px solid #FF6D00;}"
        ".c3{background:#1e3a5f;border-top:4px solid #4ade80;}"
        ".cnum{font-size:42px;font-weight:900;margin-bottom:12px;}"
        ".c1 .cnum{color:#38bdf8;} .c2 .cnum{color:#FF6D00;} .c3 .cnum{color:#4ade80;}"
        ".ctitle{font-size:20px;font-weight:800;color:#fff;margin-bottom:12px;line-height:1.4;}"
        ".cdesc{font-size:14px;color:#9ca3af;line-height:1.6;}"
        ".arrow-r{font-size:32px;color:#FF6D00;font-weight:900;position:absolute;top:260px;}"
        ".ar1{left:410px;} .ar2{left:830px;}"
        "</style></head><body>"
        "<div class='num'>3/10</div>"
        "<div class='title'>食前水ルール ── 3ステップで仕組み化</div>"
        "<div class='cards'>"
        "<div class='card c1'><div class='cnum'>①</div>"
        "<div class='ctitle'>夕食前だけ<br>固定する</div>"
        "<div class='cdesc'>いきなり毎食は不要。<br>1食だけでOK</div></div>"
        "<div class='card c2'><div class='cnum'>②</div>"
        "<div class='ctitle'>食前15分に<br>水300ml</div>"
        "<div class='cdesc'>コップ1.5杯。<br>ゆっくり30〜60秒</div></div>"
        "<div class='card c3'><div class='cnum'>③</div>"
        "<div class='ctitle'>最初の3分<br>ゆっくり食べる</div>"
        "<div class='cdesc'>味噌汁・サラダから。<br>白飯は後回し</div></div>"
        "</div>"
        "<div class='arrow-r ar1'>→</div>"
        "<div class='arrow-r ar2'>→</div>"
        "<div class='author'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div class='series' style='color:#FF6D00;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_04():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".items{position:absolute;top:120px;left:56px;right:56px;}"
        ".item{display:flex;align-items:flex-start;gap:20px;margin-bottom:20px;"
        "background:#1e3a5f;border-radius:14px;padding:22px 24px;}"
        ".ibadge{font-size:32px;font-weight:900;color:#38bdf8;min-width:44px;}"
        ".ititle{font-size:19px;font-weight:800;color:#fff;margin-bottom:6px;}"
        ".idesc{font-size:14px;color:#9ca3af;line-height:1.6;}"
        ".source{position:absolute;bottom:70px;left:56px;background:#38bdf822;border:1px solid #38bdf8;"
        "border-radius:8px;padding:10px 20px;font-size:14px;color:#38bdf8;font-weight:700;}"
        "</style></head><body>"
        "<div class='num'>4/10</div>"
        "<div class='title'>なぜ食前の水で食欲が変わるのか</div>"
        "<div class='items'>"
        "<div class='item'><span class='ibadge'>01</span><div>"
        "<div class='ititle'>満腹シグナルが早まる</div>"
        "<div class='idesc'>胃が先に満たされ「もう十分」のサインが早く立つ → 1食-75kcal</div></div></div>"
        "<div class='item'><span class='ibadge'>02</span><div>"
        "<div class='ititle'>勢い食いにブレーキ</div>"
        "<div class='idesc'>食事前の30秒のワンクッションで「帰宅→即・冷蔵庫」パターンを止める</div></div></div>"
        "<div class='item'><span class='ibadge'>03</span><div>"
        "<div class='ititle'>ニセの空腹を判定できる</div>"
        "<div class='idesc'>水を飲んで5分待つ。まだ空腹なら本物。和らいだなら脱水だった</div></div></div>"
        "</div>"
        "<div class='source'>📄 Davy et al., 2008 JADA ／ Dennis et al., 2010 Obesity</div>"
        "<div class='author'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div class='series' style='color:#38bdf8;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_05():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".panels{position:absolute;top:120px;left:56px;right:56px;display:flex;gap:28px;}"
        ".panel{flex:1;border-radius:14px;padding:28px 24px;}"
        ".ng{background:#1a0a0a;border:2px solid #ef4444;}"
        ".ok{background:#0a1a0a;border:2px solid #4ade80;}"
        ".ph{font-size:24px;font-weight:900;margin-bottom:20px;display:flex;align-items:center;gap:10px;}"
        ".ng .ph{color:#ef4444;} .ok .ph{color:#4ade80;}"
        ".prow{font-size:16px;color:#d4d6db;margin-bottom:12px;line-height:1.5;padding-left:8px;"
        "border-left:3px solid;}"
        ".ng .prow{border-color:#ef4444;} .ok .prow{border-color:#4ade80;}"
        ".presult{margin-top:20px;padding:14px;border-radius:10px;font-size:17px;font-weight:800;text-align:center;}"
        ".ng .presult{background:#ef444422;color:#ef4444;}"
        ".ok .presult{background:#4ade8022;color:#4ade80;}"
        ".vs{position:absolute;top:300px;left:50%;transform:translateX(-50%);"
        "font-size:28px;font-weight:900;color:#FF6D00;background:#0d1b2a;padding:8px 14px;"
        "border:2px solid #FF6D00;border-radius:50%;}"
        "</style></head><body>"
        "<div class='num'>5/10</div>"
        "<div class='title'>食前水なし vs あり ── 数字で比較</div>"
        "<div class='panels'>"
        "<div class='panel ng'>"
        "<div class='ph'>✗ 水なし</div>"
        "<div class='prow'>水分：750ml/日（半分以下）</div>"
        "<div class='prow'>夕食：5分で完食</div>"
        "<div class='prow'>食後：罪悪感ループ</div>"
        "<div class='presult'>→ 食べ過ぎ + 自己嫌悪</div>"
        "</div>"
        "<div class='panel ok'>"
        "<div class='ph'>✓ 食前水あり</div>"
        "<div class='prow'>食前：300ml ゆっくり飲む</div>"
        "<div class='prow'>夕食：最初3分ゆっくり</div>"
        "<div class='prow'>食後：「ちょうどいい」</div>"
        "<div class='presult'>→ 12週で-2kg多く減量</div>"
        "</div>"
        "</div>"
        "<div class='vs'>VS</div>"
        "<div class='author'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div class='series' style='color:#4ade80;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_06():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".table{position:absolute;top:120px;left:56px;right:56px;border-collapse:separate;border-spacing:0 6px;}"
        ".table th{padding:12px 16px;font-size:14px;font-weight:800;color:#FF6D00;text-align:left;"
        "border-bottom:2px solid #FF6D00;}"
        ".table td{padding:14px 16px;font-size:15px;color:#d4d6db;background:#1e3a5f;line-height:1.4;}"
        ".table tr td:first-child{border-radius:8px 0 0 8px;font-weight:800;color:#38bdf8;width:140px;}"
        ".table tr td:last-child{border-radius:0 8px 8px 0;}"
        "</style></head><body>"
        "<div class='num'>6/10</div>"
        "<div class='title'>食前水ルール 実践早見表</div>"
        "<table class='table'>"
        "<tr><th>ステップ</th><th>やること</th><th>ポイント</th></tr>"
        "<tr><td>STEP 1</td><td>夕食前だけに固定</td><td>リラックスしてる食事を選ぶ</td></tr>"
        "<tr><td>STEP 2</td><td>食前15分に水300ml</td><td>常温〜やや冷。30〜60秒で</td></tr>"
        "<tr><td>STEP 3</td><td>最初3分ゆっくり</td><td>味噌汁・サラダから開始</td></tr>"
        "<tr><td>水分目安</td><td>体重×30ml/日</td><td>68kg→約2L。300mlで底上げ</td></tr>"
        "<tr><td>崩れた日</td><td>次の食事でまた飲む</td><td>8勝6敗でOK</td></tr>"
        "</table>"
        "<div class='author'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div class='series' style='color:#38bdf8;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_07():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".flow{position:absolute;top:120px;left:50%;transform:translateX(-50%);width:700px;}"
        ".fstep{display:flex;align-items:center;gap:20px;margin-bottom:10px;}"
        ".fnum{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;"
        "justify-content:center;font-size:24px;font-weight:900;}"
        ".fn1{background:#FF6D0033;color:#FF6D00;border:2px solid #FF6D00;}"
        ".fn2{background:#FF6D0033;color:#FF6D00;border:2px solid #FF6D00;}"
        ".fn3{background:#FF6D0033;color:#FF6D00;border:2px solid #FF6D00;}"
        ".fn4{background:#4ade8033;color:#4ade80;border:2px solid #4ade80;}"
        ".fcard{background:#1e3a5f;border-radius:12px;padding:16px 24px;flex:1;}"
        ".ftitle{font-size:18px;font-weight:800;color:#fff;}"
        ".fdesc{font-size:13px;color:#9ca3af;margin-top:4px;}"
        ".conn{width:3px;height:10px;background:#FF6D00;margin-left:25px;border-radius:2px;}"
        "</style></head><body>"
        "<div class='num'>7/10</div>"
        "<div class='title'>今日からやること ── 食前水プロトコル</div>"
        "<div class='flow'>"
        "<div class='fstep'><div class='fnum fn1'>1</div><div class='fcard'>"
        "<div class='ftitle'>帰宅したらまずコップ1杯</div>"
        "<div class='fdesc'>冷蔵庫の前で水300ml。これが「直行」を止める</div></div></div>"
        "<div class='conn'></div>"
        "<div class='fstep'><div class='fnum fn2'>2</div><div class='fcard'>"
        "<div class='ftitle'>30〜60秒かけてゆっくり飲む</div>"
        "<div class='fdesc'>一気飲みしない。常温〜やや冷たい水がベスト</div></div></div>"
        "<div class='conn'></div>"
        "<div class='fstep'><div class='fnum fn3'>3</div><div class='fcard'>"
        "<div class='ftitle'>最初の3分は味噌汁・サラダから</div>"
        "<div class='fdesc'>白飯は後回し。これで「おかわり」パターンが消える</div></div></div>"
        "<div class='conn'></div>"
        "<div class='fstep'><div class='fnum fn4'>4</div><div class='fcard'>"
        "<div class='ftitle'>300mlが多ければ200mlからOK</div>"
        "<div class='fdesc'>大事なのは量より「毎回やる」こと</div></div></div>"
        "</div>"
        "<div class='author'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div class='series' style='color:#FF6D00;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_08():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".flow{position:absolute;top:130px;left:50%;transform:translateX(-50%);width:640px;}"
        ".step{border-radius:14px;padding:22px 28px;margin-bottom:12px;"
        "display:flex;align-items:center;gap:18px;}"
        ".snum{font-size:32px;font-weight:900;min-width:48px;text-align:center;"
        "border-radius:50%;width:48px;height:48px;line-height:48px;}"
        ".s1{background:#1a0a0a;border:2px solid #ef4444;} .s1 .snum{background:#ef444433;color:#ef4444;}"
        ".s2{background:#1a1a0a;border:2px solid #f59e0b;} .s2 .snum{background:#f59e0b33;color:#f59e0b;}"
        ".s3{background:#0a1a0a;border:2px solid #4ade80;} .s3 .snum{background:#4ade8033;color:#4ade80;}"
        ".stxt{font-size:19px;font-weight:700;color:#fff;line-height:1.5;}"
        ".ssub{font-size:13px;color:#9ca3af;margin-top:4px;font-weight:400;}"
        ".conn{width:4px;height:12px;margin:0 auto;border-radius:2px;"
        "background:linear-gradient(180deg,#ef4444,#4ade80);}"
        ".motto{margin-top:20px;text-align:center;padding:18px;background:#4ade8018;"
        "border:2px solid #4ade80;border-radius:14px;}"
        ".motto-t{font-size:26px;font-weight:900;color:#4ade80;}"
        "</style></head><body>"
        "<div class='num'>8/10</div>"
        "<div class='title'>崩れた日のリカバリーフロー</div>"
        "<div class='flow'>"
        "<div class='step s1'><div class='snum'>1</div><div>"
        "<div class='stxt'>崩れた。忘れた。食べ過ぎた。</div>"
        "<div class='ssub'>外食・会食・疲れ… 普通にある</div></div></div>"
        "<div class='conn'></div>"
        "<div class='step s2'><div class='snum'>2</div><div>"
        "<div class='stxt'>自己嫌悪をスキップする。</div>"
        "<div class='ssub'>「もう無理」とゼロに戻らない</div></div></div>"
        "<div class='conn'></div>"
        "<div class='step s3'><div class='snum'>3</div><div>"
        "<div class='stxt'>次の食事で、また水を飲む。</div>"
        "<div class='ssub'>それだけでリセット完了</div></div></div>"
        "<div class='motto'><div class='motto-t'>8勝6敗でOK。復帰力がすべて。</div></div>"
        "</div>"
        "<div class='author'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div class='series' style='color:#4ade80;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_09():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".content{position:absolute;top:120px;left:56px;right:56px;}"
        ".bar-section{margin-bottom:28px;}"
        ".bar-label{font-size:16px;font-weight:700;color:#d4d6db;margin-bottom:8px;}"
        ".bar-wrap{display:flex;align-items:center;gap:12px;}"
        ".bar-bg{flex:1;height:36px;background:#1e3a5f;border-radius:8px;overflow:hidden;}"
        ".bar-fill{height:100%;border-radius:8px;display:flex;align-items:center;padding-left:12px;"
        "font-size:14px;font-weight:800;color:#fff;}"
        ".bf1{width:37%;background:#ef4444;} .bf2{width:100%;background:#38bdf8;}"
        ".bf3{width:75%;background:#38bdf8;} .bf4{width:100%;background:#4ade80;}"
        ".bar-val{font-size:16px;font-weight:800;min-width:80px;}"
        ".bv1{color:#ef4444;} .bv2{color:#38bdf8;} .bv3{color:#38bdf8;} .bv4{color:#4ade80;}"
        ".insight{position:absolute;bottom:80px;left:56px;right:56px;background:#1e3a5f;"
        "border-radius:12px;padding:18px 24px;}"
        ".insight-t{font-size:16px;font-weight:800;color:#FF6D00;margin-bottom:6px;}"
        ".insight-d{font-size:14px;color:#9ca3af;line-height:1.6;}"
        ".source{position:absolute;bottom:28px;left:56px;font-size:13px;color:#3a3a3a;}"
        "</style></head><body>"
        "<div class='num'>9/10</div>"
        "<div class='title'>100kg時代の水分量を測ったら…</div>"
        "<div class='content'>"
        "<div class='bar-section'>"
        "<div class='bar-label'>100kg時代の実際の水分量</div>"
        "<div class='bar-wrap'><div class='bar-bg'><div class='bar-fill bf1'>750ml</div></div>"
        "<span class='bar-val bv1'>750ml</span></div></div>"
        "<div class='bar-section'>"
        "<div class='bar-label'>100kgの推奨量（体重×30ml）</div>"
        "<div class='bar-wrap'><div class='bar-bg'><div class='bar-fill bf2'>3,000ml</div></div>"
        "<span class='bar-val bv2'>3,000ml</span></div></div>"
        "<div class='bar-section'>"
        "<div class='bar-label'>現在68kgの推奨量</div>"
        "<div class='bar-wrap'><div class='bar-bg'><div class='bar-fill bf3'>2,040ml</div></div>"
        "<span class='bar-val bv3'>2,040ml</span></div></div>"
        "<div class='bar-section'>"
        "<div class='bar-label'>食前水を足した場合（+300ml×2食）</div>"
        "<div class='bar-wrap'><div class='bar-bg'><div class='bar-fill bf4'>+600ml/日</div></div>"
        "<span class='bar-val bv4'>底上げ</span></div></div>"
        "</div>"
        "<div class='insight'>"
        "<div class='insight-t'>食前水を始めて変わったこと</div>"
        "<div class='insight-d'>勢い食いが消えた ／ 食後の罪悪感が減った ／ おかわりが自然に不要に</div>"
        "</div>"
        "<div class='source'>出典: Dennis 2010, Obesity ／ Davy 2008, JADA</div>"
        "<div class='author'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div class='series' style='color:#38bdf8;'>" + HASHTAG + "</div>"
        "</body></html>")


def card_10():
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" + BASE_CSS +
        ".title{position:absolute;left:56px;top:44px;font-size:30px;font-weight:900;color:#fff;}"
        ".checks{position:absolute;top:130px;left:56px;right:56px;}"
        ".check{display:flex;align-items:center;gap:16px;margin-bottom:18px;}"
        ".cbadge{width:40px;height:40px;border-radius:8px;display:flex;align-items:center;"
        "justify-content:center;font-size:20px;font-weight:900;}"
        ".cb1{background:#38bdf833;color:#38bdf8;}"
        ".cb2{background:#FF6D0033;color:#FF6D00;}"
        ".cb3{background:#4ade8033;color:#4ade80;}"
        ".ctext{font-size:19px;font-weight:700;color:#d4d6db;}"
        ".cta{position:absolute;bottom:100px;left:56px;right:56px;background:#FF6D00;"
        "border-radius:14px;padding:24px 32px;text-align:center;}"
        ".cta-t{font-size:22px;font-weight:900;color:#fff;}"
        ".cta-s{font-size:15px;color:#ffffffcc;margin-top:8px;}"
        "</style></head><body>"
        "<div class='num'>10/10</div>"
        "<div class='title'>まとめ｜食前水ルール3ステップ</div>"
        "<div class='checks'>"
        "<div class='check'><div class='cbadge cb1'>✓</div>"
        "<div class='ctext'>食前300mlで満腹シグナルを早める</div></div>"
        "<div class='check'><div class='cbadge cb2'>✓</div>"
        "<div class='ctext'>夕食前だけに固定する（1食でOK）</div></div>"
        "<div class='check'><div class='cbadge cb3'>✓</div>"
        "<div class='ctext'>崩れたら翌日また飲むだけ。8勝6敗でOK</div></div>"
        "</div>"
        "<div class='cta'>"
        "<div class='cta-t'>7日間、1食だけ試してみてください。</div>"
        "<div class='cta-s'>詳しくはnoteに書きました👇 https://note.com/mash_anti_metabo</div>"
        "</div>"
        "<div class='author'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div class='series' style='color:#FF6D00;'>" + HASHTAG + "</div>"
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
            "## 投稿" + str(i+1) + "/10｜" + tag + "\n\n```\n" + tweet.strip() + FIXED_TAGS + "\n```\n\n"
            "![カード" + str(i+1) + "](x_post_" + str(i+1).zfill(2) + ".png)\n\n---\n\n"
        )
    out.write_text("".join(lines), encoding="utf-8")

if __name__ == "__main__":
    print("第 X投稿カード画像（図解版）生成開始...\n")
    for i, func in enumerate(CARD_FUNCS):
        html = func()
        fname = "x_post_" + str(i+1).zfill(2) + ".png"
        render(html, fname)
        print("✅ " + fname + "  [" + CARD_TAGS[i] + "]")
    save_tweets()
    print("\n全10枚完了。保存先: " + str(OUTPUT_DIR))

