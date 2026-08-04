#!/usr/bin/env python3
"""Render assets/og.png (the social preview card) from README.md.

Counts are parsed out of the comparison matrix rather than hardcoded, so the
card cannot drift from the list. Re-run after adding or changing entries:

    python3 script/og-image.py
"""

import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "og.png"

W, H = 1200, 630
MARGIN = 80
BG = "#0d1117"
FG = "#e6edf3"
MUTED = "#8b949e"
ACCENT = "#3fb950"

FONTS = {
    "bold": ["/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "regular": ["/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "mono": ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"],
}


def font(kind, size):
    for path in FONTS[kind]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise SystemExit(f"no font found for {kind}; tried {FONTS[kind]}")


def matrix_rows():
    """Rows of the 7-column comparison matrix in README.md."""
    lines = (ROOT / "README.md").read_text(encoding="utf-8").splitlines()
    for n, line in enumerate(lines):
        if not line.startswith("| Project"):
            continue
        if line.count("|") != 8:  # 7 columns -> 8 pipes; skips the 3-col table
            continue
        rows = []
        for row in lines[n + 2:]:
            if not row.startswith("|"):
                break
            rows.append(row)
        return rows
    raise SystemExit("comparison matrix not found in README.md")


def fit(draw, text, kind, max_width, start):
    """Largest size at or below `start` that keeps `text` within max_width."""
    for size in range(start, 12, -2):
        f = font(kind, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
    return font(kind, 12)


def main():
    rows = matrix_rows()
    stats = [
        (str(len(rows)), "sandboxes compared"),
        (str(sum("**deny-default**" in r for r in rows)), "deny-default egress"),
        (str(sum("| brokered " in r for r in rows)), "secrets brokered"),
    ]

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 10, H], fill=ACCENT)

    y = MARGIN
    d.text((MARGIN, y), "AWESOME LIST", font=font("bold", 22), fill=ACCENT)

    y += 58
    title = "Awesome AI Coding Sandboxes"
    tf = fit(d, title, "bold", W - 2 * MARGIN, 78)
    d.text((MARGIN, y), title, font=tf, fill=FG)

    y += tf.size + 28
    for line in ["Ranked by isolation, egress control",
                 "and secrets handling — not boot times."]:
        d.text((MARGIN, y), line, font=font("regular", 30), fill=MUTED)
        y += 42

    # stat row, pinned to the lower third under a hairline rule
    sy = H - MARGIN - 132
    d.line([MARGIN, sy - 44, W - MARGIN, sy - 44], fill="#21262d", width=2)
    for i, (value, label) in enumerate(stats):
        x = MARGIN + i * ((W - 2 * MARGIN) // 3)
        d.text((x, sy), value, font=font("bold", 62), fill=ACCENT)
        d.text((x, sy + 74), label, font=font("regular", 24), fill=MUTED)

    footer = "github.com/fhiltscher/awesome-ai-coding-sandboxes"
    ff = font("mono", 22)
    d.text((W - MARGIN - d.textlength(footer, font=ff), MARGIN + 4),
           footer, font=ff, fill=MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    kb = OUT.stat().st_size / 1024
    print(f"{OUT.relative_to(ROOT)}  {W}x{H}  {kb:.0f} KB")
    print("stats: " + ", ".join(f"{v} {l}" for v, l in stats))
    if kb > 200:
        print("warning: over 200 KB", file=sys.stderr)


if __name__ == "__main__":
    main()
