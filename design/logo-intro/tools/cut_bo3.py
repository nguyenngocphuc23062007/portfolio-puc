# Cắt bộ khung cáo thứ 3 (ảnh 35-50 người dùng gửi ngày 2026-11-24) thành từng động tác.
# Chỉ cắt và bỏ nền (trắng/xám, loang từ mép ô vào), KHÔNG đổi cỡ, không đổi màu, không vẽ lại.
# Mỗi bảng vẽ ở một cỡ khác nhau, nên ghi thêm "px" = số điểm ảnh của một ô pixel (đo bằng độ dày nét viền đen)
# để trang thử tự co các động tác về cùng một cỡ cáo.
# Chạy: uv run --with pillow --with numpy python design/logo-intro/tools/cut_bo3.py
import json, os, statistics, collections
import numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'cao/2-anh-ban-gui/bo-3')
OUT = os.path.join(ROOT, 'cao/5-bo-3')
os.makedirs(OUT, exist_ok=True)
# ảnh: (tên động tác, số cột, số hàng)
SHEETS = {35: ('chay', 6, 1), 36: ('lay-da', 6, 1), 37: ('bat', 3, 1), 38: ('bay-3', 3, 1), 39: ('ngoi-tho', 8, 1),
          40: ('nhay-mat', 6, 1), 41: ('vay-duoi', 10, 1), 42: ('ngoi-xuong', 5, 1), 43: ('quay-dau', 6, 1),
          44: ('dap-dat', 6, 1), 45: ('bung-ra', 4, 2), 46: ('tai-luot', 6, 1), 47: ('thut', 4, 1),
          48: ('nhin-quanh', 3, 3), 49: ('troi-dau', 6, 1), 50: ('lao-xuong', 5, 2),
          51: ('bung-ra-moi', 5, 1), 52: ('bay', 4, 3), 55: ('giu-dat', 3, 2)}   # ảnh 52: Bay đủ 12 khung   # ảnh 51: vẽ lại khung 1-5 của Bung ra, không có chữ C
DETECT = {51}   # ô rộng không đều: tách ô theo đường kẻ dò được thay vì chia đều
# Người dùng yêu cầu xoá cái hố trong động tác Lao xuống hang (2026-11-24): bỏ mảng nâu lớn sát mặt đất.
NO_HOLE = {'lao-xuong'}

def cells_by_lines(a):
    dark = (a[:, :, :3].max(2) < 90) & (a[:, :, 3] > 20)
    def groups(idx):
        out = []
        for v in idx:
            if out and v - out[-1][1] <= 2: out[-1][1] = v
            else: out.append([v, v])
        return out
    ry = groups([y for y in range(a.shape[0]) if dark[y].sum() > a.shape[1] * .8])
    cx = groups([x for x in range(a.shape[1]) if dark[:, x].sum() > (ry[-1][0] - ry[0][1]) * .9])
    y0, y1 = ry[0][1] + 6, ry[-1][0] - 6
    return [(cx[k][1] + 6, y0, cx[k + 1][0] - 6, y1) for k in range(len(cx) - 1)]

def remove_hole(rgb, alpha):
    """Xoá mảng nâu rộng nằm ở phần dưới khung (cái hố); giữ chân nâu có viền đen và các hạt đất nhỏ."""
    h, w = alpha.shape
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    black = rgb.max(2) < 70; orange = (r > 180) & (r - b > 90); white = rgb.min(2) > 200
    brown = alpha & ~black & ~orange & ~white & (rgb.max(2) < 165)   # hố nâu đậm; lòng tai xám hồng nhạt hơn nên được giữ
    lab = np.zeros((h, w), int); n = 0; keep = alpha.copy()
    for y in range(int(h * .55), h):
        for x in range(w):
            if brown[y, x] and not lab[y, x]:
                n += 1; st = [(y, x)]; lab[y, x] = n; pts = []
                while st:
                    cy, cx = st.pop(); pts.append((cy, cx))
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and brown[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = n; st.append((ny, nx))
                xs = [p[1] for p in pts]
                if max(xs) - min(xs) > w * .22:
                    for py, px_ in pts: keep[py, px_] = False
    return keep
INSET = 14
# chỉnh tay cỡ ô pixel ở những bảng đo nét viền bị lệch (chỉ có tai, hoặc có chữ C vẽ kèm), so bằng mắt với 'ngoi-tho'
PX = {'chay': 10.5, 'lay-da': 10.5, 'bat': 19, 'bay-3': 19, 'quay-dau': 12.5, 'dap-dat': 12.5, 'bung-ra': 10,
      'tai-luot': 11.5, 'thut': 15.5, 'troi-dau': 11.3, 'lao-xuong': 10.5}   # bỏ đường kẻ ô ở mép mỗi ô

LIGHT = {50: 140}   # bảng 50 có nền xám loang, cần ngưỡng thấp hơn

def bg_mask(rgb, light=175):
    """Nền: điểm sáng, gần như không màu, nối liền với mép ô."""
    mn, mx = rgb.min(2), rgb.max(2)
    cand = (mn > light) & (mx - mn < 28)
    h, w = cand.shape
    seen = np.zeros_like(cand)
    st = [(y, x) for x in range(w) for y in (0, h - 1) if cand[y, x]] + [(y, x) for y in range(h) for x in (0, w - 1) if cand[y, x]]
    for y, x in st: seen[y, x] = True
    while st:
        y, x = st.pop()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and cand[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; st.append((ny, nx))
    return seen

def stroke_px(rgb, alpha):
    """Độ dày nét viền đen theo chiều ngang (mode của các đoạn đen dài 3-60)."""
    dark = (rgb.max(2) < 90) & alpha
    c = collections.Counter()
    for row in dark:
        n = 0
        for v in row:
            if v: n += 1
            else:
                if 3 <= n <= 60: c[n] += 1
                n = 0
    best = c.most_common(6)
    return best

meta = {}
for i, (name, cols, rows) in SHEETS.items():
    im = Image.open(os.path.join(SRC, f'{i}.webp')).convert('RGBA')
    a = np.asarray(im).astype(int); H, W = a.shape[:2]
    frames = []
    if i in DETECT:
        boxes = cells_by_lines(a); cw = max(b[2] - b[0] for b in boxes); ch = max(b[3] - b[1] for b in boxes)
        rects = []
        for (bx0, by0, bx1, by1) in boxes:   # ô hẹp thì đệm nền trắng hai bên cho cùng cỡ, giữ tâm ô
            cell = np.full((ch, cw, 4), 255, int); ox = (cw - (bx1 - bx0)) // 2; cell[:by1 - by0, ox:ox + bx1 - bx0] = a[by0:by1, bx0:bx1]; rects.append(cell)
    else:
        cw, ch = W // cols - 2 * INSET, H // rows - 2 * INSET      # mọi ô cùng một cỡ
        rects = [a[round(H * r / rows) + INSET:round(H * r / rows) + INSET + ch, round(W * c / cols) + INSET:round(W * c / cols) + INSET + cw]
                 for r in range(rows) for c in range(cols)]
    for cell in rects:
        if True:
            rgb = cell[:, :, :3]; alpha = (cell[:, :, 3] > 20) & ~bg_mask(rgb, LIGHT.get(i, 175))
            # đường kẻ ô nằm giữa ảnh: hàng hoặc cột tối chạy dài hơn 85% ô (nét viền dọc của cáo có thể dài tới 60%) thì xoá (cộng 3 điểm ảnh hai bên)
            dark = (rgb.max(2) < 110) & (cell[:, :, 3] > 20)
            for y in np.where(dark.sum(1) > dark.shape[1] * .85)[0]: alpha[max(0, y - 3):y + 4] = False
            for x in np.where(dark.sum(0) > dark.shape[0] * .85)[0]: alpha[:, max(0, x - 3):x + 4] = False
            if name in NO_HOLE: alpha = remove_hole(rgb, alpha)
            frames.append((rgb, alpha))
    # khung chung của cả động tác: hộp bao của mọi khung (giữ nguyên vị trí tương đối người vẽ đặt trong ô)
    ys = [np.where(al.any(1))[0] for _, al in frames]; xs = [np.where(al.any(0))[0] for _, al in frames]
    top = min(y.min() for y in ys if len(y)); bot = max(y.max() for y in ys if len(y))
    lef = min(x.min() for x in xs if len(x)); rig = max(x.max() for x in xs if len(x))
    fw, fh = rig - lef + 1, bot - top + 1
    sheet = np.zeros((fh, fw * len(frames), 4), np.uint8)
    lows, strokes = [], collections.Counter()
    for k, (rgb, al) in enumerate(frames):
        sub = np.zeros((fh, fw, 4), np.uint8)
        sub[:, :, :3] = rgb[top:bot + 1, lef:rig + 1]; sub[:, :, 3] = al[top:bot + 1, lef:rig + 1] * 255
        sheet[:, k * fw:(k + 1) * fw] = sub
        yy = np.where(al[top:bot + 1, lef:rig + 1].sum(1) > fw * .08)[0]
        if len(yy): lows.append(int(yy.max()))
        for n, cnt in stroke_px(rgb, al): strokes[n] += cnt
    Image.fromarray(sheet).save(os.path.join(OUT, f'{name}.png'))
    px = PX.get(name, strokes.most_common(1)[0][0])
    meta[name] = dict(n=len(frames), w=int(fw), h=int(fh), ground=int(statistics.median_high(lows)) if lows else int(fh), px=int(px), src=f'{i}.webp')
    print(i, name, meta[name], strokes.most_common(4))
json.dump(dict(note='Cắt thẳng từ ảnh 35-50, chỉ bỏ nền; px = cỡ một ô pixel đo theo nét viền', anims=meta),
          open(os.path.join(OUT, 'fox.json'), 'w'), ensure_ascii=False, indent=1)
