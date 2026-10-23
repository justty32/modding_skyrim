# 12. 技術實戰：環境生成與地形調整

本教學教您如何調整既有物件高度、在指定位置生成自然景觀（山石、樹木），並討論動態地形修改的技術邊界。

> **2026-10-23 更正**：本檔舊版範例寫 `player->PlaceAtMe(...)`（Papyrus 簽章）與 `SetAngle(0,0,rot)`（C++ 只吃 `NiPoint3`），另外引用了不存在的 `SKSE::GetCrosshairRef()`。已改為正確的 C++ API，實證見文末。

## 1. 調整既有物件的 Z 高度

要把準星指到的物件抬高或壓低，先拿到該 reference，再更新它的 3D 位置。

```cpp
auto* target = GetCrosshairTarget();   // 見下方「取得準星目標」
if (target) {
    auto pos = target->GetPosition();
    pos.z += 50.0f;                    // 抬高 50 單位
    target->SetPosition(pos);
}
```

此修改只作用於當前 cell 的那一個 reference；要持久化，該 cell 的修改狀態會存進存檔。

### 取得準星目標

CommonLibSSE-NG **沒有** `SKSE::GetCrosshairRef()` 這個函式。準星目標要自己維護：訂閱 `SKSE::CrosshairRefEvent`（`include/SKSE/Events.h:30`），事件源由 `SKSE::GetCrosshairRefEventSource()`（`include/SKSE/API.h:36`）取得，在 handler 裡把 `ObjectRefHandle` 存下來備用。

## 2. 生成自然景觀 (山石與樹木)

在 C++ 中生成樹木或石頭與生成床鋪邏輯一致，但需要注意「碰撞」與「地面貼合」。

### A. 用 EditorID 查找比 FormID 穩

FormID（如 `0x38432`）在不同載入順序下可能對不上；EditorID 查找穩定得多，而且可以寫 fallback。

```cpp
auto* treeBase = RE::TESForm::LookupByEditorID<RE::TESBoundObject>("TreeFloraJuniper01");
if (!treeBase) {
    treeBase = RE::TESForm::LookupByEditorID<RE::TESBoundObject>("RockPileM01");
}
```

（舊版用的 FormID 佔位值留作對照：`0x00038432` 某種松樹 Static Tree、`0x0001B983` 某種大山石 Static Rock。要用 FormID 就走 `LookupByID<RE::TESBoundObject>()`。）

### B. 生成並推到玩家前方

```cpp
void SpawnEnvironmentDecor() {
    auto player = RE::PlayerCharacter::GetSingleton();
    if (!player) return;

    auto* rockBase = RE::TESForm::LookupByEditorID<RE::TESBoundObject>("RockPileM01");
    if (!rockBase) return;

    // 用三角函數算出玩家正前方 200 單位的位置，避免生成物卡進玩家
    float angleZ = player->data.angle.z;
    RE::NiPoint3 forward(std::sin(angleZ), std::cos(angleZ), 0.0f);
    RE::NiPoint3 spawnPos = player->GetPosition() + (forward * 200.0f);

    // PlaceObjectAtMe(要生成的 TESBoundObject, 是否強制持久化)
    auto spawned = player->PlaceObjectAtMe(rockBase, false);
    if (spawned) {
        spawned->SetPosition(spawnPos);

        // 隨機旋轉讓景觀更自然；SetAngle 只接受 NiPoint3
        float randomRot = static_cast<float>(rand() % 360);
        spawned->SetAngle(RE::NiPoint3(0.0f, 0.0f, randomRot));
    }
}
```

### C. 為什麼一定要用 `PlaceObjectAtMe`

它一次處理掉三件自己做很容易漏的事：

- reference 正確掛到父 cell；
- NIF 模型載入並接進 scene graph；
- 物理與碰撞資料初始化。

## 3. 關於「調整地形」 (Terrain Sculpting)

**警告**：Skyrim 的地形（Heightmap）是由預生成的 `.btr` / `.bnd` 數據文件定義的，這與物體（Static Objects）不同。

### A. 在純插件中修改地形的困難點：
-   **靜態性**: 引擎在加載 Cell 時會將高度圖讀入物理內存，即時修改高度圖需要極深層次的內核 Hook。
-   **Navmesh 崩潰**: 修改地形後，導航網格（NPC 走路的路徑）不會更新，會導致 NPC 懸空或穿地。

### B. 常見的替代方案：
1.  **生成「地形補丁」**:
    如果你想讓地面隆起，不要去改高度圖，而是生成一個巨大的「地表紋理山石（Landscape Static）」。這就是大多數「築牆術」模組的做法。
2.  **使用 Decals (貼花)**:
    如果你只是想改變地面的視覺外觀（如燒焦、結冰），應使用 `RE::BGSDecalManager`。

## 4. 關鍵 API 標註
-   **`TESObjectREFR::PlaceObjectAtMe`**: 生成實體。`include/RE/T/TESObjectREFR.h:454`
-   **`TESForm::LookupByEditorID<T>`**: 以 EditorID 查 form。`include/RE/T/TESForm.h:247`
-   **`TESObjectREFR::SetPosition` / `SetAngle`**: 位置與旋轉，兩者都吃 `NiPoint3`。`include/RE/T/TESObjectREFR.h:464`／`:458`
-   **`TESObjectTREE`**: 專門處理具備風吹動畫的樹木類別。`include/RE/T/TESObjectTREE.h`
-   **`RE::NiPoint3`**: 用於計算生成位置。`include/RE/N/NiPoint3.h`
-   **`RE::BGSDecalManager`**: 地表貼花。`include/RE/B/BGSDecalManager.h`
-   **`SKSE::CrosshairRefEvent` / `SKSE::GetCrosshairRefEventSource()`**: 準星目標。`include/SKSE/Events.h:30`／`include/SKSE/API.h:36`

## 5. 實戰建議
-   **貼地對齊**: 移動後的物件可能浮空，必要時射線偵測找出真正的地面高度。
-   **Handle 追蹤**: 跨 frame 追蹤生成物用 `RE::ObjectRefHandle`，不要存裸指標。
-   **持久化**: `0xFF` 段的動態生成物若未正確標為持久或 cell 重載時不在存檔內，會被引擎回收。

## 6. 總結
在 Skyrim 中，「造山」和「種樹」其實都是在正確的位置 `PlaceObjectAtMe` 生成對應的靜態模型（Statics）。除非你是製作引擎級的編輯器，否則請避免直接嘗試修改引擎的高度圖數據。

## 7. API 實證

`PlaceAtMe` 是 Papyrus 的 `ObjectReference` 函式（`external/frameworks/SkyrimNet-GamePlugin/headers/ObjectReference.psc:104`），C++ 這邊的對應物叫 `PlaceObjectAtMe`，簽章是
`NiPointer<TESObjectREFR> PlaceObjectAtMe(TESBoundObject* a_baseToPlace, bool a_forcePersist) const;`（`include/RE/T/TESObjectREFR.h:454`）。
CommonLibSSE-NG 標頭全文搜尋 `PlaceAtMe` 只命中條件函式編號 `kPlaceAtMe = 37`（`include/RE/T/TESCondition.h:75`），沒有成員函式。
`SetAngle` 只有 `void SetAngle(const NiPoint3& a_angle);` 一個多載（`:458`），不存在三個 float 的版本。
同檔延伸討論見 [18. 透過 NPC 模板生成實體](NPC_18_Generating_NPC_From_Template.md)。
