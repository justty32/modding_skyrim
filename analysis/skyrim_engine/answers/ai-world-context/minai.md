# MinAI：模組 provider 與 context builders，要分清後端

[返回入口](../ai-world-context.md)｜[欄位矩陣](minai-fields.json)

本輪官方 `MinLL/MinAI` 與 raw README 回 404，clone 回 Repository not found。
這只證明當下不可公開取得，不能推定刪除、private、archived 或棄用。
以下實碼來自公開延續 fork **`id1001-gthb/MinAI_1001@8ecb144e12033966f410b250597a77ffa9198751`**
（2026-07-15，main2patch／stable1001）；不能回推 MinLL 原版 release，也不是 runtime 驗證。
[fork README:1–9](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/README.md#L1-L9)

## 兩條出口不等價

CHIM 路徑是 Papyrus modules → `AIFF.SetContext` → `SetActorVariable` 字串 payload →
外部 AIAgentFunctions native → PHP 的 conf_opts／eventlog → context builders → system prompt。
它依賴 AIAgent、JContainers、PO3 和 server hooks，不是獨立無依賴的純 Papyrus AI。
Papyrus provider 排程是硬編排；可註冊 callback 的 registry 在 PHP prompt builder 端。
[AIFF:375–512](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_AIFF.psc#L375-L512)

Mantella adapter 主要是 `AddInGameEvent` 文字注入，不會自動搬運全部 actor kv／PHP builders。
只有 Mantella 時 scoped persistent context 降級成不持久 event，TTL／NPC scope 語義不等價。
此處 CHIM 指 AI 對話框架，與 `mojibake-dev/chim` 插件／存檔工具無關。
[adapter:18–46](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_Mantella.psc#L18-L46)、
[fallback:359–395](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_MainQuestController.psc#L359-L395)

## 位置實際以玩家為中心

`SetLocationData(actor whoCares)` 忽略參數，固定讀 player，輸出 currentLocation／currentHold／
currentWorldspace／currentCell／isInterior／isTrespassing／locationKeywords。
它由 Maintenance 和玩家 OnLocationChange 呼叫，不在每 actor SetContext 更新。
GetCurrentLocation 失敗時掃 cell 前 20 references，再查腳下物件，後兩者是代理推論；
`currentHold` 只取一次 parent，未確認 hold keyword，失敗還刻意保留上值。
[location:395–460](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_EnvironmentalAwareness.psc#L395-L460)、
[location event:128–135](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_PlayerScript.psc#L128-L135)

LocType keywords 是 records 分類，不能當視覺地圖；PHP 的 location fallback 和室內免風雨措辭
又是另一層詮釋。producer 採過欄位，不表示 builder 一定輸出；完整 consumer 證據見矩陣。

## 環境、actor 與附近集合

玩家刷新有 dayState、weatherClassification、moonPhase、moonCount、isNight。
時間段／月相／月亮數是日曆算式，不是確認天空能見月亮；weather classification 才是引擎分類。
Frostfall 可讀溫度、wetness、exposure、shelter、warmth／coverage，先在 Papyrus 轉成級距文字。
缺 mod 時不寫值，未見統一清除舊值；固定 FormID／script API 也不保證版本全相容。
PHP 另需 `hasFrostfall` gate，本 fork 找不到其 producer，故不能保證採值就自動進 prompt。
[environment:247–392](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_EnvironmentalAwareness.psc#L247-L392)、
[Frostfall gate:464–522](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/minai_plugin/contextbuilders/context_modules/environmental_context.php#L464-L522)

NPC 直接讀 bribed／intimidated／對玩家 relationship rank／child／family／sleep state／class；
所有 actor 有 level、sneak、swim、mount、encumbrance、sit state。
career=class name 不表示當下正在工作。CombatManager 的 inCombat 是 GetCombatState≥1；
vitals 的所謂 max 實際是 base actor value。裝備 provider 位於 Arousal 模組，收 worn forms、
plugin／FormID／slot masks／keywords，並非所有高頻刷新都更新。
[actor fields:267–317](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_EnvironmentalAwareness.psc#L267-L317)、
[combat:63–125](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_CombatManager.psc#L63-L125)、
[equipment:542–581](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_Arousal.psc#L542-L581)

附近資料有兩層。Papyrus 取 AI framework 已管理 agents，MinAI 自身未定 radius／LOS。
PHP 再從最新 infonpc event 取名字集合，沒有 age cutoff，合併 party／speaker／player／target，
按不分大小寫名稱去重，再查角色狀態。它不是全 loaded actors 的精確距離快照，同名也可能合流。
[Papyrus:734–751](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_AIFF.psc#L734-L751)、
[server source:1064–1112](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/minai_plugin/util.php#L1064-L1112)

## 更新、cache 與 TTL

NPC ContextEffect 首更帶 jitter，預設每次處理完成後再等 30 real seconds；玩家預設 5 秒。
SetContext 每次更新 environment／combat，medium／low tier 門檻卻用遊戲時間差換算秒，
不能把 15／30 當 real-time TTL。mutex／updateTracker 用 actor name，不是唯一 ID；
field 逐條寫，沒有整組 timestamp／transaction，可能混不同更新批次。
[effect:13–104](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_ContextEffect.psc#L13-L104)、
[tiers:391–475](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/Scripts/Source/minai_AIFF.psc#L391-L475)

actor kv 保留直到覆寫，無 TTL；PHP request cache 找不到值回空字串，IsEnabled 只認字串 true，
missing 與 false 因而混合。合法 moonPhase=0 還會被 PHP empty guard 擋掉，說明零值不可當未知。
StoreContext 是另一張 custom_context：expiresAt=server time＋ttl，查詢要求 expiresAt>now。
**此 fork 的 TTL 0 立即到期**，不是永久；key 是 modName＋eventKey，不含 npcName，跨 NPC 可覆蓋。
舊文未釘原版 commit，不能由此判歷史原版當時行為。
[TTL upsert:277–298](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/minai_plugin/customintegrations.php#L277-L298)、
[TTL query:1107–1148](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/minai_plugin/contextbuilders/context_modules/character_context.php#L1107-L1148)

## 從 provider 到 prompt 的可借部分

PHP builder registry 有 section／priority／enabled／callback，依設定過濾、排序並略過空輸出；
角色 sections 與共享 environment 分開。priority 是順序，不證明 token budget／距離 top-N。
這條路沒有通用 provenance／unknown／observed_at，外來 mod 文字也會混入敘事。
[filter/sort:183–217](https://github.com/id1001-gthb/MinAI_1001/blob/8ecb144e12033966f410b250597a77ffa9198751/minai_plugin/contextbuilders/system_prompt_context.php#L183-L217)

可借 provider／renderer 分離、分頻＋jitter、具 key／TTL 的短效 context、裝備識別保留 plugin。
不要照搬 name-string bus、時鐘混用或 getter 副作用。GetNearbyAIStr 可 TrackContext／改 AI 設定，
ContextEffect／SetContext 亦可能調 follow／animation 狀態；整套不是純讀 observer。
採其設計須另拆採集與執行；採其 runtime 則承擔 CHIM/native／PHP DB／可選 mods 的耦合。
