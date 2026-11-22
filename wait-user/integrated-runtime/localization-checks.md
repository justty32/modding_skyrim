## 四個首次生效中文層 → 現在只剩兩個（2026-09-05 核對）

抽查 **Timing is Everything SE 2.2 MCM** 與 **SkyParkour 3.6.2 `Interface/Translations` UI**；
確認無方框、mojibake、截斷、空白。排序稽核：`mod-library/l10n/tools/` 的層優先權稽核。
兩層 2026-09-05 實讀仍啟用：
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:423`＝`+Timing is Everything SE 2.2 - Traditional Chinese`、
同檔 `:640`＝`+SkyParkour 3.6.2 - Traditional Chinese`。

另外兩個抽查對象**已不在載入序，抽查取消**（原文保留在下面，不是刪除，是改寫成現況）：

<!-- wf-nav -->
- ~~**At Your Own Pace 8 ESP 推進選項**~~ —— **AYOP 全套已於 2026-09-05 停用，抽查取消。**
  `lead-ayop` 依使用者當日 14:00「At Your Own Pace 解除安裝」的裁示，把 **10 個 mod／21 支 plugin 停用不刪**，
  缺 master 0，實機讀 Save5 無 CTD、主線 MQ103=100 與四公會正常，不需新周目。
  2026-09-05 實讀證據：`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:630-639`
  十行全為 `-` 前綴（含 `-At Your Own Pace - Traditional Chinese 2026-08-21`）；
  `/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/plugins.txt` 的 AYOP 各行**皆無 `*` 前綴**
  （例：`:571` `At Your Own Pace - Thieves Guild.esp`、`:650` `At Your Own Pace - Main Quest.esp`）。
  施工證據：`instance/profiles` commit `98f7c5e`、agentctl commit `b49aeea`、
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-05/ayop/REPORT.md`、
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-05/STATE.md:73`／`:79`。
  **殘留待辦（不是抽查）**：進遊戲打 `setstage SKI_ConfigManagerInstance 1` 清 5 個 MCM 死選單；
  副作用是 Solstheim 造物主石柱的密拉克控制段會回來。
  **2026-09-25 22:2x 推進**：cx-wu-rt 已在 Save229 上送 `setstage SKI_ConfigManagerInstance 1`
  並另存新槽 `cx-wu-rt-2026-09-25`（原檔未覆蓋）；**使用者載入該槽開 MCM 確認 5 個死選單消失**；
  已知副作用：Solstheim 密拉克控制段回歸。
- ~~**The Choice is Yours 2.7 接受／拒絕對話**~~ —— **繁中層已停用，抽查對象不存在。**
  2026-09-05 實讀：`modlist.txt:624`＝`-The Choice is Yours 2.7 - Traditional Chinese`（停用），
  `:625`＝`+The Choice is Yours 2.7`（本體仍啟用，即介面是英文）。
  **待確認**：我查了 modlist／plugins／loadorder 三個檔與 09-04／09-05 的 REPORT，
  **找不到明確寫「停用 TCIY 繁中層」的裁示或施工紀錄**，最接近的是 09-04 那輪 zhmake redeploy
  （`instance/profiles` `4389eb3`「5 個空殼層 delist」）。若這是誤停，請說一聲，重新啟用即可恢復抽查。
