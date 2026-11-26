# CTD：資料層與素材

[lessons 索引](README.md)

## le-collision-nif-precision-crash

> 間歇性 Havok 崩潰（hkpTriangleShape／hkpCompressedMeshShape＋Precision.dll 在呼叫鏈）＝某個世界物件的碰撞 NIF 是 LE 格式（stream 83 帶 bhkCompressedMeshShape）；全機 258 個同類檔，風港王宮門口首次踩到

2026-09-07。SE 讀 LE 格式壓縮碰撞會把指標讀壞，但只有 Precision／HDT-SMP 的射線剛好打到壞三角形才炸，所以是間歇的；看不見的純碰撞物件（如 Capital Windhelm Expansion 的 `NewPitCollsion.nif`）更難靠畫面察覺。使用者裁「先不修」，嫌疑清單在 `agentctl/handoffs/home-2026-09-07/crash/data/nif-suspects.csv`。

**How to apply:** crash log 出現 `hkpTriangleShape`＋`hkpCompressedMeshShapeShared`＋`Precision.dll` 就先查該 cell 物件的 NIF 版本（houseCARL `nif_inspect` 回「NOT an SE stream」），不要先懷疑腳本或動畫。修法：loose 覆蓋檔移走讓原版接手；BSA 內的用 SSE NIF Optimizer／CAO 轉 SE 再 loose 覆蓋；裝飾物可用 ESL patch 停 REFR。相關：[[verify-game-alive-via-qa-not-ps]]。

**適用界線：** stream 83 只證 LE 格式，不能將所有 LE skeleton 定罪；capsule-only、無 compressed-triangle 的釋放鏈不可直接套上述壓縮碰撞結論。轉換後 bhk blocks 與所有語義欄位原樣，只算版本／serializer 相容 A/B 候選，實戰未證；stream 100／unknown=0 不替代因果證據。判新修補前先比歷史 probable frames：同家族崩潰若早於修補已出現，仍不排除觸發條件交互。案例來源：private 素材與 Precision（已刪：`agentctl/handoffs/home-2026-11-01/varinia-native-crash/PRECISION.md`）、歷史對照（已刪：`agentctl/handoffs/home-2026-11-01/varinia-native-crash/HISTORY.md`）、指令與符號界線（已刪：`agentctl/handoffs/home-2026-11-01/varinia-native-crash/SYMBOLS.md`）。本段不表示該次 CTD 已修復。

## doomperk-advanceobject-block-ctd

> 2026-09-24 格擋必 CTD 真因：Constellations 三顆 doom*Perk 在 ModSkillUse 掛 EPModSkillUsage_AdvanceObjectHasKeyword，非物件造成的技能推進會 deref 垃圾指標；補丁移除該條件

2026-09-24 使用者「每次格擋攻擊就 crash」。簽章 `SkyrimSE.exe+01D3398 movzx eax, byte ptr [rcx+0x1A]`（讀 `TESForm::formType`），`rcx = 0x9E28` 每次相同＝決定性錯誤。`ConstellationsNewSkills.esp` 的 `0E5F46 doomThiefPerk`／`0E5F49 doomMagePerk`／`0E5F4A doomWarriorPerk` entry point 都是 `ModSkillUse`，條件串最後一條 `EPModSkillUsage_AdvanceObjectHasKeyword` 要解參照「造成這次技能推進的物件」；格擋／被打／`Experience.dll PlayerSkillsEx::UseSkill_Hook` 這類非物件推進時指標未初始化 → AV。

修法：`Constellations-DoomPerk-NoAdvanceObject-2026-09-24.esp`（ESL，masters=Skyrim.esm＋ConstellationsNewSkills.esp，3 筆 PERK override）移除該條件並清掉新尾項的 OR 旗標，產物在 `agentctl/handoffs/home-2026-09-24/doomperk/`；使用者實機格擋驗證通過。副作用是三個自訂技能的經驗判定變寬鬆，使用者 09-24 裁示「不用收緊」。上游無解（Constellations 117352 最新 1.0.3 是「Updated for SkyrimSE 1.7.99 / Address Library 12」，遊戲是 1.6.1170）。Scrambled Bugs `applyMultipleSpells` 維持 false（PEPE 作者明列不相容，但不是此案真因）。若復發，次順位嫌犯：`Experience.dll` 的 `UseSkill` hook、PEPE 與 CARP 同時 hook `Condition_HasKeyword`、停用中的 Actor Value Generator（modlist 895）。

**Why:** perk entry point 專用的條件函式只在「對的觸發來源」下才有合法上下文；這類 crash 固定同位址同 `rcx`，看起來像引擎 bug，其實是 mod 的條件設計。

**How to apply:** `+01D3398` 且 `rcx` 每次相同 → 先用 houseCARL 把 crash log 裡的 keyword FormID 反查成 EditorID，再 `cross_plugin_query type=PERK references=<keyword>` 找出哪顆 perk 用它，讀 `Effects[*].Conditions` 看 entry point 與條件函式，**不要先怪 SKSE DLL**。驗收只能由使用者實機重現（格擋），靜置不崩不構成證據，別誤判成能「自動重現」。相關：[[avif-perktree-overridden-by-non-overhaul-mods]]、[[pepe-tls-end-crash-is-payloadinterpreter-dangling-listener]]、[[housecarl-setfield-cjk-byte-drop]]。

同屬「記錄欄位留空/0 不是無害、特定情境下引擎才會踩到」家族的已定罪案例（2026-10-23）：(1) AMMO 的 Projectile 欄位留空（常見於腳本暫時替玩家裝假彈藥），戰鬥 AI 評估彈藥速度時讀 null CTD（`agentctl/handoffs/done/2026-10/crossbow-ctd-2026-10-09/REPORT.md`）；(2) PERK 的 FilterActivation entry-point（EntryType 74）＋AddActivateChoice，`PerkConditionTabCount` 必須是 2，寫成 0 卻掛 PerkCondition 會載入期硬崩潰（`analysis/mod-survey/findings/systems-encounters/perk-entry-points-activate-choice.md:56`）。載入期／戰鬥中 CTD 牽涉自製或魔改記錄時，先查這類「欄位該有值卻是空/0」的情況。

## achr-base-must-be-npc-not-lvln

> ACHR 直接用 LVLN 當 base 會在啟動載入階段 CTD（DSPortP3 09-13 實機二分定案）；原版 10,504 筆 ACHR 全 NPC_，leveled 敵人走 NPC_ 的 TPLT

2026-09-13。DSPortP3 一載入就 CTD（`InitTESThread`，Character 未初始化），真因是 16 筆 ACHR 的 NAME 直接指 LVLN。原版做 leveled 敵人是 NPC_ 用 TPLT 指 LVLN（例：`LvlGiant 0003053F`、`LvlDraugrMeleeAllMale 00055954`、`LvlSkeletonMeleeMixed 000BCCC7`），ACHR 再指那個 NPC_；CK 允許的事引擎不一定吃，「ACHR 用 LVLN」是 bug 不是刻意設計。

**How to apply:** 擺敵人一律指 NPC_；要 leveled 就指原版以該 LVLN 為 TPLT 的 NPC_，或自建 NPC_ 帶 TPLT。離線 gate：`projects/darksouls-port/tools/esp_refscan.py`（ACHR.NAME 非 NPC_ 硬 fail），跟 `check_masters.py` 並列跑。離線 gate 全綠不等於能載入——「跟 vanilla 型別對照」比「FormID 存不存在」更能抓這種坑；二分先拿 crash frame 點名的物件那一類。相關：[[missing-master-scan-mast-not-housecarl]]、[[housecarl-cannot-point-real-mo2-instance]]

## gltf2nif-effect-shader-ctd

> model-converter gltf2nif 寫出的 BSEffectShaderProperty 會讓 Skyrim 載入 NIF 時 memcpy 溢寫 CTD（09-13 dsp6 實證）；加算材質先 skip，別走 effect shader

2026-09-13。DS `g_BlendMode=4`（加算光柱）寫成 `BSEffectShaderProperty` 時，進 cell 載入該 NIF 就 `VCRUNTIME140 vmovntdq` 溢寫 CTD，frame 全是 `BSEffectShaderProperty/BSEffectShaderMaterial`；BSLightingShaderProperty 路徑沒問題。離線 gate（refscan／struct／NIF reader）全綠照樣崩，因為 NIF reader 只驗自己寫的格式。

**How to apply:** 需要 effect shader 前先修 `projects/model-converter/gltf2nif/nif_writer.py` 並拿原版 NIF 逐位元對照；沒修好前 blend_mode 4 一律 skip。載入期 NIF CTD 看 crash log 的 `inputFilePath` 行定位檔案。相關：[[achr-base-must-be-npc-not-lvln]]、[[dsport-render-constraints]]

## build-green-does-not-prove-esp-content

> ModForge／自製 esp 的離線 gate 全綠不代表內容或參照正確

2026-09-05。欄位加到錯的 spec 型別（exterior cell 該用 `WorldspaceCellSpec` 卻加進 `CellSpec`）時 JSON 靜默丟棄該欄位，esp 裡值全 0 但 gate 照樣綠；沒有 gate 查參照 FormID 是否解析得到時，進遊戲在記錄載入階段 AV（暫存器低 32 位像 FormID＝未解析訊號）。「records 數」是讀進幾筆不是寫對幾筆。`agentctl/handoffs/done/2026-09-05/dsport4-2026-09-05/STATE.md:53-150`。

**How to apply:** 宣告「做到」前開 esp 核對欄位值；gate 補全參照解析掃描；回歸證據是前後各 build 一次比 SHA-256，不是測試全綠。相關：[[achr-base-must-be-npc-not-lvln]]。
