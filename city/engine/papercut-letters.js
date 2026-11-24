// Chữ giấy cắt cho bản đồ project của Puc: tách các tiêu đề thành từng chữ cái, mỗi chữ là một mẩu giấy
// dán hơi lệch (xoay và nhích lên xuống theo một dãy cố định, nên lần nào tải cũng giống nhau).
// Người đọc màn hình vẫn đọc cả câu nhờ một bản chữ ẩn; các mẩu chữ được đánh dấu aria-hidden.
// Kiểu dáng nằm trong papercraft-ui.css (.pc-word, .pc-l). Engine đổi nội dung các khung này khi chuyển thị trấn,
// nên một MutationObserver tách lại mỗi khi có chữ mới.
const TARGETS = '.c-tag .en, .panel h2, .brand .site, .ld-title, .bubble-copy strong, .keys h2';
const ROT = [-3, 2, -1.5, 3, -2.5, 1, -0.5, 2.5, -1, 1.5];
const DY = [0, -1, 1, -0.5, 0.5, -1.5, 1, 0, -1, 0.5];

function cutText(node) {
  const text = node.nodeValue.normalize('NFC');
  if (!text.trim()) return;
  const frag = document.createDocumentFragment();
  const sr = document.createElement('span'); sr.className = 'pc-sr'; sr.textContent = text; frag.append(sr);
  let k = 0;
  text.split(/(\s+)/).forEach(part => {
    if (!part) return;
    if (/^\s+$/.test(part)) { frag.append(document.createTextNode(' ')); return; }
    const word = document.createElement('span'); word.className = 'pc-word'; word.setAttribute('aria-hidden', 'true');
    for (const ch of part) {
      const l = document.createElement('span'); l.className = 'pc-l'; l.textContent = ch;
      l.style.setProperty('--r', ROT[k % ROT.length] + 'deg');
      l.style.setProperty('--y', DY[(k * 3) % DY.length] + 'px');
      word.append(l); k++;
    }
    frag.append(word);
  });
  node.replaceWith(frag);
}

function run() {
  for (const el of document.querySelectorAll(TARGETS)) {
    for (const n of [...el.childNodes]) if (n.nodeType === Node.TEXT_NODE) cutText(n);
  }
}

let queued = false;
const mo = new MutationObserver(() => { if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; run(); }); } });
mo.observe(document.body, { childList: true, subtree: true, characterData: true });
run();
