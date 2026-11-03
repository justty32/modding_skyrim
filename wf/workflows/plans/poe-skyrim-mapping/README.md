# poe-skyrim-mapping：PoE 星盤效果落地 Skyrim（定案設計＋施工計畫）

[plans](../README.md)｜出計畫 2026-11-03｜狀態：**第一波離線完成，實機待驗；第二波未施工**

把 POTC IndependentSkills 1.2.1-dev 候選包的 PoE1 主圖，從 `unit-v1`（59 節點可實作、2 節點可買）改成全主圖 1,993 個節點都能買的版本：每級 1 點，小點／大點／keystone 各值 1／3／5 份，每份換成固定的 Skyrim 數值，不設上限。對不上 Skyrim 的效果改成小加成，可以拆到 2–3 個數值上；能量護盾、異常、charge、召喚物、藥瓶、投射物與 38 個 keystone 分批做成真機制。

Done when: 每個施工切片都列出要動的檔案（附 path:line）、依賴、可派給哪類線，以及只用可觀察條件寫的 `Done when:`；映射規則、每份數值與 keystone 表都存成資料檔；50 份校準的 L50 驗證結果寫進 design。設計計畫已完成；施工狀態另見下方。

## 文件

<!-- wf-nav -->
- [decisions.md](decisions.md)：全部已定裁示與使用者原話。
- [design.md](design.md)：預算模型、拆分規則、A 類近似、驗證結果。
- [mechanics.md](mechanics.md)：C／B 級機制的裁示、共用系統（ESL、carrier AV、受傷 hook）、暫代規則。
- [keystones.md](keystones.md)：48 個 keystone 的共通裁示、互斥、施工分批與延後案。
- [phases.md](phases.md)：施工分波、依賴圖、切片索引、S15 離線驗證、S16 回家 QA；切片內容在 [phases-core.md](phases-core.md)（S1–S7）與 [phases-mechanics.md](phases-mechanics.md)（S8–S14）。
- [user-words-2026-11-03.md](user-words-2026-11-03.md)：使用者原話一至十。
- 資料檔：[atoms.json](data/atoms.json)（27 種 atom 與每份數值）、[family-rules.json](data/family-rules.json)（49 條拆分規則）、[keystones.json](data/keystones.json)（48 列）、[mechanic-decisions.csv](data/mechanic-decisions.csv)（11 列）、[grade-dist.csv](data/grade-dist.csv)。
- 被取代的舊算法、舊切片與 38 份試算在本計畫的 `archive/`。

## 現行狀態（open）

- 已完成初步抽樣；[20 項候選過目頁](../../../user/2026-11-03-perk-units.md)非完整清單；進階與高級全集調查中，涵蓋 nonwinning、disabled、hidden 與依賴，按 PERK entry 建覆蓋台帳，不設件數上限。新進階／混合數值待使用者確認，高級能力尚未選，均未採用。基本效果是純數值，進階含規則與可量化數值，高級是補能力缺口的純規則；混合效果可拆。既定基礎值不重問。
- [1.2.3 候選報告](../../../../mod-library/plugins/Path-Of-The-Companions-IndependentSkills-1.2.3-dev-2026-11-03/REPORT.md)：第一波 S1–S7（S7 為調查）及 S15 離線完成，含玩家路徑；fresh-parent 119＋5 與 Windows build 124 source 一致，239 檔 MANIFEST 核符，PE 1.2.3.0 通過。mod-library commit `bdaa1a120ef2ab8df2fd46472ec371e090dc6c11`；尚未部署，S16 回家驗收已登記且實機待驗。1.2.1／1.2.2 凍結。
- [1.2.2 候選](../../../../mod-library/plugins/Path-Of-The-Companions-IndependentSkills-1.2.2-dev-2026-11-03/REPORT.md)保留當時的離線證據：S1–S3 整合、S7 調查，S4–S6 與玩家路徑當時尚未完成；S2 暫代速度為 26.4625／47.1625、單點 2.0／0.6，原設計校準 26.2125／48.9125 保留原口徑。
- 第二波 S8–S14 尚未施工；依各機制的規格與新數值裁示繼續，不表示整個計畫完成。
- 等使用者：提供施法速度的參考 mod；延後的 10 個 keystone（9 個自創＋Supreme Ego）之後逐個討論。兩項登記在母 repo `wait-user/later-decisions.md`。
- 施工中還要請使用者定的：能量護盾規格（S9）、藥瓶門檻與冷卻（S13）、新機制 atom 的每份數值。
