// Đoạn mở đầu "portfolio" thành "puc" cùng con cáo pixel (portfolio Puc).
// Kịch bản: design/logo-intro/PROMPT.md. Danh sách động tác: design/logo-intro/CAO-CAN-VE.md. Bản thử gốc: design/logo-intro/demo/.
// Ảnh cáo: nguyên các khung người dùng gửi (ảnh 35-56), cắt bằng design/logo-intro/tools/cut_bo3.py và cut_fx.py, build.py chép vào out/intro/.
//
// Nối với bản đồ:
// - Chỉ chạy khi <html> có lớp li-on (đoạn mã trong <head> đặt: lần đầu trong phiên, không bật giảm chuyển động, không có ?nointro).
// - window.__pucIntroGate: bản đồ dựng ngầm bên dưới rồi chờ promise này (lúc logo bắt đầu thu về góc) mới chạy màn mở đầu của nó.
// - Logo thu về đúng chỗ chữ "puc" của bản đồ; khi bản đồ hiện chữ "puc" thật (lớp intro của #map bị gỡ) thì đổi chỗ và gỡ lớp phủ.
// Tham số: ?intro chạy lại dù đã xem trong phiên; ?nointro bỏ qua; ?it=1.8 dừng ở giây 1.8 để chụp kiểm tra; ?ispeed=.25 chạy chậm.
// Bấm, chạm, cuộn hoặc nhấn phím giữa chừng thì nhảy tới logo cuối.

const ON = document.documentElement.classList.contains('li-on');
let openGate = () => {};
window.__pucIntroGate = ON ? new Promise(r => { openGate = r; }) : null;

const SRC = 'intro/';
// w, h: cỡ một khung; ground: hàng chân chạm đất; px: số điểm ảnh của một ô pixel trong bảng đó (mỗi bảng vẽ một cỡ)
const A = {
  chay: { n: 6, w: 303, h: 244, ground: 234, px: 10.5 }, 'lay-da': { n: 6, w: 305, h: 264, ground: 257, px: 10.5 },
  bat: { n: 3, w: 559, h: 484, ground: 472, px: 19 }, bay: { n: 12, w: 354, h: 255, ground: 231, px: 11 },
  'ngoi-tho': { n: 8, w: 214, h: 255, ground: 254, px: 10 }, 'vay-duoi': { n: 10, w: 172, h: 188, ground: 187, px: 8 },
  'ngoi-xuong': { n: 5, w: 372, h: 385, ground: 375, px: 15 }, 'quay-dau': { n: 6, w: 298, h: 300, ground: 297, px: 12.5 },
  'dap-dat': { n: 6, w: 305, h: 310, ground: 308, px: 12.5 }, 'bung-ra': { n: 8, w: 469, h: 297, ground: 291, px: 10 },
  'tai-luot': { n: 6, w: 281, h: 143, ground: 140, px: 11.5 }, thut: { n: 4, w: 438, h: 345, ground: 335, px: 15.5 },
  'nhin-quanh': { n: 9, w: 380, h: 192, ground: 190, px: 10 }, 'troi-dau': { n: 6, w: 279, h: 208, ground: 202, px: 11.3 },
  'lao-xuong': { n: 10, w: 294, h: 296, ground: 286, px: 10.5 }, 'bung-ra-moi': { n: 5, w: 372, h: 278, ground: 273, px: 11 },
  'giu-dat': { n: 6, w: 446, h: 266, ground: 265, px: 10 },
  'bui-chay': { n: 5, w: 106, h: 53, ground: 53, px: 9 }, 'bui-dap': { n: 7, w: 148, h: 81, ground: 81, px: 7 },
  'bui-bung': { n: 8, w: 126, h: 103, ground: 103, px: 6.5 }, 'dat-vang': { n: 6, w: 130, h: 81, ground: 81, px: 8 },
  'dat-roi': { n: 5, w: 70, h: 79, ground: 79, px: 7 }, 'vach-rung': { n: 4, w: 148, h: 52, ground: 52, px: 5 },
  bong: { n: 6, w: 178, h: 29, ground: 20, px: 7.5 },
};
export const INTRO_SPRITES = Object.keys(A);
// lịch (giây). Thời lượng từng khung theo CAO-CAN-VE.md
const T = { run: .45, brake: .85, jump: 1.11, fly: 1.21, dive: 1.63, sink: 1.87, popU: 2.25, look: 2.52, duck: 2.93, tunnel: 3.07,
  popC: 3.31, land: 3.61, shake: 3.95, sit: 4.22, wag: 4.47, turn: 4.97, dock: 5.42 };
const END = 6.12;
function play(t, t0, durs, frames) { let e = (t - t0) * 1000, i = 0; while (i < durs.length - 1 && e >= durs[i]) { e -= durs[i]; i++; } return frames ? frames[i] : i; }
// dãy xoay và nhích của chữ giấy cắt, chép từ papercut-letters.js để "p", "u", "c" khớp logo bản đồ
const ROT = [-3, 2, -1.5, 3, -2.5, 1, -0.5, 2.5, -1], DY = [0, -1, 1, -0.5, 0.5, -1.5, 1, 0, -1, 0.5];
const dyOf = k => DY[(k * 3) % DY.length] / 21;
const C_ROT = -1.5, C_DY = DY[(2 * 3) % 10] / 21;
const WORD = 'portfolio', SINK = [2, 3, 4, 6, 7, 8], I_U = 1, I_C = 5;

function bez(x1, y1, x2, y2) {
  const f = (t, a, b) => 3 * a * t * (1 - t) ** 2 + 3 * b * t * t * (1 - t) + t ** 3;
  return x => { if (x <= 0) return 0; if (x >= 1) return 1; let lo = 0, hi = 1, t = x;
    for (let i = 0; i < 24; i++) { t = (lo + hi) / 2; if (f(t, x1, x2) < x) lo = t; else hi = t; } return f(t, y1, y2); };
}
const OUT = bez(.2, .8, .2, 1), IN = bez(.55, 0, 1, .45), BOUNCE = bez(.34, 1.56, .64, 1), INOUT = bez(.65, 0, .35, 1);
const clamp01 = v => Math.max(0, Math.min(1, v)), seg = (t, a, b) => clamp01((t - a) / (b - a)), lerp = (a, b, k) => a + (b - a) * k;

if (ON) start();

async function start() {
  try { sessionStorage.setItem('puc-intro', '1'); } catch {}
  const stage = document.getElementById('li-stage');
  stage.setAttribute('aria-hidden', 'true');
  const mk = (cls, parent = stage, tag = 'div') => { const e = document.createElement(tag); e.className = cls; parent.append(e); return e; };
  const bg = mk('li-bg'), brandEl = mk('li-brand'), foxwrap = mk('li-foxwrap');
  const shEl = mk('li-spr', foxwrap), foxEl = mk('li-spr', foxwrap), wordEl = mk('li-word'), fxEl = mk('li-fx');
  const letters = [...WORD].map((ch, k) => {
    const L = mk('li-L', wordEl, 'span'), gw = mk('li-gw', L, 'span'), g = mk('li-g', gw, 'span'); g.textContent = ch;
    return { L, g, k };
  });
  // hai tai cáo vector trên chữ u (màu tai thật của cáo: xám, lòng trắng, viền đen)
  const ears = [-1, 1].map(side => {
    const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); s.setAttribute('class', 'li-ear'); s.setAttribute('viewBox', '-50 -90 100 92');
    s.innerHTML = `<path d="M-46 0 Q-14 -86 0 -86 Q14 -86 46 0 Z" fill="#544E52" stroke="#000" stroke-width="5" stroke-linejoin="round"/>
      <path d="M-20 0 Q-6 -40 0 -40 Q6 -40 20 0 Z" fill="#fff"/>`;
    letters[I_U].L.append(s); return { s, side };
  });
  const pool = [...Array(14)].map(() => mk('li-spr', fxEl));
  const chips = [...Array(7)].map(() => mk('li-chip', fxEl));
  // tải trước mọi tấm ảnh để khung đầu của mỗi động tác không bị trống
  INTRO_SPRITES.forEach(n => { const im = new Image(); im.src = `${SRC}${n}.png`; });

  let G;
  function measure() {
    const vw = innerWidth, vh = innerHeight;
    wordEl.style.transform = 'none'; wordEl.style.fontSize = '100px';
    letters.forEach(l => { l.L.style.transform = 'none'; l.L.style.clipPath = 'none'; l.L.style.width = ''; l.g.textContent = WORD[l.k]; });
    const wEm = wordEl.getBoundingClientRect().width / 100;
    const F = Math.round(Math.min(140, (vw - 40) * .8 / wEm, vh * .22));   // chừa chỗ hai bên cho cáo chạy vào và ngồi
    wordEl.style.fontSize = F + 'px';
    const ww = wordEl.getBoundingClientRect().width;
    // phần mực của chữ o (canvas measureText) và độ dày nét (quét một hàng điểm ảnh qua tâm)
    const cv = document.createElement('canvas'), cx = cv.getContext('2d'); cv.width = F * 2; cv.height = F * 2;
    cx.font = `400 ${F}px "Paytone One"`; const m = cx.measureText('o');
    const asc = m.actualBoundingBoxAscent, desc = m.actualBoundingBoxDescent, inkL = -m.actualBoundingBoxLeft, inkR = m.actualBoundingBoxRight;
    cx.textBaseline = 'alphabetic'; cx.fillText('o', 10, F * 1.5);
    const row = Math.round(F * 1.5 - (asc - desc) / 2), px = cx.getImageData(0, row, F * 2, 1).data;
    let a = -1, b = -1; for (let i = 0; i < F * 2; i++) { const on = px[i * 4 + 3] > 128; if (on && a < 0) a = i; if (a >= 0 && !on) { b = i; break; } }
    const D = inkR - inkL, sw = b - a;
    const baseLocal = (() => {   // vị trí đường chân chữ trong hộp chữ, đo bằng một phần tử mốc
      const probe = document.createElement('span'); probe.style.cssText = 'display:inline-block;width:1px;height:0;vertical-align:baseline';
      letters[0].L.append(probe); const r = probe.getBoundingClientRect().top - letters[0].L.getBoundingClientRect().top; probe.remove(); return r; })();
    const B = Math.round(vh * .55), left = Math.round((vw - ww) / 2 + .14 * F), top = B - baseLocal;
    wordEl.style.left = left + 'px'; wordEl.style.top = top + 'px';
    const box = letters.map(l => { const r = l.L.getBoundingClientRect(); return { x: r.left, w: r.width }; });
    letters.forEach((l, i) => { l.L.style.width = box[i].w + 'px'; });   // khoá bề rộng: đổi o thành u/c không xô các chữ khác
    const oc = { x: (inkL + inkR) / 2, y: baseLocal - (asc - desc) / 2 };
    const S = .8 * D / 9.5;   // điểm ảnh màn hình cho một ô pixel: đầu cáo khoảng 0.8 D
    const G0 = { vw, vh, F, D, sw, asc, desc, B, left, top, baseLocal, box, oc, S };
    // u và c là chữ thật của Paytone One; chữ o giữa từ lăn về đúng chỗ chữ c trong "puc"
    const mu = cx.measureText('u'), mc = cx.measureText('c');
    G0.cX = box[I_U].x + mu.width + .01 * F; G0.dxC = G0.cX - box[I_C].x;
    G0.uC = { x: box[I_U].x + oc.x, y: B - (asc - desc) / 2 };
    G0.cC = { x: G0.cX + (mc.actualBoundingBoxRight - mc.actualBoundingBoxLeft) / 2, y: G0.uC.y };
    G0.cRight = G0.cX + mc.actualBoundingBoxRight;
    G0.shiftC = vw / 2 - (box[0].x + G0.cRight) / 2;   // khi chữ thừa chìm, cả cụm dịch để "puc" nằm giữa màn hình
    G0.oTop = B - asc;
    letters.forEach(l => { l.L.style.transformOrigin = `${oc.x}px ${baseLocal}px`; });
    // tai: quét một hàng ngay dưới đỉnh chữ u để tìm hai nhánh; mỗi tai rộng bằng nhánh, dựng thẳng, cách đầu nhánh một khe nhỏ
    cx.clearRect(0, 0, cv.width, cv.height); cx.fillText('u', 10, F * 1.5);
    const ascU = mu.actualBoundingBoxAscent, scanY = Math.round(F * 1.5 - ascU + Math.max(2, .05 * F));
    const pu = cx.getImageData(0, scanY, F * 2, 1).data, runs = [];
    for (let i = 0, st = -1; i <= F * 2; i++) { const on = i < F * 2 && pu[i * 4 + 3] > 128;
      if (on && st < 0) st = i; if (!on && st >= 0) { runs.push([st - 10, i - 10]); st = -1; } }
    const earH = .30 * D, armTop = baseLocal - ascU;
    ears.forEach(({ s: el, side }) => {
      const [r0, r1] = runs[side < 0 ? 0 : runs.length - 1] || [0, sw], earW = (r1 - r0) * 1.02, ex = (r0 + r1) / 2;
      el.setAttribute('width', earW); el.setAttribute('height', earH * 92 / 90);
      el.style.left = (ex - earW / 2) + 'px'; el.style.top = (armTop - earH - .06 * D) + 'px';
      el.style.transformOrigin = '50% 100%';
    });
    G = G0;
  }

  function sprite(el, name, frame, x, yGround, flip, op = 1) {
    const a = A[name], scale = G.S / a.px, w = a.w * scale, h = a.h * scale;
    el.style.display = 'block'; el.style.width = w + 'px'; el.style.height = h + 'px'; el.style.opacity = op;
    el.style.backgroundImage = `url(${SRC}${name}.png)`; el.style.backgroundSize = `${a.n * w}px ${h}px`;
    el.style.backgroundPosition = `${-Math.min(frame, a.n - 1) * w}px 0`;
    el.style.transform = `translate(${Math.round(x - w / 2)}px, ${Math.round(yGround - a.ground * scale)}px)${flip ? ' scaleX(-1)' : ''}`;
  }

  // ---------- toàn bộ đoạn mở đầu là một hàm của thời gian t (giây) ----------
  function render(t) {
    const { F, D, B, oTop } = G;
    const sh = G.shiftC * INOUT(seg(t, T.sink, T.popU));
    const box = G.box.map(b => ({ x: b.x + sh, w: b.w })), uC = { ...G.uC, x: G.uC.x + sh }, cC = { ...G.cC, x: G.cC.x + sh };
    const xA = Math.max(box[0].x - 1.25 * D, .85 * D);
    const xF = cC.x + D / 2 + .55 * D + 7.5 * G.S;
    const runX = u => lerp(-A.chay.w * G.S / A.chay.px, xA, 1 - (1 - u) ** 1.4);

    // nền lớp phủ mờ dần khi logo thu về góc, để lộ bản đồ đang mở ra bên dưới
    bg.style.opacity = 1 - seg(t, T.dock, T.dock + .45);

    // ----- chữ -----
    letters.forEach(({ L, g, k }) => {
      let x = 0, y = dyOf(k) * F, r = ROT[k], sx = 1, sy = 1, op = 1, clip = 'none';
      const e = OUT(seg(t, k * .04, k * .04 + .36)); y += .25 * D * (1 - e); op = e;
      if (k === 0) { const p = seg(t, 1.30, 1.42); sy = 1 - .02 * Math.sin(p * Math.PI); }
      if (k === I_U) {
        const T4 = T.dive + .1;
        if (t >= T4) { const a = seg(t, T4, T4 + .1), b = seg(t, T4 + .1, T4 + .26);
          sx = t < T4 + .1 ? lerp(1, 1.08, OUT(a)) : lerp(1.08, 1, BOUNCE(b)); sy = t < T4 + .1 ? lerp(1, .9, OUT(a)) : lerp(.9, 1, BOUNCE(b)); }
        if (t >= T.sink + .1 && t < T.popU) x = Math.sin(seg(t, T.sink + .1, T.popU) * Math.PI * 8) * .03 * D;
        if (t >= T.popU) { const sc = lerp(1.18, 1, BOUNCE(seg(t, T.popU, T.popU + .22))); sx *= sc; sy *= sc; }
      }
      if (SINK.includes(k)) {
        const j = SINK.indexOf(k), a = T.sink + j * .03, sink = 1.15 * F * IN(seg(t, a, a + .26));
        y += sink; if (t >= a) clip = `inset(-50% -50% ${F - G.baseLocal - .05 * F + sink + dyOf(k) * F}px -50%)`;
        if (t >= a + .26) op = 0;
      }
      if (k === I_C) {
        const e2 = INOUT(seg(t, T.sink, T.popU)); x += G.dxC * e2; r = lerp(ROT[k], -360 + C_ROT, e2); y = lerp(dyOf(k), C_DY, e2) * F + .25 * D * (1 - e);
        if (t >= T.tunnel + .1 && t < T.popC) x += Math.sin(seg(t, T.tunnel + .1, T.popC) * Math.PI * 4) * .03 * D;
        if (t >= T.popC) { const sc = lerp(1.18, 1, BOUNCE(seg(t, T.popC, T.popC + .22))); sx *= sc; sy *= sc; }
      }
      L.style.transform = `translate(${x}px, ${y}px) rotate(${r}deg) scale(${sx}, ${sy})`;
      L.style.opacity = op; L.style.clipPath = clip;
      const want = k === I_U && t >= T.popU ? 'u' : k === I_C && t >= T.popC ? 'c' : WORD[k];
      if (g.textContent !== want) g.textContent = want;
    });
    ears.forEach(({ s: el }, i) => {
      const a = T.sit + .06 + i * .06, p = seg(t, a, a + .32);
      const sc = p <= 0 ? 0 : p < .45 ? lerp(0, 1.15, OUT(p / .45)) : p < .75 ? lerp(1.15, .95, (p - .45) / .3) : lerp(.95, 1, (p - .75) / .25);
      el.style.transform = `scale(${sc})`;
      el.style.opacity = sc > 0 ? 1 - seg(t, T.dock, T.dock + .25) : 0;
    });

    // ----- cáo -----
    let fox = null, behind = false, clipY = null, inU = false, inC = false;
    const headY = uC.y + .12 * D;
    if (t >= T.run && t < T.brake) fox = ['chay', Math.floor((t - T.run) / .06) % 6, runX(seg(t, T.run, T.brake)), B, true];
    else if (t >= T.brake && t < T.jump) fox = ['lay-da', play(t, T.brake, [30, 30, 40, 40, 40, 80]), xA + .12 * D * OUT(seg(t, T.brake, T.brake + .06)), B, true];
    else if (t >= T.jump && t < T.fly) fox = ['bat', play(t, T.jump, [30, 30, 40]), xA + .12 * D + .25 * D * seg(t, T.jump + .03, T.fly), B, true];
    else if (t >= T.fly && t < T.dive) {
      const u = seg(t, T.fly, T.dive), x0 = xA + .37 * D;
      fox = ['bay', play(t, T.fly, [30, 30, 30, 30, 40, 50, 50, 40, 30, 30, 30, 30]), lerp(x0, uC.x, u), lerp(B, oTop + .05 * D, u) - 4 * u * (1 - u) * 1.35 * D, true];
    } else if (t >= T.dive && t < T.dive + .38) {
      fox = ['lao-xuong', play(t, T.dive, [30, 30, 30, 30, 30, 30, 30, 30, 70, 70]), uC.x, oTop + .6 * G.sw, true]; behind = true;
    } else if (t >= T.popU && t < T.look) { fox = ['troi-dau', play(t, T.popU, [40, 40, 40, 40, 40, 70]), uC.x, headY, false]; behind = true; clipY = headY; inU = true; }
    else if (t >= T.look && t < T.duck) { fox = ['nhin-quanh', play(t, T.look, [60, 35, 35, 70, 35, 35, 35, 70, 35]), uC.x, headY, false]; behind = true; clipY = headY; inU = true; }
    else if (t >= T.duck && t < T.tunnel) { fox = ['thut', play(t, T.duck, [35, 35, 35, 35]), uC.x, headY, false]; behind = true; clipY = headY; inU = true; }
    else if (t >= T.tunnel && t < T.popC - .07) fox = ['tai-luot', Math.floor((t - T.tunnel) / .04) % 6, lerp(uC.x, cC.x, INOUT(seg(t, T.tunnel, T.popC))), B + .03 * D, true];
    else if (t >= T.popC - .07 && t < T.land) {
      const i = play(t, T.popC - .07, [35, 35, 30, 35, 35, 100, 100, 100]), u = seg(t, T.popC, T.land);
      const x = lerp(cC.x, xF, u), y = B - 4 * u * (1 - u) * .8 * D;
      fox = i < 5 ? ['bung-ra-moi', i, x, y, true] : ['bung-ra', i, x, y, false];
      if (t < T.popC) { behind = true; inC = true; }
    } else if (t >= T.land && t < T.shake) fox = ['dap-dat', play(t, T.land, [35, 45, 45, 55, 70, 90]), xF, B, true];
    else if (t >= T.shake && t < T.sit) fox = ['giu-dat', play(t, T.shake, [45, 45, 45, 45, 45, 45]), xF, B, true];
    else if (t >= T.sit && t < T.wag) fox = ['ngoi-xuong', play(t, T.sit, [50, 50, 50, 50, 50]), xF, B, false];
    else if (t >= T.wag && t < T.turn) fox = ['vay-duoi', play(t, T.wag, Array(10).fill(50)), xF, B, false];
    else if (t >= T.turn && t < T.dock) fox = t < T.turn + .46 ? ['quay-dau', play(t, T.turn, [60, 60, 60, 160, 60, 60], [2, 3, 4, 4, 3, 2]), xF, B, false]
      : ['ngoi-tho', play(t, T.turn + .46, [120, 120, 120, 160, 120, 120, 120, 160]), xF, B, false];
    else if (t >= T.dock && t < T.dock + .25) fox = ['ngoi-xuong', play(t, T.dock, [50, 50, 50, 50, 50], [4, 3, 2, 1, 0]), xF, B, false];
    else if (t >= T.dock + .25) { const u = seg(t, T.dock + .25, END);
      fox = u < 1 ? ['chay', Math.floor((t - T.dock) / .06) % 6, lerp(xF, G.vw + A.chay.w * G.S / A.chay.px, IN(u)), B, true] : null; }
    if (fox) sprite(foxEl, ...fox); else foxEl.style.display = 'none';
    foxwrap.style.zIndex = behind ? 1 : 3;
    const cl = inU ? uC.x - .78 * D : 0, cr = inU ? G.vw - (uC.x + .78 * D) : 0;
    foxwrap.style.clipPath = inC ? `inset(${oTop}px ${G.vw - cC.x - .5 * D}px ${G.vh - B - .02 * D}px ${cC.x - .5 * D}px)`
      : clipY == null ? 'none' : `inset(0 ${cr}px ${G.vh - clipY}px ${cl}px)`;

    // bóng dưới cáo, nhỏ dần theo độ cao; không vẽ khi cáo trong chữ, bay trên dãy chữ, hoặc khung đã vẽ sẵn bóng
    const overWord = fox && fox[2] > box[0].x - .2 * D && fox[2] < cC.x + .6 * D;
    if (fox && !behind && !['bung-ra-moi', 'giu-dat', 'tai-luot'].includes(fox[0]) && !(overWord && fox[3] < B - .05 * D) && t < T.dock) {
      const h = Math.max(0, B - fox[3]), idx = Math.min(5, 1 + Math.round(h / (.3 * D)));
      sprite(shEl, 'bong', idx, fox[2], B + .06 * D, false, .5);
    } else shEl.style.display = 'none';

    // hiệu ứng (ảnh 56)
    const fx = [], once = (name, t0, ms, x, y, flip) => { const n = A[name].n; if (t >= t0 && t < t0 + n * ms / 1000) fx.push([name, Math.floor((t - t0) * 1000 / ms), x, y, flip]); };
    const loopFx = (name, ms, t0, t1, x, y, flip) => { if (t >= t0 && t < t1) fx.push([name, Math.floor((t - t0) * 1000 / ms) % A[name].n, x, y, flip]); };
    for (let k = 0; ; k++) { const t0 = T.run + k * .06; if (t0 >= T.brake) break; if (![1, 4].includes(k % 6)) continue;
      once('bui-chay', t0, 40, runX(seg(t0, T.run, T.brake)) - .55 * D, B + .04 * D, true); }
    once('bui-chay', T.brake, 40, xA - .4 * D, B + .04 * D, true);
    once('bui-chay', T.jump + .03, 40, xA - .1 * D, B + .04 * D, true);
    once('dat-vang', T.dive + .12, 40, uC.x, oTop + .15 * D, false);
    loopFx('vach-rung', 40, T.sink + .1, T.popU, uC.x, uC.y + .2 * D, false);
    SINK.forEach((k, j) => once('bui-chay', T.sink + j * .03 + .05, 40, box[k].x + box[k].w / 2, B + .04 * D, false));
    once('dat-roi', T.popU + .1, 50, uC.x + .15 * D, oTop - .15 * D, false);
    if (t >= T.tunnel && t < T.popC - .07) loopFx('dat-vang', 40, T.tunnel, T.popC, lerp(uC.x, cC.x, INOUT(seg(t, T.tunnel, T.popC))) - .2 * D, B + .03 * D, true);
    loopFx('vach-rung', 40, T.tunnel + .1, T.popC, cC.x, cC.y + .2 * D, false);
    once('bui-bung', T.popC, 35, cC.x + .55 * D, B + .03 * D, false);
    once('bui-dap', T.land, 40, xF, B + .04 * D, false);
    once('bui-chay', T.dock + .25, 40, xF - .4 * D, B + .04 * D, true);
    pool.forEach((el, i) => { if (fx[i]) sprite(el, ...fx[i]); else el.style.display = 'none'; });

    // mảnh bìa vỡ khi cáo phá chữ o
    const shards = [];
    [[-.6, 1.1, -.9], [-.2, .9, -.3], [.25, 1.0, .4], [.65, .6, .8]].forEach(([dx, hh, vx], i) => shards.push({ t0: T.popU, x0: uC.x + dx * D * .3, y0: oTop + G.sw * .4, vx: vx * D * 1.6, h: hh * D, size: (.09 + .02 * i) * D, spin: 260 * vx }));
    [[.2, .5], [.45, .25], [.3, .8]].forEach(([hh, dy], i) => shards.push({ t0: T.popC, x0: cC.x + D * .45, y0: cC.y - dy * D * .3, vx: (1.6 + i * .5) * D, h: hh * D, size: (.08 + .025 * i) * D, spin: 300 }));
    chips.forEach((el, i) => { const c = shards[i], u = (t - c.t0) / .45;
      if (!c || u < 0 || u >= 1) { el.style.display = 'none'; return; }
      const x = c.x0 + c.vx * u * .45, y = c.y0 - c.h * (2 * u - u * u * 1.6);
      el.style.display = 'block'; el.style.width = el.style.height = c.size + 'px'; el.style.opacity = 1 - u ** 3;
      el.style.transform = `translate(${x - c.size / 2}px, ${y - c.size / 2}px) rotate(${c.spin * u}deg)`; });

    // ----- thu logo về đúng chỗ chữ "puc" của bản đồ (map.css: .brand cách mép 14px, điện thoại cách trái 10px; cỡ chữ 21px; khung cao 35px) -----
    const d = INOUT(seg(t, T.dock, T.dock + .45)), k = 21 / F, edgeX = G.vw <= 560 ? 10 : 14, edgeY = 14;
    const pLeft = G.box[0].x, Xe = edgeX + 15 - G.left - k * (pLeft - G.left),
      Ye = edgeY + 17.5 + (.508 - .19 - .04) / 2 * 21 - G.top - k * G.baseLocal;   // phần mực "puc" nằm giữa khung
    wordEl.style.transform = `translate(${lerp(sh, Xe, d)}px, ${lerp(0, Ye, d)}px) scale(${lerp(1, k, d)})`;
    brandEl.style.left = edgeX + 'px'; brandEl.style.top = edgeY + 'px';
    brandEl.style.width = ((G.cRight + .05 * D - pLeft) * k + 30) + 'px';
    brandEl.style.opacity = seg(t, T.dock + .3, T.dock + .5);
  }

  // ---------- chạy ----------
  const q = new URLSearchParams(location.search), FIX = q.has('it') ? +q.get('it') : null, SPEED = +(q.get('ispeed') || 1);
  await document.fonts.load('400 100px "Paytone One"');
  let t0 = performance.now(), skipTo = null, lastT = 0, gateOpen = false, rz = 0;
  measure();
  addEventListener('resize', () => { cancelAnimationFrame(rz); rz = requestAnimationFrame(() => { if (G) { measure(); render(lastT); } }); });
  const skip = () => { if (lastT < T.dock) skipTo = END; };
  addEventListener('keydown', skip); addEventListener('wheel', skip, { passive: true }); stage.addEventListener('pointerdown', skip);

  await new Promise(done => {
    function tick(now) {
      let t = FIX ?? (now - t0) / 1000 * SPEED;
      if (skipTo != null) t = Math.max(t, skipTo);
      lastT = Math.min(t, END); render(lastT);
      if (lastT >= T.dock && !gateOpen) { gateOpen = true; stage.classList.add('li-docked'); openGate(); }
      if (FIX != null) { if (!gateOpen) openGate(); return; }   // chế độ chụp kiểm tra: giữ nguyên khung
      if (t < END) requestAnimationFrame(tick); else done();
    }
    requestAnimationFrame(tick);
  });
  removeEventListener('keydown', skip); removeEventListener('wheel', skip);

  // đổi chỗ với chữ "puc" của bản đồ: chờ bản đồ hiện khung giao diện (gỡ lớp intro của #map) rồi chờ khung trượt xong
  const mapEl = document.getElementById('map');
  await new Promise(res => {
    const ready = () => !mapEl || !mapEl.classList.contains('intro');
    if (ready()) return res();
    const mo = new MutationObserver(() => { if (ready()) { mo.disconnect(); res(); } });
    mo.observe(mapEl, { attributes: true, attributeFilter: ['class'] });
    setTimeout(() => { mo.disconnect(); res(); }, 6000);   // phòng khi bản đồ không dựng được (không có WebGL)
  });
  await new Promise(r => setTimeout(r, 700));
  // chữ "puc" của bản đồ hiện lại trong lúc logo của đoạn mở đầu mờ đi (250 ms), rồi gỡ hẳn lớp phủ
  document.documentElement.classList.remove('li-brand-off');
  await stage.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 250, fill: 'forwards' }).finished;
  document.documentElement.classList.remove('li-on');
  stage.remove();
}
