from contextlib import redirect_stdout
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_submodule_pins import _remote_branches_containing, main


TOOLS_DIR = Path(__file__).resolve().parent


class PinGuardFixture(unittest.TestCase):
    """A parent repo with one real submodule, both wired to throwaway remotes.

    Held separately from the tests so a second test class can reuse it without
    inheriting -- and re-running -- the first class's cases.
    """

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.sub_remote = self.root / "sub-remote.git"
        self.sub_seed = self.root / "sub-seed"
        self.parent_remote = self.root / "parent-remote.git"
        self.parent = self.root / "parent"

        self.git(self.root, "init", "--bare", "--initial-branch=main", str(self.sub_remote))
        self.git(self.root, "init", "--initial-branch=main", str(self.sub_seed))
        self.identity(self.sub_seed)
        (self.sub_seed / "payload.txt").write_text("published\n", encoding="utf-8")
        self.git(self.sub_seed, "add", "payload.txt")
        self.git(self.sub_seed, "commit", "-m", "published submodule commit")
        self.git(self.sub_seed, "remote", "add", "origin", str(self.sub_remote))
        self.git(self.sub_seed, "push", "-u", "origin", "main")

        self.git(self.root, "init", "--bare", "--initial-branch=main", str(self.parent_remote))
        self.git(self.root, "init", "--initial-branch=main", str(self.parent))
        self.identity(self.parent)
        self.git(
            self.parent,
            "-c",
            "protocol.file.allow=always",
            "submodule",
            "add",
            str(self.sub_remote),
            "modules/demo",
        )
        self.identity(self.submodule)
        self.git(self.parent, "commit", "-am", "add published submodule")
        self.git(self.parent, "remote", "add", "origin", str(self.parent_remote))
        self.git(self.parent, "push", "-u", "origin", "main")
        self.remote_parent_sha = self.rev_parse(self.parent, "HEAD")

    def tearDown(self):
        self.temp.cleanup()

    @property
    def submodule(self):
        return self.parent / "modules/demo"

    def git(self, cwd, *args, check=True):
        return subprocess.run(
            ["git", "-C", str(cwd), *args],
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def identity(self, repo):
        self.git(repo, "config", "user.name", "Pin Guard Test")
        self.git(repo, "config", "user.email", "pin-guard@example.invalid")

    def rev_parse(self, repo, ref):
        return self.git(repo, "rev-parse", ref).stdout.strip()

    def commit_submodule(self, publish=False):
        payload = self.submodule / "payload.txt"
        payload.write_text(payload.read_text(encoding="utf-8") + "next\n", encoding="utf-8")
        self.git(self.submodule, "add", "payload.txt")
        self.git(self.submodule, "commit", "-m", "next submodule commit")
        sha = self.rev_parse(self.submodule, "HEAD")
        if publish:
            self.git(self.submodule, "push", "origin", "HEAD:main")
        return sha

    def commit_parent_pin(self):
        self.git(self.parent, "add", "modules/demo")
        self.git(self.parent, "commit", "-m", "bump submodule pin")
        return self.rev_parse(self.parent, "HEAD")

    def run_guard(self, local_sha, remote_sha=None):
        output = io.StringIO()
        remote_sha = remote_sha or self.remote_parent_sha
        with redirect_stdout(output):
            result = main(
                [
                    "--repo",
                    str(self.parent),
                    "--remote",
                    "origin",
                    "--update",
                    "refs/heads/main",
                    local_sha,
                    "refs/heads/main",
                    remote_sha,
                ]
            )
        return result, output.getvalue()

