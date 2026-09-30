# Benable October 2026

Seven gift lists ready to paste into Benable, an October launch plan, and a calculator for how much traffic a commission goal takes.

| File | What it is |
|---|---|
| [`PLAN.md`](PLAN.md) | The math, a day-by-day October plan, and the rules that keep commissions from being voided |
| [`lists/`](lists) | One markdown file per list: title, description and a blurb for every item |
| [`site/index.html`](site/index.html) | The same content as one page, with copy buttons and the calculator |
| [`data/lists.json`](data/lists.json) | Source of truth for products and lists |

## The lists

1. **Prime Big Deal Days 2026: What's Actually Worth Buying** (20 items; publish by Oct 3)
2. **The 2026 Holiday Gift Guide: 30 Gifts People Actually Use** (hub list; publish by Oct 5)
3. **Gifts for Her 2026** (18 items)
4. **Gifts for Him 2026** (15 items)
5. **Gifts for Kids & Teens 2026** (17 items)
6. **The Best Gifts Under $50** (18 items)
7. **Home Upgrades That Make Life Easier** (16 items, the highest order values)

## Editing

Change products or lists in `data/lists.json`, then rebuild:

```sh
python3 scripts/build.py
```

That regenerates `lists/*.md` and `site/index.html`. Edit `site/template.html` for page layout and the plan checklist.
