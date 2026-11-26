#!/usr/bin/env python3
"""Turn in-document references into links, add "Referenced from" lists and a Back trail.

Usage (repo root):  python3 tools/add_cross_refs.py <doc page.html> [--report]
Idempotent: removes earlier xref markup first, then re-adds it. Run after tools/build_docs.py.

Written for documents that refer to themselves the way the Direct Debit Product Document does:
  A4, B3, C3                      part sections ("## A4. ...")
  S5                              Backend stories ("## S5 — ...")
  S7 section 2, S8 sections 2 and 3, S10 sections 1 to 4, S1 section 5.4
                                  numbered sub-headings inside a story (falls back to the nearest
                                  parent number: 2.1 -> 2, 3a -> 3)
  section 3 (inside a story)      the same story's sub-heading (not after an outside document's
                                  name, e.g. "UAE PASS Signature API v1.4 section 5")
  S8 rule 7                       the story's "Rules" heading
  Flow 2, Journey 3               "### Flow 2 — ..." / "### Journey 3 — ..."
  US-07, US-07 to US-13           frontend stories -> the frontend alignment section (C3)
Text inside links, code, preformatted blocks and headings is never changed.
"""
import re, sys, html
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

SKIP = {"a", "code", "pre", "h1", "h2", "h3", "h4", "h5", "h6", "script", "style", "summary"}


def heading_text(h):
    return re.sub(r"\s+", " ", h.get_text(" ")).strip()


def build_index(doc):
    idx = {"part": {}, "story": {}, "sub": {}, "rules": {}, "flow": {}, "journey": {}, "c3": None}
    story = None
    order = []  # (element, story key) in document order for context
    for h in doc.find_all(re.compile(r"^h[1-6]$")):
        t = heading_text(h)
        lvl = int(h.name[1])
        hid = h.get("id")
        if not hid:
            continue
        m = re.match(r"^([ABC])(\d{1,2})\.\s", t)
        if m and lvl <= 2:
            idx["part"][m.group(1) + m.group(2)] = (hid, t)
            if m.group(1) + m.group(2) == "C3":
                idx["c3"] = (hid, t)
            story = None
        m2 = re.match(r"^S(\d{1,2})\s*[—–-]\s", t)
        if m2 and lvl <= 2:
            story = "S" + m2.group(1)
            idx["story"][story] = (hid, t)
            idx["sub"][story] = {}
            continue
        if lvl <= 2:
            story = None
        if story and lvl >= 3:
            n = re.match(r"^(\d+[a-z]?(?:\.\d+)*)\.?\s", t)
            if n:
                idx["sub"][story].setdefault(n.group(1), (hid, t))
            if re.match(r"^Rules\b", t):
                idx["rules"][story] = (hid, t)
        f = re.match(r"^Flow (\d+)\b", t)
        if f:
            idx["flow"][f.group(1)] = (hid, t)
        j = re.match(r"^Journey (\d+)\b", t)
        if j:
            idx["journey"][j.group(1)] = (hid, t)
    return idx


def sub_target(idx, story, num):
    subs = idx["sub"].get(story, {})
    n = num
    while n:
        if n in subs:
            return subs[n]
        if "." in n:
            n = n.rsplit(".", 1)[0]
        elif re.match(r"^\d+[a-z]$", n):
            n = n[:-1]
        else:
            break
    return None


NUM = r"\d+[a-z]?(?:\.\d+)*"
RX = re.compile(
    r"(?P<storysec>\bS(?P<s1>\d{1,2})\s+(?P<word>sections?)\s+(?P<nums>" + NUM + r"(?:(?:\s*,\s*|\s+and\s+|\s+to\s+|\s*&\s*)" + NUM + r")*))"
    r"|(?P<storyrule>\bS(?P<s2>\d{1,2})\s+(?P<rword>rules?)\s+(?P<rnum>\d+))"
    r"|(?P<story>\bS(?P<s3>\d{1,2})\b(?![.\d]))"
    r"|(?P<part>(?<![\w-])(?P<pl>[ABC])(?P<pn>\d{1,2})\b(?![.\d]))"
    r"|(?P<baresec>(?<![\w])(?P<bword>[Ss]ections?)\s+(?P<bnums>" + NUM + r"(?:(?:\s*,\s*|\s+and\s+|\s+to\s+|\s*&\s*)" + NUM + r")*))"
    r"|(?P<flow>\bFlow\s+(?P<fn>\d+)\b)"
    r"|(?P<journey>\bJourney\s+(?P<jn>\d+)\b)"
    r"|(?P<us>\bUS-\d{2}(?:\.\d+)?\b)"
)


class Linker:
    def __init__(self, soup, idx):
        self.soup, self.idx = soup, idx
        self.n = 0
        self.back = {}  # target id -> list of (source link id, source label)
        self.count = 0

    def a(self, text, target, src_label):
        hid, t = target
        self.n += 1
        lid = f"xr{self.n}"
        self.back.setdefault(hid, []).append((lid, src_label))
        self.count += 1
        return f'<a class="xref" id="{lid}" href="#{hid}" title="{html.escape(t, quote=True)}">{html.escape(text)}</a>'

    def nums_html(self, story, nums, src_label):
        out, last = [], 0
        for m in re.finditer(NUM, nums):
            out.append(html.escape(nums[last:m.start()]))
            tgt = sub_target(self.idx, story, m.group(0))
            out.append(self.a(m.group(0), tgt, src_label) if tgt else html.escape(m.group(0)))
            last = m.end()
        out.append(html.escape(nums[last:]))
        return "".join(out)

    def convert(self, text, story_ctx, src_label):
        out, last, changed = [], 0, False
        for m in RX.finditer(text):
            rep = None
            g = m.groupdict()
            if g["storysec"]:
                st = "S" + g["s1"]
                if st in self.idx["story"]:
                    rep = self.a("S" + g["s1"], self.idx["story"][st], src_label) + " " + g["word"] + " " + self.nums_html(st, g["nums"], src_label)
            elif g["storyrule"]:
                st = "S" + g["s2"]
                if st in self.idx["story"]:
                    tgt = self.idx["rules"].get(st, self.idx["story"][st])
                    rep = self.a("S" + g["s2"], self.idx["story"][st], src_label) + " " + self.a(g["rword"] + " " + g["rnum"], tgt, src_label)
            elif g["story"]:
                st = "S" + g["s3"]
                if st in self.idx["story"]:
                    rep = self.a(st, self.idx["story"][st], src_label)
            elif g["part"]:
                k = g["pl"] + g["pn"]
                if k in self.idx["part"]:
                    rep = self.a(k, self.idx["part"][k], src_label)
            elif g["baresec"]:
                before = text[max(0, m.start() - 45):m.start()]
                if re.search(r"(API|[Dd]ocument|[Mm]anual|[Ss]pec|[Cc]hecklist|[Rr]ule ?[Bb]ook|[Gg]uide|FAQ|\bv\d)", before):
                    continue
                if story_ctx and story_ctx in self.idx["story"]:
                    nums = g["bnums"]
                    if sub_target(self.idx, story_ctx, re.match(NUM, nums).group(0)):
                        rep = html.escape(g["bword"]) + " " + self.nums_html(story_ctx, nums, src_label)
            elif g["flow"]:
                if g["fn"] in self.idx["flow"]:
                    rep = self.a(m.group(0), self.idx["flow"][g["fn"]], src_label)
            elif g["journey"]:
                if g["jn"] in self.idx["journey"]:
                    rep = self.a(m.group(0), self.idx["journey"][g["jn"]], src_label)
            elif g["us"]:
                if self.idx["c3"]:
                    rep = self.a(m.group(0), self.idx["c3"], src_label)
            if rep is None:
                continue
            out.append(html.escape(text[last:m.start()]))
            out.append(rep)
            last = m.end()
            changed = True
        if not changed:
            return None
        out.append(html.escape(text[last:]))
        return "".join(out)


def clean(soup):
    for a in soup.select("a.xref"):
        a.replace_with(a.get_text())
    for d in soup.select("details.refby"):
        d.decompose()
    for s in soup.select("#xref-back, #xref-script, #xref-style"):
        s.decompose()
    soup.smooth()


CSS = """
html{scroll-behavior:auto}
.doc a.xref{color:var(--accent);text-decoration:none;border-bottom:1px dotted currentColor;font-weight:500;white-space:nowrap}
.doc a.xref:hover{border-bottom-style:solid;background:var(--accent-bg)}
.doc details.refby{margin:-2px 0 12px;font-size:13px;color:var(--text-2)}
.doc details.refby summary{cursor:pointer;display:inline-flex;align-items:center;gap:6px;font:12px var(--mono);color:var(--muted);padding:2px 10px;border:1px solid var(--border);border-radius:999px;list-style:none;background:#fff}
.doc details.refby summary::-webkit-details-marker{display:none}
.doc details.refby summary:hover{border-color:#BFDBFE;color:var(--accent)}
.doc details.refby[open] summary{color:var(--accent);border-color:#BFDBFE;background:var(--accent-bg)}
.doc details.refby ul{margin:8px 0 0;padding:10px 14px 10px 30px;background:var(--bg);border-radius:10px;columns:2 260px;column-gap:28px}
.doc details.refby li{margin:2px 0;break-inside:avoid}
.doc details.refby a{color:var(--text);text-decoration:none}.doc details.refby a:hover{color:var(--accent);text-decoration:underline}
#xref-back{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);z-index:40;display:none;align-items:center;gap:10px;background:var(--ink);color:#fff;border:none;border-radius:999px;padding:10px 16px 10px 14px;font:500 14px var(--sans);box-shadow:0 10px 30px rgba(15,23,42,.3);cursor:pointer;max-width:calc(100vw - 32px)}
#xref-back.on{display:inline-flex}
#xref-back span.l{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#xref-back kbd{font:11px var(--mono);background:rgba(255,255,255,.15);border-radius:5px;padding:1px 6px}
#xref-back .x{margin-left:4px;opacity:.7;padding:0 2px}#xref-back .x:hover{opacity:1}
.doc [data-custom-style="Changed"]{color:#1D4ED8}
.doc del{color:#BE123C}
"""

JS = r"""
(function(){
  var trail=[], btn=document.getElementById('xref-back'), lbl=btn.querySelector('.l'), cnt=btn.querySelector('.c');
  function label(el){var h=el; while(h&&!/^H[1-6]$/.test(h.tagName)){h=h.previousElementSibling||h.parentElement;} return h?h.textContent.trim().slice(0,70):'previous place';}
  function show(){ if(!trail.length){btn.classList.remove('on');return;} var t=trail[trail.length-1]; lbl.textContent='Back to '+t.label; cnt.textContent=trail.length>1?'('+trail.length+')':''; btn.classList.add('on'); }
  document.addEventListener('click',function(e){
    var a=e.target.closest('a.xref, details.refby a'); if(!a) return;
    var src=a.closest('details.refby') ? a.closest('details.refby').previousElementSibling : a;
    if(!src.id){ src.id='xs'+Math.random().toString(36).slice(2,8); }
    trail.push({id:src.id,label:label(a.closest('details.refby')?src:a)}); if(trail.length>30) trail.shift(); show();
  });
  btn.addEventListener('click',function(e){
    if(e.target.classList.contains('x')){trail=[];show();return;}
    var t=trail.pop(); show(); if(!t) return;
    if(location.hash==='#'+t.id){var el=document.getElementById(t.id); el&&el.scrollIntoView({block:'center'});} else location.hash=t.id;
  });
  document.addEventListener('keydown',function(e){ if(e.altKey&&e.key==='ArrowLeft'&&trail.length){e.preventDefault();btn.click();} });
})();
"""


def main(path, report=False):
    p = Path(path)
    soup = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
    clean(soup)
    doc = soup.select_one("article.doc")
    idx = build_index(doc)
    L = Linker(soup, idx)
    story = None
    label = ""
    for el in list(doc.descendants):
        if getattr(el, "name", None) and re.match(r"^h[1-6]$", el.name):
            t = heading_text(el)
            lvl = int(el.name[1])
            m = re.match(r"^S(\d{1,2})\s*[—–-]\s", t)
            if m and lvl <= 2:
                story = "S" + m.group(1)
            elif lvl <= 2:
                story = None
            label = (story + " › " + t if story and not m else t)[:90]
            continue
        if not isinstance(el, NavigableString) or not el.strip():
            continue
        if any(par.name in SKIP for par in el.parents if par is not None and par is not doc) or el.parent is None:
            continue
        new = L.convert(str(el), story, label)
        if new:
            el.replace_with(BeautifulSoup(new, "html.parser"))
    # "Referenced from" under each target heading
    for hid, refs in L.back.items():
        h = doc.find(id=hid)
        if not h:
            continue
        seen, items = set(), []
        for lid, lab in refs:
            if lab in seen:
                continue
            seen.add(lab)
            items.append(f'<li><a href="#{lid}">{html.escape(lab)}</a></li>')
        det = BeautifulSoup(f'<details class="refby"><summary>Referenced from {len(items)} place{"s" if len(items) != 1 else ""}</summary><ul>{"".join(items)}</ul></details>', "html.parser")
        h.insert_after(det)
    st = soup.new_tag("style", id="xref-style"); st.string = CSS
    soup.head.append(st)
    btn = BeautifulSoup('<button type="button" id="xref-back" title="Go back along the references you followed (Alt + ←)"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M13 8H3M7 4L3 8l4 4"/></svg><span class="l"></span><span class="c"></span><kbd>Alt ←</kbd><span class="x" aria-label="Clear the trail">×</span></button>', "html.parser")
    soup.body.append(btn)
    sc = soup.new_tag("script", id="xref-script"); sc.string = JS
    soup.body.append(sc)
    p.write_text(str(soup), encoding="utf-8")
    print(f"{p}: {L.count} reference links, {len(L.back)} targets with 'Referenced from'")
    if report:
        print("parts", sorted(idx["part"]), "stories", sorted(idx["story"], key=lambda s: int(s[1:])))
        for s, subs in idx["sub"].items():
            print(s, sorted(subs)[:30])


if __name__ == "__main__":
    main(sys.argv[1], "--report" in sys.argv)
