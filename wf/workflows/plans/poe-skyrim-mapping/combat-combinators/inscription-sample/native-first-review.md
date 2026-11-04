# 原生施法優先的短重審

[待修舊稿](../../../../../user/2026-11-04-inscription-sample.md)｜[原生零件技術附錄](../../../../../user/2026-11-04-native-spell-templates.md)｜[六條替代候選](native-first-candidate.json)

舊刻印少了關鍵層：選點後，玩家平時已有的法術究竟如何觸發規則。本意可以是原生施法被動附狀態，但尚未完成分類／事件橋設計；因此不能當已核可範本，也不把「引擎有MGEF」當成接好了玩法。

## 保留刻印的最小修法

玩家仍裝備、施放原有法術；買點給被動能力，觀察既有SpellItem與真命中，必要時由隱藏輔助spell掛caster-owned MGEF。那是新增被動工程，不要求玩家學另一招「印記法術」。有Script.Cast／DoCombatSpellApply API，不代表所有原生施法已經自動接上它。P/B/D動態本金、手別輸入與原傷延後仍是另加機制，未因載體原生就變成現成能力。

## 另一個較貼現有操作的候選 術師蝕魔

不設印值或儲能條，不另學蝕魔法術。你照用已會的**集中持續傷害法術**磨敵魔力，再換已會的**一次放出型傷害法術**找破池機會；只有實際有MP傷或明確改道的交易才可破池。

**磨魔**：集中法術把部分原HP傷轉去削MP，示例30%。你為阻止敵人施法而犧牲當下削血。

**破池**：瞬發MP傷超過敵剩餘MP，未能扣到的一部改HP傷，示例50%。不是讓所有火冰電憑名字自動有MP傷。

**枯魔牽制**：敵MP低於25%時，其對本人傷害×0.9。可留一個枯竭敵、換打別人，不新增可疊debuff。

**奪魔續流**：集中法術真的扣掉敵MP，回本人該實扣量25%；抽乾便沒有這份續流，必須換招或換敵。

**以魔作命 高階純規則**：本人傷害法術先傷敵MP，MP不足的HP傷部分才落到HP。改成先拆法力防線再殺敵；放棄對有MP敵的立即削血，無MP生物仍照傷HP。

**斷血逐魔 高階純數值交換**：本人法術MP傷×4、HP傷×0.25（僅示例），偏極端破法支援；殺無MP敵慢很多，要靠武器、隊友或其他來源補足。

## 原生輸入不是一句合格法術

先讀實際SpellItem的CastingType（Concentration或FireAndForget）、Delivery及effects；效果以archetype、primary/secondaryAV、hostile/detrimental與實際狀態辨識。學派只是輔助分類，不能把Destruction全當直接傷害，或火命中就當仍在燃燒。裝備的法術也不是這次已成功施放。這些欄位在[SpellItem](https://raw.githubusercontent.com/CharmedBaryon/CommonLibSSE-NG/7a60f4de794095d7b0f8928d1b930a52e9a7da83/include/RE/S/SpellItem.h)及[EffectSetting](https://raw.githubusercontent.com/CharmedBaryon/CommonLibSSE-NG/7a60f4de794095d7b0f8928d1b930a52e9a7da83/include/RE/E/EffectSetting.h)可讀，但本輪缺原版records，未捏造FormID或斷言某具名spell的實際欄位。

玩家操作是持續磨魔→停手→切瞬發收招，或留枯竭敵轉打下一個。直接使用既有HP/MP與施法形態，沒有P/B/D。不過實扣、溢出、命中來源與結算重路由仍須新交易collector，並非CK拖幾個欄位便已完成。

這只是待選替代：4進階中3獨特／1共享、2高階獨特都仍是設計聲明，尚未與兄弟型完整審過；與高階／轉傷的順序也未定稿。不改common、不改24總覽、不覆寫17點或重新填圖。舊比例裁示照留；要保留刻印、採蝕魔或再換方向，由使用者看過後決定。
