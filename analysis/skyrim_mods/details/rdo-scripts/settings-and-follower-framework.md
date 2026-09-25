# RDO 的 Papyrus 腳本：投放靠資料、腳本只補三件小事 — settings-and-follower-framework

[返回入口](../rdo-scripts.md)

## 4. 「MCM」其實是偽 MCM：用 Quest 變數當開關

`RDO_MCMConfig`（`rdo_mcmconfig.psc`，全 mod 最大的 script，12 KB）**不是** SkyUI 的 `SKI_ConfigBase`，而是 `extends Quest Conditional`。腳本頂部註解講明原因：寫於 SE 早期、SKSE/SkyUI 尚未移植，所以改用「Quest Conditional + bool property」當設定載體：

```papyrus
Scriptname RDO_MCMConfig extends Quest Conditional
{... RDO will still work by extending Quest Conditional because the
script variables can still be accessed with the GetVMQuestVariable condition.}
bool property FemaleNordFriendVal = True Auto Conditional
bool property MaleDrunkEnemyVal  = True Auto Conditional
```

每個 VoiceType × {Friend / Enemy / Idle} 一個 bool property（數十個）。「關掉某嗓音的某類台詞」= 把對應 bool 設 False，再由台詞 INFO 上的 `GetVMQuestVariable` condition 讀這個變數放行/擋下。**設定開關依然落在 condition 投放層**，script 只是被動的變數容器 + 啟動時的一次性修補（§3）。這正呼應 targeting-technique 把 `GetVMQuestVariable`（1476 次）列為「狀態機/開關」維度。

其餘單支腳本，全是 vanilla 對話框架的標準黏合件，無一觸及投放：

<!-- wf-nav -->
- **TopicInfo fragment（TIF/SF）**：`rdo_thisquestsetstagetif.psc`（`ThisQuest.SetCurrentStageID(StageToSet)`）、`rdo_startquesttif.psc`（`QuestToBegin.Start()`）、`rdo_startspousestore.psc`、`rdo_showfriendgiftmenu.psc`、`rdo_changegiftfactionrank.psc`、`rdo_actordrawweapon.psc`、`rdo_dlc1bossfightdialogue.psc`、`rdo_tg08bmnordbanditkill.psc`——每支都是一兩行的 CK fragment 殼。
- **alias 腳本**：`rdo_clearaliasscript.psc`（`OnDeath → Self.Clear()`，死亡清 alias，與 ModForge 的 `RDO_ClearAliasScript` 同型）、`rdo_playeraliasquestfixesonload.psc`（`OnPlayerLoadGame → MiscQuestScript.RDO_ApplyFixes()`）。
- **共用 quest 腳本** `RDO_MiscSharedInfoQuestScript`（`rdo_miscsharedinfoquestscript.psc`，6 KB）：`RDO_MakeFollower/MakeSpouse`（加減 vanilla 隨從/婚姻陣營）、`RDO_SetGiftFactionRank`（送禮升 `a_RDOGiftFaction` rank、滿級反而 `SetRelationshipRank(-1)`）、`RDO_ApplyFixes`（修 vanilla 漏洞：救過 Saadia / 復原 Gildergreen 後 NPC 關係竟不變 → 補成 friend）。全是「改 faction/relationship 數值」的小工具函式。
- **say-once 載體** `rdo_sayoncevariablesscript.psc`：空 `Quest Conditional`，純粹給「非 Start-Game-Enabled quest 的 Say-Once 旗標」當變數掛點。

## 5. 隨從框架：自管 follower，重抄 vanilla 模式

唯一「有份量」的 script 內容是隨從系統，但它服務的是 **RDO 原創/恢復的具名隨從**（Gelebor、Isran、Valerica，各 7 支；外加 Kaie 劇情），不是對話投放：

- **`RDO_GeleborFollowerScript extends Quest Conditional`**（`rdo_geleborfollowerscript.psc`）自己實作 recruit/wait/follow/dismiss/setFollowDistance：`SetPlayerTeammate()`、`ForceRefTo`、`IgnoreFriendlyHits()`、近/中/遠跟隨用三個 bool（`RDOFollowDistance{Close,Medium,Far}`）+ `EvaluatePackage()`——典型的 self-managed follower，跟隨距離一樣靠 `Conditional` bool 給 AI package 的 condition 讀。
- **`RDO_Default*` 系列（10 支）**走另一條路——直接呼叫 **vanilla 的** `DialogueFollowerScript`：`(GetOwningQuest() as DialogueFollowerScript).FollowerFollow()`、`(pDialogueFollower as DialogueFollowerScript).SetFollower(akspeaker)`。這是把通用 NPC 接上原版隨從系統的「免寫 script」捷徑，對應 ModForge 筆記 It.32 偏好的「vanilla SetFollower」路徑。

這驗證了 sofia-follower.md 與 modforge-relevance.md 的判斷：**單一/少數具名隨從用 vanilla quest 機制就夠，不需要 SKSE 資料結構**。RDO 的 follower script 全程零 native 依賴。

## 6. script vs 純資料的比例判斷（明確結論）

| 行為 | 載體 | 靠 script？ |
|---|---|---|
| 「哪句台詞投給哪個 NPC」 | INFO + condition（VoiceType/Faction/Rank/RandomPercent…） | **完全不靠** |
| 「目標名單 / 排除名單」 | 18 個靜態 FormList + `IsInList` | **完全不靠**（FormList 是 CK 靜態資料） |
| 「功能開關（某嗓音某類台詞開/關）」 | MCM bool property + `GetVMQuestVariable` | 變數載體是 script，**判斷在 condition** |
| 「同嗓音不刷屏」節流 | 20 支計時器寫 `a_RDO_*NextComment` GlobalFloat | **靠 script**（唯一與投放相關，但只管「何時」非「給誰」） |
| quest 階段推進 / 對話起手 | TIF/SF fragment（一兩行殼） | 靠 script（vanilla 框架本來就要） |
| 具名隨從管理 | follower quest script | 靠 script（與對話投放無關） |
| vanilla 關係漏洞修補 | `RDO_ApplyFixes` 等 | 靠 script（一次性數值修補） |

換算規模感：6650 句新台詞 + 海量 condition + 18 FormList = **資料**；98 支 script 裡真正獨立的內容腳本約十餘支，其餘是 40 支機械複製的節流器/觸發殼 + 21 支三名隨從的同套框架複製。**RDO 的行為 95% 以上靠 record + condition + 靜態 FormList，script 只補節流、隨從、fragment 黏合三類 vanilla 框架瑣事。** 沒有任何一支 script 在做「規模化投放」的決策——投放是宣告式的資料，不是命令式的程式。

