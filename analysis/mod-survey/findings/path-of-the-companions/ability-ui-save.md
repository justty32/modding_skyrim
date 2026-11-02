# PoTC 技能擴充：UI、文字與存檔接點

本文記錄 UI／save／API 接點與限制，附釘版 source 位置；沒有新技能實作。

來源為 Fight-With-Me `971b8b5aba0c34c649e70307cebdaa4aaa7bf4de` 與 Paths `189f24c8a8e5b61cacfbc60b2347589c9f3eff61`；路徑相對FWM；`paths/src/Main.cpp` 相對Paths repo的 `src/Main.cpp`。以下均為這兩個上游版本的結構限制。

## 導航

<!-- wf-nav -->
| 接點 | 釘版來源 |
|---|---|
| Ability、Perk IDs與Node、樹、Record | [Paths.h:23](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/include/FWM/Paths.h#L23)、`:129`、`:260`、`:320`、`:520` |
| 簽章、編碼與解碼 | [Paths.cpp:780](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/src/Paths.cpp#L780)、`:809`、`:862`、`:1095` |
| SKSE PATH／UNLM讀寫 | [Paths Main.cpp:418](https://github.com/fatalCMD/paths-fwm-addon/blob/189f24c8a8e5b61cacfbc60b2347589c9f3eff61/src/Main.cpp#L418) |
| AUTO、boost、cooldown save | [Save.cpp:18](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/src/Save.cpp#L18)、`:57`、`:213` |
| 樹UI、能力dock、glyph | [Menu.cpp:353](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/src/Menu.cpp#L353)、`:3250`、`:4550`、`:5136` |
| 翻譯載入與lookup | [Text.cpp:106](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/src/Text.cpp#L106)、`:146`、`:179` |
| 跨DLL固定介面 | [FightWithMePathsAPI.h:13](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/include/FightWithMePathsAPI.h#L13)、`:102`；[PathsLink.cpp:90](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/src/PathsLink.cpp#L90) |
| 模板更新工具與測試 | [Strings.ps1:1](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/tools/Strings.ps1#L1)；[PathsTests.cpp:43](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/tests/PathsTests.cpp#L43) |

## 能不能只加資料

技能樹是C++編譯期資料：`Paths.h:321` 的 `inline constexpr std::array<Path,kRoles> paths`，不是JSON／INI註冊表。每個 `Node` 有perk、kind、ability、tier、most、base、name、glyph、cost、step、capstone（`:260–273`）；建構輔助 `A/B/T/C/E` 在 `:300–317`。新增節點、ID、效果或調整這些欄位都要重新編DLL。

外部資料目前可以替換翻譯、圖示與視覺素材，或調已暴露的INI tuning。Points設定只有門檻、額外點數、允許重配與debug unlimited四項，由 `paths/src/Main.cpp:76–83` 讀取、`:95–134` 寫user覆蓋檔；它不是新技能描述語言。共用 `Settings.cpp:296–301` 能調既有PathBonus係數，不是任意技能定義。

`IPaths`（API.h:102–140）提供進度讀寫、Learn／Equip、Steering／Holds等既有操作，無RegisterAbility／RegisterNode；Main.cpp exports亦未見動態註冊入口。新增技能須改相容fork；外掛註冊框架是額外工程。

## ID與存檔界線

Ability及Perk都是 `uint8_t` 且明寫append-only（`Paths.h:23–56`、`:129–248`）。不能插入中間或重用retired ID。上游Cleave改SpectralWolf、PinningShot改Windstep仍保留ordinal，舊save語意跟著ID走。

更早會碰到的是AUTO mask：目前Ability `kGlory=29`、`kCount=30`；`Orders.h:66` 的manual為uint32，`PathsLink.h:53`及`Menu.cpp:2482`皆 `1u << ability`；`Save.cpp:113–123,252–260`把mask以4 bytes存到AUTO v1。第一個新ID30仍過現有 `PathsTests.cpp:43` 的 `static_assert(kAbilityCount<32)`；第二個新ID31雖可用32-bit mask表示，count32會被這條現測試擋，必須明確檢視上界；第三個新ID32就真不能沿用此shift。若規模超過此門檻，需要一起改型別、UI／runtime bit操作、AUTO格式與舊版遷移，不能只把enum往下加。Cooldown另外以uint8 key保存，`Cooldowns.h:24–29`保留0x80–0x83給舊能力通道，也不能任意跨過。

PATH格式版本現在是5（`Paths.h:629`）。`Paths.cpp:809–858`實際寫 actor reference ID、peak、role count，每role兩個ability ID，及購買的 `(perk ID, rank)` pair，另附bonus和Skald unlock。同role內移動perk可由ID找回；換role、刪perk或改ID不會自動轉移。`Decode:887–905`跳過未知role／perk、未知slot變None，rank clamp到3；`Book::Load:1095`還會Repair可用點數／前置條件。不可把這種修剪當成無損migration。

Paths Main.cpp以SKSE unique ID `FWMP`、records `PATH`／`UNLM`保存正常進度與unlimited前的快照（`:423–470`），兩份都須遷移，且 `ResolveFormID` 在 `:475–488`重新解析actor。現成migration例子是 `Paths.cpp:931–947`：v<3重設rank保留peak；v3移除舊Healer Ward ranks並FillSlots，spent依rank重算。新增技能若只append ID、保留格式可能不必升PATH版本，但更動格式／需特殊退款或轉換就必須明定遷移，並測兩份record及舊DLL降版後再存的資料流失。

持續效果另有save：`Save.cpp:89–111`保留boost量，載入後交Abilities清理（`:213–235`）；cooldown由COOL record `:125–129,241–248`保存；Windstep在存前主動Clear（`:59`）。只改ActorValue卻不清理可能留下永久數值；PATH round-trip不代表效果save安全。

## UI與翻譯成本

現樹固定15格＝4×（1主動節點＋2分支）＋3被動，兩個攜帶slot（`Paths.h:85,277–285`）。分支parent與slot自動補位可重用，但只在既有結構內；`Menu.cpp:5138–5149`硬寫前三family、9/10/11上方family、12..14 trait，`TreeNavigation.h:7`也依索引算列。第五個主動技能不是單純array多一筆，需改布局、手把導航、API record尺寸、結構測試；純粹替換既有位置則必須先決定原購買點與舊技能如何遷移，不能默默覆蓋。

UI大多會讀新Node/Ability metadata：dock在 `Menu.cpp:3250–3303`顯示名稱、rank、cooldown、Describe與AUTO說明，按鍵送 `kAbilityNow`；detail card在 `:4579–4604`用CanLearn／CanForget／CostOf顯示可操作狀態。新技能仍要有 `Paths.cpp` 的Primary／Secondary、Measure (`:1204`)、Describe (`:1374`)及Cooldown等對應，不能只有樹名。

翻譯以完整英文原句作key，不是固定字串ID：`Text.cpp:127–135`讀 `English<TAB>Translation`、`:154–166`按語言後綴及排序載入多檔、`:179–185`缺翻譯回英文。Paths Main.cpp `:525–542`使用 `Data/SKSE/Plugins/FightWithMe/Translations`；`tools/Strings.ps1:110–154`抽FWM與Paths英文模板並檢查過期。新增名稱、auto own、描述、數值格式句都要抽新模板、補中文與format placeholders；字型涵蓋與較長中文UI是實機gate。

圖示可以沿用FontAwesome codepoint，也可新增有授權SVG：`Menu.cpp:415–418`大圖讀 `glyphs/{code:04x}.svg`，特殊private glyph的Picture／fallback在`:353–438`有白名單分支，新private區碼需接入而非放檔就算生效。新素材也須納入打包與授權記錄。

## 決策與驗證

實作前仍待使用者決定：是新增主動Ability、分支或常駐Trait；沿用4能力布局或要加容量；是否沿用兩slot；舊角色已買滿時如何分配新點與退款；新能力是舊效果的數值變體還是新機制。本研究不替使用者決定。

最小回歸沿用 `PathsTests.cpp` 的tree shape／每ability存在性 (`:570–630`)、Describe全rank (`:677`)、門檻／分支 (`:721–766`)、slot (`:837–854`)、encode／decode／截斷 (`:932–950`)、unlimited快照與遷移。另加新ID的AUTO與cooldown round-trip、既有save保留舊ID、缺／未知節點修剪、paired interface mismatch拒啟，及滑鼠／手把／中文UI實機驗證。API Version6固定7×15×2陣列；`PathsLink.cpp:104–108`拒絕不同tree signature（signature包括counts與節點規則但不含文字）。若與完整FWM一起使用，修改樹後必須以一致定義重建兩DLL；只改PoTC會被拒接。
