## home

### home-1　停用 SDA 舊 4.1.1.3 中文層？
- **問題**：4.3.2 本體與 exact 中文已啟用，但舊中文層仍在 modlist:29 啟用。
- **證據**：[SDA／Mihail 預檢][home-sda]。
- **選項與後果**：A 停用＝避免舊 record／asset 回滾；B 保留＝多一層但有版本污染風險。
- **我方建議＋門檻**：選 A；新兩層在庫、啟用且 topology gate 3/3 PASS 即停。
> 去搜尋看有沒有新中文，若沒有，那就我們自己做。
- **落地**：`home-setup.md`「Serana Dialogue Add-On 4.3.2」段。

### home-2　Mihail 首批取 8 件還是自然核心 4–6 件？
- **問題**：現清單 8 件含 Dwarven／Goblins／High Fantasy，超出原裁示語意。
- **證據**：[SDA／Mihail 預檢][home-sda]。
- **選項與後果**：A 8 件全進＝利用既有 gate、擴張範圍；B 重選 4–6 件＝守原裁示、較慢。
- **我方建議＋門檻**：選 B；hand-placed 自然件最多 6 件，非自然核心為 0。
> A
- **落地**：`home-setup.md`「Mihail 自然核心首批」段。

### home-3　mo2ctl 漂移採哪種修法？
- **問題**：三類 writer 不同步 manifest，現有差集為 181／64。
- **證據**：[漂移診斷][home-mo2]。
- **選項與後果**：A mutation 收口＝中成本、治 mo2ctl；B 關 MO2 reconcile＝涵蓋外部寫回；C 拆 checkpoint＝最完整但高成本。
- **我方建議＋門檻**：選 A；enable／disable／install／uninstall 4/4 共用 `commit_profile()` 且測試全綠才落地。
> C
- **落地**：`home-setup.md`「現役 modlist 整合度盤點」第 3 項。

### home-4　降版用 FULL 回填還是 patcher？
- **問題**：FULL 16 GB 已在本機；patcher 尚未到庫且須精確匹配升版來源。
- **證據**：[降版就緒報告][home-down]。
- **選項與後果**：A FULL 回填＝今晚可離線做；B patcher＝較省搬檔但仍待下載；C 暫不升＝零降版風險、AE 延後。
- **我方建議＋門檻**：選 A；Steam 離線且代表檔 12/12 hash 通過才寫回。
> A
- **落地**：`home-setup.md`「購買 AE 升級」段。

