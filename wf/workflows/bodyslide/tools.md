# 工具鏈：stage → plan → 沙箱建置 → 驗收

[入口](README.md)｜[headless](headless.md)｜[部署](deploy.md)

四支工具都在母 repo `tools/`，stdlib、只吃參數或環境變數，從母 repo 根執行。逐支職責見 [CODE_MAP](../common/code-map/CODE_MAP.md)；`--help` 是旗標的唯一真相。下面的 `$MO2`、`$DATA` 是本機 MO2 根與遊戲 Data 的絕對路徑，`$RUN` 是本輪 run 目錄（實體磁碟、純 ASCII、在 `mods/`／`overwrite/`／Data／`instance/` 之外，例如 `~/skyrim_mods/_staging-<日期>-<題目>/run1`）。

## 0. 前置

- `ps -eo comm=` 確認 MO2／Skyrim 沒在跑；在跑時 profile 是暫態，只能唯讀並在 REPORT 註明。
- 守門共用 `tools/bodyslide_guard.py`：live 根由 `--mo2-dir`（或 `MO2_DIR`）、`--game-data`（或 `SKYRIM_GAME_DATA`）、`instance/`（`SKYRIM_REPO` 或 git 推導）決定；缺任何一個就拒絕，不猜。

## 1. 合併 staging：`bodyslide_stage.py`

```bash
python tools/bodyslide_stage.py --mods-dir "$MO2/mods" --overwrite-dir "$MO2/overwrite" \
  --profile-dir instance/profiles/modpack-main --out "$RUN/tool" \
  --table "$RUN/stage-sources.json" --shapedata-folder 'CBBE'
```

- 照 `modlist.txt` 優先序（第一行最高、overwrite 再高；`-`／`*`／separator 不算）以大小寫不敏感合併各 mod 的 `CalienteTools/BodySlide`，`.mohidden` 排除，輸出單一大小寫的真複本樹。
- 先加 `--dry-run` 看表與容量；`--no-shapedata` 只出目錄與 OSP，給 planner 找出需要哪些 `ShapeData` 子目錄，再用 `--shapedata-folder` 逐一點名複製。全量約 2.4 GB／2,859 檔（2026-11-21 現役），容量 gate 由 `--max-bytes`／`--max-files` 擋。
- 表是 `wf-table/1`：每個相對路徑的 winner／來源／sha256、`overrides`（同路徑多提供者，含內容是否相同）、`summary.case_variants`、`summary.build_selection`（見 [headless](headless.md#buildselection-與-zap)）。表放 `$RUN` 下、`tool/` 之外。

## 2. 預檢：`bodyslide_outfit_plan.py`

```bash
python tools/bodyslide_outfit_plan.py --staging "$RUN/tool" --project 'CBBE Body' --tri
```

exit 0／`ok=true` 只代表靜態預檢通過；`conflicts`、`unselected_variants`、`catalog_errors`、`variant_check_complete` 的讀法見 [刷衣服](outfits.md#2-決定變體與身形路線)。只靠 OSP 判衝突，**不看同路徑的非 BodySlide 檔**，那一步在 [部署](deploy.md#1-先查現役贏家) 做。

本輪的精確 group／A／B preset XML 寫進 `$RUN/tool/SliderGroups/`、`$RUN/tool/SliderPresets/`（範例見 [headless](headless.md#首選原生-preset-命令)），寫完再跑一次 planner。

## 3. 沙箱建置：`bodyslide_sandbox_run.py`

```bash
for label in a b b-repeat; do
  preset="Sentinel A"; [ "$label" = a ] || preset="Sentinel B"
  python tools/bodyslide_sandbox_run.py build --run-dir "$RUN" --label "$label" \
    --group 'NativePresetTest' --preset "$preset" --tri \
    --mo2-dir "$MO2" --game-data "$DATA" || break
done
```

- `Log_BS.txt` 是 5.8.2 的滾動 log（每場 `[#Log` 開頭、舊場會被裁），runner 取最後一場並記 `log_mode`；`BuildSelection.xml` 在建置中唯讀。
- 每輪一個新 label，輸出在 `$RUN/rounds/<label>/output/`，證據在同輪 `evidence/`。
- 隔離：bwrap 唯讀 `/`、私有 `/tmp`／`/dev`／PID／IPC、停網路，唯一可寫 bind 是 `$RUN`，`tool/` 資源再覆蓋成唯讀。timeout 時只對本輪 `WINEPREFIX` 跑 `wineserver -k`。
- 先 `--dry-run` 看 argv。exit 0＝wine 0、未逾時、本輪 log 有完成字串、output 非空、safe-fallback 仍空、`--expect-file` 全在；1＝跑了但檢查不過（看 `result.json` 的 `failures`）；2＝跑之前就拒絕。
- 第一次建置會建 prefix（2026-11-21 實測 377 MB、約 15 秒，`--init-timeout`），同一 `$RUN` 的後續輪重用。同時不要超過 2 個 wine 實例。

## 4. 驗收：`bodyslide_mesh_check.py`

```bash
python tools/bodyslide_mesh_check.py --out "$RUN/compare.json" compare \
  --a "$RUN/rounds/a/output" --b "$RUN/rounds/b/output" \
  --repeat "$RUN/rounds/b-repeat/output" --tri-check --expect-changed 'CBBE'
```

- 逐 shape 沿 skin instance → `NiSkinPartition` 取實際頂點（skinned mesh 的 inline count 可為 0，不是空 mesh）；A↔B 要有可解釋的位移、B↔repeat 頂點必須全同；相對路徑集合不同即失敗。
- exit 0 全符合／1 期望不符／2 讀不到或格式不支援。`--out` 放在子命令之前；`--expect-changed` 點名必須有位移的 shape（衣服要點衣服 shape，不只內嵌身體）。不存在的 preset 會讓 runner exit 0 但 `compare` exit 1，A／B 哨兵不能省。單檔細節用 `nif FILE`、`tri FILE --nif FILE`。TRI 未解完的尾段以 `trailing_unparsed_bytes` 回報，未解的部分不冒稱驗過。

## 整範圍重建：`bodyslide_rebuild.py`

上面四步由 `bodyslide_rebuild.py` 依設定檔串起，另加批次選件（`bodyslide_select.py`：每個輸出只選一個 project，並寫 group 與 `BuildSelection.xml`）、批次驗收與輸出層組裝（`bodyslide_layer.py`：路徑集合、抽樣 NIF／TRI／BODYTRI、與舊層逐頂點比對、內嵌身體貼合度、硬連結成層＋manifest＋`layer_apply` 草稿），以及 OBody 設定層（`bodyslide_obody_config.py`）。用法與欄位見 [換身體](body-swap.md)。`bodyslide_stage.py --extra-source LABEL=DIR` 可把未安裝的轉換包解壓目錄併進 staging（優先序在 overwrite 之下、所有 mod 之上）。

## 暫存的保留與清除

- `$RUN` 是證據現場，**不是工具的家**：之後還要用的腳本一律進版控（2026-11-21 前的 runner／驗證器就是隨 staging 一起刪掉的）。
- 保留到：該輪的部署決定做完（部署者要用 output 與 sha256 對帳），或使用者說不部署；最長 30 天，到期列 WAIT_USER 請使用者裁刪，agent 不自刪。
- prefix（約 400 MB）可在最後一輪後先刪；`rounds/*/output` 若已部署，留到實機驗收結束。大小與內容寫進 REPORT。
