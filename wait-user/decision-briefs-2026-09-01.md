# 2026-09-01 單頁裁決簡報

> 本檔由 cx-decide 於 2026-09-01 產出，供使用者拍板用。**2026-09-01 sn-tidy 複查**：實測 `grep -rn "decision-briefs-2026-09-01" --include="*.md" .` 並過濾出真正的 markdown 連結語法（`[text](decision-briefs-2026-09-01.md)`，且限已納入 git 追蹤、會被 `.github/workflows/docs.yml` 連結檢查掃到的檔案），命中 **3 個檔案共 12 處連結**：`wait-user/home-setup.md`（3 處，第 6、14、23 行）、`wait-user/integrated-runtime.md`（2 處，第 6、15 行）、`wait-user/later-decisions.md`（7 處，第 24、26、28、30、33、44、51 行）。本檔已是這些裁示的授權憑證，刪除會造成斷鏈並使 CI 連結檢查失敗，**不可刪除**。

可直接回覆：`1A 2B 3A …`；需要改條件時在該編號後補一句。

### 1. Serana 要停舊版繁中，還是升 SDA 4.3.2？

- **要決定的是**：選定 SDA 本體版本與中文層路線。
- **選項**：A) 4.3.2＋exact 簡中 B) 4.1.1.3＋現成繁中 C) 4.3.2＋自製繁中差分
- **各選項的代價**：A) 失去全繁中一致性；B) 失去新版內容與修正；C) 失去快速落地，增加 900+ 行級工量。
- **已知事實**：4.3.2 有 exact 簡中；現成繁中只到 4.1.1.3，不能覆蓋新版。`agentctl/handoffs/done/2026-08-29/cx-serana/REPORT.md:183`、`:184`
- **已知事實**：4.2.0 單版已明載新增 900+ voiced lines。`agentctl/handoffs/done/2026-08-29/cx-serana/REPORT.md:170`
- **缺什麼**：選 A/C 後仍需回家取得 archives 做 binary topology gate；現在不妨礙拍板。
- **我的建議**：選 A，先吃 current 修正與 exact 層；簡中已是允許語種，成本遠低於自製差分。

### 2. follower 凍結要維持、有限解凍，還是全面重開？

- **要決定的是**：劃定新 follower 與既有 follower 修補可進施工單的邊界。
- **選項**：A) 維持凍結，只修 Sofia／Recorder B) 只解凍 Auri＋VIGILANT，並採 Sofia 選配 preflight／No Bump C) 全面重開新 follower 生態
- **各選項的代價**：A) 失去 Auri 與 VIGILANT commentary；B) 失去單純硬凍結並多一組 QA；C) 失去範圍控制，Kaidan／Inigo／3DNPC 等前置會膨脹。
- **已知事實**：現行凍結只含新 follower 與 follower framework，不含一般 NPC。`agentctl/handoffs/done/2026-08-29/cx-fdlg/REPORT.md:53`
- **已知事實**：Auri 本體與中文技術上可行，目前唯一產品阻擋是 follower 凍結。`agentctl/handoffs/done/2026-08-29/cx-fdlg/REPORT.md:91`、`:93`
- **缺什麼**：無，可直接決定；B/C 落地後才做 winner 與 runtime preflight。
- **我的建議**：選 B，把例外鎖成 Auri＋現役 VIGILANT，不順手引入第二名新 follower。

### 3. Mihail 第一批走哪種生態與分布？

- **要決定的是**：選定首批美術方向、spawn topology 與中文政策。
- **選項**：A) 自然核心 4–6 件＋原生 hand-placed＋接受 exact CHS B) Morrowind／風格 wildcard 小批＋hand-placed C) 高奇幻／全域 SkyPatcher 分布
- **各選項的代價**：A) 失去較強烈奇幻風格；B) 失去低接觸面，需更多 record／飛行 gate；C) 失去原作者擺位與低耦合回滾，變成全域敵人分布決策。
- **已知事實**：菜單共 16 件，10 件有對版中文；報告建議首批自然核心 4–6 件。`agentctl/handoffs/done/2026-08-29/cx-mihail/REPORT.md:111`、`:112`、`:113`
- **已知事實**：SkyPatcher 會移除 hand-placed spawns、改進 leveled lists，並非 base 必要前置。`agentctl/handoffs/done/2026-08-29/cx-mihail/REPORT.md:59`、`:63`
- **缺什麼**：選定小批後需回家做 CELL／asset／record 與 Apothecary／Enai preflight。
- **我的建議**：選 A，先以最小可回滾批次驗證生態密度，再決定要不要擴張風格。

### 4. Bandolier NPC 分發與中文要怎麼兼得？

- **要決定的是**：選擇放棄 NPC 分發、做 forward patch，或接受英文裝備名。
- **選項**：A) 本體＋CHS，不裝 NPC 層 B) 裝 NPC 層＋106 字串 forward patch C) 全裝但接受 93 件英文
- **各選項的代價**：A) 失去 NPC 分發；B) 失去零維護成本；C) 失去中文完整性。
- **已知事實**：NPC 層 93 個 ARMO override 自帶英文 FULL，載入順序無法救回中文。`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:9`、`:11`
- **已知事實**：既定 realistic variant 令 forward 範圍成為 83＋23 兩批。`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:19`
- **缺什麼**：無，可直接決定。
- **我的建議**：選 B，以小型 patch 同時保留原先 GO 的 NPC 分發理由與中文完整性。

### 5. Reforging 是否接受中文層綁定 SkyPatcher？

- **要決定的是**：接受 SkyPatcher 分發、放棄本輪，或自製完整中文層。
- **選項**：A) 接受 SkyPatcher＋現成中文 B) 不接受並維持 DEFER C) 保留原分發並自製 302 WEAP／300 名稱
- **各選項的代價**：A) 失去分發 topology 自由；B) 失去 Reforging 內容；C) 失去低成本且譯名品質未必更好。
- **已知事實**：現成中文只支援原模組的 SkyPatcher 版本。`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:23`、`:26`
- **已知事實**：SkyPatcher 7.0.0 已在；拒絕它則需自製 302 WEAP／300 unique 名。`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:27`、`:32`
- **缺什麼**：無，可直接決定。
- **我的建議**：選 A，既有框架已在，沒必要為保留未採用的分發自由重做 300 個名稱。

### 6. Animated Armoury 三個同版中文層選哪個流派？

- **要決定的是**：選零成本已驗層，或換成和光／WOK 名詞體系。
- **選項**：A) `72518` 已驗 DAR 簡中 B) `152701` 和光 DAR 簡中 C) `33202` WOK SSE 簡中
- **各選項的代價**：A) 失去全包名詞一致性；B) 失去既有驗證、需重做 topology；C) 失去分支確定性，SSE 層可能不對現役 DAR。
- **已知事實**：三層均標 v2.3；`72518` 本機已有且拓撲已驗。`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:36`、`:40`
- **已知事實**：`152701` 是和光 DAR；`33202` 針對 SSE、使用前須確認分支。`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:41`、`:42`
- **缺什麼**：選 B/C 才需回家取得檔案並重跑 topology。
- **我的建議**：選 A，先用已驗 exact 層；名詞差異不值得在未抽樣前推翻可用基線。

### 7. `sLanguage` 要維持 ENGLISH 還是全域改 CHINESE？

- **要決定的是**：固定全域語言槽，並指定少數 `_chinese` loose 層的處理方式。
- **選項**：A) 維持 ENGLISH，個別改檔名 B) 改 CHINESE，全域遷移現役字串層
- **各選項的代價**：A) 失去免維護的原檔名，遇到個案例外要改名；B) 失去 11 個已驗 `_English.STRINGS` 層並承擔全域回歸。
- **已知事實**：核心的 English／Chinese STRINGS md5 相同，中文本來就放在 English 槽。`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:50`、`:51`
- **已知事實**：目前已知只踩到 Missives 一件 `_chinese.txt`，改名即可；改 CHINESE 會使 11 層失效。`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:55`、`:56`
- **缺什麼**：無，可直接決定。
- **我的建議**：選 A，把例外局部修掉，不為一件檔名問題翻轉全域語言槽。

### 8. Steam 2.5 MB 補丁要不要收？

- **要決定的是**：維持 1.6.1170 釘版，或允許 TargetBuild 24914197 更新。
- **選項**：A) 繼續暫停並維持離線／釘版 B) 回家備份確認後接受更新
- **各選項的代價**：A) 失去補丁可能包含的修正；B) 失去已知 runtime 基線，可能升至 1.7.99 並觸發整包重驗。
- **已知事實**：更新目前已暫停、Steam 離線，exe 仍為 1.6.1170。`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:63`
- **已知事實**：`AutoUpdateBehavior = 1` 有把遊戲升到 1.7.99 的風險。`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:64`
- **缺什麼**：repo 無補丁 payload／changelog；若考慮 B，需回家查明後再執行。
- **我的建議**：選 A，未知 2.5 MB 更新不值得打破已釘且已整合的 runtime 基線。

### 9. C2 的 `launch-mo2.sh` 快照要保留還是刪除？

- **要決定的是**：正式指定現役正本，並決定封存交付快照的命運。
- **選項**：A) 宣告 `instance/tools/` 為唯一現役正本，保留標明用途的封存快照 B) 宣告正本並授權刪除快照
- **各選項的代價**：A) 失去零重複，仍需維護「非正本」標示；B) 失去交付當下的可追溯實檔。
- **已知事實**：3.8 KB 現役檔由 `instance/README.md` 指向；3.4 KB 檔是交付當下快照。`agentctl/handoffs/done/2026-08-29/doc-refactor/CONFLICTS.md:11`、`:12`
- **已知事實**：封存說明已規劃標明現役位於 `instance/tools/launch-mo2.sh`，兩份內容皆未動。`agentctl/handoffs/done/2026-08-29/doc-refactor/CONFLICTS.md:17`、`:18`
- **缺什麼**：無，可直接決定；B 屬刪除授權。
- **我的建議**：選 A，明確區分現役正本與歷史快照即可消除歧義，毋須犧牲證據。

### 10. C3 的 Windows codex 線是否預設開網路？

- **要決定的是**：統一 `dispatch-windows.md` 的 network access 契約。
- **選項**：A) 固定 `network_access=false` B) 預設關閉，但另設經使用者授權的外網例外車道
- **各選項的代價**：A) 失去 Windows 線直接執行需網路工作的能力；B) 失去單一簡明規則，需定義授權與用途邊界。
- **已知事實**：同檔第一節以 push 為由開網路，第四節卻要求預設關閉。`agentctl/handoffs/done/2026-08-29/doc-refactor/CONFLICTS.md:47`、`:48`
- **已知事實**：第六節又禁止 Windows 線 commit／push。`agentctl/handoffs/done/2026-08-29/doc-refactor/CONFLICTS.md:49`
- **缺什麼**：無，可直接決定。
- **我的建議**：選 A，既然 Windows 線不得 push，原本唯一開網理由已不存在。

---

## 使用者裁示（2026-09-01，公司場次，當場口頭確認）

**全部照建議**：`1A 2B 3A 4B 5A 6A 7A 8A 9A 10A`

即：
1. A — Serana 先吃 current 修正與 exact 層（archives 的 binary topology gate 留回家）
2. B — follower 有限解凍，例外鎖成 Auri ＋ 現役 VIGILANT
3. A — Mihail 第一批走最小可回滾批次（CELL／asset／record 與 Apothecary／Enai preflight 留回家）
4. B — Bandolier 以小型 patch 兼得 NPC 分發與中文
5. A — Reforging 接受中文層綁定 SkyPatcher，沿用既有框架
6. A — Animated Armoury 用已驗 exact 層
7. A — `sLanguage` 維持 ENGLISH，局部修掉檔名例外
8. A — 不收 Steam 2.5 MB 補丁，維持 1.6.1170 釘版與離線
9. A — `launch-mo2.sh` 保留封存快照並標明非正本，現役正本為 `instance/tools/launch-mo2.sh`
10. A — Windows codex 線固定 `network_access=false`

裁示已生效，落地工作見各對應檔。本檔在全部落地後刪除。
