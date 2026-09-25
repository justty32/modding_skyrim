from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class MarkdownLinkFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def symlink_or_skip_without_windows_privilege(self, link, target):
        try:
            link.symlink_to(target)
        except OSError as exc:
            if sys.platform == "win32" and getattr(exc, "winerror", None) == 1314:
                self.skipTest("Windows file-symlink privilege is unavailable")
            raise

    def add_fake_gitlink(self, name="private"):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "update-index",
                "--add",
                "--cacheinfo",
                "160000,1111111111111111111111111111111111111111," + name,
            ],
            check=True,
        )
        return self.root / name

