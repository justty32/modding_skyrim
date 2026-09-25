# immersive-citizens-ai-overhaul — comparison-modforge

← [調查入口](../immersive-citizens-ai-overhaul.md)

## 與 janquadrant AI Overhaul 的對比

| 面向 | **ICAIO（本檔）** | **AI Overhaul（janquadrant）** |
|------|------|------|
| package 下發 | **alias ALPS 分派 quest**（NPC 記錄不動，6 筆）| **直接 override NPC 記錄的 Packages 清單**（424 筆）|
| package 來源 | **1400+ bespoke**（per-NPC×地點×時段手刻）| **~10 個 vanilla 模板規模化套用** |
| 世界編輯 | 重（3078 REFR + 190 NavMesh + 263 Cell + 家具/idle 標記）| 輕（少量 cell/worldspace 放標記）|
| 防禦/逃跑 | **有，專門 Flee-package + CombatStyle 分級** | 無此重點 |
| 衝突面 | **低**（不爭 NPC 記錄；爭的是 Cell/NavMesh + vanilla Scene override）| **高**（每個被它改的 NPC 都和別的 NPC-mod 互踩）|
| 疊在 | vanilla（非 USSEP）| USSEP 之上 |

**結論差異**：janquadrant 是「換掉 NPC 的包清單」；ICAIO 是「**不碰 NPC，用一個 quest 從旁把整疊包掛上去**」。後者技術上更乾淨、衝突更低，是替**既有**世界打日程 patch 的更佳範式。

## 對 ModForge 的意義 & gap（聚焦 idea #22：替我們自己的新 NPC 排日程）

idea #22 是**新拓荒聚落的新 NPC**——我們**不需要**「override vanilla NPC」那條難路；我們從零建 NPC，可以直接把日程寫進 NPC 記錄。這讓 ICAIO 的精華對我們**幾乎全可借鏡、且更省事**。

對 ModForge 的意義 & gap（聚焦 idea #22：替我們自己的新 NPC 排日程）的逐列資料。

已抽到 [immersive-citizens-ai-overhaul-modforge-mapping.json](immersive-citizens-ai-overhaul-modforge-mapping.json)（8 列）

ICAIO 用到的能力：原表「ICAIO 用到的能力」欄。

ModForge 現況（見 [landed/npcs.md](../../../../../projects/ModForge/workflows/feature-dev/landed/npcs.md)）：原表「ModForge 現況（見 [landed/npcs.md](../../../../../projects/ModForge/workflows/feature-dev/landed/npcs.md)）」欄。

統計：8 列記錄；2 欄。

### #22 最重要的 takeaway

我們的新聚落 NPC **走「NPC 記錄直接帶 package 疊」這條（janquadrant 式，但對象是新 NPC）最省**，不必學 ICAIO 的 alias-quest 繞道——那繞道只是為了不動 vanilla 記錄。ICAIO 真正值得抄進 ModForge 的是兩個**內容配方**：①「per-NPC × 時段 × location-ref 的日程疊」要綁到**實際放置的床/攤位/工作家具 ref**（不能只有抽象 sandbox，否則 NPC 站著發呆）；② **新增一個 `flee` PACK 模板**（Flee-template + 預放安全點 location + 可選 CombatStyle），讓聚落在受襲時有「平民逃、守衛戰」的生命感——這是把「慢活聚落」從靜態佈景變成會反應的活聚落的關鍵一步。

## Verdict：**可借鏡（內容配方）＋ 需補一個 `flee` PACK 模板**

- **可借鏡**：日程疊配方、綁實體家具 ref、vendor 營業時段、分區開關——ModForge 已有對應能力，照 ICAIO 的密度去「填內容」即可生出活聚落。
- **需補（建議 roadmap）**：`flee` PACK 模板（防禦/逃跑 AI），這是 #22 受襲反應的硬缺口。
- **可忽略**：alias-package 分派 quest 與整片 vanilla Scene/Cell/NavMesh override——那是「patch 既有 Skyrim」才需要，#22 建新世界用不到（若日後做 vanilla-NPC patch，再回頭參考此 alias-ALPS 範式，它比 janquadrant 的 NPC-override 更乾淨）。

## 其他變體（一行帶過）

- `Immersive Citizens - AI Overhaul - chinese`（.rar，1.2 MB）：中文在地化版。
- `Immersive Citizens Patch ESL`（hdd，20 KB）：把主檔 flag 成 ESL 的第三方 patch。
- 解出的 FOMOD 內另含 ELE / ELFX / Open Cities 相容 patch（純燈光/城市相容，無敘事價值）。

## 解碼方法備忘（記憶體安全）

主檔 6.5 MB，`dump` / `questdiag` / `packagediag` 全走 ModForge CLI lazy overlay，**未整載 Skyrim.esm**。
- record 普查：`dump | grep -oP '\] \K[A-Za-z]+' | sort | uniq -c`。
- 機制定位：`questdiag <AI quest>` 看 alias 的 **ALPS** 行 → 證實 package 經 alias 下發；`packagediag <pkg>` 看 `PackageDataLocation/Target` + `Schedule` + Flee data-input 名稱。
- vanilla package template editorId（如 Sleep 0x019717）只標已知值，未為解 editorId 去載 master。
