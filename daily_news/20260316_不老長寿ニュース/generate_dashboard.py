#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
ARTICLE_DIR = Path(__file__).parent
FONT = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"
DATE = "2026.03.16（月）"
NEWS = [
    {"category":"🧬 不老長寿","cat_color":"#8b5cf6","title":"老化リセット治験、始動","summary":"FDA承認のエピジェネティック・リプログラミング臨床試験が開始。DNAを変えずに「細胞を若返らせる」世界初の試み。","source":"MIT Technology Review, 2026.01","stars":"★★★"},
    {"category":"⚖️ ダイエット","cat_color":"#ef4444","title":"GLP-1リバウンド解決へ","summary":"新薬TIX100がGLP-1停止後のリバウンドをマウス実験で完全防止。「薬をやめたら太り戻す」問題に新たな光。","source":"UAB Research, 2026","stars":"★★★"},
    {"category":"🥗 食事","cat_color":"#22c55e","title":"腸内細菌が肥満を防ぐ","summary":"「Turicibacter」という腸内細菌が代謝を改善・体重増加を抑制。肥満者はこの菌が少ない。食物繊維・発酵食品で増やせる。","source":"Nutrition Insight, 2026","stars":"★★"},
    {"category":"🏃 運動","cat_color":"#3b82f6","title":"運動の多様性で死亡率19%減","summary":"多様な運動の組み合わせが早期死亡リスクを19%低下（Harvard/BMJ）。「完璧な1種目より、ゆるく色々」が正解。","source":"Harvard / BMJ Medicine, 2026.01","stars":"★★★"},
    {"category":"🏃 運動","cat_color":"#3b82f6","title":"1日5分で死亡率10%減","summary":"1日5分の中〜高強度運動の追加が死亡数を10%削減に相当。睡眠・食事・運動の複合改善で寿命が最大9年延びる。","source":"CNN Health / 複数大学共同研究, 2026.01","stars":"★★★"},
]
BASE_CSS = ("@font-face{font-family:'NJ';src:url('"+FONT+"');font-weight:100 900;}"
    "*{margin:0;padding:0;box-sizing:border-box;}"
    "body{width:1280px;height:900px;overflow:hidden;background:#f0f0f0;font-family:'NJ','Meiryo',sans-serif;position:relative;}")
def build_html():
    header=("<div style='width:100%;height:76px;background:linear-gradient(135deg,#22c55e,#16a34a);display:flex;align-items:center;justify-content:space-between;padding:0 40px;'>"
        "<div><span style='font-size:11px;font-weight:700;color:rgba(255,255,255,.7);letter-spacing:2px;'>LONGEVITY NAVIGATOR</span>"
        "<div style='font-size:24px;font-weight:900;color:#fff;margin-top:2px;'>不老長寿ニュース｜"+DATE+"</div></div>"
        "<div style='text-align:right;'><div style='font-size:13px;color:rgba(255,255,255,.8);'>マーシー｜100kg→68kg｜Sub3</div>"
        "<div style='font-size:11px;color:rgba(255,255,255,.6);margin-top:2px;'>世界最先端の健康研究を毎朝お届け</div></div></div>")
    positions=[("20px","96px","610px","182px"),("650px","96px","610px","182px"),("20px","294px","610px","182px"),("650px","294px","610px","182px"),("20px","492px","1240px","182px")]
    cards=""
    for i,n in enumerate(NEWS):
        l,t,w,h=positions[i]
        cards+=("<div style='position:absolute;left:"+l+";top:"+t+";width:"+w+";height:"+h+";background:#fff;border-radius:14px;padding:16px 20px;box-shadow:0 2px 10px rgba(0,0,0,.07);overflow:hidden;'>"
            "<div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;'>"
            "<span style='background:"+n["cat_color"]+";color:#fff;font-size:12px;font-weight:700;padding:3px 12px;border-radius:12px;'>"+n["category"]+"</span>"
            "<span style='font-size:15px;color:#f59e0b;font-weight:700;'>"+n["stars"]+"</span></div>"
            "<div style='font-size:19px;font-weight:800;color:#1a1a1a;line-height:1.3;margin-bottom:8px;'>"+n["title"]+"</div>"
            "<div style='font-size:13px;color:#5a6070;line-height:1.55;'>"+n["summary"]+"</div>"
            "<div style='position:absolute;bottom:10px;right:18px;font-size:11px;color:#9ca3af;'>"+n["source"]+"</div></div>")
    footer=("<div style='position:absolute;bottom:0;width:100%;height:44px;background:#1a1a2e;display:flex;align-items:center;justify-content:space-between;padding:0 40px;'>"
        "<div style='font-size:13px;font-weight:700;color:#22c55e;'>イチ押し：「1日5分の運動追加で死亡率10%減」→ 今週X投稿に使う</div>"
        "<div style='font-size:12px;color:#6b7280;'>daily_news / 20260316</div></div>")
    return "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"+BASE_CSS+"</style></head><body>"+header+cards+footer+"</body></html>"
if __name__=="__main__":
    print("ダッシュボード生成開始...")
    html=build_html()
    tmp=ARTICLE_DIR/"_tmp_db.html"
    out=ARTICLE_DIR/"dashboard_20260316.png"
    tmp.write_text(html,encoding="utf-8")
    with sync_playwright() as p:
        b=p.chromium.launch()
        pg=b.new_page(viewport={"width":1280,"height":900})
        pg.goto("file:///"+str(tmp).replace("\\","/"))
        pg.wait_for_timeout(1000)
        pg.screenshot(path=str(out),full_page=False)
        b.close()
    tmp.unlink(missing_ok=True)
    print(f"✅ 完了: {out.name}")
