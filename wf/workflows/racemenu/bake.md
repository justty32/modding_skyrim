# racemenu／bake — 固化成 patch 層與部署

[racemenu](README.md)｜[WORKFLOWS](../../WORKFLOWS.md)

段 6–7。**臉的最終產物是 NPC patch 層**：ESP 裡的 NPC_ 臉部欄位，加上 `facegeom/<plugin>/<id>.nif` 和 `facetint/<plugin>/<id>.dds`。這樣臉不依賴存檔，換存檔、換 profile 都還在。

途徑已定案（`npc-face-patch` 報告 §4）：**主路線 A**＝主角在遊戲裡套 preset → skee 匯出頭 NIF＋tint → 離線上架（匯出已實證要在 RaceMenu 介面內做，見 [6b](bake-export.md)）；**備援 D1**＝Creation Kit Ctrl+F4。PROTEUS 只當遊戲內試戴，不產 patch。

## 6. 固化

**主角**：選定的 jslot 收進一個 preset 層（例如 `RaceMenu Character Assets (private)` 那種層），檔放在 `SKSE/Plugins/CharGen/Presets/`，走 profile-change。

**NPC**：一條指令，工具在 `agentctl/tools/npc_face/`（[tool-index](../../../agentctl/docs/tool-index.md)「NPC 臉 patch」列）：

```text
python3 agentctl/tools/npc_face/build_layer.py --jslot <preset>.jslot --npc <XXXXXX:定義plugin> \
    --staging ~/skyrim_mods/_staging-<日期>-npc-face [--head-nif X.nif --head-dds X.dds --export-weight W] [--drop-shape NAME]
```

| 步 | 工具 | 狀態 |
|---|---|---|
| 6a jslot→NPC_ 欄位 | `jslot2npc.py`：forward 現役贏家 record，只換 PNAM、HCLF、NAM7、FTST、QNAM、NAM9、NAMA、Tint Layers；ESL；MAST＝贏家的 MAST＋贏家 | **可用**（合成載入序測試＋試點 Hatak→Muiri 實產） |
| 6b 匯出頭 | `menu_drive.py` 在 RaceMenu 介面內匯出（[bake-export](bake-export.md)） | **已實證**（face-pilot-2 S3）；觸發 ESP（`npc_face/trigger/`）已被取代，留作備援 |
| 6c 上架 | `facegen_install.py`：改名搬檔、slot 6 指向新 tint、根節點補名、`--drop-shape` 刪多出的 shape、shape gate（重用 look_transplant `shape_gate`）、DDS 格式、貼圖 VFS 解析 | **已用部件正確的真匯出物上架**（Muiri 7 對 7，gate 全 PASS） |
| 6d 組層 | `build_layer.py`：層目錄＋`.npc-face.json` manifest＋`layer_apply` manifest | **可用**（Muiri `deployable=true`）；缺匯出頭停在 exit 3，`layer_apply` manifest 標 DRAFT |

### preset→NPC 臉層：整條流程逐步狀態

依據：face-pilot-2 REPORT（Hatak→Muiri）。

| 步 | 狀態 |
|---|---|
| UI 換種族（先點別的再點回目標） | 實機通過 |
| UI 載 preset（Presets F9） | 實機通過 |
| Sculpt F5 匯出頭 | 實機通過 |
| `build_layer`（含 `--drop-shape`） | 通過，`deployable=true` |
| gate（VERIFY／FACEGEN-VERIFY） | 全 PASS |
| `layer_apply` 部署 | 已做（runtime-3） |
| 實機看臉 | 已實機通過（runtime-3，部署後停用待使用者看圖），見段 7 |

仍需人工判斷：美醜；妝濃淡（Hatak 妝很重，會原樣帶到 Muiri）；體重保留或用 preset 的（`--keep-weight`，Muiri 試點保留原值）；耳朵等多餘 shape 要不要刪。

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

### 6b 匯出頭

做法、失敗原因、耳朵 shape 的處理與舊紀錄都在 [bake-export](bake-export.md)。重點：**不要用主控台 `setrace`／`sexchange` 換種族或性別**，頭 3D 不會重建，之後怎麼套 preset 匯出都是舊部件。

### 禁區

- **PROTEUS 的「清除 NPC 編輯」與 Debug 第 5 項禁用**：它呼叫 `CharGen.DeleteFaceGenData`，會刪磁碟上的 `FaceGeom／FaceTint` 檔；MO2 下可能刪到已裝 mod（JH NPC Beauty、換臉層）的實體檔（`npc-face-patch` REPORT §1.2）。
- 不借 PROTEUS 程式碼（授權未查證）；觸發元件只用 skee 公開的 Papyrus API。
- 匯出那場**不存檔**：主角會被暫時改成目標的種族與性別。

### 備援 D1：Creation Kit

CK **已裝**（Steam app 1946180，獨立資料夾，`SLocalMasterPath=Data\` 只有 `Scripts.zip`）。Proton 下 Ctrl+F4 能否出 FaceGen、能否看到 MO2 的 mod plugin **未驗證**。路線 A 已用 UI 匯出跑通，CK 目前不急；UI 路線日後又失效時，再申請「打通 CK」小專題；`jslot2npc` 產的 record 層兩條路線共用。

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

Done when：遊戲內那個 NPC 不是灰臉或素頭，外觀和使用者選定的圖一致。外觀一致與否由使用者確認。有黑臉或脖縫就停用這層。

**段 7 實機結果（Muiri 試點，runtime-3，證據 `agentctl/handoffs/home-2026-11-22/runtime-3/`）**：

- A1 部署 face-pilot-2 的層：臉、部件、貼圖都對，無黑臉；**脖子底部一圈縫**（脫衣也在）。
- A2 主控台 `setnpcweight` 試 100／0／50，只有 0 時縫消失。根因：匯出頭的脖子照**匯出當下主角的體型**烤；載 Hatak 後主角體型 0，Muiri 保留 100，接不上。
- A3 在 RaceMenu 內重匯：UI 點種族→F9 載 Hatak→**Sliders「體型」調到 1.00**（目標 weight/100）→F5 匯出；`build_layer --keep-weight --export-weight 100` 重建（做法見 [bake-export](bake-export.md)）。
- A4 實機：脖縫消失，正面／側面／背面／裸頸正常，體重保持 100。
- `build_layer` 新 gate：NPC 最終 NAM7 ≠ 匯出體型×100 就擋；本層已部署時重建（贏家是自己）拒做。
- 最終狀態：**已部署、已停用**，等使用者看圖。啟用：`layer_apply.py <runtime-3>/data/muiri-enable.layer-apply.json --apply`；不要：維持停用（MO2 會自動把停用 esp 從 plugins.txt 拿掉，故啟用 manifest 用 `plugins` 重新插入而非 `enable_plugins`）（指令全文見 [試點頁](../../user/2026-11-22-npc-face-pilot.md)）。

NPC 對 NPC 的整臉換現在就能做：走 [look-swap runbook](../../../agentctl/docs/look-swap-runbook.md)，產出的換臉層同樣適用本段 7。
