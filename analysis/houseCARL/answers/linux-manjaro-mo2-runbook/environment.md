# 結論、環境與關鍵證據

[返回入口](../linux-manjaro-mo2-runbook.md)

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
| MO2 profile | `~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/modpack-main`（唯一 profile；`Default` 已於 2026-08-20 退役） |
| profile files | `modlist.txt`、`plugins.txt`、`loadorder.txt` 皆存在 |
| .NET | SDK 8/10、runtime 8/10；缺系統 .NET 9 runtime 與 ASP.NET Core runtime 9 |

## 專案關鍵證據

<!-- wf-nav -->
- 官方 README 明列需求為 Windows 與 .NET 9 runtime / ASP.NET Core runtime，並要求 MO2：`projects/houseCARL/README.md:60`、`projects/houseCARL/README.md:62`、`projects/houseCARL/README.md:63`、`projects/houseCARL/README.md:69`。
- 官方安裝包使用 Windows setup：`projects/houseCARL/README.md:77`、`projects/houseCARL/README.md:80`。
- plugin MCP command 預設指向 `.exe`：`projects/houseCARL/plugin/.mcp.json:5`。
- server 本身支援 stdio 與 HTTP，且不需要 MO2 正在執行：`projects/houseCARL/src/housecarl-mcp/Program.cs:4`、`projects/houseCARL/src/housecarl-mcp/Program.cs:7`、`projects/houseCARL/src/housecarl-mcp/Program.cs:12`。
- server config precedence 支援 explicit paths，欄位是 `DataDir` / `ModsDir` / `ProfileDir`：`projects/houseCARL/src/housecarl-mcp/Program.cs:97`、`projects/houseCARL/src/housecarl-mcp/Program.cs:98`、`projects/houseCARL/src/housecarl-mcp/Program.cs:101`。
- `Mo2Instance` 會從 `ModOrganizer.ini` 推導 `gamePath\Data`、`base\mods`、`base\profiles\<selected_profile>`：`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:121`、`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:137`、`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:138`、`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:139`。
- `Mo2Instance.CleanValue` 只處理 `@ByteArray(...)` 與反斜線跳脫，沒有把 Wine `Z:\home\...` 映射成 Linux `/home/...`：`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:176`、`projects/houseCARL/src/housecarl-core/Mo2Instance.cs:186`。
- load order 是靜態讀 `loadorder.txt` / `modlist.txt` / `plugins.txt`，不用 USVFS：`projects/houseCARL/src/housecarl-core/Mo2LoadOrder.cs:4`、`projects/houseCARL/src/housecarl-core/Mo2LoadOrder.cs:13`、`projects/houseCARL/src/housecarl-core/Mo2LoadOrder.cs:75`。

