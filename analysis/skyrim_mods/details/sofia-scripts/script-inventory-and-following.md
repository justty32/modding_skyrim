# Sofia Follower —— Papyrus 腳本架構 — script-inventory-and-following

[返回入口](../sofia-scripts.md)

## 腳本清單（323 個，分四群）

來源：`SofiaFollower.bsa` → `scripts/`（解出於 `_sofia_extract/scripts/`）。檔名前綴即 CK 自動生成的 fragment 類別：

| 群 | 數量 | 命名 | 性質 |
|---|---|---|---|
| TIF（TopicInfo fragment） | 259 | `tif__<formid>.pex`，內部 `SRC: TIF__<FORMID>.psc` | 對白行的「結束/開始 fragment」，CK 編輯對話時掛的小片段 |
| 具名邏輯 script | 31 | `sofia*.pex` / `jjsofia*.pex` / `ski_*.pex` | 隨從的真正「大腦」與各子系統 |
| PF（Package fragment） | 11 | `pf_<pkgname>_<formid>.pex` | package 的 OnBegin/OnEnd/OnChange fragment |
| 每-NPC comment | 9 | `nazeem_comment1..3` / `carlotta_comment1..4` / `braith_comment1..2` | 對特定 vanilla NPC 吐槽的對白 fragment（手刻、非模板展開） |
| SF（Scene fragment） | 8 | `sf_<scenename>_<formid>.pex` | scene phase 的 fragment（醉酒/婚禮/idle/主線/comment scene） |
| QF（Quest fragment） | 5 | `qf_<questname>_<formid>.pex` | quest stage 的 fragment（quest/drunk/wedding/trackingmarker/Jarvis 彩蛋） |

數量驗證：259 + 31 + 11 + 9 + 8 + 5 = 323。

### TIF / SF / QF / PF —— fragment 群（283/323，佔 88%）

這四群佔了腳本總數近九成，但**單個都極小**。典型 TIF（`TIF__00020948.psc`）只有一個 `Fragment_0` 函式 + 二三個 property（指向某個 quest/scene）。它們不是「邏輯」，而是 CK 把對白選項 / scene phase / quest stage / package 事件上掛的「按一下執行這幾行」的接著劑——`Fragment_N` 函式體內通常就是 `SetStage()`、`Start()` 某個 scene、設一個 GLOB。

這正是 **ModForge 目前已能生成的那一類**（CLAUDE.md「已落地功能」：quest fragment / TIF fragment Papyrus、scene fragment）。Sofia 有 259 個 TIF——印證一個對白量大的隨從，光對白 fragment 就會是腳本檔數的主體，但這些是機械化、模板化的，自動生成正是它們該被生成的方式。

具名的 fragment 例外值得記一筆：
- `QF_JJSofiaWeddingCeremony`（`Fragment_4/6/8/10`，11 prop）—— 婚禮 quest 各 stage 的演出觸發，property 全是 `Alias_*`（PriestRef / SofiaRef / PlayerRef / 各 marker）+ `SofiaWeddingScene` + `TimeScale`，fragment 在對應 stage 啟動婚禮 scene 並調時間流速。對照 record 層的 wedding stage 0→200。
- `SF_JJSofiaDrunkScene` / `SF_JJSofiaMainQuestDialogueScene`（後者 record 層即那段 17-phase 線性獨白）—— scene 各 phase 的 fragment。
- `pf__02065568.pex` / `pf__0206602f.pex` 等無名 PF —— package fragment，多半空殼或一兩行 EvaluatePackage。

## 核心邏輯 script —— Sofia 的「大腦」分工

31 個具名 script 才是真正的隨從邏輯。沒有單一巨無霸狀態機；Sofia 把「大腦」**按子系統拆成數個常駐 quest-script**，呼應 record 層觀察到的「微服務式 quest 拆分」。按職責與規模分群（規模見文末，依 `.pex` byte 數）：

### A. 跟隨與在場核心

<!-- wf-nav -->
- **`SofiaFollowerScript.psc`**（掛 `JJSofiaFollowerMain`，12 prop）—— 隨從**狀態機本體**。函式 `SetFollower / FollowerWait / FollowerFollow / DismissFollower`，property 含 `pFollowerAlias`（ReferenceAlias）、`pCurrentHireling`（faction）、各式 `FollowerDismissMessage*`（Companions / Wedding / Wait 的解散訊息，男女分版）、`FollowerHuntingBow`+`FollowerIronArrow`（解散時發還的預設武器）。它走的是 **vanilla 隨從框架的 SetPlayerTeammate / AddToFaction(CurrentHirelingFaction) / RemoveFromFaction** 那套，加上 `SetObjectiveDisplayed`、`StartTimer`、`RegisterForUpdateGameTime`。這就是 record 層 objective[10]「is waiting for you」背後的程式碼。

- **`SofiaCatchUpNewScript.psc`**（掛 `JJSofiaScripts`，16 prop）—— **catch-up 跟隨**（隨從脫隊時瞬移趕上）。核心函式 `OnUpdate` + `SofiaCatchUp`：用 `GetDistance` 量 Sofia 對玩家距離，超過 `SofiaCatchUpDistance`（GLOB，MCM 可調）且 `SofiaCatchUpEnabled` 開、`HasLOS` 判定後 `MoveTo` 把 Sofia 拉到玩家身邊再 `EvaluatePackage`。節拍用 `RegisterForSingleUpdate`（poll 迴圈）。同檔還管馬（`SofiaRideHorse`：`SofiaHorseEnabled` 時夾帶 `JJSofiaMountHorseScene` / `JJSofiaDismountHorseScene`、`SofiaHorseSummoned`、`COCMarker`），並用 `SetAlpha`（隱形瞬移避免玩家看到 pop-in）。這是「真隨從必備、但 ModForge 完全沒有」的典型常駐邏輯。

- **`SofiaLeadTheWayScript.psc`**（7 函式：`OnPackageStart/End/Change` + `OnUpdate`）—— 帶路到目的地，靠監聽 package 生命週期事件推進。對應 record 層 `JJSofiaLeadTheWay` quest。

