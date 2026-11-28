# 獨立功能驗收

## Sofia DLC 對話擴充 1.0（2026-11-07）

Sofia 已新增黎明守衛18句、龍裔8句與原版隨從31句中文評論。這版只有字幕、沒有語音包。帶 Sofia 推進兩個 DLC 主線時，確認中文沒有方框、亂碼或截斷；與 Lydia、Serana、Aela 等原版隨從同行並靠近 Sofia 時，順路確認評論可出現。隨從評論每次條件檢查20%機率、每句只觸發一次，不以短時間沒觸發判失效；部分黎明守衛字幕停留偏久為作者已知現象。確認既有 Sofia／SofiaVigilantAct 對話仍可正常使用。來源與主選單載入證據見 [REPORT](../agentctl/handoffs/home-2026-11-07/nexus-198176/REPORT.md)。

- 代驗 2026-11-28：PASS（1.1 存檔升級部分）——升級前 Save335 與升級後 Save393 讀檔都沒跳缺內容提示，索菲亚在場、16 個選項（含 SofiaVigilantAct 8 條）全中文；DLC 評論與回話沒觸發，無法代驗（見 agentctl/handoffs/home-2026-11-28/rt-proxy/REPORT.md）

## Sofia × VIGILANT 第二～四幕（2026-11-28）

新檔帶 Sofia 走 VIGILANT 主線時順路看：第二幕（墮入）、第三幕（宅邸）、第四幕（冷港）的 Sofia 談論選項會在劇情推進後出現，中文沒有方框／截斷，語音是 Sofia 的嗓音、嘴型有動。重點：第三幕魔神開價後、選擇前可問「被燒死」那句；第四幕見到魔神本尊（深淵）時 Sofia 是否跟得進去；結局句好結局 Karma ≥100 高句、其餘中性句，壞結局低句。45 句玩家選項是 AI 補譯、未人工審，翻得怪記下來。第二、三幕各有一句選項文字相同，兩條線同時進行時會出現兩個同名選項（已知）。來源見 agentctl/handoffs/home-2026-11-28/sofia-install/REPORT.md。

## 雙手鋼製太刀 idle 的實際武器辨識（2026-10-17）

使用者描述「鋼鐵武士刀／鋼製大太刀」，名稱不確定。已證實 DaiKatana 姿態格只配攻擊、缺雙手 idle，近似名稱武器另有太刀 keyword 缺漏／Samurai 專屬路由。10-17 載入最新 Save76，當前右手實為鐵製彎刀，不能用此畫面宣稱太刀已重現；本輪未改裝備或配招。下次使用該雙手刀時，確認完整物品名稱或 FormID，再按需要取 OAR `2hm_idle.hkx` 播放來源；若要站姿隨選招，還須另選相容雙手 idle，不能直接把缺檔的攻擊包當成有站姿。見 調查報告（已刪：`agentctl/handoffs/home-2026-10-17/katana/REPORT.md`）。

agent 2026-11-22 已查：最新存檔 Save342 的背包裡沒有太刀類武器（只有伐木斧、碎岩者、灰燼之王的劍等），沒法從存檔認出是哪一把；下次拿到那把刀時告訴 agent 名稱即可。

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

內容見 [ui-checks.md](feature-runtime/ui-checks.md)。

## VIGILANT 設定載入器 MCM 繁中＋停用 Falmer 重複中文層（2026-11-15）

內容見 [ui-checks.md](feature-runtime/ui-checks.md)。

## Estates of Skyrim 0.1.8→0.1.21 更新後確認（2026-11-15）

內容見 [ui-checks.md](feature-runtime/ui-checks.md)。

## Elden Rim 戰技配到戰灰：附魔台流程實機試（2026-11-21）

你說「之後再試試看」。用戰技卷軸本來就不會跳選單，卷軸只是讓你學會一組附魔；附魔台這一步是從 plugin record 推出來的，還沒實機。玩的時候照這個順序試：

1. 身上帶要配的戰灰（例如「戰灰－力量」「戰灰－秘法」）和一顆**已充能的靈魂石**，先用戰技卷軸。
2. 到附魔台：「物品」選戰灰、「附魔」選剛學會的「戰技－×××」、「靈魂石」選一顆，製作。
3. 把附好魔的戰灰加進偏好，在偏好介面按數字鍵綁 1～8；右手拿武器，實戰按那個數字鍵放戰技。

選了戰灰卻看不到剛學的戰技，就回報一聲，再開調查線查卷軸效果有沒有生效。見[調查報告](../agentctl/handoffs/home-2026-11-21/eldenrim-arts/REPORT.md)。

## 換臉六人實機看臉與身形（2026-11-24）

內容見 [kurone-looks.md](feature-runtime/kurone-looks.md)。

## Aniya 換黑暗與 OK 十個女隨從換 Kurone 臉（2026-11-24）

內容見 [kurone-looks.md](feature-runtime/kurone-looks.md)（後兩節）。

## Kurone Follower Additional Audio 1.4 實機語音驗收（2026-11-25）

內容見 [kurone-audio.md](feature-runtime/kurone-audio.md)。

## 11-26／11-27 OBody 與其他實機驗收

各輪人物的剩餘驗收步驟見 [kurone-looks.md](feature-runtime/kurone-looks.md)；全域重置見 [整包驗收](integrated-runtime.md)。
