# wf/user/ — 給使用者本人看的頁面

這裡放**濃縮結果**：開玩前清單、審批頁、裁示單——使用者要親自讀、親自裁示的東西。
Agent 之間交接的內部報告（各線 `REPORT.md`、`STATE.md` 等）仍留在 [`agentctl/handoffs/`](../../agentctl/handoffs/)；本目錄的檔案只做摘要，連結要連回原始報告。

檔名格式：`YYYY-MM-DD-<主題>.md`（2026-10-03 的 `dsport-test-2026-10-03.md` 是例外，沿用舊名）。

**門檻**：單頁 ≤ 8 KB，超過就按主題／地點拆子資料夾、原路徑留入口頁；長清單用小節（`###`）切開，不用一張大表。

## 目前檔案

<!-- wf-nav -->
| 檔案 | 內容 |
|------|------|
| [2026-09-26-pre-play-checklist.md](2026-09-26-pre-play-checklist.md) | 09-26 早場八線調查濃縮：開玩前要做的事、裁示項；C／D／E 三節拆在 [子資料夾](2026-09-26-pre-play-checklist/)：[C-console](2026-09-26-pre-play-checklist/C-console.md)、[D-ingame](2026-09-26-pre-play-checklist/D-ingame.md)、[E-open](2026-09-26-pre-play-checklist/E-open.md) |
| [dsport-test-2026-10-03.md](dsport-test-2026-10-03.md) | 10-03 DSPort 肉眼測試清單（切 dsport-dev profile 後照做） |
| [2026-10-10-play-checklist.md](2026-10-10-play-checklist.md) | 10-10 十七線施工彙整總頁：開遊戲前、依地點分四頁的實測清單、今日安裝總表、不裝／延後 |
| ↳ 四個分頁 | [城鎮與室內](2026-10-10-play-checklist-towns.md)、[戰鬥與系統](2026-10-10-play-checklist-combat.md)、[隨從與人物](2026-10-10-play-checklist-followers.md)、[野外與地點](2026-10-10-play-checklist-wild.md)（入口頁，再拆三頁在 [子資料夾](2026-10-10-play-checklist-wild/)） |
| ↳ [installed.json](2026-10-10-play-checklist-installed.json) | 資料檔（`wf-table/1`）：10-10 當天安裝總表，每列一個 mod 與出處 REPORT；總頁「今天裝了什麼」從這裡讀 |
| ↳ [mo2-reverify.json](2026-10-10-play-checklist-mo2-reverify.json) | 資料檔（`wf-table/1`）：MO2 首開後要重驗的 plugins.txt 行（行號、該不該有 `*`、順序要求）；總頁 1a 的依據 |
| [2026-10-17-structure-review.md](2026-10-17-structure-review.md) | 10-17 Fable 全工作區結構審查：55 條建議、21 個施工包與裁示欄 |
| [2026-10-17-patrol.md](2026-10-17-patrol.md) | 10-17 六條 Opus 子專案巡檢：已順手修的、待裁示 11 項（含 push 授權） |
