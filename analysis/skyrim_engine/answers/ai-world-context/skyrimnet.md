# SkyrimNet：可核的是介面與模板，native 採集仍是黑箱

[返回入口](../ai-world-context.md)｜[欄位與證據矩陣](skyrimnet-fields.json)

基線：官方 `MinLL/SkyrimNet-GamePlugin@0194eeb1c09bab423601c2fb7a8abf1df59fd15b`，
2026-11-01。本輪沒有載入 DLL 或實機驗證。矩陣有 22 組，欄位為 id、fields、producer、
source_position、limits、source_link、evidence；逐組記錄公開消費欄位、證據層級與未知。

## 資料流與可核範圍

官方明寫 DLL 在別處建置，此 repo 沒有 C++ producer。可核 Papyrus API、decorator 文件與
Inja templates；無法核 `RE::*` 讀法、game-thread 保證、一次 snapshot 一致性、採樣頻率、
cache invalidation 或 reference validity。舊文「decorator 每次即時直接讀記憶體、沒有中間層」
超出公開證據。[CONTRIBUTING:16–29](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/CONTRIBUTING.md#L16-L29)

公開鏈是 `system_head` → `get_scene_context(npc.UUID,target.UUID,"full")` → scene component →
nearby UUID／`decnpc(UUID)`／distance／location → short profile 與文字。
本版 Scene Information 的 situationSummary 由 location、gameTime、hour 固定組裝；
另有 GM scene planner，不能混稱所有場景摘要均由 LLM 生成。
[scene_context:1–58](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/plugins/skyrimnet/base/prompts/components/context/scene_context.prompt#L1-L58)

## 附近、可見與觀察者不同

nearby 表以 sourceEntity 為中心，沒有 source 才用 player；但 NPC state summary 重新以 player
為中心，室內／室外天氣措辭條件也使用 player 的 `is_indoors`。同一 prompt 因而可能混合視角。
`get_nearby_npc_list` 文件只有「最大互動距離內」，未給 radius、排序、cap、cell 或 LOS 規則。
`FindActorByName` 的 4000 units 不能據此推定為 nearby 半徑；測試模板的 20／10 人 loop 是顯示上限，
不是 native 掃描上限。
[nearby API docs:4060–4090](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/SKSE/Plugins/SkyrimNet/docs/decorators.html#L4060-L4090)、
[state summary:1–8](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/plugins/skyrimnet/base/prompts/components/context/component_npc_state_summary.prompt#L1-L8)

另有 LOS／visible-list 介面，但不能由其存在推定預設 nearby prompt 已使用它。
OmniSight 將 player 可見人物表與 screenshot 交給 vision model，產生環境／人物敘述；
這是另一條模型推論鏈，更新和過期契約在公開資產中不完整。
[OmniSight:10–80](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/plugins/skyrimnet/base/prompts/omnisight/describe_scene.prompt#L10-L80)

## 行為文字不是活動真值

`component_npc_state_summary` 取家具英文名稱 lower-case 後比對 substring。
bed／bedroll 只輸出躺著；forge、anvil、grindstone、tanning rack、smelter 都描述成磨劍；
shrine／statue 變祈禱。這不是睡眠、工作 package 或動畫觀測，受名稱與本地化影響。
`isFollowing`、unconscious、mount 等是 native 提供值，其 producer 讀法仍未知。
[推論規則:7–62](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/plugins/skyrimnet/base/prompts/components/context/component_npc_state_summary.prompt#L7-L62)

physical-activity 模板在所有旗標皆不符時輸出能正常站立，沒有 unknown 分支；不能反過來當成健康或
站姿的證明。scene 中的非敵對 summoned creature 被描述成服務玩家，也未核召喚 owner。
[physical activity:1–33](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/plugins/skyrimnet/base/prompts/submodules/character_bio/0050_physical_activity.prompt#L1-L33)

## 事件、歷史與快取

短期事件由 eventId 與 ttlMs 管理，同 key 可更新；MinAI bridge 將秒轉毫秒，ttl≤0 以 100ms 清除。
Recent Events 消費 `scene.short_lived_events`；持久 history 是另一集合，history 模板才排除
spell／hit／combat。API／event catalog 是公開契約，native event sinks 不在此 repo；
持久 history 也會接受 mod 注入、dialogue、thought、narration，不能全稱引擎實測。
[API:72–82](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/Source/Scripts/SkyrimNetApi.psc#L72-L82)、
[MinAI bridge:52–100](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/Source/Scripts/skynet_MinAIBridge.psc#L52-L100)

history 以 gameTime 差產生相對時間；「半小時前」等門檻是顯示標籤，不是保留期限。
prompt 將穩定 persona／格式／actions 放前面，再放 history 和每回合 dynamic context，
並用 event-ID anchor 減少 prefix cache 失效；這是模型供應商的 prompt cache，
不證明引擎狀態 cache。另有最近 5 則對話重述；公開模板未給完整 tokenizer／全域 token budget。
[dialogue_response:1–68](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/plugins/skyrimnet/base/prompts/dialogue_response.prompt#L1-L68)、
[history:1–72](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/plugins/skyrimnet/base/prompts/components/event_history.prompt#L1-L72)

## identity、缺值與對外讀取

`GetEntityUUID(actor)` 文件定義 invalid actor 回空字串；虛擬 NPC 另有跨 session 穩定 UUID 保證。
不能將後者外推到實體 actor 的 respawn／reset／dynamic ref。`decnpc` 在 invalid／unloaded
時的完整輸出、缺欄位和保留舊值規則仍未知。Named Places 可按同 interior cell／worldspace、
半徑及垂直範圍加上策展地點名稱，是額外語義層。
[UUID API:404–409](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/Source/Scripts/SkyrimNetApi.psc#L404-L409)、
[Named Places:999–1009](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/Source/Scripts/SkyrimNetApi.psc#L999-L1009)

官方現有 MCP port 8889，具名讀取包括 `get_player_info`、`get_nearby_actors`、
`get_quest_property_value`、`get_monitored_events`、`get_decorators`，並列 full prompt render。
這修正舊文「只有 Mantella 有文件化對外介面」的時效；本輪未實測 server handlers。
同服務也有 console／`execute_quest_function` 等寫入，沒有公開可核的唯讀 scope／ACL 契約。
任意 prompt render 也可能呼叫可擴充 decorators，不能一概視為純讀。
[具名工具:411–444](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/docs/modding/WORKFLOW_MOD_INTEGRATION.md#L411-L444)、
[MCP overview:197–209](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/docs/FEATURES.md#L197-L209)

可借鏡視角、事件壽命、render modes 與歷史窗口；獨立採集器不能抽出這份 repo 未公開的 native。
base templates 授權限制其用於其他軟體，API script 另有 MIT notice；本研究借設計，不直接移植模板。
[LICENSE:9–37](https://github.com/MinLL/SkyrimNet-GamePlugin/blob/0194eeb1c09bab423601c2fb7a8abf1df59fd15b/LICENSE#L9-L37)
