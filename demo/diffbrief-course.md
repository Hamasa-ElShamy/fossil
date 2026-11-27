# diffbrief: rebuild course

12 commits became 12 steps. Titles are commit messages; nothing here understands the code.

## 1. diffbrief: turn a git diff into a short human review brief
`git checkout 97e77bc` · large · +1210 -0 · 2026-11-26

Try first, before reading the diff, write:
- `class FileDiff in diffbrief.py`
- `function __init__ in diffbrief.py`
- `function added in diffbrief.py`
- `function removed in diffbrief.py`
- `function parse_diff in diffbrief.py`
- `function _symbols in diffbrief.py`

Suggested build order (smaller first, tests and docs last):
1. `docs/.nojekyll`
2. `docs/report.html`
3. `pyproject.toml`
4. `LICENSE`
5. `sample-real.diff`
6. `docs/index.html`
7. `diffbrief.py`
8. `sample-click.diff`
9. `README.md`
10. `.github/workflows/tests.yml`
11. `tests/test_diffbrief.py`

Files: added `.github/workflows/tests.yml` (+12 -0), added `LICENSE` (+21 -0), added `README.md` (+83 -0), added `__pycache__/diffbrief.cpython-310.pyc` (+0 -0), added `diffbrief.py` (+271 -0), added `docs/.nojekyll` (+0 -0), added `docs/index.html` (+74 -0), added `docs/report.html` (+15 -0), added `pyproject.toml` (+20 -0), added `sample-click.diff` (+491 -0), added `sample-real.diff` (+28 -0), added `tests/__pycache__/test_diffbrief.cpython-310-pytest-9.2.0.pyc` (+0 -0), added `tests/test_diffbrief.py` (+195 -0)

## 2. UX pass: mobile-safe headings, focus outlines, RTL markup, feature grid above prose
`git checkout 0313fd1` · small · +10 -8 · 2026-11-26

Files: modified `docs/index.html` (+10 -8)

## 3. Phase A design pass: distinctive font pairing, motion tokens, orchestrated hero entrance, micro-interactions, Arabic font
`git checkout 1d76d40` · small · +19 -4 · 2026-11-26

Files: modified `docs/index.html` (+19 -4)

## 4. Test awareness: flag logic changes with no matching test change in the diff
`git checkout 13a13e0` · medium · +112 -5 · 2026-11-26

Try first, before reading the diff, write:
- `function _stem in diffbrief.py`
- `function _test_awareness in diffbrief.py`
- `function test_untested_change_flagged in tests/test_diffbrief.py`
- `function test_matching_test_clears_flag_and_counts_tests in tests/test_diffbrief.py`
- `function test_docs_only_change_not_flagged in tests/test_diffbrief.py`

Files: modified `README.md` (+2 -1), modified `__pycache__/diffbrief.cpython-310.pyc` (+0 -0), modified `diffbrief.py` (+72 -4), modified `tests/__pycache__/test_diffbrief.cpython-310-pytest-9.2.0.pyc` (+0 -0), modified `tests/test_diffbrief.py` (+38 -0)

## 5. Python impact analysis (--repo): where removed/changed symbols are still used
`git checkout e48a1b4` · medium · +149 -6 · 2026-11-26

Try first, before reading the diff, write:
- `function _py_files in diffbrief.py`
- `function _refs_in_file in diffbrief.py`
- `function _impact in diffbrief.py`
- `function analyze in diffbrief.py`
- `function test_impact_removed_symbol_still_used in tests/test_diffbrief.py`
- `function test_impact_removed_symbol_unused in tests/test_diffbrief.py`

Files: modified `README.md` (+16 -1), modified `__pycache__/diffbrief.cpython-310.pyc` (+0 -0), modified `diffbrief.py` (+93 -5), added `sample-removed-click.diff` (+13 -0), modified `tests/__pycache__/test_diffbrief.cpython-310-pytest-9.2.0.pyc` (+0 -0), modified `tests/test_diffbrief.py` (+27 -0)

## 6. Soft review signals (swallowed errors, placeholders, unused/undeclared imports)
`git checkout 6d3f15e` · medium · +138 -4 · 2026-11-26

Try first, before reading the diff, write:
- `function _declared_deps in diffbrief.py`
- `function _local_modules in diffbrief.py`
- `function _signals in diffbrief.py`
- `function test_soft_signals in tests/test_diffbrief.py`
- `function test_signals_need_no_repo_for_basic_checks in tests/test_diffbrief.py`
- `function test_clean_code_has_no_signals in tests/test_diffbrief.py`

Files: modified `README.md` (+3 -2), modified `__pycache__/diffbrief.cpython-310.pyc` (+0 -0), modified `diffbrief.py` (+91 -2), modified `tests/__pycache__/test_diffbrief.cpython-310-pytest-9.2.0.pyc` (+0 -0), modified `tests/test_diffbrief.py` (+44 -0)

## 7. Docs: English-only README and architecture notes, clearer headings
`git checkout 585f4c6` · small · +0 -10 · 2026-11-26

Files: modified `README.md` (+0 -10)

## 8. Phase B: new proof-sheet design for landing page and HTML report; report shows tests, impact and signals
`git checkout 2bf5f66` · large · +264 -107 · 2026-11-26

Try first, before reading the diff, write:
- `function row in diffbrief.py`

Files: modified `__pycache__/diffbrief.cpython-310.pyc` (+0 -0), modified `diffbrief.py` (+91 -26), modified `docs/index.html` (+113 -67), modified `docs/report.html` (+60 -14)

## 9. Landing: wrap the command box instead of scrolling
`git checkout 94be1a6` · small · +1 -1 · 2026-11-26

Files: modified `docs/index.html` (+1 -1)

## 10. Report: fix horizontal overflow at 390px
`git checkout 16777dc` · small · +8 -8 · 2026-11-26

Files: modified `__pycache__/diffbrief.cpython-310.pyc` (+0 -0), modified `diffbrief.py` (+4 -4), modified `docs/report.html` (+4 -4)

## 11. Add inline favicon (removes the 404 console error)
`git checkout c33ce02` · small · +1 -1 · 2026-11-26

Files: modified `docs/index.html` (+1 -1)

## 12. Add DESIGN.md (tokens, type, motion, RTL rules, voice, do/don't)
`git checkout a1d967a` · medium · +90 -0 · 2026-11-26

Files: added `DESIGN.md` (+90 -0)
