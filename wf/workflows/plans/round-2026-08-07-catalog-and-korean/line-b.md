# 線 B：韓文站採集

> 屬於 [本輪三 agent 分工——mod 庫收尾 + 韓文站採集](README.md)。

## 線 B：韓文站採集（codex 出治具 → agy 採集 → codex 收斂）

承 [mod-library-catalog.md 附錄 A](../mod-library-catalog/README.md)。

### Done when

- [x] `candidates` collection 存在，schema 有否決狀態欄位（被否決過的不再出現在審閱清單）（2026-08-07 B1：schema + ingest/check/gallery 工具落地）
- [x] 至少一輪採集落地：截圖 + 翻譯後簡介 + 原始連結 + 連結存活狀態（2026-08-07 B2/B3：`korean-public-2026-08-07-b2` 匯入 6 筆，連結 6/6 live）
- [x] 本機 HTML 圖庫可開，使用者能在上面逐筆過目（2026-08-07 B1：圖庫產生器已用暫存 DB fixture 驗證；2026-08-07 B3：`~/notes/projects/modding/skyrim/docs/candidates-gallery.html` 實批次 6 筆）
- [x] porting 候選回饋到 `analysis/port-source-survey/`（2026-08-11：核對後確認三筆都是裝備／道具，非地圖；已記錄其只能證明「成品移植旁路」，不證明場景佈局或碰撞可抽取）

### B1（codex）：`candidates` schema + 治具

- schema 加進 `docs/mongodb-schema.md`。關鍵欄位：`_id`（來源 URL 的 hash）、`source_site`、`source_url`、`title_ko`、`title_zh`、`summary_zh`、`category`（人物美化／獨立隨從／武器裝備／地圖 porting／其他）、`screenshots[]`（本機相對路徑）、`link_status`、`link_checked_at`、**`review_state`（`pending`/`approved`/`rejected`）+ `rejected_at`**
- 候選入庫工具：吃 agy 產在 `~/skyrim_mods/.candidates/<batch>/` 的原始檔（每筆一個資料夾：`page.html` + `shots/*.jpg` + `meta.json`）→ upsert 進 Mongo。**已是 `rejected` 的 `_id` 直接跳過**
- 連結存活檢查：HEAD 請求填 `link_status` / `link_checked_at`
- 圖庫產生器：出本機 HTML 圖庫（照本 repo 既有 `html-guide` 工作流形狀）

### B2（agy）：採集

- **範圍**：arca.live 等**公開板**與公開部落格。**需登入／入會審核的站（Naver cafe 類）不做。**
- **主題**：人物美化、獨立隨從、武器裝備、其他遊戲地圖 porting
- **下一輪優先條件（使用者 2026-08-07 補充）**：Nexus 政策原因無法上架或較敏感的其他遊戲素材 porting；Google Drive 連結必須有效；優先一次很多套裝備/武器的合集，其次是地圖 porting。
- **只抓不載**：抓頁面 HTML、截圖、原始連結。**絕不下載 mod 本體**
- **產出格式**固定成 B1 定的資料夾結構，`meta.json` 欄位由 codex 指定
- **翻譯**：只翻已抓下來的 `page.html` 內的原文成繁中，寫進 `meta.json` 的 `title_zh`/`summary_zh`。原文一併留著供對照

2026-08-07 執行結果：

- `agy` CLI 三次小/大批次嘗試都在 print mode timeout，沒有產出 fixture；前兩次主要問題是把大型 `~/skyrim_mods` workspace 掛進 agy，第三次不掛 workspace 仍超時。
- `arca.live/b/tullius` 匿名 `curl` 目前回 hCaptcha 門檻，不能作為「機器抓到原物」通過。
- 為完成 B2/B3，codex 改以 deterministic `curl`/Python 從公開 Tistory 頁建立 fixture：`~/skyrim_mods/.candidates/korean-public-2026-08-07-b2/`。本批 6 筆，禁止檔檢查通過，未下載 mod 本體。
- 依使用者補充偏好追加 `korean-policy-porting-2026-08-07-b2b`：3 筆 live pending 候選（BDO Arethel/Heled、Dark Souls 3 Silver Knight、Bloodborne Lantern），均有有效 Google Drive 頁面連結且 `binary_downloaded=false`；另外 3 筆 Drive 失效候選只留在 `_dead_drive/`，不匯入 `skyrim.candidates`。

### B3（codex）：收斂

跑候選入庫工具 + 連結存活檢查 + 圖庫產生器（後兩支在 `agentctl/tools/`），把圖庫路徑交給使用者審閱。
porting 類候選另外整理一段，回饋到 `analysis/port-source-survey/README.md`；要先依頁面內容分清「地圖／場景」與「裝備／道具」，不只看 `other-game-porting` tag。

---
