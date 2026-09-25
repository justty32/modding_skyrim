import contextlib
import io
from pathlib import Path
import tempfile
import unittest

import check_anchors


def run(root: str) -> tuple[int, str]:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = check_anchors.main([root])
    return code, output.getvalue()


class CheckAnchorsTest(unittest.TestCase):
    def test_chinese_heading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text("# 分層原則\n", encoding="utf-8")
            (root / "b.md").write_text("[x](a.md#分層原則)\n", encoding="utf-8")
            self.assertEqual(run(directory), (0, ""))

    def test_duplicate_headings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text("## 流程\n## 流程\n", encoding="utf-8")
            source = root / "b.md"
            source.write_text("[a](a.md#流程) [b](a.md#流程-1)\n", encoding="utf-8")
            self.assertEqual(run(directory), (0, ""))
            source.write_text("[x](a.md#流程-2)\n", encoding="utf-8")
            code, output = run(directory)
            self.assertEqual(code, 1)
            self.assertIn("a.md#流程-2", output)

    def test_explicit_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text('<a id="my-anchor"></a>\n', encoding="utf-8")
            (root / "b.md").write_text("[x](a.md#my-anchor)\n", encoding="utf-8")
            self.assertEqual(run(directory), (0, ""))

    def test_link_in_code_fence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text("# 有\n", encoding="utf-8")
            (root / "b.md").write_text("```\n[x](a.md#不存在)\n```\n", encoding="utf-8")
            self.assertEqual(run(directory), (0, ""))

    def test_cross_file_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text("# 某節\n", encoding="utf-8")
            source = root / "b.md"
            source.write_text("[x](a.md#某節)\n", encoding="utf-8")
            self.assertEqual(run(directory), (0, ""))
            source.write_text("[x](a.md#別節)\n", encoding="utf-8")
            code, output = run(directory)
            self.assertEqual(code, 1)
            self.assertIn("BROKEN-ANCHOR b.md:1 -> a.md#別節", output)

    def test_missing_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text("# 有\n", encoding="utf-8")
            (root / "b.md").write_text("[x](a.md#沒有)\n", encoding="utf-8")
            code, output = run(directory)
            self.assertEqual(code, 1)
            self.assertIn("BROKEN-ANCHOR", output)

    def test_missing_file_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text("[x](missing.md#frag)\n", encoding="utf-8")
            self.assertEqual(run(directory), (0, ""))

    def test_excluded_roots_and_gitmodules_are_not_scanned(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in (
                "archive/old.md",
                "reference/source.md",
                "vendor/package.md",
                "components/arbitrary-child/child.md",
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("[x](target.md#missing)\n", encoding="utf-8")
                (path.parent / "target.md").write_text("# present\n", encoding="utf-8")
            (root / ".gitmodules").write_text(
                '[submodule "dynamic"]\n'
                "\tpath = components/arbitrary-child\n"
                "\turl = https://example.invalid/child.git\n",
                encoding="utf-8",
            )
            self.assertEqual(run(directory), (0, ""))


if __name__ == "__main__":
    unittest.main()
