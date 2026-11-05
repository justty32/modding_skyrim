# plans — 實作規劃入口

真的要動工前的詳細實作規劃：精確到檔案、步驟、測試、驗證。

規劃階梯（前三段在 [planning](../planning.md)）：

```text
idea → roadmap → 詳規（本夾）→ feature-dev
```

## 規則

<!-- wf-nav -->
- 開始前寫 `Done when: <每個 task、檔案、測試與驗證都足以直接動工>`。
- 本夾一個計畫一個項目：小計畫是 `<feature>.md`，**超過 8KB 就拆成 `<feature>/` 目錄**
  （`README.md` 當入口＋索引，其餘按自然邊界切成 ≤8KB 的部分）。
  目錄型的切線是「環境事實與設計決策／分階段任務／重審／附錄／執行紀錄」。
- 設計取捨直接寫進計畫本身；本 repo 不另設 `specs/` 夾。
- 計畫要切成 bite-sized task，每步都有驗證。
- 落地或被取代後直接 `git rm` 計畫檔（[STRUCTURE](../../STRUCTURE.md) local 段「過時即刪」），活文件裡指向它的連結拿掉；刪除時在下面「已結案／被取代」表留一列：計畫名、結案日、最後 commit hash（可 `git show <hash>:<路徑>` 取回）。表只留最近 10 列。還在維護鏈上的留原地。

## 現役計畫

| 計畫 | 出計畫日期 | 對應 spec | 狀態 |
|------|------------|-----------|------|
| [poe-skyrim-mapping](poe-skyrim-mapping/README.md) —— PoE 星盤效果落地 Skyrim | 2026-11-03 | 設計寫在計畫內 | 核心第一波source已有離線交付；八職24設計樣板已補齊待過目，source／部署／實機各自記證 |

## 已結案／被取代

計畫檔已刪；`git show <hash>:wf/workflows/plans/archive/<計畫名>/README.md`（或 `.md`）取回。只留最近 10 列。

| 計畫 | 結果 | 最後所在 commit |
|---|---|---|
| [2026-11-05-slim](2026-11-05-slim/README.md) —— 全 repo 瘦身 | 2026-11-05 執行完；C3／C4 驗證未過未刪、測試待議 52 列與 push 待使用者，計畫檔暫留到這些裁定後刪 | 本列所在 commit |
| mod-library-catalog —— mod 壓縮檔建檔與清理 | L1–L4 完成，2026-10-26 結案；結論在 Mongo `archives.l4_identity` | `944fc45` |
| third-party-mod-pipeline —— 第三方 mod 取得–安裝–驗證流水線 | 2026-08-07 結案；P0–P4 完成，Bend Time Rings 端到端實機驗過 | `944fc45` |
| consolidation-2026-08-23 —— 工作區統整與四條新線 | 2026-08-23 執行完成；四條線落地、profile 改名、Downloads 歸檔 | `944fc45` |
| round-2026-08-07-catalog-and-korean —— mod 庫收尾＋韓文站採集 | 2026-08-07 執行完成；韓文 inbox 已併入通用 inbox | `944fc45` |
| ai-ingame-qa-loop | 2026-08-02 結案；Phase 0–3 與實機 QA runner 通過 | `944fc45` |
| workspace-reorg | 被 consolidation-2026-08-23 取代並刪除 | — |

## 何時不用

- 小改動已能直接安全實作，走 feature-dev。
- 設計還沒定、或只是排優先順序，走 [planning](../planning.md)。
