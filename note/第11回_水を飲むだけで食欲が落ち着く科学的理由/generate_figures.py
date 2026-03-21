#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 図解生成スクリプト（HTML/CSS + Playwright 強化版）"""
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
    """図解① 夕食暴走ループ（円形フロー）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;}"
        ".title{position:absolute;left:56px;top:40px;font-size:32px;font-weight:900;color:#fff;}"
        ".sub{position:absolute;left:56px;top:82px;font-size:16px;color:#9ca3af;}"
        ".loop{position:absolute;left:50%;top:55%;transform:translate(-50%,-45%);width:700px;height:420px;}"
        ".step{position:absolute;width:220px;padding:18px 16px;border-radius:14px;text-align:center;"
        "font-size:15px;font-weight:700;line-height:1.5;}"
        ".s1{top:0;left:240px;background:#1e3a5f;color:#38bdf8;border:2px solid #38bdf8;}"
        ".s2{top:100px;right:0;background:#1e3a5f;color:#ef4444;border:2px solid #ef4444;}"
        ".s3{bottom:30px;right:60px;background:#1e3a5f;color:#ef4444;border:2px solid #ef4444;}"
        ".s4{bottom:30px;left:60px;background:#1e3a5f;color:#f59e0b;border:2px solid #f59e0b;}"
        ".s5{top:100px;left:0;background:#1e3a5f;color:#9ca3af;border:2px solid #9ca3af;}"
        ".arrow{position:absolute;font-size:28px;color:#FF6D00;font-weight:900;}"
        ".a1{top:55px;left:420px;transform:rotate(30deg);}"
        ".a2{top:220px;right:80px;transform:rotate(90deg);}"
        ".a3{bottom:80px;left:350px;transform:rotate(180deg);}"
        ".a4{top:220px;left:80px;transform:rotate(270deg);}"
        ".a5{top:55px;left:200px;transform:rotate(330deg);}"
        ".center{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);"
        "font-size:18px;font-weight:900;color:#FF6D00;text-align:center;line-height:1.6;"
        "background:rgba(255,109,0,0.1);padding:14px 24px;border-radius:50%;width:140px;height:140px;"
        "display:flex;align-items:center;justify-content:center;border:2px dashed #FF6D00;}"
        ".credit{position:absolute;bottom:20px;right:40px;font-size:14px;color:#3a3a3a;}"
        "</style></head><body>"
        "<div class='title'>夕食の食べ過ぎループ</div>"
        "<div class='sub'>意志の弱さじゃない。体の状態が食べ過ぎやすい条件になっているだけ</div>"
        "<div class='loop'>"
        "<div class='step s1'>① 日中、水を<br>ほとんど飲まない</div>"
        "<div class='step s2'>② 夕方、脱水を<br>空腹と誤認</div>"
        "<div class='step s3'>③ 帰宅→即食事<br>5分で完食</div>"
        "<div class='step s4'>④ 食後の罪悪感<br>「やってしまった…」</div>"
        "<div class='step s5'>⑤ 翌日「今日こそ」<br>→ また同じ</div>"
        "<div class='arrow a1'>→</div>"
        "<div class='arrow a2'>→</div>"
        "<div class='arrow a3'>→</div>"
        "<div class='arrow a4'>→</div>"
        "<div class='arrow a5'>→</div>"
        "<div class='center'>毎日<br>繰り返す</div>"
        "</div>"
        "<div class='credit'>マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>")
    render(html, "図解①_夕食暴走ループ.png")


def fig2():
    """図解② 食前水3つの効果（横3列カード）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;}"
        ".title{position:absolute;left:56px;top:40px;font-size:32px;font-weight:900;color:#fff;}"
        ".sub{position:absolute;left:56px;top:82px;font-size:16px;color:#9ca3af;}"
        ".cards{position:absolute;top:140px;left:56px;right:56px;display:flex;gap:24px;}"
        ".card{flex:1;background:#1e3a5f;border-radius:16px;padding:32px 24px;}"
        ".card-num{font-size:48px;font-weight:900;margin-bottom:12px;}"
        ".c1 .card-num{color:#38bdf8;}"
        ".c2 .card-num{color:#FF6D00;}"
        ".c3 .card-num{color:#4ade80;}"
        ".card-title{font-size:22px;font-weight:800;color:#fff;margin-bottom:16px;line-height:1.4;}"
        ".card-body{font-size:15px;color:#9ca3af;line-height:1.7;}"
        ".card-data{margin-top:16px;padding:12px;border-radius:8px;font-size:14px;font-weight:700;}"
        ".c1 .card-data{background:#38bdf822;color:#38bdf8;}"
        ".c2 .card-data{background:#FF6D0022;color:#FF6D00;}"
        ".c3 .card-data{background:#4ade8022;color:#4ade80;}"
        ".arrow-between{position:absolute;top:300px;font-size:36px;color:#FF6D00;font-weight:900;}"
        ".ab1{left:400px;} .ab2{left:820px;}"
        ".credit{position:absolute;bottom:20px;right:40px;font-size:14px;color:#3a3a3a;}"
        "</style></head><body>"
        "<div class='title'>食前の水が効く3つの理由</div>"
        "<div class='sub'>食事を変える前に、食事の「前」を変える</div>"
        "<div class='cards'>"
        "<div class='card c1'>"
        "<div class='card-num'>01</div>"
        "<div class='card-title'>満腹シグナルが<br>早く立ち上がる</div>"
        "<div class='card-body'>胃が先に満たされ「もう十分」のサインが早まる</div>"
        "<div class='card-data'>1食 -75kcal（Davy 2008）</div>"
        "</div>"
        "<div class='card c2'>"
        "<div class='card-num'>02</div>"
        "<div class='card-title'>勢い食いに<br>ブレーキがかかる</div>"
        "<div class='card-body'>食事前のワンクッションで衝動的パターンを止める</div>"
        "<div class='card-data'>30秒の行動が1食を変える</div>"
        "</div>"
        "<div class='card c3'>"
        "<div class='card-num'>03</div>"
        "<div class='card-title'>ニセの空腹を<br>見分けられる</div>"
        "<div class='card-body'>脱水由来の空腹感を水で判定→本当の空腹だけに対応</div>"
        "<div class='card-data'>5分待てば答えが出る</div>"
        "</div>"
        "</div>"
        "<div class='arrow-between ab1'>→</div>"
        "<div class='arrow-between ab2'>→</div>"
        "<div class='credit'>マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>")
    render(html, "図解②_食前水3つの効果.png")


def fig3():
    """図解③ 食前水 NG vs OK 比較表"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;}"
        ".title{position:absolute;left:56px;top:40px;font-size:32px;font-weight:900;color:#fff;}"
        ".panels{position:absolute;top:120px;left:56px;right:56px;display:flex;gap:32px;height:520px;}"
        ".panel{flex:1;border-radius:16px;padding:32px;}"
        ".ng{background:#1a0a0a;border:2px solid #ef4444;}"
        ".ok{background:#0a1a0a;border:2px solid #4ade80;}"
        ".panel-header{font-size:28px;font-weight:900;margin-bottom:24px;display:flex;align-items:center;gap:12px;}"
        ".ng .panel-header{color:#ef4444;}"
        ".ok .panel-header{color:#4ade80;}"
        ".panel-icon{font-size:36px;}"
        ".row{display:flex;align-items:flex-start;gap:12px;margin-bottom:20px;}"
        ".row-time{font-size:14px;font-weight:700;min-width:50px;padding:4px 8px;border-radius:6px;text-align:center;}"
        ".ng .row-time{background:#ef444422;color:#ef4444;}"
        ".ok .row-time{background:#4ade8022;color:#4ade80;}"
        ".row-text{font-size:15px;color:#d4d6db;line-height:1.6;}"
        ".result{margin-top:20px;padding:16px;border-radius:10px;font-size:16px;font-weight:800;text-align:center;}"
        ".ng .result{background:#ef444422;color:#ef4444;}"
        ".ok .result{background:#4ade8022;color:#4ade80;}"
        ".vs{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);"
        "font-size:32px;font-weight:900;color:#FF6D00;"
        "background:#0d1b2a;padding:12px 16px;border-radius:50%;border:3px solid #FF6D00;z-index:10;}"
        ".credit{position:absolute;bottom:20px;right:40px;font-size:14px;color:#3a3a3a;}"
        "</style></head><body>"
        "<div class='title'>食前水なし vs あり ── 夕食パターン比較</div>"
        "<div class='panels'>"
        "<div class='panel ng'>"
        "<div class='panel-header'><span class='panel-icon'>✗</span> 水なしパターン</div>"
        "<div class='row'><span class='row-time'>日中</span><span class='row-text'>水ほぼゼロ（750ml以下）</span></div>"
        "<div class='row'><span class='row-time'>18時</span><span class='row-text'>脱水→空腹と誤認</span></div>"
        "<div class='row'><span class='row-time'>帰宅</span><span class='row-text'>即・冷蔵庫に直行</span></div>"
        "<div class='row'><span class='row-time'>食事</span><span class='row-text'>5分で完食。勢い食い</span></div>"
        "<div class='row'><span class='row-time'>食後</span><span class='row-text'>罪悪感「やってしまった…」</span></div>"
        "<div class='result'>→ 食べ過ぎ＋自己嫌悪ループ</div>"
        "</div>"
        "<div class='panel ok'>"
        "<div class='panel-header'><span class='panel-icon'>✓</span> 食前水パターン</div>"
        "<div class='row'><span class='row-time'>日中</span><span class='row-text'>こまめに水分補給</span></div>"
        "<div class='row'><span class='row-time'>18時</span><span class='row-text'>本当の空腹を判定</span></div>"
        "<div class='row'><span class='row-time'>食前</span><span class='row-text'>水300mlをゆっくり飲む</span></div>"
        "<div class='row'><span class='row-time'>食事</span><span class='row-text'>最初3分ゆっくり開始</span></div>"
        "<div class='row'><span class='row-time'>食後</span><span class='row-text'>適量で満足「ちょうどいい」</span></div>"
        "<div class='result'>→ 1食-75kcal × 毎日 = 月-300g脂肪</div>"
        "</div>"
        "</div>"
        "<div class='vs'>VS</div>"
        "<div class='credit'>マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>")
    render(html, "図解③_食前水NGvsOK.png")


def fig4():
    """図解④ 食前水実践早見表（テーブル型）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;}"
        ".title{position:absolute;left:56px;top:40px;font-size:32px;font-weight:900;color:#fff;}"
        ".sub{position:absolute;left:56px;top:82px;font-size:16px;color:#9ca3af;}"
        ".table{position:absolute;top:130px;left:56px;right:56px;border-collapse:separate;border-spacing:0 8px;}"
        ".table th{padding:14px 20px;font-size:15px;font-weight:800;color:#FF6D00;text-align:left;"
        "border-bottom:2px solid #FF6D00;}"
        ".table td{padding:16px 20px;font-size:16px;color:#d4d6db;background:#1e3a5f;line-height:1.5;}"
        ".table tr td:first-child{border-radius:10px 0 0 10px;font-weight:800;color:#38bdf8;width:180px;}"
        ".table tr td:last-child{border-radius:0 10px 10px 0;}"
        ".table tr td:nth-child(2){width:350px;}"
        ".tip{position:absolute;bottom:80px;left:56px;right:56px;background:#FF6D0015;border:1px solid #FF6D00;"
        "border-radius:12px;padding:18px 24px;color:#FF6D00;font-size:16px;font-weight:700;}"
        ".credit{position:absolute;bottom:20px;right:40px;font-size:14px;color:#3a3a3a;}"
        "</style></head><body>"
        "<div class='title'>食前水ルール 実践早見表</div>"
        "<div class='sub'>3ステップ × 1食だけ。これだけで食欲の暴走を抑える</div>"
        "<table class='table'>"
        "<tr><th>ステップ</th><th>やること</th><th>ポイント</th></tr>"
        "<tr><td>STEP 1</td><td>夕食前だけに固定する</td><td>一番リラックスしている食事を選ぶ</td></tr>"
        "<tr><td>STEP 2</td><td>食前10〜15分に水300ml</td><td>常温〜やや冷たい水。30〜60秒でゆっくり</td></tr>"
        "<tr><td>STEP 3</td><td>最初の3分はゆっくり食べる</td><td>味噌汁・サラダから。白飯は後回し</td></tr>"
        "<tr><td>水分目安</td><td>1日の目安 = 体重×30ml</td><td>68kg→約2L。食前300mlで底上げ</td></tr>"
        "<tr><td>崩れた日</td><td>次の食事でまた飲むだけ</td><td>8勝6敗でOK。復帰力が全て</td></tr>"
        "</table>"
        "<div class='tip'>💡 300mlが多ければ200mlからOK。大事なのは量より「毎回やる」こと</div>"
        "<div class='credit'>マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>")
    render(html, "図解④_食前水実践早見表.png")


def fig5():
    """図解⑤ 崩れた日の復帰フロー（縦型3ステップ）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;}"
        ".title{position:absolute;left:56px;top:40px;font-size:32px;font-weight:900;color:#fff;}"
        ".sub{position:absolute;left:56px;top:82px;font-size:16px;color:#9ca3af;}"
        ".flow{position:absolute;top:140px;left:50%;transform:translateX(-50%);width:600px;}"
        ".step{background:#1e3a5f;border-radius:14px;padding:24px 32px;margin-bottom:16px;"
        "display:flex;align-items:center;gap:20px;}"
        ".step-num{font-size:36px;font-weight:900;min-width:56px;text-align:center;"
        "border-radius:50%;width:56px;height:56px;line-height:56px;}"
        ".n1{background:#ef444433;color:#ef4444;}"
        ".n2{background:#f59e0b33;color:#f59e0b;}"
        ".n3{background:#4ade8033;color:#4ade80;}"
        ".step-text{font-size:20px;font-weight:700;color:#fff;line-height:1.5;}"
        ".step-detail{font-size:14px;color:#9ca3af;margin-top:4px;font-weight:400;}"
        ".connector{width:4px;height:16px;background:linear-gradient(180deg,#ef4444,#4ade80);"
        "margin:0 auto;border-radius:2px;}"
        ".motto{position:absolute;bottom:80px;left:50%;transform:translateX(-50%);"
        "background:#FF6D0018;border:2px solid #FF6D00;border-radius:16px;"
        "padding:20px 48px;text-align:center;}"
        ".motto-text{font-size:28px;font-weight:900;color:#FF6D00;}"
        ".motto-sub{font-size:15px;color:#9ca3af;margin-top:8px;}"
        ".credit{position:absolute;bottom:20px;right:40px;font-size:14px;color:#3a3a3a;}"
        "</style></head><body>"
        "<div class='title'>崩れた日の復帰フロー</div>"
        "<div class='sub'>完璧を目指さない。戻れる力が習慣の本体</div>"
        "<div class='flow'>"
        "<div class='step'><div class='step-num n1'>1</div><div>"
        "<div class='step-text'>崩れた。忘れた。食べ過ぎた。</div>"
        "<div class='step-detail'>外食・会食・疲れ… 普通にある。責めない。</div>"
        "</div></div>"
        "<div class='connector'></div>"
        "<div class='step'><div class='step-num n2'>2</div><div>"
        "<div class='step-text'>自己嫌悪をスキップする。</div>"
        "<div class='step-detail'>「もう無理」とゼロに戻らない。1日のミスは1日で終わり。</div>"
        "</div></div>"
        "<div class='connector'></div>"
        "<div class='step'><div class='step-num n3'>3</div><div>"
        "<div class='step-text'>次の食事で、また水を飲む。</div>"
        "<div class='step-detail'>それだけでリセット完了。習慣は生きている。</div>"
        "</div></div>"
        "</div>"
        "<div class='motto'>"
        "<div class='motto-text'>8勝6敗でOK。</div>"
        "<div class='motto-sub'>週5日できたら十分。復帰力がすべて。</div>"
        "</div>"
        "<div class='credit'>マーシー｜100kg→68kg｜Sub3</div>"
        "</body></html>")
    render(html, "図解⑤_崩れた日の復帰フロー.png")


if __name__ == "__main__":
    print("第 図解5枚 生成開始...\n")
    fig1(); fig2(); fig3(); fig4(); fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))

