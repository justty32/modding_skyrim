# racemenu／bake — 固化成 patch 層與部署

[racemenu](README.md)｜[WORKFLOWS](../../WORKFLOWS.md)

段 6–7。**目標定位：臉的最終產物是 NPC patch 層**——ESP 裡的 NPC_ 臉部欄位，加上 `facegeom/<plugin>/<id>.nif` 和 `facetint/<plugin>/<id>.dds`。這樣臉不依賴存檔，換存檔、換 profile 都還在。

**本段全部未實作。「preset→NPC patch」的途徑待 `npc-face-patch` 報告定案**（報告路徑：`agentctl/handoffs/home-2026-11-22/npc-face-patch/REPORT.md`，報告出來後把結論吸收進本檔）。下面只記已知的對應關係和硬規則，供那條線與下一階段施工參考。

## 6. 固化

**主角**：選定的 jslot 收進一個 preset 層（例如 `RaceMenu Character Assets (private)` 那種層），檔放在 `SKSE/Plugins/CharGen/Presets/`，走 profile-change。

**NPC**（依據：調查 REPORT §6a）：

| jslot | NPC_ |
|---|---|
| `morphs.default.morphs` | NAM9 |
| `morphs.default.presets` | NAMA |
| `headParts` | PNAM |
| `actor.headTexture` | FTST |
| `actor.hairColor` | HCLF→CLFM |
| `tintInfo` | TintLayers＋QNAM |
| `actor.weight` | NAM7 |

- sculpt、custom morph、overlay 在 record 裡**沒有欄位**，只能烤進頭 NIF。
- 頭 NIF 的來源現在全斷：
  - 本機沒有 CK。
  - RaceMenu `ExportHead` 未驗證。
  - 沒有自製的烘頭工具。
- 候選途徑：
  - (a) 遊戲內 `ExportHead`，再用上架工具處理 NIF。
  - (b) PROTEUS 的 Copy Appearance 加 ExportHead。
  - (c) CK。
  
  由 `npc-face-patch` 定案。

硬規則（工作區踩過的，見 `wf/lessons/faces-facegen-consistency.md`、`faces-troubleshooting.md`）：

- facegen NIF 的 shape 名要和 HDPT EDID 一字不差。
- 部件數量要和 PNAM 對得上。
- 自訂種族不讀預烤 facegen。
- 層名用 ASCII。
- 不改來源 mod。

Done when（將來）：

- 層的 ESP 通過 `instance/tools/check_masters.py`，`present=no` 為 0。
- facegen 的 shape 名和 PNAM 一致。
- 和 `look_transplant/transplant.py --verify` 同等的檢查綠燈。

## 7. 部署與驗收

沿用 [profile-change](../profile-change/README.md)：

1. `instance/tools/layer_apply.py` dry-run。
2. 取得使用者授權。
3. apply。
4. 跑 `reverify.py`。
5. 依 [runtime-qa](../runtime-qa/README.md) 實機看臉。

Done when（將來）：遊戲內那個 NPC 不是灰臉或素頭，外觀和使用者選定的圖一致。外觀一致與否由使用者確認。

NPC 對 NPC 的整臉換現在就能做：走 [look-swap runbook](../../../agentctl/docs/look-swap-runbook.md)，產出的換臉層同樣適用本段 7。
