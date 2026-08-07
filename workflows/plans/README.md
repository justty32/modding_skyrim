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
- 落地或被取代後移到 `archive/`。

## 現役計畫

| 計畫 | 出計畫日期 | 對應 spec | 狀態 |
|------|------------|-----------|------|
| [third-party-mod-pipeline](third-party-mod-pipeline.md) —— 第三方 mod 取得–安裝–驗證流水線 | 2026-08-04 | [ai-ingame-qa-loop](ai-ingame-qa-loop.md) | P0–P3 已完成；只剩 P4 真實 mod 端到端實機驗收 |
| [mod-library-catalog](mod-library-catalog.md) —— mod 壓縮檔建檔與清理 | 2026-08-04 | 無 | 建檔與 L1–L3 已執行；待 Nexus 補值與 107 筆終態決策 |

## 已結案／被取代

| 計畫 | 結果 |
|------|------|
| [ai-ingame-qa-loop](ai-ingame-qa-loop.md) | 2026-08-02 結案；Phase 0–3 與實機 QA runner 全過 |
| [workspace-reorg](workspace-reorg.md) | 被 2026-08-02/03 的多 repo + submodule 佈局取代，不再執行 |

## 何時不用

- 小改動已能直接安全實作，走 feature-dev。
- 設計還沒定，走 specs。
- 只是排優先順序，走 roadmap。
