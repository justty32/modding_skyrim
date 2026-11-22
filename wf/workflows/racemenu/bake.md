# racemenu／bake — 固化成 patch 層與部署

[racemenu](README.md)｜[WORKFLOWS](../../WORKFLOWS.md)

段 6–7。**臉的最終產物是 NPC patch 層**：ESP 裡的 NPC_ 臉部欄位，加上 `facegeom/<plugin>/<id>.nif` 和 `facetint/<plugin>/<id>.dds`。這樣臉不依賴存檔，換存檔、換 profile 都還在。

途徑已定案（`npc-face-patch` 報告 §4）：**主路線 A**＝主角在遊戲裡套 preset → skee 匯出頭 NIF＋tint → 離線上架；**備援 D1**＝Creation Kit Ctrl+F4。PROTEUS 只當遊戲內試戴，不產 patch。

## 6. 固化

**主角**：選定的 jslot 收進一個 preset 層（例如 `RaceMenu Character Assets (private)` 那種層），檔放在 `SKSE/Plugins/CharGen/Presets/`，走 profile-change。

**NPC**：一條指令，工具在 `agentctl/tools/npc_face/`（[tool-index](../../../agentctl/docs/tool-index.md)「NPC 臉 patch」列）：

```text
python3 agentctl/tools/npc_face/build_layer.py --jslot <preset>.jslot --npc <XXXXXX:定義plugin> \
    --staging ~/skyrim_mods/_staging-<日期>-npc-face [--head-nif X.nif --head-dds X.dds]
```

| 步 | 工具 | 狀態 |
|---|---|---|
| 6a jslot→NPC_ 欄位 | `jslot2npc.py`：forward 現役贏家 record，只換 PNAM、HCLF、NAM7、FTST、QNAM、NAM9、NAMA、Tint Layers；ESL；MAST＝贏家的 MAST＋贏家 | **可用**（合成載入序測試＋試點 Hatak→Muiri 實產） |
| 6b 匯出頭 | 觸發 ESP＋Papyrus（`npc_face/trigger/`）：`player.addspell` → 強制第三人稱 → `LoadCharacter`／`LoadPreset` → `ExportHead`／`SaveExternalCharacter` | **實機 4 場失敗**：觸發、GLOB、出檔都正常，但頭部件沒換（見下「實機紀錄」） |
| 6c 上架 | `facegen_install.py`：改名搬檔、slot 6 指向新 tint、根節點補名、shape gate（重用 look_transplant `shape_gate`）、DDS 格式、貼圖 VFS 解析 | **格式已用真匯出物驗**（根無名、512² 未壓縮 RGBA、slot 6 原值）；部件錯的匯出物 gate a 確實擋下 |
| 6d 組層 | `build_layer.py`：層目錄＋`.npc-face.json` manifest＋`layer_apply` manifest | **可用**；缺匯出頭時停在 exit 3，只出 record patch＋待補清單，`layer_apply` manifest 標 DRAFT |

jslot 對 NPC_ 的換算（實證者附依據，見 `jslot2npc.py` 檔頭）：

| jslot | NPC_ | 備註 |
|---|---|---|
| `headParts[].formIdentifier` | PNAM | `type` 欄**不是** HDPT 類型，不拿來驗 |
| `actor.hairColor`＝(R<<16)\|(G<<8)\|B | HCLF | 先找同色現成 CLFM，找不到在 patch 內新建 |
| `actor.weight` | NAM7 | `--keep-weight` 保留原值 |
| `actor.headTexture` | FTST | |
| `tintInfo[].texture` | TINI | 用貼圖路徑對 RACE tint 清單；jslot 的 `index` 不是 TINI |
| `tintInfo[].color` | TINC＋TINV | 最高位元組當不透明度（推論） |
| 膚色 tint RGB/255 | QNAM | |
| `morphs.default.morphs`／`presets` | NAM9／NAMA | |

- sculpt、custom morph、overlay 在 record 裡**沒有欄位**，只能靠匯出頭 NIF 帶過去；工具會出警告。
- 會報錯停手：jslot lint error、NPC 用 template traits、headpart 的性別旗標或 valid races 不含目標、tint 不在目標種族該性別清單、headpart 來自不在現役載入序或不在 master 集合的 plugin（`--allow-extra-masters` 才加 master）。
- **只有 record、沒有 FaceGen 的層不准部署**：舊 FaceGen 仍是贏家而 PNAM 已換，會素頭或錯臉。

硬規則（工作區踩過的，見 `wf/lessons/faces-facegen-consistency.md`、`faces-troubleshooting.md`）：

- facegen NIF 的 shape 名要和 HDPT EDID 一字不差；部件集合＝PNAM＋ExtraParts＋未被取代的種族預設件。
- FaceGen 資料夾用**定義** plugin（`Skyrim.esm`），不是 patch esp。
- 自訂種族不讀預烤 facegen。
- 層名用 ASCII；不改來源 mod。

### 6b 實機紀錄（2026-11-22 runtime-pilot，場 2–5）

| 場 | 做法 | 結果 |
|---|---|---|
| 2 | console `sexchange`＋`setrace`，觸發 `LoadPreset`（等 2 秒）→ 匯出 | 5 檔都出了；shape 是原主角 `MaleHeadImperial` 等 8 件＋女嘴 |
| 3 | 腳本先 `ForceThirdPerson`、等 5 秒；另在主角可見時重觸發 | 同上 |
| 4 | 腳本改 `LoadCharacter` → `LoadPreset` → `LoadCharacter` | 同上 |
| 5 | 主選單 `coc QASmoke` 新角色（Nord 男），同流程 | Nord 男預設件＋女嘴＋女眉；Hatak 部件一件都沒上 |

- 匯出檔本身格式正常（`facegen_install` 測試以場 5 檔為真樣本）；問題在遊戲裡的頭部件沒被換掉。
- 真因未定位。不要再用同一組 Papyrus 呼叫重試；候選：使用者在 RaceMenu 介面手動載 preset 後由 agent 觸發 `ExportHead`（一分鐘的人手），或打通 CK（D1）。
- 收回流程照 trigger README 跑了 4 輪，每輪 `layer_apply --revert` 逐位元組還原、overwrite 匯出檔搬進備份夾，profile 雜湊回到放入前。

### 禁區

- **PROTEUS 的「清除 NPC 編輯」與 Debug 第 5 項禁用**：它呼叫 `CharGen.DeleteFaceGenData`，會刪磁碟上的 `FaceGeom／FaceTint` 檔；MO2 下可能刪到已裝 mod（JH NPC Beauty、換臉層）的實體檔（`npc-face-patch` REPORT §1.2）。
- 不借 PROTEUS 程式碼（授權未查證）；觸發元件只用 skee 公開的 Papyrus API。
- 匯出那場**不存檔**：主角會被暫時改成目標的種族與性別。

### 備援 D1：Creation Kit

CK **已裝**（Steam app 1946180，獨立資料夾，`SLocalMasterPath=Data\` 只有 `Scripts.zip`）。Proton 下 Ctrl+F4 能否出 FaceGen、能否看到 MO2 的 mod plugin **未驗證**。路線 A 的匯出沒有產物、或產物結構不像 FaceGen 時，先申請「打通 CK」小專題；`jslot2npc` 產的 record 層兩條路線共用。

Done when：

- `build_layer` exit 0（`deployable=true`），層 ESP 是 ESL、FaceGen 兩檔在定義 plugin 路徑下。
- `VERIFY.txt` 與 `FACEGEN-VERIFY-*.txt` 的 gate 全 PASS（WARN 要在回報裡逐條解釋）。

## 7. 部署與驗收

沿用 [profile-change](../profile-change/README.md)：

1. `python3 instance/tools/layer_apply.py <層>.layer-apply.json` dry-run（現役 `plugins.txt` 若是遊戲寫回的純 LF，manifest 要加 `"accept_lf": ["plugins.txt"]`）。
2. 取得使用者授權。
3. `--apply`。
4. `check_masters.py`（present=no 為 0）、`look_transplant/transplant.py --verify mods/<層>`、`reverify.py`。
5. 依 [runtime-qa](../runtime-qa/README.md) 實機看臉：`placeatme` 複本與真身都看，排除存檔臉快取。

Done when：遊戲內那個 NPC 不是灰臉或素頭，外觀和使用者選定的圖一致。外觀一致與否由使用者確認。**本段尚未跑過**（6b 沒有可用匯出頭）；試點結果見 [npc-face-pilot](../../user/2026-11-22-npc-face-pilot.md)。

NPC 對 NPC 的整臉換現在就能做：走 [look-swap runbook](../../../agentctl/docs/look-swap-runbook.md)，產出的換臉層同樣適用本段 7。
