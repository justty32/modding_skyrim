#!/usr/bin/env python3
"""Render class-local SVGs from published tables only; no raw graph, allocator or runtime.

One-hop context is clipped; node coordinates and edges are never rearranged.
Render SVG to PNG separately with existing rsvg-convert if desired.
"""

import argparse

import html

from pathlib import Path

import sys

import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    parser.add_argument('--tabledb-dir',
         type=Path,
         help='directory containing tabledb.py; auto-detected in repository')
    a = parser.parse_args()
    folder = a.tabledb_dir
    if folder is None:
        folder = next((p / 'wf/tools' for p in Path(__file__).resolve().parents if (p / 'wf/tools/tabledb.py').is_file()),
             None)
    if folder is None:
        parser.error('supply --tabledb-dir outside the repository')
    sys.path.insert(0, str(folder))
    from tabledb import load
    src = a.data_root.resolve()
    out = a.output_root.resolve()
    out.mkdir(parents=True, exist_ok=True)
    reservation = load(str(src / 'reservation.json')).rows
    profiles = load(str(src / 'subtypes.json')).rows
    for cl in 'VGDRCMSX':
        f = out / f'region-{cl}.svg'
        rr = load(str(src / f'region-{cl}.json')).rows
        by = {r['id']: r for r in rr}
        rules = {r['node_id']: r for r in reservation if r['class'] == cl}
        connectors = {i for r in profiles if r['class'] == cl for i in r['ordinary_connector_ids']}
        selected = set(rules) | connectors
        anchors = {i for i, r in by.items() if r['type'] == 'start' and set(r['neighbors']) & selected}
        selected |= anchors
        assert all((i in by for i in selected))
        xy = [by[i]['position'] for i in selected]
        minx = min((x for x, y in xy)) - 220
        maxx = max((x for x, y in xy)) + 650
        miny = min((y for x, y in xy)) - 250
        maxy = max((y for x, y in xy)) + 230
        width = maxx - minx
        height = maxy - miny
        boundary = {e for i in selected for e in by[i]['neighbors'] if e in by} - selected
        visible = selected | {i for i in boundary if by[i]['position'] and minx <= by[i]['position'][0] <= maxx and (miny <= by[i]['position'][1] <= maxy)}
        svg = [(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{minx} {miny} {width} {height}" role="img">'
            f'<title>Class {cl}: local window; original node coordinates and edges; context clipped</title>'
            f'<defs>'
            f'<clipPath id="window">'
            f'<rect x="{minx}" y="{miny}" width="{width}" height="{height}"/>'
            f'</clipPath>'
            f'</defs>'
            f'<rect x="{minx}" y="{miny}" width="{width}" height="{height}" fill="#101723"/>'
            f'<g clip-path="url(#window)">'
        )]
        edges = 0
        for i in sorted(selected | boundary):
            if i not in by or not by[i]['position']:
                continue
            for e in by[i]['neighbors']:
                if e <= i or e not in by or (not by[e]['position']) or (not {i, e} & selected):
                    continue
                x, y = by[i]['position']
                a, b = by[e]['position']
                svg.append(f'<line x1="{x}" y1="{y}" x2="{a}" y2="{b}" stroke="#536475" stroke-width="9" data-edge="{i}-{e}"/>')
                edges += 1
        for i in sorted(visible):
            r = by[i]
            x, y = r['position']
            rule = rules.get(i)
            color = '#f3c355' if rule and rule['tier'] == 'high' else '#59d1ae' if rule else '#d6deea' if i in anchors else '#90a6bd' if i in selected else '#364252'
            label = rule['slot'] if rule else str(i)
            size = 60 if rule else 43
            svg.append((
                f'<g data-node="{i}" data-selected="{str(i in selected).lower()}">'
                f'''<circle cx="{x}" cy="{y}" r="{(38 if rule and rule['tier'] == 'high' else 21)}" fill="{color}"/>'''
                f'<text x="{x + 35}" y="{y - 7}" font-size="{size}" fill="#e7edf5" paint-order="stroke" stroke="#101723" stroke-width="5">{html.escape(label)}</text>'
                f'</g>'
            ))
        svg.append((
            f'</g>'
            f'<rect x="{minx}" y="{miny}" width="{width}" height="140" fill="#101723"/>'
            f'<text x="{minx + 30}" y="{miny + 75}" font-size="55" fill="#e7edf5">Class {cl} | local window | 30 rules | {len(connectors)} ordinary | context clipped</text>'
            f'</svg>'
        ))
        text = '\n'.join(svg)
        ET.fromstring(text)
        f.write_text(text)
    print('Rendered 8 class-local SVGs from published tables; no layout or source-data edits.')


if __name__ == '__main__':
    main()
