"""Exercise the tracked hook after real Git checkout, including CRLF defaults."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("bash") and shutil.which("python3"),
                     "the tracked hook requires bash and python3")
class HookCheckoutTests(unittest.TestCase):
    def git(self, repo, *args, check=True):
        return subprocess.run(
            ["git", "-C", str(repo), *args], check=check,
            capture_output=True, text=True,
        )

    def identity(self, repo):
        self.git(repo, "config", "user.name", "Hook Test")
        self.git(repo, "config", "user.email", "hook@example.invalid")

    def test_checkout_and_git_commit_preserve_hook_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            seed = base / "seed"
            self.git(base, "init", "--initial-branch=main", str(seed))
            self.identity(seed)
            self.git(seed, "config", "core.autocrlf", "false")
            self.git(seed, "config", "core.hooksPath", ".git/no-hooks")
            hook = seed / "tools/hooks/pre-commit"
            hook.parent.mkdir(parents=True)
            hook.write_bytes((ROOT / "tools/hooks/pre-commit").read_bytes())
            (seed / ".gitattributes").write_bytes((ROOT / ".gitattributes").read_bytes())
            (seed / "ordinary.txt").write_bytes(b"ordinary text\n")
            self.git(seed, "add", ".")
            self.git(seed, "update-index", "--chmod=+x", "tools/hooks/pre-commit")
            self.git(seed, "commit", "-m", "seed")

            for autocrlf in ("true", "false", "input"):
                with self.subTest(autocrlf=autocrlf):
                    checkout = base / autocrlf
                    self.git(base, "clone", "--no-checkout", str(seed), str(checkout))
                    self.git(checkout, "config", "core.autocrlf", autocrlf)
                    self.git(checkout, "checkout", "main")
                    self.identity(checkout)
                    self.git(checkout, "config", "core.hooksPath", "tools/hooks")
                    self.assertNotIn(b"\r", (checkout / "tools/hooks/pre-commit").read_bytes())
                    expected = b"ordinary text\r\n" if autocrlf == "true" else b"ordinary text\n"
                    self.assertEqual((checkout / "ordinary.txt").read_bytes(), expected)

                    # Public checkout without the private gate retains its documented fallback.
                    allowed = self.git(checkout, "commit", "--allow-empty", "-m", "without gate")
                    self.assertIn("略過大小閘門", allowed.stderr)

                    # A fixture gate checks arguments and proves rejection reaches Git.
                    gate = checkout / "agentctl/tools/repo_hooks/precommit_gate.py"
                    gate.parent.mkdir(parents=True)
                    gate.write_text(
                        "import pathlib, sys\n"
                        "assert sys.argv[1:3] == ['--policy', 'mother']\n"
                        "assert sys.argv[3] == '--repo'\n"
                        "assert pathlib.Path(sys.argv[4]).resolve() == pathlib.Path.cwd()\n"
                        "print('fixture gate rejected', file=sys.stderr)\n"
                        "sys.exit(1)\n", encoding="utf-8",
                    )
                    before = self.git(checkout, "rev-parse", "HEAD").stdout
                    blocked = self.git(checkout, "commit", "--allow-empty", "-m", "blocked", check=False)
                    self.assertNotEqual(blocked.returncode, 0)
                    self.assertIn("fixture gate rejected", blocked.stderr)
                    self.assertEqual(self.git(checkout, "rev-parse", "HEAD").stdout, before)


if __name__ == "__main__":
    unittest.main()
