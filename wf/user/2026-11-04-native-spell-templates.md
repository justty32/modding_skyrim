# Skyrim原生法術有哪些零件

本頁是技術附錄；它不能替代「選點後正常原生法術如何觸發規則」的設計。刻印樣板現為待修，未核可作範本。

有很多現成法效可用；「沒有叫Mark的法術樣板」不等於不能在敵人身上掛一個印。不過**限時法效狀態**和我們提議的**付魔存帳、解印、延後原傷**是兩件事：前者有原生底座，後者仍要寫邏輯。這次先盤點，尚未替你改掉[刻印樣板](2026-11-04-inscription-sample.md)。

## 先分三層

**法術怎麼施放、怎麼送到目標。** SPEL/MagicSystem可表達常駐、一次放出、持續施法，以及Self、Touch、Aimed、TargetActor、TargetLocation等Delivery選項；另有Scroll類型。這些是結構選項，不等於全部都能任意搭配。SpellType還含疾病、毒、附魔等魔法來源分類，不全是玩家手施法術。[固定原碼](https://raw.githubusercontent.com/CharmedBaryon/CommonLibSSE-NG/7a60f4de794095d7b0f8928d1b930a52e9a7da83/include/RE/M/MagicSystem.h)

**法效做什麼。** MGEF的Archetype決定引擎效果種類；還能配置持續、強度、範圍、ActorValue、關鍵字、條件與視效。[EffectSetting欄位](https://raw.githubusercontent.com/CharmedBaryon/CommonLibSSE-NG/7a60f4de794095d7b0f8928d1b930a52e9a7da83/include/RE/E/EffectSetting.h)

**另外加什麼邏輯。** Papyrus或C++可接生命週期及自訂行為，但Script archetype不是現成交易帳本；其他Archetype也不因此不能掛效果腳本。

## 可先考慮的十組原生效果

**數值／資源**：ValueModifier、DualValueModifier、PeakValueModifier、Absorb。可改ActorValue、處理雙值或吸取；適合從傷害、恢復、增減屬性方向組法效。PVM精確疊加／同keyword處理仍待核，不能先保證只留最強。

**心智／行動控制**：Calm、Demoralize、Frenzy、Rally、Paralysis、Stagger、Disarm、TurnUndead、Banish。可作控制效果方向；等級、抗性、種族等限制要逐類查，不能光看名字推可控所有敵人。

**召喚／使役**：SummonCreature、Reanimate、CommandSummoned。已有召喚生命週期與受控Actor資料，不等於任意更換召喚owner。

**召喚裝備**：BoundWeapon、EnhanceWeapon。有裝備、背包事件及效果開始／結束底座；收鞘等精確限制未核。

**隱蔽／感知／照明**：Invisibility、DetectLife、NightEye、Light。Darkness也有原生ID，但本輪只記存在，不把冷僻ID當已證實可用玩法。

**狀態解除**：Dispel、CureDisease、CurePoison、CureParalysis、CureAddiction。原生與Papyrus已有清除效果／法術入口；解除一枚effect不會自動替自訂印帳結算退款。

**近身光環**：Cloak。有原生範圍更新載具，適合研究鄰近目標的持續效果；精確半徑、選敵與tick仍需記錄／實機，不會自動替印找遷移對象。

**地面／物理**：SpawnHazard、Telekinesis、GrabActor。可研究地面危險物與抓物等行為；Telekinesis抓物不能直接當成任意拉NPC。

**時間／變身／特殊狀態**：SlowTime、Etherealize、Werewolf、VampireLord、Disguise。確認有原生種類，但作用範圍與限制沒有逐一實機驗過。

**靈魂／腳本／其他特殊**：SoulTrap、Script、SpawnScriptedRef等。另有Guide、WerewolfFeed、Concussion、ValueAndParts、AccumulateMagnitude、Lock、Open等冷僻ID；靈魂陷阱不是通用儲傷帳本，腳本效果也不是已完成刻印機制。

以上分組是導覽；完整[十組與來源](../workflows/plans/poe-skyrim-mapping/combat-combinators/inscription-sample/native-template-groups.json)、[47個有名Archetype ID](../workflows/plans/poe-skyrim-mapping/combat-combinators/inscription-sample/native-archetypes.json)可查。[固定枚舉原碼](https://raw.githubusercontent.com/CharmedBaryon/CommonLibSSE-NG/7a60f4de794095d7b0f8928d1b930a52e9a7da83/include/RE/E/EffectArchetypes.h)有0–46及None=-1；**47個ID不等於47個都驗過可用的玩家法術**。

## 哪些能拿來做「印」

**原生零件已存在**：ActiveEffect有caster、target、spell、duration、magnitude、uniqueID等；MGEF有keyword、shader／hit art等視覺欄位。因此可自製一個「附敵、有限時、有符文提示」的MGEF狀態，不必引擎另有Mark archetype。[ActiveEffect](https://raw.githubusercontent.com/CharmedBaryon/CommonLibSSE-NG/7a60f4de794095d7b0f8928d1b930a52e9a7da83/include/RE/A/ActiveEffect.h)

**需要自行寫腳本／帳務**：每effect變數、開始／結束／死亡事件可以支撐簡單狀態，但每施術者分帳、P/B/D、20%原生實付、退款、消印與搬餘額不會由欄位自動保障。Papyrus有HasMagicEffect／HasMagicEffectWithKeyword；不能拿某個Form自帶keyword檢查，冒充Actor目前持有效果。[原版效果API](https://raw.githubusercontent.com/ianpatt/skse64/master/scripts/vanilla/ActiveMagicEffect.psc)／[Actor API](https://raw.githubusercontent.com/ianpatt/skse64/master/scripts/vanilla/Actor.psc)

**需要新C++或先驗hook**：把原法傷攔住並保型存D、原生實付交易收集、施法改成近戰交付、阻止合成效果自觸，不能因為有Script效果就當已經可做。GetDuration／GetTimeElapsed／GetMagnitude等又有[SKSE擴充API](https://raw.githubusercontent.com/ianpatt/skse64/master/scripts/modified/ActiveMagicEffect.psc)的界線，不能全寫成vanilla。

原生ActiveEffect也有存讀生命週期；若自訂帳選讀檔清空，視效／effect實例要同步清，避免「有標、無帳」。Rune沒有同名Archetype：Projectile、Explosion、Hazard是可研究的零件，這次沒有本機vanilla記錄bytes，不能假定每個原版符文都走同一條鏈。

## 比較務實的起點

可先考慮**原法傷照常＋原生限時MGEF／符文提示＋持印時條件效果**的小型樣板，先看狀態能否可靠掛上、分caster與清掉。若保留動態付魔／本金，仍要加小額帳務；若保留爆破延後原傷及觸法，仍需C++邊界證明。這只是可選實作路線，沒有悄悄替換已審提案。

本次CK頁面403，故不借其未讀正文支持細節；也未取得本機原版Spell／MGEF記錄，沒有捏造具體FormID／EDID。先讓你看引擎現成有哪些，再決定刻印要採哪種載具；未新增ESP、腳本或plugin。
