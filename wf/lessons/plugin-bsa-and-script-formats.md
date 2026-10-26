# plugin／BSA／腳本的格式事實與量測陷阱

[lessons 索引](README.md)

## missing-master-scan-mast-not-housecarl

> houseCARL load_order_status 的「缺 master 0」只看 plugins.txt 勾選，證明不了 master 有裝；驗收要用全稱掃 TES4 MAST 的 check_masters.py（原 type: memory）

`housecarl_load_order_status` 報「缺 master 0」時，可能有借用 patch 的 master 根本不在 load order（2026-09-03 實際有 **13 個**）（MO2 開關時會自動取消勾選，但 `git checkout --` 還原後又變回啟用）。MO2 回寫 diff 反推也不行（390 行重排只挑得出 3 筆）。

**Why:** 用這個數字當驗收會整批假通過；全稱掃 MAST 後遊戲內 plugin 數才與 plugins.txt 對得上。
**How to apply:** 安裝／部署類交接書的「缺 master」驗收一律指定 `instance/tools/check_masters.py --out <csv>`（讀 TES4 MAST，`present=no` 必須 0；`--out` 必填，`--candidate` 可讀未安裝的單一 plugin；`agentctl/handoffs/home-2026-09-03/lrfw/tools/` 另有一份原始副本）。可選 patch 的規則寫死「master 不在啟用集就不勾」。相關：[[verify-game-alive-via-qa-not-ps]]。

隱含 master 判定是「5 個原版＋`Skyrim.ccc` 中經 MO2 解析器可見的檔」，不是「loadorder 前 N 行」（新 plugin 被塞到 loadorder 開頭就會假報）；本機是 13 個（其中 3 個 CC 小件在 `Creation Club Missing Archives (private)` mod 裡，不在遊戲 Data）。三個 profile 檔第 1 行都是 MO2 註解、loadorder 前段是隱含 master、modlist 第 1 行優先權最高——交接書寫「插最上面」一定錯。

自動化「缺前置/缺 master」gate 的「缺」只是起點不是終點——gate 若只比對暫存候選彼此、沒比對現役已裝啟用的全部 mod，會把前置早已在現役 load order 裡的候選誤判成缺（2026-08-31 至少 3 件）。驗收前要再用 `housecarl_read_plugin_file` 讀出候選 plugin 完整 masters 清單，逐一對現役 `plugins.txt` 比對存在且啟用（`*`），不能只信 gate 回報的第一個「缺哪一個」。source: agentctl/handoffs/done/2026-08-31/fixdis-2026-08-31/FIX-REPORT.md:43-57

同一個「別信二手摘要，查原始紀錄」的坑還有兩個變種——active 集合只掃 plugins.txt 打星號會漏掉隱式啟用的 CC 插件（本機曾差 59 支，真實 active 集合要用 loadorder.txt 扣掉未勾選項，或信 houseCARL/qa_state 的 active 數字，`agentctl/handoffs/done/2026-09/home-2026-09-11/donor/REPORT.md:105-111`）；判斷 mod 實際機制／類別要直接讀該 mod 現役 esp 的 record 組成，不要照抄既有分析文件或 catalog 分類標籤（曾把只有 9 筆 float GMST 的 mod 誤記成天氣 overhaul）。

## bsa-voice-index-false-negative

> 2026-09-18 隨從文本解包：BSA 語音索引靜默回 0 會捏造「缺語音」；語音不只 .fuz；中文層要看文本不只看路徑（原 type: project）

2026-09-18 vf-text 隊（`modpack-design/content-plan/dialogue/`，工具 `dump_follower_dialogue.py`／`translation_pipeline.py`）踩到的假陰性：BSA 語音索引失敗時靜默回 0 → Inigo／Sofia／Recorder 全被標「缺語音」；Rigmor 48%「缺語音」其實是多隨從 plugin（OK_Followers.esp 裝 11 個）的 voice_type 錯歸屬，真值全部 0–7%；語音檔還有 .xwm/.wav 不只 .fuz；中文層偵測只看路徑會把 daegon/kaeserius 判 0%；GetIsID 命中要看比較運算子；「JP TEXT」mod 其實是中文。

**Why:** 這類統計一錯就會推出「要補配音」的假工項。

**How to apply:** 索引結果為 0 一律當錯誤不當數據；多隨從 plugin 用 voice_type 分攤；缺語音率 >20% 先懷疑統計而非 mod。相關：[[voiced-follower-makeover-project]]、[[translation-layer-cost-threshold]]。


## esl-binary-format-facts

> 手寫腳本讀寫 ESL/TES4 二進位格式的兩個關鍵位置：旗標 offset 與 cell 覆寫的 Partial Record 旗標

TES4 flags（含 ESL 位元 `0x00000200`）正確位置是 **offset 0x08**，不是 0x18（交接書曾寫錯；0x18 讀到的其實是 HEDR 子紀錄；`agentctl/handoffs/done/2026-09/home-2026-09-07/chron/REPORT.md:68`）。另外（第三方指南轉述，未實測）：ESM-flag plugin 正確區分 persistent／temporary 並依序載入；非 ESM-flag plugin（含 ESL）全部記錄視為 persistent；ESL 新增的 cell record 若被另一 plugin 覆寫、覆寫方沒標 **Partial Record**（xEdit unknown 14 旗標），原 cell 的 temporary 引用會被整個忽略，觸發暫態引用消失 bug；要保留的引用要同時標 persistent。

**中途存檔對已有 plugin「只加 ESL 旗標」實測可行**（2026-10-26 Save132，6 支）：條件是新增記錄的 local ID 已在 0x800–0xFFF、FormID 不變。讀舊存檔時引擎與 SKSE co-save 都按檔名把 full index 重對應到 light 槽（例：803 個 alias 腳本實例從 `66000D63` 接到 `FE265D63`）；背包、裝備、任務、Papyrus 讀檔段與不加旗標的對照組 0 差異；以 light 狀態存檔、關遊戲重開再讀回也 0 差異（`agentctl/handoffs/home-2026-10-26/esltest/REPORT.md`、`eslapply/REPORT.md`）。**要 compact（改 FormID）的仍然會壞既有存檔**，只在新周目做；「已存 light 後再撤旗標」沒測過。

**Why:** 前者已有實測錯誤前例，後者直接對應一類已知的暫態引用消失 bug，兩者都會讓手刻/手補 patch 悄悄壞掉。

**How to apply:** 手寫腳本判斷 ESL/ESPFE 一律讀 offset 0x08；任何改到 ESL 定義的 cell record 的 patch，先查覆寫方是否該標 Partial Record、暫態引用是否同時標 persistent。省 full 槽時先挑「只加旗標」的候選（`agentctl/handoffs/home-2026-10-26/shell-esl/tools/esl_candidates.py`＋`tier.py` 的 T1），旗標複本放 overlay 的排序規則見 [[eslify-overlay-snapshot-goes-stale]]。

**ESLifier 在 Linux**（2026-10-26 v0.16.17 PoC，`agentctl/handoffs/home-2026-10-26/eslifierpoc/REPORT.md`）：
- **可以跑的組合**：官方 Windows 版 exe＋system wine＋建立時就帶 `WINEDLLOVERRIDES=mscoree,mshtml=` 的乾淨 prefix，GUI 放在 Xvfb 虛擬螢幕。
- **Proton 的 wine 不行**：Qt 載不起來。
- **初始化被打斷的 prefix 不行**：缺 `syswow64`，BSArch 起不來，BSA 會被靜默跳過，log 照寫「Extracting」。
- **不要改跑 Python 原始碼**：原始碼把 facegen／voice 路徑寫成反斜線字面值（`scanner.py:385-398`、`compact_form_ids.py:224`），在 Linux 下會全部漏掉。
- 它的輸出是贏家快照，跟 overlay 一樣會過期。施工步驟見 `agentctl/docs/new-playthrough-esl-runbook.md`。

## load-order-and-asset-measurement-pitfalls

> 算衝突／重複／贏家這類統計時，好幾種看起來合理的算法會系統性算錯規模


**asset winner ≠ plugin winner**：聲音/lip 等資產檔的 winner 由 MO2 VFS（檔案覆蓋順序）決定，跟 plugin record 的 winner（load order）是兩套獨立規則，要分別驗，不能把 xEdit 單檔視圖當現役結果（`agentctl/handoffs/done/2026-08/cx-serana/REPORT.md`）。

**override 筆數 ≠ 衝突筆數**：借用內容覆寫 98,487 個 FormID，真正與現役也動過的只有 16,780（17%），其餘只是「蓋原版」的正常行為；算衝突規模要用「現役覆寫索引 ∩ 借用側覆寫索引」的交集，不能直接拿 override 總數當衝突數。

**FormID 漂移比對用 EDID 不用 FULL**：素材升版後 FormID 位移，用 FULL 比對會產生假 GONE（中文層 FULL 早是中文名，英文名只活在 EDID）；改用 EDID 且規則由鬆到緊（結尾相符>含名字>完全相符），否則會被語意不同但部分相符的記錄搶走。

**同 VFS 路徑的重複貼圖是 0 VRAM 成本**：只佔硬碟；真正會重複吃 VRAM 的只有「不同 VFS 路徑但位元組相同且同時在場」的檔案，估算前先分這兩組。

**Why:** 四個都是直覺算法高估/算錯規模的例子，會把正常行為誤判成要修的衝突，或把成本算錯一個數量級。

**How to apply:** 算衝突/重複規模前先確認用的是交集而非併集、資產層要分開驗、FormID 比對用 EDID 分級規則。

## papyrus-recompile-for-translation-pitfalls

> 重編譯 Papyrus 源碼來改中文字串，兩個不報錯但會悄悄壞掉的坑

直接餵 UTF-8（無 BOM）的 `.psc` 給編譯器會編譯成功，但中文字串在產物裡變雙重編碼亂碼（編譯器把 UTF-8 位元組誤當 ANSI 讀），不會報編譯錯誤，只有逐字串檢查才會發現；存檔一律加 UTF-8 BOM 才正常。另外，缺編譯旗標檔/缺完整相依 script 時重編譯既有 `.pex`，動手翻譯前要先做 round-trip 驗證：用「未修改」的 `.psc` 編一次，跟原廠 `.pex` 比對字串表 multiset、userFlagTable、檔案大小，證明工具鏈本身保真（差異要能被編譯者/機器名長度等已知因素完全解釋）才算過關；編譯旗標檔可從既有 `.pex` 的 userFlagTable 位元索引重建（`agentctl/handoffs/done/2026-08/opus-zh-summary/SUMMARY.md:667-694`）。

**Why:** 兩個坑都是「編譯成功＝看起來沒事」但產物其實壞了，只有逐字串/逐項比對才抓得到。

**How to apply:** 任何要重編譯含中文字串的 `.psc`，存檔一律加 BOM；動手翻譯前先用未修改源碼做 round-trip 驗證當硬閘門，不要編完直接上。
