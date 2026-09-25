# wench-derivatives — modforge-verdict

← [調查入口](../wench-derivatives.md)

## ModForge meaning & gap（對 idea #22）

### 相對 IW，這批新增的唯一機制：**Deadly Wenches 的 vanilla-LL 注入**
IW finding 已涵蓋 marker-spawn / package / scene / radiant。DW 補上**第二種人口原語**：

| 機制 | IW | DW | #22 用途 |
|------|----|----|----------|
| 室內生活人口 | XMarker + 新 LL + script spawn | — | 酒館裡有人住、幹活 |
| 野外/戰鬥人口 | — | **override vanilla 敵人 LL，additive 注入自家 NPC** | 開拓路上會遇到的敵人/旅人多樣化 |

**ModForge 生成性：** override 一個既有 LeveledNpc 並 additive 加 entry，是 ModForge 已能做的 record 操作（與 worldspace/cell override 同類，見 landed）。**缺的便利層** = 一個 `leveledListInject[]` generator：給「target vanilla LL FormID + 要注入的 NPC/LL + 數量/權重」，自動產出保留原條目的 additive override。這比 IW finding 列的 `spawnPoints[]` generator **更輕、更該先做**——因為它不需要 marker/script，純資料。

> 但對 #22 的「異世界」場景：DW 機制依賴 **vanilla 敵人 LL 存在**。異世界自建 worldspace 沒有 vanilla LL 可寄生 → DW 模式不可直接移植，你得自己定義敵人 LL 並貼到自己的 spawn 點（那其實就退回 IW 的「自家新 LL」路徑）。所以 **DW 的價值是「在 vanilla Skyrim 上鋪人口」的範本，對純異世界 #22 反而是 IW 路徑更適用。**

### Yuriana 對 #22
無新人口機制（90-cell override + radiant 是 IW 內容層的重做）。唯一可借 = **standalone 語音隨從打包範本**（vanilla follower faction + 正確 NPC flags + cloned voice），補足 #22「異世界有名有姓、可同行的住民」這一格——這與 ModForge voice-gen 管線直接銜接，**屬借鏡而非新缺口**。

---

## Verdict

| Mod | 判定 | 理由 |
|-----|------|------|
| **Deadly Wenches** | **可借鏡（中）** | 唯一新機制 = vanilla-LL additive 注入（補 IW 的野外/戰鬥人口維度）；ModForge 已能生 override，缺輕量 `leveledListInject[]` generator。但**對純異世界 #22 用處有限**（無 vanilla LL 可寄生），主要適用「改造 vanilla Skyrim」情境。內容無敘事價值。**需相容**：DW override 91 vanilla 敵人 LL，與任何也改這些 LL 的 mod 衝突；且硬依賴 IW.esp。 |
| **Buxom Wench Yuriana** | **可借鏡（低）/部分可忽略** | 人口機制無新意（IW 內容層平行重做，90-cell override）。可借 = standalone 語音隨從範本（follower faction + Essential+Class+AutoCalc + cloned voice），呼應 ModForge voice-gen 管線。**需相容**：90 vanilla cell override。 |
| **Less Buxom … Overhaul** | **可忽略** | 無 plugin，純美術/動畫替換包。 |

與 Sofia patch 無直接交集。**淨增量結論：** 相對已調查的 IW，這三件套對 #22 只新增「vanilla-LL 注入」一種人口原語（DW），且它在異世界場景不如 IW 的自家-LL 路徑適用；Yuriana 提供的是隨從打包範本而非人口機制。**重點仍回到 IW finding 列的 generator 缺口。**
