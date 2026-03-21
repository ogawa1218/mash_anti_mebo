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
    """図解① 体重計回避ループ（円形フロー）"""
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
        "<div class='title'>体重計回避ループ</div>"
        "<div class='sub'>意志の弱さじゃない。ハードルが高すぎるだけ</div>"
        "<div class='loop'>"
        "<div class='step s1'>① 食べすぎた<br>（昨夜の夜食）</div>"
        "<div class='step s2'>② 体重計が怖い<br>「増えてるかも…」</div>"
        "<div class='step s3'>③ 測定を回避<br>「明日でいいか」</div>"
        "<div class='step s4'>④ 現実が見えない<br>不安だけが増大</div>"
        "<div class='step s5'>⑤ さらに食べすぎ<br>「どうせもう…」</div>"
        "<div class='arrow a1'>\u2192</div>"
        "<div class='arrow a2'>\u2192</div>"
        "<div class='arrow a3'>\u2192</div>"
        "<div class='arrow a4'>\u2192</div>"
        "<div class='arrow a5'>\u2192</div>"
        "<div class='center'>毎週<br>繰り返す</div>"
        "</div>"
        "<div class='credit'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "</body></html>")
    render(html, "図解①_体重計回避ループ.png")


def fig2():
    """図解② if-then × 最小レベル（横3列カード）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;display:flex;flex-direction:column;align-items:center;}"
        ".title{margin-top:40px;font-size:32px;font-weight:900;color:#fff;text-align:center;}"
        ".sub{font-size:16px;color:#9ca3af;margin-top:8px;text-align:center;}"
        ".cards{display:flex;gap:32px;margin-top:48px;}"
        ".card{width:340px;padding:32px 28px;border-radius:16px;text-align:center;}"
        ".c1{background:#0d2035;border:2px solid #38bdf8;}"
        ".c2{background:#0d2035;border:2px solid #FF6D00;}"
        ".c3{background:#0d2035;border:2px solid #4ade80;}"
        ".card-num{font-size:48px;font-weight:900;margin-bottom:12px;}"
        ".n1{color:#38bdf8;} .n2{color:#FF6D00;} .n3{color:#4ade80;}"
        ".card-title{font-size:22px;font-weight:800;color:#fff;margin-bottom:16px;line-height:1.4;}"
        ".card-body{font-size:16px;color:#9ca3af;line-height:1.7;text-align:left;}"
        ".card-body strong{color:#fff;}"
        ".arrow-r{font-size:36px;color:#FF6D00;font-weight:900;align-self:center;margin-top:48px;}"
        ".credit{position:absolute;bottom:20px;right:40px;font-size:14px;color:#3a3a3a;}"
        "</style></head><body>"
        "<div class='title'>体重計に乗り続ける2つの仕組み</div>"
        "<div class='sub'>if-thenプランニング \u00d7 ハードルを極限まで下げる</div>"
        "<div class='cards'>"
        "<div class='card c1'>"
        "<div class='card-num n1'>01</div>"
        "<div class='card-title'>if-then<br>プランニング</div>"
        "<div class='card-body'><strong>「トイレの後に、乗る」</strong><br><br>"
        "いつ・何をするかを<br>事前に決めるだけ。<br><br>"
        "実行率<strong>2\u301c3倍</strong><br>"
        "<span style='font-size:13px;color:#555;'>Gollwitzer 1999</span></div>"
        "</div>"
        "<div class='arrow-r'>\u00d7</div>"
        "<div class='card c2'>"
        "<div class='card-num n2'>02</div>"
        "<div class='card-title'>ハードルを<br>極限まで下げる</div>"
        "<div class='card-body'><strong>レベル1：乗るだけ（3秒）</strong><br><br>"
        "記録しない。<br>数字も見なくていい。<br><br>"
        "2秒でできるレベルへ<br>"
        "<span style='font-size:13px;color:#555;'>BJ Fogg Tiny Habits</span></div>"
        "</div>"
        "<div class='arrow-r'>\u2192</div>"
        "<div class='card c3'>"
        "<div class='card-num n3'>03</div>"
        "<div class='card-title'>自動で<br>続く計測習慣</div>"
        "<div class='card-body'><strong>毎朝「考えずに」乗れる</strong><br><br>"
        "毎日計測群は<br>6ヶ月で<strong>-6.1kg</strong><br>"
        "vs 週1回群 -3.7kg<br>"
        "<span style='font-size:13px;color:#555;'>Steinberg 2015</span></div>"
        "</div>"
        "</div>"
        "<div class='credit'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "</body></html>")
    render(html, "図解②_if-then×最小レベル.png")


def fig3():
    """図解③ 意志力 vs 仕組み 比較表（NG vs OK）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;display:flex;flex-direction:column;align-items:center;}"
        ".title{margin-top:40px;font-size:32px;font-weight:900;color:#fff;}"
        ".sub{font-size:16px;color:#9ca3af;margin-top:8px;}"
        ".compare{display:flex;gap:40px;margin-top:40px;}"
        ".panel{width:540px;padding:36px 32px;border-radius:16px;}"
        ".ng{background:rgba(239,68,68,0.08);border:2px solid #ef4444;}"
        ".ok{background:rgba(74,222,128,0.08);border:2px solid #4ade80;}"
        ".panel-head{font-size:24px;font-weight:900;margin-bottom:24px;text-align:center;}"
        ".ph-ng{color:#ef4444;} .ph-ok{color:#4ade80;}"
        ".row{display:flex;align-items:flex-start;gap:14px;margin-bottom:18px;}"
        ".icon{font-size:20px;min-width:28px;text-align:center;margin-top:2px;}"
        ".row-text{font-size:17px;color:#d4d6db;line-height:1.6;font-weight:500;}"
        ".row-text strong{color:#fff;}"
        ".credit{position:absolute;bottom:20px;right:40px;font-size:14px;color:#3a3a3a;}"
        "</style></head><body>"
        "<div class='title'>意志力で測る vs 仕組みで測る</div>"
        "<div class='sub'>同じ「毎朝測る」でも、設計が違うと結果が変わる</div>"
        "<div class='compare'>"
        "<div class='panel ng'>"
        "<div class='panel-head ph-ng'>\u2717 意志力で測る</div>"
        "<div class='row'><span class='icon'>\u274c</span><span class='row-text'>「<strong>明日から毎朝測ろう</strong>」</span></div>"
        "<div class='row'><span class='icon'>\u274c</span><span class='row-text'>測って<strong>記録して分析</strong>まで<br>全部セットで考える</span></div>"
        "<div class='row'><span class='icon'>\u274c</span><span class='row-text'>増えたら<strong>「最悪…」</strong>と<br>自己否定する</span></div>"
        "<div class='row'><span class='icon'>\u274c</span><span class='row-text'>1日サボったら<br><strong>「もういいや」</strong>で終了</span></div>"
        "<div class='row'><span class='icon' style='color:#ef4444;'>\u2193</span><span class='row-text'>結果：<strong>3日で挫折</strong></span></div>"
        "</div>"
        "<div class='panel ok'>"
        "<div class='panel-head ph-ok'>\u2713 仕組みで測る</div>"
        "<div class='row'><span class='icon'>\u2705</span><span class='row-text'>「<strong>トイレの後に乗る</strong>」<br>if-thenで固定</span></div>"
        "<div class='row'><span class='icon'>\u2705</span><span class='row-text'>レベル1：<strong>乗るだけ</strong><br>記録もコメントも不要</span></div>"
        "<div class='row'><span class='icon'>\u2705</span><span class='row-text'>増えたら<strong>「観測完了」</strong><br>と声に出す</span></div>"
        "<div class='row'><span class='icon'>\u2705</span><span class='row-text'>1日サボっても<br><strong>翌朝また乗る</strong></span></div>"
        "<div class='row'><span class='icon' style='color:#4ade80;'>\u2191</span><span class='row-text'>結果：<strong>8勝6敗で継続</strong></span></div>"
        "</div>"
        "</div>"
        "<div class='credit'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "</body></html>")
    render(html, "図解③_意志力vs仕組み比較.png")


def fig4():
    """図解④ 計測習慣レベル早見表（テーブル）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;display:flex;flex-direction:column;align-items:center;}"
        ".title{margin-top:44px;font-size:32px;font-weight:900;color:#fff;}"
        ".sub{font-size:16px;color:#9ca3af;margin-top:8px;}"
        "table{margin-top:40px;border-collapse:separate;border-spacing:0;width:1100px;"
        "border-radius:16px;overflow:hidden;}"
        "th{background:#1e3a5f;color:#38bdf8;font-size:18px;font-weight:800;padding:18px 20px;"
        "text-align:center;border-bottom:2px solid #2a4a6f;}"
        "td{background:#0d2035;color:#d4d6db;font-size:17px;font-weight:500;padding:20px 20px;"
        "text-align:center;border-bottom:1px solid #1a3050;line-height:1.5;}"
        "tr:last-child td{border-bottom:none;}"
        ".lv{font-size:22px;font-weight:900;}"
        ".lv1{color:#4ade80;} .lv2{color:#38bdf8;} .lv3{color:#FF6D00;} .lv4{color:#f59e0b;}"
        ".rec{background:rgba(74,222,128,0.1) !important;}"
        ".rec td{color:#fff;font-weight:700;}"
        ".badge{display:inline-block;background:#4ade80;color:#0d1b2a;font-size:13px;"
        "font-weight:900;padding:3px 10px;border-radius:6px;margin-left:8px;}"
        ".credit{position:absolute;bottom:20px;right:40px;font-size:14px;color:#3a3a3a;}"
        "</style></head><body>"
        "<div class='title'>計測習慣レベル早見表</div>"
        "<div class='sub'>レベル1から始めれば、誰でも続けられる</div>"
        "<table>"
        "<tr><th>レベル</th><th>やること</th><th>時間</th><th>記録</th><th>期間の目安</th></tr>"
        "<tr class='rec'>"
        "<td><span class='lv lv1'>Lv.1</span><span class='badge'>推奨</span></td>"
        "<td>体重計に乗る。以上。</td><td>3秒</td><td>不要</td><td>最初の7\u301c14日間</td></tr>"
        "<tr>"
        "<td><span class='lv lv2'>Lv.2</span></td>"
        "<td>乗って、数字を見る</td><td>5秒</td><td>不要</td><td>2\u301c3週目</td></tr>"
        "<tr>"
        "<td><span class='lv lv3'>Lv.3</span></td>"
        "<td>乗って、数字をメモする</td><td>15秒</td><td>数字のみ</td><td>3\u301c4週目</td></tr>"
        "<tr>"
        "<td><span class='lv lv4'>Lv.4</span></td>"
        "<td>乗って、記録＋一言<br>（「観測完了」）</td><td>30秒</td><td>数字＋一言</td><td>1ヶ月目〜</td></tr>"
        "</table>"
        "<div class='credit'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "</body></html>")
    render(html, "図解④_計測習慣レベル表.png")


def fig5():
    """図解⑤ 崩れた日の復帰フロー（縦型3ステップ）"""
    html = ("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        + BASE_CSS +
        "body{background:#0d1b2a;display:flex;flex-direction:column;align-items:center;}"
        ".title{margin-top:40px;font-size:32px;font-weight:900;color:#fff;}"
        ".sub{font-size:16px;color:#9ca3af;margin-top:8px;}"
        ".trigger{margin-top:32px;background:rgba(239,68,68,0.12);border:2px solid #ef4444;"
        "border-radius:14px;padding:16px 40px;text-align:center;}"
        ".trigger-text{font-size:18px;font-weight:700;color:#ef4444;}"
        ".flow{margin-top:16px;display:flex;flex-direction:column;align-items:center;gap:8px;}"
        ".arrow-down{font-size:28px;color:#FF6D00;font-weight:900;}"
        ".fstep{width:700px;padding:24px 32px;border-radius:14px;display:flex;align-items:center;gap:24px;}"
        ".f1{background:#1e3a5f;border:2px solid #f59e0b;}"
        ".f2{background:#1e3a5f;border:2px solid #FF6D00;}"
        ".f3{background:#1e3a5f;border:2px solid #4ade80;}"
        ".fnum{font-size:36px;font-weight:900;min-width:48px;text-align:center;}"
        ".fn1{color:#f59e0b;} .fn2{color:#FF6D00;} .fn3{color:#4ade80;}"
        ".ftitle{font-size:20px;font-weight:800;color:#fff;margin-bottom:4px;}"
        ".fdesc{font-size:15px;color:#9ca3af;line-height:1.5;}"
        ".result{margin-top:16px;background:rgba(74,222,128,0.12);border:2px solid #4ade80;"
        "border-radius:14px;padding:16px 40px;text-align:center;}"
        ".result-text{font-size:20px;font-weight:900;color:#4ade80;}"
        ".result-sub{font-size:15px;color:#9ca3af;margin-top:4px;}"
        ".credit{position:absolute;bottom:20px;right:40px;font-size:14px;color:#3a3a3a;}"
        "</style></head><body>"
        "<div class='title'>体重が増えた朝のリカバリーフロー</div>"
        "<div class='sub'>if-then：「増えていたら \u2192 3秒待って \u2192 観測完了と言う」</div>"
        "<div class='trigger'>"
        "<div class='trigger-text'>\u26a0 朝、体重が昨日より+1kg増えていた</div>"
        "</div>"
        "<div class='flow'>"
        "<div class='arrow-down'>\u2193</div>"
        "<div class='fstep f1'>"
        "<div class='fnum fn1'>1</div>"
        "<div><div class='ftitle'>3秒待つ</div>"
        "<div class='fdesc'>反射的に責めない。3秒だけ間を取る。<br>±1-2kgは水分・内容物の変動。</div></div>"
        "</div>"
        "<div class='arrow-down'>\u2193</div>"
        "<div class='fstep f2'>"
        "<div class='fnum fn2'>2</div>"
        "<div><div class='ftitle'>「観測完了」と声に出す</div>"
        "<div class='fdesc'>評価コメント（太った・最悪）を封じる。<br>事実だけを確認する。</div></div>"
        "</div>"
        "<div class='arrow-down'>\u2193</div>"
        "<div class='fstep f3'>"
        "<div class='fnum fn3'>3</div>"
        "<div><div class='ftitle'>翌朝もう1回乗る</div>"
        "<div class='fdesc'>連続性を切らないことが最大の勝利条件。<br>「また戻れた」でOK。</div></div>"
        "</div>"
        "</div>"
        "<div class='result'>"
        "<div class='result-text'>8勝6敗で成功。完璧を目指さない。</div>"
        "<div class='result-sub'>14日のうち8日乗れたら、それは立派な習慣です。</div>"
        "</div>"
        "<div class='credit'>マーシー｜100kg\u219268kg｜Sub3</div>"
        "</body></html>")
    render(html, "図解⑤_崩れた日の復帰フロー.png")


if __name__ == "__main__":
    print("第 図解5枚 生成開始...\n")
    fig1(); fig2(); fig3(); fig4(); fig5()
    print("\n全5枚完了。保存先: " + str(OUTPUT_DIR))

