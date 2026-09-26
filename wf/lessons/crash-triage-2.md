# CTD 真因與判法（2/3）

[lessons 索引](README.md)｜同主題：[crash-triage](crash-triage.md)、[crash-triage-3](crash-triage-3.md)

## doomperk-advanceobject-block-ctd

> 2026-09-24 格擋必 CTD 真因：Constellations 三顆 doom*Perk 在 ModSkillUse 掛 EPModSkillUsage_AdvanceObjectHasKeyword，非物件造成的技能推進會 deref 垃圾指標；補丁移除該條件（原 type: project）

2026-09-24 使用者「每次格擋攻擊就 crash」。簽章 `SkyrimSE.exe+01D3398 movzx eax, byte ptr [rcx+0x1A]`（讀 `TESForm::formType`），**`rcx = 0x9E28` 七次完全相同**＝決定性錯誤不是隨機毀損。

真因在資料層：`ConstellationsNewSkills.esp` 覆寫的三顆 perk
`0E5F46 doomThiefPerk`（Athletics）／`0E5F49 doomMagePerk`（Sorcery）／`0E5F4A doomWarriorPerk`（HandToHand），
entry point 都是 **`ModSkillUse`**（每次技能使用都觸發），條件串最後一條是
**`EPModSkillUsage_AdvanceObjectHasKeyword`**。該函式要解參照「造成這次技能推進的物件」；
格擋／被打／`Experience.dll PlayerSkillsEx::UseSkill_Hook` 這類不是由物件造成的推進，那個指標未初始化 → AV。

修法：`Constellations-DoomPerk-NoAdvanceObject-2026-09-24.esp`（ESL，masters=Skyrim.esm＋ConstellationsNewSkills.esp，3 筆 PERK override），
移除三顆的該條件（7→6）並清掉新尾項的 OR 旗標，其餘位元組不變。產物在 `agentctl/handoffs/home-2026-09-24/doomperk/`。**使用者 2026-09-24 09:5x 實機格擋驗證通過，不再崩。**
副作用：三個自訂技能的經驗判定變寬鬆，使用者 09-24 裁示「不用收緊」。
上游無解：Constellations 117352 最新 1.0.3 是「Updated for SkyrimSE 1.7.99 / Address Library 12」，遊戲是 1.6.1170，不能升也沒修這個。

排除過的：Scrambled Bugs `applyMultipleSpells`（PEPE 作者明列不相容、PEPE log 確實偵測到，改 false 後同簽章再崩；層仍保留因為不相容是真的）。
次順位嫌犯若復發：`Experience.dll` 的 `UseSkill` hook、PEPE 與 CARP 同時 hook 同一個 `Condition_HasKeyword`、停用中的 Actor Value Generator（modlist 895，PEPE／CARP／Constellations 都附 AVG toml）。

**Why:** perk entry point 專用的條件函式只在「對的觸發來源」下才有合法上下文；換一個來源觸發同一個 entry point 就會 deref 垃圾。這類 crash 會固定在同一個位址與同一個 `rcx`，看起來像引擎 bug，其實是某個 mod 的條件設計踩到。

**How to apply:** `+01D3398` 且 `rcx` 每次相同 → 先用 houseCARL 把 crash log 裡的 keyword FormID 反查成 EditorID，再 `cross_plugin_query type=PERK references=<keyword>` 找出哪顆 perk 用它，讀 `Effects[*].Conditions` 看 entry point 與條件函式，**不要先怪 SKSE DLL**。驗收只能由使用者實機重現（格擋），靜置不崩不構成證據——2026-09-24 我誤判成「自動重現」害線空跑 15 分鐘。相關：[[avif-perktree-overridden-by-non-overhaul-mods]]、[[pepe-tls-end-crash-is-payloadinterpreter-dangling-listener]]、[[housecarl-setfield-cjk-byte-drop]]。

## spid-outfit-manager-live-inventory-reset-ctd

> 2026-09-24 長毛象 CTD +02B789A 真因是 SPID Outfit Manager 對活體 reset inventory 觸發 3D 重掛載；call stack 沒有 SKSE DLL 不代表 SKSE DLL 無關（原 type: project）

2026-09-24 10:23 野外走路（巨人營地，cell grid `(-6,1)`）CTD，簽章 `SkyrimSE.exe+02B789A  mov rcx,[rcx+0x130]`、rcx=0，全機首見。崩在**背景載入執行緒**（frame 10-11 是 kernel32/ntdll 進入點），現場 `QueuedCharacter` / `IOManager` / `BSFadeNode "skeleton.nif"`，RDI = 長毛象 `[ACHR:001038A9]`。

真因鏈：崩潰前 **2.4 秒** SPID 對**同一個 ACHR** 做了 `[🧥] Resetting inventory`。SPID v7.3.2.16 的 Outfit Manager 開機就裝了 `ShouldBackgroundClone` / `Load3D` / `Resurrect` / `ResetInventory` hook —— 正是崩潰所在那條路。使用者目視確認長毛象模型正常 → 排除壞網格，是**已在場的 actor 被重新掛載 3D** 跟背景載入佇列對撞。

驅動者只有一支：`CT77 Remodeled Armor ...` 的 `ElderOutfit_DISTR.ini`（全 load order 唯一的 outfit 分配）。為了讓老年 NPC 換裝，SPID 把整個場景的活人活獸都 reset 一輪。修法＝空檔覆寫層 `SPID-NoElderOutfit-2026-09-24` 壓在 CT77 之上（modlist 1308）。SPID 7.3.3 changelog 無 outfit manager 修正，升級無用。

**Why:** 兩個會重複踩的誤判 ——
(1) **call stack 全是原版碼、沒有 SKSE DLL，不等於 SKSE DLL 無關**：hook 是 trampoline，跑完跳回原版碼就不留名字。要改看該 DLL 的 log 有沒有在崩潰前幾秒動過同一個 FormID。
(2) **`Resetting inventory` / `Resurrecting` 的總次數會被遊玩時長汙染**（32 分鐘實玩 vs 短煙霧），不能當 A/B 指標。

**How to apply:** SKSE plugin 的嫌疑要用「崩潰前數秒 log 裡有沒有同一個 ACHR/FormID」來定罪，不是看 call stack 有沒有它。SPID 這類 A/B 的指標用**活體 reset**＝被 `Resetting inventory` 但沒有配對 `Resurrecting` 的 ACHR 數（有配對的是屍體復活重配，屬另一類）——本案 before 75、after 0，不吃時長。相關：[[doomperk-advanceobject-block-ctd]]、[[verify-waituser-against-logs]]。

## daegon-itemfinding-script-ctd

> Daegon 的 k101DaegonItemFindingAliasScript 換地點時經 PO3 FindAllReferencesOfType 崩潰；2.2.1.2 也沒修，pex 要一直藏著（原 type: memory）

2026-09-18 晚三次同址 CTD `SkyrimSE.exe+030B0B3`（Papyrus VM 執行緒），真因是 Daegon and Kaeserius 的
`k101DaegonItemFindingAliasScript`（OnLocationChange）呼叫 po3_PapyrusExtender `FindAllReferencesOfType(player, k101TempFormList)`，
引擎掃玩家周圍參考時踩壞指標（crash log 暫存器直接印出 `Character "黛宮"`）。
升到最終版 2.2.1.2 後 byte 比對：三處呼叫原封不動，所以 `mods/Daegon-2.2.1.2/scripts/k101DaegonItemFindingAliasScript.pex.mohidden` 要一直藏。

**Why:** 作者已退圈不會再修；PO3 5.5.0.1 過舊（上游 6.5.2）是承載者但不是觸發者。
**How to apply:** 看到同址 +030B0B3 先確認 pex 還藏著；Daegon 新版 Initialize 開機會噴 6 行 SkillBooksArray/TopicArray None，是藏 pex 的直接後果，正常。升 PO3 另案。
相關：[[daegon-2212-midsave-upgrade]]
