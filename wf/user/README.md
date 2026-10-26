# wf/user/ — 給使用者本人看的頁面

這裡放**濃縮結果**：開玩前清單、審批頁、裁示單——使用者要親自讀、親自裁示的東西。
Agent 之間交接的內部報告（各線 `REPORT.md`、`STATE.md` 等）仍留在 [`agentctl/handoffs/`](../../agentctl/handoffs/)；本目錄的檔案只做摘要，連結要連回原始報告。

檔名格式：`YYYY-MM-DD-<主題>.md`。已用完或過時的頁照 [STRUCTURE archive 規則](../STRUCTURE.md#archive-規則)封存到 [archive/](archive/README.md)；還被 WAIT_USER open 項或 open 驗收清單引用的頁不封存。

**門檻**：單頁 ≤ 8 KB，超過就按主題／地點拆子資料夾、原路徑留入口頁；長清單用小節（`###`）切開，不用一張大表。

## 目前檔案

<!-- wf-nav -->
| 檔案 | 內容 |
|------|------|
| [2026-10-26-follower-stats-gear.md](2026-10-26-follower-stats-gear.md) | 語音隨從能力值／裝備審批頁（59 人逐人勾選、產 VFSTATS 變更單）與重產方法 |
| [2026-10-26-follower-look-pages.md](2026-10-26-follower-look-pages.md) | 隨從換頭三頁（換臉挑選／隨從名冊／素材目錄）的網址、10-26 刷新內容與重產方法 |
| [2026-10-26-mod-library-viewer.md](2026-10-26-mod-library-viewer.md) | 天際儲藏庫（mod 資產庫頁）10-26 刷新：線上頁連結、這次更新了什麼、舊命名檔來源辨識怎麼看 |
| [2026-10-21-offline-fixes.md](2026-10-21-offline-fixes.md) | DSP 候選包、houseCARL 名稱解析與 consumer 相容修補的離線成果及未部署界線 |
| [2026-10-10-play-checklist.md](2026-10-10-play-checklist.md) | 10-10 十七線施工彙整總頁：開遊戲前、依地點分四頁的實測清單、今日安裝總表、不裝／延後 |
| ↳ 四個分頁 | [城鎮與室內](2026-10-10-play-checklist-towns.md)、[戰鬥與系統](2026-10-10-play-checklist-combat.md)、[隨從與人物](2026-10-10-play-checklist-followers.md)、[野外與地點](2026-10-10-play-checklist-wild.md)（入口頁，再拆三頁在 [子資料夾](2026-10-10-play-checklist-wild/)） |
| ↳ [installed.json](2026-10-10-play-checklist-installed.json) | 資料檔（`wf-table/1`）：10-10 當天安裝總表，每列一個 mod 與出處 REPORT；總頁「今天裝了什麼」從這裡讀 |
| ↳ [mo2-reverify.json](2026-10-10-play-checklist-mo2-reverify.json) | 資料檔（`wf-table/1`）：MO2 首開後要重驗的 plugins.txt 行（行號、該不該有 `*`、順序要求）；總頁 1a 的依據 |
| [2026-10-26-moveset-pages.md](2026-10-26-moveset-pages.md) | 招式五頁（姿態配置、裝備分配、總覽、MCO 挑選表、候選）10-26 現況版入口 |
