# 系統／機制型 · 自建據點與經營經濟

← [mod-survey](README.md)｜[survey index](index.md)

逐 mod 機制拆解 + 對 ModForge 的「可生成 / 需新支援 / 純參考」標記。共通缺口已彙整進 [roadmap](../../projects/ModForge/workflows/roadmap/README.md)「mod-survey 浮現的 record/生成缺口」。

<!-- wf-nav -->

| Mod | Finding | 機制重點 | ModForge 缺口 |
| --- | --- | --- | --- |
| **Tundra Defense SSE（Nexus 14310 v1.04）** ⭐#22 build/manage/defend | [findings/tundra-defense.md](findings/tundra-defense.md) | `Tundra Defense SSE.esp`（Skyrim.esm-only，BSA 含 56 `.pex`，**無 .psc**，需 SKSE） | 無（系統 pattern 最高，直指 #22 核心） | **自建據點＋募兵＋波次守城**唯一完整藍圖：建材＝Ingestible(potion)→script-MGEF"Construct X"→spawner `PlaceAtMe`→`aaaFortMainQuestScript` 定位狀態機；募兵＝程序化 `PlaceActorAtMe`+faction+teammate；守城＝`aaaFortPlayerQuestScript` 的 MESG 選單+OnUpdate spawn `Raider*` base at boundary markers；UI＝87 MESG（**無 MCM**）；狀態＝quest-script property（**0 GLOB**）。**已驗證**：全部靜態零件（ALCH/MGEF/ACTI/FACT/LVLN/NPC/PACK/KYWD/BOOK/SHOU/SPEL）可生 + `scriptAttach`（反射式，`Generator.Build.Scripts.cs` 已驗）能掛回 controller `.pex`；**兩硬缺口＝① MESG 無多按鈕選單（`MessageSpec` `Spec.Items.cs:42` 缺欄，同 Real Estate）② 整套執行期玩法（定位/raid/募兵/持久化）irreducibly bespoke Papyrus，須隨附 controller `.pex`**。`settlements:` Phase-2 要新增 `buildables:`/`defense:`/`recruitment:`/`manageMenu:` 原語（多 needs-controller+內建泛用 placement/raid controller `.pex`）|
| **AnnoRim（Nexus 159600 v1.2）** ⭐#22/#24 build/economy | [findings/annorim.md](findings/annorim.md) | `AnnoRim.esp`（Skyrim+4DLC + `Sailable Ship.esm`；**無 SKSE/PapyrusUtil/JContainers/MCM/BSA**，45 `.psc` 全附源碼，~900MB loose 資產） | 無（經濟/經營 pattern 高，直指 #22/#24） | **Anno 式海島殖民經營**，純 vanilla-Papyrus 手搓：**建造＝設計期預置 disabled 物件掛 enable-parent XMarker + activator script 檢查/扣 MiscObject 資源→`Enable()` 目標→`Disable()` self（切可見性、非 runtime PlaceAtMe）**＝**#24 快照該吐的 placement 產物格式最直接先例**；經濟全走真實 inventory（`ANNOSurplusContainerDynamic` 12h 產出 / `ANNORespawnContainerScript` 補貨 / `ANNOTaxScript` 7 天發金收租 / `ANNOTokenExchangeScript` keyword→token 貨幣 / `ANNOMasterContainerManager` 16×128 Form[] chunk 手搓倉庫聚合，**無 JContainers**）；海運貿易＝Sailable-Ship 船沿 HarborMarker 航點操舵賣貨 + `ANNORaidSystem`（GLOB×RiskMult 擲骰三級損失）；自訂 `AzurianSea` worldspace。**與 Tundra Defense 互補（和平經濟 vs 守城）**，給 #22 補 `buildables:`/`production:`/`tax:`/`currency:` 原語。缺口＝已知的 `MessageSpec` buttons[]（建造 Yes/No）+ 執行期迴圈須附 controller `.pex`，**無新缺口** |
