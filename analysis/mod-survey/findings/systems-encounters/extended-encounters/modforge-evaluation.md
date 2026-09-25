# 3. 對 ModForge 的參考價值

← [原文入口](../extended-encounters.md)

## 3. 對 ModForge 的參考價值

### 可生成（ModForge 已有對應支援）

<!-- wf-nav -->
- **掛 SM 事件的骨架 quest**：`QuestStoryEventSpec`（`Spec.StoryManager.cs`，`event` + `conditions` + `keyword`）已能把一顆 quest 接到 vanilla SM event root，這正是 EE 每顆遭遇 quest 的型態。✅
- **AI package（vanilla template 包裝）**：`Spec.Packages.cs` / `Spec.Packages.Templates.cs` 已支援 `Template` + Travel/Sandbox/Patrol/Follow/Escort/Eat/UseItemAt 等 data input（指向 placed ref 或 in-spec placement）。EE 的 Orbit/Travel/Sandbox/Scavenge 大多落在這套裡。✅（cf. memory `scene-playidle-recipe`/package 系列）
- **LeveledNpc / LeveledItem**：`LeveledNpcSpec`/`LeveledItemSpec`（`Spec.Items.cs`）已支援 chanceNone + 權重 entries；spawn 也能吃 LVLN 當 base（`Spec.World.cs`）。EE 的「random enemy」可直接表達。✅
- **ReferenceAlias + fill + 條件 + alias 腳本**：`QuestAliasSpec`（`Fill`、`Conditions`、`Script`/`ScriptSource`/`ScriptProperties`）已能描述 EE 的演員/marker alias 與其腳本。✅
- **Outfit / Faction / Message / Activator / 自製 NPC**：全是 ModForge 既有 record 路線。✅

### 需新支援（缺口）

<!-- wf-nav -->
- **獨立 SM branch/quest-node 樹**：ModForge 目前是「quest 自己宣告 storyEvent」掛到 vanilla root；EE 卻自建 `StoryManagerBranchNode` + 30 個 `StoryManagerQuestNode`，**依 location-type keyword 分流、底下掛一票候選 quest 做加權隨機選擇**。要生成這種「多候選 + 條件路由」的 SM 子樹，需要新的 spec（branch/node 結構 + 候選 quest 清單 + 各自條件/權重）。⚠️ 需確認 `Generator.Build.StoryManager.cs` 目前能生到哪一層（branch node? 多 quest 候選?）— 這是最大缺口。
- **navmesh-tester 動態 spawn helper**：EE 的「拋棄式 actor `MoveTo` 隨機偏移 → `EnableAI` 吸 navmesh → marker 跟隨 → delete」是一段可重用的 Papyrus 樣板。ModForge 目前偏向預擺 placement（cf. memory `programmatic-navmesh`、`refpos`）；若要做「玩家附近隨機生成」這類遭遇，值得把這段做成可生成的 alias-script 樣板（搭配隱形 marker alias 自動生成）。⚠️
- **「一個 quest = 多 alias marker（trigger/scene1..4/center）」的成組 alias 樣板**：可生成，但目前要手寫每個 alias；值得一個 high-level「encounter scaffold」糖衣自動鋪 marker alias + cleanup 腳本。⚠️

### 純參考（設計觀念，不必生成）

- **「marker + MoveTo + delete，不預擺 cell」的零-bloat 哲學**：解釋了為何隨機遭遇不該往 cell 塞 placement。
- **EditorID 即路由表的命名法**（`EE_WI_LocType*` / `EE_LI_LocType*`）：對 AI-agent 友善的 spec 命名值得借鏡。
- **GlobalShort 開關 + MCM gate 模式**：每 feature 一個 global toggle，Papyrus 丟 story event 前先檢查。
- **「骨架 quest（無 objective/log）純當 SM 容器」**：提醒 ModForge 的 SM quest 不一定要有任務日誌。

### 相關既有筆記

- memory `story-manager-kill-recipe`：SMBN additive-parent vanilla root — EE 的三條 branch 用同一招。
- memory `programmatic-navmesh` / `refpos`：與 EE 的 navmesh-tester 動態定位互補（一個是預擺，一個是 runtime 找點）。
- package 系列（`dispatcher-magic-trigger`、`scene-playidle-recipe`）：EE 證明大量遭遇可以**只靠 package 不靠 scene/dialogue** 跑起來。
- memory `sm-quest-journal-progression`：EE 反例 — 它的 SM quest 刻意**不**進日誌（無 startUpStage objective）。

---

### TL;DR

機制 = **vanilla SM event root → EE 自建 branch/quest-node 樹（依 location keyword 路由 + 加權隨機選候選 quest）→ 骨架 quest 跑 QF fragment：用拋棄式 NavmeshTester actor `MoveTo` 玩家附近吸 navmesh 找合法點 → 把隱形 marker alias 移過去、依 alias fill 演員（含 LeveledNpc）→ 綁 vanilla-template AI package 演出 → 走遠即 delete 歸零**。對 ModForge：SM 事件掛載 / package / LeveledNpc / alias 都已可生成；最大缺口是「多候選 + keyword 路由的獨立 SM branch/quest-node 子樹生成」與「navmesh-tester 動態 spawn Papyrus 樣板」，前者建議當下一個功能優先評估。
