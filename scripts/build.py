"""Build the Benable lists from data/lists.json.

Writes one ready-to-paste markdown file per list into lists/ and renders
site/index.html from site/template.html with the data embedded.

Usage: python3 scripts/build.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "lists.json"
LISTS_DIR = ROOT / "lists"
TEMPLATE = ROOT / "site" / "template.html"
PAGE = ROOT / "site" / "index.html"


def normalize(item):
    return {"id": item} if isinstance(item, str) else item


def validate(data):
    products = data["products"]
    for lst in data["lists"]:
        for item in map(normalize, lst["items"]):
            if item["id"] not in products:
                raise SystemExit(f"{lst['slug']}: unknown product id {item['id']!r}")
    for pid, p in products.items():
        if p["price"] not in data["meta"]["price_bands"]:
            raise SystemExit(f"{pid}: unknown price band {p['price']!r}")


def list_markdown(lst, products, bands):
    out = [
        f"# {lst['title']}",
        "",
        "**Paste as the list description:**",
        "",
        f"> {lst['description']}",
        "",
        f"**When:** {lst['when']}",
    ]
    if lst.get("note"):
        out += ["", f"**Note for you (don't paste):** {lst['note']}"]
    out += ["", "---", ""]
    for i, item in enumerate(map(normalize, lst["items"]), 1):
        p = products[item["id"]]
        meta = [f"`{p['price']}` ({bands[p['price']]})", " · ".join(p["where"])]
        if item.get("for"):
            meta.insert(0, f"**{item['for']}**")
        out += [f"## {i}. {p['name']}", "", " — ".join(meta), "", p["why"], ""]
        if p.get("note"):
            out += [f"_Note for you: {p['note']}_", ""]
    return "\n".join(out)


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    validate(data)

    LISTS_DIR.mkdir(exist_ok=True)
    for stale in LISTS_DIR.glob("*.md"):
        stale.unlink()
    bands = data["meta"]["price_bands"]
    for n, lst in enumerate(data["lists"], 1):
        path = LISTS_DIR / f"{n:02d}-{lst['slug']}.md"
        path.write_text(list_markdown(lst, data["products"], bands), encoding="utf-8")

    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8")
    if "/*__DATA__*/null" not in html:
        raise SystemExit("template is missing the /*__DATA__*/null placeholder")
    PAGE.write_text(html.replace("/*__DATA__*/null", payload), encoding="utf-8")

    items = sum(len(l["items"]) for l in data["lists"])
    print(f"{len(data['lists'])} lists, {items} list items, {len(data['products'])} products")


if __name__ == "__main__":
    main()
