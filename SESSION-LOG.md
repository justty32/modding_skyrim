# SESSION-LOG — 進度日誌 hub

只放還沒完成的活狀態。已完成的實作與調查歷史由對應 plan、子專案文檔與 git history 承接；需使用者親自做或決定的事在 [WAIT_USER.md](WAIT_USER.md)。

## 現役工作

### 第三方 mod 流水線

- P0–P4 已完成；`projects/agent-bridge` 的 P1/P2/P3 commits 為 `30a97be` / `35d5692` / `6106646`，P4 補強 commit 為 `c641d77`。
- P4 實測 mod：`Bend Time Rings`（Nexus 10974，本機 archive sha256 `53f6d341cc72c143bd45d4518a487934345ab0b7da725b5d8cb880b1bcdc5513`），profile git commit `cfb34db Validate Bend Time Rings P4`。
- 驗收結果：zip install → manifest → QA profile `try/bend-time-rings` → houseCARL static gates → `qa.json` 到達 Bannered Mare + 穿上 `Ring of Slow Time` → 使用者視覺 handoff 通過。
- 權威計畫：[third-party-mod-pipeline.md](workflows/plans/third-party-mod-pipeline.md)。

### mod 庫建檔

- 1,585 筆 archive / 1,433 個 mod group 已建檔；DLL runtime 檢查、L1/L2 清理與 L3 隔離已執行。
- P1.4 Nexus 在架狀態補值治具已完成並過 SkyUI 驗收；A2 正在跑全量補值。完成後再產可重跑清理報告。
- 107 筆 `quarantined_at` 不一致紀錄已從 `archives` 移除；稽核清單在 `~/notes/projects/modding/skyrim/docs/removed-missing-quarantine-2026-08-07.md`。
- 權威計畫：[mod-library-catalog.md](workflows/plans/mod-library-catalog.md)。

### 韓文站採集

- 本輪已開線 B：先做公開站偵查與候選資料 schema，再由 agy 只抓頁面 HTML、截圖與原始連結，不下載 mod 本體。
- 權威計畫：[round-2026-08-07-catalog-and-korean.md](workflows/plans/round-2026-08-07-catalog-and-korean.md)。

### darksouls-port

- P2 新版碰撞已將懸空碰撞面積降 98.9%；走廊基本正常，門洞仍會卡。
- `--ghost-tol 0.02` 可將 h0006 懸空面積由 2.0 降到 0.1 m²，代價是載體約 341 → 440；使用者已決定先收現狀，套用與實機複驗留在 [WAIT_USER.md](WAIT_USER.md)。
- 技術細節：`projects/darksouls-port/p1/P1-INGAME-FINDINGS.md`。

### houseCARL

- Linux `set_mo2_instance` 仍不會將 Wine `Z:\\...` 轉回 Linux path；explicit-paths mode 可繼續使用。
- 兩條 rebase 後的 fix branch 尚未 force-push/開 PR，`projects/houseCARL` 也因此尚未納入 submodule。三項都等使用者決定，見 [WAIT_USER.md](WAIT_USER.md)。

## 已關閉的方向

- `scene-capture-bridge` 的 Windows/MSVC CI 於 2026-08-07 放棄：唯一受支援的建置與出貨路徑是 Linux clang-cl + xwin。失敗的 GitHub Actions workflow 已移除，不再追 fmt/MSVC STL 相容性。
- AI 全自動 mod QA 迴圈已結案，無 open 項；見 [ai-ingame-qa-loop.md](workflows/plans/ai-ingame-qa-loop.md) 第六節。
- 舊 `workspace-reorg` 方案已被現行多 repo + submodule 佈局取代，不再執行。

## 各工作流 session-log

| 工作流 | session-log | open 摘要 |
|--------|-------------|----------|
| feature-dev | [workflows/feature-dev/session-log.md](workflows/feature-dev/session-log.md) | 無 |
| refactor | [workflows/refactor/session-log.md](workflows/refactor/session-log.md) | 無 |
| investigation | [workflows/investigation/session-log.md](workflows/investigation/session-log.md) | 無 |
