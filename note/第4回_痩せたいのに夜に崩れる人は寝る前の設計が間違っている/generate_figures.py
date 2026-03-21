#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 図解 自動生成スクリプト
Longevity Navigator - マーシー
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ===== 設定 =====
W, H = 1280, 720
FONT_PATH = "C:/Windows/Fonts/NotoSansJP-VF.ttf"
ARTICLE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ARTICLE_DIR, "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== カラー =====
BG     = (26, 42, 58)
PANEL  = (39, 41, 45)
TEXT   = (212, 214, 219)
MUTED  = (122, 126, 138)
ORANGE = (255, 109, 0)
BLUE   = (56, 189, 248)
GREEN  = (74, 222, 128)
RED    = (255, 23, 68)
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)


def f(size):
    return ImageFont.truetype(FONT_PATH, size)


def new_canvas(bg=BG):
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    return img, draw


def ct(draw, text, y, font, color, x0=0, w=W):
    """x0からw幅の領域でテキストを中央揃え"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = x0 + (w - tw) // 2
    draw.text((x, y), text, font=font, fill=color)


def rr(draw, x1, y1, x2, y2, radius=16, fill=PANEL, outline=None, ow=2):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius,
                            fill=fill, outline=outline, width=ow)


def arrow_r(draw, x1, x2, y, color=ORANGE, w=3):
    """右向き矢印"""
    draw.line([(x1, y), (x2 - 12, y)], fill=color, width=w)
    draw.polygon([(x2 - 12, y - 7), (x2, y), (x2 - 12, y + 7)], fill=color)


def arrow_d(draw, x, y1, y2, color=ORANGE, w=3):
    """下向き矢印"""
    draw.line([(x, y1), (x, y2 - 12)], fill=color, width=w)
    draw.polygon([(x - 7, y2 - 12), (x, y2), (x + 7, y2 - 12)], fill=color)


# ======================================================
# 図解① 寝る90分前ルール 全体像
# ======================================================
def make_figure1():
    img, draw = new_canvas()

    ct(draw, "寝る90分前ルール｜3ステップ", 28, f(50), WHITE)
    ct(draw, "睡眠は布団に入る瞬間では決まらない", 90, f(26), MUTED)

    card_w, card_h = 340, 460
    gap = 25
    total = card_w * 3 + gap * 2
    sx = (W - total) // 2
    cy = 145

    cards = [
        ("90分前", "光を落とす", "照明を1段暗く", "スマホはナイトモード", ORANGE),
        ("60分前", "食を締める", "追加カロリーを入れない", "歯磨きがトリガー", ORANGE),
        ("20分前", "脳を静かにする", "呼吸1分 ＋ ストレッチ2分", "＋ 明日の準備2分", ORANGE),
    ]

    for i, (time_txt, title, d1, d2, accent) in enumerate(cards):
        cx = sx + i * (card_w + gap)
        rr(draw, cx, cy, cx + card_w, cy + card_h, radius=20, fill=PANEL)

        # 時間ラベル（大きく）
        ct(draw, time_txt, cy + 20, f(52), accent, x0=cx, w=card_w)

        # 区切り線
        draw.line([(cx + 30, cy + 90), (cx + card_w - 30, cy + 90)], fill=(60, 65, 75), width=2)

        # タイトル
        ct(draw, title, cy + 106, f(32), WHITE, x0=cx, w=card_w)

        # 説明2行
        ct(draw, d1, cy + 160, f(22), TEXT, x0=cx, w=card_w)
        ct(draw, d2, cy + 196, f(22), TEXT, x0=cx, w=card_w)

        # 矢印（カード間）
        if i < 2:
            ax1 = cx + card_w + 2
            ax2 = cx + card_w + gap - 2
            arrow_r(draw, ax1, ax2, cy + card_h // 2, ORANGE, 4)

    ct(draw, "戦いは朝じゃない。寝る前に始まっている。", 628, f(30), ORANGE)

    path = os.path.join(OUTPUT_DIR, "図解①_寝る90分前ルール.png")
    img.save(path)
    print(f"✅ {path}")


# ======================================================
# 図解② 睡眠不足が太りやすくする3つのメカニズム
# ======================================================
def make_figure2():
    img, draw = new_canvas()

    ct(draw, "睡眠が崩れると、なぜ太るのか", 18, f(50), WHITE)

    # 起点ノード
    tn_w, tn_h = 340, 64
    tn_x = (W - tn_w) // 2
    tn_y = 96
    rr(draw, tn_x, tn_y, tn_x + tn_w, tn_y + tn_h, radius=32,
       fill=(55, 10, 18), outline=RED, ow=2)
    ct(draw, "睡眠不足", tn_y + 14, f(34), RED)

    # 分岐3方向
    branch_y = tn_y + tn_h + 16
    tips_x = [200, 640, 1080]
    cx_top = W // 2
    for tx in tips_x:
        draw.line([(cx_top, branch_y), (tx, branch_y + 60)], fill=RED, width=3)
        arrow_d(draw, tx, branch_y + 60, branch_y + 96, RED, 3)

    # 3枚カード
    card_w, card_h = 300, 220
    card_y = branch_y + 96
    card_xs = [50, 490, 930]
    branches = [
        ("① 食欲が暴走", "レプチン↓ グレリン↑", "甘い物・脂っこい物に", "手が伸びる"),
        ("② 判断が雑になる", "前頭前皮質の機能↓", "菓子パン＞サラダチキン", "を選ぶ"),
        ("③ 活動量が落ちる", "だるい→動かない→眠りが浅い", "悪循環に入る", ""),
    ]
    for i, (title, sub, r1, r2) in enumerate(branches):
        bx = card_xs[i]
        rr(draw, bx, card_y, bx + card_w, card_y + card_h, radius=16, fill=PANEL)
        ct(draw, title, card_y + 14, f(28), RED, x0=bx, w=card_w)
        draw.line([(bx + 20, card_y + 54), (bx + card_w - 20, card_y + 54)],
                  fill=(60, 65, 75), width=1)
        ct(draw, sub, card_y + 64, f(20), TEXT, x0=bx, w=card_w)
        ct(draw, r1, card_y + 102, f(19), MUTED, x0=bx, w=card_w)
        if r2:
            ct(draw, r2, card_y + 132, f(19), MUTED, x0=bx, w=card_w)

    # 合流 → 結論ノード
    merge_y = card_y + card_h + 12
    conc_y = merge_y + 64
    for bx in card_xs:
        draw.line([(bx + card_w // 2, merge_y),
                   (cx_top, conc_y - 12)], fill=BLUE, width=3)

    cn_w = 520
    cn_x = (W - cn_w) // 2
    rr(draw, cn_x, conc_y, cn_x + cn_w, conc_y + 62, radius=31,
       fill=(8, 28, 48), outline=BLUE, ow=2)
    ct(draw, "もっと頑張る前に、まず寝る。", conc_y + 14, f(30), BLUE)

    draw.text((20, H - 28), "Taheri S et al. PLoS Med. 2004", font=f(18), fill=MUTED)

    path = os.path.join(OUTPUT_DIR, "図解②_睡眠不足メカニズム.png")
    img.save(path)
    print(f"✅ {path}")


# ======================================================
# 図解③ 照明とメラトニンの比較
# ======================================================
def make_figure3():
    img = Image.new("RGB", (W, H), (10, 10, 15))
    mid = W // 2

    # 左背景（赤みがかった暗色）
    left = Image.new("RGB", (mid, H), (38, 8, 14))
    img.paste(left, (0, 0))
    # 右背景（青みがかった暗色）
    right = Image.new("RGB", (mid, H), (8, 18, 38))
    img.paste(right, (mid, 0))

    draw = ImageDraw.Draw(img)

    # 中央線
    draw.line([(mid, 0), (mid, H)], fill=WHITE, width=3)

    # --- 左側 NG ---
    ct(draw, "❌ 寝る直前まで明るい部屋", 28, f(28), RED, x0=0, w=mid)
    ct(draw, "蛍光灯 全開", 76, f(52), RED, x0=0, w=mid)

    left_items = [
        "メラトニン分泌が約90分遅延",
        "脳が「まだ昼だ」と判断",
        "寝つきが悪く、睡眠の質が低下",
    ]
    for i, item in enumerate(left_items):
        ct(draw, f"・{item}", 200 + i * 56, f(24), RED, x0=0, w=mid)

    ct(draw, "体内時計 90分ズレる", 580, f(32), RED, x0=0, w=mid)

    # --- 右側 OK ---
    ct(draw, "✅ 90分前に照明を落とす", 28, f(28), BLUE, x0=mid, w=mid)
    ct(draw, "間接照明 ＋ ナイトモード", 76, f(40), BLUE, x0=mid, w=mid)

    right_items = [
        "メラトニンが自然に分泌開始",
        "脳が「もう夜だ」と認識",
        "スムーズに入眠できる",
    ]
    for i, item in enumerate(right_items):
        ct(draw, f"・{item}", 200 + i * 56, f(24), BLUE, x0=mid, w=mid)

    ct(draw, "自然な眠りのスイッチON", 580, f(32), GREEN, x0=mid, w=mid)

    draw.text((20, H - 28),
              "Gooley JJ et al. J Clin Endocrinol Metab. 2011",
              font=f(18), fill=MUTED)

    path = os.path.join(OUTPUT_DIR, "図解③_照明とメラトニン比較.png")
    img.save(path)
    print(f"✅ {path}")


# ======================================================
# 図解④ 「食を締める」実践フロー
# ======================================================
def make_figure4():
    img, draw = new_canvas()

    ct(draw, "食を締める｜実践フロー", 20, f(50), WHITE)
    ct(draw, "我慢ではなく、締め時を「仕組み」で決める", 82, f(26), MUTED)

    # レイアウト基準
    cy = 330  # 中心ライン
    nw, nh = 190, 80  # ノード幅・高さ

    # ステップ1
    s1x = 60
    rr(draw, s1x, cy - nh // 2, s1x + nw, cy + nh // 2, radius=40, fill=PANEL)
    ct(draw, "寝る60分前", cy - nh // 2 + 12, f(26), WHITE, x0=s1x, w=nw)
    ct(draw, "時計を確認", cy - nh // 2 + 46, f(20), MUTED, x0=s1x, w=nw)

    arrow_r(draw, s1x + nw, s1x + nw + 60, cy, ORANGE, 4)

    # ステップ2
    s2x = s1x + nw + 60
    rr(draw, s2x, cy - nh // 2, s2x + nw, cy + nh // 2, radius=40, fill=ORANGE)
    ct(draw, "歯を磨く", cy - nh // 2 + 10, f(28), BLACK, x0=s2x, w=nw)
    ct(draw, "これがトリガー", cy - nh // 2 + 46, f(19), BLACK, x0=s2x, w=nw)

    # フォーク点
    fork_x = s2x + nw + 50
    draw.line([(s2x + nw, cy), (fork_x, cy)], fill=ORANGE, width=3)

    # 2ルートへ分岐
    top_y = cy - 120
    bot_y = cy + 120
    draw.line([(fork_x, cy), (fork_x, top_y)], fill=GREEN, width=3)
    draw.line([(fork_x, cy), (fork_x, bot_y)], fill=BLUE, width=3)

    rw, rh = 250, 90

    # ルートA（上）
    arrow_r(draw, fork_x, fork_x + 40, top_y, GREEN, 3)
    rax = fork_x + 40
    rr(draw, rax, top_y - rh // 2, rax + rw, top_y + rh // 2, radius=16, fill=PANEL)
    ct(draw, "お腹が空いていない", top_y - rh // 2 + 16, f(24), GREEN, x0=rax, w=rw)
    ct(draw, "そのまま就寝準備へ", top_y - rh // 2 + 52, f(22), TEXT, x0=rax, w=rw)

    # ルートB（下）
    arrow_r(draw, fork_x, fork_x + 40, bot_y, BLUE, 3)
    rbx = fork_x + 40
    rr(draw, rbx, bot_y - rh // 2, rbx + rw, bot_y + rh // 2, radius=16, fill=PANEL)
    ct(draw, "どうしても空腹が強い", bot_y - rh // 2 + 16, f(24), BLUE, x0=rbx, w=rw)
    ct(draw, "温かいノンカフェイン飲料", bot_y - rh // 2 + 52, f(22), TEXT, x0=rbx, w=rw)

    # 合流
    merge_x = rax + rw + 50
    draw.line([(rax + rw, top_y), (merge_x, top_y)], fill=GREEN, width=3)
    draw.line([(rax + rw, bot_y), (merge_x, bot_y)], fill=BLUE, width=3)
    draw.line([(merge_x, top_y), (merge_x, bot_y)], fill=WHITE, width=3)
    arrow_r(draw, merge_x, merge_x + 50, cy, WHITE, 3)

    # ゴール
    gx = merge_x + 50
    gw, gh = 270, 80
    rr(draw, gx, cy - gh // 2, gx + gw, cy + gh // 2, radius=40, fill=GREEN)
    ct(draw, "今日の食事はここまで", cy - gh // 2 + 12, f(24), BLACK, x0=gx, w=gw)
    ct(draw, "✓ 完了", cy - gh // 2 + 46, f(24), BLACK, x0=gx, w=gw)

    path = os.path.join(OUTPUT_DIR, "図解④_食を締める実践フロー.png")
    img.save(path)
    print(f"✅ {path}")


# ======================================================
# 図解⑤ 崩れた日の復帰フロー
# ======================================================
def make_figure5():
    # グラデーション背景（暗→明）
    img = Image.new("RGB", (W, H))
    for y in range(H):
        r = 10 + int((26 - 10) * y / H)
        g = 10 + int((42 - 10) * y / H)
        b = 10 + int((58 - 10) * y / H)
        for x in range(W):
            img.putpixel((x, y), (r, g, b))

    draw = ImageDraw.Draw(img)

    ct(draw, '崩れた日の"戻り方"', 18, f(50), WHITE)
    ct(draw, "完璧を目指さない。70点を長く続ける。", 78, f(26), ORANGE)

    # ノード1（失敗）
    n1w, n1h = 480, 64
    n1x = (W - n1w) // 2
    n1y = 148
    rr(draw, n1x, n1y, n1x + n1w, n1y + n1h, radius=32,
       fill=(50, 8, 15), outline=RED, ow=2)
    ct(draw, "3ステップ全部できなかった", n1y + 14, f(28), RED)

    arrow_d(draw, W // 2, n1y + n1h, n1y + n1h + 56, RED, 3)

    # 中間メッセージ
    msg_y = n1y + n1h + 56
    ct(draw, "自分を責めない。1つだけでOK", msg_y, f(34), WHITE)
    ct(draw, "1日抜けても習慣強度にほぼ影響なし（メタ分析）", msg_y + 46, f(20), MUTED)

    # 3つの選択肢への分岐
    opt_y = msg_y + 130
    opt_w, opt_h = 280, 100
    opt_xs = [110, 500, 890]
    opts = [
        ("照明だけ暗くした", "合格 ✓"),
        ("夜食だけ回避した", "合格 ✓"),
        ("呼吸1分だけやった", "合格 ✓"),
    ]

    for ox in opt_xs:
        draw.line([(W // 2, msg_y + 88), (ox + opt_w // 2, opt_y - 12)],
                  fill=BLUE, width=2)
        arrow_d(draw, ox + opt_w // 2, opt_y - 12, opt_y, BLUE, 2)

    for i, (opt, result) in enumerate(opts):
        ox = opt_xs[i]
        rr(draw, ox, opt_y, ox + opt_w, opt_y + opt_h, radius=16, fill=PANEL)
        ct(draw, opt, opt_y + 16, f(24), BLUE, x0=ox, w=opt_w)
        ct(draw, result, opt_y + 56, f(24), GREEN, x0=ox, w=opt_w)

    # 合流 → ゴール
    goal_y = opt_y + opt_h + 48
    for ox in opt_xs:
        draw.line([(ox + opt_w // 2, opt_y + opt_h),
                   (W // 2, goal_y - 12)], fill=GREEN, width=2)

    gw, gh = 580, 68
    gx = (W - gw) // 2
    rr(draw, gx, goal_y, gx + gw, goal_y + gh, radius=34, fill=GREEN)
    ct(draw, "8勝6敗で十分。ゼロにしなければ勝ち ✓", goal_y + 18, f(26), BLACK)

    path = os.path.join(OUTPUT_DIR, "図解⑤_崩れた日の復帰フロー.png")
    img.save(path)
    print(f"✅ {path}")


# ======================================================
# メイン
# ======================================================
# ======================================================
# 記事への画像埋め込み
# ======================================================
def embed_images_into_article():
    article_path = os.path.join(ARTICLE_DIR, "第4回_痩せたいのに夜に崩れる人は寝る前の設計が間違っている.md")
    output_path  = os.path.join(ARTICLE_DIR, "第4回_完成版（画像埋め込み済み）.md")

    replacements = [
        (
            "**【ここに図解①を挿入】**\n**寝る90分前ルール｜3ステップの全体像**",
            "![寝る90分前ルール｜3ステップの全体像](./images/図解①_寝る90分前ルール.png)"
        ),
        (
            "**【ここに図解②を挿入】**\n**睡眠不足が太りやすくする3つのメカニズム**",
            "![睡眠不足が太りやすくする3つのメカニズム](./images/図解②_睡眠不足メカニズム.png)"
        ),
        (
            "**【ここに図解③を挿入】**\n**就寝前の照明とメラトニンの関係（比較図）**",
            "![就寝前の照明とメラトニンの関係](./images/図解③_照明とメラトニン比較.png)"
        ),
        (
            "**【ここに図解④を挿入】**\n**「食を締める」実践フロー（歯磨きトリガー）**",
            "![「食を締める」実践フロー](./images/図解④_食を締める実践フロー.png)"
        ),
        (
            "**【ここに図解⑤を挿入】**\n**崩れた日の復帰フロー**",
            "![崩れた日の復帰フロー](./images/図解⑤_崩れた日の復帰フロー.png)"
        ),
    ]

    with open(article_path, encoding="utf-8") as f:
        content = f.read()

    for old, new in replacements:
        content = content.replace(old, new)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 画像埋め込み完了: {output_path}")


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("図解生成開始...\n")
    make_figure1()
    make_figure2()
    make_figure3()
    make_figure4()
    make_figure5()
    print("\n記事への画像埋め込み中...")
    embed_images_into_article()
    print(f"\n全工程完了!")
    print(f"保存先: {OUTPUT_DIR}")


