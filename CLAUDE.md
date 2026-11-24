# Portfolio của Puc

## Trước khi làm giao diện hoặc thiết kế

- Mỗi lần làm, sửa hay chấm giao diện, gọi skill `frontend-design:frontend-design` và skill dự án `papercraft-ui` (`.claude/skills/papercraft-ui/SKILL.md`) trước khi viết mã. Không dựa vào trí nhớ của lần trước.
- Việc cần một kỹ năng mà chưa có skill: tìm nguồn trên mạng, rồi viết skill mới vào `.claude/skills/<tên>/SKILL.md` (ghi nguồn đã học) trước khi làm.
- Cuối mỗi lần làm, thêm điều mới học được vào mục Nhật ký của skill đó.
- Giao diện không được giống mặc định của AI. Danh sách cấm nằm trong `papercraft-ui`.
- Khi đặt hoặc sắp lại cây, nhà, đồ vật trên bản đồ, gọi thêm skill `natural-placement`.
- Khi tối ưu hoặc thêm thứ nặng vào bản đồ 3D, gọi `performance`, `core-web-vitals` và `web-3d-performance`; đo trước và sau trong cùng điều kiện.

## Quy trình

- Thiết kế đi theo skill `portfolio-pipeline`: người dùng chọn hướng, rồi duyệt bản Figma, rồi mới làm trang thật.
- Con cáo pixel dùng đúng các ảnh người dùng gửi, không tự chỉnh sửa (skill `pixel-character`).
- Máy không có Node. Dùng Python (`uv run --with ...`) và Blender chạy nền.
