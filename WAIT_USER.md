# WAIT_USER — 等待使用者的事

只列需要使用者親自做/驗證才能繼續的 open 項。完成即移除，不留完成清單。

常見類型：

- 實機或 UI 手動驗證
- 外部帳號、權限、下載、授權
- 本機環境變數或工具安裝
- 不能由 agent 代跑的指令
- 高風險操作的確認

## Open

- **`projects/houseCARL` 還沒納入母 repo 的 submodule**（2026-08-03）：它是 `Avick3110/houseCARL` 的 fork，本機 HEAD 在 `fix/dialogue-encoding-lint`（`87ce894`）——**那個 rebase 過的 commit 還沒推上 fork**，釘成 submodule 會讓別人 `clone --recurse-submodules` 直接失敗。目前用 `.gitignore` 排除。解法二選一，要你定：
  1. 先做上面那條 force-push（把兩條 fix branch 推上 fork），再把 submodule 釘在 fork 的分支上；
  2. 或 submodule 只釘 `main`（`8385fc6`，已在 origin），fix branch 留本機。

- **houseCARL:兩條 fix branch 已 rebase 到 upstream 最新(8385fc6),probe 全 PASS,待使用者決定**(2026-07-17):
  1. 是否 force-push 更新 fork 上的 `fix/linux-loose-asset-resolution`、`fix/dialogue-encoding-lint`(fork 上仍是舊 base 版本)。
  2. 是否向 upstream `Avick3110/houseCARL` 開兩個 PR——**當初 branch 推了 fork 但 PR 從未開出**;upstream 91 個新 commit 皆未修這些 Linux 問題,修正仍有效。

