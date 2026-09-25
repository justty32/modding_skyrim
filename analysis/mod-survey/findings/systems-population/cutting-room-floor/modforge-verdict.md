# cutting-room-floor — modforge-verdict

← [調查入口](../cutting-room-floor.md)

## ModForge meaning & gap（對 idea #22）

#22「異世界裡有人住的聚落」要的「固定住民 + 在地生活 + 一點在地任務/對白」，CRF 是比 IW 更貼切的藍圖——因為 #22 多半是**手擺固定居民**（村莊／據點），不是動態生匿名人群。對照 landed（`workflows/feature-dev/landed/`）：

**ModForge 已能直接生成（占 CRF 機制 ~85%）：**
- placements（interior 內裝 + 往 cell additive 加 REFR/ACHR）、NPC build（race/class/voice/outfit/faction/crimefaction/**autocalc+class 配對**/Unique）、per-NPC packages（eat/work/sandbox/sleep，含 template 繼承 + work-marker LocationTarget）、vendor faction（sellBuyList/merchantContainer/vendorLocation/營業時段）、Relationship、新 interior cell + Location、radiant quest（stage/objective/branch dialogue）、SM 節點 additive 掛根、GlobalShort gate。
- **異世界更省事**：自家 worldspace 不必 override vanilla 外景 cell（CRF 一半複雜度來自此 + USSEP 相容），直接在新 cell 擺 ACHR + 內裝。

**Gap（CRF 有、ModForge 缺便利層的）：**
<!-- wf-nav -->
1. **「聚落 generator」**：CRF 每個聚落 = {幾個 cell + N 個具名居民 + 每人三件套 package + 三件套 faction（town/services/house）+ 內裝 placements}。ModForge 能逐件生，但缺一個 `settlement[]` / `village[]` 高階原語：給 cell + 居民清單（名字/角色/vendor?）→ 自動展開出 faction 三件套、vendor 設定、daily-schedule package、把居民 ACHR 擺進 cell。**最該補的一格**（與 IW finding 的 `populate[]` 同源，但 CRF 版偏「固定具名住民」而非「LL spawn」）。
2. **per-NPC dailySchedule template**：72 個手刻 package 不可規模化。一個「eat→work(綁 workmarker)→sandbox→sleep」參數化模板（給 hour/duration/location）能一鍵展開，省掉 CRF/IW 共同最痛點。
3. **非破壞 toggle 慣用法**：`CRFChangeLocation` 的「StartGameEnabled 無文字 quest + 條件填 reference alias + AllowDisabled flag enable/disable ref」是疊加式整合的標準手法。ModForge 已有 quest/alias/fragment 零件（`radiant-alias-package-byte-truths`、`dispatcher-magic-trigger`），但值得封一個 `enableState[]` / `worldEdit[]` 便利層（「依條件啟用/停用某 ref」）——#22 若要在世界推進中讓聚落「長出來/變化」會直接用到。

**設計教訓給 #22：** 先做 Frost River 的最小垂直切片——1 個聚落 cell（自家 worldspace，免 override）+ 3 個具名居民（vendor 1 + 一般 2，各帶 eat/work/sandbox/sleep）+ town/services faction + 1 個 `Supply Line` 式在地 repeatable 任務 + 招募/閒聊分支對白。這就驗證了「有名字、會幹活、會交易、有事可做」的固定住民密度，再往多聚落擴張。**CRF 給的是「固定住民聚落」的骨架，IW 給的是「動態人群」的填充——#22 兩者都要，但先抄 CRF 的固定骨架更穩。**

## Verdict

**可借鏡（高）**——官方風的「在世界裡長出有人住的小聚落」最乾淨範本，~85% 已是 ModForge landed 能力；真正缺的是把零件包成「settlement generator（居民 + faction 三件套 + dailySchedule package + vendor）」與「非破壞 enableState toggle」兩個便利層。內容本身（復原 vanilla cut content）對 #22 無直接敘事價值，**只借機制、不借內容**。與 Sofia patch 無交集（CRF 不改 vanilla follower topics），但它 **override 109 個 vanilla cell + 46 個 vanilla NPC**：任何也碰這些聚落/NPC 的 mod（含 #22 若放在 vanilla 場景）都需與 CRF 做相容 patch（如本機已有的 `AI Overhaul - CRF Patch`）。
