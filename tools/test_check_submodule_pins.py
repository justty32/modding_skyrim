from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from submodule_pins_testlib import PinGuardFixture, TOOLS_DIR
from check_submodule_pins import _remote_branches_containing


class SubmodulePinGuardTests(PinGuardFixture):
    def test_unchanged_pin_allows_push_even_with_unpublished_submodule_head(self):
        self.commit_submodule(publish=False)
        (self.parent / "note.txt").write_text("parent only\n", encoding="utf-8")
        self.git(self.parent, "add", "note.txt")
        self.git(self.parent, "commit", "-m", "parent-only change")

        result, output = self.run_guard(self.rev_parse(self.parent, "HEAD"))

        self.assertEqual(result, 0)
        self.assertIn("no gitlink changes", output)

    def test_published_pin_allows_push(self):
        self.commit_submodule(publish=True)
        local_sha = self.commit_parent_pin()

        result, output = self.run_guard(local_sha)

        self.assertEqual(result, 0)
        self.assertIn("is available remotely", output)
        self.assertNotIn("remote default branch", output)

    def test_side_branch_pin_warns_but_allows_push(self):
        sub_sha = self.commit_submodule(publish=False)
        self.git(self.submodule, "push", "origin", "HEAD:side-branch")
        self.git(self.submodule, "fetch", "origin")
        local_sha = self.commit_parent_pin()

        result, output = self.run_guard(local_sha)

        self.assertEqual(result, 0)
        self.assertIn("WARN", output)
        self.assertIn(f"modules/demo @ {sub_sha[:12]}", output)
        self.assertIn("origin/side-branch", output)
        self.assertIn("remote default branch(es) origin/main", output)

    def test_pin_on_another_remotes_default_branch_does_not_warn(self):
        """一個 submodule 可以有多個 remote（houseCARL：`origin` 是上游、`fork` 是自有 fork）。

        pin 落在 `fork` 的預設分支上時不該被判成「掛在側分支」——即使呼叫 guard 時
        傳入的是 `origin`，而 `origin/main` 並不含這個 commit。
        """
        fork_remote = self.root / "fork-remote.git"
        self.git(self.root, "init", "--bare", "--initial-branch=main", str(fork_remote))
        self.git(self.submodule, "remote", "add", "fork", str(fork_remote))

        sub_sha = self.commit_submodule(publish=False)
        # 只推到 fork 的預設分支；origin 那邊完全沒有這個 commit 的分支。
        self.git(self.submodule, "push", "fork", "HEAD:main")
        self.git(self.submodule, "fetch", "fork")
        self.git(self.submodule, "remote", "set-head", "fork", "-a")
        local_sha = self.commit_parent_pin()

        result, output = self.run_guard(local_sha)

        self.assertEqual(result, 0)
        self.assertIn(f"modules/demo @ {sub_sha[:12]}", output)
        self.assertNotIn("WARN", output)
        self.assertNotIn("remote default branch", output)

    def test_remote_head_is_not_listed_as_a_branch(self):
        """`refs/remotes/<remote>/HEAD` 的 refname:short 就是 `<remote>`（沒有 `/HEAD` 後綴）。

        只濾 `/HEAD` 後綴會讓它以「一個叫 fork 的分支」的樣子混進分支清單。
        這裡直接測 helper——經過 `warn_if_...` 的路徑測不到它，因為修好之後
        「某個 remote 的 HEAD 含有這個 commit」就等於「不會警告」，這條路走不到。
        """
        fork_remote = self.root / "fork-remote.git"
        self.git(self.root, "init", "--bare", "--initial-branch=main", str(fork_remote))
        self.git(self.submodule, "remote", "add", "fork", str(fork_remote))
        sub_sha = self.commit_submodule(publish=False)
        self.git(self.submodule, "push", "fork", "HEAD:main")
        self.git(self.submodule, "fetch", "fork")
        self.git(self.submodule, "remote", "set-head", "fork", "-a")

        listed = _remote_branches_containing(self.submodule, sub_sha)

        self.assertIn("fork/main", listed)
        self.assertNotIn("fork", listed)   # 裸的 remote 名不可以出現
        for name in listed:
            self.assertIn("/", name, f"裸的 remote 名漏進分支清單：{name!r}")

    def test_missing_remote_head_skips_side_branch_warning(self):
        self.commit_submodule(publish=False)
        self.git(self.submodule, "push", "origin", "HEAD:side-branch")
        self.git(self.submodule, "fetch", "origin")
        self.git(
            self.submodule,
            "symbolic-ref",
            "--delete",
            "refs/remotes/origin/HEAD",
        )
        local_sha = self.commit_parent_pin()

        result, output = self.run_guard(local_sha)

        self.assertEqual(result, 0)
        self.assertNotIn("WARN", output)
        self.assertNotIn("remote default branch", output)

    def test_unpublished_pin_blocks_with_actionable_command(self):
        sub_sha = self.commit_submodule(publish=False)
        local_sha = self.commit_parent_pin()

        result, output = self.run_guard(local_sha)

        self.assertNotEqual(result, 0)
        self.assertIn(f"modules/demo @ {sub_sha[:12]}", output)
        self.assertIn("git -C modules/demo push origin", output)
        self.assertIn("--no-verify", output)

    def test_uninitialized_submodule_warns_but_allows_push(self):
        self.commit_submodule(publish=False)
        local_sha = self.commit_parent_pin()
        self.git(self.parent, "submodule", "deinit", "-f", "modules/demo")

        result, output = self.run_guard(local_sha)

        self.assertEqual(result, 0)
        self.assertIn("WARN", output)
        self.assertIn("not initialized", output)

    def test_locally_missing_commit_warns_but_allows_push(self):
        (self.sub_seed / "missing.txt").write_text("not fetched\n", encoding="utf-8")
        self.git(self.sub_seed, "add", "missing.txt")
        self.git(self.sub_seed, "commit", "-m", "locally absent submodule commit")
        missing_sha = self.rev_parse(self.sub_seed, "HEAD")
        self.git(
            self.parent,
            "update-index",
            "--cacheinfo",
            f"160000,{missing_sha},modules/demo",
        )
        self.git(self.parent, "commit", "-m", "pin locally absent commit")

        result, output = self.run_guard(self.rev_parse(self.parent, "HEAD"))

        self.assertEqual(result, 0)
        self.assertIn("WARN", output)
        self.assertIn("not present locally", output)

    def test_deleted_branch_is_skipped(self):
        result, output = self.run_guard("0" * 40)

        self.assertEqual(result, 0)
        self.assertIn("no gitlink changes", output)

    def test_git_push_dry_run_triggers_configured_hook(self):
        try:
            (self.parent / "tools").symlink_to(TOOLS_DIR, target_is_directory=True)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest("Windows file-symlink privilege is unavailable")
            raise
        self.git(self.parent, "config", "core.hooksPath", "tools/hooks")
        self.commit_submodule(publish=False)
        (self.parent / "note.txt").write_text("parent only\n", encoding="utf-8")
        self.git(self.parent, "add", "note.txt")
        self.git(self.parent, "commit", "-m", "parent-only change")

        allowed = self.git(
            self.parent, "push", "--dry-run", "origin", "main", check=False
        )
        allowed_output = allowed.stdout + allowed.stderr

        self.assertEqual(allowed.returncode, 0)
        self.assertIn("no gitlink changes", allowed_output)

        self.commit_parent_pin()
        blocked = self.git(
            self.parent, "push", "--dry-run", "origin", "main", check=False
        )
        blocked_output = blocked.stdout + blocked.stderr

        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("refusing parent-repo push", blocked_output)
        self.assertIn("git -C modules/demo push origin main", blocked_output)



if __name__ == "__main__":
    unittest.main()
