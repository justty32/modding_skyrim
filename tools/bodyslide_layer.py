#!/usr/bin/env python3
"""Verify one BodySlide batch output and turn it into a replaceable MO2 output layer.

Library for bodyslide_rebuild.py. Read only towards the round output; the layer is a new
directory of hardlinks (same disk; falls back to copies) plus meta.ini, so nothing is
duplicated on disk. layer_apply.py later copies the layer into mods/ as real files.

verify_batch():
  * path set: expected NIF/TRI (from bodyslide_select) vs the files actually written;
    missing and extra are both failures, TRI the project may skip (no morphable slider)
    are reported as 'tri_missing' and judged by the caller.
  * samples: per sampled project the NIF parses (bodyslide_mesh_check.parse_nif), carries a
    BODYTRI string naming its .tri, and the .tri parses with in-range indices.
  * body_match: embedded body shapes (CBBE/3BA/BaseShape) against the batch-0 body of the same
    weight, nearest vertex; CBBE-topology bodies built on the base preset sit on it (p95 = 0),
    3BA-reference bodies only partly (extra loops and their own Vanilla slider data).
  * baseline: when reference directories are given (an old output layer built with the same
    base preset, or the live body), the sample's shapes are compared vertex by vertex; equal
    shapes prove the base shape did not change. Shapes absent from the reference are listed.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import shutil

import bodyslide_mesh_check as bmc

TOLERANCE = 1e-4
BODY_SHAPES = ('CBBE', '3BA', 'BaseShape')
BODY_FILES = {'0': 'meshes/actors/character/character assets/femalebody_0.nif',
              '1': 'meshes/actors/character/character assets/femalebody_1.nif'}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def scan(root: Path) -> dict:
    """casefolded rel -> real Path (fails on case collisions, like mesh_check)."""
    return {k: v for k, v in bmc.scan_dir(root).items()} if root.is_dir() else {}


def pick_samples(projects: list, n: int) -> list:
    """Deterministic spread without repeats: one project per OSP first, then the rest by name."""
    if n <= 0 or not projects:
        return []
    seen, first, rest = set(), [], []
    for p in sorted(projects, key=lambda p: (p['osp'], p['name'])):
        (rest if p['osp'] in seen else first).append(p)
        seen.add(p['osp'])
    pool = first + rest
    if len(first) >= n:
        pool = first
    elif len(pool) <= n:
        return pool
    else:
        pool = first + rest[:n - len(first)] if len(first) else rest
        return pool[:n]
    return [pool[int(i * len(pool) / n)] for i in range(n)]


class _Grid:
    """Nearest-neighbour lookup on a 1-unit voxel grid (body meshes are ~13k points)."""

    def __init__(self, pts, h=1.0):
        self.h, self.cells = h, {}
        for q in pts:
            self.cells.setdefault(self._key(q), []).append(q)

    def _key(self, q):
        return tuple(math.floor(c / self.h) for c in q)

    def dist(self, q):
        k, best = self._key(q), math.inf
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for r in self.cells.get((k[0] + dx, k[1] + dy, k[2] + dz), ()):
                        best = min(best, math.dist(q, r))
        return best


_BODY_CACHE: dict = {}


def body_match(nif_rel: str, pos: dict, body_dir: Path | None) -> dict | None:
    """Embedded body shapes vs the built global body of the same weight (nearest vertex)."""
    names = [n for n in pos if n in BODY_SHAPES]
    weight = nif_rel[-5] if nif_rel.endswith(('_0.nif', '_1.nif')) else None
    if not names or body_dir is None or weight is None:
        return None
    key = (str(body_dir), weight)
    if key not in _BODY_CACHE:
        bpos = bmc.parse_nif(Path(body_dir) / BODY_FILES[weight])[1]
        _BODY_CACHE[key] = _Grid([q for v in bpos.values() for q in v])
    grid, out = _BODY_CACHE[key], {}
    for n in names:
        ds = sorted(grid.dist(q) for q in pos[n])
        if ds:
            out[n] = dict(vertices=len(ds), p50=round(ds[len(ds) // 2], 5), p95=round(ds[int(len(ds) * .95)], 5),
                          on_body=round(sum(d <= 1e-3 for d in ds) / len(ds), 3))
    return out


def _shape_diff(pa, pb):
    if len(pa) != len(pb):
        return dict(same_count=False, a=len(pa), b=len(pb))
    d = max((math.dist(x, y) for x, y in zip(pa, pb)), default=0.0)
    return dict(same_count=True, vertices=len(pa), max_distance=round(d, 6), equal=d <= TOLERANCE)


def check_sample(project: dict, files: dict, references: list, body_dir: Path | None = None) -> dict:
    nif_rel = project['outputs'][-1]  # _1.nif (high weight) or the single .nif
    row = dict(project=project['name'], osp=project['osp'], nif=nif_rel, failures=[])
    path = files.get(nif_rel.casefold())
    if path is None:
        row['failures'].append('nif missing')
        return row
    try:
        rep, pos = bmc.parse_nif(path)
    except bmc.FormatError as exc:
        row['failures'].append(f'nif unreadable: {exc}')
        return row
    row['shapes'] = {s['name']: len(pos.get(s['name'], [])) for s in rep['shapes']}
    try:
        match = body_match(nif_rel, pos, body_dir)
    except (bmc.FormatError, OSError) as exc:
        match = dict(error=str(exc))
    if match:
        row['body_match'] = match
    row['bodytri'] = [b['value'] for b in rep['bodytri']]
    if rep['errors'] or rep['unsupported']:
        row['failures'].append(f"nif parse problems: {rep['errors'][:2] + rep['unsupported'][:2]}")
    tri_rel = project.get('tri')
    if tri_rel:
        tri = files.get(tri_rel.casefold())
        if tri is None:
            row['failures'].append('tri missing')
        else:
            want = tri_rel.split('/', 1)[1].replace('/', '\\').casefold()  # BODYTRI is Data\meshes-relative
            if not any(v.replace('/', '\\').casefold().endswith(want) for v in row['bodytri']):
                row['failures'].append(f'BODYTRI {row["bodytri"]} does not name {tri_rel}')
            limits = {k: len(v) for k, v in pos.items()}
            try:
                trep, _ = bmc.parse_tri(tri, limits)
                row['tri_morph_shapes'] = {s['name']: s['morph_count'] for s in trep['position_shapes']}
                fails = [f for f in trep['check_failures'] if 'trailing' not in f]
                if fails:
                    row['failures'].append(f'tri: {fails[:3]}')
            except bmc.FormatError as exc:
                row['failures'].append(f'tri unreadable: {exc}')
    baselines = []
    for rel in project['outputs']:
        for ref in references:
            rpath = scan_cached(ref).get(rel.casefold())
            if rpath is None:
                continue
            try:
                _r, rpos = bmc.parse_nif(rpath)
                npos = pos if rel == nif_rel else bmc.parse_nif(files[rel.casefold()])[1]
            except (bmc.FormatError, KeyError) as exc:
                baselines.append(dict(nif=rel, reference=str(ref), error=str(exc), equal=False))
                break
            diffs = {name: _shape_diff(npos[name], rpos[name]) for name in npos if name in rpos}
            baselines.append(dict(nif=rel, reference=str(ref), shapes=diffs,
                                  only_new=sorted(set(npos) - set(rpos)), only_ref=sorted(set(rpos) - set(npos)),
                                  equal=bool(diffs) and all(d.get('equal') for d in diffs.values())))
            break
    if baselines:
        row['baseline'] = dict(per_nif=baselines, reference=baselines[0]['reference'],
                               equal=all(b['equal'] for b in baselines))
    row['ok'] = not row['failures']
    return row


_SCAN_CACHE: dict = {}


def scan_cached(root: Path) -> dict:
    key = str(root)
    if key not in _SCAN_CACHE:
        _SCAN_CACHE[key] = scan(Path(root))
    return _SCAN_CACHE[key]


def verify_batch(output: Path, selection: dict, samples: int = 5, references: list | None = None,
                 body_dir: Path | None = None) -> dict:
    files = scan(output)
    expected = {p.casefold() for p in selection['expected']}
    expected_tri = {p.casefold() for p in selection['expected_tri']}
    actual = set(files)
    missing = sorted(expected - actual)
    tri_missing = sorted(expected_tri - actual)
    extra = sorted(actual - expected - expected_tri)
    rows = [check_sample(p, files, [Path(r) for r in references or []], body_dir)
            for p in pick_samples(selection['projects'], samples)]
    failures = []
    if missing:
        failures.append(f'{len(missing)} expected NIFs missing')
    if extra:
        failures.append(f'{len(extra)} unexpected files')
    bad = [r['project'] for r in rows if not r['ok']]
    if bad:
        failures.append(f'samples failed: {bad}')
    return dict(ok=not failures, failures=failures, files=len(actual), expected_nif=len(expected),
                expected_tri=len(expected_tri), missing=missing, tri_missing=tri_missing,
                extra=extra, samples=rows)


def _link(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def assemble_layer(output: Path, layer_dir: Path, selection: dict, meta: dict) -> dict:
    """Hardlink the round output into layer_dir, write meta.ini and return the manifest."""
    if layer_dir.exists() and any(layer_dir.iterdir()):
        raise FileExistsError(f'layer directory not empty: {layer_dir}')
    owner = {}
    for p in selection['projects']:
        for rel in p['outputs'] + ([p['tri']] if p['tri'] else []):
            owner[rel.casefold()] = p
    rows, total = [], 0
    for key, src in sorted(scan(output).items()):
        rel = src.relative_to(output).as_posix()
        _link(src, layer_dir / rel)
        size = src.stat().st_size
        total += size
        p = owner.get(key, {})
        rows.append(dict(path=rel, bytes=size, sha256=sha256(src), project=p.get('name'),
                         osp=p.get('osp'), source_mod=p.get('mod')))
    comments = (f"BodySlide rebuild {meta['config']} batch {meta['batch']}: preset {meta['preset']!r}, "
                f"morphs {'on' if meta['morphs'] else 'off'}, {len(rows)} files; manifest.json next to the layer")
    (layer_dir / 'meta.ini').write_text(
        '[General]\ngameName=Skyrim Special Edition\nmodid=0\n'
        f"version={meta['revision']}\ncategory=0\ncomments={comments}\n", encoding='utf-8')
    return dict(schema='bodyslide-layer/1', layer=layer_dir.name, **meta, files=len(rows), bytes=total,
                projects=len(selection['projects']), source_mods=sorted({r['source_mod'] or '?' for r in rows}),
                rows=rows)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding='utf-8')
    tmp.replace(path)
