# DSPort 肉眼測試清單（2026-10-03）

完整報告在 `agentctl/handoffs/home-2026-10-03/dsp/REPORT.md`。

## 0. 切到 dsport-dev，然後啟動
**不要從 Steam 啟動**，也不要按 Play 或 Verify。
1. 從開始選單開 MO2，或執行 `instance/tools/launch-mo2.sh`，不要加 `--skse`。
2. 左上角的 Profile 切成 `dsport-dev`。
3. 確認勾選狀態：`DSPort P3 Dev 2026-10-03` 要勾；navAuthored 和 2026-09-05 都不要勾。
4. 右上角執行選單選 SKSE，按 Run。
5. 到主選單後不要讀檔，開 console 輸入 `coc DSPortWorld_Cell_0_0`，再輸入 `tgm`。如果跳出「Done Writing」，按 OK 就好。

## 1. 進場
- 預期：看到北方不死院的石牆。
- 異常：閃退，或一直往虛空掉下去。

## 2. A16 光柱（牢房）
依序輸入：
```
player.setpos x 2048
player.setpos y 2048
player.setpos z 19940
getpos x
getpos y
player.setangle z 0
```
`getpos` 應該回傳約 2048 / 2048。滑鼠稍微往上抬。
- 預期：正前方有一道半透明、偏亮的光柱。
- 異常：黑色或不透明的片狀、粉紫色、完全看不到、一靠近就崩。
- 片狀邊界是已知問題，看看能不能接受。

## 3. A19 光柱（上層走廊）
依序輸入：
```
player.setpos x 2160
player.setpos y -2437
player.setpos z 21120
getpos x
getpos y
player.setangle z 90
```
光柱在東邊 300–600 單位外、頭頂前方。判斷標準跟第 2 項一樣。

## 4. 地板與天空
在上面兩個位置和中庭慢慢轉一圈 360°，也要上下看。
- 地板：任何角度都應該有貼圖。如果會隨視角消失，記下 `getpos` 的座標和面朝方向。
- 天空：在某些角度消失或發白是已知問題，這版沒修，記下來就好。

## 5. 屍鬼會不會跨格追擊
依序輸入：
```
player.setpos x 2020
player.setpos y -500
player.setpos z 20000
player.placeatme 0005593C
```
往北（+Y）走到 y 大約 +700。
- 正式包：屍鬼走到 y≈0 會被彈回去卡住。這是已知限制，不算壞。
- 想看 authored 版：先 `qqq` 退出，在 MO2 改勾 navAuthored、取消勾正式包（兩個只能勾一個），從第 0 步重來。預期屍鬼會追過來。看完記得勾回正式包。

## 6. 測完切回 modpack-main
1. `qqq` 退出遊戲。
2. Profile 切回 `modpack-main`，關掉 MO2。
3. 如果有崩潰，crash log 在 `.../My Games/Skyrim Special Edition/SKSE/crash-*.log`。

## 回報格式
- 光柱 A16、A19：OK／片狀難看／看不到
- 地板：穩定／會消失（附位置）
- 屍鬼 flat、authored：有跟／沒跟／崩
