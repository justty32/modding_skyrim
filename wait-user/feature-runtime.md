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
另有一個新回報待查：準星指向很遠處再移回來，ghost 會消失且不會恢復（疑為 cell mismatch 清除路徑）。

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

以 Mysticism 2.5.0、Adamant 6.0.4 抽樣 vendor 買書→讀書→施放、代表性天賦、BFCO 輕／重／方向／
sprint attack、長期平衡與存讀檔；證據見
[`Batch 4M/P RESULT`](../agentctl/logs/simonrim-batch4-4mp-2026-08-16/RESULT.md)。

## Expanded Skyrim Weaponry Batch 3A

以真人遊玩或錄影確認鐵製戰戟、鋼製雙刃巨劍的拔收、BFCO 普攻及動作銜接；單張截圖不能替代
時間軸結論。靜態、模型與 runtime distribution 已完成。
