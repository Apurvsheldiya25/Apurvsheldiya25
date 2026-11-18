"""Tidies the 3D contribution graph made by github-profile-3d-contrib.

The tool's radar chart and language donut only see public repos, so they under-report.
This removes them (and the star/fork counters) and adds pixel-font labels in the freed space.

Run:  python scripts/clean_3d.py path/to/profile-pixel.svg
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))
from make_pixels import CYAN, ORANGE, PURPLE, WHITE, YELLOW, text_path, text_width  # noqa: E402

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
LEVELS = ["#1c1245", PURPLE, CYAN, YELLOW, ORANGE]


def main(path):
    tree = ET.parse(path)
    root = tree.getroot()
    texts = [t for t in root.iter(f"{{{NS}}}text") if t.text]
    count = next((t.text.strip() for t in texts if "fill-strong" in t.get("class", "")), "")
    period = next((t.text.strip() for t in texts if re.fullmatch(r"\d{4}-\d\d-\d\d / \d{4}-\d\d-\d\d", t.text.strip())), "")

    # Root children: <style>, background <rect>, the 3D bars <g>, radar <g transform>, pie <g transform>, footer <g>.
    groups = [c for c in root if c.tag == f"{{{NS}}}g"]
    bars = max(groups, key=lambda g: len(g))
    for g in groups:
        if g is not bars:
            root.remove(g)

    W = int(float(root.get("width", 1280)))
    n = re.sub(r"\D", "", count)
    big = f"{int(n):,}" if n else ""
    title, sub = "CONTRIBUTION CITY", "ONE TOWER PER DAY - PRIVATE WORK INCLUDED"
    o = ['<g shape-rendering="crispEdges">']
    o.append(f'<path d="{text_path(title, W - 40 - text_width(title, 6), 40, 6)}" fill="{ORANGE}"/>')
    o.append(f'<path d="{text_path(sub, W - 40 - text_width(sub, 2), 100, 2)}" fill="{WHITE}" opacity=".75"/>')
    if period:
        p = period.replace(" / ", " - ")
        o.append(f'<path d="{text_path(p, W - 40 - text_width(p, 2), 124, 2)}" fill="#8a84b8"/>')
    lx = W - 40 - (text_width("LESS", 2) + 5 * 26 + text_width("MORE", 2) + 24)
    o.append(f'<path d="{text_path("LESS", lx, 156, 2)}" fill="#8a84b8"/>')
    for i, c in enumerate(LEVELS):
        o.append(f'<rect x="{lx + text_width("LESS", 2) + 12 + i * 26}" y="152" width="20" height="20" fill="{c}"/>')
    o.append(f'<path d="{text_path("MORE", W - 40 - text_width("MORE", 2), 156, 2)}" fill="#8a84b8"/>')
    if big:
        o.append(f'<path d="{text_path(big, 40, 650, 10)}" fill="{YELLOW}"/>')
        o.append(f'<path d="{text_path("CONTRIBUTIONS - LAST 12 MONTHS", 40, 735, 3)}" fill="{WHITE}" opacity=".85"/>')
    o.append("</g>")

    out = ET.tostring(root, encoding="unicode")
    out = out.replace("</svg>", "".join(o) + "</svg>")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(path, "cleaned:", big, period)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
