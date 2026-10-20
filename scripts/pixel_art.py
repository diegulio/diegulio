"""Pixel-art SVG generator for diegulio's README prototypes.

usage: python3 scripts/pixel_art.py statics/pixel <avatar.png>
(avatar.png = the 128px avatar from diegulio.github.io/avatar.png)
Every image is drawn on a logical pixel grid and emitted as one <path> per
colour, so files stay small and render crisp on GitHub (SVG CSS animations
work inside <img>).
"""
import math
import os
import random
import sys

from PIL import Image

OUT = sys.argv[1]
AVATAR = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- palette
INK = "#20251f"
PAPER = "#f4f3ed"
MUTED = "#9aa196"
LIME = "#d0f875"
LIME_D = "#7f9b33"
ORANGE = "#e67847"
ORANGE_D = "#a9512c"
BOARD = "#2b3a30"
BOARD_HI = "#3f5244"
BOARD_LO = "#18211b"

# ---------------------------------------------------------------- 5x7 font
F = {
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    "C": [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"],
    "H": ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "I": [" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "J": ["  ###", "   # ", "   # ", "   # ", "#  # ", "#  # ", " ##  "],
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
    "W": ["#   #", "#   #", "#   #", "# # #", "# # #", "# # #", " # # "],
    "X": ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    "Y": ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    "0": [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    "3": ["#### ", "    #", "    #", " ### ", "    #", "    #", "#### "],
    "4": ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    "5": ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    "6": [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    "8": [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    " ": ["   "] * 7,
    ".": [" ", " ", " ", " ", " ", " ", "#"],
    ",": ["  ", "  ", "  ", "  ", "  ", " #", "# "],
    ":": [" ", " ", "#", " ", " ", "#", " "],
    "!": ["#", "#", "#", "#", "#", " ", "#"],
    "'": ["#", "#", " ", " ", " ", " ", " "],
    "-": ["   ", "   ", "   ", "###", "   ", "   ", "   "],
    "/": ["    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "],
    ">": ["#   ", " #  ", "  # ", "   #", "  # ", " #  ", "#   "],
    "<": ["   #", "  # ", " #  ", "#   ", " #  ", "  # ", "   #"],
    "_": ["     ", "     ", "     ", "     ", "     ", "     ", "#####"],
    "+": ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    "?": [" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "],
    "(": [" ##", "#  ", "#  ", "#  ", "#  ", "#  ", " ##"],
    ")": ["## ", "  #", "  #", "  #", "  #", "  #", "## "],
    "&": [" ##  ", "#  # ", "# #  ", " #   ", "# # #", "#  # ", " ## #"],
    "*": ["     ", "# # #", " ### ", "#####", " ### ", "# # #", "     "],
    "#": [" # # ", " # # ", "#####", " # # ", "#####", " # # ", " # # "],
    "=": ["     ", "     ", "#####", "     ", "#####", "     ", "     "],
    "^": [" ### ", "#####", "#####", " ### ", "  #  ", "     ", "     "],  # heart-ish
    "~": ["#    ", "##   ", "###  ", "#### ", "###  ", "##   ", "#    "],  # play cursor
    "|": ["#"] * 7,
    "@": [" ### ", "#   #", "# ###", "# # #", "# ###", "#    ", " ####"],
}


def text_w(s, scale=1, sp=1):
    s = s.upper()
    return sum(len(F.get(c, F["?"])[0]) * scale for c in s) + sp * scale * (len(s) - 1)


class Layer:
    def __init__(self):
        self.px = {}

    def set(self, x, y, c):
        if c:
            self.px[(int(x), int(y))] = c

    def rect(self, x, y, w, h, c):
        for yy in range(int(y), int(y + h)):
            for xx in range(int(x), int(x + w)):
                self.set(xx, yy, c)

    def frame(self, x, y, w, h, c):
        self.rect(x, y, w, 1, c)
        self.rect(x, y + h - 1, w, 1, c)
        self.rect(x, y, 1, h, c)
        self.rect(x + w - 1, y, 1, h, c)

    def text(self, s, x, y, c, scale=1, sp=1, shadow=None):
        if shadow:
            self.text(s, x + scale if scale > 1 else x + 1, y + (scale if scale > 1 else 1), shadow, scale, sp)
        for ch in s.upper():
            g = F.get(ch, F["?"])
            for r, row in enumerate(g):
                for k, v in enumerate(row):
                    if v == "#":
                        self.rect(x + k * scale, y + r * scale, scale, scale, c)
            x += len(g[0]) * scale + sp * scale
        return x

    def text_c(self, s, cx, y, c, scale=1, sp=1, shadow=None):
        return self.text(s, cx - text_w(s, scale, sp) // 2, y, c, scale, sp, shadow)

    def sprite(self, rows, x, y, cmap, scale=1, flip=False):
        w = max(len(r) for r in rows)
        for r, row in enumerate(rows):
            row = row.ljust(w, ".")
            if flip:
                row = row[::-1]
            for k, v in enumerate(row):
                if v in cmap and cmap[v]:
                    self.rect(x + k * scale, y + r * scale, scale, scale, cmap[v])

    def svg(self, attrs=""):
        # merge horizontal runs, then stack identical runs vertically
        rows = {}
        for (x, y), c in self.px.items():
            rows.setdefault(y, {})[x] = c
        runs = []
        for y in sorted(rows):
            xs = sorted(rows[y])
            start = prev = xs[0]
            col = rows[y][start]
            for x in xs[1:] + [None]:
                c = rows[y].get(x) if x is not None else None
                if x is not None and x == prev + 1 and c == col:
                    prev = x
                    continue
                runs.append((start, y, prev - start + 1, col))
                if x is not None:
                    start = prev = x
                    col = c
        open_ = {}
        boxes = []
        for x, y, w, c in runs:
            key = (x, w, c)
            if key in open_ and open_[key][0] + open_[key][1] == y:
                open_[key][1] += 1
            else:
                if key in open_:
                    boxes.append((x, open_[key][0], w, open_[key][1], c))
                open_[key] = [y, 1]
        for (x, w, c), (y, h) in open_.items():
            boxes.append((x, y, w, h, c))
        by_col = {}
        for x, y, w, h, c in boxes:
            by_col.setdefault(c, []).append(f"M{x} {y}h{w}v{h}h-{w}z")
        paths = "".join(f'<path fill="{c}" d="{"".join(d)}"/>' for c, d in by_col.items())
        return f"<g {attrs}>{paths}</g>" if attrs else paths


BASE_CSS = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def doc(name, W, H, scale, body, title, css="", defs=""):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*scale}" height="{H*scale}" '
        f'shape-rendering="crispEdges" role="img" aria-label="{title}"><title>{title}</title>'
        f"<style>{css}{BASE_CSS}</style>{defs}{body}</svg>"
    )
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)
    print(f"{name:28s} {len(svg)/1024:6.1f} KB")


# ---------------------------------------------------------------- sprites
ICONS = {
    "eye": ([
        "", "", "",
        ".....kkkkkk.....",
        "...kkwwwwwwkk...",
        "..kwwwbbbbwwwk..",
        ".kwwwbbppbbwwwk.",
        "kwwwwbppgpbwwwwk",
        "kwwwwbppppbwwwwk",
        ".kwwwbbppbbwwwk.",
        "..kwwwbbbbwwwk..",
        "...kkwwwwwwkk...",
        ".....kkkkkk.....",
    ], {"k": INK, "w": PAPER, "b": "#4f8fb8", "p": INK, "g": PAPER}),
    "chair": ([
        "",
        "....kkkkkkkk....",
        "....kooooook....",
        "....kooooook....",
        "....kooooook....",
        "....kooooook....",
        "....kkkkkkkk....",
        ".....k....k.....",
        "..kkkkkkkkkkkk..",
        "..kooooooooook..",
        "..kkkkkkkkkkkk..",
        ".......kk.......",
        ".......kk.......",
        "....kkkkkkkk....",
        "...k..k..k..k...",
        "..kk.kk..kk.kk..",
    ], {"k": INK, "o": ORANGE}),
    "pasta": ([
        "",
        ".....s..s..s....",
        "......s..s..s...",
        ".....s..s..s....",
        "....yyyryyyy....",
        "..yyrmrrryyyyy..",
        ".yyyrrrrrryymyy.",
        "kkkkkkkkkkkkkkkk",
        "kwwwwwwwwwwwwwwk",
        ".kwwwwwwwwwwwwk.",
        ".kwwwwwwwwwwwwk.",
        "..kwwwwwwwwwwk..",
        "...kkwwwwwwkk...",
        ".....kkkkkk.....",
    ], {"k": INK, "w": PAPER, "y": "#f2c94c", "r": "#d4483b", "m": "#7a3b22", "s": MUTED}),
    "resume": ([
        "",
        "...kkkkkkkk.....",
        "...kwwwwwwkk....",
        "...kwbbwwwwkk...",
        "...kwbbwgggwk...",
        "...kwwwwwwwwk...",
        "...kwggggggwk...",
        "...kwwwwwwwwk...",
        "...kwllllllwk...",
        "...kwwwwwwwwk...",
        "...kwgggggwwk...",
        "...kwwwwwwwwk...",
        "...kwggggwwwk...",
        "...kwwwwwwwwk...",
        "...kkkkkkkkkk...",
    ], {"k": INK, "w": PAPER, "b": "#4f8fb8", "g": MUTED, "l": LIME}),
    "dog": ([
        "", "",
        ".k.kk........kk.",
        ".kkbbk......kbbk",
        ".kbbbkkkkkkkkbbbk"[:16],
        ".kboooooooooooobk"[:16],
        "..kooppooooppook",
        "..koooooooooook.",
        "..koowwwwwwwook.",
        "...kowwwkkwwwok.",
        "...kowwwwwwwwok.",
        "....kowwrrwwok..",
        ".....kkkkkkkk...",
    ], {"k": INK, "b": "#8a4b2a", "o": "#d98b4a", "w": PAPER, "p": INK, "r": "#d4483b"}),
    "alien": ([
        "", "",
        "....kkkkkkkk....",
        "...kggggggggk...",
        "..kggggggggggk..",
        "..kgwwggggwwgk..",
        "..kgwkggggwkgk..",
        "..kggggggggggk..",
        "..kggkkkkkkggk..",
        "...kggggggggk...",
        "..kgk.kggk.kgk..",
        "..kk..k..k..kk..",
    ], {"k": INK, "g": LIME, "w": PAPER}),
}

SPORT = {
    "run": [
        "......kk....",
        "......kk....",
        "....kkkk....",
        "...k.kk.k...",
        "..k..kk..k..",
        ".....kk.....",
        "....k..k....",
        "...k....k...",
        "..k......k..",
        "..k.......k.",
    ],
    "swim": [
        "............",
        ".......kk...",
        ".kk....kk...",
        "..kk..kkk...",
        "...kkkkk....",
        "............",
        "bb..bb..bb..",
        ".bbbbbbbbbbb",
        "............",
        ".bb..bb..bb.",
    ],
    "bike": [
        "............",
        "........k...",
        "...kkkkkk...",
        "....k..k....",
        ".kkk....kkk.",
        "k...kk.k...k",
        "k...k..k...k",
        ".kkk....kkk.",
        "............",
        "............",
    ],
    "gym": [
        "............",
        "............",
        "kk......kk..",
        "kk......kk..",
        "kkkkkkkkkk..",
        "kk......kk..",
        "kk......kk..",
        "............",
        "............",
        "............",
    ],
}

for name, (rows, cmap) in ICONS.items():
    L = Layer()
    L.sprite(rows, 0, 0, cmap)
    doc(f"icon-{name}.svg", 16, 16, 3, L.svg(), name)

# ---------------------------------------------------------------- avatar
def avatar_layer(size, ox, oy):
    im = Image.open(AVATAR).convert("RGB").resize((size, size), Image.NEAREST)
    im = im.quantize(colors=20, method=Image.MEDIANCUT).convert("RGB")
    L = Layer()
    for y in range(size):
        for x in range(size):
            L.set(ox + x, oy + y, "#%02x%02x%02x" % im.getpixel((x, y)))
    return L


# ================================================================ A: Santiago
def banner_a():
    W, H = 400, 120
    rnd = random.Random(7)
    bg = Layer()
    SKY = ["#8fc4da", "#a6d2e3", "#c2e1ea"]
    for y in range(92):
        band = 0 if y < 22 else 1 if y < 48 else 2
        for x in range(W):
            c = SKY[band]
            if y in (22, 23) and (x + y) % 2 == 0:
                c = SKY[0]
            if y in (48, 49) and (x + y) % 2 == 0:
                c = SKY[1]
            bg.set(x, y, c)
    # sun
    for y in range(8, 40):
        for x in range(300, 336):
            d = math.hypot(x - 318, y - 22)
            if d <= 8:
                bg.set(x, y, "#f8eaa6")
            elif d <= 10 and (x + y) % 2 == 0:
                bg.set(x, y, "#f6f0cf")
    # far andes
    for x in range(W):
        top = int(46 + 9 * math.sin(x * 0.045 + 1.2) + 6 * math.sin(x * 0.11 + 0.3) + 3 * math.sin(x * 0.27))
        nxt = 46 + 9 * math.sin((x + 1) * 0.045 + 1.2) + 6 * math.sin((x + 1) * 0.11 + 0.3) + 3 * math.sin((x + 1) * 0.27)
        shade = nxt > top
        snow = 38 + int(2 * math.sin(x * 0.7))
        for y in range(top, 92):
            if y < snow:
                c = "#cfd8dd" if shade else "#f3f6f3"
            else:
                c = "#8696a1" if shade else "#9aaab4"
            bg.set(x, y, c)
    # near ridge
    for x in range(W):
        top = int(64 + 6 * math.sin(x * 0.06 + 4) + 4 * math.sin(x * 0.15 + 1))
        for y in range(top, 92):
            bg.set(x, y, "#7d8d86" if (x // 3 + y) % 7 else "#728179")
    # San Cristobal
    cx = 236
    for x in range(cx - 46, cx + 47):
        top = int(56 + 0.021 * (x - cx) ** 2)
        for y in range(top, 92):
            c = "#6c9150" if x > cx + 3 else "#7fa35e"
            if rnd.random() < 0.06 and y > top + 2:
                c = "#557a3e"
            bg.set(x, y, c)
    # zig-zag path up the hill
    for i, y in enumerate(range(58, 90)):
        bg.set(cx - 8 + abs((i % 16) - 8) * 2 - 4, y, "#c9b48a")
    bg.rect(cx - 1, 47, 3, 9, PAPER)
    bg.rect(cx - 2, 50, 5, 1, PAPER)
    bg.rect(cx, 45, 1, 2, PAPER)
    # chilean flag
    bg.rect(196, 66, 1, 24, "#4a514b")
    bg.rect(197, 66, 3, 3, "#1f4fa3")
    bg.set(198, 67, PAPER)
    bg.rect(200, 66, 5, 3, PAPER)
    bg.rect(197, 69, 8, 3, "#d52b1e")
    # city
    x = 0
    cols = ["#a9b6bb", "#97a5ab", "#bac5c8", "#8c9aa1"]
    while x < W:
        w = rnd.randint(7, 15)
        h = rnd.randint(5, 17)
        if 150 < x < 215:
            h = rnd.randint(4, 8)
        c = rnd.choice(cols)
        bg.rect(x, 92 - h, w, h, c)
        for wy in range(92 - h + 2, 91, 3):
            for wx in range(x + 2, x + w - 1, 3):
                bg.set(wx, wy, "#dfe6e8")
        x += w + rnd.randint(0, 2)
    # costanera tower
    for y in range(24, 92):
        inset = max(0, 7 - (y - 24)) // 2
        for xx in range(352 + inset, 366 - inset):
            bg.set(xx, y, "#b8d0dc" if (xx - 352) % 4 == 1 else "#88a9bb")
    bg.rect(358, 16, 2, 8, "#4a514b")
    # ground, track, road
    bg.rect(0, 92, W, 4, "#8dbb5c")
    for x in range(0, W, 5):
        bg.set(x + rnd.randint(0, 3), 91, "#79a64b")
    bg.rect(0, 96, W, 12, "#c87553")
    bg.rect(0, 96, W, 1, "#a95f40")
    bg.rect(0, 107, W, 1, "#a95f40")
    for x in range(0, W, 8):
        bg.rect(x, 101, 4, 1, "#e9bba0")
    bg.rect(0, 108, W, 4, "#9cc56a")
    bg.rect(0, 112, W, 8, "#565f5b")
    for x in range(2, W, 12):
        bg.rect(x, 115, 6, 1, "#e9d27a")
    for x in (162, 286, 392):
        bg.rect(x, 78, 1, 14, "#3a4440")
        bg.rect(x - 1, 76, 3, 2, "#f6e7a1")
    # sign board
    bx, by, bw, bh = 10, 10, 132, 50
    for px in (28, 122):
        bg.rect(px, by + bh, 3, 92 - by - bh, "#3c463f")
        bg.rect(px, by + bh, 1, 92 - by - bh, "#525e55")
    bg.rect(bx, by, bw, bh, BOARD)
    bg.frame(bx, by, bw, bh, BOARD_LO)
    bg.rect(bx + 1, by + 1, bw - 2, 1, BOARD_HI)
    # rooftop plants like the lab building
    for i, px in enumerate((18, 48, 98, 128)):
        bg.rect(px, by - 3, 5, 3, ORANGE_D)
        bg.rect(px + 1, by - 6, 3, 3, "#5d8a46" if i % 2 else "#6fa046")
    bg.text_c("DIEGULIO", bx + bw // 2, by + 7, LIME, scale=2, shadow=LIME_D)
    bg.text_c("DATA SCIENTIST", bx + bw // 2, by + 27, PAPER)
    end = bg.text_c("SANTIAGO, CL", bx + bw // 2 - 3, by + 37, MUTED)

    fx = Layer()
    cursor = Layer()
    cursor.rect(end + 1, by + 43, 5, 1, ORANGE)
    # lit windows that flicker
    win = [Layer(), Layer(), Layer()]
    for (x, y), c in list(bg.px.items()):
        if c == "#dfe6e8" and rnd.random() < 0.18:
            win[rnd.randint(0, 2)].set(x, y, "#f4d77a")
    # clouds (drawn twice for a seamless loop)
    cloud = [".....wwww.......", "...wwwwwwww.www.", ".wwwwwwwwwwwwwww", "wwwwwwwwwwwwwwww", ".sssssssssssssss"]
    clouds = Layer()
    for ox in (0, W):
        clouds.sprite(cloud, ox + 160, 12, {"w": "#fbfcfa", "s": "#dde9ee"})
        clouds.sprite(cloud, ox + 260, 30, {"w": "#fbfcfa", "s": "#dde9ee"}, flip=True)
        clouds.sprite(cloud[:4], ox + 40, 66, {"w": "#eef4f5"})
    birds = [Layer(), Layer()]
    for bx_, by_ in ((270, 18), (280, 14), (288, 20)):
        birds[0].sprite(["k.k", ".k."], bx_, by_, {"k": "#4a514b"})
        birds[1].sprite(["kkk"], bx_, by_ + 1, {"k": "#4a514b"})
    rcm = {"h": INK, "s": "#e0b18c", "o": ORANGE, "d": BOARD, "w": PAPER}
    runner = [Layer(), Layer()]
    runner[0].sprite(["..hhh...", "..hss...", "..sss...", ".oooo...", "s.oo.s..", "..oo....", "..dd....", ".d..d...", "s....s..", "w.....w."], 0, 97, rcm)
    runner[1].sprite(["..hhh...", "..hss...", "..sss...", "..ooo...", "..oos...", "..oo....", "..dd....", "..dd....", "..s.s...", "..ww.w.."], 0, 97, rcm)
    bike = Layer()
    bike.sprite([
        ".......hh......", ".......hs......", "......ooo......", ".....oo..s.....",
        "....dd...k.....", "...k.dkkkk.....", ".kkk..d..kkk...", "k...k.k.k...k..",
        "k...k...k...k..", ".kkk.....kkk...",
    ], 0, 109, {"h": INK, "s": "#e0b18c", "o": LIME_D, "d": BOARD, "k": INK})

    body = bg.svg() + clouds.svg('class="clouds"')
    body += "".join(w.svg(f'class="win w{i}"') for i, w in enumerate(win))
    body += f'<g class="birds">{birds[0].svg("class=\"f0\"")}{birds[1].svg("class=\"f1\"")}</g>'
    body += cursor.svg('class="blink"')
    body += f'<g class="runner">{runner[0].svg("class=\"f0\"")}{runner[1].svg("class=\"f1\"")}</g>'
    body += bike.svg('class="bike"')
    css = (
        f".clouds{{animation:drift 90s steps({W}) infinite}}"
        f"@keyframes drift{{to{{transform:translateX(-{W}px)}}}}"
        ".f0{animation:fa .5s infinite}.f1{animation:fb .5s infinite}"
        "@keyframes fa{0%,49%{opacity:1}50%,100%{opacity:0}}@keyframes fb{0%,49%{opacity:0}50%,100%{opacity:1}}"
        ".birds{animation:fly 40s steps(160) infinite}@keyframes fly{to{transform:translateX(-160px)}}"
        ".blink{animation:fa 1s infinite}"
        ".win{opacity:1}.w0{animation:fa 7s infinite}.w1{animation:fb 11s infinite}"
        f".runner{{animation:run 16s steps(220) infinite}}@keyframes run{{from{{transform:translateX(-12px)}}to{{transform:translateX({W+12}px)}}}}"
        f".bike{{animation:ride 9s steps(210) infinite;animation-delay:-3s}}@keyframes ride{{from{{transform:translateX(-20px)}}to{{transform:translateX({W+20}px)}}}}"
    )
    doc("a-banner.svg", W, H, 2, body, "diegulio: data scientist in Santiago, pixel art banner", css)


# ================================================================ B: RPG sheet
def banner_b():
    W, H = 400, 150
    bg = Layer()
    bg.rect(0, 0, W, H, INK)
    bg.frame(2, 2, W - 4, H - 4, PAPER)
    bg.frame(4, 4, W - 8, H - 8, "#5b6258")
    # avatar
    bg.rect(12, 12, 52, 52, PAPER)
    bg.rect(14, 14, 48, 48, INK)
    av = avatar_layer(44, 16, 16)
    bg.text("LVL UP!", 14, 70, ORANGE)
    bg.text("EXP", 14, 82, MUTED)
    bg.rect(14, 91, 48, 5, "#3a4237")
    exp = Layer()
    exp.rect(14, 91, 46, 5, LIME)
    # identity
    bg.text("DIEGO MACHADO", 76, 14, PAPER, scale=2, shadow="#4a5147")
    rows = [("CLASS", "DATA SCIENTIST"), ("ALSO", "TEACHER @ USACH"), ("HOME", "SANTIAGO, CL"), ("MOTTO", "BUILD TO LEARN")]
    for i, (k, v) in enumerate(rows):
        y = 38 + i * 11
        bg.text(k, 76, y, MUTED)
        bg.text(v, 116, y, LIME if i == 0 else PAPER)
    # skills
    sx = 262
    bg.text("SKILL TREE", sx, 14, ORANGE)
    stats = [("ML", 9), ("TIME", 7), ("NLP", 8), ("VISION", 8), ("AUDIO", 6), ("LLMS", 9)]
    bars = Layer()
    for i, (k, v) in enumerate(stats):
        y = 28 + i * 11
        bg.text(k, sx, y, PAPER)
        for s in range(10):
            bg.rect(sx + 40 + s * 9, y, 7, 7, "#3a4237")
            if s < v:
                bars.rect(sx + 40 + s * 9, y, 7, 7, LIME if v >= 8 else "#a9c860")
    # side quests
    bg.rect(12, 104, W - 24, 1, "#5b6258")
    bg.text("SIDE QUESTS", 14, 112, ORANGE)
    q = 100
    for name, label in (("run", "RUN"), ("swim", "SWIM"), ("bike", "BIKE"), ("gym", "GYM")):
        bg.sprite(SPORT[name], q, 108, {"k": PAPER, "b": "#7fc1d8"}, scale=2 if False else 1)
        bg.text(label, q + 15, 112, PAPER)
        q += 15 + text_w(label) + 18
    bg.text("STAMINA", 14, 128, MUTED)
    bg.rect(64, 128, 120, 7, "#3a4237")
    stam = Layer()
    stam.rect(64, 128, 120, 7, ORANGE)
    stam.rect(64, 128, 120, 1, "#f19a72")
    bg.text("COFFEE", 200, 128, MUTED)
    bg.rect(244, 128, 140, 7, "#3a4237")
    cof = Layer()
    cof.rect(244, 128, 98, 7, "#c79a6b")
    cof.rect(244, 128, 98, 1, "#e0bb90")
    cur = Layer()
    cur.text("~", sx - 8, 14, LIME)
    body = bg.svg() + av.svg() + exp.svg('class="grow"') + bars.svg('class="grow d1"')
    body += stam.svg('class="grow d2"') + cof.svg('class="grow d3"') + cur.svg('class="blink"')
    body += Layer().svg()
    css = (
        ".grow{transform-box:fill-box;transform-origin:left;animation:grow 1.4s steps(14) both}"
        ".d1{animation-delay:.3s}.d2{animation-delay:.6s}.d3{animation-delay:.9s}"
        "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        ".blink{animation:bl 1s infinite}@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}"
    )
    doc("b-sheet.svg", W, H, 2, body, "Diego Machado character sheet: data scientist, skill tree and side quests", css)


# ================================================================ C: arcade
ALIENS = {
    "bug": (["..k....k..", "...k..k...", "..kkkkkk..", ".kk.kk.kk.", "kkkkkkkkkk", "k.kkkkkk.k", "k.k....k.k", "...kk.kk.."],
            ["..k....k..", "k..k..k..k", "k.kkkkkk.k", "kkk.kk.kkk", "kkkkkkkkkk", "..kkkkkk..", "..k....k..", ".k......k."]),
    "head": (["...kkkk...", ".kkkkkkkk.", "kkkkkkkkkk", "kk..kk..kk", "kkkkkkkkkk", "..kk..kk..", ".kk.kk.kk.", "k........k"],
             ["...kkkk...", ".kkkkkkkk.", "kkkkkkkkkk", "kk..kk..kk", "kkkkkkkkkk", "...kkkk...", "..kk..kk..", "...k..k..."]),
    "squid": (["....kk....", "...kkkk...", "..kkkkkk..", ".kk.kk.kk.", ".kkkkkkkk.", "...k..k...", "..k.kk.k..", ".k.k..k.k."],
              ["....kk....", "...kkkk...", "..kkkkkk..", ".kk.kk.kk.", ".kkkkkkkk.", "..k.kk.k..", ".k......k.", "..k....k.."]),
}


def banner_c():
    W, H = 400, 140
    rnd = random.Random(3)
    bg = Layer()
    bg.rect(0, 0, W, H, "#0d1310")
    stars = [Layer(), Layer()]
    for _ in range(70):
        stars[rnd.randint(0, 1)].set(rnd.randint(0, W - 1), rnd.randint(14, 120), rnd.choice(["#3b4a40", "#56685b", "#7e8f80"]))
    # hud
    bg.text("1UP", 10, 6, ORANGE)
    bg.text("DIEGULIO", 32, 6, PAPER)
    bg.text_c("HI-SCORE 2026", W // 2, 6, LIME)
    bg.text("CREDIT 01", W - 10 - text_w("CREDIT 01"), 6, PAPER)
    # title
    bg.text_c("DIEGULIO", W // 2, 62, LIME, scale=3, shadow=LIME_D)
    bg.text_c("DATA SCIENCE  -  AI  -  LLMS", W // 2, 90, PAPER)
    press = Layer()
    press.text_c("PRESS START TO READ THE BLOG", W // 2, 106, ORANGE)
    # aliens, two frames
    fr = [Layer(), Layer()]
    kinds = [("squid", "#7fd6e0"), ("head", "#f0c27b"), ("bug", LIME)]
    for r, (kind, col) in enumerate(kinds):
        for c in range(9):
            x = 104 + c * 18
            y = 20 + r * 12
            for f in (0, 1):
                fr[f].sprite(ALIENS[kind][f], x, y, {"k": col})
    # player + shots
    ship = Layer()
    ship.sprite(["......k......", ".....kkk.....", ".....kkk.....", ".kkkkkkkkkkk.", "kkkkkkkkkkkkk", "kkkkkkkkkkkkk"], 0, 124, {"k": ORANGE})
    shot = Layer()
    shot.rect(6, 118, 1, 4, PAPER)
    bg.rect(0, 131, W, 1, LIME_D)
    # bunkers made of tiny data bars
    for bx in (60, 150, 240, 330):
        for i, h in enumerate((3, 5, 4, 6, 2, 5, 3)):
            bg.rect(bx + i * 2, 118 - h, 2, h, "#3f6b4a")
    scan = '<rect width="100%" height="100%" fill="url(#scan)"/>'
    defs = '<defs><pattern id="scan" width="4" height="2" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".28"/></pattern></defs>'
    body = bg.svg() + stars[0].svg('class="tw0"') + stars[1].svg('class="tw1"')
    body += f'<g class="march">{fr[0].svg("class=\"f0\"")}{fr[1].svg("class=\"f1\"")}</g>'
    body += f'<g class="ship">{shot.svg("class=\"shot\"")}{ship.svg()}</g>'
    body += press.svg('class="blink"') + scan
    css = (
        ".f0{animation:fa 1s infinite}.f1{animation:fb 1s infinite}"
        "@keyframes fa{0%,49%{opacity:1}50%,100%{opacity:0}}@keyframes fb{0%,49%{opacity:0}50%,100%{opacity:1}}"
        ".march{animation:march 8s steps(16) infinite alternate}@keyframes march{from{transform:translateX(-60px)}to{transform:translateX(60px)}}"
        ".ship{animation:ship 6s steps(60) infinite alternate}@keyframes ship{from{transform:translateX(70px)}to{transform:translateX(320px)}}"
        ".shot{animation:shot .9s steps(12) infinite}@keyframes shot{from{transform:translateY(0)}to{transform:translateY(-90px);opacity:0}}"
        ".blink{animation:fa 1.2s infinite}"
        ".tw0{animation:fa 3s infinite}.tw1{animation:fb 4s infinite}"
    )
    doc("c-arcade.svg", W, H, 2, body, "diegulio arcade title screen: press start to read the blog", css, defs)


# ================================================================ headers, buttons, inventory
THEMES = {
    "a": dict(bg=BOARD, lo=BOARD_LO, hi=BOARD_HI, fg=LIME, sub=PAPER, mut=MUTED),
    "b": dict(bg=INK, lo="#5b6258", hi=PAPER, fg=PAPER, sub=LIME, mut=MUTED),
    "c": dict(bg="#0d1310", lo="#0d1310", hi=LIME_D, fg=LIME, sub=ORANGE, mut="#7e8f80"),
}


def header(name, theme, label, tag=""):
    t = THEMES[theme]
    pad = 8
    tw = text_w(label)
    gw = text_w(tag) + 8 if tag else 0
    W, H = pad * 2 + gw + tw + (10 if theme == "b" else 0), 17
    L = Layer()
    L.rect(0, 0, W, H, t["bg"])
    if theme == "a":
        L.frame(0, 0, W, H, t["lo"])
        L.rect(1, 1, W - 2, 1, t["hi"])
    elif theme == "b":
        L.frame(0, 0, W, H, PAPER)
        L.frame(2, 2, W - 4, H - 4, t["lo"])
    else:
        L.frame(0, 0, W, H, t["hi"])
    x = pad
    cur = Layer()
    if theme == "b":
        cur.text("~", x, 5, LIME)
        x += 10
    if tag:
        L.text(tag, x, 5, t["sub"])
        x += gw
    L.text(label, x, 5, t["fg"])
    body = L.svg() + cur.svg('class="blink"')
    css = ".blink{animation:bl 1s infinite}@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}"
    if theme == "c":
        body += '<rect width="100%" height="100%" fill="url(#scan)"/>'
    defs = '<defs><pattern id="scan" width="4" height="2" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".3"/></pattern></defs>' if theme == "c" else ""
    doc(name, W, H, 2, body, f"{tag} {label}".strip(), css, defs)


def button(name, label, face, ink, hi, lo):
    W, H = text_w(label) + 16, 15
    L = Layer()
    L.rect(1, 0, W - 2, H, INK)
    L.rect(0, 1, W, H - 2, INK)
    L.rect(1, 1, W - 2, H - 2, face)
    L.rect(1, 1, W - 2, 1, hi)
    L.rect(1, 1, 1, H - 3, hi)
    L.rect(1, H - 3, W - 2, 2, lo)
    L.text(label, 8, 3, ink)
    doc(name, W, H, 2, L.svg(), label)


def inventory(name, theme, items, cols=5):
    t = {
        "a": dict(bg=PAPER, slot="#e6e7de", line="#c9ccc0", fg=INK, edge=INK),
        "b": dict(bg=INK, slot="#2b322a", line="#5b6258", fg=PAPER, edge=PAPER),
        "c": dict(bg="#0d1310", slot="#121c16", line=LIME_D, fg=LIME, edge=LIME_D),
    }[theme]
    sw, sh, g = 74, 17, 4
    rows = math.ceil(len(items) / cols)
    W, H = cols * sw + (cols + 1) * g + 4, rows * sh + (rows + 1) * g + 4
    L = Layer()
    L.rect(0, 0, W, H, t["bg"])
    L.frame(0, 0, W, H, t["edge"])
    for i, it in enumerate(items):
        x = 2 + g + (i % cols) * (sw + g)
        y = 2 + g + (i // cols) * (sh + g)
        L.rect(x, y, sw, sh, t["slot"])
        L.frame(x, y, sw, sh, t["line"])
        L.text_c(it, x + sw // 2, y + 5, t["fg"])
    doc(name, W, H, 2, L.svg(), "Tools: " + ", ".join(items))


def continue_footer():
    W, H = 220, 22
    L = Layer()
    L.rect(0, 0, W, H, "#0d1310")
    L.frame(0, 0, W, H, LIME_D)
    L.text("CONTINUE?", 12, 8, PAPER)
    L.text("THANKS FOR PLAYING", 92, 8, LIME)
    digits = ""
    css = ""
    for i, d in enumerate("9876543210"):
        D = Layer()
        D.text(d, 70, 8, ORANGE)
        digits += D.svg(f'class="d d{i}"')
        css += f".d{i}{{animation-delay:{i}s}}"
    css = ".d{opacity:0;animation:cd 10s steps(1) infinite}@keyframes cd{0%{opacity:1}10%,100%{opacity:0}}" + css
    css += "@media (prefers-reduced-motion: reduce){.d0{opacity:1}}"
    doc("c-continue.svg", W, H, 2, L.svg() + digits, "Continue? Thanks for playing", css)


banner_a()
banner_b()
banner_c()

TOOLS = ["PYTHON", "PYTORCH", "TENSORFLOW", "SCIKIT-LEARN", "PANDAS", "OPENCV", "LANGCHAIN", "FASTAPI", "DOCKER", "GCP", "AWS", "SQL", "MONGODB", "BASH", "GIT"]

for i, (tag, label) in enumerate([("01 /", "WHAT I DO"), ("02 /", "PROJECTS"), ("03 /", "LAB NOTES"), ("04 /", "TOOLBOX"), ("05 /", "OFF THE KEYBOARD")], 1):
    header(f"a-h{i}.svg", "a", label, tag)
for i, label in enumerate(["ABOUT", "QUEST LOG", "LORE (BLOG)", "INVENTORY"], 1):
    header(f"b-h{i}.svg", "b", label)
for i, label in enumerate(["SELECT GAME", "LATEST LEVELS", "POWER-UPS"], 1):
    header(f"c-h{i}.svg", "c", label)

button("a-btn-blog.svg", "BLOG", ORANGE, PAPER, "#f19a72", ORANGE_D)
button("a-btn-cv.svg", "TRAYECTORIA", LIME, INK, "#e6ffb0", LIME_D)
button("a-btn-in.svg", "LINKEDIN", PAPER, INK, "#ffffff", "#c9ccc0")
button("b-btn-blog.svg", "> READ BLOG", INK, PAPER, "#4a5147", "#0f130f")
button("b-btn-cv.svg", "> STATUS", INK, LIME, "#4a5147", "#0f130f")
button("b-btn-in.svg", "> PARTY UP", INK, ORANGE, "#4a5147", "#0f130f")
button("c-btn-blog.svg", "1P START", ORANGE, INK, "#f19a72", ORANGE_D)
button("c-btn-cv.svg", "HIGH SCORES", LIME, INK, "#e6ffb0", LIME_D)
button("c-btn-in.svg", "2P JOIN", "#7fd6e0", INK, "#c3f0f5", "#3f8f99")

inventory("a-tools.svg", "a", TOOLS)
inventory("b-tools.svg", "b", TOOLS)
inventory("c-tools.svg", "c", TOOLS)
continue_footer()
