# 版控、repo 佈局與文件整理（1/4）

[lessons 索引](README.md)｜同主題：[git-and-repos-2](git-and-repos-2.md)、[git-and-repos-3](git-and-repos-3.md)、[git-and-repos-4](git-and-repos-4.md)

## workspace-not-a-git-repo

> ~/repo/moddings/skyrim 現在是 git repo(2026-08-03 起),推 justty32/modding_skyrim,子專案以 submodule 納入（原 type: memory）

**2026-08-03 起 `~/repo/moddings/skyrim` 是 git repo**，remote＝`git@github.com:justty32/modding_skyrim.git`（**PUBLIC**），`projects/` 下的子專案以 **submodule** 納入。這**推翻了 2026-07-17「這個工作區不做版控」的決定**（當時已移除 .git 並把同模式套到 `~/repo/moddings/` 全部資料夾）。

母 repo 只裝**文字**（首版 2.2 MB / 753 檔）：頂層導引文檔、`analysis/`、`workflows/`、`dist/` 骨架。`.gitignore` 刻意排除三類：

- **他人的 clone**：`external/frameworks/`（193M）、`analysis/tool-survey/repos/`（294M）——著作權 + 體積，且各自帶自己的 `.git`。需要時照各自 README 重 clone。
- **`projects/houseCARL/`**：是別人 repo 的 fork 且本機 HEAD 在未推上 fork 的 rebase 分支，釘成 submodule 會讓 `clone --recurse-submodules` 壞掉（見工作區 WAIT_USER）。
- `venv/`、`__pycache__` 等本機環境。

**Why:** 使用者臨時改主意要版控（正是 [[push-and-remote-actions]] 說的那種轉向）。母 repo 是 public，所以「什麼能進版控」的判準從「有沒有用」變成「是不是我們的產物 + 能不能公開」。

**How to apply:**
- 工作區根目錄現在可以正常 `git add`/`commit`；push 仍照慣例先確認。
- **加新子專案時**：先讓它有可 clone 的 remote，再 `git submodule add <url> projects/<name>`。**submodule 只能釘已經在 remote 上的 commit**——釘到未 push 的 commit，別人 clone 會直接失敗（houseCARL 就是為此被排除）。
- **敏感內容走 private submodule**：`skyrim_darksouls_port`、`skyrim_sofia_patch`、`skyrim_game_data` 是 private（DS 資產抽取器、逐字提取的對白）。public 母 repo 配 private submodule 可行，只是沒權限的人抓不到那幾個。
- 驗收方式：`git clone --recurse-submodules` 到暫存區實跑一次，別只看 push 成功。

## workspace-layout-and-duties

> ~/repo/moddings/skyrim 的目錄職責——2026-08-23 起分成 instance/mod-library/modpack-design/agentctl 四條線，projects/ 只放軟體；部署狀態不再歸 ~/notes 管（原 type: memory）

**2026-08-23 統整後的佈局**（取代 2026-07-17 的 dist/external/notes 三分法）。
母 repo `justty32/modding_skyrim` 是 **public**，底下四條主線各是獨立 repo：

| 線 | 管什麼 | 可見性 |
|---|---|---|
| `instance/` | 本機部署狀態：MO2 instance、現役 profile `Modpack-KR`、load order、profile 稽核工具 | private |
| `mod-library/` | mod 庫：MongoDB 索引、自製繁中翻譯層、自製插件與修正 esp | **必須永遠 private** |
| `modpack-design/` | 整合包設計：六階段整包計畫、技術債、選型調查 | private（待審後可能公開） |
| `agentctl/` | 讓 AI 操控 Skyrim 的總控：工作流、agent 交接、QA harness、執行證據 | private（待審後可能公開） |

`projects/` 現在**只放軟體開發 repo**（ModForge、agent-bridge、houseCARL 等 11 個）；
狀態與知識類不放這裡。`analysis/` 仍是引擎/SKSE 知識與 mod 技術拆解（含 `mod-survey/` 136 份，
**沒有搬走**——它是框架技術分析，不是遊玩規劃）。`external/` 是他人框架原始碼落點。

**Why:** 原本的 dist/analysis/notes 分法長成一整坨，使用者說「我發現我們的東西已經變成一整坨」。
新分法按「這東西實際上是什麼」切。`mod-library` 必須 private 的理由不是隱私是散布——
它的翻譯層**內含他人 mod 的完整原始 ESP 複本**（例如 20MB 的完整 USSEP plugin），
這批東西在 2026-08-23 之前一直躺在 public 母 repo 的 `dist/` 底下。

**How to apply:**
- **「部署/MO2 狀態歸 ~/notes 管」這條已作廢** —— 現在歸 `instance/`。`~/notes/projects/modding/skyrim/`
  只剩不進版控的 66MB 截圖與 57MB MongoDB 快照，加一份轉址 README。
- 產物完成後放 `mod-library/` 對應子目錄並附 `SOURCE.md`；同步檢查根 README 的導引。
- 佈局變動必須更新根 README.md 與 AGENTS.md（兩者都有此條規則）。
- `~/skyrim_mods/`（125GB）與 `~/games/skyrim-qa-baselines`（刻意的 repo 外唯讀主檔）留原地。
- 執行記錄見 `workflows/plans/consolidation-2026-08-23.md`。

相關：[[workspace-not-a-git-repo]]、[[profiles-repo-has-remote]]、[[dont-clutter-home-with-agent-output]]

## push-and-remote-actions

> "push/刪 remote branch 的分寸——使用者會臨時改主意,做到 commit 後直接問一句或照最新指示走,不要把「不代勞」當成固定規則"（原 type: memory）

2026-08-02 同一個 session 裡使用者對 push 給過**三種**指示:先是「ModForge 那批未 push 的 commit 我之後自己 push,agent 不要代勞、也不用再問」,接著 houseCARL 的 force-push/開 PR 選「兩件都先不做」,最後在 my_skyrim_plugin_1 收尾時說「剩下的我自己push」→ 隨即改口「不,你幫我push吧」(於是 agent 推了兩個 repo 的 main/master,並刪掉五條 remote 分支)。

**Why:** 他要的是**逐次自己決定**,不是一條固定規則。把某一次的「我自己來」當成長期政策會猜錯;反過來預設代勞也會猜錯。

**How to apply:**
- 工作照常做到 **local commit**(commit 到主分支是慣例)。
- push / 刪 remote branch / 開 PR **看當次指示**;沒有指示時,在回報裡寫清楚「ahead N,未 push」並把指令備好,讓他一句話就能決定——不要長篇問句。
- 刪分支這種不可逆的,**先確保救援資訊已經在 remote 上**(例:my_skyrim_plugin_1 是先把記錄各分支 SHA 的 `BRANCHES.md` push 上去,才 `git push origin --delete`)。
- 相關:[[workspace-not-a-git-repo]]

## profiles-repo-has-remote

> MO2 profiles repo 自 2026-08-22 起有 private remote，收工檢查要多看 unpushed（原 type: project）

MO2 profiles repo（`.../modorganizer2/profiles`）2026-08-22 起有 remote：
**`justty32/modpack-kr-profiles`（private）**。當天推上 34 個 branch 與 tag
`pre-single-profile-20260820`。

**Why**：在此之前它完全沒有 remote，所有 profile commit（VIGILANT promotion、
D3/D4、上游升級、整批安裝）只有本機副本。磁碟壞掉等於全部消失。

**How to apply**：收工檢查**不能只看 working tree 乾淨**，要多一項
`git log --oneline origin/main..main | wc -l` 應為 0。feature 分支照舊停在
`feat/*` 不 promote，但也要推上去才有救援價值（見 [[push-and-remote-actions]]）。

**2026-08-23 位置變更**：profiles 的**實體工作目錄搬到
`~/repo/moddings/skyrim/instance/profiles`**，掛成 `instance` repo 的 submodule；
MO2 原位置 `.../modorganizer2/profiles` 改成指過去的 **symlink**。
git submodule 要求工作目錄真的在 submodule 路徑上，這是唯一能同時滿足兩邊的做法。
還原方式寫在 `instance/README.md`。**尚未實機驗證**——要從 Steam 啟動一次才算過。
