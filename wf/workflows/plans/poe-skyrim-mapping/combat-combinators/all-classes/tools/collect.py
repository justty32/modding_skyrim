"""Collect the checked lightweight rule index; preserve the original CLI."""
import argparse
import json
from pathlib import Path
import sys

from collection import collect_classes, check_geometry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data-root', type=Path, default=Path(__file__).parent)
    ap.add_argument('--repo-root', type=Path, default=Path.cwd())
    ap.add_argument('--geometry-root', type=Path)
    args = ap.parse_args()
    repo = args.repo_root.resolve()
    sys.path.insert(0, str(repo / 'wf/tools'))
    from tabledb import load

    data_root = args.data_root.resolve()
    results, wrappers = collect_classes(data_root, repo, load)
    if args.geometry_root:
        check_geometry(args.geometry_root, data_root, wrappers, results, load)
    status = {
        'contract': 'wf-table/1', 'source': 'REPORT.md', 'extracted': '2026-11-04',
        'columns': ['class', 'state', 'rules', 'bytes', 'legacy_refs', 'errors'],
        'rows': results,
    }
    (data_root / 'collection-status.json').write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + '\n'
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))
    if len(wrappers) == 240 and not any(r.get('errors') for r in results):
        path = data_root / 'effective-rules.json'
        index = {
            'contract': 'wf-table/1', 'source': 'REPORT.md', 'extracted': '2026-11-04',
            'columns': ['class_id', 'rule_id', 'tier', 'effective_scope',
                        'stable_subtype', 'payload_sha256', 'legacy_reference',
                        'draft_path', 'draft_rule_id'],
            'rows': [],
        }
        path.write_text(json.dumps(index, ensure_ascii=False))
        table = load(str(path))
        for wrapper in wrappers:
            table.add(wrapper)
        table.save()
        print('240 effective rules collected', path.stat().st_size)
    if any(r.get('state') == 'pending' or r.get('errors') for r in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
