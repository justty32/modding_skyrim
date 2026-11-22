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

    def test_validate_subset(self):
        self.assertEqual(oc.validate({'npcFormID': {}}, SCHEMA), [])
        self.assertTrue(oc.validate({'unknown': 1}, SCHEMA))
        self.assertTrue(oc.validate({'blacklistedNpcsFormID': {'a': ['zz']}}, SCHEMA))


if __name__ == '__main__':
    unittest.main()
