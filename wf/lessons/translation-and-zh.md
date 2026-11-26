# 中文層部署 gate 與引擎的字串機制

[lessons 索引](README.md)｜對版與載體見 [zh-layer-version-and-carrier](zh-layer-version-and-carrier.md)，政策見 [zh-policy-and-naming](zh-policy-and-naming.md)，工具與掃描見 [zh-tooling-and-scans](zh-tooling-and-scans.md)

## zh-layer-gate-base-mod-must-be-enabled

> 中文層部署前要查本體 mod 在 modlist 是否啟用，不能只看 plugins.txt；本體停用而中文層 esp 啟用會造成成批 `Cannot open store for class`

2026-09-03：中文層只帶 esp（＋少量 MCM 腳本），本體（含 scripts BSA）沒載入時 esp 的 VMAD 引用全部落空，噴 `Cannot open store for class`。只看 plugin 是否啟用的帳（如 `zh-gap-winners.csv`）會把這種層標成 `ACTIVE-PARTIAL`；只驗「新增 0」看不出存量本身就是病。

**How to apply:** 中文層／覆蓋層的部署 gate 加一條「本體 mod 在 `modlist.txt` 是 `+`」，本體停用就不部署、也不勾 esp；`Cannot open store` 的存量要按 class 歸因到來源 mod（`post2/data/cannot-open-store-by-mod.csv` 的做法：掃 BSA 名稱表＋plugin 位元組搜尋），別只比新增數。相關：[[missing-master-scan-mast-not-housecarl]]、[[slanguage-english-chinese-in-english-slot]]。

帳本標籤「READY-IN-LIBRARY」只代表中文層檔案已在庫、拓撲已驗，不代表本體已裝；兩件事併成一句話會誤判成「只差裝中文層」（2026-10-23，Animated Armoury／Immersive Weapons 案例，`agentctl/handoffs/done/2026-08-28/opus-install-prep/PLAN.md:290-312`）。看到 READY 類標籤要額外雙向搜尋 MO2 mods/ 與 modlist 確認本體真的已裝且啟用。

## slanguage-english-chinese-in-english-slot

> 本包 skyrim.ini 是 sLanguage=ENGLISH，中文全塞在 *_English.STRINGS / *_english.txt 槽；只附 _chinese 檔的中文層會靜默失效

`instance/profiles/modpack-main/skyrim.ini` 是 `sLanguage=ENGLISH`，`Skyrim Traditional Chinese 8.20 Core and Fonts` 把 `*_Chinese.*` 與 `*_English.*` 兩份 STRINGS 都做成繁中內容（2026-08-27）。所以本包的硬規則：**引擎只讀 English 槽**——MCM 翻譯必須是 `*_english.txt`、外部字串必須是 `*_English.STRINGS`；只給 `_chinese` 的層裝了看起來沒錯、實機全英文、零報錯。

**How to apply**：
- 評估中文層時先看實體型態：純 ESP 替換層與 sLanguage 無關（排本體下面即可）；translations txt 型要確認有 `_english.txt`（或改名）；DSD 型本機沒裝 DSD 不能用。
- 已知踩雷：Missives Settings Loader 只給 `Missives_chinese.txt`（改名即生效）。
- Modex 走自有 JSON 語言系統，要在 Modex 設定裡切語言，光裝中文層不生效。
- 「要不要改 sLanguage」是全域決定，使用者未裁示，不要順手改。

字串層資料夾名大小寫要對（2026-10-23）：MO2 的 wine VFS 對路徑大小寫不敏感，但遊戲引擎讀 `Strings` 子目錄本身在 Proton 下對大小寫敏感，用小寫 `strings/` 錯了會靜默失效；命名要逐字元比對現役已驗證生效的同類層（`agentctl/handoffs/done/2026-09/home-2026-09-03/cc/REPORT.md:47`）。

相關：[[no-cht-chs-preference]]、[[translation-layer-cost-threshold]]

## non-localized-esp-overwrites-localized-vanilla-string

> non-localized 插件覆寫 vanilla localized 記錄時會把內嵌英文字串整個蓋掉中文，CELL/NPC 任何「為了改別的欄位整筆 forward」的記錄都會連帶英文化

2026-08-28～09-01：覆寫 vanilla ARMO 的 mod 把中文名變英文（`agentctl/handoffs/done/2026-08-27/opus-qa-triage/REPORT.md:279`）；換臉 mod 把 NPC 名字寫死英文字面、繞過字串表（`agentctl/handoffs/done/2026-09/home-2026-09-11/misc/REPORT.md:42-47`）；只為改 Music／WaterHeight 而整筆 forward 的 CELL 連帶 FULL 回英文，集中在少數 winner plugin（`agentctl/handoffs/done/2026-09-01/hcell-2026-09-01/REPORT.md:80-139`）。

**Why:** 成因是 vanilla localized／覆寫插件 non-localized 的資料層級差異，不是排序錯誤，調序救不了，是反覆出現的通用迴歸成因。

**How to apply:** 回報「某物品/NPC/地名變回英文」先查 base record 是不是 vanilla localized、覆寫插件是否 non-localized 或整筆 forward 了別的欄位，修復只在 conflict patch 疊寫 FULL 一欄取回中文；接受「mod 贏過現役」建議前先查現役勝者本身是不是已經中文，避免誤判（`agentctl/handoffs/done/2026-09/home-2026-09-03/go19x/REPORT.md:71`）；決定第三方內容載入序位置前先算這個位置會讓多少欄位中文回退，照代價表選（`agentctl/handoffs/done/2026-09/home-2026-09-03/lrrev/REPORT.md:111`）。相關：[[zh-layer-gate-base-mod-must-be-enabled]]
