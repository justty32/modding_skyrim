"""BodySlide 滑桿模型與帶界限最小平方（stdlib-only、唯讀）。給 bodyslide_fit.py 用。

模型（BodySlide 建置的線性疊加）：
  pos[shape][i] = base[shape][i] + sum_k x_k * diff_k[shape][i]
  x_k = value_k / 100；invert 滑桿 x_k = 1 - value_k / 100；uv 滑桿只動 UV、zap 滑桿刪頂點，都不進擬合。
  _0.nif 用 small 值、_1.nif 用 big 值，兩組各自獨立。

格式依據（只讀、不 import）：
- OSD：BodySlide-and-Outfit-Studio src/files/OSDataFile.cpp `OSDataFile::Read`——u32 magic
  0x4F534400（bytes `\\0DSO`）、u32 version、u32 資料數；每筆 u8 名長＋名、u16 筆數、每筆 u16 index＋3×f32。
- OSP：`<SliderSet>` 的 DataFolder／SourceFile／`<Shape target=..>NIF shape 名</Shape>`（可帶 DataFolder）、
  `<Slider name invert small big uv zap>` 下的 `<Data name target local>檔.osd\\資料名</Data>`。
- invert：BodySlide `SliderSet` 的 bInvert，建置時以 1-v 套用。
"""
from __future__ import annotations

import math
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

import bodyslide_mesh_check as mc

OSD_MAGIC = 0x4F534400


class ModelError(Exception):
    pass


def read_osd(path: Path) -> dict:
    """{資料名: {vertex index: (dx, dy, dz)}}。"""
    d = Path(path).read_bytes()
    if len(d) < 12:
        raise ModelError(f'{path}: too short for OSD')
    magic, _ver, n = struct.unpack_from('<III', d, 0)
    if magic != OSD_MAGIC:
        raise ModelError(f'{path}: bad OSD magic 0x{magic:08X}')
    p, out = 12, {}
    for _ in range(n):
        ln = d[p]
        name = d[p + 1:p + 1 + ln].decode('latin-1')
        p += 1 + ln
        (cnt,) = struct.unpack_from('<H', d, p)
        p += 2
        diff = {}
        for idx, x, y, z in struct.iter_unpack('<H3f', d[p:p + 14 * cnt]):
            diff[idx] = (x, y, z)
        p += 14 * cnt
        out[name] = diff
    if p != len(d):
        raise ModelError(f'{path}: {len(d) - p} trailing bytes')
    return out


def write_osd(path: Path, data: dict) -> None:
    """測試與工具用：{資料名: {index: (dx,dy,dz)}} → OSD。"""
    out = bytearray(struct.pack('<III', OSD_MAGIC, 1, len(data)))
    for name, diff in data.items():
        nb = name.encode('latin-1')
        out += bytes([len(nb)]) + nb + struct.pack('<H', len(diff))
        for idx, v in sorted(diff.items()):
            out += struct.pack('<H3f', idx, *v)
    Path(path).write_bytes(bytes(out))


def _ci(root: Path, rel: str) -> Path:
    """大小寫不敏感解析（ShapeData 在 Linux 上大小寫混雜）。"""
    cur = Path(root)
    for part in rel.replace('\\', '/').split('/'):
        if not part:
            continue
        hit = cur / part
        if not hit.exists() and cur.is_dir():
            low = part.casefold()
            hit = next((c for c in cur.iterdir() if c.name.casefold() == low), hit)
        cur = hit
    return cur


def find_slider_set(osp: Path, set_name: str) -> ET.Element:
    for ss in ET.parse(osp).getroot().iter('SliderSet'):
        if ss.get('name') == set_name:
            return ss
    raise ModelError(f'{osp}: no SliderSet {set_name!r}')


def load_model(osp: Path, set_name: str, shapedata: Path) -> dict:
    """讀 OSP 的一個 SliderSet＋其 ShapeData，回傳模型。"""
    ss = find_slider_set(osp, set_name)
    folder = (ss.findtext('DataFolder') or '').strip()
    source = (ss.findtext('SourceFile') or '').strip()
    targets = {}
    for sh in ss.iter('Shape'):
        targets[sh.get('target')] = {'shape': (sh.text or '').strip(), 'folder': sh.get('DataFolder') or folder}
    base_nif = _ci(shapedata, f'{folder}/{source}')
    if not base_nif.is_file():
        raise ModelError(f'base NIF not found: {base_nif}')
    rep, pos = mc.parse_nif(base_nif)
    shapes = {t['shape']: [tuple(v) for v in pos[t['shape']]] for t in targets.values() if t['shape'] in pos}
    if not shapes:
        raise ModelError(f'{base_nif}: none of the set shapes {sorted(t["shape"] for t in targets.values())} found')
    osd_cache, sliders, skipped = {}, [], []
    for sl in ss.iter('Slider'):
        name = sl.get('name')
        kind = 'uv' if sl.get('uv') == 'true' else 'zap' if sl.get('zap') == 'true' else 'pos'
        entry = {'name': name, 'invert': sl.get('invert') == 'true', 'kind': kind,
                 'small': float(sl.get('small') or 0), 'big': float(sl.get('big') or 0), 'diffs': {}}
        for dd in sl.iter('Data'):
            tgt = targets.get(dd.get('target'))
            if tgt is None or tgt['shape'] not in shapes:
                continue
            text = (dd.text or '').strip()
            if dd.get('local') != 'true' or '\\' not in text and '/' not in text:
                skipped.append(f'{name}/{dd.get("name")}: non-local data not supported')
                continue
            fname, dname = text.replace('/', '\\').rsplit('\\', 1)
            fpath = _ci(shapedata, f'{tgt["folder"]}/{fname}')
            if fpath not in osd_cache:
                if not fpath.is_file():
                    raise ModelError(f'OSD not found: {fpath}')
                osd_cache[fpath] = read_osd(fpath)
            diff = osd_cache[fpath].get(dname)
            if diff is None:
                skipped.append(f'{name}/{dname}: not in {fpath.name}')
                continue
            n = len(shapes[tgt['shape']])
            entry['diffs'][tgt['shape']] = {i: v for i, v in diff.items() if i < n}
        sliders.append(entry)
    return {'osp': str(osp), 'set': set_name, 'base_nif': str(base_nif), 'base_sha256': rep['sha256'],
            'shapes': shapes, 'sliders': sliders, 'skipped': skipped}


def fit_vars(model: dict) -> list:
    """參與擬合的滑桿：位置類、且在模型 shape 上有非零 diff。"""
    return [s for s in model['sliders'] if s['kind'] == 'pos'
            and any(any(c for v in d.values() for c in v) for d in s['diffs'].values())]


def to_x(s: dict, value: float) -> float:
    return 1.0 - value / 100.0 if s['invert'] else value / 100.0


def to_value(s: dict, x: float) -> float:
    return 100.0 * (1.0 - x) if s['invert'] else 100.0 * x


def apply_values(model: dict, values: dict, size: str) -> dict:
    """values {slider: value}（缺的用 OSP 預設）→ {shape: positions}。"""
    out = {k: [list(v) for v in pos] for k, pos in model['shapes'].items()}
    for s in model['sliders']:
        if s['kind'] != 'pos':
            continue
        x = to_x(s, values.get(s['name'], s[size]))
        if x == 0:
            continue
        for shape, diff in s['diffs'].items():
            tgt = out[shape]
            for i, (dx, dy, dz) in diff.items():
                p = tgt[i]
                p[0] += x * dx
                p[1] += x * dy
                p[2] += x * dz
    return {k: [tuple(v) for v in pos] for k, pos in out.items()}


def normal_matrix(model: dict, vars_: list) -> list:
    """A[k][l] = sum_v diff_k(v)·diff_l(v)（逐頂點累加，只走非零項）。"""
    n = len(vars_)
    A = [[0.0] * n for _ in range(n)]
    for shape in model['shapes']:
        per_v = {}
        for k, s in enumerate(vars_):
            for i, v in s['diffs'].get(shape, {}).items():
                per_v.setdefault(i, []).append((k, v))
        for lst in per_v.values():
            for a in range(len(lst)):
                ka, (ax, ay, az) = lst[a]
                row = A[ka]
                for b in range(a, len(lst)):
                    kb, (bx, by, bz) = lst[b]
                    row[kb] += ax * bx + ay * by + az * bz
    for a in range(n):
        for b in range(a + 1, n):
            A[b][a] = A[a][b]
    return A


def rhs(model: dict, vars_: list, residual: dict) -> list:
    """b_k = sum_v diff_k(v)·r(v)；residual {shape: [(rx,ry,rz)]}。"""
    out = []
    for s in vars_:
        acc = 0.0
        for shape, diff in s['diffs'].items():
            r = residual[shape]
            for i, (dx, dy, dz) in diff.items():
                rx, ry, rz = r[i]
                acc += dx * rx + dy * ry + dz * rz
        out.append(acc)
    return out


def cholesky_solve(M: list, y: list) -> list:
    n = len(y)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        Li = L[i]
        for j in range(i + 1):
            Lj = L[j]
            s = M[i][j] - sum(Li[k] * Lj[k] for k in range(j))
            if i == j:
                if s <= 0:
                    raise ModelError('normal matrix not positive definite (raise ridge)')
                Li[i] = math.sqrt(s)
            else:
                Li[j] = s / Lj[j]
    z = [0.0] * n
    for i in range(n):
        z[i] = (y[i] - sum(L[i][k] * z[k] for k in range(i))) / L[i][i]
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (z[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]
    return x


def solve_box(A: list, b: list, lo: list, hi: list, ridge: float, max_iter: int | None = None) -> tuple:
    """min 0.5 x'(A+λI)x - b'x，lo<=x<=hi；primal active set（從 x=clamp(0) 可行點出發）。

    回傳 (x, info)。λ = ridge × mean(diag A)，只用來打破共線滑桿的不定性（偏向 x=0＝不動）。"""
    n = len(b)
    if n == 0:
        return [], {'iterations': 0, 'lambda': 0.0, 'at_bound': []}
    lam = ridge * (sum(A[i][i] for i in range(n)) / n or 1.0)
    M = [row[:] for row in A]
    for i in range(n):
        M[i][i] += lam
    x = [min(max(0.0, lo[i]), hi[i]) for i in range(n)]
    fixed = {i for i in range(n) if x[i] != 0.0}
    it = 0
    for it in range(1, (max_iter or 6 * n + 20) + 1):
        free = [i for i in range(n) if i not in fixed]
        if free:
            r = [b[i] - sum(M[i][j] * x[j] for j in fixed) for i in free]
            y = cholesky_solve([[M[i][j] for j in free] for i in free], r)
            alpha, block = 1.0, []
            for k, i in enumerate(free):
                step = y[k] - x[i]
                if y[k] < lo[i] - 1e-12 and step < 0:
                    a = (lo[i] - x[i]) / step
                elif y[k] > hi[i] + 1e-12 and step > 0:
                    a = (hi[i] - x[i]) / step
                else:
                    continue
                if a < alpha - 1e-15:
                    alpha, block = a, [i]
                elif abs(a - alpha) <= 1e-15:
                    block.append(i)
            for k, i in enumerate(free):
                x[i] += alpha * (y[k] - x[i])
            if block:
                for i in block:
                    x[i] = lo[i] if abs(x[i] - lo[i]) <= abs(x[i] - hi[i]) else hi[i]
                    fixed.add(i)
                continue
        g = [sum(M[i][j] * x[j] for j in range(n)) - b[i] for i in range(n)]
        worst, wi = 0.0, None
        for i in fixed:
            if x[i] <= lo[i] and g[i] < -worst:
                worst, wi = -g[i], i
            elif x[i] >= hi[i] and g[i] > worst:
                worst, wi = g[i], i
        if wi is None:
            break
        fixed.discard(wi)
    at_bound = sorted(i for i in fixed if x[i] in (lo[i], hi[i]))
    return x, {'iterations': it, 'lambda': lam, 'at_bound': at_bound}


def match_shapes(model: dict, target: dict) -> tuple[dict, list]:
    """模型 shape → 目標 NIF shape：先同名，再以頂點數唯一對上；回傳 (mapping, problems)。"""
    mapping, problems, used = {}, [], set()
    for name, base in model['shapes'].items():
        if name in target and len(target[name]) == len(base):
            mapping[name] = name
            used.add(name)
    for name, base in model['shapes'].items():
        if name in mapping:
            continue
        cands = [t for t, pos in target.items() if t not in used and len(pos) == len(base)]
        if len(cands) == 1:
            mapping[name] = cands[0]
            used.add(cands[0])
        else:
            counts = {t: len(p) for t, p in target.items()}
            problems.append(f'shape {name!r} ({len(base)} verts): no unique same-count shape in target {counts}')
    return mapping, problems


def percentile(sorted_vals: list, q: float) -> float:
    if not sorted_vals:
        return 0.0
    k = min(len(sorted_vals) - 1, max(0, int(math.ceil(q * len(sorted_vals))) - 1))
    return sorted_vals[k]


REGIONS = (  # (名稱, z 下限比例) 由上往下判；手臂另以 |x| 判
    ('neck_shoulders', 0.80), ('chest', 0.68), ('waist_belly', 0.585), ('hips_butt_groin', 0.48),
    ('thighs', 0.29), ('knees_calves', 0.08), ('feet_ankles', -1.0))


def region_of(p, zmin: float, height: float) -> str:
    zf = (p[2] - zmin) / height if height else 0.0
    if zf > 0.55 and abs(p[0]) > 0.11 * height:
        return 'arms'
    for name, lo in REGIONS:
        if zf >= lo:
            return name
    return 'feet_ankles'


def residual_stats(model: dict, target: dict, mapping: dict, fitted: dict) -> dict:
    """逐頂點距離 |target - fitted|：整體 rms／max／p50／p95／p99，以及大約部位（以基準身高分帶）。"""
    main = max(model['shapes'], key=lambda k: len(model['shapes'][k]))
    zs = [p[2] for p in model['shapes'][main]]
    zmin, height = min(zs), max(zs) - min(zs)
    dists, by_region, worst = [], {}, (0.0, None, None)
    for shape, tshape in mapping.items():
        for i, (t, f) in enumerate(zip(target[tshape], fitted[shape])):
            d = math.sqrt((t[0] - f[0]) ** 2 + (t[1] - f[1]) ** 2 + (t[2] - f[2]) ** 2)
            dists.append(d)
            reg = region_of(model['shapes'][shape][i], zmin, height)
            r = by_region.setdefault(reg, [0, 0.0, 0.0])
            r[0] += 1
            r[1] += d * d
            r[2] = max(r[2], d)
            if d > worst[0]:
                worst = (d, shape, i)
    dists.sort()
    n = len(dists) or 1
    rms = math.sqrt(sum(d * d for d in dists) / n)
    total_sq = sum(d * d for d in dists) or 1.0
    regions = {k: {'verts': v[0], 'rms': round(math.sqrt(v[1] / v[0]), 4), 'max': round(v[2], 4),
                   'share_of_sq_error': round(v[1] / total_sq, 3)} for k, v in sorted(by_region.items())}
    return {'verts': len(dists), 'height': round(height, 3), 'rms': round(rms, 4), 'max': round(dists[-1] if dists else 0, 4),
            'p50': round(percentile(dists, .5), 4), 'p95': round(percentile(dists, .95), 4),
            'p99': round(percentile(dists, .99), 4), 'worst_vertex': {'shape': worst[1], 'index': worst[2]},
            'regions': regions}


def fit_size(model: dict, vars_: list, A: list, target: dict, mapping: dict, bounds: tuple, ridge: float,
             integer: bool = True) -> tuple[dict, dict]:
    """一個尺寸（small 或 big）的擬合；回傳 ({slider: value}, info)。"""
    residual = {}
    for shape, tshape in mapping.items():
        residual[shape] = [(t[0] - b[0], t[1] - b[1], t[2] - b[2])
                           for t, b in zip(target[tshape], model['shapes'][shape])]
    b = rhs(model, vars_, residual)
    vlo, vhi = bounds
    lo = [to_x(s, vhi if s['invert'] else vlo) for s in vars_]
    hi = [to_x(s, vlo if s['invert'] else vhi) for s in vars_]
    x, info = solve_box(A, b, lo, hi, ridge)
    values = {}
    for s, xv in zip(vars_, x):
        v = to_value(s, xv)
        values[s['name']] = float(round(v)) if integer else round(v, 4)
    info['at_bound'] = [vars_[i]['name'] for i in info['at_bound']]
    return values, info


def retarget_bodytri(data: bytes, new_value: str) -> tuple[bytes, str]:
    """NIF 的 BODYTRI 改指 new_value：新字串附加到 header 字串表尾，只改 NiStringExtraData 的 value 索引。

    block 大小不變、其他字串不動（舊字串可能被別處共用）；回傳 (新 bytes, 舊值)。"""
    h = mc.read_nif_header(mc.Reader(data))
    hits = []
    for i, t in enumerate(h['types']):
        if t == 'NiStringExtraData':
            ni, vi = struct.unpack_from('<II', data, h['offsets'][i])
            if mc.string_at(h, ni) == 'BODYTRI':
                hits.append((i, vi))
    if len(hits) != 1:
        raise ModelError(f'expected exactly one BODYTRI NiStringExtraData, found {len(hits)}')
    block, old_idx = hits[0]
    old = h['strings'][old_idx]
    enc = new_value.encode('latin-1')
    so = h['strings_offset']
    n, maxlen = struct.unpack_from('<II', data, so)
    p = so + 8
    for _ in range(n):
        (ln,) = struct.unpack_from('<I', data, p)
        p += 4 + ln
    head = bytearray(data[:so]) + struct.pack('<II', n + 1, max(maxlen, len(enc))) + data[so + 8:p]
    head += struct.pack('<I', len(enc)) + enc
    shift = len(head) - p
    out = bytearray(head) + data[p:]
    struct.pack_into('<I', out, h['offsets'][block] + shift + 4, n)
    return bytes(out), old
