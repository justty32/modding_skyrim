# CTD：資料層與素材

[lessons 索引](README.md)

## le-collision-nif-precision-crash

> 間歇性 Havok 崩潰（hkpTriangleShape／hkpCompressedMeshShape＋Precision.dll 在呼叫鏈）＝某個世界物件的碰撞 NIF 是 LE 格式（stream 83 帶 bhkCompressedMeshShape）；全機 258 個同類檔，風港王宮門口首次踩到（原 type: project）

2026-09-07 使用者從 Windhelm 王宮走出時崩，第二次同路徑沒崩。lead-crash 掃全機 32240 個 NIF：1046 個 LE 格式、258 個帶壓縮碰撞；風港 6 個（Capital Windhelm Expansion 的 `NewPitCollsion.nif` 純碰撞看不見、魚攤 3 個、Assorted Mesh Fixes 覆蓋原版的 `whmaingatesteps.nif`／`whtempletalos3.nif`）。使用者裁「先不修」，清單在 `agentctl/handoffs/home-2026-09-07/crash/data/nif-suspects.csv`。

**Why:** SE 讀 LE 格式壓縮碰撞會把指標讀壞，但只有 Precision／HDT-SMP 的射線剛好打到壞三角形才炸，所以是間歇的；看不見的純碰撞物件更難靠畫面察覺。

**How to apply:** crash log 出現 `hkpTriangleShape`＋`hkpCompressedMeshShapeShared`＋`Precision.dll` 就先查該 cell 物件的 NIF 版本（houseCARL `nif_inspect` 回「NOT an SE stream」），不要先懷疑腳本或動畫。修法：loose 覆蓋檔移走讓原版接手；BSA 內的用 SSE NIF Optimizer／CAO 轉 SE 再 loose 覆蓋；裝飾物可用 ESL patch 停 REFR。相關：[[verify-game-alive-via-qa-not-ps]]。

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

## achr-base-must-be-npc-not-lvln

> ACHR 直接用 LVLN 當 base 會在啟動載入階段 CTD（DSPortP3 09-13 實機二分定案）；原版 10,504 筆 ACHR 全 NPC_，leveled 敵人走 NPC_ 的 TPLT（原 type: project）

2026-09-13 dsp5 三線＋實機二分定案：DSPortP3 一載入就 CTD（`InitTESThread`，Character 未初始化）的真因是 16 筆 ACHR 的 NAME 直接指 LVLN（`LCharGiant`／`LCharDraugrMeleeAllMale`／`LCharSkeletonMeleeMixed`）。拿掉這 16 筆的變體一輪就過主選單。

**Why:** Skyrim.esm 10,504 筆 ACHR 全部 NPC_ base、LVLN-base 是 0（ref 隊與頂層各自獨立掃過）。原版做 leveled 敵人是 NPC_ 用 TPLT 指 LVLN（例：`LvlGiant 0003053F`、`LvlDraugrMeleeAllMale 00055954`、`LvlSkeletonMeleeMixed 000BCCC7`），ACHR 再指那個 NPC_。CK 允許的事引擎不一定吃。之前 ESP-AUDIT 把「ACHR 用 LVLN」判成「刻意設計不是 bug」，錯了。

**How to apply:**
1. 擺敵人一律指 NPC_；要 leveled 就指原版以該 LVLN 為 TPLT 的 NPC_，或自建 NPC_ 帶 TPLT。
2. 離線 gate：`projects/darksouls-port/tools/esp_refscan.py`（09-13 起 ACHR.NAME 非 NPC_ 硬 fail）；跟 `check_masters.py` 並列跑。
3. 離線 gate 全綠不等於能載入——「跟 vanilla 型別對照」比「FormID 存不存在」更能抓這種坑；二分順序先拿 crash frame 裡點名的物件那一類。
相關：[[missing-master-scan-mast-not-housecarl]]、[[housecarl-cannot-point-real-mo2-instance]]

## gltf2nif-effect-shader-ctd

> model-converter gltf2nif 寫出的 BSEffectShaderProperty 會讓 Skyrim 載入 NIF 時 memcpy 溢寫 CTD（09-13 dsp6 實證）；加算材質先 skip，別走 effect shader（原 type: project）

2026-09-13 dsp6：材質線把 DS `g_BlendMode=4`（加算光柱）兩筆寫成 `BSEffectShaderProperty`，進 cell 載入 `m0070B1A18.nif` 時 `VCRUNTIME140 vmovntdq` 溢寫 CTD，frame 全是 `BSEffectShaderProperty/BSEffectShaderMaterial`。改成 skip 後正常。

**Why:** gltf2nif 的 effect shader 區塊格式與引擎期望不符（BSLightingShaderProperty 路徑沒問題）。離線 gate（refscan／struct／NIF reader）全綠照樣崩，因為 NIF reader 只驗自己寫的格式。

**How to apply:** 需要 effect shader 前先修 `projects/model-converter/gltf2nif/nif_writer.py` 並拿原版 NIF 逐位元對照；沒修好前 blend_mode 4 一律 skip。載入期 NIF CTD 看 crash log 的 `inputFilePath` 行就能定位檔案。
相關：[[achr-base-must-be-npc-not-lvln]]、[[dsport-render-constraints]]
