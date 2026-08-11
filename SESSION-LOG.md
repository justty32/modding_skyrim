# SESSION-LOG — 進度日誌 hub

只放還沒完成的活狀態。已完成的實作與調查歷史由對應 plan、子專案文檔與 git history 承接；需使用者親自做或決定的事在 [WAIT_USER.md](WAIT_USER.md)。

## 現役工作

### Play-KR 環境音 runtime 驗收

- 2026-08-11 使用 Play-KR + 暫時 QA try branch 實機啟動，AgentBridge 0.6.0 的 `GET /state?include=plugins` 直接確認六個目標 plugin 都在 engine runtime load order：`Regional Sounds Expansion.esp` (`FE:01D`)、`Reverb Interior Sounds Expansion.esp` (`FE:01E`)、Rain (`FE:01F`)、Thunder (`FE:020`)、`AcousticTemplateFixes.esp` (`FE:021`)、Reverb compatibility (`FE:022`)。
- 已載入現有 `Save3_474D...Tamriel...` 測試存檔，結構化 state 顯示玩家在戶外 `WhiterunExterior15` (`CELL 0x0000963B`)、`interior=false`、`worldspace=Tamriel`，玩家狀態正常；過程無 CTD。
- **這次尚未完成室內 runtime acceptance**：從戶外 `coc WhiterunBreezehome` 後 game-thread state 持續 503；乾淨重啟後單次 `load Save2_474D...WhiterunBreezehome...` 也未在時限內開始抽取 game-thread task。Skyrim 程序仍存活、`/ping` 正常且無 crash log，但這不能當作室內通過證據。後續應從已進入遊戲的 state 載入 Save2，或先解決 0.6.0 在 main-menu/load transition 的 task-queue 可觀測性，再補室內取樣。
- log 範圍：本輪後新 crash log = 0；最新 Papyrus log 只有 5 條既有類型的 missing-class 訊息，無 Regional/Reverb/AcousticTemplate 目標名稱；SkyPatcher 載入 `Acoustic Space Improvement Fixes` cell config 並完成 Cell Patcher，無 error/warn。Sound Record Distributor 已解析 Regional/Reverb 規則，但 log 仍有一條通用 `Failed to dispatch message to MergeMapper`，本輪無 before-runtime baseline 可證明它是新訊息，故不將其歸因於本批 mod。
- 結束已 `mo2ctl kill --mo2` + `try-fail`：測試存檔副本與 try branch 均移除，AgentBridge 回復 disabled；selected profile 仍是 Play-KR，profile repo `main` 於 `dd65524` 乾淨、與 HEAD 語意相同。`dd65524` 只是保留第一次啟動產生的合法 Play-KR runtime INI/plugins 格式化基線。
- 自動化穩定性不等於聽感；戶外區域音、雨雷、室內殘響與音量仍留 [WAIT_USER.md](WAIT_USER.md) 由使用者人耳驗證。

### agent-bridge MessageBox control

- 0.7.0 離線實作已完成（agent-bridge `716349f`）：`game.message_box` structured state、`POST /messagebox/select`、Python client、qa.json step 與 MCP tool 已落地；精確 message guard 用來避免等待期間 modal 被替換後誤按。client tests 47/47 PASS，clang-cl + xwin DLL build PASS。
- 本輪不啟動、不切換、不修改 MO2／Skyrim 執行狀態；實機 acceptance 等另一個 agent 釋放執行權後再做，項目已列在 [WAIT_USER.md](WAIT_USER.md)。

### 第三方 mod 流水線

- P0–P4 已完成；`projects/agent-bridge` 的 P1/P2/P3 commits 為 `30a97be` / `35d5692` / `6106646`，P4 補強 commit 為 `c641d77`。
- P4 實測 mod：`Bend Time Rings`（Nexus 10974，本機 archive sha256 `53f6d341cc72c143bd45d4518a487934345ab0b7da725b5d8cb880b1bcdc5513`），profile git commit `cfb34db Validate Bend Time Rings P4`。
- 驗收結果：zip install → manifest → QA profile `try/bend-time-rings` → houseCARL static gates → `qa.json` 到達 Bannered Mare + 穿上 `Ring of Slow Time` → 使用者視覺 handoff 通過。
- 權威計畫：[third-party-mod-pipeline.md](workflows/plans/third-party-mod-pipeline.md)。

### mod 庫建檔

- 1,585 筆 archive / 1,433 個 mod group 已建檔；DLL runtime 檢查、L1/L2 清理與 L3 隔離已執行。
- P1.4 Nexus 在架狀態補值已完成；A4-review 已完成，280 個漢化包中 259 個 high 寫回 `archives.translates_mod_id`，9 low + 12 none 留人工。
- A3 清理報告產生器（P1.5/P1.7）已在 notes 側落地：`tools/cleanup_report.py` 可重跑、寫入前自動備份。2026-08-11 重驗：離線 fixture 13/13 PASS（含 L2 三條例外），實庫唯讀 invariants 6/6 PASS，兩次分類一致。
- 本線現無可自動執行的清理待辦；後續只剩 notes 側 `l4-review-worklist.md` 的人工辨識與來源挑選，不進刪除流程。
- 107 筆 `quarantined_at` 不一致紀錄已從 `archives` 移除；稽核清單在 `~/notes/projects/modding/skyrim/docs/removed-missing-quarantine-2026-08-07.md`。
- 權威計畫：[mod-library-catalog.md](workflows/plans/mod-library-catalog.md)。

### 韓文站採集

- **B1/B2/B3 皆已完成**（2026-08-07；2026-08-11 完成調查回饋）。B1：`candidates` schema + `ingest_candidates.py` / `check_links.py` / `build_gallery.py` 落地，`rejected` 保險栓用暫存 DB fixture 驗證。B2/B3：兩批候選落地——`korean-public-2026-08-07-b2` 6 筆（連結 6/6 live），`korean-policy-porting-2026-08-07-b2b` 3 筆 live pending；圖庫在 `~/notes/projects/modding/skyrim/docs/candidates-gallery.html`。全程未下載任何 mod 本體。
- **採集方式已改變，別再照原計畫派 agy**：`agy` CLI 三次批次嘗試全部在 print mode timeout、零產出（前兩次疑因掛了大型 `~/skyrim_mods` workspace，第三次不掛仍超時）。改由 codex 以 deterministic `curl`/Python 從公開 Tistory 頁建 fixture。另：`arca.live/b/tullius` 匿名 `curl` 會撞 hCaptcha，不能作為「機器抓到原物」的通過條件。
- b2b 三筆已回饋到 [port-source-survey](analysis/port-source-survey/README.md)：逐筆對照保留的 `meta.json` 與 `page.html` 後，確認 BDO Arethel/Heled 是服裝、DS3 Silver Knight 是盔甲武器、Bloodborne Lantern 是道具／武器，**全部都不是地圖 port**。它們證明「使用別人已轉好的 Skyrim 成品」這條旁路，不證明來源遊戲的場景佈局或碰撞可抽取。線 B 無剩餘 open。
- 權威計畫：[round-2026-08-07-catalog-and-korean.md](workflows/plans/round-2026-08-07-catalog-and-korean.md)。

### 移植素材來源調查（port-source-survey）

- 2026-08-11 新增「四道關卡」評估框架（開容器／網格／**佈局**／碰撞），把最高分候選從猜測星等改成有來源的判斷。
- 三處更正：Bethesda 系非零轉檔（NIF 版本不同，需 `skyblivion-NIFConverter`）；**DS3/Sekiro 不是「同棧」**（MSB3/MSBS + havok 版本皆異，現有 extractor 釘死 MSB1）；BG3 上修並修掉「BG3 屬 Unity 系」的分類錯誤。
- 實質結論：**BG3 是最強的非 Bethesda 候選**——`Levels/` 的 `.lsf` 可經 LSLib 轉 `.lsx` 純文字讀取擺放，功能等價於 MSB，最難的「佈局」關是通的。
- 桌面能查的已做完；剩下的待辦都需要本機有該遊戲，建議優先驗 BG3 的 `.lsx` 擺放欄位能否對映 ModForge spec placements。
- 權威文件：[analysis/port-source-survey/README.md](analysis/port-source-survey/README.md)。

### darksouls-port

- P2 新版碰撞已將懸空碰撞面積降 98.9%；走廊基本正常，門洞仍會卡。
- **幽靈碰撞有兩個互相獨立的來源，別混為一談**：
  - **根因一：平面內填洞**（有門洞的牆，凸包把洞填實）→ 解法是 `--ghost-tol` 0.25 → 0.02。使用者已決定先收現狀，套用與實機複驗留在 [WAIT_USER.md](WAIT_USER.md)。
  - **根因二候選「按 `ConnectCollision` 型別整類排除」已於 2026-08-11 實證不可行**：直接 dump `extracted/msb_m18_01.json` 確認 `h0054B1` 與 `h0099B1` **各自同時**有一筆 `Collision` 與一筆 `ConnectCollision`，四筆的 position / rotation / scale 分別完全相同。它們是同一 model 的重複語義引用，不是可分開刪除的幾何；以 model 名過濾會同時砍掉 `h0054B1` 的真地板。結論是維持 P2 現行 `ORPHAN_DIST = 2.0` m 的個別 hull 距離過濾，extractor 不加型別過濾或白名單。證據表與原結論更正見 [P1-INGAME-FINDINGS.md](projects/darksouls-port/p1/P1-INGAME-FINDINGS.md) 根因二。
- 離視覺幾何 >2 m 的 61 顆孤兒 hull（1.2%）**已在 P2 砍掉，不是待辦**：`drop_orphan_hulls()` 以 `ORPHAN_DIST = 2.0` m 逐顆過濾並無條件套用，`h0098`/`h0099` 整檔清空、殘留載體 NIF 也一併 prune。現裝的 `DSPortP1` 已含此過濾。
- **動任何碰撞重跑前的已知阻礙**：`tools/collision_hulls.py` 的相依全是 lazy import，跑起來才炸，而目前哪個 venv 都不齊。**`shapely` 是必要的且正好在 `--ghost-tol` 的關鍵路徑上；`vhacdx` 不需要**（只在 `--method vhacd` 用，預設是 `components`）。權威 setup 在該檔檔頭 docstring，步驟見 [WAIT_USER.md](WAIT_USER.md)。
- 技術細節：[P1-INGAME-FINDINGS.md](projects/darksouls-port/p1/P1-INGAME-FINDINGS.md)。

### houseCARL

**2026-08-11 定案：只顧自己的 fork，不再追上游。** force-push 兩條 fix branch 到 fork、submodule 釘 fork branch、**不開 upstream PR**、`set_mo2_instance` 的第三條 fix **先不開**。執行步驟在 [WAIT_USER.md](WAIT_USER.md)（需在家做）。

上游現況（2026-08-11 查證，是這次決策的依據）：

- upstream `main` 比兩條 branch 的 rebase 基準 `8385fc6` **多 228 個 commit、147 個檔案有改動**，總計 717 commits，最新 release 1.9.0，八月初仍在密集出 PR（#311–#320）。**2026-07-17 那次 rebase 已再度過期**，而且是個持續移動的目標。
- 那些 Linux 問題**仍然沒有人修**：近期 commit 搜 Linux / Wine / gamePath / loose asset / dialogue lint 全部零命中；issue 搜 Linux、Wine、Proton 也是零。修正仍有效。
- 但上游對 Linux 的接受度不樂觀：README 第一條需求寫「Windows.」，通篇未提 Linux/Wine；`CONTRIBUTING.md` 雖寫歡迎 issue 與 PR 且要求「動大工程前先開 issue」，**但該 repo 的 issue creation 被限制**，前置步驟不一定做得到；近期可見的 PR（#278–#320）作者清一色是 owner 本人（用 PR 對自己 review 當工作流）。*未翻完全部 248 個 closed PR，故不斷言「從無外部 PR 被合併」。*
- 推論：開 PR 的期望值低，且維持 PR 存活要一直追那 228+ 的漂移；force-push 到自己 fork 不依賴任何人點頭，是唯一能讓修正不被上游漂移吃掉的動作。

已知限制（決策後仍存在，不再視為待辦）：

- Linux 下 `set_mo2_instance` 不會把 `ModOrganizer.ini` 的 Wine `Z:\...` 前綴轉回 Linux path，接上 `/Data` 成為壞路徑。**繞法：explicit-paths mode**（`DataDir`/`ModsDir`/`ProfileDir`），mod 庫建檔、DLL 檢查、load order 讀取都是在這個模式下完成的。唯一失去的是 `load_order_status(profile=...)` 跨 profile 檢查，改為直接讀 profile 檔案。哪天 explicit-paths 真的擋到再開第三條 branch。

## 已關閉的方向

- `scene-capture-bridge` 的 Windows/MSVC CI 於 2026-08-07 放棄：唯一受支援的建置與出貨路徑是 Linux clang-cl + xwin。失敗的 GitHub Actions workflow 已移除，不再追 fmt/MSVC STL 相容性。
- AI 全自動 mod QA 迴圈與 agent-bridge 0.6.0 semantic control 已結案：livingNpcs generic anchor/parley 整鏈 **31/31 PASS**；loaded actor、name/runtime FormID、跨 interior/exterior cell move、action retry、dialogue index/TopicInfo FormID 與 MCP `qa_wait` 均已實機通過。實作與驗收權威在 `projects/agent-bridge` README，原計畫見 [ai-ingame-qa-loop.md](workflows/plans/ai-ingame-qa-loop.md) 第六節。
- 舊 `workspace-reorg` 方案已被現行多 repo + submodule 佈局取代，不再執行。

## 各工作流 session-log

| 工作流 | session-log | open 摘要 |
|--------|-------------|----------|
| feature-dev | [workflows/feature-dev/session-log.md](workflows/feature-dev/session-log.md) | 無 |
| refactor | [workflows/refactor/session-log.md](workflows/refactor/session-log.md) | 無 |
| investigation | [workflows/investigation/session-log.md](workflows/investigation/session-log.md) | 無 |
