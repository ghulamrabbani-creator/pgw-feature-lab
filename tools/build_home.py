#!/usr/bin/env python3
"""Build the Lab home page (index.html). Run from the repo root:
    python3 tools/build_home.py
Content lives in SECTIONS below; the look comes from assets/lab.css (Workbench, see MASTER.md).
Re-run tools/build_search_index.py after this (it is cheap and keeps the index current).
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# status: done | works | next
SECTIONS = [
    ("done", "Solutioning complete", "Solution documents written and agreed.", [
        {
            "name": "Split Payout", "href": "split-payout/", "meta": "MVP",
            "line": "One partner order, paid out to the partner and its vendors from one transaction.",
            "systems": ["PGW", "APEX", "MA", "Merchant Portal"],
            "docs": [("Product document", "v1.6", "split-payout/docs/product.html"),
                     ("PGW dev stories", "v0.5", "split-payout/docs/stories.html")],
            "pages": [("End-to-end view", "split-payout/end-to-end.html"),
                      ("Money flow", "split-payout/money-flow.html"),
                      ("Onboarding", "split-payout/onboarding.html"),
                      ("Split modes", "split-payout/split-modes.html"),
                      ("Config & Payment Simulator", "split-payout/simulator.html"),
                      ("Advice lifecycle", "split-payout/advice-lifecycle.html"),
                      ("What can go wrong", "split-payout/what-can-go-wrong.html")],
            "note": "",
        },
        {
            "name": "Direct Debit", "href": "", "meta": "UAE Direct Debit Marketplace (DDS)",
            "line": "Recurring bank-to-bank collections under a signed contract, with frequency-based debits, from the Merchant Portal.",
            "systems": ["DD Backend (new)", "DDS", "Merchant Portal", "APEX", "MA", "PGW config"],
            "docs": [], "pages": [("Merchant Portal prototype", "https://merchant-portal-replica.vercel.app/direct-debit")],
            "note": "Lab pages are being built.",
        },
    ]),
    ("works", "In the works", "Solution being written; pages follow the documents.", [
        {
            "name": "MCP", "href": "mcp/", "meta": "Multi-currency pricing",
            "line": "The customer pays on HPP in their own currency; the merchant stays in AED.",
            "systems": ["PGW", "HPP", "MA", "APEX", "Planet"],
            "docs": [("Solution requirements", "v3.0", "mcp/docs/requirements.html"),
                     ("PGW dev stories", "v0.1", "mcp/docs/stories.html")],
            "pages": [("End-to-end view", "mcp/end-to-end.html"),
                      ("HPP simulator", "mcp/hpp-simulator.html"),
                      ("Calculator", "mcp/calculator.html"),
                      ("Order model", "mcp/order-model.html")],
            "note": "Planned: Rate file lifecycle, What can go wrong. Parked: Federation and enrichment.",
        },
        {
            "name": "Network Tokenization", "href": "network-tokenization/", "meta": "Visa network token mandate",
            "line": "Saved-card (CIT and MIT) payments sent with the scheme token on MPGS and CyberSource; PGW records it on every transaction.",
            "systems": ["PGW", "MPGS", "CyberSource", "PGW config", "APEX (parked)"],
            "docs": [("PGW dev stories", "v1.1", "network-tokenization/docs/stories.html")],
            "pages": [("Token layers", "network-tokenization/token-layers.html"),
                      ("Payment explorer", "network-tokenization/payment-explorer.html"),
                      ("What PGW records", "network-tokenization/what-pgw-records.html"),
                      ("Switches and rollout", "network-tokenization/switches-and-rollout.html"),
                      ("Not yet defined", "network-tokenization/not-yet-defined.html")],
            "note": "Parked: NT-A1 (APEX keys), NT-X (token status). Guest checkout in POC.",
        },
    ]),
    ("next", "To work on next", "Scoping and discovery.", [
        {
            "name": "Pay by Bank", "href": "", "meta": "via Lean Technologies",
            "line": "Account-to-account payment through Open Finance; the customer approves in their bank app.",
            "systems": ["PGW", "APEX", "MA", "Merchant Portal", "Lean (new)"],
            "docs": [], "pages": [], "note": "",
        },
    ]),
]

ICONS = {
    "done": '<path d="M3 8.5l3 3 7-7"/>',
    "works": '<path d="M3 8h10M9 4l4 4-4 4"/>',
    "next": '<circle cx="8" cy="8" r="5.5"/><path d="M8 5v3l2 1.5"/>',
    "arrow": '<path d="M3 8h10M9 4l4 4-4 4"/>',
    "ext": '<path d="M9 3h4v4M13 3L7 9M11 9.5V13H3V5h3.5"/>',
    "search": '<circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5L14 14"/>',
}
LABEL = {"done": "Solutioning complete", "works": "In the works", "next": "To work on next"}


def e(s):
    return html.escape(s, quote=True)


def icon(n, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[n]}</svg>')


def link(label, href):
    ext = href.startswith("http")
    attrs = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a href="{e(href)}"{attrs}>{e(label)}{icon("ext", "ic ext") if ext else ""}</a>'


def card(f, status):
    has_lab = bool(f["href"])
    docs = "".join(f'<li>{link(l, h)}<span class="ver">{e(v)}</span></li>' for l, v, h in f["docs"])
    pages = "".join(f"<li>{link(l, h)}</li>" for l, h in f["pages"])
    cols = ""
    if docs or pages:
        cols = '<div class="feat-cols">'
        if docs:
            cols += f'<div><h4>Documents</h4><ul class="eps">{docs}</ul></div>'
        if pages:
            ttl = "Visual pages" if has_lab else "Prototype"
            cols += f'<div><h4>{ttl}</h4><ul class="eps">{pages}</ul></div>'
        cols += "</div>"
    note = f'<p class="note">{e(f["note"])}</p>' if f["note"] else ""
    systems = "".join(f"<li>{e(s)}</li>" for s in f["systems"])
    title = f'<a href="{f["href"]}">{e(f["name"])}</a>' if has_lab else e(f["name"])
    open_ = f'<a class="open" href="{f["href"]}">Open {e(f["name"])} {icon("arrow")}</a>' if has_lab else ""
    cls = "feat" + ("" if has_lab else " nolab") + (" small" if status == "next" else "")
    return f"""<article class="{cls}" id="{e(f['name'].lower().replace(' ', '-'))}">
<p class="feat-meta">{e(f['meta'])}</p>
<h3>{title}</h3>
<p class="feat-line">{e(f['line'])}</p>
{cols}{note}
<div class="feat-foot"><span class="lbl">Systems</span><ul class="sys">{systems}</ul>{open_}</div>
</article>"""


def section(status, title, lead, feats):
    cards = "\n".join(card(f, status) for f in feats)
    return f"""<section class="sec st-{status}" id="{status}">
<div class="sec-head"><span class="badge b-{status}">{icon(status)}{e(LABEL[status])}</span><p class="sec-lead">{e(lead)}</p></div>
<div class="feats n{len(feats)}">{cards}</div>
</section>"""


CSS = """
.home-hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:center;padding:24px 0 40px}
.home-hero h1.page{font-size:44px;line-height:1.1}
.home-hero .lead{margin-bottom:24px}
.hsearch{display:flex;align-items:center;gap:10px;width:100%;max-width:600px;background:#fff;border:1px solid var(--border-2);border-radius:14px;padding:13px 16px;font:500 16px var(--sans);color:var(--muted);cursor:text;box-shadow:0 1px 2px rgba(15,23,42,.05);transition:border-color .2s,box-shadow .2s;text-align:left}
.hsearch:hover,.hsearch:focus-visible{border-color:var(--accent);box-shadow:0 0 0 3px #DBEAFE}
.hsearch .ic{width:18px;height:18px;flex:none;color:var(--muted)}
.hsearch span{flex:1}
.hsearch kbd{font:12px var(--mono);border:1px solid var(--border);border-radius:5px;padding:1px 6px;color:var(--muted)}
.tries{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:12px 0 0;font-size:13px;color:var(--muted)}
.tries button{font:12.5px var(--mono);border:1px solid var(--border);background:#fff;border-radius:999px;padding:3px 10px;color:var(--text-2);cursor:pointer;transition:border-color .2s,color .2s}
.tries button:hover{border-color:var(--accent);color:var(--accent)}
.home-hero figure{margin:0}
.home-hero img{display:block;width:100%;height:auto;border-radius:16px;border:1px solid var(--border);background:#fff}
.sec{margin-top:40px}
.sec-head{display:flex;align-items:center;flex-wrap:wrap;gap:8px 14px;margin-bottom:16px}
.sec-lead{margin:0;color:var(--text-2);font-size:15px}
.badge{display:inline-flex;align-items:center;gap:8px;font:700 20px var(--head);letter-spacing:-.01em;padding:6px 16px 6px 12px;border-radius:999px;border:1.5px solid}
.badge .ic{width:18px;height:18px}
.b-done{color:var(--s-pass);background:var(--s-pass-bg);border-color:var(--s-pass)}
.b-works{color:var(--s-released);background:var(--s-released-bg);border-color:var(--s-released)}
.b-next{color:var(--s-undef);border-color:#94A3B8;border-style:dashed;background:repeating-linear-gradient(135deg,#F8FAFC 0 6px,#EEF2F7 6px 9px)}
.feats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.feats.n1{grid-template-columns:minmax(0,1fr)}
.feat{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px;display:flex;flex-direction:column;box-shadow:0 1px 2px rgba(15,23,42,.04);transition:box-shadow .2s,border-color .2s}
.feat:hover{box-shadow:0 8px 24px rgba(15,23,42,.08);border-color:#BFDBFE}
.st-done .feat{border-top:3px solid var(--s-pass)}
.st-works .feat{border-top:3px solid var(--s-released)}
.feat.small{max-width:700px}
.st-next .feat{border-style:dashed;border-color:#CBD5E1}
.feat-meta{font:12px var(--mono);color:var(--muted);margin:0}
.feat h3{font:700 24px var(--head);letter-spacing:-.015em;margin:2px 0 0}
.feat h3 a{color:inherit;text-decoration:none}.feat h3 a:hover{color:var(--accent)}
.feat-line{margin:10px 0 16px;color:var(--text)}
.feat-cols,.note{margin-bottom:18px}
.feat-cols{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,3fr);gap:24px;flex:1}
.feat h4{font:600 12px var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:0 0 6px}
.eps{list-style:none;margin:0;padding:0}
.eps li{display:flex;align-items:center;flex-wrap:wrap;gap:8px;padding:5px 0}
.eps a{color:var(--ink);font-weight:500;text-decoration:none;display:inline-flex;align-items:center;gap:5px}
.eps a:hover{color:var(--accent);text-decoration:underline}
.eps .ext{width:13px;height:13px;color:var(--muted)}
.ver{font:12px var(--mono);color:var(--muted)}
.note{font-size:13.5px;color:var(--text-2);margin:12px 0 0;padding:8px 12px;border-radius:10px;background:var(--bg)}
.feat-foot{display:flex;align-items:center;flex-wrap:wrap;gap:8px 12px;margin-top:auto;padding-top:14px;border-top:1px solid var(--border)}
.lbl{font:12px var(--mono);color:var(--muted)}
.sys{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.sys li{font:12px var(--mono);padding:2px 9px;background:#F1F5F9;color:#334155;border-radius:999px}
.open{margin-left:auto;display:inline-flex;align-items:center;gap:6px;font-weight:600;font-size:14px;color:var(--accent);text-decoration:none}
.open .ic{width:14px;height:14px}
.ic{display:inline-block;vertical-align:middle}
@media (max-width:1100px){.feats{grid-template-columns:minmax(0,1fr)}}
@media (max-width:900px){.home-hero{grid-template-columns:minmax(0,1fr);gap:28px}.home-hero h1.page{font-size:34px}}
@media (max-width:640px){.feat-cols{grid-template-columns:minmax(0,1fr)}.feat{padding:18px}.badge{font-size:18px}.hsearch kbd{display:none}}
"""


def page():
    secs = "\n".join(section(*s) for s in SECTIONS)
    tries = "".join(f'<button type="button" data-lab-search value="{e(t)}">{e(t)}</button>' for t in
                    ["deferredSplit", "rate file", "amount validation", "refund"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PGW Feature Lab</title>
<link rel="stylesheet" href="assets/lab.css">
<style>{CSS}</style>
</head>
<body>
<header class="lab-header"><div class="inner">
<a class="lab-brand" href="./"><span>pgw/</span>Feature Lab</a>
</div></header>
<main class="wrap">
<section class="home-hero">
<div>
<p class="eyebrow">payment gateway · new features</p>
<h1 class="page">How new PGW features work, end to end</h1>
<p class="lead">Each feature has its documents and visual pages: flows, simulators and scenarios that show the configuration, the calls between systems and what can go wrong. The documents are the reference; the visual pages illustrate them.</p>
<button type="button" class="hsearch" data-lab-search aria-label="Search the Lab">{icon("search")}<span>Search pages, fields, checks, scenarios</span><kbd>Ctrl K</kbd></button>
<p class="tries">Try: {tries}</p>
</div>
<figure><img src="assets/img/hero-workbench.webp" width="1344" height="768" alt="Isometric workbench with blue, green and orange pipes running through modular blocks."></figure>
</section>
{secs}
</main>
<footer class="lab-footer">Pages marked Illustrative use fictional numbers. The published documents are the reference.</footer>
<script src="assets/search.js" defer></script>
</body>
</html>
"""


if __name__ == "__main__":
    (ROOT / "index.html").write_text(page(), encoding="utf-8")
    print("index.html built")
