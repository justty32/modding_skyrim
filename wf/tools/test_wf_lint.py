import os
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, "wf-lint.sh")
CHECKS = os.path.join(HERE, "wf-lint-checks.sh")


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    return p


def run(root, *args):
    return subprocess.run(
        ["bash", LINT, *args, root],
        capture_output=True, text=True,
    )


class QueryCmdTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = self.d.name

    def tearDown(self):
        self.d.cleanup()

    def test_command_line_form_is_reported(self):
        write(self.root, "notes/a.md",
              "# a\n\n已抽到 x.json（3 列）。怎麼查：\n\n```\n"
              "python3 ../wf/tools/tabledb.py x.json\n```\n")
        r = run(self.root)
        self.assertIn("QUERYCMD notes/a.md:6", r.stdout)
        self.assertIn("querycmd=1", r.stdout)

    def test_bare_tool_path_without_python3_is_reported(self):
        write(self.root, "notes/b.md", "# b\n\n- `wf/tools/tabledb.py logs/x.json get 0`\n")
        r = run(self.root)
        self.assertIn("QUERYCMD notes/b.md:3", r.stdout)
        self.assertIn("querycmd=1", r.stdout)

    def test_bare_tool_name_is_not_reported(self):
        write(self.root, "notes/c.md", "# c\n\n讀寫走 `tabledb.py`，不整份讀進 context。\n")
        r = run(self.root)
        self.assertNotIn("QUERYCMD", r.stdout)
        self.assertIn("querycmd=0", r.stdout)

    def test_exempt_paths_and_files(self):
        cmd = "python3 tools/tabledb.py x.json get 0\n"
        write(self.root, "wf/workflows/common/x.md", cmd)
        write(self.root, "archive/old.md", cmd)
        write(self.root, "AGENTS.md", cmd)
        write(self.root, "notes/AGENTS.md", cmd)
        write(self.root, "workflows/common/data-files.md", cmd)
        write(self.root, "workflows/common/data-files-fmt.md", cmd)
        write(self.root, "workflows/tidy.md", cmd)
        r = run(self.root)
        self.assertNotIn("QUERYCMD", r.stdout)
        self.assertIn("querycmd=0", r.stdout)

    def test_skills_dir_exempt_but_sibling_dir_still_reported(self):
        cmd = "python3 tools/tabledb.py x.json get 0\n"
        write(self.root, "skills/foo/SKILL.md", cmd)
        write(self.root, "notes/a.md", cmd)
        r = run(self.root)
        self.assertNotIn("skills/foo/SKILL.md", r.stdout)
        self.assertIn("QUERYCMD notes/a.md:1", r.stdout)
        self.assertIn("querycmd=1", r.stdout)

    def test_strict_fails_plain_warns(self):
        write(self.root, "notes/a.md", "# a\n\npython3 wf/tools/tabledb.py x.json\n")
        self.assertEqual(run(self.root).returncode, 0)
        r = run(self.root, "--strict")
        self.assertEqual(r.returncode, 1)
        self.assertIn("querycmd=1", r.stdout.splitlines()[-1])

    def test_multiple_hits_counted_per_line(self):
        write(self.root, "notes/a.md",
              "# a\n\n```\npython3 tools/tabledb.py x.json\n"
              "python3 tools/tabledb.py x.json get 0\n"
              "python3 tools/tabledb.py x.json find id=1\n```\n")
        r = run(self.root)
        self.assertIn("querycmd=3", r.stdout)


class PercentEncodedLinkTest(unittest.TestCase):
    """連結目標含空白／括號時必須 percent-encode，檢查器要解碼後再判存在。"""

    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = self.d.name

    def tearDown(self):
        self.d.cleanup()

    def test_encoded_link_to_existing_file_is_not_broken(self):
        write(self.root, "raws/BFCO - Framework (SSE AE VR).txt", "x\n")
        write(self.root, "notes/a.md",
              "[raw](../raws/BFCO%20-%20Framework%20%28SSE%20AE%20VR%29.txt)\n")
        r = run(self.root)
        self.assertNotIn("BROKEN", r.stdout)
        self.assertIn("TOTAL broken=0", r.stdout)
        self.assertEqual(r.returncode, 0)

    def test_encoded_link_to_missing_file_is_still_broken(self):
        write(self.root, "notes/a.md", "[raw](../raws/No%20Such%20File.txt)\n")
        r = run(self.root)
        self.assertIn("BROKEN notes/a.md -> ../raws/No%20Such%20File.txt", r.stdout)
        self.assertIn("TOTAL broken=1", r.stdout)

    def test_unencoded_link_still_judged_on_the_literal_path(self):
        write(self.root, "raws/plain.txt", "x\n")
        write(self.root, "notes/a.md",
              "[ok](../raws/plain.txt)\n\n[bad](../raws/absent.txt)\n")
        r = run(self.root)
        self.assertEqual(r.stdout.count("BROKEN "), 1)
        self.assertIn("BROKEN notes/a.md -> ../raws/absent.txt", r.stdout)

    def test_malformed_percent_escape_is_broken_not_a_crash(self):
        write(self.root, "notes/a.md", "[bad](../raws/100%25%ZZ.txt)\n")
        r = run(self.root)
        self.assertIn("BROKEN notes/a.md -> ../raws/100%25%ZZ.txt", r.stdout)
        self.assertIn("TOTAL broken=1", r.stdout)


class OversizeSubmoduleTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = self.d.name

    def tearDown(self):
        self.d.cleanup()

    def test_submodule_path_skipped_but_own_file_reported(self):
        write(self.root, "ext/mod/big.txt", "x" * 9000)
        write(self.root, "own/big.txt", "x" * 9000)
        write(self.root, ".gitmodules", '[submodule "ext"]\n\tpath = ext/mod\n')
        r = subprocess.run(
            ["bash", "-c", f'. "{CHECKS}"; list_oversize_files "{self.root}"'],
            capture_output=True, text=True,
        )
        self.assertIn("own/big.txt", r.stdout)
        self.assertNotIn("ext/mod/big.txt", r.stdout)


class VenvPruneTest(unittest.TestCase):
    """.venv／venv（Python 虛擬環境）不下鑽：uv/venv 專案的 site-packages 不該被當成專案檔掃。"""

    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = self.d.name

    def tearDown(self):
        self.d.cleanup()

    def test_oversize_scan_skips_dot_venv_and_venv(self):
        write(self.root, ".venv/lib/python3.13/site-packages/openai/README.md", "x" * 9000)
        write(self.root, "venv/lib/site-packages/foo/README.md", "x" * 9000)
        write(self.root, "own/big.txt", "x" * 9000)
        r = subprocess.run(
            ["bash", "-c", f'. "{CHECKS}"; list_oversize_files "{self.root}"'],
            capture_output=True, text=True,
        )
        self.assertIn("own/big.txt", r.stdout)
        self.assertNotIn(".venv", r.stdout)
        self.assertNotIn("/venv/", r.stdout)

    def test_owned_files_scan_skips_dot_venv_and_venv(self):
        write(self.root, ".venv/lib/python3.13/site-packages/openai/README.md", "# stray\n")
        write(self.root, "venv/lib/site-packages/foo/README.md", "# stray\n")
        write(self.root, "notes/a.md", "# a\n")
        r = subprocess.run(
            ["bash", "-c", f'. "{CHECKS}"; list_md "{self.root}"'],
            capture_output=True, text=True,
        )
        self.assertIn("notes/a.md", r.stdout)
        self.assertNotIn(".venv", r.stdout)
        self.assertNotIn("/venv/", r.stdout)


if __name__ == "__main__":
    unittest.main()
