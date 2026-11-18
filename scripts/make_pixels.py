"""Generates the animated pixel-art SVGs used in the profile README.

Run:  python scripts/make_pixels.py   (writes into assets/)
Pure SVG + CSS/SMIL animation, so GitHub renders it with no external services.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

NIGHT, NIGHT2 = "#070b1a", "#1a1040"
PINK, CYAN, YELLOW, GREEN, PURPLE, WHITE = "#ff4fd8", "#3df5ff", "#ffd23f", "#6bff8a", "#7c5cff", "#f4f1ff"

# ---------------------------------------------------------------- 5x7 pixel font
F = {
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    "C": [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"],
    "H": ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"],
    "J": ["  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    "S": [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"],
    "X": ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    "Y": ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    "0": [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    "3": ["#####", "   # ", "  #  ", "   # ", "    #", "#   #", " ### "],
    "4": ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    "5": ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    "6": [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    "8": [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    "@": [" ### ", "#   #", "# ###", "# # #", "# ###", "#    ", " ####"],
    "/": ["    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "],
    ">": ["#    ", " #   ", "  #  ", "   # ", "  #  ", " #   ", "#    "],
    "-": ["     ", "     ", "     ", " ### ", "     ", "     ", "     "],
    "+": ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    ".": ["     ", "     ", "     ", "     ", "     ", "     ", "  #  "],
    "*": ["     ", "  #  ", "# # #", " ### ", "# # #", "  #  ", "     "],
    ":": ["     ", "  #  ", "     ", "     ", "     ", "  #  ", "     "],
    "!": ["  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "],
    "?": [" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "],
    "&": [" ##  ", "#  # ", "# #  ", " #   ", "# # #", "#  # ", " ## #"],
    " ": ["     "] * 7,
}


def text_width(s, px):
    return len(s) * 6 * px - px


def glyph_path(ch, ox, oy, px):
    """One <path> 'd' fragment for a character (merged runs per row)."""
    d = []
    for r, row in enumerate(F[ch.upper()]):
        c = 0
        while c < 5:
            if row[c] == "#":
                start = c
                while c < 5 and row[c] == "#":
                    c += 1
                d.append(f"M{ox + start * px} {oy + r * px}h{(c - start) * px}v{px}h-{(c - start) * px}z")
            else:
                c += 1
    return "".join(d)


def text_path(s, ox, oy, px):
    return "".join(glyph_path(ch, ox + i * 6 * px, oy, px) for i, ch in enumerate(s))


def svg(w, h, body, style="", label=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'shape-rendering="crispEdges" role="img" aria-label="{label}">\n'
        f"<style>{style}\n@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>\n"
        f"{body}\n</svg>\n"
    )


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("wrote", name, len(content), "bytes")


# ---------------------------------------------------------------- hero banner
def hero():
    rnd = random.Random(25)
    W, H = 1200, 380
    parts = [
        f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{NIGHT}"/><stop offset="1" stop-color="{NIGHT2}"/></linearGradient>'
        f'<linearGradient id="name" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0" spreadMethod="reflect">'
        f'<stop offset="0" stop-color="{PINK}"/><stop offset=".5" stop-color="{YELLOW}"/><stop offset="1" stop-color="{CYAN}"/>'
        f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="1200 0" dur="6s" repeatCount="indefinite"/>'
        f"</linearGradient>"
        f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".22"/></pattern>'
        f"</defs>",
        f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
    ]
    # stars
    for _ in range(90):
        x, y = rnd.randrange(0, W, 3), rnd.randrange(0, 250, 3)
        s = rnd.choice([3, 3, 3, 6])
        col = rnd.choice([WHITE, WHITE, CYAN, YELLOW, PINK])
        parts.append(
            f'<rect class="tw" x="{x}" y="{y}" width="{s}" height="{s}" fill="{col}" '
            f'style="animation-duration:{rnd.uniform(1.6, 4.5):.2f}s;animation-delay:-{rnd.uniform(0, 4):.2f}s"/>'
        )
    # pixel moon
    cx, cy, r, p = 1060, 70, 6, 6
    for gy in range(-r, r + 1):
        for gx in range(-r, r + 1):
            if gx * gx + gy * gy <= r * r:
                col = "#f5e9c8"
                if (gx, gy) in {(-2, -2), (-1, -2), (2, 1), (3, 1), (-3, 2), (0, 3)}:
                    col = "#d9c99a"
                parts.append(f'<rect x="{cx + gx * p}" y="{cy + gy * p}" width="{p}" height="{p}" fill="{col}"/>')
    # shooting star
    parts.append(
        '<g class="shoot">'
        + "".join(f'<rect x="{-i * 6}" y="{-i * 3}" width="6" height="3" fill="{WHITE}" opacity="{1 - i * 0.15:.2f}"/>' for i in range(6))
        + "</g>"
    )
    # name with pixel shadow and drop-in letters
    name, px = "APURV SHELADIYA", 9
    nx, ny = (W - text_width(name, px)) // 2, 70
    for i, ch in enumerate(name):
        if ch == " ":
            continue
        x = nx + i * 6 * px
        parts.append(
            f'<g class="drop" style="animation-delay:{i * 0.07:.2f}s">'
            f'<path d="{glyph_path(ch, x + px, ny + px, px)}" fill="{PURPLE}" opacity=".55"/>'
            f'<path d="{glyph_path(ch, x, ny, px)}" fill="url(#name)"/></g>'
        )
    # typed subtitle loop
    sub, sp = "FOUNDER @ OPTIQAI  *  AI PRODUCT BUILDER", 4
    sw = text_width(sub, sp)
    sx, sy = (W - sw) // 2, 160
    steps = [min(k * 6 * sp, sw + sp) for k in range(len(sub) + 1)] + [sw + sp] * 30
    vals = ";".join(str(v) for v in steps)
    dur = len(steps) * 0.09
    parts.append(
        f'<clipPath id="type"><rect x="{sx}" y="{sy - 2}" height="{7 * sp + 4}" width="0">'
        f'<animate attributeName="width" values="{vals}" calcMode="discrete" dur="{dur:.2f}s" repeatCount="indefinite"/></rect></clipPath>'
        f'<path d="{text_path(sub, sx, sy, sp)}" fill="{WHITE}" clip-path="url(#type)"/>'
        f'<rect class="blink" y="{sy}" x="{sx}" width="{3 * sp}" height="{7 * sp}" fill="{GREEN}">'
        f'<animate attributeName="x" values="{";".join(str(sx + v + sp) for v in steps)}" calcMode="discrete" dur="{dur:.2f}s" repeatCount="indefinite"/></rect>'
    )
    tag, tp = "TYPESCRIPT / REACT / ELECTRON / AI UX", 3
    parts.append(f'<path d="{text_path(tag, (W - text_width(tag, tp)) // 2, 212, tp)}" fill="{CYAN}" opacity=".75"/>')
    # skyline with flickering windows
    x, ground = 0, H - 24
    while x < W:
        bw = rnd.choice([48, 60, 72, 84, 96])
        bh = rnd.choice([48, 60, 72, 90, 108, 126])
        shade = rnd.choice(["#120a2e", "#1c1245", "#160d3a"])
        parts.append(f'<rect x="{x}" y="{ground - bh}" width="{bw}" height="{bh}" fill="{shade}"/>')
        for wy in range(ground - bh + 12, ground - 12, 18):
            for wx in range(x + 12, x + bw - 12, 18):
                if rnd.random() < 0.45:
                    col = rnd.choice([YELLOW, YELLOW, CYAN, PINK])
                    cls = ' class="flick"' if rnd.random() < 0.35 else ""
                    st = f' style="animation-delay:-{rnd.uniform(0, 6):.1f}s;animation-duration:{rnd.uniform(3, 8):.1f}s"' if cls else ""
                    parts.append(f'<rect{cls}{st} x="{wx}" y="{wy}" width="6" height="6" fill="{col}" opacity=".85"/>')
        x += bw + rnd.choice([0, 6, 12])
    parts.append(f'<rect x="0" y="{ground}" width="{W}" height="24" fill="#0d0820"/>')
    for gx in range(0, W, 24):
        parts.append(f'<rect x="{gx}" y="{ground + 9}" width="12" height="3" fill="{PURPLE}" opacity=".5"/>')
    # pixel saucer crossing the sky
    ufo = ["   ###   ", "  #####  ", " ####### ", "#########", " # # # # "]
    p = 5
    u = []
    for r_, row in enumerate(ufo):
        for c_, ch in enumerate(row):
            if ch == "#":
                col = CYAN if r_ < 2 else ("#b7b2d9" if r_ < 4 else YELLOW)
                u.append(f'<rect x="{c_ * p}" y="{r_ * p}" width="{p}" height="{p}" fill="{col}"/>')
    beam = f'<path class="beam" d="M{2 * p} {5 * p}h{5 * p}l{2 * p} {6 * p}h-{9 * p}z" fill="{GREEN}" opacity=".25"/>'
    parts.append(f'<g class="ufo"><g class="bob">{beam}{"".join(u)}</g></g>')
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    style = (
        ".tw{animation:tw 3s steps(2) infinite}@keyframes tw{50%{opacity:.15}}"
        ".drop{animation:drop .6s steps(6) both}@keyframes drop{0%{transform:translateY(-140px);opacity:0}100%{transform:none;opacity:1}}"
        ".blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
        ".flick{animation:fl 5s steps(1) infinite}@keyframes fl{0%,60%{opacity:.85}61%,80%{opacity:.1}81%{opacity:.85}}"
        ".shoot{animation:sh 7s linear infinite}@keyframes sh{0%{transform:translate(1250px,10px);opacity:0}4%{opacity:1}16%{transform:translate(860px,205px);opacity:0}100%{transform:translate(860px,205px);opacity:0}}"
        ".ufo{animation:fly 16s steps(160) infinite}@keyframes fly{0%{transform:translate(-80px,250px)}100%{transform:translate(1280px,236px)}}"
        ".bob{animation:bob 1.2s steps(2) infinite}@keyframes bob{50%{transform:translateY(-5px)}}"
        ".beam{animation:bl .5s steps(1) infinite}"
    )
    save("pixel-hero.svg", svg(W, H, "\n".join(parts), style, "Apurv Sheladiya - Founder of OptiqAI, AI product builder"))


# ---------------------------------------------------------------- section titles
def label(name, text, color):
    px = 4
    w = text_width("> " + text, px) + 40
    h = 7 * px + 16
    body = (
        f'<path d="{glyph_path(">", 8, 8, px)}" fill="{GREEN}" class="blink"/>'
        f'<path d="{text_path(text, 8 + 12 * px, 8, px)}" fill="{color}"/>'
        f'<rect x="8" y="{h - 4}" width="{w - 16}" height="4" fill="{color}" opacity=".35"/>'
        f'<rect class="run" x="8" y="{h - 4}" width="24" height="4" fill="{color}"/>'
    )
    style = (
        ".blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
        f".run{{animation:run 3s steps(30) infinite}}@keyframes run{{to{{transform:translateX({w - 40}px)}}}}"
    )
    save(name, svg(w, h, body, style, text.title()))


# ---------------------------------------------------------------- player HUD
def hud():
    W, H = 1200, 300
    parts = [f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>',
             f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="none" stroke="{PURPLE}" stroke-width="6"/>',
             f'<rect x="18" y="18" width="{W - 36}" height="{H - 36}" fill="none" stroke="{PURPLE}" stroke-width="3" opacity=".4"/>']
    # avatar: little pixel builder with a laptop
    me = [
        "  ######  ",
        " ######## ",
        " #ssssss# ",
        " s#ss#ss  ",
        " ssssssss ",
        "  ssmmss  ",
        "   cccc   ",
        " cccccccc ",
        "cccccccccc",
        "cc llll cc",
        "  llllll  ",
        " LLLLLLLL ",
    ]
    cmap = {"#": "#2b1a0f", "s": "#f1c27d", "m": "#c26b5a", "c": PINK, "l": "#b7b2d9", "L": "#8a84b8"}
    p = 10
    for r_, row in enumerate(me):
        for c_, ch in enumerate(row):
            if ch in cmap:
                parts.append(f'<rect x="{60 + c_ * p}" y="{60 + r_ * p}" width="{p}" height="{p}" fill="{cmap[ch]}"/>')
    parts.append(f'<rect class="glow" x="{60 + 3 * p}" y="{60 + 10 * p}" width="{4 * p}" height="{p}" fill="{CYAN}"/>')
    parts.append(f'<path d="{text_path("PLAYER 1", 52, 205, 3)}" fill="{YELLOW}"/>')
    parts.append(f'<path class="blink" d="{text_path("READY", 70, 235, 3)}" fill="{GREEN}"/>')
    # stats
    lines = [("CLASS", "AI PRODUCT BUILDER", CYAN), ("GUILD", "OPTIQAI - FOUNDER", PINK), ("QUESTS", "OPTIQAI  SUPERCLIP  CLEBBY", YELLOW)]
    for i, (k, v, col) in enumerate(lines):
        y = 50 + i * 34
        parts.append(f'<path d="{text_path(k + ":", 220, y, 3)}" fill="#8a84b8"/>')
        parts.append(f'<path d="{text_path(v, 360, y, 3)}" fill="{col}"/>')
    # skill bars
    skills = [("TYPESCRIPT", 92, CYAN), ("REACT", 90, PINK), ("AI UX", 88, YELLOW), ("ELECTRON", 80, GREEN), ("PRODUCT", 94, PURPLE)]
    bx, bw = 360, 420
    for i, (k, lvl, col) in enumerate(skills):
        y = 160 + i * 22
        parts.append(f'<path d="{text_path(k, 220, y, 2)}" fill="{WHITE}"/>')
        parts.append(f'<rect x="{bx}" y="{y - 2}" width="{bw}" height="16" fill="#1c1245"/>')
        segs = int(lvl / 100 * (bw // 12))
        for s in range(segs):
            parts.append(
                f'<rect class="seg" style="animation-delay:{0.3 + i * 0.25 + s * 0.03:.2f}s" x="{bx + 2 + s * 12}" y="{y}" width="10" height="12" fill="{col}"/>'
            )
        parts.append(f'<path d="{text_path(f"LV{lvl}", bx + bw + 14, y, 2)}" fill="{col}"/>')
    # right panel: inventory
    ix = 900
    parts.append(f'<path d="{text_path("INVENTORY", ix, 50, 3)}" fill="{YELLOW}"/>')
    items = ["TS", "RE", "VI", "TW", "SB", "EL", "GH", "AI"]
    cols = [CYAN, PINK, PURPLE, CYAN, GREEN, "#9feaf9", WHITE, YELLOW]
    for i, it in enumerate(items):
        x, y = ix + (i % 4) * 66, 84 + (i // 4) * 66
        parts.append(f'<rect x="{x}" y="{y}" width="56" height="56" fill="#1c1245" stroke="{cols[i]}" stroke-width="3"/>')
        parts.append(f'<path d="{text_path(it, x + 28 - text_width(it, 3) // 2, y + 18, 3)}" fill="{cols[i]}"/>')
    parts.append(f'<rect class="sel" x="{ix - 4}" y="80" width="64" height="64" fill="none" stroke="{WHITE}" stroke-width="3"/>')
    parts.append(f'<path d="{text_path("XP", ix, 238, 3)}" fill="{GREEN}"/>')
    parts.append(f'<rect x="{ix + 40}" y="236" width="220" height="16" fill="#1c1245"/>')
    parts.append(f'<rect class="xp" x="{ix + 42}" y="238" width="216" height="12" fill="{GREEN}"/>')
    style = (
        ".blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
        ".glow{animation:bl 1.4s steps(1) infinite}"
        ".seg{animation:pop .2s steps(1) both}@keyframes pop{from{opacity:0}to{opacity:1}}"
        ".sel{animation:sel 8s steps(1) infinite}"
        "@keyframes sel{0%{transform:translate(0,0)}12.5%{transform:translate(66px,0)}25%{transform:translate(132px,0)}37.5%{transform:translate(198px,0)}"
        "50%{transform:translate(0,66px)}62.5%{transform:translate(66px,66px)}75%{transform:translate(132px,66px)}87.5%{transform:translate(198px,66px)}}"
        ".xp{transform-box:fill-box;animation:xp 4s steps(24) infinite}@keyframes xp{0%{transform:scaleX(0)}80%,100%{transform:scaleX(1)}}"
    )
    save("pixel-hud.svg", svg(W, H, "\n".join(parts), style, "Player card: AI product builder, founder of OptiqAI"))


# ---------------------------------------------------------------- divider + footer
def divider():
    W, H, p = 1200, 18, 12
    cols = [PINK, YELLOW, CYAN, GREEN, PURPLE]
    parts = [
        f'<rect class="d" x="{i * p}" y="3" width="{p - 3}" height="{p}" fill="{cols[i % 5]}" style="animation-delay:{i * 0.04:.2f}s"/>'
        for i in range(W // p)
    ]
    style = ".d{opacity:.25;animation:wave 4s steps(4) infinite}@keyframes wave{0%,20%{opacity:.25}10%{opacity:1}}"
    save("pixel-divider.svg", svg(W, H, "\n".join(parts), style, ""))


def footer():
    W, H = 1200, 150
    parts = [f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>']
    t1, t2 = "PRESS START TO COLLABORATE", "INSERT IDEA  -  BUILD  -  SHIP  -  REPEAT"
    parts.append(f'<path class="blink" d="{text_path(t1, (W - text_width(t1, 6)) // 2, 34, 6)}" fill="{YELLOW}"/>')
    parts.append(f'<path d="{text_path(t2, (W - text_width(t2, 3)) // 2, 100, 3)}" fill="{CYAN}" opacity=".8"/>')
    # coins
    for i, x in enumerate([90, 1080]):
        parts.append(
            f'<g class="coin" style="animation-delay:{i * 0.4}s;transform-origin:{x + 15}px 60px">'
            f'<rect x="{x}" y="45" width="30" height="30" fill="{YELLOW}"/><rect x="{x + 6}" y="51" width="18" height="18" fill="#e0a800"/>'
            f'<rect x="{x + 12}" y="54" width="6" height="12" fill="{YELLOW}"/></g>'
        )
    style = (
        ".blink{animation:bl 1.2s steps(1) infinite}@keyframes bl{60%{opacity:0}}"
        ".coin{animation:spin 1s steps(4) infinite}@keyframes spin{50%{transform:scaleX(.2)}}"
    )
    save("pixel-footer.svg", svg(W, H, "\n".join(parts), style, "Press start to collaborate"))


# ---------------------------------------------------------------- desk scene
def desk():
    """Animated pixel scene: coding at night with a window, monitor, mug and cat."""
    rnd = random.Random(7)
    p, W, H = 6, 480, 360
    R = lambda x, y, w, h, c, extra="": f'<rect x="{x * p}" y="{y * p}" width="{w * p}" height="{h * p}" fill="{c}"{extra}/>'
    parts = [
        '<defs><linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#140c33"/>'
        '<stop offset="1" stop-color="#22145a"/></linearGradient>'
        f'<clipPath id="scr"><rect x="{23 * p}" y="{13 * p}" width="{34 * p}" height="{21 * p}"/></clipPath>'
        f'<clipPath id="win"><rect x="{4 * p}" y="{5 * p}" width="{14 * p}" height="{18 * p}"/></clipPath></defs>',
        f'<rect width="{W}" height="{H}" fill="url(#wall)"/>',
    ]
    # window with sky, moon, stars, distant city
    parts.append(R(3, 4, 16, 20, "#3a2a7a"))
    parts.append(R(4, 5, 14, 18, "#0a0f2a"))
    g = ['<g clip-path="url(#win)">']
    for _ in range(14):
        x, y = rnd.randint(4, 17), rnd.randint(5, 14)
        g.append(R(x, y, 1, 1, WHITE, f' class="tw" style="animation-delay:-{rnd.uniform(0, 3):.1f}s"'))
    g.append(R(13, 7, 3, 3, "#f5e9c8"))
    g.append(R(13, 7, 1, 1, "#0a0f2a"))
    for x in range(4, 18, 2):
        hgt = rnd.randint(3, 7)
        g.append(R(x, 23 - hgt, 2, hgt, "#1c1245"))
        if rnd.random() < 0.6:
            g.append(R(x, 23 - hgt + 1, 1, 1, YELLOW, ' class="fl"'))
    g.append("</g>")
    parts += g
    parts.append(R(10, 5, 1, 18, "#3a2a7a"))
    parts.append(R(4, 13, 14, 1, "#3a2a7a"))
    # shelf with books + plant
    parts.append(R(60, 10, 16, 1, "#4a3420"))
    for i, c in enumerate([PINK, CYAN, YELLOW, PURPLE, GREEN]):
        parts.append(R(61 + i * 2, 5 + (i % 2), 2, 5 - (i % 2), c))
    parts.append(R(72, 8, 3, 2, "#a0522d"))
    parts.append(f'<g class="sway" style="transform-origin:{73.5 * p}px {8 * p}px">' + R(73, 5, 1, 3, GREEN) + R(72, 5, 1, 1, GREEN) + R(74, 4, 1, 2, GREEN) + "</g>")
    # desk
    parts.append(R(0, 44, 80, 2, "#5b3a8a"))
    parts.append(R(0, 46, 80, 1, "#3a2466"))
    parts.append(R(4, 47, 2, 13, "#3a2466"))
    parts.append(R(74, 47, 2, 13, "#3a2466"))
    # lamp glow
    parts.append(f'<ellipse class="glow" cx="{66 * p}" cy="{44 * p}" rx="{10 * p}" ry="{2 * p}" fill="{YELLOW}" opacity=".18"/>')
    parts += [R(65, 43, 4, 1, "#2a2a40"), R(66, 33, 1, 10, "#2a2a40"), R(63, 30, 6, 3, "#ff8a3d"), R(64, 33, 4, 1, YELLOW, ' class="glow"')]
    # monitor
    parts += [R(22, 12, 36, 23, "#2a2a40"), R(23, 13, 34, 21, "#05081a"), R(38, 35, 4, 6, "#2a2a40"), R(33, 41, 14, 3, "#2a2a40")]
    lines, y = [], 0
    for i in range(40):
        ind = [0, 2, 2, 4, 4, 6][rnd.randrange(6)]
        x = 24 + ind
        segs = rnd.randint(1, 3)
        for _ in range(segs):
            w = rnd.randint(2, 6)
            if x + w > 55:
                break
            lines.append(f'<rect x="{x * p}" y="{(14 + y) * p}" width="{w * p}" height="{p - 2}" fill="{rnd.choice([PINK, CYAN, YELLOW, GREEN, PURPLE, WHITE])}"/>')
            x += w + 1
        y += 2 if rnd.random() < 0.85 else 4
    scroll = y * p
    parts.append(f'<g clip-path="url(#scr)"><g class="code">{"".join(lines)}</g></g>')
    parts.append(R(24, 32, 2, 1, GREEN, ' class="blink"'))
    parts.append(R(56, 33, 1, 1, GREEN, ' class="blink"'))
    # mug with steam
    parts += [R(52, 40, 4, 4, WHITE), R(56, 41, 1, 2, WHITE), R(52, 40, 4, 1, "#6b3e26")]
    for i in range(3):
        parts.append(R(53 + (i % 2), 38, 1, 1, "#b7b2d9", f' class="steam" style="animation-delay:{i * 0.6:.1f}s"'))
    # cat sitting on desk, tail wags (two frames)
    cat = [(9, 36, 6, 7), (10, 34, 4, 3), (9, 33, 1, 2), (13, 33, 1, 2)]
    for x, y_, w, h in cat:
        parts.append(R(x, y_, w, h, "#e8e6f0"))
    parts += [R(11, 35, 1, 1, GREEN, ' class="blink2"'), R(13, 35, 1, 1, GREEN, ' class="blink2"'), R(12, 36, 1, 1, PINK)]
    parts.append('<g class="tA">' + R(15, 40, 3, 1, "#e8e6f0") + R(17, 37, 1, 3, "#e8e6f0") + "</g>")
    parts.append('<g class="tB">' + R(15, 42, 4, 1, "#e8e6f0") + R(18, 40, 1, 2, "#e8e6f0") + "</g>")
    # developer (back view) on chair, nodding while typing
    dev = (
        R(34, 32, 12, 3, "#2b1a0f") + R(33, 35, 14, 6, "#2b1a0f") + R(34, 41, 12, 1, "#f1c27d")
        + R(30, 42, 20, 6, PINK) + R(28, 45, 24, 10, PINK) + R(39, 42, 2, 4, "#c23aa8")
        + R(36, 39, 1, 3, CYAN) + R(43, 39, 1, 3, CYAN) + R(35, 38, 10, 1, CYAN)
    )
    parts.append(f'<g class="nod">{dev}</g>')
    parts += [R(29, 50, 22, 10, "#2a2a40"), R(30, 51, 20, 8, "#3a3a58")]
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#sc)"/>')
    parts.insert(0, '<defs><pattern id="sc" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".18"/></pattern></defs>')
    style = (
        ".tw{animation:tw 2.5s steps(2) infinite}@keyframes tw{50%{opacity:.15}}"
        ".fl{animation:tw 4s steps(1) infinite}"
        ".blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
        ".blink2{animation:ey 4s steps(1) infinite}@keyframes ey{0%,92%{opacity:1}93%,100%{opacity:0}}"
        f".code{{animation:code 14s steps({scroll // p}) infinite}}@keyframes code{{to{{transform:translateY(-{scroll - 18 * p}px)}}}}"
        ".steam{animation:st 1.8s steps(6) infinite}@keyframes st{0%{transform:translateY(0);opacity:.9}100%{transform:translateY(-36px);opacity:0}}"
        ".tA{animation:tA 1.2s steps(1) infinite}@keyframes tA{50%{opacity:0}}"
        ".tB{opacity:0;animation:tB 1.2s steps(1) infinite}@keyframes tB{50%{opacity:1}}"
        ".nod{animation:nod .8s steps(1) infinite}@keyframes nod{50%{transform:translateY(3px)}}"
        ".glow{animation:gl 3s steps(3) infinite}@keyframes gl{50%{opacity:.35}}"
        ".sway{animation:sw 3s steps(2) infinite}@keyframes sw{50%{transform:rotate(8deg)}}"
    )
    save("pixel-desk.svg", svg(W, H, "\n".join(parts), style, "Pixel art: coding late at night with a cat on the desk"))


if __name__ == "__main__":
    desk()
    hero()
    divider()
    footer()
