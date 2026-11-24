# Bản đồ project (thành phố giấy gấp)

Bản đồ 3D: mỗi thị trấn là một nhóm việc, mỗi toà nhà là một project. Bấm tên thị trấn để bay tới, bấm toà nhà để xem project.

## Học từ yahaha.net

- Bản đồ của yahaha.net (tác giả Seven) **không vẽ tay từng thành phố**. Nó được sinh từ một file `site.json` bằng engine **site-to-map** của cùng tác giả.
- Engine này viết bằng Three.js 0.170 và gồm ba phần:
  - `world-gen.js` sinh vùng đất từ một hạt giống (seed): bờ biển, núi, sông, hồ, ruộng, đường và cầu, rồi đặt các thị trấn theo vai trò.
  - `map-engine.js` dựng mọi thứ bằng mã:
    - nhà theo từng `kind` (khoảng 40 kiểu nhà và 11 kiểu vật trang trí)
    - cây, cừu, cối xay gió, thuyền, chim, người đi đường, xe ngựa, khói
    - viền mực, nhoè kiểu mô hình thu nhỏ, ánh sáng theo giờ thật
  - `daylight.js` đổi màu trời theo giờ ngay từ lúc trang mới hiện.
- **Giấy phép:**
  - Mã của yahaha.net (repo `dofy/yahaha`) **không có giấy phép**, nên chỉ đọc để học, không chép.
  - Engine site-to-map được phát hành **MIT**, nên dùng được nếu giữ ghi công. Thư mục `engine/` là bản chép từ `references/papercraft/site-to-map` (commit f07e5f3), kèm file giấy phép `engine/LICENSE-site-to-map`.

## Thêm so với bản gốc

Những chỗ đã sửa trong `engine/`:

- Cáo giấy:
  - cáo đi dạo trên đường, vẫy đuôi khi đi
  - mỗi thị trấn có một con cáo ngồi canh ở rìa, đuôi đung đưa

  Phần này được đánh dấu bằng chú thích "thêm cho portfolio của Puc" trong `map-engine.js`.
- Giao diện tiếng Việt, bao gồm cả chữ trên màn chờ trong `engine/template.html`.
- Giao diện kiểu giấy cắt nằm trong `engine/papercraft-ui.css` và giữ nguyên bảng màu gốc. Cách làm học từ:
  - CSS-Tricks "Stacked Paper": các tờ lót xếp lệch phía sau
  - Aimee's Papercraft World: đường khâu nét đứt
  - hướng dẫn clip-path của MDN và Chrome: mép cắt sắc, bóng đặt ở lớp ngoài để không bị cắt mất

  Nhãn 3D chỉ dùng box-shadow vì chúng di chuyển mỗi khung hình.
- Nhà cửa chi tiết hơn theo ảnh tham khảo `design/city-ref/bo-chi-tiet-lang.png`:
  - cửa sổ có khung, cửa chớp và bồn hoa
  - cửa ra vào có bậc và mái hiên
  - mái có ngói và nóc, ống khói có nắp
  - cỏ quanh chân tường
  - mỗi nhà ngoại ô có 2–3 món đồ trong sân
- Mọi khối đứng yên được gộp theo chất liệu (`bakeStatic()`), nên lệnh vẽ giảm mạnh dù có nhiều chi tiết hơn. Thêm `?debug` vào địa chỉ để xem số liệu.
- Cảnh vật được bố trí theo skill `natural-placement`:
  - nhà bám dọc đường, cửa quay ra đường, càng xa càng thưa; thêm xóm nhỏ
  - rừng lấy mẫu đĩa Poisson, mép thưa dần, có trảng cỏ
  - cây mọc thành mảng theo loài; có dải cây ven sông, hàng cây mép ruộng và cây lẻ trên đồng
- Builder viết bằng Python (`build.py`) vì máy không có Node.

## Chạy

```bash
python3 city/build.py
```

```bash
cd city/out && python3 -m http.server 8770
```

Sau đó mở http://localhost:8770.

`build.py` đặt mã băm vào tên file JS và CSS (ví dụ `map-engine.a17f840f.js`), nên mỗi lần dựng lại, trình duyệt sẽ tải bản mới chứ không dùng bản cũ trong bộ đệm.

Cách đo và tối ưu hiệu năng xem trong skill `web-3d-performance`. Thêm `?inspect&debug` vào địa chỉ để có số liệu.

Các tham số thêm vào địa chỉ để xem thử:

- `?t=21`: xem lúc 21 giờ.
- `?still=4`: giữ khung hình đứng yên để chụp.
- `#cao-do`: mở thẳng thị trấn Cáo Đỏ.

## Cần điền

Mọi `url` trong `site.json` đang là chỗ trống dạng `/du-an/<tên>`, chưa có trang thật. Hãy thay bằng link GitHub, trang demo hoặc trang project. Có thể sửa luôn tên, mô tả và cách chia thị trấn cho đúng ý.

## Đoạn mở đầu "portfolio" thành "puc"

- Mã: `engine/logo-intro.js` và `engine/logo-intro.css` (chuyển từ bản thử `design/logo-intro/demo/`). Kịch bản ở `design/logo-intro/PROMPT.md`, danh sách động tác của cáo ở `design/logo-intro/CAO-CAN-VE.md`.
- Ảnh cáo và hiệu ứng: cắt từ ảnh người dùng gửi bằng `design/logo-intro/tools/cut_bo3.py` rồi `cut_fx.py` (chạy theo thứ tự này). `build.py` chép các ảnh đang dùng vào `out/intro/`.
- Chỉ chạy lần đầu trong mỗi phiên (`sessionStorage`), không chạy khi máy bật giảm chuyển động. Một đoạn mã nhỏ trong `<head>` của `template.html` quyết định việc này trước khi trang vẽ.
- Bản đồ dựng ngầm bên dưới, rồi chờ `window.__pucIntroGate` (lúc logo bắt đầu thu về góc) mới chạy màn mở đầu của nó. Logo thu về đúng chỗ chữ "puc" của bản đồ, và đổi chỗ khi bản đồ hiện khung giao diện.
- Tham số: `?intro` chạy lại, `?nointro` bỏ qua, `?it=2.4` dừng ở giây 2.4 để chụp kiểm tra, `?ispeed=.25` chạy chậm. (`?t=` vẫn là giờ trong ngày của bản đồ.)
- Bấm, chạm, cuộn hoặc nhấn phím giữa chừng thì nhảy tới logo cuối.

