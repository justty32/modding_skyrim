#!/usr/bin/env python3
"""Rebuild every configured BodySlide batch from one config file: stage -> plan -> build -> verify -> layer.

One-line rebuild after changing the config (base preset, batches, layer names, revision):
  python tools/bodyslide_rebuild.py all --config CONFIG.json

Subcommands (each reads the config; --batch ID limits to some batches, repeatable):
  stage   merge live BodySlide resources (+ extra_sources) into <run>/tool via bodyslide_stage.py;
          an existing <run>/tool is reused, never overwritten (new run name = new staging)
  plan    catalog + per-batch project choice (bodyslide_select.py); writes
          <run>/tool/SliderGroups/bodyslide-rebuild.xml, <run>/tool/BuildSelection.xml and
          <run>/plan/<batch>.json. Exit 1 on unresolved same-output variants, uncovered stems of a
          replaced layer, cross-batch overlaps or a missing preset (human decisions).
  build   one bodyslide_sandbox_run.py round per batch (label <batch>-<revision><suffix>)
  verify  path set + sampled NIF/TRI/BODYTRI + baseline vertex compare (bodyslide_layer.py)
  layer   <staging_root>/layers/<layer>-<revision>/ (hardlinks + meta.ini), manifest.json and a
          layer_apply.py draft (layer-apply/1) per batch; never touches MO2
  obody   NPC -> preset table (config 'obody', see bodyslide_obody_config.py) -> its own layer
          <obody.layer>-<obody.revision> with OBody_presetDistributionConfig.json + delta presets;
          change one NPC = edit the table, bump obody.revision, rerun this step only;
          obody.neutralize_tri [Data-relative .tri paths] adds empty TRIs for private bodies that
          are already baked to the target preset; obody.extra_files {Data-relative path: source}
          copies files into the layer (e.g. a private body NIF retargeted by bodyslide_fit.py
          retarget-bodytri); obody.staging_root puts layers/ and manifests/ under another staging
  all     stage, plan, build, verify, layer, obody; stops at the first failing step

Config (JSON, schema bodyslide-rebuild/1; see wf/workflows/bodyslide/body-swap.md):
  name, revision, mo2_dir, game_data, profile, staging_root, run, base_preset, morphs,
  preset_files [user preset XMLs copied into the staged SliderPresets, e.g. one saved from the
  BodySlide GUI, so base_preset can name it], obody {...},
  timeout, samples, stage_shapedata ("all" | "none" | [folders]), stage_max_bytes, body_reference (dir with the built femalebody_0/1,
  or malebody_0/1 with body_sex "male"), body_sex ("female" default | "male": which global body and embedded
  body shapes verify compares against), extra_sources {label: dir},
  zaps {project: {zap: bool}},
  batches [{id, layer, before, replaces [mod names], references [dirs], select {...},
            prefer [...], avoid [...], exclude_projects [...], exclude_stems [...], choose {...}}]
Relative paths (extra_sources, references, body_reference, select.scope.table) resolve against
staging_root.

Exit: 0 ok; 1 a step finished but needs a human (see its JSON); 2 refused (bad config, guard).
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodyslide_layer as layer  # noqa: E402
import bodyslide_select as select  # noqa: E402

HERE = Path(__file__).resolve().parent
GROUP_FILE = 'bodyslide-rebuild.xml'
ASCII_NAME = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,80}$')
REQUIRED = ('name', 'revision', 'mo2_dir', 'game_data', 'staging_root', 'run', 'base_preset', 'batches')


class ConfigError(Exception):
    pass


def load_config(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding='utf-8'))
    if cfg.get('schema') != 'bodyslide-rebuild/1':
        raise ConfigError('schema must be bodyslide-rebuild/1')
    missing = [k for k in REQUIRED if k not in cfg]
    if missing:
        raise ConfigError(f'missing keys: {missing}')
    base = path.resolve().parent
    root = Path(os.path.expanduser(cfg['staging_root']))
    if not root.is_absolute():
        root = base / root
    cfg['_base'], cfg['_root'] = base, root
    cfg['_run'] = root / cfg['run']
    cfg.setdefault('profile', 'modpack-main')
    cfg.setdefault('morphs', True)
    cfg.setdefault('timeout', 7200)
    cfg.setdefault('samples', 5)
    cfg.setdefault('body_sex', 'female')
    if cfg['body_sex'] not in layer.BODY_SETS:
        raise ConfigError(f"body_sex must be one of {sorted(layer.BODY_SETS)}")
    ids = [b.get('id') for b in cfg['batches']]
    for b in cfg['batches']:
        for key in ('id', 'layer'):
            if not ASCII_NAME.match(str(b.get(key, ''))):
                raise ConfigError(f'batch {b.get("id")!r}: {key} must be ASCII [A-Za-z0-9._-]')
    if len(set(ids)) != len(ids):
        raise ConfigError(f'duplicate batch ids: {ids}')
    if not ASCII_NAME.match(cfg['revision']) or not ASCII_NAME.match(cfg['run']):
        raise ConfigError('revision and run must be ASCII names')
    return cfg


def under(cfg, value) -> Path:
    p = Path(os.path.expanduser(value))
    return p if p.is_absolute() else cfg['_root'] / p


def pick(cfg, only):
    if not only:
        return cfg['batches']
    unknown = set(only) - {b['id'] for b in cfg['batches']}
    if unknown:
        raise ConfigError(f'unknown batch ids: {sorted(unknown)}')
    return [b for b in cfg['batches'] if b['id'] in only]


def group_name(batch) -> str:
    return f"BSO {batch['id']}"


def label(cfg, batch, suffix='') -> str:
    return f"{batch['id']}-{cfg['revision']}{suffix}"


def layer_name(cfg, batch) -> str:
    return f"{batch['layer']}-{cfg['revision']}"


def stage_table(cfg) -> Path:
    return cfg['_root'] / f"{cfg['run']}-stage-sources.json"


def add_preset_files(cfg, tool: Path) -> list:
    """Copy user preset XMLs (preset_files) into the staged SliderPresets; same name must be same bytes."""
    done = []
    for src in cfg.get('preset_files', []):
        src = under(cfg, src)
        dst = tool / 'SliderPresets' / src.name
        data = src.read_bytes()
        if dst.exists() and dst.read_bytes() != data:
            raise ConfigError(f'preset_files: {dst} exists with other content; rename {src.name}')
        dst.parent.mkdir(exist_ok=True)
        dst.write_bytes(data)
        done.append(dict(file=str(src), staged=str(dst), sha256=layer.sha256(dst)))
    return done


def cmd_stage(cfg, args) -> dict:
    tool = cfg['_run'] / 'tool'
    if tool.is_dir() and any(tool.iterdir()):
        return dict(ok=True, reused=str(tool), table=str(stage_table(cfg)), preset_files=add_preset_files(cfg, tool))
    mo2 = Path(cfg['mo2_dir'])
    argv = [sys.executable, str(HERE / 'bodyslide_stage.py'), '--mods-dir', str(mo2 / 'mods'),
            '--overwrite-dir', str(mo2 / 'overwrite'), '--profile-dir', str(mo2 / 'profiles' / cfg['profile']),
            '--game-data', cfg['game_data'], '--out', str(tool), '--table', str(stage_table(cfg)),
            '--max-bytes', str(cfg.get('stage_max_bytes', 3e9))]
    for lbl, d in cfg.get('extra_sources', {}).items():
        argv += ['--extra-source', f'{lbl}={under(cfg, d)}']
    shapedata = cfg.get('stage_shapedata', 'all')
    if shapedata == 'none':
        argv.append('--no-shapedata')
    elif isinstance(shapedata, list):
        for folder in shapedata:
            argv += ['--shapedata-folder', folder]
    elif shapedata != 'all':
        raise ConfigError('stage_shapedata must be "all", "none" or a list of ShapeData folders')
    proc = subprocess.run(argv, capture_output=True, text=True)
    # exit 1 = staged but needs a human (symlinks skipped / MO2 BuildSelection); plan enforces the latter.
    out = dict(ok=proc.returncode in (0, 1), exit=proc.returncode, argv=argv)
    if proc.returncode in (0, 1):
        out['preset_files'] = add_preset_files(cfg, tool)
    try:
        out['stage'] = json.loads(proc.stdout)
    except ValueError:
        out['stdout'], out['stderr'] = proc.stdout[-2000:], proc.stderr[-2000:]
    return out


def preset_names(tool: Path) -> set:
    import xml.etree.ElementTree as ET
    names = set()
    for d in tool.iterdir():
        if d.name.casefold() == 'sliderpresets' and d.is_dir():
            for f in d.glob('*.xml'):
                try:
                    names |= {p.get('name') for p in ET.parse(f).getroot().iter('Preset')}
                except ET.ParseError:
                    pass
    return names


def cmd_plan(cfg, args) -> dict:
    tool = cfg['_run'] / 'tool'
    catalog, cat_errors = select.load_catalog(tool, stage_table(cfg))
    plans, errors, owner = {}, [], {}
    for batch in cfg['batches']:  # always all batches: cross-batch overlap needs every selection
        res = select.select_batch(catalog, batch, cfg['_root'])
        plans[batch['id']] = res
        for p in res['projects']:
            prev = owner.setdefault(p['stem'], batch['id'])
            if prev != batch['id']:
                errors.append(f"stem {p['stem']} in batches {prev} and {batch['id']}")
        errors += [f"{batch['id']}: {e}" for e in res['errors']]
        if res['unresolved']:
            errors.append(f"{batch['id']}: {len(res['unresolved'])} unresolved same-output stems")
    if cfg['base_preset'] not in preset_names(tool):
        errors.append(f"preset {cfg['base_preset']!r} not found in staged SliderPresets")
    # Only a BuildSelection that came from MO2 (stage table) needs review; our own one is rewritten.
    staged_bs = [b['staged_rel'] for b in json.loads(stage_table(cfg).read_text(encoding='utf-8'))
                 ['summary'].get('build_selection', [])] if stage_table(cfg).is_file() else []
    plan_dir = cfg['_run'] / 'plan'
    summary = {}
    for batch in cfg['batches']:
        res = plans[batch['id']]
        rec = dict(batch=batch['id'], group=group_name(batch), layer=layer_name(cfg, batch),
                   projects=[{k: p[k] for k in ('name', 'osp', 'mod', 'stem', 'outputs', 'tri', 'out_path')}
                             for p in res['projects']],
                   **{k: res[k] for k in ('decisions', 'unresolved', 'uncovered', 'errors',
                                          'expected', 'expected_tri')})
        layer.write_json(plan_dir / f"{batch['id']}.json", rec)
        summary[batch['id']] = dict(projects=len(res['projects']), nif=len(res['expected']),
                                    tri=len(res['expected_tri']), unresolved=len(res['unresolved']),
                                    uncovered=len(res['uncovered']))
    ok = not errors
    if ok and not args.dry_run:
        groups = ''.join(select.group_xml(group_name(b), [p['name'] for p in plans[b['id']]['projects']])
                         .split('<SliderGroups>\n', 1)[1].rsplit('</SliderGroups>', 1)[0]
                         for b in cfg['batches'])
        (tool / 'SliderGroups').mkdir(exist_ok=True)
        (tool / 'SliderGroups' / GROUP_FILE).write_text(
            f'<?xml version="1.0" encoding="UTF-8"?>\n<SliderGroups>\n{groups}</SliderGroups>\n', encoding='utf-8')
        allp = [p for b in cfg['batches'] for p in plans[b['id']]['projects']]
        if staged_bs and not cfg.get('override_build_selection'):
            ok = False
            errors.append(f'staged {staged_bs} came from MO2; set override_build_selection after review')
        else:
            (tool / 'BuildSelection.xml').write_text(select.build_selection_xml(allp, cfg.get('zaps')),
                                                     encoding='utf-8')
    return dict(ok=ok, errors=errors, catalog=len(catalog), catalog_errors=cat_errors,
                staged_build_selection=staged_bs, batches=summary, plan_dir=str(plan_dir))


def runner_argv(cfg, batch, suffix, dry):
    argv = [sys.executable, str(HERE / 'bodyslide_sandbox_run.py'), 'build', '--run-dir', str(cfg['_run']),
            '--label', label(cfg, batch, suffix), '--group', group_name(batch), '--preset', cfg['base_preset'],
            '--timeout', str(batch.get('timeout', cfg['timeout'])), '--mo2-dir', cfg['mo2_dir'],
            '--game-data', cfg['game_data']]
    if cfg['morphs']:
        argv.append('--tri')
    if dry:
        argv.append('--dry-run')
    return argv


def cmd_build(cfg, args) -> dict:
    out, ok = {}, True
    for batch in pick(cfg, args.batch):
        proc = subprocess.run(runner_argv(cfg, batch, args.suffix, args.dry_run), capture_output=True, text=True)
        out[batch['id']] = dict(exit=proc.returncode, stdout=proc.stdout[-1500:], stderr=proc.stderr[-1500:])
        if proc.returncode:
            ok = False
            break
    return dict(ok=ok, batches=out)


def load_plan(cfg, batch):
    return json.loads((cfg['_run'] / 'plan' / f"{batch['id']}.json").read_text(encoding='utf-8'))


def cmd_verify(cfg, args) -> dict:
    out, ok = {}, True
    for batch in pick(cfg, args.batch):
        plan = load_plan(cfg, batch)
        res = layer.verify_batch(cfg['_run'] / 'rounds' / label(cfg, batch, args.suffix) / 'output', plan,
                                 cfg['samples'], [under(cfg, r) for r in batch.get('references', [])],
                                 under(cfg, cfg['body_reference']) if cfg.get('body_reference') else None,
                                 cfg['body_sex'])
        layer.write_json(cfg['_run'] / 'verify' / f"{label(cfg, batch, args.suffix)}.json", res)
        out[batch['id']] = {k: res[k] for k in ('ok', 'failures', 'files', 'expected_nif', 'expected_tri')}
        out[batch['id']]['tri_missing'] = len(res['tri_missing'])
        out[batch['id']]['baseline_equal'] = [s.get('baseline', {}).get('equal') for s in res['samples']]
        out[batch['id']]['body_on'] = [{k: v.get('on_body') for k, v in s.get('body_match', {}).items()}
                                       for s in res['samples'] if s.get('body_match')]
        ok = ok and res['ok']
    return dict(ok=ok, batches=out)


def cmd_layer(cfg, args) -> dict:
    out = {}
    for batch in pick(cfg, args.batch):
        name = layer_name(cfg, batch)
        dest = cfg['_root'] / 'layers' / name
        meta = dict(config=cfg['name'], batch=batch['id'], revision=cfg['revision'],
                    preset=cfg['base_preset'], morphs=cfg['morphs'],
                    round=label(cfg, batch, args.suffix))
        manifest = layer.assemble_layer(cfg['_run'] / 'rounds' / meta['round'] / 'output', dest,
                                        load_plan(cfg, batch), meta)
        mdir = cfg['_root'] / 'manifests'
        layer.write_json(mdir / f'{name}.json', manifest)
        draft = {'schema': 'layer-apply/1', 'name': f"bodyslide-{batch['id']}", 'round': cfg['revision'],
                 'mods': [{'name': name, 'src': str(dest), 'replace': False}],
                 'modlist': [{'mod': name, 'enabled': True, 'before': batch.get('before')}]}
        if batch.get('replaces'):
            draft['disable_mods'] = list(batch['replaces'])
        layer.write_json(mdir / f'{name}.layer-apply.json', draft)
        out[batch['id']] = dict(layer=str(dest), files=manifest['files'], bytes=manifest['bytes'])
    return dict(ok=True, batches=out)


def cmd_obody(cfg, args) -> dict:
    """NPC -> preset table (obody section) -> its own small layer; equipment layers untouched."""
    import bodyslide_obody_config as oc
    if 'obody' not in cfg:
        return dict(ok=True, skipped='no obody section')
    spec = dict(cfg['obody'])
    spec.setdefault('base_preset', cfg['base_preset'])
    spec.setdefault('presets_dirs', [str(cfg['_run'] / 'tool' / 'SliderPresets')])
    rev = spec.get('revision', cfg['revision'])
    name = f"{spec.get('layer', 'BSO-NPC-Body-Assignments')}-{rev}"
    if not ASCII_NAME.match(name):
        raise ConfigError(f'obody layer name must be ASCII: {name!r}')
    new, presets, report = oc.build(spec, cfg['_root'])
    out_root = under(cfg, spec['staging_root']) if spec.get('staging_root') else cfg['_root']
    dest = out_root / 'layers' / name
    extra = {rel: under(cfg, src) for rel, src in (spec.get('extra_files') or {}).items()}
    report['problems'] += [f'extra_files {rel}: source missing {src}' for rel, src in extra.items() if not src.is_file()]
    if report['problems'] or args.dry_run:
        return dict(ok=not report['problems'], layer=str(dest), **report)
    if dest.exists() and any(dest.iterdir()):
        raise FileExistsError(f'layer directory not empty: {dest} (bump obody.revision)')
    cfg_path = dest / 'SKSE' / 'Plugins' / 'OBody_presetDistributionConfig.json'
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_path.write_text(json.dumps(new, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
    if report['generated']:
        pp = dest / 'CalienteTools' / 'BodySlide' / 'SliderPresets' / spec.get('presets_file', 'BSO-OBody-Presets.xml')
        pp.parent.mkdir(parents=True, exist_ok=True)
        pp.write_text(presets, encoding='utf-8')
    for rel in spec.get('neutralize_tri', []):
        # Empty PIRT (0 shapes): RaceMenu finds no morph for a private body that is already
        # baked to the target shape, so the NPC's delta preset moves only the equipment.
        tri = dest / rel.replace('\\', '/')
        tri.parent.mkdir(parents=True, exist_ok=True)
        tri.write_bytes(b'PIRT\x00\x00')
    copied = {}
    for rel, src in extra.items():
        # e.g. a private body NIF whose BODYTRI was retargeted (bodyslide_fit.py retarget-bodytri)
        dst = dest / rel.replace('\\', '/')
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        copied[rel] = layer.sha256(dst)
    report['extra_files'] = copied
    (dest / 'meta.ini').write_text('[General]\ngameName=Skyrim Special Edition\nmodid=0\n'
                                   f'version={rev}\ncategory=0\ncomments=OBody NPC body assignments from '
                                   f"{cfg['name']} (base {spec['base_preset']!r})\n", encoding='utf-8')
    mdir = out_root / 'manifests'
    draft = {'schema': 'layer-apply/1', 'name': 'bodyslide-obody', 'round': rev,
             'mods': [{'name': name, 'src': str(dest), 'replace': False}],
             'modlist': [{'mod': name, 'enabled': True, 'before': spec.get('before')}]}
    if spec.get('replaces'):
        draft['disable_mods'] = list(spec['replaces'])
    layer.write_json(mdir / f'{name}.layer-apply.json', draft)
    layer.write_json(mdir / f'{name}.json', dict(layer=name, **report))
    return dict(ok=True, layer=str(dest), **report)


STEPS = {'stage': cmd_stage, 'plan': cmd_plan, 'build': cmd_build, 'verify': cmd_verify, 'layer': cmd_layer,
         'obody': cmd_obody}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('step', choices=[*STEPS, 'all'])
    ap.add_argument('--config', type=Path, required=True)
    ap.add_argument('--batch', action='append', default=[], help='batch id (repeatable; default all)')
    ap.add_argument('--suffix', default='', help='round label suffix for a rebuild of the same revision')
    ap.add_argument('--dry-run', action='store_true', help='plan: write nothing into the tool; build: runner --dry-run')
    args = ap.parse_args(argv)
    try:
        cfg = load_config(args.config)
        steps = list(STEPS) if args.step == 'all' else [args.step]
        result = {}
        for step in steps:
            result[step] = STEPS[step](cfg, args)
            if not result[step]['ok']:
                break
    except (ConfigError, select.SelectError, FileExistsError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 0 if all(r['ok'] for r in result.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
