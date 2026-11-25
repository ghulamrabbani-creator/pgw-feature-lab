#!/usr/bin/env python3
"""Build the Lab search index (assets/search-index.js).

Run from the repo root after any page or doc change:
    python3 tools/build_search_index.py

What it does:
1. Makes sure every page loads assets/search.js (idempotent).
2. Gives an id to every static h2-h4 that has none, so results can jump to it (idempotent).
3. Opens each page in headless Chrome (file://) so content built by JavaScript is indexed too,
   and records one entry per section (heading + text until the next heading) and one entry
   per "try it" scenario link (#try=...).

Needs: playwright (Python) and Chrome at /usr/bin/google-chrome (or set CHROME).
"""
import asyncio, json, os, re, html as htmlmod
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEATURES = {"split-payout": "Split Payout", "mcp": "MCP", "direct-debit": "Direct Debit",
            "network-tokenization": "Network Tokenization", "pay-by-bank": "Pay by Bank"}
SKIP_DIRS = {"preview", "tools", "assets", ".git", "node_modules"}


def pages():
    out = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS:
            continue
        out.append(rel)
    return out


def slug(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = htmlmod.unescape(t).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60] or "section"


def ensure_script_and_ids(rel):
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    changed = False
    depth = len(rel.parts) - 1
    tag = f'<script src="{"../" * depth}assets/search.js" defer></script>'
    if "assets/search.js" not in s:
        s = s.replace("</body>", tag + "\n</body>", 1)
        changed = True
    # ids on static headings (outside <script>)
    scripts = [(m.start(), m.end()) for m in re.finditer(r"<script\b.*?</script>", s, re.S)]
    in_script = lambda i: any(a <= i < b for a, b in scripts)
    used = set(re.findall(r'\bid="([^"]+)"', s))
    out, last = [], 0
    for m in re.finditer(r"<h([2-4])(\s[^>]*)?>(.*?)</h\1>", s, re.S):
        attrs = m.group(2) or ""
        if in_script(m.start()) or re.search(r"\bid=", attrs) or "${" in m.group(0):
            continue
        base = slug(m.group(3))
        hid, n = base, 2
        while hid in used:
            hid, n = f"{base}-{n}", n + 1
        used.add(hid)
        out.append(s[last:m.start()])
        out.append(f'<h{m.group(1)} id="{hid}"{attrs}>{m.group(3)}</h{m.group(1)}>')
        last = m.end()
        changed = True
    if out:
        out.append(s[last:])
        s = "".join(out)
    if changed:
        p.write_text(s, encoding="utf-8")


EXTRACT = r"""
() => {
  const SKIP = 'script,style,noscript,header.lab-header,.toc,footer,.lab-footer,#lab-search,template';
  const root = document.querySelector('main') || document.body;
  const h1 = document.querySelector('h1');
  const pageTitle = (h1 ? h1.innerText : document.title).trim();
  const secs = [];
  let cur = { h: pageTitle, id: '', lvl: 1, x: [] };
  secs.push(cur);
  let lastId = '';
  const stack = [];
  const anchorOf = el => {
    if (el.id) return el.id;
    const a = el.closest('[id]');
    if (a && a !== root && a.tagName !== 'MAIN' && a.tagName !== 'BODY') return a.id;
    return lastId;
  };
  const walk = el => {
    for (const n of el.childNodes) {
      if (n.nodeType === 3) { const t = n.textContent.replace(/\s+/g, ' ').trim(); if (t) cur.x.push(t); continue; }
      if (n.nodeType !== 1) continue;
      if (n.matches(SKIP)) continue;
      if (/^H[1-4]$/.test(n.tagName) && n !== h1) {
        const id = anchorOf(n);
        if (id) lastId = id;
        const lvl = +n.tagName[1], h = n.innerText.replace(/\s+/g, ' ').trim();
        while (stack.length && stack[stack.length - 1].lvl >= lvl) stack.pop();
        const parent = stack.length ? stack[stack.length - 1].h : '';
        stack.push({ lvl, h });
        cur = { h, id, lvl, parent, x: [] };
        secs.push(cur);
        continue;
      }
      walk(n);
    }
  };
  walk(root);
  const tries = [...document.querySelectorAll('a[href^="#try="]')].map(a => ({ t: a.innerText.replace(/\s+/g,' ').trim(), href: a.getAttribute('href'), title: a.getAttribute('title') || '' }));
  return { pageTitle, title: document.title, secs: secs.map(s => ({ h: s.h, id: s.id, lvl: s.lvl, parent: s.parent || '', x: s.x.join(' ') })), tries };
}
"""


async def render_all(rels):
    from playwright.async_api import async_playwright
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROME", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        ctx = await b.new_context(viewport={"width": 1366, "height": 900})
        await ctx.route(re.compile(r"^https?://"), lambda r: r.abort())
        for rel in rels:
            pg = await ctx.new_page()
            await pg.goto((ROOT / rel).as_uri())
            await pg.wait_for_timeout(250)
            res[rel] = await pg.evaluate(EXTRACT)
            await pg.close()
        await b.close()
    return res


def kind_of(rel):
    if "docs" in rel.parts:
        return "Document"
    if rel.name == "index.html":
        return "Hub"
    return "Visual page"


def main():
    rels = [r for r in pages() if str(r) != "index.html"]
    for r in rels:
        ensure_script_and_ids(r)
    ensure_script_and_ids(Path("index.html"))
    data = asyncio.run(render_all(rels))
    entries = []
    for rel, d in data.items():
        feat = FEATURES.get(rel.parts[0], "Lab")
        url = rel.as_posix()
        page = d["pageTitle"]
        kind = kind_of(rel)
        seen = set()
        for s in d["secs"]:
            text = s["x"][:4000]
            if not s["h"] and not text:
                continue
            key = (s["h"], s["id"])
            if key in seen and not text:
                continue
            seen.add(key)
            u = url + ("#" + s["id"] if s["id"] else "")
            ctx = page + (" › " + s["parent"][:70] if s.get("parent") else "")
            entries.append([feat, ctx, kind, s["h"] or page, u, text])
        tseen = set()
        for t in d["tries"]:
            if not t["t"] or t["href"] in tseen:
                continue
            tseen.add(t["href"])
            entries.append([feat, page, "Scenario", "Try it: " + t["t"], url + t["href"], t["title"]])
    out = {"built": date.today().isoformat(), "fields": ["feature", "page", "kind", "heading", "url", "text"], "e": entries}
    f = ROOT / "assets" / "search-index.js"
    f.write_text("window.__labSearchIndex=" + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"{len(entries)} entries from {len(rels)} pages, {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
