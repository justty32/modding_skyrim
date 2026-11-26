# houseCARL 在 Linux 上的平台坑（路徑、環境變數、鏡像、靜默錯答）

[lessons 索引](README.md)

本檔是 houseCARL 跑在 Linux／wine（不是上游預設環境）上的坑，外加它不報錯卻答錯的幾類情境。與平台無關的坑（Nexus 欄位、寫入編碼、複製類工具語意、agent-bridge）在 [housecarl-and-tools](housecarl-and-tools.md)。

## housecarl-localappdata-env-on-linux

> houseCARL 在 Linux 讀不到 localized 欄位，真因是上游 Mutagen 要 Windows 環境變數 `LocalAppData`；判準是贏家 plugin 帶不帶 Localized 旗標，不是「偶發、重試即可」

2026-10-24 定罪。真因、症狀表、修法與驗收已整份寫在 `agentctl/docs/housecarl/localappdata.md`，照它做；要點：

- 兩種症狀同一個病：拋 `Could not determine plugin listings path`，或**不拋例外**而把欄位降級成 `Name = (unreadable: ...)`（`read_record`／`batch_record_detail`），很容易被讀成「這筆本來就沒名字」。**凡是靠 houseCARL 讀名稱做的統計，只要樣本含原版／DLC／CC，修正前的結論都要重算。**
- **判準：看贏家 plugin 帶不帶 Localized 旗標**（原版／DLC／CC 必壞，一般 mod 的 esp 必好），決定性的；重試、換時段、等別線刷新鏡像一概沒用。真因在上游 Mutagen，**不要去改 houseCARL 的 C# 程式碼**。
- **修法：補環境變數，拼法只能是 `LocalAppData`**（Linux 的 .NET 大小寫敏感，`LOCALAPPDATA` 修不好、症狀跟沒修一樣）；那個目錄刻意不放 `Plugins.txt`。

**生效條件（容易漏）**：環境變數寫進 MCP 設定後，**既有的 housecarl-mcp 行程仍是壞的，要重開 Claude Code**。開工前先跑 `instance/tools/housecarl_localappdata.sh --check`，不要假設已生效——跟 [[tmux-working-text-is-not-liveness]] 同一類錯誤：設定檔改了不等於跑著的那個行程改了。不必重開 session 的端到端驗：`instance/tools/housecarl_smoke.py`。報告 `agentctl/handoffs/home-2026-10-24/hcpath/REPORT.md`。相關：[[housecarl-silent-wrong-answer-bugs]]。

## housecarl-cannot-point-real-mo2-instance

> houseCARL 指不到真實 MO2 實例（ModOrganizer.ini 的 gamePath 是 wine 的 Z:\ 形式），要用 POSIX 鏡像；profiles 用快照複製不 symlink

`housecarl_set_mo2_instance` 指真實 `/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2` **必定失敗**（「game Data folder is missing: Z:\home\...\Skyrim Special Edition/Data」）：真實 `ModOrganizer.ini` 的 gamePath 是 wine 的 `Z:\...` 形式，houseCARL 不做 Windows→POSIX 轉換（2026-09-05 實測）。用鏡像是唯一解；交接書別寫「先指回真實實例」，也別指到某線 session 的 scratchpad 鏡像（會隨 session 消失）。

**How to apply:** 用常設鏡像 `~/.local/share/housecarl-mirror`：`ModOrganizer.ini` 的 gamePath 改 POSIX、`mods`／`Data` symlink 到真實目錄、`profiles` 用 `cp -a` **快照**（不 symlink，否則 houseCARL 寫入路徑會指回版控目錄）。刷新腳本 `instance/tools/housecarl-mirror.sh`。相關：[[mo2-auto-adds-stray-mods-dirs]]（houseCARL 寫入產物別落在真實 mods/）。

此鏡像供讀取，不能當成可寫隔離環境；製作產物須用 staging 內的實體 `mods` 目錄。寫入或複製前，同時檢查父目錄與目的檔的解析路徑都留在 staging，包含既存的檔案 symlink，避免沿連結改到真實實例。

鏡像是快照：profile 剛改過而鏡像沒刷新時，houseCARL 會高信心回報「這支 esp 不在載入順序／沒贏」，誤判 patch 沒生效（2026-09-08）。**做記錄層贏家判定前先刷新鏡像的 profile 快照**，並把「鏡像時間戳 ≥ profiles 最後 commit」寫進驗收。

`Could not determine plugin listings path` 跟鏡像無關，見 [[housecarl-localappdata-env-on-linux]]；`cross_plugin_query` 或自寫 `resolve_load_order.py` 這類不走 Mutagen listing 路徑的算法是「繞過」不是「沒壞」——繞過時讀到的 localized 欄位仍是空的或錯的。

## housecarl-merge-facegen-backslash-filename

> houseCARL merge_plugins 在 Linux 把 facegen 輸出寫成含反斜線的單一檔名，不是真目錄；合併後要手動攤開並對齊大小寫

houseCARL `merge_plugins` 會自動把 FaceGen 搬到新 plugin 名的資料夾（這是選它而不選 xEdit 的原因），但在 Linux 上寫出來的是 `textures\actors\character\...\00000800.dds` 這種**含反斜線的單一檔名**，遊戲找不到（2026-09-06 實測）。Windows 路徑分隔符沒轉 POSIX；MO2／Proton 下大小寫也要對齊原 mod 用的 `Meshes/actors/character/FaceGenData/FaceGeom/`。

**How to apply:** 合併後先 `find mods/<new> -name '*\\*'` 抓出來，逐個攤成真目錄再驗；FormID 對照表另存（FormID 全變，招募中的隨從會消失）。相關：[[housecarl-cannot-point-real-mo2-instance]]（profiles 改過要重跑 `instance/tools/housecarl-mirror.sh`）。

同樣的 FormID 重編風險也出現在 `compact_plugin`（compact 成 ESL）：帶 NPC facegen 的 esp compact 後 FormID 變了、以 FormID 命名的 facegen 檔對不上會當場黑臉。compact 帶 facegen 的 esp 前先掃有沒有 FormID 命名的 facegen 檔，優先避免 compact，先清點 full 槽餘量是否真的不夠（`agentctl/handoffs/done/2026-09/home-2026-09-12/lgperk/REPORT.md:116`）。

## housecarl-silent-wrong-answer-bugs

> houseCARL 有多處會在特定情境下悄悄給錯答案，不是「查無結果」而是「結果是錯的」

**大小寫／反斜線（native Linux）：** LooseCache 大小寫不敏感比對但只記第一次出現的大小寫，查過小寫路徑的子樹之後對 resolver 永久隱形；內部路徑正規化成反斜線、碰 loose filesystem 前沒轉本機路徑，`housecarl_skse_inventory` 會回報 0 DLL 即使檔案都在。本機 fork 已修，換 source／重裝要重查（`analysis/houseCARL/answers/linux-manjaro-mo2-runbook/verification.md`；`agentctl/docs/housecarl/linux-porting-issues.md`）。

**`resolve_names=true` 失敗**：缺 `LocalAppData`，見 [[housecarl-localappdata-env-on-linux]]。要查人類可讀名稱的替代路線 esplib／whichmod 仍然正確。

**localized 字串**：`f0148dc8` 之前的 build 只讀 plugin 旁邊的表、不看 MO2 VFS，中文層的鬆散 `strings/*_english.strings` 讀不到，會**靜默回英文**或空值（Gold001 回 `Gold`，遊戲裡是「金幣」）。`f0148dc8` 起照 VFS 贏家讀 strings（同 `housecarl_asset_status` 的 resolver），對獨立 oracle `instance/tools/whichmod.py` 10/10；副作用：forward／CopyFrom 寫出的 localized 欄位帶的是 VFS 中文，不是原版英文（`agentctl/handoffs/home-2026-10-26/hcjk/REPORT.md` §1–3）。

**判贏家照 plugins.txt 字面順序**，不套引擎「master 類（.esm/.esl/ESM旗標）排所有普通 esp 前面」的規則；候選群混有 master 類時判贏家會錯（2026-10-10 實測 8 筆翻盤；`agentctl/handoffs/done/2026-10/home-2026-10-10/mo2-reorder/REPORT.md`）。

**How to apply:** 碰到 0 DLL／resolve_names 失敗／排序判贏家，先假設是已知 bug，不要照字面信任結果。用 houseCARL 驗中文前先確認跑著的 housecarl-mcp 是 `f0148dc8` 以後的 build（`agentctl/tools/check_housecarl_deployed.py`；換檔後要重開 Claude Code 才生效），JSON 讀 `display` 不讀 `value`（`value` 是給寫回用的原始 token，看起來仍像 mojibake）；不確定時改用 `whichmod.py` 當 oracle；候選群混 master 類時一律跑 `engine_winners.py` 交叉驗證。
