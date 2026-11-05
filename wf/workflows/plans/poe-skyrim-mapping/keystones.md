# keystone：48 個規則型 keystone 的方案與分批

[README](README.md)｜[decisions](decisions.md)｜[mechanics](mechanics.md)｜[phases](phases.md)

48 個 keystone 中，第一批施工 38 個（真規則 29、近似 9）；自創 9 個加上 Supreme Ego 共 10 個延後，上線前用 5 份通用加成佔位。討論稿與分組推薦在 poe-keystones（已刪，取回：`git -C agentctl show bf38e9c9e017:handoffs/home-2026-11-03/poe-keystones/REPORT.md`）。

## 資料檔

已抽到 [keystones.json](data/keystones.json)（48 列）。本檔是現行正本，複製自 poe-keystones 線的產出；之後的裁示與施工狀態改在本計畫的這份。欄位：

- `node_id`、`分組`（G1–G6）、`名稱`、`PoE原文`（3.29.1 全部 stat 行）、`白話`。
- `正面方案`：含落地路線。`負面與建議`、`負面建議`：保留／改寫／無。
- `依賴機制`、`工作量`（`*`＝只算共用系統上的增量）、`推薦`。
- `exclusive_with`：互斥對象與組號。`施工批次`。`佔位`：延後案的 5 份 atom 拆分。

統計：推薦為真規則 29、近似 9、自創 9、待重新設計 1；負面為保留 23、改寫 18、無 7；工作量 S 14、S\* 9、M 8、M\* 15、L 1、待定 1。

## 共通裁示（使用者已定 2026-11-03）

原話：「1.a,2.b,3.yes,4.a,5.按照建議」。

1. 負面效果保留原意，做不到才改寫。
2. 「只能造成 X 傷害」改成非 X 傷害 −50%；自創的 Roiling Tempest 不適用。
3. 互斥：要，共 6 組、18 個 keystone（逐列在 `exclusive_with`）：
   - X1：Resolute／Precise Technique × Elemental Overload／Perfect Agony
   - X2：Bitter Frost × Avatar of Fire／Voracious Flame
   - X3：Chaos Inoculation × Blood Magic／Vaal Pact／The Agnostic
   - X4：Blood Magic × Mind Over Matter／Eldritch Battery／The Agnostic
   - X5：The Agnostic × 6 個護盾 keystone
   - X6：Ghost Reaver × Wicked Ward／Vaal Pact
4. AI 不懂的規則一視同仁，例如 Chaos Inoculation 對隨從也把生命鎖在 1。隨從可能猝死或不出手（Blood Magic 魔力為 0），使用者接受。
5. 施工先後：先做 ESL＋受傷管線 hook，再做護盾。

## 施工分批

第一批依共用系統排序，每個 keystone 取它的依賴中最後上線的那一個（逐列在 `施工批次`）：

| 段 | 依賴切片 | 個數 |
|---|---|---:|
| K1 ESL＋受傷 hook | S4、S5 | 18 |
| K2 護盾 | S9 | 8 |
| K3 異常載具 | S10 | 8 |
| K4 charge | S11 | 2 |
| K5 召喚物 | S12 | 2 |

第一批的 keystone 在自己那段上線前，走 family-rules 的通路規則（HP 0.4＋SP 0.3＋AR 0.3）。

## 延後的 10 個

原話：「這些自創規則啥的，我們可以後續慢慢更新加上，不急著做」。

- 9 個自創案（Solipsism、Versatile Combatant、Iron Reflexes、Acrobatics、Roiling Tempest、Ancestral Bond、Runebinder、Hex Master、Bloodsoaked Blade）與 Supreme Ego（待重新設計），之後逐個和使用者討論；Vaal Pact 的「吸血鬼之約」備案一併討論。
- 上線前用 `佔位` 欄的 5 份通用加成：依主題拆 2 個 atom，每份取 [atoms.json](data/atoms.json) 的值。
- Roiling Tempest 維持原案，不加非雷電 −50%（使用者回「隨意」，頂層代選）。

## 施工前要核實

perk entry 與條件函式名稱是憑 CK 知識寫的，施工前對照 <https://ck.uesp.net/wiki/Perk_Entry_Point> 核實；Call to Arms 的玩家端 entry 待查。3.29 原文與舊記憶不同（例如 Conduit 沒有負面、Glancing Blows 是 65%），以資料檔為準。
