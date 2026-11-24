# Kế hoạch làm con cáo mượt và chi tiết hơn

Bản hiện tại: 94 khung, 23 động tác, cắt từ ảnh 12 đến 16.webp. Các khung đó là ảnh phóng to, mỗi hàng vẽ một cỡ khác nhau. Kế hoạch này để bạn vẽ lại trên lưới pixel thật và thêm khung cho chuyển động mượt.

## 1. Quy tắc chung, áp dụng cho mọi khung

| Mục | Quy định | Vì sao |
|---|---|---|
| Cỡ khung | 64 × 64 ô cho mọi động tác | Đổi động tác không bị nhảy vị trí |
| Đường đất | Chân hoặc bụng chạm hàng thứ 56, tính từ trên xuống | Cáo không nhấp nhô khi đổi động tác |
| Vị trí mũi | Đứng yên thì mũi luôn ở cột 24 | Đầu không trượt qua lại giữa các khung |
| Cỡ cáo | Ngồi cao khoảng 26 ô, nằm dài khoảng 40 ô, giữ cố định | Hiện mỗi hàng một cỡ |
| Hướng | Nhìn sang trái | Web tự lật khi đi sang phải |
| Màu | Đen `#000000`, cam `#F38C1D`, xám `#544E52`, trắng `#FFFFFF`, thêm tối đa 2 màu phụ (cam tối để đổ bóng, hồng má) | Ít màu thì nét sạch |
| Một ô | Bằng 1 điểm ảnh, không phóng to, không làm mờ | Web tự phóng to cho nét |
| Khuôn mặt | Một mẫu mắt và mõm cố định, chép sang mọi khung có dáng đầu thẳng | Lỗi mắt lệch của bản trước |
| Hiệu ứng | Vạch rung, tim, Zzz để ở lớp riêng, không vẽ chung vào cáo | Web điều khiển riêng, cáo không bị dính vạch |

## 2. Nguyên tắc cho mượt

1. **Khung chính trước, khung chen sau.** Vẽ 2 đến 4 dáng chính của động tác, chạy thử, ưng rồi mới vẽ khung chen giữa.
2. **Lấy đà trước, dư âm sau.** Trước khi nhảy hay chạy thì hơi nén người lại. Sau khi dừng thì đuôi và tai còn lắc thêm 1 đến 2 khung.
3. **Đuôi và tai đi trễ.** Thân di chuyển trước, đuôi theo sau 1 đến 2 khung. Đây là chi tiết làm cáo trông mềm nhất.
4. **Mỗi khung có thời lượng riêng.** Đặt thời lượng trong Aseprite thay vì một tốc độ chung cho cả động tác. Ví dụ: dáng chính giữ 150 ms, khung chen 60 ms.
5. **Thở chỉ lệch 1 ô.** Bụng phồng 1 ô là đủ, lệch 2 ô trở lên sẽ trông như giật.
6. **Ngồi yên nên tách nhỏ.** Làm một vòng thở ngắn, kèm các đoạn ngắn chạy xen ngẫu nhiên: chớp mắt, giật tai, quẫy đuôi. Cách này sống động hơn một vòng dài mà tốn ít khung hơn.
7. **Có khung chuyển giữa các động tác.** Quay đầu, phanh, ngồi xuống, đứng dậy. Thiếu những khung này là nguyên nhân chính gây khựng.

## 3. Bảng động tác

Ưu tiên: **1** là cáo dùng liên tục trên trang, làm trước. **2** là tương tác chính. **3** là trang trí.

### 3a. Di chuyển và đứng yên

| Ưu tiên | Động tác | Hiện có | Mục tiêu | Dáng chính và chi tiết cần thêm | Thời lượng gợi ý |
|---|---|---|---|---|---|
| 1 | Ngồi thở | 4 | 6 | Hít vào, giữ, thở ra. Ngực phồng 1 ô, tai nhích theo | 150 ms mỗi khung, lặp |
| 1 | Chớp mắt (xen vào khi ngồi) | 0 | 3 | Mở, nhắm hờ, nhắm, rồi mở lại | 60 / 60 / 100 ms |
| 1 | Giật tai (xen vào khi ngồi) | 0 | 3 | Một tai gập rồi bật lại | 80 ms |
| 1 | Quẫy đuôi (xen vào khi ngồi) | 4 | 6 | Đuôi cong sang, đầu đuôi trễ 1 khung | 90 ms |
| 1 | **Đi bộ** (mới) | 0 | 8 | Chạm đất, hạ thấp, bước qua, nhấc lên, lặp cho chân kia. Thân nhấp nhô 1 ô | 100 ms, lặp |
| 1 | Chạy | 6 | 8 | Duỗi người, chụm chân, bay người. Đuôi kéo phía sau, tai cụp | 70 ms, lặp |
| 1 | **Bắt đầu chạy** (mới) | 0 | 2 | Nén người rồi bật đi | 60 ms |
| 1 | **Phanh** (mới) | 0 | 3 | Chân trước chống, mông trượt, đuôi vung lên trước | 70 / 70 / 120 ms |
| 1 | **Quay đầu** (mới) | 0 | 4 | Nhìn nghiêng, gần chính diện, nghiêng phía kia. Đuôi quét theo | 60 ms |
| 2 | Ngồi xuống từ dáng đi | 0 | 3 | Mông hạ, chân trước duỗi, đuôi cuộn vào | 80 ms |
| 2 | Đứng dậy từ dáng ngồi | 0 | 3 | Làm ngược động tác ngồi xuống | 80 ms |

### 3b. Bấm vào cáo: nhảy

| Ưu tiên | Động tác | Hiện có | Mục tiêu | Dáng chính và chi tiết | Thời lượng |
|---|---|---|---|---|---|
| 1 | Giật mình "> <" | 3 | 4 | Co rúm, lông dựng, nảy nhẹ 1 ô | 50 / 50 / 80 / 120 ms |
| 1 | Lấy đà | 2 | 3 | Hạ thấp người, mông nhún, đuôi vểnh | 70 ms, khung cuối giữ 140 ms |
| 1 | Bật lên | 1 | 2 | Duỗi thẳng, chân sau đạp | 50 ms |
| 1 | Bay lên | 1 | 2 | Người dài ra, tai bay ngược ra sau | 70 ms |
| 1 | Đỉnh | 1 | 2 | Người tròn lại, đuôi phấp phới | 100 ms |
| 1 | Rơi | 1 | 2 | Chân trước duỗi chờ đáp, tai dựng | 70 ms |
| 1 | Đáp đất | 1 | 3 | Bẹp người 1 khung, nảy lại, về dáng ngồi | 50 / 80 / 120 ms |

Trang web tự di chuyển cáo theo đường cong lúc nhảy. Vì vậy các khung nhảy vẽ cáo **tại chỗ**, không tự nâng cáo lên trong khung, và bỏ bóng dưới đất (web vẽ bóng riêng).

### 3c. Nghỉ và ngủ

| Ưu tiên | Động tác | Hiện có | Mục tiêu | Dáng chính và chi tiết | Thời lượng |
|---|---|---|---|---|---|
| 2 | Nằm xuống | 3 | 6 | Ngồi, chân trước trượt ra, ngực hạ, mông hạ, đầu gối lên chân | 100 ms |
| 2 | Nằm thở, mắt nhắm | 4 | 6 | Lưng phồng 1 ô | 200 ms, lặp |
| 2 | Ngủ | 6 | 8 | Thở chậm, tai giật 1 lần mỗi vòng, đuôi quét nhẹ | 250 ms, lặp |
| 3 | Trở mình khi ngủ (mới) | 0 | 6 | Lật nửa người rồi nằm lại | 120 ms |
| 2 | Thức dậy và vươn vai | 6 | 10 | Mở mắt, ngẩng đầu, chổng mông vươn chân trước, ngáp, lắc người, ngồi | 100 ms, khung ngáp giữ 300 ms |
| 3 | Nằm vẫy đuôi | 4 | 6 | Chỉ đuôi chuyển động, thân đứng yên | 100 ms |

### 3d. Tương tác với chuột và trang

| Ưu tiên | Động tác | Hiện có | Mục tiêu | Dáng chính và chi tiết | Thời lượng |
|---|---|---|---|---|---|
| 2 | Vui khi được xoa | 4 | 8 | Nhắm tít mắt, dụi đầu sang trái rồi phải, đuôi quẫy nhanh | 90 ms, lặp |
| 2 | Nhún mông chuẩn bị vồ | 6 | 8 | Mông lắc trái phải, đuôi lắc ngược chiều | 70 ms, lặp |
| 2 | **Vồ** (mới) | 0 | 6 | Bật ra, bay thấp, hai chân trước chụp xuống, đáp | 60 ms |
| 2 | Bị nhấc | 5 | 6 | Đung đưa, chân lơ lửng trễ nhịp so với thân | 110 ms, lặp |
| 2 | **Giãy khi bị nhấc** (mới) | 0 | 4 | Chân đạp loạn, mặt "> <" | 70 ms |
| 2 | Choáng "x x" | 4 | 6 | Đầu lắc lư thành vòng tròn, sao quay (lớp riêng) | 120 ms, lặp |
| 2 | Ló ra mép | 4 | 6 | Tai lên, mắt lên, nửa mặt, chân bám mép | 90 ms |
| 2 | **Thụt vào** (mới) | 0 | 3 | Làm ngược động tác ló ra, nhanh hơn | 60 ms |
| 2 | Nhìn lên | 4 | 5 | Ngẩng dần, khung cuối giữ | 90 ms, khung cuối 400 ms |
| 3 | Nghiêng đầu | 4 | 5 | Nghiêng, giữ, về thẳng. Tai nghiêng trễ 1 khung | 100 ms, giữ 400 ms |

### 3e. Trò vặt khi rảnh

| Ưu tiên | Động tác | Hiện có | Mục tiêu | Chi tiết | Thời lượng |
|---|---|---|---|---|---|
| 3 | Đào đất | 5 | 8 | Hai chân trước luân phiên, đất bắn ra sau (lớp riêng) | 70 ms, lặp |
| 3 | Ăn | 4 | 8 | Cúi, nhai 2 lần, nuốt, liếm mép | 110 ms |
| 3 | Ngửi | 4 | 6 | Mũi nhích từng ô, đầu dò sang trái và phải | 100 ms |
| 3 | Dỗi | 3 | 6 | Quay mặt đi, má phồng, liếc lại | 150 ms |
| 3 | Gãi tai (mới) | 0 | 6 | Chân sau gãi nhanh, mắt nhắm | 60 ms, lặp |

### 3f. Hiệu ứng rời (khung 16 × 16 ô)

| Hiệu ứng | Hiện có | Mục tiêu | Ghi chú |
|---|---|---|---|
| Zzz | 4 | 6 | Chữ z nhỏ bay lên rồi mờ dần |
| Tim | 4 | 5 | Bật ra, nảy, nhỏ dần |
| Dấu "!" | 3 | 3 | Như hiện tại |
| Bụi | 5 | 6 | Một bộ khi chạy, một bộ to hơn khi đáp đất |
| Vạch rung | 3 | 3 | Như hiện tại |
| Sao choáng | 4 | 8 | Một vòng quay đủ |
| Bóng dưới đất | 3 cỡ | 3 cỡ | Web tự co giãn bóng theo độ cao khi nhảy |
| Đất bắn (mới) | 0 | 4 | Dùng cho đào đất |

## 4. Tổng khối lượng

| Nhóm | Hiện có | Mục tiêu |
|---|---|---|
| Ưu tiên 1 | 24 khung | 61 khung |
| Ưu tiên 2 | 46 khung | 88 khung |
| Ưu tiên 3 | 28 khung | 51 khung |
| Hiệu ứng | 26 khung | 38 khung |

Cộng lại khoảng 240 khung, gấp đôi rưỡi hiện tại. Ưu tiên 1 là phần cần nhất, làm xong riêng nó cũng đã đổi hẳn cảm giác trên trang.

## 5. Thứ tự làm và việc của từng bên

| Giai đoạn | Bạn làm | Tôi làm | Xong khi |
|---|---|---|---|
| 0. Dựng nền | Vẽ lại dáng ngồi và dáng nằm trên khung 64 × 64. Chốt cỡ cáo và khuôn mặt mẫu | Đặt khung, đường đất, cột mũi vào file mẫu; kiểm tra cỡ | Hai dáng gốc được duyệt |
| 1. Đi lại | Ngồi thở, chớp mắt, giật tai, đi bộ, chạy, bắt đầu chạy, phanh, quay đầu | Gắn vào web, nối các động tác, quay video để bạn xem | Cáo đi, chạy, dừng, quay đầu không bị giật |
| 2. Nhảy | Bộ nhảy 7 phần ở mục 3b | Thêm đường bay và bóng | Bấm vào cáo nhảy mượt |
| 3. Ngủ | Nằm xuống, nằm thở, ngủ, thức dậy | Nối chuỗi tự đi ngủ | Để yên 12 giây cáo ngủ tự nhiên |
| 4. Tương tác | Vui, nhún mông, vồ, bị nhấc, giãy, choáng, ló ra, thụt vào, nhìn lên | Gắn với chuột và mép trang | Mọi tương tác chạy đúng |
| 5. Trang trí | Ưu tiên 3 và hiệu ứng | Thêm vào lượt trò vặt ngẫu nhiên | Xong toàn bộ |

Mỗi giai đoạn: bạn gửi file, tôi gắn lên trang thử trong ngày, bạn xem rồi sửa, sau đó mới sang giai đoạn kế.

## 6. Cách gửi file

- Một file Aseprite `cao.aseprite` cho toàn bộ, mỗi động tác là một **tag** đặt tên theo cột "Động tác", không dấu, ví dụ `ngoi-tho`, `di-bo`, `chay`, `quay-dau`.
- Thời lượng từng khung đặt ngay trong Aseprite. Web sẽ đọc đúng con số đó.
- Lớp `cao` cho thân cáo, lớp `fx` cho hiệu ứng. Lớp nào tên bắt đầu bằng `_` (như `_nhap`, `_luoi`) sẽ không được xuất.
- Nếu chưa có Aseprite: xuất PNG mỗi động tác một hàng, khung 64 × 64 ở đúng cỡ 1 ô bằng 1 điểm ảnh, kèm bảng ghi thời lượng.

Lệnh tôi dùng để xuất, bạn không cần chạy:

```bash
aseprite -b cao.aseprite --ignore-layer fx --split-tags --sheet sprites/cao.png --data sprites/cao.json --format json-array --list-tags
```

## 7. Tự kiểm trước khi gửi

- [ ] Bật onion skin (xem mờ khung trước và sau): đầu không trượt khi không cần trượt.
- [ ] Chạy lặp 10 lần liền: không thấy cú giật ở chỗ nối khung cuối về khung đầu.
- [ ] Đặt hai động tác nối nhau cạnh nhau, ví dụ ngồi rồi đi: khung cuối của động tác này gần với khung đầu của động tác kia.
- [ ] Mặt giống mẫu, trừ khung có biểu cảm riêng.
- [ ] Không có điểm ảnh lẻ ngoài viền, không có màu ngoài bảng màu.
