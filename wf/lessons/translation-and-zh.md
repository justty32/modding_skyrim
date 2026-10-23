# 翻譯與中文層

[lessons 索引](README.md)

## zh-layer-gate-base-mod-must-be-enabled

> 中文層部署前要查本體 mod 在 modlist 是否啟用，不能只看 plugins.txt；Apocalypse 案例讓 242 個 Cannot open store 躺了三天（原 type: memory）

2026-09-03 post2 隊發現：Papyrus 323 個 `Cannot open store for class` 有 242 個來自 `Apocalypse - Magic of Skyrim.esp`——本體 `Apocalypse 10.2.3`（含 scripts BSA）早在 profiles 入版控（08-23）前就已停用（連 Ordinator／Vokriinator patch 一起，是刻意退役），但 08-31 22:45 的中文層部署把 `MAG-Apocalypse-Magic-of-Skyrim-CHS-MCM-7934` 啟用並在 plugins.txt 勾了同名 esp。`zh-gap-winners.csv` 把它標成 `ACTIVE-PARTIAL`，因為那張表只看 plugin 是否啟用，沒看本體 mod。

**Why:** 中文層只帶 esp（＋少量 MCM 腳本），本體 BSA 沒載入時 esp 的 VMAD 引用全部落空；`Cannot open store` 存量 318 從 lrinst 之前就在，四隊的「新增 0」驗收都沒發現存量本身就是病。
**How to apply:** 中文層／覆蓋層的部署 gate 要加一條「本體 mod 在 `modlist.txt` 是 `+`」，本體停用就不部署、也不勾 esp；`Cannot open store` 的存量要按 class 歸因到來源 mod（`post2/data/cannot-open-store-by-mod.csv` 的做法：掃 BSA 名稱表＋plugin 位元組搜尋），別只比新增數。zhmake 124 層裡也有 Apocalypse 簡中層，部署前先裁本體去留。相關：[[missing-master-scan-mast-not-housecarl]]、[[slanguage-english-chinese-in-english-slot]]。

2026-10-23 補：帳本標籤「READY-IN-LIBRARY」只代表中文層檔案已在庫、拓撲已驗，不代表本體已裝；曾有交接文件把兩件事併成一句話，誤判成「只差裝中文層」，實際本體都還沒裝進 MO2（Animated Armoury／Immersive Weapons 案例，`agentctl/handoffs/done/2026-08-28/opus-install-prep/PLAN.md:290-312`）。看到 READY 類標籤要額外雙向搜尋 MO2 mods/ 與 modlist 確認本體真的已裝且啟用。

## apocalypse-rebuild-waits-new-playthrough

> "2026-09-25 現役 Apocalypse 中文層其實是 7934 版記錄集（4,218 筆）整支換掉本體；10.2.3 英文底版重建層（staging apoc/）少 465 筆會動舊存檔，留到新周目才裝；同名覆蓋層部署要先比 record 集合"（原 type: memory）

2026-09-25 cx-deploy 前檢抓到：現役 `Apocalypse - Magic of Skyrim.esp` 的 winner 是 `Apocalypse-Magic-of-Skyrim-Simplified-Chinese-FULL-Completion-Combined-Dev-2026-09-03`，它把整支 esp 換成 CHS 7934 版的記錄集（4,218 筆），本體目錄雖是 10.2.3（3,945 筆）但實際跑的是舊結構。cx-apoc 以英文 10.2.3 重建的層（`~/skyrim_mods/_staging-2026-09-25/apoc/`、mod-library `Apocalypse-Magic-of-Skyrim-10.2.3-Chinese-Rebuilt-Dev-2026-09-25`）刪 465 筆／新增 192 筆，裝上去會讓舊存檔指到不存在的 FormID。

**Why**：同名覆蓋型中文層不是「翻譯」而是「整支替換」，版本不同就是換了本體。

**How to apply**：① 舊存檔在用時，Apocalypse 只能裝保留舊結構的 zhfix 層（已於 profiles `6dcb0fa` 部署）；10.2.3 重建層等**新周目**再裝。② 之後任何同名覆蓋層部署前，先用 record 型別＋raw FormID 集合比對現役 winner（cx-deploy 的 `deploy/work/preflight.py`），集合不同就不能在舊存檔上換。③ RDO 62500 Final 集合與現役相同（9,765 筆）可直接換。相關：[[zhport-editorid-fallback-and-hdpt-untranslatable]]、[[nexus-api-version-is-not-proof]]

## slanguage-english-chinese-in-english-slot

> 本包 skyrim.ini 是 sLanguage=ENGLISH，中文全塞在 *_English.STRINGS / *_english.txt 槽；只附 _chinese 檔的中文層會靜默失效（原 type: memory）

2026-08-27 opus-zh-active 稽核發現：`instance/profiles/modpack-main/skyrim.ini` 是 `sLanguage=ENGLISH`，
`Skyrim Traditional Chinese 8.20 Core and Fonts` 把 `*_Chinese.*` 與 `*_English.*` 兩份 STRINGS
都做成繁中內容。所以本包的硬規則：**引擎只讀 English 槽**——MCM 翻譯必須是 `*_english.txt`、
外部字串必須是 `*_English.STRINGS`；只給 `_chinese` 的層裝了看起來沒錯、實機全英文、零報錯。

**How to apply**：
- 評估中文層時先看實體型態：純 ESP 替換層與 sLanguage 無關（排本體下面即可）；
  translations txt 型要確認有 `_english.txt`（或改名）；DSD 型本機沒裝 DSD 不能用。
- 已知踩雷：Missives Settings Loader 只給 `Missives_chinese.txt`（改名即生效）。
- Modex 走自有 JSON 語言系統，要在 Modex 設定裡切語言，光裝中文層不生效。
- 「要不要改 sLanguage」是全域決定，使用者未裁示，不要順手改。

相關：[[no-cht-chs-preference]]、[[translation-layer-cost-threshold]]

2026-10-23 補：CC 官方簡中字串層初版用小寫 `strings/` 資料夾名——MO2 的 wine VFS 對路徑大小寫不敏感，但遊戲引擎讀 `Strings` 子目錄本身在 Proton 下對大小寫敏感，錯了會靜默失效；命名要逐字元比對現役已驗證生效的同類層（`agentctl/handoffs/done/2026-09/home-2026-09-03/cc/REPORT.md:47`）。

## non-localized-esp-overwrites-localized-vanilla-string

> non-localized 插件覆寫 vanilla localized 記錄時會把內嵌英文字串整個蓋掉中文，CELL/NPC 任何「為了改別的欄位整筆 forward」的記錄都會連帶英文化

2026-08-28～09-01 多線重複踩到同一機制：`Common Clothes and Armors` 覆蓋 24 筆 vanilla ARMO 把中文名變英文（`agentctl/handoffs/done/2026-08-27/opus-qa-triage/REPORT.md:279`）；換臉 mod `KuroneYsoldaReplacer.esp` 把 NPC 名字寫死英文字面繞過字串表（`agentctl/handoffs/done/2026-09/home-2026-09-11/misc/REPORT.md:42-47`）；hcell 全機掃描抓到 237 筆 CELL FULL 因為別的欄位（Music/WaterHeight）被順手 forward 而連帶回英文，集中在前五個 winner plugin（`agentctl/handoffs/done/2026-09-01/hcell-2026-09-01/REPORT.md:80-139`）。

**Why:** 問題出在 vanilla localized／覆寫插件 non-localized 的資料層級結構差異，不是排序錯誤，調序救不了，是反覆出現的通用迴歸成因。

**How to apply:** 回報「某物品/NPC/地名變回英文」先查 base record 是不是 vanilla localized、覆寫插件是否 non-localized 或整筆 forward 了別的欄位，修復只在 conflict patch 疊寫 FULL 一欄取回中文；接受「mod 贏過現役」建議前先查現役勝者本身是不是已經中文，避免誤判（`agentctl/handoffs/done/2026-09/home-2026-09-03/go19x/REPORT.md:71`）；決定第三方內容載入序位置前先算這個位置會讓多少欄位中文回退，照代價表選（`agentctl/handoffs/done/2026-09/home-2026-09-03/lrrev/REPORT.md:111`）。相關：[[zh-layer-gate-base-mod-must-be-enabled]]

## zh-layer-exact-match-protocol-topology-not-version-string

> 判斷中文層是否對版，要比對 masters／record 拓撲／FormID 集合是否完全相同，而不是看版本號或 bytes

七步協定在 hmih 八件 mod 稽核落地：身分記錄→分開解壓→二進位拓撲比對（masters/record 計數/FormID set/GRUP 與 subrecord 順序全同才算對齊，硬 gate）→CELL/placement 掃描→asset winner→records/gameplay 接觸面→回滾單位結論（`agentctl/handoffs/done/2026-09-01/hmih-2026-09-01/ANALYSIS-COMMON.md:33-121`；bgdl/ank 兩場次獨立採用同口徑亦判定成功）。版本不嚴格匹配時改用「字串ID集合覆蓋率」量化：100% 覆蓋且非文字欄位不動才可裝（`agentctl/handoffs/done/2026-10/home-2026-10-03/want-watch/rounds/20261003-1410/REPORT.md`）。

**Why:** 版號、header、bytes 都可能騙人——header 版號常落後於頁面最新檔案，唯一可信的是逐欄位拓撲比對。

**How to apply:** 搜中文層要廣搜本體全名＋常見後綴變體（CHS/CHT/zh_CN/譯者自訂名），不要只加 Chinese 關鍵字；選檔比對 Nexus files 分頁的精確 MAIN 版本，不信 header；判定「已有/已完整」前先查實際 load order winner（不要只憑有 CHT 資料夾就假設已中文化），翻譯層幾乎都在 Nexus、中文站只當補充；偵測是否已含中文要用 UTF-8 解碼＋連續漢字門檻＋濾假名；同一 plugin 若有多個兄弟 overlay 要先合併成單一 Combined 層才能裝，覆蓋率統計對每層各自 diff 再聯集，不能只看最上層；分母排除英文原本就空的欄位，BSA-only 字串算不出時要註明是下界。相關：[[zh-layer-gate-base-mod-must-be-enabled]]、[[zhport-editorid-fallback-and-hdpt-untranslatable]]

## zh-carrier-type-determines-deploy-risk

> 中文層的實作方式（純 Strings／整支 esp 替換／MCM txt／BSA 注入／DSD）決定它會不會被本體升版拖垮，體積與檔案型態就是訊號

Frozen Heart 只換 3 支 Strings 檔（ESM localized flag），本體升版腳本/模型/地形不受影響，只需比對字串編號集合；整支 esp 替換型（如 BnB）升版會把新版記錄整個蓋回舊版，須走拓撲 gate（`agentctl/handoffs/done/2026-10/home-2026-10-10/frozenheart-zh/REPORT.md`）。體積是另一訊號：KB 級通常純字串替換，百 MB 級是整包重打包，曾遇 210MB BSA 注入型層整包蓋掉本體資產需獨立驗收（`agentctl/handoffs/done/2026-09/home-2026-09-03/zhnex/REPORT.md:118`；`agentctl/handoffs/done/2026-08-28/opus-zh-summary/SUMMARY.md:730-732`）。DSD 是 runtime 字串替換,不參與 record 衝突、恆勝過 ESP 層且會遮蔽版本漂移（`agentctl/handoffs/done/2026-08-30/zh-2026-08-30/DSD-WINNER-CONTRACT.md:6-60`）；MCM 的 translations txt 只改介面文字，解決不了 ESP record 缺口。

**Why:** 不同載體的升版風險、覆蓋範圍、失效模式完全不同，用同一套 gate 驗收會漏判。

**How to apply:** 部署前先判定載體型態；純 Strings 型比對編號集合即可，整支替換型要走拓撲比對；補丁排在整支替換層之後又帶英文 FULL/DESC 要疊 forward 層把中文聯集加回去；覆蓋層 MO2 優先度用 `--priority before:`，`after:` 是排後面＝更低優先權，容易弄反；自帶 checksum/完整性檢查的 mod（如 OStim）覆寫前先讀原始碼找出被鎖定檔名，改完重算 checksum 附上；框架用「目錄列舉＋先讀先贏」載入翻譯檔的，只能同名覆蓋不能靠加新檔案。相關：[[slanguage-english-chinese-in-english-slot]]

2026-10-23 補（E2bs-07）：現成中文包版本落後本體時（Chatty NPCs 1.51 vs 1.6.1 少 4~5 條 QUST 條件、FLST 少 LNAM、少整筆 KYWD），直接拿中文包 esp 出貨等於把 mod 降級；一律改以本體 esp 當載體、用 zhport 類工具只搬中文字串，記錄結構一個位元不動，讓完整性由「結構沒改過」保證而不靠版本號（`agentctl/handoffs/done/2026-09/home-2026-09-11/zh/REPORT.md:46-49`）。
