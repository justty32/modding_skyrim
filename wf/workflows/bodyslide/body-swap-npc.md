# 逐 NPC 指定身形

[入口](README.md)｜[換身體](body-swap.md)｜[使用者自己捏身形](body-swap-self.md)｜[擬合](fit.md)

本頁由 [換身體](body-swap.md) 拆出，內容不變。

機制選 OBody NG 的 JSON（`npcFormID`），不另做 esp。選它的理由：

- 只要一個資產層，不改 plugin，換人只要改表。
- OBody 依 FormID 指定 preset，優先於 faction／plugin／race 與隨機（Aietos/OBody-NG `e33bbc1` 的 `Body.cpp` `GenerateActorBody`）。
- morph 透過 RaceMenu 同時套到裸身與帶 `.tri` 的裝備。

改用專屬身體 mesh／skin patch esp 只改得到裸身，裝備仍是共用的基準形，正好是這次要解決的問題。

設定檔 `obody` 段的 `npc_presets` 表：

```json
"npc_presets": [{"plugin": "Skyrim.esm", "formid": "01A696", "preset": "Kurone Big Change Body", "note": "Aela"}]
```

`bodyslide_rebuild.py obody` 依表產出獨立層 `<obody.layer>-<obody.revision>`，內容：

- 每個 preset 對應一個差量 preset `BSO <preset> (morph)`，值為 preset 減 `base_preset`，可為負值。OBody 與 skee 都不夾值（同 commit 的 `PresetManager.cpp` `SliderSetFromNode`；SKSE64Plugins `479ecab` 的 `BodyMorphInterface.cpp`）。
- 把該 NPC 寫進 `npcFormID`，並自動移出 `blacklistedNpcsFormID`（黑名單比指派先判斷）。
- 隨機池只留 `BSO Neutral`（零形），其餘 preset 全部列入 `blacklistedPresetsFromRandomDistribution`。隨機池不可以是空的：OBody 4.4.3 在隨機池為空時，連指定的 NPC 都不處理。
- `neutralize_tri` 會給「裸身已經烤成目標形」的私有身體放一個空 `.tri`，免得差量又推一次裸身。

要改某個 NPC：改表、`obody.revision` 換新值、只跑 `obody` 一步，裝備層不用重刷。

**流程**：使用者捏好並存成 preset → 告訴 agent「某 NPC 用某 preset」→ agent 改表重產 → 部署線換層 → 使用者進遊戲用 OBody MCM 的 reset actor（或 Reset Distribution）讓她重新套用。

**人工判斷點**：

- NPC 的身體家族：CBBE／3BA 才做得到，UNP 系與原版系拓樸不同，要先換身體。
- 私有身體有沒有 `.tri`，以及它是否已等於目標 preset。用頂點比對當證據，不相等時用 [擬合](fit.md) 反推 preset。
- preset 名與檔名不能含 OBody 會跳過的字（cloth、outfit、nevernude、bikini、feet、hands、push、cleavage、armor），工具會擋。
- 存檔裡已經記住的舊隨機 morph 不會自己消失，要在遊戲內 reset，並由使用者看結果。
