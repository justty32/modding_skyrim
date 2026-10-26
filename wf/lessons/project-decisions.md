# 專案裁示與地圖／內容限制

[lessons 索引](README.md)

## new-save-plan-2026-10-04

> 使用者 10-04 說要開新檔並陸續提新檔前的改動；10-08 調查＋施工完成（拔 Rigmor／FC／Spell Research／Biggie／SkyInteract、IFD Lydia→FDE、DynDOLOD 整組停用），待新檔實機確認

2026-10-04 使用者說要開新檔，並列新檔前想做的改動，說「還有其他的，稍微等我」。清單權威來源：母 repo 頂層 `play-notes.md`（使用者自己寫，10-08 內容）：刪 rigmor 兩個、spell research、forgotten city、biggie traits；Improved Follower Dialogue - Lydia 要換一個（bug／衝突多、有些台詞靜音、OOC）。

**Why:** 使用者要一次說完再施工（見 [[investigate-all-then-install-once]]）。

**How to apply:** 使用者還有新檔想法時先收齊、整理成清單給他確認再派線；刪 mod 前查 DynDOLOD.esp／Occlusion.esp 的 master（[[dyndolod-esp-masters-pin-content-mods]]）與同概念兄弟。10-04 已做：OBody 隨從黑名單＋Zeroed preset 排除、Aniya 皮膚修正、launch-mo2.sh 快取變數（HUD 預設關），報告在 `agentctl/handoffs/home-2026-10-04/`。

使用者裁示（10-08，調查在 `agentctl/handoffs/home-2026-10-08/newsave/REPORT-{quests,systems,lydia}.md`）：Lydia 換 FDE Lydia 1.5＋簡中（安裝包已在庫）；拔 Rigmor 後恢復原版邊境隱形牆（不補 `bBorderRegionsEnabled`）；SkyInteract 隨 Biggie 一起拔。依賴關係：Rigmor 與 IFD Lydia 被 DynDOLOD／Occlusion 釘 master；IFD 另被 `JhNPCBeautyDev.esp`×2、Lydia-Look-From 換臉層當 master，ESLify-Overlay 內有 IFD 修正層副本。

現況（10-08 施工完成，profiles `2cdbf1a`，REPORT-build.md）：39 mod／26 plugin 停用，FDE Lydia 上線，**DynDOLOD 整組停用**（含 Resources、TexGen Fixes；使用者裁「很想停掉」遠景→以後拔 mod 不用重跑 LOD）。待使用者新檔實機確認：Lydia 語音／外觀、主選單外的實際遊玩。殘留未清：OBody 黑名單與 IGYH FLM ini 內的 IFD／Rigmor 條目（無害）。

## campfire-deferred-to-next-playthrough

> 2026-10-10 使用者裁「campfire 下個新檔吧」；Campfire 一族留到下一個新周目一次裝，現周目不裝

2026-10-10 使用者原話「campfire下個新檔吧」。現周目只裝了 Dovah Rider Carriage＋Simple Hunting Overhaul＋DAK（profiles `c3a4321`），Campfire 不裝。

下個新周目要一起評估的包：Campfire 667（排除包內舊 PapyrusUtil.dll）＋Script Optimization 149913，或改用 Campfire 2026（193929，ESL 版只能新檔，含 DAK／SHO 補丁，10-10 時太新：10/3 發布 6 天 5 版）；Survival Skills CSF（171040，接現役 CSF 選單）；可選 Skills of the Wild 37693（會拿掉羅盤）。Frostfall 不裝。調查細節：`agentctl/handoffs/2026-10-10/campfire-frostfall/REPORT.md`。

**Why:** Campfire 的 ESL 版與 Survival Skills 都偏好新檔，中途加裝風險高。

**How to apply:** 使用者說要開新周目時，把這包列進新檔清單一起調查施工（[[investigate-all-then-install-once]]），屆時重查 Campfire 2026 的 bug 頁與版本穩定度。

Campfire 安裝包內含的 `SKSE/Plugins/PapyrusUtil.dll` 會與現役已裝版本衝突——這是非 .esp 層級的衝突，常規 esp 層面的衝突檢查會漏掉，現役雖未裝但一裝即踩。下次新周目真的要裝 Campfire（含 Campfire 2026／Survival Skills CSF）時，安裝步驟要加一條：手動排除該 mod 包裡的 PapyrusUtil.dll，不要整包覆蓋安裝。
source: modpack-design/sources/OPEN.md:18

## self-made-vs-repack-classification

> 2026-10-10 使用者定的 mod 分類：別人 mod 的重包／改版算原作，只有自己從零做的（patch 等）才算自製；中文層另歸漢化

使用者原話（2026-10-10）：「我們修改過的版本，類似這種重包的，都算原作。只有我們自己做的，包括patch等，才算自製」。

**Why:** 頁面篩選「只看非漢化包和自製的」要能看到所有第三方內容；Katana Flattened 這類重包被算成自製就看不到了。

**How to apply:** 分類規則（共用來源 `mod-library/viewer/content_class.py`）：重包、改條件版、修正重包 → 第三方原作；patch、相容件、合併層、overlay、換臉層、轉發層等從零自製 → 自製；中文翻譯層 → 漢化。各頁產頁腳本都要對齊這份規則。

同日補充判準（使用者原話）：「只要我們動過後，那個檔案仍對標於原作檔，那就算」原作——修正層只覆蓋原作同路徑檔（如 Facegen/Mesh-Texture-Fix-Combined、SmeltingPlus-Fix、JH NPC Beauty Dev）算原作；換臉層算自製（使用者確認）。

這條分類規則不等於授權規則——動畫/moveset 格式轉換（如 MCO→BFCO）查證 Nexus 授權頁顯示「私人轉換僅供自用可以，轉換後再發布不被允許」，跟「整包分發」是兩條獨立的授權問題；任何涉及格式轉換/移植的調查，授權查證要分別寫清楚「自用轉換」vs「整包分發」各自的結論，不要用其中一個代表全部（`analysis/mod-survey/action-system/findings/mco-to-bfco-conversion/costs-and-validation.md:27,61-64,113-115`）。


## safe-refactor-characterization-and-extract-method

> 重構前用原檔產生 golden 並 byte-equal 比對，但 byte-equal 在跨平台/CRLF 情境會騙人；抽方法時 continue／具名引數委派編譯器不會報錯卻會執行期出錯。

2026-09-02～09-25 三條教訓：(1) 拆 >300 行工具前先用 fixture 跑 CLI 產生 golden（在原檔上先跑綠），拆後輸出含 exit code byte-equal；沒有已追蹤 fixture 的函式（NIF、DLL、Mongo）要明列殘餘風險（`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-code/REPORT.md:31,52-54`）。(2) Windows 上 python 文字 stdout 會變 CRLF，CLI 原始輸出跟 `--out` 檔／API 輸出不是 byte-identical，但兩次 CLI 互比又一致，驗收抓不到；要比「CLI stdout＝檔案＝API」三者，輸出走 `sys.stdout.buffer.write(...encode("utf-8"))`（`agentctl/handoffs/done/2026-09-02/spike-2026-09-02/REPORT.md:132-136`）。(3) extract-method 兩陷阱：迴圈內 continue 抽出後要改 `return null`＋呼叫端補 `if (x is null) continue`；具名引數傳給 `Action<>` 委派要改位置引數（委派參數名是 arg1..argN）；捕獲多個外層可變變數的區塊優先不抽（`agentctl/handoffs/done/2026-08-27/opus-modforge/RESULTS.md:51`）。

**Why:** 這些陷阱編譯器都不報錯，只有實際執行/跨平台情境才現形。

**How to apply:** 重構交接書寫死 golden-on-original 流程；byte-identical 驗收一律三方比對並確認輸出走 bytes；extract-method 前先掃 continue/break 與具名引數委派呼叫。

## verify-before-acting-process-rigor

> 施工前先驗證：隱性基線要寫下來、QA 多項不可互相外推、升級第三方庫要查授權不只 API、舊報告的版本假設要重查、想動實體路徑先問是否必要。

2026-08～10 五條教訓：(1) 持續影響判定的隱性基線決策（body base、ENB、runtime 版本）一發現它在擋候選就要補文件寫理由/代價/推翻條件，不要停留在 tribal knowledge（`agentctl/handoffs/done/2026-08-27/opus-gaps/staging/body-skin-baseline-2026-08-27.md:54`）。(2) 多項並列 QA 任務每項要獨立終態，不可用已驗項外推到同類未驗項（`agentctl/handoffs/done/2026-08-31/rtqa-2026-08-31/CHARTER.md:7`）。(3) 升級第三方庫解安全漏洞時，新主版本可能牽涉商業授權而非只是 API breaking change，ModForge 的 ImageSharp 4.x Release 組態就需要 Six Labors 商業授權（`agentctl/handoffs/home-2026-10-17/improve/REPORT.md`）。(4) 其他報告裡「現況是什麼版本/狀態」的斷言要重新查證最新 commit 證據，不能直接沿用（同上）。(5) 想重新整理檔案佈局（如按字母分桶）前先問是否真要動實體路徑——mod-library 的 Mongo 掃描快取以絕對路徑為鍵不是內容雜湊，搬動會觸發約 90 GiB 全量重 hash；多數「好找」需求用 repo 外 symlink view 就能滿足（`agentctl/handoffs/done/2026-08-29/cx-libsort/REPORT.md:130-164`）。

**Why:** 都是「省一步查證/記錄，後面要付更大代價」的模式。

**How to apply:** 隱性基線發現即補文件；QA 清單逐項覆核禁止外推；庫升級查授權；舊報告斷言重查；大規模檔案搬動先問必要性。相關：[[verify-waituser-against-logs]]

## follower-dialogue-volume-and-voice-type-notes

> 隨從對話資料分析三個陷阱：換 VoiceType 前要查別家台詞是否只錄了舊聲線、OOC 抱怨先查作者頁有沒有聲明重新詮釋、統計對話量要依角色選對歸因方法而非套單一計數公式。

2026-10-08～10-09 三條教訓：(1) IFD 把萊迪亞 VoiceType 從原版 FemaleEvenToned 改成自訂聲線，本包裡約 170 句由 Inigo/Vilja/Feris/RDO/Rigmor 等別家 mod 寫給她、只錄了原版聲線的台詞，到她嘴裡只剩字幕沒聲音（Fuz Ro D'oh 讓字幕照播，容易被誤判為 bug）（`agentctl/handoffs/done/2026-10/home-2026-10-08/newsave/REPORT-lydia.md`）。(2) 使用者反映隨從「OOC」，查證發現 IFD 作者頁明寫刻意重新詮釋人設（不想寫成典型忠僕），疊加「別家台詞用舊人設寫」造成混搭觀感，不是翻譯或腳本錯誤（同上）。(3) 跨 66 位隨從對話量比較：naive OR INFO 計數被同 plugin 角色灌水，只認 GetIsID 的嚴格計數對共用 voice_type 的角色嚴重低估（某角色嚴格值 167 vs 實際 2655）；正確做法按角色分情況取 GetIsID∪voice_type 聯集並記錄 attribution_method（`modpack-design/content-plan/dialogue/SUMMARY.md:12-17`）。

**Why:** plugin／voice_type 的共享關係會讓單純的字面統計或換設定操作產生隱藏副作用。

**How to apply:** 換隨從 VoiceType 前掃全載入順序裡引用該 NPC 的 INFO，比對語音檔錄在哪個 voice type；收到 OOC 反映先查作者頁聲明；統計對話量先判斷角色是否共用 plugin/voice_type 再選歸因方法。
