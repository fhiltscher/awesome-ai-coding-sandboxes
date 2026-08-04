#!/usr/bin/env python3
"""Generate _data/sandboxes.json from the comparison matrix in README.md.

The README table is the single source of truth. This turns it into the data
Jekyll needs for the ItemList JSON-LD (_includes/head-custom.html).

    script/sandboxes-data.py            regenerate _data/sandboxes.json
    script/sandboxes-data.py --check    fail if it is out of sync (CI)

Run it after touching the matrix, or CI will tell you off.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUT = ROOT / "_data" / "sandboxes.json"

# The matrix, not the "Isolation building blocks" table further down.
SECTION = ("## Comparison matrix", "### What the data shows")

LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FOOTNOTE = re.compile(r"\[\^[^\]]+\]")

# Only OSI/FSF licenses get a URL; "Prop." and "unverified" carry no identifier.
LICENSE_URLS = {
    "MIT": "https://opensource.org/licenses/MIT",
    "Apache": "https://www.apache.org/licenses/LICENSE-2.0",
    "AGPL": "https://www.gnu.org/licenses/agpl-3.0.html",
}

STATE_LABELS = {
    "eph": "ephemeral workspace",
    "pers": "persistent workspace",
    "both": "ephemeral and persistent workspace",
}


def clean(cell):
    """Strip markdown emphasis and footnote refs from a table cell."""
    return FOOTNOTE.sub("", cell).replace("**", "").replace("_", "").strip()


def matrix_rows(text):
    """Yield the data rows of the comparison matrix as lists of cells."""
    start, end = text.index(SECTION[0]), text.index(SECTION[1])
    for line in text[start:end].splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells[0] == "Project" or set(cells[0]) <= {"-", " "}:
            continue  # header / separator
        yield cells


def to_item(position, cells):
    project, isolation, egress, secrets, hosting, state, license_ = cells

    link = LINK.search(project)
    if not link:
        raise SystemExit(f"row {position}: no project link in {project!r}")

    features = [
        f"{clean(isolation)} isolation",
        f"{clean(egress)} egress control",
        f"{clean(secrets)} secrets",
        clean(hosting),
    ]
    if label := STATE_LABELS.get(clean(state)):
        features.append(label)

    item = {
        "@type": "SoftwareApplication",
        "name": clean(link.group(1)),
        "url": link.group(2),
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Linux",
        "featureList": features,
    }
    if url := LICENSE_URLS.get(clean(license_)):
        item["license"] = url

    return {"@type": "ListItem", "position": position, "item": item}


def build():
    rows = list(matrix_rows(README.read_text(encoding="utf-8")))
    return [to_item(i, cells) for i, cells in enumerate(rows, start=1)]


def main():
    items = build()
    payload = json.dumps(items, indent=2, ensure_ascii=False) + "\n"

    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != payload:
            sys.exit(
                "_data/sandboxes.json is out of sync with the README matrix.\n"
                "Run: script/sandboxes-data.py"
            )
        print(f"in sync ({len(items)} entries)")
        return

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(payload, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(items)} entries)")


def demo():
    """Self-check against the real README."""
    items = build()
    assert len(items) >= 30, f"expected the full matrix, got {len(items)}"
    assert [i["position"] for i in items] == list(range(1, len(items) + 1))

    first = items[0]["item"]
    assert first["name"] == "Cleanroom", first["name"]
    assert first["url"].startswith("http")
    assert "deny-default egress control" in first["featureList"]
    assert first["license"] == LICENSE_URLS["MIT"]

    # Footnote refs must not leak into names or feature strings.
    blob = json.dumps(items)
    assert "[^" not in blob and "**" not in blob

    names = [i["item"]["name"] for i in items]
    assert "AgentENV" in names, "footnote-suffixed name mangled"
    assert len(set(names)) == len(names), "duplicate project names"
    print(f"ok — {len(items)} entries parsed")


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else main()
