# Sofia Follower —— Papyrus 腳本架構 — infrastructure-and-state

[返回入口](../sofia-scripts.md)

### E. 系統 / 基礎建設

<!-- wf-nav -->
- **`SofiaMCMscript.psc`**（掛 `JJSofiaMCM`，**最大的 script，21.7 KB、19 函式、24 prop**）—— SkyUI MCM 設定選單。函式全是 SkyUI 框架回呼：`OnConfigInit/OnConfigOpen/OnConfigClose/OnPageReset/OnOptionSelect/OnOptionSliderAccept/OnOptionMenuAccept/…`，外加 `ResetSofia`（重置隨從）、`RemoveAllSpells`、`UpdateStats`、`IntToHex`。它 `extends SKI_ConfigBase`（SkyUI 提供的基底；同 BSA 內無此基底 `.pex`，靠玩家裝 SkyUI 提供），把 record 層那批 MCM-寫入 GLOB（`SofiaCatchUpEnabled/Distance`、`SofiaCommentFrequency`、`SofiaDisableComments`、`SofiaHorseEnabled`、戰鬥風格 index…）暴露成可調選項。**這是 Sofia 唯一真正吃 SKSE/SkyUI 的地方，且為選配。**
- **`SofiaHasSKSEscript.psc`**（`CheckSKSE`）+ **`SofiaCheckOnLoadSKSE.psc`** —— **SKSE 探測降級**。`CheckSKSE` 呼叫 `SKSE.GetVersion()`（string table 裡的 `skse` / `GetVersion`）判斷有無 SKSE，設 `SofiaHasSKSE` GLOB；沒 SKSE 就跳過 MCM、用預設值跑。這就是 readme「Do I need SKSE? No」的程式碼證據。
- **`SofiaNewVersionScript.psc`** / **`SofiaUpdateScript.psc`** / **`SofiaReloadScripts.psc`** / **`JJSofiaScriptsStartup.psc`** —— 版本升級/腳本熱重載骨架（舊存檔升新版時重設 property、重註冊 update）。對應 record 層 `SofiaIsUpdated`/`SofiaModVersion` GLOB。
- **`SofiaAliasScript.psc`**（`OnDeath/OnPackageChange`，`extends ReferenceAlias`）—— 掛在 Sofia 的 alias 上，處理她死亡（essential 復活流程）與 package 切換。
- **`SKI_PlayerLoadGameAlias.psc`**（`OnPlayerLoadGame`）—— SkyUI 提供的標準「玩家讀檔時觸發」alias 基底（隨 SkyUI 一起編進來，用於 MCM 重註冊）。
- **`JJSofiaSummon.psc`** / **`JJSofiaSetHorseEffect.psc`** —— 召喚找人 spell（`SummonSofiaSpell`）與召喚馬的 magic effect。
- **`SofiaKeyDebugScript.psc`**（`OnKeyDown` + `RegisterForKey`）—— **熱鍵 debug**（需 SKSE 的 `RegisterForKey`），開發者用，玩家版多半不綁鍵。

### F. 每-NPC comment（手刻 9 支，非模板展開）

`nazeem_comment1..3`、`carlotta_comment1..4`、`braith_comment1..2` —— 對應 record 層那套「8 組 `*Comment` quest + `*SayComment` scene」。**注意：這些是手刻命名的獨立 fragment，不是程式化批次展開**——印證 record 層的判斷「同一份模板複製 N 份、手動換目標 actor 與台詞」。Guard/Taarie 的 comment 則走 SF（`sf_jjsofiaguardsaycomment` / `sf_jjsofiataariesaycomment`），混用兩種掛法。

## 狀態管理手法 —— 印證「零 SKSE 資料結構依賴」

對全部 323 個 `.pex` 的 string table 做精確 token 掃描（`StorageUtil` / `JContainers64` / `JValue` / `JFormDB` / `JIntMap` / `JFormMap` / `PapyrusUtil`）：**零命中**。唯一含 `skse` 子字串的是檔名（`SofiaHasSKSEscript` 等），其引用的也只是 `SKSE.GetVersion()` 做版本探測，與 `RegisterForKey`（debug 熱鍵，選配）。

因此 record 層的結論在程式碼層完全成立——Sofia 的狀態三條腿：

1. **GlobalVariable（57 個）**：跨子系統共享的旗標與設定（catch-up/comment 開關與數值、好感度 `SofiaPlayerLike`、`SofiaHasSKSE`、技能鏡像、暫存 `JJTemp*`）。多支 script 共讀同一批 GLOB（如 `SofiaCommentFrequency` 被 CommentScript 與 MCMScript 共用）——GLOB 當「跨 script 全域變數」用。
2. **Quest script property**：`JJSofiaVariablesScript` 的 33 個 conditional property、`SofiaMCMscript` 24 prop、`SofiaFollowerScript` 12 prop、`JJSofiaQuestLineManager` 161 prop——Papyrus property 隨 quest 進存檔，承載「複雜/結構化但無需 per-actor 表」的狀態。conditional property 還能被對白 condition 直接讀，省去 getter。
3. **Quest stage**：線性進度（wedding 0→200、drunk 0→50），由 QF fragment 推進。

**為何夠用、不需 JContainers**：Sofia 是唯一隨從，好感度只要一個 GLOB，從不需要「每個 NPC 各自一張狀態表」那種會逼出 JFormDB 的場景（對照 `architecture/jcontainers.md` 對 per-actor KV 的分析）。`JJSofiaQuestLineManager` 那 161 個 property 看似龐大，但它是**靜態的 Form 引用表**（編譯期固定），不是 runtime 動態增長的容器——用 property bag 就能裝，正是「不掛 native 資料結構」的關鍵。

