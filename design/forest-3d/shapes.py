# Hình dáng và bảng màu dùng chung cho script Blender (build_forest.py) và script vẽ texture (paint_textures.py).
import math, random, re

PAL = {
    'ground': '#6F9283', 'ground2': '#7FA191', 'ground3': '#5F8373',
    'path': '#E4DFC8', 'pathEdge': '#CBC6AE', 'edge': '#EDE8D6',
    'pine': '#2C4A3A', 'pineLight': '#3B5E4A', 'trunk': '#A8382C',
    'yellow': '#C9B24E', 'yellowShade': '#B39C3C', 'vein': '#B5372B',
    'round': '#A9A84C', 'roundShade': '#949239',
    'flame': '#D2743A', 'flameShade': '#E3A04A', 'flameVein': '#9E3A22',
    'rock': '#7D988A', 'stone': '#89A092', 'teal': '#2F6F68', 'tealLine': '#245650', 'orange': '#D27E3C', 'yband': '#D8B24A',
    'grass': '#4F7A55', 'grass2': '#6E9460', 'fern': '#3C6A4A', 'bush': '#5C8A57', 'flower': '#E6C24E', 'dry': '#7A5A3A',
    'mushCap': '#C2423A', 'dot': '#F2EBD8', 'stem': '#E9E0C8',
    'fox': '#DB7A30', 'foxDark': '#C4652A', 'cream': '#F3ECDA', 'ink': '#2A1E18',
    'wood': '#7A5234', 'woodLight': '#B98A5A', 'lamp': '#FFD58A', 'hat': '#E2B84A', 'cloth': '#C9B48E', 'skin': '#E8C8A8', 'pants': '#4A3C32', 'boot': '#3A2C24', 'shirt': '#E6DECB', 'pack': '#A8402E', 'band': '#8A4A2A',
}
# ---------- đọc đường SVG (M, L, C, Z) thành đa giác ----------
def svg_poly(d, steps=10):
    toks = re.findall(r'[MLCZmlcz]|-?\d*\.?\d+', d)
    pts, i, cmd, cur, polys = [], 0, None, (0, 0), []
    while i < len(toks):
        t = toks[i]
        if t in 'MLCZmlcz': cmd = t; i += 1
        if cmd in 'Zz':
            if pts: polys.append(pts); pts = []
            continue
        if cmd == 'M':
            if pts: polys.append(pts)
            cur = (float(toks[i]), float(toks[i + 1])); pts = [cur]; i += 2; cmd = 'L'
        elif cmd == 'L':
            cur = (float(toks[i]), float(toks[i + 1])); pts.append(cur); i += 2
        elif cmd == 'C':
            p1 = (float(toks[i]), float(toks[i + 1])); p2 = (float(toks[i + 2]), float(toks[i + 3])); p3 = (float(toks[i + 4]), float(toks[i + 5])); i += 6
            p0 = cur
            for s in range(1, steps + 1):
                u = s / steps; a = (1 - u) ** 3; b_ = 3 * (1 - u) ** 2 * u; c = 3 * (1 - u) * u * u; e = u ** 3
                pts.append((a * p0[0] + b_ * p1[0] + c * p2[0] + e * p3[0], a * p0[1] + b_ * p1[1] + c * p2[1] + e * p3[1]))
            cur = p3
        else:
            i += 1
    if pts: polys.append(pts)
    return polys

LEAF = 'M50 4 C84 30 96 70 90 100 C84 128 68 138 50 138 C32 138 16 128 10 100 C4 70 16 30 50 4 Z'
FLAME = 'M30 2 C46 24 56 56 54 86 C52 110 42 124 30 124 C18 124 8 110 6 86 C4 56 14 24 30 2 Z'
PINE = 'M45 2 L58 30 L52 30 L66 58 L58 58 L74 90 L64 90 L82 124 L70 124 L88 160 L2 160 L20 124 L8 124 L26 90 L16 90 L32 58 L24 58 L38 30 L32 30 Z'
SHAPES = {
    'pine': (90, 190, [('M40 150 L50 150 L51 190 L39 190 Z', 'trunk', 'fill', 'main'), (PINE, 'pine', 'fill', 'main'),
                       ('M45 8 L56 30 L50 31 L64 58 L56 59 L72 90 L62 91 L80 124 L68 125 L85 157 L45 157 Z', 'pineLight', 'fill', 0)]),
    'yellow': (100, 170, [('M45 130 L55 130 L56 170 L44 170 Z', 'trunk', 'fill', 'main'), (LEAF, 'yellow', 'fill', 'main'),
                          ('M50 8 C82 32 93 70 88 100 C82 126 67 135 50 135 Z', 'yellowShade', 'fill', 0),
                          ('M50 134 L50 18 M50 54 L33 38 M50 54 L67 38 M50 82 L27 63 M50 82 L73 63 M50 110 L30 94 M50 110 L70 94', 'vein', 'line', 2.4)]),
    'flame': (60, 150, [('M26 116 L34 116 L35 150 L25 150 Z', 'trunk', 'fill', 'main'), (FLAME, 'flame', 'fill', 'main'),
                        ('M30 6 C45 26 54 56 52 86 C50 108 41 121 30 121 Z', 'flameShade', 'fill', 0),
                        ('M30 120 L30 16 M30 46 L18 34 M30 46 L42 34 M30 72 L14 58 M30 72 L46 58 M30 98 L16 86 M30 98 L44 86', 'flameVein', 'line', 2)]),
    'shrub': (130, 60, [('M4 58 C4 40 14 30 26 30 C30 16 46 10 58 16 C68 6 88 8 94 20 C108 16 124 28 122 44 C128 48 128 54 126 58 Z', 'teal', 'fill', 'main'),
                        ('M6 57 C22 47 42 51 64 47 C88 51 108 47 124 57 Z', 'orange', 'fill', 0),
                        ('M22 44 C30 36 40 34 48 36 M56 30 C66 22 80 22 88 30 M94 40 C102 34 112 36 116 42', 'tealLine', 'line', 2.5)]),
    'grass': (50, 36, [('M2 36 L8 12 L12 30 L18 4 L22 30 L28 8 L32 30 L38 14 L42 32 L48 18 L48 36 Z', 'grass', 'fill', 'main')]),
    'grass2': (50, 36, [('M2 36 L6 16 L12 30 L16 6 L22 30 L30 10 L32 30 L40 12 L42 32 L48 20 L48 36 Z', 'grass2', 'fill', 'main')]),
    'foxSit': (60, 74, [('M40 66 C56 70 64 56 58 40 C68 50 66 72 46 72 Z', 'foxDark', 'fill', 'main'),
                        ('M18 74 L18 46 C18 38 22 34 26 32 L22 28 L6 30 L18 21 L19 8 L26 17 L33 6 L35 22 C41 28 43 38 41 46 L46 74 Z', 'fox', 'fill', 'main'),
                        ('M22 34 C20 44 22 56 26 64 L32 64 C30 54 30 44 28 36 Z', 'cream', 'fill', 0),
                        ('M58 40 C64 44 67 52 66 58 C62 52 60 46 58 40 Z', 'cream', 'fill', 0),
                        ('M24 21 L27 21 L27 24 L24 24 Z', 'ink', 'fill', 0)]),
    'foxWalk': (84, 52, [('M62 22 C74 14 84 22 82 32 C78 26 72 26 64 30 Z', 'foxDark', 'fill', 'main'),
                         ('M10 22 L1 19 L12 14 L15 3 L21 11 L27 3 L29 14 C40 14 56 16 64 22 C66 30 62 36 56 36 L56 52 L50 52 L50 38 L24 38 L24 52 L18 52 L18 36 C12 34 10 28 10 22 Z', 'fox', 'fill', 'main'),
                         ('M14 24 C16 30 20 34 26 36 L30 34 C24 30 20 26 18 22 Z', 'cream', 'fill', 0),
                         ('M16 14 L19 14 L19 17 L16 17 Z', 'ink', 'fill', 0)]),
    'sign': (200, 300, [('M94 30 L108 30 L110 300 L92 300 Z', 'wood', 'fill', 'main'),
                        ('M30 50 L176 50 L176 96 L30 96 L10 73 Z', 'woodLight', 'fill', 'main'),
                        ('M26 112 L172 112 L192 135 L172 158 L26 158 Z', 'woodLight', 'fill', 'main'),
                        ('M34 174 L176 174 L176 220 L34 220 L14 197 Z', 'woodLight', 'fill', 'main')]),
}

ROUND = 'M50 6 C80 6 96 30 94 58 C96 88 76 108 50 108 C24 108 4 88 6 58 C4 30 20 6 50 6 Z'
def _flowers(n, w, h, top):
    out = ''
    rnd = random.Random(n)
    for i in range(n):
        x = rnd.uniform(14, w - 14); y = rnd.uniform(top + 8, h - 10); r = 3.2
        out += f'M{x - r} {y} L{x} {y - r} L{x + r} {y} L{x} {y + r} Z '
    return out
def _fern_d():
    d = ''
    for ang in (-62, -34, -10, 14, 38, 64):
        a = math.radians(ang); L = 58 - abs(ang) * 0.28; bx, by = 50, 68
        ux, uy = math.sin(a), -math.cos(a); px, py = -uy, ux
        left, right = [], []
        teeth = 9
        for i in range(teeth + 1):
            t = i / teeth; wd = 9 * math.sin(math.pi * min(1, t * 1.15)) * (1 - t * 0.35)
            bend = 6 * t * t * (1 if ang >= 0 else -1)
            cx, cy = bx + ux * L * t + px * bend, by + uy * L * t + py * bend
            jag = wd * (1.0 if i % 2 else 0.55)
            left.append((cx + px * jag, cy + py * jag)); right.append((cx - px * jag, cy - py * jag))
        pts = left + right[::-1]
        d += 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z '
    return d
SHAPES.update({
    'round': (100, 160, [('M45 100 L55 100 L56 160 L44 160 Z', 'trunk', 'fill', 'main'), (ROUND, 'round', 'fill', 'main'),
                         ('M50 10 C78 10 92 32 90 58 C92 86 74 104 50 104 Z', 'roundShade', 'fill', 0),
                         ('M50 104 L50 20 M50 44 L34 32 M50 44 L66 32 M50 66 L28 50 M50 66 L72 50 M50 88 L32 74 M50 88 L68 74', 'vein', 'line', 2.6)]),
    'shrubY': (130, 60, [('M4 58 C4 40 14 30 26 30 C30 16 46 10 58 16 C68 6 88 8 94 20 C108 16 124 28 122 44 C128 48 128 54 126 58 Z', 'teal', 'fill', 'main'),
                         ('M6 57 C22 47 42 51 64 47 C88 51 108 47 124 57 Z', 'yband', 'fill', 0),
                         ('M8 52 C24 44 44 47 64 43 C88 47 108 43 122 52', 'orange', 'line', 2.2)]),
    'flowerBush': (130, 56, [('M4 56 C2 36 18 22 36 24 C44 10 70 8 82 18 C100 12 124 24 124 42 C128 48 128 52 126 56 Z', 'bush', 'fill', 'main'),
                             (_flowers(14, 130, 56, 18), 'flower', 'fill', 0)]),
    'fern': (100, 70, [(_fern_d(), 'fern', 'fill', 'main')]),
    'arrowSign': (90, 40, [('M4 6 L74 6 L88 20 L74 34 L4 34 Z', 'woodLight', 'fill', 'main')]),
})
