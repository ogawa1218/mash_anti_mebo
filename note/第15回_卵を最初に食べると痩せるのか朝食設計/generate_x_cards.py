#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "images" / "x_posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FONT_URL = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"

CARDS = [
    {
        "kicker": "共感",
        "title": "崩れは夜じゃない。\n朝で仕込まれている。",
        "body": "菓子パン → 10時に甘いもの → 昼大盛り → 夕方だるい → 夜ドカ食い。\nこの連鎖を切る候補が、朝の卵です。",
        "accent": "#ff6d00",
    },
    {
        "kicker": "研究",
        "title": "卵朝食は、\n昼食量を下げやすい。",
        "body": "過体重・肥満のRCTでは、ベーグル朝食より満腹感が高く、昼食摂取量が約160kcal少なかった。",
        "accent": "#38bdf8",
    },
    {
        "kicker": "重要",
        "title": "でも、卵だけで\n痩せるわけじゃない。",
        "body": "差が出るのは、卵をきっかけに1日の総摂取が整ったとき。卵は痩せ薬ではなく補助輪です。",
        "accent": "#4ade80",
    },
    {
        "kicker": "理由",
        "title": "卵先食べが強いのは\n再現性が高いから。",
        "body": "たんぱく質を入れやすい。判断が減る。コンビニでもできる。40代はこの3つが大きい。",
        "accent": "#ff6d00",
    },
    {
        "kicker": "個数",
        "title": "研究の中心は2個。\n3個は実務案。",
        "body": "2個で崩れる人だけ3個を試す。正解探しではなく、10時の空腹と昼の食べ過ぎ感で判定します。",
        "accent": "#38bdf8",
    },
    {
        "kicker": "判定",
        "title": "見るべきは体重より\n10時の自分。",
        "body": "間食したさ、昼食後の眠気、夕方のだるさ。体重より先に、食欲が変わるかを見ます。",
        "accent": "#4ade80",
    },
    {
        "kicker": "失敗",
        "title": "卵を足しただけでは\n痩せない。",
        "body": "朝に卵を追加して、昼も夜もそのままなら総量は増えるだけ。卵の価値は“その後”にあります。",
        "accent": "#ff6d00",
    },
    {
        "kicker": "成功",
        "title": "卵の価値は\n1日の流れを変えること。",
        "body": "昼の主食が少し減る。15時の間食が1回減る。夜のスタートが整う。これが勝ち筋です。",
        "accent": "#38bdf8",
    },
    {
        "kicker": "注意",
        "title": "毎日3個固定で\n押し切らない。",
        "body": "LDLが高い人、脂質異常症・糖尿病で通院中の人は主治医優先。健康習慣と自己流は別です。",
        "accent": "#4ade80",
    },
    {
        "kicker": "行動",
        "title": "今夜やることは1つ。\n6個だけ茹でる。",
        "body": "全部変えなくていい。卵を1パック買って、まず6個だけ準備する。朝の最初の1手だけ変えればいい。",
        "accent": "#ff6d00",
    },
]


def build_html(card: dict, idx: int) -> str:
    accent = card["accent"]
    number = f"{idx:02d}/10"
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        "@font-face{font-family:'NJ';src:url('" + FONT_URL + "');font-weight:100 900;}"
        "*{margin:0;padding:0;box-sizing:border-box;}"
        "body{width:1280px;height:720px;overflow:hidden;background:#05080c;position:relative;"
        "font-family:'NJ','Yu Gothic UI',sans-serif;color:#fff;}"
        ".bg{position:absolute;inset:0;background:"
        "radial-gradient(circle at 15% 15%,rgba(56,189,248,.16),transparent 28%),"
        "radial-gradient(circle at 85% 20%,rgba(255,109,0,.16),transparent 24%),"
        "linear-gradient(180deg,#08131c 0%,#05080c 100%);}"
        ".grid{position:absolute;inset:0;opacity:.06;background-image:"
        "linear-gradient(rgba(255,255,255,.08) 1px,transparent 1px),"
        "linear-gradient(90deg,rgba(255,255,255,.08) 1px,transparent 1px);background-size:44px 44px;}"
        ".edge{position:absolute;left:0;top:0;width:8px;height:100%;background:" + accent + ";}"
        ".tag{position:absolute;left:60px;top:48px;padding:10px 16px;border-radius:999px;font-size:18px;font-weight:800;"
        "background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.14);color:" + accent + ";}"
        ".num{position:absolute;right:58px;top:52px;font-size:22px;font-weight:800;color:#9ca3af;}"
        ".title{position:absolute;left:60px;top:126px;width:1040px;font-size:62px;line-height:1.2;font-weight:900;letter-spacing:-.04em;}"
        ".body{position:absolute;left:60px;top:332px;width:1040px;font-size:30px;line-height:1.65;font-weight:700;color:#d1d5db;}"
        ".rule{position:absolute;left:60px;right:60px;bottom:118px;height:2px;background:linear-gradient(90deg," + accent + ",transparent);}"
        ".footer{position:absolute;left:60px;bottom:52px;font-size:22px;font-weight:800;}"
        ".footer span{color:" + accent + ";}"
        "</style></head><body>"
        "<div class='bg'></div><div class='grid'></div><div class='edge'></div>"
        "<div class='tag'>" + card["kicker"] + "</div>"
        "<div class='num'>" + number + "</div>"
        "<div class='title'>" + card["title"].replace("\n", "<br>") + "</div>"
        "<div class='body'>" + card["body"].replace("\n", "<br>") + "</div>"
        "<div class='rule'></div>"
        "<div class='footer'>マーシー <span>｜ 卵朝食で食欲設計</span></div>"
        "</body></html>"
    )


def render(html: str, out_path: Path) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.set_content(html)
        page.wait_for_timeout(700)
        page.screenshot(path=str(out_path))
        browser.close()


def main() -> None:
    for idx, card in enumerate(CARDS, start=1):
        html = build_html(card, idx)
        (OUTPUT_DIR / f"x_card_{idx:02d}.html").write_text(html, encoding="utf-8")
        render(html, OUTPUT_DIR / f"x_card_{idx:02d}.png")


if __name__ == "__main__":
    main()
