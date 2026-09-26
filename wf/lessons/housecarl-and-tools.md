# houseCARL、xEdit、DynDOLOD 等工具坑（1/2）

[lessons 索引](README.md)｜同主題：[housecarl-and-tools-2](housecarl-and-tools-2.md)

## housecarl-setfield-cjk-byte-drop

> houseCARL set_field 寫中文會靜默丟位元組（cp1252 解碼吃掉 81 8D 8F 90 9D），check_errors 驗不出；寫中文一律用 bulk_apply CopyFrom（原 type: project）

2026-09-01 hcell 隊實測：houseCARL/Mutagen 讀寫字串欄走 Windows-1252，檔案實為 UTF-8。cp1252 未定義的五個位元組（81 8D 8F 90 9D）在「讀」的階段就被靜默丟掉——「讀出中文再寫回」會毀掉多數 CJK 名稱（實測「區」E5 8D 80 → E5 80）。check_errors 驗不出（只查 FormLink/master/parse）。既有 docs 只記了寫出變 ?，沒記讀取丟位元組這半邊。

**Why:** 會靜默毀損所有經 set_field 轉寫的中文字串，且無工具告警。

**How to apply:** houseCARL 寫中文欄一律 `bulk_apply verb=CopyFrom`（DeepCopy 位元組保真、不經顯示層）；驗收必做位元組級 diff 對正本，不能只靠 check_errors。位元組層讀 CELL FULL 可用 agentctl/handoffs/hcell-2026-09-01/tools/cellfull.py。相關：[[chinese-diff-ok-but-no-tofu]]。

## housecarl-cannot-point-real-mo2-instance

> houseCARL 指不到真實 MO2 實例（ModOrganizer.ini 的 gamePath 是 wine 的 Z:\ 形式），要用 POSIX 鏡像；profiles 用快照複製不 symlink（原 type: memory）

2026-09-05 lead-ayop 實測：`housecarl_set_mo2_instance` 指真實 `/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2` **必定失敗**（「game Data folder is missing: Z:\home\...\Skyrim Special Edition/Data」），因為真實 `ModOrganizer.ini` 的 gamePath 是 wine 的 `Z:\...` 形式，houseCARL 不做 Windows→POSIX 轉換。上午各線用 /tmp 鏡像不是偷懶，是唯一解。

**Why:** 交接書若寫「先指回真實實例」，每條線都會白撞一次；而指到某線 session 的 scratchpad 鏡像則會隨 session 消失、profiles 快照也會過時。
**How to apply:** 用鏡像目錄：`ModOrganizer.ini` 的 gamePath 改 POSIX、`mods`／`Data` symlink 到真實目錄、`profiles` 用 `cp -a` **快照**（不 symlink，否則 houseCARL 寫入路徑會指回版控目錄）。有線改過 modlist/plugins 就先重新 cp 再讀。2026-09-05 的鏡像在 `/tmp/housecarl-mirror-2026-09-05`（重開機就沒了）；常設化＋刷新腳本收進 `instance/tools/` 登記在 `agentctl/docs/backlog.md`。相關：[[mo2-auto-adds-stray-mods-dirs]]（houseCARL 寫入產物別落在真實 mods/）。

**2026-09-08 追加：** 鏡像是快照，profile 剛改過（新 patch 套上）而鏡像沒刷新時，houseCARL 會高信心回報「這支 esp 不在載入順序／沒贏」——lead-rsc2 因此誤判第一輪 patch 沒生效、白做一輪。**做記錄層贏家判定前先刷新鏡像的 profile 快照**（`~/.local/share/housecarl-mirror`），並把「鏡像時間戳 ≥ profiles 最後 commit」寫進驗收。

## housecarl-merge-facegen-backslash-filename

> houseCARL merge_plugins 在 Linux 把 facegen 輸出寫成含反斜線的單一檔名，不是真目錄；合併後要手動攤開並對齊大小寫（原 type: memory）

2026-09-06 lead-rm 合併 Thora／Torvi／Hrefna 三支 esp 時實測：houseCARL `merge_plugins` 會自動把 FaceGen 搬到新 plugin 名的資料夾（這是選它而不選 xEdit 的原因），但在 Linux 上寫出來的是 `textures\actors\character\...\00000800.dds` 這種**含反斜線的單一檔名**，遊戲找不到。

**Why:** Windows 路徑分隔符沒轉 POSIX；MO2／Proton 下大小寫也要對齊原 mod 用的 `Meshes/actors/character/FaceGenData/FaceGeom/`。
**How to apply:** 合併後先 `find mods/<new> -name '*\\*'` 抓出來，逐個攤成真目錄再驗；FormID 對照表另存（FormID 全變，招募中的隨從會消失）。相關：[[housecarl-cannot-point-real-mo2-instance]]（鏡像在 `~/.local/share/housecarl-mirror`，profiles 改過要重跑 `instance/tools/housecarl-mirror.sh`）。

## missing-master-scan-mast-not-housecarl

> houseCARL load_order_status 的「缺 master 0」只看 plugins.txt 勾選，證明不了 master 有裝；驗收要用全稱掃 TES4 MAST 的 check_masters.py（原 type: memory）

2026-09-03 lrzh／lrfw 發現：`housecarl_load_order_status` 報「缺 master 0」時，實際有 **13 個**借用 patch 的 master 根本不在 load order（MO2 開關時會自動取消勾選，但 `git checkout --` 還原後又變回啟用）。MO2 回寫 diff 反推也不行（390 行重排只挑得出 3 筆）。

**Why:** 今天 inst2／rt2／lrinst／lrzh 四隊的驗收都用了這個假數字；lrfw 全稱掃 MAST 後遊戲內 plugin 數（790）才第一次與 plugins.txt 對上。
**How to apply:** 安裝／部署類交接書的「缺 master」驗收一律指定 `instance/tools/check_masters.py --out <csv>`（讀 TES4 MAST，`present=no` 必須 0；`--out` 必填，`--candidate` 可讀未安裝的單一 plugin；2026-09-03 晚 18:21 已從 lrfw 交接書搬進 instance，原檔仍留在 `agentctl/handoffs/home-2026-09-03/lrfw/tools/`）。可選 patch 的規則寫死「master 不在啟用集就不勾」。相關：[[verify-game-alive-via-qa-not-ps]]。

2026-09-03 晚補：隱含 master 判定曾是「loadorder 前 13 行」，inst3 工人把新 plugin 塞到 loadorder 開頭就假報 44 筆；20:41 已改成「5 個原版＋`Skyrim.ccc` 中經 MO2 解析器可見的檔」（instance 9cddaef），本機是 13 個（其中 3 個 CC 小件在 `Creation Club Missing Archives (private)` mod 裡，不在遊戲 Data）。三個 profile 檔第 1 行都是 MO2 註解、loadorder 前段是隱含 master、modlist 第 1 行優先權最高——交接書寫「插最上面」一定錯。

## bsa-voice-index-false-negative

> 2026-09-18 隨從文本解包：BSA 語音索引靜默回 0 會捏造「缺語音」；語音不只 .fuz；中文層要看文本不只看路徑（原 type: project）

2026-09-18 vf-text 隊（`modpack-design/content-plan/dialogue/`，工具 `dump_follower_dialogue.py`／`translation_pipeline.py`）踩到的假陰性：BSA 語音索引失敗時靜默回 0 → Inigo／Sofia／Recorder 全被標「缺語音」；Rigmor 48%「缺語音」其實是多隨從 plugin（OK_Followers.esp 裝 11 個）的 voice_type 錯歸屬，真值全部 0–7%；語音檔還有 .xwm/.wav 不只 .fuz；中文層偵測只看路徑會把 daegon/kaeserius 判 0%；GetIsID 命中要看比較運算子；「JP TEXT」mod 其實是中文。

**Why:** 這類統計一錯就會推出「要補配音」的假工項。

**How to apply:** 索引結果為 0 一律當錯誤不當數據；多隨從 plugin 用 voice_type 分攤；缺語音率 >20% 先懷疑統計而非 mod。相關：[[voiced-follower-makeover-project]]、[[translation-layer-cost-threshold]]。
