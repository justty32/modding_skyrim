# SESSION-LOG — 進度日誌 hub

只放還沒完成的活狀態。已完成的實作與調查歷史由對應 plan、子專案文檔與 git history 承接；需使用者親自做或決定的事在 [WAIT_USER.md](WAIT_USER.md)。

## 現役工作

### 第三方 mod 流水線

- P0–P4 已完成；`projects/agent-bridge` 的 P1/P2/P3 commits 為 `30a97be` / `35d5692` / `6106646`，P4 補強 commit 為 `c641d77`。
- P4 實測 mod：`Bend Time Rings`（Nexus 10974，本機 archive sha256 `53f6d341cc72c143bd45d4518a487934345ab0b7da725b5d8cb880b1bcdc5513`），profile git commit `cfb34db Validate Bend Time Rings P4`。
- 驗收結果：zip install → manifest → QA profile `try/bend-time-rings` → houseCARL static gates → `qa.json` 到達 Bannered Mare + 穿上 `Ring of Slow Time` → 使用者視覺 handoff 通過。
- 權威計畫：[third-party-mod-pipeline.md](workflows/plans/third-party-mod-pipeline.md)。

### mod 庫建檔

- 1,585 筆 archive / 1,433 個 mod group 已建檔；DLL runtime 檢查、L1/L2 清理與 L3 隔離已執行。
- P1.4 Nexus 在架狀態補值已完成；A4-review 已完成，280 個漢化包中 259 個 high 寫回 `archives.translates_mod_id`，9 low + 12 none 留人工。
- 剩餘主要 open：A3 清理報告產生器（P1.5）+ L2 三條例外驗證。
- 107 筆 `quarantined_at` 不一致紀錄已從 `archives` 移除；稽核清單在 `~/notes/projects/modding/skyrim/docs/removed-missing-quarantine-2026-08-07.md`。
- 權威計畫：[mod-library-catalog.md](workflows/plans/mod-library-catalog.md)。

### 韓文站採集

- **B1/B2/B3 皆已完成**（2026-08-07）。B1：`candidates` schema + `ingest_candidates.py` / `check_links.py` / `build_gallery.py` 落地，`rejected` 保險栓用暫存 DB fixture 驗證。B2/B3：兩批候選落地——`korean-public-2026-08-07-b2` 6 筆（連結 6/6 live），`korean-policy-porting-2026-08-07-b2b` 3 筆 live pending；圖庫在 `~/notes/projects/modding/skyrim/docs/candidates-gallery.html`。全程未下載任何 mod 本體。
- **採集方式已改變，別再照原計畫派 agy**：`agy` CLI 三次批次嘗試全部在 print mode timeout、零產出（前兩次疑因掛了大型 `~/skyrim_mods` workspace，第三次不掛仍超時）。改由 codex 以 deterministic `curl`/Python 從公開 Tistory 頁建 fixture。另：`arca.live/b/tullius` 匿名 `curl` 會撞 hCaptcha，不能作為「機器抓到原物」的通過條件。
- **唯一剩餘 open：地圖 porting 類候選回饋到 [port-source-survey](analysis/port-source-survey/README.md)**。b2b 那 3 筆正是此類（BDO Arethel/Heled、Dark Souls 3 Silver Knight、Bloodborne Lantern），且與該調查的結論有直接張力，見其「待辦」段。
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
  - **根因二：`ConnectCollision` 被當成實心碰撞搬進來**（DS 的地圖切換觸發體，在 DS 裡不可見）→ 與根因一無關。**但「按 MSB part 型別整類排除」這個修法目前是有爭議的，先別動手**（2026-08-11 稽核發現）：P1 findings（`e0c1f7f`，2026-08-03）主張型別判準，而後來的 P2 實作（`1d65760`，2026-08-06）在 `tools/p1_batch.py` `msb_collision_models()` docstring 記下相反發現——`h0054B1` 與 `h0099B1` **各自同時**被註冊成 `Collision` 與 `ConnectCollision`，且 `h0054B1` 那 144 顆 hull **多數是真地板**，故型別分不開、改用距離。晚的證據在程式碼那邊；照舊文件整類排除會砍掉 144 顆地板。**待驗證**：dump MSB 看兩者的 part 引用與型別，需要 `extracted/msb_m18_01.json`（只在家裡那台）。細節見 [P1-INGAME-FINDINGS.md](projects/darksouls-port/p1/P1-INGAME-FINDINGS.md) 根因二。
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
