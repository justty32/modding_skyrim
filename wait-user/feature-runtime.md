# 獨立功能驗收

## Scene ghost rendered-camera ray

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
vanilla／AVE loot/vendor 階級比例。靜態與 smoke 不重跑；證據見
[`Batch 4E RESULT`](../agentctl/logs/simonrim-batch4-4e-2026-08-16/RESULT.md)。

## Simonrim Batch 4A

以 Apothecary 1.3.9 等現役組合抽樣跨來源鍊金、戰鬥塗毒、vendor 庫存／價格／early-game 供應、
長 session 平衡與存讀檔。既有 gate 7/7、SPID 19/19 不重跑；證據見
[`Batch 4A RESULT`](../agentctl/logs/simonrim-batch4-4a-2026-08-16/RESULT.md)。

## Simonrim Batch 4M/P

以**現役**的 `Mysticism 2.4.2 Vokriinator Black Pin`（`modlist.txt:27`）與
`Adamant 5.9.2 Vokriinator Black Pin`（`modlist.txt:37`）抽樣：vendor 買書→讀書→施放、
代表性天賦、BFCO 輕／重／方向／sprint attack、長期平衡與存讀檔。

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

以真人遊玩或錄影確認鐵製戰戟、鋼製雙刃巨劍的拔收、BFCO 普攻及動作銜接；單張截圖不能替代
時間軸結論。靜態、模型與 runtime distribution 已完成。

## DSPortP2.esp 實機驗收（sup-dsport）

darksouls-port P2 整合輪離線已完成：`DSPortP2.esp`（457 statics／575 placements／1145 records）與 MO2-ready
`out/DSPortP2/` 730 檔已打包，147 筆擺放物旋轉在 esp record 層全量驗過不符 0。**只剩實機**：清單在該專案
`p2/P2-PLAN.md` 第十節。當時卡在 `desktop.lock`，2026-08-30 查鎖已釋放，等你放行時間即可派線。
