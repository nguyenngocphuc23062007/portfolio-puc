---
name: papercraft-ui
description: Design rules for the portfolio's paper-craft interface (the 3D project map in city/ and any page that shares its look) - palette, type, cut-paper techniques, and a list of AI-looking defaults that are banned here. Use before designing, restyling or reviewing any interface in this portfolio, together with the frontend-design skill.
---

# Giao diện giấy thủ công (papercraft UI)

Áp dụng cho bản đồ project ở `city/` và mọi trang dùng chung kiểu giấy. Phần mã nằm ở `city/engine/papercraft-ui.css`. Màu giấy đổi theo giờ được đặt trong `city/engine/daylight.js`.

## Quy trình mỗi lần làm giao diện

1. Gọi skill `frontend-design:frontend-design`, đọc lại file này rồi mới bắt tay sửa.
2. Viết kế hoạch ngắn gồm màu, chữ, bố cục và điểm nhấn. Đối chiếu kế hoạch với danh sách **Cấm** bên dưới. Phần nào trùng danh sách thì sửa trước khi viết mã.
3. Sau khi sửa, dựng lại trang bằng `python3 city/build.py`. Chạy `cd city/out && python3 -m http.server 8770` rồi xem trong trình duyệt ở 4 trường hợp:
   - `?t=10&still=4`: ban ngày
   - `?t=21&still=4`: ban đêm
   - rộng 800 px: máy tính bảng, giao diện chuyển sang bong bóng
   - rộng 375 px: điện thoại, trang không được cuộn ngang

   Thêm `#<id-thị-trấn>` vào cuối địa chỉ để xem trong một thị trấn. Đổi tham số `v=` mỗi lần tải để trình duyệt không dùng bản cũ.
4. Chụp màn hình và tự soi. Chưa xem ảnh chụp thì không được nói là đã xong.
5. Học được điều gì mới thì ghi vào mục **Nhật ký** ở cuối file này.

## Chất liệu và màu

Mọi màu đều lấy từ cảnh rừng nỉ (`design/forest-3d`) và con cáo. Không có màu nào đặt ra chỉ để trang trí.

| Vai trò | Ban ngày | Ghi chú |
|---|---|---|
| Giấy (`--ui-card`) | `#fafbf7`, giấy trắng | người dùng muốn giao diện luôn trắng; không dùng tông kem |
| Mực (`--ui-ink`) | `#25321f`, xanh thông đậm | không dùng đen pha nâu |
| Chữ phụ / mờ | `#435238` / `#65734f` | |
| Đường kẻ (`--ui-line`) | `#c2cca7` | |
| Băng dính, chọn (`--ui-hot`) | `#ecc961`, mù tạt | dùng cho mục đang chọn và băng dính |
| Bìa kraft lót (`--pc-kraft`) | pha `--ui-card` với `#a47a49` | chỉ đặt sau tấm thông tin và bảng phím tắt |
| Hành động (`--pc-fox`) | `#d9661c`, cam cáo | chỉ dùng cho nút "Xem project" và mục đang chọn trên bản đồ; chữ trên nền này màu tối `#22180f` |

Giấy luôn trắng ở mọi giờ, chỉ ngả theo ánh sáng: trắng ấm lúc bình minh và hoàng hôn (`#fbf9f5`, `#fbf8f3`), trắng xám dưới ánh trăng ban đêm (`#dde1df`). Mực luôn tối. Bảng đầy đủ theo từng giờ có trong `daylight.js`.

## Chữ

- **Tiêu đề là chữ giấy cắt.** Áp dụng cho tên thị trấn trên bản đồ, tiêu đề tấm thông tin, logo "puc", màn chờ và bong bóng trên điện thoại.
  - Font **Paytone One**: nét dày, đầu nét bằng như cắt từ bìa cứng, có dấu tiếng Việt.
  - `city/engine/papercut-letters.js` tách mỗi tiêu đề thành từng chữ cái. Mỗi chữ là một mẩu giấy xoay lệch −3° đến 3° và nhích lên xuống 1–1.5 px theo một dãy cố định, nên lần nào tải cũng giống nhau. Người đọc màn hình vẫn đọc cả câu nhờ một bản chữ ẩn (`.pc-sr`).
  - **Trên giấy trắng:** chữ mực xanh thông, chồng lên hai lớp bìa (xô thơm rồi kraft) bằng `text-shadow` nhích 0.035em mỗi lớp, cộng một bóng mềm. Đây là cách của shadcn "Paper Cut Text".
  - **Trên bản đồ:** tên thị trấn không có khung. Đó là chữ dán cắt rời, viền giấy trắng (`-webkit-text-stroke: .26em` cộng `paint-order: stroke fill`), màu lấy từ màu mái của thị trấn pha với mực. Rê chuột thì chữ nhấc lên 3 px.
- **Căn chữ giấy cắt trong khung theo phần mực, không theo hộp dòng.** Paytone One có phần trên dòng rất cao (1.095em), nên chữ thường như "puc" luôn rơi xuống đáy khung. Đo bằng canvas `measureText` (`actualBoundingBoxAscent`/`Descent`), đặt `line-height: 1` rồi nhấc cả từ lên đúng độ lệch (với "puc" là .245em). Muốn soi thì phóng khung lên 4 lần bằng `transform: scale(4)` rồi chụp màn hình.
- **Be Vietnam Pro** (400–600): mọi chữ còn lại. Chữ dài mà cắt từng chữ cái thì khó đọc.
- Không nghiêng, không viết hoa toàn bộ. Tên địa danh có giãn chữ `.12em` như chữ trên bản đồ thật.
- Đã kiểm tra font nào có dấu tiếng Việt bằng cách gọi `fonts.googleapis.com/css2` rồi xem có nhóm `/* vietnamese */` không.
  - Có: Paytone One, Baloo 2, Grandstander, Phudu, Bungee, Patrick Hand, Mali.
  - Không: Lilita One, Chewy, Rubik.
  - Font "Paper Cutouts" (online-fonts) không có dấu tiếng Việt và giữ bản quyền, nên không dùng.

## Kỹ thuật giấy (đã thử và dùng được)

- **Mép giấy:** dùng `clip-path: polygon(...)` với góc vát 3–5 px và cạnh lệch tối đa 1.5 px. Hai đường cắt có sẵn là `--pc-cut` và `--pc-cut-2`.
  - **Không** dùng bộ lọc SVG `feTurbulence`/`feDisplacementMap` cho mép giấy. Đã thử và bị bỏ vì mép nhoè, trông bẩn, lại nặng máy.
- **Bóng:** clip-path cắt luôn bóng. Vì vậy tờ giấy nằm ở `::before`, còn `filter: drop-shadow` đặt ở chính khung bên ngoài. Bóng gồm hai lớp: một lớp sát mép 1 px và một lớp tỏa 4–6 px.
- **Tờ lót:** chỉ dùng một tờ kraft lệch khoảng 10 px và xoay khoảng 1.5°. Chỉ đặt sau tấm thông tin, vì đây là điểm nhấn duy nhất của trang.
- **Băng dính:** mù tạt bán trong suốt, hai đầu răng cưa (`--pc-tape-ends`), dán chéo hai góc trên của tấm thông tin. Mục đang chọn cũng được đánh dấu bằng một miếng băng dính dán dưới chữ.
- **Vân giấy:** dùng `--pc-fibre`, một ảnh nhiễu SVG rất nhạt có độ đậm 0.08, đặt làm lớp nền trên màu giấy.
- **Nhãn 3D trên bản đồ:** nhãn di chuyển mỗi khung hình, nên không dùng `filter` hay `clip-path`. Tờ kraft lót được giả bằng `box-shadow` lệch.
- **Huy hiệu thị trấn:** lá cờ đuôi én cắt bằng clip-path, màu lấy theo màu mái của thị trấn đó.
- **Ô màu toà nhà:** mẩu giấy vuông xoay khoảng −7°.

## Nhà cửa và đồ vật 3D (bản đồ ở `city/`)

- **Ảnh tham khảo:** `design/city-ref/bo-chi-tiet-lang.png` (Figma AI vẽ, nằm ở node 20:233 trong file Figma).
  - Nhà có khung cửa sổ trắng, cửa chớp xanh ô liu, bồn hoa, cửa ra vào có bậc đá và mái hiên, nắp ống khói, nóc mái và hàng ngói.
  - Đồ trong sân: hàng rào trắng, cổng gỗ, hộp thư, đống củi, đống rơm, luống rau, dây phơi, thùng gỗ và chậu cây.
- **Mã:** bộ chi tiết nằm trong `city/engine/map-engine.js`, tìm chú thích "bộ chi tiết nhà cửa".
  - Hàm cửa và mái: `dressWindow`, `dressDoor`, `tufts`, `chimneyCap`, `ridgeCap`, `roofLines`.
  - Hàm đồ trong sân: `yardProp(kind)`.
  - Mọi khối dùng chung một bộ hình học `KG` (hộp, trụ, khối hai mươi mặt, nón 6 cạnh, chóp 4 cạnh), đặt bằng `kp(...)` và co giãn bằng scale. **Không** tạo `new THREE.BoxGeometry(...)` mới cho mỗi chi tiết.
- **Nhân bản để nhẹ máy:** `bakeStatic()` chạy một lần sau khi dựng xong, gộp mọi khối đứng yên thành một khối cho mỗi chất liệu.
  - Toà nhà của project được gộp trong chính toà đó, nên vẫn bấm chọn, tô sáng và mọc lên lúc mở đầu được.
  - Vật có hoạt hình được tự nhận ra (chạy thử các hàm hoạt hình rồi so ma trận) và để riêng.
  - Đo ngày 2026-11-24 (dùng `?debug`, xem `window.__map.baked` và `renderer.info`): khoảng 5.100 khối gộp còn 119, khoảng 800–1.900 lệnh vẽ mỗi khung tuỳ góc nhìn. Trước khi gộp là khoảng 6.000 lệnh vẽ với ít chi tiết hơn.
- **Thêm vật mới:**
  - Vật đứng yên chỉ cần dựng bằng `kp` là sẽ được gộp tự động.
  - Vật cần đổi chất liệu riêng hoặc bấm được thì phải thêm vào danh sách giữ riêng (`pickables` hoặc `districts`).
  - Đặt tên hàm mới cẩn thận: engine là một hàm rất dài, trùng tên (như `ridge`) sẽ làm trang trắng.

## Cấm (các mặc định trông như AI làm)

Bản đầu tiên của bản đồ (chép từ engine site-to-map) mắc gần hết những lỗi này, và người dùng đã chê là "bị AI quá":

- Nền kem `#F4F1EA`–`#FFFDF8` đi với tiêu đề chữ có chân in nghiêng (Cormorant) và điểm nhấn san hô hoặc đất nung (`#ff6554`, `#D97757`).
- Nhãn viết hoa giãn chữ đặt trên tiêu đề, ví dụ "PUC · TRANG VÀ THIẾT KẾ".
- Chuỗi nối bằng dấu chấm giữa: "A · B · C". Thay bằng dấu phẩy hoặc câu thường.
- Chữ đơn cách (monospace) cho nhãn nhỏ, giờ, phím tắt.
- Mã ô kiểu "A1", "B2" khi chúng không giúp người xem việc gì.
- Mọi thứ cùng một độ bo góc, cùng một bóng xám mềm, viền hình viên thuốc khắp nơi.
- Trang trí chồng chất: khâu nét đứt cộng góc gấp cộng nếp gấp cộng băng dính trên cùng một tấm. Trang chỉ có một điểm nhấn; trước khi xong, bỏ bớt một món.
- Mũi tên "→" gắn sau chữ trên nút, dấu gạch dài có cách hai bên trong nhãn.

## Bố cục và cách đi lại (người dùng chốt 2026-11-24)

- Trên màn hình chỉ có: chữ "puc", giờ ở góc dưới (không có dòng bản quyền, khung giờ thẳng cột với khung "puc"), tên thị trấn và tên project trên bản đồ, và tấm thông tin.
  - Tấm thông tin chỉ gồm tiêu đề và danh sách tên.
  - Không có thanh công cụ, đường dẫn vị trí, la bàn hay dòng hướng dẫn.
  - Không có dòng mô tả, số đếm hay đoạn giới thiệu.
- Mọi thao tác bằng chuột và cuộn, không cần chữ hướng dẫn:
  - kéo chuột trái để xoay, kéo chuột phải để dời
  - cuộn hoặc chụm hai ngón để phóng to, thu nhỏ
  - bấm tên thị trấn để bay tới, bấm toà nhà để chọn
  - bấm chỗ trống để lùi một bước
  - cuộn ra xa hơn 1.6 lần khoảng nhìn của thị trấn thì tự về toàn bản đồ, nhưng chỉ khi chính người dùng đã kéo hoặc cuộn
  - bấm "puc" để về góc nhìn ban đầu
- Đừng thêm lại chữ giải thích. Nếu thao tác chưa dễ hiểu, sửa ở cách bản đồ phản hồi: con trỏ đổi hình, chữ nhấc lên khi rê chuột.

## Văn bản

Viết bằng tiếng Việt thường, câu ngắn, động từ rõ. Ví dụ: "Bấm một toà nhà để xem project, bấm Esc để quay lại."

Không lấp chỗ trống bằng chữ. Mỗi dòng chữ chỉ làm một việc.

## Nguồn đã học

- [CSS-Tricks: Stacked Paper Effect](https://css-tricks.com/?p=13593): xếp tờ lót phía sau tờ chính.
- [MDN: CSS clipping](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_masking/Clipping) và [Chrome: Shaped Cutouts](https://developer.chrome.com/docs/modern-web-guidance/guides/visual-design/shaped-cutouts): cắt mép bằng clip-path, đặt bóng ở lớp ngoài.
- [dev.to: CSS paper effects](https://dev.to/s_aitchison/3-experiments-with-css-paper-effects-2o56): băng dính, góc gấp.
- Aimee's Papercraft World (`references/papercraft/aimee-weis-papercraft-world`, mã MIT): khung nét đứt như đường khâu. Ở đây đã thử và bỏ vì quá nhiều chi tiết.
- [shadcn: Paper Cut Text](https://www.shadcn.io/text/paper-cut-text): chồng nhiều lớp chữ, lớp dưới nhạt dần về màu nền, mỗi lớp nhích 0.03em.
- Skill `frontend-design`: danh sách các mặc định trông như AI làm.

## Nhật ký

- 2026-11-24: bỏ bộ lọc SVG làm mép giấy vì bị nhoè, chuyển sang clip-path. Bỏ tông kem, chữ Cormorant và màu san hô vì người dùng thấy giống AI; đổi sang giấy xanh xô thơm, chữ Baloo 2 và Be Vietnam Pro, màu cam cáo. Bỏ các nhãn viết hoa, chữ đơn cách, chuỗi nối dấu chấm giữa và mã A1/B1.
- 2026-11-24: người dùng muốn giao diện trắng, nên giấy đổi về trắng ở mọi giờ (ban đêm là trắng xám dưới ánh trăng, không còn nền tối). Tiêu đề đổi sang chữ giấy cắt: Paytone One tách từng chữ cái; trên bản đồ là chữ dán viền trắng, không còn khung nhãn. Đã bỏ Baloo 2.
- 2026-11-24: bỏ thanh công cụ, đường dẫn vị trí, la bàn, dòng hướng dẫn và mọi chữ phụ trong tấm thông tin. Thêm cách đi lại chỉ bằng chuột: bấm chỗ trống để lùi, cuộn ra xa để về toàn bản đồ, bấm "puc" để về góc nhìn ban đầu. Lỗi gặp phải: lúc mới tải, màn mở đầu cũng làm khoảng nhìn xa ra nên bị tính nhầm là người dùng cuộn ra; đã sửa bằng cách chỉ tính sau khi người dùng tự kéo hoặc cuộn.
- 2026-11-24: thêm chi tiết nhà cửa theo ảnh tham khảo của Figma AI, kèm 9 loại đồ trong sân; tăng số nhà quanh mỗi thị trấn (6–12). Thêm `bakeStatic()` gộp khối tĩnh theo chất liệu. Lỗi gặp phải: trùng tên hàm `ridge` làm trang trắng; hạt giống không phải số nguyên làm phép chia lấy dư trả về chỉ số lẻ, nên phải đổi sang dùng `hash`.
- 2026-11-24: người dùng thấy chữ "puc" và đồng hồ lệch so với khung. "puc" thấp khoảng 5 px vì phần trên dòng của Paytone One; đã căn theo phần mực. Khung giờ trước đây cách lề trái 70 px (chỗ của la bàn đã bỏ), giờ thẳng cột với "puc"; chấm mặt trời và chữ được căn giữa bằng flex, lề hai bên bằng nhau. Bỏ dòng "© 2026 Puc".
- 2026-11-24: làm bản thử đoạn mở đầu "portfolio" thành "puc" ở `design/logo-intro/demo/index.html`. Chữ lớn dùng đúng kiểu logo "puc": Paytone One cam cáo, bóng cứng `#9a4313` lệch .04em, dãy xoay và nhích chép từ `papercut-letters.js`, nên "p", "u", "c" ở cuối khớp tư thế logo bản đồ. Chữ u và c được cắt từ chữ o bằng `mask-image: conic-gradient(...)` đặt ở tâm phần mực của chữ o. Đầu cắt phẳng như kéo cắt bìa, hợp với Paytone One hơn đầu bo tròn. Phần tử mang mặt nạ phải có đệm (`padding: .2em 0; margin: -.2em 0`), nếu không mặt nạ cắt mất bóng chữ. Tai cáo nằm ở phần tử anh em, không đặt trong phần tử có mặt nạ. Mọi thứ là hàm của thời gian, nên `?t=1.8` dừng đúng một khung để chụp kiểm tra.
- 2026-11-24: người dùng thấy tai trên chữ u bị lệch. Nguyên nhân: cắt chữ o bằng hình nêm (`conic-gradient`) tới tận tâm, nên hai nhánh có đầu vát chéo và không có chỗ phẳng cho tai; tai đặt ở vai cong ngoài nên nghiêng và chìa ra. Đổi sang cắt **rãnh thẳng** bằng mặt nạ hai lớp (`linear-gradient` cả ô trừ một hình chữ nhật, `mask-composite: subtract`, Safari/WebKit dùng `-webkit-mask-composite: source-out`). Rãnh rộng đúng bằng lòng chữ o: dọc từ đỉnh xuống tâm cho u, ngang từ tâm sang phải cho c. Tai đặt trên đỉnh nhánh, mép trong thẳng hàng mép rãnh, nghiêng 10°. Soi bằng cách phóng `.word` lên 3 lần rồi chụp.
- 2026-11-24: sau khi cắt rãnh, chỗ rãnh trắng hơn nền vì mặt nạ khoét luôn bóng mờ (`text-shadow`) quanh chữ. Quy tắc: phần tử bị khoét bằng `mask` không được mang bóng; đặt bóng ở lớp bọc ngoài bằng `filter: drop-shadow(...)`, để bóng tính theo hình đã cắt.
- 2026-11-24: người dùng chê chữ u và c tự cắt từ chữ o (cả kiểu nêm lẫn kiểu rãnh) là xấu. Đổi sang: khi cáo phá chữ o thì đổi hẳn thành chữ u, c thật của Paytone One, kèm mảnh bìa văng và nhịp phồng rồi nảy về. Bài học: đừng tự chế chữ từ hình học khi font đã có chữ đẹp; hiệu ứng "biến đổi" có thể do chuyển động gánh. Khoá bề rộng từng ô chữ trước khi đổi chữ để các chữ sau không bị xô. Tai đặt theo đỉnh hai nhánh đo bằng canvas (quét một hàng ngay dưới đỉnh chữ u).
- 2026-11-24: gắn đoạn mở đầu vào bản đồ (`city/engine/logo-intro.js`, `logo-intro.css`, mọi lớp có tiền tố `li-`). Bài học khi ghép một lớp phủ lên bản đồ:
  - Quyết định có chạy hay không bằng đoạn mã trong `<head>`, để màn chờ của bản đồ không loé lên.
  - Giấu màn chờ của bản đồ khi lớp phủ đang chạy; trước khi giấu, nó hiện ra đúng lúc nền lớp phủ mờ đi.
  - Bản đồ chờ một promise (`window.__pucIntroGate`) rồi mới chạy màn mở đầu của nó, nên logo thu về góc đúng lúc bản đồ bung ra.
  - Đổi chỗ logo bằng hai lớp riêng: `li-on` (lớp phủ) và `li-brand-off` (giấu chữ "puc" của bản đồ), để hai logo mờ chéo nhau thay vì chớp.
  - Bản đồ đã dùng `?t=` cho giờ, nên tham số của đoạn mở đầu đổi thành `?it=`.

