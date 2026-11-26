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
- 落地或被取代後直接 `git rm` 計畫檔（[STRUCTURE](../../STRUCTURE.md) local 段「過時即刪」），活文件裡指向它的連結拿掉；刪除時在 [closed.json](closed.json)（已結案／被取代表）加一列：計畫名、結案日、最後 commit hash（可 `git show <hash>:<路徑>` 取回）。表只留最近 10 列。還在維護鏈上的留原地。

## 現役計畫

<!-- wf-nav -->
| 計畫 | 出計畫日期 | 對應 spec | 狀態 |
|------|------------|-----------|------|
| [poe-skyrim-mapping](poe-skyrim-mapping/README.md) —— PoE 星盤效果落地 Skyrim | 2026-11-03 | 設計寫在計畫內 | 核心第一波source已有離線交付；八職24設計樣板已補齊待過目，source／部署／實機各自記證 |
| [racemenu-face](racemenu-face/README.md) —— AI 捏臉第二階段起的派線清單（R1–R7） | 2026-11-22 | 設計寫在計畫內；工作流 [racemenu](../racemenu/README.md) | R5 正向、R4 觸發元件、R6 驗證已做（離線）；實機試點待授權；R1–R3、R7 未動工 |
| [miku-outfit](miku-outfit/README.md) —— 初音整套：換色、武器，及網格、特效、物理的後續 | 2026-11-26 | 設計寫在計畫內；工作流 [design-session](../racemenu/design-session.md) | 階段 0 工具由 outfit-tools 線施工中（公司）；其餘未動工，待使用者答 17 題決定清單 |
| [tools-lib-refactor](tools-lib-refactor/README.md) —— agentctl/tools 的 NIF、DDS、ESP 寫入等重複收成 tools/lib/ | 2026-11-26 | 設計寫在計畫內；工作流 [refactor](../refactor/README.md) | 使用者 11-26 答「都按照推薦。」：精簡版（S0、A2、A3、B1、B3、B4、B5、D1）11-26 做完，靜態通過，待回家驗；其餘步驟本輪不做 |

## 已結案／被取代

計畫檔已刪；`git show <hash>:wf/workflows/plans/archive/<計畫名>/README.md`（或 `.md`）取回。只留最近 10 列。

已抽到 [closed.json](closed.json)（7 列，新的在前）。欄位：

- `plan`：計畫（名稱 —— 一句話）
- `result`：結果
- `last_commit`：最後所在 commit

## 何時不用

- 小改動已能直接安全實作，走 feature-dev。
- 設計還沒定、或只是排優先順序，走 [planning](../planning.md)。
