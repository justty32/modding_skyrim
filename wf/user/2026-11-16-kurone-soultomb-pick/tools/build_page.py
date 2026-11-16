#!/usr/bin/env python3
"""Inject the wf-table/1 tables into page-template.html -> one offline HTML file.

Usage: python3 -I build_page.py DATA_DIR TEMPLATE OUT.html
"""
import json, sys
from pathlib import Path


def rows(d, n):
    return json.load(open(Path(d) / f"{n}.json", encoding="utf-8"))["rows"]


def main(data_dir, template, out):
    donors, dx = rows(data_dir, "donors"), rows(data_dir, "donors-excluded")
    targets, tx = rows(data_dir, "targets"), rows(data_dir, "targets-excluded")
    bodies = rows(data_dir, "bodies")
    meta = json.load(open(Path(data_dir) / "donors.json", encoding="utf-8"))
    data = {
        "meta": {"extracted": meta["extracted"], "profile": "modpack-main",
                 "donor_mod": "Kurone Soul Tomb 2.0fix9 + Update Patch 2.0Fix15 + Teleport Add-on 2.1（CHS 層贏家）",
                 "counts": {"donors": len(donors), "donors_excluded": len(dx),
                            "targets": len(targets), "targets_excluded": len(tx)}},
        "donors": donors, "donors_excluded": dx, "targets": targets, "targets_excluded": tx, "bodies": bodies,
    }
    blob = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    html = Path(template).read_text(encoding="utf-8")
    ph = "__PICK_DATA__"
    if html.count(ph) != 1:
        sys.exit(f"template must contain {ph} exactly once (found {html.count(ph)})")
    Path(out).write_text(html.replace(ph, blob), encoding="utf-8")
    print(out, len(html) + len(blob), "bytes")


if __name__ == "__main__":
    main(*sys.argv[1:4])
