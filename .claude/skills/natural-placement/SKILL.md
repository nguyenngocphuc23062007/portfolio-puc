---
name: natural-placement
description: Rules for laying out trees, houses and props on a generated map so it looks natural rather than random or gridded - blue-noise spacing with variable radius, density fields with soft edges, species patches by elevation and water, houses strung along roads facing the street, hamlets, hedgerows and lone trees. Use when placing or re-placing scenery in city/engine/map-engine.js or any procedural scene in this portfolio.
---

# Bố trí cảnh vật tự nhiên

Áp dụng cho bản đồ 3D ở `city/` và mọi cảnh dựng bằng mã trong portfolio. Đọc kèm skill `papercraft-ui`, vì nhà cửa dùng bộ chi tiết `KG`/`kp` và `bakeStatic()` của skill đó.

## Vì sao cảnh trông giả

- **Lưới có rung (jittered grid):** cây xếp thành hàng chéo, nhìn từ trên thấy rõ ô vuông.
- **Ngưỡng cứng:** rừng có mép dao cắt (ví dụ `dens > .56` thì rất dày, dưới đó gần như không có cây).
- **Trộn loài kiểu muối tiêu:** mỗi cây chọn loài ngẫu nhiên, nên không có mảng thông hay mảng cây lá vàng.
- **Nhà rắc vòng quanh thị trấn, quay hướng ngẫu nhiên:** không bám đường, cửa không nhìn ra đường.
- **Cùng một cỡ ở mọi nơi:** rừng thật có cây lớn ở giữa, cây non ở mép.

## Quy tắc

1. **Khoảng cách kiểu "blue noise", bán kính thay đổi.**
   - Dùng lấy mẫu đĩa Poisson: thử điểm theo một thứ tự cố định (theo `hash`), chỉ nhận điểm khi không có cây nào đã nhận trong bán kính `R(x, z)`. Có thể làm nhanh bằng lưới băm không gian.
   - `R` nhỏ ở nơi rừng dày (khoảng 0.45) và lớn ở đồng trống (1.5–2.5). Đây là cách Red Blob Games gợi ý: đổi `R` theo vùng sinh thái để đổi mật độ.
   - Không dùng lưới đều có rung.
2. **Trường mật độ mềm.**
   - Xác suất có cây là `smoothstep(a, b, density)`, không phải ngưỡng cứng. Như vậy mép rừng thưa dần.
   - Cộng thêm một lớp nhiễu tần số thấp để đục **khoảng trống** (trảng cỏ) giữa rừng.
   - Lấy ý từ Horizon Zero Dawn: mỗi lớp cảnh có bản đồ mật độ riêng, tính từ độ cao, độ dốc, khoảng cách tới đường và nước, và các lớp khác. Lớp đặt trước chiếm chỗ (footprint), lớp sau tránh ra.
3. **Thứ tự đặt (lớp trước chiếm chỗ):** đường và sông, rồi thị trấn và ruộng, rồi nhà ven đường và trang trại, rồi cây ven sông và hàng rào cây, rồi rừng, cuối cùng là cây lẻ trên đồng.
4. **Loài theo mảng, không theo từng cây.**
   - Chọn loài bằng nhiễu tần số thấp (mảng rộng 6–10 đơn vị), cộng thêm độ cao: cao thì thông và tuyết tùng, thấp và gần nước thì bạch dương và cây lá rộng.
   - Cho tối đa khoảng 15% cây lạc loài để mảng không quá đều.
5. **Cỡ cây theo vị trí:** cây ở giữa rừng to hơn (×1.1–1.4), cây ở mép và cây lẻ nhỏ hơn (×0.7–0.9). Thêm ±15% ngẫu nhiên, và xoay ngẫu nhiên quanh trục đứng.
6. **Cây đi theo đường nét của cảnh.**
   - **Ven sông:** một dải cây thưa cách mép nước 0.6–1.4, chủ yếu bạch dương và cây lá rộng.
   - **Hàng rào cây:** cây cách nhau 0.9–1.3 dọc mép ruộng và một số đoạn đường ngoài thị trấn, có chỗ đứt quãng.
   - **Cây lẻ:** rải rất thưa trên đồng (bán kính 2–3), hay đứng gần nhà hoặc góc ruộng.
7. **Nhà bám đường (làng dọc đường).**
   - Từ mép mỗi thị trấn, đi dọc các con đường ra ngoài. Cứ 1.3–2.2 đơn vị (ngẫu nhiên) thì đặt một nhà, xen kẽ hai bên đường.
   - Nhà lùi vào 0.75–1.0 so với tim đường, **cửa quay ra đường**, lệch thêm tối đa ±10°.
   - Càng xa thị trấn càng thưa (xác suất giảm dần), sau 6–9 đơn vị thì thôi.
   - Thêm 1–2 **xóm nhỏ** (2–4 nhà quây quần, hướng nhà gần giống nhau) ở chỗ đất bằng gần ruộng.
   - Các bài báo về sinh làng (Galin và cộng sự 2012) cũng làm theo thứ tự: đường trước, rồi chia lô thẳng hàng với đường, rồi mới đặt nhà.
8. **Cây chỉ mọc trên đất cỏ** (hàm `rocky()` và `blocked()` trong `map-engine.js`):
   - Không mọc trên đá: mặt đất tô màu đá khi cao hơn 2.6 hoặc dốc (xem `tClass`), nên giới hạn cây ở độ cao 2.3, và đo dốc ở 8 hướng trên hai vòng .55 và 1.1 quanh chân cây. Đo một điểm thì cây sát mép vách hoặc trên bậc phẳng nhỏ giữa vách vẫn lọt.
   - Không mọc dưới chân nón núi: núi là hình nón riêng, không nằm trong hàm độ cao `H`, nên phải so độ cao mặt nón tại chỗ đó với mặt đất.
   - Giữ cả **tán** ra khỏi đường, không chỉ thân: tâm cây cách tim đường liên trấn ít nhất .95 (đường rộng .84, tán rộng tới .45), cách phố trong trấn .72.
   - Rừng không vào trong ranh giới thị trấn (`blobSd < .3`).
   - Mọi lớp cây (kể cả vòng rừng xa) đều phải qua cùng các phép kiểm tra này.
   - Xếp phép kiểm tra từ rẻ đến đắt: mật độ, khoảng cách Poisson, `blocked`, cuối cùng mới đo dốc.
9. **Không chồng lấn:** mỗi vật ghi bán kính chiếm chỗ vào `occupied`, và lớp sau phải kiểm tra. Nhà ngoại ô chiếm khoảng 1.0 vì có sân.
10. **Luôn cố định:** mọi lựa chọn dùng `hash`/`fbm` theo toạ độ, không dùng `Math.random()`. Như vậy lần nào tải cũng ra cùng một cảnh, và ảnh chụp kiểm tra (`?still`) lặp lại được.
11. **Kiểm tra bằng mắt:**
    - Nhìn từ trên (`?t=10&still=4`) để xem có còn hàng lối hay mép cứng không.
    - Nhìn gần một thị trấn để xem nhà có quay ra đường không.
    - Đo hiệu năng bằng `?debug`: rừng là InstancedMesh nên thêm cây gần như không tốn lệnh vẽ, nhưng tốn tam giác.

## Nguồn đã học

- [Red Blob Games: Making maps with noise](https://www.redblobgames.com/maps/terrain-from-noise/) (phần đặt cây): mỗi điểm chỉ đặt cây khi giá trị nhiễu của nó lớn nhất trong bán kính R, R đổi theo vùng; tác giả khuyên dùng đĩa Poisson hoặc lưới có rung vì đều hơn nhiễu tần số cao.
- [Guerrilla Games: GPU-based procedural placement in Horizon Zero Dawn (GDC 2017)](https://www.guerrilla-games.com/read/gpu-based-procedural-placement-in-horizon-zero-dawn): bản đồ mật độ theo từng lớp, vùng sinh thái (ecotope) quyết định loài, lớp này chiếm chỗ lớp kia, mọi thứ cố định và ổn định cục bộ.
- [Galin và cộng sự: Procedural generation of villages on arbitrary terrains (2012)](https://perso.liris.cnrs.fr/egalin/Articles/2012-villages.pdf): đường và hạt giống làng mọc cùng nhau, chia lô theo hướng đường và địa hình rồi mới đặt nhà.
- Tổng quan về phân bố thực vật ([ar5iv 2208.01471](https://ar5iv.labs.arxiv.org/html/2208.01471)): cách đơn giản nhất là lấy mẫu ngẫu nhiên hoặc đĩa Poisson; các cách sau thêm cỡ cây khác nhau và luật hệ sinh thái.

## Nhật ký

- 2026-11-24: viết skill. Áp dụng lần đầu cho `city/engine/map-engine.js`: rừng đổi sang đĩa Poisson bán kính thay đổi, có mép mềm, trảng cỏ, mảng loài, dải cây ven sông, hàng rào cây và cây lẻ; nhà ngoại ô đổi sang bám đường và quay ra đường, thêm xóm nhỏ.
- 2026-11-24: kết quả đo bằng `?debug`: khoảng 2.500 cây (InstancedMesh), khoảng 2.000 lệnh vẽ ở góc nhìn toàn bản đồ, ngang với trước khi đổi. Nhìn gần Bến Phim thấy nhà xếp hai bên đường, song song với đường; rừng thành mảng theo loài (bạch dương vàng, cây tròn, thông); có cây lẻ trên đồng và dải cây ven sông. Chưa làm: hàng rào cây dọc đường ngoài thị trấn (mới có dọc mép ruộng) và dải cây ở rừng xa (vòng rừng ngoài vẫn dùng lưới thưa của bản gốc).
- 2026-11-24: người dùng thấy cây mọc trên núi và trên đường. Nguyên nhân:
  - (1) chỉ loại cây trong hộp bao của nón núi khi mặt đất thấp hơn 1, còn vòng rừng xa không kiểm tra gì;
  - (2) cho cây mọc tới độ cao 3–3.4, trong khi đất từ 2.6 đã là đá;
  - (3) khoảng cách tới đường tính theo thân cây, nên tán cây vẫn chùm ra đường;
  - (4) rừng tràn vào trong hàng rào thị trấn Xưởng Dữ Liệu.

  Đã sửa bằng `rocky()` và mở rộng `blocked()`. Kiểm tra bằng cách chiếu vị trí từng cây ra màn hình rồi bắn tia xuống mặt đất để xem pháp tuyến: cây trên vách hoá ra đứng trên một bậc phẳng nhỏ giữa vách, nên mới thêm vòng đo 1.1. Lần đầu đặt phép đo dốc lên đầu vòng lặp làm bước trồng rừng chậm từ 200 lên 740 ms; đưa xuống cuối thì về lại khoảng 220 ms.
