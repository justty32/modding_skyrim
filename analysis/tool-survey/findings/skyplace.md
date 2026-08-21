# SkyPlace — Tool Survey Finding

**Nexus**: https://www.nexusmods.com/skyrimspecialedition/mods/149455

**Source**: https://github.com/QTR-Modding/SkyPlace-SKSE

**Author**: SkyrimThiago / QTR-Modding | **Version**: 1.4.1 | **License**: 未找到

**Surveyed**: 2026-08-21（Nexus 事實沿用已查證交接；GitHub `main` 原始碼檢視）

相關主線：[SkyrimIngameEditor — Tool Survey Finding](skyrim-ingame-editor.md)。

---

## 結論

SkyPlace 是成熟度相當高的**玩家向 runtime reference 操作器**，不是能產出 mod plugin 的
遊戲內 editor。它能選取、搬動、旋轉、縮放、群組、收進物品欄再放回物件，也會讓結果跟著
特定存檔延續；但原始碼中沒有 ESP writer、record serializer 或可交給 ModForge 的輸出格式。
因此它不能取代 SkyrimIngameEditor 的 EspGenerator，也不能取代
Godot Worldspace Editor → ModForge 的可重建 REFR/LAND pipeline。

| 問題 | 判定 |
|---|---|
| Feature 1：Reference 放置／移動 | ✅ runtime 操作完整；包含多選、群組、碰撞／貼地處理與物品欄往返 |
| Feature 2：LAND 地形編輯 | ❌ 沒有 LAND／heightmap 編輯路徑 |
| ESP 匯出 | ❌ 沒有 |
| 持久化 | ✅ 存檔綁定；runtime reference state 由遊戲存檔承接，群組 metadata 另寫 `<save>_Place.bin` |
| 原始碼／授權 | 原始碼公開；repo 未提供 LICENSE／COPYING，GitHub Community Standards 也未列 License |

---

## Feature 1：實際放置／移動機制

### 選取

`Picker::Tick()` 每次 tick 從 gameplay camera 做 `RayCast::Cast(..., 500)`，由命中的
`NiAVObject::GetUserData()` 取得 `TESObjectREFR` handle，再以 `Shader::IsMovable()` 的
heuristic 決定是否可操作；它是**準星／相機物理射線**選取，不是
SkyrimIngameEditor `TargetManager` 呼叫 `Console::SelectReference(screenX, screenY)` 的
任意螢幕座標 console pick。

### 移動與變形

`Placer::Tick()` 持續向相機前方 raycast，把命中點當 placement position；
`ApplyGroupTransform()` 對單一或多個 reference 呼叫 `Transform::SetPosition()`、
`Transform::SetAngle()`、`TESObjectREFR::SetScale()` 並同步 3D/Havok collision，完成時
`FinishGroupMove()` 用 `Transform::Wrap()` 固化位置。`Transform::Wrap()` 對一般 world
reference 走遊戲內部 `MoveTo`，必要時處理跨 cell／multibound；對 inventory object 則直接
更新 position／angle。

### 「帶著走」不是 authored REFR 新建

`ObjectGroup::PickUp()` 會把選中 references 的 base FormID、相對 transform、scale 與物品欄
內容整理成 group，建立 runtime `TESObjectMISC`，把 group item 放進玩家物品欄，然後
disable/delete 原 references。`ObjectGroup::Materialize()` 放回時用
`PlayerCharacter::PlaceObjectAtMe()` 建立 runtime references，再套回相對 transform。

這證明 SkyPlace 已解掉玩家操作層的「選取 → 群組 → 搬動／縮放 → 放下」問題，但這些
reference 是遊戲執行期物件；它沒有建立可提交到 plugin 的 `IPlacedGetter`／REFR record。

### 與 SkyrimIngameEditor 的一句話差異

SkyPlace 以準星物理 raycast 選取並直接操縱／重建 runtime references；
SkyrimIngameEditor 以 `Console::SelectReference` 做螢幕座標選取，再由 ImGui
`ReferenceTransformEditor` 編輯並把 form 排入 ESP 序列化流程。

---

## 持久化與 ESP 匯出

### 有存檔持久化，但不是 ESP

SkyPlace 的 `SaveGameHook` 在 Skyrim 儲存前取得 `.ess` 完整路徑並呼叫
`Persistence::Save()`；後者把副檔名改成 `_Place.bin`。`LoadGameHook` 載入同名 sidecar。
binary version 7 保存 group item、member base FormID、相對位置／旋轉／縮放、preview
transform、inventory chest FormID 與 HUD 狀態。一般 world reference 的 transform 則是用
遊戲 runtime `MoveTo`／transform API 修改，隨該 save 的 reference change state 保存。

因此答案分兩層：

- **能持久化**：不是只活到關遊戲；結果綁定 `.ess` 與其 `_Place.bin` sidecar。
- **不能匯出 ESP**：repo 沒有 ESP writer、Mutagen、JSON record serializer、plugin master
  收集或 export command；`Persistence` 寫的是 SkyPlace 私有 binary group metadata，不是
  TES plugin records。

這條路徑不能產生可安裝、可版控、可跨存檔重現的場景 patch，所以對「取代 CK 編輯流程」
沒有直接交付價值。

---

## 原始碼與授權

- Source repo：[`QTR-Modding/SkyPlace-SKSE`](https://github.com/QTR-Modding/SkyPlace-SKSE)
- 授權：**找不到**。2026-08-21 檢查 repo root 沒有 `LICENSE`、`LICENSE.md`、`COPYING`，
  GitHub Community Standards 的 License 項也未完成。
- 影響：source 可讀不等於獲准複製、修改或散布。未取得作者明示授權前，只能把它當行為與
  架構參考，不能把程式碼借進 MIT 的 SkyrimIngameEditor 或本專案元件。

---

## 對 SkyrimIngameEditor 擴展優先序的影響

既有優先序**不改**：

1. **存檔／匯出按鈕仍是第一**：SkyPlace 沒有 ESP 輸出，不能省掉這段。
2. **Reference 新建仍要做**：SkyPlace 的 `PlaceObjectAtMe()` 可證明 runtime placement
   互動可行，但不能替代 authored REFR + `EnqueueForm` + master 收集。
3. **Reference 刪除仍要做**：SkyPlace 的 disable/delete 是 savegame state，不是 plugin
   deleted override。
4. **LAND 工作完全不變**：SkyPlace 沒有地形資料模型、筆刷或 LAND serializer。

能省的是**互動設計探索**，不是 SIE 的 editor/export 實作：準星 raycast、可移動 heuristic、
多選 group transform、floor clipping、collision scale、跨 cell/multibound 與鍵鼠／手把操作，
都已有可觀察的參考實作；但因 repo 無授權，目前只能重新實作概念，不能直接搬碼。

---

## 與 Godot Worldspace Editor／ModForge 的關係

| 對象 | 關係 | 理由 |
|---|---|---|
| `projects/godot-worldspace-editor` | 只在「人眼擺物件」UX 層局部競合；不是 end-to-end 競品 | Godot editor 離線輸出 `placements.json`／heightmap／splatmap，可重建且涵蓋 LAND；SkyPlace 只改特定遊戲存檔的 runtime references，沒有 LAND 或交換格式 |
| ModForge | 目前無直接整合 | ModForge 消費結構化 spec／`placements.json` 並生成 REFR/LAND/ESP；SkyPlace 沒有可供消費的 export。若未來另做 capture/serializer bridge，它的遊戲內 transform UX 才可能成為輸入前端 |
| 可借用元件 | 目前不能直接借碼 | repo 無明示授權，且 Nexus 所述 modder API 仍是 coming soon；可借的是經重新實作的 interaction ideas，不是現成合法元件 |

---

## 原始碼依據

- 選取／raycast：[`src/Picker.cpp`](https://github.com/QTR-Modding/SkyPlace-SKSE/blob/main/src/Picker.cpp)，
  `Cast()`、`Picker::Tick()`
- runtime transform／放置：[`src/Placer.cpp`](https://github.com/QTR-Modding/SkyPlace-SKSE/blob/main/src/Placer.cpp)，
  `Placer::Cast()`、`ApplyGroupTransform()`、`FinishGroupMove()`；
  [`include/Transform.h`](https://github.com/QTR-Modding/SkyPlace-SKSE/blob/main/include/Transform.h)，
  `MoveTo_Impl()`、`Wrap()`
- group pickup／materialize：[`src/ObjectGroup.cpp`](https://github.com/QTR-Modding/SkyPlace-SKSE/blob/main/src/ObjectGroup.cpp)，
  `ObjectGroup::PickUp()`、`ObjectGroup::Materialize()`
- save sidecar：[`src/Hooks.cpp`](https://github.com/QTR-Modding/SkyPlace-SKSE/blob/main/src/Hooks.cpp)，
  `SaveGameHook`、`LoadGameHook`；
  [`src/Persistence.cpp`](https://github.com/QTR-Modding/SkyPlace-SKSE/blob/main/src/Persistence.cpp)，
  `Persistence::Save()`、`Persistence::Load()`
- 授權缺口：[`GitHub Community Standards`](https://github.com/QTR-Modding/SkyPlace-SKSE/community)
