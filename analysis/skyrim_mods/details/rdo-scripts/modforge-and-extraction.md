# RDO 的 Papyrus 腳本：投放靠資料、腳本只補三件小事 — modforge-and-extraction

[返回入口](../rdo-scripts.md)

## 7. 對 ModForge 的意義

解包結果**正面印證** dialogue-targeting-technique.md 與 modforge-relevance.md 的核心判斷：要複製 RDO 式對話包，重點在 **spec/builder（condition + FormList + vanilla override）**，而非生成複雜 Papyrus。

具體推論：

<!-- wf-nav -->
1. **不需要生成「投放邏輯」的 Papyrus**。RDO 規模再大也沒寫一行「決定投給誰」的 script——這件事 ModForge 應該也用純 condition + FormList 在 build 期產出，與其現有 `BuildCondition` dispatch 路線一致（modforge-relevance.md §二.1 列的 `GetIsVoiceType`/`IsInList` 補 case 即可）。
2. **FormList builder 是靜態產物**，不必生成任何維護它的 script——RDO 的 18 個 voice 名單全靜態。ModForge 加 FormList builder 是純 record 生成工作。
3. **真正需要生成的 script 只有三類小東西**，且 ModForge 多半已有對應能力：
   - 節流計時器（per-VoiceType 寫 GlobalFloat）——ModForge 已能生成 GLOB + quest fragment 風格 Papyrus（CLAUDE.md「已落地：Quest 階段 / MFSE_AdvanceStage」），這類「擲骰寫全域變數」的 fragment 是同型工作。
   - 一兩行的 TIF/SF fragment（SetStage / Start quest）——ModForge 的 `Generator.QuestFragments.cs` 正是做這個。
   - alias `OnDeath → Clear()` / `OnPlayerLoadGame → 修補`——ModForge 已有 alias 腳本生成（`RDO_ClearAliasScript` 與 ModForge 既有的 alias OnActivate 同型）。
4. **MCM 開關可以「偽 MCM」起步**：RDO 證明 SE 早期連 SkyUI 都不用，純 `Quest Conditional` bool + `GetVMQuestVariable` 就能做功能開關。ModForge 若要做對話包的開關，最低成本路線是生成這種偽 MCM quest，而非一開始就上 `SKI_ConfigBase`（後者是 modforge-relevance.md §二.3 的進階 opt-in）。

一句話收束：**RDO 把「規模」全押在資料，把 script 壓到 vanilla 框架的最小公倍數。ModForge 要抄 RDO，抄的是它的 spec 範式（override + condition 模板 + FormList），生成的 Papyrus 反而比 ModForge 現有 trigger 庫還簡單。**

## 解包方法與還原程度

**第一關 — 解 BSA（自寫 Python extractor）**

<!-- wf-nav -->
- pip BSA 庫（`bethesda_structs` / `bsa` / `libbsa`）本機皆無、`7z 26.01` 無法把此檔當 archive 開啟、系統無 `bsarch`/`bsab`。改走自寫 extractor。
- 讀 header（`/tmp/bsa_extract.py`）：magic `BSA\0`、version **105**（SSE）、archiveFlags `0x33`（= include-dir-names | include-file-names | **compressed** | bit5）、folderCount 73、fileCount 5619、fileFlags `0x11b`。
- v105 的 folder record 為 24 bytes（uint64 offset）；file record 16 bytes；folder-name block 與 file-name block 依格式逐段解析。檔案大小高位 bit `0x40000000` = 該檔壓縮旗標**反轉** archive 預設。
- 壓縮為 **zlib**（非 lz4——本機無 lz4 模組，但 SSE BSA 用 zlib，Python stdlib `zlib.decompress` 即可，前 4 bytes 為原始大小）。
- 只抽 `scripts/`（`.pex`）與 `scripts/source/`（`.psc`），**跳過所有 sound/voice/`.fuz`**（佔 116 MB 絕大體積）。成功抽出 **196 檔 = 98 `.pex` + 98 `.psc`**，解壓後大小合理（數百 B 到 12 KB）。

**第二關 — 讀 `.pex`：不需要**

BSA 內附完整 `scripts/source/*.psc` 原始碼，與 `.pex` 一一對應。本文全部引用直接取自 `.psc` 純文字，**還原程度 100%（即原始碼，非反編譯重建）**，無需 Champollion / PEX string-table 解析 / `strings`。

**取證索引**

- 解包腳本：`/tmp/bsa_extract.py`；輸出：`/tmp/rdo_bsa/scripts/`（.pex）、`/tmp/rdo_bsa/scripts/source/`（.psc）。
- 節流：`rdo_idlecommenttimerfnord.psc`（`Commented()` 寫 `a_RDO_FNORDNextComment`）、`rdo_nextidlecommentfnord.psc`（fragment 殼）。
- 名單證偽：`grep -rniE "RDOVoices|AddForm" /tmp/rdo_bsa/scripts/source` 僅命中 `rdo_mcmconfig.psc:198+` 的 LeveledActor 注入。
- 偽 MCM：`rdo_mcmconfig.psc:1`（`extends Quest Conditional` + 頂部註解）。
- 隨從：`rdo_geleborfollowerscript.psc`、`rdo_defaultfollowme.psc`/`rdo_defaultrecruit.psc`（呼叫 vanilla `DialogueFollowerScript`）。
- 共用工具：`rdo_miscsharedinfoquestscript.psc`（`RDO_MakeFollower`/`RDO_SetGiftFactionRank`/`RDO_ApplyFixes`）。
