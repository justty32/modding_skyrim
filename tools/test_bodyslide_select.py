"""bodyslide_select tests on synthetic OSP catalogs."""
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from bodyslide_select import (SelectError, build_selection_xml, group_xml, load_catalog,
                              norm_stem, select_batch)


def osp(*sets):
    body = ''.join(
        f'<SliderSet name="{n}"><SourceFile>s.nif</SourceFile><OutputPath>{path}</OutputPath>'
        f'<OutputFile GenWeights="{gw}"{pm}>{stem}</OutputFile><Shape target="B">B</Shape><Shape target="B">B</Shape>'
        f'<Slider name="VanillaSSEHi"/><Slider name="Zap X" zap="true"/></SliderSet>'
        for n, path, stem, gw, pm in sets)
    return f'<SliderSetInfo version="1">{body}</SliderSetInfo>'


def s(name, path, stem, gw='true', prevent=False):
    return (name, path, stem, gw, ' PreventMorphFile="true"' if prevent else '')


class SelectTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.tool = self.base / 'tool'
        (self.tool / 'SliderSets' / 'sub').mkdir(parents=True)
        files = {
            'SliderSets/ct77.osp': osp(s('CT77 Iron', 'meshes\\armor\\iron', 'CuirassF'),
                                       s('CT77 Robe', 'meshes\\clothes\\robe', 'robef')),
            'SliderSets/cbbe.osp': osp(s('CBBE Iron', 'meshes\\armor\\iron', 'cuirassf'),
                                       s('CBBE Iron (Physics)', 'meshes\\armor\\iron', 'cuirassf'),
                                       s('CBBE Boots', 'meshes\\armor\\iron', 'bootsf', 'false', True)),
            'SliderSets/sub/body.osp': osp(s('CBBE Body', 'meshes\\actors\\character\\character assets', 'femalebody'),
                                           s('CBBE Body NeverNude', 'meshes\\actors\\character\\character assets', 'femalebody')),
            'SliderSets/broken.osp': '<SliderSetInfo',
        }
        for rel, text in files.items():
            (self.tool / rel).write_text(text)
        self.table = self.base / 'stage.json'
        self.table.write_text(json.dumps({'rows': [
            {'staged_rel': 'SliderSets/ct77.osp', 'winner_mod': 'CT77 Remodeled Armor'},
            {'staged_rel': 'SliderSets/cbbe.osp', 'winner_mod': 'CBBE 2.0.3 General'},
            {'staged_rel': 'SliderSets/sub/body.osp', 'winner_mod': 'CBBE 2.0.3 General'}]}))
        self.cat, self.errors = load_catalog(self.tool, self.table)

    def test_norm_stem(self):
        self.assertEqual(norm_stem('Meshes\\Armor\\Iron\\CuirassF_1.nif'), 'meshes/armor/iron/cuirassf')
        self.assertEqual(norm_stem('armor/iron/cuirassf.nif'), 'meshes/armor/iron/cuirassf')
        self.assertEqual(norm_stem('meshes/x/y.tri'), 'meshes/x/y')

    def test_catalog(self):
        self.assertEqual(len(self.cat), 7)
        self.assertEqual(len(self.errors), 1)
        boots = next(p for p in self.cat if p['name'] == 'CBBE Boots')
        self.assertEqual(boots['outputs'], ['meshes/armor/iron/bootsf.nif'])
        self.assertIsNone(boots['tri'])
        iron = next(p for p in self.cat if p['name'] == 'CT77 Iron')
        self.assertEqual(iron['mod'], 'CT77 Remodeled Armor')
        self.assertEqual(iron['outputs'], ['meshes/armor/iron/cuirassf_0.nif', 'meshes/armor/iron/cuirassf_1.nif'])
        self.assertEqual(iron['out_path'], 'meshes\\armor\\iron\\CuirassF')
        self.assertEqual(iron['zaps'], ['Zap X'])
        with self.assertRaises(SelectError):
            load_catalog(self.base)

    def test_prefer_avoid_and_unresolved(self):
        batch = {'select': {'osp_mods': ['CBBE 2.0.3*']}, 'avoid': ['\\(Physics\\)'],
                 'prefer': ['mod:CT77', 'project:NeverNude']}
        r = select_batch(self.cat, batch)
        picked = {d['stem']: d.get('project') for d in r['decisions']}
        self.assertEqual(picked['meshes/armor/iron/cuirassf'], 'CT77 Iron')
        self.assertEqual(picked['meshes/actors/character/character assets/femalebody'], 'CBBE Body NeverNude')
        self.assertEqual(r['unresolved'], [])
        self.assertIn('meshes/armor/iron/bootsf.nif', r['expected'])
        self.assertNotIn('meshes/armor/iron/bootsf.tri', r['expected_tri'])
        r2 = select_batch(self.cat, {'select': {'stems': ['meshes/armor/iron/cuirassf_1.nif']}})
        self.assertEqual(len(r2['unresolved']), 1)
        self.assertEqual(len(r2['unresolved'][0]['left']), 3)

    def test_choose_exclude_and_errors(self):
        r = select_batch(self.cat, {'select': {'stems': ['armor/iron/cuirassf']},
                                    'choose': {'meshes/armor/iron/cuirassf': 'CBBE Iron'}})
        self.assertEqual(r['decisions'][0]['project'], 'CBBE Iron')
        r = select_batch(self.cat, {'select': {'stems': ['armor/iron/cuirassf']},
                                    'choose': {'meshes/armor/iron/cuirassf': 'Nope'}})
        self.assertTrue(r['errors'])
        r = select_batch(self.cat, {'select': {'stems': ['armor/iron/cuirassf', 'armor/none/x']},
                                    'exclude_projects': ['Iron']})
        self.assertEqual(r['decisions'][0]['project'], None)
        self.assertEqual(r['uncovered'][0]['stem'], 'meshes/armor/none/x')
        r = select_batch(self.cat, {'select': {'projects': ['CBBE Body', 'Missing']}})
        self.assertEqual([d['project'] for d in r['decisions']], ['CBBE Body'])
        self.assertEqual(len(r['errors']), 1)

    def test_replaced_layer_and_scope(self):
        layer = self.base / 'layer' / 'meshes' / 'Armor' / 'Iron'
        layer.mkdir(parents=True)
        (layer / 'CuirassF_0.nif').write_bytes(b'')
        (layer / 'GoneF_1.nif').write_bytes(b'')
        r = select_batch(self.cat, {'select': {'stems_from_dirs': [str(self.base / 'layer')]},
                                    'prefer': ['mod:CT77']})
        self.assertEqual([d['project'] for d in r['decisions']], ['CT77 Iron'])
        self.assertIn('replaced layer', r['errors'][0])
        scope = self.base / 'scope.json'
        scope.write_text(json.dumps({'rows': [
            {'mesh': 'meshes/clothes/robe/robef_1.nif', 'winner_mod': 'CT77 Out|x'},
            {'mesh': 'meshes/armor/iron/cuirassf_1.nif', 'winner_mod': 'Other'}]}))
        r = select_batch(self.cat, {'select': {'scope': {'table': 'scope.json', 'where': {'winner_mod': ['CT77*']}}},
                                    'exclude_stems': []}, base=self.base)
        self.assertEqual([d['project'] for d in r['decisions']], ['CT77 Robe'])

    def test_bad_prefer_rule(self):
        with self.assertRaises(SelectError):
            select_batch(self.cat, {'select': {'stems': ['armor/iron/cuirassf']}, 'prefer': ['weird']})

    def test_xml_writers(self):
        g = ET.fromstring(group_xml('BSO "b1"', ['A & B', 'C']))
        self.assertEqual(g.find('Group').get('name'), 'BSO "b1"')
        self.assertEqual([m.get('name') for m in g.iter('Member')], ['A & B', 'C'])
        iron = next(p for p in self.cat if p['name'] == 'CT77 Iron')
        b = ET.fromstring(build_selection_xml([iron], {'CT77 Iron': {'Zap X': True}}))
        oc = b.find('OutputChoice')
        self.assertEqual((oc.get('path'), oc.get('choice')), ('meshes\\armor\\iron\\CuirassF', 'CT77 Iron'))
        self.assertEqual(b.find('ZapChoice').get('choice'), 'true')


if __name__ == '__main__':
    unittest.main()
