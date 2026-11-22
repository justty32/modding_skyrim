# 換身體、自己捏身形、逐 NPC 指定身形

[入口](README.md)｜[工具鏈](tools.md)｜[部署](deploy.md)

裝備跟著身形變，靠三件事：裝備帶 `.tri`（Build Morphs）、角色身上有 morph 值、morph 值是「相對於烤入基準的差量」。本頁把三件事收進一份設定檔，換基準、加裝備、改某個 NPC 都是「改設定 → 重跑一行」。

**何時用**：換全域基準身形、新增要跟 morph 的裝備批次、給某個 NPC 指定身形、使用者自己捏了 preset 要套用。
**何時不用**：單件試刷走 [刷衣服](outfits.md)；部署走 [部署](deploy.md)；找轉換包走 [nexus-intake](../nexus-intake/README.md)。

## Done when

- 設定檔改完，`bodyslide_rebuild.py all` exit 0；`plan` 的 `unresolved`／`uncovered` 為 0，或逐條寫進 REPORT 由人裁示。
- 每批的 `verify` 通過：路徑集合一致、`.tri` 齊、抽樣 NIF／TRI／BODYTRI 可解；有舊層可比的批次 `baseline_equal` 全真，否則說明差在哪。
- 新層與 manifest 在 `<staging_root>/layers/`、`manifests/`；部署另走 [部署](deploy.md)。

## 設定檔與一行重建

設定檔是 `bodyslide-rebuild/1` JSON；現役有兩份（private）：女體 `agentctl/tools/bodyslide/rebuild-cbbe.json`、男體 `rebuild-himbo.json`，各自一個 `base_preset`、一個 staging。欄位以 `python tools/bodyslide_rebuild.py --help` 為準，重點：

| 欄位 | 作用 |
|---|---|
| `base_preset` | 烤入基準（現役 `CBBE Vanilla`），全部裝備與全域身體都用它 |
| `morphs` | `true` 才產 `.tri` |
| `revision`、`run` | 輸出層名尾碼與 staging 子目錄；換基準時兩者都換新值，舊層保留可回退 |
| `batches[]` | 每批的 `select`（`projects`／`osp_mods`／`stems`／`stems_from_dirs`／`scope`）、同輸出變體的 `prefer`／`avoid`／`choose`、`layer`、`before`、`replaces`、`references` |
| `extra_sources`、`preset_files` | 未安裝的轉換包、使用者自己存的 preset XML |
| `stage_shapedata` | `"all"`／`"none"`／資料夾清單，控制 staging 容量 |
| `body_sex` | `female`（預設）／`male`：`verify` 拿哪個全域身體（femalebody／malebody）與哪組內嵌身體 shape 比對 |
| `obody` | 逐 NPC 指定身形的表與 OBody 設定，見下文；OBody 只有一個設定檔，所以只由一份設定檔持有（現役在 `rebuild-himbo.json`） |

```bash
python tools/bodyslide_rebuild.py all --config agentctl/tools/bodyslide/rebuild-cbbe.json
```

`all` 依序跑 `stage → plan → build → verify → layer → obody`，任一步不過就停。也可單跑一步，`--batch` 限定批次。同版號重建用 `--suffix=-x`（等號不可省，值以 `-` 開頭）。`scope` 選法讀 `agentctl/tools/bodyslide_scope_scan.py` 產的表；mod 有增減就先重跑它。

## 換身體（換全域基準）

1. 確認新身體是 CBBE 系。換到 3BA 或 UNP 系要先換身體本體與轉換包，見下方人工判斷點。
2. 改 `base_preset`，`revision` 與 `run` 換新值，然後跑 `all`。
3. 看 `verify`：舊層是舊基準烤的，`baseline_equal` 預期為假；改看 `body_on`，CBBE 拓樸的內嵌身體應為 1.0。
4. 部署新版號的層、停用舊版號；回退＝反過來。OBody 的差量 preset 依賴基準，`obody.revision` 一起換新值重產。

### 男體（HIMBO）

男體走另一份設定檔 `rebuild-himbo.json`，流程同上，差在四處：

- 範圍表用男性模式：`agentctl/tools/bodyslide_scope_scan.py --sex male`（取 ARMA 的 MOD2，家族另認 HIMBO／SOS／SAM／原版男體）。
- 設定檔加 `"body_sex": "male"`，`base_preset` 用 `HIMBO Zero for OBody`（全滑桿為 0；本機實測建出的 `malebody_1` 與作者預烤的 for OBody 版逐頂點相同）。
- 轉換包沒裝進 MO2 時用 `extra_sources`；`select.scope` 以 `osp_mods` 篩，只建現役男性 ARMA 真的會讀到的件。
- **男女共用同一 mesh 路徑的件要排除**（`exclude_stems`）：HIMBO 版會讓女性穿到 HIMBO 形。判準是本輪輸出檔與女性 ARMA 路徑、女體 `BSO-*` 層檔案的交集為 0。

OBody 分男女：preset 的 `set` 含 himbo／talos／sam／sos／savren 就算男性（OBody 4.4.3 `IsFemalePreset`）。`obody.neutral` 可以是清單，男女各放一個零形 preset 進 `random_pool`；某一性別的隨機池是空的，OBody 會跳過該性別所有人（連指定的也跳過），存檔裡的舊 morph 也不會清。男性 NPC 要指定身形時，`npc_presets` 那列加 `"sex": "male"`，差量基準取 `obody.male.base_preset`。工具會擋「女性 preset 的 set 讀起來是男性」與反之。

## 使用者自己捏身形

**遊戲內（RaceMenu）**：適合「我的角色」。部署帶 `.tri` 的身體與裝備層後，RaceMenu 身體滑桿的改動會同時套到裸身與裝備。需要三樣東西：

- 滑桿定義 `RaceMenuMorphsCBBE.esp`：現役沒有裝，3BA 包 `CBBE 3BA (3BBB)-30174` 的 `15 RaceMenuMorphs/00 RaceMenuMorphs - CBBE` 有附，不必另外下載。
- 身體 `.tri`：由 `BSO-Body-*` 層提供。
- EngineFixes 記憶體設定：現役 `bOverrideMemoryManager`／`bOverrideScaleformAllocator` 皆為 `true`。這會讓 RaceMenu 的 CBBE morph 調一兩次後就失效（Nexus 109080 的說明），要改設定或裝 109080。
- 隨從／NPC：RaceMenu 不能直接捏 NPC，改用下文「逐 NPC 指定」。
- 臉不歸這裡：RaceMenu 的臉部滑桿、preset（`.jslot`）與固化成 NPC patch 層走 [racemenu](../racemenu/README.md)。

**BodySlide 視窗**：適合全域基準或某個 NPC 的固定樣子。在 MO2 的 Executables 新增 `Data/CalienteTools/BodySlide/BodySlide.exe`（實體在 `BodySlide and Outfit Studio 5.8.2` mod；改 `ModOrganizer.ini` 屬 `instance/`，由使用者或部署線做）。舊版 wine 下 preset 下拉曾空白（[lesson](../../lessons/faces-troubleshooting.md#bodyslide-wine-preset-empty-nam7-weight)），待實機。視窗裡**只存 preset、不按 Build**：Build 會落到 `overwrite/`，蓋過所有 `BSO-*` 層。preset 經 MO2 存進 `overwrite/CalienteTools/BodySlide/SliderPresets/<檔名>.xml`；告訴 agent 檔名與 preset 名，當基準就改 `base_preset`，給 NPC 用就加進 `obody.npc_presets`（新 `run` 的 stage 會收進 overwrite，或用 `preset_files` 點名）。

headless 建置跑在 staging 的私有 prefix 與 bwrap 唯讀沙箱，讀 staging 當下的複本，不會和 GUI 改到同一個檔；只會搶 CPU，而 GUI 之後才存的 preset 要重 stage 或列進 `preset_files`。

**怎麼選**：自己的角色在遊戲內捏，所見即所得。全域基準與 NPC 固定形在 BodySlide 存 preset，交給設定檔重建。

## 逐 NPC 指定身形

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

## 換身體時的人工判斷點

- 同一輸出路徑的變體要選哪一個（物理、zap、alt）：第一次由人裁示，之後寫進 `choose`。
- 轉換包與本體的版本是否對得上：看 `plan` 的 `uncovered` 與 esp 的 ARMA 路徑。
- 3BA 參考形的裝備用 CBBE preset 烤，內嵌身體只有約一半頂點會貼在全域身體上（`body_on` 約 0.48）。這是 3BA 拓樸本身造成的，不是建置失敗。
- 實機外觀（穿脫跳形、破洞、存檔殘留 morph）只能由使用者在遊戲裡看。
