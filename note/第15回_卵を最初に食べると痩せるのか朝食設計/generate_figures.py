#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "images" / "note_figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FONT_URL = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf"


def shell(title: str, body: str) -> str:
    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
        "@font-face{font-family:'NJ';src:url('" + FONT_URL + "');font-weight:100 900;}"
        "*{margin:0;padding:0;box-sizing:border-box;}"
        "body{width:1280px;height:670px;overflow:hidden;background:#061018;color:#fff;"
        "font-family:'NJ','Yu Gothic UI',sans-serif;position:relative;}"
        ".bg1{position:absolute;inset:0;background:"
        "radial-gradient(circle at 18% 20%,rgba(56,189,248,.18),transparent 26%),"
        "radial-gradient(circle at 84% 12%,rgba(255,109,0,.16),transparent 28%),"
        "linear-gradient(180deg,#08131f 0%,#03070b 100%);}"
        ".noise{position:absolute;inset:0;opacity:.06;background-image:"
        "linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),"
        "linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:36px 36px;}"
        ".frame{position:absolute;inset:28px;border:1px solid rgba(255,255,255,.08);border-radius:28px;}"
        ".title{position:absolute;left:48px;top:40px;font-size:44px;font-weight:900;letter-spacing:-.03em;}"
        ".label{position:absolute;left:48px;top:18px;font-size:14px;font-weight:800;letter-spacing:.18em;color:#f97316;}"
        ".brand{position:absolute;right:44px;bottom:28px;font-size:16px;color:#9ca3af;}"
        ".panel{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);"
        "border-radius:24px;backdrop-filter:blur(12px);}"
        ".muted{color:#9ca3af;}"
        ".orange{color:#ff6d00;}"
        ".blue{color:#38bdf8;}"
        ".green{color:#4ade80;}"
        "</style></head><body>"
        "<div class='bg1'></div><div class='noise'></div><div class='frame'></div>"
        "<div class='label'>NOTE FIGURE</div>"
        "<div class='title'>" + title + "</div>"
        + body +
        "<div class='brand'>マーシー｜第 卵朝食設計</div>"
        "</body></html>"
    )


def fig01() -> tuple[str, str]:
    items = [
        ("7:00", "卵2〜3個を先に食べる", "#ff6d00"),
        ("10:00", "間食したさが下がりやすい", "#38bdf8"),
        ("12:00", "昼の主食を少し抑えやすい", "#4ade80"),
        ("15:00", "眠気・だるさが軽くなりやすい", "#38bdf8"),
        ("夜", "ドカ食いの入口を1段階小さくする", "#ff6d00"),
    ]
    lines = ""
    for idx, (time, text, color) in enumerate(items):
        top = 150 + idx * 78
        lines += (
            "<div style='position:absolute;left:88px;top:" + str(top) + "px;display:flex;align-items:center;'>"
            "<div class='panel' style='width:120px;height:56px;border-color:" + color + "66;display:flex;"
            "align-items:center;justify-content:center;font-size:28px;font-weight:900;color:" + color + ";'>" + time + "</div>"
            "<div style='width:58px;height:4px;background:" + color + ";margin:0 18px;border-radius:999px;'></div>"
            "<div class='panel' style='width:760px;padding:16px 24px;font-size:28px;font-weight:800;'>" + text + "</div>"
            "</div>"
        )
    body = (
        lines +
        "<div style='position:absolute;right:72px;top:164px;width:250px;' class='panel'>"
        "<div style='padding:22px 20px;'>"
        "<div style='font-size:18px;font-weight:800;color:#38bdf8;margin-bottom:10px;'>研究の示唆</div>"
        "<div style='font-size:16px;line-height:1.7;color:#d1d5db;'>"
        "卵朝食は昼前の満腹感を高め、昼食量を減らしやすい。<br>"
        "狙うのは“朝だけ”ではなく“その後の崩れ”です。"
        "</div></div></div>"
    )
    return "figure_01_朝の卵が効く場所", shell("卵が効くのは、朝よりその後", body)


def fig02() -> tuple[str, str]:
    body = (
        "<div style='position:absolute;left:64px;top:136px;width:540px;height:430px;' class='panel'>"
        "<div style='padding:28px;'>"
        "<div class='orange' style='font-size:26px;font-weight:900;margin-bottom:16px;'>言えること</div>"
        "<div style='font-size:26px;line-height:1.75;font-weight:700;'>"
        "・短期の満腹感は上がりやすい<br>"
        "・昼食量が下がる報告がある<br>"
        "・減量食と組み合わせると有利な可能性"
        "</div></div></div>"
        "<div style='position:absolute;right:64px;top:136px;width:540px;height:430px;' class='panel'>"
        "<div style='padding:28px;'>"
        "<div class='blue' style='font-size:26px;font-weight:900;margin-bottom:16px;'>言えないこと</div>"
        "<div style='font-size:26px;line-height:1.75;font-weight:700;'>"
        "・卵だけで脂肪が落ちる<br>"
        "・3個が万人に最適<br>"
        "・朝食を足せば必ず痩せる"
        "</div></div></div>"
        "<div style='position:absolute;left:120px;right:120px;bottom:68px;' class='panel'>"
        "<div style='padding:18px 24px;font-size:24px;font-weight:800;text-align:center;'>"
        "卵は <span class='orange'>痩せ薬</span> ではない。<span class='blue'>食欲設計ツール</span> として使う。"
        "</div></div>"
    )
    return "figure_02_言えること言えないこと", shell("卵朝食で、何が言えて何が言えないか", body)


def fig03() -> tuple[str, str]:
    body = (
        "<div style='position:absolute;left:76px;top:150px;width:500px;height:360px;' class='panel'>"
        "<div style='padding:28px;'>"
        "<div class='blue' style='font-size:30px;font-weight:900;margin-bottom:18px;'>卵2個</div>"
        "<div style='font-size:24px;line-height:1.8;font-weight:700;'>"
        "・研究の中心はこちら<br>"
        "・約12gのたんぱく質<br>"
        "・まず始めやすい<br>"
        "・LDLが気になる人にも入りやすい"
        "</div></div></div>"
        "<div style='position:absolute;right:76px;top:150px;width:500px;height:360px;' class='panel'>"
        "<div style='padding:28px;'>"
        "<div class='orange' style='font-size:30px;font-weight:900;margin-bottom:18px;'>卵3個</div>"
        "<div style='font-size:24px;line-height:1.8;font-weight:700;'>"
        "・約18gのたんぱく質<br>"
        "・10時に崩れやすい人向き<br>"
        "・体格が大きい人で試す価値<br>"
        "・重ければ2個＋汁物へ戻す"
        "</div></div></div>"
        "<div style='position:absolute;left:112px;right:112px;bottom:74px;text-align:center;font-size:28px;font-weight:900;'>"
        "正解は固定ではない。<span class='green'>10時の空腹</span>で判定する。"
        "</div>"
    )
    return "figure_03_2個と3個の考え方", shell("エビデンスの中心は2個。3個は実務仮説", body)


def fig04() -> tuple[str, str]:
    steps = [
        ("1", "朝いちで卵2個", "主食より先に入れる"),
        ("2", "崩れるなら3個", "2個で昼前に空腹なら増やす"),
        ("3", "味噌汁か無糖飲料", "満足感と再現性を補強"),
        ("4", "4項目だけ記録", "間食欲・眠気・だるさ・続けやすさ"),
    ]
    html = ""
    for idx, (num, title, note) in enumerate(steps):
        left = 80 + idx % 2 * 560
        top = 150 + idx // 2 * 180
        color = "#ff6d00" if idx % 2 == 0 else "#38bdf8"
        html += (
            "<div class='panel' style='position:absolute;left:" + str(left) + "px;top:" + str(top) + "px;width:500px;height:138px;"
            "border-color:" + color + "55;'>"
            "<div style='padding:22px 24px;display:flex;gap:16px;'>"
            "<div style='width:56px;height:56px;border-radius:50%;background:" + color + ";display:flex;align-items:center;"
            "justify-content:center;font-size:28px;font-weight:900;color:#000;'>" + num + "</div>"
            "<div><div style='font-size:28px;font-weight:900;line-height:1.3;'>" + title + "</div>"
            "<div class='muted' style='font-size:18px;line-height:1.6;margin-top:6px;'>" + note + "</div></div>"
            "</div></div>"
        )
    html += (
        "<div style='position:absolute;left:160px;right:160px;bottom:58px;text-align:center;font-size:24px;font-weight:800;'>"
        "1週間だけでいい。<span class='orange'>ゼロか100</span>ではなく、<span class='green'>翌日に再開</span>で判定する。"
        "</div>"
    )
    return "figure_04_1週間プロトコル", shell("卵先食べ 1週間プロトコル", html)


def fig05() -> tuple[str, str]:
    body = (
        "<div style='position:absolute;left:76px;top:152px;width:500px;height:360px;' class='panel'>"
        "<div style='padding:28px;'>"
        "<div class='green' style='font-size:28px;font-weight:900;margin-bottom:16px;'>向いている人</div>"
        "<div style='font-size:24px;line-height:1.8;font-weight:700;'>"
        "・朝がパンだけになりやすい<br>"
        "・10時に間食したくなる<br>"
        "・昼にドカ食いしやすい<br>"
        "・朝の準備を固定したい"
        "</div></div></div>"
        "<div style='position:absolute;right:76px;top:152px;width:500px;height:360px;' class='panel'>"
        "<div style='padding:28px;'>"
        "<div class='orange' style='font-size:28px;font-weight:900;margin-bottom:16px;'>注意が必要な人</div>"
        "<div style='font-size:24px;line-height:1.8;font-weight:700;'>"
        "・LDLが高い<br>"
        "・脂質異常症で通院中<br>"
        "・糖尿病がある<br>"
        "・毎日3個固定にしたい人"
        "</div></div></div>"
        "<div style='position:absolute;left:120px;right:120px;bottom:66px;' class='panel'>"
        "<div style='padding:20px 24px;text-align:center;font-size:22px;font-weight:800;'>"
        "迷ったら <span class='blue'>2個から</span>。通院中なら <span class='orange'>主治医の指示を優先</span>。"
        "</div></div>"
    )
    return "figure_05_向いている人注意が必要な人", shell("卵先食べは誰に向くか", body)


FIGURES = [fig01, fig02, fig03, fig04, fig05]


def render(html: str, out_path: Path) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 670})
        page.set_content(html)
        page.wait_for_timeout(900)
        page.screenshot(path=str(out_path))
        browser.close()


def main() -> None:
    for fn in FIGURES:
        stem, html = fn()
        (OUTPUT_DIR / f"{stem}.html").write_text(html, encoding="utf-8")
        render(html, OUTPUT_DIR / f"{stem}.png")


if __name__ == "__main__":
    main()

