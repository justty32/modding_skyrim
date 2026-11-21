#!/usr/bin/env python3
"""Read-only Skyrim SE OSP v1 preflight; never builds or resolves MO2 winners.

Example: python tools/bodyslide_outfit_plan.py --staging /isolated/BodySlide \
  --project 'Exact XML project name' [--project 'Another project'] [--tri]

Rules: ousnius/BodySlide-and-Outfit-Studio commit
033016464d31761bfaf6966db3ea9c3c3cb6105a:
src/components/SliderSet.cpp LoadSliderSet, GetInputFileName,
GetOutputFilePath, ResolveSliderDataFile; src/program/BodySlideApp.cpp
BuildBodies (NIF suffixes and conditional TRI creation).
"""
import argparse
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


LIMITS = [
    'Input must already be a merged staging; no MO2, archives or winner discovery.',
    'Only .osp files under SliderSets are scanned; other project formats unverified.',
    'Only standalone OSP version 1 SliderSet projects; inheritance/add-ons rejected.',
    'Source presence only: NIF/OSD/BSD validity, OSD member names and geometry unverified.',
    'No preset/group/slider/zap compatibility or runtime/OBody validation.',
    'TRI paths are conditional candidates, not guaranteed files; morph content unverified.',
    'Output paths assume Skyrim SE normal batch build into a fresh isolated directory.',
    'Official pinned rules are not proof of equivalence to a local development binary.',
]


def relative(value, allow_empty=False):
    value = value.replace('\\', '/')
    parts = value.split('/')
    if (not value and not allow_empty) or value.startswith('/') or any(
        p == '..' or ':' in p or any(c in p for c in '<>"|?*') for p in parts
    ):
        raise ValueError(f'unsafe or empty relative path: {value!r}')
    if any(p.endswith((' ', '.')) and p not in ('', '.') for p in parts):
        raise ValueError(f'Windows trailing space/dot path unsupported: {value!r}')
    return '/'.join(p for p in parts if p not in ('', '.'))


def present(root, rel):
    """Resolve Windows-style case insensitivity without silently choosing collisions."""
    node = root
    for part in relative(rel).split('/'):
        if not node.is_dir():
            return False
        matches = [p for p in node.iterdir() if p.name.casefold() == part.casefold()]
        if len(matches) > 1:
            raise ValueError(f'ambiguous case-insensitive source: {rel}')
        if not matches:
            return False
        node = matches[0]
        if not node.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'source symlink escapes staging: {rel}')
    return node.is_file()


def boolean(element, name, default):
    value = element.get(name)
    if value is None:
        return default
    if value not in ('true', 'false', '1', '0'):
        raise ValueError(f'unsupported {name} boolean: {value!r}')
    return value in ('true', '1')


def describe(element, osp, tri):
    if element.tag != 'SliderSet' or element.find('BaseProject') is not None:
        raise ValueError('inheritance/add-on project unsupported')
    def text(tag, empty=False):
        value = element.findtext(tag)
        if value is None or (not value and not empty):
            raise ValueError(f'missing {tag}')
        return value
    shapes = element.findall('Shape')
    shape_names = [shape.text for shape in shapes]
    targets = [shape.get('target', shape.text) for shape in shapes]
    if len(set(shape_names)) != len(shape_names) or len(set(targets)) != len(targets):
        raise ValueError('duplicate Shape names or shared targets unsupported (upstream map merging/order)')
    folder = relative(text('DataFolder'), allow_empty=True)
    source = relative(text('SourceFile'))
    output = relative(text('OutputPath', True), allow_empty=True)
    name = relative(text('OutputFile'))
    if '/' in name:
        raise ValueError('OutputFile must be a filename stem')
    out = element.find('OutputFile')
    weights = boolean(out, 'GenWeights', True)
    prevent = boolean(out, 'PreventMorphFile', False)
    stem = '/'.join(p for p in (output, name) if p)
    outputs = [stem + suffix for suffix in (('_0.nif', '_1.nif') if weights else ('.nif',))]
    conditional = [stem + '.tri'] if tri and not prevent else []
    sources = {'/'.join(p for p in ('ShapeData', folder, source) if p)}
    for data in element.findall('./Slider/Data'):
        value = data.text or ''
        local = boolean(data, 'local', False)
        folders = [folder]
        if not local:
            for shape in element.findall('Shape'):
                if shape.get('target', shape.text) == data.get('target'):
                    folders = shape.get('DataFolder', folder).split(';')
                    break
        normalized = value.replace('\\', '/')
        if normalized.lower().endswith('.bsd'):
            filename = normalized
        elif '/' in normalized:
            filename, member = normalized.rsplit('/', 1)
            if not member:
                raise ValueError(f'missing OSD member: {value!r}')
        else:
            raise ValueError(f'unrecognized slider data reference: {value!r}')
        # Keep ordered alternatives together; one existing folder is sufficient.
        sources.add(tuple('/'.join(p for p in ('ShapeData', relative(f, True), relative(filename)) if p)
                          for f in folders))
    return dict(project=element.get('name'), osp=osp, outputs=outputs,
                conditional_outputs=conditional, source_candidates=[list(s) if isinstance(s, tuple) else [s]
                                                                     for s in sorted(sources, key=str)])


def plan(staging, selected, tri=False):
    if not (staging / 'SliderSets').is_dir():
        raise ValueError('staging must contain SliderSets/')
    catalog = {}
    errors = []
    for osp in sorted((staging / 'SliderSets').rglob('*')):
        if not osp.is_file() or osp.suffix.lower() != '.osp':
            continue
        if not osp.resolve().is_relative_to(staging.resolve()):
            raise ValueError(f'OSP symlink escapes staging: {osp}')
        try:
            root = ET.parse(osp).getroot()
            if root.tag != 'SliderSetInfo' or root.get('version') != '1':
                raise ValueError('expected SliderSetInfo version="1"')
            for element in root:
                if element.tag in ('SliderSet', 'SliderSetAddOn'):
                    catalog.setdefault(element.get('name', ''), []).append((element, str(osp.relative_to(staging))))
        except (ET.ParseError, ValueError) as exc:
            errors.append(f'{osp.relative_to(staging)}: {exc}')
    rows = []
    for name in dict.fromkeys(selected):
        matches = catalog.get(name, [])
        if len(matches) != 1:
            errors.append(f'{name}: expected one exact project, found {len(matches)}')
            continue
        try:
            row = describe(*matches[0], tri)
            row['missing_sources'] = [paths for paths in row['source_candidates']
                                      if not any(present(staging, p) for p in paths)]
            if row['missing_sources']:
                errors.append(f'{name}: missing source files')
            rows.append(row)
        except ValueError as exc:
            errors.append(f'{name}: {exc}')
    owners = {}
    for row in rows:
        for path in row['outputs'] + row['conditional_outputs']:
            owners.setdefault(path.casefold(), []).append(row['project'])
    conflicts = [{'output': path, 'projects': names} for path, names in owners.items() if len(names) > 1]
    if conflicts:
        errors.append('selected projects have overlapping output paths')
    alternatives = []
    uninspected = []
    for name, matches in catalog.items():
        if name in selected:
            continue
        for element, osp in matches:
            try:
                row = describe(element, osp, tri)
                overlap = [p for p in row['outputs'] + row['conditional_outputs'] if p.casefold() in owners]
                if overlap:
                    alternatives.append(dict(project=name, osp=osp, overlapping_outputs=overlap))
            except ValueError as exc:
                uninspected.append(dict(project=name, osp=osp, reason=str(exc)))
    return dict(ok=not errors, projects=rows, conflicts=conflicts,
                unselected_variants=alternatives, uninspected_projects=uninspected,
                errors=errors, limitations=LIMITS)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--staging', type=Path, required=True, help='already merged isolated BodySlide resource root (read only)')
    parser.add_argument('--project', action='append', required=True, help='exact XML name; repeat for each selected project')
    parser.add_argument('--tri', action='store_true', help='include conditional TRI collision candidates')
    args = parser.parse_args(argv)
    try:
        report = plan(args.staging, args.project, args.tri)
    except (OSError, ValueError) as exc:
        print(json.dumps({'ok': False, 'errors': [str(exc)]}))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
