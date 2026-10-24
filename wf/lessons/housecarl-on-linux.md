# houseCARL 在 Linux 上的平台坑（路徑、環境變數、鏡像、靜默錯答）

[lessons 索引](README.md)

本檔從 [housecarl-and-tools](housecarl-and-tools.md) 拆出（2026-10-24）：那三節加上本檔第一節會讓原檔超過 16 KB，且四節共用同一個軸——**houseCARL 本身沒問題，是它跑在 Linux／wine 這個不是上游預設的環境上**。原檔留的是與平台無關的坑（Nexus 欄位、複製類工具語意、編碼、版本比較、agent-bridge）。

## housecarl-localappdata-env-on-linux

> houseCARL 在 Linux 讀不到 localized 欄位，真因是上游 Mutagen 要 Windows 環境變數 `LocalAppData`；判準是贏家 plugin 帶不帶 Localized 旗標，不是「偶發、重試即可」

2026-10-24 `hcpath` 線定罪。兩種症狀其實同一個病：拋 `Could not determine plugin listings path`，或**不拋例外**而把欄位降級成 `Name = (unreadable: ...)`。

**真因在上游，不在 houseCARL。** Mutagen 0.53.1 讀任何 localized string（FULL／DESC…）前要先列該 plugin 適用的 BSA，那條路徑最後會讀 Windows 環境變數 `LocalAppData`，Linux 沒有就丟例外。houseCARL 自己的 C# 原始碼 grep `Listings` 是 **0 命中**——**不要去改它的程式碼**。

**判準（取代「偶發、重試即可」）：看贏家 plugin 帶不帶 Localized 旗標。** 原版／DLC／CC 必壞，一般 mod 的 esp 必好。所以同一天同一台機器查 A 失敗、查 B 成功，看起來像擲骰子，其實是決定性的。重試、換時段、等別線跑完鏡像刷新，一概沒用。

**反例一**：~~「別線同時在跑 `housecarl-mirror.sh` 刷新鏡像」~~ 不是原因（2026-10-10 的誤判，更正見下一節末段）。
**反例二**：~~「`read_record`／`batch_record_detail` 正常」~~ 是誤判。它們不丟例外，只把欄位靜默降級成 `(unreadable: ...)`，很容易被讀成「這筆本來就沒名字」。**凡是靠 houseCARL 讀名稱做的統計，只要樣本含原版／DLC／CC，修正前的結論都要重算。**

**修法：補環境變數，不動 C# 原始碼。拼法只能是 `LocalAppData`。** Linux 的 .NET 讀環境變數**大小寫敏感**，照 Windows 習慣寫 `LOCALAPPDATA` 會修不好，而且症狀跟沒修一模一樣（舊報告就是這樣寫的，照抄會白做一輪）。那個目錄**刻意不放 `Plugins.txt`**：實測放與不放，`Skyrim.esm` 的 17 個 BSA 排序逐行相同，不值得養第二份會過期的載入序。

**生效條件（容易漏）**：環境變數寫進 MCP 設定後，**既有的 housecarl-mcp 行程仍是壞的，要重開 Claude Code／Codex**。所以開工前先跑 `--check`，不要假設已生效——這跟 [[tmux-working-text-is-not-liveness]] 同一類錯誤：設定檔改了不等於跑著的那個行程改了。

工具與證據：`instance/tools/housecarl_localappdata.sh`（建目錄＋驗兩個註冊檔，帶 `--check`）、`instance/tools/housecarl_smoke.py`（自己另起 housecarl-mcp 走 MCP stdio 做端到端驗，不必重開 session）、文件 `agentctl/docs/housecarl/localappdata.md`、報告 `agentctl/handoffs/home-2026-10-24/hcpath/REPORT.md`、`instance` commit `98ab181`。相關：[[housecarl-silent-wrong-answer-bugs]]（同屬「不報錯但答案是錯的」一類）。

## housecarl-cannot-point-real-mo2-instance

> houseCARL 指不到真實 MO2 實例（ModOrganizer.ini 的 gamePath 是 wine 的 Z:\ 形式），要用 POSIX 鏡像；profiles 用快照複製不 symlink（原 type: memory）

2026-09-05 lead-ayop 實測：`housecarl_set_mo2_instance` 指真實 `/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2` **必定失敗**（「game Data folder is missing: Z:\home\...\Skyrim Special Edition/Data」），因為真實 `ModOrganizer.ini` 的 gamePath 是 wine 的 `Z:\...` 形式，houseCARL 不做 Windows→POSIX 轉換。上午各線用 /tmp 鏡像不是偷懶，是唯一解。

**Why:** 交接書若寫「先指回真實實例」，每條線都會白撞一次；而指到某線 session 的 scratchpad 鏡像則會隨 session 消失、profiles 快照也會過時。
**How to apply:** 用鏡像目錄：`ModOrganizer.ini` 的 gamePath 改 POSIX、`mods`／`Data` symlink 到真實目錄、`profiles` 用 `cp -a` **快照**（不 symlink，否則 houseCARL 寫入路徑會指回版控目錄）。有線改過 modlist/plugins 就先重新 cp 再讀。2026-09-05 的鏡像在 `/tmp/housecarl-mirror-2026-09-05`（重開機就沒了）；常設化＋刷新腳本收進 `instance/tools/` 登記在 `agentctl/docs/backlog.md`。相關：[[mo2-auto-adds-stray-mods-dirs]]（houseCARL 寫入產物別落在真實 mods/）。

**2026-09-08 追加：** 鏡像是快照，profile 剛改過（新 patch 套上）而鏡像沒刷新時，houseCARL 會高信心回報「這支 esp 不在載入順序／沒贏」——lead-rsc2 因此誤判第一輪 patch 沒生效、白做一輪。**做記錄層贏家判定前先刷新鏡像的 profile 快照**（`~/.local/share/housecarl-mirror`），並把「鏡像時間戳 ≥ profiles 最後 commit」寫進驗收。

2026-10-10 補：~~houseCARL 偶發「Could not determine plugin listings path」等間歇性錯誤，常見原因是別線同時在跑 `housecarl-mirror.sh` 刷新鏡像（而非鏡像過期）；…重試幾次或改路即可，不必停工等候~~（`agentctl/handoffs/done/2026-10/home-2026-10-10/smi/REPORT.md`）。

**2026-10-24 更正：上面那段的歸因是錯的，別照抄。** `Could not determine plugin listings path` 不是間歇性的、跟別線刷不刷鏡像無關、重試無效——真因是環境變數 `LocalAppData`，判準見本檔 [[housecarl-localappdata-env-on-linux]]。原文唯一仍成立的是半句：`cross_plugin_query` 或自寫 `resolve_load_order.py` 這類**不走 Mutagen listing 路徑**的替代算法確實可用，但那是「繞過」不是「沒壞」——繞過時讀到的 localized 欄位仍然是空的或錯的。證據：`agentctl/handoffs/home-2026-10-24/hcpath/REPORT.md`。

## housecarl-merge-facegen-backslash-filename

> houseCARL merge_plugins 在 Linux 把 facegen 輸出寫成含反斜線的單一檔名，不是真目錄；合併後要手動攤開並對齊大小寫（原 type: memory）

2026-09-06 lead-rm 合併 Thora／Torvi／Hrefna 三支 esp 時實測：houseCARL `merge_plugins` 會自動把 FaceGen 搬到新 plugin 名的資料夾（這是選它而不選 xEdit 的原因），但在 Linux 上寫出來的是 `textures\actors\character\...\00000800.dds` 這種**含反斜線的單一檔名**，遊戲找不到。

**Why:** Windows 路徑分隔符沒轉 POSIX；MO2／Proton 下大小寫也要對齊原 mod 用的 `Meshes/actors/character/FaceGenData/FaceGeom/`。
**How to apply:** 合併後先 `find mods/<new> -name '*\\*'` 抓出來，逐個攤成真目錄再驗；FormID 對照表另存（FormID 全變，招募中的隨從會消失）。相關：[[housecarl-cannot-point-real-mo2-instance]]（鏡像在 `~/.local/share/housecarl-mirror`，profiles 改過要重跑 `instance/tools/housecarl-mirror.sh`）。

2026-10-23 補：同樣的 FormID 重編風險也出現在 `compact_plugin`（compact 成 ESL）——若該 esp 帶 NPC facegen 且檔名就是 FormID，compact 後 FormID 變了、facegen 檔名對不上會當場黑臉；compact 帶 facegen 的 esp 前先掃是否有 FormID 命名的 facegen 檔，優先避免 compact，先清點 full 槽餘量是否真的不夠（`agentctl/handoffs/done/2026-09/home-2026-09-12/lgperk/REPORT.md:116`）。

## housecarl-silent-wrong-answer-bugs

> houseCARL 有多處會在特定情境下悄悄給錯答案，不是「查無結果」而是「結果是錯的」


**大小寫／反斜線（native Linux）：** LooseCache 大小寫不敏感比對但只記第一次出現的大小寫，查過小寫路徑的子樹之後對 resolver 永久隱形；內部路徑正規化成反斜線，碰 loose filesystem 前沒轉本機路徑，`housecarl_skse_inventory` 會回報 0 DLL 即使檔案都在（本機 fork 已修，換 source／重裝要重查；`analysis/houseCARL/answers/linux-manjaro-mo2-runbook/verification.md`）。

**`resolve_names=true` 在本機必定失敗**（`Could not determine plugin listings path`），重試也沒用，要查人類可讀名稱改用 esplib/whichmod（2026-10 多條獨立線各自命中）。**2026-10-24 更正**：「必定」只對一半——它只在**贏家 plugin 帶 Localized 旗標**時失敗（原版／DLC／CC 必壞，一般 mod 的 esp 本來就會過），而且不是 houseCARL 的 bug，是缺環境變數，已修；判準與「要重開 CLI 才生效」見 [[housecarl-localappdata-env-on-linux]]。修好之前 esplib／whichmod 的替代路線仍然正確。

**判贏家照 plugins.txt 字面順序**，不套引擎「master 類（.esm/.esl/ESM旗標）排所有普通 esp 前面」的規則；候選群混有 master 類時要另外跑 `engine_winners.py` 模擬引擎實際順序交叉驗證（2026-10-10 六條線的「排序讓某 mod 輸」驗收都建立在這個會出錯的前提上，實測 8 筆翻盤；`agentctl/handoffs/done/2026-10/home-2026-10-10/mo2-reorder/REPORT.md`）。

**Why:** 三類都不報錯，給出看似正常但錯誤的答案，前兩類已有多條獨立線踩過。

**How to apply:** 碰到 0 DLL／resolve_names 失敗／排序判贏家，先假設是已知 bug，不要照字面信任結果；候選群混 master 類時一律跑 `engine_winners.py` 交叉驗證。

