# WAIT_USER — 等待使用者的事

只列需要使用者親自做/驗證才能繼續的 open 項。完成即移除，不留完成清單。

常見類型：

- 實機或 UI 手動驗證
- 外部帳號、權限、下載、授權
- 本機環境變數或工具安裝
- 不能由 agent 代跑的指令
- 高風險操作的確認

## Open

- **darksouls-port 門洞仍卡，參數已備好但未套用**（2026-08-06，**使用者決定先收現狀**；2026-08-11 補上前置條件與備援）：症狀是使用者實走回報「只有過門會卡，過道上走基本沒問題」——根因是平面內填洞，有門洞的牆其凸包把門洞填實。`--ghost-tol` 是**每顆 hull** 的容許量，一個門洞切成好幾顆、每顆合法填 0.24 m²，加起來就把門框內縮到卡人。

  **⚠️ 動手前的前置條件**：`tools/collision_hulls.py` 需要 `trimesh`、`scipy`、`vhacdx`，**目前哪個 venv 都沒有**（`model-converter/.venv` 只有 numpy + pygltflib，`import trimesh`／`import scipy` 皆失敗）。不補相依就跑不了全量重跑這步。

  執行步驟：

  1. 補上 `trimesh` / `scipy` / `vhacdx` 相依。
  2. `--ghost-tol` 預設 0.25 → **0.02**（h0006 實測：hull 233 → 302，總憑空面積 2.0 → 0.1 m²，**+30% hull 換 20 倍改善**）。
  3. 全量重跑 47 個 hkx。全量代價估計：載體 NIF 341 → 約 440 塊。
  4. `rm -rf out/DSPortP1` 後重新打包 → `mo2ctl install --force` 重裝 → 進場走一次門。

  **若 0.02 還是卡**：下一個懷疑對象是門框側壁（reveal）自成 patch 後的**厚度**，那要調 `--planar-thresh`，**不是繼續降 `--ghost-tol`**。

  **`DSPortP1` 目前仍裝在 MO2 裡**（新版碰撞、332 個載體），故意留著讓下次能直接進場。技術細節見 [P1-INGAME-FINDINGS.md](projects/darksouls-port/p1/P1-INGAME-FINDINGS.md)。

- **houseCARL：收進自己的 fork，需在家執行**（決策於 2026-08-11，取代原本三條待決事項）：方針是**只顧自己的 repo，不再追上游**——force-push 兩條 fix branch 到 fork、submodule 釘 fork branch、**不開 upstream PR**。要你在家做，因為 clone 只在家裡那台、且需要你的推送權限：

  1. `git push --force-with-lease` 把 `fix/linux-loose-asset-resolution`、`fix/dialogue-encoding-lint` 推上 fork（fork 上仍是 rebase 前的舊 base 版本）。用 `--force-with-lease` 不要用 `--force`。
  2. 把 `projects/houseCARL` 從 `.gitignore` 移除，以 submodule 釘在 fork 的 `fix/dialogue-encoding-lint`（本機 HEAD `87ce894`）——**必須等 1. 推完**，否則 `clone --recurse-submodules` 會失敗。
  3. 同步更新 `AGENTS.md` 裡「`projects/houseCARL` 不是 submodule、不要在母 repo 追蹤它的內容」那段本地規則。

  決策理由與上游現況見 [SESSION-LOG.md](SESSION-LOG.md) 的 houseCARL 節。
