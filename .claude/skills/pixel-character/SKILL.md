---
name: pixel-character
description: Design and draft pixel-art character poses that stay on model with a reference sprite, then animate only after approval. Use for the portfolio fox or any small pixel character.
---
# Pixel character

## Order of work (do not skip)
1. Trace the reference on its true grid. Lock it; never edit it.
2. Write down its rules: palette, outline, proportions, head/body ratio, line breaks, how much detail per area.
3. Draft **static key poses** by hand, row by row. No motion yet.
4. Check each at 1x, at 8x, and as a solid black silhouette. Redraw weak ones.
5. Show the sheet. **Gate: the user approves poses.**
6. Animate approved poses only.

## Drawing
- Silhouette first: the pose must read when filled black.
- Curves step monotonically (1,1,2,3), never 1,3,1. No doubled corners.
- One pixel density. Never shear, scale, or freely rotate pixels; redraw the part.
- Clusters, not stray pixels. A single pixel must mean something (an eye glint).
- Keep the reference's colour count and flatness. No shading the reference does not have.
- Parts have volume: legs taper out of the body mass, tail has a base, belly and tip. No sticks or tubes.
- Keep the locked face exactly, in every pose. Never round or reshape it; the user rejected that.
- Mochi rule (from the user's references in pet/drafts/mau): the head hides most of the body; paws are small grey nubs peeking out under the chin; no leg columns. Legs show only when sitting, leaping or stretching. Eyes stay as flat dashes unless the emotion needs otherwise.
- The torso carries the action (arch, coil, diagonal), because the face is fixed. Redraw the tail for each action.
- Head more than half the height; visible body and tail shorter than the head.
- Every pose needs a line of action: arched for gather, long for extend, diagonal for rise and fall.
- Keep volume constant: a longer body is thinner, a shorter one is taller.

## Motion notes for after approval
- Walk: two contact and two passing poses, symmetric. Contact lowest, passing highest. Hind leg follows the opposite fore leg. Equal stride front and back.
- Hips, chest and head are three bouncing balls, each a little later than the last. Tail last.
- Run: bunch tight, then extend long. The tighter the squash, the longer the stretch.
- Jump: anticipation, launch, rise, held apex, fall, landing squash. Uneven timing gives character.
- Integer movement only. Feet must not skate: stride per cycle equals distance travelled.

## Smoothness and frame counts (learned 2026-11-23)
- Smooth comes from strong keys plus timing, not from frame count alone. Lock 2 to 4 key poses, play them, then add in-betweens. Too many even in-betweens make motion floaty and sluggish (SLYNYRD 8).
- Mix ones and twos: anticipation and settle on twos (about 80 ms a frame), the fast part on ones (about 40 ms). Give each frame its own duration; one longer hold can fix a whole move.
- Cycle budget: 8-frame run = contact, recoil, pass, high point for each side, 80 ms each. Removing frames means slowing the rest so energy stays (6 frames 107 ms, 4 frames 160 ms). Never drop contact or pass.
- Quadruped: animate legs, then body, then head, then tail and ears last, each a frame or two late. Gallop footfall: left rear, right rear, right fore, left fore. Bunch then stretch; a tighter bunch gives a longer stretch. Cycles must be symmetric or they hitch.
- Jump: squash frame, leave the ground on the next frame, stretch while rising, round and slow at the apex (hold 2 to 3 frames), stretch on the fall, squash on landing for 1 to 2 frames, then settle with a small overshoot. Keep volume: squash wider, stretch thinner.
- Smears: one frame that blends positions, only for the fastest moments (launch, burst). Use instead of extra frames, not with them.
- Sub-pixel motion: move a detail by fading pixels in and out across in-betweens (colour by colour) rather than jumping a whole pixel. Works for ears, cheeks, tail tip, breathing.
- Anchor: one pivot point for every frame (nose column while still, ground row always). Most jitter is inconsistent anchoring or drawing at fractional screen positions.
- Arcs: head, tail tip and body follow arcs between keys, never straight lines.
- Check: loop 10 times, silhouette in black, onion skin; a single stray pixel in a loop is obvious.

## Sources read
Gamezxz/pixel-art-studio f8c2466 (MIT), SLYNYRD Pixelblog 25, Cathy Feraday Miller "Animating Four-Legged Beasts", SLYNYRD Pixelblog 8, Tiny Warrior Games "Pixel Art Sub-Pixel Animation", Game Developer "12 principles for game animation" (Pedro Medeiros jump squash). Pose-specific pixel guidance for small foxes was not found; those choices come from studying the reference.

## Nhật ký
- 2026-11-24: nhận bộ 3 (16 bảng, ảnh 35–50) và cắt bằng `design/logo-intro/tools/cut_bo3.py`. Bài học:
  - Mỗi bảng ảnh AI phóng to vẽ một cỡ khác nhau. Đo độ dày nét viền đen (mode các đoạn đen theo hàng) để biết cỡ một ô pixel, rồi co khi hiển thị; không resample file.
  - Đo nét viền sai khi bảng chỉ có tai, hoặc có vẽ kèm vật khác (chữ C), nên phải so bằng mắt bề ngang đầu cáo với một bảng chuẩn (ngồi thở).
  - Đường kẻ ô có thể nằm giữa ảnh: xoá hàng hoặc cột tối dài hơn 85% ô. Ngưỡng 55% xoá nhầm nét viền dọc của cáo.
  - Ảnh RGBA có nền trong suốt mang màu (0,0,0) bên dưới; chỉ xét điểm có alpha khi tìm nét tối.
  - Bỏ nền bằng loang từ mép ô qua các điểm sáng không màu; nền xám loang (bảng 50) cần ngưỡng sáng thấp hơn.

