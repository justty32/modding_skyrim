# real-estate — modforge-roadmap

← [調查入口](../real-estate.md)

## ModForge relevance

逐機制對照 ModForge 既有能力（凡「ModForge 不能」都已 grep `src/ModForge.Core/` 核實）：

ModForge relevance的逐列資料。

已抽到 [real-estate-modforge-mapping.json](real-estate-modforge-mapping.json)（11 列）

RE 機制：原表「RE 機制」欄。

ModForge 對應：原表「ModForge 對應」欄。

狀態（核實）：原表「狀態（核實）」欄。

統計：11 列記錄；3 欄。

## Roadmap implications

**1. 最高價值 GAP — 多按鈕 Message-box 選單（MESG menu buttons）。** 已核實 `MessageSpec`（`Spec.Items.cs:42`）只有 `EditorId/Name/Description`，無按鈕欄位。任何「啟動物件→跳選單→依選擇分支」的互動（買/賣、是/否/取消、多選服務）目前只能靠 fragment 手刻或 vanilla MESG override。RE 是這類 UI 的典型代表（22 個 MESG，全是買賣/提示選單）。**建議給 `MessageSpec` 補 `buttons: []`（ITXT/menu-button + 對應 quest stage / fragment 分支）**，並讓 ACTI/Book 的 OnActivate fragment 能讀回 `MenuResult`。這個缺口同時解鎖大量「對話框驅動」mod（不限房產）。

**2. settlements macro 的「ownership / 收益」面（idea #22 的另一半）。** [settlement-npc-expansions](../../systems-population/settlement-npc-expansions.md) 與 [populated-skyrim-family](../../systems-population/populated-skyrim-family.md) 補的是「住滿人 + 店家結構」；RE 補的是**「這個地點屬於誰、產出多少資源」**。`SettlementSpec` 目前無此維度。若 #22 要做「玩家開拓並擁有一個聚落」，可從 RE 借三個原語：(a) **per-asset 計價/收益 GLOB 組** + (b) **被動收益 timer fragment 模板**（`RegisterForUpdateGameTime`→`AddItem(Gold)` 進指定容器）+ (c) **token-replacement 式所有權切換** 或更乾淨的 runtime `SetActorOwner` fragment。這些 ModForge 全能生（GLOB/script-attach/placement 都 landed），缺的是**把它們打包成 `ownership:` / `income:` 宣告層**的便利層——和家族 finding 反覆得到的同一結論（缺量產 sugar，不缺能力）。

**3. 可直接複用的 pattern（無需新支援）：**
- **「腳本化 Activator 告示牌」= 給任意 vanilla 地點掛一個可買/可互動掛鉤**（不改該地點記錄、純 additive 置放一個帶 per-instance 屬性的 ACTI ref）。這是「在既有世界上疊一層玩家系統」最低衝突的做法，[skillTrees](../../../../../projects/ModForge/workflows/feature-dev/landed/world.md) 的 in-world node 已證明 ModForge 完全能生。
- **token Form 當「可替換引用容器」**（`RE_*Replacement` weapons）：讓 script 屬性指向一個佔位 Form、runtime 改其指向——繞過「Papyrus 不能動態建 Form」的限制。值得記入 conventions 當一個可重用招式。
- **「一個 quest instance + InstanceGlobal 當總帳」**（`RE_Quest` + ledger quill）：ModForge 的 `InstanceGlobals` 正是這個 pattern 的一級支援。

**風險 / 相容**：RE override 大量 vanilla cell（122 cell，在每棟可買房外塞告示牌 ref）——與任何也改這些 cell 的 mod（城市重做、JK's、ETaC…）需相容 patch（RE 自帶 USSEP patch 變體即為此）。與 Sofia patch 無交集。

## Verdict

**可借鏡（高，限「玩家側經濟/所有權系統」與 #22 的收益面）**。RE 是 vanilla-only（僅 SkyUI）實作「買房收租」的乾淨範本，機制原語（GLOB 計價、script-attach timer 收租、XOWN/SetActorOwner 所有權、relationship PERK、MCM、教學 quest）**ModForge 幾乎全已 landed**。**唯一硬缺口是 MESG 多按鈕選單**（`MessageSpec` 已核實無按鈕欄位）——這是買賣 UI 的命脈，也是跨多種互動 mod 的通用缺口，建議優先補。內容本身（教學 quest）無敘事價值，只借機制配方。最小垂直切片：1 棟可買房（告示牌 ACTI + OnActivate 多按鈕 MESG + XOWN 切換 + 一個收益 GLOB + timer fragment + MCM 倍率滑桿），驗「能買、會收租、能賣」。
