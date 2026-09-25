# jks-skyrim-setdressing — modforge-verdict

← [調查入口](../jks-skyrim-setdressing.md)

## ModForge meaning（直指 #22 與 Godot editor）

**設定 idea #22「漂泊開拓慢活：有人住的otherworld聚落」要的「看起來被使用的空間」，本質就是 placement-volume 問題——而 ModForge 的 placement pipeline 已完全覆蓋這條低階機制：**

- **REFR 置放 + PlacementSpec 六欄**（Scale / InitiallyDisabled / EnableParent / Lock / Ownership / Count）+ **vanilla cell override** + map marker — 全 landed（`world.md`）。JK's 用到的每一欄 ModForge 都生得出來；ModForge 還多了 EnableParent/gate 旋鈕，正好補 JK's「靜態無狀態」的弱點。
- **Static base + TextureSet 改皮** — 可生成。
- **新 interior cell from-scratch + vendor faction + merchant container + 店主 NPC/package** — 全 landed。
- **NavMesh override**（custom NAVM+NAVI）— landed（記憶 `programmatic-navmesh`）；這是 set-dressing 量產時**必須一起生**的配套。

**真正的契合點 = Godot worldspace editor 就是 set-dressing 的天然 authoring 前端。** [`projects/godot-worldspace-editor`](../../../../../projects/godot-worldspace-editor/README.md) 的匯出格式 `placements.json`（`base / position(m) / rotation(rad) / scale / instanceId?`）與本調查 `cellrefs` 倒出的 cell 內容**逐欄 1:1**——JK's 那 106 筆/cell 的雜物擺放，正是「在 WYSIWYG 編輯器裡 hand-place 或 GDScript 程序化散佈」最適合做的事，做完一鍵 `godotPlacements: {$include}` 掛進 worldspace spec → ModForge 生 REFR。**JK's 是用 CK 手刷出來的；ModForge + Godot editor 是這套手藝的可腳本化替代前端。**

對照兩種 set-dressing 路線：
| | JK's（本檔，靜態）| BOS（[base-object-swapper](../../frameworks-tools/base-object-swapper.md)，runtime）|
|---|---|---|
| 機制 | cell override 寫死 REFR | SKSE 載入時依 ini 條件換 base |
| 狀態化 | ✗（佈景固定）| ✓（可條件/機率/時段）|
| ModForge 對接 | placement pipeline + Godot editor（生 REFR）| 生 BOS `_SWAP.ini`（純設定，見該檔）|
| #22 用途 | 把新聚落一次塞滿、定調 | 讓佈景隨開拓進度演變 |

→ #22 的 set-dressing 需求 = **placement-volume 問題，ModForge 既有 pipeline 已能解，最佳 authoring 工具是 Godot worldspace editor**；若要「會變化的聚落」再疊 BOS 輸出。與 population sibling 合看：#22 一個聚落 = `settlementPopulation:`（活人，見 populated-skyrim finding 的 GAP）＋ Godot-placed set-dressing（物件密度）＋ navmesh。

風險：① REFR 數爆漲快（單城就上千），量產要 count 上限 + navmesh-safe 紀律；② cell/worldspace/navmesh override 衝突面大，與其他城市 mod 不相容是常態（patch 文化）；③ 靜態密度 ≠ 狀態，別誤當模擬。

## Verdict

**可借鏡（高，系統面）／需相容（外部 mod 衝突面）**。敘事價值無，但它是 #22「讓聚落看起來有人在用」的 placement-volume 活範本：低階機制 ModForge 100% 已具備，**天然 authoring 工具就是 Godot worldspace editor**（`placements.json` 與 cellrefs 逐欄對得上）。模組化 per-city 版本同 pattern、只是範圍切片。與 [populated-skyrim-family.md](../populated-skyrim-family.md)（活人那半）、[base-object-swapper.md](../../frameworks-tools/base-object-swapper.md)（狀態化那條路）合看，構成 #22 聚落的完整佈置藍圖。
