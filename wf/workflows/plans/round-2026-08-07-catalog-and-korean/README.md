# plan：本輪三 agent 分工——mod 庫收尾 + 韓文站採集

出計畫日期 2026-08-07。上游計畫：[mod-library-catalog.md](../mod-library-catalog/README.md)（本輪做它的 P1.4、P1.5 與附錄 A、附錄 B）。
前一輪的三 agent 並行記錄見 `SESSION-LOG.md` 與 commit `dcd385b`。

**本輪不碰**：`projects/darksouls-port`、`projects/houseCARL`（使用者 2026-08-07 決定先放著）。

## 角色與鐵律

| agent | 角色 | 做什麼 | 不做什麼 |
|---|---|---|---|
| **codex** | 領導 | 出 schema／判準／治具骨架、review deepseek 與 agy 的產出、**唯一有 commit 權** | 不跑大量迴圈（那是 deepseek 的活） |
| **deepseek** | 執行 | 跑 codex 寫好的腳本、大量 API／解析迴圈、填 Mongo 欄位 | **不寫治具、不 commit、不 `git add`** |
| **agy** | 網路搜尋與採集 | 韓文站公開板搜尋、抓截圖／簡介／原始連結、翻譯簡介 | **不做事實判斷、不寫 Mongo、不 commit** |

**index.lock 鐵律**：只有 codex 碰 git。deepseek 寫 MongoDB 與 `~/notes/projects/modding/skyrim/logs/`，agy 寫 `~/skyrim_mods/.candidates/`（非版控）。三者落點互斥。

**幻覺隔離**（agy 專用）：原始連結、截圖檔、頁面 HTML **必須是機器抓下來的原物**，agy 只被允許在「已抓到的原文」上做翻譯與摘要。任何 agy 自己「記得」的 mod 名稱、作者、連結一律不採信——收斂時 codex 以「原始檔案是否存在」為準，不以 agy 的敘述為準。

**驅動方式**：tmux `send-keys` + `capture-pane`（不是 stdin 注入；`dev.tty.legacy_tiocsti=0` 讓後者做不到）。每個 agent 一個獨立 tmux session。

---

## 使用者已定案（2026-08-07）

1. **Nexus 走 personal API key**：使用者自行生 key，A1 治具寫成吃 `api.nexusmods.com`（回 JSON、有明確 status 欄位、有 rate-limit header 可讀），不猜 HTML。key 從環境變數 `NEXUS_API_KEY` 讀，**不得寫進任何版控檔案**。
   - **A1 寫治具不需要 key，可立刻開工；A2 實跑要等 key 到手。**
2. **那 107 筆 `quarantined_at` 不一致的資料：從 `archives` 移除**。副作用要在 A3 前先做掉：移除前先 pymongo dump，並在 `docs/` 留一份被移除的 sha256 + 原檔名清單（不進 `archives`，但保留稽核痕跡）。做完把 `WAIT_USER.md` 那條刪掉。

## 派工順序

| 階段 | codex | deepseek | agy |
|---|---|---|---|
| T0（現在，不等 key） | **A1** 寫 Nexus 狀態富化工具（吃 Nexus API） | **A4a** 從 Mongo 拉 `is_translation=true` 清單，做檔名正規化配對，產 TSV 草稿（**不寫回 Mongo**） | **B2-recon** 列出可爬的公開站／板塊清單、各站結構與可行性，**先不正式採集** |
| T1（key 到手 + A1 驗收過） | **B1** `candidates` schema + ingest／link-check／gallery 三支治具 | **A2** 長跑補值 | 待 B1 定下 `meta.json` 欄位 |
| T2 | **A3** 清理報告 + 107 筆移除 + P1.7 備份；**B3** 收斂 | **A4b** 用 codex 的 matcher 正式填 `translates_mod_id`、出版本差異矩陣 | **B2** 正式採集 |

## 風險

- **Nexus 控速**：1,000+ 次請求，打太快會被擋。這是 A1 治具的首要設計約束，不是 A2 的臨場判斷。
- **agy 幻覺**：已由「原物優先」規則隔離（見上）。收斂時以檔案存在與否為準。
- **mongod 是手動啟動的**：腳本在 mongod 沒開時要給明確錯誤與啟動指令，不要 timeout。
- **deepseek 越權改腳本**：派工時要明講「回報不修」，並在 capture-pane 檢查時留意它有沒有動 `tools/`。

## 本計畫的其他部分

| 檔案 | 內容 |
|---|---|
| [`line-a.md`](line-a.md) | 線 A：mod 庫收尾 |
| [`line-b.md`](line-b.md) | 線 B：韓文站採集 |
