# 18. 技術實戰：透過 NPC 模板生成實體

在製作召喚類、同伴類或動態世界模組時，你經常需要從一個現有的數據藍圖（`TESNPC`）生成一個實體（`Actor`）。

> **2026-10-23 更正**：本檔舊版在 C++ 範例裡寫 `PlaceAtMe()` 與 `SetPlayerTeammate()`，那兩個是 **Papyrus** 函式名，CommonLibSSE-NG 的 C++ 介面沒有同名成員（實證見文末「API 實證」節）。已改為正確的 C++ API。

## 1. 核心概念：`TESNPC` vs `Actor`
-   **`RE::TESNPC`**: 這是靜態數據（模板），定義了對象的臉、預設屬性、種族和技能。
-   **`RE::Actor`**: 這是世界中的實體，是基於模板生成的具體對象。

生成實體有兩條路，差別在「用現成的 `TESNPC`」還是「跑出一個新的 `TESNPC`」：

| 路線 | 做法 | 適用 |
|---|---|---|
| A. 直接用現成模板 | `LookupByID<RE::TESNPC>()` 拿到既有 NPC，直接生成 | 召喚衛兵／狼這類「複製既有角色」 |
| B. 複製出新的動態模板 | `IFormFactory` 造新 `TESNPC`，再 `Copy()` 既有模板，改名改屬性後生成 | 要改名字／屬性，又不想動原始 NPC |

## 2. 路線 A：用現成模板召喚一個自定義衛兵

```cpp
#include <RE/Skyrim.h>
#include <SKSE/SKSE.h>

void SpawnNPCAtPlayer() {
    auto player = RE::PlayerCharacter::GetSingleton();
    if (!player) return;

    // 1. 獲取 NPC 模板 (PlaceHolder ID: 0x00012E46 - 雪漫城衛兵)
    auto npcBase = RE::TESForm::LookupByID<RE::TESNPC>(0x00012E46);
    if (!npcBase) return;

    // 2. 在玩家位置生成實體
    //    參數：要生成的 TESBoundObject, 是否強制持久化
    //    回傳：NiPointer<RE::TESObjectREFR>
    auto spawnedRef = player->PlaceObjectAtMe(npcBase, false);
    if (!spawnedRef) return;

    // 3. 轉換為 Actor 以執行進階邏輯
    auto newActor = spawnedRef->As<RE::Actor>();
    if (!newActor) return;

    // 讓他立刻變成玩家的盟友
    // C++ 沒有 SetPlayerTeammate()，要直接設 BOOL_BITS 旗標
    newActor->GetActorRuntimeData().boolBits.set(RE::Actor::BOOL_BITS::kPlayerTeammate);

    // 改過 AI 相關狀態後刷新行為
    newActor->EvaluatePackage();

    RE::DebugNotification(fmt::format("已召喚: {}", newActor->GetName()).c_str());
}
```

## 3. 路線 B：複製模板造一個新的動態 NPC

不想逐項硬寫屬性時，挑一個基底 NPC（例如 `Player 0x00000007` 或 `EncCitizen01`）複製。

```cpp
// 1. 取得模板與工廠
auto* templateNPC = RE::TESForm::LookupByID<RE::TESNPC>(0x00000007);  // Player
auto* factory = RE::IFormFactory::GetConcreteFormFactoryByType<RE::TESNPC>();
if (!templateNPC || !factory) return;

// 2. 造新的動態 TESNPC 並複製模板資料
auto* newNpcBase = factory->Create()->As<RE::TESNPC>();
if (!newNpcBase) return;
newNpcBase->Copy(templateNPC);        // TESNPC::Copy(TESForm*) override
newNpcBase->fullName = "Generated Citizen";

// 3. 生成，並用三角函數推到施法者前方，避免跟施法者重疊
auto spawned = caster->PlaceObjectAtMe(newNpcBase, false);
if (spawned) {
    float angleZ = caster->data.angle.z;
    RE::NiPoint3 forward(std::sin(angleZ), std::cos(angleZ), 0.0f);
    spawned->SetPosition(caster->GetPosition() + (forward * 150.0f));
    spawned->SetAngle(caster->data.angle);
    spawned->As<RE::Actor>()->EvaluatePackage();   // 套用模板帶來的 AI package
}
```

**不要用 `TESDataHandler::CreateReferenceAtLocation` 生動態 NPC**：它要你自己備齊 cell／worldspace／linked-room handle 等 10 個參數（`include/RE/T/TESDataHandler.h:77`），而 `PlaceObjectAtMe` 會替你處理 3D 初始化與 cell 掛載。

## 4. 關鍵 API 標註（C++ / CommonLibSSE-NG）
-   **`RE::TESNPC`**: NPC 的基礎數據類別。`include/RE/T/TESNPC.h`
-   **`PlaceObjectAtMe()`**: 最核心的生成函數。`include/RE/T/TESObjectREFR.h`
-   **`TESNPC::Copy()`**: 從另一個 form 複製資料。`include/RE/T/TESNPC.h`
-   **`IFormFactory::GetConcreteFormFactoryByType<T>()`**: 取得某 form type 的工廠。`include/RE/I/IFormFactory.h`
-   **`Actor::BOOL_BITS::kPlayerTeammate`**: 隊友旗標（C++ 只有 `IsPlayerTeammate()` 讀取器，沒有設定器）。`include/RE/A/Actor.h`
-   **`Actor::EvaluatePackage()`**: 重新評估 AI package。`include/RE/A/Actor.h`
-   **`RE::DebugNotification()`**: 左上角提示。`include/RE/M/Misc.h`

## 5. 實戰建議
-   **位置偏移**: 務必用 `SetPosition()` 把實體推離施法者，否則會疊在一起（見路線 B 的三角函數寫法）。
-   **Null 檢查**: `factory`、模板、`spawned` 三者都要檢查，少一個就可能是啟動期 CTD。
-   **等級同步**: 動態生成的 NPC 默認會根據模板的等級規則自動縮放（Scaling）。
-   **Handle 安全**: 跨 frame 追蹤生成物請存 `RE::ObjectRefHandle`，不要存裸指標。
-   **動態 FormID 會漂**: `0xFF` 段的動態 form 在存檔／讀檔後 ID 可能改變，別把它寫進設定檔。
-   **回收**: 對於動態生成的 NPC，務必使用 `SetDelete(true)` 進行清理，避免存檔中累積過多「死掉的衛兵」。（參考高級教學 13：回收機制）

## 6. API 實證（為什麼不是 `PlaceAtMe`）

`PlaceAtMe` 與 `SetPlayerTeammate` **都是真的函式，但屬於 Papyrus，不屬於 C++**。兩邊不是「誰對」，是分屬兩個介面：

| 介面 | 生成 | 設隊友 | 憑據 |
|---|---|---|---|
| Papyrus | `ObjectReference Function PlaceAtMe(Form akFormToPlace, int aiCount = 1, bool abForcePersist = false, bool abInitiallyDisabled = false) native` | `Function SetPlayerTeammate(bool abTeammate = true, bool abCanDoFavor = true) native` | `external/frameworks/SkyrimNet-GamePlugin/headers/ObjectReference.psc:104`、`Actor.psc:175` |
| C++（CommonLibSSE-NG） | `NiPointer<TESObjectREFR> PlaceObjectAtMe(TESBoundObject* a_baseToPlace, bool a_forcePersist) const;` | 無設定器，只有 `IsPlayerTeammate()` 與 `BOOL_BITS::kPlayerTeammate` 旗標 | `include/RE/T/TESObjectREFR.h:454`、`include/RE/A/Actor.h:616`／`:188` |

舊版那行 `player->PlaceAtMe(npcBase, 1, false, false)` 的四個參數跟 Papyrus 簽章一字不差，可見是把 Papyrus 寫法直接搬進 C++ 範例。在 CommonLibSSE-NG 標頭全文搜尋 `PlaceAtMe`，唯一命中是條件函式編號 `kPlaceAtMe = 37`（`include/RE/T/TESCondition.h:75`），沒有任何成員函式。
