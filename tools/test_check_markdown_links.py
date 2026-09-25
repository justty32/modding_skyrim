from pathlib import Path
from contextlib import redirect_stdout
import io
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from markdown_links_testlib import MarkdownLinkFixture
from check_markdown_links import check_file, main, tracked_markdown


class MarkdownLinkCheckerTests(MarkdownLinkFixture):
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

    def test_ignores_links_inside_inline_code_spans(self):
        (self.root / "doc.md").write_text(
            "寫法 `[label](rel/path.md#anchor)` 或 ``x `[a](b.md)` y``；[ok](real.md)\n",
            encoding="utf-8",
        )
        (self.root / "real.md").write_text("# real\n", encoding="utf-8")
        checked, broken = check_file(self.root / "doc.md", self.root)
        self.assertEqual(checked, 1)
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
