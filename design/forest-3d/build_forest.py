# Dựng khu rừng giấy 3D cho màn đầu portfolio, chạy trong Blender không cần mở giao diện:
#   /Applications/Blender.app/Contents/MacOS/Blender -b -P design/forest-3d/build_forest.py -- --samples 96
# Kết quả: design/forest-3d/forest.blend (mở bằng Blender để chỉnh tay) và design/forest-3d/render.png.
# Phong cách lấy cảm hứng từ ảnh mẫu (rừng giấy, nền xanh xám, lối đi kem); bố cục và từng vật là của riêng trang này.
import bpy, bmesh, math, random, re, sys, os
from mathutils import Vector

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def arg(name, default):
    return type(default)(ARGS[ARGS.index(name) + 1]) if name in ARGS else default
SAMPLES = arg('--samples', 96)
SEED = arg('--seed', 7)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, arg('--out', 'render.png'))
random.seed(SEED)

# ---------- bảng màu (dịu như nỉ và giấy) ----------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shapes import PAL, svg_poly, SHAPES
def rgb(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [1]

# ---------- dọn cảnh ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ---------- vật liệu ----------
_mats = {}
def mat(key, rough=0.92, emit=0.0, bump=0.12, sheen=0.3):
    k = (key, emit)
    if k in _mats: return _mats[k]
    m = bpy.data.materials.new(f'{key}{"_glow" if emit else ""}')
    m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = rgb(PAL[key])
    b.inputs['Roughness'].default_value = rough
    if 'Sheen Weight' in b.inputs: b.inputs['Sheen Weight'].default_value = sheen
    if emit:
        b.inputs['Emission Color'].default_value = rgb(PAL[key]); b.inputs['Emission Strength'].default_value = emit
    if bump:
        tex = nt.nodes.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = 380; tex.inputs['Detail'].default_value = 8
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.002
        nt.links.new(tex.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    _mats[k] = m
    return m

# ---------- dựng tấm giấy đứng ----------
def flat_mesh(name, polys2d, thick, material, rim=None):
    """polys2d: danh sách đa giác trong mặt phẳng XZ (đơn vị mét). Mặt giấy quay về phía -Y."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    for pi, poly in enumerate(polys2d):
        if len(poly) < 3: continue
        vs = [bm.verts.new((x, -0.0016 * pi, z)) for x, z in poly]
        try: bm.faces.new(vs)
        except ValueError: pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='EAR_CLIP')
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); me.materials.append(material)
    if thick:
        if rim: me.materials.append(rim)
        sol = ob.modifiers.new('bề dày', 'SOLIDIFY'); sol.thickness = thick; sol.offset = 1
        if rim: sol.material_offset_rim = 1
    return ob

def stroke_polys(d, width):
    out = []
    for line in svg_poly(d, 6):
        for (x0, y0), (x1, y1) in zip(line, line[1:]):
            dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L * width / 2, dx / L * width / 2
            out.append([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)])
    return out

ACG = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'references', 'hand-drawn', 'ambientcg')
def felt_detail(nt, b, color_out, scale, asset='Fabric034', coord='UV', normal_strength=0.7, amount=0.35):
    """Phủ vân nỉ chụp thật (ambientCG, CC0) lên màu đã có: nhân độ sáng sợi nỉ và dùng normal map của nó."""
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale, scale, scale)
    nt.links.new(tc.outputs[coord], mp.inputs['Vector'])
    col = nt.nodes.new('ShaderNodeTexImage'); col.image = bpy.data.images.load(os.path.join(ACG, asset, f'{asset}_2K-JPG_Color.jpg'), check_existing=True)
    nt.links.new(mp.outputs['Vector'], col.inputs['Vector'])
    bw = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(col.outputs['Color'], bw.inputs['Color'])
    rng = nt.nodes.new('ShaderNodeMapRange'); rng.inputs['From Min'].default_value = 0.2; rng.inputs['From Max'].default_value = 0.8
    rng.inputs['To Min'].default_value = 1 - amount; rng.inputs['To Max'].default_value = 1 + amount * 0.6
    nt.links.new(bw.outputs['Val'], rng.inputs['Value'])
    mul = nt.nodes.new('ShaderNodeVectorMath'); mul.operation = 'MULTIPLY'
    nt.links.new(color_out, mul.inputs[0]); nt.links.new(rng.outputs['Result'], mul.inputs[1])
    nt.links.new(mul.outputs['Vector'], b.inputs['Base Color'])
    nm = nt.nodes.new('ShaderNodeTexImage'); nm.image = bpy.data.images.load(os.path.join(ACG, asset, f'{asset}_2K-JPG_NormalGL.jpg'), check_existing=True)
    nm.image.colorspace_settings.name = 'Non-Color'; nt.links.new(mp.outputs['Vector'], nm.inputs['Vector'])
    nmap = nt.nodes.new('ShaderNodeNormalMap'); nmap.inputs['Strength'].default_value = normal_strength
    nt.links.new(nm.outputs['Color'], nmap.inputs['Color']); nt.links.new(nmap.outputs['Normal'], b.inputs['Normal'])

TEX = os.path.join(HERE, 'textures')
_tmats = {}
def tex_mat(kind, v):
    key = (kind, v)
    if key in _tmats: return _tmats[key]
    m = bpy.data.materials.new(f'giấy {kind} {v}'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    img = bpy.data.images.load(os.path.join(TEX, f'{kind}_{v}.png'), check_existing=True)
    tn = nt.nodes.new('ShaderNodeTexImage'); tn.image = img; tn.extension = 'EXTEND'
    nt.links.new(tn.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.96
    if 'Sheen Weight' in b.inputs: b.inputs['Sheen Weight'].default_value = 0.55; b.inputs['Sheen Roughness'].default_value = 0.6
    # vân nỉ: nhiễu mịn + một chút theo độ sáng của hình vẽ
    felt_detail(nt, b, tn.outputs['Color'], 1.2, 'Fabric034', 'UV', 0.8, 0.28)
    _tmats[key] = m; return m

def make_standee(kind, parts, w, h, height):
    """Một tấm giấy cắt theo đường viền các phần chính, mặt in texture vẽ tay, mép là giấy."""
    k = height / h
    v = random.randrange(3)
    polys = []
    for d, col, mode, sw in parts:
        if mode == 'fill' and sw == 'main':
            polys += [[((x - w / 2) * k, (h - y) * k) for x, y in p] for p in svg_poly(d)]
    ob = flat_mesh(kind, polys, 0.014, tex_mat(kind, v))  # mép dùng luôn màu tờ giấy, như nỉ cắt
    uv = ob.data.uv_layers.new(name='UV')
    for loop in ob.data.loops:
        co = ob.data.vertices[loop.vertex_index].co
        uv.data[loop.index].uv = (co.x / (k * w) + 0.5, co.z / (k * h))
    root = bpy.data.objects.new(kind, None); ob.parent = root
    return root

_protos = {}
def proto(kind, height):
    w, h, parts = SHAPES[kind]
    key = (kind, round(height, 2))
    return make_standee(kind, parts, w, h, height)

import json
ARTD = os.path.join(HERE, 'art'); OUTL = json.load(open(os.path.join(ARTD, 'outlines.json')))
ART_OF = {'pine': ['pine', 'pine2'], 'yellow': ['yellow'], 'round': ['round'], 'flame': ['flame'], 'shrub': ['shrub', 'shrubDark'],
          'shrubY': ['shrubY'], 'flowerBush': ['flowerBush'], 'fern': ['fern'], 'grass': ['grass'], 'grass2': ['grass'],
          'foxSit': ['foxSit'], 'foxWalk': ['foxWalk'], 'mushrooms': ['mushrooms'], 'boulder': ['boulder'], 'lanternArt': ['lantern'], 'logArt': ['log']}
_artmesh, _artmat = {}, {}
def art_mesh(name):
    """Tấm nỉ cắt theo đúng đường bao của hình vẽ, cao 1 m, mặt in chính hình vẽ đó."""
    if name in _artmesh: return _artmesh[name]
    o = OUTL[name]; w, h = o['w'], o['h']; k = 1.0 / h
    me = bpy.data.meshes.new('nỉ ' + name); bm = bmesh.new()
    poly = o['polys'][0]
    vs = [bm.verts.new(((px - w / 2) * k, 0, (h - py) * k)) for px, py in poly]
    bm.faces.new(vs)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='EAR_CLIP')
    uv = bm.loops.layers.uv.new('UV')
    for f in bm.faces:
        for lp in f.loops:
            co = lp.vert.co; lp[uv].uv = (co.x / (k * w) + 0.5, co.z / (k * h))
    bm.to_mesh(me); bm.free()
    m = bpy.data.materials.new('nỉ vẽ ' + name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tn = nt.nodes.new('ShaderNodeTexImage'); tn.image = bpy.data.images.load(os.path.join(ARTD, name + '.png'), check_existing=True); tn.extension = 'EXTEND'
    nt.links.new(tn.outputs['Color'], b.inputs['Base Color']); nt.links.new(tn.outputs['Alpha'], b.inputs['Alpha'])
    b.inputs['Roughness'].default_value = 0.97
    if 'Sheen Weight' in b.inputs: b.inputs['Sheen Weight'].default_value = 0.6; b.inputs['Sheen Roughness'].default_value = 0.55
    felt_detail(nt, b, tn.outputs['Color'], 1.0, 'Fabric034', 'UV', 0.45, 0.12)
    me.materials.append(m)
    _artmesh[name] = me; return me
def add_art(kind, x, y, height, rot=None, cross=False):
    name = random.choice(ART_OF[kind]); me = art_mesh(name)
    root = bpy.data.objects.new(kind, None); root.location = (x, y, 0); root.scale = (height, height, height)
    root.rotation_euler = (0, 0, math.radians(rot if rot is not None else random.uniform(-15, 15)))
    if random.random() < 0.5 and not cross: root.scale.x = -height   # lật ngang cho đỡ lặp
    coll.objects.link(root)
    for i in range(2 if cross else 1):
        ob = bpy.data.objects.new(f'{kind}.{i}', me); ob.parent = root; ob.rotation_euler.z = math.radians(90 * i)
        sol = ob.modifiers.new('bề dày', 'SOLIDIFY'); sol.thickness = 0.012 / height; sol.offset = 1
        coll.objects.link(ob)
    return root

def link_tree(root, coll):
    coll.objects.link(root)
    for c in root.children: coll.objects.link(c)

coll = bpy.data.collections.new('Rừng giấy'); scene.collection.children.link(coll)

def add_standee(kind, x, y, height, rot=None, cross=False):
    if kind in ART_OF: return add_art(kind, x, y, height, rot, cross)
    r = proto(kind, height)
    r.location = (x, y, 0)
    r.rotation_euler = (0, 0, math.radians(rot if rot is not None else random.uniform(-18, 18)))
    link_tree(r, coll)
    if cross:  # cây giấy cài chéo hai tấm, nhìn góc nào cũng có khối
        r2 = proto(kind, height); r2.location = (x, y, 0)
        r2.rotation_euler = (0, 0, r.rotation_euler.z + math.radians(90)); link_tree(r2, coll)
    return r

# ---------- mặt đất nỉ ----------
def _mv(o):
    for c in list(o.users_collection): c.objects.unlink(o)
    coll.objects.link(o)
bpy.ops.mesh.primitive_plane_add(size=1)
ground = bpy.context.active_object; ground.name = 'Mặt đất nỉ'; ground.scale = (30, 22, 1)
gm = bpy.data.materials.new('ground'); gm.use_nodes = True; nt = gm.node_tree; b = nt.nodes['Principled BSDF']
b.inputs['Roughness'].default_value = 1.0
if 'Sheen Weight' in b.inputs: b.inputs['Sheen Weight'].default_value = 0.8
noise = nt.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 1.2; noise.inputs['Detail'].default_value = 3
ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = rgb(PAL['ground3']); ramp.color_ramp.elements[1].color = rgb(PAL['ground2'])
ramp.color_ramp.elements[0].position = 0.38; ramp.color_ramp.elements[1].position = 0.62
nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
felt_detail(nt, b, ramp.outputs['Color'], 20, 'Fabric028', 'Generated', 1.0, 0.3)
ground.data.materials.append(gm)

# ---------- lối đi chữ Y như ảnh mẫu ----------
def catmull(pts, n=12):
    out = []
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]; p1, p2 = pts[i], pts[i + 1]; p3 = pts[i + 2] if i + 2 < len(pts) else p2
        for s_ in range(n):
            t = s_ / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1]); return out
MAIN = [(-11, -0.9), (-6.5, -1.2), (-3, -0.7), (0.0, -0.3), (1.8, 0.6), (2.6, 2.6), (2.9, 5.0), (3.1, 9)]
BRANCH = [(1.9, 0.9), (3.6, 0.0), (6.0, -0.6), (9.0, -0.3), (12, -0.5)]
LINES = [catmull(MAIN), catmull(BRANCH)]
def ribbon(name, line, half, z, color):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); left, right = [], []
    for i, (x, y) in enumerate(line):
        a = line[min(i + 1, len(line) - 1)]; b_ = line[max(i - 1, 0)]
        dx, dy = a[0] - b_[0], a[1] - b_[1]; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
        hw = half * (1 + 0.12 * math.sin(i * 0.8))
        left.append(bm.verts.new((x + nx * hw, y + ny * hw, z))); right.append(bm.verts.new((x - nx * hw, y - ny * hw, z)))
    for i in range(len(line) - 1): bm.faces.new((left[i], left[i + 1], right[i + 1], right[i]))
    bm.to_mesh(me); bm.free(); ob = bpy.data.objects.new(name, me); me.materials.append(mat(color, bump=0.25)); coll.objects.link(ob)
for i, line in enumerate(LINES):
    ribbon(f'Mép lối đi {i}', line, 0.38, 0.004 + i * 0.002, 'pathEdge')
    ribbon(f'Lối đi {i}', line, 0.32, 0.012 + i * 0.002, 'path')
def dpath(x, y): return min(math.hypot(x - a, y - b) for line in LINES for a, b in line)

# ---------- khối 3D: đá, đá dẹt, nấm, gỗ, đèn, người đội mũ ----------
def boulder(x, y, s, tall=0.9, col='rock'):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1)
    r = bpy.context.active_object; r.name = 'Đá nỉ'
    for v in r.data.vertices:
        v.co.x *= random.uniform(0.7, 1.3); v.co.y *= random.uniform(0.7, 1.2); v.co.z = max(0, v.co.z) * random.uniform(0.7, 1.1)
    r.location = (x, y, 0); r.scale = (s * random.uniform(0.9, 1.3), s, s * tall); r.rotation_euler.z = random.uniform(0, 6.28)
    r.data.materials.append(felt(col)); _mv(r)
_felts = {}
def felt(key):
    if key in _felts: return _felts[key]
    m = bpy.data.materials.new('nỉ ' + key); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 7; nz.inputs['Detail'].default_value = 4
    rp = nt.nodes.new('ShaderNodeValToRGB'); c = rgb(PAL[key])
    rp.color_ramp.elements[0].color = [c[0] * 0.8, c[1] * 0.84, c[2] * 0.84, 1]; rp.color_ramp.elements[1].color = [min(1, c[0] * 1.12), min(1, c[1] * 1.12), min(1, c[2] * 1.1), 1]
    nt.links.new(nz.outputs['Fac'], rp.inputs['Fac']); nt.links.new(rp.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 1.0
    if 'Sheen Weight' in b.inputs: b.inputs['Sheen Weight'].default_value = 0.8; b.inputs['Sheen Roughness'].default_value = 0.5
    fz = nt.nodes.new('ShaderNodeTexNoise'); fz.inputs['Scale'].default_value = 700; fz.inputs['Detail'].default_value = 14
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.4; bp.inputs['Distance'].default_value = 0.003
    nt.links.new(fz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    _felts[key] = m; return m
def stone(x, y, s): boulder(x, y, s, tall=0.35, col='stone')
def mushroom(x, y, s):
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.07 * s, depth=0.26 * s, location=(x, y, 0.13 * s))
    st = bpy.context.active_object; st.data.materials.append(mat('stem')); _mv(st)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=7, radius=0.2 * s, location=(x, y, 0.24 * s))
    cap = bpy.context.active_object; cap.scale.z = 0.72
    for v in cap.data.vertices: v.co.z = max(v.co.z, -0.02)
    cap.data.materials.append(mat('mushCap')); _mv(cap)
    for i in range(6):
        a = random.uniform(0, 6.28); r = random.uniform(0.06, 0.15) * s
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.028 * s, depth=0.01, location=(x + math.cos(a) * r, y + math.sin(a) * r, 0.24 * s + 0.12 * s))
        dot = bpy.context.active_object; dot.data.materials.append(mat('dot')); dot.rotation_euler = (math.sin(a) * -0.7, math.cos(a) * 0.7, 0); _mv(dot)
def log(x, y, s, rot):
    bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=0.12 * s, depth=0.7 * s, location=(x, y, 0.12 * s), rotation=(0, math.radians(90), math.radians(rot)))
    o = bpy.context.active_object; o.data.materials.append(mat('wood')); _mv(o)
def lantern(x, y):
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.035, depth=1.6, location=(x, y, 0.8)); p = bpy.context.active_object; p.data.materials.append(mat('wood')); _mv(p)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.022, depth=0.42, location=(x - 0.19, y, 1.58), rotation=(0, math.radians(90), 0)); arm = bpy.context.active_object; arm.data.materials.append(mat('wood')); _mv(arm)
    bpy.ops.mesh.primitive_cube_add(size=0.16, location=(x - 0.36, y, 1.4)); lamp = bpy.context.active_object; lamp.scale.z = 1.3; lamp.data.materials.append(mat('lamp', emit=1.4)); _mv(lamp)
    light = bpy.data.lights.new('Đèn treo', 'POINT'); light.energy = 25; light.color = (1, 0.8, 0.5); light.shadow_soft_size = 0.2
    lo = bpy.data.objects.new('Đèn treo', light); lo.location = (x - 0.36, y - 0.12, 1.36); coll.objects.link(lo)
    s1 = add_standee('arrowSign', x + 0.05, y - 0.05, 0.22, rot=0); s1.location.z = 1.05
    s2 = add_standee('arrowSign', x + 0.05, y - 0.05, 0.22, rot=180); s2.location.z = 0.78
def hiker(x, y):  # người nhỏ đội mũ rơm như ảnh mẫu
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.08, depth=0.46, location=(x, y, 0.23)); b_ = bpy.context.active_object; b_.data.materials.append(felt('cloth')); _mv(b_)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.07, location=(x, y, 0.52)); h = bpy.context.active_object; h.data.materials.append(mat('skin')); _mv(h)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.135, depth=0.015, location=(x, y, 0.575)); hb = bpy.context.active_object; hb.data.materials.append(mat('hat')); _mv(hb)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.065, depth=0.07, location=(x, y, 0.61)); hc = bpy.context.active_object; hc.data.materials.append(mat('hat')); _mv(hc)
    bpy.ops.mesh.primitive_cube_add(size=0.12, location=(x + 0.02, y + 0.09, 0.3)); bag = bpy.context.active_object; bag.scale = (1, 0.6, 1.3); bag.data.materials.append(mat('flame')); _mv(bag)

# ---------- bố cục theo ảnh mẫu ----------
taken = []
def free(x, y, r, pathgap=0.55):
    if dpath(x, y) < pathgap + r: return False
    return all(math.hypot(x - a, y - b) > r + rb for a, b, rb in taken)
def take(x, y, r, pathgap=0.55):
    if free(x, y, r, pathgap): taken.append((x, y, r)); return True
    return False
TREE_H = {'pine': (1.6, 2.6), 'yellow': (1.1, 1.6), 'flame': (0.8, 1.3), 'round': (1.0, 1.4)}
def tree(kind, x, y, mul=1.0):
    if take(x, y, 0.22):
        add_standee(kind, x, y, random.uniform(*TREE_H[kind]) * mul, cross=True); return True
    return False
def area(cx, cy, rx, ry, n, picks, f):
    for _ in range(n):
        x = cx + random.uniform(-rx, rx); y = cy + random.uniform(-ry, ry)
        f(random.choice(picks), x, y)

# đá nỉ vẽ tay quanh cụm đá
for _ in range(14):
    x, y = random.uniform(-2.2, 1.8), random.uniform(1.6, 6.4)
    if take(x, y, 0.3, 0.6): add_art('boulder', x, y, random.uniform(0.4, 0.7))
# cụm đá lớn ở giữa phía trên
for _ in range(40):
    x, y = random.uniform(-1.6, 1.4), random.uniform(2.4, 6.2)
    if take(x, y, 0.4, 0.7): add_art('boulder', x, y, random.uniform(0.6, 1.0))
# nấm đỏ góc trên bên trái
for _ in range(18):
    x, y = random.uniform(-4.8, -2.4), random.uniform(3.2, 5.4)
    if take(x, y, 0.3): add_art('mushrooms', x, y, random.uniform(0.45, 0.8))
# cây: thông rải rác, lá lửa và cây lá vàng
area(-5.5, 3.0, 3.0, 1.8, 46, ['flame', 'flame', 'round', 'pine'], tree)
area(-2.4, 4.6, 1.0, 1.4, 6, ['pine'], tree)
for x, y in [(-0.3, 3.7), (-1.9, 2.5), (0.9, 5.4)]: tree('pine', x, y, 1.05)
area(-8.0, 1.2, 1.4, 1.6, 10, ['round', 'pine', 'flame'], tree)
area(6.0, 3.4, 3.2, 2.6, 52, ['yellow', 'yellow', 'pine', 'round'], tree)
area(5.0, 0.9, 1.6, 0.6, 6, ['yellow'], tree)
area(-1.6, -2.6, 5.0, 0.8, 18, ['pine', 'yellow'], tree)
area(5.8, -2.6, 3.0, 1.2, 14, ['pine', 'yellow', 'yellow'], tree)
# cây gần camera (sẽ nhoè)
for x in (-4.6, -1.2, 2.6, 5.4):
    tree('pine', x + random.uniform(-0.3, 0.3), -4.3 + random.uniform(-0.4, 0.4), 1.2)
# bụi, cỏ, đá dẹt, dương xỉ
for _ in range(3200):
    x, y = random.uniform(-12, 12), random.uniform(-7.5, 9)
    r = random.random()
    if r < 0.24 and take(x, y, 0.24, 0.45): add_standee(random.choice(['shrub', 'shrubY']), x, y, random.uniform(0.34, 0.52))
    elif r < 0.38 and take(x, y, 0.24, 0.45): add_standee('flowerBush', x, y, random.uniform(0.28, 0.42))
    elif r < 0.45 and take(x, y, 0.22, 0.45): add_art('boulder', x, y, random.uniform(0.22, 0.36))
    elif r < 0.55 and take(x, y, 0.2, 0.45): add_standee('fern', x, y, random.uniform(0.34, 0.55), cross=True)
    elif r < 0.70 and take(x, y, 0.08, 0.5): add_standee(random.choice(['grass', 'grass2']), x, y, random.uniform(0.12, 0.2))
# bụi xanh viền cam dọc lối đi như ảnh mẫu
for line in LINES:
    for i in range(0, len(line), 9):
        x, y = line[i]; side = random.choice([-1, 1]); ox = random.uniform(0.75, 1.0) * side
        if take(x, y + ox, 0.28, 0.45): add_standee(random.choice(['shrub', 'shrubY', 'flowerBush']), x, y + ox, random.uniform(0.34, 0.48), rot=random.uniform(-10, 10))
for x, y, s, r in [(-1.0, -1.8, 1.0, 15), (6.6, 1.2, 1.1, 70), (-7.0, -2.4, 0.9, -20)]:
    taken.append((x, y, 0.4)); add_art('logArt', x, y, 0.45 * s, rot=r * 0.3)
# cáo giấy nhỏ
for (x, y), kind, rot in [((-2.6, 1.3), 'foxWalk', 15), ((2.3, 3.4), 'foxSit', -10), ((-3.9, 2.8), 'foxSit', 35), ((-0.6, 2.2), 'foxSit', 20), ((-3.4, 5.0), 'foxWalk', -10), ((-6.6, 3.8), 'foxSit', 30), ((-4.8, 2.0), 'foxWalk', 15), ((4.4, 5.6), 'foxSit', -20)]:
    taken.append((x, y, 0.2)); add_standee(kind, x, y, 0.55 if kind == 'foxSit' else 0.42, rot=rot)
hiker(1.1, 0.2); taken.append((1.1, 0.2, 0.3))
add_art('lanternArt', 4.1, 3.6, 1.5, rot=0); taken.append((4.1, 3.6, 0.4))

# ---------- ánh sáng mềm, camera nghiêng có nhoè ----------
world = bpy.data.worlds.new('Trời'); scene.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = rgb('#C9D2C6'); world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.8
sun = bpy.data.lights.new('Nắng', 'SUN'); sun.energy = 2.9; sun.angle = math.radians(25); sun.color = (1.0, 0.94, 0.84)
so = bpy.data.objects.new('Nắng', sun); so.rotation_euler = (math.radians(38), math.radians(-10), math.radians(-30)); scene.collection.objects.link(so)
cam = bpy.data.cameras.new('Camera'); cam.lens = arg('--lens', 38); cam.dof.use_dof = True; cam.dof.aperture_fstop = arg('--fstop', 0.32)
co = bpy.data.objects.new('Camera', cam); scene.collection.objects.link(co); scene.camera = co
co.location = (0.5, -6.9, 5.5)
focus = bpy.data.objects.new('Điểm nét', None); focus.location = (0.7, 0.7, 0.3); scene.collection.objects.link(focus)
cam.dof.focus_object = focus
dirv = focus.location - co.location; co.rotation_euler = dirv.to_track_quat('-Z', 'Y').to_euler()

scene.render.engine = 'CYCLES'
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'METAL'; prefs.get_devices()
    for dv in prefs.devices: dv.use = True
    scene.cycles.device = 'GPU'
except Exception as e:
    print('GPU không bật được, dùng CPU:', e)
scene.cycles.samples = SAMPLES; scene.cycles.use_denoising = True
scene.render.resolution_x = arg('--w', 1440); scene.render.resolution_y = arg('--h', 900); scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'Standard'; scene.view_settings.exposure = 0.15
scene.render.filepath = OUT_PNG
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'forest.blend'))
bpy.ops.render.render(write_still=True)
print('XONG', OUT_PNG)
