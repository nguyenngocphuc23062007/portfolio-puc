---
name: web-3d-performance
description: How to measure and speed up the portfolio's three.js map (city/) on desktop, tablet and phone - render pacing, device quality tiers, adaptive pixel ratio, on-demand shadow maps, static merging, label layers, hashed assets and module preloading, with the measured before/after numbers. Use with the performance and core-web-vitals skills whenever the map feels slow, before adding heavy scenery, or when testing on new devices.
---

# Hiệu năng bản đồ 3D (three.js)

Dùng kèm skill `performance` và `core-web-vitals`, cộng `papercraft-ui` và `natural-placement` khi đổi cảnh.

## Đo trước, sửa sau

1. Dựng trang bằng `python3 city/build.py`, rồi chạy `cd city/out && python3 -m http.server 8770`.
2. Mở `http://localhost:8770/index.html?t=10&inspect&debug`. Có ba nguồn số liệu:
   - `window.__siteMap`: `frameMs` là thời gian CPU trung bình mỗi khung; `frames` là số khung đã vẽ (gọi `reset()` trước khi đo).
   - `window.__map.renderer.info`: đặt `autoReset = false`, gọi `reset()`, đợi một khung rồi đọc `render.calls` (số lệnh vẽ, gồm cả lượt bóng, lượt pháp tuyến và lượt hậu kỳ).
   - Mốc thời gian dựng: `performance.getEntriesByType('mark')`, gồm các mốc `map-step-0…6`, `map-bake-start`/`end` và `map-ready`.
3. Thử ba cỡ màn hình bằng `resize_window`: máy tính (1280×760), `tablet` và `mobile` (giả lập màn cảm ứng, DPR 2). Trên điện thoại còn phải kiểm tra trang không cuộn ngang (`scrollWidth === innerWidth`).
4. Giả lập trong khung trình duyệt vẫn dùng GPU của máy Mac, nên **số khung hình không đại diện cho điện thoại thật**. Chỉ dùng giả lập để kiểm tra mức chất lượng có bật đúng không; tốc độ thật phải đo trên máy thật.

## Những gì đã làm (và vì sao)

| Việc | Cách làm | Lý do |
|---|---|---|
| Gộp khối tĩnh | `bakeStatic()` (xem skill `papercraft-ui`) | Lệnh vẽ là nút thắt chính; các hướng dẫn three.js đặt mục tiêu khoảng 100–200 lệnh vẽ trên điện thoại yếu |
| Nhịp vẽ theo thời gian | tối đa 60 khung/giây; 30 khung/giây sau 12 giây không thao tác | Màn 120 Hz không cần vẽ gấp đôi cho một bản đồ; đỡ tốn pin khi để yên |
| Bóng đổ khi cần | chỉ vẽ lại bản đồ bóng khi mặt trời đổi, lúc mở đầu, khi camera đang bay, và cứ 4 khung một lần cho vật di chuyển | Trước đây vẽ lại mọi khung, mỗi lần là thêm một lượt vẽ cả cảnh |
| Mức chất lượng theo thiết bị | màn cảm ứng: mật độ điểm ảnh tối đa 1.5, MSAA 2, bóng 1536; máy tính: 2, 4, 3072 | Mật độ điểm ảnh là chi phí lớn nhất trên điện thoại |
| Tự giảm và tăng độ nét | khung chậm hơn 1/40 giây kéo dài 1.5 giây thì giảm mật độ điểm ảnh 0.25 (thấp nhất 1); nhanh ổn định 6 giây thì tăng lại | Theo cách "adaptive pixel ratio" mà các hướng dẫn hiệu năng three.js khuyên dùng |
| Nhãn là lớp riêng | `.labels > * { will-change: transform }` | Nhãn dời mỗi khung; chữ giấy cắt có viền và bóng nên vẽ lại khá tốn |
| Tên file có mã băm | `build.py` đặt tên kiểu `map-engine.<băm>.js` | Máy chủ thử không gửi Cache-Control nên trình duyệt từng chạy module cũ sau khi sửa; có mã băm thì bản mới luôn được tải, khi đưa lên mạng có thể đặt bộ đệm lâu |
| Tải trước module | import map đặt trong `<head>`, tiếp theo là `modulepreload` cho three.js, ba phần bổ sung và các file engine | Đỡ phải tải nối đuôi từng file. **Import map phải đứng trước mọi `modulepreload`**, nếu không trình duyệt báo lỗi không phân giải được "three" |
| Màn chờ ngắn hơn | tối thiểu 0.5 giây thay vì 1.4 giây | Bản đồ dựng xong trong khoảng 0.6 giây, nên màn chờ cũ giữ người xem vô ích |

## Kết quả đo ngày 2026-11-24

Đo trong khung trình duyệt trên máy Mac, máy chủ ở máy, three.js đã nằm sẵn trong bộ đệm.

| | Trước | Sau |
|---|---|---|
| Thời điểm bản đồ hiện (`map-ready`) | 1.619 ms | 858 ms |
| Số khung vẽ mỗi giây khi đang thao tác | 97–122 (theo tần số màn hình) | 60 |
| Số khung vẽ mỗi giây khi để yên hơn 12 giây | như lúc thao tác | 29–30 |
| Lệnh vẽ mỗi khung (toàn bản đồ) | 2.011 ở mọi khung | 1.333 ở 3/4 số khung, 2.011 ở khung vẽ lại bóng |
| Thời gian CPU mỗi khung | 9,7–12,1 ms | khoảng 8 ms |
| Điện thoại giả lập (DPR 2) | mật độ điểm ảnh 2 | 1.5, bóng 1536, MSAA 2, không cuộn ngang |

## Còn có thể làm

- Tự lưu three.js cùng trang, hoặc gom các module lại, để không phụ thuộc CDN và bật nén Brotli trên máy chủ thật.
- Vẽ lượt pháp tuyến (dùng cho nét mực) ở nửa độ phân giải trên điện thoại.
- Dùng phiên bản đơn giản hơn (LOD) cho rừng xa.
- Tách vòng lặp lấy mẫu rừng (khoảng 200 ms) thành nhiều đoạn nhỏ để không chặn luồng chính.
- Đo trên điện thoại và Safari thật; chưa làm.

## Nguồn đã học

- [Utsubo: 100 Three.js tips that actually improve performance](https://www.utsubo.com/blog/threejs-best-practices-100-tips): gộp và nhân bản để giảm lệnh vẽ, giới hạn mật độ điểm ảnh trên điện thoại.
- [Codrops: Building efficient three.js scenes (2025)](https://tympanus.net/codrops/2025/02/11/building-efficient-three-js-scenes-optimize-performance-while-maintaining-quality/)
- [PlayCanvas optimization guidelines](https://developer.playcanvas.com/user-manual/optimization/guidelines/): mục tiêu lệnh vẽ cho điện thoại yếu.
- [vue-threejs: scaling performance](https://blueraai.github.io/vue-threejs/advanced/scaling-performance.html): vẽ theo nhu cầu, giảm hậu kỳ khi đang chuyển động.
- [three.js forum: restricting viewport size for mobile](https://discourse.threejs.org/t/restricting-viewport-size-for-mobile/7270): không có mật độ điểm ảnh "đúng" cho mọi máy, nên phải tự điều chỉnh.
- [Babylon.js forum: optimizing on lower-end devices](https://forum.babylonjs.com/t/best-practices-for-optimizing-babylon-js-scenes-not-just-on-lower-end-devices/58688): đèn không đổi thì chỉ vẽ bản đồ bóng một lần.
- Skill `performance` và `core-web-vitals` trong dự án: đo trước khi sửa, so trước và sau trong cùng điều kiện, ngân sách tải trang.

## Nhật ký

- 2026-11-24: viết skill và áp dụng toàn bộ bảng trên. Lỗi gặp phải: (1) module cũ bị giữ trong bộ đệm, đã sửa bằng tên file có mã băm; (2) đặt `modulepreload` trước import map làm trang dừng ở màn chờ, đã sửa bằng cách chuyển import map lên `<head>`; (3) cách bỏ xen kẽ một khung không ra 30 khung/giây trên màn 120 Hz, nên đổi sang giới hạn theo thời gian.
