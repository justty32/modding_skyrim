# 三、共通模式 vs 差異

← [原文入口](../animated-vehicles.md)

## 三、共通模式 vs 差異

兩者**頂層思路相同**：載具 base 都是 **`Activator` + 自帶動畫 NIF**，乘客都用 **`SplineTranslateToRefNode` 黏到 NIF 的命名節點**（座位 / 甲板），都有**距離分級的 `RegisterForSingleUpdate` 效能節流**，都用 **global + 隨機擲骰**控制出現，坐姿都靠 **vanilla idle 動畫事件**。

最關鍵的差異在「**船 vs 車到底誰在動**」：

本表整理「三、共通模式 vs 差異」的逐項記錄。

已抽到 [record-patterns-and-modforge-mechanism-comparison.json](record-patterns-and-modforge-mechanism-comparison.json)（8 列）。

欄位「面向」：保留原表的面向。

欄位「Animated Ships」：保留原表的Animated Ships。

欄位「Animated Carriage」：保留原表的Animated Carriage。

統計：8 筆記錄，3 個欄位。


**串法總結**：兩者都不是用 vanilla Travel/Patrol package 在驅動移動。Package 在這兩個 mod 裡只是「讓 NPC 站在載具上擺對姿勢」的配角。真正的移動是：船＝美術（NIF 動畫），車＝Papyrus（`TranslateToRef` + linked-ref 鏈）。

---

## 四、關鍵 record 與資產（代表性）

<!-- wf-nav -->
- **載具 base（兩者）**：`Activator`，model 指向自帶動畫 NIF。
  - Ship：`[00081D] zxActDistantShipLong01` → `shiplongboat01.nif`（+ `zxShp_DistantShiptBase` script）
  - Cart：`[0009C2] zxACTESTCartAShadowmere2NS "Carriage"` → `Carriage02_Shadow.nif`（含 `activationSound`/`loopingSound`，keyword 標 cart-type/horse-type/`zxACCartIsRunning`）
- **路徑節點 base（Carriage 專有）**：`[0009DC] zxACCartMarker01` → `CarriageMarker01.nif`（marker 美術，放置後靠 `linkedRef` 串）。
- **路徑 placement（Carriage）**：`ACLine_Whiterun.esp` 的 `PlacedObject`，每筆 `placed obj → base 0009DC:AnimatedCarriage.esm @ (x,y,z)` + `linkedRef → 下一節點`。**這就是「一條路線 = 一堆帶 linkedRef 的 placement」的純資料表達**。
- **Idle / 動畫掛接**：
  - Ship NIF 命名節點：`ShipCenterNode` / `RidingShipNode0..N` / `RidingShipNodePlayer`（乘客座位）。
  - Cart NIF 命名節點：`RidingNode<seat>` / `HorsePosition`（馬位）。
  - 坐姿 = vanilla 動畫事件名（`IdleSitCrossLeggedEnterInstant`、`IdleJarlChairEnterInstant`…）＋ 一組 `Idle` records（`IdleCartDriverSway` 等）。
- **vendor（Ship）**：`zxSHSolitudeTraderFaction` 等 18 個 Faction 帶 vendor flag + `merchantContainer` + `sellBuyList`（沿用既有 vendor-faction 模式）。
- **內嵌動畫 vs 引擎驅動**：船體擺動 / 航行＝**NIF 內嵌（havok/NiController）**；車身位移＝**引擎 `TranslateToRef`**；車身搖晃姿態 + 兩者坐姿＝**vanilla idle 動畫事件（資料層）**。

---

## 五、對 ModForge 的參考價值

整體判斷：**「東西在動」這件事兩條路都不在 ModForge 的資料生成射程內**——船靠美術（NIF 動畫，屬 havok-blender 線），車靠一支不小的 Papyrus 狀態機。但**支撐它們的骨架幾乎全是 ModForge 該能生成的純資料**。

### 可生成（ModForge 資料層已涵蓋或接近）

<!-- wf-nav -->
- **載具 / marker 的 base records**：`Activator`（model NIF path、keyword、activation/looping sound）、`Static`、`Container`、`Faction`(vendor)、`Outfit`、`FormList`、`Keyword`、`GlobalShort`、`Idle` 引用 — 都是現成 spec record 類型。
- **vendor faction**（Ship 港船的 trader/fisherman）：與既有 vendor-faction 例子同型，直接可生。
- **NPC 上載具的站樁 Package**：兩者的主力 Package 全是 template `0x0654E2` 的 idle 模板。ModForge 的 `packages[]` 已是 template-driven（見 `docs/spec/SPEC-packages.md`）；只要先 `packagediag Skyrim.esm 0x0654E2` 拿到 slot schema，這類「在某 ref 上站樁/演 idle」就能掛上（與 SM/scene PlayIdle 筆記 `scene-playidle-recipe`、`dispatcher-magic-trigger` 的 idle/magic-effect 串法同源）。
- **idle 動畫事件掛接（坐姿）**：透過 magic effect 腳本 `Debug.SendAnimationEvent("Idle…EnterInstant")` 觸發，用的是 **vanilla 動畫事件名**——這層「掛接邏輯」屬腳本，但「掛哪個 idle、配哪個 magic effect / spell / FormList」是純資料，可比照既有 magic/scene 筆記生成。

### 需新支援（ModForge 目前缺，但屬資料層、值得補）

- **placement 的 `linkedRef`（最重要）**：Carriage 的整條路線就是「一串帶 `linkedRef` 的 `PlacedObject`」。目前 `docs/spec/SPEC-world.md` 的 `placements[]` 支援 `base/cell/worldspace/rotation/scale/persistent/enable-parent`，**但沒看到 linked-ref 欄位**。補一個 `linkedRef`（+ 具名 keyword 變體如 `kwAlternativePath`）就能讓 ModForge 直接生成「路徑節點鏈」這種資料結構——這跟 navmesh 筆記（`programmatic-navmesh`）、placement 既有能力是同一層，是高價值的小增量。
- **dynamic-spawn 的工廠資料**：cart/horse 的「cart-type → mode → horse-type 多層 FormList 查表」是純資料（巢狀 FormList），ModForge 已能生 FormList；要完整重現只差把這種「查表用 FormList 樹」當 pattern 記錄即可。

### 純參考（不打算讓 ModForge 生）

- **船體航行 / 浮動動畫**：NIF 內嵌 NiControllerSequence，屬美術資產（havok-blender 線），ModForge 不生 NIF。船的「移動」整個落在這裡。
- **載具移動狀態機（Carriage）**：`zxAC_RqBaseScript` 的 `TranslateToRef` + `OnTranslationAlmostComplete` 路徑遍歷、`PlaceAtMe`/`Delete` 生命週期、`SetVehicle` 綁定、ragdoll/敵對/停車分支——是一支完整的手寫 Papyrus radiant 系統，超出 spec 描述能力，屬「需手寫腳本 + 用 ModForge 生資料骨架」的混合工作流（可參考 dialogue/scene 筆記裡「ModForge 生 records、手寫 .psc 補邏輯」的既有分工）。
- **效能節流 / 排程細節**（距離分級 update、時段 bitmask）：純腳本實作層，參考即可。

### 一句話結論

ModForge 能把這兩個 mod 的**整副骨架**（Activator/marker base、FormList 查表、vendor faction、站樁 package、idle 掛接、以及——若補上 `linkedRef`——整條路徑節點鏈）當資料生出來；真正讓船浮動 / 讓車跑的那一層，分別歸給**美術（NIF 動畫）**與**手寫 Papyrus 狀態機**，ModForge 只負責餵料。
