# Dựng trang bản đồ project từ site.json (bản Python của scripts/build.mjs trong site-to-map, vì máy không có Node).
# Chạy: python3 city/build.py   ->  city/out/index.html cùng engine. Xem thử: python3 -m http.server -d city/out 8770
import json, os, re, shutil, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, 'engine')
SITE = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'site.json')
OUT = os.path.join(HERE, sys.argv[2] if len(sys.argv) > 2 else 'out')

site = json.load(open(SITE, encoding='utf-8'))
kinds = json.load(open(os.path.join(ENGINE, 'kinds.json'), encoding='utf-8'))
KINDS = {k['kind'] for k in kinds}
SLOTS = ['center', 'highland', 'coast', 'south', 'east', 'town']

def loc(v, lang):
    if v is None: return ''
    if isinstance(v, str): return v
    return v.get(lang) or v.get('en') or next(iter(v.values()), '')

errors, used_slots, used_keys = [], set(), set()
cities = site.get('cities') or []
if not cities: errors.append('cities phải có ít nhất một thị trấn')
if len(cities) > 9: errors.append('tối đa 9 thị trấn')
for c in cities:
    where = f'thị trấn "{c.get("id")}"'
    if not re.fullmatch(r'[a-z0-9-]+', c.get('id', '')): errors.append(f'{where}: id chỉ gồm chữ thường, số, gạch ngang')
    if not c.get('name'): errors.append(f'{where}: thiếu name')
    s = c.get('slot')
    if s and s not in SLOTS: errors.append(f'{where}: slot phải là một trong {SLOTS}')
    if s and s != 'town' and s in used_slots: errors.append(f'{where}: slot "{s}" dùng hai lần')
    used_slots.add(s)
    k = (c.get('key') or '').lower()
    if k:
        if not re.fullmatch(r'[a-z]', k) or k in 'hotvli': errors.append(f'{where}: key "{k}" phải là một chữ, không phải H O T V L I')
        if k in used_keys: errors.append(f'{where}: key "{k}" dùng hai lần')
        used_keys.add(k)
    for it in c.get('items') or []:
        if not it.get('name') or not it.get('url'): errors.append(f'{where}: mỗi project cần name và url')
        if it.get('kind') and it['kind'] not in KINDS: errors.append(f'{where}: kind lạ "{it["kind"]}"')
if errors:
    print('site.json có lỗi:\n- ' + '\n- '.join(errors)); sys.exit(1)

lang = site['site'].get('lang') if site['site'].get('lang') not in (None, 'auto') else (site['site'].get('languages') or ['en'])[0]
title = loc((site.get('text') or {}).get(lang, {}).get('title'), lang) or site['site'].get('brand') or 'Map'
esc = lambda s: html.escape(str(s or ''), quote=True)
noscript = '<nav class="no-js" aria-label="Tất cả project">' + ''.join(
    f'<section><h2>{esc(loc(c["name"], lang))}</h2><ul>' + ''.join(f'<li><a href="{esc(it["url"])}">{esc(loc(it["name"], lang))}</a></li>' for it in c['items']) + '</ul></section>'
    for c in cities) + '</nav>'
daylight = site.get('ui', {}).get('daylight')
page = open(os.path.join(ENGINE, 'template.html'), encoding='utf-8').read()
page = (page.replace('{{LANG}}', 'zh-CN' if lang == 'zh' else lang)
        .replace('{{TITLE}}', esc(title))
        .replace('{{DAYLIGHT}}', f' data-daylight="{daylight}"' if isinstance(daylight, (int, float)) else '', 1)
        .replace('{{DESCRIPTION}}', esc(site['site'].get('description') or title))
        .replace('{{NOSCRIPT}}', noscript, 1)
        .replace('{{SITE_JSON}}', json.dumps(site, ensure_ascii=False).replace('<', '\\u003c'), 1))
os.makedirs(OUT, exist_ok=True)
# portfolio Puc: tên file có mã băm nội dung (map-engine.3f2a1c9d.js…). Trình duyệt được giữ file lâu mà không bao giờ
# dùng nhầm bản cũ; trước đây máy chủ không gửi Cache-Control nên trình duyệt tự giữ module cũ sau khi sửa.
import hashlib, glob
for old_f in glob.glob(os.path.join(OUT, '*.*.js')) + glob.glob(os.path.join(OUT, '*.*.css')): os.remove(old_f)
for f in ('map-engine.js', 'world-gen.js', 'daylight.js', 'map.css', 'papercraft-ui.css', 'papercut-letters.js', 'logo-intro.js', 'logo-intro.css'):
    p2 = os.path.join(OUT, f)
    if os.path.exists(p2): os.remove(p2)
def emit(name, text):
    h = hashlib.sha1(text.encode('utf-8')).hexdigest()[:8]
    stem, ext = os.path.splitext(name); out = f'{stem}.{h}{ext}'
    open(os.path.join(OUT, out), 'w', encoding='utf-8').write(text); return out
read = lambda f: open(os.path.join(ENGINE, f), encoding='utf-8').read()
H = {f: emit(f, read(f)) for f in ('world-gen.js', 'daylight.js', 'map.css', 'papercraft-ui.css', 'papercut-letters.js', 'logo-intro.js', 'logo-intro.css')}
eng = read('map-engine.js').replace("from './world-gen.js'", f"from './{H['world-gen.js']}'").replace("import './daylight.js'", f"import './{H['daylight.js']}'")
H['map-engine.js'] = emit('map-engine.js', eng)
page = (page.replace('href="map.css"', f'href="{H["map.css"]}"').replace('href="papercraft-ui.css"', f'href="{H["papercraft-ui.css"]}"')
        .replace('src="daylight.js"', f'src="{H["daylight.js"]}"').replace("from './map-engine.js'", f"from './{H['map-engine.js']}'")
        .replace("import './papercut-letters.js'", f"import './{H['papercut-letters.js']}'")
        .replace('href="logo-intro.css"', f'href="{H["logo-intro.css"]}"').replace('src="logo-intro.js"', f'src="{H["logo-intro.js"]}"')
        .replace('{{MODULEPRELOAD}}', ''.join(f'<link rel="modulepreload" href="{h}">' for h in (H['map-engine.js'], H['world-gen.js'], H['daylight.js']))))
assert all(v in page or v in eng for v in H.values()), 'thiếu tham chiếu file băm'
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
# portfolio Puc: ảnh con cáo và hiệu ứng của đoạn mở đầu (cắt từ ảnh người dùng gửi, xem design/logo-intro/tools/)
SPR = os.path.join(HERE, '..', 'design', 'logo-intro', 'cao', '5-bo-3')
names = re.findall(r"^\s+'?([a-z-]+)'?: \{ n:", read('logo-intro.js'), re.M) + re.findall(r", '?([a-z-]+)'?: \{ n:", read('logo-intro.js'))
os.makedirs(os.path.join(OUT, 'intro'), exist_ok=True)
for n in sorted(set(names)): shutil.copyfile(os.path.join(SPR, n + '.png'), os.path.join(OUT, 'intro', n + '.png'))
print(f'đoạn mở đầu: {len(set(names))} tấm ảnh trong out/intro/')
print(f'xong {OUT}/index.html: {len(cities)} thị trấn, {sum(len(c["items"]) for c in cities)} project')
