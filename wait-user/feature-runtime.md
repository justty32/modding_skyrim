# 獨立功能驗收

## MGRR 雙持傷害（2026-10-14）

斯丹達爾護符觸發的 MGRR 動作缺少一般 HitFrame、依賴 Precision，當時攻擊碰撞關閉。使用者要求不依賴 Precision；已在他關閉 Skyrim／MO2 後部署 HitFrame 獨立覆蓋層，10 個攻擊檔補 18 個事件。6 項離線測試、10/10 VFS winner／hash、SKSE 主選單檢查通過，Precision 攻擊碰撞已還原為關閉。**待驗：第三人稱戴回斯丹達爾護符、雙持原武器，左鍵普攻是否讓敵人扣血。** 主選單檢查不代表實際傷害已通過。詳見 [補丁與驗證](../agentctl/handoffs/home-2026-10-14/dagger/README.md)及 [REPORT](../agentctl/handoffs/home-2026-10-14/dagger/REPORT.md)。

## 2026-09-20：PI 啟動崩潰候選層與技能條件 crash 驗證

內容見 [crash-validation.md](feature-runtime/crash-validation.md)。

## 2026-09-24：長毛象 CTD（`SkyrimSE+02B789A`）

內容見 [crash-validation.md](feature-runtime/crash-validation.md)。

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

## DSPort P3 物件邊界（2026-09-14）

內容見 [dsport-p3.md](feature-runtime/dsport-p3.md)。

## DSPort P3 多層 navmesh（2026-09-14）

內容見 [dsport-p3.md](feature-runtime/dsport-p3.md)。

