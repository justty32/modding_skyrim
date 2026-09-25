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
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/ayop/REPORT.md`、
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/STATE.md:73`／`:79`。
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

## RDO 中文層（抽查對象 2026-09-04 換過版本、2026-09-05 又裁了新版）

離線 topology、文字與 script-binding gates 已過；抽查關係對話／字幕、任務／通知、賄賂金額、
Gelebor／Isran／Valerica 等待／離隊通知，確認無方框、亂碼、空白、未替換 token、截斷、新 crash。
**抽查清單本身沒過期，過期的是抽查對象**，所以改寫而不是刪除：

<!-- wf-nav -->
- **原對象**：`RDO Final Traditional Chinese Dev 2026-08-16`（自製繁中層），範圍見
  [`layer README`](../../mod-library/l10n/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/README.md)。
  **2026-09-04 已停用**——`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:376`
  ＝`-RDO Final Traditional Chinese Dev 2026-08-16`；施工證據 `instance/profiles` commit `e8c3f5c`
  （「old 施工包：RDO 簡中主 esp 層（停舊繁中層）＋NFF 簡中 ESP-ONLY 層」）。
- **現在實際裝的是**：`RDO Final Simplified Chinese 33398 Final`（**簡中**）——
  同檔 `modlist.txt:375`＝`+RDO Final Simplified Chinese 33398 Final`（啟用）。
  同族另有 `:244` `+RDO-Updated-Simplified-Chinese-FULL-Completion-Combined-Dev-2026-09-03`、
  `:245` `+RDO - Update and MCM Simplified Chinese`。
  本體 `plugins.txt:520`＝`*Relationship Dialogue Overhaul.esp`、`:565`＝`*RDO Updated.esp`，皆啟用。
  **所以進遊戲看到的會是簡體字，不是正體**——依「繁簡都可接受」的既定偏好，這不算 FAIL。
- **2026-09-05 使用者裁示：RDO 中文層改採 `62500`**（照常跑中文驗收＋回退 gate）。
  **尚未落地**，且已登記一條風險：`62500` 的 hard requirement `76474`
  （Unofficial Chinese Localisation by Reconquista Studios）是另一套全域中文化基底，
  與現役自製逐 mod 層可能打架，套用前先核對。
  證據：`/home/lorkhan/repo/moddings/skyrim/modpack-design/wf/wait_todo/gameplay-install.md`（「RDO 中文層」節）、
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/rulings/REPORT.md`、
  `/home/lorkhan/repo/moddings/skyrim/agentctl/docs/backlog.md`。
- **結論：這一項先不要進遊戲抽查**——`62500` 換上去之前抽查現役簡中層，換完還得再抽一次。
  等 `62500` 落地後再排。
- **2026-09-25 22:2x 推進**：cx-wu-rdo 正在下載 62500#347829 與 76474#556503（共 38,139,442 bytes）
  並做衝突表，結果（22:31）：兩檔已下載到 `~/skyrim_mods/_dl-2026-09-25/rdo/`、解到 `_staging-2026-09-25/rdo/{62500,76474}/`；record 身分重疊 **6,091 個 FormID、7 個自製層**（RDO Updated 自製層 5,942、ZH Misc Dialogue 89、ImprovedCompanionsBoogaloo 34、Alternate Start 11、Serana Dialogue Edit 11、Rigmor 3、SDA 1），76474 另有 210 個 loose-file 路徑重疊；安裝位置建議與完整表在 `agentctl/handoffs/home-2026-09-25/wu/rdo/REPORT.md`、`conflicts.json.gz`。**裝不裝、放哪層由使用者裁**。

