# Vẽ texture "tranh in trên giấy nỉ" cho từng loại vật, mỗi loại 3 biến thể.
# Chạy: uv run --with pillow --with numpy python design/forest-3d/paint_textures.py
# Kết quả: design/forest-3d/textures/<loại>_<số>.png, khớp đúng khung SVG của hình trong shapes.py.
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from shapes import PAL, svg_poly, SHAPES
OUT = os.path.join(HERE, 'textures'); os.makedirs(OUT, exist_ok=True)
MAXD = 640
LEAFY = {'yellow', 'round', 'flame', 'pine', 'teal', 'bush', 'fern', 'grass', 'grass2'}
WOOD = {'trunk', 'wood', 'woodLight'}

def hexrgb(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float) / 255

def smooth_noise(W, H, scale, rng):
    a = Image.fromarray((rng.random((max(2, H // scale), max(2, W // scale))) * 255).astype(np.uint8))
    a = a.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale / 3))
    v = np.asarray(a, float) / 255; return (v - v.mean()) / (v.std() + 1e-6)

def mask_of(polys, W, H, k):
    m = Image.new('L', (W * 2, H * 2), 0); d = ImageDraw.Draw(m)
    for p in polys:
        if len(p) >= 3: d.polygon([(x * k * 2, y * k * 2) for x, y in p], fill=255)
    return np.asarray(m.resize((W, H), Image.LANCZOS), float) / 255

def paint(kind, variant):
    w, h, parts = SHAPES[kind]
    k = MAXD / max(w, h); W, H = max(8, int(round(w * k))), max(8, int(round(h * k)))
    rng = np.random.default_rng(hash((kind, variant)) % 2 ** 32); prng = random.Random(variant * 97 + len(kind))
    canvas = np.zeros((H, W, 3)); alpha = np.zeros((H, W))
    yy, xx = np.mgrid[0:H, 0:W]; xn, yn = xx / W, yy / H
    tint = 1 + rng.uniform(-0.05, 0.05, 3)
    for d, col, mode, sw in parts:
        if mode == 'line':
            layer = Image.new('L', (W, H), 0); dr = ImageDraw.Draw(layer)
            for line in svg_poly(d, 8):
                pts = [(x * k, y * k) for x, y in line]
                for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                    wd = max(1, int(sw * k * prng.uniform(0.7, 1.15)))
                    dr.line([(x0, y0), (x1, y1)], fill=255, width=wd)
                    dr.ellipse([x1 - wd / 2, y1 - wd / 2, x1 + wd / 2, y1 + wd / 2], fill=255)
            m = np.asarray(layer.filter(ImageFilter.GaussianBlur(0.8)), float) / 255 * alpha
            c = hexrgb(PAL[col]) * tint
            canvas = canvas * (1 - m[..., None]) + c * (0.9 + 0.2 * rng.random((H, W, 1))) * m[..., None]
            continue
        m = mask_of(svg_poly(d), W, H, k)
        if m.max() == 0: continue
        base = hexrgb(PAL[col]) * tint
        is_shade = sw != 'main'
        grad = 0.10 * (0.55 - (xn * 0.55 + yn * 0.45))
        mott = smooth_noise(W, H, max(6, W // 9), rng) * 0.06 + smooth_noise(W, H, max(3, W // 28), rng) * 0.035
        fib = rng.normal(0, 1, (H, W)) * 0.03
        shade = 1 + grad + mott + fib
        # mép in đậm hơn một chút (giấy in, mép cắt)
        blur = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(2, W / 55))), float) / 255
        edge = np.clip((1 - blur) * 2.4, 0, 1) * m
        shade -= edge * (0.16 if not is_shade else 0.05)
        col_arr = np.clip(base[None, None] * shade[..., None], 0, 1)
        # nét lá vẽ tay trong tán cây, vân gỗ trên thân
        if col in LEAFY and not is_shade:
            dab = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dab)
            n = int(W * H / (900 if kind != 'pine' else 700))
            for _ in range(n):
                cx, cy = prng.uniform(0, W), prng.uniform(0, H)
                if m[int(min(H - 1, cy)), int(min(W - 1, cx))] < 0.5: continue
                L = W * prng.uniform(0.035, 0.07)
                if kind == 'pine': ang = prng.uniform(0.15, 0.55) * (1 if cx > W / 2 else -1) + (math.pi if cx < W / 2 else 0)
                else: ang = prng.uniform(0, math.pi)
                f = prng.uniform(0.78, 1.18); c = np.clip(base * f * 255, 0, 255).astype(int)
                wid = L * (0.18 if kind == 'pine' else 0.42)
                pts = []
                for t in range(12):
                    a_ = t / 12 * 2 * math.pi
                    px, py = math.cos(a_) * L, math.sin(a_) * wid
                    pts.append((cx + px * math.cos(ang) - py * math.sin(ang), cy + px * math.sin(ang) + py * math.cos(ang)))
                dd.polygon(pts, fill=(int(c[0]), int(c[1]), int(c[2]), prng.randint(90, 170)))
            dab = np.asarray(dab.filter(ImageFilter.GaussianBlur(0.6)), float) / 255
            da = dab[..., 3] * m
            col_arr = col_arr * (1 - da[..., None]) + dab[..., :3] * da[..., None]
        if col in WOOD:
            grain = smooth_noise(W, H, 3, rng)
            grain = np.asarray(Image.fromarray(((grain - grain.min()) / (np.ptp(grain) + 1e-6) * 255).astype(np.uint8)).resize((max(2, W // 6), H)).resize((W, H)), float) / 255
            col_arr = col_arr * (0.88 + 0.22 * grain[..., None])
        canvas = canvas * (1 - m[..., None]) + col_arr * m[..., None]
        alpha = np.maximum(alpha, m)
    img = np.dstack([np.clip(canvas, 0, 1) * 255, alpha * 255]).astype(np.uint8)
    # tô tràn màu ra ngoài mép một chút để khi lọc texture không bị viền đen
    rgba = Image.fromarray(img, 'RGBA')
    bg = rgba.filter(ImageFilter.GaussianBlur(6)); bgn = np.asarray(bg, float)
    a = bgn[..., 3:4] / 255 + 1e-6; fill = np.clip(bgn[..., :3] / a, 0, 255)
    rgb = np.where(img[..., 3:4] > 0, img[..., :3], fill).astype(np.uint8)
    Image.fromarray(np.dstack([rgb, img[..., 3]]), 'RGBA').save(os.path.join(OUT, f'{kind}_{variant}.png'))
    return W, H

if __name__ == '__main__':
    for kind in SHAPES:
        for v in range(3):
            paint(kind, v)
    print('xong', len(os.listdir(OUT)), 'texture')
