# 中文層工具與掃描（zhport、靜態掃描、QA）

[lessons 索引](README.md)｜部署 gate 見 [translation-and-zh](translation-and-zh.md)，政策見 [zh-policy-and-naming](zh-policy-and-naming.md)

## zhport-editorid-fallback-and-hdpt-untranslatable
<a id="zhport-whitelist-gap-before-1009"></a>

> 中文層對種子時 FormID 對不上（作者改版重編）要改用 EditorID 比對；HDPT 頭部件 EDID／名稱絕不翻譯；白名單漏收的欄位會靜默留英文

2026-09-12：`zhport.py` 用 FormID 對舊中文包種子，遇到作者改版整批重編 FormID 時 gaps 被嚴重高估，改用 EditorID 比對就救回（gaps 虛高會誘人整包重翻，白花翻譯量又降低一致性）。HDPT 頭部件代號要留英文：翻下去 facegen 對名失敗會整顆作廢（見 [[hdpt-edid-must-match-facegen-shape-names]]）。

**How to apply:** 中文層任務 gate 前先看 gaps 比例，>50% 先換 EditorID 比對再決定翻不翻；翻譯範圍排除 HDPT／FLST／種族內部代號，只翻玩家讀得到的欄。

**排除範圍**還包括 pex 腳本裡靠字串比對的 3D 節點名（如 `MoveToNode(self,"FortSungard")`），翻了會讓對應功能失效（內戰地圖旗子插不到位），跑 zhport/pexstrings 前要先掃一輪這類呼叫參數（`agentctl/handoffs/done/2026-10/home-2026-10-10/m152315/REPORT.md`）。

**白名單**（`mod-library/l10n/tools/zhport_fields.py`）含玩家對話選項 `INFO.RNAM`、任務日誌 `QUST.CNAM`、任務目標 `QUST.NNAM`、NPC 短名 `NPC_.SHRT`、世界地圖區域名 `REGN.RDMP`（2026-10-09，mod-library `357bf71`、`f6e59e0`；`agentctl/handoffs/done/2026-10/home-2026-10-10/m186441/REPORT.md`）。有人回報「中文層某些選項／日誌是英文」、或跑完 zhport 仍有英文殘留時，不要只假設是內部代號不翻，要逐條核對是不是玩家讀得到但白名單漏收的欄位類型，漏了就補白名單＋測試。

本體大版本升級（8,000+ 行等級）不必全文重翻，用舊版翻譯當 corpus 建原文 exact-key map，相同行自動投射、只把變動行與新行放進人工隊列，工作量可降一個數量級（`agentctl/handoffs/done/2026-08-29/cx-serana/REPORT.md:192-199`）。本體整支替換式舊版翻譯遇大版升級，可用 `zhport.py port --seed-match both`（carrier=新版本體、seed=舊版中文、lexicon-pair=舊版英文對舊版中文）把譯文重新映射到新版 esp，gate 用 fontgate(缺字0)+esplib stats --cmp（跟新本體 record 集合比對 same）（`agentctl/handoffs/done/2026-10/home-2026-10-08/want/REPORT-build.md`）。

zhport 的種子同鍵規則會把載體裡「已經是中文、來自另一層」的欄位也換成種子譯文，不是單純補缺；只想補缺欄不想動既有翻譯時，carrier 與 seed 都用英文版本，缺口欄位改用 `--override` 指定（`agentctl/handoffs/done/2026-10/home-2026-10-10/tradingposts/REPORT.md`）。

舊中文層當種子搬字時，種子與載體的 master index 可能不同（例：種子 esp 該 master 前綴 05、載體 03），zhport.py 不做正規化會對不上 FormID 鍵；先核對兩邊 master 清單順序，不一致就把種子譯文轉成與 FormID 無關的 glossary（EditorID 或英文原文為鍵）再搬（`agentctl/handoffs/done/2026-09/home-2026-09-11/zhfix/REPORT.md:26-27`）。

**種子同鍵不比英文**（2026-10-26）：seed 模式只看鍵（含第幾次出現）就搬譯文，不檢查載體英文跟種子英文是否相同；補丁版改過按鈕數、樓層分法或名稱時會錯植（例：MESG 刪掉一個按鈕後序位移，seed 把「An Archive」配成「实验室」，按下去選到的跟字面不一樣），而且 `zhport.py verify` 抓不到（它只驗「改成報告寫的字」）（`agentctl/handoffs/home-2026-10-26/cowzh/REPORT.md`「建層」節）。補丁類載體不給 seed，改用 `--override` 逐欄明列，自動部分只收「種子同鍵且英文逐字相同」者。

**記錄數不是可翻字串數**：交接書與盤點常寫「N 筆 record」，那是 plugin 的記錄數，多數是 REFR／NAVM／CELL 配置、沒有字（例：7,467 筆記錄的補丁只有 35 個非空可翻欄位，`agentctl/handoffs/home-2026-10-26/cowzh/REPORT.md`「範圍與一個更正」）。估中文層工作量、決定派工前，先跑 `zhport.py scan` 數白名單欄位。

相關：[[translation-layer-cost-threshold]]、[[no-cht-chs-preference]]、[[voiced-follower-makeover-project]]、[[bsa-voice-index-false-negative]]

## zh-static-scan-misses-runtime-and-script-strings

> 靜態掃描 ESP record 不是可靠的完整度訊號——運行期注入、pex 內嵌通知、FOMOD toml 顯示字串都在它看不到的地方，而且空殼層能同時通過結構與完成度兩個 gate

esp 靜態掃描還有英文的對話，遊戲內可能已由 DSD 注入成中文（`agentctl/handoffs/done/2026-09/home-2026-09-12/zhfix2/REPORT.md:119`）；反過來，中文層可能只附部分 .pex，通知字串仍是英文硬編（`agentctl/handoffs/done/2026-08-27/opus-qa-triage/REPORT.md:199`）；顯示名稱也可能寫在 FOMOD 產生的 preset toml、由 DLL 直接讀，不在 esp 裡（`agentctl/handoffs/done/2026-10/home-2026-10-10/artisans-guard/REPORT.md`）。ESP 與 carrier 位元組完全相同的空殼層能同時通過結構 Gate A（判等）與完成度 Gate B（讀 ledger 不讀最終 esp）（`agentctl/handoffs/done/2026-09/home-2026-09-03/zhmake/REPORT.md:105`）；翻譯層建置引擎遇資料不符時有的靜默略過（continue）有的直接中止（SystemExit），選錯引擎拿到的失敗語意完全不同（`mod-library/l10n/tools/README.md:45-47,54-59`）。

**Why:** 「esp 沒有英文」「建置沒報錯」都不等於「玩家看到的是中文」，完整度要從多個通道實測才算數；診斷 MCM 問題時也不能只信中文標籤字面，可能譯得像另一個開關，要對照 DLL 實際變數名。

**How to apply:** 盤點覆蓋率把「運行期注入」「pex 通知字串」「ini/toml 設定檔字串」各自列一類分開查；gate 加 sha256(層esp)≠sha256(carrier) 硬檢查，完成度一律從最終產物實測不信 ledger；選建置引擎前先確認它遇不符資料是靜默跳過還是中止。相關：[[bsa-voice-index-false-negative]]

## zh-qa-checker-token-and-variant-false-positives

> 自動化翻譯 QA 檢查器（控制標記守恆／簡繁異體字偵測）本身會有系統性假陽性，命中清單要配例外表才能用

builder 安全 gate 會因控制標記不一致（來源缺 `<10>`、`<Alias=Item>` 大小寫寫成 `<Alias=item>`、尾端換行沒保留）整條跳過詞條，看起來像「沒對上」其實不是版本或 FormID 錯位（`agentctl/handoffs/done/2026-08-31/zh2-2026-08-31/REPORT.md:37-56`）；簡繁判別工具會把「秘/祕」「斗篷/鬥篷」這類正簡同形或異體字誤判成錯字（`agentctl/handoffs/done/2026-09-01/hperk-2026-09-01/REPORT.md`）；中文沒有空白分隔，用 `%[^%\s]+%` 查 token 守恆會把「50% more damage」裡兩個字面 `%` 誤判成佔位符。

**Why:** 這些是工具本身的邊界案例，不是翻譯真的錯，照單全收會逼出錯誤修正方向。

**How to apply:** 詞條「沒對上」先查 builder gate 日誌，核對控制標記大小寫/特殊符號/尾端換行是否一致；簡繁偵測前先核對命中是否落在已知異體字例外表；token 守恆檢查只用 `<…>`／`$Token`／`\n`／`{…}` 四類明確清單比對，不用泛用正則配空白邊界。
