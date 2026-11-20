# PGW Feature Lab: design system (MASTER)

Source of truth for the Lab's look. Read this before building any page. Change it only when Rabbani asks.
This is an own product: not Geidea Design System. Do not use Geidea branding here.

## Direction: Blueprint
Light, quiet, technical. Long documents must stay comfortable to read; specs must be unambiguous.

## Colour tokens (assets/lab.css)
| Token | Hex | Use |
|---|---|---|
| --ink | #0F172A | Headings, header bar |
| --text | #1E293B | Body text |
| --text-2 | #475569 | Supporting text |
| --muted | #64748B | Meta, captions |
| --bg | #F8FAFC | Page |
| --card | #FFFFFF | Cards, document body |
| --border / --border-2 | #E2E8F0 / #CBD5E1 | Hairlines |
| --money | #0E7C66 | Money movement, primary action ("View it visually") |
| --money-bg | #E6F4F1 | Money tints |
| --link | #1D4ED8 | Links, focus ring |
| --code-bg / --code-fg | #0F172A / #A7F3D0 | Payload blocks |
| --warn-bg / --warn-fg | #FEF3C7 / #92400E | "Illustrative" and draft tags |

Rule: teal means money moving. Use it the same way on every visual page (flows, simulator, fee calculator).

## Type
- IBM Plex Sans 400/500/600 for all UI and prose. Body 16px, line-height 1.6.
- JetBrains Mono for field names, payloads, endpoints, version tags, eyebrows.

## Components
- Header: ink bar, `pgw/` mono prefix, breadcrumbs.
- Tile, row list, tag (default teal, `grey`, `warn`), doc layout (sticky contents + white article), visual-link button.
- Every simulated or illustrative page carries `<span class="tag warn">Illustrative</span>` near the title.
- Every visual page states which doc version it reflects and links back ("Read the requirement") to the doc anchor.

## Quality checklist (from UI UX Pro Max)
- Text contrast 4.5:1 minimum; visible focus states; keyboard reachable.
- prefers-reduced-motion respected; transitions 150–300ms.
- Responsive at 375, 768, 1024, 1440. No horizontal page scroll (tables scroll inside their box).
- SVG icons only, no emoji.

## Document publishing
- The .docx is the master. Publish with `tools/build_docs.py` (pandoc), wording unchanged.
- Anchors are pandoc heading ids; visual pages link to them (e.g. `docs/product.html#money-flow`).
- After re-publishing, re-check that every "View it visually" link still points to an existing anchor.
