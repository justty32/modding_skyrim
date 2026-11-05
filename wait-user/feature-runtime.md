# 獨立功能驗收

## 2026-10-18 施工後實機驗收

當天三批施工都只改 profile／mod 目錄，沒有開 MO2 或遊戲（profiles `fa48d3d`），以下只能玩的時候順路看。逐項證據見 當日現況（已刪：`agentctl/handoffs/home-2026-10-18/STATE.md`）。

- **開 MO2 前後**：MO2 開關一輪後實讀 `plugins.txt`，`*` 總數應為 1291；當天停用的 39 支都沒有 `*`（agent 可代做）。
- **讀檔**：舊存檔跳「缺少內容」可直接繼續。
- **Hearthfire 小麥**：自宅田裡看得到、採得到、名稱是「小麥」（看不到就清空那格重種）。
- **戰鬥**：打幾場持盾 NPC不卡永久舉盾、格擋頻率如常；閃避照舊。
- **貼圖**：烏鴉岩 Boethiah 神龕、Castle Volkihar 外塔屋頂不再缺貼圖；Braidwood Inn 隔間門、Dragonsreach 寢室酒櫃不再紫色。
- **擺設**：ULP 各地點擺設回來（看過的格子可能有快取）；Dibella 神殿擺設沒浮空；JK 系列店內地毯位置正常。

有任何一項壞掉，還原檔在 `~/skyrim_mods/_layer-apply/` 下三組 `*-20261018T*`。

## 雙手鋼製太刀 idle 的實際武器辨識（2026-10-17）

使用者描述「鋼鐵武士刀／鋼製大太刀」，名稱不確定。已證實 DaiKatana 姿態格只配攻擊、缺雙手 idle，近似名稱武器另有太刀 keyword 缺漏／Samurai 專屬路由。10-17 載入最新 Save76，當前右手實為鐵製彎刀，不能用此畫面宣稱太刀已重現；本輪未改裝備或配招。下次使用該雙手刀時，確認完整物品名稱或 FormID，再按需要取 OAR `2hm_idle.hkx` 播放來源；若要站姿隨選招，還須另選相容雙手 idle，不能直接把缺檔的攻擊包當成有站姿。見 調查報告（已刪：`agentctl/handoffs/home-2026-10-17/katana/REPORT.md`）。

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

## Astrid（換 Bell 的臉）五官確認（2026-10-26，BLOCKED）

face3 實機拍到 Astrid 真身 `BD54B31B`（金髮、眼罩、造型臉，不是素頭大媽臉），但叫出 Bell 本尊複本後相機兩次跑進牆裡，拍不到同框。靜態檢查全過（tpfix `PASS 7/7`、贏家是換臉層、Bell 已藏）。這是測不出來，不是測出壞的，現狀不動。請使用者看一眼 Astrid 的五官是不是 Bell；截圖在 `~/skyrim_mods/_staging-2026-10-26/face3/shots/astrid-face.png`（不進 git）。證據見 face3 REPORT（已刪：`agentctl/handoffs/home-2026-10-26/face3/REPORT.md`）。

## ESL 旗標 6 支的 UI 功能順路確認（2026-10-26）

`ESLify-Overlay` r2 已正式套用（profiles `5a3d6af`）：RaceMenuPlugin、BetterContainerControls、NSV Spell Copies、WindhelmSegregation、DudestiaOutfitChanger、CompanionsTweaks 改成 light，FormID 不變。agent 已實測「light 狀態存檔→重開遊戲→讀回」背包／裝備／任務／Papyrus 讀檔段都一致，co-save 也接得上。沒測到的只有要真的點 UI 的部分，玩的時候順路看：

- **RaceMenu**：開得起來、滑桿能動（`showracemenu` 或鏡子）。
- **Better Container Controls**：開容器，全取／分類快捷鍵照舊。
- **換裝戒指（Dudestia Outfit Changer）**：對隨從用一次，換得上去。

還原：持 game.lock、MO2 關著，先取回 revert 檔 `git -C agentctl show 3db1b772:handoffs/home-2026-10-26/eslapply/data/layer-revert.json > /tmp/eslapply-layer-revert.json`，再跑 `python3 instance/tools/layer_apply.py --revert /tmp/eslapply-layer-revert.json`。它把 modlist 蓋回套用前、把舊 ESLify-Overlay 從 `~/skyrim_mods/_layer-apply/eslapply-r1-20261026T110518/mods/` 搬回、ESLify-Overlay-NSV 搬進備份（不刪），再 profiles `record --kind fix`。revert 沒有 dry-run；三檔被別線改過會拒絕，屆時手動刪 `+ESLify-Overlay-NSV` 那行、把 ESLify-Overlay 目錄換回備份。已用新 light 存檔再撤旗標的反向路徑沒測過，先拿存檔複本試；revert json 內若寫死來源路徑，執行前先確認（原 REPORT `agentctl/handoffs/home-2026-10-26/eslapply/REPORT.md` 已刪，可由同一 commit 取回）。
