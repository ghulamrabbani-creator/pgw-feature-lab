"""Insert "View it visually" buttons after doc headings (idempotent).

Usage (run from the repo root):  python3 tools/add_visual_links.py
Reads tools/visual_links.json: {page: {heading_id: href | [[label, href], ...]}}.
A plain href gives one "View it visually" button; a list gives one labelled button each, in a row.
Safe to re-run: existing buttons are removed and re-added. Warns when a heading id no longer exists.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def apply(page, links):
    path = os.path.join(ROOT, page)
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'\n?<div class="visual-links" data-auto>.*?</div>', "", s, flags=re.S)
    s = re.sub(r'\n?<a class="visual-link"[^>]*data-auto[^>]*>.*?</a>', "", s, flags=re.S)
    missing = []
    for hid, href in links.items():
        m = re.search(rf'<h([1-6])\s+id="{re.escape(hid)}"[^>]*>.*?</h\1>', s, re.S)
        if not m:
            missing.append(hid)
            continue
        if isinstance(href, str):
            btn = f'\n<a class="visual-link" data-auto href="{href}">{ICON}View it visually</a>'
        else:
            btn = '\n<div class="visual-links" data-auto>' + "".join(
                f'<a class="visual-link" href="{h}">{ICON}{label}</a>' for label, h in href) + '</div>'
        s = s[:m.end()] + btn + s[m.end():]
    open(path, "w", encoding="utf-8").write(s)
    print(f"{page}: {len(links) - len(missing)} buttons" + (f"; MISSING anchors: {missing}" if missing else ""))
    return not missing


def main(only=None):
    cfg = json.load(open(os.path.join(ROOT, "tools", "visual_links.json"), encoding="utf-8"))
    ok = True
    for page, links in cfg.items():
        if only and os.path.abspath(os.path.join(ROOT, page)) != os.path.abspath(only):
            continue
        ok &= apply(page, links)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
