# 使用者自己捏身形

[入口](README.md)｜[換身體](body-swap.md)｜[逐 NPC 指定身形](body-swap-npc.md)

本頁由 [換身體](body-swap.md) 拆出，內容不變。

**遊戲內（RaceMenu）**：適合「我的角色」。部署帶 `.tri` 的身體與裝備層後，RaceMenu 身體滑桿的改動會同時套到裸身與裝備。需要三樣東西：

- 滑桿定義 `RaceMenuMorphsCBBE.esp`：現役沒有裝，3BA 包 `CBBE 3BA (3BBB)-30174` 的 `15 RaceMenuMorphs/00 RaceMenuMorphs - CBBE` 有附，不必另外下載。
- 身體 `.tri`：由 `BSO-Body-*` 層提供。
- EngineFixes 記憶體設定：現役 `bOverrideMemoryManager`／`bOverrideScaleformAllocator` 皆為 `true`。這會讓 RaceMenu 的 CBBE morph 調一兩次後就失效（Nexus 109080 的說明），要改設定或裝 109080。
- 隨從／NPC：RaceMenu 不能直接捏 NPC，改用下文「逐 NPC 指定」。
- 臉不歸這裡：RaceMenu 的臉部滑桿、preset（`.jslot`）與固化成 NPC patch 層走 [racemenu](../racemenu/README.md)。

**BodySlide 視窗**：適合全域基準或某個 NPC 的固定樣子。在 MO2 的 Executables 新增 `Data/CalienteTools/BodySlide/BodySlide.exe`（實體在 `BodySlide and Outfit Studio 5.8.2` mod；改 `ModOrganizer.ini` 屬 `instance/`，由使用者或部署線做）。舊版 wine 下 preset 下拉曾空白（[lesson](../../lessons/faces-troubleshooting.md#bodyslide-wine-preset-empty-nam7-weight)），待實機。視窗裡**只存 preset、不按 Build**：Build 會落到 `overwrite/`，蓋過所有 `BSO-*` 層。preset 經 MO2 存進 `overwrite/CalienteTools/BodySlide/SliderPresets/<檔名>.xml`；告訴 agent 檔名與 preset 名，當基準就改 `base_preset`，給 NPC 用就加進 `obody.npc_presets`（新 `run` 的 stage 會收進 overwrite，或用 `preset_files` 點名）。

headless 建置跑在 staging 的私有 prefix 與 bwrap 唯讀沙箱，讀 staging 當下的複本，不會和 GUI 改到同一個檔；只會搶 CPU，而 GUI 之後才存的 preset 要重 stage 或列進 `preset_files`。

**怎麼選**：自己的角色在遊戲內捏，所見即所得。全域基準與 NPC 固定形在 BodySlide 存 preset，交給設定檔重建。
