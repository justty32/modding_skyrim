# 本機驗證證據

[headless 路線](headless.md)｜[入口](README.md)

服裝 project 的 CT77 現役／CBBE 對照、實際衣服 shape 與 TRI 驗證見 [服裝證據](outfit-evidence.md)。

## 原生 preset：2026-11-18 四輪對照

`/tmp/bs-native-preset-test.py` 複製官方未修改 `SE 3BBB Amazing.osp`，在 staging 寫精確 group 與 A／B preset，再以 `xvfb-run -a wine BodySlide.exe -gbuild NativePresetTest -p <名稱> -t <隔離路徑>` 執行。本次沒有 `-tri`，每輪只有兩個 NIF；A、B、不存在名稱、B repeat 四輪 exit 0。

`/tmp/bs-native-preset-us4l112k/geometry.json` 的直接頂點比較：small／big 的 `Breasts` 同時由 0 改為 100，low／high 各在 18,436 頂點中有 7,709 個改變，最大距離約 2.088543；另兩個 1,905／201 頂點 shape 完全不變。B repeat 與 B 的全部頂點相同，證明此輸入下的幾何可重現；不是全檔 hash 的決定性聲明。

不存在的 `Nonexistent Sentinel` 同樣 exit 0，兩個體重全部 shape 頂點卻與 A／default 相同。這直接證明 exit 0 不能證明 preset 有套用。原始 argv／退出碼／檔案 hash 在同目錄 `results.json`；暫存路徑不作永久依賴，這裡保存可重建的輸入與結論。此證據優先於較早 OSP fallback probe 的「原生 preset 未驗證」界線；未驗證完整裝備批次或遊戲外觀。

### 原生 B＋TRI 合測與 Config

同一目錄 `REPORT.md`、`tri.py`、`check-tri.py`／`tri-validation.json` 記錄後續同 group 的 `-p 'Sentinel B' -tri`。使用空的 `b-tri` output，Config 的 OutputDataPath 改為**已存在且帶結尾反斜線**的私有 safe-fallback。exit 0、log 僅一個 project 並完成；產生 low／high NIF 及 5,010,861-byte `femalebody.tri`。兩個 NIF 的全部頂點與未加 `-tri` 的 B 相同，safe-fallback 保持空白。

TRI parser 驗 PIRT header、三個 position morph shape section、索引均在對應 NIF 頂點數內且 scale 有限；尾端 30,937 bytes 的 UV morph section 未解碼，因此只通過已解碼部分的結構與索引驗證，不宣稱完整 TRI 語義或遊戲 morph 已驗。

早先四輪 Config 是逐字複製，空 game paths／ProjectPath `.`，OutputDataPath 當時仍為歷史值；每次明確 `-t`，log／產物路徑證明輸出在隔離目錄。後續合測才改 safe-fallback。第一次 fallback 不存在且未帶結尾反斜線時在 OpenGL 初始化後停滯，由本輪精確 PID 終止；根因未隔離，不能宣稱其中單一條件必然致錯。修正後未加特殊 GLX 選項也成功，GLX workaround 是另一次環境故障的處置。

複製的來源 OSP 在原生建置後仍逐 bytes 等同原版，所有 ShapeData 同來源。錯 group 的探索輪仍套用 B，因 preset `set` 精確符合 project；不能把 group 當作唯一適用機制。形式 A／B fixture 的 group／set 皆相容。

## 舊個案的驗證界線

歷史驗證器 `agentctl/handoffs/home-2026-11-07/chronicon-kurone/work/final-review.py:234–258` 另行比對 preset XML 的 small／big 明確值與實際 OSP、輸入／輸出 hash、每套 21 件、low／high 及兩套作者 preset 的 `NiSkinPartition` block hash 不同；這比只看完成字串更強，但不是直接解析頂點座標的 A／B 哨兵，也不是全 profile 服裝驗收。場次檔可到期，不作本工作流的必要依賴。

同檔 `:225–232` 驗的是該輪精確 23 個 OBody NPC 排除，且明記既存 co-save morph 仍可能需要 runtime reset。不能把該輪排除數與設定搬到新任務，也不以改設定代替已載入角色的實機檢查。

## 2026-11-18 隔離實跑

本機 binary SHA-256 為 `3ad463a665d6a735953f177fb87d0f1060ed9cf9c62685a23f681110b98177e2`。取歷史 OSP 的 `bcb1 CBBE 3BBB Body Amazing` 與 `SE 3BBB Amazing` ShapeData（約 20 MB），在專用 group `Probe` 實跑。外層 `bwrap` 設 `/` 唯讀、私有 `/tmp`、僅測試目錄可寫、停網路，HOME／WINEPREFIX 在測試夾，移除 WAYLAND_DISPLAY／DBUS_SESSION_BUS_ADDRESS。本輪暫存 `/tmp` 只是可丟棄 probe，不是部署備份或永久證據。

runner 起 `Xvfb -displayfd FD -screen 0 1280x1024x24 -nolisten tcp -extension GLX`，讀回 DISPLAY 後跑 `wine BodySlide.exe -gbuild Probe -t <隔離 Windows 路徑> -tri`，只關自己的 Xvfb。上面的 `xvfb-run` snippet 是等效啟動形狀，並非本次逐字 argv。本機預設 GLX 曾觸發 NVIDIA EGL segfault；關閉 GLX 後此批建成功，預覽／其他 OpenGL 功能不在此結論內。

baseline 與 sentinel 兩輪 wrapper／Wine 皆 exit 0，且均有本輪完成 log。每輪三檔：`femalebody_0.nif`、`femalebody_1.nif` 各 2,007,438 bytes，`femalebody.tri` 5,010,861 bytes。只把 OSP `Breasts small` 從 0 改為 100，僅 `_0.nif` hash 改變，`_1.nif`／TRI 不變；後續 `vertex-comparison.json` 直接解析頂點，確認 low 在 18,436 點中有 7,709 點位移，high 全部頂點不變；與只改 small 的預期一致。

第三輪把 OSP OutputPath 還原為歷史 `meshes/actors/character/kurone_native/bcb1`，三檔與 2026-11-07 舊輸出逐位元組全等。先前不同輸出路徑造成 BODYTRI 字串差異，因此不能直接用不同路徑的 NIF hash 推論身材變化。

實證原件是 `/tmp/bs-probe-20261118-w0n92l00/` 的 `report.md`、`source.json`、`results.json`、`historical-comparison.json`、`clean-command.json` 與 `run_private.py`；暫存到期不影響上面的持久結論。此實測只證明指定真實 project 的 `-gbuild`＋OSP defaults 路線，未證明 CLI 直接挑 preset、全 profile 服裝批建、衝突選項、遊戲內外觀或 morph 運行。
