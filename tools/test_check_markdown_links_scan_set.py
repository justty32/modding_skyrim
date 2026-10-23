"""What the checker scans, not what it finds.

Regression cover for 2026-10-23: the scan set came from `git ls-files`, so a
document written but not yet `git add`ed was never opened and the run still
printed OK. A link checker that silently skips the files you just wrote is
worse than no link checker, because its green is quoted as evidence.
"""

from pathlib import Path
from contextlib import redirect_stdout
import io
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from markdown_links_testlib import MarkdownLinkFixture
from check_markdown_links import main, tracked_markdown, untracked_markdown


class ScanSetTests(MarkdownLinkFixture):
    def test_untracked_markdown_with_broken_link_is_caught(self):
        self.init_git_repo()
        committed = self.root / "committed.md"
        committed.write_text("# committed\n", encoding="utf-8")
        self.git("add", "committed.md")
        fresh = self.root / "fresh-index.md"
        fresh.write_text("[gone](no-such-file.md)\n", encoding="utf-8")

        stream = io.StringIO()
        with patch("check_markdown_links.repo_root", return_value=self.root):
            with redirect_stdout(stream):
                result = main([])
        output = stream.getvalue()

        self.assertEqual(result, 1)
        self.assertIn("fresh-index.md:1: broken local link:", output)
        self.assertIn("(tracked 1, untracked 1)", output)

    def test_ignored_markdown_is_not_scanned(self):
        self.init_git_repo()
        (self.root / ".gitignore").write_text("repos/\n", encoding="utf-8")
        self.git("add", ".gitignore")
        clone = self.root / "repos" / "third-party"
        clone.mkdir(parents=True)
        (clone / "README.md").write_text("[gone](no-such-file.md)\n", encoding="utf-8")

        stream = io.StringIO()
        with patch("check_markdown_links.repo_root", return_value=self.root):
            with redirect_stdout(stream):
                result = main([])
        output = stream.getvalue()

        self.assertEqual(result, 0)
        self.assertNotIn("broken local link:", output)
        self.assertIn("(tracked 0, untracked 0)", output)

    def test_scan_set_splits_tracked_from_untracked(self):
        self.init_git_repo()
        (self.root / "a.md").write_text("# a\n", encoding="utf-8")
        (self.root / "b.md").write_text("# b\n", encoding="utf-8")
        self.git("add", "a.md", "b.md")
        (self.root / "c.md").write_text("# c\n", encoding="utf-8")

        tracked = tracked_markdown(self.root)
        untracked = untracked_markdown(self.root)

        self.assertEqual(
            sorted(path.name for path in tracked), ["a.md", "b.md"]
        )
        self.assertEqual([path.name for path in untracked], ["c.md"])
        self.assertEqual(set(tracked) & set(untracked), set())

    def test_untracked_markdown_reaches_into_submodules(self):
        submodule = self.add_fake_gitlink()
        submodule.mkdir()
        subprocess.run(["git", "init", "-q", str(submodule)], check=True)
        (submodule / "fresh.md").write_text("# fresh\n", encoding="utf-8")

        untracked = untracked_markdown(self.root)

        self.assertEqual(untracked, [submodule / "fresh.md"])

    def test_explicit_paths_report_no_scan_breakdown(self):
        source = self.root / "source.md"
        source.write_text("no links\n", encoding="utf-8")

        stream = io.StringIO()
        with patch("check_markdown_links.repo_root", return_value=self.root):
            with redirect_stdout(stream):
                result = main([str(source)])

        self.assertEqual(result, 0)
        self.assertNotIn("tracked", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
