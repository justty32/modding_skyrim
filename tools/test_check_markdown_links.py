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

    def test_ignores_fenced_code_and_external_urls_but_checks_anchor(self):
        source = self.root / "source.md"
        source.write_text(
            "```cpp\n[fake](missing.md)\n```\n"
            "# Heading\n[web](https://example.com) [section](#heading)\n",
            encoding="utf-8",
        )

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(broken, [])

    def test_ignores_links_inside_inline_code_spans(self):
        (self.root / "doc.md").write_text(
            "寫法 `[label](rel/path.md#anchor)` 或 ``x `[a](b.md)` y``；[ok](real.md)\n",
            encoding="utf-8",
        )
        (self.root / "real.md").write_text("# real\n", encoding="utf-8")
        checked, broken = check_file(self.root / "doc.md", self.root)
        self.assertEqual(checked, 1)
        self.assertEqual(broken, [])

    def test_reports_missing_same_file_anchor(self):
        source = self.root / "source.md"
        source.write_text("# Present\n[missing](#absent)\n", encoding="utf-8")

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(len(broken), 1)
        self.assertEqual(broken[0][1], "#absent")

    def test_accepts_cross_file_unicode_and_formatted_heading_anchor(self):
        target = self.root / "target.md"
        target.write_text("## `Batch 7`：終態驗收\n", encoding="utf-8")
        source = self.root / "source.md"
        source.write_text(
            "[target](target.md#batch-7終態驗收)\n", encoding="utf-8"
        )

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(broken, [])

    def test_reports_missing_cross_file_anchor(self):
        target = self.root / "target.md"
        target.write_text("# Present\n", encoding="utf-8")
        source = self.root / "source.md"
        source.write_text("[missing](target.md#absent)\n", encoding="utf-8")

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(len(broken), 1)
        self.assertEqual(broken[0][1], "target.md#absent")

    def test_accepts_setext_heading_anchor(self):
        source = self.root / "source.md"
        source.write_text("Setext Heading\n==============\n[link](#setext-heading)\n", encoding="utf-8")

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(broken, [])

    def test_preserves_literal_hyphens_in_heading_anchor(self):
        source = self.root / "source.md"
        source.write_text("# Version 1.8.1b-compatible\n[link](#version-181b-compatible)\n", encoding="utf-8")

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(broken, [])

    def test_duplicate_heading_anchors_get_numeric_suffix(self):
        source = self.root / "source.md"
        source.write_text(
            "# Repeat\n## Repeat\n[second](#repeat-1)\n", encoding="utf-8"
        )

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(broken, [])

    def test_accepts_explicit_html_anchor(self):
        source = self.root / "source.md"
        source.write_text(
            '<a id="fixed-anchor"></a>\n[target](#fixed-anchor)\n',
            encoding="utf-8",
        )

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(broken, [])

    def test_heading_anchor_ignores_inline_link_syntax(self):
        # A heading that links out slugs from the link text alone; without the
        # unwrapping step the URL bleeds into the slug as "batch-7targetmd".
        (self.root / "target.md").write_text("target\n", encoding="utf-8")
        source = self.root / "source.md"
        source.write_text(
            "## [Batch 7](target.md) 終態驗收\n[link](#batch-7-終態驗收)\n",
            encoding="utf-8",
        )

        checked, broken = check_file(source, self.root)

        # The heading's own link counts too, hence 2.
        self.assertEqual(checked, 2)
        self.assertEqual(broken, [])

    def test_headings_inside_fenced_code_are_not_anchors(self):
        # A shell comment in a fenced block is not a heading. If the anchor
        # harvest ignored fences it would mint "取消部署" and wave this through.
        source = self.root / "source.md"
        source.write_text(
            "```bash\n# 取消部署\n```\n[link](#取消部署)\n",
            encoding="utf-8",
        )

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(len(broken), 1)
        self.assertEqual(broken[0][1], "#取消部署")

    def test_closed_atx_heading_drops_trailing_hashes(self):
        # "## 標題 ##" renders as "標題"; keeping the closing run would slug it
        # as "標題-" and reject the correct anchor.
        source = self.root / "source.md"
        source.write_text("## 終態驗收 ##\n[link](#終態驗收)\n", encoding="utf-8")

        checked, broken = check_file(source, self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(broken, [])

    def test_cli_names_the_missing_anchor(self):
        target = self.root / "target.md"
        target.write_text("# 有的標題\n", encoding="utf-8")
        source = self.root / "source.md"
        source.write_text("[x](target.md#沒有的標題)\n", encoding="utf-8")

        stream = io.StringIO()
        with redirect_stdout(stream):
            result = main([str(source)])
        output = stream.getvalue()

        self.assertEqual(result, 1)
        self.assertIn("source.md:1: broken anchor:", output)
        self.assertIn('has no "#沒有的標題"', output)
        self.assertIn("1 missing anchor(s)", output)

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
