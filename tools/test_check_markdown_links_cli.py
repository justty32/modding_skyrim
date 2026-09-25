from pathlib import Path
from contextlib import redirect_stdout
import io
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from markdown_links_testlib import MarkdownLinkFixture
from check_markdown_links import check_file, main, tracked_markdown


class MarkdownCliTests(MarkdownLinkFixture):
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

    def test_cli_returns_nonzero_for_broken_link(self):
        source = self.root / "source.md"
        source.write_text("[missing](missing.md)\n", encoding="utf-8")

        stream = io.StringIO()
        with patch("check_markdown_links.repo_root", return_value=self.root):
            with redirect_stdout(stream):
                result = main([str(source)])

        self.assertEqual(result, 1)
        self.assertIn("source.md:1: broken local link:", stream.getvalue())

    def test_cli_skip_uninitialized_submodules_is_opt_in(self):
        self.add_fake_gitlink()
        source = self.root / "source.md"
        source.write_text("[private](private/README.md)\n", encoding="utf-8")

        with patch("check_markdown_links.repo_root", return_value=self.root):
            with redirect_stdout(io.StringIO()):
                strict_result = main([str(source)])
            stream = io.StringIO()
            with redirect_stdout(stream):
                skipped_result = main(
                    ["--skip-uninitialized-submodules", str(source)]
                )

        self.assertEqual(strict_result, 1)
        self.assertEqual(skipped_result, 0)
        self.assertIn("1 target(s) not checked in uninitialized submodules", stream.getvalue())

    def test_cli_does_not_skip_initialized_submodule_missing_target(self):
        submodule = self.add_fake_gitlink()
        (submodule / ".git").mkdir(parents=True)
        source = self.root / "source.md"
        source.write_text("[private](private/missing.md)\n", encoding="utf-8")

        stream = io.StringIO()
        with patch("check_markdown_links.repo_root", return_value=self.root):
            with redirect_stdout(stream):
                result = main(
                    ["--skip-uninitialized-submodules", str(source)]
                )

        self.assertEqual(result, 1)
        self.assertIn("source.md:1: broken local link:", stream.getvalue())

    def test_cli_skip_uninitialized_submodules_keeps_parent_repo_strict(self):
        self.add_fake_gitlink()
        source = self.root / "source.md"
        source.write_text(
            "[private](private/README.md) [parent](missing.md)\n",
            encoding="utf-8",
        )

        stream = io.StringIO()
        with patch("check_markdown_links.repo_root", return_value=self.root):
            with redirect_stdout(stream):
                result = main(
                    ["--skip-uninitialized-submodules", str(source)]
                )

        self.assertEqual(result, 1)
        self.assertIn("missing.md", stream.getvalue())
        self.assertNotIn("private/README.md", stream.getvalue())

    def test_cli_excludes_source_matching_repeated_glob(self):
        backup = self.root / "backup"
        backup.mkdir()
        source = backup / "source.md"
        source.write_text("[missing](missing.md)\n", encoding="utf-8")

        stream = io.StringIO()
        with patch("check_markdown_links.repo_root", return_value=self.root):
            with redirect_stdout(stream):
                result = main(
                    [
                        "--exclude-source",
                        "elsewhere/*.md",
                        "--exclude-source",
                        "backup/*.md",
                        str(source),
                    ]
                )

        self.assertEqual(result, 0)
        self.assertNotIn("broken local link:", stream.getvalue())
        self.assertIn("1 source(s) excluded", stream.getvalue())

    def test_cli_ignores_nonexistent_exclude_source(self):
        source = self.root / "source.md"
        source.write_text("no links\n", encoding="utf-8")

        with patch("check_markdown_links.repo_root", return_value=self.root):
            with redirect_stdout(io.StringIO()):
                result = main(
                    ["--exclude-source", "missing-directory/", str(source)]
                )

        self.assertEqual(result, 0)

    def test_cli_can_skip_markdown_symlink(self):
        missing_target = self.root / "missing.md"
        link = self.root / "link.md"
        self.symlink_or_skip_without_windows_privilege(link, missing_target)

        with redirect_stdout(io.StringIO()):
            result = main(["--skip-symlinks", str(link)])

        self.assertEqual(result, 0)



if __name__ == "__main__":
    unittest.main()
