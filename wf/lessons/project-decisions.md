# 專案裁示與開發／驗證流程的嚴謹度

[lessons 索引](README.md)

## new-save-plan-2026-10-04

> 使用者 10-04 說要開新檔並陸續提新檔前的改動；10-08 調查＋施工完成（拔 Rigmor／FC／Spell Research／Biggie／SkyInteract、IFD Lydia→FDE、DynDOLOD 整組停用），待新檔實機確認

2026-10-04 使用者說要開新檔、列新檔前想做的改動，說「還有其他的，稍微等我」。清單權威來源：母 repo 頂層 `play-notes.md`（使用者自己寫）：刪 rigmor 兩個、spell research、forgotten city、biggie traits；Improved Follower Dialogue - Lydia 要換一個（bug／衝突多、有些台詞靜音、OOC）。

使用者裁示（10-08，調查在 `agentctl/handoffs/home-2026-10-08/newsave/REPORT-{quests,systems,lydia}.md`）：Lydia 換 FDE Lydia 1.5＋簡中；拔 Rigmor 後恢復原版邊境隱形牆（不補 `bBorderRegionsEnabled`）；SkyInteract 隨 Biggie 一起拔；**DynDOLOD 整組停用**（含 Resources、TexGen Fixes；使用者裁「很想停掉」遠景）。施工在 profiles `2cdbf1a`（REPORT-build.md）；10-04 先做的 OBody 隨從黑名單＋Zeroed preset 排除、Aniya 皮膚修正、launch-mo2.sh 快取變數（HUD 預設關）報告在 `agentctl/handoffs/home-2026-10-04/`。殘留無害條目：OBody 黑名單與 IGYH FLM ini 內的 IFD／Rigmor；ESLify-Overlay 內有 IFD 修正層副本。

**How to apply:** 使用者有新檔想法時先收齊、整理成清單給他確認再派線（[[investigate-all-then-install-once]]）。DynDOLOD 停用期間拔 mod 不用重跑 LOD；重新啟用 DynDOLOD 前，刪 mod 要查 DynDOLOD.esp／Occlusion.esp 的 master（[[dyndolod-esp-masters-pin-content-mods]]）與同概念兄弟。

## campfire-deferred-to-next-playthrough

> 2026-10-10 使用者裁「campfire 下個新檔吧」；Campfire 一族留到下一個新周目一次裝，現周目不裝

2026-10-10 使用者原話「campfire下個新檔吧」。現周目裝的是 Dovah Rider Carriage＋Simple Hunting Overhaul＋DAK（profiles `c3a4321`），Campfire 與 Frostfall 不裝。Campfire 的 ESL 版與 Survival Skills 都偏好新檔，中途加裝風險高。

下個新周目一起評估：Campfire 667＋Script Optimization 149913，或 Campfire 2026（193929，ESL 版只能新檔，含 DAK／SHO 補丁）；Survival Skills CSF（171040，接現役 CSF 選單）；可選 Skills of the Wild 37693（會拿掉羅盤）。調查：`agentctl/handoffs/2026-10-10/campfire-frostfall/REPORT.md`。

**How to apply:** 使用者說要開新周目時把這包列進新檔清單（[[investigate-all-then-install-once]]），屆時重查 Campfire 2026 的 bug 頁與版本穩定度。裝任何 Campfire 包時，手動排除包內的 `SKSE/Plugins/PapyrusUtil.dll`（會蓋掉現役版本；非 .esp 衝突，esp 層檢查抓不到），不整包覆蓋。source: modpack-design/sources/OPEN.md:18

## self-made-vs-repack-classification

> 2026-10-10 使用者定的 mod 分類：別人 mod 的重包／改版算原作，只有自己從零做的（patch 等）才算自製；中文層另歸漢化

使用者原話（2026-10-10）：「我們修改過的版本，類似這種重包的，都算原作。只有我們自己做的，包括patch等，才算自製」。同日補充（使用者原話）：「只要我們動過後，那個檔案仍對標於原作檔，那就算」原作——換臉層算自製（使用者確認）。

**Why:** 頁面篩選「只看非漢化包和自製的」要看得到所有第三方內容。

**How to apply:** 分類規則（共用來源 `mod-library/viewer/content_class.py`，各產頁腳本對齊它）：重包、改條件版、修正重包、只覆蓋原作同路徑檔的修正層（如 Facegen/Mesh-Texture-Fix-Combined、SmeltingPlus-Fix、JH NPC Beauty Dev）→ 第三方原作；patch、相容件、合併層、overlay、換臉層、轉發層等從零自製 → 自製；中文翻譯層 → 漢化。

分類規則不等於授權規則：格式轉換／移植（如 MCO→BFCO）的授權要分開寫「自用轉換」與「整包分發」兩個結論——該例 Nexus 授權頁是「私人轉換僅供自用可以，轉換後再發布不被允許」（出處：MCO→BFCO 轉換研究的授權查證，已封存）。

## safe-refactor-characterization-and-extract-method

> 重構前用原檔產生 golden 並 byte-equal 比對，但 byte-equal 在跨平台/CRLF 情境會騙人；抽方法時 continue／具名引數委派編譯器不會報錯卻會執行期出錯。

2026-09 三條，編譯器都不報錯；重構交接書照寫：

1. 拆 >300 行工具前，先在原檔上用 fixture 跑 CLI 產生 golden，拆後輸出含 exit code byte-equal；沒有已追蹤 fixture 的函式（NIF、DLL、Mongo）明列殘餘風險（`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-code/REPORT.md:31,52-54`）。
2. Windows 上 python 文字 stdout 會變 CRLF，CLI 輸出與 `--out` 檔／API 輸出不 byte-identical，但兩次 CLI 互比一致而抓不到；要比「CLI stdout＝檔案＝API」三方，輸出走 `sys.stdout.buffer.write(...encode("utf-8"))`（`agentctl/handoffs/done/2026-09-02/spike-2026-09-02/REPORT.md:132-136`）。
3. extract-method：迴圈內 continue 抽出後改 `return null`＋呼叫端 `if (x is null) continue`；具名引數傳給 `Action<>` 委派要改位置引數（參數名是 arg1..argN）；捕獲多個外層可變變數的區塊優先不抽（`agentctl/handoffs/done/2026-08-27/opus-modforge/RESULTS.md:51`）。

## verify-before-acting-process-rigor

> 施工前先驗證：隱性基線要寫下來、QA 多項不可互相外推、升級第三方庫要查授權不只 API、舊報告的版本假設要重查、想動實體路徑先問是否必要。

都是「省一步查證／記錄，後面付更大代價」（2026-08～10）：

1. 持續影響判定的隱性基線（body base、ENB、runtime 版本）一發現它在擋候選，就補文件寫理由／代價／推翻條件（`agentctl/handoffs/done/2026-08-27/opus-gaps/staging/body-skin-baseline-2026-08-27.md:54`）。
2. 多項並列 QA 每項要獨立終態，不用已驗項外推同類未驗項（`agentctl/handoffs/done/2026-08-31/rtqa-2026-08-31/CHARTER.md:7`）。
3. 升級第三方庫解漏洞時查授權不只 API：ModForge 的 ImageSharp 4.x Release 組態要 Six Labors 商業授權（`agentctl/handoffs/home-2026-10-17/improve/REPORT.md`）。
4. 別份報告「現況是什麼版本／狀態」的斷言，要對最新 commit 重查（同上）。
5. 想重整檔案佈局（如按字母分桶）先問是否真要動實體路徑：mod-library 的 Mongo 掃描快取以絕對路徑為鍵，搬動觸發約 90 GiB 全量重 hash；「好找」多半用 repo 外 symlink view 就夠（`agentctl/handoffs/done/2026-08-29/cx-libsort/REPORT.md:130-164`）。

相關：[[verify-waituser-against-logs]]

## follower-dialogue-volume-and-voice-type-notes

> 隨從對話資料分析三個陷阱：換 VoiceType 前要查別家台詞是否只錄了舊聲線、OOC 抱怨先查作者頁有沒有聲明重新詮釋、統計對話量要依角色選對歸因方法而非套單一計數公式。

2026-10-08～10-09（前兩條出處 `agentctl/handoffs/done/2026-10/home-2026-10-08/newsave/REPORT-lydia.md`）：

1. 換 VoiceType 會讓別家 mod 寫給該 NPC、只錄了原聲線的台詞變成只剩字幕沒聲音（例：IFD 改了萊迪亞的聲線，Inigo/Vilja/RDO 等寫給她的台詞全啞；Fuz Ro D'oh 讓字幕照播，易誤判為 bug）。換之前掃全載入順序裡引用該 NPC 的 INFO，比對語音檔錄在哪個 voice type。
2. 隨從「OOC」先查作者頁：IFD 作者明寫刻意重新詮釋人設，疊加別家台詞用舊人設寫造成混搭觀感，不是翻譯或腳本錯。
3. 跨隨從比對話量：naive OR INFO 計數會被同 plugin 角色灌水，只認 GetIsID 會嚴重低估共用 voice_type 的角色；按角色取 GetIsID∪voice_type 聯集並記錄 attribution_method（`modpack-design/content-plan/dialogue/SUMMARY.md:12-17`）。
