# 二、Animated Carriage — 做什麼 + 怎麼運作

← [原文入口](../animated-vehicles.md)

## 二、Animated Carriage — 做什麼 + 怎麼運作

**做什麼**：在 Tamriel 各 Hold 之間，沿預鋪路徑出現「馬拉著走的馬車」radiant 事件（含囚車、商隊、婚禮、葬禮、衛兵、敵對劫車等變體），馬車跑到終點站變回靜態擺設、乘客下車；玩家也能 activate 上車跟著跑。

**核心機制 = linked-ref 路徑節點鏈 + `TranslateToRef` 平移 + radiant quest 工廠生成**：

<!-- wf-nav -->
1. **路徑 = 一串放在世界裡的 marker Activator，用 `GetLinkedRef()` 串成 linked list**。
   在 `ACLine_Whiterun.esp` 裡看得最清楚：大量 `PlacedObject`，base 是 `zxACCartMarker01/02`（`[0009DC]/[0009DE]`，model 是 `CarriageMarker0X.nif`），**每個 ref 都帶 `linkedRef → 下一個節點`**。`StartMarker → … → ENDMarker` 即一條路線；節點還能掛 `kwAlternativePath` 第二條 linked-ref 做 50% 機率分岔。
2. **`zxAC_StartMarkerScript`（marker 上的腳本）= 觸發器**：`OnCellAttach`/距離 <6000 時依日夜 + global 機率（`zxACgEventChanceDay/Night`）擲骰，從 FormList 抽一個 radiant 旅程 Quest，`Reset()`→`Start()`，並把自己當 start point 餵給它（`SendStartPoint(self)` + HoldLocation + CrimeFaction + sprint flag）。`gCarriageLine` global 當「這條線正在用」的鎖。
3. **`zxAC_RqBaseScript`（旅程 Quest 腳本）= 移動本體**：
   - `CreateCart()`：`StartPoint.PlaceAtMe(...)` 從 cart-type/horse-type FormList **動態生成**一台 cart Activator ref（`zxACCartA05Shadowmere` 之類，base 也是 Activator + 自帶動畫 NIF）。
   - `GoToNextMarker()` → `CartRef.TranslateToRef(NextMarker, fSpeed, …)`：**引擎平移把整台 cart ref 搬向下一節點**。
   - cart 的 `OnTranslationAlmostComplete` → 回呼 `UpdateCartMoving()` → `SetNextMarker()`（沿 `GetLinkedRef()` 走下一格）→ 再 `TranslateToRef`。如此沿節點鏈一格一格走，這是**引擎驅動的真實 ref 移動**，跟船完全不同。
   - 到 ENDMarker：`GenerateStaticCartAt`（放靜態 cart 擺設 `zxACCartStatic*`）+ `GenerateHorseMarkerAt` + `GenerateLivingHorseAt`（`PlaceAtMe` 一匹真馬 Actor + `SetOutfit` 換皮 + `SetVehicle(HorseMarker)`），cart ref `Disable`，乘客 `ExitPassenger` 下車；全程結束 `RemoveCarriage` 把所有臨時 ref `Delete`。
4. **乘客系統（多個 alias 腳本）**：
   - `zxAC_PassengerAliasScript`：用 `SetVehicle(CartRef)` 把 Actor 綁到 cart（vanilla 載具機制），加友善 faction、設 crime faction；監聽動畫事件 `ExitCartEnd` 下車、`RemoveCharacterControllerFromWorld` 處理 ragdoll；被玩家/衛兵攻擊就 `StopCartAtCurrentLoc` 停車並轉敵對。
   - `zxAC_PlayIdleOnCartAliasScript` + `zxAC_MgEPlayIdleOnCart`（ActiveMagicEffect）：用一個 **Spell（FormList 隨機抽）** 當載體，magic effect 觸發時 `Debug.SendAnimationEvent(MyRef, "IdleSitCrossLeggedEnterInstant" / "IdleJarlChairEnterInstant" / …)` — **車上坐姿全是 vanilla idle 動畫事件名，不是自製 HKX**。另有 `Idle Property IdleCartDriverSway` 等一票 Idle records 做車身搖晃姿態。
5. **`zxAC_ManagerQuestScript`（單例 manager Quest）= 工廠 + 工具庫**：`GenerateCart/StaticCart/HorseMarker/LivingHorse`、`MovePassengerTo/EnablePassenger/SetPassengerOn/ReplaceVehicle/ExitPassenger`、token 計數等，全靠 keyword + FormList 查表（cart type → horse type → 具體 base 的多層 FormList）。

**玩家怎麼搭**：activate 跑動中的 cart（`bRidable`）→ `MoveOnCart` 把玩家 spline 到 `RidingNode<seat>` → 用 `SetVehicle` 綁定 → 隨 `TranslateToRef` 一起被搬到終點。

---

