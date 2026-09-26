# CTD 真因與判法（3/3）

[lessons 索引](README.md)｜同主題：[crash-triage](crash-triage.md)、[crash-triage-2](crash-triage-2.md)

## custom-navm-combat-pathing-ctd

> 自訂多層 exterior NAVM 在敵人對玩家做戰鬥尋路時 CTD（PathingCell 空指標）；DS 港 navmesh 第 5 項的真相（原 type: memory）

2026-09-13 dsp8-meas 實機：DSPortP3 的 7 格自訂 navmesh（由 DS NVM 直轉、最多 3 層疊）
進得了遊戲、玩家能走，但屍鬼一進入戰鬥尋路（`CombatPathingRequest…FindTargetLocation`）
就 `EXCEPTION_ACCESS_VIOLATION` 讀 0x14，stack 物件 `Pathing*`／`PathingCell*`，
角色 `0xF5000D3D`、cell `0xF5000A5C`／`0xF5000A71`。crash log 存在
`agentctl/handoffs/home-2026-09-13/dsp8/meas/runtime/crash-combat-pathing-18-04.log`。

**Why:** dsp5～7 三輪走動都沒事，因為玩家用 setpos／tcl 沒讓敵人真的追；第 9 項「敵人 alive」
不等於 navmesh 可用。先前用 `placeatme` 生隨從也沒建立 teammate，所以隨從測試看不出來。

**How to apply:** 修 navmesh 時先用 `out/bisect/nonavm/` 那支（無自訂 NAVM）做對照，
確認是 NAVM 不是 NPC；驗收要「敵人主動追到玩家 15 秒不 CTD」而不是「走一圈沒事」；
懷疑點依序：跨格接縫（7 格自訂與 49 格平面沒接）、NAVM 的 NVNM 鄰接／cover 欄位、
多層疊面。相關：[[dsport-render-constraints]]、[[achr-base-must-be-npc-not-lvln]]。

**2026-09-15 更正：** 同址（SkyrimSE.exe+04D0038）崩潰在原版荒野 cell 也發生（09-08、09-15，雪狼／泥沼蟹），四次共同點是 `MaxsuCombatEscape.dll`（Better Combat Escape - NG 1.0.4）的 CellEventHandler 在 actor 換 cell 事件裡同步跑戰鬥尋路。已停用該 mod；自訂 NAVM 不再是這個位址的首要嫌犯，看到 CombatPath＋Pathing 空指標先查 SKSE DLL 的 cell 事件 hook。

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
