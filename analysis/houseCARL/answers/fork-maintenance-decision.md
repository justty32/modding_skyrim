# houseCARL fork 維護決策

> 決策日期：2026-08-11。狀態：已定案，等待發布到 fork 與納入母 repo。

## 決策

- 只維護自己的 fork，不再追求 upstream PR。
- 將兩條已驗證 fix branch 發布到 `justty32/houseCARL`：
  `fix/linux-loose-asset-resolution` 與 `fix/dialogue-encoding-lint`。
- 發布後，母 repo 把 `projects/houseCARL` 納為 submodule，釘在 fork 的
  `fix/dialogue-encoding-lint`。
- `set_mo2_instance` 的 Wine `Z:\...` → Linux path 第三條 fix 暫不開；explicit-paths mode
  仍可滿足目前工作流。

## 目前可驗證狀態（2026-08-12，家用 Manjaro）

| 項目 | SHA／結果 |
|---|---|
| 本地 `fix/linux-loose-asset-resolution` | `84576e3` |
| fork 同名 branch | `40c9e3f`（rebase 前） |
| 本地 `fix/dialogue-encoding-lint` | `87ce894` |
| fork 同名 branch | `0bbd208`（rebase 前） |
| 本地 rebase 基準 `main` | `8385fc6` |
| upstream `origin/main` | `655221d` |
| upstream 相對基準漂移 | 159 commits、134 files；`+22597/-1843` |

兩個本地 branch 已在 2026-08-12 於各自 detached worktree 重新 self-contained publish；
`case-insensitive-asset-guard` 與 `dialogue-encoding-guard` 均 PASS，publish 0 error（只有既有
nullable/obsolete warnings）。臨時 worktree 與 publish 產物已清除，原工作區未切 branch。
fork 尚未收到 rebase 後 SHA，因此一般 push 會是 non-fast-forward；實際發布必須使用
`--force-with-lease`，並先核對上表的 fork 舊 tip 沒被別的工作覆寫。

## 為什麼不追 upstream

- 官方交付與 README 以 Windows 為目標；Linux/Wine/Proton 不在宣告支援範圍。
- upstream 持續高速變動，讓兩條 Linux fix 保持 PR-ready 的成本高於本地收益。
- 2026-08-11 的 source/issue/commit 稽核未找到同類 Linux path、case sensitivity 或 dialogue
  encoding 修正；現有 fix 仍有實際用途。
- `CONTRIBUTING.md` 要求大改前先開 issue，但該 repo 的 issue creation 受限；近期可見 PR
  也主要是 owner 自己的工作流。這不代表 upstream 永遠不收外部貢獻，只代表本案期望值低。

## 完成條件與執行入口

發布、submodule 納管與母 repo 規則更新的精確順序放在根
[`WAIT_USER.md`](../../../WAIT_USER.md)。Linux build、publish、explicit-paths 設定與驗證方式
見 [linux-manjaro-mo2-runbook.md](linux-manjaro-mo2-runbook.md)。

Done when：兩條 fork branch 可由 fresh clone 取得；母 repo recursive clone 能 checkout
`projects/houseCARL`；`.gitignore`、`AGENTS.md` 與 README 的 submodule 清單同步。
