# plugin／BSA／腳本的格式事實與量測陷阱

[lessons 索引](README.md)｜[存檔體積、身份解析與清理證據](plugin-bsa-and-script-formats/README.md)

## missing-master-scan-mast-not-housecarl

> houseCARL load_order_status 的「缺 master 0」只看 plugins.txt 勾選，證明不了 master 有裝；驗收要用全稱掃 TES4 MAST 的 check_masters.py

2026-09-03：`housecarl_load_order_status` 報「缺 master 0」時，仍可能有 master 不在 load order（MO2 開關時會自動取消勾選，`git checkout --` 還原後又變回啟用）；MO2 回寫 diff 反推也挑不全。拿這個數字當驗收會整批假通過。

安裝／部署類交接書的「缺 master」驗收一律指定 `instance/tools/check_masters.py --out <csv>`（讀 TES4 MAST，`present=no` 必須 0；`--out` 必填，`--candidate` 可讀未安裝的單一 plugin；原始副本在 `agentctl/handoffs/home-2026-09-03/lrfw/tools/`）。可選 patch 的規則寫死「master 不在啟用集就不勾」。相關：[[verify-game-alive-via-qa-not-ps]]。

隱含 master 是「5 個原版＋`Skyrim.ccc` 中經 MO2 解析器可見的檔」，不是「loadorder 前 N 行」（新 plugin 被塞到 loadorder 開頭就會假報）；本機 13 個，其中 3 個 CC 小件在 `Creation Club Missing Archives (private)` mod 裡、不在遊戲 Data。三個 profile 檔第 1 行都是 MO2 註解、loadorder 前段是隱含 master、modlist 第 1 行優先權最高——交接書寫「插最上面」一定錯。

自動「缺前置/缺 master」gate 報的「缺」只是起點：gate 若只比對暫存候選彼此、沒比對現役全部啟用 mod，會把前置早在現役 load order 的候選誤判成缺。驗收前用 `housecarl_read_plugin_file` 讀候選完整 masters，逐一對現役 `plugins.txt` 確認存在且啟用（`*`），不能只信 gate 的「缺哪一個」（`agentctl/handoffs/done/2026-08-31/fixdis-2026-08-31/FIX-REPORT.md:43-57`）。

同類「別信二手摘要，查原始紀錄」：active 集合只掃 plugins.txt 星號會漏隱式啟用的 CC 插件，真實 active 集合用 loadorder.txt 扣掉未勾選項，或信 houseCARL/qa_state 的 active 數（`agentctl/handoffs/done/2026-09/home-2026-09-11/donor/REPORT.md:105-111`）；判 mod 實際機制／類別要直接讀它現役 esp 的 record 組成，不照抄分析文件或 catalog 標籤。

## bsa-voice-index-false-negative

> BSA 語音索引靜默回 0 會捏造「缺語音」；語音不只 .fuz；中文層要看文本不只看路徑

2026-09-18（`modpack-design/content-plan/dialogue/`，工具 `dump_follower_dialogue.py`／`translation_pipeline.py`）：BSA 語音索引失敗時靜默回 0，會把隨從全標「缺語音」；多隨從 plugin（如 OK_Followers.esp）的 voice_type 錯歸屬也會灌高缺語音率；語音檔還有 .xwm/.wav；中文層偵測只看路徑會判 0%；GetIsID 命中要看比較運算子；mod 名寫「JP TEXT」不代表是日文。統計一錯就會推出「要補配音」的假工項。

**How to apply:** 索引結果為 0 一律當錯誤不當數據；多隨從 plugin 用 voice_type 分攤；缺語音率 >20% 先懷疑統計而非 mod。相關：[[voiced-follower-makeover-project]]、[[translation-layer-cost-threshold]]。

## esl-binary-format-facts

> 手寫腳本讀寫 ESL/TES4 二進位格式的關鍵位置：旗標 offset 與 cell 覆寫的 Partial Record 旗標；中途存檔只加 ESL 旗標可行；ESLifier 在 Linux 的跑法

TES4 flags（含 ESL 位元 `0x00000200`）在 **offset 0x08**，不是 0x18（0x18 是 HEDR 子紀錄；`agentctl/handoffs/done/2026-09/home-2026-09-07/chron/REPORT.md:68`）。第三方指南轉述、未實測：ESM-flag plugin 正確區分 persistent／temporary 並依序載入，非 ESM-flag plugin（含 ESL）全部記錄視為 persistent；ESL 新增的 cell record 若被另一 plugin 覆寫、覆寫方沒標 **Partial Record**（xEdit unknown 14 旗標），原 cell 的 temporary 引用會整個被忽略；要保留的引用同時標 persistent。改到 ESL 定義的 cell record 的 patch，先查這兩項。

**中途存檔對已有 plugin「只加 ESL 旗標」實測可行**（2026-10-26 Save132）：條件是新增記錄的 local ID 已在 0x800–0xFFF、FormID 不變；引擎與 SKSE co-save 讀舊檔時按檔名把 full index 重對應到 light 槽，背包、裝備、任務、Papyrus 與對照組 0 差異，存成 light 再讀回也 0 差異（`agentctl/handoffs/home-2026-10-26/esltest/REPORT.md`、`eslapply/REPORT.md`）。**要 compact（改 FormID）的仍會壞既有存檔**，只在新周目做；「已存 light 後再撤旗標」沒測過。省 full 槽先挑「只加旗標」候選（`agentctl/handoffs/home-2026-10-26/shell-esl/tools/esl_candidates.py`＋`tier.py` 的 T1），旗標複本在 overlay 的排序見 [[eslify-overlay-snapshot-goes-stale]]。

**ESLifier 在 Linux**（2026-10-26 v0.16.17，`agentctl/handoffs/home-2026-10-26/eslifierpoc/REPORT.md`）：用官方 Windows exe＋system wine＋建立時就帶 `WINEDLLOVERRIDES=mscoree,mshtml=` 的乾淨 prefix，GUI 放 Xvfb。Proton 的 wine 載不起 Qt；初始化被打斷的 prefix 缺 `syswow64`，BSArch 起不來、BSA 被靜默跳過而 log 照寫「Extracting」；不要改跑 Python 原始碼（facegen／voice 路徑寫成反斜線字面值，`scanner.py:385-398`、`compact_form_ids.py:224`，Linux 下全漏）。輸出是贏家快照，跟 overlay 一樣會過期。施工步驟見 `agentctl/docs/new-playthrough-esl-runbook.md`。

## load-order-and-asset-measurement-pitfalls

> 算衝突／重複／贏家這類統計時，好幾種看起來合理的算法會系統性算錯規模

- **asset winner ≠ plugin winner**：聲音/lip 等資產的贏家由 MO2 VFS 檔案覆蓋順序決定，跟 plugin record 的贏家（load order）是兩套規則，要分別驗，xEdit 單檔視圖不是現役結果（`agentctl/handoffs/done/2026-08/cx-serana/REPORT.md`）。
- **override 筆數 ≠ 衝突筆數**：大多 override 只是「蓋原版」；衝突規模用「現役覆寫索引 ∩ 借用側覆寫索引」的交集算。
- **FormID 漂移比對用 EDID 不用 FULL**：中文層的 FULL 是中文名；EDID 比對由鬆到緊（結尾相符>含名字>完全相符），否則會被部分相符的記錄搶走。
- **同 VFS 路徑的重複貼圖 0 VRAM 成本**：只有「不同 VFS 路徑但位元組相同且同時在場」才重複吃 VRAM。

## papyrus-recompile-for-translation-pitfalls

> 重編譯 Papyrus 源碼來改中文字串，兩個不報錯但會悄悄壞掉的坑

`.psc` 存 UTF-8 無 BOM 會編譯成功，但中文字串變雙重編碼亂碼（編譯器當 ANSI 讀）；一律存 UTF-8 BOM。缺編譯旗標檔／相依 script 時重編既有 `.pex`，翻譯前先做 round-trip：用「未修改」的 `.psc` 編一次，跟原廠 `.pex` 比字串表 multiset、userFlagTable、檔案大小，差異要能被已知因素（編譯者/機器名長度）完全解釋才算工具鏈保真；旗標檔可從既有 `.pex` 的 userFlagTable 位元索引重建（`agentctl/handoffs/done/2026-08/opus-zh-summary/SUMMARY.md:667-694`）。兩個坑都是「編譯成功＝看起來沒事」，round-trip 當硬閘門，不要編完直接上。

## formid-prefix-shifts-cite-plugin-and-local-id

> 新增或移除一個 plugin，排在後面的所有 plugin 的 runtime FormID 前綴都會位移（2026-11-22 Apocalypse `69`→`6A`）；WAIT_USER、文件、主控台指令一律寫「plugin 名＋本地 ID」

完整 FormID 前兩位是 load order 索引，是活值；ESL 的 `FE xxx` 也隨 light plugin 數量位移（[apocalypse-swap REPORT](../../agentctl/handoffs/home-2026-11-22/apocalypse-swap/REPORT.md)、[waituser-runtime REPORT](../../agentctl/handoffs/home-2026-11-22/waituser-runtime/REPORT.md) I10）。寫給人或 agent 的 FormID 用 `XXXXXX:Plugin.esp`（houseCARL 文字格式，見 [common/gotchas](../workflows/common/gotchas.md)）；主控台要用時當場用 `whichmod.py` 或 load order 換算前綴，不抄舊值。
