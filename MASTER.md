# PGW Feature Lab: design system (MASTER)

Source of truth for the Lab's look. Read this before building any page. Change it only when Rabbani asks.
This is an own product: not Geidea Design System. Do not use Geidea branding here.

## Direction: Explorable Workbench (chosen 25-Nov-2026, replaces Blueprint)
Light, calm product-UI look: white cards on a cool grey page, rounded corners, cobalt accent. Long documents must stay comfortable to read; specs must be unambiguous.

## Colour tokens (assets/lab.css)
| Token | Hex | Use |
|---|---|---|
| --ink | #0F172A | Headings |
| --text | #1E293B | Body text |
| --text-2 | #475569 | Supporting text |
| --muted | #64748B | Meta, captions |
| --bg | #F4F6F9 | Page |
| --card | #FFFFFF | Cards, document body, header |
| --border / --border-2 | #E2E8F0 / #CBD5E1 | Hairlines |
| --accent / --accent-bg | #1D4ED8 / #EFF6FF | Links, focus, eyebrow, hover, search |
| --money / --money-bg | #047857 / #ECFDF5 | Money moving, pass, primary "View it visually" |
| --code-bg / --code-fg | #0F172A / #A7F3D0 | Payload blocks |
| --warn-bg / --warn-fg | #FEF3C7 / #92400E | "Illustrative" and draft tags |

### Status colours (always colour + icon or word + border style, never colour alone)
| State | Text | Background | Border |
|---|---|---|---|
| Pass / money moving | #047857 | #ECFDF5 | solid |
| Released / kept by Geidea | slate #475569 on visual pages; #3730A3 for feature status "In the works" | #F1F5F9 / #EEF2FF | solid |
| Held at APEX | #B45309 | #FFFBEB | double |
| Rejected | #BE123C | #FFF1F2 | solid |
| Not defined / waiting | #475569 | hatched #F8FAFC/#E2E8F0 | dashed |

Rule: green means money moving. Use it the same way on every visual page.

## Feature status (home page)
Solutioning complete (green, check) · In the works (indigo, arrow) · To work on next (dashed, hatched, clock). Set in `tools/build_home.py`.

## Type
- Plus Jakarta Sans 600/700 for headings (`--head`).
- Inter 400/500/600 for UI and prose (`--sans`). Body 16px, line-height 1.6.
- JetBrains Mono for field names, payloads, endpoints, version tags, eyebrows (`--mono`).

## Components
- Header: white bar, `pgw/` mono prefix in accent, breadcrumbs, search button (added by `assets/search.js`).
- Cards and row lists: radius 16px, 1px border, soft shadow; hover = blue border + lifted shadow.
- Tag/pill (radius 999px): default green, `grey`, `warn`.
- Doc layout: sticky contents + white article.
- Every simulated or illustrative page carries `<span class="tag warn">Illustrative</span>` near the title.
- Every visual page states which doc version it reflects and links back to the doc anchor.
- Exception: anything that depicts a Geidea screen (PGW config modal, MA config, HPP, Merchant Portal) uses Geidea Design System tokens (`.gx`, `.gh` scopes).

## Search
- `assets/search.js` on every page (Ctrl/Cmd+K, "/", header button, home search box). Results jump to page + section and flash the target.
- Index: `assets/search-index.js`, built by `python3 tools/build_search_index.py` from the rendered pages (includes content built by JavaScript and every `#try=` scenario link). Re-run after any page or doc change. It also adds missing ids to h2–h4 and the script tag to new pages.

## Sensitive data
The site is public. Never show real MIDs, OIC numbers, TRIDs, merchant names, emails, account numbers or real documents/screenshots. Use dummy values, and the SAME dummy value everywhere it repeats (keep a per-feature table of dummy values in the feature's hub source comment or handover).

## Quality checklist
- Text contrast 4.5:1 minimum; visible focus states; keyboard reachable.
- prefers-reduced-motion respected; transitions 150–300ms.
- Responsive at 375, 768, 1366, 1920. No horizontal page scroll (tables scroll inside their box).
- SVG icons only, no emoji.

## Document publishing
- The .docx is the master. Publish with `tools/build_docs.py` (pandoc), wording unchanged.
- Anchors are pandoc heading ids; visual pages link to them (e.g. `docs/product.html#money-flow`).
- After re-publishing, re-check that every "View it visually" link still points to an existing anchor, then rebuild the search index.
