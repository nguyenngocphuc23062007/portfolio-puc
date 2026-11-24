# Chỉnh màu sau render cho khớp ảnh mẫu: chuyển trung bình và độ lệch màu (không gian Lab) về đúng ảnh mẫu,
# rồi thêm tối viền và hạt phim.
# Chạy: uv run --with pillow --with numpy --with scikit-image python design/forest-3d/grade.py <vào.png> [ra.png] [--ref ảnh_mẫu] [--amount 0.85]
import sys, os
import numpy as np
from PIL import Image
from skimage import color

args = sys.argv[1:]
def opt(name, default):
    if name in args:
        i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return type(default)(v)
    return default
HERE = os.path.dirname(os.path.abspath(__file__))
REF = opt('--ref', os.path.join(HERE, '..', 'mau', 'rung-ni.png'))
AMOUNT = opt('--amount', 0.85)
src, dst = args[0], (args[1] if len(args) > 1 else args[0])

im = np.asarray(Image.open(src).convert('RGB')).astype(float) / 255
if os.path.exists(REF) and AMOUNT > 0:
    ref = np.asarray(Image.open(REF).convert('RGB')).astype(float) / 255
    h0, w0 = ref.shape[:2]; ref = ref[int(h0 * 0.04):int(h0 * 0.96), int(w0 * 0.03):int(w0 * 0.97)]  # bỏ mép đen của ảnh chụp video
    a, r = color.rgb2lab(im), color.rgb2lab(ref)
    out = (a - a.mean((0, 1))) / (a.std((0, 1)) + 1e-6) * r.std((0, 1)) + r.mean((0, 1))
    im = np.clip(color.lab2rgb(a * (1 - AMOUNT) + out * AMOUNT), 0, 1)
h, w, _ = im.shape; yy, xx = np.mgrid[0:h, 0:w]
d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
im *= (1 - 0.22 * np.clip((d - 0.6) / 0.8, 0, 1) ** 1.5)[..., None]
im += np.random.default_rng(1).normal(0, 0.012, im.shape)
Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8)).save(dst)
