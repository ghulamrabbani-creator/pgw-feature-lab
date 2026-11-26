"""Replace people's names with team names in published pages (public site; Rabbani 25-Nov-2026).

Usage (repo root): python3 tools/apply_public_names.py [page.html ...]   (no args = every page)
Map: tools/public_names.json, applied in order (longest phrases first). Only visible text and
attribute values change; heading ids are left alone. build_docs.py calls this on every publish.
Prints any known first name still present so the map can be extended.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
NAMES = r"\b(George|Vivek|Haggag|Alsomali|Wankhade|Eldegheidy|Arul|Arulraj|Talha|Sidra|Rohit|Asad|Manjunath|Badr|Emir|Nancy|Derya|Hussam|Dheeraj|Sherly|Marina|Musaad|Farida|Konchada|Mithun|Pankaj|Yassmin|Nehal|Lamia|Elgendy|Qurany|Osama|Pramod|ElTabbakh|Rahmatullah|Mahmoud)\b"

def apply(path):
    s = path.read_text(encoding="utf-8")
    o = s
    for a, b in json.load(open(ROOT / "tools" / "public_names.json", encoding="utf-8")):
        s = s.replace(a, b)
        s = s.replace(a.replace("&", "&amp;"), b.replace("&", "&amp;"))
    if s != o:
        path.write_text(s, encoding="utf-8")
    left = sorted(set(re.findall(NAMES, re.sub(r'\sid="[^"]*"', "", s))))
    if left:
        print(f"{path.relative_to(ROOT)}: names still present: {left}")
    return s != o

def main(args):
    files = [Path(a).resolve() for a in args] or [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]
    n = sum(apply(p) for p in files)
    print(f"public names: {n} file(s) changed")

if __name__ == "__main__":
    main(sys.argv[1:])
