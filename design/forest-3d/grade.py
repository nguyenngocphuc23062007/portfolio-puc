# Chỉnh màu sau render cho giống ảnh chụp mô hình: bóng ngả xanh ngọc, sáng ấm, tương phản thấp, tối viền, hạt phim.
import sys
import numpy as np
from PIL import Image
p = sys.argv[1]
im = np.asarray(Image.open(p).convert('RGB')).astype(float) / 255
lum = im @ [0.299, 0.587, 0.114]
shadow = np.clip(1 - lum * 1.6, 0, 1)[..., None]; high = np.clip((lum - 0.55) * 2.2, 0, 1)[..., None]
im = im + shadow * np.array([-0.02, 0.025, 0.03]) + high * np.array([0.03, 0.015, -0.02])
im = 0.035 + im * 0.95                      # nâng điểm đen, hạ tương phản
gray = (im @ [0.299, 0.587, 0.114])[..., None]; im = gray + (im - gray) * 1.06
h, w, _ = im.shape; yy, xx = np.mgrid[0:h, 0:w]
d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
im *= (1 - 0.34 * np.clip((d - 0.5) / 0.8, 0, 1) ** 1.5)[..., None]
im += np.random.default_rng(1).normal(0, 0.012, im.shape)
Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8)).save(sys.argv[2] if len(sys.argv) > 2 else p)
