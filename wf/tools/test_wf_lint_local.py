"""專案自訂檢查 hook：<dir>/wf/tools/wf-lint-local.sh（test_wf_lint.py 已到 8 KB 上限，拆出）。"""
import os
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, "wf-lint.sh")


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    return p


def run(root, *args):
    return subprocess.run(["bash", LINT, *args, root], capture_output=True, text=True)


class LocalHookTest(unittest.TestCase):
    """hook 自己印 finding 行；非 0 結束碼計入 local=N，比照 biglist 只在 --strict 算失敗。"""

    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = self.d.name
        write(self.root, "notes/a.md", "# a\n")

    def tearDown(self):
        self.d.cleanup()

    def test_failing_hook_warns_plain_and_fails_strict(self):
        write(self.root, "wf/tools/wf-lint-local.sh",
              '#!/usr/bin/env bash\necho "LOCALFIND $1 strict=$2"\nexit 1\n')
        r = run(self.root)
        self.assertIn("LOCALFIND %s strict=0" % self.root, r.stdout)
        self.assertIn("local=1", r.stdout)
        self.assertEqual(r.returncode, 0)
        r = run(self.root, "--strict")
        self.assertIn("LOCALFIND %s strict=1" % self.root, r.stdout)
        self.assertIn("local=1", r.stdout.splitlines()[-1])
        self.assertEqual(r.returncode, 1)

    def test_no_hook_leaves_behaviour_unchanged(self):
        r = run(self.root)
        self.assertNotIn("LOCALFIND", r.stdout)
        self.assertIn("local=0", r.stdout)
        self.assertEqual(r.returncode, 0)
        r = run(self.root, "--strict")
        self.assertIn("local=0", r.stdout.splitlines()[-1])
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
