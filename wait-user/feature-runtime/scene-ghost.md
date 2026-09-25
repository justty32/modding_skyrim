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
[`instance/README.md`](../../instance/README.md)。使用者以物品 ghost 在第一人稱、vanilla 第三人稱、
SmoothCam 各靜置確認**不再轉、不再靠近**。

**這只是症狀確認，不等於那 15 條通過**——15 條驗的是 rendered-camera ray 的落點精度，還沒跑。

「準星指向很遠處再移回來，ghost 會消失且不會恢復」這個新回報已於 2026-08-26 離線修好，
但**尚未部署、尚未實機驗收**：修正 `21867c1`（分支 `fix/ghost-cell-clear-2026-08-26`，已推 origin），
DLL SHA-256 `b302857681988f4930f666d41aef13c8ab9ef94486d8e746b81f1832c4a965e3`（1906688 bytes）。
成因與修法見 [`調查記錄`](../../projects/scene-capture-bridge/GHOST_CELL_CLEAR_INVESTIGATION_2026-08-26.md)
與 [`收線記錄`](../../agentctl/handoffs/done/README.md)。**要跑 15 條之前先部署這顆 DLL**，
否則驗的還是舊行為。

原始 FAIL 記錄： 使用者以部署中的 DLL
（SHA-256 `dccc10e0…3fd67`，與文件記錄的 `a17e460` build 相同）實測：ghost 會持續自轉並持續往玩家
靠近；手完全不動仍繼續，第一人稱／vanilla 第三人稱／SmoothCam 三者皆然；按 F11 放下的真實 ref
不受影響。症狀與輸入無關，指向每幀重新定位 ghost 的迴圈。診斷線 `ghost-spin` 進行中。
**修好之前跑 15 條只會全組 FAIL，是浪費實機時間。**

修好後再重跑固定 15 條，涵蓋第一人稱、vanilla 第三人稱、SmoothCam；2026-08-22 的證據只支持 2 條，
不能當作 13/15 通過。清單見
[`固定 15 條`](../../agentctl/logs/scene-ghost-camera-ray-2026-08-22.md#runtime-驗收清單固定-15-條)。

