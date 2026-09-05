# 整包 UI／中文／任務驗收

## GO19 新內容要不要改用新周目正式驗收

ECSS 作者要求全新存檔，Gray Cowl 周年版是大改替換件，Faehaven 也建議新存檔；2026-09-03 用 Dev0A 舊存檔時第一局
79 秒後 crash，第二局正常，且今天新增的 11 個 plugin 沒出現在 crash 現場。A＝現在開新周目，把這三件正式驗收；
B＝繼續舊周目，但接受之後的 crash／任務狀態不能歸咎於部署。證據：`agentctl/handoffs/home-2026-09-03/inst2/REPORT.md`。

## Auri＋現役 VIGILANT 有限解凍整合

**裁示：B —— follower 只有限解凍 Auri＋現役 VIGILANT，並採 Sofia 選配 preflight／No Bump。**
（2026-09-01，使用者當場口頭裁示；見[裁示簡報](decision-briefs-2026-09-01.md)第 2 條。）回家以 Auri
2.2 本體、exact 2.2 中文、VIGILANT commentary 0.2／tweaks 做 winner preflight 與部署；Auri 不匯入
NFF，Sofia 的 RDO／AI Overhaul／No Bump 選配須重新核對現役 clothing binding fix winner。
**通過**＝離線 winner／版本／中文層無回滾，再實機驗 Auri 招募與跟隨、VIGILANT commentary 條件／
字幕、Sofia 選配及既有 VIGILANT／Sofia 行為都無新衝突；不得藉此加入第二名新 follower。

**狀態（2026-09-05 實讀，本項仍 open 但只剩實機那半）**：檔案層都已到位——
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:735`＝`+Song Of The Green (Auri Follower) 2.2`（啟用），
中文層 `:732`／`:733`／`:734` 三行皆 `+`；`plugins.txt:734`＝`*018Auri.esp`（啟用）。
VIGILANT 1.8.2 四層仍啟用（`modlist.txt:357`／`:358`／`:360`／`:421`）；
Sofia 的 clothing binding fix winner 仍在（`modlist.txt:417`／`:418`、`plugins.txt:599`＝`*SofiaClothingBindingFixDev.esp`）。
**還沒做的是實機那一段**（Auri 招募／跟隨、VIGILANT commentary 條件與字幕、Sofia 選配無新衝突）。
另註：`/home/lorkhan/repo/moddings/skyrim/agentctl/status/todo/20-Auri到底還做不做.md` 有一份平行筆記，兩處講同一件事。

## DMK 中文層 smoke 以標準 baseline save 重跑

2026-09-01 的 DMK（**Directional Movement Keys** 1.5.0）smoke 執行時，baseline save pair
不在磁碟上（`7e70ae2` 誤刪，2026-09-02 已於公司復原），因此當時開檔用的不是 `runtime-qa` 規定的固定基準。
回家以復原後的 baseline save pair 重跑一次 DMK 中文層 smoke。
**通過**＝以標準基準開檔，DMK 中文層顯示與 2026-09-01 的結論一致；若不一致，原結論作廢並重驗。

**路徑已變（2026-09-04）**：baseline pair 依使用者 09-04 第 10 題裁示 A 搬到
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/baselines/ModpackKRDev0A.{ess,skse}`
（2026-09-05 實讀該目錄兩檔皆在，2.9 MB／6.2 KB），**不再在 `modpack-main/saves/` 底下**。
證據：`instance/profiles` commit `0f64c20`、母 repo commit `afb530d`（wf baseline save pair 路徑改指 `instance/profiles/baselines`）、
agentctl commit `b009076`、`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/SESSION-LOG.md`（「09-04 使用者裁示」節第 10 題）。
**人工校對層本身已上線**（`modlist.txt:520` 啟用、`:519` 機翻層停用，詳見
[`回家下載／重建`](home-setup.md) 的已完成節），所以這項剩下的只有「用標準基準重跑一次 smoke」。

## Modpack-KR Batch 6 final gameplay

自動 lane 21/21 PASS、`load_epoch 1 → 2`、0 new crash 不能代替真人。需驗新遊戲、城市／NPC、~~BFCO~~
**MCO**、Mysticism／Adamant、CT77／~~AVE~~、RDO、VIGILANT Altano 入口／字幕／語音、
自然跨 worldspace、MCM 與 description overlay 書。VIGILANT 四層須同版 1.8.2；Silent Voice 缺口已
接受、不需 TTS。證據見 [`Batch 6 RESULT`](../agentctl/logs/modpack-kr-final-smoke-2026-08-21/RESULT.md)。

**對象更正（2026-09-05 實讀，清單不刪只改名）**：
- **BFCO → MCO**：2026-09-02 使用者裁示戰鬥框架從 BFCO 移回 MCO 並已施工。
  `/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:407`＝`-BFCO - Attack Behavior Framework 3.100.5`（**停用**）、
  `:403`＝`-BFCO Traditional Chinese 3.100.5 Dev 2026-08-16`（**停用**）；
  現役是 `plugins.txt:864`＝`*Attack_MCO.esp`、`:865`＝`*scar-adxp-patch.esp`，`modlist.txt:404`＝`+SCAR 2.01`。
  所以這條驗的是 **MCO 的輕／重／方向／sprint attack**，不是 BFCO。
- **AVE**：`modlist.txt:620`＝`-Simonrim AVE Constellations Merge 1.5 Dev 2026-08-16`（**停用**）、
  `:457`＝`-Thaumaturgy AVE Patch 1.1 Reference Dev 2026-08-16`（**停用**）。AVE 那半**作廢**，
  CT77 仍在（`:610`／`:613`／`:614`／`:615` 皆 `+`），只驗 CT77。
- Silent Voice 仍在：`modlist.txt:1319`＝`+Fuz Ro D-oh - Silent Voice`。

## 四個首次生效中文層 → 現在只剩兩個（2026-09-05 核對）

抽查 **Timing is Everything SE 2.2 MCM** 與 **SkyParkour 3.6.2 `Interface/Translations` UI**；
確認無方框、mojibake、截斷、空白。排序稽核：`mod-library/l10n/tools/` 的層優先權稽核。
兩層 2026-09-05 實讀仍啟用：
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:423`＝`+Timing is Everything SE 2.2 - Traditional Chinese`、
同檔 `:640`＝`+SkyParkour 3.6.2 - Traditional Chinese`。

另外兩個抽查對象**已不在載入序，抽查取消**（原文保留在下面，不是刪除，是改寫成現況）：

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

- **原對象**：`RDO Final Traditional Chinese Dev 2026-08-16`（自製繁中層），範圍見
  [`layer README`](../mod-library/l10n/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/README.md)。
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

## VIGILANT 1.8.2 正體中文

現役已是 exact 1.8.2，45 筆 `BOOK.DESC` 私人 text-only layer 亦已升版。到晨星城風岳旅店找
Altano，抽查主線開場、對話／字幕、日誌／目標、書籍、物品／效果、MCM，至少打開一件「石之碎片」
確認描述為正體。英／日配音保留；作者檔與私人修正不公開重發。

## 2026-08-20 任務內容批

抽查 UNSLAAD 3.0.6b、Missives 2.03、DAc0da 1.1.0b、GLENMORIL 0.96.80b 的 MCM／任務入口、
~~正體~~**中文**日誌／對話／字幕、語音與跨 worldspace。GLENMORIL 語音覆蓋 3,653/4,792，UNSLAAD 英語語音
只涵蓋 Act 1；Silent Voice 是接受狀態。證據見
[`quest batch`](../agentctl/logs/quest-content-batch-2026-08-20.md)與
[`final smoke`](../agentctl/logs/modpack-kr-final-smoke-2026-08-21/RESULT.md)。

**對象更正（2026-09-05 實讀，四件都還在，但兩件的中文層從繁中換成簡中）**：
- **UNSLAAD**：`modlist.txt:356`＝`+Unslaad SE 3.0.6b Dev 2026-08-20`（本體啟用），
  中文層現役是 `:353`＝`+ZH-Unslaad-CHS-113238-Dev-2026-09-03`（**簡中**），
  原繁中層 `:354`＝`-Unslaad Traditional Chinese 3.0.6 Dev 2026-08-20`（**已停用**）。
- **DAc0da**：`:349`＝`+DAc0da 1.1.0b Dev 2026-08-20`（本體啟用），
  中文層現役是 `:344`＝`+ZH-DAc0da-CHS-139176-Dev-2026-09-03`（**簡中**），
  原繁中層 `:345`＝`-DAc0da Traditional Chinese 1.1.0 Dev 2026-08-20`（**已停用**）；
  另有 `:346`＝`+DAc0da-Voiced-Traditional-Chinese-Combined-Dev-2026-09-03`（語音層繁中，啟用）。
- **Missives**：`:322-332`／`:350` 共 12 個條目全啟用，仍是繁中層。
- **GLENMORIL**：`:333-338`／`:341-343` 全啟用，仍是繁中層。
所以「正體日誌／對話／字幕」這個條件對 UNSLAAD／DAc0da 已不適用，改按
「有中文、無方框破版」判（繁簡都可接受）。

## JhNPCBeautyDev 蓋掉 NPC 中文名（2026-08-28 發現，待裁示）

`JhNPCBeautyDev.esp` 在**插件層**覆蓋數個 NPC 的 `FULL`，把中文名寫成英文，已確認的有
**Lydia**（`override_depth=4`）、Bryling、Erdi、EvetteSan。症狀是「對話中文、名字英文」。
由 `loadorder.txt` 決定，**與 modlist 優先度無關**，2026-08-28 的順序修復管不到。
`opus-apply-order` 與其子線各自獨立撞到同一件事。

**先請確認範圍**：進遊戲看 Lydia 的名字是不是英文，並留意還有沒有別的 NPC 中文名變英文
（上面四個是資料層查到的，不保證窮盡）。

**2026-09-05 實讀：本項仍然有效、對象還在。**
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/plugins.txt:629`＝`*JhNPCBeautyDev.esp`（**啟用**）、
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/loadorder.txt:688`＝`JhNPCBeautyDev.esp`。
注意它**不在 `modlist.txt` 裡**（`grep -i JhNPC` 對 modlist 零命中）——這是 MO2 mod 名與 plugin 名不同名造成的，
不是它沒安裝；查它要查 `plugins.txt`／`loadorder.txt`，別只查 modlist。
同一件事另有筆記 `/home/lorkhan/repo/moddings/skyrim/agentctl/status/todo/22-JhNPCBeautyDev帳本對不上.md`。

**兩條修法擇一**（dispatcher 2026-08-28 判定延後，理由是不在剛修好並 commit 的 load order 上
疊第二次改動、且當時沒有實機驗證窗口）：
- 調 `loadorder.txt` 把 `JhNPCBeautyDev.esp` 往前移 —— 簡單，但會讓它的**外觀**被別人蓋掉，
  而外觀正是這個 mod 的用途，等於本末倒置。
- 做一個小 patch plugin，把那幾筆 `NPC_` 的 `FULL` forward 回中文 —— 不動外觀，但要多一個插件名額。

傾向後者，但要等實機確認範圍後再定。

所有本頁項目共同檢查：無方框、mojibake、截斷、空白或新 crash；未走過的流程不得稱 gameplay PASS。

## 已完成／作廢（封存）

> 以下四項在 2026-09-05 逐條對照證據後判定不再需要你動作，從 open 清單移到這裡保存歷史；每項附證據絕對路徑或 commit hash。

### ~~Missives 中文層與 MCM 取捨~~（兩題並存，均已裁示）

**判定：這是兩題，不互相推翻。**

- **(a) 中文層採 Loader 版還是原版**：沿用 2026-09-01 裁示 A；全域 `sLanguage` 維持 `ENGLISH`，
  Missives 的 `_chinese.txt` 仍按原計畫局部改為同 basename 的 `_english.txt`。目前仍找不到已執行改名的證據，
  所以這項保留為待部署／驗收，不因 (b) 而取消。
- **(b) MCM 可否接受部分英文**：**2026-09-05 使用者裁 B：接受部分英文**；Settings Loader 勝出。
  這只決定 MCM winner 與可接受的顯示結果，不撤銷 (a) 的全域語言槽與局部檔名裁示。

證據：
`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/STATE.md:102`、
`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/rulings/REPORT.md:13`。

以下保留裁示前的原始等待事項與衝突脈絡；其中「打架／待確認」是 19:38 裁示前的歷史文字，
已由上面的 (a)／(b) 分題結論收束：

**裁示：A —— `sLanguage` 維持 `ENGLISH`，局部修 Missives 檔名。**（2026-09-01，使用者當場口頭裁示；
見[裁示簡報](decision-briefs-2026-09-01.md)第 7 條。）回家把 Missives 的 `_chinese.txt` 翻譯檔改為
同 basename 的 `_english.txt`，不改全域 `sLanguage`，也不遷移 11 個已驗 `_English.STRINGS` 層。
**通過**＝部署 winner 只留下可由 `ENGLISH` 槽載入的正確檔名，進遊戲抽查 Missives MCM／任務文字
確實載入中文，且既有 11 個 STRINGS 層無回歸。

**⚠ 兩條裁示打架，落地前要你再確認一次（2026-09-05 發現）**：
- 2026-09-01 裁示 A（上面這條）＝**改檔名讓 Missives MCM 完整中文**。
- 2026-09-05 裁示（condense cd2 第 9 題「Missives MCM 優先度」）＝**B，Settings Loader 勝出、接受部分英文**。
  證據：`/home/lorkhan/repo/moddings/skyrim/modpack-design/wf/wait_todo/zh-layer.md`（「Missives MCM 優先度」節）、
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/rulings/HANDOFF-lead-rulings.md`（B 段第 12 條）。
  兩者不完全互斥（一個講檔名、一個講誰勝出），但**合起來的淨效果是「MCM 會有幾句英文」**，
  與 09-01 的「確實載入中文」驗收條件相衝。同一件事另有筆記
  `/home/lorkhan/repo/moddings/skyrim/agentctl/status/todo/19-Missives兩條裁示互相打架.md`。
- **待確認（19:38 裁示前狀態）**：我查了 09-04／09-05 兩天的 REPORT 與 profiles commit，
  **找不到「已執行 `_chinese.txt` → `_english.txt` 改名」的證據**；現役 Missives 家族 12 個條目
  （`modlist.txt:322-332`、`:350`）都還在啟用。這段等待狀態已由上面的 19:38 裁示終結。

### ~~天賦／Serana 中文層實機確認（promote `feat/zh-dsport-2026-09-02` 的前提）~~（2026-09-03 由 rt1 完成，證據 /home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/rt1/REPORT.md）

**判定：已完成（2026-09-03 由 rt1 實機確認，2026-09-05 核對無異動）。**

2026-09-02 晚 MCO 遷移 16 條實機驗收已由使用者全過並 promote（`instance/profiles` main `9e188e2`）。
之後 dispatcher 在 `feat/zh-dsport-2026-09-02` 部署了 SDA 4.3.2 補完層（插英文本體之前，舊 4.1.1.3 停用）與
Ordinator／SPERG 天賦補完三層。請使用者進遊戲看：技能樹 perk 名稱／說明是否中文、Serana 對話是否中文；
過了就 promote，任一不過就依 [`sda/REPORT.md`](../agentctl/handoffs/home-2026-09-02/sda/REPORT.md)、
[`zhgap/REPORT.md`](../agentctl/handoffs/home-2026-09-02/zhgap/REPORT.md) 的 backup 覆回。

### EnaiRim Batch 7 終態 gate

**判定：作廢——抽查對象已不在載入序（2026-09-05 核對）。**
`Audugan` 與 `Valravn` 在現役 profile 三個檔裡**一次都沒出現**：
`grep -ic` 對 `/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt`、
`.../plugins.txt`、`.../loadorder.txt` 三檔皆回 **0**。
同節提到的 BFCO 也已於 2026-09-02 停用改 MCO（`modlist.txt:407` 為 `-`），
TK Dodge／Precision／WYT 的組合條件因此不再成立。
**這節整段的驗收前提（Batch 1–6 施工後的 EnaiRim 終態）已被 2026-09-02 的 MCO 遷移與
2026-09-03 起的 LoreRim 借用兩輪改動覆蓋。** 若之後真要重開 EnaiRim Batch 7，
請以當時的載入序重新產生清單，不要沿用本節。
原始固定範圍仍在 `/home/lorkhan/repo/moddings/skyrim/agentctl/logs/simonrim-to-enairim-final-selection-2026-08-24/batch-7-integration-promotion-plan.md`。

等 Batch 1–6 施工後，確認 Audugan／Valravn private CHT 與新文字層顯示；shrine／standing stone／
High Hrothgar candidates 無穿插且可互動；Valravn 搭 BFCO／Precision／TDM／TK Dodge／WYT 的輸入、
多人節奏、武器速度、耐力與命中手感；抽查 race／faith／spell／enchantment／shout UI。固定範圍見
[`Batch 7 計畫`](../agentctl/logs/simonrim-to-enairim-final-selection-2026-08-24/batch-7-integration-promotion-plan.md)。

### modlist 優先度修復的實機驗收（2026-08-28 套用，待驗）

**判定：已被後續多輪覆蓋，不再單獨列 open（2026-09-05 核對）。**
三個理由，每個都有實讀證據：
1. **數字對象整批作廢。** 原文驗的是「377 行／318 啟用、Active 318」；
   2026-09-05 實讀 `/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt`
   ＝**1379 行／啟用 1278**，`plugins.txt`＝874 行／啟用 851。中間經過 grow／trim／MCO 遷移／
   LoreRim 借用／CC 全開／LOD 五輪大改，`launch-mo2.sh` 開出來不可能是 318。
2. **BFCO 症狀不存在了。** 原文要驗「第三人稱能否正常攻擊（BFCO 行為圖被 vanilla 壓掉）」；
   BFCO 已於 2026-09-02 停用改 MCO（`modlist.txt:407` 為 `-`、`plugins.txt:864`＝`*Attack_MCO.esp`），
   而 MCO 遷移的 16 條實機驗收 2026-09-02 由使用者口頭全過。
3. **中文顯示已在 2026-09-05 由使用者親眼驗過。** 當日 13:36／13:4x 六項目視全 PASS，
   其中 ⑦ 六把武器名中文、⑥ 平民閒聊中文都通過。
   證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/win/data/ingame-checks.csv`、
   `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/win/REPORT.md`、
   `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/STATE.md:66`／`:70`／`:71`、
   agentctl commit `f087dda`／`f983f38`。
Ordinator 天賦頁是否中文這一條，改由
[`四個首次生效中文層`](#四個首次生效中文層--現在只剩兩個2026-09-05-核對) 之外的日常抽查涵蓋，
不在本檔另列。

2026-08-28 已把 `modlist.txt` 從事故後的名稱序重建為正確優先度並 commit（377 行／318 啟用；
winner 差異 5485→5；Pandora Output 重新壓過 TK Dodge RE；9 個被本體壓掉的中文層全回復），
資料層由 houseCARL 實查 Ordinator 天賦、ESW 武器名、AI Overhaul NPC 名、Sofia 皆已回中文。
**還沒進遊戲驗**。請用 `launch-mo2.sh` 開 MO2 確認 Active 318 → 進遊戲**離開存檔重進**，驗：
第三人稱能否正常攻擊（原症狀：BFCO 行為圖被 vanilla 壓掉）、Ordinator 天賦頁是否中文、
武器名是否中文。證據見 [`opus-apply-order`](../agentctl/handoffs/done/2026-08-28/opus-apply-order/)
與 [`根因`](../agentctl/logs/modlist-priority-bug-2026-08-23.md)。
