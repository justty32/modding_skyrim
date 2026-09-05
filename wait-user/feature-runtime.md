# 獨立功能驗收

> **2026-09-05 核對結論（todo-23）**：Simonrim 時代的 Batch 4E／4A／4M/P 三節，
> **抽樣對象逐個實讀後全部仍在啟用清單裡，三節都不作廢**——過期的是行號與框架名（BFCO→MCO），不是清單。
> 只有 4E 的「AVE loot/vendor 階級比例」與 4M/P 的「BFCO 攻擊」兩個子條件因對象停用而作廢，已就地標註。
> 判準：`modlist.txt` 以 `+` 開頭＝啟用、`plugins.txt` 以 `*` 開頭＝啟用（檔案是 CRLF，比對前 `tr -d '\r'`）。
> 核對來源：`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/{modlist.txt,plugins.txt}`
> （`instance/profiles` main `5f47044`）。

## Scene ghost rendered-camera ray

> **狀態（2026-09-05 16:10 更新）**：15 條仍未跑，本項仍 open。
> 同日 `lead-scb` 線已完成 `scene-capture-bridge` 體檢並交付 REPORT，但沒有執行這裡的 15 條 runtime 驗收。
> 排這 15 條之前先看它的交付：
> `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/scb/`
> （證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/scb/REPORT.md`、
> `/home/lorkhan/repo/moddings/skyrim/agentctl/inbox/done/2026-09-05/originals/20260905T1610-cx-scb-a-DONE.md`）。
> 本檔未改這節的技術內容——`projects/scene-capture-bridge` 是別線的領地。

**2026-08-25 已修並經實機確認症狀消失；15 條仍未跑。**
成因有兩個、互相餵養：`Physics::FreezeDeferred()` 把 `Get3D()!=nullptr` 當成凍結成功、忽略
`SetMotionType` 回傳值，一次失敗就永久保持 dynamic（既有缺陷，來自初始匯入 `2cc87c5`，**不是**
`75308c9`）；`a17e460` 的新 A8 collector 只拒絕 `IsPlayerRef()`、沒拒絕 ghost 自己，於是每幀 ray
打到那個未凍結的 ghost 並把它移到新 hit point，逐幀往玩家靠近。修正 `5273576`
（分支 `fix/ghost-ray-self-hit-2026-08-25`，已推 origin），已部署，SHA 見
[`instance/README.md`](../instance/README.md)。使用者以物品 ghost 在第一人稱、vanilla 第三人稱、
SmoothCam 各靜置確認**不再轉、不再靠近**。

**這只是症狀確認，不等於那 15 條通過**——15 條驗的是 rendered-camera ray 的落點精度，還沒跑。

「準星指向很遠處再移回來，ghost 會消失且不會恢復」這個新回報已於 2026-08-26 離線修好，
但**尚未部署、尚未實機驗收**：修正 `21867c1`（分支 `fix/ghost-cell-clear-2026-08-26`，已推 origin），
DLL SHA-256 `b302857681988f4930f666d41aef13c8ab9ef94486d8e746b81f1832c4a965e3`（1906688 bytes）。
成因與修法見 [`調查記錄`](../projects/scene-capture-bridge/GHOST_CELL_CLEAR_INVESTIGATION_2026-08-26.md)
與 [`收線記錄`](../agentctl/handoffs/done/README.md)。**要跑 15 條之前先部署這顆 DLL**，
否則驗的還是舊行為。

原始 FAIL 記錄： 使用者以部署中的 DLL
（SHA-256 `dccc10e0…3fd67`，與文件記錄的 `a17e460` build 相同）實測：ghost 會持續自轉並持續往玩家
靠近；手完全不動仍繼續，第一人稱／vanilla 第三人稱／SmoothCam 三者皆然；按 F11 放下的真實 ref
不受影響。症狀與輸入無關，指向每幀重新定位 ghost 的迴圈。診斷線 `ghost-spin` 進行中。
**修好之前跑 15 條只會全組 FAIL，是浪費實機時間。**

修好後再重跑固定 15 條，涵蓋第一人稱、vanilla 第三人稱、SmoothCam；2026-08-22 的證據只支持 2 條，
不能當作 13/15 通過。清單見
[`固定 15 條`](../agentctl/logs/scene-ghost-camera-ray-2026-08-22.md#runtime-驗收清單固定-15-條)。

## Simonrim Batch 4E

抽樣附魔分解→學習→製作→裝備／重載／充能、Empowered Strike power-attack proc、slot restriction、
vanilla ~~／AVE~~ loot/vendor 階級比例。靜態與 smoke 不重跑；證據見
[`Batch 4E RESULT`](../agentctl/logs/simonrim-batch4-4e-2026-08-16/RESULT.md)。

**2026-09-05 核對：對象仍在，本節有效。**
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:458`＝`+Thaumaturgy 1.5 Dev 2026-08-16`（啟用）、
`:453`＝`+Thaumaturgy Execute XP VMAD Fix 1.5 Dev 2026-08-16`（啟用）、
`:455`／`:456` 兩個繁中層皆 `+`；
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/plugins.txt:567`＝`*Thaumaturgy.esp`、
`:639`＝`*ModpackKR_Thaumaturgy_ExecuteXP_VMADFixDev.esp`。
**只有 AVE 那半作廢**：`modlist.txt:457`＝`-Thaumaturgy AVE Patch 1.1 Reference Dev 2026-08-16`（**已停用**）、
`:620`＝`-Simonrim AVE Constellations Merge 1.5 Dev 2026-08-16`（**已停用**），
所以 loot/vendor 階級比例只抽 vanilla 這一邊。

## Simonrim Batch 4A

以 Apothecary 1.3.9 等現役組合抽樣跨來源鍊金、戰鬥塗毒、vendor 庫存／價格／early-game 供應、
長 session 平衡與存讀檔。既有 gate 7/7、SPID 19/19 不重跑；證據見
[`Batch 4A RESULT`](../agentctl/logs/simonrim-batch4-4a-2026-08-16/RESULT.md)。

**2026-09-05 核對：對象仍在且仍是 1.3.9，本節完全有效、無需改動。**
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:439`＝`+Apothecary 1.3.9 Dev 2026-08-16`（啟用），
三個 patch `:441` Fishing 1.4.1／`:443` Saints and Seducers 1.4.0／`:445` Rare Curios 1.4.0 與各自繁中層皆 `+`，
`:436`＝`+Apothecary Ethereal VMAD Fix 1.3.9 Dev 2026-08-16`、
`:437`＝`+Apothecary-Traditional-Chinese-Completion-OBJTEXT-Completion-Dev-2026-09-03`；
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/plugins.txt:606`＝`*Apothecary.esp`、
`:635`／`:636`／`:637` 三個 patch esp、`:638`＝`*ApothecaryEtherealVMADFix.esp` 全部啟用。

## Simonrim Batch 4M/P

以**現役**的 `Mysticism 2.4.2 Vokriinator Black Pin`（`modlist.txt:277`）與
`Adamant 5.9.2 Vokriinator Black Pin`（`modlist.txt:290`）抽樣：vendor 買書→讀書→施放、
代表性天賦、~~BFCO~~ **MCO** 輕／重／方向／sprint attack、長期平衡與存讀檔。

**2026-09-05 核對：兩個抽樣對象都仍在啟用清單，本節不作廢，只改行號與框架名。**
- 行號從 `:27`／`:37` 更正為 **`:277`／`:290`**（modlist 從 08-26 的數百行長到 1379 行，舊行號早就失真；
  行號會再變，比對請用 mod 名不要用行號）。實讀：
  `/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:277`＝`+Mysticism 2.4.2 Vokriinator Black Pin 2026-08-21`、
  同檔 `:290`＝`+Adamant 5.9.2 Vokriinator Black Pin 2026-08-21`；
  `/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/plugins.txt:569`＝`*MysticismMagic.esp`、
  `:607`＝`*Adamant.esp`。原文說的 2.5.0／6.0.4 舊版仍是停用狀態（`modlist.txt:461`／`:462`、`:459`／`:451`／`:452` 皆 `-`），
  與 08-26 的判斷一致。
- **BFCO → MCO**：2026-09-02 使用者裁示戰鬥框架移回 MCO 並已施工。
  `modlist.txt:407`＝`-BFCO - Attack Behavior Framework 3.100.5`（**停用**）、`:403` 繁中層亦 `-`；
  現役是 `plugins.txt:864`＝`*Attack_MCO.esp`、`:865`＝`*scar-adxp-patch.esp`、`modlist.txt:404`＝`+SCAR 2.01`。
  所以這一條抽的是 **MCO 的輕／重／方向／sprint attack**。
  遷移證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-02/mco2/REPORT.md`、
  `instance/profiles` main `9e188e2`。

> **驗收對象已於 2026-08-26 改寫。** 原文寫的是 `Mysticism 2.5.0`／`Adamant 6.0.4`，
> 那兩個版本已在 2026-08-21 的 Simonrim→EnaiRim 遷移（Vokriinator Black 路線）中停用
> （`modlist.txt:175`、`:178` 現在是 `-`）；
> [`batches.md`](../agentctl/logs/simonrim-to-enairim-final-selection-2026-08-24/batches.md) 第 9 行
> 明訂保留 Mysticism 2.4.2 作唯一 base，是既定方向。**抽樣清單本身沒有過期，只有版本號過期**，
> 所以改寫而不是刪除。

舊版本的證據見
[`Batch 4M/P RESULT`](../agentctl/logs/simonrim-batch4-4mp-2026-08-16/RESULT.md)——那是 2.5.0／6.0.4
的結果，**不能直接沿用**到現役組合。EnaiRim Batch 1 終態 gate 也會驗 Mysticism 2.4.2 base；
兩者若排在同一個驗收窗口，這份清單可以併進去一起跑，但不要因此把它從本檔移除。

## Expanded Skyrim Weaponry Batch 3A

以真人遊玩或錄影確認鐵製戰戟、鋼製雙刃巨劍的拔收、~~BFCO~~ **MCO** 普攻及動作銜接；單張截圖不能替代
時間軸結論。靜態、模型與 runtime distribution 已完成。

**2026-09-05 核對：對象仍在，本節有效（同樣把 BFCO 改成 MCO）。**
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:598`＝`+Expanded Skyrim Weaponry 1.01 CHT`（啟用）、
`:600`＝`+Expanded Skyrim Weaponry 1.01 NPC`（啟用）；同族簡中層 `:599` 為 `-`（停用，正常，與 CHT 二選一）。
另註：2026-09-05 使用者已親眼驗過「六把武器名中文」PASS（
`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/win/data/ingame-checks.csv` 第 ⑦ 項），
但**那只驗名稱文字，沒驗拔收與動作銜接**，本節的動作驗收仍未做。
