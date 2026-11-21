"""Isolated OSP preflight tests; fixture bytes are presence markers, not meshes."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from bodyslide_outfit_plan import main, plan


class OutfitPlanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'SliderSets').mkdir()
        (self.root / 'ShapeData' / 'Body').mkdir(parents=True)
        for name in ('body.nif', 'body.osd'):
            (self.root / 'ShapeData' / 'Body' / name).write_bytes(b'presence only')

    def write(self, name='A', stem='body', attrs='', extra='', folder='SliderSets'):
        xml = f'''<SliderSetInfo version="1"><SliderSet name="{name}">
<DataFolder>Body</DataFolder><SourceFile>body.nif</SourceFile>
<OutputPath>meshes\\armor</OutputPath><OutputFile {attrs}>{stem}</OutputFile>
<Shape target="Body">Body</Shape><Slider name="Test"><Data target="Body" local="true">body.osd\\Test</Data></Slider>
{extra}</SliderSet></SliderSetInfo>'''
        (self.root / folder / f'{name}.osp').write_text(xml)

    def test_success_and_no_mutation(self):
        self.write()
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = plan(self.root, ['A'], True)
        self.assertTrue(result['ok'])
        self.assertEqual(result['projects'][0]['outputs'], ['meshes/armor/body_0.nif', 'meshes/armor/body_1.nif'])
        self.assertEqual(result['projects'][0]['conditional_outputs'], ['meshes/armor/body.tri'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_single_weight_prevent_morph_and_literal_stem(self):
        self.write(stem='body.nif', attrs='GenWeights="false" PreventMorphFile="true"')
        row = plan(self.root, ['A'], True)['projects'][0]
        self.assertEqual(row['outputs'], ['meshes/armor/body.nif.nif'])
        self.assertEqual(row['conditional_outputs'], [])

    def test_conflict_and_unselected_variant(self):
        self.write()
        self.write('B', 'BODY')
        self.assertTrue(plan(self.root, ['A'])['unselected_variants'])
        report = plan(self.root, ['A', 'B'])
        self.assertFalse(report['ok'])
        self.assertEqual(len(report['conflicts']), 2)

    def test_actual_output_collision_across_weight_modes(self):
        self.write()
        self.write('B', 'body_0', 'GenWeights="false"')
        self.assertFalse(plan(self.root, ['A', 'B'])['ok'])

    def test_missing_source_and_invalid_name_exit_nonzero(self):
        self.write()
        (self.root / 'ShapeData' / 'Body' / 'body.osd').unlink()
        for name in ('A', 'no such project'):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                code = main(['--staging', str(self.root), '--project', name])
            self.assertEqual(code, 1)
            self.assertFalse(json.loads(output.getvalue())['ok'])

    def test_duplicate_name_and_inheritance_rejected(self):
        self.write(extra='<BaseProject ProjectName="Base"/>')
        self.assertIn('unsupported', plan(self.root, ['A'])['errors'][0])
        (self.root / 'SliderSets' / 'duplicate.osp').write_bytes((self.root / 'SliderSets' / 'A.osp').read_bytes())
        self.assertIn('found 2', plan(self.root, ['A'])['errors'][0])

    def test_nonlocal_shape_folder_alternatives(self):
        self.write()
        path = self.root / 'SliderSets' / 'A.osp'
        path.write_text(path.read_text().replace('<Shape target="Body">', '<Shape target="Body" DataFolder="Missing;Body">').replace('local="true"', 'local="false"'))
        self.assertTrue(plan(self.root, ['A'])['ok'])

    def test_missing_shape_override_does_not_fall_back_to_project_folder(self):
        self.write()
        path = self.root / 'SliderSets' / 'A.osp'
        path.write_text(path.read_text().replace('<Shape target="Body">', '<Shape target="Body" DataFolder="Shared">').replace('local="true"', 'local="false"'))
        result = plan(self.root, ['A'])
        self.assertFalse(result['ok'])
        self.assertEqual(result['projects'][0]['missing_sources'], [['ShapeData/Shared/body.osd']])

    def test_shared_target_and_duplicate_shape_are_rejected(self):
        for shape in ('<Shape target="Body" DataFolder="Missing">A</Shape>',
                      '<Shape target="Other" DataFolder="Missing">Body</Shape>'):
            self.write(extra=shape)
            result = plan(self.root, ['A'])
            self.assertFalse(result['ok'])
            self.assertIn('duplicate Shape', result['errors'][0])

    def test_malformed_xml_and_path_escape_fail_closed(self):
        self.write(stem='../escape')
        self.assertFalse(plan(self.root, ['A'])['ok'])
        self.write()
        (self.root / 'SliderSets' / 'bad.osp').write_text('<')
        # F8: an unrelated unparseable OSP no longer flips the selected project's ok,
        # but the variant check is marked incomplete and the error is kept.
        report = plan(self.root, ['A'])
        self.assertTrue(report['ok'])
        self.assertFalse(report['variant_check_complete'])
        self.assertTrue(report['warnings'])
        self.assertIn('bad.osp', report['catalog_errors'][0])
        (self.root / 'SliderSets' / 'A.osp').write_text('<SliderSetInfo version="1"><SliderSet name="A">')
        self.assertIn('found 0', plan(self.root, ['A'])['errors'][0])  # selected OSP unreadable

    def test_source_case_ambiguity_rejected(self):
        self.write()
        (self.root / 'ShapeData' / 'Body' / 'BODY.NIF').write_bytes(b'collision')
        self.assertIn('ambiguous', plan(self.root, ['A'])['errors'][0])

    def test_root_version_gate(self):
        self.write()
        path = self.root / 'SliderSets' / 'A.osp'
        path.write_text(path.read_text().replace('version="1"', 'version="2"'))
        report = plan(self.root, ['A'])
        self.assertFalse(report['ok'])
        self.assertIn('found 0', report['errors'][0])
        self.assertIn('version="1"', report['catalog_errors'][0])
        path.write_text(path.read_text().replace('<SliderSetInfo version="2">', '<SliderSetInfo>'))
        self.assertIn('version="1"', plan(self.root, ['A'])['catalog_errors'][0])

    def test_lowercase_slidersets_root_is_scanned(self):
        (self.root / 'SliderSets').rename(self.root / 'slidersets')
        (self.root / 'ShapeData').rename(self.root / 'shapedata')
        self.write(folder='slidersets')
        self.write('B', folder='slidersets')  # same output -> must be seen as a variant
        report = plan(self.root, ['A'])
        self.assertTrue(report['ok'], report['errors'])
        self.assertEqual([v['project'] for v in report['unselected_variants']], ['B'])

    def test_both_slidersets_case_variants_fail_closed(self):
        self.write()
        (self.root / 'slidersets').mkdir()
        self.write('B', folder='slidersets')
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            plan(self.root, ['A'])
        code, out = self.cli('--staging', str(self.root), '--project', 'A')
        self.assertEqual(code, 2)
        self.assertFalse(out['ok'])
        self.assertIn('ambiguous', out['errors'][0])

    def test_both_shapedata_case_variants_fail_closed(self):
        self.write()
        (self.root / 'shapedata').mkdir()
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            plan(self.root, ['A'])

    def test_symlink_staging_refused_without_crash(self):
        self.write()
        real = self.root / 'real.osp'
        (self.root / 'SliderSets' / 'A.osp').rename(real)
        (self.root / 'SliderSets' / 'A.osp').symlink_to(real)
        code, out = self.cli('--staging', str(self.root), '--project', 'A')
        self.assertEqual(code, 1)
        self.assertIn('symlinked OSP refused', out['catalog_errors'][0])
        self.assertFalse(out['variant_check_complete'])
        (self.root / 'SliderSets' / 'A.osp').unlink()
        self.write()
        nif = self.root / 'ShapeData' / 'Body' / 'body.nif'
        nif.rename(self.root / 'body.nif')
        nif.symlink_to(self.root / 'body.nif')
        report = plan(self.root, ['A'])
        self.assertFalse(report['ok'])
        self.assertIn('symlink refused', report['projects'][0]['source_error'])

    def test_cli_exit_2_on_missing_staging_roots(self):
        code, out = self.cli('--staging', str(self.root / 'nope'), '--project', 'A')
        self.assertEqual(code, 2)
        (self.root / 'SliderSets').rmdir()
        code, out = self.cli('--staging', str(self.root), '--project', 'A')
        self.assertEqual(code, 2)
        self.assertIn('SliderSets', out['errors'][0])

    def test_tri_only_conflict(self):
        self.write()
        self.write('B', 'body', 'GenWeights="false"')
        self.assertTrue(plan(self.root, ['A', 'B'])['ok'])
        report = plan(self.root, ['A', 'B'], tri=True)
        self.assertFalse(report['ok'])
        self.assertEqual([c['output'] for c in report['conflicts']], ['meshes/armor/body.tri'])

    def test_non_ascii_project_name(self):
        self.write('中文衣服', '衣服')
        code, out = self.cli('--staging', str(self.root), '--project', '中文衣服')
        self.assertEqual(code, 0)
        self.assertEqual(out['projects'][0]['project'], '中文衣服')
        self.assertEqual(out['projects'][0]['outputs'][0], 'meshes/armor/衣服_0.nif')

    def test_osd_member_in_subdirectory(self):
        self.write()
        path = self.root / 'SliderSets' / 'A.osp'
        path.write_text(path.read_text().replace('>body.osd\\Test<', '>sub\\body.osd\\Test<'))
        report = plan(self.root, ['A'])
        self.assertFalse(report['ok'])
        self.assertEqual(report['projects'][0]['missing_sources'], [['ShapeData/Body/sub/body.osd']])
        (self.root / 'ShapeData' / 'Body' / 'sub').mkdir()
        (self.root / 'ShapeData' / 'Body' / 'sub' / 'body.osd').write_bytes(b'presence only')
        self.assertTrue(plan(self.root, ['A'])['ok'])

    def test_ambiguous_source_keeps_row_for_conflicts(self):
        self.write()
        self.write('B')
        (self.root / 'ShapeData' / 'Body' / 'BODY.NIF').write_bytes(b'collision')
        report = plan(self.root, ['A', 'B'])
        self.assertFalse(report['ok'])
        self.assertEqual(len(report['projects']), 2)
        self.assertIn('ambiguous', report['projects'][0]['source_error'])
        self.assertEqual(len(report['conflicts']), 2)

    def cli(self, *argv):
        with contextlib.redirect_stdout(io.StringIO()) as output, \
                contextlib.redirect_stderr(io.StringIO()):
            code = main(list(argv))
        return code, json.loads(output.getvalue())

if __name__ == '__main__':
    unittest.main()
