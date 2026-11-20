"""Convert a finalised .docx into a Lab document page (wording unchanged).

Usage (run from the repo root):
  python3 tools/build_docs.py <docx> <out.html> --title "..." --version "..." --date "..." --feature "Split Payout" [--toc-depth 2]

Requires pandoc. Images go to a media folder next to the output page.
Section anchors are pandoc's heading ids, so links like product.html#money-flow keep working
across versions as long as the heading text stays the same.
"""
import argparse, html, os, re, subprocess, sys

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · PGW Feature Lab</title>
<link rel="stylesheet" href="../../assets/lab.css">
</head>
<body>
<header class="lab-header"><div class="inner">
<a class="lab-brand" href="../../"><span>pgw/</span>Feature Lab</a>
<nav class="lab-crumbs"><a href="../">{feature}</a> / {title}</nav>
</div></header>
<div class="doc-layout">
<aside class="toc" aria-label="Contents"><p>contents</p><ol>
{toc}
</ol></aside>
<main>
<div class="doc-meta"><span class="tag">{version}</span><span class="tag grey">{date}</span><span class="tag grey">Source: {source}</span></div>
<article class="doc">
{body}
</article>
</main>
</div>
<footer class="lab-footer">Published copy of the master Word document. Wording is unchanged; the .docx stays the master.</footer>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("out")
    ap.add_argument("--title", required=True)
    ap.add_argument("--version", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--feature", required=True)
    ap.add_argument("--toc-depth", type=int, default=2)
    a = ap.parse_args()

    out_dir = os.path.dirname(os.path.abspath(a.out))
    stem = os.path.splitext(os.path.basename(a.out))[0]
    media = f"media-{stem}"
    body = subprocess.run(
        ["pandoc", a.docx, "-t", "html5", f"--extract-media={media}"],
        cwd=out_dir, check=True, capture_output=True, text=True,
    ).stdout

    toc = []
    for level, hid, inner in re.findall(r'<h([1-3]) id="([^"]+)"[^>]*>(.*?)</h\1>', body, re.S):
        if int(level) > a.toc_depth:
            continue
        text = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
        toc.append(f'<li class="l{level}"><a href="#{hid}">{html.escape(text)}</a></li>')

    page = TEMPLATE.format(
        title=html.escape(a.title), version=html.escape(a.version), date=html.escape(a.date),
        feature=html.escape(a.feature), source=html.escape(os.path.basename(a.docx)),
        toc="\n".join(toc), body=body,
    )
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"wrote {a.out}: {len(toc)} toc entries")


if __name__ == "__main__":
    sys.exit(main())
