"""Render review-only HTML from per-class tables; no game or source mutations."""
from pathlib import Path
import argparse
import sys
from review_content import render_content
from review_page import render_page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data-root', type=Path, default=Path(__file__).parent)
    ap.add_argument('--repo-root', type=Path, default=Path.cwd())
    ap.add_argument('--output', type=Path)
    ap.add_argument('--geometry-root', type=Path)
    ap.add_argument('--semantics-pass', action='store_true')
    ap.add_argument('--geometry-verified', action='store_true')
    args = ap.parse_args()
    B = args.data_root.resolve()
    repo = args.repo_root.resolve()
    out = (args.output or B / 'REVIEW.html').resolve()
    sys.path.insert(0, str(repo / 'wf/tools'))
    from tabledb import load
    nav, intro, parts = render_content(B, repo, out, args.geometry_root, load)
    page = render_page(nav, intro, parts, args.semantics_pass, args.geometry_verified)
    out.write_text(page)
    assert out.stat().st_size <= 1024 ** 2
    print('HTML bytes', out.stat().st_size)


if __name__ == '__main__':
    main()
