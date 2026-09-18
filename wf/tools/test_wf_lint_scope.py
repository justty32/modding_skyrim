"""wf-lint 的掃描範圍與計數：封存夾／submodule 不下鑽、BROKEN 計數不溢位。共用 helper 在 test_wf_lint。"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_wf_lint import run, write  # noqa: E402


class LinkScopeAndCountTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = self.d.name

    def tearDown(self):
        self.d.cleanup()

    def test_broken_count_does_not_overflow_exit_status(self):
        for index in range(300):
            write(self.root, f"docs/{index}.md", "[missing](nowhere.md)\n")
        r = run(self.root)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.count("BROKEN "), 300)
        self.assertIn("TOTAL broken=300", r.stdout)

    def test_markdown_scope_excludes_archive_reference_vendor_and_submodules(self):
        write(self.root, "README.md", "[missing](nowhere.md)\n")
        excluded_noise = (
            "[missing](missing.md)\n\n"
            "python3 tools/tabledb.py data.json\n\n"
            "{{placeholder}}\n\n"
            + "".join(f"- row {index}: {'x' * 40}\n" for index in range(30))
        )
        write(self.root, "archive/old.md", excluded_noise)
        write(self.root, "reference/target.md", "# present\n")
        write(self.root, "reference/source.md", excluded_noise + "[anchor](target.md#absent)\n")
        write(self.root, "vendor/package.md", "[vendor](missing.md)\n")
        write(self.root, "components/arbitrary-child/child.md", "[child](missing.md)\n")
        write(
            self.root,
            ".gitmodules",
            '[submodule "not-a-hard-coded-name"]\n'
            "\tpath = components/arbitrary-child\n"
            "\turl = https://example.invalid/child.git\n",
        )
        r = run(self.root)
        self.assertEqual(r.stdout.count("BROKEN "), 1)
        self.assertIn("BROKEN README.md -> nowhere.md", r.stdout)
        self.assertIn("TOTAL broken=1", r.stdout)
        self.assertNotIn("archive/old.md", r.stdout)
        self.assertNotIn("reference/source.md", r.stdout)
        self.assertNotIn("vendor/package.md", r.stdout)
        self.assertNotIn("arbitrary-child/child.md", r.stdout)
        self.assertIn("biglist=0", r.stdout)
        self.assertIn("querycmd=0", r.stdout)
        self.assertIn("residue={{=0", r.stdout)

    def test_mail_inbox_and_superseded_are_archived_like_archive(self):
        # 放信的 inbox/（含 done/）與 superseded/ 是不可改的原文：不掃壞連結／BIGLIST；workflows/inbox/ 照掃。
        mail = "[gone](missing.md)\n" + "".join(f"- 產出 {i}: {'x' * 40}\n" for i in range(30))
        write(self.root, "inbox/pending.md", mail)
        write(self.root, "inbox/done/from-other.md", mail)
        write(self.root, "workflows/dispatch/superseded/h1.md", mail)
        write(self.root, "workflows/inbox/README.md", "[doc](missing.md)\n")
        r = run(self.root)
        self.assertEqual(r.stdout.count("BROKEN "), 1)
        self.assertIn("BROKEN workflows/inbox/README.md", r.stdout)
        self.assertIn("biglist=0", r.stdout)
        self.assertIn("inbox_pending=1", r.stdout)


if __name__ == "__main__":
    unittest.main()
