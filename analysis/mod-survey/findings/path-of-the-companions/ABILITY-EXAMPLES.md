# 三個既有能力的最小切面

此處是理解擴充邊界的例證，不是已選定的新技能，也不是實作清單已獲批准。所有FWM行號基於 `971b8b5aba0c34c649e70307cebdaa4aaa7bf4de`；[固定版來源](https://github.com/fatalCMD/Fight-With-Me/tree/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de)。各例共用ID、樹、UI、AUTO、save接點見 [主報](ABILITIES.md) 與 [導航資料](ability-map.json)。

## Arcane Surge：有期限的能力值增益

定義在 `include/FWM/Paths.h:414`，主能力附Overflow與Conduit兩分支。rank數值是 `src/Paths.cpp:295` 的Primary switch；持續時間在 `Paths.h:723`，冷卻在 `Paths.cpp:1184`。這些是編進DLL的C++資料，不能只改INI增加另一招。

`AbilityPolicy.cpp:49` 決定低魔力時可AUTO；`AbilityAuto.cpp:28` 把實際戰場轉成純Context，再經共用Pace；`Arts.cpp:1838` 檢查已選slot、AUTO或明令、冷卻、失能狀態和資源；`Arts.cpp:1618` dispatch至 `Surge`（`:1246`）。Surge會拒絕重複啟用，使用 `Abilities::Lift` 增加MagickaRateMult，Overflow即刻補魔，Conduit對隊友施加增益。成功後 `Arts.cpp:1880` 才扣資源／記pacing／啟動冷卻。

可重用核心是 `Abilities.cpp:1213` 的Lift：以actor＋ActorValue＋source perk識別，同來源刷新只補差額；`:1289`在到期時撤回。save中的temporary modifier由 `Boosts/LoadBoosts` (`:1264/:1282`)記帳，load後先扣回，避免永久累加；不是把每個buff的完整剩餘狀態保存後續跑。因此新增buff必須先決定load後撤銷還是另做續時紀錄，不可直接Damage/ModActorValue而忘記反向清理。

視覺可選擇沿用已有shader，或用 `Surges.cpp:62` Call／`:72` Tick與 `ArcaneSurge.h` 的純姿態數據。原版將視覺生命週期和數值增益分開；關視覺或缺mesh不能抹掉數值。`Abilities::CastGesture` (`Abilities.cpp:94`)嘗試既有idle；手上沒有spell時不強迫換spell來完成手勢，這對native NPC尤其重要。

相對成本：若只新增已存在ActorValue的普通buff、沿用視覺，為低至中；新ID／固定樹位置與mask門檻仍需先解。若只是改既有技能的rank數值，成本更低，但仍要重建DLL並核balance/save repair。更小的被動例子是Iron Hide：`Paths.h:354` trait，`Arts.cpp:1492` Traits持續Keep護甲；不需新增Ability／slot／manual bit，但需新Perk與樹位置，並核卸除／改role時撤回。

## Elemental Burst：飛行表現、範圍命中與分支效果

定義在 `Paths.h:417`；`Arts.cpp:1340` 取得指定／當前目標、視線與距離，組合 `Blasts::Strike`（元素、傷害、半徑、硬直、Searing與分支）。`Arts.cpp:1280` 依當前已持法術、effective pools與已知法術判元素；這是讀取候選，不是為能力強制換手。`Forms.cpp:114`的Skyrim原法術主要提供施放聲／手光；真正命中不是把那些spell丟給原AI自行施放。

`Blasts.cpp:381` 建立Live記錄；`:406` Tick在飛行結束呼叫 `Land`（`:257`）。Land檢查敵方集合、水平距離／高度，以 `Blast::Share` 距離衰減，手動套元素與魔法抗性，再走 `PartyBalance::Damage`（`PartyBalance.cpp:76`）做全隊／Skald倍率。Searing在初擊後才降抗；火元素追加burn，冰／電損資源；tick與Clear (`Blasts.cpp:444`)負責清理。

純數學／姿態層是 `Blast.h/.cpp`；engine adapter是 `Blasts.cpp`；效果生成在 `Effects.cpp:1203`；NIF node命名契約與生成器在 `Blast.h:8`、`tools/blast/BuildBlast.js`。新招若沿用球體飛行與範圍命中，可重用這三層；新軌跡／碰撞／命中時機就要重寫對應adapter，不能只換貼圖。多段傷害不得同時再施放會造成相同傷害的原版spell，否則可能重複計算。

相對成本：沿用現有命中和VFX形態為中；新增軌跡、物理碰撞、持續引導、全新mesh node或動畫為高。驗證要涵蓋目標消失、無視線／跨高度、抗性邊界、敵我排除、群體倍率、分支先後、重複施放、缺視覺、離戰／load清理。

## Healing Circle：持續範圍效果加能力專屬移動要求

這招走舊的專用路徑，不能以為所有能力只加Arts::Run一個case就完成。`Abilities.cpp:728` Heal處理healRequested、AUTO、cooldown、資源與隊友健康；`:794`將rank與branches組成Strength，`HealCircle::Place`選中心，`:812`呼叫 `Circles::Raise`。`Battle.cpp:1555`手動命令也特判Heal；一般新技能則可走Arts::Request。

`HealCircle.h:17`給時長／半徑，`:30` Seek用健康、距離、高度、同空間、剩餘時長判可追圈；其純Place／At可離線測。`Circles.cpp:339`建立效果與marker，`:367` Tick分開視覺fade和真正治療時間，`:237` Mend回復隊友、燒不死敵人，`:327` Finish釋放marker／音效／effect。`Circles.cpp:387` PullFor才是對戰鬥planner提出進圈要求。

新的領域若要吸引 NPC，不能只做效果而忘記能力專屬控制與撤除契約，也不能把整個角色的普通配裝限制當成移動需求。若新領域不要求走位，應讓它只作範圍數值效果。上游圈要求入口是 `Circles::PullFor`，與圈內治療 tick 分開。

相對成本：沿用範圍tick且不加移動為中；帶進圈、導航、優先權、退出清理為中至高。需驗同時多圈、消失／死亡／卸載／離隊、沒有active ability時不改普通combat，以及 circle 結束時另一個能力的目標要求能正常接手。

## 真召喚不是狼頭效果的同義詞

`Arts.cpp:897` Kynareth's Maw建立的是Spirit資料＋`Effects::Head`（`:950`），以幾何和tick實現咬擊；不是建立可跟隨、戰鬥、有AI package的NPC。`Paths.h:49` 的AtronachRetired已退役且保留ID。若將來要真正召喚生物，還要定義actor所有權、派系／敵我、生命週期、dismiss／load與召喚上限、跟隨／戰鬥框架互動；目前這三個例子不能證明已有可直接註冊的通用召喚模組。此類列高成本，是否需要仍是玩法待決。
