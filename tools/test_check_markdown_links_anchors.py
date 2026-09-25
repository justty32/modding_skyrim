from pathlib import Path
from contextlib import redirect_stdout
import io
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from markdown_links_testlib import MarkdownLinkFixture
from check_markdown_links import check_file, main, tracked_markdown


class MarkdownAnchorTests(MarkdownLinkFixture):
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



if __name__ == "__main__":
    unittest.main()
