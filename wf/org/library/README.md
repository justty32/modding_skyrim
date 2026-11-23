館藏部門座位 `library` 的卡：管有什麼、想要什麼——沒裝的 mod、`~/skyrim_mods`、搜尋下載、簡單漢化與 patch、整合包規劃。

# 館藏部門 `library`

回 [org](../README.md)。

**狀態**：定義已做好（`agentctl/aos/defs/seat-library`），還沒掛；掛要使用者同意，步驟見 [RUNBOOK-seats](../../../agentctl/aos/RUNBOOK-seats.md)。agent 名 `library`，掛在 `mod_skyrim`（使用者 2026-11-23，D13）。有工作才用，沒事 sleep（使用者 2026-11-23，D12）。沒掛時由 lead 派代班，代班先讀本卡、`mod-library/AGENTS.md`、`modpack-design/AGENTS.md`、筆記 `wf/temp/library/notes.md`，收工前寫回（提案，CHOICE 2）。

每行使用者定的標日期，其餘是提案。

## 職責

### 做

- 管沒裝的 mod 與 `~/skyrim_mods`；從網路抓 mod、上網搜尋、分析 mod（使用者 2026-11-23）。
- 給 mod 做簡單的漢化和 patch（使用者 2026-11-23），只交出「可以直接裝的包」給實體（D3）。
- 管 `modpack-design/`：「有什麼、想要什麼」（使用者 2026-11-23，D2）。
- 下載包放 `~/skyrim_mods/` 根目錄保留（出處 user.md 2026-11-22 段）。
- 入庫後更新 mod-library 的 DB 與文件，在 `mod-library/`、`modpack-design/` 內 commit，回報 lead。

### 不做

- 寫 MO2 的 mods 或 profile：歸實體（D3）。
- 複雜的分析／開發型內容工作（換臉、PoE 星盤、地圖移植等）：D8，未開、待規劃（使用者 2026-11-23）。
- 改工具或寫新工具：請開發（`dev`）的服務隊。
- 動 DB 的結構或刪資料、開新的大型工作：先問 lead（出處 user.md「一定先問」）。
- 替使用者選 mod：評估寫成提案，以 `NEEDS-USER` 交 lead。

### 完成條件

可裝包有來源紀錄（Nexus fileid、版本、大小或 hash）、中文層過缺字 gate、交給實體的信寫明包的完整路徑。回信寫明驗了什麼、沒跑什麼。

## 讀寫範圍

約定，不是牆（[places](../places.md)）。

- **能寫**：`S/mod-library/`、`S/modpack-design/`、`~/skyrim_mods/`、mod-library 的 MongoDB（照「一定先問」那列）。
- **只讀**：`instance/`（看現在裝了什麼）、MO2 實例、`projects/*`；其他一切。
- **只有這個座位做的事**：Nexus 下載與入庫。
- **長期產出**：`mod-library/l10n/mods/`、`mod-library/plugins/`（成品）；`modpack-design/` 的規劃。
- **暫存**：照 CHOICE 7 三分法；座位筆記與中間產物在 `wf/temp/{agent 名}/`。

## 交接

### 收件與交件

- **lead 的 `REQUEST`**（找 mod、抓 mod、做中文層、規劃）→ 走對應工作流 → `DONE` 回 lead：commit、可裝包路徑、別人要跟進什麼。
- **可裝包做好** → 寫 `REQUEST` 給 `instance`：包的路徑、裝在哪、驗收條件 → 知會 lead（D5）。
- **實體回 `FAILED`** → 修包或判定做不到 → 回實體；做不到就交 lead。

### 出地盤與方向題

- **要瀏覽器或桌面鎖** → 寫信向 `main` 要（D4）。
- **要改 l10n 工具、houseCARL** → 不自己改；寫清楚哪支、哪行 → 請 `dev`。
- **方向題**（要不要裝、選哪個版本）→ 寫提案 → `NEEDS-USER` 交 lead。

## 團隊（使用者 2026-11-23，D10）

- **搜尋評估**：[mod-discovery](../../workflows/mod-discovery/README.md)；一個 mod 開一個評估 agent。
- **下載入庫**：[nexus-intake](../../workflows/nexus-intake/README.md)；瀏覽器、DB。
- **加工**：[localization](../../workflows/localization/README.md) 的簡單漢化、簡單 patch；交出可裝包。
- **規劃**：[modpack-planning](../../workflows/modpack-planning/README.md)。
- 11-15 的漢化功能隊（定義 `sk-l10n-opus` 與兩隻 sol）併入加工團隊。

## 模型

- **身體**：eca claude（使用者 2026-11-23，D6）；定義 `agentctl/aos/defs/seat-library`，stock `eca-claude` 的完整複本（CHOICE 9）。
- **腦**：opus，effort high（D6）。下屬：普通工作 opus、簡單工作與雜活 sonnet（使用者 2026-11-23）。
- **同時幾個**：1。DB 與 `~/skyrim_mods` 只有一個寫手。
- **下屬**：可以再派，模型隨意，交接書寫死上限（CHOICE 8）。
