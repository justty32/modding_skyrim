# immersive-wenches — modforge-verdict

← [調查入口](../immersive-wenches.md)

## ModForge meaning & gap（對 idea #22）

idea #22「漂泊開拓慢活：異世界裡有人住的酒館/聚落」的人口+生活感，IW 是最貼近的現成藍圖。對照 landed（見 `workflows/feature-dev/landed/`）：

**ModForge 已能直接生成的（占 IW 機制 ~80%）：**
- placements（cell override 放 XMarker / 靜態 ACHR）、NPC build（race/class/voice/outfit/keyword/combatstyle/template/autocalc+class 配對）、packages（sandbox/serve/sleep/patrol）、LeveledNpc、Faction/Relationship、scenes（多 phase Dialog+Package，已 in-game confirmed）、dialogue INFO（含 alias 條件填充）、SM Kill/quest node 觸發（`story-manager-kill-recipe` / `dispatcher-magic-trigger`）、radiant quest stage+objective+GlobalShort gate、MCM（`mcm-helper-registration-recipe`）。
- 異世界場景下**更簡單**：自家 worldspace/cell 不必 override vanilla（IW 一半複雜度來自 91 個 vanilla cell override 與相容性），可直接在新 cell 放 marker + 生怪。

**Gap（IW 有、ModForge 缺便利層的）：**
<!-- wf-nav -->
1. **「生怪點 + LeveledNpc + 控制器」便利層**：IW 的核心是「marker 陣列 ←script→ leveled spawn」。ModForge 能各別生這些 record，但缺一個像 immersive-patrols finding 提的 `patrolGroups[]` 那樣的 **`spawnPoints[]` / `populate[]` generator**（給 cell + marker 數 + LL + 數量 global + 控制器腳本模板，一鍵產出）。這正是 #22 要的「把酒館填滿」原語。**最該補的一格。**
2. **per-location × per-時段 package 套組**：473 個手刻 package 不可規模化；ModForge 若提供「dailySchedule template」（白天 serve / 晚上 socialize / 夜睡 / 早巡）按 location 參數化展開成一組 package + 條件，能一舉省掉 IW 最痛的工作量。
3. **ambient scene 的 condition-filled alias + `MatchingRefInLoadedArea`**：ModForge scene 已能跑，但要確認能生「以 keyword/voicetype 條件 + MatchingRefInLoadedArea 抓現場 NPC」的 alias（IW 整個生活感建立在此），以及把 scene 掛到 **SM Quest node 隨機觸發**（而非單一 trigger）——這是「自然發生」感的關鍵。
4. World-Interaction（`event=ADIA filter=World Interactions\...`）piggyback：給 NPC 一個 keyword 就接上 vanilla 酒館互動——對 vanilla 場景超省力，但異世界無 vanilla WI 可借，需自建一套 WI 風格 quest（屬第 3 點延伸）。

**設計教訓給 #22：** 先做最小垂直切片——1 間異世界酒館 cell + 3 個 spawn marker + 1 個 wench-style LeveledNpc + 一組 daily-schedule package + 1 個 SM 觸發的 serving scene，就能驗證「有人住、會幹活、會互動」的活人口密度，再往聚落擴張。不必一開始就做 IW 的 91-cell 規模或 radiant 任務層。

## Verdict

**可借鏡（高）**——機制範本直接對應 idea #22，且 ~80% 已是 ModForge landed 能力；真正缺的是把零件包成「人口填充 generator」（spawnPoints + dailySchedule + condition-filled ambient scene + SM 觸發）的便利層。內容本身（generic radiant + 成人傾向 ambient）對 #22 無敘事價值，**只借機制、不借內容**。與 Sofia patch 無直接交集（IW 不改 vanilla follower topics，但 override 91 個 vanilla 酒館 cell，與任何也改這些 cell 的 mod 需做相容 patch）。
