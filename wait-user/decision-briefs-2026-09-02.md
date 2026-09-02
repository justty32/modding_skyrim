# 今晚裁決簡報（2026-09-02）

今晚四隊只調查、整理可執行方案，未動 profile。
共 **15 題**；建議每題後只寫一個字母，想改門檻再補數字。
回覆例：`want-1 A；home-2 B（改 5 件）`。

| 隊 | REPORT 題數 | 本檔題數 |
|---|---:|---:|
| want | 5 | 5 |
| home | 4 | 4 |
| mco | 3 | 3 |
| vfo | 3 | 3 |
| **合計** | **15** | **15** |

## want

### want-1　Gray Cowl 要不要換周年版？
- **問題**：周年版須新周目，且會放棄現役舊版繁中層。
- **證據**：[26 件審查][want-review]。
- **選項與後果**：A 留舊版＝可續檔、有中文；B 換周年版＝新內容，但新周目且中文歸零。
- **我方建議＋門檻**：選 A；只有「新周目＋周年版中文層 1 件對版」才改 B。

### want-2　Unique Thane Weapons 還是 LOTD？
- **問題**：`35497` 與後續 GO 的 LOTD 互斥。
- **證據**：[26 件審查][want-review]。
- **選項與後果**：A 留 LOTD＝大型內容方向不變；B 裝 `35497`＝放棄 LOTD 相容。
- **我方建議＋門檻**：選 A；若 LOTD 延後至少 1 個周目才改 B。

### want-3　兩套魔法要不要接受平衡風險？
- **問題**：`139953`／`145420` 是加法，但分別碰現役魔法與附魔平衡。
- **證據**：[26 件審查][want-review]。
- **選項與後果**：A 暫緩＝維持平衡；B 兩件都進＝內容多、調平成本高；C 逐件進＝較易回滾。
- **我方建議＋門檻**：選 C；一次只進 1 件，未處理 record 衝突須為 0。

### want-4　要不要建新周目候選清單？
- **問題**：`72772` 必須新周目；`145599` 還另與現役 Alternate Start 衝突。
- **證據**：[26 件審查][want-review]。
- **選項與後果**：A 建清單＝集中延後；B 不建＝逐件散置；C 全放棄＝最省維護。
- **我方建議＋門檻**：選 A；新周目限定件達 2 件即建單，`145599` 仍維持 NO-GO。

### want-5　15 件 GO 要不要開下載單？
- **問題**：15 件已判 GO，本場尚未下載或寄單。
- **證據**：[want REPORT][want-report]、[26 件審查][want-review]。
- **選項與後果**：A 開單＝先入庫、不安裝；B 暫停＝零下載、延後施工。
- **我方建議＋門檻**：選 A；15/15 的 fileId／bytes 齊全且 4K 檔為 0 才送單。

## home

### home-1　停用 SDA 舊 4.1.1.3 中文層？
- **問題**：4.3.2 本體與 exact 中文已啟用，但舊中文層仍在 modlist:29 啟用。
- **證據**：[SDA／Mihail 預檢][home-sda]。
- **選項與後果**：A 停用＝避免舊 record／asset 回滾；B 保留＝多一層但有版本污染風險。
- **我方建議＋門檻**：選 A；新兩層在庫、啟用且 topology gate 3/3 PASS 即停。

### home-2　Mihail 首批取 8 件還是自然核心 4–6 件？
- **問題**：現清單 8 件含 Dwarven／Goblins／High Fantasy，超出原裁示語意。
- **證據**：[SDA／Mihail 預檢][home-sda]。
- **選項與後果**：A 8 件全進＝利用既有 gate、擴張範圍；B 重選 4–6 件＝守原裁示、較慢。
- **我方建議＋門檻**：選 B；hand-placed 自然件最多 6 件，非自然核心為 0。

### home-3　mo2ctl 漂移採哪種修法？
- **問題**：三類 writer 不同步 manifest，現有差集為 181／64。
- **證據**：[漂移診斷][home-mo2]。
- **選項與後果**：A mutation 收口＝中成本、治 mo2ctl；B 關 MO2 reconcile＝涵蓋外部寫回；C 拆 checkpoint＝最完整但高成本。
- **我方建議＋門檻**：選 A；enable／disable／install／uninstall 4/4 共用 `commit_profile()` 且測試全綠才落地。

### home-4　降版用 FULL 回填還是 patcher？
- **問題**：FULL 16 GB 已在本機；patcher 尚未到庫且須精確匹配升版來源。
- **證據**：[降版就緒報告][home-down]。
- **選項與後果**：A FULL 回填＝今晚可離線做；B patcher＝較省搬檔但仍待下載；C 暫不升＝零降版風險、AE 延後。
- **我方建議＋門檻**：選 A；Steam 離線且代表檔 12/12 hash 通過才寫回。

## mco

### mco-1　今晚切 P2，並用非 DXP 路徑？
- **問題**：cx-mco5 找到同一 MAIN 的 `Modern Combat Overhaul` FOMOD 選項；本體與 1.6.1170 支援層都在庫。
- **證據**：[非 DXP 表][mco-nondxp]、[mco REPORT][mco-report]。
- **選項與後果**：A 非 DXP＝守原裁示；B DXP＝攻速語意失效；C 等＝今晚不切。
- **我方建議＋門檻**：選 A；兩個庫內檔 2/2 hash 命中且切後缺 master=0 才進 P3。

| 來源 | 版本 | 風險 |
|---|---|---|
| 175044／FOMOD Modern Combat Overhaul | 1.6.0.6 | 推薦；庫內、無 DLL，須 85491 |
| 85491 MCO Universal Support | 1.0 | 庫內且涵蓋 1.6.1170；屬 archived |
| 117275 Bug Fixes | 2.0.6 | 非本體，1170 僅間接證據 |
| 83383 No Directional Power Attacks | 2.0 | 非框架且與 117275 不相容 |
| 45378 Attack Behavior Revamp | 5.2 | 另一舊框架，無 1170 證據 |

### mco-2　SCAR 2 接受 GitHub 手動下載？
- **問題**：SCAR 2 v2.01 只在 GitHub，明示支援 1.6.1170；Nexus 仍是舊 v1.06b。
- **證據**：[mco REPORT][mco-report]。
- **選項與後果**：A 接受＝可滿足既定 SCAR 2；B 拒絕＝P2 等候；C 用 Nexus 舊版＝偏離裁示。
- **我方建議＋門檻**：選 A；只收 1 個官方 release asset，hash 登記且版本明列 1170。

### mco-3　11 件 ASK ESP 是否整批保留？
- **問題**：11/11 只有 ESP、沒有 SKSE DLL；風險已縮成技能／效果語意。
- **證據**：[mco REPORT][mco-report]。
- **選項與後果**：A 全留＝保留原動作效果；B 全停＝最保守但功能損失；C 逐件試＝較慢。
- **我方建議＋門檻**：選 A；11/11 各自可回滾且缺 master=0 才整批 RESTORE。

## vfo

### vfo-1　Sofia 外觀選哪一組？
- **問題**：81155、100407 已在庫且 closure 完整；其餘候選仍須下載或補查。
- **證據**：[Sofia 簡報][vfo-look]。
- **選項與後果**：A 81155＝最小、須 forward WNAM；B 100407＝另一張臉、同樣須 forward；C 另三組＝先下載補查。
- **我方建議＋門檻**：選 A；下載 0 件、髮型 closure 3/3 OK、WNAM 1 筆 forward 後才施工。

### vfo-2　要不要動 53 位隨從的作者平衡？
- **問題**：53/53 都是 AutoCalc，多數有自訂 class；現在改會覆蓋作者設計。
- **證據**：[vfo REPORT][vfo-report]。
- **選項與後果**：A 不動＝保留原意；B 全體正規化＝整齊但侵入大；C 只修離群＝需實測。
- **我方建議＋門檻**：選 A；同一隨從在 3 場中至少 2 場獨力處理逾 50% 敵人才改 C。

### vfo-3　clothes／armour 解除後，裝備面怎麼做？
- **問題**：11 列僅 outfit；42 列牽涉 quest／alias，Sofia 還有自動重穿流程。
- **證據**：[綁定機制][vfo-cloth]、[vfo REPORT][vfo-report]。
- **選項與後果**：A 裝備不動＝最穩；B 53 位全改＝可能與腳本搶控制；C 分層＝先安全列、複雜列逐件查。
- **我方建議＋門檻**：選 C；先處理 11 件 outfit-only，42 件 alias-quest 不准批改（批次件數 0）。

[want-review]: ../modpack-design/sources/mod-want-review-2026-09-02.md
[want-report]: ../agentctl/handoffs/home-2026-09-02/want/REPORT.md
[home-sda]: ../agentctl/handoffs/home-2026-09-02/home/sda-mihail-library-precheck.md
[home-mo2]: ../agentctl/handoffs/home-2026-09-02/home/mo2ctl-drift-diagnosis.md
[home-down]: ../agentctl/handoffs/home-2026-09-02/home/downgrade-readiness.md
[mco-nondxp]: ../agentctl/handoffs/home-2026-09-02/mco/cx-mco5/nondxp-options.csv
[mco-report]: ../agentctl/handoffs/home-2026-09-02/mco/REPORT.md
[vfo-look]: ../modpack-design/content-plan/followers/voiced-follower-overhaul/sofia-look-decision-brief-2026-09-02.md
[vfo-report]: ../agentctl/handoffs/home-2026-09-02/vfo/REPORT.md
[vfo-cloth]: ../agentctl/handoffs/home-2026-09-02/vfo/cx-vfo4/clothing-binding-mechanism.md
