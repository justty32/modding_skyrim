# Kurone Soul Tomb 換臉挑選頁（2026-11-16）

[入口頁](../2026-11-16-kurone-soultomb-pick.md)

給使用者在桌面挑「Soul Tomb 角色 → 哪個隨從」和身形的離線頁。頁面本身在使用者桌面 `~/Desktop/kurone-soultomb-pick.html`，不進版控；這裡放資料表與重產腳本。換臉不移除原 NPC（使用者 2026-11-16 原話），所以頁面沒有隱藏素材選項。

## 資料表（`data/`，wf-table/1，modpack-main 2026-11-16 現役贏家）

- [donors.json](data/donors.json)（68 列）：Soul Tomb 可當素材的 NPC。欄位：formkey、edid、name_zh（CHS 層贏家名）、name_en（英文原名）、plugin、race、sex、group（主要角色／雜兵）、custom_race（自訂種族）、placed（世界中擺放數）、note、facegen_layer。女 44（其中 43 位是自訂種族）、男 24（雜兵 14）。
- [donors-excluded.json](data/donors-excluded.json)（38 列）：排除的素材與原因：生物／無臉 23、屍體道具 10、同一角色的劇情分身 5（混沌乙女 3、弗倫 2）。
- [targets.json](data/targets.json)（256 列，76 個 mod）：帶隨從派系（PotentialFollowerFaction／CurrentFollowerFaction）的人形 NPC，加上 Serana、語音隨從名冊與 11-07 身體表裡的人。欄位：formkey、edid、name（優先中文）、mod（定義 plugin 的原始 mod）、race、sex、face_now（facegen 現役提供者；空＝原版 BSA）、face_note、body_now、kurone_1107、follower_faction。女 161。原版 NPC 的 mod 欄寫「原版 Skyrim／DLC／CC」。
- [targets-excluded.json](data/targets-excluded.json)（176 列）：PROTEUS 玩家預設槽 81、Soul Tomb 自己的角色 47、動物／生物 34、沒名字的範本 14。
- [bodies.json](data/bodies.json)（13 列）：不換、Rim Lydia、Big Change V2、MAIN 原裝 9 種、Kurone7 預設（Soul Tomb 現用）。

## 匯出 JSON

格式 `kurone-soultomb-pick/1`，欄位說明在頁面 NOTES（[tools/NOTES.md](tools/NOTES.md)）。換臉施工線直接吃 `picks[]`：`target`、`donor`（null＝不換臉）、`parts`、`body.id`、`warnings`。

## 重產

腳本在 [tools/](tools/)：`dump_soultomb_npcs.py`（Soul Tomb NPC 原始傾印）→ `scan_followers.py`（全載入序隨從掃描）→ `prep_tables.py`（篩選規則都寫在裡面）→ `build_page.py`（把表塞進 `page-template.html`）。全部唯讀，只讀 MO2 mods 與 profile。

## 驗收（2026-11-16，skyrim-alt-looks）

頁面範本由 gpt 工人 skyrim-alt-looks-page-11161 寫（它的說明在 [tools/NOTES.md](tools/NOTES.md)；它沒有執行環境，執行驗收由上游做）。上游實測：node 語法檢查通過；無頭 Firefox（`tools/ff_test.py`，獨立 profile）無 JS 錯誤、256 列都在、預設只顯示女性 161 列；兩列選同一素材兩列都標紅；男性目標選 Kurone 身形有提醒；素材下拉預設同性別（女目標 45 項、男目標 25 項，開關打開 69 項），已選的異性素材在關掉開關後仍保留；匯出→清除→匯入後 picks 完全相同；檔內無外部網址。
