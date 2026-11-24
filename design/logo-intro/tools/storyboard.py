# Vẽ hình minh hoạ cho đoạn mở đầu "portfolio" -> "puc".
# Chạy: uv run --with pillow --with numpy python design/logo-intro/tools/storyboard.py
# Chữ: Futura Medium có sẵn trên macOS, dùng để minh hoạ (bản thật dùng Jost 500, xem PROMPT.md).
# Cáo: lấy thẳng từ pet/sprites/*.png (khung cắt từ ảnh gốc, cỡ 1:1).
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SPR = os.path.join(ROOT, 'pet', 'sprites')
OUT = os.path.join(ROOT, 'design', 'logo-intro', 'img')
os.makedirs(OUT, exist_ok=True)
META = json.load(open(os.path.join(SPR, 'fox.json')))

INK = (0, 0, 0)            # cùng màu viền cáo
BG = (255, 255, 255)
ORANGE = (0xF3, 0x8C, 0x1D)
GREY = (0x54, 0x4E, 0x52)
NOTE = (120, 112, 106)
FONT = '/System/Library/Fonts/Supplemental/Futura.ttc'
SIZE = 300
W, H = 2000, 720
BASE = 520                 # đường chân chữ
F = ImageFont.truetype(FONT, SIZE, index=0)
CAP = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 34, index=0)
CAPB = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 40, index=2)

ASC = F.getbbox('o')[1]    # khoảng từ đỉnh ô chữ tới đỉnh chữ o

# ---------- chữ ----------
def glyph(ch):
    """Mặt nạ của một chữ (L), gốc ở (0,0) của ô chữ."""
    w = int(F.getlength(ch)) + 20
    im = Image.new('L', (w, SIZE + 40), 0)
    ImageDraw.Draw(im).text((0, 0), ch, font=F, fill=255)
    return im

def baseline_offset():
    # đáy chữ o trong ô chữ chính là đường chân chữ (gần đúng, chữ o hơi lố 1-2 px)
    a = np.array(glyph('o')) > 128
    return np.where(a.any(1))[0].max()
BOFF = baseline_offset()

O_MASK = np.array(glyph('o')).astype(np.float32) / 255
ys, xs = np.where(O_MASK > 0.5)
O_BOX = (xs.min(), ys.min(), xs.max(), ys.max())
O_C = ((xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2)
O_R = (xs.max() - xs.min()) / 2
STROKE = 30

def cut_o(center_deg, half_deg, caps=True, ss=4):
    """Chữ o bị khoét một khe quanh góc center_deg (0 = bên phải, -90 = trên). Đầu nét bo tròn."""
    m = O_MASK.copy()
    h, w = m.shape
    yy, xx = np.mgrid[0:h, 0:w]
    ang = np.degrees(np.arctan2(yy - O_C[1], xx - O_C[0]))
    d = (ang - center_deg + 180) % 360 - 180
    m[np.abs(d) < half_deg] = 0
    im = Image.fromarray((m * 255).astype(np.uint8))
    if caps:
        big = Image.new('L', (w * ss, h * ss), 0)
        dr = ImageDraw.Draw(big)
        rm = O_R - STROKE / 2
        for sgn in (-1, 1):
            a = math.radians(center_deg + sgn * half_deg)
            cx, cy = O_C[0] + rm * math.cos(a), O_C[1] + rm * math.sin(a)
            r = STROKE / 2
            dr.ellipse([(cx - r) * ss, (cy - r) * ss, (cx + r) * ss, (cy + r) * ss], fill=255)
        caps_im = big.resize((w, h), Image.LANCZOS)
        im = Image.fromarray(np.maximum(np.array(im), np.array(caps_im)))
    return im

def cap_points(center_deg, half_deg):
    rm = O_R - STROKE / 2
    pts = []
    for sgn in (-1, 1):
        a = math.radians(center_deg + sgn * half_deg)
        pts.append((O_C[0] + rm * math.cos(a), O_C[1] + rm * math.sin(a), center_deg + sgn * half_deg))
    return pts

U_CUT = (-90, 50)   # chữ u: khoét đỉnh, khe rộng 100 độ
C_CUT = (0, 42)     # chữ c: khoét bên phải, khe rộng 84 độ

def stamp(canvas, mask, x, y, color=INK, alpha=1.0, sx=1.0, sy=1.0, clip_below=None):
    """Đặt chữ: (x, y) là góc trái của ô chữ, y tính sao cho chân chữ nằm ở BASE."""
    if sx != 1 or sy != 1:
        w, h = mask.size
        nw, nh = max(1, int(w * sx)), max(1, int(h * sy))
        mask = mask.resize((nw, nh), Image.LANCZOS)
        x += (w - nw) / 2
        y += (h - nh) * (BOFF / h)  # co giãn quanh chân chữ
    m = np.array(mask).astype(np.float32) / 255 * alpha
    if clip_below is not None:
        rows = np.arange(m.shape[0])[:, None] + int(y)
        m[(rows > clip_below)[:, 0]] = 0
    layer = Image.new('RGB', mask.size, color)
    canvas.paste(layer, (int(x), int(y)), Image.fromarray((m * 255).astype(np.uint8)))

def word_layout(text, x0):
    xs = []
    x = x0
    for ch in text:
        xs.append(x)
        x += F.getlength(ch) - 6   # chữ hơi khít (-0.02em)
    return xs, x

TOP = BASE - BOFF  # y của ô chữ để chân chữ chạm BASE

# ---------- tai cáo trên chữ u ----------
def ear(canvas, cx, cy, tilt_deg, size=1.0, ss=4):
    """Tai vector theo màu tai cáo: viền đen, ngoài xám, lòng trắng. (cx, cy): giữa chân tai."""
    Wc, Hc = canvas.size
    layer = Image.new('RGBA', (Wc * ss, Hc * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    t = math.radians(tilt_deg)
    def pts(shape, k=1.0, dy=0):
        out = []
        for px, py in shape:
            px, py = px * k * size, (py * k + dy) * size
            out.append(((cx + px * math.cos(t) - py * math.sin(t)) * ss, (cy + px * math.sin(t) + py * math.cos(t)) * ss))
        return out
    outer = [(-30, 10), (-24, -14), (-14, -38), (-6, -52), (6, -52), (14, -38), (24, -14), (30, 10)]
    inner = [(-15, 8), (-8, -12), (0, -26), (8, -12), (15, 8)]
    d.polygon(pts(outer, 1.22, 2), fill=INK + (255,))
    d.polygon(pts(outer), fill=GREY + (255,))
    d.polygon(pts(inner), fill=(255, 255, 255, 255))
    layer = layer.resize((Wc, Hc), Image.LANCZOS)
    canvas.paste(layer, (0, 0), layer)

# ---------- cáo pixel ----------
_cache = {}
def fox(name, i, flip=False):
    if name not in _cache:
        _cache[name] = Image.open(os.path.join(SPR, name + '.png')).convert('RGBA')
    m = META['anims'][name]
    fr = _cache[name].crop((i * m['w'], 0, (i + 1) * m['w'], m['h']))
    if flip:
        fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    return fr, m['ground']

def put_fox(canvas, name, i, cx, ground_y, flip=False, clip=None, alpha=1.0):
    fr, g = fox(name, i, flip)
    x, y = int(cx - fr.width / 2), int(ground_y - g)
    if clip is not None:   # clip = (x0, y0, x1, y1) vùng được phép hiện, toạ độ màn hình
        a = np.array(fr.split()[3]).astype(np.uint8)
        yy, xx = np.mgrid[0:fr.height, 0:fr.width]
        X, Y = xx + x, yy + y
        ok = (X >= clip[0]) & (Y >= clip[1]) & (X < clip[2]) & (Y < clip[3])
        a[~ok] = 0
        fr.putalpha(Image.fromarray(a))
    if alpha < 1:
        a = np.array(fr.split()[3]).astype(np.float32) * alpha
        fr.putalpha(Image.fromarray(a.astype(np.uint8)))
    canvas.paste(fr, (x, y), fr)
    return fr.width

def put_fx(canvas, name, i, cx, cy, flip=False):
    m = META['fx'][name]
    im = Image.open(os.path.join(SPR, 'fx-' + name + '.png')).convert('RGBA')
    fr = im.crop((i * m['w'], 0, (i + 1) * m['w'], m['h']))
    if flip:
        fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    canvas.paste(fr, (int(cx - fr.width / 2), int(cy - fr.height / 2)), fr)

# ---------- chú thích ----------
def caption(canvas, title, sub):
    d = ImageDraw.Draw(canvas)
    d.text((60, 44), title, font=CAPB, fill=INK)
    words, line, y = sub.split(' '), '', 98
    for w_ in words:
        t = (line + ' ' + w_).strip()
        if d.textlength(t, font=CAP) > canvas.width - 120:
            d.text((60, y), line, font=CAP, fill=NOTE); y += 44; line = w_
        else:
            line = t
    d.text((60, y), line, font=CAP, fill=NOTE)

def ground_line(canvas):
    d = ImageDraw.Draw(canvas)
    for x in range(60, W - 60, 18):
        d.line([(x, BASE + 2), (x + 8, BASE + 2)], fill=(214, 208, 202), width=2)

def arrow_path(canvas, pts, color=NOTE):
    d = ImageDraw.Draw(canvas)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = int(math.hypot(x1 - x0, y1 - y0) / 14)
        for k in range(0, n, 2):
            a, b = k / n, min(1, (k + 1) / n)
            d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], fill=color, width=4)
    (xa, ya), (xb, yb) = pts[-2], pts[-1]
    ang = math.atan2(yb - ya, xb - xa)
    for s in (-1, 1):
        d.line([(xb, yb), (xb - 22 * math.cos(ang + s * 0.5), yb - 22 * math.sin(ang + s * 0.5))], fill=color, width=4)

def bezier(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]

def new():
    c = Image.new('RGB', (W, H), BG)
    ground_line(c)
    return c

# ---------- bố cục ----------
WORD = 'portfolio'
X0 = 380
XS, XEND = word_layout(WORD, X0)
G = {ch: glyph(ch) for ch in set(WORD)}
U_IM, C_IM = cut_o(*U_CUT), cut_o(*C_CUT)
# vị trí cuối của "puc": p giữ nguyên, u ở chỗ chữ o thứ nhất, c ngay sau
P_X, U_X = XS[0], XS[1]
C_X = U_X + F.getlength('o') - 6
O1, O2 = 1, 5     # chữ o thứ nhất biến thành u, chữ o thứ hai (giữa từ) lăn về thành c
OTHERS = [2, 3, 4, 6, 7, 8]

def o_center(x):
    return x + O_C[0], TOP + O_C[1]

def draw_word(c, which=range(9), alpha=1.0, rise=None):
    for i in which:
        dy = 0 if rise is None else rise[i]
        a = alpha if rise is None else max(0, 1 - dy / 60)
        stamp(c, G[WORD[i]], XS[i], TOP + dy, alpha=a)

frames = []

# Cảnh 1: chữ hiện lên
c = new()
draw_word(c, rise={i: min(42, max(0, (i - 4) * 11)) for i in range(9)})
caption(c, 'Cảnh 1  ·  0,00 – 0,45 s  ·  Chữ "portfolio" hiện lên', 'Từng chữ trồi lên 0,25 D và hiện dần, chữ sau chậm hơn chữ trước 40 ms. Ảnh chụp ở 0,30 s: các chữ cuối còn đang lên.')
frames.append(('01-chu-hien', c))

# Cảnh 2: cáo chạy vào
c = new(); draw_word(c)
put_fox(c, 'dash', 2, 200, BASE, flip=True)
put_fx(c, 'dust', 1, 90, BASE - 30, flip=True)
caption(c, 'Cảnh 2  ·  0,45 – 0,80 s  ·  Cáo chạy vào từ mép trái', 'Động tác "chạy" (dash) lật sang phải, 12 khung/giây. Bụi bung sau chân sau mỗi lần chạm đất.')
frames.append(('02-cao-chay-vao', c))

# Cảnh 3: cáo bay qua chữ p
c = new(); draw_word(c)
oc = o_center(XS[O1])
path = bezier((250, BASE - 40), (XS[0] + 40, BASE - 470), (oc[0], TOP + O_BOX[1] - 30))
arrow_path(c, path[:22])
put_fox(c, 'leap', 1, XS[0] + 70, BASE - 250, flip=True)
put_fox(c, 'crouch', 1, 230, BASE, flip=True, alpha=0.25)
caption(c, 'Cảnh 3  ·  0,80 – 1,10 s  ·  Nhún rồi bay qua chữ p', 'Lấy đà 2 khung (bóng mờ bên trái), rồi bay theo đường cong cao 260 px, hạ xuống đúng miệng chữ o đầu tiên.')
frames.append(('03-bay-qua-p', c))

# Cảnh 4: chui vào chữ o (chỉ thấy mông và đuôi)
c = new()
for i in range(9):
    if i == O1:
        stamp(c, G['o'], XS[i], TOP, sx=1.08, sy=0.9)
    else:
        stamp(c, G[WORD[i]], XS[i], TOP)
top_o = TOP + O_BOX[1] + 10
put_fox(c, 'dig', 1, oc[0] + 10, top_o + 62, flip=True, clip=(0, 0, W, top_o + 40))
stamp(c, G['o'], XS[O1], TOP, sx=1.08, sy=0.9)
caption(c, 'Cảnh 4  ·  1,10 – 1,30 s  ·  Chui tọt vào chữ o', 'Cáo cắm đầu vào miệng chữ o, chỉ còn thấy mông và đuôi. Chữ o bẹp xuống (rộng 108 %, cao 90 %) rồi nảy lại.')
frames.append(('04-chui-vao-o', c))

# Cảnh 5: các chữ thừa chìm xuống, chữ o thứ hai lăn về
c = new()
stamp(c, G['p'], XS[0], TOP)
stamp(c, G['o'], XS[O1], TOP)
put_fx(c, 'shake', 1, XS[O1] + O_C[0] + 110, TOP + O_C[1] - 60)
sink = {2: 175, 3: 170, 4: 165, 6: 70, 7: 55, 8: 40}
for i in OTHERS:
    if i == O2: continue
    stamp(c, G[WORD[i]], XS[i], TOP + sink[i], clip_below=BASE + 2)
    put_fx(c, 'dust', 0, XS[i] + F.getlength(WORD[i]) / 2, BASE - 12)
mid = XS[3] + 10
stamp(c, G['o'], mid, TOP)
d = ImageDraw.Draw(c)
for k in range(3):
    d.line([(mid + 175 + k * 10, TOP + O_C[1] - 40 + k * 40), (mid + 235 + k * 10, TOP + O_C[1] - 40 + k * 40)], fill=NOTE, width=5)
arrow_path(c, [(mid + 70, BASE + 80), (C_X + 70, BASE + 80)])
caption(c, 'Cảnh 5  ·  1,30 – 1,75 s  ·  Chữ thừa chìm xuống đất, chữ o lăn về', 'r, t, f, l, i và chữ o cuối chìm dần qua đường chân chữ, mỗi chữ chậm hơn chữ trước 30 ms, có bụi. Chữ o giữa từ lăn sang trái, xoay một vòng.')
frames.append(('05-chu-chim', c))

# Cảnh 6: phá đỉnh chữ o thành u, cáo ló đầu
c = new()
stamp(c, G['p'], P_X, TOP); stamp(c, U_IM, U_X, TOP); stamp(c, G['o'], C_X, TOP)
ucx, ucy = o_center(U_X)
capy = TOP + min(p[1] for p in cap_points(*U_CUT))
put_fox(c, 'peek', 3, ucx, capy + 62, flip=True, clip=(0, 0, W, capy + 44))
# mảnh vỡ của đỉnh chữ o
d = ImageDraw.Draw(c)
for k, (dx, dy, r) in enumerate([(-110, -150, 13), (90, -190, 10), (150, -120, 8), (-160, -90, 7)]):
    d.ellipse([ucx + dx - r, TOP + O_BOX[1] + dy - r, ucx + dx + r, TOP + O_BOX[1] + dy + r], fill=INK)
caption(c, 'Cảnh 6  ·  1,75 – 2,05 s  ·  Đỉnh chữ o vỡ ra, chữ o thành chữ u', 'Đỉnh chữ o bật ra thành 4 mảnh tròn bay lên rồi rơi. Đầu cáo ló lên giữa hai nhánh chữ u, nhìn sang trái rồi sang phải (động tác "ló ra").')
frames.append(('06-thanh-chu-u', c))

# Cảnh 7: chui dưới đất, phá bên phải chữ o thành c
c = new()
stamp(c, G['p'], P_X, TOP); stamp(c, U_IM, U_X, TOP); stamp(c, C_IM, C_X, TOP)
ccx, ccy = o_center(C_X)
d = ImageDraw.Draw(c)
# ụ đất chạy ngầm từ u sang c
for k in range(5):
    x = ucx + 20 + k * (ccx - ucx - 40) / 4
    d.arc([x - 34, BASE - 16, x + 34, BASE + 22], 200, 340, fill=NOTE, width=5)
put_fox(c, 'leap', 1, ccx + 210, ccy + 120, flip=True)
for k, (dx, dy, r) in enumerate([(120, -60, 12), (150, 30, 10), (95, 70, 8)]):
    d.ellipse([ccx + dx - r, ccy + dy - r, ccx + dx + r, ccy + dy + r], fill=INK)
put_fx(c, 'dust', 2, ccx + 90, ccy + 40)
caption(c, 'Cảnh 7  ·  2,05 – 2,40 s  ·  Đào ngầm sang chữ o thứ hai, phá ra bên phải', 'Ụ đất nhô lên chạy từ chữ u sang chữ o (nét đứt). Cáo phóng ra từ hông phải của chữ o, mảnh vỡ bay theo hướng nhảy: chữ o thành chữ c.')
frames.append(('07-thanh-chu-c', c))

# Cảnh 8: đáp đất, ngồi, chữ u mọc tai
c = new()
stamp(c, G['p'], P_X, TOP); stamp(c, U_IM, U_X, TOP); stamp(c, C_IM, C_X, TOP)
for (x, y, a) in cap_points(*U_CUT):
    ear(c, U_X + x, TOP + y - 6, 20 if a > -90 else -20, size=0.62)
put_fox(c, 'wag', 3, C_X + O_C[0] + 250, BASE)
caption(c, 'Cảnh 8  ·  2,40 – 2,80 s  ·  Đáp đất, ngồi vẫy đuôi, chữ u mọc tai', 'Cáo đáp đất (bẹp 1 khung) rồi ngồi quay mặt về chữ, vẫy đuôi một lần. Hai tai bật lên trên hai đầu nhánh chữ u, nảy 2 lần.')
frames.append(('08-ket-thuc', c))

for name, im in frames:
    im.save(os.path.join(OUT, name + '.png'))

# Logo cuối, cỡ lớn
c = Image.new('RGB', (1400, 720), BG)
x0 = 300
TOP2 = 520 - BOFF
stamp(c, G['p'], x0, TOP2); stamp(c, U_IM, x0 + 174, TOP2); stamp(c, C_IM, x0 + 348, TOP2)
for (x, y, a) in cap_points(*U_CUT):
    ear(c, x0 + 174 + x, TOP2 + y - 6, 20 if a > -90 else -20, size=0.62)
fr, g = fox('idle', 0)
c.paste(fr, (x0 + 560, 520 - g), fr)
c.save(os.path.join(OUT, '09-logo-cuoi.png'))

# Sơ đồ dựng chữ u và c từ chữ o
c = Image.new('RGB', (1800, 640), BG)
d = ImageDraw.Draw(c)
cols = [('o', G['o'], None), ('u = o khoét đỉnh 100°', U_IM, U_CUT), ('c = o khoét phải 84°', C_IM, C_CUT)]
for k, (label, m, cut) in enumerate(cols):
    x = 140 + k * 560
    topy = 470 - BOFF
    stamp(c, m, x, topy)
    cx, cy = x + O_C[0], topy + O_C[1]
    if cut:
        for s in (-1, 1):
            a = math.radians(cut[0] + s * cut[1])
            d.line([(cx, cy), (cx + (O_R + 50) * math.cos(a), cy + (O_R + 50) * math.sin(a))], fill=ORANGE, width=4)
    d.text((x - 10, 520), label, font=CAPB, fill=INK)
d.text((140, 40), 'Chữ u và c được cắt ra từ đúng chữ o, cùng nét, cùng độ dày, đầu nét bo tròn', font=CAPB, fill=INK)
d.text((140, 96), 'Không dùng chữ u và c có sẵn trong font: chữ u của Jost có chân phải, chữ c có độ mở khác.', font=CAP, fill=NOTE)
c.save(os.path.join(OUT, '00-dung-chu.png'))

# Bảng tổng: 8 cảnh thu nhỏ
TW, TH = 1000, 360
sheet = Image.new('RGB', (TW * 2 + 60, (TH + 30) * 4 + 30), (238, 234, 230))
for k, (name, im) in enumerate(frames):
    t = im.resize((TW, TH), Image.LANCZOS)
    sheet.paste(t, (20 + (k % 2) * (TW + 20), 20 + (k // 2) * (TH + 30)))
sheet.save(os.path.join(OUT, 'tong-quan.png'))
print('ok', [n for n, _ in frames])
