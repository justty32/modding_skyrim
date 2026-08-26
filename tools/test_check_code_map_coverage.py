from contextlib import redirect_stdout
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_code_map_coverage as mod
from check_code_map_coverage import main


BASE_INDEX = (
    "# CODE_MAP\n\n| 檔案 | 職責 |\n|---|---|\n"
    "| `instance/tools/seeded.py` | fixture 自帶的腳本，先索引起來 |\n"
)


class CodeMapCoverageTests(unittest.TestCase):
    """A synthetic workspace: a mother repo with a real nested submodule.

    The submodule is not decoration. The failure this checker exists to prevent
    is a checker whose reach stops at a gitlink, so every test runs against a
    tree where that mistake would actually show up.
    """

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.line_remote = self.root / "line-remote.git"
        self.line_seed = self.root / "line-seed"
        self.repo = self.root / "workspace"

        self.git(self.root, "init", "--bare", "--initial-branch=main", str(self.line_remote))
        self.git(self.root, "init", "--initial-branch=main", str(self.line_seed))
        self.identity(self.line_seed)
        (self.line_seed / "tools").mkdir()
        (self.line_seed / "tools/seeded.py").write_text("print('seed')\n", encoding="utf-8")
        self.git(self.line_seed, "add", ".")
        self.git(self.line_seed, "commit", "-m", "seed line tools")
        self.git(self.line_seed, "remote", "add", "origin", str(self.line_remote))
        self.git(self.line_seed, "push", "-u", "origin", "main")

        self.git(self.root, "init", "--initial-branch=main", str(self.repo))
        self.identity(self.repo)
        (self.repo / "tools").mkdir()
        self.code_map = self.repo / "wf/workflows/common/code-map"
        self.code_map.mkdir(parents=True)
        # `seeded.py` ships with the submodule fixture; index it up front so
        # each test starts from a clean tree and only measures what it adds.
        self.write_index(BASE_INDEX)
        self.git(
            self.repo,
            "-c",
            "protocol.file.allow=always",
            "submodule",
            "add",
            str(self.line_remote),
            "instance",
        )
        self.git(self.repo, "add", ".")
        self.git(self.repo, "commit", "-m", "workspace with one line submodule")

        # Point the checker at this synthetic layout instead of the real one.
        self._saved_roots = mod.TOOL_ROOTS
        self._saved_pages = mod.INDEX_PAGES
        mod.TOOL_ROOTS = ("tools", "instance/tools")
        mod.INDEX_PAGES = ("wf/workflows/common/code-map/CODE_MAP.md",)

    def tearDown(self):
        mod.TOOL_ROOTS = self._saved_roots
        mod.INDEX_PAGES = self._saved_pages
        self.temp.cleanup()

    def git(self, cwd, *args, check=True):
        return subprocess.run(
            ["git", "-C", str(cwd), *args],
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def identity(self, repo):
        self.git(repo, "config", "user.name", "Coverage Test")
        self.git(repo, "config", "user.email", "coverage@example.invalid")

    def write_index(self, text):
        (self.code_map / "CODE_MAP.md").write_text(text, encoding="utf-8")

    def add_script(self, rel, *, commit=True):
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("print('tool')\n", encoding="utf-8")
        if commit:
            owner = self.repo / "instance" if rel.startswith("instance/") else self.repo
            inner = rel[len("instance/"):] if rel.startswith("instance/") else rel
            self.git(owner, "add", inner)
            self.git(owner, "commit", "-m", f"add {inner}")
        return path

    def write_baseline(self, *entries):
        (self.repo / "tools").mkdir(exist_ok=True)
        (self.repo / mod.BASELINE).write_text(
            "# baseline\n" + "".join(f"{e}\n" for e in entries), encoding="utf-8"
        )

    def run_check(self):
        output = io.StringIO()
        with redirect_stdout(output):
            result = main(["--repo", str(self.repo)])
        return result, output.getvalue()

    def test_indexed_script_passes(self):
        self.add_script("tools/documented.py")
        self.write_index(BASE_INDEX + "| `tools/documented.py` | 做某件事 |\n")

        result, output = self.run_check()

        self.assertEqual(result, 0)
        self.assertIn("coverage OK", output)

    def test_unindexed_script_fails_and_names_the_file(self):
        self.add_script("tools/orphan.py")

        result, output = self.run_check()

        self.assertNotEqual(result, 0)
        self.assertIn("UNINDEXED", output)
        self.assertIn("tools/orphan.py", output)

    def test_script_inside_a_submodule_is_reached(self):
        """The mother repo's own `git ls-files` stops at the gitlink.

        `instance/tools/hidden.py` is committed to the submodule and is
        invisible to `git -C <mother> ls-files instance/tools`. If the checker
        ever goes back to asking only the mother repo, this test goes red --
        which is the whole point, because that is the exact hole
        `check_markdown_links.py` shipped with.
        """
        self.add_script("instance/tools/hidden.py")

        mother_view = self.git(self.repo, "ls-files", "instance/tools").stdout
        self.assertEqual(mother_view.strip(), "", "前提失效：母 repo 竟然看得到 submodule 內的檔案")

        result, output = self.run_check()

        self.assertNotEqual(result, 0)
        self.assertIn("instance/tools/hidden.py", output)

    def test_baselined_script_stays_quiet(self):
        self.add_script("tools/known_debt.py")
        self.write_baseline("tools/known_debt.py")

        result, output = self.run_check()

        self.assertEqual(result, 0)
        self.assertNotIn("UNINDEXED", output)

    def test_baseline_does_not_excuse_a_different_new_script(self):
        """A baseline entry must cover exactly one path, not act as a blanket."""
        self.add_script("tools/known_debt.py")
        self.add_script("tools/brand_new.py")
        self.write_baseline("tools/known_debt.py")

        result, output = self.run_check()

        self.assertNotEqual(result, 0)
        self.assertIn("tools/brand_new.py", output)
        self.assertNotIn("tools/known_debt.py", output)

    def test_stale_baseline_entry_fails(self):
        self.write_baseline("tools/deleted_long_ago.py")

        result, output = self.run_check()

        self.assertNotEqual(result, 0)
        self.assertIn("STALE", output)
        self.assertIn("tools/deleted_long_ago.py", output)

    def test_untracked_script_is_ignored(self):
        """Only tracked files count; a scratch file must not fail the check."""
        self.add_script("tools/scratch.py", commit=False)

        result, output = self.run_check()

        self.assertEqual(result, 0)
        self.assertIn("coverage OK", output)


if __name__ == "__main__":
    unittest.main()
