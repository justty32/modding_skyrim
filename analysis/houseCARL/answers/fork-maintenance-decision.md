# houseCARL fork 維護決策

> 決策日期：2026-08-11。狀態：2026-08-20 已將兩條 fork fix 收束到預設分支並更新母 repo pin。

## 決策

- 只維護自己的 fork，不再追求 upstream PR。
- 將兩條已驗證 fix branch 發布到 `justty32/houseCARL`：
  `fix/linux-loose-asset-resolution` 與 `fix/dialogue-encoding-lint`。
- 發布後，母 repo 把 `projects/houseCARL` 納為 submodule，釘在 fork 的
  `fix/dialogue-encoding-lint`。
- 2026-08-20 將 `fix/linux-loose-asset-resolution` 的修正 cherry-pick 到
  `fix/dialogue-encoding-lint`，再把 fork 的 `main` 與 dialogue branch 一起 fast-forward 到同一個
  consolidated tip。獨立 Linux branch 保留為歷史入口；未刪遠端分支。
- `set_mo2_instance` 的 Wine `Z:\...` → Linux path 第三條 fix 暫不開；explicit-paths mode
  仍可滿足目前工作流。

## 目前可驗證狀態（2026-08-20，家用 Manjaro）

| 項目 | SHA／結果 |
|---|---|
| 本地 `fix/linux-loose-asset-resolution` | `84576e3` |
| fork 同名 Linux branch | `84576e3`（保留；沒有刪除） |
| 本地 `fix/dialogue-encoding-lint` | `ff802dd` |
| fork 同名 dialogue branch | `ff802dd` |
| fork 預設分支 `main` | `ff802dd` |
| consolidated tip 的共同基準 | `8385fc6` |
| upstream `origin/main` | `21f8c8a` |
| consolidated tip 相對 upstream | 落後 368 commits；有 2 個 fork-only commits（dialogue encoding + Linux asset resolution） |

2026-08-20 收束前，`fork/main` 在 `e463f55`，dialogue branch 在 `87ce894`，前者是後者的祖先且
可直接 fast-forward；但 dialogue branch 沒包含 fork 已發布的 Linux fix。為免預設分支只收其中一條，
先在隔離 worktree 將 `84576e3` cherry-pick 成 `ff802dd`，只在 `CiAll.cs` 與 `Program.cs` 的 guard
註冊點發生衝突，解法是同時保留兩個 guard。之後以 atomic、non-force push 將既有 dialogue branch
與 `fork/main` 同步 fast-forward 到 `ff802dd`；沒有開 PR、force-push 或刪除遠端分支。

驗證結果：`dotnet clean`、`dotnet build housecarl.sln` 成功（18 個既有 warning、0 error）；Linux
self-contained publish 成功；`case-insensitive-asset-guard`、`dialogue-encoding-guard`、
`skse-config-audit-guard` 均 PASS。`ci-all` 在 native Linux 為 78/97 pass；19 個 failure 主要落在
Windows-style path／filesystem fixture（另含缺 `where.exe`、setup file-lock 與兩個 SkyPatcher assertion），
因此不能把這個舊版 aggregate runner 當作 Linux 全綠 gate。這次不擴大修正；與兩條 fork patch 直接
相符的三個 self-contained guard 都已通過。

## 為什麼不追 upstream

- 官方交付與 README 以 Windows 為目標；Linux/Wine/Proton 不在宣告支援範圍。
- upstream 持續高速變動，讓兩條 Linux fix 保持 PR-ready 的成本高於本地收益。
- 2026-08-11 的 source/issue/commit 稽核未找到同類 Linux path、case sensitivity 或 dialogue
  encoding 修正；現有 fix 仍有實際用途。
- `CONTRIBUTING.md` 要求大改前先開 issue，但該 repo 的 issue creation 受限；近期可見 PR
  也主要是 owner 自己的工作流。這不代表 upstream 永遠不收外部貢獻，只代表本案期望值低。

## 完成條件與執行入口

發布、branch 收束與 submodule 納管已完成。Linux build、publish、explicit-paths 設定與驗證方式見
[linux-manjaro-mo2-runbook.md](linux-manjaro-mo2-runbook.md)。

Done when：fork 的 `main` 與 `fix/dialogue-encoding-lint` 指向同一個包含兩條 fix 的 tip；獨立 Linux
branch 仍可由 fresh clone 取得；母 repo recursive clone 能 checkout consolidated tip。
