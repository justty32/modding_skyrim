# honed-metal — services-mechanism

← [調查入口](../honed-metal.md)

## Classification

- 類型：**服務型框架 mod（含原生 SKSE DLL）**，非 record-edit mod。
- 敘事價值：**無**（純機制，對白重用原版語音）。
- 系統價值：**中高**（對 ModForge）——浮現「服務對話開原生製作選單」「付錢→給/改物件」兩個可重用 primitive；但核心是 bespoke runtime（見 §3）。

## 1. 它做什麼

玩家付錢請原版（與 modded）NPC 鐵匠/附魔師代工，而非自己做：**鐵匠打造+強化武防；附魔師附魔+充能物件**。NPC 能做什麼、收多少，隨 **NPC 的 smithing/enchanting 技能等級**（決定其等效 perk + 可處理的裝備 tier）+ **玩家 barter + 經濟設定**。⚠UNVERIFIED：後期版本把成本**更偏 NPC 技能、較不偏物件價值**，材料成本另加。材料：**NPC 用自己的材料、可花時間/金幣取得缺的常見材料**，但**稀有材料（如龍骨）玩家須自備**。明確**支援 mod 新增的武防**。可選「Skill Based Smithing」讓成品數值隨 NPC 技能加成。預設把若干 lore NPC（Eorlund、Neloth、Baldor 等）設為大師匠人。

## 2. 機制 / 怎麼實作

**框架/腳本驅動 + 原生 SKSE DLL**：

<!-- wf-nav -->
- **SKSE C++ DLL（核心）**：新版出 **per-runtime C++ DLL**，選錯版本啟動即 SKSE 報錯（另有社群 repack）。**另有「最後一個無 SKSE plugin 的版本」**（純 Papyrus fallback、號稱任何遊戲版本可跑）——證明 DLL 加能力但歷史上存在 Papyrus 路徑。config 在 `Data/SKSE/plugins/HonedMetal.ini`（perk-ID 黑名單，避免 perk-overhaul 干擾）。⚠UNVERIFIED：DLL 與 Papyrus 的確切分工（讀不到 C++ 源碼）。
- **硬依賴：SkyUI（或 SkyAway）+ 對版 SKSE**。MCM ⇒ SkyUI MCM 框架。**無證據**依賴 PapyrusUtil / ConsoleUtil / JContainers / SPID——**勿假設**。
- **物品發現靠 FormList + 原版 perk/COBJ 系統**：可用材料存在 **plugin 內的 FormList**（一個常見：礦/錠/充魂石；一個稀有/違禁）。用「掛在遊戲 perk 樹上的 smithing/enchanting perk」判斷 NPC 能做什麼與 tier。⚠UNVERIFIED：可製作物品到底是從原版 **COBJ** 配方列舉，還是純 keyword/FormList 成員——只證實「材料用 FormList、能力用 perk-gate」，未證實成品列舉路徑。
- **對話是真 dialogue 記錄、非 SPID**：mod **對匠人 NPC 加了新 topic/response**，**重用原版語音**（移除自帶語音、指向既有音檔、隨機挑；伴隨 mod「Voice Tweak」修字幕/voicetype 不符）。把 NPC 變匠人靠 **faction 成員**——MCM 有「Add NPC to Smithing/Enchanting Faction」，對話條件幾乎必 gate 在這些 faction。⚠UNVERIFIED：附掛機制（quest alias vs 共用 info 條件在 faction）——faction-driven 模型已證實。
- **互動流程（最吃重的 bespoke 部分）**：附魔：對話「能幫我附魔嗎？」→ **開容器/轉移視窗**（玩家放入物件 + 可選充魂石）→ 關閉後**腳本以程式開啟原版附魔選單**，玩家像自己附魔般選。**「開容器→腳本開原生製作選單」是核心 trick，最可能由 SKSE DLL 撐**。MCM「NPCs Have Materials」切換 NPC 是否供應充魂石。
- **軟依賴/patch**：伴隨 mod（Additional Materials、CCOR/CCOR patch、FLM patch、翻譯）擴充材料 FormList——即**擴充性靠改 FormList**，本身是有用的 pattern。

