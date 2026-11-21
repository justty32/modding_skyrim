#!/usr/bin/env python3
"""Merge the live MO2 BodySlide resources into one isolated, single-case staging tree.

Read only towards MO2: mods/, overwrite/ and the profile are never written.
The staging tree gets real copies (shutil.copy2; never hardlinks/symlinks),
each re-hashed after copying. A wf-table/1 JSON source table records, for every
case-insensitive relative path, the winner mod and every provider.

Example:
  python tools/bodyslide_stage.py --mods-dir MO2/mods --overwrite-dir MO2/overwrite \
    --profile-dir MO2/profiles/modpack-main --out /isolated/run1/BodySlide --dry-run

modlist.txt semantics (MO2): first line = highest priority; '+Name' enabled,
'-Name' disabled (excluded); '*' lines (unmanaged/DLC/CC), names ending in
'_separator', '#' comments and blank lines are skipped; CRLF/BOM tolerated.
Enabled mods whose directory is missing are listed in summary.missing_mod_dirs.
overwrite/ outranks every mod.

Inside each source, CalienteTools/BodySlide is located case-insensitively per
level; two case variants at one level in the same source is fail-closed. Files
or directories whose name ends in '.mohidden' are excluded and counted.
Symlinks are never followed; they are skipped and listed in summary.errors.

Merge: key = casefolded path below BodySlide/; the highest-priority provider
wins. Output casing: known top-level folders use the canonical BodySlide
spelling; deeper directories use the highest-priority provider's spelling;
file names use the winner's spelling. Every disagreement is in
summary.case_variants. summary.build_selection reports any root
BuildSelection*.xml, because in CLI batch mode it decides which of several
same-output outfits is built and which zap sliders apply (review F5).

Exit codes:
  0  staged (or dry-run table written), nothing needs a human.
  1  finished, but needs a human: symlinks were skipped (summary.errors) or a
     root BuildSelection*.xml is present (summary.attention). Overrides whose
     contents differ are normal MO2 priority resolution and do NOT cause 1;
     they are listed in the table's 'overrides' (summary counts them).
  2  refused / fail-closed: bad arguments or missing inputs, path guard
     refusal, --out not empty, ambiguous case variants inside one source,
     a path that is a file in one source and a directory in another,
     unreadable source files, capacity gate exceeded (nothing copied; the
     table is still written), or a post-copy hash mismatch.
"""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodyslide_guard  # noqa: E402  (shared path guard, used as-is)

KNOWN_TOP = {n.casefold(): n for n in (
    'SliderSets', 'ShapeData', 'SliderPresets', 'SliderGroups', 'SliderCategories',
    'ConversionSets', 'RefTemplates')}
OVERWRITE = '(overwrite)'
COLUMNS = ['staged_rel', 'winner_mod', 'winner_rel', 'sha256', 'size', 'providers', 'copied']
HEAD_BYTES = 2048


class Fatal(Exception):
    """Precondition failure or fail-closed condition (exit 2)."""


def sha256_file(path) -> str:
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b''):
                h.update(chunk)
    except OSError as exc:
        raise Fatal(f'cannot read source file {path}: {exc}') from exc
    return h.hexdigest()


def parse_modlist(data: bytes):
    """Return (enabled names highest priority first, disabled count)."""
    text = data.decode('utf-8-sig')
    enabled, disabled = [], 0
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip('\r').lstrip('﻿')
        if not line.strip() or line.startswith('#'):
            continue
        flag, name = line[0], line[1:]
        if flag == '*' or name.endswith('_separator'):
            continue
        if flag not in '+-':
            raise Fatal(f'modlist.txt line {number}: unrecognized entry {line!r}')
        if not name or name in ('.', '..') or '/' in name or '\\' in name:
            raise Fatal(f'modlist.txt line {number}: unsafe mod name {name!r}')
        if flag == '+':
            enabled.append(name)
        else:
            disabled += 1
    return enabled, disabled


def child_ci(parent: Path, name: str, label: str, errors: list):
    """Single case-insensitive child directory, None if absent; fail-closed on variants."""
    try:
        entries = list(os.scandir(parent))
    except OSError:
        return None
    matches = sorted((e for e in entries if e.name.casefold() == name.casefold()), key=lambda e: e.name)
    if len(matches) > 1:
        raise Fatal(f'{label}: ambiguous case variants {[e.name for e in matches]} in {parent}')
    if not matches:
        return None
    entry = matches[0]
    if entry.is_symlink():
        errors.append(f'{label}: symlink not followed: {entry.path}')
        return None
    return entry if entry.is_dir(follow_symlinks=False) else None


def count_files(path: str) -> int:
    return sum(len(files) + sum(os.path.islink(os.path.join(d, x)) for x in dirs)
               for d, dirs, files in os.walk(path, followlinks=False))


def scan_source(label: str, root: Path, errors: list, counters: dict):
    """Yield (bs_rel, mod_rel, abs_path, size) for one mod/overwrite directory."""
    ct = child_ci(root, 'CalienteTools', label, errors)
    if ct is None:
        return []
    bs = child_ci(Path(ct.path), 'BodySlide', label, errors)
    if bs is None:
        return []
    prefix = f'{ct.name}/{bs.name}'
    found, seen = [], {}
    for dirpath, dirnames, filenames in os.walk(bs.path, followlinks=False):
        keep = []
        for d in dirnames:
            full = os.path.join(dirpath, d)
            if os.path.islink(full):
                errors.append(f'{label}: symlink not followed: {full}')
            elif d.casefold().endswith('.mohidden'):
                counters['mohidden'] += count_files(full) or 1
            else:
                keep.append(d)
        dirnames[:] = sorted(keep)
        for f in sorted(filenames):
            full = os.path.join(dirpath, f)
            try:
                st = os.lstat(full)
            except OSError as exc:
                raise Fatal(f'{label}: cannot stat {full}: {exc}') from exc
            if stat.S_ISLNK(st.st_mode):
                errors.append(f'{label}: symlink not followed: {full}')
                continue
            if f.casefold().endswith('.mohidden'):
                counters['mohidden'] += 1
                continue
            if not stat.S_ISREG(st.st_mode):
                errors.append(f'{label}: not a regular file, skipped: {full}')
                continue
            rel = Path(os.path.relpath(full, bs.path)).as_posix()
            key = rel.casefold()
            if key in seen:
                raise Fatal(f'{label}: ambiguous case variants {seen[key]!r} and {rel!r} under {bs.path}')
            seen[key] = rel
            found.append((rel, f'{prefix}/{rel}', full, st.st_size))
    return found


def collect(args, errors, counters):
    profile = args.profile_dir
    modlist = profile / 'modlist.txt'
    if not args.mods_dir.is_dir():
        raise Fatal(f'--mods-dir is not a directory: {args.mods_dir}')
    if args.overwrite_dir is not None and not args.overwrite_dir.is_dir():
        raise Fatal(f'--overwrite-dir is not a directory: {args.overwrite_dir}')
    try:
        data = modlist.read_bytes()
    except OSError as exc:
        raise Fatal(f'cannot read {modlist}: {exc}') from exc
    enabled, disabled = parse_modlist(data)
    sources = []
    if args.overwrite_dir is not None:
        sources.append((OVERWRITE, args.overwrite_dir))
    missing = []
    for name in enabled:
        path = args.mods_dir / name
        if path.is_symlink():
            errors.append(f'{name}: symlinked mod directory not followed: {path}')
        elif path.is_dir():
            sources.append((name, path))
        else:
            missing.append(name)
    providers = {}  # casefold key -> [provider dicts, highest priority first]
    with_bs = []
    for rank, (label, path) in enumerate(sources, 1):
        files = scan_source(label, path, errors, counters)
        if files:
            with_bs.append(label)
        for rel, mod_rel, full, size in files:
            providers.setdefault(rel.casefold(), []).append(dict(
                rank=rank, mod=label, rel=rel, mod_rel=mod_rel, abs=full, size=size,
                sha256=sha256_file(full)))
    meta = dict(modlist=dict(path=str(modlist), sha256=hashlib.sha256(data).hexdigest()),
                enabled_mods=len(enabled), disabled_mods=disabled, missing_mod_dirs=missing,
                mods_with_bodyslide=with_bs)
    return providers, meta


def choose_casing(providers):
    """Return ({key: output rel}, case_variants)."""
    file_keys = set(providers)
    spellings = {}  # dir prefix key -> {spelling: [best rank, mods]}
    for key, provs in providers.items():
        for p in provs:
            parts = p['rel'].split('/')
            for i in range(len(parts) - 1):
                pkey = '/'.join(parts[:i + 1]).casefold()
                slot = spellings.setdefault(pkey, {}).setdefault(parts[i], [p['rank'], set()])
                slot[0] = min(slot[0], p['rank'])
                slot[1].add(p['mod'])
    clash = sorted(file_keys & set(spellings))
    if clash:
        raise Fatal(f'path is a file in one source and a directory in another: {clash[:5]}')
    chosen, variants = {}, []
    for pkey in sorted(spellings, key=lambda k: (k.count('/'), k)):
        options = spellings[pkey]
        parent = pkey.rsplit('/', 1)[0] if '/' in pkey else None
        if parent is None and pkey in KNOWN_TOP:
            name = KNOWN_TOP[pkey]
        else:
            name = min(options, key=lambda s: (options[s][0], s))
        chosen[pkey] = (chosen[parent] + '/' if parent else '') + name
        if set(options) != {name}:
            variants.append(dict(dir=chosen[pkey], chosen=name, variants=[
                dict(name=s, mods=sorted(options[s][1])) for s in sorted(options)]))
    out = {}
    for key, provs in providers.items():
        winner = provs[0]['rel']
        parent = key.rsplit('/', 1)[0] if '/' in key else None
        out[key] = (chosen[parent] + '/' if parent else '') + winner.rsplit('/', 1)[-1]
    return out, variants


def selected_for_copy(key: str, args) -> bool:
    parts = key.split('/')
    if parts[0] != 'shapedata' or len(parts) == 1:
        return True
    if args.no_shapedata:
        return False
    if not args.shapedata_folder:
        return True
    return len(parts) >= 3 and parts[1] in {f.casefold() for f in args.shapedata_folder}


def build_table(providers, meta, args):
    rel_of, variants = choose_casing(providers)
    rows, overrides, winners = [], [], {}
    for key in sorted(providers, key=lambda k: rel_of[k].casefold()):
        provs = providers[key]
        win = provs[0]
        winners[rel_of[key]] = win
        rows.append(dict(staged_rel=rel_of[key], winner_mod=win['mod'], winner_rel=win['mod_rel'],
                         sha256=win['sha256'], size=win['size'], providers=len(provs),
                         copied=selected_for_copy(key, args)))
        if len(provs) > 1:
            overrides.append(dict(staged_rel=rel_of[key],
                                  identical=len({p['sha256'] for p in provs}) == 1,
                                  providers=[dict(priority=p['rank'], mod=p['mod'], rel=p['mod_rel'],
                                                  sha256=p['sha256']) for p in provs]))
    if len({r['staged_rel'] for r in rows}) != len(rows) or \
            len({r['staged_rel'].casefold() for r in rows}) != len(rows):
        raise Fatal('internal error: output casing is not unique')
    build_selection = []
    config_xml = None
    for rel, win in winners.items():
        key = rel.casefold()
        if '/' in key:
            continue
        if key.startswith('buildselection') and key.endswith('.xml'):
            with open(win['abs'], 'rb') as fh:
                head = fh.read(HEAD_BYTES)
            build_selection.append(dict(staged_rel=rel_of[key], mod=win['mod'], sha256=win['sha256'],
                                        size=win['size'], head=head.decode('utf-8', 'replace')))
        elif key == 'config.xml':
            config_xml = dict(staged_rel=rel_of[key], mod=win['mod'], sha256=win['sha256'])
    copied = [r for r in rows if r['copied']]
    differing = [o for o in overrides if not o['identical']]
    summary = dict(meta, files=len(rows), total_bytes=sum(r['size'] for r in rows),
                   copied_files=len(copied), copied_bytes=sum(r['size'] for r in copied),
                   overrides=len(overrides), overrides_differing=len(differing),
                   overrides_differing_mods=sorted({p['mod'] for o in differing for p in o['providers']}),
                   case_variants=variants, build_selection=build_selection, config_xml=config_xml)
    return rows, overrides, summary, winners


def resolve_roots(args):
    roots, missing = bodyslide_guard.live_roots(
        mods=args.mods_dir, overwrite=args.overwrite_dir, game_data=args.game_data,
        instance=args.instance_dir, extra=[args.profile_dir])
    if 'mods' in missing or 'overwrite' in missing:
        raise Fatal('live mods/overwrite roots must be known for the --out guard: pass '
                    '--overwrite-dir or set MO2_OVERWRITE_DIR / MO2_DIR')
    return roots, [m for m in missing if m not in ('mods', 'overwrite')]


def check_targets(args, roots):
    errors = bodyslide_guard.check_isolated({'--out': args.out, '--table': args.table}, roots)
    out_real, table_real = bodyslide_guard.real(args.out), bodyslide_guard.real(args.table)
    if table_real == out_real or table_real.is_relative_to(out_real):
        errors.append(f'--table {table_real} must not be inside --out (BodySlide would scan it)')
    if out_real.is_relative_to(table_real):
        errors.append(f'--out {out_real} must not be inside --table')
    if args.out.is_symlink() or args.out.exists() and (not args.out.is_dir() or any(args.out.iterdir())):
        errors.append(f'--out must not exist or be an empty directory: {args.out}')
    if errors:
        raise Fatal('; '.join(errors))


def copy_tree(rows, winners_by_rel, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    for row in rows:
        if not row['copied']:
            continue
        src = winners_by_rel[row['staged_rel']]['abs']
        dst = out / row['staged_rel']
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst, follow_symlinks=False)
    for row in rows:
        if row['copied']:
            dst = out / row['staged_rel']
            if dst.is_symlink() or not dst.is_file() or sha256_file(dst) != row['sha256']:
                raise Fatal(f'post-copy verification failed: {dst}')


def write_table(path: Path, rows, overrides, summary):
    doc = {'contract': 'wf-table/1', 'source': 'generated by tools/bodyslide_stage.py',
           'extracted': date.today().isoformat(), 'columns': COLUMNS, 'link_columns': [],
           'rows': rows, 'overrides': overrides, 'summary': summary}
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    os.replace(tmp, path)


def parse_args(argv):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--mods-dir', type=Path, required=True, help='MO2 mods/ (read only)')
    p.add_argument('--profile-dir', type=Path, required=True, help='MO2 profile dir holding modlist.txt (read only)')
    p.add_argument('--overwrite-dir', type=Path, help='MO2 overwrite/ (read only; highest priority source)')
    p.add_argument('--game-data', type=Path, help='game Data dir, guarded against (else SKYRIM_GAME_DATA)')
    p.add_argument('--instance-dir', type=Path, help='instance dir, guarded against (else SKYRIM_REPO or git)')
    p.add_argument('--out', type=Path, required=True, help='staging root to create; must not exist or be empty')
    p.add_argument('--table', type=Path, help='source table JSON (default <out>.sources.json; never inside --out)')
    p.add_argument('--dry-run', action='store_true', help='write the table only; copy nothing')
    g = p.add_mutually_exclusive_group()
    g.add_argument('--no-shapedata', action='store_true', help='copy nothing under ShapeData/')
    g.add_argument('--shapedata-folder', action='append', default=[], metavar='NAME',
                   help='copy only this first-level ShapeData/ folder (case-insensitive; repeatable)')
    p.add_argument('--max-bytes', type=float, default=3e9, help='capacity gate on copied bytes (default 3e9)')
    p.add_argument('--max-files', type=int, default=15000, help='capacity gate on copied files (default 15000)')
    args = p.parse_args(argv)
    if args.table is None:
        args.table = args.out.with_name(args.out.name + '.sources.json')
    return args


def run(args):
    roots, unknown = resolve_roots(args)
    check_targets(args, roots)
    errors, counters = [], {'mohidden': 0}
    providers, meta = collect(args, errors, counters)
    rows, overrides, summary, winners = build_table(providers, meta, args)
    capacity_ok = summary['copied_bytes'] <= args.max_bytes and summary['copied_files'] <= args.max_files
    attention = []
    if errors:
        attention.append(f'{len(errors)} symlink/irregular entries skipped (see errors)')
    if summary['build_selection']:
        attention.append('BuildSelection*.xml present: decides batch winners and zap (review F5)')
    summary.update(mohidden_excluded=counters['mohidden'], errors=errors, attention=attention,
                   guard_unknown_roots=unknown, dry_run=args.dry_run, out=str(args.out),
                   shapedata_filter=('none' if args.no_shapedata else args.shapedata_folder or 'all'),
                   capacity=dict(max_bytes=args.max_bytes, max_files=args.max_files, ok=capacity_ok))
    if not capacity_ok:
        write_table(args.table, rows, overrides, summary)
        raise Fatal(f'capacity gate exceeded: {summary["copied_files"]} files / '
                    f'{summary["copied_bytes"]} bytes; nothing copied (table: {args.table})')
    if not args.dry_run:
        copy_tree(rows, winners, args.out)
    write_table(args.table, rows, overrides, summary)
    return summary


def main(argv=None):
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return 2 if exc.code else 0
    try:
        summary = run(args)
    except Fatal as exc:
        print(json.dumps({'ok': False, 'exit': 2, 'errors': [str(exc)]}, ensure_ascii=False))
        return 2
    code = 1 if summary['attention'] else 0
    brief = {k: v for k, v in summary.items() if k != 'case_variants'}
    brief['case_variants'] = len(summary['case_variants'])
    brief['build_selection'] = [{k: v for k, v in b.items() if k != 'head'} for b in summary['build_selection']]
    print(json.dumps({'ok': code == 0, 'exit': code, 'table': str(args.table), 'summary': brief},
                     ensure_ascii=False, indent=1))
    return code


if __name__ == '__main__':
    sys.exit(main())
