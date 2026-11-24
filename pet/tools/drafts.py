#!/usr/bin/env python3
"""Bản thảo tư thế tĩnh. Mỗi phần vẽ tay theo hàng: 'y: x0-x1[màu] ...'. Viền đen tự thêm như con gốc."""
import sys, os, zlib, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from original import ORIGINAL as O
RGB = {'o': (0xf3, 0x8c, 0x1d), 'k': (0, 0, 0), 'g': (0x54, 0x4e, 0x52), 'w': (255, 255, 255)}
CELL = {(x, y): c for y, r in enumerate(O) for x, c in enumerate(r) if c != '.'}
HM = [19]*5+[18, 18]+[19]*5+[20]*3
FLAT = {(x, y): c for (x, y), c in CELL.items() if x <= HM[y]}          # đầu gốc, áp đất
def head(eyes='sleep', flat=False):
    h = dict(FLAT)
    if eyes == 'sleep': return h
    for x in (4, 5, 6, 13, 14, 15): h[(x, 11)] = 'o'
    L = {'open': [(5, 10), (5, 11), (4, 10), (4, 11)], 'tall': [(4, 9), (5, 9), (4, 10), (5, 10), (4, 11), (5, 11)],
         'up': [(4, 8), (5, 8), (4, 9), (5, 9), (4, 10), (5, 10)], 'happy': [(3, 11), (4, 10), (5, 10), (6, 11)],
         'down': [(4, 10), (5, 10), (4, 11), (5, 11), (4, 12), (5, 12)], 'shut': [(3, 10), (4, 11), (5, 11), (6, 10)], 'wow': [(x, y) for x in (4, 5, 6) for y in (8, 9, 10, 11)],
         'squeeze': [(3, 9), (4, 9), (5, 10), (6, 10), (3, 11), (4, 11)], 'dizzy': [(4, 9), (6, 9), (5, 10), (4, 11), (6, 11)], 'sulk': [(3, 10), (4, 10), (5, 10), (6, 10), (4, 11), (5, 11)],
         'wink': [(3, 11), (4, 10), (5, 10), (6, 11)]}[eyes]
    for (x, y) in L:
        h[(x, y)] = 'k'
        if eyes != 'wink': h[(19-x, y)] = 'k'
    if eyes == 'wink':
        for p in [(14, 9), (15, 9), (14, 10), (15, 10), (14, 11), (15, 11)]: h[p] = 'k'
        h[(14, 9)] = 'w'
    for e, p in {'tall': [(4, 9), (14, 9)], 'up': [(4, 8), (14, 8)], 'wow': [(4, 8), (13, 8), (5, 8), (14, 8), (4, 9), (13, 9)]}.items():
        if e == eyes:
            for q in p: h[q] = 'w'
    if eyes == 'wow': h[(9, 13)] = h[(10, 13)] = 'k'
    return h
def P(txt, dx=0, dy=0):
    out = {}
    for line in txt.strip().split('\n'):
        ys, rest = line.split(':'); ys = ys.strip()
        a, b = (ys.split('..')+[ys])[:2] if '..' in ys else (ys, ys)
        for y in range(int(a), int(b)+1):
            for tok in rest.split():
                c = 'o'
                if tok[-1].isalpha(): c, tok = tok[-1], tok[:-1]
                x0, x1 = (tok.split('~')+[tok])[:2] if '~' in tok else (tok, tok)
                for x in range(int(x0), int(x1)+1): out[(x+dx, y+dy)] = c
    return out
class Pose:
    def __init__(s): s.px = {}; s.air = 0
    def put(s, *txts):
        part = {}
        for t in txts: part.update(P(t) if isinstance(t, str) else t)
        for (x, y) in part:
            for q in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if q not in part: s.px[q] = 'k'
        s.px.update(part); return s
    def far(s, txt):                           # chân phía xa: xám trơn, lùi ra sau, không chen nét cam
        return s.put({q: 'g' for q in P(txt)})
    def line(s, pts, c='k'):
        for p in pts: s.px[p] = c
        return s
    def head(s, x, y, eyes='tall', flat=False):
        for (a, b), c in head(eyes, flat).items(): s.px[(a+x, b+y)] = c
        return s
# ---------- VÒNG 5: theo ba ảnh mẫu người dùng gửi (pet/drafts/mau). Mochi: đầu che người, bàn chân xám ló ra ----------
def sh(txt, dx=0, dy=0): return {(x+dx, y+dy): c for (x, y), c in P(txt).items()}
ST = {}
def pose(name):
    def d(fn): ST[name] = fn(Pose()); return fn
    return d
@pose('Ngủ (bản gốc, đã duyệt)')
def _(p): p.px = dict(CELL); return p
@pose('Nằm, mở mắt (đã duyệt)')
def _(p): p.px = dict(CELL); return p.head(0, 0, 'tall', True)
@pose('Nhún mông 1')                              # GIF 2, khung 5
def _(p):
    p.put("""3: 32~33
4: 32~34
5: 32~35
6: 32~34 35w
7: 32~33 34~35w
8: 31~32 33~35w
9: 31~35w
10: 31~34w""")
    p.put("""-1: 23~27
0: 21~29
1: 20~30
2..7: 20~31
8..9: 20~30
10: 20~29
11: 20~26 27~28g
12: 20~25
13: 20~23""")
    return p.head(0, 0, 'sleep', True)
@pose('Nhún mông 2')                              # GIF 2, khung 6
def _(p):
    p.put("""0: 31~32
1: 31~34
2..3: 31~35
4: 31~33 34~35w
5: 31~32 33~35w
6: 31~35w
7: 30~34w
8: 30~33w""")
    p.put("""-3: 23~26
-2: 21~28
-1: 20~29
0: 20~30
1..3: 20~30
4..6: 20~30
7..8: 20~29
9: 20~28
10: 20~25 26~28g
11: 20~25
12: 20~23
13: 20~21""")
    return p.head(0, 0, 'sleep', True)
@pose('Vươn vai')                                 # GIF 1, khung 3
def _(p):
    p.put("""-1: 31~32
0: 32~33
1: 32~34
2: 32~35
3: 32~33 34~35w
4: 32 33~35w
5: 32~35w
6: 33~34w""")
    p.put("""-4: 23~26
-3: 21~28
-2: 20~29
-1: 20~30
0..4: 20~30
5..7: 20~30
8: 20~25 27~30
9: 20~24 27~29
10: 20~23 27g 28~29
11: 20~23 27~29g
12: 19~22
13: 19~21""")
    p.put('15: 0~4g 12~16g\n16: 0~3g 12~15g')
    return p.head(0, 0, 'sleep', True)
@pose('Giật mình')                                # GIF 1, khung 4
def _(p):
    p.put("""-8: 30~32w
-7: 28~34w
-6: 26~28 29~34w
-5: 25~29 30~34w
-4: 24~30 31~33w
-3: 23~33
-2: 23~32
-1: 22~31
0: 22~29
1: 22~27
2: 22~25""")
    p.put("""2: 20~23
3: 20~25
4: 20~27
5: 20~28
6: 20~29
7..9: 20~30
10: 20~25 27~30
11: 20~24 28~29 30~31g
12: 20~23 29~31g
13: 19~21""")
    p.put('15: 0~3g 11~14g\n16: 0~2g 11~13g')
    return p.head(0, 0, 'squeeze', True)
@pose('Chạy 1')                                   # GIF 1, khung 5
def _(p):
    p.air = 3
    p.put("""-2: 30~32w
-1: 29~34w
0: 27~29 30~34w
1: 26~30 31~34w
2: 25~31 32~33w
3: 24~33
4: 23~32
5: 23~31
6: 23~29
7: 23~27""")
    p.put('15: 4~6g\n16: 4~6g')
    p.put("""6: 20~21
7: 20~24
8..9: 19~25
10: 19~26
11: 19~27
12: 19~28 29~30g
13: 19~24 27~30g
14: 14~21
15: 13~18
16: 11~12g 13~16
17: 10~13g""")
    return p.head(0, 0, 'sleep', True)
@pose('Chạy 2')                                   # GIF 1, khung 6
def _(p):
    p.air = 4
    p.put("""0: 27~30
1: 25~28 29~33w
2: 24~29 30~34w
3: 23~30 31~34w
4: 22~31 32~33w
5: 22~32
6: 22~30
7: 22~27""")
    p.put('15: 3~5g\n16: 3~6g')
    p.put("""6: 20
7: 19~23
8: 19~24
9..10: 19~25
11: 19~27
12: 19~28 29~30g
13: 19~25 28~31g
14: 13~21
15: 12~18
16: 11~12g 13~15
17: 10~13g""")
    return p.head(0, 0, 'sleep', True)
def chin(p, x, y, eyes):                          # đầu ngồi: hàng 0-12 gốc, cằm thu 1 ô như GIF 1 khung 7
    h = head(eyes, True); h = {q: c for q, c in h.items() if q[1] <= 12}
    for yy, r in {13: '.kkooooowwwoooooookk', 14: '...'+'k'*15}.items():
        for xx, c in enumerate(r):
            if c != '.': h[(xx, yy)] = c
    for (a, b), c in h.items(): p.px[(a+x, b+y)] = c
    return p
def sitbody(p, dx=0, wag=0):
    p.put(sh("""15: 21~23w
16: 20 21~25w
17: 20~21 22~25w
18: 19~22 23~25w
19: 19~25
20: 19~24
21: 19~23""", dx, 0) if not wag else sh("""13: 23~25w
14: 22~26w
15: 22~26w
16: 21~22 23~26w
17: 20~26
18: 19~25
19: 19~24
20: 19~23
21: 19~21""", dx, 0))
    p.put("""14: 6~14
15: 5~15
16: 5~16
17: 4~16
18..19: 4~17
20: 4 5~6g 7 9 10g 11 13~17
21: 4~7g 9~11g 13~16g 17""")
    p.line([(8, y) for y in (18, 19, 20, 21, 22)]+[(12, y) for y in (19, 20, 21, 22)]); return p
@pose('Ngồi')                                     # GIF 1, khung 7
def _(p): return chin(sitbody(p), 0, 0, 'sleep')
@pose('Vui')                                      # bảng dáng, hàng 4
def _(p): return chin(sitbody(p, 0, 1), 0, 0, 'happy')
@pose('Nghiêng đầu')                              # GIF 1, khung 8
def _(p):
    p.put("""21: 22~24
22: 22~24 25~26w
23..24: 22~23 24~27w
25: 22~23 24~26w""")
    p.put("""16: 9~16
17: 9~17
18: 9~18
19: 9~18
20: 9~19
21: 8~20
22: 8~20
23..24: 8~20
25: 8~10g 12~14g 16~18g 19~20""")
    p.line([(11, y) for y in (22, 23, 24, 25, 26)]+[(15, y) for y in (22, 23, 24, 25, 26)])
    p.put("""1: 13~14g
2: 12~14g
3: 12~13g 14~15w
4: 12~13g 14~16w
5: 2g 9~11 12~13g 14~16w
6: 1~3g 7~14 15~16w 17
7: 1~3g 5~17
8: 1w 2~3g 4~18
9: 1~2w 3g 4~18
10: 2~3w 4~19
11: 2~3w 4~19
12: 3~20
13: 3~21
14: 4~21
15: 4~19
16: 4~16
17: 5~13
18: 5~10
19: 5~7""")
    for x0, x1, y, c in ((12, 14, 13, 'w'), (10, 15, 14, 'w'), (11, 14, 15, 'w'), (11, 13, 16, 'w'), (12, 13, 14, 'k'), (6, 6, 15, 'k'), (7, 8, 14, 'k'), (9, 9, 14, 'o'), (15, 15, 11, 'k'), (16, 17, 10, 'k')):
        for x in range(x0, x1+1): p.px[(x, y)] = c
    return p
@pose('Ngủ cuộn')                                 # GIF 1, khung 9
def _(p):
    p.put("""-1: 22~26
0: 20~28
1: 20~29
2: 20~30
3..4: 20~31
5..6: 20~31
7..10: 20~32
11: 20~21 22w 23~32
12: 20~23w 24~31
13: 20~24w 25~30""")
    p.line([(22, 9), (23, 8), (24, 7), (25, 7), (26, 6), (27, 6), (28, 6), (29, 6), (30, 7), (21, 10)])
    for q in [(20, 11), (21, 11), (22, 11), (23, 11), (22, 10), (23, 10)]: p.px[q] = 'w'
    return p.head(0, 0, 'sleep', True)
def lump(p, dx=0, dy=0, flip=False):              # phần thân sau và đuôi ló sau đầu, theo bảng dáng
    up = """0: 23~25
1: 21~26
2: 20~24 25~27w
3: 20~24 25~28w
4: 20~23 24~28w
5: 20~23 24~28w
6: 20~24 25~27w
7: 20~26
8: 20~25
9: 20~24
10: 20~23
11: 20~22
12: 20~22g"""
    dn = """3: 20~23
4: 20~25
5: 20~26
6: 20~27
7: 20~27
8: 20~24 25~28w
9: 20~23 24~28w
10: 20~23 24~28w
11: 20~22 24~27w
12: 20~22g 24~26w"""
    p.put(sh(up if flip else dn, dx, dy))
    if not flip: p.line([(23+dx, 10+dy), (23+dx, 11+dy), (23+dx, 12+dy), (23+dx, 13+dy), (24+dx, 9+dy)])
    return p
@pose('Đi 1')                                     # bảng dáng, hàng 3 phải
def _(p):
    lump(p, 0, 0); p.put('15: -1~3g 10~13g\n16: -1~2g 9~13g')
    return p.head(0, 0, 'sleep', True)
@pose('Đi 2')
def _(p):
    lump(p, 0, -1, True); p.put('14: 4~7g 14~17g\n15: 3~7g 13~17g')
    return p.head(0, -1, 'sleep', True)
@pose('Nhảy: lấy đà')                             # bảng dáng, hàng 2 khung 1
def _(p): return lump(p, 0, 1).head(0, 0, 'sleep', True)
@pose('Nhảy: vọt')                                # khung 2
def _(p):
    p.air = 8; lump(p, 0, 0); p.put('14: 0~3g\n15: -1~2g\n16: -1~1g').put('14: 13~16g\n15: 14~17g\n16: 14~16g')
    return p.head(0, 0, 'sleep', True)
@pose('Nhảy: đỉnh')                               # khung 3
def _(p):
    p.air = 14; lump(p, 0, 0); p.put('15: 3~6g 12~15g\n16: 3~5g 13~15g')
    return p.head(0, 0, 'sleep', True)
@pose('Nhảy: rơi')                                # khung 4
def _(p):
    p.air = 7; lump(p, 0, -2); p.put('14: 1~4g 13~16g\n15: 1~3g 14~16g\n16: 0~3g 14~17g')
    return p.head(0, 0, 'sleep', True)
@pose('Đáp đất')
def _(p):
    lump(p, 0, 2); p.put('14: -1~0g\n15: -2~3g 13~17g\n16: -2~2g 13~16g')
    return p.head(0, 0, 'shut', True)
@pose('Choáng')                                   # bảng dáng, hàng 4 khung 2
def _(p): return lump(p, 0, 1).head(0, 0, 'dizzy', True)
@pose('Ló ra mép')                                # bảng dáng, hàng 4 khung cuối
def _(p):
    h = head('tall', True)
    p.put('14: 0~8\n15: 0~8\n16: 0~8\n17: 0~8\n18: 0~7\n19: 0~2g 4~6g')
    p.line([(3, 18), (3, 19), (3, 20)])
    for (x, y), c in h.items():
        if x >= 9: p.px[(x-9, y)] = c
    for q in [q for q in p.px if q[0] < 0]: p.px.pop(q)
    for y in range(-2, 22): p.px[(-1, y)] = 'k'
    return p
EYES = [('sleep', 'Ngủ (gốc)'), ('tall', 'Mở mắt'), ('open', 'Mở mắt, chấm'), ('up', 'Nhìn lên'), ('happy', 'Vui'), ('wink', 'Nháy'), ('wow', 'Giật mình'), ('shut', 'Nhắm chặt'), ('dizzy', 'Choáng'), ('sulk', 'Dỗi'), ('squeeze', 'Nhăn mặt')]
def png(path, w, h, buf):
    raw = b''.join(b'\0'+bytes(buf[y*w*4:(y+1)*w*4]) for y in range(h))
    ch = lambda t, d: struct.pack('>I', len(d))+t+d+struct.pack('>I', zlib.crc32(t+d))
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))+ch(b'IDAT', zlib.compress(raw, 9))+ch(b'IEND', b''))
CW, CH, GX, GY = 60, 50, 9, 46
def draw(path, items, cols, k=6, sil=False, bg=(245, 245, 245)):
    rows = -(-len(items)//cols); w, h = cols*CW*k, rows*CH*k; buf = bytearray((bytes(bg)+b'\xff' if bg else b'\0\0\0\0')*(w*h))
    for i, (px, air) in enumerate(items):
        oy = GY-air-max(y for _, y in px)
        for (x, y), c in px.items():
            X, Y = i % cols*CW+GX+x, i//cols*CH+oy+y
            if 0 <= X < w//k and 0 <= Y < h//k:
                for q in range(k):
                    a = ((Y*k+q)*w+X*k)*4; buf[a:a+4*k] = bytes((RGB[c] if not sil else (20, 20, 20))+(255,))*k
    png(path, w, h, buf)
import base64, tempfile
def uri(px, k=1, sil=False, dy=0, cw=60, ch=50):
    f = tempfile.mktemp('.png'); global CW, CH, GX, GY
    s = (CW, CH, GX, GY); CW, CH, GX, GY = cw, ch, 8, ch-4
    draw(f, [(px, dy)], 1, k, sil, None); CW, CH, GX, GY = s
    d = base64.b64encode(open(f, 'rb').read()).decode(); os.remove(f); return 'data:image/png;base64,'+d
NOTE = {'Ngủ (bản gốc, đã duyệt)': 'Khóa', 'Nằm, mở mắt (đã duyệt)': 'Khóa', 'Nhún mông 1': 'GIF 2, khung 5', 'Nhún mông 2': 'GIF 2, khung 6', 'Vươn vai': 'GIF 1, khung 3', 'Giật mình': 'GIF 1, khung 4',
 'Chạy 1': 'GIF 1, khung 5', 'Chạy 2': 'GIF 1, khung 6', 'Ngồi': 'GIF 1, khung 7', 'Nghiêng đầu': 'GIF 1, khung 8', 'Ngủ cuộn': 'GIF 1, khung 9', 'Vui': 'Bảng dáng, hàng 4',
 'Đi 1': 'Bảng dáng, hàng 3', 'Đi 2': 'Bảng dáng, hàng 3', 'Nhảy: lấy đà': 'Bảng dáng, hàng 2', 'Nhảy: vọt': 'Bảng dáng, hàng 2', 'Nhảy: đỉnh': 'Bảng dáng, hàng 2', 'Nhảy: rơi': 'Bảng dáng, hàng 2', 'Đáp đất': 'Suy từ mẫu', 'Choáng': 'Bảng dáng, hàng 4', 'Ló ra mép': 'Bảng dáng, hàng 4'}
if __name__ == '__main__':
    out = sys.argv[1]; names = list(ST)
    draw(out+'/d1.png', [(ST[n].px, ST[n].air) for n in names], 4, 6); draw(out+'/d1s.png', [(ST[n].px, ST[n].air) for n in names], 4, 4, True)
    cards = ''.join(f'<figure><div class="st"><img src="{uri(ST[n].px, 1, False, ST[n].air)}" alt=""><i></i></div><figcaption><b>{i+1}. {n}</b><span>{NOTE[n]}</span><img class="s" src="{uri(ST[n].px, 1, True, ST[n].air)}" alt=""></figcaption></figure>' for i, n in enumerate(names))
    faces = ''.join(f'<figure class="f"><img src="{uri(head(e, True), 1, False, 0, 36, 24)}" alt=""><figcaption><b>{chr(65+i)}. {l}</b></figcaption></figure>' for i, (e, l) in enumerate(EYES))
    html = f"""<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bản thảo cáo</title><style>
body{{margin:0;padding:32px 24px 64px;background:#f5f5f5;color:#222;font:16px/1.5 system-ui,sans-serif}}main{{max-width:1180px;margin:auto}}h1{{font-size:32px;margin:0}}h2{{margin:40px 0 12px}}p{{max-width:70ch}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:16px}}figure{{margin:0;background:#fff;border:1px solid #ddd;border-radius:6px;overflow:hidden}}
.st{{position:relative;height:252px;background:#efefef;overflow:hidden}}.st img{{width:300px;height:250px;image-rendering:pixelated;position:absolute;left:50%;margin-left:-150px}}.st i{{position:absolute;left:0;right:0;top:236px;border-top:1px dashed #bbb}}
figcaption{{padding:10px 14px;border-top:1px solid #eee;display:grid;grid-template-columns:1fr 56px;align-items:center}}figcaption span{{grid-column:1;color:#555;font-size:14px}}.s{{grid-column:2;grid-row:1/3;width:56px;image-rendering:pixelated}}
.f{{text-align:center}}.f>img{{width:216px;image-rendering:pixelated}}.f figcaption{{display:block}}.faces{{grid-template-columns:repeat(auto-fill,minmax(216px,1fr))}}</style>
<main><h1>Bản thảo cáo, chờ duyệt</h1><p>Vòng 5, theo ba ảnh mẫu của bạn. Tư thế tĩnh, chưa có chuyển động. Đường đứt là mặt đất, hình đen nhỏ là bóng để xem dáng có đọc được không. Duyệt hoặc chê theo số (tư thế) và chữ (nét mặt).</p>
<h2>Tư thế</h2><div class="g">{cards}</div><h2>Nét mặt</h2><div class="g faces">{faces}</div></main></html>"""
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'drafts', 'ban-thao.html'), 'w').write(html)
    # kiểm tra: mặt gốc nguyên vẹn (trừ ô mắt/miệng)
    for e, _ in EYES:
        h = head(e, True); assert all(h.get(q) == c for q, c in FLAT.items() if not (8 <= q[1] <= 13 and c in 'ko' and 3 <= q[0] <= 16 or q[1] == 13)), e
    print('mặt gốc giữ nguyên ở', len(EYES), 'nét mặt');