# immersive-citizens-ai-overhaul — ai-mechanism

← [調查入口](../immersive-citizens-ai-overhaul.md)

## 分類

- 類型：**NPC AI / 日程 overhaul（framework 等級）**。改善「standard state」（沒察覺威脅時的日程 / sandbox）與「combat state」（被攻擊時的防禦 / 逃跑），不碰「alert state」。
- Plugin：有，單一大 ESP。
- 敘事價值：**低**（不講故事）；**系統 / pattern 價值：極高**——是整個 mod-survey 裡「如何替成群 NPC 排豐富日程」最完整的真實範本，**直接服務 idea #22**。

## 規模 / 關鍵記錄

主檔 `Immersive Citizens - AI Overhaul.esp`，6.5 MB，**6505 records**，`localized=False`（英文 inline）。
Masters：Skyrim + Update + Dawnguard + HearthFires + Dragonborn + ccBGSSSE001-Fish（**疊在 vanilla 上、非 USSEP**——與 janquadrant 疊 USSEP 不同）。

規模 / 關鍵記錄的逐列資料。

已抽到 [immersive-citizens-ai-overhaul-records.json](immersive-citizens-ai-overhaul-records.json)（10 列）

群組：原表「群組」欄。

數量：原表「數量」欄。

意義：原表「意義」欄。

統計：10 列記錄；3 欄。

## 核心機制 pattern：**alias-package 分派 quest（不碰 NPC 記錄）**

這是與 janquadrant 的**根本差異**，也是本調查最重要的發現：

```
NPCO_AI<地點>NPCs  (Start-Game-Enabled QUST, flags=4096, 無 stage/objective)
  └─ Reference alias[i]  → 指向某 vanilla NPC（Optional + AllowReserved）
       └─ ALPS（alias-override packages）= 該 NPC 的整疊 bespoke 日程包
```

- 一個地點一個 quest。例：Whiterun quest 有 **117 個 alias / 111 個帶 package 疊**；Riverwood 67 alias。整個 mod ~46 個這種 quest 覆蓋全 Skyrim + Solstheim + 各陣營。
- **package 經 alias 的 ALPS 槽下發，NPC 記錄本身不動**——所以才只有 6 筆 NPC override。這正是「override 既有 vanilla NPC 的 package 清單」的**正規、低衝突替代法**（CK 的 "alias package override"）。
- alias 多為**具名 ref**（Alvor / Camilla…），少數是**條件 alias**（`RiverwoodExtraCivilian` conds=10：`HasKeyword` + `GetInFaction` + `GetIsID` 把非具名雜魚也收進來）。

### package 本身：per-NPC × per-地點 × per-時段，全手刻

命名即配方：`NPCOWhiterunBrenuinSleep1x8` = Brenuin 在 Whiterun，凌晨 **1 點睡 8 小時**（`hour=1 durationMin=480`）。`packagediag` 證實：
- `PackageTemplate -> 019717 Sleep`（vanilla 模板）
- `PackageDataLocation`（指一個 NPCO 放置的 location ref）+ `PackageDataTarget`（指特定那張床 ref）+ `Schedule(hour/duration)`。
- 一個 NPC 的 ALPS 疊 = eat / sleep / sit-工作 / travel / 多個時段 sandbox（**具體在前、broad sandbox fallback 在後**，與 ModForge 鐵律一致）。

### 防禦 / 逃跑 / 戰鬥 AI（「combat state」）

不是普通 sandbox，是專門的 **Flee-template package**（`packagediag` 看 data input 名稱很白）：
- `...DefenselessCivilian`：data 有 `"Flee From Target(s) Object List"`、`"Location 1 to Flee"`（`LocationFallback NearEditorLocation` radius 128）、`"Distance to Flee"`、`"Distance to Keep from threat"`——**手無寸鐵者往預放的安全點跑**。
- `...ArmedCivilian Combat`：同樣有逃跑槽 **＋ 自訂 `CombatStyle`**——能打的居民會還手。
- 武裝 / 平民 / hero / mage 各一套，按 NPC 戰力分。逃跑落點靠**預放 ref + 補的 navmesh**（解釋了 3078 REFR / 190 NavMesh）。

### 分區開關 + 全域手感

- `NPCO_AIGlobal<Hold>` GlobalShort（每個 hold / 陣營一顆）= 玩家可關掉某區 AI 的相容開關。
- 8 個 GameSetting override 把 sandbox 睡眠時段、戰鬥失蹤偵測時限、社交觸發距離整體調軟，是「感覺更像人」的隱形底層。
- vendor faction（`ServicesWhiterun*` 帶 `hours=6-17 radius` + `vendorLocation` 攤位 marker）= 商人只在營業時段顧攤——與 janquadrant 的 vendor 手法同源。

