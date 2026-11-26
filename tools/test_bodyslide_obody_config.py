"""bodyslide_obody_config tests on synthetic OBody config/schema/presets."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

import bodyslide_obody_config as oc

SCHEMA = {
    'type': 'object', 'additionalProperties': False,
    'properties': {
        'npcFormID': {'$ref': '#/definitions/npcFormID'},
        'blacklistedNpcsFormID': {'type': 'object', 'additionalProperties': {
            'type': 'array', 'items': {'$ref': '#/definitions/FormID'}}},
        'blacklistedPresetsFromRandomDistribution': {'type': 'array', 'items': {'type': 'string', 'minLength': 1}},
    },
    'definitions': {
        'FormID': {'type': 'string', 'pattern': '^[0-9A-Fa-f]{3,8}$'},
        'npcFormID': {'type': 'object', 'additionalProperties': {
            'type': 'object', 'propertyNames': {'$ref': '#/definitions/FormID'},
            'additionalProperties': {'type': 'array', 'items': {'type': 'string'}}}},
    },
}


class ObodyTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        b = self.base = Path(tmp.name)
        (b / 'presets').mkdir()
        (b / 'presets' / 'body.xml').write_text(
            '<SliderPresets><Preset name="Vanilla" set="CBBE Body">'
            '<SetSlider name="VanillaSSEHi" size="big" value="100"/><SetSlider name="VanillaSSELo" size="small" value="100"/>'
            '</Preset><Preset name="Target" set="CBBE 3BBB Body Amazing">'
            '<SetSlider name="Breasts" size="big" value="60"/><SetSlider name="Butt" size="small" value="10"/>'
            '<SetSlider name="Dflt" size="big" value="30"/>'
            '</Preset><Preset name="Random A" set="CBBE Body"/></SliderPresets>')
        (b / 'presets' / 'outfit set.xml').write_text('<SliderPresets><Preset name="Skipped" set="x"/></SliderPresets>')
        (b / 'osp.osp').write_text('<SliderSetInfo><SliderSet name="x"><Slider name="Dflt" small="0" big="50"/></SliderSet></SliderSetInfo>')
        (b / 'schema.json').write_text(json.dumps(SCHEMA))
        (b / 'base.json').write_text(json.dumps({
            'npcFormID': {}, 'blacklistedNpcsFormID': {'Aela.esp': ['000D63', '000ABC'], 'Other.esp': ['000123']},
            'blacklistedPresetsFromRandomDistribution': ['- Zeroed Sliders -']}))
        self.spec = {'base_config': 'base.json', 'schema': 'schema.json', 'presets_dirs': ['presets'],
                     'neutral': {'name': 'BSO Neutral', 'set': 'CBBE Body'}, 'random_pool': ['BSO Neutral'],
                     'deltas': [{'name': 'BSO Delta', 'target': 'Target', 'base': 'Vanilla', 'osp': 'osp.osp'}],
                     'assign': {'Aela.esp': {'D63': ['BSO Delta']}}, 'unblacklist': {'Aela.esp': ['000D63']}}

    def run_cli(self, spec, out='layer', *extra):
        cfg = self.base / 'cfg.json'
        cfg.write_text(json.dumps({'obody': spec}))
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            code = oc.main(['--config', str(cfg), '--out', str(self.base / out), *extra])
        return code, json.loads(buf.getvalue())

    def test_generate_layer(self):
        code, r = self.run_cli(self.spec)
        self.assertEqual(code, 0, r)
        self.assertEqual(r['loaded_presets'], 3)
        d = r['deltas']['BSO Delta']
        self.assertEqual(d['VanillaSSEHi/big'], -100)
        self.assertEqual(d['VanillaSSELo/small'], -100)
        self.assertEqual(d['Breasts/big'], 60)
        self.assertEqual(d['Dflt/big'], -20)  # target 30 vs base falling back to OSP default 50
        out = json.loads((self.base / 'layer/SKSE/Plugins/OBody_presetDistributionConfig.json').read_text())
        self.assertEqual(out['npcFormID'], {'Aela.esp': {'D63': ['BSO Delta']}})
        self.assertEqual(out['blacklistedNpcsFormID'], {'Aela.esp': ['000ABC'], 'Other.esp': ['000123']})
        bl = out['blacklistedPresetsFromRandomDistribution']
        self.assertIn('Random A', bl)
        self.assertIn('BSO Delta', bl)
        self.assertNotIn('BSO Neutral', bl)
        self.assertIn('- Zeroed Sliders -', bl)
        xml = ET.parse(self.base / 'layer/CalienteTools/BodySlide/SliderPresets/BSO-OBody-Presets.xml').getroot()
        self.assertEqual([p.get('name') for p in xml.iter('Preset')], ['BSO Neutral', 'BSO Delta'])
        self.assertEqual(self.run_cli(self.spec)[0], 2)  # out not empty

    def test_problems_block_writing(self):
        bad = dict(self.spec, random_pool=[], unblacklist={})
        bad['neutral'] = {'name': 'Outfit Neutral'}
        bad['assign'] = {'Aela.esp': {'D63': ['Missing'], 'XYZ!': ['BSO Delta']}}
        code, r = self.run_cli(bad, 'bad')
        self.assertEqual(code, 1)
        text = ' '.join(r['problems'])
        for needle in ('random_pool is empty', 'clothed-set', 'still in blacklistedNpcsFormID', "'Missing'", 'XYZ!'):
            self.assertIn(needle, text)
        self.assertFalse((self.base / 'bad').exists())

    def test_dry_run_and_missing_delta_source(self):
        code, r = self.run_cli(self.spec, 'dry', '--dry-run')
        self.assertEqual(code, 0)
        self.assertFalse((self.base / 'dry').exists())
        spec = dict(self.spec, deltas=[{'name': 'BSO X', 'target': 'Nope', 'base': 'Vanilla'}], assign={})
        code, r = self.run_cli(spec, 'x')
        self.assertEqual(code, 1)
        self.assertIn("'Nope' not loaded", ' '.join(r['problems']))

    def test_npc_presets_table(self):
        spec = {k: v for k, v in self.spec.items() if k not in ('deltas', 'assign', 'unblacklist')}
        spec.update(base_preset='Vanilla', osp='osp.osp', npc_presets=[
            {'plugin': 'Aela.esp', 'formid': '000D63', 'preset': 'Target'},
            {'plugin': 'Other.esp', 'formid': '0x123', 'preset': 'Target'}])
        code, r = self.run_cli(spec, 'npc')
        self.assertEqual(code, 0, r)
        self.assertEqual(r['generated'], ['BSO Neutral', 'BSO Target (morph)'])
        out = json.loads((self.base / 'npc/SKSE/Plugins/OBody_presetDistributionConfig.json').read_text())
        self.assertEqual(out['npcFormID'], {'Aela.esp': {'000D63': ['BSO Target (morph)']},
                                            'Other.esp': {'123': ['BSO Target (morph)']}})
        self.assertEqual(out['blacklistedNpcsFormID'], {'Aela.esp': ['000ABC']})
        self.assertEqual(oc.delta_name('Kurone Outfit'), 'BSO Kurone O_utfit (morph)')
        code, r = self.run_cli(dict(spec, base_preset=None), 'npc2')
        self.assertEqual(code, 2)

    def test_unblacklist_plugin_key_case_insensitive(self):
        spec = {k: v for k, v in self.spec.items() if k not in ('deltas', 'assign', 'unblacklist')}
        spec.update(base_preset='Vanilla', osp='osp.osp', npc_presets=[
            {'plugin': 'other.ESP', 'formid': '000123', 'preset': 'Target'}])
        code, r = self.run_cli(spec, 'case')
        self.assertEqual(code, 0, r)
        out = json.loads((self.base / 'case/SKSE/Plugins/OBody_presetDistributionConfig.json').read_text())
        self.assertNotIn('Other.esp', out['blacklistedNpcsFormID'])
        self.assertEqual(r['unblacklisted'], ['Other.esp:000123'])

    def male_spec(self):
        (self.base / 'presets' / 'himbo.xml').write_text(
            '<SliderPresets><Preset name="HIMBO Zero" set="HIMBO Body - Nude">'
            '<SetSlider name="PecsMass" size="big" value="0"/></Preset>'
            '<Preset name="Kaes" set="HIMBO Body - SOS"><SetSlider name="PecsMass" size="big" value="81"/>'
            '<SetSlider name="PecsMass" size="small" value="20"/></Preset></SliderPresets>')
        spec = {k: v for k, v in self.spec.items() if k not in ('deltas', 'assign', 'unblacklist')}
        spec.update(base_preset='Vanilla', osp='osp.osp')
        return spec

    def test_male_pool_required_once_male_presets_load(self):
        code, r = self.run_cli(self.male_spec(), 'm0')
        self.assertEqual(code, 1)
        self.assertIn('no male preset', ' '.join(r['problems']))

    def test_male_and_female_groups(self):
        spec = self.male_spec()
        spec['neutral'] = [{'name': 'BSO Neutral', 'set': 'CBBE Body'},
                           {'name': 'BSO HIMBO Neutral', 'set': 'HIMBO Body - Nude', 'sliders': ['PecsMass']}]
        spec['random_pool'] = ['BSO Neutral', 'BSO HIMBO Neutral']
        spec['male'] = {'base_preset': 'HIMBO Zero', 'delta_set': 'HIMBO Body - Nude'}
        spec['npc_presets'] = [{'plugin': 'Aela.esp', 'formid': '000D63', 'preset': 'Target'},
                               {'plugin': 'Other.esp', 'formid': '123', 'preset': 'Kaes', 'sex': 'male'}]
        code, r = self.run_cli(spec, 'mf')
        self.assertEqual(code, 0, r)
        self.assertEqual(r['random_pool_by_sex'], {'female': ['BSO Neutral'], 'male': ['BSO HIMBO Neutral']})
        self.assertEqual(r['deltas']['BSO Kaes (morph)'], {'PecsMass/big': 81, 'PecsMass/small': 20})
        self.assertEqual(r['deltas']['BSO HIMBO Neutral'], {'PecsMass/small': 0.0, 'PecsMass/big': 0.0})
        out = json.loads((self.base / 'mf/SKSE/Plugins/OBody_presetDistributionConfig.json').read_text())
        self.assertEqual(out['npcFormID']['Other.esp'], {'123': ['BSO Kaes (morph)']})
        for name in ('HIMBO Zero', 'Kaes', 'BSO Kaes (morph)', 'Random A'):
            self.assertIn(name, out['blacklistedPresetsFromRandomDistribution'])
        xml = ET.parse(self.base / 'mf/CalienteTools/BodySlide/SliderPresets/BSO-OBody-Presets.xml').getroot()
        sets = {p.get('name'): p.get('set') for p in xml.iter('Preset')}
        self.assertEqual(sets['BSO Kaes (morph)'], 'HIMBO Body - Nude')
        self.assertEqual(sets['BSO Target (morph)'], 'CBBE 3BBB Body Amazing')  # female row: target's own set

    def test_male_sex_mismatch_and_bad_rows(self):
        spec = self.male_spec()
        spec['neutral'] = [{'name': 'BSO Neutral', 'set': 'CBBE Body'}]
        spec['random_pool'] = ['BSO Neutral', 'HIMBO Zero']
        spec['male'] = {'base_preset': 'HIMBO Zero', 'delta_set': 'CBBE Body'}  # wrong: reads female
        spec['npc_presets'] = [{'plugin': 'Other.esp', 'formid': '123', 'preset': 'Kaes', 'sex': 'male'}]
        code, r = self.run_cli(spec, 'mm')
        self.assertEqual(code, 1)
        self.assertIn('reads as female', ' '.join(r['problems']))
        for bad in ({'sex': 'x'}, {'sex': 'male'}):
            s2 = dict(spec, npc_presets=[dict(plugin='O.esp', formid='1', preset='Kaes', **bad)])
            if bad['sex'] == 'male':
                s2.pop('male')
            self.assertEqual(self.run_cli(s2, 'mx')[0], 2)
        self.assertTrue(oc.is_male_set('HIMBO Body') and not oc.is_male_set('CBBE Body'))

    def test_declared_utf16_but_utf8_bom_is_read(self):
        # CT77SE.xml shape: says UTF-16, is UTF-8 with a BOM; expat refuses it, OBody (pugixml) loads it
        body = ('<?xml version="1.0" encoding="UTF-16"?>\r\n<SliderPresets><Preset name="Liar Né" set="CBBE Body">'
                '<SetSlider name="Butt" size="big" value="70"/></Preset></SliderPresets>')
        f = self.base / 'presets' / 'liar.xml'
        f.write_bytes(b'\xef\xbb\xbf' + body.encode('utf-8'))
        with self.assertRaises(ET.ParseError):
            ET.parse(f)
        self.assertEqual(oc.read_presets(f)['Liar Né']['sliders'], {('Butt', 'big'): 70.0})
        # real UTF-16 declared as UTF-8, and BOM-less UTF-16, are decoded from the bytes too
        (self.base / 'presets' / 'u16.xml').write_bytes(
            body.replace('UTF-16', 'UTF-8').replace('Liar Né', 'Wide A').encode('utf-16'))
        (self.base / 'presets' / 'u16le.xml').write_bytes(body.replace('Liar Né', 'Wide B').encode('utf-16-le'))
        code, r = self.run_cli(self.spec, 'enc')
        self.assertEqual(code, 0, r)
        self.assertEqual(r['loaded_presets'], 6)
        bl = json.loads((self.base / 'enc/SKSE/Plugins/OBody_presetDistributionConfig.json').read_text())[
            'blacklistedPresetsFromRandomDistribution']
        for name in ('Liar Né', 'Wide A', 'Wide B'):
            self.assertIn(name, bl)

    def test_unreadable_preset_file_is_an_error(self):
        (self.base / 'presets' / 'broken one.xml').write_text('<SliderPresets><Preset name="Half"')
        (self.base / 'presets' / 'bad bytes.xml').write_bytes(b'<SliderPresets name="\xff\xfe\xfa"/>')
        code, r = self.run_cli(self.spec, 'broken')
        self.assertEqual(code, 2)
        self.assertFalse(r['ok'])
        self.assertIn('2 preset file(s) unreadable', r['error'])
        self.assertIn('broken one.xml', r['error'])
        self.assertIn('bad bytes.xml', r['error'])
        self.assertFalse((self.base / 'broken').exists())

    def test_validate_subset(self):
        self.assertEqual(oc.validate({'npcFormID': {}}, SCHEMA), [])
        self.assertTrue(oc.validate({'unknown': 1}, SCHEMA))
        self.assertTrue(oc.validate({'blacklistedNpcsFormID': {'a': ['zz']}}, SCHEMA))


if __name__ == '__main__':
    unittest.main()
