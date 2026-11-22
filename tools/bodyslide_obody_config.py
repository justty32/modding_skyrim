#!/usr/bin/env python3
"""Generate an OBody NG override layer (distribution JSON + presets) from the rebuild config's `obody` section.

Read only towards the inputs; writes only below --out (a new layer directory):
  <out>/SKSE/Plugins/OBody_presetDistributionConfig.json
  <out>/CalienteTools/BodySlide/SliderPresets/<presets_file>   (neutral + delta presets)
and prints a JSON report. Exit 0 ok, 1 validation failed (nothing written), 2 bad input.

The `obody` section (inside a bodyslide-rebuild/1 config, or a standalone JSON file):
  base_config   current winning OBody_presetDistributionConfig.json (copied, then edited)
  schema        OBody_presetDistributionConfig_schema.json (validated against; subset of JSON Schema)
  presets_dirs  SliderPresets directories whose presets OBody will load (to list names)
  presets_file  file name for generated presets (default BSO-OBody-Presets.xml)
  neutral       {"name", "set", "sliders"?} or a list of them: zero presets that stay in the random
                pool (one per sex). "sliders" names the slider(s) written as 0 (default Breasts);
                a male neutral needs a slider of its own body, e.g. a HIMBO slider.
  random_pool   preset names left eligible for random distribution; every other loaded or
                generated preset is added to blacklistedPresetsFromRandomDistribution.
                OBody 4.4.3 splits presets by sex on the preset's set (IsFemalePreset: a set
                containing himbo/talos/sam/sos/savren is male) and returns before any per-NPC
                lookup when that sex's random pool is empty (Body.cpp GenerateActorBody), which
                also leaves old morphs on those actors. So the female pool may not be empty, and
                the male pool may not be empty once any male preset is loaded or generated.
  deltas        [{"name", "set", "target", "base", "osp"?}]: target preset minus base preset,
                slider by slider and per size (small/big); a slider absent from one side uses
                the OSP default from "osp" (else 0). Negative values are kept: OBody does not
                clamp (PresetManager.cpp SliderSetFromNode, value/100).
  assign        {"Plugin.esp": {"FormID": ["Preset"]}} -> npcFormID (merged)
  unblacklist   {"Plugin.esp": ["FormID"]} removed from blacklistedNpcsFormID; required for every
                assigned NPC because the blacklist is checked first (Body.cpp).
  npc_presets   the per-NPC table: [{"plugin", "formid", "preset", "sex"?, "note"}]. Each distinct preset P
                becomes a delta 'BSO P (morph)' = P - base_preset (needs base_preset; optional osp,
                delta_set), assigned to the NPC, and the NPC is removed from blacklistedNpcsFormID.
                Rows with "sex": "male" use the "male" section instead.
  male          {"base_preset", "osp"?, "delta_set"?}: base for male rows (the preset the male body
                and male equipment were built with, e.g. "HIMBO Zero for OBody").
Preset names and file names must avoid OBody's clothed-set words (IsClothedSet:
cloth outfit nevernude bikini feet hands push cleavage armor) or OBody skips them.
Source: Aietos/OBody-NG commit e33bbc1 (the 4.4.3 bump).
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import sys
from xml.sax.saxutils import quoteattr
import xml.etree.ElementTree as ET

CLOTHED = ('cloth', 'outfit', 'nevernude', 'bikini', 'feet', 'hands', 'push', 'cleavage', 'armor')
MALE_BODY = ('himbo', 'talos', 'sam', 'sos', 'savren')


def is_male_set(body_set: str) -> bool:
    """OBody's IsFemalePreset, inverted: substring match on the preset's set."""
    return any(w in (body_set or '').casefold() for w in MALE_BODY)


class InputError(Exception):
    pass


def read_presets(path: Path) -> dict:
    """{name: {'set': str, 'sliders': {(slider, size): value}}} from one SliderPresets XML."""
    out = {}
    root = ET.parse(path).getroot()
    for p in root.iter('Preset'):
        sliders = {}
        for s in p.iter('SetSlider'):
            sliders[(s.get('name'), s.get('size') or 'small')] = float(s.get('value', '0'))
        out[p.get('name')] = {'set': p.get('set', ''), 'sliders': sliders, 'file': path.name}
    return out


def load_presets(dirs) -> dict:
    """Like OBody: top-level *.xml only, clothed file names skipped."""
    found = {}
    for d in dirs:
        for f in sorted(Path(d).glob('*.xml')):
            if any(w in f.name.casefold() for w in CLOTHED):  # OBody sees Data\CalienteTools\...\<name>
                continue
            try:
                for name, p in read_presets(f).items():
                    if not any(w in name.casefold() for w in CLOTHED):
                        found.setdefault(name, p)
            except ET.ParseError:
                continue
    return found


def osp_defaults(osp: Path | None) -> dict:
    if osp is None:
        return {}
    out = {}
    for s in ET.parse(osp).getroot().iter('Slider'):
        for size in ('small', 'big'):
            if s.get(size) is not None:
                out[(s.get('name'), size)] = float(s.get(size))
    return out


def delta_sliders(target: dict, base: dict, defaults: dict) -> dict:
    keys = set(target) | set(base)
    out = {}
    for key in sorted(keys):
        t = target.get(key, defaults.get(key, 0.0))
        b = base.get(key, defaults.get(key, 0.0))
        if round(t - b, 4) != 0:
            out[key] = round(t - b, 4)
    return out


def preset_xml(presets: list) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<SliderPresets>']
    for p in presets:
        lines.append(f'    <Preset name={quoteattr(p["name"])} set={quoteattr(p["set"])}>')
        for (slider, size), value in sorted(p['sliders'].items()):
            v = int(value) if float(value).is_integer() else value
            lines.append(f'        <SetSlider name={quoteattr(slider)} size="{size}" value="{v}"/>')
        lines.append('    </Preset>')
    lines.append('</SliderPresets>')
    return '\n'.join(lines) + '\n'


def validate(doc, schema, node=None, path='$') -> list:
    """JSON Schema subset used by OBody's schema: $ref, type, properties, additionalProperties,
    propertyNames, items, pattern, enum, minLength."""
    node = schema if node is None else node
    if '$ref' in node:
        ref = node['$ref']
        if not ref.startswith('#/'):
            return [f'{path}: unsupported $ref {ref}']
        target = schema
        for part in ref[2:].split('/'):
            target = target[part]
        return validate(doc, schema, target, path)
    errs = []
    types = node.get('type')
    if types:
        names = types if isinstance(types, list) else [types]
        pyt = {'object': dict, 'array': list, 'string': str, 'boolean': bool, 'number': (int, float),
               'integer': int, 'null': type(None)}
        if not any(isinstance(doc, pyt[t]) for t in names):
            return [f'{path}: expected {types}']
    if isinstance(doc, str):
        if 'pattern' in node and not re.search(node['pattern'], doc):
            errs.append(f'{path}: {doc!r} does not match {node["pattern"]}')
        if len(doc) < node.get('minLength', 0):
            errs.append(f'{path}: too short')
    if 'enum' in node and doc not in node['enum']:
        errs.append(f'{path}: not in enum')
    if isinstance(doc, dict):
        props = node.get('properties', {})
        for k, v in doc.items():
            if 'propertyNames' in node:
                errs += validate(k, schema, node['propertyNames'], f'{path}.<key {k!r}>')
            if k in props:
                errs += validate(v, schema, props[k], f'{path}.{k}')
            elif node.get('additionalProperties') is False:
                errs.append(f'{path}: unexpected key {k!r}')
            elif isinstance(node.get('additionalProperties'), dict):
                errs += validate(v, schema, node['additionalProperties'], f'{path}.{k}')
    if isinstance(doc, list) and 'items' in node:
        for i, v in enumerate(doc):
            errs += validate(v, schema, node['items'], f'{path}[{i}]')
    return errs


def delta_name(preset: str, prefix: str = 'BSO') -> str:
    """Delta preset name for an assigned preset; clothed-set words are masked so OBody loads it."""
    name = f'{prefix} {preset} (morph)'
    for w in CLOTHED:
        name = re.sub(w, lambda m: m.group(0)[0] + '_' + m.group(0)[1:], name, flags=re.I)
    return name


def expand_npc_presets(spec: dict) -> dict:
    """npc_presets [{plugin, formid, preset, note?}] -> deltas + assign + unblacklist.

    Equipment and the global body are baked with base_preset, so an NPC that should look like
    preset P needs the morph P - base_preset (one delta per distinct P, shared by NPCs)."""
    rows = spec.get('npc_presets') or []
    if not rows:
        return spec
    if not spec.get('base_preset'):
        raise InputError('npc_presets needs base_preset (the preset the equipment was built with)')
    spec = copy.deepcopy(spec)
    deltas = {d['name']: d for d in spec.setdefault('deltas', [])}
    for row in rows:
        fid = row['formid'].upper().removeprefix('0X')
        sex = row.get('sex', 'female')
        if sex not in ('female', 'male'):
            raise InputError(f'npc_presets {row["plugin"]}:{row["formid"]}: sex must be female or male')
        src = (spec.get('male') or {}) if sex == 'male' else spec
        if not src.get('base_preset'):
            raise InputError(f'npc_presets {row["plugin"]}:{row["formid"]}: male rows need male.base_preset')
        name = delta_name(row['preset'])
        deltas.setdefault(name, {'name': name, 'target': row['preset'], 'base': src['base_preset'], 'sex': sex,
                                 **({'osp': src['osp']} if src.get('osp') else {}),
                                 **({'set': src['delta_set']} if src.get('delta_set') else {})})
        spec.setdefault('assign', {}).setdefault(row['plugin'], {})[fid] = [name]
        spec.setdefault('unblacklist', {}).setdefault(row['plugin'], []).append(fid)
    spec['deltas'] = list(deltas.values())
    return spec


def build(spec: dict, base_dir: Path) -> tuple[dict, str, dict]:
    def p(value):
        q = Path(value).expanduser()
        return q if q.is_absolute() else base_dir / q
    config = json.loads(p(spec['base_config']).read_text(encoding='utf-8-sig'))
    schema = json.loads(p(spec['schema']).read_text(encoding='utf-8-sig'))
    loaded = load_presets([p(d) for d in spec.get('presets_dirs', [])])
    generated, problems = [], []
    neutrals = spec.get('neutral') or []
    for n in [neutrals] if isinstance(neutrals, dict) else neutrals:
        nset = n.get('set', 'CBBE Body')
        generated.append({'name': n['name'], 'set': nset, 'sex': 'male' if is_male_set(nset) else 'female',
                          'sliders': {(sl, size): 0.0 for sl in n.get('sliders', ['Breasts'])
                                      for size in ('small', 'big')}})
    spec = expand_npc_presets(spec)
    for d in spec.get('deltas', []):
        for key in ('target', 'base'):
            if d[key] not in loaded:
                problems.append(f'delta {d["name"]!r}: {key} preset {d[key]!r} not loaded')
        if problems:
            continue
        defaults = osp_defaults(p(d['osp'])) if d.get('osp') else {}
        generated.append({'name': d['name'], 'set': d.get('set', loaded[d['target']]['set']),
                          'sex': d.get('sex', 'male' if is_male_set(loaded[d['target']]['set']) else 'female'),
                          'sliders': delta_sliders(loaded[d['target']]['sliders'],
                                                   loaded[d['base']]['sliders'], defaults)})
    pfile = spec.get('presets_file', 'BSO-OBody-Presets.xml')
    for name in [g['name'] for g in generated] + [pfile]:
        if any(w in name.casefold() for w in CLOTHED):
            problems.append(f'{name!r} contains an OBody clothed-set word and would be skipped')
    for g in generated:
        if g['sex'] == 'female' and is_male_set(g['set']):
            problems.append(f'{g["name"]!r}: set {g["set"]!r} reads as a male body to OBody')
        if g['sex'] == 'male' and not is_male_set(g['set']):
            problems.append(f'{g["name"]!r}: male preset but set {g["set"]!r} reads as female to OBody')
        if g['name'] in loaded:
            problems.append(f'{g["name"]!r} already exists in the loaded presets')
    names = set(loaded) | {g['name'] for g in generated}
    sets = {**{k: v['set'] for k, v in loaded.items()}, **{g['name']: g['set'] for g in generated}}
    pool = list(spec.get('random_pool', []))
    if not pool:
        problems.append('random_pool is empty: OBody 4.4.3 would skip every female NPC, assignments included')
    problems += [f'random_pool: {n!r} is not a loaded or generated preset' for n in pool if n not in names]
    by_sex = {'female': sorted(n for n in pool if n in sets and not is_male_set(sets[n])),
              'male': sorted(n for n in pool if n in sets and is_male_set(sets[n]))}
    if pool and not by_sex['female']:
        problems.append('random_pool has no female preset: OBody 4.4.3 would skip every female NPC')
    if not by_sex['male'] and any(is_male_set(v) for v in sets.values()):
        problems.append('random_pool has no male preset while male presets are loaded: OBody 4.4.3 skips '
                        'every male NPC (assignments included) and leaves their old morphs')
    new = copy.deepcopy(config)
    new['blacklistedPresetsFromRandomDistribution'] = sorted(
        set(config.get('blacklistedPresetsFromRandomDistribution', [])) | (names - set(pool)))
    bl = new.setdefault('blacklistedNpcsFormID', {})
    removed = []
    for plugin, ids in spec.get('unblacklist', {}).items():
        keep = [x for x in bl.get(plugin, []) if x.upper().lstrip('0') not in {i.upper().lstrip('0') for i in ids}]
        removed += [f'{plugin}:{x}' for x in bl.get(plugin, []) if x not in keep]
        if plugin in bl:
            bl[plugin] = keep
            if not keep:
                del bl[plugin]
    assigned = []
    for plugin, ids in spec.get('assign', {}).items():
        for fid, presets in ids.items():
            for pr in presets:
                if pr not in names:
                    problems.append(f'assign {plugin}:{fid}: preset {pr!r} not loaded or generated')
            if any(fid.upper().lstrip('0') == x.upper().lstrip('0') for x in bl.get(plugin, [])):
                problems.append(f'assign {plugin}:{fid} is still in blacklistedNpcsFormID (add it to unblacklist)')
            new.setdefault('npcFormID', {}).setdefault(plugin, {})[fid] = list(presets)
            assigned.append(f'{plugin}:{fid}')
    problems += validate(new, schema)
    report = dict(loaded_presets=len(loaded), generated=[g['name'] for g in generated],
                  random_pool=pool, random_pool_by_sex=by_sex, blacklisted_presets=len(new['blacklistedPresetsFromRandomDistribution']),
                  unblacklisted=removed, assigned=assigned, problems=problems,
                  deltas={g['name']: {f'{k[0]}/{k[1]}': v for k, v in g['sliders'].items()} for g in generated})
    return new, preset_xml(generated), report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', type=Path, required=True, help='rebuild config with an "obody" section, or that section alone')
    ap.add_argument('--out', type=Path, required=True, help='new (empty or missing) layer directory')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args(argv)
    try:
        cfg = json.loads(args.config.read_text(encoding='utf-8'))
        spec = cfg.get('obody', cfg)
        new, presets, report = build(spec, args.config.resolve().parent)
    except (OSError, ValueError, KeyError, ET.ParseError, InputError) as exc:
        print(json.dumps({'ok': False, 'error': f'{type(exc).__name__}: {exc}'}, ensure_ascii=False))
        return 2
    ok = not report['problems']
    if ok and not args.dry_run:
        if args.out.exists() and any(args.out.iterdir()):
            print(json.dumps({'ok': False, 'error': f'--out not empty: {args.out}'}))
            return 2
        cfg_path = args.out / 'SKSE' / 'Plugins' / 'OBody_presetDistributionConfig.json'
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        cfg_path.write_text(json.dumps(new, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
        if report['generated']:
            pp = args.out / 'CalienteTools' / 'BodySlide' / 'SliderPresets' / spec.get('presets_file', 'BSO-OBody-Presets.xml')
            pp.parent.mkdir(parents=True, exist_ok=True)
            pp.write_text(presets, encoding='utf-8')
    print(json.dumps(dict(ok=ok, out=str(args.out), dry_run=args.dry_run, **report), ensure_ascii=False, indent=1))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
