# 驗證結果、Smoke Test 與 Linux 修正

[返回入口](../linux-manjaro-mo2-runbook.md)

## 已驗證結果

在 `projects/houseCARL/` 執行：

```sh
dotnet build housecarl.sln
```

結果：成功，16 個 warning，0 error。

直接跑 framework-dependent build 會失敗，因為系統缺 runtime：

```text
需要 Microsoft.NETCore.App 9.0.0
需要 Microsoft.AspNetCore.App 9.0.0
```

改用 self-contained Linux publish 成功：

```sh
dotnet publish src/housecarl-mcp/housecarl-mcp.csproj \
  -c Release \
  -r linux-x64 \
  --self-contained true \
  -p:PublishSingleFile=false \
  -p:PublishTrimmed=false \
  -o /tmp/housecarl-linux-publish
```

用 explicit paths 啟動 HTTP 模式成功：

```sh
HOUSECARL_DATA_DIR=/tmp/housecarl-test \
HouseCarl__DataDir="$HOME/.local/share/Steam/steamapps/common/Skyrim Special Edition/Data" \
HouseCarl__ModsDir="$HOME/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods" \
HouseCarl__ProfileDir="$HOME/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/modpack-main" \
/tmp/housecarl-linux-publish/housecarl-mcp --http
```

啟動訊息確認：

```text
houseCARL listening on http://127.0.0.1:7345 — reading explicit configured paths STANDALONE (MO2 need not be running)
```

2026-07-10 進一步實測後，已完成全域 Codex MCP 註冊：

```sh
codex mcp add housecarl \
  --env HOUSECARL_DATA_DIR="$HOME/.local/share/housecarl" \
  --env HouseCarl__DataDir="$HOME/.local/share/Steam/steamapps/common/Skyrim Special Edition/Data" \
  --env HouseCarl__ModsDir="$HOME/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods" \
  --env HouseCarl__ProfileDir="$HOME/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/modpack-main" \
  -- "$HOME/tools/housecarl/server/housecarl-mcp"
```

`codex mcp list` 顯示 `housecarl` enabled；目前這個已啟動的 Codex session 不會動態載入新 MCP，重開 session 後才會直接出現工具。

## 實測 Smoke Test

使用手寫 MCP client 直接呼叫 `~/tools/housecarl/server/housecarl-mcp`，結果：

<!-- wf-nav -->
1. `tools/list`：成功列出 35 個工具，包含 `housecarl_load_order_status`、`housecarl_read_record`、`housecarl_skse_inventory`。
2. `housecarl_load_order_status`：成功讀取當時仍在使用的 `Default` profile（已於 2026-08-20
   退役；目前唯一 profile 是 `Modpack-KR`）。
   - 103 enabled mods，2 disabled mods。
   - 52 active plugins。
   - 49 plugins resolved to real files。
   - 警告 3 個 CC plugin 在 `loadorder.txt` 中但實體檔案未找到：`ccbgssse068-bloodfall.esl`、`ccbgssse069-contest.esl`、`ccvsvsse004-beafarmer.esl`。
3. `housecarl_skse_inventory`：修正 Linux path 問題後成功讀取 SKSE plugin layer。
   - 65 top-level DLL。
   - 63 config files，10 個 config folder。
   - 63 個 DLL 有靜態 metadata。
   - 5 個 version-locked 到 runtime `1.6.1170`：`Fuz Ro D'oh.dll`、`JContainers64.dll`、`PapyrusUtil.dll`、`skee64.dll`、`SSEFpsStabilizer.dll`。
   - 2 個 contested DLL：`BehaviorDataInjector.dll`、`BFCO.dll`。
4. `housecarl_read_record`：成功讀 `00000F:Skyrim.esm`。
   - type：`MiscItem`
   - editorid：`Gold001`
   - winner：`Skyrim.esm`
   - `Value = 1`、`Weight = 0`

## 必要 Linux 修正

第一次跑 `housecarl_skse_inventory` 時只看到 `0 DLL(s)`。實體檔案其實存在於 `mods/*/SKSE/Plugins/*.dll`，問題是 houseCARL 內部把 asset path 正規化成 Windows/BSA 語意的反斜線路徑，例如 `SKSE\Plugins\EngineFixes.dll`；在 Linux 檔案系統上，反斜線不是 path separator。

已在本機 clone 裡做兩個小修正，並重新 publish 到 `~/tools/housecarl/server`：

- `projects/houseCARL/src/housecarl-core/AssetResolver.cs`：新增 `NativeRelPath`，在碰 loose filesystem 前把 canonical backslash path 轉成本機 path；另新增 `AssetDirName` / `AssetFileName`，避免 Unix 上 `Path.GetFileName("SKSE\\Plugins\\x.dll")` 把整串當檔名。
- `projects/houseCARL/src/housecarl-mcp/LoadOrderService.cs`：SKSE inventory 顯示檔名時改用 canonical asset path basename。

這是本機 patch，不是 upstream release；之後更新 houseCARL source 後需要重新套用或確認 upstream 已修。

### 第二層：大小寫敏感（2026-07-10 追加）

分隔符只是第一層。houseCARL 還假設檔案系統**大小寫不敏感**（Windows / Wine 成立，native Linux 不成立）。三處都會**靜默給出錯誤答案**，違反它自己「never a silent absent」的承諾：

| # | 位置 | 症狀 |
|---|------|------|
| A | `housecarl-core/AssetResolver.cs`（`LooseCache`） | subtree 快取 key 用 `OrdinalIgnoreCase`，但 `Path.Combine` 拿**第一次出現的大小寫**組真實路徑。只要有人先用小寫查過 `scripts\`，整個 `Scripts\` 子樹對 resolver 永久隱形（直到 snapshot 重建） |
| B | `housecarl-core/DialogueValidate.cs`、`housecarl-mcp/LoadOrderService.cs` | 組出全大寫 `SEQ\<plugin>.seq`，磁碟上是 `Seq/` → 謊報「SGE quest 沒有 .seq」，叫你重生一個早就存在的檔案 |
| C | `housecarl-core/ArchiveDiscovery.cs` | 硬編碼 `"Skyrim.ini"`，Linux MO2 寫的是 `skyrim.ini` |

**C 就是本文件先前記為「profile 缺 `Skyrim.ini`」的那個警告** —— 檔案一直都在（目前為
`profiles/modpack-main/skyrim.ini`，含完整 `[Archive]` 區段），是 houseCARL 找不到。後果是 base BSA
完全不進資產掃描，vanilla 資產一律讀成 ABSENT。

A 的連鎖後果最嚴重：`validate_dialogue` 會把**已編譯的** result script 報成 `WILL NOT FIRE`，`validate_scripts` 把腳本報成 unverifiable。單次呼叫內即可重現：

```text
scripts/TopicInfo.pex        → WINS: Skyrim - Misc.bsa     ← 小寫先進來，毒化快取 key
Scripts/MFSofVigGesture.pex  → ABSENT                       ← 檔案其實就在磁碟上
```

修法：新增大小寫不敏感的目錄／檔案解析（先試 literal path，Windows 上零成本；miss 才逐段比對真實子目錄），並讓 loose 命中回傳**真實檔名**組成的路徑（保證能開檔）。B 因此自動修好；C 用同樣的檔名 fallback。

另外 `DialogueValidate` 的非 ASCII 檢查把所有 `> 0x7F` 字元報成「usually render as in-game mojibake」。實測 ModForge 產出的 esp 裡 `—` 是 `0x97`、`é` 是 `0xE9`，都是**合法 Windows-1252**，位元組正確、不會 mojibake。已改成兩級：cp1252 無法表示的（CJK / emoji / C1 control）才是真缺陷（會被寫成 `?`）；可表示但非 ASCII 的只提示「遊戲字型可能缺字」。

