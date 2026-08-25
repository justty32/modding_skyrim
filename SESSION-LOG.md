# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

## 現役工作

截至 **2026-08-23（Asia/Taipei）**，母 repo 沒有仍在執行中的 agent 工作，也沒有 codex 線在跑；
Skyrim／MO2 已關閉，兩個資源鎖都未持有。

**2026-08-23 的主線是工作區統整**（[consolidation-2026-08-23](wf/workflows/plans/consolidation-2026-08-23/README.md)）。
日常工作現在分成四條獨立的線，各自是 private submodule：

| 線 | 管什麼 |
|---|---|
| [`instance/`](instance/) | 本機部署狀態：MO2 instance、現役 profile `modpack-main`、load order、profile 稽核 |
| [`mod-library/`](mod-library/) | mod 庫：MongoDB 索引、自製繁中翻譯層、自製插件與修正 esp |
| [`modpack-design/`](modpack-design/) | 整合包設計：六階段整包計畫、技術債、選型調查 |
| [`agentctl/`](agentctl/) | AI 操控總控：工作流、agent 交接、QA harness、執行證據 |

各線自己的續行點在 [`agentctl/SESSION-LOG.md`](agentctl/SESSION-LOG.md)——那是 Skyrim 工作線的交接主線。
**本檔只管母 repo。**

## 2026-08-24 open 規劃

- **2026 YouTube mod 候選池**：已把三個使用者提供 URL 依 video id 去重；動畫專題保存在
  [`Syn Gaming 動畫候選筆記`](modpack-design/content-plan/syn-gaming-animation-showcase-backlog-2026-08-24.md)，
  另外兩支 gameplay／VFX／NPC／地點／UI 清單保存在
  [`綜合候選筆記`](modpack-design/content-plan/youtube-mod-showcase-backlog-2026-08-24.md)。全部仍是
  `UNREVIEWED`／`DEFER`，不是下載清單；之後一次只查一項，先從 BFCO 明示 moveset、Simple Dual Block、
  RAM 或 RaySense root 擇一。Nariva 簡介的 `Nazeem Says More` 與 Gulan0 idle 共用 Nexus 165916，已標
  `SOURCE-LINK-HOLD`，不得以疑似誤植連結繼續施工。
  另六支後續影片已拆到[沉浸／gameplay](modpack-design/content-plan/youtube-immersion-gameplay-showcases-2026-08-24.md)
  與[戰鬥／動畫](modpack-design/content-plan/syn-gaming-combat-animation-showcases-2026-08-24.md)兩頁；重複推薦只提高
  盤點優先度，不算相容證據。SoftGaming 清單中的 TrueHUD、SmoothCam、Remember Lockpick Angle、
  Dynamic Things Alternative、Biggie Traits、TDM、Better Jumping、SkyParkour、BFCO 已由現役 profile
  證明啟用，不列為新品；Attack MCO、Blade and Blunt、Wildcat 依現役 BFCO＋Valravn 路線保持 NO-GO。
  最新六支再收進[動畫／戰鬥補充](modpack-design/content-plan/youtube-animation-combat-showcases-addendum-2026-08-24.md)
  與[魔法 showcase 對照](modpack-design/content-plan/youtube-magic-showcase-backlog-2026-08-24.md)：Glenny 與
  SoftGaming combat 的 MCO stacks 整體隔離；魔法影片的 Mysticism／Apocalypse／Triumvirate 已是本輪選型，
  其餘新法術全部 `DEFER-AFTER-ENAIRIM`，不擴張 Batch 1。
  後續沉浸／legacy intake 讓總數來到 **35 個唯一 video ids**；新候選分別進
  [沉浸第二輪](modpack-design/content-plan/youtube-immersion-showcases-round2-2026-08-24.md)與
  [2018–2023 legacy 索引](modpack-design/content-plan/youtube-legacy-showcases-2018-2023.md)。Dynamic Things
  Alternative 是此輪唯一由現役 profile 新確認的 enabled 項；Andromeda／CGO／Lupine／YASH 保持產品
  NO-GO，Oldrim-only 與 description-incomplete 來源保持 HOLD。redshift 的五個魔法 immersion 候選已併入
  既有魔法頁，不改 EnaiRim Batch 1。

  **2026-08-25 續行中**：使用者要求把 YouTube 候選全部研究完；公司端維持一次只查一項、只做唯讀
  官方來源查核，不下載／部署。全池起始有 162 個 `UNREVIEWED` 文字命中；本輪先把 locomotion 的跨影片
  重複與第一個 sitting 候選收束到 156：Vanargand II 男女 main 為 `GO` staged visual pilot、Leviathan II
  為同 scope `DEFER-ALTERNATE`、Gulan0 mod 164743 因公司端 adult preference 為
  `DEFER-SOURCE-HOLD`、Modern Female Sitting 2.0 OAR main 為 `GO` conditional pilot。其後 sitting群組亦已
  收束到 152個文字命中：Simple Sit與 Dynamic Sitting因同 scope淘汰；Take a Seat 1.01 OAR為正交的
  NPC ground／ledge／meditation `GO`；Barstool Exit是 `DEFER` repro-first Pandora behavior fix；固定 owner表見
  [`youtube-sitting-owner-comparator-2026-08-25.md`](modpack-design/content-plan/youtube-sitting-owner-comparator-2026-08-25.md)。
  單項報告與索引都在 [`youtube-audits/animation-combat.md`](modpack-design/content-plan/youtube-audits/animation-combat.md)。
  下一件依動畫主池順序查 Sonder's RaySense Wall Leaning 188857；不得把 `UNREVIEWED` 清零當唯一完成證據，
  最後仍須逐個來源頁反查所有 35 個 video ids 的候選皆有結論或明確 HOLD。

## 2026-08-23 已收束

- **工作區統整**：`~/notes/projects/modding/skyrim` 的 1047 檔依性質分流到四條線，
  逐檔比對驗證；實機截圖與 MongoDB 快照刻意留在 repo 外。順帶修掉一個曝險——
  `dist/mods/` 的 34 個翻譯層內含他人 mod 的完整原始 ESP，一直躺在這個 public repo 裡。
- **MO2 profile 改名**：`Modpack-KR` → `main` → `modpack-main`（前綴是為了不跟分支名撞）。
  走完 `feat → release → main`；`check_profiles.py` 新增 `selected_profile` 比對，
  補上一道從來沒有的閘門。
- **中文層排序失效**：四個覆蓋層裝在本體下方而完全失效（11 個檔被英文本體贏走），已上移並晉升。
  常駐稽核 `mod-library/l10n/tools/audit_layer_priority.py`。
- **agent 協作協議正規化**：`agentctl/docs/driving-codex.md` 與 `resource-locks.md`；
  修好兩個指向已刪除 `~/skyrim_agent_out` 的死路徑（遊戲鎖與 inbox）。
- **連結檢查涵蓋四條線**：`git ls-files` 到 gitlink 就停，四條線的 87 個壞連結沒人在看。
  全數修復，檢查器改為連 submodule 一起掃（427 檔 → 789 檔）。
- **Downloads 歸檔**：113 個 Skyrim mod 壓縮檔逐一開檔判斷，61 個新的入 `~/skyrim_mods/hdd/`。

- **過時作廢內容清理**：刪掉三份（已被取代兩次的 `workspace-reorg` 計畫、任務已完成的
  `CONSOLIDATION-TODO`、已併入通用 inbox 的韓文 inbox）。**查過但沒刪的更多**——
  Simonrim 那批看起來被 EnaiRim 取代，實際 modlist 顯示還啟用著；Adamant 6.0.2 看起來被
  6.0.4 取代，實際還裝著而且是 5 份 recovery-checkpoint 的回滾來源。
- **頂層重構**：工作流骨架收進 `wf/`、`scripts/`＋`tests/` 併成 `tools/`，頂層 22 → 15 項
  （對齊 tome4／elin 已在用的慣例）。47 個連結重新指向，CI 指令跟著改並實測。
  一開始判斷不必拆檔，**使用者否決並定下「`wf/` 內超過 8KB 就拆」的硬線**，
  五份計畫（34K／31K／25K／18K／11K）各自拆成目錄，切線是
  「環境事實與設計決策／分階段任務／重審／附錄／執行紀錄」。
  120 個標題逐一比對確認沒漏，15 個連結重指。現在 `wf/` 最大的檔 7.8K。
- **七套 Skyrim 工作流**：mod-discovery／nexus-intake（含衛星件與整套系列）／localization
  （含補全既有中文層）／profile-change／modpack-planning／agent-dispatch／runtime-qa，
  外加 `refactor/moving-things.md`（六類會斷的東西）與 `testing.md` 的
  **「綠燈不等於有檢查」**。全部帶著實際踩過的坑，路由在 [`wf/WORKFLOWS.md`](wf/WORKFLOWS.md)。
- **HID 能力實況入版控**：這台機器能不能驅動螢幕鍵鼠的事實原本只在 repo 外的
  `~/shared_agent_locks/README.md`，且有兩處是錯的（`ydotool` 其實已安裝，擋住的是
  `/dev/uinput` 權限而非缺軟體）。已實測校正並收進 `agentctl/docs/resource-locks.md`。
- **L4 舊命名壓縮檔改用 md5 還原來源**：`md5_search` 吃檔案內容不看檔名，174 筆跑出
  28 個 hit（146 miss 是對岸站台或重打包，不是檔案有問題）。工具
  `mod-library/db/resolve_legacy_md5.py`，報告 `mod-library/audits/l4-md5-resolution.md`。
  **檔名裡的 Nexus id 不可信**——實測一筆檔名寫 77993、內容其實是 82876。
  四筆上游已下架，依 D5 保險栓標了 `never_delete`。
- **三個 db 腳本的預設路徑在搬家後沒對過**：報告輸出指向不存在的 `mod-library/docs/`，
  而 `BACKUP_DIR`／`LOG_DIR` 會把 MongoDB 快照 `mkdir` 進 git repo。
  `scan_mod_library.py` 當初改對了，這三個漏了——**同一次搬遷、同一類錯、只補到一半**。

## Durable 狀態入口

- 四條線的入口：各線 README；Skyrim 工作線交接主線在 `agentctl/SESSION-LOG.md`
- houseCARL fork 維護決策：
  [fork-maintenance-decision.md](analysis/houseCARL/answers/fork-maintenance-decision.md)
- houseCARL Linux/MO2 技術方案：
  [linux-manjaro-mo2-runbook.md](analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md)
- 需使用者或外部環境才能完成的工作：[WAIT_USER.md](WAIT_USER.md)

## 各工作流 session-log

| 工作流 | session-log | open 摘要 |
|--------|-------------|----------|
| feature-dev | [workflows/feature-dev/session-log.md](wf/workflows/feature-dev/session-log.md) | 無 |
| refactor | [workflows/refactor/session-log.md](wf/workflows/refactor/session-log.md) | 無 |
| investigation | [workflows/investigation/session-log.md](wf/workflows/investigation/session-log.md) | 無 |
