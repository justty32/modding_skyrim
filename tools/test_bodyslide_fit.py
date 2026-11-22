"""bodyslide_fit／bodyslide_fit_model 的測試：fixture 在測試內合成（NIF 用 test_bodyslide_mesh_check 的 builder）。

正控（真實檔）：Aela 的私有身體 kurone_native/bcb1 已知＝`Kurone Big Change Body`（3BA）；
本機 staging 與 MO2 mods 都在才跑，否則 skip。
"""
from __future__ import annotations

import contextlib
import io
import json
import shutil
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodyslide_fit as bf  # noqa: E402
import bodyslide_fit_model as fm  # noqa: E402
import bodyslide_mesh_check as mc  # noqa: E402
from test_bodyslide_mesh_check import skinned_nif  # noqa: E402

BASE = [(0.0, 0.0, 0.0), (0.0, 0.0, 50.0), (0.0, 0.0, 100.0), (10.0, 0.0, 70.0), (-10.0, 0.0, 70.0),
        (5.0, 3.0, 20.0)]
D_A = {1: (1.0, 0.0, 0.0), 3: (0.0, 2.0, 0.0)}          # 一般滑桿
D_B = {2: (0.0, 0.0, 1.5), 4: (0.5, 0.5, 0.0)}          # invert 滑桿
D_C = {0: (0.0, 1.0, 0.0), 5: (1.0, 1.0, 1.0)}          # 一般滑桿
OSP = """<?xml version="1.0" encoding="UTF-8"?>
<SliderSetInfo version="1">
  <SliderSet name="Test Body">
    <DataFolder>TB</DataFolder>
    <SourceFile>base.nif</SourceFile>
    <Shape target="BodyT">Body</Shape>
    <Slider name="A" invert="false" small="0" big="0"><Data name="BodyTA" target="BodyT" local="true">tb.osd\\BodyTA</Data></Slider>
    <Slider name="B" invert="true" small="100" big="100"><Data name="BodyTB" target="BodyT" local="true">tb.osd\\BodyTB</Data></Slider>
    <Slider name="C" invert="false" small="0" big="0"><Data name="BodyTC" target="BodyT" local="true">tb.osd\\BodyTC</Data></Slider>
    <Slider name="U" invert="false" small="0" big="0" uv="true"><Data name="BodyTU" target="BodyT" local="true">tb.osd\\BodyTU</Data></Slider>
  </SliderSet>
</SliderSetInfo>
"""
PRESETS = """<?xml version="1.0" encoding="UTF-8"?>
<SliderPresets>
  <Preset name="Base P" set="Test Body"><SetSlider name="A" size="small" value="10"/></Preset>
</SliderPresets>
"""


def shaped(values: dict) -> list:
    out = [list(v) for v in BASE]
    for name, diff in (('A', D_A), ('B', D_B), ('C', D_C)):
        v = values.get(name, 100.0 if name == 'B' else 0.0)
        x = 1 - v / 100 if name == 'B' else v / 100
        for i, d in diff.items():
            for k in range(3):
                out[i][k] += x * d[k]
    return [tuple(p) for p in out]


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        sd = self.tmp / 'ShapeData' / 'TB'
        sd.mkdir(parents=True)
        (sd / 'base.nif').write_bytes(skinned_nif(BASE))
        fm.write_osd(sd / 'tb.osd', {'BodyTA': D_A, 'BodyTB': D_B, 'BodyTC': D_C, 'BodyTU': {0: (0.1, 0.1, 0.0)}})
        self.osp = self.tmp / 'tb.osp'
        self.osp.write_text(OSP, encoding='utf-8')
        (self.tmp / 'presets.xml').write_text(PRESETS, encoding='utf-8')

    def target(self, name, small: dict, big: dict, shape='Body', bodytri=None):
        p0, p1 = self.tmp / f'{name}_0.nif', self.tmp / f'{name}_1.nif'
        p0.write_bytes(skinned_nif(shaped(small), shape=shape, bodytri=bodytri))
        p1.write_bytes(skinned_nif(shaped(big), shape=shape, bodytri=bodytri))
        return p0, p1

    def fitter(self, **kw):
        return bf.Fitter(self.osp, 'Test Body', self.tmp / 'ShapeData', **kw)

    def cli(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = bf.main([str(a) for a in args])
        return code, buf.getvalue()


class ModelTests(Base):
    def test_osd_roundtrip(self):
        d = fm.read_osd(self.tmp / 'ShapeData' / 'TB' / 'tb.osd')
        self.assertEqual(sorted(d), ['BodyTA', 'BodyTB', 'BodyTC', 'BodyTU'])
        self.assertEqual(d['BodyTA'][3], (0.0, 2.0, 0.0))

    def test_bad_osd_magic(self):
        p = self.tmp / 'bad.osd'
        p.write_bytes(struct.pack('<III', 1, 1, 0))
        with self.assertRaises(fm.ModelError):
            fm.read_osd(p)

    def test_model_kinds_and_fit_vars(self):
        m = fm.load_model(self.osp, 'Test Body', self.tmp / 'ShapeData')
        kinds = {s['name']: s['kind'] for s in m['sliders']}
        self.assertEqual(kinds['U'], 'uv')
        self.assertEqual([s['name'] for s in fm.fit_vars(m)], ['A', 'B', 'C'])

    def test_apply_matches_definition_with_invert(self):
        m = fm.load_model(self.osp, 'Test Body', self.tmp / 'ShapeData')
        got = fm.apply_values(m, {'A': 30, 'B': 40, 'C': -20}, 'small')['Body']
        want = shaped({'A': 30, 'B': 40, 'C': -20})
        for g, w in zip(got, want):
            for a, b in zip(g, w):
                self.assertAlmostEqual(a, b, places=5)

    def test_solve_box_known_solution_and_bounds(self):
        A = [[2.0, 0.0], [0.0, 1.0]]
        x, info = fm.solve_box(A, [2.0, 3.0], [-10, -10], [10, 1.5], ridge=0.0)
        self.assertAlmostEqual(x[0], 1.0)
        self.assertAlmostEqual(x[1], 1.5)
        self.assertEqual(info['at_bound'], [1])

    def test_solve_box_collinear_with_ridge(self):
        A = [[1.0, 1.0], [1.0, 1.0]]
        x, _ = fm.solve_box(A, [2.0, 2.0], [-5, -5], [5, 5], ridge=1e-6)
        self.assertAlmostEqual(x[0] + x[1], 2.0, places=4)
        self.assertAlmostEqual(x[0], x[1], places=4)


class FitTests(Base):
    def test_recovers_values_both_sizes(self):
        t0, t1 = self.target('t', {'A': 40, 'B': 70, 'C': -30}, {'A': 120, 'B': 0, 'C': 55})
        res = self.fitter().fit(t0, t1, 'Fit T')
        s = res['preset']['sliders']
        self.assertEqual((s[('A', 'small')], s[('B', 'small')], s[('C', 'small')]), (40, 70, -30))
        self.assertEqual((s[('A', 'big')], s[('B', 'big')], s[('C', 'big')]), (120, 0, 55))
        self.assertNotIn(('U', 'small'), s)
        self.assertEqual(res['verdict'], 'usable')
        self.assertLess(res['sizes']['big']['fit']['max'], 1e-3)

    def test_bound_clamps_and_reports(self):
        t0, t1 = self.target('t', {'A': 300}, {'A': 300})
        res = self.fitter(bounds=(-100, 200)).fit(t0, t1, 'Fit T')
        self.assertEqual(res['preset']['sliders'][('A', 'small')], 200)
        self.assertIn('A', res['sizes']['small']['solver']['at_bound'])
        self.assertGreater(res['sizes']['small']['fit']['max'], 0.9)

    def test_same_as_base_and_baseline(self):
        t0, t1 = self.target('t', {'A': 10}, {})
        base = bf.preset_values(self.tmp / 'presets.xml', 'Base P')
        res = self.fitter().fit(t0, t1, 'Fit T', base=base)
        self.assertEqual(res['verdict'], 'same_as_base')
        self.assertEqual(res['sizes']['small']['baseline']['rms'], 0.0)

    def test_topology_mismatch_unfittable(self):
        p0, p1 = self.tmp / 'x_0.nif', self.tmp / 'x_1.nif'
        for p in (p0, p1):
            p.write_bytes(skinned_nif(BASE[:5], shape='Other'))
        res = self.fitter().fit(p0, p1, 'Fit X')
        self.assertEqual(res['verdict'], 'unfittable')
        self.assertIn('no unique same-count shape', res['problems'][0])

    def test_shape_matched_by_vertex_count_when_name_differs(self):
        t0, t1 = self.target('t', {'C': 50}, {'C': 50}, shape='3BA')
        res = self.fitter().fit(t0, t1, 'Fit T')
        self.assertEqual(res['mapping'], {'Body': '3BA'})
        self.assertEqual(res['preset']['sliders'][('C', 'big')], 50)

    def test_verdict_thresholds(self):
        h = 100.0
        self.assertEqual(bf.verdict({'height': h, 'rms': 0.19, 'p99': 0.59}), 'usable')
        self.assertEqual(bf.verdict({'height': h, 'rms': 0.3, 'p99': 0.59}), 'marginal')
        self.assertEqual(bf.verdict({'height': h, 'rms': 0.3, 'p99': 1.3}), 'poor')

    def test_bodytri_reported(self):
        t0, t1 = self.target('t', {}, {}, bodytri='actors\\character\\x\\femalebody.tri')
        res = self.fitter().fit(t0, t1, 'Fit T')
        self.assertEqual(res['targets']['big']['bodytri'], ['actors\\character\\x\\femalebody.tri'])


class CliTests(Base):
    def test_fit_cli_writes_preset_and_report(self):
        t0, t1 = self.target('t', {'A': 25}, {'A': 75})
        out, rep = self.tmp / 'p.xml', self.tmp / 'r.json'
        code, text = self.cli('fit', '--osp', self.osp, '--set', 'Test Body', '--shapedata', self.tmp / 'ShapeData',
                              '--target0', t0, '--target1', t1, '--name', 'Fit T', '--out-preset', out, '--report', rep)
        self.assertEqual(code, 0, text)
        self.assertEqual(json.loads(text)['verdict'], 'usable')
        x = out.read_text(encoding='utf-8')
        self.assertIn('<Preset name="Fit T" set="Test Body">', x)
        self.assertIn('<SetSlider name="A" size="big" value="75"/>', x)
        self.assertEqual(json.loads(rep.read_text())['preset']['sliders']['A/small'], 25)

    def test_batch_cli(self):
        t0, t1 = self.target('t', {'C': 60}, {'C': 90})
        u0, u1 = self.tmp / 'u_0.nif', self.tmp / 'u_1.nif'
        for p in (u0, u1):
            p.write_bytes(skinned_nif(BASE[:4]))
        spec = {'sets': {'T': {'osp': str(self.osp), 'set': 'Test Body', 'shapedata': str(self.tmp / 'ShapeData')}},
                'base_preset': {'file': str(self.tmp / 'presets.xml'), 'name': 'Base P'},
                'presets_file': 'Fits.xml',
                'bodies': [{'id': 'good', 'set': 'T', 'w0': str(t0), 'w1': str(t1), 'preset_name': 'Fit Good'},
                           {'id': 'bad', 'set': 'T', 'w0': str(u0), 'w1': str(u1), 'preset_name': 'Fit Bad'}]}
        sp = self.tmp / 'spec.json'
        sp.write_text(json.dumps(spec), encoding='utf-8')
        code, text = self.cli('batch', '--spec', sp, '--out', self.tmp / 'out')
        self.assertEqual(code, 0, text)
        summary = json.loads((self.tmp / 'out' / 'summary.json').read_text())
        self.assertEqual([r['verdict'] for r in summary['rows']], ['usable', 'unfittable'])
        presets = (self.tmp / 'out' / 'Fits.xml').read_text()
        self.assertIn('Fit Good', presets)
        self.assertNotIn('Fit Bad', presets)

    def test_retarget_bodytri_keeps_geometry(self):
        src = self.tmp / 'b_1.nif'
        src.write_bytes(skinned_nif(shaped({'A': 50}), bodytri='actors\\character\\character assets\\femalebody.tri'))
        out = self.tmp / 'o' / 'b_1.nif'
        code, text = self.cli('retarget-bodytri', '--nif', src, '--out', out, '--value', 'actors\\bso\\null.tri')
        self.assertEqual(code, 0, text)
        r = json.loads(text)
        self.assertTrue(r['positions_identical'])
        self.assertEqual(r['old'], 'actors\\character\\character assets\\femalebody.tri')
        rep, _ = mc.parse_nif(out)
        self.assertEqual([b['value'] for b in rep['bodytri']], ['actors\\bso\\null.tri'])
        self.assertIn('actors\\character\\character assets\\femalebody.tri', rep and mc.read_nif_header(
            mc.Reader(out.read_bytes()))['strings'])

    def test_retarget_requires_one_bodytri(self):
        src = self.tmp / 'n_1.nif'
        src.write_bytes(skinned_nif(BASE))
        code, text = self.cli('retarget-bodytri', '--nif', src, '--out', self.tmp / 'o.nif', '--value', 'x.tri')
        self.assertEqual(code, 2)
        self.assertIn('BODYTRI', text)


STAGING = Path.home() / 'skyrim_mods/bodyslide-sources/female'
B3 = STAGING / 'src/3ba-30174/00 Base/CalienteTools/BodySlide'
AELA = Path.home() / ('games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/'
                      'Kurone-All-Looks-Private3BA-2026-11-07/meshes/actors/character/kurone_native/bcb1')
BCB = STAGING / 'run1/tool/SliderPresets/Kurone Big Change Body.xml'


@unittest.skipUnless((B3 / 'SliderSets/SE 3BBB Amazing.osp').is_file() and (AELA / 'femalebody_1.nif').is_file()
                     and BCB.is_file(), 'local 3BA ShapeData / Aela body / BCB preset not present')
class AelaPositiveControl(unittest.TestCase):
    """正控：Aela 的身體已知＝Kurone Big Change Body；擬合應近乎零誤差並還原出該 preset。"""

    def test_aela_recovers_bcb(self):
        f = bf.Fitter(B3 / 'SliderSets/SE 3BBB Amazing.osp', 'CBBE 3BBB Body Amazing', B3 / 'ShapeData')
        bcb = bf.preset_values(BCB, 'Kurone Big Change Body')
        res = f.fit(AELA / 'femalebody_0.nif', AELA / 'femalebody_1.nif', 'Fit Aela', compare=bcb)
        self.assertEqual(res['verdict'], 'usable')
        defaults = {s['name']: s for s in f.model['sliders']}
        same = total = 0
        for size in ('small', 'big'):
            self.assertLess(res['sizes'][size]['fit']['rms'], 0.001)
            self.assertLess(res['sizes'][size]['fit']['max'], 0.01)
            self.assertLess(res['sizes'][size]['compare']['max'], 0.001)  # 模型重現 BCB 建置
        for (slider, size), v in res['preset']['sliders'].items():
            total += 1
            same += abs(bcb[size].get(slider, defaults[slider][size]) - v) <= 1
        self.assertEqual(same, total)


if __name__ == '__main__':
    unittest.main()
