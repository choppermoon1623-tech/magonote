# -*- coding: utf-8 -*-
"""manual-src-*.md を読み、孫の手デザインの説明書 manual.html を生成する"""
import io, os, re, html

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SRC, "..", "manual.html")   # このフォルダの1つ上（リポジトリ直下）に出力

# 表示順・アイコン・URL（ポータルと同じ）
CATS = [
    ("📄", "書類・PDF", [
        ("📄", "PDFツール", "pdf-tool"),
        ("🧾", "プリントスキャナー", "print-scanner"),
        ("🏆", "差し込み印刷", "mail-merge"),
        ("📝", "テキスト整形", "text-formatter"),
        ("🈷️", "ふりがな付け", "furigana"),
        ("📖", "面付け・小冊子", "booklet-maker"),
    ]),
    ("🖼️", "画像", [
        ("🔄", "画像形式変換", "image-convert"),
        ("📐", "写真リサイザー", "photo-resizer"),
        ("🪪", "証明写真メーカー", "id-photo"),
        ("🙈", "顔モザイク", "face-mosaic"),
    ]),
    ("🗂️", "ファイル整理", [
        ("🏷️", "一括リネーム", "file-renamer"),
    ]),
    ("🔗", "QR・共有", [
        ("🔳", "QRコード工房", "qr-studio"),
    ]),
    ("🎵", "音声", [
        ("🎙️", "オーディオスタジオ", "audio-studio"),
    ]),
    ("🏫", "教室・進行", [
        ("⏱️", "大型タイマー", "big-timer"),
        ("🎯", "ランダム指名ルーレット", "name-roulette"),
        ("✅", "QR提出チェック", "submit-check"),
        ("🧩", "班分けメーカー", "group-maker"),
        ("🪑", "席替えメーカー", "seat-maker"),
        ("🧹", "当番表メーカー", "toban-maker"),
        ("🏆", "トーナメント・対戦表", "tournament-maker"),
        ("🗓️", "週時間割メーカー", "jikanwari-maker"),
    ]),
]
BASE = "https://choppermoon1623-tech.github.io/"

# ---- md 読み込み ----
def parse_md(path, store):
    cur = None; mode = None
    for raw in io.open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if line.startswith("## "):
            cur = line[3:].strip()
            store[cur] = {"lede": "", "steps": [], "feat": [], "note": []}
            mode = None
        elif cur is None:
            continue
        elif line.startswith("**ひとこと:**"):
            store[cur]["lede"] = line.split("**ひとこと:**", 1)[1].strip()
        elif line.startswith("**使い方:**"):
            mode = "steps"
        elif line.startswith("**便利機能:**"):
            mode = "feat"
        elif line.startswith("**注意・コツ:**"):
            mode = "note"
        elif re.match(r"^\d+\.\s", line) and mode == "steps":
            store[cur]["steps"].append(re.sub(r"^\d+\.\s*", "", line).strip())
        elif line.startswith("- ") and mode in ("feat", "note"):
            store[cur][mode].append(line[2:].strip())
    return store

apps = {}
for f in ["manual-src-a.md", "manual-src-b.md", "manual-src-c.md", "manual-src-d.md", "manual-src-e.md"]:
    parse_md(os.path.join(SRC, f), apps)

def e(s):
    return html.escape(s, quote=False)

# 「」内のUIラベルを強調
def fmt(s):
    s = e(s)
    return re.sub(r"「([^」]+)」", r"「<b class=\"ui\">\1</b>」", s)

# ---- 検証: 全アプリ分あるか ----
missing = []
for _, _, items in CATS:
    for _, name, _ in items:
        if name not in apps:
            missing.append(name)
if missing:
    raise SystemExit("MISSING: " + ", ".join(missing))

# ---- HTML 生成 ----
toc_parts = []
body_parts = []
for cic, cname, items in CATS:
    links = "".join(
        f'<a href="#{slug}">{ic} {e(name)}</a>' for ic, name, slug in items
    )
    toc_parts.append(f'<div class="toc-cat"><span class="toc-h">{cic} {e(cname)}</span>{links}</div>')

    arts = []
    for ic, name, slug in items:
        d = apps[name]
        steps = "".join(f"<li>{fmt(s)}</li>" for s in d["steps"])
        feat = "".join(f"<li>{fmt(s)}</li>" for s in d["feat"])
        note = "".join(f"<li>{fmt(s)}</li>" for s in d["note"])
        arts.append(f"""
    <article class="app" id="{slug}" data-app>
      <h3><span class="ic">{ic}</span>{e(name)}
        <a class="open" href="{BASE}{slug}/" target="_blank" rel="noopener">アプリを開く ↗</a></h3>
      <p class="lede">{fmt(d["lede"])}</p>
      <div class="cols">
        <div>
          <h4>🔰 使い方</h4>
          <ol>{steps}</ol>
        </div>
        <div>
          <h4>✨ 便利機能</h4>
          <ul class="feat">{feat}</ul>
          <h4>⚠️ 注意・コツ</h4>
          <ul class="note">{note}</ul>
        </div>
      </div>
    </article>""")
    body_parts.append(f"""
  <section class="cat" data-cat>
    <h2 id="cat-{cname}">{cic} {e(cname)} <span class="n"></span></h2>
    {''.join(arts)}
  </section>""")

TOC = "".join(toc_parts)
BODY = "".join(body_parts)

page = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>孫の手 説明書</title>
<style>
  :root{
    --bg:#101418; --panel:#1a2129; --panel2:#202a35; --line:rgba(255,255,255,.08);
    --text:#e8eef2; --muted:#8fa3af; --accent:#c8a35a; --accent2:#7fc4a0; --warn:#e0b96a;
    --jp:"Zen Kaku Gothic New","Hiragino Kaku Gothic ProN","Yu Gothic",-apple-system,sans-serif;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:var(--jp);background:var(--bg);color:var(--text);line-height:1.75;min-height:100vh}
  .wrap{max-width:1000px;margin:0 auto;padding:36px 20px 60px}

  header{display:flex;align-items:flex-start;gap:16px;flex-wrap:wrap}
  header .mark{font-size:44px;line-height:1}
  header h1{font-size:clamp(24px,5vw,34px);font-weight:900;letter-spacing:.02em}
  header h1 span{color:var(--accent)}
  header .lead{color:var(--muted);font-size:13.5px;margin-top:3px}
  .backlink{margin-left:auto;align-self:center}
  .backlink a{color:var(--accent2);text-decoration:none;font-size:13px;border:1px solid var(--line);
    background:var(--panel);padding:8px 14px;border-radius:999px;display:inline-block}
  .backlink a:hover{border-color:var(--accent2)}

  .common{margin-top:18px;background:var(--panel);border:1px solid var(--line);
    border-left:3px solid var(--accent);border-radius:12px;padding:14px 18px;font-size:13.5px}
  .common b{color:var(--accent2)}
  .common ul{margin:6px 0 0 1.3em}

  .searchbar{margin:20px 0 4px}
  .searchbar input{width:100%;padding:12px 16px;font-size:15px;font-family:var(--jp);
    background:var(--panel);color:var(--text);border:1px solid var(--line);border-radius:12px;outline:none}
  .searchbar input:focus{border-color:var(--accent2)}

  .toc{margin-top:16px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:12.5px}
  .toc-cat{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline;padding:3px 0}
  .toc-h{color:var(--muted);font-weight:700;min-width:8.5em}
  .toc a{color:var(--accent2);text-decoration:none;white-space:nowrap}
  .toc a:hover{text-decoration:underline}

  .cat{margin-top:30px}
  .cat h2{font-size:17px;font-weight:900;display:flex;align-items:center;gap:10px}
  .cat h2 .n{font-size:11px;font-weight:700;color:var(--muted);background:var(--panel2);
    padding:2px 10px;border-radius:999px;border:1px solid var(--line)}
  .cat h2::after{content:"";flex:1;height:1px;background:var(--line)}

  article.app{background:var(--panel);border:1px solid var(--line);border-radius:14px;
    padding:18px 20px 16px;margin-top:14px;scroll-margin-top:14px}
  article.app h3{font-size:16.5px;font-weight:900;display:flex;align-items:center;gap:9px;flex-wrap:wrap}
  article.app h3 .ic{font-size:21px}
  article.app h3 .open{margin-left:auto;font-size:12px;font-weight:700;color:var(--accent);
    text-decoration:none;border:1px solid rgba(200,163,90,.4);padding:4px 12px;border-radius:999px}
  article.app h3 .open:hover{background:rgba(200,163,90,.12)}
  .lede{color:var(--muted);font-size:13px;margin-top:6px}
  .cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 26px;margin-top:12px}
  @media(max-width:760px){.cols{grid-template-columns:1fr}}
  article.app h4{font-size:12.5px;font-weight:900;color:var(--accent);margin:10px 0 5px;letter-spacing:.04em}
  article.app ol{margin-left:1.4em;font-size:13px}
  article.app ol li{margin:5px 0}
  article.app ul{margin-left:1.3em;font-size:12.5px;list-style:none}
  article.app ul li{margin:5px 0;position:relative;padding-left:2px}
  article.app ul.feat li::before{content:"✔";color:var(--accent2);position:absolute;left:-1.2em}
  article.app ul.note{color:#d9cba8}
  article.app ul.note li::before{content:"！";color:var(--warn);font-weight:900;position:absolute;left:-1.2em}
  b.ui{color:var(--accent2);font-weight:700}

  .hidden{display:none}
  .empty{color:var(--muted);font-size:13px;padding:20px 4px;display:none}
  .empty.show{display:block}
  .totop{position:fixed;right:18px;bottom:18px;background:var(--panel2);border:1px solid var(--line);
    color:var(--text);border-radius:999px;padding:9px 14px;font-size:13px;text-decoration:none}
  .totop:hover{border-color:var(--accent)}

  footer{margin-top:44px;border-top:1px solid var(--line);padding-top:18px;
    color:var(--muted);font-size:12px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
  footer a{color:var(--accent2);text-decoration:none}
  footer a:hover{text-decoration:underline}

  @media print{
    :root{--bg:#fff;--panel:#fff;--panel2:#f2f2f2;--line:#bbb;--text:#111;--muted:#555;
      --accent:#7a5c1e;--accent2:#1e6b4c;--warn:#8a6100}
    body{background:#fff;color:#111;font-size:11.5px}
    .searchbar,.toc,.totop,.backlink,header .lead{display:none !important}
    .wrap{max-width:none;padding:0}
    article.app{break-inside:avoid;border:1px solid #bbb;box-shadow:none;margin-top:10px;padding:12px 14px}
    article.app ul.note{color:#7a5c1e}
    .cat h2{break-after:avoid}
    a{color:inherit;text-decoration:none}
    article.app h3 .open{display:none}
  }
</style>
</head>
<body>
<div class="wrap">

  <header>
    <div class="mark">🖐️</div>
    <div>
      <h1>孫の手 <span>説明書</span></h1>
      <div class="lead">収録アプリの使い方ガイド（印刷して職員室に置いても使えます）</div>
    </div>
    <div class="backlink"><a href="./">← 孫の手トップへ</a></div>
  </header>

  <div class="common">
    <b>全アプリ共通のこと</b>
    <ul>
      <li>どれも<b>ブラウザだけで動き、ファイルや名簿が端末の外に送信されることはありません</b>。インストール・会員登録も不要です。</li>
      <li>入力内容の自動保存は「そのパソコンの・そのブラウザの中」に記憶されます。別のPCには引き継がれないので、大事なデータは各アプリの保存機能でファイルに残してください。</li>
      <li>推奨ブラウザは <b>Chrome / Edge</b> です（一部機能はこの2つでのみ動きます）。</li>
      <li>印刷がずれるときは、印刷画面で「余白：なし」「倍率：100%」になっているか確認してください。</li>
    </ul>
  </div>

  <div class="searchbar">
    <input id="q" type="search" placeholder="🔍 アプリ名・やりたいことで探す（例：ふりがな、ZIP、印刷）">
  </div>

  <nav class="toc">__TOC__</nav>

__BODY__

  <div class="empty" id="empty">該当する説明が見つかりませんでした。</div>

  <a class="totop" href="#top" onclick="window.scrollTo({top:0,behavior:'smooth'});return false;">↑ 上へ</a>

  <footer>
    <span>孫の手 ／ H.M Works</span>
    <a href="./">🖐️ 孫の手トップへ →</a>
  </footer>
</div>

<script>
(function(){
  document.querySelectorAll('[data-cat]').forEach(sec => {
    sec.querySelector('.n').textContent = sec.querySelectorAll('article.app').length + 'アプリ';
  });
  const q = document.getElementById('q'), empty = document.getElementById('empty');
  q.addEventListener('input', () => {
    const t = q.value.trim().toLowerCase();
    let hit = 0;
    document.querySelectorAll('[data-cat]').forEach(sec => {
      let n = 0;
      sec.querySelectorAll('article.app').forEach(c => {
        const show = !t || c.textContent.toLowerCase().indexOf(t) >= 0;
        c.classList.toggle('hidden', !show);
        if(show) n++;
      });
      sec.classList.toggle('hidden', n === 0);
      hit += n;
    });
    empty.classList.toggle('show', hit === 0);
  });
})();
</script>
</body>
</html>
"""
page = page.replace("__TOC__", TOC).replace("__BODY__", BODY)
io.open(OUT, "w", encoding="utf-8", newline="\n").write(page)
print("OK", OUT, len(page), "chars,", sum(len(v["steps"]) for v in apps.values()), "steps,", len(apps), "apps")
