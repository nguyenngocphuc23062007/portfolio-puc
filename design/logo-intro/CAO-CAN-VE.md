# Các động tác cáo cần vẽ mới cho đoạn mở đầu

Mọi động tác ở đây đều **vẽ mới**, không dùng lại khung cũ. Có 19 động tác cáo, tổng **127 khung**, và 7 bộ hiệu ứng, tổng **41 khung**. Mỗi động tác có bảng mô tả từng khung kèm thời lượng.

Xem cùng [PROMPT.md](PROMPT.md) (kịch bản 8 cảnh) và [pet/KE-HOACH-CAO.md](../../pet/KE-HOACH-CAO.md) (quy tắc vẽ cáo chung).

---

## 0. Đối chiếu với bản thử (2026-11-24)

Bản thử [demo/index.html](demo/index.html) đang dùng bộ khung cũ trong `pet/sprites/`. Bảng dưới ghi từng chỗ cáo bị khựng, khung đang dùng tạm, và động tác cần vẽ (số thứ tự theo mục 3).

### Đã nhận bộ 3 (ảnh 35–50, ngày 2026-11-24) và gắn vào bản thử

- Cắt bằng `tools/cut_bo3.py` vào `cao/5-bo-3/`: chỉ cắt và bỏ nền, không đổi cỡ, không vẽ lại. Mỗi bảng vẽ một cỡ (một ô pixel từ 8 đến 19 điểm ảnh), nên `fox.json` ghi `px` để trang tự co về cùng cỡ cáo. Một số bảng chỉnh `px` bằng mắt, so với cáo ngồi thở.
- Đã có: Chạy (6 khung; người dùng chốt là đủ, không cần 8), Lấy đà, Bật nhảy, Bay (ảnh 52, đủ 12 khung; bảng 3 khung cũ giữ ở `bay-3.png`), Lao xuống hang, Trồi đầu, Nhìn quanh, Thụt xuống, Tai lướt, Bung ra, Đáp đất, Quay đầu, Ngồi xuống, Vẫy đuôi, Ngồi thở, Nháy mắt.
- **Bung ra:** đã nhận ảnh 51 (khung 1–5 vẽ lại, không có chữ C), cắt vào `bung-ra-moi.png`. Bản thử chạy 5 khung này rồi nối khung 6–8 của ảnh 45.
- **Lao xuống hang:** theo yêu cầu, đã xoá cái hố trong khung (công cụ cắt bỏ mảng nâu đậm rộng sát mặt đất, giữ chân và hạt đất). Mặt đất của khung đặt lùi sau nét trên chữ o, nên cáo như chui vào trong chữ.
- **Đứng dậy:** chưa có, đang chạy ngược động tác Ngồi xuống.
- **Giũ đất** (ảnh 55) chạy ngay sau Đáp đất. **Hiệu ứng** (ảnh 56: bụi chạy, bụi đáp, bụi bung, đất văng, đất rơi, vạch rung, bóng 6 cỡ) cắt bằng `tools/cut_fx.py` và đã thay hết hiệu ứng của bộ cũ. Bóng nhỏ dần theo độ cao của cáo.
- **Còn thiếu:** Tai giật (không bắt buộc). Ảnh 54 trùng ảnh 52.
- Đoạn mở đầu giờ dài 6,1 giây; bấm hoặc nhấn phím để bỏ qua.
- Bóng, vạch tốc độ và đất vẽ sẵn trong khung thì được giữ nguyên.

### Lỗi chung của bộ khung cũ (phải sửa ở mọi động tác)

- **Mỗi động tác một cỡ:** khung rộng từ 155 đến 255 điểm ảnh, đường đất ở 106 đến 188. Vì vậy cáo to nhỏ khác nhau khi đổi động tác; rõ nhất là lúc chuyển từ đáp đất sang ngồi. Bộ mới phải cùng lưới 64 × 64, đường đất hàng 56.
- **Bóng và vạch tốc độ vẽ dính trong khung** (`dash` khung 4, cả 3 khung `leap`). Khi cáo bay cao, bóng bay theo cáo, và bóng chớp tắt khi chạy. Bộ mới không vẽ bóng; web tự vẽ bóng theo độ cao.

### Bắt buộc phải có (11 động tác, 73 khung)

| Chỗ trong bản thử | Đang dùng tạm | Vì sao khựng | Cần vẽ |
|---|---|---|---|
| Chạy vào | `dash`, 6 khung | Bóng chớp tắt; thiếu khung bước qua nên vòng chạy giật | 1 Chạy (8) |
| Dừng trước chữ p | nhảy thẳng từ `dash` sang `crouch` | Không có phanh, cáo đang chạy đứng khựng lại | 2 Lấy đà (6) |
| Bật lên | `crouch` khung 1 sang `leap` khung 0 | Không có khung nén và khung nhòe, cáo như bị dịch chuyển | 3 Bật nhảy (3) |
| Bay qua chữ p | `leap`, 3 khung cho 0.18 giây | Quá ít khung cho một đường bay dài; không có dáng đỉnh và dáng chúi đầu | 4 Bay (12) |
| Chui vào chữ o | `dig` khung 1 (dáng nằm ngang) tụt thẳng xuống | **Chỗ khựng nhất:** cáo không cắm đầu mà rơi thẳng như bị kéo xuống; đuôi không quẫy | 5 Lao xuống hang (10) |
| Thụt khỏi chữ u | `peek` chạy ngược | Chạy ngược nhìn máy móc, thiếu nén người và vệt tai | 8 Thụt xuống (4) |
| Phá chữ c | `leap` từ trong chữ c | Không có dáng cuộn trong chữ và bung ra, mảnh vỡ bay mà cáo chưa nén | 10 Bung ra (8) |
| Đáp đất | `land`, 1 khung giữ 0.09 giây | Một khung thì không có nén và nảy, cáo dừng cứng | 11 Đáp đất (6) |
| Quay về phía chữ | lật ảnh ngay lập tức | Cáo đang hướng phải bỗng quay trái trong một khung | 12 Quay đầu (6) |
| Ngồi xuống | `land` sang `idle` | Đứng sang ngồi không có khung chuyển, lại đổi cỡ | 13 Ngồi xuống (5) |
| Chạy đi lúc thu logo | `idle` sang `dash` | Ngồi rồi chạy ngay, không đứng dậy | 17 Đứng dậy (5) |

Thêm hiệu ứng **Bóng** (6 cỡ), vì bộ mới bỏ bóng trong khung.

### Nên có (8 động tác, 54 khung)

| Động tác | Thay cho | Thêm được gì |
|---|---|---|
| 6 Trồi đầu (6) | `peek` 4 khung (dùng tạm được) | Tai ló trước, đầu lố lên rồi hạ về |
| 7 Nhìn quanh (9) | đang giữ yên một khung | Cáo ngó hai bên trước khi thụt xuống, có tính cách |
| 9 Tai lướt (6) | ụ đất giấy kraft | Thấy rõ cáo đang đào ngầm sang chữ kia |
| 14 Vẫy đuôi (10) | `wag` 4 khung | Đuôi quét mềm, chóp đuôi trễ |
| 15 Ngồi thở (8) | `idle` 4 khung | Lúc giữ logo cuối, cáo không đứng im như ảnh |
| 16 Nháy mắt (6) | chưa có | Khoảnh khắc chào người xem |
| 18 Giũ đất (6), 19 Tai giật (3) | chưa có | Trang trí |

Hiệu ứng bụi và đất (mục 4) cũng thuộc nhóm nên có. Bụi `fx-dust` cũ dùng tạm được.

### Thứ tự vẽ đề xuất cho bản thử

1. **Lao xuống hang** và **Đáp đất + Quay đầu + Ngồi xuống**: hai chỗ khựng thấy rõ nhất.
2. **Chạy, Lấy đà, Bật nhảy, Bay**: phần mở đầu.
3. **Bung ra, Thụt xuống, Đứng dậy**.
4. Nhóm nên có.

Vẽ xong đợt nào thì gửi mình; bản thử chỉ cần đổi tên tệp và thời lượng trong bảng `A` ở đầu đoạn mã để gắn vào.

---

## 1. Học được gì từ các trang hướng dẫn

| Nguyên tắc | Áp dụng cho con cáo |
|---|---|
| Mượt là nhờ **dáng chính rõ** và **nhịp đúng**, không phải cứ nhiều khung là mượt. Chen quá nhiều khung đều nhau sẽ làm chuyển động lề mề (SLYNYRD, bài 8). | Vẽ dáng chính trước, chạy thử, rồi mới chen khung giữa. Các khung chen ở dưới đều có thời lượng ngắn. |
| **Trộn hai nhịp**: lấy đà và kết thúc thì mỗi hình giữ khoảng 80 ms; đoạn nhanh nhất thì mỗi hình chỉ 30–40 ms. | Mỗi khung có thời lượng riêng, ghi trong cột "ms". |
| Vòng chạy 8 khung gồm chạm đất, nảy, bước qua, điểm cao, lặp cho mỗi bên. Bớt khung thì phải kéo dài thời lượng các khung còn lại. Không bao giờ bỏ khung chạm đất và khung bước qua. | Vòng chạy 8 khung, mỗi khung 50 ms. |
| Thú 4 chân: vẽ chân trước, rồi tới thân, rồi đầu, cuối cùng là đuôi và tai, mỗi phần trễ hơn phần trước 1–2 khung. Khi phi nước đại, cáo chụm người lại rồi duỗi ra; chụm càng chặt thì duỗi càng xa. Vòng lặp phải cân đối hai bên, nếu không sẽ bị khựng. | Tai và đuôi luôn trễ 1–2 khung so với thân. |
| Nhảy: khung đầu nén người, khung kế tiếp đã rời đất. Lúc bay lên thì người dài ra, tới đỉnh thì tròn lại và giữ lâu hơn, lúc rơi lại dài ra, chạm đất nén 1–2 khung rồi nảy nhẹ về (theo Pedro Medeiros). Nén thì bè ra, duỗi thì thon lại, để thể tích không đổi. | Áp dụng cho các động tác số 3, 4, 11. |
| **Khung nhòe** (smear: một khung kéo vệt nối hai vị trí) chỉ dùng cho khoảnh khắc nhanh nhất, và dùng thay cho khung chen chứ không dùng thêm vào. | Một khung nhòe lúc bật nhảy, một khung lúc phá khỏi chữ c. |
| **Chuyển động nhỏ hơn 1 ô**: muốn một chi tiết nhích chưa tới 1 ô thì làm mờ dần các ô ở chỗ cũ và hiện dần ở chỗ mới qua vài khung chen, thay vì nhảy nguyên 1 ô. | Dùng cho thở, tai nhích, má phồng. |
| Mọi khung có chung một điểm neo (cột mũi khi đứng yên, hàng đất ở mọi khung). Phần lớn hiện tượng rung giật là do điểm neo lệch, hoặc do vẽ ở toạ độ lẻ trên màn hình. | Đường đất hàng 56; cột mũi 24 khi đứng yên. |
| Đầu, chóp đuôi và thân đi theo **đường cong**, không đi thẳng. | Kiểm tra bằng onion skin (bật hiện mờ khung trước và sau). |

Nguồn:
- [SLYNYRD Pixelblog 8: Intro to Animation](https://slynyrd.com/blog/2018/8/19/pixelblog-8-intro-to-animation)
- [SLYNYRD Pixelblog 25: Motion Cycles](https://slynyrd.com/blog/2020/1/23/pixelblog-25-motion-cycles)
- [Animating Four-Legged Beasts (Game Developer)](https://www.gamedeveloper.com/art/animating-four-legged-beasts)
- [Pixel Art Sub-Pixel Animation (Tiny Warrior Games)](https://tinywarriorgames.com/2019/01/04/game-development-pixel-art-sub-pixel-animation/)
- [12 principles for game animation (Game Developer)](https://www.gamedeveloper.com/game-platforms/12-principles-for-game-animation)
- [Animating on ones, twos and threes (iD Tech)](https://www.idtech.com/blog/what-does-animating-on-ones-twos-and-threes-mean)

---

## 2. Quy cách chung

| Mục | Quy định |
|---|---|
| Khung | 64 × 64 ô, một ô bằng một điểm ảnh. Riêng động tác số 4 (bay) và số 10 (bung ra) dùng khung 96 × 64. |
| Hướng | Cáo nhìn sang **trái**, web tự lật khi cáo đi sang phải. Riêng động tác số 12 (quay đầu) có ghi hướng riêng. |
| Đường đất | Hàng 56. Khi cáo bay, vẽ cáo **tại chỗ** trong khung; độ cao do web điều khiển. **Không vẽ bóng** trong khung. |
| Cột mũi | Cột 24 với mọi động tác đứng yên. |
| Mặt | Đúng khuôn mặt mẫu: mắt gạch ngang, mõm trắng. Khung nào có biểu cảm riêng thì có ghi trong bảng. |
| Màu | Đen, cam, xám, trắng của cáo. Thêm tối đa 1 màu cam tối để làm khung nhòe. |
| Phần bị che | Khi cáo chui vào hoặc ra khỏi chữ, vẫn **vẽ đủ thân**. Web tự che phần nằm trong chữ. |
| Tên tag Aseprite | Ghi trong ngoặc ở tiêu đề mỗi động tác. |

---

## 3. Động tác cáo

### 1. Chạy (`chay`): 8 khung, lặp. Dùng ở cảnh 2.

Phi nước đại. Thứ tự chân chạm đất: sau trái, sau phải, trước phải, trước trái. Thân nhấp nhô ±2 ô; đầu nhấp nhô ngược nhịp hông, trễ 1 khung. Tai cụp ra sau. Đuôi uốn sóng, trễ 2 khung.

| Khung | Dáng | Thân (ô so với dáng chuẩn) | ms |
|---|---|---|---|
| 1 | Vươn: chân trước duỗi tới, chân sau duỗi ra sau, người dài nhất | −1 | 50 |
| 2 | Chân trước chạm đất, thân bắt đầu thu lại | −2 | 50 |
| 3 | Thu người: 4 chân chụm dưới bụng, lưng cong nhẹ | −1 | 50 |
| 4 | Chân sau chạm đất, lưng cong nhất, người ngắn nhất | −2 | 50 |
| 5 | Đạp: chân sau đẩy, thân bắt đầu duỗi, đầu hơi chúi | 0 | 50 |
| 6 | Bay: 4 chân rời đất, người duỗi | +2 | 50 |
| 7 | Bay xuống, chân trước đưa ra trước | +1 | 50 |
| 8 | Chen giữa khung 7 và khung 1 | 0 | 50 |

Một vòng 8 khung, cáo đi được 24 ô. Web cho cáo chạy đúng tốc độ đó để chân không bị trượt.

### 2. Lấy đà (`lay-da`): 6 khung. Dùng ở cảnh 3.

| Khung | Dáng | ms |
|---|---|---|
| 1 | Phanh: chân trước chống thẳng, mông còn trôi tới, đuôi vung lên trước | 30 |
| 2 | Mông hạ xuống, đuôi bắt đầu về | 30 |
| 3 | Người hạ thấp, ngực sát đất, tai dựng | 40 |
| 4 | Nhún mông sang trái 1 ô, đuôi lắc sang phải | 40 |
| 5 | Nhún mông sang phải 1 ô, đuôi lắc sang trái | 40 |
| 6 | Nén sâu nhất: người bè ra, giữ lâu | 80 |

### 3. Bật nhảy (`bat`): 3 khung. Dùng ở cảnh 3.

| Khung | Dáng | ms |
|---|---|---|
| 1 | Nén sâu hơn khung 6 động tác số 2 một chút, chân sau gồng | 30 |
| 2 | **Khung nhòe**: thân kéo dài thành vệt cam từ chỗ cũ tới chỗ mới, tai và đuôi thành vệt mảnh | 30 |
| 3 | Đã rời đất: người duỗi dài nhất và thon nhất, chân sau còn duỗi về phía sau | 40 |

### 4. Bay qua chữ p (`bay`): 12 khung, khung 96 × 64. Dùng ở cảnh 3.

| Khung | Pha | Dáng | ms |
|---|---|---|---|
| 1–4 | Lên | Người dài, thon dần lại theo từng khung. Tai bay ngược ra sau. Đuôi duỗi thẳng rồi bắt đầu cong. | 30 mỗi khung |
| 5–8 | Đỉnh | Người cuộn tròn, 4 chân co, đuôi xoè thành hình chữ S. Khung 6 và 7 gần giống nhau, chỉ đuôi và tai nhích nhẹ (chưa tới 1 ô). | 40 / 50 / 50 / 40 |
| 9–12 | Rơi | Chúi đầu dần xuống. Chân trước duỗi ra chờ chạm. Tai dựng ngược lên trên. Người dài ra lại. | 30 mỗi khung |

### 5. Lao xuống hang (`lao-xuong`): 10 khung. Dùng ở cảnh 4.

| Khung | Dáng | ms |
|---|---|---|
| 1 | Thân chúi 45°, chân trước khép sát như lặn | 30 |
| 2 | Thân chúi 70° | 30 |
| 3 | Thân dựng đứng, đầu cắm xuống, người dài nhất | 30 |
| 4 | Như khung 3 nhưng tụt xuống 4 ô | 30 |
| 5 | Mông chạm đáy, người nén lại, bụng bè ra | 30 |
| 6 | Chân sau đạp, thân tụt thêm 6 ô | 30 |
| 7 | Chỉ còn mông và đuôi trên miệng hang | 30 |
| 8 | Chỉ còn đuôi, dựng thẳng | 30 |
| 9 | Đuôi quẫy cong sang trái | 70 |
| 10 | Đuôi quẫy sang phải rồi tụt xuống | 70 |

### 6. Trồi đầu (`troi-dau`): 6 khung. Dùng ở cảnh 6.

| Khung | Phần nhô lên khỏi miệng chữ u | ms |
|---|---|---|
| 1 | Chóp hai tai | 40 |
| 2 | Cả hai tai | 40 |
| 3 | Tai và trán | 40 |
| 4 | Tới mắt | 40 |
| 5 | Cả đầu và một chút cổ, lố lên cao hơn khung 6 một ô | 40 |
| 6 | Hạ về đúng chỗ, tai rung nhẹ | 70 |

### 7. Nhìn quanh (`nhin-quanh`): 9 khung. Dùng ở cảnh 6.

Tai đi trễ đầu 1 khung.

| Khung | Dáng | ms |
|---|---|---|
| 1 | Nhìn thẳng | 60 |
| 2 | Đầu xoay ¼ sang trái | 35 |
| 3 | Đầu xoay hẳn sang trái, tai còn thẳng | 35 |
| 4 | Giữ, tai nghiêng theo | 70 |
| 5 | Quay về giữa | 35 |
| 6 | Xoay ¼ sang phải | 35 |
| 7 | Xoay hẳn sang phải | 35 |
| 8 | Giữ, tai nghiêng theo | 70 |
| 9 | Về giữa | 35 |

### 8. Thụt xuống (`thut`): 4 khung. Dùng ở cảnh 6.

| Khung | Dáng | ms |
|---|---|---|
| 1 | Đầu nén xuống 2 ô, tai dựng | 35 |
| 2 | Chỉ còn tai và trán | 35 |
| 3 | Chỉ còn chóp tai | 35 |
| 4 | Còn một vệt tai mảnh (khung nhòe), rồi mất | 35 |

### 9. Tai lướt dưới đất (`tai-luot`): 6 khung, lặp. Dùng ở cảnh 7.

Chỉ có chóp hai tai nhô lên khỏi mặt đất, lướt từ chữ u sang chữ o như vây cá.

| Khung | Dáng | ms |
|---|---|---|
| 1–3 | Hai tai nghiêng dần về phía sau, lắc lệch nhau 1 khung | 40 mỗi khung |
| 4–6 | Hai tai thẳng dần lại | 40 mỗi khung |

### 10. Bung ra khỏi chữ c (`bung-ra`): 8 khung, khung 96 × 64. Dùng ở cảnh 7.

| Khung | Dáng | ms |
|---|---|---|
| 1 | Người cuộn tròn bên trong chữ (web che gần hết), mặt "> <" | 35 |
| 2 | Nén chặt hơn nữa | 35 |
| 3 | **Khung nhòe**: vệt cam bắn ngang sang phải | 30 |
| 4 | Duỗi dài nằm ngang, chân trước vươn tới, tai bay ra sau, mặt "> <" | 35 |
| 5 | Như khung 4, mặt trở lại bình thường | 35 |
| 6 | Người bắt đầu cong xuống | 40 |
| 7 | Chân trước duỗi chờ chạm đất | 40 |
| 8 | Chân sắp chạm, đuôi vểnh lên | 50 |

### 11. Đáp đất (`dap-dat`): 6 khung. Dùng ở cảnh 8.

| Khung | Dáng | ms |
|---|---|---|
| 1 | Chân trước chạm đất | 35 |
| 2 | Nén sâu: người bè ra 2 ô, thấp xuống 3 ô | 45 |
| 3 | Chân sau chạm đất | 45 |
| 4 | Nảy: cao hơn dáng đứng 1 ô | 55 |
| 5 | Về dáng đứng, đuôi còn đung đưa | 70 |
| 6 | Đứng yên, đuôi dừng | 90 |

### 12. Quay đầu (`quay-dau`): 6 khung. Dùng ở cảnh 8.

Khung 1 nhìn sang **phải**, khung 6 nhìn sang **trái**. Web **không lật** động tác này.

| Khung | Dáng | ms |
|---|---|---|
| 1 | Nhìn phải | 40 |
| 2 | ¾ nhìn phải | 40 |
| 3 | Nhìn thẳng ra màn hình | 40 |
| 4 | ¾ nhìn trái | 40 |
| 5 | Nhìn trái, đuôi còn quét theo phía sau | 40 |
| 6 | Đuôi về chỗ | 70 |

### 13. Ngồi xuống (`ngoi-xuong`): 5 khung. Dùng ở cảnh 8.

| Khung | Dáng | ms |
|---|---|---|
| 1 | Mông hạ 2 ô | 50 |
| 2 | Mông hạ 4 ô, chân trước thẳng | 50 |
| 3 | Chạm đất, đuôi bắt đầu cuộn | 50 |
| 4 | Đuôi cuộn ra trước chân, người nảy lên 1 ô | 50 |
| 5 | Dáng ngồi chuẩn | 50 |

### 14. Vẫy đuôi khi ngồi (`vay-duoi`): 10 khung, lặp. Dùng ở cảnh 8.

| Khung | Dáng | ms |
|---|---|---|
| 1–4 | Đuôi quét sang phải, chóp đuôi trễ 1 khung | 50 mỗi khung |
| 5 | Giữ, ngực phồng 1 ô (theo cách nhích dưới 1 ô) | 50 |
| 6–9 | Đuôi quét sang trái | 50 mỗi khung |
| 10 | Giữ | 50 |

### 15. Ngồi thở (`ngoi-tho`): 8 khung, lặp. Dùng khi giữ logo cuối.

| Khung | Dáng | ms |
|---|---|---|
| 1–3 | Hít vào: ngực nhích dần lên 1 ô | 120 mỗi khung |
| 4 | Giữ | 160 |
| 5–7 | Thở ra | 120 mỗi khung |
| 8 | Giữ | 160 |

### 16. Nháy mắt với người xem (`nhay-mat`): 6 khung. Dùng khi giữ logo cuối.

| Khung | Dáng | ms |
|---|---|---|
| 1 | Đầu xoay ¾ ra màn hình | 60 |
| 2 | Nhìn thẳng ra màn hình | 60 |
| 3 | Một mắt thành hình "^", má phồng | 120 |
| 4 | Giữ | 120 |
| 5 | Mắt về như cũ | 60 |
| 6 | Đầu quay về dáng ngồi | 60 |

### 17. Đứng dậy rồi chạy đi (`dung-day`): 5 khung. Dùng sau cảnh 8.

| Khung | Dáng | ms |
|---|---|---|
| 1 | Nhổm mông | 50 |
| 2 | Đứng thẳng 4 chân | 50 |
| 3 | Chồm người tới trước | 40 |
| 4 | Bước đầu tiên | 40 |
| 5 | Nối vào khung 1 của động tác Chạy | 40 |

### 18. Giũ đất (`giu-dat`): 6 khung. Không bắt buộc, chèn sau động tác Đáp đất.

Lắc người từ đầu tới đuôi, mỗi phần trễ 1 khung. Mặt "> <". Đất rơi từ người xuống. Mỗi khung 45 ms.

### 19. Tai giật (`tai-giat`): 3 khung. Không bắt buộc, chạy xen khi cáo ngồi.

Một tai gập xuống, bật lên, rung nhẹ. Thời lượng 40 / 40 / 80 ms.

---

## 4. Hiệu ứng pixel (khung 24 × 24, trừ bóng)

| Hiệu ứng | Khung | Mô tả | ms |
|---|---|---|---|
| Bụi chạy (`bui-chay`) | 5 | Cụm nhỏ bung ra, bay nhẹ về sau, tan | 40 |
| Bụi đáp (`bui-dap`) | 7 | Hai cụm bắn sang hai bên, rồi tan | 40 |
| Bụi bung (`bui-bung`) | 8 | Cụm to khi cáo phá khỏi chữ c | 35 |
| Đất văng (`dat-vang`) | 6 | 3–4 hạt đất bắn theo đường cong, dùng khi tai lướt và khi giũ đất | 40 |
| Đất rơi (`dat-roi`) | 5 | Hạt đất rơi khỏi đầu cáo khi trồi lên | 50 |
| Vạch rung (`vach-rung`) | 4 | Vạch hai bên chữ o khi chữ rung | 40 |
| Bóng (`bong`) | 6 cỡ | Từ rộng 20 ô xuống 8 ô, web chọn cỡ theo độ cao của cáo; khung 32 × 8 | |

---

## 5. Thời gian mới của đoạn mở đầu

Nhiều khung hơn thì các nhịp kéo dài thêm. Cả đoạn dài khoảng **4,5 giây** thay vì 2,8 giây.

| Từ | Đến | Diễn biến | Động tác |
|---|---|---|---|
| 0,00 | 0,45 | Chữ "portfolio" hiện lên | |
| 0,45 | 0,85 | Chạy vào | 1 |
| 0,85 | 1,11 | Phanh, lấy đà | 2 |
| 1,11 | 1,21 | Bật nhảy | 3 |
| 1,21 | 1,63 | Bay qua chữ p | 4 |
| 1,63 | 2,01 | Lao xuống hang | 5 |
| 1,87 | 2,25 | Chữ thừa chìm, chữ o lăn về (bắt đầu từ lúc chỉ còn đuôi) | |
| 2,25 | 2,52 | Phá đỉnh chữ o, trồi đầu | 6 |
| 2,52 | 2,93 | Nhìn quanh | 7 |
| 2,93 | 3,07 | Thụt xuống | 8 |
| 3,07 | 3,31 | Tai lướt dưới đất sang chữ o thứ hai | 9 |
| 3,31 | 3,61 | Phá hông chữ o, bung ra | 10 |
| 3,61 | 3,95 | Đáp đất | 11 |
| 3,95 | 4,22 | Quay đầu về phía chữ; tai mọc trên chữ u | 12 |
| 4,22 | 4,47 | Ngồi xuống | 13 |
| 4,47 | 5,00 | Vẫy đuôi, giữ logo | 14, 15 |
| 5,00 | 5,45 | Thu logo lên đầu trang; cáo đứng dậy và chạy đi | 17, 1 |

**Nếu thấy dài**, có thể bỏ bớt và vẫn giữ đủ khung cho các phần còn lại:
- Bỏ Nhìn quanh: bớt 0,41 giây.
- Bỏ Tai lướt, để chữ o thứ hai tự rung: bớt 0,24 giây.
- Cho cáo ngồi quay mặt sang phải, bỏ Quay đầu: bớt 0,27 giây.

Bỏ cả ba thì còn khoảng 3,6 giây. Người xem luôn bấm hoặc cuộn được để bỏ qua.

---

## 6. Thứ tự vẽ

| Đợt | Động tác | Số khung | Vì sao làm trước |
|---|---|---|---|
| 1 | 1 Chạy, 2 Lấy đà, 3 Bật nhảy, 4 Bay, 11 Đáp đất | 35 | Khung xương của cả đoạn, và dùng lại được cho con cáo trên trang |
| 2 | 5 Lao xuống, 6 Trồi đầu, 8 Thụt xuống, 10 Bung ra | 28 | Bốn khoảnh khắc biến chữ, quan trọng nhất của ý tưởng |
| 3 | 12 Quay đầu, 13 Ngồi xuống, 14 Vẫy đuôi, 15 Ngồi thở | 29 | Kết thúc và logo cuối |
| 4 | 7 Nhìn quanh, 9 Tai lướt, 16 Nháy mắt, 17 Đứng dậy | 26 | Làm cho sống động |
| 5 | 18 Giũ đất, 19 Tai giật, hiệu ứng | 9 + 41 | Trang trí |

Mỗi đợt: vẽ **dáng chính** trước (các khung có thời lượng dài nhất trong bảng), gửi tôi gắn lên trang thử để xem nhịp, rồi mới vẽ khung chen.

---

## 7. Kiểm tra trước khi gửi

- [ ] Bật onion skin: đầu, chóp đuôi và thân đi theo đường cong, không giật cục.
- [ ] Tai và đuôi trễ hơn thân 1–2 khung.
- [ ] Vòng lặp chạy 10 lần liền không thấy chỗ nối.
- [ ] Tô đen cả con cáo, dáng vẫn đọc được.
- [ ] Nén thì bè ra, duỗi thì thon lại, thể tích không đổi.
- [ ] Không có ô lẻ ngoài viền, không có bóng vẽ trong khung.
- [ ] Đường đất ở hàng 56, cột mũi ở cột 24 với các động tác đứng yên.
