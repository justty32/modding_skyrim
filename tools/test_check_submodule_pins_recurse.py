from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from submodule_pins_testlib import PinGuardFixture, TOOLS_DIR
from check_submodule_pins import _remote_branches_containing


class PushRecurseTests(PinGuardFixture):
    """`push.recurseSubmodules=on-demand` 讓 git 自己在同一次 push 裡發布 submodule。

    這個 hook 跑在 git 遞迴進 submodule **之前**，所以在不知道這個設定的情況下
    它會擋掉「一次 push 全部搞定」——擋掉的正是它自己要求使用者手動做的事。
    2026-08-26 在拋棄式 parent/submodule 上實測過：hook 關掉時一次 `git push`
    先推 submodule 再推母 repo；hook 開著且不認這個設定時直接 exit 1。
    """

    def test_on_demand_lets_an_unpublished_pin_through(self):
        sub_sha = self.commit_submodule(publish=False)
        local_sha = self.commit_parent_pin()
        self.git(self.parent, "config", "push.recurseSubmodules", "on-demand")

        result, output = self.run_guard(local_sha)

        self.assertEqual(result, 0)
        self.assertIn("push.recurseSubmodules=on-demand", output)
        self.assertIn(f"modules/demo @ {sub_sha[:12]}", output)
        self.assertNotIn("refusing parent-repo push", output)

    def test_only_lets_an_unpublished_pin_through(self):
        self.commit_submodule(publish=False)
        local_sha = self.commit_parent_pin()
        self.git(self.parent, "config", "push.recurseSubmodules", "only")

        result, output = self.run_guard(local_sha)

        self.assertEqual(result, 0)
        self.assertIn("push.recurseSubmodules=only", output)

    def test_check_still_blocks_because_git_will_not_publish_anything(self):
        """`check` 只是叫 git 自己也做一次檢查，它不會幫你推。"""
        self.commit_submodule(publish=False)
        local_sha = self.commit_parent_pin()
        self.git(self.parent, "config", "push.recurseSubmodules", "check")

        result, output = self.run_guard(local_sha)

        self.assertNotEqual(result, 0)
        self.assertIn("refusing parent-repo push", output)

    def test_unset_still_blocks(self):
        self.commit_submodule(publish=False)
        local_sha = self.commit_parent_pin()

        result, output = self.run_guard(local_sha)

        self.assertNotEqual(result, 0)
        self.assertIn("refusing parent-repo push", output)
        self.assertIn("push.recurseSubmodules on-demand", output)

    def test_on_demand_does_not_silence_the_side_branch_warning(self):
        """讓路的是「還沒發布」，不是「發布到哪」——側分支的警告仍然要出。"""
        sub_sha = self.commit_submodule(publish=False)
        self.git(self.submodule, "push", "origin", "HEAD:side-branch")
        self.git(self.submodule, "fetch", "origin")
        local_sha = self.commit_parent_pin()
        self.git(self.parent, "config", "push.recurseSubmodules", "on-demand")

        result, output = self.run_guard(local_sha)

        self.assertEqual(result, 0)
        self.assertIn("WARN", output)
        self.assertIn("origin/side-branch", output)



if __name__ == "__main__":
    unittest.main()
