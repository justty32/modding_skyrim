# honed-metal — modforge-roadmap

← [調查入口](../honed-metal.md)

## 3. 對 ModForge 的意義

「付費請 NPC 代工」**部分可表達**，但核心是 bespoke runtime。

**乾淨對應既有功能**：
- **faction-gate 服務對話**——ModForge 已會對原版 NPC 注入對話（quest+alias+INFO 條件）+ **vendor faction**。「加 NPC 進匠人 faction → 條件對話 topic」正是 vendor/dialogue pattern；剛落地的 `settlements:` 概念相鄰（大量 faction-tag NPC）。
- **MCM**——ModForge 生 MCM（memory `mcm-helper-registration-recipe`）。切換/技能滑桿可生。
- **FormList**——ModForge 能出 FormList + FLM 分發；材料清單擴充模型契合。
- **付錢交易 + 訊息框**——有 message box / GLOB / Papyrus fragment；「扣金幣→給/強化物件」fragment 可達。
- **Storage**——JContainers/PapyrusUtil KV（已實機確認）可存 per-NPC 技能/材料狀態。

**不對應——須手寫 `.pex`（或 ModForge 產不出的 DLL）**：
- **轉移容器後腳本開原生附魔/打造選單**——引擎級（HM 用 C++ SKSE DLL）。**ModForge 產不出 C++ SKSE plugin**；只能附帶預寫 DLL，或找純 Papyrus 等價（舊版無 DLL 暗示有 Papyrus 路徑但較受限）。
- **成本公式**（物件值 × NPC 技能 × barter × 材料）——非平凡 bespoke Papyrus controller。
- **perk 驅動能力 gating** + runtime 讀原版 COBJ/perk 樹判可製作性——bespoke。
- **容器轉移 UX + 強化/充能套用**——bespoke fragment。

**誠實結論**：ModForge 能生**外殼**（faction、條件服務對話、MCM、FormList、訊息框、扣金幣 fragment、storage）。**controller**（開選單、成本數學、perk/技能 gating、強化/附魔套用）是**大量手寫 Papyrus controller**，原生選單 trick 還可能要 ModForge 以 asset 出貨**預建 SKSE DLL**。即：scaffolding 可生成、brain 須 bespoke。

## 4. Roadmap 意涵

<!-- wf-nav -->
1. **「服務對話開原生製作/物品選單」**——高價值新 primitive：fragment 開容器轉移 +/或原生選單。HM 證實需求也證實它要 SKSE-DLL 肌肉 → 標「**需附帶 helper .pex/.dll asset**」，非純生成。與 vendor 成對（vendor 開 barter；此開 craft）。
2. **付錢→給/改物件交易 pattern**——通用 fragment 模板：`Player.GetGoldAmount() ≥ cost` → 扣金幣 → 給/強化/附魔目標。可重用於 vendor/服務/賄賂。乾淨的可生成 macro 候選。
3. **FormList 驅動的物品/材料發現 + 擴充性**——HM「兩個 FormList（常見/稀有）+ FLM/CCOR patch 擴充」是 ModForge 已有記錄（FormList + FLM 分發）的 pattern。值得寫成 spec idiom：*能力清單即 FormList、由分發擴充*。
4. **faction-tag NPC 開服務**——直接重用 vendor-faction + dialogue-condition + 新 `settlements:`。一個 `services:` macro（鐵匠/附魔/訓練）把 NPC tag 進服務 faction + 自動接條件對話，是 `settlements:` 的天然下一個姊妹。
5. **技能/perk-gate 行為**——記為缺口：ModForge 有 GLOB/perk，但「服務品質隨 NPC 技能」要 Papyrus controller 讀 actor 技能——多半是附帶 helper 而非生成。

**淨結論**：scaffolding（對話+faction+FormList+MCM+金幣交易 fragment+storage）可生成；**原生選單-from-對話 + 成本/技能 controller 是真缺口**，傾向做一小套**預寫「服務 controller」.pex/.dll asset** 讓 ModForge 接線，而非生成那段邏輯。

---

### 來源
- https://www.skyrimodding.com/honed-metal-npc-crafting-and-enchanting-services/（已抓，Nexus 描述鏡像，主來源）
- https://www.nexusmods.com/skyrimspecialedition/mods/61015（SE 頁；403，靠搜尋摘要）
- https://www.nexusmods.com/skyrim/mods/51024（LE 頁；摘要）
- https://stepmodifications.org/wiki/SkyrimLE:Honed_Metal_-NPC_Crafting_and_Enchanting_services（摘要）
- https://www.nexusmods.com/skyrimspecialedition/mods/51254（Additional Materials — FormList 機制）
- https://www.nexusmods.com/skyrimspecialedition/mods/34393（Voice Tweak — 對話/語音機制）

**未能完全證實**：成本公式權重；可製作物品來自 COBJ 列舉 vs FormList/keyword；對話附掛機制（alias vs faction 條件共用 info）；DLL 與 Papyrus 確切分工；任何 FormID/腳本/MCM 選項識別符（皆未捏造）。
