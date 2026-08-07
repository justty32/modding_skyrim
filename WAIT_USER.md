# WAIT_USER — 等待使用者的事

只列需要使用者親自做/驗證才能繼續的 open 項。完成即移除，不留完成清單。

常見類型：

- 實機或 UI 手動驗證
- 外部帳號、權限、下載、授權
- 本機環境變數或工具安裝
- 不能由 agent 代跑的指令
- 高風險操作的確認

## Open

- **第三方 mod 流水線只剩 P4 端到端實機驗收**（2026-08-07）：P0–P3 已完成，20 個單元測試全綠。需在家挑一個真實第三方 mod，走完「下載工作單 → `try/<mod>` 安裝 → 排序 → houseCARL before/after 靜態關卡 → `qa.json` 實機 → 視覺 handoff → `try-pass`」，並確認 profile git 留下可回滾 commit。權威步驟見 [third-party-mod-pipeline.md](workflows/plans/third-party-mod-pipeline.md) P4。

- **darksouls-port 門洞仍卡，參數已備好但未套用**（2026-08-06，**使用者決定先收現狀**）：`--ghost-tol` 0.25 → 0.02，h0006 實測憑空面積 2.0 → 0.1 m²，代價是載體 NIF 341 → 約 440 塊。要動就是改預設、全量重跑 47 個 hkx、`rm -rf out/DSPortP1` 後重新打包、`mo2ctl install --force` 重裝，再進場走一次門。**`DSPortP1` 目前仍裝在 MO2 裡**（新版碰撞、332 個載體），故意留著讓下次能直接進場。

- **houseCARL 的 `set_mo2_instance` 在 Linux 下不能用——第三個同族 Linux 路徑 bug**（2026-08-04）：指向 `~/games/mod-organizer-2-skyrimspecialedition/modorganizer2` 被拒，錯誤是找不到 `Z:\home\lorkhan\.local\share\Steam\steamapps\common\Skyrim Special Edition/Data`。它把 `ModOrganizer.ini` 的 `gamePath` 當字面路徑用，**沒有把 Wine 的 `Z:\` 前綴翻回 Linux 路徑**，然後接上 `/Data` 就成了混合式的壞路徑。跟已在本檔掛著的 `fix/linux-loose-asset-resolution` 是同一家族。

  **實際影響有限**：explicit-paths mode 全程可用（本次建檔、DLL 檢查、load order 讀取都是在這個模式下完成的）。**唯一失去的是 `load_order_status(profile=...)` 跨 profile 檢查**——無法用它比對 `Default` 與新建的 `QA`，只能直接讀 profile 檔案。

  要你定：**是否開第三條 fix branch**？考慮到 fork 上已經有兩條沒推、PR 從未開出（見下面兩條），再加一條會讓那筆債更難清。另一個選項是先不修，維持 explicit-paths mode。

- **`projects/houseCARL` 還沒納入母 repo 的 submodule**（2026-08-03）：它是 `Avick3110/houseCARL` 的 fork，本機 HEAD 在 `fix/dialogue-encoding-lint`（`87ce894`）——**那個 rebase 過的 commit 還沒推上 fork**，釘成 submodule 會讓別人 `clone --recurse-submodules` 直接失敗。目前用 `.gitignore` 排除。解法二選一，要你定：
  1. 先做上面那條 force-push（把兩條 fix branch 推上 fork），再把 submodule 釘在 fork 的分支上；
  2. 或 submodule 只釘 `main`（`8385fc6`，已在 origin），fix branch 留本機。

- **houseCARL:兩條 fix branch 已 rebase 到 upstream 最新(8385fc6),probe 全 PASS,待使用者決定**(2026-07-17):
  1. 是否 force-push 更新 fork 上的 `fix/linux-loose-asset-resolution`、`fix/dialogue-encoding-lint`(fork 上仍是舊 base 版本)。
  2. 是否向 upstream `Avick3110/houseCARL` 開兩個 PR——**當初 branch 推了 fork 但 PR 從未開出**;upstream 91 個新 commit 皆未修這些 Linux 問題,修正仍有效。

