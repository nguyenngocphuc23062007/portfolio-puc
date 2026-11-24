# Tách nền trắng của 3 tấm hình vẽ (tạo bằng Figma AI), cắt từng vật thành PNG trong suốt và lấy đường viền.
# Chạy: uv run --with pillow --with numpy --with scikit-image python design/forest-3d/cut_art.py
# Kết quả: design/forest-3d/art/<tên>.png và art/outlines.json (đa giác viền, toạ độ điểm ảnh).
import os, json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from skimage import measure

HERE = os.path.dirname(os.path.abspath(__file__)); ART = os.path.join(HERE, 'art')
NAMES = {  # thứ tự: trái sang phải, trên xuống dưới
    'trees': ['pine', 'yellow', 'round', 'flame', 'pine2'],
    'plants': ['shrub', 'shrubY', 'flowerBush', 'fern', 'grass', 'shrubDark'],
    'props': ['mushrooms', 'foxSit', 'foxWalk', 'boulder', 'lantern', 'log'],
}

def cut(sheet, names):
    src = np.asarray(Image.open(os.path.join(ART, 'sheets', sheet + '.png')).convert('RGBA')).astype(int)
    im = src[..., :3]; H, W, _ = im.shape
    if src[..., 3].min() < 128:   # ảnh đã có nền trong suốt
        bg = src[..., 3] < 128
    else:                          # nền trắng: loang từ mép vào
        light = (im.min(2) > 226) & ((im.max(2) - im.min(2)) < 22)
        lab, _ = ndimage.label(light)
        border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
        bg = np.isin(lab, list(border))
    fg = ndimage.binary_opening(~bg, iterations=2)
    fg = ndimage.binary_fill_holes(fg)
    lab2, n = ndimage.label(fg)
    sizes = ndimage.sum(fg, lab2, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if s > 2500]
    objs = []
    for i in keep:
        ys, xs = np.where(lab2 == i)
        objs.append((ys.min(), ys.max(), xs.min(), xs.max(), i))
    # gộp thành hàng theo vị trí, sắp xếp trái sang phải
    one_row = sheet == 'trees'
    objs.sort(key=lambda o: (False if one_row else (o[0] + o[1]) / 2 > H * 0.55, (o[2] + o[3]) / 2))
    out = {}
    for (y0, y1, x0, x1, i), name in zip(objs, names):
        pad = 6; y0, x0 = max(0, y0 - pad), max(0, x0 - pad); y1, x1 = min(H - 1, y1 + pad), min(W - 1, x1 + pad)
        m = (lab2[y0:y1 + 1, x0:x1 + 1] == i)
        a = Image.fromarray(np.where(m, src[y0:y1 + 1, x0:x1 + 1, 3], 0).astype(np.uint8))
        rgb = Image.fromarray(im[y0:y1 + 1, x0:x1 + 1].astype(np.uint8))
        rgba = rgb.copy(); rgba.putalpha(a)
        rgba.save(os.path.join(ART, name + '.png'))
        h, w = m.shape
        cs = measure.find_contours(np.pad(m.astype(float), 1), 0.5)
        polys = []
        for c in cs:
            if len(c) < 30: continue
            c = measure.approximate_polygon(c, tolerance=1.2)
            polys.append([[float(p[1] - 1), float(p[0] - 1)] for p in c])
        polys.sort(key=len, reverse=True)
        out[name] = {'w': w, 'h': h, 'polys': polys[:1]}
    return out

if __name__ == '__main__':
    allp = {}
    for sheet, names in NAMES.items():
        allp.update(cut(sheet, names))
    json.dump(allp, open(os.path.join(ART, 'outlines.json'), 'w'))
    for k, v in allp.items(): print(k, v['w'], v['h'], len(v['polys'][0]) if v['polys'] else 0)
