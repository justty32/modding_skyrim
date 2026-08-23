# houseCARL 在 Manjaro + Proton Skyrim + MO2 上跑起來的最小方案

日期：2026-07-10  
來源專案：<https://github.com/Avick3110/houseCARL>  
本機 clone：`projects/houseCARL/`  
分析目標：只回答「如何讓 houseCARL 在這台 Manjaro 上跑起來，並適配目前 Skyrim/MO2/Proton 環境」。

## 結論

houseCARL 官方安裝路線是 Windows installer，但核心 server 是 `net9.0` C# MCP server；在這台 Manjaro 上可行的路線是：

1. 不用官方 `houseCARL-Setup.exe`。
2. 從 source 對 `src/housecarl-mcp/housecarl-mcp.csproj` 做 Linux self-contained publish。
3. 在 Codex 用 `codex mcp add` 註冊 published `housecarl-mcp`。
4. 不使用 `HouseCarl__Mo2InstanceDir` 單一路徑模式，改用 explicit paths：`HouseCarl__DataDir`、`HouseCarl__ModsDir`、`HouseCarl__ProfileDir`。

原因是本機 MO2 的 `ModOrganizer.ini` 記錄的是 Wine 路徑：

```text
/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/ModOrganizer.ini:4
gamePath=@ByteArray(Z:\\home\\lorkhan\\.local\\share\\Steam\\steamapps\\common\\Skyrim Special Edition)
```

native Linux houseCARL 會把這個值清成 `Z:\home\...`，而不是 `/home/lorkhan/...`，所以 `Mo2InstanceDir` 模式會找不到 game `Data` 目錄。

## 已確認的本機環境

| 項目 | 狀態 |
|---|---|
| OS | Manjaro Linux |
| Steam | native `/usr/bin/steam` |
| Skyrim app id | `489830`，見 `~/games/mod-organizer-2-skyrimspecialedition/variables.sh` |
| Skyrim game root | `~/.local/share/Steam/steamapps/common/Skyrim Special Edition` |
| Skyrim Data | `~/.local/share/Steam/steamapps/common/Skyrim Special Edition/Data` |
| MO2 instance | `~/games/mod-organizer-2-skyrimspecialedition/modorganizer2` |
| MO2 mods | `~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods` |
| MO2 profile | `~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/main`（唯一 profile；`Default` 已於 2026-08-20 退役） |
| profile files | `modlist.txt`、`plugins.txt`、`loadorder.txt` 皆存在 |
| .NET | SDK 8/10、runtime 8/10；缺系統 .NET 9 runtime 與 ASP.NET Core runtime 9 |

## 專案關鍵證據

- 官方 README 明列需求為 Windows 與 .NET 9 runtime / ASP.NET Core runtime，並要求 MO2：`projects/houseCARL/README.md:60`、`projects/houseCARL/README.md:62`、`projects/houseCARL/README.md:63`、`projects/houseCARL/README.md:69`。
- 官方安裝包使用 Windows setup：`projects/houseCARL/README.md:77`、`projects/houseCARL/README.md:80`。
- plugin MCP command 預設指向 `.exe`：`projects/houseCARL/plugin/.mcp.json:5`。
- server 本身支援 stdio 與 HTTP，且不需要 MO2 正在執行：`projects/houseCARL/src/housecarl-mcp/Program.cs:4`、`projects/houseCARL/src/housecarl-mcp/Program.cs:7`、`projects/houseCARL/src/housecarl-mcp/Program.cs:12`。
- server config precedence 支援 explicit paths，欄位是 `DataDir` / `ModsDir` / `ProfileDir`：`projects/houseCARL/src/housecarl-mcp/Program.cs:97`、`projects/houseCARL/src/housecarl-mcp/Program.cs:98`、`projects/houseCARL/src/housecarl-mcp/Program.cs:101`。
- `Mo2Instance` 會從 `ModOrganizer.ini` 推導 `gamePath\Data`、`base\mods`、`base\profiles\<selected_profile>`：`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:121`、`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:137`、`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:138`、`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:139`。
- `Mo2Instance.CleanValue` 只處理 `@ByteArray(...)` 與反斜線跳脫，沒有把 Wine `Z:\home\...` 映射成 Linux `/home/...`：`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:176`、`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:186`。
- load order 是靜態讀 `loadorder.txt` / `modlist.txt` / `plugins.txt`，不用 USVFS：`projects/houseCARL/src/housecarl-core/Mo2LoadOrder.cs:4`、`projects/houseCARL/src/housecarl-core/Mo2LoadOrder.cs:13`、`projects/houseCARL/src/housecarl-core/Mo2LoadOrder.cs:75`。

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
HouseCarl__ProfileDir="$HOME/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/main" \
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
  --env HouseCarl__ProfileDir="$HOME/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/main" \
  -- "$HOME/tools/housecarl/server/housecarl-mcp"
```

`codex mcp list` 顯示 `housecarl` enabled；目前這個已啟動的 Codex session 不會動態載入新 MCP，重開 session 後才會直接出現工具。

## 實測 Smoke Test

使用手寫 MCP client 直接呼叫 `~/tools/housecarl/server/housecarl-mcp`，結果：

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
`profiles/main/skyrim.ini`，含完整 `[Archive]` 區段），是 houseCARL 找不到。後果是 base BSA
完全不進資產掃描，vanilla 資產一律讀成 ABSENT。

A 的連鎖後果最嚴重：`validate_dialogue` 會把**已編譯的** result script 報成 `WILL NOT FIRE`，`validate_scripts` 把腳本報成 unverifiable。單次呼叫內即可重現：

```text
scripts/TopicInfo.pex        → WINS: Skyrim - Misc.bsa     ← 小寫先進來，毒化快取 key
Scripts/MFSofVigGesture.pex  → ABSENT                       ← 檔案其實就在磁碟上
```

修法：新增大小寫不敏感的目錄／檔案解析（先試 literal path，Windows 上零成本；miss 才逐段比對真實子目錄），並讓 loose 命中回傳**真實檔名**組成的路徑（保證能開檔）。B 因此自動修好；C 用同樣的檔名 fallback。

另外 `DialogueValidate` 的非 ASCII 檢查把所有 `> 0x7F` 字元報成「usually render as in-game mojibake」。實測 ModForge 產出的 esp 裡 `—` 是 `0x97`、`é` 是 `0xE9`，都是**合法 Windows-1252**，位元組正確、不會 mojibake。已改成兩級：cp1252 無法表示的（CJK / emoji / C1 control）才是真缺陷（會被寫成 `?`）；可表示但非 ASCII 的只提示「遊戲字型可能缺字」。

## 建議安裝步驟

### 1. 建立穩定安裝位置

不要長期使用 `/tmp/housecarl-linux-publish`。建議放到：

```sh
mkdir -p "$HOME/tools/housecarl/server"
dotnet publish "$HOME/repo/moddings/skyrim/projects/houseCARL/src/housecarl-mcp/housecarl-mcp.csproj" \
  -c Release \
  -r linux-x64 \
  --self-contained true \
  -p:PublishSingleFile=false \
  -p:PublishTrimmed=false \
  -o "$HOME/tools/housecarl/server"
```

**publish 不會產生 `corpus.json`**，必須另外補（官方 `scripts/build-plugin.ps1` 的 step 1 + step 3；只做 publish 會漏掉）。少了它，讀取工具靠 reflection fallback 還能活，但**所有寫入工具與 type 過濾查詢全部失效**，錯誤訊息是：

```text
FileNotFoundException: corpus.json not found at .../server/corpus.json
```

generator 也是 `net9.0`，同樣需要 self-contained publish 才能在本機跑：

```sh
cd "$HOME/repo/moddings/skyrim/projects/houseCARL"
dotnet publish src/housecarl-generator -c Release -r linux-x64 --self-contained true -o /tmp/hc-gen
/tmp/hc-gen/housecarl-generator "$PWD/generated" "$PWD/.claude/skills/mutagen-reference/references"
cp generated/corpus.json "$HOME/tools/housecarl/server/corpus.json"
```

放進去後**不需重啟** server 即生效。

### 2. 註冊到 Codex MCP

Codex CLI 目前支援 `codex mcp add`，可用 `--env` 註冊 stdio server：

```sh
codex mcp add housecarl \
  --env HOUSECARL_DATA_DIR="$HOME/.local/share/housecarl" \
  --env HouseCarl__DataDir="$HOME/.local/share/Steam/steamapps/common/Skyrim Special Edition/Data" \
  --env HouseCarl__ModsDir="$HOME/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods" \
  --env HouseCarl__ProfileDir="$HOME/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/main" \
  -- "$HOME/tools/housecarl/server/housecarl-mcp"
```

之後重開 Codex session，再用：

```sh
codex mcp list
```

確認 `housecarl` 狀態是 enabled。

### 2026-08-20 profile 遷移後的故障模式

MO2 單 profile 遷移後，`Default` 已退役，`ModOrganizer.ini` 的
`selected_profile=@ByteArray(Modpack-KR)`，`profiles/` 底下也只剩 `Modpack-KR`。若 houseCARL 的
explicit `ProfileDir` 仍指向舊目錄，每個查詢都會失敗並回報：

```text
InvalidOperationException: No active plugins resolved from the MO2 profile
```

遇到這個症狀時，先核對 houseCARL 實際收到的 `HouseCarl__ProfileDir` 是否指向仍存在且包含
`modlist.txt`、`plugins.txt`、`loadorder.txt` 的 profile。本機需同步修正以下兩處：

- `~/.codex/config.toml`
- `~/.claude.json`

兩者的 `HouseCarl__ProfileDir` 都應指向
`~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/main`。2026-08-20 修正時已各留
一份 `.bak-20260820` 備份。

> **操作警告：** 修改 `~/.codex/config.toml` 會讓所有正在執行的 Codex session 退出；2026-08-20
> 實測四條線都在改檔後 90 秒內死亡。要改設定前先讓所有 Codex session 收工，再動這個檔案。

### 3. 不建議先走的路線

不建議直接註冊 `HouseCarl__Mo2InstanceDir="$HOME/games/mod-organizer-2-skyrimspecialedition/modorganizer2"`，除非先修 houseCARL 的 Wine path 映射，或修改 MO2 ini 讓 native Linux 程式可讀；否則它會從 `gamePath=@ByteArray(Z:\\home\\...)` 推出不存在的 `Z:\home\...\Data`。

也不建議在 Linux 上跑官方 `houseCARL-Setup.exe` 作為主路線；它的交付與 config 目標是 Windows/Claude/Codex 的 Windows 佈局，README 也明寫 Windows。

## 可選：不用 self-contained，改裝系統 runtime

若想用 framework-dependent build，可安裝 Arch/Manjaro 套件：

```sh
sudo pacman -S dotnet-runtime-9.0 aspnet-runtime-9.0
```

但這條路仍然需要 explicit paths 或 Wine path 映射修正；runtime 只解決「程式可啟動」，不解決 MO2 `gamePath` 是 `Z:\...` 的問題。

## 風險與限制

1. **目前 Codex 需重開 session 才能直接用工具**：已註冊 `housecarl` MCP，但本次已啟動的 Codex session 不會自動熱載新 MCP。
2. **寫入 patch 前要先小規模讀取測試**：先問 active load order/status，再讀一個 vanilla record；確認解析正常後再要求它產 patch。
3. **in-place lane 暫時不要用**：houseCARL 支援直接改現有 plugin，但預設新 patch lane 才適合 Linux 首次驗證。
4. **Papyrus compiler / BSArch 外部工具另算**：資料層讀寫和 patch 產生可先跑；Papyrus 編譯、BSA repack 會牽涉 Wine/CK/工具路徑，應另做一次工具路徑設定。
5. **`corpus.json` 必須在 exe 旁邊**：只做 publish 會漏掉它，寫入工具與 type 查詢會全部失效（見「建議安裝步驟 1」）。
6. **大小寫敏感修正尚未進 upstream**：本機 clone 已修並 publish；換 source 或重裝後要重新確認（見「必要 Linux 修正 → 第二層」）。

## 最小驗證順序

1. 註冊 MCP 後，先問 houseCARL load order status。
2. 確認它看到 `Modpack-KR` profile、active plugin 數與 MO2 大致一致。
3. 讀 `Skyrim.esm` 裡一個穩定 vanilla record。
4. 查一個已裝 SKSE plugin inventory，確認 VFS/mod winner 能解析。
5. 建立一個無害測試 patch mod，例如新增/修改容易回復的 dummy override；產物應出現在 `~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/houseCARL - <name>/`。
6. 在 MO2 refresh，啟用該 mod，再用 xEdit 或 MO2 檢查，不直接進遊戲測大型變更。
