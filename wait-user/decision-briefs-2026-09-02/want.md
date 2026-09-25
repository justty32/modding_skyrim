## want

> 我還沒實際開始玩，沒有舊週目。

### want-1　Gray Cowl 要不要換周年版？
- **問題**：周年版須新周目，且會放棄現役舊版繁中層。
- **證據**：[26 件審查][want-review]。
- **選項與後果**：A 留舊版＝可續檔、有中文；B 換周年版＝新內容，但新周目且中文歸零。
- **我方建議＋門檻**：選 A；只有「新周目＋周年版中文層 1 件對版」才改 B。
> 換
- **落地**：`../modpack-design/sources/mod-want-review-2026-09-02.json` `ruling` 欄；`../agentctl/handoffs/home-2026-09-02/rule/zh-check.md`。

### want-2　Unique Thane Weapons 還是 LOTD？
- **問題**：`35497` 與後續 GO 的 LOTD 互斥。
- **證據**：[26 件審查][want-review]。
- **選項與後果**：A 留 LOTD＝大型內容方向不變；B 裝 `35497`＝放棄 LOTD 相容。
- **我方建議＋門檻**：選 A；若 LOTD 延後至少 1 個周目才改 B。
> 換LOTD
- **落地**：`../modpack-design/sources/mod-want-review-2026-09-02.json` `ruling` 欄；使用者 20:40 口頭確認＝A。

### want-3　兩套魔法要不要接受平衡風險？
- **問題**：`139953`／`145420` 是加法，但分別碰現役魔法與附魔平衡。
- **證據**：[26 件審查][want-review]。
- **選項與後果**：A 暫緩＝維持平衡；B 兩件都進＝內容多、調平成本高；C 逐件進＝較易回滾。
- **我方建議＋門檻**：選 C；一次只進 1 件，未處理 record 衝突須為 0。
>　B
- **落地**：`../modpack-design/sources/mod-want-review-2026-09-02.json` `ruling` 欄。

### want-4　要不要建新周目候選清單？
- **問題**：`72772` 必須新周目；`145599` 還另與現役 Alternate Start 衝突。
- **證據**：[26 件審查][want-review]。
- **選項與後果**：A 建清單＝集中延後；B 不建＝逐件散置；C 全放棄＝最省維護。
- **我方建議＋門檻**：選 A；新周目限定件達 2 件即建單，`145599` 仍維持 NO-GO。
> B
- **落地**：`../modpack-design/sources/mod-want-review-2026-09-02.json` `ruling` 欄。

### want-5　15 件 GO 要不要開下載單？
- **問題**：15 件已判 GO，本場尚未下載或寄單。
- **證據**：[want REPORT][want-report]、[26 件審查][want-review]。
- **選項與後果**：A 開單＝先入庫、不安裝；B 暫停＝零下載、延後施工。
- **我方建議＋門檻**：選 A；15/15 的 fileId／bytes 齊全且 4K 檔為 0 才送單。
> 開
- **落地**：`../modpack-design/sources/mod-want-review-2026-09-02.json` `ruling` 欄。

