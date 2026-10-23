# 獨立功能驗收

## 2026-10-18 施工後實機驗收

當天三批施工都只改 profile／mod 目錄，沒有開 MO2 或遊戲（profiles `fa48d3d`），以下只能玩的時候順路看。逐項證據見 [當日現況](../agentctl/handoffs/home-2026-10-18/STATE.md#待使用者實機驗收)。

- **開 MO2 前後**：MO2 開關一輪後實讀 `plugins.txt`，`*` 總數應為 1291；當天停用的 39 支都沒有 `*`（agent 可代做）。
- **讀檔**：舊存檔跳「缺少內容」可直接繼續。
- **Hearthfire 小麥**：自宅田裡看得到、採得到、名稱是「小麥」（看不到就清空那格重種）。
- **戰鬥**：打幾場持盾 NPC不卡永久舉盾、格擋頻率如常；閃避照舊。
- **貼圖**：烏鴉岩 Boethiah 神龕、Castle Volkihar 外塔屋頂不再缺貼圖；Braidwood Inn 隔間門、Dragonsreach 寢室酒櫃不再紫色。
- **擺設**：ULP 各地點擺設回來（看過的格子可能有快取）；Dibella 神殿擺設沒浮空；JK 系列店內地毯位置正常。

有任何一項壞掉，還原檔在 `~/skyrim_mods/_layer-apply/` 下三組 `*-20261018T*`。

## 雙手鋼製太刀 idle 的實際武器辨識（2026-10-17）

使用者描述「鋼鐵武士刀／鋼製大太刀」，名稱不確定。已證實 DaiKatana 姿態格只配攻擊、缺雙手 idle，近似名稱武器另有太刀 keyword 缺漏／Samurai 專屬路由。10-17 載入最新 Save76，當前右手實為鐵製彎刀，不能用此畫面宣稱太刀已重現；本輪未改裝備或配招。下次使用該雙手刀時，確認完整物品名稱或 FormID，再按需要取 OAR `2hm_idle.hkx` 播放來源；若要站姿隨選招，還須另選相容雙手 idle，不能直接把缺檔的攻擊包當成有站姿。見 [調查報告](../agentctl/handoffs/home-2026-10-17/katana/REPORT.md)。

## 2026-09-24：長毛象 CTD（`SkyrimSE+02B789A`）

2026-10-23 重新開啟（原「2026-09-25 結案」是誤判）。內容見 [crash-validation.md](feature-runtime/crash-validation.md)。

## Scene ghost rendered-camera ray

內容見 [scene-ghost.md](feature-runtime/scene-ghost.md)。

## Simonrim Batch 4E

內容見 [simonrim-and-weaponry.md](feature-runtime/simonrim-and-weaponry.md)。

## Simonrim Batch 4A

內容見 [simonrim-and-weaponry.md](feature-runtime/simonrim-and-weaponry.md)。

## Simonrim Batch 4M/P

內容見 [simonrim-and-weaponry.md](feature-runtime/simonrim-and-weaponry.md)。

## Expanded Skyrim Weaponry Batch 3A

內容見 [simonrim-and-weaponry.md](feature-runtime/simonrim-and-weaponry.md)。

## Asset converter 一鍵靜態模型整包（2026-09-10）

內容見 [asset-converter.md](feature-runtime/asset-converter.md)。

## DSPort P3 可見性候選（2026-10-21）

內容見 [dsport-p3.md](feature-runtime/dsport-p3.md)。

## DSPort P3 多層 navmesh（2026-09-14）

內容見 [dsport-p3.md](feature-runtime/dsport-p3.md)。

## 已完成（封存）

### 2026-09-20：PI 啟動崩潰候選層與技能條件 crash 驗證（2026-09-24／2026-10-23 兩段結案）

兩個子項都已不等使用者。

**技能條件 crash（B 型 `SkyrimSE+01D3398`）2026-09-24 結案**：移除三顆 `doom*Perk` 的
`EPModSkillUsage_AdvanceObjectHasKeyword` 條件的補丁已部署正式 `modpack-main`（profiles `3f5c37d`），
**使用者實機格擋確認不再崩潰，第 6 條 PASS**。09:16／09:34 兩次都是格擋時崩潰、並非靜置重現——靜置不算證據。
見 [doomperk 報告](../agentctl/handoffs/done/2026-09/home-2026-09-24/doomperk/REPORT.md)。

**PI 合併層（A 型 PEPE `_tls_end`）2026-10-23 結案**：原文寫「已建立但停用（profiles `0cd417d`），
待使用者決定啟用及冷啟動 A/B」**已過期**。`PayloadInterpreter-Config-Consolidated-Dev-2026-09-20`
早在 2026-09-20 就啟用——`instance/profiles` commit `7dec499`（author／commit date 皆
`2026-09-20 13:57:55 +0800`，訊息「Enable PI consolidated configs after three startup checks」，
diff 正是該行由 `-` 改 `+`），2026-10-23 實讀 `instance/profiles/modpack-main/modlist.txt:119`
＝`+PayloadInterpreter-Config-Consolidated-Dev-2026-09-20`。啟用後約一個月 `_tls_end` 簽章零復發：
10-10 的啟動 crash 調查實讀 skse64.log「155 個 `loaded correctly`，沒有 `disabled`／`fatal error`／
`incompatible`」而明確排除此型（[crash-1 報告](../agentctl/handoffs/done/2026-10/home-2026-10-10/crash-1/REPORT.md)`:16`），
09-28 與 10-09 兩份 crash 報告也都逐一比對後排除。「冷啟動 A/B」因此已無對象。
殘留的只有一條操作習慣（此型 crash 後 skse64.log 會被下次啟動覆蓋，要定案得先 copy 走），
已併進 [長毛象那項](feature-runtime/crash-validation.md)的「下次再崩要做的事」。
原始調查見 [crash2 REPORT](../agentctl/handoffs/done/2026-09/home-2026-09-20/crash2/REPORT.md)
與 [操作步驟](../agentctl/handoffs/done/2026-09/home-2026-09-20/crash2/FIX-AND-AB.md)。

### MGRR 雙持傷害（2026-10-14；2026-10-17 驗收通過）

斯丹達爾護符觸發的 MGRR 動作缺少一般 HitFrame、依賴 Precision，當時攻擊碰撞關閉。使用者要求不依賴 Precision；已部署 HitFrame 獨立覆蓋層，10 個攻擊檔補 18 個事件。6 項離線測試、10/10 VFS winner／hash、SKSE 主選單檢查通過，Precision 攻擊碰撞已還原為關閉。2026-10-17 使用者回覆「那個 OK 了」，確認實際傷害通過；另因不喜歡動作而要求移除，當日已停用本體與補丁並解除專用護符排除。詳見 [補丁與驗證](../agentctl/handoffs/done/2026-10/home-2026-10-14/dagger/README.md)及 [移除報告](../agentctl/handoffs/home-2026-10-17/mgrr/REPORT.md)。

