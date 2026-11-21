# Headless 路線與版本證據

[入口](README.md)

## 版本先行

本機 mod 標示為 `5.8.2 Dev 2026-08-15`，不能當成官方 tag 的逐位元組版本；每次保存執行檔 SHA-256。官方 [v6.1.0 固定提交](https://github.com/ousnius/BodySlide-and-Outfit-Studio/tree/033016464d31761bfaf6966db3ea9c3c3cb6105a) 的 [BodySlideApp.h:580–609](https://github.com/ousnius/BodySlide-and-Outfit-Studio/blob/033016464d31761bfaf6966db3ea9c3c3cb6105a/src/program/BodySlideApp.h#L580) 與 [BodySlideApp.cpp:6035–6127](https://github.com/ousnius/BodySlide-and-Outfit-Studio/blob/033016464d31761bfaf6966db3ea9c3c3cb6105a/src/program/BodySlideApp.cpp#L6035) 是新 CLI 的查證入口。新版支援 `--quiet`，仍需 display；不可把新旗標套到舊 binary。

## 首選：原生 preset 命令

本機 binary 已實測支援 `-gbuild <group> -p <preset>`。先保留原版未修改 OSP，將 preset XML 放進本輪 staging 的 `SliderPresets/`，並用 group 精確挑出 project。以下例子分別放在 `SliderGroups/probe.xml` 和 `SliderPresets/probe.xml`；A／B 只改有效 slider，其他欄位相同。範例用現役家族的 `CBBE Body`（11-18 的證據用的是 3BA `CBBE 3BBB Body Amazing`，那只是能力試驗）：

```xml
<SliderGroups><Group name="NativePresetTest">
  <Member name="CBBE Body"/>
</Group></SliderGroups>
```

```xml
<SliderPresets>
  <Preset name="Sentinel A" set="CBBE Body">
    <Group name="NativePresetTest"/>
    <SetSlider name="Breasts" size="small" value="0"/>
    <SetSlider name="Breasts" size="big" value="0"/>
  </Preset>
  <Preset name="Sentinel B" set="CBBE Body">
    <Group name="NativePresetTest"/>
    <SetSlider name="Breasts" size="small" value="100"/>
    <SetSlider name="Breasts" size="big" value="100"/>
  </Preset>
</SliderPresets>
```

原生 A／B 四輪最初未加 `-tri`，後續 B＋`-tri` 合測也通過；結果見 [證據](evidence.md)。**不存在的 preset 仍可能 exit 0 並產生 default 身體**，所以名稱存在性、project 適用性與 A／B 頂點哨兵是必要門檻；group 與 preset 的精確 `set` 都要查，group 不匹配不一定拒用 preset。

## 執行：一律經沙箱 runner

可照抄的建置指令只有 [工具鏈第 3 步](tools.md#3-沙箱建置bodyslide_sandbox_runpy) 那一條。**不要在一般 shell 直接跑 `wine BodySlide.exe`**：Wine 的 `Z:` 對映整個 `/`，`-t` 或 `OutputDataPath` 打錯就直接寫進現役 mod 或 overwrite；工具目錄若直接指向現役 BodySlide mod，`Log_BS.txt`／Config 也會寫回去並被 MO2 收編。runner 開跑前對 run 目錄做 realpath 守門，再用 bwrap 唯讀根把可寫範圍縮到 run 目錄。

runner 每輪自動寫入下面這份最小 Config（原 staging 的 Config 另存 `Config.staged.xml`），`OutputDataPath` 是本輪已存在、空白、帶結尾反斜線的 safe-fallback，避免 `-t` 遺漏時寫到別處；`GameDataPath`／`ProjectPath` 的 `.` 以工具副本為 cwd：

```xml
<Config>
  <TargetGame>4</TargetGame>
  <WarnMissingGamePath>false</WarnMissingGamePath>
  <BSATextureScan>false</BSATextureScan>
  <GameDataPath>.</GameDataPath>
  <OutputDataPath>Z:\path\to\run\safe-fallback\</OutputDataPath>
  <ProjectPath>.</ProjectPath>
  <GameRegKey/><GameRegVal/>
  <LogLevel>3</LogLevel>
  <Language>-1</Language>
</Config>
```

- **不要整份照抄現役 Config**：現役是 `TargetGame=-1`、`WarnMissingGamePath=true`、`BSATextureScan=true`，啟動時會跳選遊戲對話框，headless 下只會卡到 timeout（推論，未逐項實驗）。
- `DefaultGroups` 一旦非空，`-gbuild` 會連「未分組 outfit」一起建（依 Config 內的上游註解）；最小 Config 不帶這段。
- run 目錄與所有路徑用純 ASCII（runner 會拒絕非 ASCII）；BodySlide 在 wine 下吃非 ASCII `-t`／工具路徑的行為未驗。
- 這是 Xvfb 上執行 wx／Wine 的無人值守路線，不是不需要顯示伺服器的純 CLI。本機預設 GLX 曾觸發 NVIDIA EGL segfault，runner 的 Xvfb 一律關 GLX。`-tri` 只在本輪需要 morph 且專案支援時啟用。
- timeout 只殺 `xvfb-run` 會留下私有 prefix 的 wineserver；runner 對本輪 `WINEPREFIX` 跑 `wineserver -k` 並收掉自己的 bwrap session，不影響別的 prefix，也不全域 kill Wine。

歷史舊版 log 的完成字串是 `All group build sets processed successfully!`；官方新版為 `All command-line build sets processed successfully!`，見 [新版 cpp:6035–6127](https://github.com/ousnius/BodySlide-and-Outfit-Studio/blob/033016464d31761bfaf6966db3ea9c3c3cb6105a/src/program/BodySlideApp.cpp#L6035)。兩者都只是輔助訊號：`Log_BS.txt` 會 append，runner 建置前記 byte offset、只切本輪新增段並記 byte range；逐 project 核結果與輸出集合，不把舊完成字串算本輪成功。

## BuildSelection 與 zap

依上游 v6.1.0 `BodySlideApp.cpp` 的 `CommandLineBuild()`／`GetCmdLineBuildOutfits()`（commit 0330164）：同輸出路徑的多個 outfit，若 `BuildSelection.xml` 有已存的選擇，批次只建被選的那件；沒有就全部照建，誰最後寫入沒有規定。批次模式下 zap 值也只從 BuildSelection 讀（原註解："Only BuildSelection is a reliable source for zap values in batch mode."）。

- 使用者在 GUI 刷過一次，`BuildSelection.xml` 就可能落進 overwrite，之後被合併進 staging，靜默改掉 group 內的勝者與 zap。`bodyslide_stage.py` 的 `summary.build_selection` 記錄它在不在、來自哪個 mod 與內容，manifest 要抄下。
- 同輸出只靠縮小 group 解決，不依賴 BuildSelection；含 zap 的 project（例如 CT77 Zap 系）逐一驗 zap 結果。
- 2026-11-21 現役 `mods/` 與 `overwrite/` 都沒有 `BuildSelection*.xml`。本機 5.8.2 的實際行為見 [證據](evidence.md#buildselection-與同輸出2026-11-21)；沒有那節時一律當「依上游原始碼推論、本機未驗」。

## Fallback：OSP defaults 與幾何哨兵

舊版本的本機歷史路線（2026-11-07 `chronicon-kurone` 的 `bake.py`，未進版控、不保證仍在磁碟）把兩套 preset 的值寫入獨立 OSP default，使用專用 group、prefix 和 output。要重做時在本輪 staging 的 OSP 副本上改 default，再照常經 runner 建置；不重跑歷史現場。

只在原生 preset 路線對本輪輸入不適用且有證據時，才採 OSP defaults；此時 runner 不帶 `--preset`，必要時加 `--tri`。歷史腳本的「所有顯式值都有被寫入」斷言，只證明 XML 值被寫入 OSP；不能獨自證明執行時真的套用了那些值。兩條路線都建立相同 project 的 A／B 哨兵：A 為中性或已知基準，B 為一個已知有效且非零 slider；除 slider 外維持相同輸入，隔離輸出，解析對應 shape 頂點，確認出現可解釋的座標差異。hash 不同不能單獨當作幾何變化證明；固定 A／B／B-repeat 已驗指定語義便停，不為收尾追加建置。若 A／B 幾何相同，先查 preset/group／default 覆蓋路徑與 slider 是否對該 shape 有效。

同一路徑多 project 的選擇，必須在 manifest 明定並縮小 group（BuildSelection 的影響見上節）。不可依列舉順序默認最後一件贏，也不可在 quiet 模式等互動選單。

本機另有 OBody NG `4.4.3`；這個版本標籤不是本輪設定證據。全域 OBody 零基底＋TRI 與私有 NPC 固定體型分開規劃，查目前模型路徑、排除規則與 morph 使用方式後再建置。私有路徑本身不自動證明角色不會被套 morph。

## 實證

本機 OSP fallback、歷史回歸與原生 preset 幾何哨兵見 [驗證證據](evidence.md)。
