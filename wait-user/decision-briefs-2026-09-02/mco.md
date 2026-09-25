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

- **落地**：`../agentctl/handoffs/home-2026-09-02/mco2/`。

### mco-2　SCAR 2 接受 GitHub 手動下載？
- **問題**：SCAR 2 v2.01 只在 GitHub，明示支援 1.6.1170；Nexus 仍是舊 v1.06b。
- **證據**：[mco REPORT][mco-report]。
- **選項與後果**：A 接受＝可滿足既定 SCAR 2；B 拒絕＝P2 等候；C 用 Nexus 舊版＝偏離裁示。
- **我方建議＋門檻**：選 A；只收 1 個官方 release asset，hash 登記且版本明列 1170。
> A
- **落地**：`../modpack-design/content-plan/gameplay/data/mco-migration-steps.csv` P2-06 `ruling`。

### mco-3　11 件 ASK ESP 是否整批保留？
- **問題**：11/11 只有 ESP、沒有 SKSE DLL；風險已縮成技能／效果語意。
- **證據**：[mco REPORT][mco-report]。
- **選項與後果**：A 全留＝保留原動作效果；B 全停＝最保守但功能損失；C 逐件試＝較慢。
- **我方建議＋門檻**：選 A；11/11 各自可回滾且缺 master=0 才整批 RESTORE。
> A
- **落地**：`../modpack-design/content-plan/gameplay/data/mco-migration-steps.csv` P3-04 `ruling`。

