from pathlib import Path
from contextlib import redirect_stdout
import io
import sys
import tempfile
import unittest
from unittest.mock import patch

# check_markdown_links.py sits beside this file; it used to be imported from a
# scripts package that no longer exists.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_markdown_links import check_file, main, tracked_markdown


class MarkdownLinkCheckerTests(unittest.TestCase):
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

    def test_accepts_existing_relative_link(self):
        (self.root / "target.md").write_text("target\n", encoding="utf-8")
        source = self.root / "source.md"
        source.write_text("[target](target.md)\n", encoding="utf-8")

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(broken, [])

    def test_reports_missing_relative_link(self):
        source = self.root / "source.md"
        source.write_text("[missing](missing.md)\n", encoding="utf-8")

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(len(broken), 1)
        self.assertEqual(broken[0][1], "missing.md")

    def test_ignores_fenced_code_external_urls_and_anchors(self):
        source = self.root / "source.md"
        source.write_text(
            "```cpp\n[fake](missing.md)\n```\n"
            "[web](https://example.com) [section](#heading)\n",
            encoding="utf-8",
        )

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 0)
        self.assertEqual(broken, [])

    def test_symlink_uses_canonical_document_directory(self):
        canonical = self.root / "canonical"
        canonical.mkdir()
        (canonical / "target.md").write_text("target\n", encoding="utf-8")
        document = canonical / "document.md"
        document.write_text("[target](target.md)\n", encoding="utf-8")
        link_dir = self.root / "links"
        link_dir.mkdir()
        link = link_dir / "document.md"
        self.symlink_or_skip_without_windows_privilege(link, document)

        checked, broken = check_file(link, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(broken, [])

    def test_cli_returns_nonzero_for_broken_link(self):
        source = self.root / "source.md"
        source.write_text("[missing](missing.md)\n", encoding="utf-8")

        with redirect_stdout(io.StringIO()):
            result = main([str(source)])

        self.assertEqual(result, 1)

    def test_cli_can_skip_markdown_symlink(self):
        missing_target = self.root / "missing.md"
        link = self.root / "link.md"
        self.symlink_or_skip_without_windows_privilege(link, missing_target)

        with redirect_stdout(io.StringIO()):
            result = main(["--skip-symlinks", str(link)])

        self.assertEqual(result, 0)

    def test_tracked_markdown_skips_deleted_worktree_file(self):
        existing = self.root / "existing.md"
        existing.write_text("ok\n", encoding="utf-8")

        with patch(
            "check_markdown_links._ls_files",
            side_effect=[["existing.md", "deleted.md"], []],
        ):
            sources = tracked_markdown(self.root)

        self.assertEqual(sources, [existing])


if __name__ == "__main__":
    unittest.main()
