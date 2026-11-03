# poe-skyrim-mapping：PoE 星盤效果落地 Skyrim（定案設計＋施工計畫）

[plans](../README.md)｜出計畫 2026-11-03｜狀態：**第一波部分施工中**

把 POTC IndependentSkills 1.2.1-dev 候選包的 PoE1 主圖，從 `unit-v1`（59 節點可實作、2 節點可買）改成全主圖 1,993 個節點都能買的版本：每級 1 點，小點／大點／keystone 各值 1／3／5 份，每份換成固定的 Skyrim 數值，不設上限。對不上 Skyrim 的效果改成小加成，可以拆到 2–3 個數值上；能量護盾、異常、charge、召喚物、藥瓶、投射物與 38 個 keystone 分批做成真機制。

Done when: 每個施工切片都列出要動的檔案（附 path:line）、依賴、可派給哪類線，以及只用可觀察條件寫的 `Done when:`；映射規則、每份數值與 keystone 表都存成資料檔；50 份校準的 L50 驗證結果寫進 design。設計計畫已完成；施工狀態另見下方。

## 文件

<!-- wf-nav -->
- [decisions.md](decisions.md)：全部已定裁示與使用者原話。
- [design.md](design.md)：預算模型、拆分規則、A 類近似、驗證結果。
- [mechanics.md](mechanics.md)：C／B 級機制的裁示、共用系統（ESL、carrier AV、受傷 hook）、暫代規則。
- [keystones.md](keystones.md)：48 個 keystone 的共通裁示、互斥、施工分批與延後案。
- [phases.md](phases.md)：施工分波、依賴圖、切片索引、S15 離線驗證、S16 回家 QA；切片內容在 [phases-core.md](phases-core.md)（S1–S7）與 [phases-mechanics.md](phases-mechanics.md)（S8–S14）。
- [user-words-2026-11-03.md](user-words-2026-11-03.md)：使用者原話一至九。
- 資料檔：[atoms.json](data/atoms.json)（27 種 atom 與每份數值）、[family-rules.json](data/family-rules.json)（49 條拆分規則）、[keystones.json](data/keystones.json)（48 列）、[mechanic-decisions.csv](data/mechanic-decisions.csv)（11 列）、[grade-dist.csv](data/grade-dist.csv)。
- 被取代的舊算法、舊切片與 38 份試算在本計畫的 `archive/`。

## 現行狀態（open）

- 新調查：參考已安裝天賦樹，包含未 winning 者；winning 只記為現況欄，評估依賴及玩家／隨從可移植性。基本效果單位是純數值；進階效果單位含規則與可量化數值；高級效果單位是純規則、補能力缺口，混合效果可拆。候選詳見[使用者過目頁](../../../user/2026-11-03-perk-units.md)，尚未選定效果或新數值。
- 新進階單位及混合效果的數值部分，先在 `wf/user/` 候選頁列每份數值、疊加、觸發／冷卻／門檻、例子及來源與提案的區別，待使用者過目確認後才採用。此 gate 不影響既定基礎值、S4–S6，也不擴及所有高級規則；調查不改既定 atoms 或實作。

- 1.2.3 新候選 in-flight：離線續做 S4–S6 並補玩家星盤路徑，尚未部署；1.2.1／1.2.2 凍結。1.2.2 的 runtime 僅處理 Party，無 companion 時 Menu 直接返回，玩家路徑尚未實作。

- 第一波部分施工中：[1.2.2 候選](../../../../mod-library/plugins/Path-Of-The-Companions-IndependentSkills-1.2.2-dev-2026-11-03/REPORT.md)以離線 source 為主、尚未部署；1.2.1 凍結。S1–S3 已整合，fresh-parent 重套後全套離線驗證通過（71＋5 canonical snapshots、MANIFEST 115 檔核符，mod-library commit `42e326d354f96cf5a8d8ae5cb0c77ec6b0c4d668`）；隔離 Windows 真 build 與 PE 1.2.2.0 驗證通過。S7 調查完成；S6 僅定位 Arts／PathsLink 的 actor-context，尚未接線；S4、S5 未完成。carrier 四類 UI disabled 且不寫 AV，SKILL pending。
- S2 keystone 暫代的實作速度結果為 26.4625／47.1625，單點 2.0／0.6；原設計校準 26.2125／48.9125 保留原口徑。暫代的裁量與證據見候選報告及 agentctl 報告。
- 下一步：續做 S4–S6、補玩家 View／Battle 快照、PoE 專用 selector 與 runtime／queue 套用；驗證零 companion 可購點、每級 1 點高水位、reset、存讀及 AV／SKILL／carrier，再完成第一波 S15。玩家不加入 PartyAI，不動原 perk 點。S15 完整後才依 [S16](phases.md#s16-回家-buildqa-登記-wait_user) 登記回家 QA；既有 1.2.1 待驗項保留。
- 等使用者：提供施法速度的參考 mod；延後的 10 個 keystone（9 個自創＋Supreme Ego）之後逐個討論。兩項登記在母 repo `wait-user/later-decisions.md`。
- 施工中還要請使用者定的：能量護盾規格（S9）、藥瓶門檻與冷卻（S13）、新機制 atom 的每份數值。
