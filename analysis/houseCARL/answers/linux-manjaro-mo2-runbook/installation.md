# 安裝與 runtime 選項

[返回入口](../linux-manjaro-mo2-runbook.md)

## 建議安裝步驟

### 1. 建立穩定安裝位置

不要長期使用 `/tmp/housecarl-linux-publish`。建議放到：

```sh
mkdir -p "$HOME/tools/housecarl/server"
VERSION=$(python3 -c "import json;print(json.load(open('$HOME/repo/moddings/skyrim/projects/houseCARL/plugin/.claude-plugin/plugin.json'))['version'])")
dotnet publish "$HOME/repo/moddings/skyrim/projects/houseCARL/src/housecarl-mcp/housecarl-mcp.csproj" \
  -c Release \
  -r linux-x64 \
  --self-contained true \
  -p:PublishSingleFile=false \
  -p:PublishTrimmed=false \
  -p:Version="$VERSION" \
  -o "$HOME/tools/housecarl/server"
```

**`-p:Version` 不能省。**`ServerInfo.Version` 是唯一能從外部問出「現在部署的是哪一版」的欄位，
而它只在 build 時被 `-p:Version` 戳進去（`src/housecarl-mcp/housecarl-mcp.csproj:19-21`）。省略的話 exe 會回報
`0.0.0-dev`，於是「該不該重 publish」這個問題就永遠答不出來——2026-08-26 就是這樣才讓一個 1.6.0
的 build 在線上活了 47 天。官方 `scripts/build-plugin.ps1:57` 也是從同一份 `plugin.json` 讀版本，
這裡只是把同一條規則搬到 Linux。

**swap 用 `mv`，不要就地覆寫。**先 publish 到暫存目錄、smoke 過了再
`mv server server.bak-<舊版本>-<日期>` ＋ `mv <暫存> server`。rename 不動舊 inode，
所以正在跑的 MCP server 行程（實測同時有 7 支）不會被拉掉半條腿。

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
  --env HouseCarl__ProfileDir="$HOME/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/modpack-main" \
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
`~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/modpack-main`。2026-08-20 修正時已各留
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

