# 換身體、自己捏身形、逐 NPC 指定身形

[入口](README.md)｜[工具鏈](tools.md)｜[部署](deploy.md)｜[自己捏身形](body-swap-self.md)｜[逐 NPC 指定](body-swap-npc.md)

裝備跟著身形變，靠三件事：裝備帶 `.tri`（Build Morphs）、角色身上有 morph 值、morph 值是「相對於烤入基準的差量」。本頁把三件事收進一份設定檔，換基準、加裝備、改某個 NPC 都是「改設定 → 重跑一行」。

**何時用**：換全域基準身形、新增要跟 morph 的裝備批次、給某個 NPC 指定身形、使用者自己捏了 preset 要套用。
**何時不用**：單件試刷走 [刷衣服](outfits.md)；部署走 [部署](deploy.md)；找轉換包走 [nexus-intake](../nexus-intake/README.md)。

## Done when

- 設定檔改完，`bodyslide_rebuild.py all` exit 0；`plan` 的 `unresolved`／`uncovered` 為 0，或逐條寫進 REPORT 由人裁示。
- 每批的 `verify` 通過：路徑集合一致、`.tri` 齊、抽樣 NIF／TRI／BODYTRI 可解；有舊層可比的批次 `baseline_equal` 全真，否則說明差在哪。
- 新層與 manifest 在 `<staging_root>/layers/`、`manifests/`；部署另走 [部署](deploy.md)。

## 設定檔與一行重建

設定檔是 `bodyslide-rebuild/1` JSON；現役有兩份（private）：女體 `agentctl/tools/bodyslide/rebuild-cbbe.json`、男體 `rebuild-himbo.json`，各自一個 `base_preset`、一個重建根（`staging_root`）。**重建根固定在 `~/skyrim_mods/bodyslide-sources/<female|male|body-fit>/`，不是暫存，清暫存時不可刪**；根內要留什麼、來源丟了怎麼從下載包重解，見設定檔夾的 README（private）。欄位以 `python tools/bodyslide_rebuild.py --help` 為準，重點：

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

遊戲內 RaceMenu 與 BodySlide 視窗兩條路、怎麼選，已移到 [使用者自己捏身形](body-swap-self.md)。

## 逐 NPC 指定身形

以 OBody NG JSON 指定 NPC 身形（`obody.npc_presets`）、流程與人工判斷點，已移到 [逐 NPC 指定身形](body-swap-npc.md)。

## 換身體時的人工判斷點

- 同一輸出路徑的變體要選哪一個（物理、zap、alt）：第一次由人裁示，之後寫進 `choose`。
- 轉換包與本體的版本是否對得上：看 `plan` 的 `uncovered` 與 esp 的 ARMA 路徑。
- 3BA 參考形的裝備用 CBBE preset 烤，內嵌身體只有約一半頂點會貼在全域身體上（`body_on` 約 0.48）。這是 3BA 拓樸本身造成的，不是建置失敗。
- 實機外觀（穿脫跳形、破洞、存檔殘留 morph）只能由使用者在遊戲裡看。
