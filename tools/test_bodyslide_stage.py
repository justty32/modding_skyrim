"""bodyslide_stage tests on a synthetic MO2 tree (fixture bytes are markers, not meshes)."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from bodyslide_stage import main, parse_modlist, Fatal
from bodyslide_outfit_plan import plan

ENV_KEYS = ('MO2_DIR', 'MO2_MODS_DIR', 'MO2_OVERWRITE_DIR', 'SKYRIM_GAME_DATA', 'SKYRIM_REPO')


def osp(name, stem):
    return (f'<SliderSetInfo version="1"><SliderSet name="{name}"><DataFolder>Body</DataFolder>'
            f'<SourceFile>body.nif</SourceFile><OutputPath>meshes\\armor</OutputPath>'
            f'<OutputFile>{stem}</OutputFile><Shape target="Body">Body</Shape>'
            f'<Slider name="T"><Data target="Body" local="true">body.osd\\T</Data></Slider>'
            f'</SliderSet></SliderSetInfo>')


def snapshot(root):
    """Every path (incl. dirs and symlinks) with its bytes, mode and mtime."""
    state = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in dirnames + filenames:
            p = Path(dirpath, name)
            st = os.lstat(p)
            data = os.readlink(p) if p.is_symlink() else (p.read_bytes() if p.is_file() else None)
            state[str(p.relative_to(root))] = (data, st.st_mode, st.st_mtime_ns)
    return state


class StageTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.mods = self.base / 'mo2' / 'mods'
        self.over = self.base / 'mo2' / 'overwrite'
        self.prof = self.base / 'mo2' / 'profiles' / 'p'
        for d in (self.mods, self.over, self.prof):
            d.mkdir(parents=True)
        self.work = self.base / 'work'
        self.work.mkdir()
        self.out = self.work / 'BodySlide'
        env = mock.patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        for key in ENV_KEYS:
            os.environ.pop(key, None)

    def put(self, mod, rel, data=b'x', root='CalienteTools/BodySlide'):
        base = self.over if mod is None else self.mods / mod
        path = base / root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if isinstance(data, bytes) else data.encode())
        return path

    def modlist(self, *lines, crlf=True, bom=True):
        text = ('\r\n' if crlf else '\n').join(lines) + '\r\n'
        (self.prof / 'modlist.txt').write_bytes(('﻿' if bom else '').encode() + text.encode())

    def run_cli(self, *extra, out=None, overwrite=True):
        argv = ['--mods-dir', str(self.mods), '--profile-dir', str(self.prof),
                '--out', str(out or self.out), *extra]
        if overwrite:
            argv += ['--overwrite-dir', str(self.over)]
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            code = main(argv)
        return code, json.loads(buf.getvalue())

    def table(self, path=None):
        return json.loads(Path(path or str(self.out) + '.sources.json').read_text(encoding='utf-8'))

    def test_modlist_semantics(self):
        enabled, disabled = parse_modlist(
            '﻿# comment\r\n+High\r\n-Off\r\n*DLC: Dawnguard\r\n+Group_separator\r\n\r\n+Low\r\n'.encode())
        self.assertEqual((enabled, disabled), (['High', 'Low'], 1))
        with self.assertRaises(Fatal):
            parse_modlist(b'?weird\n')
        with self.assertRaises(Fatal):
            parse_modlist(b'+../escape\n')

    def test_priority_case_merge_copy_and_read_only(self):
        self.modlist('+High', '-Disabled', '*Unmanaged', '+Sep_separator', '+Gone', '+Low')
        self.put('High', 'slidersets/a.osp', osp('A', 'a'))
        self.put('High', 'ShapeData/Body/body.osd', 'high osd')
        self.put('Low', 'SliderSets/b.osp', osp('B', 'b'))
        self.put('Low', 'shapedata/body/body.osd', 'low osd')
        self.put('Low', 'shapedata/body/body.nif', 'nif')
        self.put('Low', 'ShapeData/Body/same.txt', 'same')
        self.put('High', 'ShapeData/Body/same.txt', 'same')
        self.put('Disabled', 'SliderSets/disabled.osp', 'off')
        self.put(None, 'ShapeData/Body/body.osd', 'overwrite osd')
        before = snapshot(self.base / 'mo2')
        code, report = self.run_cli()
        self.assertEqual(code, 0, report)
        self.assertEqual(before, snapshot(self.base / 'mo2'))
        t = self.table()
        self.assertEqual(t['contract'], 'wf-table/1')
        rows = {r['staged_rel']: r for r in t['rows']}
        self.assertEqual(sorted(rows), ['ShapeData/Body/body.nif', 'ShapeData/Body/body.osd',
                                        'ShapeData/Body/same.txt', 'SliderSets/a.osp', 'SliderSets/b.osp'])
        osd = rows['ShapeData/Body/body.osd']
        self.assertEqual((osd['winner_mod'], osd['providers']), ('(overwrite)', 3))
        self.assertEqual(rows['SliderSets/a.osp']['winner_rel'], 'CalienteTools/BodySlide/slidersets/a.osp')
        over = {o['staged_rel']: o for o in t['overrides']}
        self.assertFalse(over['ShapeData/Body/body.osd']['identical'])
        self.assertTrue(over['ShapeData/Body/same.txt']['identical'])
        self.assertEqual([p['mod'] for p in over['ShapeData/Body/body.osd']['providers']],
                         ['(overwrite)', 'High', 'Low'])
        s = t['summary']
        self.assertEqual(s['missing_mod_dirs'], ['Gone'])
        self.assertEqual((s['enabled_mods'], s['files'], s['overrides_differing']), (3, 5, 1))
        self.assertEqual(s['overrides_differing_mods'], ['(overwrite)', 'High', 'Low'])
        self.assertIn('slidersets', json.dumps(s['case_variants']))
        # Output tree: one casing per casefold path, real copies with matching hashes.
        seen = {}
        for dirpath, dirnames, filenames in os.walk(self.out):
            for name in dirnames + filenames:
                rel = str(Path(dirpath, name).relative_to(self.out))
                self.assertNotIn(rel.casefold(), seen, f'{rel} vs {seen.get(rel.casefold())}')
                seen[rel.casefold()] = rel
        for rel, row in rows.items():
            dst = self.out / rel
            self.assertFalse(dst.is_symlink())
            self.assertEqual(dst.stat().st_nlink, 1)
            self.assertEqual(hashlib.sha256(dst.read_bytes()).hexdigest(), row['sha256'])
        self.assertEqual((self.out / 'ShapeData/Body/body.osd').read_text(), 'overwrite osd')
        # The planner sees both projects that came from different casings.
        self.assertEqual(plan(self.out, ['A'])['projects'][0]['missing_sources'], [])
        self.assertEqual(sorted(plan(self.out, ['A', 'B'])['errors']), [])

    def test_mohidden_and_symlinks_excluded(self):
        self.modlist('+M')
        self.put('M', 'SliderSets/keep.osp')
        self.put('M', 'SliderSets/old.osp.mohidden')
        self.put('M', 'ShapeData/Old.mohidden/a.nif')
        self.put('M', 'ShapeData/Old.mohidden/b.nif')
        target = self.put('M', 'outside.nif', root='elsewhere')
        link = self.mods / 'M/CalienteTools/BodySlide/ShapeData/link.nif'
        link.symlink_to(target)
        (self.mods / 'M/CalienteTools/BodySlide/LinkedDir').symlink_to(target.parent, target_is_directory=True)
        code, report = self.run_cli('--dry-run')
        self.assertEqual(code, 1)
        self.assertFalse(self.out.exists())
        s = self.table()['summary']
        self.assertEqual(s['mohidden_excluded'], 3)
        self.assertEqual(s['files'], 1)
        self.assertEqual(len(s['errors']), 2)

    def test_case_variants_inside_one_mod_fail_closed(self):
        self.modlist('+M')
        self.put('M', 'SliderSets/a.osp')
        self.put('M', 'SliderSets/b.osp', root='CalienteTools/Bodyslide')
        code, report = self.run_cli()
        self.assertEqual(code, 2)
        self.assertIn('ambiguous', report['errors'][0])
        self.assertFalse(self.out.exists())
        self.assertFalse(Path(str(self.out) + '.sources.json').exists())
        (self.mods / 'M/CalienteTools/Bodyslide/SliderSets/b.osp').unlink()
        (self.mods / 'M/CalienteTools/Bodyslide/SliderSets').rmdir()
        (self.mods / 'M/CalienteTools/Bodyslide').rmdir()
        self.put('M', 'sliderSets/A.OSP')
        code, report = self.run_cli()
        self.assertEqual(code, 2)
        self.assertIn('ambiguous', report['errors'][0])

    def test_file_versus_directory_fail_closed(self):
        self.modlist('+A', '+B')
        self.put('A', 'ShapeData/Body')
        self.put('B', 'shapedata/body/x.nif')
        code, report = self.run_cli()
        self.assertEqual(code, 2)
        self.assertIn('file in one source', report['errors'][0])

    def test_guard_refusals(self):
        self.modlist('+M')
        self.put('M', 'SliderSets/a.osp')
        cases = [
            ('out inside mods', ['--table', str(self.work / 't.json')], self.mods / 'staged'),
            ('out contains mods', ['--table', str(self.work / 't.json')], self.base / 'mo2'),
            ('table inside out', ['--table', str(self.out / 't.json')], None),
            ('table inside overwrite', ['--table', str(self.over / 't.json')], None),
            ('table inside profile', ['--table', str(self.prof / 't.json')], None),
        ]
        for label, extra, out in cases:
            with self.subTest(label):
                before = snapshot(self.base)
                code, report = self.run_cli(*extra, out=out)
                self.assertEqual(code, 2, report)
                self.assertEqual(before, snapshot(self.base))
        code, report = self.run_cli(overwrite=False)
        self.assertEqual(code, 2)
        self.assertIn('overwrite', report['errors'][0])
        os.environ['MO2_OVERWRITE_DIR'] = str(self.over)
        self.assertEqual(self.run_cli('--dry-run', overwrite=False)[0], 0)
        self.out.mkdir()
        (self.out / 'stale').write_text('x')
        code, report = self.run_cli()
        self.assertEqual(code, 2)
        self.assertIn('empty directory', report['errors'][0])

    def test_missing_inputs_exit_2(self):
        code, report = self.run_cli()
        self.assertEqual(code, 2)
        self.assertIn('modlist.txt', report['errors'][0])
        self.modlist('+M')
        code, report = self.run_cli('--overwrite-dir', str(self.base / 'nope'), overwrite=False)
        self.assertIn('--overwrite-dir', report['errors'][0])
        self.assertEqual(code, 2)

    def test_capacity_gate(self):
        self.modlist('+M')
        self.put('M', 'SliderSets/a.osp', b'12345')
        self.put('M', 'SliderSets/b.osp', b'12345')
        for extra in (['--max-files', '1'], ['--max-bytes', '9']):
            with self.subTest(extra):
                code, report = self.run_cli(*extra)
                self.assertEqual(code, 2)
                self.assertIn('capacity', report['errors'][0])
                self.assertFalse(self.out.exists())
                self.assertFalse(self.table()['summary']['capacity']['ok'])
        self.assertEqual(self.run_cli('--max-files', '2', '--max-bytes', '10')[0], 0)

    def test_shapedata_filter_and_dry_run(self):
        self.modlist('+M')
        self.put('M', 'SliderSets/a.osp')
        self.put('M', 'ShapeData/CBBE/a.nif')
        self.put('M', 'ShapeData/Other/b.nif')
        self.put('M', 'ShapeData/loose.txt')
        code, _ = self.run_cli('--shapedata-folder', 'cbbe')
        self.assertEqual(code, 0)
        copied = {r['staged_rel']: r['copied'] for r in self.table()['rows']}
        self.assertEqual(copied, {'ShapeData/CBBE/a.nif': True, 'ShapeData/Other/b.nif': False,
                                  'ShapeData/loose.txt': False, 'SliderSets/a.osp': True})
        self.assertTrue((self.out / 'ShapeData/CBBE/a.nif').is_file())
        self.assertFalse((self.out / 'ShapeData/Other').exists())
        out2 = self.work / 'second'
        code, _ = self.run_cli('--no-shapedata', '--dry-run', out=out2)
        self.assertEqual(code, 0)
        self.assertFalse(out2.exists())
        rows = self.table(str(out2) + '.sources.json')['rows']
        self.assertEqual([r['staged_rel'] for r in rows if r['copied']], ['SliderSets/a.osp'])

    def test_known_top_level_folder_gets_canonical_case(self):
        self.modlist('+Lower')
        self.put('Lower', 'slidersets/sub/X.osp')
        self.put('Lower', 'reftemplates/t.xml')
        self.assertEqual(self.run_cli()[0], 0)
        self.assertEqual(sorted(r['staged_rel'] for r in self.table()['rows']),
                         ['RefTemplates/t.xml', 'SliderSets/sub/X.osp'])
        self.assertTrue((self.out / 'SliderSets/sub/X.osp').is_file())

    def test_post_copy_hash_mismatch_fails_closed(self):
        self.modlist('+M')
        self.put('M', 'SliderSets/a.osp', b'good')
        corrupt = lambda src, dst, **kw: Path(dst).write_bytes(b'corrupt')  # noqa: E731
        with mock.patch('bodyslide_stage.shutil.copy2', side_effect=corrupt):
            code, report = self.run_cli()
        self.assertEqual(code, 2)
        self.assertIn('verification failed', report['errors'][0])

    def test_build_selection_and_config_reported(self):
        self.modlist('+App', '+Mod')
        self.put('App', 'Config.xml', '<Config/>')
        self.put(None, 'BuildSelection.xml', '<BuildSelection><OutputChoice/></BuildSelection>')
        code, report = self.run_cli('--dry-run')
        self.assertEqual(code, 1)
        s = self.table()['summary']
        self.assertEqual(s['build_selection'][0]['mod'], '(overwrite)')
        self.assertIn('OutputChoice', s['build_selection'][0]['head'])
        self.assertEqual(s['config_xml']['mod'], 'App')
        self.assertTrue(s['attention'])


if __name__ == '__main__':
    unittest.main()
