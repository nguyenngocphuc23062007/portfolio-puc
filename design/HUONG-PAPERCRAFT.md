# Hướng giao diện: diorama giấy ban đêm

Bạn chọn ngày 24/11/2026, dựa trên ảnh mẫu `design/mau/papercraft-dem.webp`. Hướng này thay cho 5 phương án A đến E trước đây. Bản brief cũ (vở ô ly) chỉ còn là nháp.

## Những gì có trong ảnh mẫu

- **Cách dựng:** cảnh nhìn chéo từ trên xuống như một mô hình đặt trên bàn. Mọi vật là **bìa giấy cắt phẳng dựng đứng**: cây tròn, cây thông, bụi hoa, nhà mái ngói, cầu vồng gỗ, cột biển chỉ đường, ghế, hòn đá. Mỗi tấm có viền giấy sáng và đổ bóng ngắn xuống đất.
- **Ánh sáng:** đêm xanh thẫm, đèn vàng ấm hắt ra từ cửa sổ nhà và từ một chiếc đèn lồng. Đom đóm là các chấm vàng lơ lửng. Trời phía xa tối và mờ dần.
- **Màu:** cam đất, đỏ gạch, vàng nghệ, xanh rêu, xanh lam đậm cho dòng suối, kem cho lối đi. Màu sẫm và ấm, không có màu chói.
- **Bố cục:** ngôi nhà có đèn ở bên trái làm điểm nhấn. Lối đi sáng uốn giữa cảnh, con suối chảy ngang phía sau, cây viền quanh mép như khung tranh.
- **Chất liệu:** giấy có vân, mép cắt hơi răng cưa, các lớp xếp chồng tạo chiều sâu.

Ảnh mẫu là tác phẩm của người khác (có dòng chữ facebook.com/bacthaychip trên ảnh), nên chỉ dùng để lấy cảm hứng. Cảnh của trang sẽ vẽ mới.

## Gợi ý gắn với nội dung portfolio

- Mỗi vật trong cảnh là một mục của trang: ngôi nhà là "Giới thiệu", cột biển chỉ đường là menu, các bụi hoa là dự án, cây cầu dẫn sang "Liên hệ".
- Con cáo pixel sống trong cảnh, ngủ trước cửa nhà, chạy theo lối đi. Đây là chỗ ghép hai thế giới: cáo pixel đứng trong diorama giấy.
- Logo mở đầu "portfolio" thành "puc" diễn ra trên chính lối đi của cảnh.
- Rê chuột làm camera nghiêng nhẹ, các lớp giấy lệch nhau tạo chiều sâu. Đom đóm bay quanh con trỏ.

## Kỹ thuật dự kiến

- **Three.js:** cảnh dựng từ các tấm phẳng có độ dày, mỗi tấm vẽ riêng (SVG hoặc PNG), cộng texture giấy làm bằng mã theo skill `3d-paper-material`. Chỉ một nguồn sáng ấm cho mỗi cửa sổ, sương mù màu đêm, hơi nhoè ở cảnh xa.
- **Dự phòng:** máy yếu hoặc tắt WebGL thì hiện ảnh tĩnh của cảnh. Bật chế độ giảm chuyển động thì cảnh đứng yên.
- **Tham khảo mã:** `references/papercraft/` (xem README trong đó).

## Bản phác màn đầu trong Figma (24/11/2026)

- Trang Figma "Màn đầu: diorama giấy đêm": https://www.figma.com/design/3eNkhJOdHCqVH09pcM2JQt?node-id=14-233
- Các mẫu giấy dùng lại nằm ở khung "Thành phần giấy (dùng lại)" ngay bên dưới.
- Trạng thái: **chờ bạn duyệt**.

## Bước tiếp theo theo đúng quy trình

1. Vẽ bản phác màn đầu theo hướng này trong Figma, gồm bố cục cảnh, các vật và chỗ đặt chữ.
2. Bạn duyệt bản Figma.
3. Rồi mới dựng mã.
