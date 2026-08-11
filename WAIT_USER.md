# WAIT_USER — 等待使用者的事

只列需要使用者親自做/驗證才能繼續的 open 項。完成即移除，不留完成清單。

常見類型：

- 實機或 UI 手動驗證
- 外部帳號、權限、下載、授權
- 本機環境變數或工具安裝
- 不能由 agent 代跑的指令
- 高風險操作的確認

## Open

- **darksouls-port 門洞仍卡，參數已備好但未套用**（2026-08-06，**使用者決定先收現狀**）：`--ghost-tol` 0.25 → 0.02，h0006 實測憑空面積 2.0 → 0.1 m²，代價是載體 NIF 341 → 約 440 塊。要動就是改預設、全量重跑 47 個 hkx、`rm -rf out/DSPortP1` 後重新打包、`mo2ctl install --force` 重裝，再進場走一次門。**`DSPortP1` 目前仍裝在 MO2 裡**（新版碰撞、332 個載體），故意留著讓下次能直接進場。

- **houseCARL：收進自己的 fork，需在家執行**（決策於 2026-08-11，取代原本三條待決事項）：方針是**只顧自己的 repo，不再追上游**——force-push 兩條 fix branch 到 fork、submodule 釘 fork branch、**不開 upstream PR**。要你在家做，因為 clone 只在家裡那台、且需要你的推送權限：

  1. `git push --force-with-lease` 把 `fix/linux-loose-asset-resolution`、`fix/dialogue-encoding-lint` 推上 fork（fork 上仍是 rebase 前的舊 base 版本）。用 `--force-with-lease` 不要用 `--force`。
  2. 把 `projects/houseCARL` 從 `.gitignore` 移除，以 submodule 釘在 fork 的 `fix/dialogue-encoding-lint`（本機 HEAD `87ce894`）——**必須等 1. 推完**，否則 `clone --recurse-submodules` 會失敗。
  3. 同步更新 `AGENTS.md` 裡「`projects/houseCARL` 不是 submodule、不要在母 repo 追蹤它的內容」那段本地規則。

  決策理由與上游現況見 [SESSION-LOG.md](SESSION-LOG.md) 的 houseCARL 節。
