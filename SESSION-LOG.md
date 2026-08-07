# SESSION-LOG — 進度日誌 hub

只放還沒完成的活狀態。已完成的實作與調查歷史由對應 plan、子專案文檔與 git history 承接；需使用者親自做或決定的事在 [WAIT_USER.md](WAIT_USER.md)。

## 現役工作

### 第三方 mod 流水線

- P0–P3 已完成；`projects/agent-bridge` 的 P1/P2/P3 commits 為 `30a97be` / `35d5692` / `6106646`。2026-08-07 重跑 py_compile 與 20 個單元測試全綠。
- 已有 archive/FOMOD 安裝與重放、manifest、profile git `try/<mod>` pass/fail 回滾治具，以及 houseCARL before/after 靜態關卡。
- 唯一剩餘的是 P4：挑一個真實第三方 mod 走完全流程。需家中 MO2/Skyrim 與使用者視覺 handoff。
- 權威計畫：[third-party-mod-pipeline.md](workflows/plans/third-party-mod-pipeline.md)。

### mod 庫建檔

- 1,659 筆 / 85.7 GiB 已建檔；DLL runtime 檢查、L1/L2 清理與 L3 隔離已執行。
- 下一步：P1.4 Nexus 在架狀態補值，再完成可重跑的清理報告。
- 107 筆 `quarantined_at` 與檔案不一致的資料在重掃前必須先決定終態；見 [WAIT_USER.md](WAIT_USER.md)。
- 權威計畫：[mod-library-catalog.md](workflows/plans/mod-library-catalog.md)。

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
