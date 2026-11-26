# 版控：repo 佈局、remote 與 push

[lessons 索引](README.md)

## workspace-not-a-git-repo

> ~/repo/moddings/skyrim 是 git repo（2026-08-03 起），推 justty32/modding_skyrim（PUBLIC），子專案以 submodule 納入

remote＝`git@github.com:justty32/modding_skyrim.git`（**PUBLIC**）。母 repo 只裝**文字**（頂層導引、`analysis/`、`wf/`）。`.gitignore` 刻意排除他人的 clone（`external/frameworks/`、`analysis/tool-survey/repos/`：著作權＋體積，需要時照各自 README 重 clone）與 `venv/`、`__pycache__` 等本機環境。

**Why:** 母 repo 是 public，「什麼能進版控」的判準是「是不是我們的產物＋能不能公開」，不是「有沒有用」。

**How to apply:**
- **加新子專案時**：先讓它有可 clone 的 remote，再 `git submodule add <url> projects/<name>`。**submodule 只能釘已經在 remote 上的 commit**——釘到未 push 的 commit，別人 clone 會直接失敗（收尾順序見 [[submodule-push-order-and-staleness]]）。
- **敏感內容走 private submodule**：`skyrim_darksouls_port`、`skyrim_sofia_patch`、`skyrim_game_data` 是 private（DS 資產抽取器、逐字提取的對白）。public 母 repo 配 private submodule 可行，只是沒權限的人抓不到那幾個。
- 驗收：`git clone --recurse-submodules` 到暫存區實跑一次，別只看 push 成功。

## workspace-layout-and-duties

> ~/repo/moddings/skyrim 的目錄職責——2026-08-23 起分成 instance/mod-library/modpack-design/agentctl 四條線，projects/ 只放軟體；部署狀態不歸 ~/notes 管

**佈局（2026-08-23 起）**：public 母 repo 底下四條主線各是獨立 repo：

| 線 | 管什麼 | 可見性 |
|---|---|---|
| `instance/` | 本機部署狀態：MO2 instance、現役 profile `Modpack-KR`、load order、profile 稽核工具 | private |
| `mod-library/` | mod 庫：MongoDB 索引、自製繁中翻譯層、自製插件與修正 esp | **必須永遠 private** |
| `modpack-design/` | 整合包設計：六階段整包計畫、技術債、選型調查 | private（待審後可能公開） |
| `agentctl/` | 讓 AI 操控 Skyrim 的總控：工作流、agent 交接、QA harness、執行證據 | private（待審後可能公開） |

`projects/` **只放軟體開發 repo**（ModForge、agent-bridge、houseCARL 等），狀態與知識類不放這裡；`analysis/` 是引擎／SKSE 知識與 mod 技術拆解（`mod-survey/` 是技術分析不是遊玩規劃，留這裡）；`external/` 是他人框架原始碼。

**Why:** 使用者 2026-08-23 說「我發現我們的東西已經變成一整坨」；佈局按「這東西實際上是什麼」切。`mod-library` 必須 private 的理由不是隱私是散布——它的翻譯層**內含他人 mod 的完整原始 ESP 複本**（例如完整 USSEP plugin），不能進 public 母 repo。

**How to apply:**
- 部署／MO2 狀態歸 `instance/`，不歸 ~/notes。`~/notes/projects/modding/skyrim/` 只放不進版控的截圖與 MongoDB 快照，加一份轉址 README。
- 產物完成後放 `mod-library/` 對應子目錄並附 `SOURCE.md`；同步檢查根 README 的導引。
- 佈局變動必須同步更新根 README.md 與 AGENTS.md。
- `~/skyrim_mods/` 與 `~/games/skyrim-qa-baselines`（刻意的 repo 外唯讀主檔）留原地。
- 執行記錄見 `workflows/plans/consolidation-2026-08-23.md`。

相關：[[workspace-not-a-git-repo]]、[[profiles-repo-has-remote]]、[[dont-clutter-home-with-agent-output]]

## push-and-remote-actions

> push 由頂層定時統一做（家 23:00、公司 16:50）；刪 remote branch、force push、開 PR 看當次指示，別把某次的「不代勞」當成固定規則

**push（現行）**：各線、各座位只 commit 不 push；家裡每天 23:00、公司 WSL 每天 16:50 由頂層統一 push（[D25、D32](../org/decisions-2026-11b.md)）。使用者原話（2026-11-24 家、2026-11-25 公司，節錄 push 那句）：

> push就是晚上十一點統一push。

> 1.公司WSL這邊就是每天四點五十統一push。

**其他 remote 動作**：2026-08-02 同一個 session 裡使用者對 push 給過三種指示：「ModForge 那批未 push 的 commit 我之後自己 push,agent 不要代勞、也不用再問」、houseCARL 的 force-push／開 PR 選「兩件都先不做」、my_skyrim_plugin_1 收尾時說「剩下的我自己push」→ 隨即改口「不,你幫我push吧」。push 已定時統一；其餘 remote 動作仍**逐次決定**，某一次的「我自己來」不是長期政策。

**How to apply:**
- 做到 **local commit**（commit 到主分支是慣例），回報寫「ahead N，未 push」。
- 刪 remote branch／force push／開 PR **看當次指示**；沒有指示就備好指令、用一句話問。
- 刪分支這種不可逆的，**先確保救援資訊已經在 remote 上**（例：my_skyrim_plugin_1 先 push 記錄各分支 SHA 的 `BRANCHES.md`，才 `git push origin --delete`）。
- 母 repo 設了 `push.recurseSubmodules=on-demand` 與 `submodule.recurse=true` 時，推母 repo 會連帶推有變動的子 repo；只想推特定 repo 就先確認這兩個 config，必要時 `--recurse-submodules=no`（`agentctl/handoffs/done/2026-09-01/hwrap-2026-09-01/REPORT.md`）。

公開 repo 歷史裡有敏感資訊（例：houseCARL fork 的作者信箱）時，優先選不改歷史的防再發（hook）：改作者 force push、搬私有 repo 都會斷下游 gitlink／clone，GitHub object network 仍留 SHA；除非使用者明確接受下游斷鏈（`agentctl/handoffs/home-2026-10-17/improve/cleanup/HOUSECARL-REBASE-BRIEF.md`）。

相關：[[workspace-not-a-git-repo]]

## profiles-repo-has-remote

> MO2 profiles repo 自 2026-08-22 起有 private remote，收工檢查要多看 unpushed

MO2 profiles repo 的 remote：**`justty32/modpack-kr-profiles`（private）**（2026-08-22 起）；有 tag `pre-single-profile-20260820`。

**Why**：沒推上 remote 的 profile commit 只有本機副本，磁碟壞掉等於全部消失。

**How to apply**：收工**不能只看 working tree 乾淨**，還要 `git log --oneline origin/main..main | wc -l` 應為 0。`feat/*` 分支不 promote 也要推上去才有救援價值（見 [[push-and-remote-actions]]）。

**位置（2026-08-23 起）**：profiles 的**實體工作目錄在 `~/repo/moddings/skyrim/instance/profiles`**，掛成 `instance` repo 的 submodule；MO2 那邊的 `.../modorganizer2/profiles` 是指過去的 **symlink**（submodule 要求工作目錄在 submodule 路徑上，只能這樣兩邊兼顧）。還原方式寫在 `instance/README.md`。repo 根只放真 profile，工具／測試／文件／baseline 在隱藏的 `.repo/`（見 [[mo2-phantom-profile-workflows-dir]]）。

## gitlink-is-a-commit-not-a-branch

> 別在文件裡寫「某個 submodule 釘在某條分支上」；gitlink 指的是 commit，寫成分支會讓人拿錯東西對帳

2026-08-26 使用者看到 `AGENTS.md` 寫「houseCARL 釘在 `justty32/houseCARL` 的 `fix/dialogue-encoding-lint`」，指示刪掉，理由是「pin 這個概念不應該存在」。

**Why:** gitlink 記的是 **commit** 不是分支；寫成「釘在分支 X」，讀的人就會去對分支 X 而不是那個 commit。

**How to apply:** 文件描述 submodule 關係時寫真正的規則（例：「只維護自有 fork、不追 upstream」），不寫「釘在哪條分支」；要講具體狀態就給 commit hash，並說明它從哪些遠端 ref 可達（那才是會不會變孤兒的判準）。只管**文件寫法**，不必清洗既有的 `chore: 推進 pin` 這類 commit 訊息——見 [[dont-inflate-light-preferences]]。

消費方的 pin gate 也吃 commit（darksouls-port `verify_converter()` 要求 model-converter `HEAD`＝`converter-pin.json`，只改文件也判 mismatch）：改被別 repo 以 commit 釘選的 repo 前先查消費方 pin 檔；純文件改動放獨立分支，等要重釘 pin 時再合進 main（`agentctl/handoffs/home-2026-10-17/patrol/p5-dsport-converter-godot/REPORT.md`）。

相關：[[workspace-layout-and-duties]]、[[verify-waituser-against-logs]]、[[submodule-push-order-and-staleness]]
