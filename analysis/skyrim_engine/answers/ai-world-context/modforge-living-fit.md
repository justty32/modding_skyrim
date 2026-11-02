# ModForge／Living：把上下文接到有限玩法的候選

[返回入口](../ai-world-context.md)｜[QA agent 觀測路線](bridge-fit.md)

對照 `ModForge@b60741b09a0301ee425532269a54513993a5d961`。
本篇是研究候選，不是開工計畫；Living 仍依使用者界線，回家參考 FDE Janessa 後再決定。
本輪沒有重開 Sofia 短場景、DSP 或隨從調整，也沒有接 LLM／編 PEX／部署。

## Living 已有基礎，也有明確真缺口

Living 已有持久 actor roster、離場模擬、在場 materialize、favor 對話和 follower handoff。
controller 輪詢每個 alias，分別做 game-time AdvanceSim 與 real-time Presence。
離場 deeds 是 timer 累積的抽象進度，anchor 是循環索引；不是 actor 真的去地牢，也不證明任何人目擊戰鬥。
[controller:23–44](../../../../projects/ModForge/assets/papyrus/MFLivingWorldController.psc)、
[alias:47–70](../../../../projects/ModForge/assets/papyrus/MFLivingNpcAlias.psc)

favor 已由 macro 生成 GLOB 與 TIF SetGlobal；fund／praise +1，parley +5。
但 alias 沒有 Favor／Alignment properties，`AdvanceSim` 仍 `anchorIdx+1`，所以 favor 尚未驅動日常 anchor。
fund 目前只有對話文字與 favor delta，沒有扣金幣。
alignment 只在自製 hostile NPC 設 Aggressive，外部 hostile 明拒；Backstory／Anchor.Kind 是作者資料，
不是 runtime 記憶或活動訊號。
[macro:43–48,138–140,173–196](../../../../projects/ModForge/src/ModForge.Core/Macros/Generator.LivingNpcs.cs)、
[alias:16–33,62–64](../../../../projects/ModForge/assets/papyrus/MFLivingNpcAlias.psc)、
[spec:40–44,63](../../../../projects/ModForge/src/ModForge.Core/Spec/Spec.LivingNpc.cs)

YUA 15/15 與 generic 31/31 已有 runtime 記錄，不能因較舊 design 仍寫 generic 未驗而否定它。
YUA 證的是 vanilla IsPlayerTeammate 契約；其他 follower framework 仍需 adapter。
[Living README:44–50](../../../../projects/ModForge/sub_projs/living-adventurers/README.md)、
[YUA:203–211](../../../../projects/ModForge/sub_projs/living-adventurers/yua-mvp.md)

## 作者、觀測者與狀態 owner 分工

ModForge 負責可 review 的離線 spec→records／Quest／Scene／scripts／package。
既有 Scene presence gates 可處理 combat／dead、距離、可選 player LOS、冷卻與 PlayOnce；
其中 LOS 是玩家看 actor，不是 NPC 目擊世界。
[Scene spec:19–37,95–107](../../../../projects/ModForge/src/ModForge.Core/Spec/Spec.Scene.cs)、
[banter controller:81–117](../../../../projects/ModForge/assets/papyrus/MFSceneBanterController.psc)

runtime observer 負責採集，context builder 負責時間／視角／預算。既有 Living 程式與持久紀錄保有
favor、anchor、movement、recruitment 的權威；新增意圖由相應 controller／對話程式驗證。
AI 最多提出合法 line_id／reaction_id／anchor_id，
不能憑敘事改寫這些權威狀態。StorageWrites／GLOB 是現有儲存原語，不等於已建 episodic memory。
[dialogue storage:93–118](../../../../projects/ModForge/src/ModForge.Core/Spec/Spec.Dialogue.cs)

**正式玩法不可要求 QA bridge 常駐。** agent-bridge 是可移除、不進玩家 load order 的 harness。
日後可以共享資料契約，但 production observer 要由既有玩法 runtime、小型獨立 observer，
或外部 AI mod 的正式 API 承接，需先決定依賴與生命週期。現在也沒有已接好的
外部 LLM→即時 NPC 台詞／TTS 播放通道，文字生成不等於 NPC 已說出。
[agent-bridge AGENTS](../../../../projects/agent-bridge/AGENTS.md)

observed engine event、controller 的 simulated progress、LLM interpretation 應分開。
deeds 不存成 witnessed kill；死亡 snapshot 不證凶手；只有確證的對話／Quest 結果才能觸發權威 favor 改變。
執行時須重查 actor ownership、epoch、combat、條件、冷卻；舊 epoch 意圖作廢，重送不得重複加值，
超時不是成功。這是必要的候選邊界，沒有在此設計通用 RPC 或自治 agent framework。

## 切片 A：一個場景的一句短評

先選一 NPC、一室內 cell、少量參與者，明示 NPC 感知範圍或 system-supplied context，輸出一條預寫短評。
無 LLM 可用條件／variants／Scene；有 LLM 只挑合法 line_id，玩法判定相同。
最小驗收：換 cell、角色離場、讀值不可用時不引用舊人；玩家觀測不冒充 NPC 目擊；沒有新資訊可以不說。

離線資料契約／renderer 成本低；真正 NPC 視角 producer 與語音接線成本中高，需家中實機。
先決選擇是「誰知道這件事」和輸出方式，不是先選模型或全面開放世界掃描。

## 切片 B：對一個確證事件回應一次

以已完成 praise 對話、GLOB 確實增加作事件，先不做戰鬥凶手推斷。
預寫 reaction／topic／rumor 由 event identity、gate、cooldown 去重；LLM 可挑語氣或 reaction，
不能再自行加 favor，也不能將 fund 說成已付金幣。
最小驗收：點選失敗無事件，同 event 重送只回應一次，讀檔 replay policy 明確，combat／recruited gate 保留。

成本低至中。既有 GLOB／StorageWrites／Scene gate 可用；缺的是一致事件身分、receipt 與受限接線，
不是重建整套 NPC agent。公司可擬合成正反例；事件 producer、PEX、save/reload 在家中驗。

## 切片 C：favor 只影響一個離場 anchor 分支

保留現有 anchors，作者指定一個 favor 閾值與兩個合法 anchor；下次 off-screen tick 才由 controller
偏向其中一個。LLM 最多提出已授權 anchor 偏好，不能每次輸出便 MoveTo。
招募期間交給 follower system，dismiss grace、off-screen 收回、combat、冷卻仍須保留。
[ownership／Presence:79–126](../../../../projects/ModForge/assets/papyrus/MFLivingNpcAlias.psc)

最小驗收：閾值兩側、save/reload、超時／非法 anchor／舊 epoch 都有確定 fallback；
recruited 期間零 MoveTo、零抽象 tick。成本中，涉及 macro／validator／script properties／PEX／runtime。
這正是尚未做的 behavior 切片；等回家與 FDE 參考後裁示，不因本輪研究而自動開工。

## 公司與回家各能完成什麼

公司 WSL 可進行契約／合成例、renderer、狀態轉移與重送規則設計、native 條件和 LLM chooser
同輸入比較；這次只研究，尚未新增 fixtures 或產品程式。
家中才驗真 observer／witness、DLL producer、PEX、台詞播放、存讀檔、招募／dismiss ownership，
以及玩家眼前不瞬移。三切片都不需要先耦合技能框架或讀改私有能力池。
