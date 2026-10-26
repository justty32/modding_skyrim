# 中文層工具與掃描（zhport、靜態掃描、QA）

[lessons 索引](README.md)

## zhport-editorid-fallback-and-hdpt-untranslatable

> 中文層對種子時 FormID 對不上（作者改版重編）要改用 EditorID 比對；HDPT 頭部件 EDID／名稱絕不翻譯（原 type: project）

2026-09-12：`zhport.py` 用 FormID 對舊中文包種子，遇到作者改版整批重編 FormID 時 gaps 被嚴重高估；改用 EditorID 比對就救回。HDPT 頭部件代號要留英文：翻下去 facegen 對名失敗會整顆作廢（見 [[hdpt-edid-must-match-facegen-shape-names]]）。

**Why:** gaps 異常大時工人會急著整包重翻，白花翻譯量又降低一致性。

**How to apply:** 中文層任務 gate 前先看 gaps 比例，>50% 先換 EditorID 比對再決定翻不翻；翻譯範圍排除 HDPT／FLST／種族內部代號，只翻玩家讀得到的欄。

以下 2026-10-23 整理：

- **排除範圍**還包括 pex 腳本裡靠字串比對的 3D 節點名（如 `MoveToNode(self,"FortSungard")`），翻了會讓對應功能失效（內戰地圖旗子插不到位），跑 zhport/pexstrings 前要先掃一輪這類呼叫參數（`agentctl/handoffs/done/2026-10/home-2026-10-10/m152315/REPORT.md`）。
- 本體大版本升級（8,000+ 行等級）不必全文重翻，用舊版翻譯當 corpus 建原文 exact-key map，相同行自動投射、只把變動行與新行放進人工隊列，工作量可降一個數量級（`agentctl/handoffs/done/2026-08-29/cx-serana/REPORT.md:192-199`）。
- 本體整支替換式舊版翻譯遇大版升級，可用 `zhport.py port --seed-match both`（carrier=新版本體、seed=舊版中文、lexicon-pair=舊版英文對舊版中文）把譯文重新映射到新版 esp，gate 用 fontgate(缺字0)+esplib stats --cmp（跟新本體 record 集合比對 same）（`agentctl/handoffs/done/2026-10/home-2026-10-08/want/REPORT-build.md`）。
- zhport 的種子同鍵規則會把載體裡「已經是中文、來自另一層」的欄位也換成種子譯文，不是單純補缺；只想補缺欄不想動既有翻譯時，carrier 與 seed 都用英文版本，缺口欄位改用 `--override` 指定（`agentctl/handoffs/done/2026-10/home-2026-10-10/tradingposts/REPORT.md`）。
- 舊中文層當種子搬字時，種子與載體的 master index 可能不同（例：種子 esp 該 master 前綴 05、載體 03），zhport.py 不做正規化會對不上 FormID 鍵；先核對兩邊 master 清單順序，不一致就把種子譯文轉成與 FormID 無關的 glossary（EditorID 或英文原文為鍵）再搬（`agentctl/handoffs/done/2026-09/home-2026-09-11/zhfix/REPORT.md:26-27`）。

相關：[[translation-layer-cost-threshold]]、[[chinese-diff-ok-but-no-tofu]]

## zhport-whitelist-gap-before-1009

> 2026-10-09 前 zhport 白名單漏 INFO.RNAM／QUST.CNAM／QUST.NNAM／NPC_.SHRT，用它以本體重建的中文層這四類會退回英文

2026-10-09 起 zhport 白名單已含玩家對話選項（`INFO.RNAM`）、任務日誌（`QUST.CNAM`）、任務目標（`QUST.NNAM`）、NPC 短名（`NPC_.SHRT`），並有 `--override`；之後又補了世界地圖區域名 `REGN.RDMP`（有測試斷言，`agentctl/handoffs/done/2026-10/home-2026-10-10/m186441/REPORT.md`）。

**Why:** 10-09 之前用 zhport 以新版本體重建過的中文層可能都有這個靜默退化。清查結果（agentctl `vf-text3/DONE-zhport-audit.md`）：真退化 4 層已修補部署；6 層種子中文包已刪無法判定（BLOCKED，要重下載）；另有 74 支 esp 2,791 欄是自譯時從沒翻過（非退化）。後兩項待使用者裁示。09-11／09-12 的 zhport 層只存在 MO2 `mods/`，沒回寫 mod-library。

**How to apply:** 有人回報「中文層某些選項／日誌是英文」先懷疑這條；清查要使用者點頭才開線。跑完 zhport 若仍有英文殘留，不要只假設是內部代號不翻，要逐條核對是不是玩家讀得到但白名單漏收的欄位類型。相關：[[zhport-editorid-fallback-and-hdpt-untranslatable]]、[[voiced-follower-makeover-project]]、[[bsa-voice-index-false-negative]]。


## prefix-rename-rules-need-longest-first-ordering

> 批次改名規則若有前綴包含關係，短規則排在長規則前面會搶先命中、吃掉本該給長規則的字串

2026-08-27 把 `mco_*` 檔名轉 BFCO 命名時，短規則（`mco_powerattack`）排在長規則（`mco_powerattackloop`）前面會提前命中吃掉長字串、產生錯誤改名；長規則排前即正確，負向對照測試證實順序真的會咬到（`agentctl/handoffs/done/2026-08-27/cx-convert/RESULTS.md:11`）。

**Why:** 規則表的比對順序不會因為「語意上更精確」自動優先，程式只認第一個命中的規則。

**How to apply:** 寫批次改名/替換規則表時，只要規則之間存在字首包含關係，一律把較長（較精確）的規則排在前面；測試 fixture 要刻意把短規則排前做負向對照，證明順序真的會咬到而不是空焗試。

## zh-static-scan-misses-runtime-and-script-strings

> 靜態掃描 ESP record 不是可靠的完整度訊號——運行期注入、pex 內嵌通知、FOMOD toml 顯示字串都在它看不到的地方，而且空殼層能同時通過結構與完成度兩個 gate

Guard Dialogue Overhaul 的對話在 esp 靜態掃描看起來還有上百句英文，實際遊戲內由 DSD 注入覆蓋 97.75% 中文，2 份獨立記錄重複確認（`agentctl/handoffs/done/2026-09/home-2026-09-12/zhfix2/REPORT.md:119`）；反過來，Trade Routes 簡中層本體 32 個 .pex 只出 2 個，出的 2 個裡區域名稱與通知字串仍是英文硬編（`agentctl/handoffs/done/2026-08-27/opus-qa-triage/REPORT.md:199`）；Artisans of Skyrim 的附魔/藥水名稱寫在 FOMOD 產生的 preset toml 裡，DLL 直接讀 toml 顯示，不在 esp 裡（`agentctl/handoffs/done/2026-10/home-2026-10-10/artisans-guard/REPORT.md`）。另一面，一個 ESP 與 carrier 位元組完全相同的空殼層能同時通過結構 Gate A（判等）與完成度 Gate B（讀 ledger 不讀最終 esp）（`agentctl/handoffs/done/2026-09/home-2026-09-03/zhmake/REPORT.md:105`）；翻譯層建置引擎遇資料不符時有的靜默略過（continue）有的直接中止（SystemExit），選錯引擎拿到的失敗語意完全不同（`mod-library/l10n/tools/README.md:45-47,54-59`）。

**Why:** 「esp 沒有英文」「建置沒報錯」都不等於「玩家看到的是中文」，完整度要從多個通道實測才算數；診斷 MCM 問題時也不能只信中文標籤字面，可能譯得像另一個開關，要對照 DLL 實際變數名。

**How to apply:** 盤點覆蓋率把「運行期注入」「pex 通知字串」「ini/toml 設定檔字串」各自列一類分開查；gate 加 sha256(層esp)≠sha256(carrier) 硬檢查，完成度一律從最終產物實測不信 ledger；選建置引擎前先確認它遇不符資料是靜默跳過還是中止。相關：[[bsa-voice-index-false-negative]]

## zh-qa-checker-token-and-variant-false-positives

> 自動化翻譯 QA 檢查器（控制標記守恆／簡繁異體字偵測）本身會有系統性假陽性，命中清單要配例外表才能用

builder 安全 gate 會因控制標記不一致（來源缺 `<10>`、`<Alias=Item>` 大小寫寫成 `<Alias=item>`、尾端換行沒保留）整條跳過詞條，看起來像「沒對上」其實不是版本或 FormID 錯位（`agentctl/handoffs/done/2026-08-31/zh2-2026-08-31/REPORT.md:37-56`）；簡繁判別工具會把「秘/祕」「斗篷/鬥篷」這類正簡同形或異體字誤判成錯字（`agentctl/handoffs/done/2026-09-01/hperk-2026-09-01/REPORT.md`）；中文沒有空白分隔，用 `%[^%\s]+%` 查 token 守恆會把「50% more damage」裡兩個字面 `%` 誤判成佔位符。

**Why:** 這些是工具本身的邊界案例，不是翻譯真的錯，照單全收會逼出錯誤修正方向。

**How to apply:** 詞條「沒對上」先查 builder gate 日誌，核對控制標記大小寫/特殊符號/尾端換行是否一致；簡繁偵測前先核對命中是否落在已知異體字例外表；token 守恆檢查只用 `<…>`／`$Token`／`\n`／`{…}` 四類明確清單比對，不用泛用正則配空白邊界。
