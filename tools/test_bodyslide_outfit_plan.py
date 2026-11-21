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

    def write(self, name='A', stem='body', attrs='', extra=''):
        xml = f'''<SliderSetInfo version="1"><SliderSet name="{name}">
<DataFolder>Body</DataFolder><SourceFile>body.nif</SourceFile>
<OutputPath>meshes\\armor</OutputPath><OutputFile {attrs}>{stem}</OutputFile>
<Shape target="Body">Body</Shape><Slider name="Test"><Data target="Body" local="true">body.osd\\Test</Data></Slider>
{extra}</SliderSet></SliderSetInfo>'''
        (self.root / 'SliderSets' / f'{name}.osp').write_text(xml)

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
        self.assertFalse(plan(self.root, ['A'])['ok'])

    def test_source_case_ambiguity_rejected(self):
        self.write()
        (self.root / 'ShapeData' / 'Body' / 'BODY.NIF').write_bytes(b'collision')
        self.assertIn('ambiguous', plan(self.root, ['A'])['errors'][0])


if __name__ == '__main__':
    unittest.main()
