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
          'foxSit': ['foxSit'], 'foxWalk': ['foxWalk'], 'mushrooms': ['mushrooms'], 'boulder': ['boulder'], 'lanternArt': ['lantern'], 'logArt': ['log'], 'shrubDark': ['shrubDark']}
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
        sol = ob.modifiers.new('bề dày', 'SOLIDIFY'); sol.thickness = 0.008; sol.offset = 1
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
ground = bpy.context.active_object; ground.name = 'Mặt đất nỉ'; ground.scale = (70, 70, 1)
gm = bpy.data.materials.new('ground'); gm.use_nodes = True; nt = gm.node_tree; b = nt.nodes['Principled BSDF']
b.inputs['Roughness'].default_value = 1.0
if 'Sheen Weight' in b.inputs: b.inputs['Sheen Weight'].default_value = 0.8
noise = nt.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 9; noise.inputs['Detail'].default_value = 3
ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = rgb(PAL['ground3']); ramp.color_ramp.elements[1].color = rgb(PAL['ground2'])
ramp.color_ramp.elements[0].position = 0.38; ramp.color_ramp.elements[1].position = 0.62
nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
felt_detail(nt, b, ramp.outputs['Color'], 45, 'Fabric028', 'Generated', 1.0, 0.3)
ground.data.materials.append(gm)

# ---------- camera đặt trước, để xếp từng vật theo đúng vị trí của nó trên khung hình ảnh mẫu ----------
from bpy_extras.object_utils import world_to_camera_view
RX, RY = arg('--w', 1440), arg('--h', 900)
scene.render.resolution_x = RX; scene.render.resolution_y = RY; scene.render.resolution_percentage = 100
cam = bpy.data.cameras.new('Camera'); cam.lens = arg('--lens', 70); cam.sensor_fit = 'HORIZONTAL'; cam.sensor_width = 36
cam.dof.use_dof = True; cam.dof.aperture_fstop = arg('--fstop', 0.065)
co = bpy.data.objects.new('Camera', cam); scene.collection.objects.link(co); scene.camera = co
PITCH, DIST = math.radians(arg('--pitch', 42.0)), arg('--dist', 22.0)
co.location = (0, -DIST * math.cos(PITCH), DIST * math.sin(PITCH))
co.rotation_euler = (Vector((0, 0, 0)) - co.location).to_track_quat('-Z', 'Y').to_euler()
bpy.context.view_layer.update()

def g(u, v):
    """Điểm trên mặt đất nằm ở vị trí (u, v) của khung hình (0..1, gốc trên trái)."""
    d = co.matrix_world.to_3x3() @ Vector(((u - 0.5) * 36, (0.5 - v) * 36 * RY / RX, -cam.lens))
    o = co.matrix_world.translation; t = -o.z / d.z; p = o + d * t; p.z = 0; return p
def h_for(p, v, frac):
    """Chiều cao để vật đứng ở p cao đúng frac khung hình (như trong ảnh mẫu)."""
    lo, hi = 0.005, 30.0
    for _ in range(40):
        m = (lo + hi) / 2; q = world_to_camera_view(scene, co, p + Vector((0, 0, m)))
        if (v - (1 - q.y)) < frac: lo = m
        else: hi = m
    return (lo + hi) / 2

# ---------- lối đi: một đường uốn từ mép trái, qua người đội mũ, vòng lên trên như ảnh mẫu ----------
def catmull(pts, n=10):
    out = []
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]; p1, p2 = pts[i], pts[i + 1]; p3 = pts[i + 2] if i + 2 < len(pts) else p2
        for s_ in range(n):
            t = s_ / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1]); return out
PATH_UV = [(-0.12, 0.62), (0.0, 0.605), (0.1, 0.59), (0.2, 0.575), (0.3, 0.565), (0.4, 0.55), (0.5, 0.555), (0.6, 0.548),
           (0.67, 0.515), (0.72, 0.465), (0.765, 0.40), (0.785, 0.33), (0.775, 0.25), (0.752, 0.15), (0.738, 0.05), (0.728, -0.08), (0.72, -0.25)]
LINE = catmull([tuple(g(u, v))[:2] for u, v in PATH_UV])
HALF = (g(0.5, 0.55) - g(0.556, 0.55)).length / 2
print('nửa bề rộng lối đi', round(HALF, 3))
def ribbon(name, line, half, z, color, seed):
    rr = random.Random(seed)
    ph = [rr.uniform(0, 6.28) for _ in range(4)]
    me = bpy.data.meshes.new(name); bm = bmesh.new(); left, right = [], []
    for i, (x, y) in enumerate(line):
        a = line[min(i + 1, len(line) - 1)]; b_ = line[max(i - 1, 0)]
        dx, dy = a[0] - b_[0], a[1] - b_[1]; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
        wl = half * (1 + 0.13 * math.sin(i * 0.37 + ph[0]) + 0.05 * math.sin(i * 1.3 + ph[1]))   # mép cắt tay, không đều
        wr = half * (1 + 0.13 * math.sin(i * 0.41 + ph[2]) + 0.05 * math.sin(i * 1.7 + ph[3]))
        left.append(bm.verts.new((x + nx * wl, y + ny * wl, z))); right.append(bm.verts.new((x - nx * wr, y - ny * wr, z)))
    for i in range(len(line) - 1): bm.faces.new((left[i], left[i + 1], right[i + 1], right[i]))
    bm.to_mesh(me); bm.free(); ob = bpy.data.objects.new(name, me)
    pm = bpy.data.materials.new(name); pm.use_nodes = True; nt = pm.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = 1.0
    if 'Sheen Weight' in b.inputs: b.inputs['Sheen Weight'].default_value = 0.7
    rgbn = nt.nodes.new('ShaderNodeRGB'); rgbn.outputs[0].default_value = rgb(PAL[color])
    felt_detail(nt, b, rgbn.outputs[0], 6, 'Fabric028', 'Generated', 0.9, 0.22)
    me.materials.append(pm); coll.objects.link(ob)
ribbon('Mép lối đi', LINE, HALF * 1.16, 0.004, 'pathEdge', 1)
ribbon('Lối đi', LINE, HALF, 0.010, 'path', 2)
def dpath(x, y): return min(math.hypot(x - a, y - b) for a, b in LINE)

# ---------- đá nỉ góc cạnh (khối gập như ảnh mẫu, không phải cục tròn) ----------
_rockm = None
_rockms = {}
def rock_mat(dark=False):
    if dark in _rockms: return _rockms[dark]
    m = bpy.data.materials.new('nỉ đá' + (' tối' if dark else '')); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    geo = nt.nodes.new('ShaderNodeNewGeometry'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(geo.outputs['Normal'], sep.inputs[0])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.5; nz.inputs['Detail'].default_value = 2
    tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    mix = nt.nodes.new('ShaderNodeMath'); mix.operation = 'MULTIPLY_ADD'; mix.inputs[1].default_value = 0.8
    nt.links.new(sep.outputs['Z'], mix.inputs[0]); nt.links.new(nz.outputs['Fac'], mix.inputs[2])
    rp = nt.nodes.new('ShaderNodeValToRGB'); e = rp.color_ramp.elements
    k_ = 0.42 if dark else 1.0
    def dk(h_): c_ = rgb(h_); return [c_[0] * k_, c_[1] * k_, c_[2] * k_, 1]
    e[0].position = 0.25; e[0].color = dk(PAL['rockDark']); e[1].position = 1.15; e[1].color = dk(PAL['rockTop'])
    mid = e.new(0.65); mid.color = dk(PAL['rock'])
    nt.links.new(mix.outputs[0], rp.inputs['Fac'])
    b.inputs['Roughness'].default_value = 1.0
    if 'Sheen Weight' in b.inputs: b.inputs['Sheen Weight'].default_value = 0.7; b.inputs['Sheen Roughness'].default_value = 0.5
    felt_detail(nt, b, rp.outputs['Color'], 1.4, 'Fabric034', 'Object', 0.6, 0.18)
    _rockms[dark] = m; return m
def shard(x, y, h, w=0.55, lean=0.0, dark=False):
    """Một khối đá: bao lồi của vài điểm ngẫu nhiên, cao h, đáy rộng w*h, mặt phẳng gãy góc."""
    bm = bmesh.new(); W = h * w * random.uniform(0.85, 1.2); D = W * random.uniform(0.6, 0.9)
    pts = []   # điểm trên nửa khối elip: ra khối vòm gãy mặt như nỉ gấp, không nhọn như pha lê
    for i in range(8):
        t = i / 8 * 6.283 + random.uniform(-0.25, 0.25); pts.append((math.cos(t) * W * random.uniform(0.8, 1), math.sin(t) * D * random.uniform(0.8, 1), 0))
    for i in range(7):
        t = random.uniform(0, 6.283); ph = random.uniform(0.3, 1.25); z = h * math.sin(ph)
        pts.append((math.cos(ph) * math.cos(t) * W * random.uniform(0.85, 1.05) + lean * z, math.cos(ph) * math.sin(t) * D, z))
    pts.append((lean * h + random.uniform(-0.1, 0.1) * W, 0, h))
    vs = [bm.verts.new(p) for p in pts]
    res = bmesh.ops.convex_hull(bm, input=vs)
    dead = {g_ for g_ in res['geom_interior'] + res['geom_unused'] if isinstance(g_, bmesh.types.BMVert)}
    if dead: bmesh.ops.delete(bm, geom=list(dead), context='VERTS')
    me = bpy.data.meshes.new('đá'); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('Đá nỉ', me); me.materials.append(rock_mat(dark))
    ob.location = (x, y, -0.02); ob.rotation_euler.z = random.uniform(-0.5, 0.5); coll.objects.link(ob)
    bev = ob.modifiers.new('mép nỉ', 'BEVEL'); bev.width = h * 0.012; bev.segments = 2; bev.limit_method = 'ANGLE'
    return ob

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

# ---------- người nhỏ đội mũ rơm, đeo ba lô ----------
def hiker(x, y, h):
    root = bpy.data.objects.new('Người đội mũ rơm', None); root.location = (x, y, 0); root.scale = (h, h, h); root.rotation_euler.z = math.radians(-8); coll.objects.link(root)
    def put(o, m):
        o.data.materials.append(m); _mv(o); o.parent = root
        for f in o.data.polygons: f.use_smooth = True
    for sx in (-0.07, 0.07):
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.055, depth=0.42, location=(sx, 0, 0.21)); put(bpy.context.active_object, felt('pants'))
        bpy.ops.mesh.primitive_cube_add(size=1, location=(sx, -0.03, 0.025)); s = bpy.context.active_object; s.scale = (0.1, 0.16, 0.05); put(s, felt('boot'))
    bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=0.14, depth=0.34, location=(0, 0, 0.58)); t = bpy.context.active_object; t.scale.y = 0.75; put(t, felt('shirt'))
    for sx in (-0.17, 0.17):
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.04, depth=0.3, location=(sx, 0, 0.58), rotation=(0, math.radians(8 if sx > 0 else -8), 0)); put(bpy.context.active_object, felt('shirt'))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0, 0.14, 0.6)); bp = bpy.context.active_object; bp.scale = (0.24, 0.14, 0.3); put(bp, felt('pack'))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=8, radius=0.085, location=(0, 0, 0.84)); put(bpy.context.active_object, felt('skin'))
    bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=0.26, depth=0.025, location=(0, 0, 0.9), rotation=(math.radians(-10), 0, 0)); put(bpy.context.active_object, felt('hat'))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.11, location=(0, 0.01, 0.93)); c = bpy.context.active_object; c.scale.z = 0.75; put(c, felt('hat'))
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.112, depth=0.025, location=(0, 0.01, 0.925)); put(bpy.context.active_object, felt('band'))
    return root

# ---------- xếp vật theo ảnh mẫu: (loại, u, v, cao bằng bao nhiêu khung hình) ----------
taken = []
def place(kind, u, v, frac, rot=None, cross=None, mirror=None):
    p = g(u, v); h = h_for(p, v, frac)
    if kind == 'rock': shard(p.x, p.y, h, w=random.uniform(0.36, 0.5), lean=random.choice([-1, 1]) * random.uniform(0.18, 0.4), dark=v > 0.85)
    elif kind == 'lump': shard(p.x, p.y, h, w=1.0, lean=random.uniform(-0.2, 0.2), dark=True)
    elif kind == 'hiker': hiker(p.x, p.y, h)
    else:
        if cross is None: cross = False
        r = add_art(kind, p.x, p.y, h, rot=rot, cross=cross)
        if mirror is not None: r.scale.x = abs(r.scale.x) * (-1 if mirror else 1)
    taken.append((p.x, p.y, max(0.15, h * (0.35 if kind not in ('grass',) else 0.15))))
    return p, h

LAYOUT = [
    # cụm đá lớn giữa phía trên
    ('rock', 0.50, 0.40, 0.144), ('rock', 0.565, 0.385, 0.194), ('rock', 0.455, 0.30, 0.122), ('rock', 0.60, 0.33, 0.216),
    ('rock', 0.53, 0.25, 0.202), ('rock', 0.645, 0.25, 0.187), ('rock', 0.575, 0.16, 0.230), ('rock', 0.49, 0.14, 0.173),
    ('rock', 0.665, 0.12, 0.194), ('rock', 0.61, 0.06, 0.202), ('rock', 0.445, 0.20, 0.108), ('rock', 0.70, 0.20, 0.130),
    ('rock', 0.40, 0.07, 0.130), ('rock', 0.53, 0.04, 0.158), ('rock', 0.68, 0.03, 0.144),
    # đá nhỏ dẹt rải rác
    ('lump', 0.31, 0.705, 0.045), ('lump', 0.37, 0.695, 0.04), ('lump', 0.665, 0.335, 0.05), ('lump', 0.71, 0.485, 0.05),
    ('lump', 0.885, 0.79, 0.055), ('lump', 0.935, 0.405, 0.03), ('lump', 0.045, 0.46, 0.04), ('lump', 0.655, 0.735, 0.045),
    ('lump', 0.25, 0.77, 0.035), ('lump', 0.13, 0.80, 0.05), ('lump', 0.95, 0.80, 0.05),
    # đá lớn sát camera (sẽ nhoè)
    ('rock', 0.18, 1.06, 0.30), ('rock', 0.30, 1.08, 0.22), ('rock', 0.64, 1.07, 0.24), ('rock', 0.92, 1.03, 0.26), ('rock', 0.80, 1.06, 0.2),
    ('rock', 0.14, 0.90, 0.16),
    # thông
    ('pine', 0.40, 0.355, 0.30), ('pine', 0.225, 0.185, 0.19), ('pine', 0.125, 0.12, 0.11), ('pine', 0.42, 0.91, 0.30),
    ('pine', 0.665, 0.80, 0.27), ('pine', 0.725, 0.96, 0.25), ('pine', 0.03, 0.97, 0.40), ('pine', 0.985, 0.70, 0.22),
    ('pine', 0.83, 0.03, 0.10),
    # cây lá vàng, cây tròn, lá lửa
    ('round', 0.09, 0.485, 0.17), ('round', 0.29, 0.55, 0.15), ('yellow', 0.62, 0.50, 0.23), ('yellow', 0.835, 0.72, 0.24),
    ('flame', 0.90, 0.71, 0.14), ('yellow', 0.975, 0.41, 0.18), ('yellow', 0.77, 0.06, 0.10),
    ('flame', 0.065, 0.325, 0.10), ('flame', 0.105, 0.33, 0.08), ('flame', 0.255, 0.41, 0.16), ('flame', 0.305, 0.28, 0.08),
    ('flame', 0.355, 0.40, 0.10), ('flame', 0.02, 0.22, 0.08),
    # nấm đỏ lớn phía trên trái và nấm nhỏ
    ('mushrooms', 0.30, 0.17, 0.17), ('mushrooms', 0.255, 0.11, 0.12), ('mushrooms', 0.20, 0.385, 0.05),
    # bụi vòm xanh viền cam/vàng
    ('shrub', 0.17, 0.645, 0.098), ('shrub', 0.50, 0.71, 0.078), ('shrub', 0.75, 0.29, 0.065), ('shrubY', 0.85, 0.125, 0.046),
    ('shrubY', 0.08, 0.50, 0.065), ('shrub', 0.03, 0.49, 0.052), ('shrubY', 0.315, 0.30, 0.039),
    # bụi hoa và bụi lá thấp
    ('flowerBush', 0.17, 0.725, 0.045), ('flowerBush', 0.235, 0.72, 0.04), ('flowerBush', 0.60, 0.715, 0.045),
    ('flowerBush', 0.95, 0.645, 0.045), ('flowerBush', 0.875, 0.355, 0.04), ('flowerBush', 0.345, 0.48, 0.04),
    ('flowerBush', 0.44, 0.485, 0.04), ('flowerBush', 0.515, 0.49, 0.04), ('shrubDark', 0.555, 0.835, 0.08),
    ('flowerBush', 0.90, 0.92, 0.05), ('flowerBush', 0.06, 0.66, 0.04),
    ('fern', 0.37, 0.825, 0.06), ('fern', 0.33, 0.83, 0.045), ('fern', 0.62, 0.62, 0.035), ('fern', 0.10, 0.70, 0.035),
    # cáo
    ('foxWalk', 0.155, 0.27, 0.05), ('foxWalk', 0.355, 0.245, 0.045), ('foxSit', 0.47, 0.425, 0.07), ('foxSit', 0.225, 0.465, 0.055),
    ('foxSit', 0.91, 0.13, 0.04), ('foxSit', 0.965, 0.15, 0.04),
    # cột đèn có biển chỉ đường, người đội mũ rơm
    ('lanternArt', 0.845, 0.36, 0.17), ('logArt', 0.035, 0.585, 0.05),
    ('hiker', 0.585, 0.61, 0.115),
    ('shrub', 0.62, 0.02, 0.065), ('shrubY', 0.86, 0.06, 0.046), ('flowerBush', 0.66, 0.045, 0.03), ('shrub', 0.93, 0.03, 0.052),
    ('round', 0.95, 0.10, 0.09), ('flowerBush', 0.80, 0.21, 0.035), ('shrubY', 0.92, 0.25, 0.052), ('flowerBush', 0.70, 0.40, 0.035),
    ('fern', 0.16, 0.20, 0.05), ('shrubY', 0.05, 0.10, 0.052), ('flowerBush', 0.42, 0.62, 0.035), ('fern', 0.27, 0.62, 0.04),
]
for kind, u, v, frac in LAYOUT:
    place(kind, u, v, frac, mirror=(False if kind in ('foxSit', 'foxWalk') and u < 0.5 else None))

# cỏ và đá vụn lấp chỗ trống, thưa như ảnh mẫu
def free(x, y, r, gap):
    if dpath(x, y) < HALF * 1.2 + gap: return False
    return all(math.hypot(x - a, y - b) > r + rb for a, b, rb in taken)
for i in range(380):
    u, v = random.uniform(-0.05, 1.05), random.uniform(0.0, 1.1)
    p = g(u, v); r = random.random()
    if r < 0.35:
        h = h_for(p, v, random.uniform(0.025, 0.04))
        if free(p.x, p.y, h * 0.6, 0.05): add_art('grass', p.x, p.y, h); taken.append((p.x, p.y, h * 0.6))
    elif r < 0.65:
        h = h_for(p, v, random.uniform(0.015, 0.03))
        if free(p.x, p.y, h, 0.05): shard(p.x, p.y, h, w=1.4, dark=True); taken.append((p.x, p.y, h))
    elif r < 0.72:
        h = h_for(p, v, random.uniform(0.03, 0.045))
        if free(p.x, p.y, h, 0.1): add_art('flowerBush', p.x, p.y, h); taken.append((p.x, p.y, h))

# ---------- ánh sáng mềm, nét ở người đội mũ, nhoè trên và dưới ----------
world = bpy.data.worlds.new('Trời'); scene.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = rgb('#C8CDB4'); world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.4
sun = bpy.data.lights.new('Nắng', 'SUN'); sun.energy = 3.2; sun.angle = math.radians(18); sun.color = (1.0, 0.92, 0.78)
so = bpy.data.objects.new('Nắng', sun); so.rotation_euler = (math.radians(40), math.radians(-14), math.radians(-35)); scene.collection.objects.link(so)
focus = bpy.data.objects.new('Điểm nét', None); focus.location = g(0.55, 0.50) + Vector((0, 0, 0.3)); scene.collection.objects.link(focus)
cam.dof.focus_object = focus

scene.render.engine = 'CYCLES'
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'METAL'; prefs.get_devices()
    for dv in prefs.devices: dv.use = True
    scene.cycles.device = 'GPU'
except Exception as e:
    print('GPU không bật được, dùng CPU:', e)
scene.cycles.samples = SAMPLES; scene.cycles.use_denoising = True
scene.view_settings.view_transform = 'Standard'; scene.view_settings.exposure = arg('--exposure', 0.0)
scene.render.filepath = OUT_PNG
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'forest.blend'))
bpy.ops.render.render(write_still=True)
print('XONG', OUT_PNG)
