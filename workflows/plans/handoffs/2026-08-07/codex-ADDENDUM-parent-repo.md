# 追加交接 — codex 也接手母 repo 的這三件事

**使用者 2026-08-07 明確授權。** 這份**覆蓋** `codex-COORDINATOR.md` 裡「母 repo 你唯讀取用、不要在裡面 commit」那條——就這三件事而言，你可以在 `~/repo/moddings/skyrim` 動手並 commit。其餘部分那條仍然有效（不要順手改別的）。

母 repo 是 `justty32/modding_skyrim`（public）。**不要 push，只 commit**——push 要使用者自己決定。

## 1. 把本輪的計畫與交接書 commit 進母 repo

目前未進版控的新檔：

- `workflows/plans/round-2026-08-07-catalog-and-korean.md`（本輪計畫）
- `workflows/plans/handoffs/2026-08-07/` 底下五份：`codex-A1.md`、`deepseek-A4a.md`、`agy-B2-recon.md`、`codex-A4-review.md`、`codex-COORDINATOR.md`，以及本檔

順帶更新 `SESSION-LOG.md`：mod 庫那一節的「下一步：P1.4 Nexus 在架狀態補值」要改成現況（治具已寫完、SkyUI 驗收過、A2 待跑），並新增「韓文站採集」一條。

`WAIT_USER.md` 有兩條可以動：
- **107 筆 `quarantined_at` 不一致**——使用者已決定**從 `archives` 移除**（不是改終態）。做掉之後把這條刪除。做之前先 pymongo dump，並在 `~/notes/.../docs/` 留一份被移除的 sha256 + 原檔名清單當稽核痕跡。
- 其餘幾條（darksouls-port、houseCARL、流水線 P4）**不要動**，那些本輪刻意放著。

## 2. `agent-bridge` 的 submodule 指標往前釘

已驗證：`projects/agent-bridge` 的 main 已推上 origin（`6106646`），`main...origin/main` 同步。commit `dcd385b` 當時「新 commit 沒推上 remote，現在釘上去會讓 `clone --recurse-submodules` 壞掉」的理由，**對 agent-bridge 已不成立**。

所以可以把母 repo 的 gitlink 更新到 `6106646`。

**但 `darksouls-port` 不要動**——它的新 commit 依然沒有 remote（`WAIT_USER.md` 與 README 都記著它還沒有 remote），釘上去就會壞掉。

另外 `git status` 一直顯示 ` M projects/scene-capture-bridge`,但那個 submodule 自身 worktree 是乾淨的（HEAD `9933c3c`）。**先查清楚它是 gitlink 不一致還是別的原因再決定要不要一起收**，不要盲目 `git add`。

## 3. 把本輪兩個技術發現補進計畫文件

補進 `workflows/plans/mod-library-catalog.md`（權威計畫）或本輪計畫，你判斷哪邊合適：

**(a) Nexus API 的判定欄位已釘死**（實打 SkyUI 12604 驗證）：
- `GET api.nexusmods.com/v1/games/skyrimspecialedition/mods/{id}.json`，header `apikey`
- `status='published'` + `available=True` → `live`
- 版本要另打 `/files.json`，取 `category_name='MAIN'` + `category_id=1` + `is_primary=True` 那筆。**mod header 的 `version` 會落後**——SkyUI header 是 6.9、最新 MAIN file 是 6.11
- rate limit 實測 2000/小時、20000/天，1,272 筆一小時內跑得完

**(b) 漢化包的資料模型陷阱**（deepseek 發現）：
漢化包在 Nexus 上**有自己的 mod id**，所以檔名裡解析出的 id 是漢化包本身的、不是本體的。aggregate 時它們被當成獨立 mod 建了條目，導致 `mods` 裡混著 **255 個純漢化包 stub**（`archive_ids` 為空）。比對本體時必須排除這些，否則會把漢化包配到另一個漢化包（實際發生過：`Beyond Skyrim - Bruma SE (CHT)` → `Beyond Skyrim Bruma - CNS`）。這條也要記進 `~/notes/.../docs/mongodb-schema.md`。

順帶：deepseek 從資料裡實掃出 **38 種漢化衍生標記**（清單在 `/home/lorkhan/skyrim_agent_out/deepseek/translation-pairs-summary.md`），比原計畫列的那幾個多得多，值得收進計畫。**但其中 `MCM` 與 `CLEAN` 是誤收的**，不是翻譯標記，收錄時要剔掉。

---

做完印一行 `PARENT-REPO DONE`。**再說一次:只 commit,不 push。**
