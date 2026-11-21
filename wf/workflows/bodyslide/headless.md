# Headless 路線與版本證據

[入口](README.md)

## 版本先行

本機 mod 標示為 `5.8.2 Dev 2026-08-15`，不能當成官方 tag 的逐位元組版本；每次保存執行檔 SHA-256。官方 [v6.1.0 固定提交](https://github.com/ousnius/BodySlide-and-Outfit-Studio/tree/033016464d31761bfaf6966db3ea9c3c3cb6105a) 的 [BodySlideApp.h:580–609](https://github.com/ousnius/BodySlide-and-Outfit-Studio/blob/033016464d31761bfaf6966db3ea9c3c3cb6105a/src/program/BodySlideApp.h#L580) 與 [BodySlideApp.cpp:6035–6127](https://github.com/ousnius/BodySlide-and-Outfit-Studio/blob/033016464d31761bfaf6966db3ea9c3c3cb6105a/src/program/BodySlideApp.cpp#L6035) 是新 CLI 的查證入口。新版支援 `--quiet`，仍需 display；不可把新旗標套到舊 binary。

## 首選：原生 preset 命令

本機 binary 已實測支援 `-gbuild <group> -p <preset>`。先保留原版未修改 OSP，將 preset XML 放進獨立 staging 的 `SliderPresets/`，並用 group 精確挑出 project。以下例子分別放在 `SliderGroups/probe.xml` 和 `SliderPresets/probe.xml`；A／B 只改有效 slider，其他欄位相同：

```xml
<SliderGroups><Group name="NativePresetTest">
  <Member name="CBBE 3BBB Body Amazing"/>
</Group></SliderGroups>
```

```xml
<SliderPresets>
  <Preset name="Sentinel A" set="CBBE 3BBB Body Amazing">
    <Group name="NativePresetTest"/>
    <SetSlider name="Breasts" size="small" value="0"/>
    <SetSlider name="Breasts" size="big" value="0"/>
  </Preset>
  <Preset name="Sentinel B" set="CBBE 3BBB Body Amazing">
    <Group name="NativePresetTest"/>
    <SetSlider name="Breasts" size="small" value="100"/>
    <SetSlider name="Breasts" size="big" value="100"/>
  </Preset>
</SliderPresets>
```

原生 A／B 四輪最初未加 `-tri`，後續 B＋`-tri` 合測也通過；結果見 [證據](evidence.md)。**不存在的 preset 仍可能 exit 0 並產生 default 身體**，所以名稱存在性、project 適用性與 A／B 頂點哨兵是必要門檻；group 與 preset 的精確 `set` 都要查，group 不匹配不一定拒用 preset。

## 共用環境與命令形狀

本輪自行設定絕對路徑，`BS_TOOL_DIR` 必須是副本，內有已核對的 Config／資源與 group。`BS_TARGET_WIN` 是同一 Wine prefix 可見的 Windows 絕對輸出路徑，必須落在隔離空目錄；以下變數不可指向 live mods／Data。

設定副本可取本次已跑配置的必要欄位作起點（不是宣稱刪除其他欄位後已另測過）。`OutputDataPath` 改成**本輪已存在、空白**的 safe-fallback Windows 路徑，保留結尾反斜線，避免 `-t` 遺漏時寫到 live；`GameDataPath`／`ProjectPath` 的 `.` 以工具副本為 cwd。每輪 output／evidence 使用新目錄，先確認未有舊檔，禁止就地清空不明目錄。

```xml
<Config>
  <TargetGame>4</TargetGame>
  <WarnMissingGamePath>false</WarnMissingGamePath>
  <BSATextureScan>false</BSATextureScan>
  <GameDataPath>.</GameDataPath>
  <OutputDataPath>Z:\本輪路徑\safe-fallback\</OutputDataPath>
  <ProjectPath>.</ProjectPath>
  <GameRegKey/><GameRegVal/>
  <LogLevel>3</LogLevel>
  <Language>-1</Language>
</Config>
```

```bash
: "${BS_TOOL_DIR:?請設定本輪工具副本}"
: "${BS_PRIVATE_PREFIX:?請設定本輪專用 Wine prefix}"
: "${BS_TARGET_WIN:?請設定隔離 Windows 輸出路徑}"
: "${BS_EXACT_GROUP:?請設定已審核的精確 group}"
: "${BS_EXACT_PRESET:?請設定已核對存在的精確 preset 名稱}"
: "${BS_EVIDENCE_DIR:?請設定本輪 evidence 絕對路徑}"
cd "$BS_TOOL_DIR" || exit 1
env WINEPREFIX="$BS_PRIVATE_PREFIX" WINEDEBUG=-all \
  WINEDLLOVERRIDES='mscoree,mshtml=' LIBGL_ALWAYS_SOFTWARE=1 \
  timeout 120s xvfb-run -a \
  --server-args='-screen 0 1280x1024x24 -nolisten tcp -extension GLX' \
  wine BodySlide.exe \
  -gbuild "$BS_EXACT_GROUP" -p "$BS_EXACT_PRESET" -t "$BS_TARGET_WIN" \
  > "$BS_EVIDENCE_DIR/stdout.log" 2> "$BS_EVIDENCE_DIR/stderr.log"
```

這是 Xvfb 上執行 wx／Wine 的無人值守路線；不是不需要顯示伺服器的純 CLI。歷史腳本 timeout 是 Python `subprocess.run(timeout=120)`，此處的 shell timeout 是流程守門範例；超時後按本輪 PID 查殘留，不全域 kill Wine。`-tri` 只在本輪需要 morph 且專案支援時啟用。

歷史舊版 log 的完成字串是 `All group build sets processed successfully!`；官方新版為 `All command-line build sets processed successfully!`，見 [新版 cpp:6035–6127](https://github.com/ousnius/BodySlide-and-Outfit-Studio/blob/033016464d31761bfaf6966db3ea9c3c3cb6105a/src/program/BodySlideApp.cpp#L6035)。兩者都只是輔助訊號：`Log_BS.txt` 可能 append，建置前記 byte offset／前輪快照，驗精確 prefix 後切本輪新增段並記 byte range；保留原件，逐 project 核結果與輸出集合，不把舊完成字串算本輪成功。歷史 42 件是該輪輸入的斷言，不能照搬成本輪數量。

## Fallback：OSP defaults 與幾何哨兵

下例是舊版本的本機歷史路線，來源為實體磁碟 `/home/lorkhan/skyrim_mods/_staging-2026-11-07-chronicon-kurone/native-bake/bake.py:35–48`，不是全現役 profile 的自動化工具。它把兩套 preset 的值寫入獨立 OSP default，使用專用 group、prefix 和 output；原腳本會複製／改 staging，因此**先閱讀並複製至本輪空目錄，不直接重跑歷史現場**。

只在原生 preset 路線對本輪輸入不適用且有證據時，才採 OSP defaults；此時從共用命令移除 `-p`，必要時加 `-tri`。歷史腳本的「所有顯式值都有被寫入」斷言，只證明 XML 值被寫入 OSP；不能獨自證明執行時真的套用了那些值。兩條路線都建立相同 project 的 A／B 哨兵：A 為中性或已知基準，B 為一個已知有效且非零 slider；除 slider 外維持相同輸入，隔離輸出，解析對應 shape 頂點，確認出現可解釋的座標差異。hash 不同不能單獨當作幾何變化證明；固定 A／B／B-repeat 已驗指定語義便停，不為收尾追加建置。若 A／B 幾何相同，先查 preset/group／default 覆蓋路徑與 slider 是否對該 shape 有效。

同一路徑多 project 的選擇，必須在 manifest 明定並縮小 group 或使用該版本已查證的 conflict 選項。不可依列舉順序默認最後一件贏，也不可在 quiet 模式等互動選單。

本機另有 OBody NG `4.4.3`；這個版本標籤不是本輪設定證據。全域 OBody 零基底＋TRI 與私有 NPC 固定體型分開規劃，查目前模型路徑、排除規則與 morph 使用方式後再建置。私有路徑本身不自動證明角色不會被套 morph。

## 實證

本機 OSP fallback、歷史回歸與原生 preset 幾何哨兵見 [驗證證據](evidence.md)。
