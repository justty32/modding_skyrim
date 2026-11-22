#!/usr/bin/env python3
"""把一套已烤好的身體 NIF 擬合成 BodySlide preset（stdlib-only；只讀輸入，只寫 --out）。

用途：自帶專屬身體的 NPC 穿共用裝備時，裝備是基準形；擬合出「這套身體＝基準身體＋哪些滑桿值」，
再經 OBody 的 NPC→preset 對照表（bodyslide_rebuild.py obody）把差量推到裝備上。

子命令：
  fit    --osp OSP --set NAME --shapedata DIR --target0 X_0.nif --target1 X_1.nif --name PRESET
         [--base-preset XML --base-name NAME] [--compare-preset XML --compare-name NAME]
         [--out-preset XML] [--report JSON] [--bounds LO HI] [--ridge R]
  batch  --spec SPEC.json --out DIR        多套身體共用一次法方程（同一滑桿集只算一次）
  retarget-bodytri --nif IN --out OUT --value 'actors\\...\\x.tri'
         複製 NIF、把 BODYTRI 改指另一個 tri（給 BODYTRI 指向全域 femalebody.tri 的私有 CBBE 身體，
         改指空 tri 以免差量又推一次裸身）；驗證 shape 與頂點完全不變

前提：目標 NIF 的每個模型 shape 都要有頂點數相同的對應 shape（先同名、再以頂點數唯一對上），
頂點依 index 一一對應；對不上＝拓樸不同＝verdict "unfittable"，不硬做。

判定（以基準身體高度 H 為尺度；H 約 120 單位，1 單位約 1.43 cm）：
  usable    RMS <= 0.002H 且 p99 <= 0.006H（約 0.24／0.72 單位＝3／10 mm）。理由：CBBE 系裝備離皮膚
            約 0.3～1 單位；現役 3BA 參考形裝備內嵌身體對全域身體 p95 約 0.28 已被接受。
  marginal  RMS <= 0.005H 且 p99 <= 0.0125H（約 0.6／1.5 單位）：輪廓大致跟上，局部可能穿模。
  poor      其餘：不是滑桿組合能做出的身形（手修過、別的拓樸對位），裝備跟不上。
  same_as_base  基準 preset 本身就已達 usable：不必指定。
max 誤差只回報不入判定（少數縫線／生殖器頂點）。

Exit：0＝完成（含 poor／unfittable 的判定）；2＝輸入讀不到或格式錯。
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodyslide_mesh_check as mc  # noqa: E402
import bodyslide_fit_model as fm  # noqa: E402
from bodyslide_obody_config import preset_xml, read_presets  # noqa: E402

USABLE = (0.002, 0.006)
MARGINAL = (0.005, 0.0125)
SIZES = (('small', 'target0'), ('big', 'target1'))


def verdict(stats: dict) -> str:
    h = stats['height'] or 1.0
    for name, (r, p) in (('usable', USABLE), ('marginal', MARGINAL)):
        if stats['rms'] <= r * h and stats['p99'] <= p * h:
            return name
    return 'poor'


def worst(a: str, b: str) -> str:
    order = ['usable', 'marginal', 'poor']
    return order[max(order.index(a), order.index(b))]


def preset_values(path: Path, name: str) -> dict:
    presets = read_presets(Path(path))
    if name not in presets:
        raise fm.ModelError(f'{path}: no preset {name!r}')
    out = {'small': {}, 'big': {}}
    for (slider, size), v in presets[name]['sliders'].items():
        out[size][slider] = v
    return out


class Fitter:
    """一個滑桿集的模型＋法方程，供多套身體重用。"""

    def __init__(self, osp: Path, set_name: str, shapedata: Path, bounds=(-100.0, 200.0), ridge=1e-6):
        t = time.time()
        self.model = fm.load_model(Path(osp), set_name, Path(shapedata))
        self.vars = fm.fit_vars(self.model)
        self.A = fm.normal_matrix(self.model, self.vars)
        self.bounds, self.ridge = tuple(bounds), ridge
        self.setup_seconds = round(time.time() - t, 1)

    def evaluate(self, target: dict, mapping: dict, values: dict, size: str) -> dict:
        return fm.residual_stats(self.model, target, mapping, fm.apply_values(self.model, values, size))

    def fit(self, target0: Path, target1: Path, name: str, base: dict | None = None,
            compare: dict | None = None) -> dict:
        res = {'name': name, 'set': self.model['set'], 'targets': {}, 'sizes': {}, 'problems': []}
        targets = {}
        for size, key in SIZES:
            path = Path(target0 if key == 'target0' else target1)
            rep, pos = mc.parse_nif(path)
            targets[size] = pos
            res['targets'][size] = {'file': str(path), 'sha256': rep['sha256'],
                                    'shapes': {k: len(v) for k, v in pos.items()},
                                    'bodytri': [b['value'] for b in rep['bodytri']]}
        mapping, problems = fm.match_shapes(self.model, targets['small'])
        mapping1, problems1 = fm.match_shapes(self.model, targets['big'])
        res['problems'] = problems + [p for p in problems1 if p not in problems]
        if mapping != mapping1:
            res['problems'].append(f'_0/_1 shape mapping differ: {mapping} vs {mapping1}')
        res['mapping'] = mapping
        if res['problems']:
            res['verdict'] = 'unfittable'
            return res
        sliders, verdicts, base_verdicts = {}, [], []
        for size, _key in SIZES:
            values, info = fm.fit_size(self.model, self.vars, self.A, targets[size], mapping, self.bounds, self.ridge)
            stats = self.evaluate(targets[size], mapping, values, size)
            entry = {'fit': stats, 'verdict': verdict(stats), 'solver': info}
            if base:
                bstats = self.evaluate(targets[size], mapping, base[size], size)
                entry['baseline'] = bstats
                base_verdicts.append(verdict(bstats))
            if compare:
                entry['compare'] = self.evaluate(targets[size], mapping, compare[size], size)
            res['sizes'][size] = entry
            verdicts.append(entry['verdict'])
            for slider, v in values.items():
                sliders[(slider, size)] = v
        res['verdict'] = worst(*verdicts)
        if base_verdicts and worst(*base_verdicts) == 'usable':
            res['verdict'] = 'same_as_base'
        res['preset'] = {'name': name, 'set': self.model['set'], 'sliders': sliders}
        return res


def jsonable(res: dict) -> dict:
    out = dict(res)
    if 'preset' in out:
        p = out['preset']
        out['preset'] = {'name': p['name'], 'set': p['set'],
                         'sliders': {f'{k[0]}/{k[1]}': v for k, v in sorted(p['sliders'].items())}}
    return out


def cmd_fit(args) -> int:
    f = Fitter(args.osp, args.set, args.shapedata, args.bounds, args.ridge)
    base = preset_values(args.base_preset, args.base_name) if args.base_preset else None
    comp = preset_values(args.compare_preset, args.compare_name) if args.compare_preset else None
    res = f.fit(args.target0, args.target1, args.name, base, comp)
    res['model'] = {'base_nif': f.model['base_nif'], 'fit_sliders': len(f.vars), 'skipped': f.model['skipped'],
                    'setup_seconds': f.setup_seconds}
    if args.out_preset and 'preset' in res:
        Path(args.out_preset).write_text(preset_xml([res['preset']]), encoding='utf-8')
    text = json.dumps(jsonable(res), ensure_ascii=False, indent=1)
    if args.report:
        Path(args.report).write_text(text + '\n', encoding='utf-8')
    print(text if not args.report else json.dumps({'verdict': res['verdict'], 'report': str(args.report)}))
    return 0


def cmd_batch(args) -> int:
    spec = json.loads(Path(args.spec).read_text(encoding='utf-8'))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    base = preset_values(spec['base_preset']['file'], spec['base_preset']['name']) if spec.get('base_preset') else None
    fitters, summary, presets = {}, [], []
    for body in spec['bodies']:
        key = body['set']
        if key not in fitters:
            s = spec['sets'][key]
            fitters[key] = Fitter(s['osp'], s['set'], s['shapedata'], spec.get('bounds', (-100, 200)),
                                  spec.get('ridge', 1e-6))
        f = fitters[key]
        comp = preset_values(body['compare']['file'], body['compare']['name']) if body.get('compare') else None
        try:
            res = f.fit(body['w0'], body['w1'], body['preset_name'], base, comp)
        except (mc.FormatError, fm.ModelError, OSError) as exc:
            res = {'name': body['preset_name'], 'verdict': 'unfittable', 'problems': [f'{type(exc).__name__}: {exc}']}
        res['id'] = body['id']
        (out / f'fit-{body["id"]}.json').write_text(json.dumps(jsonable(res), ensure_ascii=False, indent=1) + '\n',
                                                     encoding='utf-8')
        row = {'id': body['id'], 'set': key, 'preset': body['preset_name'], 'verdict': res['verdict'],
               'problems': res.get('problems', [])}
        for size, entry in res.get('sizes', {}).items():
            row[f'{size}_rms'], row[f'{size}_p99'], row[f'{size}_max'] = (
                entry['fit']['rms'], entry['fit']['p99'], entry['fit']['max'])
            if 'baseline' in entry:
                row[f'{size}_base_rms'] = entry['baseline']['rms']
        summary.append(row)
        if res['verdict'] in ('usable', 'marginal') and 'preset' in res:
            presets.append(res['preset'])
        print(json.dumps(row, ensure_ascii=False), flush=True)
    (out / spec.get('presets_file', 'BSO-BodyFit-Presets.xml')).write_text(preset_xml(presets), encoding='utf-8')
    (out / 'summary.json').write_text(json.dumps({'fitters': {k: {'fit_sliders': len(f.vars), 'setup_seconds':
                                      f.setup_seconds, 'base_nif': f.model['base_nif'], 'skipped': f.model['skipped']}
                                      for k, f in fitters.items()}, 'rows': summary}, ensure_ascii=False, indent=1) + '\n',
                                      encoding='utf-8')
    return 0


def cmd_retarget(args) -> int:
    data = Path(args.nif).read_bytes()
    new, old = fm.retarget_bodytri(data, args.value)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(new)
    rep_a, pos_a = mc.parse_nif(Path(args.nif))
    rep_b, pos_b = mc.parse_nif(args.out)
    same = pos_a == pos_b and [s['name'] for s in rep_a['shapes']] == [s['name'] for s in rep_b['shapes']]
    ok = same and [b['value'] for b in rep_b['bodytri']] == [args.value] and not rep_b['errors']
    print(json.dumps({'ok': ok, 'out': str(args.out), 'old': old, 'new': args.value, 'positions_identical': same,
                      'sha256': rep_b['sha256']}, ensure_ascii=False))
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    f = sub.add_parser('fit')
    f.add_argument('--osp', type=Path, required=True)
    f.add_argument('--set', required=True)
    f.add_argument('--shapedata', type=Path, required=True)
    f.add_argument('--target0', type=Path, required=True)
    f.add_argument('--target1', type=Path, required=True)
    f.add_argument('--name', required=True, help='name of the fitted preset')
    f.add_argument('--base-preset', type=Path)
    f.add_argument('--base-name')
    f.add_argument('--compare-preset', type=Path)
    f.add_argument('--compare-name')
    f.add_argument('--out-preset', type=Path)
    f.add_argument('--report', type=Path)
    f.add_argument('--bounds', type=float, nargs=2, default=(-100.0, 200.0))
    f.add_argument('--ridge', type=float, default=1e-6)
    b = sub.add_parser('batch')
    b.add_argument('--spec', type=Path, required=True)
    b.add_argument('--out', type=Path, required=True)
    r = sub.add_parser('retarget-bodytri')
    r.add_argument('--nif', type=Path, required=True)
    r.add_argument('--out', type=Path, required=True)
    r.add_argument('--value', required=True)
    args = ap.parse_args(argv)
    try:
        return {'fit': cmd_fit, 'batch': cmd_batch, 'retarget-bodytri': cmd_retarget}[args.cmd](args)
    except (mc.FormatError, fm.ModelError, OSError, KeyError, ValueError) as exc:
        print(json.dumps({'ok': False, 'error': f'{type(exc).__name__}: {exc}'}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    sys.exit(main())
