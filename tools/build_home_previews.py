#!/usr/bin/env python3
"""Build the three home-page options for the T002 redesign review.

Content is defined once here; each option only changes fonts, colours,
layout details and the hero visual. Output: preview/index-<option>.html
and preview/index.html (chooser). Run from the repo root.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "preview"

# ---------------------------------------------------------------- content
# aud: e = engineering, b = business & ops
LIVE = [
    {
        "id": "split-payout", "name": "Split Payout", "href": "../split-payout/",
        "status": ("pass", "Lab section complete"),
        "meta": "MVP · in build",
        "line": "One partner order, paid out to the partner and its vendors from one transaction.",
        "counts": "7 visual pages · 2 documents",
        "systems": ["PGW", "APEX", "MA", "Merchant Portal"],
        "docs": [
            ("Product document", "v1.6", "../split-payout/docs/product.html", "eb"),
            ("PGW dev stories", "v0.5", "../split-payout/docs/stories.html", "e"),
        ],
        "pages": [
            ("End-to-end view", "../split-payout/end-to-end.html", "eb"),
            ("Money flow", "../split-payout/money-flow.html", "b"),
            ("Onboarding", "../split-payout/onboarding.html", "b"),
            ("Split modes", "../split-payout/split-modes.html", "eb"),
            ("Config & Payment Simulator", "../split-payout/simulator.html", "e"),
            ("Advice lifecycle", "../split-payout/advice-lifecycle.html", "e"),
            ("What can go wrong", "../split-payout/what-can-go-wrong.html", "eb"),
        ],
        "planned": "",
    },
    {
        "id": "mcp", "name": "MCP", "href": "../mcp/",
        "status": ("released", "In build · pages added as docs land"),
        "meta": "Jan-2027 · in build",
        "line": "The customer pays on HPP in their own currency; the merchant stays in AED.",
        "counts": "3 visual pages · 2 documents (drafts)",
        "systems": ["PGW", "HPP", "MA", "APEX", "Planet"],
        "docs": [
            ("Solution requirements", "v3.0", "../mcp/docs/requirements.html", "eb"),
            ("PGW dev stories", "v0.1", "../mcp/docs/stories.html", "e"),
        ],
        "pages": [
            ("End-to-end view", "../mcp/end-to-end.html", "eb"),
            ("HPP simulator", "../mcp/hpp-simulator.html", "eb"),
            ("Calculator", "../mcp/calculator.html", "e"),
        ],
        "planned": "Planned: Order model, Rate file lifecycle, What can go wrong. Parked: Federation and enrichment.",
    },
]

COMING = [
    ("Pay by Bank", "Account-to-account payment through Lean (Open Finance); the customer approves in their bank app.",
     ["PGW", "APEX", "MA", "Merchant Portal", "Lean (new)"]),
    ("Direct Debit", "Recurring bank-to-bank collections through the UAE Direct Debit Marketplace (DDS).",
     ["DD Backend (new)", "DDS", "Merchant Portal", "APEX", "MA", "PGW config"]),
    ("Network Tokenization", "Repeat and merchant-initiated card payments sent with the scheme token.",
     ["PGW", "MA config", "MPGS", "CyberSource"]),
]

LENSES = [
    ("Visual flows", "Swimlanes, money flows and lifecycles. Switch the settings and the flow redraws.", "eb"),
    ("Simulators", "Try a scenario and see each check, decision and record. Marked Illustrative; numbers are fictional.", "e"),
    ("Documents and stories", "The reference. Published from the final .docx; headings carry buttons to the matching visual page.", "eb"),
]

STATES = [
    ("pass", "Pass / money moving", "check"),
    ("released", "Released / kept by Geidea", "arrow"),
    ("held", "Held at APEX", "pause"),
    ("rejected", "Rejected", "cross"),
    ("undef", "Not defined / waiting", "query"),
]

NEWS = [
    ("25-Nov-2026", "MCP", "Solution requirements v3.0 and PGW stories v0.1 published, with buttons to the visual pages", "../mcp/docs/requirements.html"),
    ("25-Nov-2026", "MCP", "Calculator: quote rounded up, refund planner with the last-cent rule", "../mcp/calculator.html"),
    ("25-Nov-2026", "MCP", "End-to-end view: rate file, HPP offer, payment, clearing, settlement and refunds in one swimlane", "../mcp/end-to-end.html"),
    ("24-Nov-2026", "MCP", "Section opened: hub page and HPP simulator", "../mcp/hpp-simulator.html"),
    ("24-Nov-2026", "Split Payout", "Rule of 24-Nov: an UPDATE is accepted on the transaction date only", "../split-payout/advice-lifecycle.html"),
    ("24-Nov-2026", "Split Payout", "Updates reach APEX only through the day-end file (APEX alignment of 23-Nov)", "../split-payout/end-to-end.html"),
    ("24-Nov-2026", "Split Payout", "End-to-end view, Advice lifecycle and What can go wrong added; story and page links both ways", "../split-payout/end-to-end.html"),
    ("24-Nov-2026", "Split Payout", "Onboarding swimlane and Split modes added", "../split-payout/onboarding.html"),
]

AUD_LABEL = {"e": "Eng", "b": "Biz & Ops"}

ICONS = {
    "check": '<path d="M3 8.5l3 3 7-7" />',
    "arrow": '<path d="M3 8h10M9 4l4 4-4 4" />',
    "pause": '<path d="M5.5 3.5v9M10.5 3.5v9" />',
    "cross": '<path d="M4 4l8 8M12 4l-8 8" />',
    "query": '<path d="M5.5 6a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5v.4M8 12.6v.2" />',
}


def esc(s):
    return html.escape(s, quote=True)


def icon(name):
    return (f'<svg class="ic" viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def chip(state, text):
    ic = dict((s, i) for s, _, i in STATES)[state]
    return f'<span class="st st-{state}">{icon(ic)}{esc(text)}</span>'


def aud_tags(aud):
    return "".join(f'<span class="aud aud-{a}">{AUD_LABEL[a]}</span>' for a in aud)


def entry(label, href, aud, extra=""):
    return (f'<li class="ep" data-aud="{aud}"><a href="{esc(href)}">{esc(label)}</a>'
            f'{extra}<span class="auds">{aud_tags(aud)}</span></li>')


def feature_card(f):
    docs = "".join(entry(l, h, a, f'<span class="ver">{esc(v)}</span>') for l, v, h, a in f["docs"])
    pages = "".join(entry(l, h, a) for l, h, a in f["pages"])
    planned = f'<p class="planned">{esc(f["planned"])}</p>' if f["planned"] else ""
    systems = "".join(f"<li>{esc(s)}</li>" for s in f["systems"])
    return f"""<article class="feat" id="f-{f['id']}">
<div class="feat-head">
<div><p class="feat-meta">{esc(f['meta'])}</p><h3><a href="{f['href']}">{esc(f['name'])}</a></h3></div>
{chip(*f['status'])}
</div>
<p class="feat-line">{esc(f['line'])}</p>
<p class="feat-count">{esc(f['counts'])}</p>
<div class="feat-cols">
<div><h4>Documents</h4><ul class="eps">{docs}</ul></div>
<div><h4>Visual pages</h4><ul class="eps">{pages}</ul>{planned}</div>
</div>
<div class="feat-foot"><span class="lbl">Systems</span><ul class="sys">{systems}</ul>
<a class="open" href="{f['href']}">Open {esc(f['name'])} hub {icon('arrow')}</a></div>
</article>"""


def coming_card(name, line, systems):
    sys_ = "".join(f"<li>{esc(s)}</li>" for s in systems)
    return f"""<article class="soon">
<div class="soon-head"><h3>{esc(name)}</h3>{chip('undef', 'Not in the Lab yet')}</div>
<p>{esc(line)}</p>
<div class="feat-foot"><span class="lbl">Systems touched</span><ul class="sys">{sys_}</ul></div>
</article>"""


def body(hero_visual, numbered):
    n = (lambda i: f'<span class="num">0{i}</span>') if numbered else (lambda i: "")
    live = "\n".join(feature_card(f) for f in LIVE)
    coming = "\n".join(coming_card(*c) for c in COMING)
    lenses = "".join(f'<li class="lens" data-aud="{a}"><h3>{esc(t)}</h3><p>{esc(d)}</p><span class="auds">{aud_tags(a)}</span></li>'
                     for t, d, a in LENSES)
    states = "".join(f"<li>{chip(s, t)}</li>" for s, t, _ in STATES)
    news = "".join(f'<tr><td class="d">{esc(d)}</td><td class="f">{esc(f)}</td><td><a href="{esc(h)}">{esc(u)}</a></td></tr>'
                   for d, f, u, h in NEWS)
    return f"""<header class="hdr"><div class="inner">
<a class="brand" href="../"><span>pgw/</span>Feature Lab</a>
<nav class="nav" aria-label="Sections"><a href="#live">Features</a><a href="#coming">Coming</a><a href="#read">How to read</a><a href="#new">What's new</a></nav>
<div class="lens-sw" role="group" aria-label="Audience lens">
<span class="lens-lbl">Lens</span>
<button type="button" data-lens="all" aria-pressed="true">All</button>
<button type="button" data-lens="e" aria-pressed="false">Engineering</button>
<button type="button" data-lens="b" aria-pressed="false">Business &amp; Ops</button>
</div>
</div></header>
<p class="lens-note" id="lens-note" aria-live="polite" hidden></p>
<main>
<section class="hero"><div class="inner">
<div class="hero-copy">
<p class="eyebrow">payment gateway · new features</p>
<h1>How new PGW features work, end to end</h1>
<p class="lead">Each feature has its documents and visual pages: flows, simulators and scenarios that show the configuration, the calls between systems and what can go wrong. The documents are the reference; the visual pages illustrate them.</p>
<ul class="hero-stats"><li><b>2</b> features live</li><li><b>10</b> visual pages</li><li><b>4</b> documents</li><li><b>3</b> coming</li></ul>
<p class="hero-cta"><a class="btn" href="#live">See the features</a><a class="btn ghost" href="#read">How to read this Lab</a></p>
</div>
<figure class="hero-vis">{hero_visual}</figure>
</div></section>

<section class="sec" id="live"><div class="inner">
<h2>{n(1)}Live features</h2>
<p class="sec-lead">Use the lens at the top to highlight the best entry points for your role. Nothing is hidden.</p>
<div class="feats">{live}</div>
</div></section>

<section class="sec" id="coming"><div class="inner">
<h2>{n(2)}Coming to the Lab</h2>
<p class="sec-lead">Next features to be explained here. Systems from each feature's scope notes.</p>
<div class="soons">{coming}</div>
</div></section>

<section class="sec" id="read"><div class="inner">
<h2>{n(3)}How to read this Lab</h2>
<ol class="lenses">{lenses}</ol>
<h3 class="legend-t">Status legend</h3>
<p class="sec-lead">Every state has a colour, an icon, a word and a border style, so it reads without colour too.</p>
<ul class="legend">{states}</ul>
</div></section>

<section class="sec" id="new"><div class="inner">
<h2>{n(4)}What's new</h2>
<div class="tbl"><table><thead><tr><th>Date</th><th>Feature</th><th>Update</th></tr></thead><tbody>{news}</tbody></table></div>
</div></section>
</main>
<footer class="ftr"><div class="inner">Pages marked Illustrative use fictional numbers. The published documents are the reference.</div></footer>
<script>
(function () {{
  var btns = document.querySelectorAll('.lens-sw button');
  var note = document.getElementById('lens-note');
  var names = {{ e: 'Engineering', b: 'Business & Ops' }};
  function apply(l) {{
    document.body.setAttribute('data-lens', l);
    btns.forEach(function (b) {{ b.setAttribute('aria-pressed', b.dataset.lens === l ? 'true' : 'false'); }});
    document.querySelectorAll('[data-aud]').forEach(function (el) {{
      el.classList.toggle('hit', l !== 'all' && el.dataset.aud.indexOf(l) > -1);
      el.classList.toggle('dim', l !== 'all' && el.dataset.aud.indexOf(l) === -1);
    }});
    note.hidden = l === 'all';
    note.textContent = l === 'all' ? '' : 'Highlighting entry points for ' + names[l] + '. Everything else stays available.';
    try {{ localStorage.setItem('lab-lens', l); }} catch (e) {{}}
  }}
  btns.forEach(function (b) {{ b.addEventListener('click', function () {{ apply(b.dataset.lens); }}); }});
  var saved = 'all';
  try {{ saved = localStorage.getItem('lab-lens') || 'all'; }} catch (e) {{}}
  apply(['all', 'e', 'b'].indexOf(saved) > -1 ? saved : 'all');
  window.__home = {{ apply: apply }};
}})();
</script>"""


# ------------------------------------------------------------ shared CSS
BASE_CSS = """
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:120px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--body)}
a{color:var(--link)}
a:focus-visible,button:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
.inner{max-width:1440px;margin:0 auto;padding:0 24px}
.hdr{position:sticky;top:0;z-index:20}
.hdr .inner{display:flex;align-items:center;gap:20px;flex-wrap:wrap;padding-top:12px;padding-bottom:12px}
.brand{font-weight:600;text-decoration:none;white-space:nowrap}
.brand span{font-family:var(--mono);font-weight:400;margin-right:6px}
.nav{display:flex;gap:18px;font-size:14px;flex:1}
.nav a{text-decoration:none}
.lens-sw{display:flex;align-items:center;gap:4px;padding:3px;border-radius:999px}
.lens-lbl{font:12px var(--mono);padding:0 8px}
.lens-sw button{font:500 13px var(--body);border:0;border-radius:999px;padding:6px 12px;cursor:pointer;background:transparent;transition:background .2s,color .2s}
.lens-note{margin:0;padding:8px 24px;text-align:center;font-size:14px}
.hero .inner{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:48px;align-items:center;padding-top:56px;padding-bottom:56px}
.hero h1{margin:0 0 16px}
.eyebrow{font:13px var(--mono);margin:0 0 10px}
.lead{font-size:18px;max-width:640px;margin:0 0 24px}
.hero-stats{list-style:none;padding:0;margin:0 0 28px;display:flex;flex-wrap:wrap;gap:10px 24px;font-size:14px}
.hero-stats b{font:600 22px var(--head);margin-right:4px}
.hero-cta{display:flex;flex-wrap:wrap;gap:12px;margin:0}
.btn{display:inline-block;padding:10px 18px;text-decoration:none;font-weight:600;font-size:15px;transition:background .2s,border-color .2s}
.hero-vis{margin:0}
.hero-vis img,.hero-vis svg{display:block;width:100%;height:auto}
.hero-vis figcaption{font:12px var(--mono);margin-top:8px}
.sec .inner{padding-top:56px;padding-bottom:16px}
.sec h2{margin:0 0 6px}
.sec-lead{margin:0 0 24px;max-width:760px}
.feats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.feat{padding:24px;display:flex;flex-direction:column}
.feat-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap}
.feat-meta{font:12px var(--mono);margin:0}
.feat h3{margin:2px 0 0}
.feat h3 a{text-decoration:none;color:inherit}
.feat-line{margin:12px 0 4px}
.feat-count{font:13px var(--mono);margin:0 0 16px}
.feat-cols{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,3fr);gap:24px;flex:1}
.feat h4{font:600 12px var(--mono);text-transform:uppercase;letter-spacing:.06em;margin:0 0 6px}
.eps{list-style:none;margin:0;padding:0}
.ep{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:6px 8px;margin:0 -8px;border-radius:6px;transition:opacity .2s,background .2s}
.ep a{font-weight:500}
.ver{font:12px var(--mono)}
.auds{margin-left:auto;display:flex;gap:4px}
.aud{font:11px var(--mono);padding:1px 6px;border-radius:4px;white-space:nowrap}
.planned{font-size:13px;margin:10px 0 0}
.feat-foot{display:flex;align-items:center;flex-wrap:wrap;gap:8px 12px;margin-top:18px;padding-top:14px}
.lbl{font:12px var(--mono)}
.sys{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.sys li{font:12px var(--mono);padding:2px 8px}
.open{margin-left:auto;display:inline-flex;align-items:center;gap:6px;font-weight:600;font-size:14px;text-decoration:none}
.open .ic{width:14px;height:14px}
.soons{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.soon{padding:20px;display:flex;flex-direction:column}
.soon-head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap}
.soon h3{margin:0}
.soon p{margin:10px 0 0;flex:1}
.lenses{list-style:none;margin:0 0 32px;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;counter-reset:l}
.lens{padding:20px;position:relative;transition:opacity .2s}
.lens h3{margin:0 0 6px}
.lens p{margin:0 0 10px;font-size:15px}
.lens .auds{margin:0}
.legend-t{margin:0 0 4px}
.legend{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:10px}
.st{display:inline-flex;align-items:center;gap:6px;font:500 13px var(--body);padding:4px 10px;border-width:1.5px;border-style:solid;white-space:nowrap}
.st .ic{width:14px;height:14px;flex:none}
.tbl{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:15px}
th,td{text-align:left;padding:10px 12px;vertical-align:top}
td.d{font:13px var(--mono);white-space:nowrap}
td.f{white-space:nowrap;font-weight:500}
.ftr .inner{padding-top:40px;padding-bottom:40px;font-size:13px}
.dim{opacity:.45}
.dim:hover,.dim:focus-within{opacity:1}
@media (max-width:1100px){.feats{grid-template-columns:minmax(0,1fr)}.soons,.lenses{grid-template-columns:minmax(0,1fr)}}
@media (max-width:900px){.hero .inner{grid-template-columns:minmax(0,1fr);gap:32px;padding-top:36px}.nav{display:none}.lens-sw{margin-left:auto}}
@media (max-width:640px){.feat-cols{grid-template-columns:minmax(0,1fr)}.lens-lbl{display:none}.lens-sw button{padding:6px 9px;font-size:12px}
 .hdr .inner{gap:8px}.lens-sw{margin-left:0;width:100%;justify-content:space-between}
 table,thead,tbody,tr,th,td{display:block}thead{display:none}tr{padding:10px 0}td{padding:2px 0}td.d,td.f{display:inline-block;margin-right:10px}
 .feat,.soon,.lens{padding:18px}}
"""

# ---------------------------------------------------------- per option
THEMES = {}

THEMES["blueprint"] = dict(
    title="Blueprint",
    fonts="family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500",
    css="""
:root{--bg:#F8FAFC;--card:#fff;--ink:#0F172A;--text-2:#475569;--muted:#64748B;--border:#E2E8F0;--money:#0E7C66;--money-bg:#E6F4F1;
--link:#1D4ED8;--focus:#1D4ED8;--body:'IBM Plex Sans',system-ui,sans-serif;--head:'IBM Plex Sans',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace}
.hdr{background:var(--ink);color:#fff}.hdr a{color:#fff}.brand span{color:#A7F3D0}.nav a{color:#CBD5E1}.nav a:hover{color:#fff}
.lens-sw{background:#1E293B}.lens-lbl{color:#94A3B8}.lens-sw button{color:#CBD5E1}.lens-sw button[aria-pressed=true]{background:#A7F3D0;color:var(--ink)}
.lens-note{background:var(--money-bg);color:#0B5546}
.hero{background-image:linear-gradient(#E2E8F0 1px,transparent 1px),linear-gradient(90deg,#E2E8F0 1px,transparent 1px);background-size:32px 32px;background-color:#F8FAFC;border-bottom:1px solid var(--border)}
.hero h1{font-size:40px;line-height:1.15;font-weight:600}
.eyebrow{color:var(--money)}.lead{color:var(--text-2)}.hero-stats{color:var(--text-2)}.hero-stats b{color:var(--ink)}
.btn{background:var(--money);color:#fff;border-radius:8px;border:1px solid var(--money)}.btn:hover{background:#0B6655}
.btn.ghost{background:#fff;color:var(--ink);border-color:#CBD5E1}.btn.ghost:hover{border-color:var(--money)}
.hero-vis{background:#fff;border:1px solid var(--border);border-radius:12px;padding:16px}.hero-vis figcaption{color:var(--muted)}
.sec h2{font-size:24px;font-weight:600}.sec-lead{color:var(--text-2)}
.feat,.soon,.lens{background:var(--card);border:1px solid var(--border);border-radius:12px}
.feat{border-top:3px solid var(--money)}
.feat h3{font-size:22px;font-weight:600}.feat-meta,.feat-count,.ver,.lbl{color:var(--muted)}.feat-line{color:var(--text-2)}.feat h4{color:var(--muted)}
.ep a{color:var(--ink);text-decoration:none}.ep a:hover{color:var(--link);text-decoration:underline}
.ep.hit{background:var(--money-bg)}
.aud{background:#F1F5F9;color:#475569}.aud-e{background:#EEF2FF;color:#3730A3}.aud-b{background:#FEF3C7;color:#92400E}
.planned{color:var(--muted)}
.feat-foot{border-top:1px solid var(--border)}.sys li{background:#F1F5F9;color:#334155;border-radius:4px}.open{color:var(--money)}
.soon{border-style:dashed;border-color:#CBD5E1}.soon h3{font-size:18px;font-weight:600}.soon p{color:var(--text-2);font-size:15px}
.lens h3{font-size:17px;font-weight:600}.lens p{color:var(--text-2)}.lens.hit{border-color:var(--money)}
.legend-t{font-size:17px;font-weight:600}
.st{border-radius:6px}
.st-pass{color:#0B5E4E;background:#E6F4F1;border-color:#0E7C66}
.st-released{color:#334155;background:#F1F5F9;border-color:#64748B}
.st-held{color:#92400E;background:#FFF7ED;border-color:#B45309;border-style:double;border-width:3px}
.st-rejected{color:#991B1B;background:#FEF2F2;border-color:#B91C1C}
.st-undef{color:#92400E;background:#FEF3C7;border-color:#D97706;border-style:dashed}
.tbl{background:#fff;border:1px solid var(--border);border-radius:12px}
th{font:600 12px var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid var(--border);background:#F8FAFC}
td{border-top:1px solid var(--border)}td.d{color:var(--muted)}
.ftr{color:var(--muted)}
""",
    numbered=False,
    hero="svg",
)

THEMES["ledger"] = dict(
    title="Clearing Ledger",
    fonts="family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Plus+Jakarta+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500",
    css="""
:root{--bg:#FAF8F5;--card:#fff;--ink:#181A1F;--text-2:#4E5460;--accent:#0F6E58;--rule:#E4DDD1;--link:#0F6E58;--focus:#0F6E58;
--body:'Plus Jakarta Sans',system-ui,sans-serif;--head:'Newsreader',Georgia,serif;--mono:'IBM Plex Mono',ui-monospace,monospace}
.hdr{background:rgba(250,248,245,.96);border-bottom:1px solid var(--ink);backdrop-filter:blur(6px)}
.brand{color:var(--ink);font-family:var(--head);font-size:20px;font-weight:600}.brand span{font-family:var(--mono);font-size:14px;color:var(--accent)}
.nav a{color:var(--text-2)}.nav a:hover{color:var(--ink);text-decoration:underline}
.lens-sw{border:1px solid var(--rule);background:#fff}.lens-lbl{color:var(--text-2)}.lens-sw button{color:var(--text-2)}
.lens-sw button[aria-pressed=true]{background:var(--ink);color:#fff}
.lens-note{background:#EEF5F2;color:#0B4F40;border-bottom:1px solid var(--rule)}
h1,h2,h3{font-family:var(--head);font-weight:600;letter-spacing:-.01em}
.hero{border-bottom:1px solid var(--rule)}
.hero h1{font-size:52px;line-height:1.05;font-weight:500}
.eyebrow{color:var(--accent);text-transform:uppercase;letter-spacing:.12em;font-size:12px}
.lead{color:var(--text-2)}
.hero-stats{border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:12px 0;color:var(--text-2)}
.hero-stats b{font-family:var(--head);color:var(--ink);font-size:26px;font-weight:500}
.btn{background:var(--ink);color:#fff;border:1px solid var(--ink);border-radius:2px}.btn:hover{background:var(--accent);border-color:var(--accent)}
.btn.ghost{background:transparent;color:var(--ink)}.btn.ghost:hover{background:#fff;border-color:var(--accent);color:var(--accent)}
.hero-vis figcaption{color:var(--text-2)}
.sec h2{font-size:34px;font-weight:500;border-bottom:1px solid var(--ink);padding-bottom:10px;margin-bottom:12px;display:flex;align-items:baseline;gap:14px}
.num{font:500 14px var(--mono);color:var(--accent)}
.sec-lead{color:var(--text-2)}
.feat,.lens{background:var(--card);border:1px solid var(--rule);border-radius:2px}
.feat{border-left:4px solid var(--accent)}
.feat h3{font-size:30px;font-weight:500}.feat-meta,.feat-count,.ver,.lbl,.feat h4{color:var(--text-2)}.feat-line{color:var(--ink);font-family:var(--head);font-size:19px;font-style:italic}
.ep{border-bottom:1px dotted var(--rule);border-radius:0}.ep a{color:var(--ink);text-decoration:none}.ep a:hover{color:var(--accent);text-decoration:underline}
.ep.hit{background:#EEF5F2}
.aud{border:1px solid var(--rule);color:var(--text-2);border-radius:2px}.aud-e{color:#3B5B78;border-color:#BCC9D6}.aud-b{color:#9A4D06;border-color:#E3C9A8}
.planned{color:var(--text-2);font-style:italic}
.feat-foot{border-top:1px solid var(--rule)}.sys li{border:1px solid var(--rule);color:var(--ink);border-radius:2px}.open{color:var(--accent)}
.soon{border-top:2px solid var(--ink);padding:16px 0 0}.soon h3{font-size:24px;font-weight:500}.soon p{color:var(--text-2)}
.lens{border-top:3px solid var(--ink)}.lens h3{font-size:22px;font-weight:500}.lens p{color:var(--text-2)}.lens.hit{border-top-color:var(--accent);background:#F5FAF8}
.legend-t{font-size:22px;font-weight:500}
.st{border-radius:2px;background:#fff}
.st-pass{color:#0D6E52;border-color:#0D6E52}
.st-released{color:#3B5B78;border-color:#3B5B78}
.st-held{color:#9A4D06;border-color:#9A4D06;border-style:double;border-width:3px}
.st-rejected{color:#B42318;border-color:#B42318}
.st-undef{color:#5C5346;border-color:#B5A88F;background:#F3EEE5;border-style:dashed}
th{font:500 12px var(--mono);text-transform:uppercase;letter-spacing:.08em;color:var(--text-2);border-bottom:1px solid var(--ink)}
td{border-bottom:1px solid var(--rule)}td.d{color:var(--text-2)}td.f{font-family:var(--head);font-size:17px}
td a{color:var(--ink);text-decoration-color:var(--rule);text-underline-offset:3px}td a:hover{color:var(--accent)}
.ftr{border-top:1px solid var(--ink);color:var(--text-2);margin-top:40px}
@media (max-width:640px){.hero h1{font-size:38px}.sec h2{font-size:28px}}
""",
    numbered=True,
    hero="ledger",
)

THEMES["workbench"] = dict(
    title="Explorable Workbench",
    fonts="family=Plus+Jakarta+Sans:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500",
    css="""
:root{--bg:#F4F6F9;--card:#fff;--ink:#0F172A;--text-2:#475569;--accent:#1D4ED8;--border:#E2E8F0;--link:#1D4ED8;--focus:#1D4ED8;
--body:'Inter',system-ui,sans-serif;--head:'Plus Jakarta Sans',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace}
.hdr{background:#fff;border-bottom:1px solid var(--border);box-shadow:0 1px 2px rgba(15,23,42,.04)}
.brand{color:var(--ink);font-family:var(--head);font-weight:700}.brand span{color:var(--accent)}
.nav a{color:var(--text-2)}.nav a:hover{color:var(--accent)}
.lens-sw{background:#EEF2F7}.lens-lbl{color:var(--text-2)}.lens-sw button{color:var(--text-2)}
.lens-sw button[aria-pressed=true]{background:#fff;color:var(--accent);box-shadow:0 1px 3px rgba(15,23,42,.12)}
.lens-note{background:#EFF6FF;color:#1E3A8A}
h1,h2,h3{font-family:var(--head);font-weight:700;letter-spacing:-.015em}
.hero h1{font-size:44px;line-height:1.1}
.eyebrow{color:var(--accent);display:inline-block;background:#EFF6FF;padding:2px 10px;border-radius:999px}
.lead{color:var(--text-2)}.hero-stats{color:var(--text-2)}
.hero-stats li{background:#fff;border:1px solid var(--border);border-radius:10px;padding:8px 14px}.hero-stats{gap:10px}
.hero-stats b{font-family:var(--head);color:var(--ink)}
.btn{background:var(--accent);color:#fff;border-radius:10px;border:1px solid var(--accent)}.btn:hover{background:#1E40AF}
.btn.ghost{background:#fff;color:var(--ink);border-color:var(--border)}.btn.ghost:hover{border-color:var(--accent);color:var(--accent)}
.hero-vis img{border-radius:16px;border:1px solid var(--border);background:#fff}.hero-vis figcaption{color:var(--text-2)}
.sec h2{font-size:28px}.sec-lead{color:var(--text-2)}
.feat,.soon,.lens{background:var(--card);border:1px solid var(--border);border-radius:16px;box-shadow:0 1px 2px rgba(15,23,42,.04);transition:box-shadow .2s,border-color .2s,opacity .2s}
.feat:hover{box-shadow:0 8px 24px rgba(15,23,42,.08);border-color:#BFDBFE}
.feat h3{font-size:24px}.feat-meta,.feat-count,.ver,.lbl,.feat h4{color:var(--text-2)}.feat-line{color:var(--ink)}
.ep{border:1px solid transparent}.ep a{color:var(--ink);text-decoration:none}.ep a:hover{color:var(--accent)}
.ep.hit{background:#EFF6FF;border-color:#BFDBFE}
.aud{background:#F1F5F9;color:var(--text-2)}.aud-e{background:#EEF2FF;color:#3730A3}.aud-b{background:#FFF7ED;color:#B45309}
.planned{color:var(--text-2)}
.feat-foot{border-top:1px solid var(--border)}.sys li{background:#F1F5F9;color:#334155;border-radius:999px}.open{color:var(--accent)}
.soon{background:repeating-linear-gradient(135deg,#fff 0 12px,#F8FAFC 12px 24px)}.soon h3{font-size:19px}.soon p{color:var(--text-2);font-size:15px}
.lens h3{font-size:18px}.lens p{color:var(--text-2)}.lens.hit{border-color:var(--accent);box-shadow:0 0 0 3px #DBEAFE}
.legend-t{font-size:18px}
.st{border-radius:999px}
.st-pass{color:#047857;background:#ECFDF5;border-color:#047857}
.st-released{color:#3730A3;background:#EEF2FF;border-color:#3730A3}
.st-held{color:#B45309;background:#FFFBEB;border-color:#B45309;border-style:double;border-width:3px}
.st-rejected{color:#BE123C;background:#FFF1F2;border-color:#BE123C}
.st-undef{color:#475569;border-color:#94A3B8;border-style:dashed;background:repeating-linear-gradient(135deg,#F8FAFC 0 5px,#E2E8F0 5px 7px)}
.tbl{background:#fff;border:1px solid var(--border);border-radius:16px}
th{font:600 12px var(--body);color:var(--text-2);text-transform:uppercase;letter-spacing:.05em;background:#F8FAFC;border-bottom:1px solid var(--border)}
td{border-top:1px solid var(--border)}td.d{color:var(--text-2)}
.ftr{color:var(--text-2)}
""",
    numbered=False,
    hero="workbench",
)

# Blueprint hero: drawn, not generated. One order, split at APEX (Split Payout example, fictional numbers).
BLUEPRINT_SVG = """<svg viewBox="0 0 640 360" role="img" aria-labelledby="bp-t bp-d" font-family="JetBrains Mono, monospace">
<title id="bp-t">One order from customer to payouts</title>
<desc id="bp-d">A customer pays AED 1,000. PGW passes it to APEX, which pays the partner and two vendors and keeps Geidea's MDR. Fictional numbers.</desc>
<defs><pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#EEF2F6"/></pattern>
<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#0E7C66"/></marker>
<marker id="as" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#64748B"/></marker></defs>
<rect width="640" height="360" fill="url(#g)"/>
<g font-size="11" fill="#64748B"><text x="16" y="22">CUSTOMER</text><text x="168" y="22">PGW</text><text x="316" y="22">APEX</text><text x="476" y="22">PAYOUTS</text></g>
<g stroke="#CBD5E1" stroke-dasharray="3 4"><path d="M150 30V344M298 30V344M446 30V344"/></g>
<rect x="16" y="150" width="112" height="56" rx="6" fill="#fff" stroke="#0F172A" stroke-width="1.5"/>
<text x="28" y="173" font-size="12" fill="#0F172A">Pays</text><text x="28" y="192" font-size="14" font-weight="500" fill="#0F172A">AED 1,000</text>
<rect x="168" y="150" width="112" height="56" rx="6" fill="#fff" stroke="#0F172A" stroke-width="1.5"/>
<text x="180" y="173" font-size="12" fill="#0F172A">Session +</text><text x="180" y="192" font-size="12" fill="#0F172A">split advice</text>
<rect x="316" y="150" width="112" height="56" rx="6" fill="#fff" stroke="#0F172A" stroke-width="1.5"/>
<text x="328" y="173" font-size="12" fill="#0F172A">Validate +</text><text x="328" y="192" font-size="12" fill="#0F172A">settle</text>
<path d="M128 178H166M280 178H314" stroke="#0E7C66" stroke-width="3" marker-end="url(#ar)"/>
<g fill="none" stroke-width="3"><path d="M428 168C450 168 446 70 470 70" stroke="#0E7C66" marker-end="url(#ar)"/>
<path d="M428 176C452 176 446 140 470 140" stroke="#0E7C66" marker-end="url(#ar)"/>
<path d="M428 184C452 184 446 216 470 216" stroke="#0E7C66" marker-end="url(#ar)"/>
<path d="M428 194C450 194 446 290 470 290" stroke="#64748B" stroke-dasharray="6 4" marker-end="url(#as)"/></g>
<g font-size="12"><rect x="474" y="52" width="150" height="36" rx="6" fill="#E6F4F1" stroke="#0E7C66"/><text x="486" y="75" fill="#0B5E4E">Partner</text>
<rect x="474" y="122" width="150" height="36" rx="6" fill="#E6F4F1" stroke="#0E7C66"/><text x="486" y="145" fill="#0B5E4E">Vendor A</text>
<rect x="474" y="198" width="150" height="36" rx="6" fill="#E6F4F1" stroke="#0E7C66"/><text x="486" y="221" fill="#0B5E4E">Vendor B</text>
<rect x="474" y="272" width="150" height="36" rx="6" fill="#F1F5F9" stroke="#64748B"/><text x="486" y="295" fill="#334155">MDR kept by Geidea</text></g>
<text x="16" y="344" font-size="10" fill="#94A3B8">Split Payout · illustrative</text>
</svg>"""

HERO = {
    "svg": BLUEPRINT_SVG + '<figcaption>Split Payout in one picture: teal is money moving, slate is kept by Geidea.</figcaption>',
    "ledger": '<img src="../assets/img/hero-ledger.webp" width="1376" height="768" alt="Drafting-style drawing: one dark line splits into green, blue and amber channels across ledger tables." loading="eager"><figcaption>One payment, three channels. Illustration.</figcaption>',
    "workbench": '<img src="../assets/img/hero-workbench.webp" width="1344" height="768" alt="Isometric workbench with blue, green and orange pipes running through modular blocks." loading="eager"><figcaption>Illustration.</figcaption>',
}


def page(key):
    t = THEMES[key]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>PGW Feature Lab · preview: {t['title']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{t['fonts']}&display=swap">
<style>{BASE_CSS}{t['css']}</style>
</head>
<body data-lens="all" class="opt-{key}">
{body(HERO[t['hero']], t['numbered'])}
</body>
</html>
"""


CHOOSER = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>Feature Lab home: three options</title>
<style>body{margin:0;font:16px/1.6 system-ui,sans-serif;background:#F8FAFC;color:#0F172A}main{max-width:900px;margin:0 auto;padding:48px 24px}
h1{font-size:28px;margin:0 0 8px}p{color:#475569}ol{padding:0;list-style:none;display:grid;gap:16px}
li a{display:block;padding:20px;background:#fff;border:1px solid #E2E8F0;border-radius:12px;text-decoration:none;color:inherit}li a:hover{border-color:#1D4ED8}
b{display:block;font-size:18px}span{color:#475569;font-size:15px}</style></head>
<body><main><h1>Feature Lab home: three options</h1>
<p>Same content and structure, three looks. Preview only; the live home page is unchanged.</p>
<ol>
<li><a href="index-blueprint.html"><b>1. Blueprint + new structure</b><span>Current Lab look (IBM Plex Sans, teal), drawn hero.</span></a></li>
<li><a href="index-ledger.html"><b>2. Clearing Ledger</b><span>Editorial: Newsreader headings, warm paper, ruled sections.</span></a></li>
<li><a href="index-workbench.html"><b>3. Explorable Workbench</b><span>Product UI: Plus Jakarta Sans + Inter, cobalt, rounded cards.</span></a></li>
</ol></main></body></html>
"""

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for k in THEMES:
        (OUT / f"index-{k}.html").write_text(page(k), encoding="utf-8")
    (OUT / "index.html").write_text(CHOOSER, encoding="utf-8")
    print("built", ", ".join(THEMES))
