# 翻譯與中文層（2/2）

[lessons 索引](README.md)｜同主題：[translation-and-zh](translation-and-zh.md)

## zh-layer-gate-base-mod-must-be-enabled

> 中文層部署前要查本體 mod 在 modlist 是否啟用，不能只看 plugins.txt；Apocalypse 案例讓 242 個 Cannot open store 躺了三天（原 type: memory）

2026-09-03 post2 隊發現：Papyrus 323 個 `Cannot open store for class` 有 242 個來自 `Apocalypse - Magic of Skyrim.esp`——本體 `Apocalypse 10.2.3`（含 scripts BSA）早在 profiles 入版控（08-23）前就已停用（連 Ordinator／Vokriinator patch 一起，是刻意退役），但 08-31 22:45 的中文層部署把 `MAG-Apocalypse-Magic-of-Skyrim-CHS-MCM-7934` 啟用並在 plugins.txt 勾了同名 esp。`zh-gap-winners.csv` 把它標成 `ACTIVE-PARTIAL`，因為那張表只看 plugin 是否啟用，沒看本體 mod。

**Why:** 中文層只帶 esp（＋少量 MCM 腳本），本體 BSA 沒載入時 esp 的 VMAD 引用全部落空；`Cannot open store` 存量 318 從 lrinst 之前就在，四隊的「新增 0」驗收都沒發現存量本身就是病。
**How to apply:** 中文層／覆蓋層的部署 gate 要加一條「本體 mod 在 `modlist.txt` 是 `+`」，本體停用就不部署、也不勾 esp；`Cannot open store` 的存量要按 class 歸因到來源 mod（`post2/data/cannot-open-store-by-mod.csv` 的做法：掃 BSA 名稱表＋plugin 位元組搜尋），別只比新增數。zhmake 124 層裡也有 Apocalypse 簡中層，部署前先裁本體去留。相關：[[missing-master-scan-mast-not-housecarl]]、[[slanguage-english-chinese-in-english-slot]]。

## zhport-editorid-fallback-and-hdpt-untranslatable

> 中文層對種子時 FormID 對不上（作者改版重編）要改用 EditorID 比對；HDPT 頭部件 EDID／名稱絕不翻譯（原 type: project）

2026-09-12 want4 批（lead-want4）：`zhport.py` 用 FormID 對舊中文包種子，遇到作者改版整批重編 FormID 時 gaps 被嚴重高估（Runic Arts 少算 170 欄、Sacrifices 605/706）；改用 EditorID 比對就救回。另外 13 個 HDPT 頭部件代號留英文是對的：翻下去 facegen 對名失敗會整顆作廢（見 [[hdpt-edid-must-match-facegen-shape-names]]）。

**Why:** gaps 異常大時工人會急著整包重翻，白花翻譯量又降低一致性。

**How to apply:** 中文層任務 gate 前先看 gaps 比例，>50% 先換 EditorID 比對再決定翻不翻；翻譯範圍排除 HDPT／FLST／種族內部代號，只翻玩家讀得到的欄。
相關：[[translation-layer-cost-threshold]]、[[chinese-diff-ok-but-no-tofu]]

## apocalypse-rebuild-waits-new-playthrough

> "2026-09-25 現役 Apocalypse 中文層其實是 7934 版記錄集（4,218 筆）整支換掉本體；10.2.3 英文底版重建層（staging apoc/）少 465 筆會動舊存檔，留到新周目才裝；同名覆蓋層部署要先比 record 集合"（原 type: memory）

2026-09-25 cx-deploy 前檢抓到：現役 `Apocalypse - Magic of Skyrim.esp` 的 winner 是 `Apocalypse-Magic-of-Skyrim-Simplified-Chinese-FULL-Completion-Combined-Dev-2026-09-03`，它把整支 esp 換成 CHS 7934 版的記錄集（4,218 筆），本體目錄雖是 10.2.3（3,945 筆）但實際跑的是舊結構。cx-apoc 以英文 10.2.3 重建的層（`~/skyrim_mods/_staging-2026-09-25/apoc/`、mod-library `Apocalypse-Magic-of-Skyrim-10.2.3-Chinese-Rebuilt-Dev-2026-09-25`）刪 465 筆／新增 192 筆，裝上去會讓舊存檔指到不存在的 FormID。

**Why**：同名覆蓋型中文層不是「翻譯」而是「整支替換」，版本不同就是換了本體。

**How to apply**：① 舊存檔在用時，Apocalypse 只能裝保留舊結構的 zhfix 層（已於 profiles `6dcb0fa` 部署）；10.2.3 重建層等**新周目**再裝。② 之後任何同名覆蓋層部署前，先用 record 型別＋raw FormID 集合比對現役 winner（cx-deploy 的 `deploy/work/preflight.py`），集合不同就不能在舊存檔上換。③ RDO 62500 Final 集合與現役相同（9,765 筆）可直接換。相關：[[zhport-editorid-fallback-and-hdpt-untranslatable]]、[[nexus-api-version-is-not-proof]]
