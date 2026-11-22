#!/usr/bin/env python3
"""Pick the BodySlide projects of one rebuild batch and write its group / BuildSelection XML.

Library for bodyslide_rebuild.py (no CLI of its own). Read only towards the staging.

Catalog: every SliderSet in <tool>/SliderSets/**/*.osp, with the OSP's source mod taken
from the bodyslide_stage.py source table. Parsing is lenient on purpose (duplicate Shape
names are allowed - BodySlide builds them); the strict per-project preflight stays in
bodyslide_outfit_plan.py.

A batch selects *output stems* ('meshes/armor/iron/cuirassf', casefolded, no _0/_1/.nif)
and then exactly one project per stem:
  select.projects        exact project names (must exist exactly once)
  select.osp_mods        every project whose OSP winner mod is listed ('Prefix*' allowed)
  select.stems           explicit stems or mesh paths
  select.stems_from_dirs NIFs found under these directories (a live layer being replaced)
  select.scope           {"table": wf-table from bodyslide_scope_scan.py, "where": {col: [values]}}
Per stem the candidates are all catalog projects writing it. Resolution order:
  choose {stem: project} > drop exclude_projects (regex) > avoid (regex, kept if it would
  empty the set) > prefer rules in order ('mod:<prefix>' or 'project:<regex>'; a rule that
  matches nobody is skipped). More than one left -> unresolved (a human decision).
Upstream semantics of same-output builds and BuildSelection: BodySlideApp.cpp
CommandLineBuild/GetCmdLineBuildOutfits, commit 033016464d31761bfaf6966db3ea9c3c3cb6105a;
local 5.8.2 hangs without a choice (wf/workflows/bodyslide/evidence.md).
"""
from __future__ import annotations

import fnmatch
import json
import os
from pathlib import Path
import re
from xml.sax.saxutils import quoteattr
import xml.etree.ElementTree as ET

NIF_SUFFIX = re.compile(r'(_[01])?\.nif$', re.I)


class SelectError(Exception):
    """Configuration or catalog problem that stops the batch."""


def norm_stem(value: str) -> str:
    """'Meshes\\Armor\\Iron\\CuirassF_1.nif' -> 'meshes/armor/iron/cuirassf'."""
    s = value.replace('\\', '/').strip().strip('/').casefold()
    s = NIF_SUFFIX.sub('', s)
    if s.endswith('.tri'):
        s = s[:-4]
    if not s.startswith('meshes/'):
        s = 'meshes/' + s
    return s


def _bool(value, default):
    if value is None:
        return default
    return value.strip().lower() in ('true', '1')


def load_catalog(tool: Path, stage_table: Path | None = None) -> tuple[list, list]:
    """Return (projects, errors). Each project: name, osp, mod, stem, out_path, outputs, tri, ..."""
    sliders = [p for p in tool.iterdir() if p.name.casefold() == 'slidersets' and p.is_dir()]
    if len(sliders) != 1:
        raise SelectError(f'{tool}: expected exactly one SliderSets directory, found {len(sliders)}')
    winners = {}
    if stage_table is not None:
        for row in json.loads(Path(stage_table).read_text(encoding='utf-8'))['rows']:
            winners[row['staged_rel'].casefold()] = row['winner_mod']
    projects, errors = [], []
    for dirpath, dirnames, filenames in os.walk(sliders[0]):
        dirnames.sort()
        for fname in sorted(filenames):
            if not fname.casefold().endswith('.osp'):
                continue
            path = Path(dirpath, fname)
            rel = path.relative_to(tool).as_posix()
            try:
                root = ET.parse(path).getroot()
            except (ET.ParseError, OSError) as exc:
                errors.append(f'{rel}: {exc}')
                continue
            for el in root:
                if el.tag not in ('SliderSet', 'SliderSetAddOn'):
                    continue
                out = el.find('OutputFile')
                if out is None or not (out.text or '').strip():
                    errors.append(f'{rel}: {el.get("name")!r} has no OutputFile')
                    continue
                out_path = ((el.findtext('OutputPath') or '').strip().strip('\\/') + '\\'
                            + out.text.strip()).lstrip('\\')
                stem = norm_stem(out_path)
                weights = _bool(out.get('GenWeights'), True)
                rel_stem = stem
                outputs = [rel_stem + s for s in (('_0.nif', '_1.nif') if weights else ('.nif',))]
                sliders_el = el.findall('Slider')
                projects.append(dict(
                    name=el.get('name', ''), osp=rel, mod=winners.get(rel.casefold()),
                    stem=stem, out_path=out_path, outputs=outputs,
                    tri=None if _bool(out.get('PreventMorphFile'), False) else rel_stem + '.tri',
                    addon=el.tag != 'SliderSet',
                    shapes=[s.text for s in el.findall('Shape')],
                    sliders=sorted({s.get('name') for s in sliders_el}),
                    zaps=sorted({s.get('name') for s in sliders_el if _bool(s.get('zap'), False)})))
    return projects, errors


def _mod_match(mod, patterns):
    return mod is not None and any(fnmatch.fnmatchcase(mod, p) for p in patterns)


def _layer_stems(dirs):
    stems = set()
    for d in dirs:
        d = Path(d)
        if not d.is_dir():
            raise SelectError(f'stems_from_dirs: not a directory: {d}')
        for dirpath, _dirs, files in os.walk(d):
            for f in files:
                if f.casefold().endswith('.nif'):
                    stems.add(norm_stem(Path(dirpath, f).relative_to(d).as_posix()))
    return stems


def _scope_stems(scope, base: Path):
    table = Path(scope['table'])
    if not table.is_absolute():
        table = base / table
    rows = json.loads(table.read_text(encoding='utf-8'))['rows']
    where = scope.get('where', {})
    out = set()
    for row in rows:
        ok = True
        for col, allowed in where.items():
            vals = str(row.get(col, '')).split('|')
            if not any(_mod_match(v, allowed) for v in vals):
                ok = False
                break
        if ok:
            out.add(norm_stem(row.get('stem') or row['mesh']))
    return out


def _resolve(stem, cands, batch):
    names = {c['name'] for c in cands}
    chosen = batch.get('choose', {}).get(stem)
    if chosen:
        if chosen not in names:
            return None, f'choose: {chosen!r} does not write {stem}'
        return [c for c in cands if c['name'] == chosen], 'choose'
    rule = 'only'
    excl = [re.compile(x) for x in batch.get('exclude_projects', [])]
    cands = [c for c in cands if not any(r.search(c['name']) for r in excl)]
    if not cands:
        return [], 'excluded'
    avoid = [re.compile(x) for x in batch.get('avoid', [])]
    kept = [c for c in cands if not any(r.search(c['name']) for r in avoid)]
    if kept and len(kept) < len(cands):
        cands, rule = kept, 'avoid'
    for pref in batch.get('prefer', []):
        if len(cands) == 1:
            break
        kind, _, value = pref.partition(':')
        if kind == 'mod':
            hit = [c for c in cands if (c['mod'] or '').startswith(value)]
        elif kind == 'project':
            hit = [c for c in cands if re.search(value, c['name'])]
        else:
            raise SelectError(f'prefer rule must be mod:… or project:…, got {pref!r}')
        if hit:
            cands, rule = hit, pref
    return cands, rule


def select_batch(catalog: list, batch: dict, base: Path = Path('.')) -> dict:
    """Resolve one batch. 'base' anchors relative scope tables."""
    by_stem, by_name = {}, {}
    for p in catalog:
        by_stem.setdefault(p['stem'], []).append(p)
        by_name.setdefault(p['name'], []).append(p)
    sel = batch.get('select', {})
    wanted, origin, errors = {}, {}, []
    for name in sel.get('projects', []):
        hits = by_name.get(name, [])
        if len(hits) != 1:
            errors.append(f'project {name!r}: expected exactly one, found {len(hits)}')
            continue
        wanted.setdefault(hits[0]['stem'], set()).add('projects')
        origin.setdefault(hits[0]['stem'], name)
    if sel.get('osp_mods'):
        for p in catalog:
            if _mod_match(p['mod'], sel['osp_mods']):
                wanted.setdefault(p['stem'], set()).add('osp_mods')
    for s in sel.get('stems', []):
        wanted.setdefault(norm_stem(s), set()).add('stems')
    if sel.get('stems_from_dirs'):
        for s in _layer_stems(sel['stems_from_dirs']):
            wanted.setdefault(s, set()).add('replaced_layer')
    if sel.get('scope'):
        for s in _scope_stems(sel['scope'], base):
            wanted.setdefault(s, set()).add('scope')
    for s in batch.get('exclude_stems', []):
        wanted.pop(norm_stem(s), None)
    chosen, decisions, unresolved, uncovered = [], [], [], []
    for stem in sorted(wanted):
        cands = by_stem.get(stem, [])
        if origin.get(stem):
            cands = [c for c in cands if c['name'] == origin[stem]] or cands
        if not cands:
            uncovered.append(dict(stem=stem, via=sorted(wanted[stem])))
            continue
        picked, rule = _resolve(stem, cands, batch)
        if picked is None:
            errors.append(rule)
            continue
        row = dict(stem=stem, via=sorted(wanted[stem]), rule=rule,
                   candidates=sorted(f"{c['name']} <{c['mod']}>" for c in by_stem[stem]))
        if len(picked) == 1:
            row['project'] = picked[0]['name']
            chosen.append(picked[0])
        elif picked:
            row['left'] = sorted(c['name'] for c in picked)
            unresolved.append(row)
        else:
            row['project'] = None
        decisions.append(row)
    names = [p['name'] for p in chosen]
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        errors.append(f'project chosen for several stems: {dupes}')
    # Layer replacement must keep full coverage, otherwise disabling the old layer loses files.
    lost = [u for u in uncovered if 'replaced_layer' in u['via']]
    if lost:
        errors.append(f'{len(lost)} stems of the replaced layer have no project')
    return dict(projects=chosen, decisions=decisions, unresolved=unresolved,
                uncovered=uncovered, errors=errors,
                expected=sorted({o for p in chosen for o in p['outputs']}),
                expected_tri=sorted({p['tri'] for p in chosen if p['tri']}))


def group_xml(group: str, names: list) -> str:
    members = ''.join(f'    <Member name={quoteattr(n)}/>\n' for n in names)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<SliderGroups>\n  <Group name={quoteattr(group)}>\n{members}  </Group>\n</SliderGroups>\n'


def build_selection_xml(projects: list, zaps: dict | None = None) -> str:
    """OutputChoice per chosen project (exact OSP output string) and optional ZapChoice."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<BuildSelection>']
    for p in sorted(projects, key=lambda p: p['out_path'].casefold()):
        lines.append(f'  <OutputChoice path={quoteattr(p["out_path"])} choice={quoteattr(p["name"])}/>')
    for project, sliders in sorted((zaps or {}).items()):
        for zap, on in sorted(sliders.items()):
            lines.append(f'  <ZapChoice project={quoteattr(project)} zap={quoteattr(zap)} '
                         f'choice="{"true" if on else "false"}"/>')
    lines.append('</BuildSelection>')
    return '\n'.join(lines) + '\n'
