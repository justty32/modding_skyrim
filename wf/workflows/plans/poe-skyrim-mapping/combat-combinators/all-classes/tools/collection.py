"""Validate rule identities, class tiers and geometry prerequisites."""
from pathlib import Path
import collections
import hashlib
import json


def sha(row):
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(payload.encode()).hexdigest()


LEGACY_SUBTYPES = {'G': 'G1', 'D': 'D1', 'C': 'C3'}


def resolve(row, repo, load):
    if row.get('row_kind') != 'legacy_reference':
        return (row, None)
    locator = row['source_path']
    locator = locator['$fmt'].replace('${gitRoot}', str(repo)) if isinstance(locator, dict) else locator
    p = Path(locator)
    p = p if p.is_absolute() else repo / p
    r = next((x for x in load(str(p)).rows if x['rule_id'] == row['source_rule_id']))
    assert sha(r) == row['source_rule_sha256'], row['rule_id']
    assert r['rule_id'] == row['rule_id']
    reference = {
        'source_path': str(p.relative_to(repo)) if p.is_relative_to(repo) else str(p),
        'source_rule_id': r['rule_id'],
        'source_rule_sha256': sha(r),
    }
    return r, reference


def collect_classes(B, repo, load):
    results = []
    wrappers = []
    for c in ['V', 'G', 'D', 'R', 'C', 'M', 'S', 'X']:
        d = B / c
        p = d / 'rules.json'
        if not p.exists():
            results.append({'class': c, 'state': 'pending'})
            continue
        errors = []
        rrows = load(str(p)).rows
        effective = []
        try:
            for r in rrows:
                e, ref = resolve(r, repo, load)
                effective.append(e)
                scope = 'class_common' if e.get('scope') == 'class_common' else 'subtype'
                sub = None if scope == 'class_common' else LEGACY_SUBTYPES[c] if ref else e.get('owner_subtype')
                wrappers.append({
                    'class_id': c, 'rule_id': e['rule_id'], 'tier': e['tier'],
                    'effective_scope': scope, 'stable_subtype': sub,
                    'payload_sha256': sha(e), 'legacy_reference': ref,
                    'draft_path': str(p.relative_to(B)), 'draft_rule_id': e['rule_id'],
                })
        except Exception as x:
            errors.append(str(x))
        if len(rrows) != 30:
            errors.append('rule count ' + str(len(rrows)))
        ids = [r.get('rule_id') for r in rrows]
        if len(set(ids)) != len(ids):
            errors.append('duplicate rule IDs')
        deliverables = ['subtypes.json', 'parameters.json', 'feasibility.json', 'REPORT.md']
        if not all((d / name).exists() for name in deliverables):
            errors.append('missing deliverables')
        total = sum((f.stat().st_size for f in d.rglob('*') if f.is_file()))
        if total > 150000:
            errors.append('class exceeds150KiB')
        for f in d.glob('*.json'):
            if f.stat().st_size > 1024 * 1024:
                errors.append('JSON exceeds1MiB ' + f.name)
            if load(str(f)).meta.get('contract') != 'wf-table/1':
                errors.append('contract missing ' + f.name)
        for sub in [c + str(i) for i in (1, 2, 3)]:
            s = [w for w in wrappers if w['class_id'] == c and w['stable_subtype'] == sub]
            ct = collections.Counter((w['tier'] for w in s))
            if ct != {'advanced': 6, 'high': 2}:
                errors.append(sub + ' tier counts ' + str(dict(ct)))
        common = [w for w in wrappers if w['class_id'] == c and w['effective_scope'] == 'class_common']
        ct = collections.Counter((w['tier'] for w in common))
        if ct != {'advanced': 4, 'high': 2}:
            errors.append('common tier counts ' + str(dict(ct)))
        results.append({
            'class': c, 'state': 'checked', 'rules': len(rrows), 'bytes': total,
            'legacy_refs': sum(r.get('row_kind') == 'legacy_reference' for r in rrows),
            'errors': errors,
        })
    return results, wrappers


def check_geometry(geometry_root, B, wrappers, results, load):
    gr = load(str(geometry_root / 'reservation.json')).rows
    by = {r['slot']: r for r in gr}
    geoerrors = []
    if len(gr) != 240 or len(by) != 240 or set(by) != {w['rule_id'] for w in wrappers}:
        geoerrors.append('geometry slot coverage/duplicates')
    for w in wrappers:
        if w['legacy_reference']:
            continue
        dp = Path(w['draft_path'])
        dp = dp if dp.is_absolute() else B / dp
        r = next((r for r in load(str(dp)).rows if r['rule_id'] == w['rule_id']))
        if r['rule_id'] not in by:
            continue
        try:
            expected = sorted((by[q]['node_id'] for q in r.get('requires_slots', [])))
        except KeyError:
            geoerrors.append(r['rule_id'] + ' unknown prerequisite slot')
            continue
        if expected != sorted(by[r['rule_id']]['requires_nodes']):
            geoerrors.append(r['rule_id'] + ' missing/extra strong AND prerequisite')
    results.append({'class': 'geometry_join', 'state': 'checked', 'rules': len(gr), 'errors': geoerrors})
