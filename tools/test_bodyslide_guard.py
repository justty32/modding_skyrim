"""bodyslide_guard: live-root discovery and both-direction isolation checks."""
from pathlib import Path
import tempfile
import unittest

import bodyslide_guard as guard


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.mo2 = self.base / 'mo2'
        for d in ('mods/A', 'overwrite', 'profiles'):
            (self.mo2 / d).mkdir(parents=True)
        self.data = self.base / 'game' / 'Data'
        self.data.mkdir(parents=True)
        self.instance = self.base / 'repo' / 'instance'
        self.instance.mkdir(parents=True)
        self.roots, self.missing = guard.live_roots(self.mo2, game_data=self.data,
                                                    instance=self.instance, env={})

    def test_roots_from_mo2_dir(self):
        self.assertEqual(self.missing, [])
        self.assertEqual(self.roots['mods'], self.mo2 / 'mods')
        self.assertEqual(self.roots['profiles'], self.mo2 / 'profiles')

    def test_env_fallback_and_missing(self):
        roots, missing = guard.live_roots(env={'MO2_DIR': str(self.mo2)}, instance=self.instance)
        self.assertEqual(missing, ['game_data'])
        self.assertEqual(roots['overwrite'], self.mo2 / 'overwrite')

    def test_outside_is_ok(self):
        run = self.base / 'staging' / 'run'
        run.mkdir(parents=True)
        self.assertEqual(guard.check_isolated({'run': run}, self.roots), [])

    def test_inside_and_containing_refused(self):
        for bad in (self.mo2 / 'mods' / 'A' / 'out', self.mo2 / 'overwrite', self.data / 'x',
                    self.instance / 'profiles', self.base, Path('/')):
            with self.subTest(bad=bad):
                self.assertTrue(guard.check_isolated({'run': bad}, self.roots))

    def test_symlink_into_live_refused(self):
        link = self.base / 'innocent'
        link.symlink_to(self.mo2 / 'mods' / 'A')
        errors = guard.check_isolated({'run': link}, self.roots)
        self.assertTrue(any('inside live mods' in e for e in errors))

    def test_non_ascii(self):
        self.assertTrue(guard.non_ascii('/x/本輪'))
        self.assertFalse(guard.non_ascii('/x/run-1'))


if __name__ == '__main__':
    unittest.main()
