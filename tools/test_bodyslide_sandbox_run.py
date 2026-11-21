"""bodyslide_sandbox_run: preflight refusals, argv shape, result evaluation, real bwrap isolation."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

import bodyslide_sandbox_run as runner


class SandboxRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.mo2 = self.base / 'mo2'
        for d in ('mods', 'overwrite', 'profiles'):
            (self.mo2 / d).mkdir(parents=True)
        self.data = self.base / 'Data'
        self.data.mkdir()
        self.inst = self.base / 'instance'
        self.inst.mkdir()
        self.run_dir = self.base / 'run'
        (self.run_dir / 'tool' / 'SliderSets').mkdir(parents=True)
        (self.run_dir / 'tool' / 'BodySlide.exe').write_bytes(b'MZ')

    def call(self, *extra, run=None):
        argv = ['build', '--run-dir', str(run or self.run_dir), '--label', 'a', '--group', 'G',
                '--preset', 'P', '--tri', '--mo2-dir', str(self.mo2), '--game-data', str(self.data),
                '--instance-dir', str(self.inst), *extra]
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = runner.main(argv)
        return code, json.loads(out.getvalue())

    def test_dry_run_argv_shape(self):
        with mock.patch.object(runner.shutil, 'which', return_value='/usr/bin/x'):
            code, plan = self.call('--dry-run')
        self.assertEqual(code, 0)
        argv = plan['bwrap_argv']
        self.assertEqual(argv[:5], ['bwrap', '--ro-bind', '/', '/', '--dev'])
        binds = [argv[i + 1] for i, a in enumerate(argv) if a == '--bind']
        self.assertEqual(binds, [str(self.run_dir.resolve())])
        self.assertIn('--unshare-net', argv)
        self.assertIn(str(self.run_dir.resolve() / 'tool' / 'SliderSets'), argv)
        self.assertEqual(plan['wine_argv'][-2:], ['-t', runner.win_path(self.run_dir.resolve() / 'rounds' / 'a' / 'output')])
        self.assertIn('-tri', plan['wine_argv'])
        self.assertFalse((self.run_dir / 'rounds').exists())

    def test_refuses_run_dir_inside_mods(self):
        bad = self.mo2 / 'mods' / 'Output'
        shutil.copytree(self.run_dir, bad)
        with mock.patch.object(runner.shutil, 'which', return_value='/usr/bin/x'):
            code, report = self.call('--dry-run', run=bad)
        self.assertEqual(code, 2)
        self.assertTrue(any('inside live mods' in e for e in report['errors']))

    def test_refuses_unknown_live_roots(self):
        argv = ['build', '--run-dir', str(self.run_dir), '--label', 'a', '--group', 'G', '--dry-run']
        with mock.patch.dict(runner.os.environ, {}, clear=True), \
                mock.patch.object(runner.guard, '_git_root', return_value=None), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(runner.main(argv), 2)
        self.assertIn('live roots unknown', json.loads(out.getvalue())['errors'][0])

    def test_refuses_existing_round_bad_label_missing_exe_and_tools(self):
        (self.run_dir / 'rounds' / 'a').mkdir(parents=True)
        (self.run_dir / 'tool' / 'BodySlide.exe').unlink()
        with mock.patch.object(runner.shutil, 'which', return_value=None):
            code, report = self.call('--dry-run')
        self.assertEqual(code, 2)
        text = ' '.join(report['errors'])
        for needle in ('round already exists', 'BodySlide.exe', 'bwrap not found'):
            self.assertIn(needle, text)

    def test_refuses_non_ascii_and_dirty_fallback(self):
        odd = self.base / 'run本輪'
        shutil.copytree(self.run_dir, odd)
        (odd / 'safe-fallback').mkdir()
        (odd / 'safe-fallback' / 'x.nif').write_bytes(b'x')
        with mock.patch.object(runner.shutil, 'which', return_value='/usr/bin/x'):
            code, report = self.call('--dry-run', run=odd)
        self.assertEqual(code, 2)
        self.assertTrue(any('ASCII' in e for e in report['errors']))
        self.assertTrue(any('safe-fallback' in e for e in report['errors']))

    def test_win_path(self):
        self.assertEqual(runner.win_path(Path('/a/b')), 'Z:\\a\\b\\')

    def test_evaluate(self):
        good = dict(wine_returncode=0, timed_out=False)
        outs = [dict(path='meshes/x_0.nif')]
        self.assertEqual(runner.evaluate(good, runner.COMPLETION[0], outs, [], ['MESHES/x_0.nif']), [])
        self.assertTrue(runner.evaluate(good, 'old log only', outs, [], []))
        self.assertTrue(runner.evaluate(dict(wine_returncode=0, timed_out=True), runner.COMPLETION[1], outs, [], []))
        self.assertTrue(runner.evaluate(good, runner.COMPLETION[0], [], [], []))
        self.assertTrue(runner.evaluate(good, runner.COMPLETION[0], outs, ['leak.nif'], []))
        self.assertTrue(runner.evaluate(good, runner.COMPLETION[0], outs, [], ['meshes/x_1.nif']))

    def test_log_slice_append_rewrite_and_missing(self):
        log = self.base / 'Log_BS.txt'
        old = b'old ' + runner.COMPLETION[0].encode()
        log.write_bytes(old + b' new round')
        self.assertEqual(runner.log_slice(log, old), (b' new round', 'append'))
        log.write_bytes(b'fresh run')  # rewritten: the old completion line must not leak in
        self.assertEqual(runner.log_slice(log, old), (b'fresh run', 'rewritten'))
        self.assertEqual(runner.log_slice(self.base / 'none.txt', old), (b'', 'missing'))
        s1 = b'[#Log Sat 1]\nProcessing A\n' + runner.COMPLETION[1].encode() + b'\n'
        s2 = b'[#Log Sat 2]\nProcessing B\n'
        log.write_bytes(s1 + s2)  # rolling log: only the last session is this round
        self.assertEqual(runner.log_slice(log, s1), (s2, 'last-session'))
        log.write_bytes(s1)  # BodySlide never started: the last session is the old one
        self.assertEqual(runner.log_slice(log, s1), (b'', 'stale'))

    def test_real_bwrap_only_run_dir_writable(self):
        if shutil.which('bwrap') is None:
            self.skipTest('bwrap not installed')
        # outside dir next to this file, not under /tmp (the sandbox's private /tmp would hide it)
        holder = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent, prefix='.bwrap-probe-')
        self.addCleanup(holder.cleanup)
        outside = Path(holder.name)
        run = self.run_dir.resolve()
        script = (f'test -d {outside} || exit 7; touch {outside}/bad 2>/dev/null && exit 8; '
                  f'touch {run}/tool/SliderSets/x 2>/dev/null && exit 9; touch {run}/ok')
        argv = runner.bwrap_argv(run, ['sh', '-c', script], {'PATH': '/usr/bin:/bin'})
        proc = subprocess.run(argv, capture_output=True, timeout=30)
        if proc.returncode not in (0, 7, 8, 9):
            self.skipTest('bwrap unusable here: ' + proc.stderr.decode(errors='replace'))
        self.assertEqual(proc.returncode, 0, 'outside visible? 7=hidden 8=outside writable 9=tool writable')
        self.assertTrue((run / 'ok').exists())
        self.assertFalse((outside / 'bad').exists())

if __name__ == '__main__':
    unittest.main()
