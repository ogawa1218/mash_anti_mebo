const fs = require("fs");
const path = require("path");
const { chromium } = require("C:/Users/masas/product/2nd-Brain/Health_app/node_modules/playwright");

const BASE_DIR = __dirname;
const IMAGES_DIR = path.join(BASE_DIR, "images");
const THUMB_DIR = path.join(IMAGES_DIR, "thumbnails");
const FIG_DIR = path.join(IMAGES_DIR, "note_figures");
const X_DIR = path.join(IMAGES_DIR, "x_posts");
const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const FONT_URL = "file:///C:/Windows/Fonts/NotoSansJP-VF.ttf";
const PORTRAIT = "C:/Users/masas/product/2nd-Brain/04_アウトプット/Longevity/note/Image/portrait_marcy.png";

for (const dir of [IMAGES_DIR, THUMB_DIR, FIG_DIR, X_DIR]) {
  fs.mkdirSync(dir, { recursive: true });
}

function portraitData() {
  if (!fs.existsSync(PORTRAIT)) return "";
  return "data:image/png;base64," + fs.readFileSync(PORTRAIT).toString("base64");
}

function writeHtml(dir, name, html) {
  fs.writeFileSync(path.join(dir, `${name}.html`), html, "utf8");
}

async function shot(browser, dir, name, html, viewport) {
  writeHtml(dir, name, html);
  const page = await browser.newPage({ viewport });
  await page.setContent(html, { waitUntil: "load" });
  await page.waitForTimeout(700);
  await page.screenshot({ path: path.join(dir, `${name}.png`) });
  await page.close();
}

function pageShell({ title, body, width = 1280, height = 670 }) {
  return `<!DOCTYPE html>
  <html><head><meta charset="UTF-8"><style>
  @font-face{font-family:'NJ';src:url('${FONT_URL}');font-weight:100 900;}
  *{margin:0;padding:0;box-sizing:border-box;}
  body{width:${width}px;height:${height}px;overflow:hidden;position:relative;background:#05080c;color:#fff;
  font-family:'NJ','Yu Gothic UI',sans-serif;}
  .bg{position:absolute;inset:0;background:
    radial-gradient(circle at 16% 18%,rgba(56,189,248,.18),transparent 28%),
    radial-gradient(circle at 82% 16%,rgba(255,109,0,.18),transparent 26%),
    linear-gradient(180deg,#08131c 0%,#05080c 100%);}
  .grid{position:absolute;inset:0;opacity:.06;background-image:
    linear-gradient(rgba(255,255,255,.08) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.08) 1px,transparent 1px);
    background-size:40px 40px;}
  .frame{position:absolute;inset:28px;border:1px solid rgba(255,255,255,.08);border-radius:28px;}
  .title{position:absolute;left:48px;top:42px;font-size:44px;font-weight:900;letter-spacing:-.03em;}
  .label{position:absolute;left:48px;top:18px;font-size:14px;font-weight:800;letter-spacing:.18em;color:#ff6d00;}
  .panel{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:24px;backdrop-filter:blur(12px);}
  .muted{color:#9ca3af}.orange{color:#ff6d00}.blue{color:#38bdf8}.green{color:#4ade80}
  .brand{position:absolute;right:44px;bottom:28px;font-size:16px;color:#9ca3af;}
  </style></head><body>
  <div class="bg"></div><div class="grid"></div><div class="frame"></div>
  <div class="label">MARCY CONTENT</div><div class="title">${title}</div>
  ${body}
  <div class="brand">マーシー｜第 卵朝食設計</div>
  </body></html>`;
}

function thumbHtml(v, portrait) {
  const portraitBlock = portrait
    ? `<div class="portrait-wrap"><img class="portrait-img" src="${portrait}"></div>`
    : "";
  return `<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
  @font-face{font-family:'NJ';src:url('${FONT_URL}');font-weight:100 900;}
  *{margin:0;padding:0;box-sizing:border-box;}
  body{width:1280px;height:670px;overflow:hidden;background:#000;position:relative;color:#fff;
  font-family:'NJ','Yu Gothic UI',sans-serif;}
  .bg{position:absolute;inset:0;background:
    radial-gradient(circle at 18% 18%,rgba(56,189,248,.16),transparent 28%),
    radial-gradient(circle at 78% 30%,rgba(255,109,0,.22),transparent 32%),
    linear-gradient(180deg,#050505 0%,#000 100%);}
  .grid{position:absolute;inset:0;opacity:.08;background-image:
    linear-gradient(rgba(255,255,255,.08) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.08) 1px,transparent 1px);background-size:48px 48px;}
  .accent{position:absolute;left:0;top:0;width:8px;height:100%;background:linear-gradient(180deg,#ff6d00 0%,#38bdf8 100%);}
  .wrap{position:absolute;left:74px;top:0;width:720px;height:100%;display:flex;flex-direction:column;justify-content:center;z-index:2;}
  .eyebrow{font-size:20px;font-weight:800;letter-spacing:.16em;color:#9ca3af;margin-bottom:18px;}
  .line1,.line2{font-size:60px;line-height:1.24;font-weight:800;letter-spacing:-.03em;}
  .line3{font-size:82px;line-height:1.14;font-weight:900;letter-spacing:-.04em;color:#ff6d00;text-shadow:0 0 36px rgba(255,109,0,.32);margin-top:12px;}
  .badge{position:absolute;top:42px;right:42px;border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:10px 16px;font-size:18px;font-weight:700;color:#d1d5db;background:rgba(255,255,255,.04);backdrop-filter:blur(10px);z-index:3;}
  .footer{position:absolute;left:52px;bottom:34px;z-index:3;}
  .footer-name{font-size:24px;font-weight:800;}.footer-sub{font-size:16px;color:#9ca3af;margin-top:4px;}
  .note{position:absolute;right:44px;bottom:32px;font-size:18px;color:#d1d5db;z-index:3;}
  .portrait-wrap{position:absolute;right:0;top:0;width:540px;height:100%;overflow:hidden;
    mask-image:linear-gradient(to right,transparent 0%,rgba(0,0,0,.35) 18%,black 42%,black 100%);}
  .portrait-img{width:100%;height:100%;object-fit:cover;object-position:center top;filter:contrast(1.05) brightness(.84) saturate(.9);}
  </style></head><body>
  <div class="bg"></div><div class="grid"></div><div class="accent"></div>${portraitBlock}
  <div class="badge">第15回｜朝食設計</div>
  <div class="wrap">
    <div class="eyebrow">EGG BREAKFAST</div>
    <div class="line1">${v.line1}</div>
    <div class="line2">${v.line2}</div>
    <div class="line3">${v.line3}</div>
  </div>
  <div class="footer"><div class="footer-name">マーシー</div><div class="footer-sub">100kg→68kg(-32kg)｜Sub3 Runner</div></div>
  <div class="note">意志力ではなく、仕組みで変える</div>
  </body></html>`;
}

function xCardHtml(card, index) {
  return `<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
  @font-face{font-family:'NJ';src:url('${FONT_URL}');font-weight:100 900;}
  *{margin:0;padding:0;box-sizing:border-box;}
  body{width:1280px;height:720px;overflow:hidden;background:#05080c;position:relative;color:#fff;
  font-family:'NJ','Yu Gothic UI',sans-serif;}
  .bg{position:absolute;inset:0;background:
    radial-gradient(circle at 15% 15%,rgba(56,189,248,.16),transparent 28%),
    radial-gradient(circle at 85% 20%,rgba(255,109,0,.16),transparent 24%),
    linear-gradient(180deg,#08131c 0%,#05080c 100%);}
  .grid{position:absolute;inset:0;opacity:.06;background-image:
    linear-gradient(rgba(255,255,255,.08) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.08) 1px,transparent 1px);background-size:44px 44px;}
  .edge{position:absolute;left:0;top:0;width:8px;height:100%;background:${card.accent};}
  .tag{position:absolute;left:60px;top:48px;padding:10px 16px;border-radius:999px;font-size:18px;font-weight:800;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.14);color:${card.accent};}
  .num{position:absolute;right:58px;top:52px;font-size:22px;font-weight:800;color:#9ca3af;}
  .title{position:absolute;left:60px;top:126px;width:1040px;font-size:62px;line-height:1.2;font-weight:900;letter-spacing:-.04em;}
  .body{position:absolute;left:60px;top:332px;width:1040px;font-size:30px;line-height:1.65;font-weight:700;color:#d1d5db;}
  .rule{position:absolute;left:60px;right:60px;bottom:118px;height:2px;background:linear-gradient(90deg,${card.accent},transparent);}
  .footer{position:absolute;left:60px;bottom:52px;font-size:22px;font-weight:800;}
  .footer span{color:${card.accent};}
  </style></head><body>
  <div class="bg"></div><div class="grid"></div><div class="edge"></div>
  <div class="tag">${card.kicker}</div><div class="num">${String(index).padStart(2, "0")}/10</div>
  <div class="title">${card.title.replace(/\n/g, "<br>")}</div>
  <div class="body">${card.body.replace(/\n/g, "<br>")}</div>
  <div class="rule"></div><div class="footer">マーシー <span>｜ 卵朝食で食欲設計</span></div>
  </body></html>`;
}

const thumbnails = [
  { suffix: "a", line1: "卵を先に食べると", line2: "本当に痩せるのか？", line3: "科学で検証" },
  { suffix: "b", line1: "朝の卵2〜3個で", line2: "10時の暴走は", line3: "止まるのか" },
  { suffix: "c", line1: "卵は痩せ薬じゃない", line2: "でも朝の食欲設計には", line3: "かなり強い" },
];

const figures = [
  {
    name: "figure_01_朝の卵が効く場所",
    title: "卵が効くのは、朝よりその後",
    body: `
      ${[
        ["7:00", "卵2〜3個を先に食べる", "#ff6d00"],
        ["10:00", "間食したさが下がりやすい", "#38bdf8"],
        ["12:00", "昼の主食を少し抑えやすい", "#4ade80"],
        ["15:00", "眠気・だるさが軽くなりやすい", "#38bdf8"],
        ["夜", "ドカ食いの入口を1段階小さくする", "#ff6d00"],
      ].map((it, idx) => `
        <div style="position:absolute;left:88px;top:${150 + idx * 78}px;display:flex;align-items:center;">
          <div class="panel" style="width:120px;height:56px;border-color:${it[2]}66;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:${it[2]};">${it[0]}</div>
          <div style="width:58px;height:4px;background:${it[2]};margin:0 18px;border-radius:999px;"></div>
          <div class="panel" style="width:760px;padding:16px 24px;font-size:28px;font-weight:800;">${it[1]}</div>
        </div>`).join("")}
        <div style="position:absolute;right:72px;top:164px;width:250px;" class="panel">
          <div style="padding:22px 20px;">
            <div style="font-size:18px;font-weight:800;color:#38bdf8;margin-bottom:10px;">研究の示唆</div>
            <div style="font-size:16px;line-height:1.7;color:#d1d5db;">卵朝食は昼前の満腹感を高め、昼食量を減らしやすい。<br>狙うのは“朝だけ”ではなく“その後の崩れ”。</div>
          </div>
        </div>`,
  },
  {
    name: "figure_02_言えること言えないこと",
    title: "卵朝食で、何が言えて何が言えないか",
    body: `
      <div style="position:absolute;left:64px;top:136px;width:540px;height:430px;" class="panel"><div style="padding:28px;">
      <div class="orange" style="font-size:26px;font-weight:900;margin-bottom:16px;">言えること</div>
      <div style="font-size:26px;line-height:1.75;font-weight:700;">・短期の満腹感は上がりやすい<br>・昼食量が下がる報告がある<br>・減量食と組み合わせると有利な可能性</div></div></div>
      <div style="position:absolute;right:64px;top:136px;width:540px;height:430px;" class="panel"><div style="padding:28px;">
      <div class="blue" style="font-size:26px;font-weight:900;margin-bottom:16px;">言えないこと</div>
      <div style="font-size:26px;line-height:1.75;font-weight:700;">・卵だけで脂肪が落ちる<br>・3個が万人に最適<br>・朝食を足せば必ず痩せる</div></div></div>
      <div style="position:absolute;left:120px;right:120px;bottom:68px;" class="panel"><div style="padding:18px 24px;font-size:24px;font-weight:800;text-align:center;">
      卵は <span class="orange">痩せ薬</span> ではない。<span class="blue">食欲設計ツール</span> として使う。</div></div>`,
  },
  {
    name: "figure_03_2個と3個の考え方",
    title: "エビデンスの中心は2個。3個は実務仮説",
    body: `
      <div style="position:absolute;left:76px;top:150px;width:500px;height:360px;" class="panel"><div style="padding:28px;">
      <div class="blue" style="font-size:30px;font-weight:900;margin-bottom:18px;">卵2個</div>
      <div style="font-size:24px;line-height:1.8;font-weight:700;">・研究の中心はこちら<br>・約12gのたんぱく質<br>・まず始めやすい<br>・LDLが気になる人にも入りやすい</div></div></div>
      <div style="position:absolute;right:76px;top:150px;width:500px;height:360px;" class="panel"><div style="padding:28px;">
      <div class="orange" style="font-size:30px;font-weight:900;margin-bottom:18px;">卵3個</div>
      <div style="font-size:24px;line-height:1.8;font-weight:700;">・約18gのたんぱく質<br>・10時に崩れやすい人向き<br>・体格が大きい人で試す価値<br>・重ければ2個＋汁物へ戻す</div></div></div>
      <div style="position:absolute;left:112px;right:112px;bottom:74px;text-align:center;font-size:28px;font-weight:900;">
      正解は固定ではない。<span class="green">10時の空腹</span>で判定する。</div>`,
  },
  {
    name: "figure_04_1週間プロトコル",
    title: "卵先食べ 1週間プロトコル",
    body: `
      ${[
        ["1", "朝いちで卵2個", "主食より先に入れる", "#ff6d00", 80, 150],
        ["2", "崩れるなら3個", "2個で昼前に空腹なら増やす", "#38bdf8", 640, 150],
        ["3", "味噌汁か無糖飲料", "満足感と再現性を補強", "#ff6d00", 80, 330],
        ["4", "4項目だけ記録", "間食欲・眠気・だるさ・続けやすさ", "#38bdf8", 640, 330],
      ].map((it) => `
        <div class="panel" style="position:absolute;left:${it[4]}px;top:${it[5]}px;width:500px;height:138px;border-color:${it[3]}55;">
          <div style="padding:22px 24px;display:flex;gap:16px;">
            <div style="width:56px;height:56px;border-radius:50%;background:${it[3]};display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:#000;">${it[0]}</div>
            <div><div style="font-size:28px;font-weight:900;line-height:1.3;">${it[1]}</div>
            <div class="muted" style="font-size:18px;line-height:1.6;margin-top:6px;">${it[2]}</div></div>
          </div>
        </div>`).join("")}
      <div style="position:absolute;left:160px;right:160px;bottom:58px;text-align:center;font-size:24px;font-weight:800;">
      1週間だけでいい。<span class="orange">ゼロか100</span>ではなく、<span class="green">翌日に再開</span>で判定する。</div>`,
  },
  {
    name: "figure_05_向いている人注意が必要な人",
    title: "卵先食べは誰に向くか",
    body: `
      <div style="position:absolute;left:76px;top:152px;width:500px;height:360px;" class="panel"><div style="padding:28px;">
      <div class="green" style="font-size:28px;font-weight:900;margin-bottom:16px;">向いている人</div>
      <div style="font-size:24px;line-height:1.8;font-weight:700;">・朝がパンだけになりやすい<br>・10時に間食したくなる<br>・昼にドカ食いしやすい<br>・朝の準備を固定したい</div></div></div>
      <div style="position:absolute;right:76px;top:152px;width:500px;height:360px;" class="panel"><div style="padding:28px;">
      <div class="orange" style="font-size:28px;font-weight:900;margin-bottom:16px;">注意が必要な人</div>
      <div style="font-size:24px;line-height:1.8;font-weight:700;">・LDLが高い<br>・脂質異常症で通院中<br>・糖尿病がある<br>・毎日3個固定にしたい人</div></div></div>
      <div style="position:absolute;left:120px;right:120px;bottom:66px;" class="panel"><div style="padding:20px 24px;text-align:center;font-size:22px;font-weight:800;">
      迷ったら <span class="blue">2個から</span>。通院中なら <span class="orange">主治医の指示を優先</span>。</div></div>`,
  },
];

const xCards = [
  { kicker: "共感", title: "崩れは夜じゃない。\n朝で仕込まれている。", body: "菓子パン → 10時に甘いもの → 昼大盛り → 夕方だるい → 夜ドカ食い。\nこの連鎖を切る候補が、朝の卵です。", accent: "#ff6d00" },
  { kicker: "研究", title: "卵朝食は、\n昼食量を下げやすい。", body: "過体重・肥満のRCTでは、ベーグル朝食より満腹感が高く、昼食摂取量が約160kcal少なかった。", accent: "#38bdf8" },
  { kicker: "重要", title: "でも、卵だけで\n痩せるわけじゃない。", body: "差が出るのは、卵をきっかけに1日の総摂取が整ったとき。卵は痩せ薬ではなく補助輪です。", accent: "#4ade80" },
  { kicker: "理由", title: "卵先食べが強いのは\n再現性が高いから。", body: "たんぱく質を入れやすい。判断が減る。コンビニでもできる。40代はこの3つが大きい。", accent: "#ff6d00" },
  { kicker: "個数", title: "研究の中心は2個。\n3個は実務案。", body: "2個で崩れる人だけ3個を試す。正解探しではなく、10時の空腹と昼の食べ過ぎ感で判定します。", accent: "#38bdf8" },
  { kicker: "判定", title: "見るべきは体重より\n10時の自分。", body: "間食したさ、昼食後の眠気、夕方のだるさ。体重より先に、食欲が変わるかを見ます。", accent: "#4ade80" },
  { kicker: "失敗", title: "卵を足しただけでは\n痩せない。", body: "朝に卵を追加して、昼も夜もそのままなら総量は増えるだけ。卵の価値は“その後”にあります。", accent: "#ff6d00" },
  { kicker: "成功", title: "卵の価値は\n1日の流れを変えること。", body: "昼の主食が少し減る。15時の間食が1回減る。夜のスタートが整う。これが勝ち筋です。", accent: "#38bdf8" },
  { kicker: "注意", title: "毎日3個固定で\n押し切らない。", body: "LDLが高い人、脂質異常症・糖尿病で通院中の人は主治医優先。健康習慣と自己流は別です。", accent: "#4ade80" },
  { kicker: "行動", title: "今夜やることは1つ。\n6個だけ茹でる。", body: "全部変えなくていい。卵を1パック買って、まず6個だけ準備する。朝の最初の1手だけ変えればいい。", accent: "#ff6d00" },
];

async function main() {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const portrait = portraitData();

  for (const v of thumbnails) {
    await shot(browser, THUMB_DIR, `thumbnail_${v.suffix}`, thumbHtml(v, portrait), { width: 1280, height: 670 });
  }

  for (const fig of figures) {
    await shot(browser, FIG_DIR, fig.name, pageShell({ title: fig.title, body: fig.body }), { width: 1280, height: 670 });
  }

  for (let i = 0; i < xCards.length; i += 1) {
    await shot(browser, X_DIR, `x_card_${String(i + 1).padStart(2, "0")}`, xCardHtml(xCards[i], i + 1), { width: 1280, height: 720 });
  }

  await browser.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});


