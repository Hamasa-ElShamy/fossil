# Fossil design system

Read this before changing the site (`docs/index.html`) or the course page (`fossil/render.py`). Add no new directions.

- Direction: sediment layers. A strata band across the top of the landing page, warm sandstone paper, dark brown ink, one rust accent used for the card edge and links.
- Colour: paper `#f7f1e6`, ink `#2b1f16`, accent `#8c3f17`, muted `#5d4a3a` (AA on paper). Diff lines: added `#e6f6e6`, removed `#fdeaea`, hunk header on lavender.
- Type: Literata for headings (serif, story feel), Inter for interface text, JetBrains Mono for code, Cairo for Arabic.
- Light only. Arabic: the toggle sets `lang` and `dir`; code, diffs and commands stay LTR.
- Motion: one small lift on buttons, off under `prefers-reduced-motion`.
- Targets 44px minimum (buttons, step links, file summaries).
- Honesty: titles are commit messages and the page says nothing understands the code. Numbers shown come from measurements only.
