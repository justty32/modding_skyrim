"""bodyslide_rebuild / bodyslide_layer tests: synthetic MO2 tree, fake round outputs, no Wine."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import xml.etree.ElementTree as ET

import bodyslide_layer as layer
import bodyslide_rebuild as rb
from test_bodyslide_mesh_check import V3, skinned_nif, tri_bytes

ENV_KEYS = ('MO2_DIR', 'MO2_MODS_DIR', 'MO2_OVERWRITE_DIR', 'SKYRIM_GAME_DATA', 'SKYRIM_REPO')


def osp(name, path, stem):
    return (f'<SliderSetInfo version="1"><SliderSet name="{name}"><DataFolder>D</DataFolder>'
            f'<SourceFile>s.nif</SourceFile><OutputPath>{path}</OutputPath><OutputFile GenWeights="true">{stem}'
            f'</OutputFile><Shape target="Body">Body</Shape></SliderSet></SliderSetInfo>')


class RebuildTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        b = self.base = Path(tmp.name)
        env = mock.patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        for key in ENV_KEYS:
            os.environ.pop(key, None)
        os.environ['SKYRIM_REPO'] = str(b / 'repo')
        (b / 'repo' / 'instance').mkdir(parents=True)
        self.mo2 = b / 'mo2'
        (self.mo2 / 'overwrite').mkdir(parents=True)
        (self.mo2 / 'profiles' / 'p').mkdir(parents=True)
        (self.mo2 / 'profiles' / 'p' / 'modlist.txt').write_text('+Armor\r\n+Body\r\n+OldLayer\r\n')
        bs = self.mo2 / 'mods' / 'Armor' / 'CalienteTools' / 'BodySlide'
        (bs / 'SliderSets').mkdir(parents=True)
        (bs / 'SliderSets' / 'a.osp').write_text(osp('Iron', 'meshes\\armor\\iron', 'cuirassf'))
        bs2 = self.mo2 / 'mods' / 'Body' / 'CalienteTools' / 'BodySlide'
        (bs2 / 'SliderSets').mkdir(parents=True)
        (bs2 / 'SliderPresets').mkdir(parents=True)
        (bs2 / 'SliderSets' / 'b.osp').write_text(osp('Iron Old', 'meshes\\armor\\iron', 'cuirassf'))
        (bs2 / 'SliderPresets' / 'p.xml').write_text('<SliderPresets><Preset name="Base" set="X"/></SliderPresets>')
        self.old = self.mo2 / 'mods' / 'OldLayer' / 'meshes' / 'armor' / 'iron'
        self.old.mkdir(parents=True)
        (self.old / 'cuirassf_1.nif').write_bytes(skinned_nif(V3, bodytri='armor\\iron\\cuirassf.tri'))
        (b / 'data').mkdir()
        self.root = b / 'staging'
        self.cfg = b / 'cfg' / 'rebuild.json'
        self.cfg.parent.mkdir()
        self.write_cfg()

    def write_cfg(self, **extra):
        cfg = {'schema': 'bodyslide-rebuild/1', 'name': 't', 'revision': 'r1', 'mo2_dir': str(self.mo2),
               'game_data': str(self.base / 'data'), 'profile': 'p', 'staging_root': str(self.root),
               'run': 'run1', 'base_preset': 'Base', 'samples': 3,
               'batches': [{'id': 'b1', 'layer': 'BSO-Iron', 'before': 'OldLayer', 'replaces': ['OldLayer'],
                            'references': [str(self.mo2 / 'mods' / 'OldLayer')],
                            'select': {'stems_from_dirs': [str(self.mo2 / 'mods' / 'OldLayer')]},
                            'prefer': ['mod:Armor']}]}
        cfg.update(extra)
        self.cfg.write_text(json.dumps(cfg))

    def run_cli(self, *argv):
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            code = rb.main([*argv, '--config', str(self.cfg)])
        return code, json.loads(buf.getvalue())

    def fake_round(self, nif_bytes=None, tri=True):
        out = self.root / 'run1' / 'rounds' / 'b1-r1' / 'output' / 'meshes' / 'armor' / 'iron'
        out.mkdir(parents=True)
        nif = nif_bytes or skinned_nif(V3, bodytri='armor\\iron\\cuirassf.tri')
        (out / 'cuirassf_0.nif').write_bytes(nif)
        (out / 'cuirassf_1.nif').write_bytes(nif)
        if tri:
            (out / 'cuirassf.tri').write_bytes(tri_bytes([('Body', [('VanillaSSEHi', [(0, 1, 2, 3)])])]))
        return out

    def test_config_validation(self):
        self.write_cfg(revision='r 1')
        self.assertEqual(self.run_cli('plan')[0], 2)
        self.write_cfg(batches=[{'id': 'b1', 'layer': 'Ä'}])
        self.assertEqual(self.run_cli('plan')[0], 2)
        self.write_cfg(schema='x')
        self.assertEqual(self.run_cli('plan')[0], 2)

    def test_stage_plan_verify_layer(self):
        code, r = self.run_cli('stage')
        self.assertEqual(code, 0, r)
        self.assertEqual(self.run_cli('stage')[1]['stage']['reused'], str(self.root / 'run1' / 'tool'))
        code, r = self.run_cli('plan')
        self.assertEqual(code, 0, r)
        self.assertEqual(r['plan']['batches']['b1']['projects'], 1)
        tool = self.root / 'run1' / 'tool'
        g = ET.parse(tool / 'SliderGroups' / 'bodyslide-rebuild.xml').getroot()
        self.assertEqual([m.get('name') for m in g.iter('Member')], ['Iron'])
        self.assertEqual(g.find('Group').get('name'), 'BSO b1')
        bsel = ET.parse(tool / 'BuildSelection.xml').getroot()
        self.assertEqual(bsel.find('OutputChoice').get('choice'), 'Iron')
        self.assertEqual(self.run_cli('plan')[0], 0)  # our own BuildSelection does not block a re-plan
        code, r = self.run_cli('build', '--dry-run')
        argv = r['build']['batches']['b1']
        self.assertIn('exit', argv)
        self.fake_round()
        code, r = self.run_cli('verify')
        self.assertEqual(code, 0, r)
        self.assertEqual(r['verify']['batches']['b1']['baseline_equal'], [True])
        code, r = self.run_cli('layer')
        self.assertEqual(code, 0, r)
        lay = self.root / 'layers' / 'BSO-Iron-r1'
        self.assertTrue((lay / 'meta.ini').is_file())
        self.assertEqual((lay / 'meshes/armor/iron/cuirassf.tri').stat().st_nlink, 2)
        man = json.loads((self.root / 'manifests' / 'BSO-Iron-r1.json').read_text())
        self.assertEqual((man['files'], man['projects']), (3, 1))
        self.assertEqual({row['project'] for row in man['rows']}, {'Iron'})
        draft = json.loads((self.root / 'manifests' / 'BSO-Iron-r1.layer-apply.json').read_text())
        self.assertEqual(draft['modlist'][0], {'mod': 'BSO-Iron-r1', 'enabled': True, 'before': 'OldLayer'})
        self.assertEqual(draft['disable_mods'], ['OldLayer'])
        self.assertEqual(self.run_cli('layer')[0], 2)  # layer dir not empty: refuse

    def test_stage_shapedata_option(self):
        sd = self.mo2 / 'mods' / 'Armor' / 'CalienteTools' / 'BodySlide' / 'ShapeData'
        (sd / 'D').mkdir(parents=True)
        (sd / 'D' / 's.nif').write_bytes(b'n')
        (sd / 'E').mkdir()
        (sd / 'E' / 's.nif').write_bytes(b'n')
        self.write_cfg(stage_shapedata=['D'])
        self.assertEqual(self.run_cli('stage')[0], 0)
        tool = self.root / 'run1' / 'tool'
        self.assertTrue((tool / 'ShapeData' / 'D' / 's.nif').is_file())
        self.assertFalse((tool / 'ShapeData' / 'E').exists())
        self.write_cfg(stage_shapedata='weird', run='run2')
        self.assertEqual(self.run_cli('stage')[0], 2)

    def test_preset_files_and_obody_layer(self):
        user = self.base / 'my preset.xml'
        user.write_text('<SliderPresets><Preset name="Mine" set="X"><SetSlider name="Butt" size="big" value="40"/>'
                        '</Preset></SliderPresets>')
        (self.base / 'schema.json').write_text('{"type": "object"}')
        (self.base / 'obase.json').write_text('{"blacklistedNpcsFormID": {"A.esp": ["000D62"]}}')
        self.write_cfg(preset_files=[str(user)], obody={
            'base_config': str(self.base / 'obase.json'), 'schema': str(self.base / 'schema.json'),
            'neutral': {'name': 'BSO Neutral'}, 'random_pool': ['BSO Neutral'], 'revision': 'n1',
            'before': 'OBody-Old', 'replaces': ['OBody-Old'],
            'neutralize_tri': ['meshes\\actors\\character\\x\\femalebody.tri'],
            'npc_presets': [{'plugin': 'A.esp', 'formid': '000D62', 'preset': 'Mine'}]})
        code, r = self.run_cli('stage')
        self.assertEqual(code, 0, r)
        self.assertTrue((self.root / 'run1/tool/SliderPresets/my preset.xml').is_file())
        code, r = self.run_cli('obody')
        self.assertEqual(code, 0, r)
        lay = self.root / 'layers' / 'BSO-NPC-Body-Assignments-n1'
        cfg = json.loads((lay / 'SKSE/Plugins/OBody_presetDistributionConfig.json').read_text())
        self.assertEqual(cfg['npcFormID'], {'A.esp': {'000D62': ['BSO Mine (morph)']}})
        self.assertEqual(cfg['blacklistedNpcsFormID'], {})
        tri = lay / 'meshes/actors/character/x/femalebody.tri'
        self.assertEqual(layer.bmc.parse_tri(tri)[0]['position_shapes'], [])
        draft = json.loads((self.root / 'manifests' / 'BSO-NPC-Body-Assignments-n1.layer-apply.json').read_text())
        self.assertEqual(draft['disable_mods'], ['OBody-Old'])
        self.assertEqual(self.run_cli('obody')[0], 2)  # same revision twice: refuse
        user.write_text('<SliderPresets/>')
        self.assertEqual(self.run_cli('stage')[0], 2)  # same file name, other bytes

    def test_obody_staging_root_and_extra_files(self):
        (self.base / 'schema.json').write_text('{"type": "object"}')
        (self.base / 'obase.json').write_text('{}')
        nif = self.base / 'patched.nif'
        nif.write_bytes(b'NIFDATA')
        other = self.base / 'other-staging'
        obody = {'base_config': str(self.base / 'obase.json'), 'schema': str(self.base / 'schema.json'),
                 'neutral': {'name': 'BSO Neutral'}, 'random_pool': ['BSO Neutral'], 'revision': 'n2',
                 'staging_root': str(other), 'extra_files': {'meshes\\x\\femalebody_1.nif': str(nif)}}
        self.write_cfg(obody=obody)
        code, r = self.run_cli('obody')
        self.assertEqual(code, 0, r)
        lay = other / 'layers' / 'BSO-NPC-Body-Assignments-n2'
        self.assertEqual((lay / 'meshes/x/femalebody_1.nif').read_bytes(), b'NIFDATA')
        self.assertIn('meshes\\x\\femalebody_1.nif', r['obody']['extra_files'])
        self.assertTrue((other / 'manifests' / 'BSO-NPC-Body-Assignments-n2.layer-apply.json').is_file())
        self.assertFalse((self.root / 'layers' / 'BSO-NPC-Body-Assignments-n2').exists())
        obody['revision'], obody['extra_files'] = 'n3', {'meshes\\y.nif': str(self.base / 'missing.nif')}
        self.write_cfg(obody=obody)
        code, r = self.run_cli('obody')
        self.assertEqual(code, 1)
        self.assertTrue(any('source missing' in p for p in r['obody']['problems']))

    def test_mo2_build_selection_needs_review(self):
        (self.mo2 / 'mods' / 'Armor' / 'CalienteTools' / 'BodySlide' / 'BuildSelection.xml').write_text('<BuildSelection/>')
        self.assertEqual(self.run_cli('stage')[0], 0)
        code, r = self.run_cli('plan')
        self.assertEqual(code, 1)
        self.assertIn('override_build_selection', ' '.join(r['plan']['errors']))
        self.write_cfg(override_build_selection=True)
        self.assertEqual(self.run_cli('plan')[0], 0)

    def test_verify_failures(self):
        self.run_cli('stage')
        self.run_cli('plan')
        out = self.fake_round(nif_bytes=skinned_nif([(9.0, 9.0, 9.0)] + V3[1:], bodytri='other.tri'), tri=False)
        (out / 'stray.nif').write_bytes(b'')
        code, r = self.run_cli('verify')
        self.assertEqual(code, 1)
        v = json.loads((self.root / 'run1' / 'verify' / 'b1-r1.json').read_text())
        self.assertEqual(v['tri_missing'], ['meshes/armor/iron/cuirassf.tri'])
        self.assertEqual(v['extra'], ['meshes/armor/iron/stray.nif'])
        s = v['samples'][0]
        self.assertIn('tri missing', s['failures'])
        self.assertFalse(s['baseline']['equal'])

    def test_plan_reports_missing_preset_and_unresolved(self):
        self.write_cfg(base_preset='Nope')
        self.run_cli('stage')
        code, r = self.run_cli('plan')
        self.assertEqual(code, 1)
        self.assertTrue(any('Nope' in e for e in r['plan']['errors']))
        self.write_cfg(batches=[{'id': 'b1', 'layer': 'L', 'select': {'stems': ['armor/iron/cuirassf']}}])
        code, r = self.run_cli('plan')
        self.assertEqual(r['plan']['batches']['b1']['unresolved'], 1)
        self.assertFalse((self.root / 'run1' / 'tool' / 'BuildSelection.xml').exists())

    def test_body_match(self):
        body = self.base / 'body' / 'meshes/actors/character/character assets'
        body.mkdir(parents=True)
        (body / 'femalebody_1.nif').write_bytes(skinned_nif(V3, shape='CBBE'))
        pos = {'CBBE': [V3[1], V3[2]], '3BA': [(1.0, 2.0, 3.5)], 'Cloth': [(50.0, 0.0, 0.0)]}
        m = layer.body_match('meshes/x/a_1.nif', pos, self.base / 'body')
        self.assertEqual(m['CBBE']['on_body'], 1.0)
        self.assertEqual(m['3BA']['on_body'], 0.0)
        self.assertAlmostEqual(m['3BA']['p50'], 0.5)
        self.assertNotIn('Cloth', m)
        self.assertIsNone(layer.body_match('meshes/x/a.nif', pos, self.base / 'body'))
        self.assertIsNone(layer.body_match('meshes/x/a_1.nif', {'Cloth': []}, self.base / 'body'))

    def test_body_match_male(self):
        body = self.base / 'mbody' / 'meshes/actors/character/character assets'
        body.mkdir(parents=True)
        (body / 'malebody_1.nif').write_bytes(skinned_nif(V3, shape='HIMBO - Body'))
        pos = {'HIMBO - Body': [V3[1], V3[2]], 'CBBE': [(9.0, 9.0, 9.0)]}
        m = layer.body_match('meshes/x/a_1.nif', pos, self.base / 'mbody', 'male')
        self.assertEqual(list(m), ['HIMBO - Body'])
        self.assertEqual(m['HIMBO - Body']['on_body'], 1.0)
        self.assertIsNone(layer.body_match('meshes/x/a_1.nif', {'Cloth': []}, self.base / 'mbody', 'male'))

    def test_body_sex_config(self):
        self.write_cfg(body_sex='robot')
        code, r = self.run_cli('plan')
        self.assertEqual(code, 2)
        self.assertIn('body_sex', r['error'])

    def test_pick_samples_spread(self):
        projects = [dict(name=f'p{i}', osp=f'o{i % 3}.osp') for i in range(9)]
        self.assertEqual([p['name'] for p in layer.pick_samples(projects, 3)], ['p0', 'p1', 'p2'])
        five = [p['name'] for p in layer.pick_samples(projects, 5)]
        self.assertEqual(len(set(five)), 5)
        self.assertEqual(len(layer.pick_samples(projects[:2], 5)), 2)
        one_osp = [dict(name=f'q{i}', osp='o.osp') for i in range(3)]
        self.assertEqual(sorted(p['name'] for p in layer.pick_samples(one_osp, 5)), ['q0', 'q1', 'q2'])
        self.assertEqual(layer.pick_samples([], 5), [])


if __name__ == '__main__':
    unittest.main()
