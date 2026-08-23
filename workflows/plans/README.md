# plans — 實作規劃入口

真的要動工前的詳細實作規劃：精確到檔案、步驟、測試、驗證。

規劃階梯：

```text
idea → roadmap → spec → plan → feature-dev
```

## 規則

- 開始前寫 `Done when: <每個 task、檔案、測試與驗證都足以直接動工>`。
- 本夾 `*.md` = 各功能的逐步實作計畫。
- 建議命名：`<feature>.md`。
- 對應設計方案：`specs/<feature>-design.md`。
- 計畫要切成 bite-sized task，每步都有驗證。
- 落地或被取代後，在下面的「已結案／被取代」表登記結果。**不另設 `archive/`**——計畫留原地並在表裡標明狀態；只有連歷史參考價值都沒有的才刪除，並在表裡註明可從 git 歷史取回。

## 現役計畫

| 計畫 | 出計畫日期 | 對應 spec | 狀態 |
|------|------------|-----------|------|
| [third-party-mod-pipeline](third-party-mod-pipeline.md) —— 第三方 mod 取得–安裝–驗證流水線 | 2026-08-04 | [ai-ingame-qa-loop](ai-ingame-qa-loop.md) | P0–P4 已完成；Bend Time Rings 端到端實機驗收通過 |
| [mod-library-catalog](mod-library-catalog.md) —— mod 壓縮檔建檔與清理 | 2026-08-04 | 無 | 建檔與 L1–L3 已執行；Nexus 補值與 107 筆終態決策已完成；**僅留 L4 的 109 筆舊命名壓縮檔人工辨識**（清單在 [`mod-library/audits/l4-review-worklist.md`](../../mod-library/audits/l4-review-worklist.md)）。工具已隨統整移到 `mod-library/db/` |

## 已結案／被取代

| 計畫 | 結果 |
|------|------|
| [consolidation-2026-08-23](consolidation-2026-08-23.md) —— 工作區統整與四條新線 | 2026-08-23 執行完成；四條線落地、profile 改名、Downloads 歸檔。執行結果與使用者裁決記在同一份文件末尾 |
| [round-2026-08-07-catalog-and-korean](round-2026-08-07-catalog-and-korean.md) —— 三 agent 分工：mod 庫收尾＋韓文站採集 | 2026-08-07 執行完成，是 [mod-library-catalog](mod-library-catalog.md) 的 P1.4／P1.5 與附錄 A／B。韓文 inbox 後已併入通用 inbox |
| [ai-ingame-qa-loop](ai-ingame-qa-loop.md) | 2026-08-02 結案；Phase 0–3 與實機 QA runner 全過 |
| ~~workspace-reorg~~ | 2026-08-01 的佈局設計。先被 2026-08-02/03 的多 repo + submodule 佈局取代，再被 [consolidation-2026-08-23](consolidation-2026-08-23.md) 取代；2026-08-23 刪除，可從 git 歷史取回 |

## 何時不用

- 小改動已能直接安全實作，走 feature-dev。
- 設計還沒定，走 specs。
- 只是排優先順序，走 roadmap。
