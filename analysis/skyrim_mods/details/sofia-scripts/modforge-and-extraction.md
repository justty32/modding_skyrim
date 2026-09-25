# Sofia Follower —— Papyrus 腳本架構 — modforge-and-extraction

[返回入口](../sofia-scripts.md)

## 對 ModForge 的意義

ModForge 已能生成 fragment 那一層（quest fragment / TIF fragment / scene fragment Papyrus，見 ModForge CLAUDE.md「已落地功能」）。Sofia 的 283 個 fragment（TIF/SF/QF/PF）正落在 ModForge 的能力範圍內、且本就該被自動生成。**真正的缺口是那 31 個具名常駐邏輯 script**——一個能動的隨從靠它們活著，而 ModForge 目前一個都不生成。把它們整理成「ModForge 若要做隨從品類，需補的 script 模板」優先序：

<!-- wf-nav -->
1. **跟隨距離維持 / catch-up（`SofiaCatchUpNewScript` 模式）** —— 最不可省。`OnUpdate` poll + `GetDistance` 比 `SofiaCatchUpDistance` GLOB + `HasLOS` + `MoveTo`(+`SetAlpha` 隱形瞬移) + `EvaluatePackage`。這是「隨從不會永遠卡在門後」的引擎。ModForge 有 follow PACK template，但沒有這支補丁式 catch-up script——應做成一個參數化模板（距離 GLOB + 目標 alias）。
2. **comment 排程器（`SofiaCommentScript` 模式）** —— 「會講話的隨從」核心。timer-poll（`RegisterForSingleUpdate`）+ frequency GLOB + 總開關 GLOB + `scene.Start()` 念一句 + `IsInDialogueWithPlayer` 防插嘴。ModForge 有 AutoStart 在場偵測 scene controller（`MFSceneBanterController`），形狀已很接近——把它擴成「依 frequency 週期觸發 idle banter scene」就補上了，這是 ModForge 既有資產最容易延伸出的一支。
3. **取玩家準心目標（`JJSofiaGetTargetScript` 模式）** —— Skyrim 無原生 API，靠 cast 一個 script-effect spell 讀 target。任何「對你正看的東西做反應」的隨從都要這支。小而通用，值得做成模板。
4. **狀態中樞 quest script（`JJSofiaVariablesScript` 模式）** —— 一個 quest 掛滿 conditional property 當持久化狀態表，被對白 condition 直接讀。ModForge 已會生 GlobalSpec（GLOB），但 conditional-property-on-quest 這種「能被對白 condition 讀的 per-quest 狀態」目前沒有抽象——對隨從對白分支很有用。
5. **MCM 設定選單（`SofiaMCMscript` + `SofiaHasSKSEscript` 降級）** —— `extends SKI_ConfigBase` + 一套 OnConfig* 回呼把 GLOB 暴露成選項，配 `SKSE.GetVersion()` 探測降級。隨從類 mod 幾乎都有 MCM，這是 ModForge 最大的「使用者可調設定」缺口（與 `architecture/sofia-follower.md` 的結論一致）。需要生成 SkyUI 基底依賴 + config schema → OnConfig* 模板。
6. **版本升級/腳本重載骨架（`Sofia*Update/NewVersion/ReloadScripts`）** —— 任何要「更新後不破壞舊存檔」的 mod 都需要。ModForge 生成物若要可長期維護，這是務實的一塊。

務實結論：Sofia 在程式碼層也證明了「純 GLOB + quest property + quest stage，零 SKSE 資料結構」足以撐起成熟單體隨從。ModForge 預設不需要 native 依賴。但「隨從會跟上、會應景吐槽」這兩件最定義「活隨從」的事，分別靠 catch-up script 與 comment 排程器——這兩支（加上取準心目標的小工具）是 ModForge 把「能生隨從骨架」變成「能生有靈魂的隨從」最值得先補的 script 模板，且都與 ModForge 既有的 PACK / AutoStart-scene 資產同源、延伸成本低。

## 解包方法與還原程度

**BSA 解包（自寫 extractor，完整還原檔案）。** 目標 `SofiaFollower.bsa`（78 MB），header magic `BSA\0`、version `0x69`(105) = Skyrim SE 格式。先解 36-byte header：`archive_flags = 0x3`（bit0 dir-names + bit1 file-names 存在，**bit2 compressed 未設**），故檔案**未壓縮**、無需 zlib（每檔資料即原始 bytes）。folder_count=13、file_count=1824。用 Python 按 v105 佈局自寫 extractor：13 個 24-byte folder record（uint64 hash / uint32 count / uint32 pad / uint64 offset，offset 需減 total_file_name_length 才是真實位置）→ 每 folder block 前置 1-byte 命名長度 + folder 名 + N 個 16-byte file record（uint64 hash / uint32 size / uint32 offset；size bit30 = 與 archive 預設相反的壓縮 toggle，本檔皆未壓）→ 末端 file-name block（null 分隔，與 record 同序）。只抽 `folder.startswith('scripts')` 的條目，得 **323 個 `.pex`，零遺漏、零損毀**（mesh/texture/voice 未抽）。BSA 內**無 `scripts/source/*.psc`**，只有編譯後 bytecode。pip 上的 `bsa` 套件無內容、`bethesda-structs` 未安裝，故未用第三方庫。

**`.pex` 反組（自寫 PEX header/string-table/debug 解析器，函式簽名級還原）。** Champollion（完整反編譯器）未 build（vcpkg 條目存在但 build 過重，放棄）。改用 Python 自寫 PEX 解析器：PEX 為 big-endian、magic `0xFA57C0DE`，依序讀 header → **string table（u16 count + 每筆 u16-len 字串）** → **debug info（每函式：object/state/name 字串索引 + type + 指令數）** → user-flags/objects。本解析器**完整還原了 string table 與 debug 函式表**（object::state::function 三元組）——這已足以取得：每個 script 的真實 `.psc` 名、所有自訂函式名、所有 property/變數名（`::Xxx_var` 樣式）、所引用的引擎 API 與型別名、以及所有字串字面值（含對白訊息如「Sofia has spent … Septims」）。**未還原的是函式體 bytecode（opcode 指令流）**——故「邏輯做什麼」是由「函式名 + property 名 + 被呼叫的引擎函式名 + 字串字面值 + 對照 record 層」推斷，而非逐行反編譯。對本分析（架構、子系統分工、狀態管理手法、ModForge 模板缺口）這個還原層級完全足夠且結論可靠；若需逐行演算法細節（如 catch-up 的確切距離判斷分支），才需要 Champollion 級反編譯。
