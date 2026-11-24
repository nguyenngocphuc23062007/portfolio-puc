# Cắt bảng hiệu ứng (ảnh 56 người dùng gửi ngày 2026-11-24): mỗi hàng một hiệu ứng, cột đầu là chữ nhãn.
# Dò đường kẻ ngang (ranh giới hàng) và đường kẻ dọc trong từng hàng; bỏ cột nhãn và ô trống; chỉ bỏ nền, không đổi cỡ.
# Chạy SAU cut_bo3.py (cut_bo3.py ghi lại fox.json từ đầu, mất mục fx).
# Chạy: uv run --with pillow --with numpy python design/logo-intro/tools/cut_fx.py
import json, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'cao/2-anh-ban-gui/bo-3/56.webp'); OUT = os.path.join(ROOT, 'cao/5-bo-3')
NAMES = ['bui-chay', 'bui-dap', 'bui-bung', 'dat-vang', 'dat-roi', 'vach-rung', 'bong']

def bg_mask(rgb, light=175):
    mn, mx = rgb.min(2), rgb.max(2); cand = (mn > light) & (mx - mn < 28)
    h, w = cand.shape; seen = np.zeros_like(cand)
    st = [(y, x) for x in range(w) for y in (0, h - 1) if cand[y, x]] + [(y, x) for y in range(h) for x in (0, w - 1) if cand[y, x]]
    for y, x in st: seen[y, x] = True
    while st:
        y, x = st.pop()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and cand[ny, nx] and not seen[ny, nx]: seen[ny, nx] = True; st.append((ny, nx))
    return seen

def groups(idx):
    out = []
    for v in idx:
        if out and v - out[-1][1] <= 2: out[-1][1] = v
        else: out.append([v, v])
    return out

a = np.asarray(Image.open(SRC).convert('RGBA')).astype(int); H, W = a.shape[:2]
dark = (a[:, :, :3].max(2) < 120) & (a[:, :, 3] > 20)
rows = groups([y for y in range(H) if dark[y].sum() > W * .7])
meta = {}
for ri, name in enumerate(NAMES):
    y0, y1 = rows[ri][1] + 4, rows[ri + 1][0] - 4
    band = dark[y0:y1]
    cols = groups([x for x in range(W) if band[:, x].sum() > (y1 - y0) * .8])
    cells = [(cols[k][1] + 4, cols[k + 1][0] - 4) for k in range(len(cols) - 1)][1:]   # bỏ cột nhãn
    frames = []
    for x0, x1 in cells:
        cell = a[y0:y1, x0:x1]; rgb = cell[:, :, :3]; al = (cell[:, :, 3] > 20) & ~bg_mask(rgb)
        if al.sum() < 15: continue                       # ô trống
        frames.append((rgb, al))
    cw = max(f[0].shape[1] for f in frames); ch = max(f[0].shape[0] for f in frames)
    pads = []
    for rgb, al in frames:   # căn giữa ngang, giữ đáy ô (mặt đất) cho mọi khung
        R = np.zeros((ch, cw, 3), int); A_ = np.zeros((ch, cw), bool); ox = (cw - rgb.shape[1]) // 2; oy = ch - rgb.shape[0]
        R[oy:, ox:ox + rgb.shape[1]] = rgb; A_[oy:, ox:ox + rgb.shape[1]] = al; pads.append((R, A_))
    ys = np.where(np.any([p[1].any(1) for p in pads], 0))[0]; xs = np.where(np.any([p[1].any(0) for p in pads], 0))[0]
    t, b, l, r = ys.min(), ys.max(), xs.min(), xs.max(); fw, fh = r - l + 1, b - t + 1
    sheet = np.zeros((fh, fw * len(pads), 4), np.uint8)
    for k, (R, A_) in enumerate(pads):
        sheet[:, k * fw:(k + 1) * fw, :3] = R[t:b + 1, l:r + 1]; sheet[:, k * fw:(k + 1) * fw, 3] = A_[t:b + 1, l:r + 1] * 255
    Image.fromarray(sheet).save(os.path.join(OUT, f'{name}.png'))
    meta[name] = dict(n=len(pads), w=int(fw), h=int(fh), ground=int(fh))
    print(name, meta[name])
p = os.path.join(OUT, 'fox.json'); j = json.load(open(p)); j['fx'] = meta
json.dump(j, open(p, 'w'), ensure_ascii=False, indent=1)
