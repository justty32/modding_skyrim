# Sofia Follower v2.51 — design-and-modforge

[返回入口](../sofia-follower.md)

## 關鍵設計

<!-- wf-nav -->
- **微服務式 quest 拆分**：一個職責一個 quest（30 個），換取獨立 start/stop 的可控性與救援能力（readme 全靠 `stopquest`/`startquest` 粒度排錯）。
- **批次模板化 comment**：8 組 `*Comment`+`*SayComment` 結構同構、只換目標 actor 與台詞——典型「同一份模板複製 N 份」需求。
- **scene = phase 序列 + 三種 action**：Dialog（念台詞）/ Package（走位、施法）/ Timer（停頓），actor 用 alias 索引、帶 DeathEnd/CombatEnd/DialoguePause 三旗標確保可中斷不卡死；單 actor 線性獨白與多 actor 對拍（婚禮）共用同一機制。
- **GLOB 萬用化**：設定、狀態、技能鏡像、裝備分類、甚至暫存變數全用 GLOB——因為只有一個隨從，不需要 per-actor 狀態表，這是「不掛 JContainers 也夠用」的根因。
- **vanilla template 覆寫**：54 個 package 全 `template=Skyrim.esm:...`，戰鬥風格用 FormList+GLOB index 在 runtime 切換而非重建 record。
- **SKSE 為選配**：核心功能零 SKSE 依賴，MCM 才需要；`JJSofiaGetHasSKSE` 在 runtime 探測並降級。

## 對 ModForge 的意義

ModForge（`projects/ModForge`）已有 QuestSpec / SceneSpec / ScenePhaseSpec（Dialog/Package/Timer action）/ NpcSpec / GlobalSpec / RelationshipSpec / PACK templates / AutoStart 在場偵測。對照 Sofia 的真實做法：

### ModForge 已對齊的
<!-- wf-nav -->
- **Scene 結構**：Sofia 的 scene 正是 ModForge SceneSpec/ScenePhaseSpec 的形狀——phase 序列、每 phase 一個 Dialog/Package/Timer action（ModForge `SceneAction.TypeEnum` 恰好就這三種，見 ModForge CLAUDE.md 鐵律），actor alias + DeathEnd/CombatEnd/DialoguePause behavior flags。Sofia 的 `JJSofiaMainQuestDialogueScene`（17 phase 線性獨白）幾乎可一對一用 ModForge ScenePhaseSpec 重建。
- **comment scene 的 BeginOnQuestStart/StopQuestOnEnd**：對應 ModForge scene `Conditions.beginOnQuestStart`。
- **Package 走位 action**：對應 ModForge scene 的 Package action 引用 `packages[]` 的 PACK。
- **GlobalSpec**：Sofia 的 57 個 GLOB 正是 ModForge GlobalSpec（short/long/float）的目標用例。
- **NpcSpec**：race/class/voice/combatStyle/aiData/perk/essential-protected 都已涵蓋。
- **RelationshipSpec**：ModForge 已有 Parent/Child/Rank（`Spec.Actors.cs`），對應 Sofia 的 3 個 RELA（隨從對玩家固定 Ally）。
- **uniqueActor alias fill**：Sofia 的 comment quest 用 `uniqueActor -> Skyrim.esm:NPC` 指向 vanilla NPC，對應 ModForge 的 `uniqueActor:<ref>` alias fill。

### Sofia 用了、ModForge 目前沒有的
<!-- wf-nav -->
1. **MCM 設定選單（SkyUI）**：`JJSofiaMCM`（SofiaMCMscript 26 prop）+ `JJSofiaGetHasSKSE` 降級偵測。ModForge 無 MCM 生成；隨從類 mod 的「使用者可調設定」幾乎都靠 MCM，這是最大缺口。要做需生成 MCM Papyrus + config schema + SKSE 探測降級。
2. **DialogView record**：CK 編輯用的對話視圖聚合（9 個）。ModForge 直接生 quest/branch/topic，不產 DLVW；對 in-game 無影響，但若要讓產物在 CK 裡可維護，缺這層。
3. **多 actor 對拍 scene**：婚禮 scene（3 actor / 20 phase，Dialog+Package 交錯）。ModForge SceneSpec 目前以單/少 actor 為主，需確認多 alias actor + phase>action（純等待 phase）的支援程度。
4. **批次 per-NPC comment 生成**：Sofia 手刻 8 組同構 comment（quest+scene+alias+對白）。ModForge 缺「給一份模板 + 一張目標 NPC 清單 → 批次展開 N 組 quest/scene」的生成器。這是把 Sofia 模式自動化的明確機會。
5. **戰鬥風格 runtime 切換矩陣**：FormList（CombatStyle 集合）+ GLOB index + 一大群成對 CombatOverride package。ModForge 有 PACK templates 但無「FormList + 切換 index」這種 runtime 多態 package 的高階抽象。
6. **VoiceType 自訂 + voice asset 管線**：Sofia 自訂 4 個 VoiceType 並在 BSA 帶 .fuz。ModForge 的 voice-gen interface 仍是 deferred plan（見 MEMORY voice-gen-interface-future）。
7. **救援用的 quest 粒度約定**：Sofia 刻意把功能拆成可單獨 stopquest 的 quest。ModForge QuestSpec 可生多 quest，但沒有「為 runtime 排錯而拆分」這個設計指引。

### 務實結論
Sofia 證明「不掛 JContainers，純用 GLOB + quest stage + script property」足以撐起一個成熟單體隨從——這對 ModForge 是好消息：**預設不需要 native 依賴**就能生成像樣的隨從。JContainers 的 per-actor 狀態表只在「多隨從 / 每 NPC 各自狀態」時才必要（見 `jcontainers.md` 與 `others/modforge-relevance.md`）。ModForge 若要瞄準隨從這個品類，**優先補的是 MCM 生成與批次 per-NPC comment 展開**，而非資料結構持久化。
