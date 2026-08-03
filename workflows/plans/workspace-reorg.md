# plan：工作區結構整理（非侵入式佈局 + ModForge 升頂層）

出計畫日期 2026-08-01。參照正規模板 `~/repo/workflows/`（kernel + flavor），採其 [non-invasive-import.md](file:///home/lorkhan/repo/workflows/non-invasive-import.md) 的非侵入式佈局。

## 現況問題

頂層有 **11 個 `.md` + 5 個資料夾**，其中 8 個 `.md` 是工作流骨架（不是這個工作區的內容），把真正的內容目錄（`analysis/` `projects/` `dist/` `external/`）淹沒了：

```
ADOPTION.md  AGENTS.md  DEV-GUIDE.md  INIT-QUESTIONS.md  MAINTENANCE.md
PRINCIPLES.md  README.md  SESSION-LOG.md  SYNC.md  WAIT_USER.md  WORKFLOWS.md
analysis/  dist/  external/  projects/  workflows/
```

另外 `projects/` 只裝 3 個專案，但其中 **ModForge 是主線**（其他兩個是 fork 與實驗 plugin），被埋在一層 `projects/` 底下不合比重。

> 缺 `CLAUDE.md`（模板 kernel 有，本工作區沒有）——順便補上。

## 目標佈局

```
skyrim/
  AGENTS.md          ← 唯一的薄路由器（頂層入口）
  CLAUDE.md          ← 新增，一句話轉址回 AGENTS.md
  README.md          ← 留頂層:這是外來 agent「找成品去部署」的入口,屬工作區內容而非工作流骨架
  wf/                ← 工作流骨架整包收進來
    WORKFLOWS.md  INDEX.md  DEV-GUIDE.md  PRINCIPLES.md
    SESSION-LOG.md  WAIT_USER.md
    ADOPTION.md  MAINTENANCE.md  SYNC.md  INIT-QUESTIONS.md
    workflows/
  ModForge/          ← 從 projects/ 提到頂層(主線自製專案)
  my_skyrim_plugin_1/← 同上(projects/ 清空後消失)
  vendor/            ← 所有外部下載來的東西集中在此
    frameworks/      ← 原 external/frameworks(Mantella、SkyrimNet、MinAI、IntelEngine)
    mods/            ← 原 external/mods
    houseCARL/       ← 他人 repo 的 fork(原 projects/houseCARL)
    skse/            ← 外部下載的開發用原始碼
    commonlibsse-ng/ ←(平放,不另設 sdk/ 子層——對齊 tome4 的 vendor/t-engine4)
  docs/              ← 原 analysis/(對齊 tome4)
  self_mods/         ← 原 dist/(對齊 tome4)
```

### 先例：`~/repo/moddings/tome4`

同一個 `~/repo/moddings/` 底下的 tome4 已經在用這套佈局，直接對齊它，不要另創一套：

```
tome4/  AGENTS.md  CLAUDE.md  README.md  docs/  self_mods/  sub_proj/  tools/  vendor/  wf/
        vendor/ = chn-mod  dlc  orig  t-engine4(引擎原始碼)  README.md
```

- **`wf/`、`vendor/` 命名與職責完全一致** —— 本計畫照抄。
- **`vendor/t-engine4` 是引擎原始碼平放在 vendor 根層** —— 印證 SKSE / CommonLibSSE-NG 也該平放，不需要 `sdk/` 中介層。
- **`vendor/README.md` 是慣例** —— 本計畫的 vendor README 照做。
- **`analysis/` → `docs/`、`dist/` → `self_mods/`**（使用者 2026-08-01 決定）：命名一併對齊 tome4。
  代價要清楚：這兩個名字目前被 `AGENTS.md`、根 `README.md`（外來 agent 靠它找成品的入口）、`analysis/` 內部大量交叉引用、以及本資料夾兩份計畫綁定，**改名的連結修正量是整個計畫裡最大的一項**（步驟 6 要一併處理，`grep -rn 'analysis/\|dist/'`）。另外 `~/notes` 側若有引用需回頭核（唯讀確認，不代改）。
- **刻意不對齊的一點**：tome4 用 `sub_proj/` 收自製專案；本工作區依使用者決定讓 ModForge 升頂層（它是主線，不是眾多小專案之一）。
- **`tools/`**：tome4 有、本工作區沒有。若日後 QA 迴圈的 `mo2ctl` / qa-client 落地（見 [ai-ingame-qa-loop](ai-ingame-qa-loop.md)），那就是它們的落點。

頂層從 16 項降到 8 項，且每一項都是「內容」或「入口」；**自製 vs 外部**在頂層一眼可分。

**四個判斷**：
- `README.md` **不搬**。模板說頂層只留 `AGENTS.md`/`CLAUDE.md`，但本工作區的 `README.md` 有獨立職責（AGENTS.md 本地規則已明載：它是 `~/notes` 側 agent 被派來找成品時的入口，必須永遠答得出「成品在哪」）——那是工作區內容，不是工作流骨架。
- **`external/` → `vendor/`**（使用者 2026-08-01 決定）：外部下載素材統一落點。原 `external/README.md` 的職責（說明「實體 97G 庫留在 `~/skyrim_mods/`，本目錄是未來新進素材的預定落點」）搬成 `vendor/README.md`，內容照舊。
- **`projects/` 消失**：houseCARL 移入 `vendor/`、ModForge 與 my_skyrim_plugin_1 升頂層後，這層分類只剩一個成員，沒有存在意義。
- **houseCARL 放 `vendor/` 但要加註**：它不是純唯讀素材——本機有兩條未進 upstream 的 Linux fix branch（見 `WAIT_USER.md`），且 `~/tools/housecarl/server/` 的 MCP 是從它 publish 出來的。在 `vendor/README.md` 標明「唯一有本地 commit 的 vendor 項目」，避免日後有人當可拋棄的下載物砍掉。

## Done when

- [ ] 上述佈局落地，頂層只剩 8 項。
- [ ] 全 repo 沒有指向舊路徑的壞連結（`projects/ModForge`、同層 `WORKFLOWS.md` 等）。
- [ ] `AGENTS.md` 的向下連結全部改指 `wf/`，且其「目錄佈局」與「本地專案規則」段落同步更新。
- [ ] ModForge 自己的 git repo 內容零改動（純目錄搬移）。

**不包含**：導入 `~/repo/workflows` 的 flavor 包（dev/knowledge）、重寫任何工作流內容、動 `~/skyrim_mods/` 或 `~/notes/`。

## 步驟

**先做**：`tar czf ~/skyrim-workspace-$(date +%F).tar.gz -C ~/repo/moddings skyrim --exclude='*/.git'` —— 這裡不是 git repo，沒有 undo。

| # | 任務 | 驗證 |
|---|---|---|
| 1 | 先把**所有**舊路徑引用抓出來存檔：`grep -rn 'projects/ModForge' ~/repo/moddings/skyrim --include='*.md'`，以及 8 個要搬的 `.md` 各自被誰引用 | 得到一份待修清單 |
| 2 | `mkdir wf`，把 8 個工作流 `.md` + `workflows/` 搬進去 | `ls` 確認頂層剩 8 項 |
| 3 | 修 `AGENTS.md` 的向下連結（`WORKFLOWS.md` → `wf/WORKFLOWS.md` 等）；新增 `CLAUDE.md` 轉址 | 逐條點過 |
| 4 | 修 `wf/` 內部指向頂層 `README.md` 的相對連結（多一層，要 `../README.md`）。`wf/` 內彼此的相對連結不受影響 | grep `](README.md)` 等 |
| 4.5 | **先盤點** SKSE / CommonLibSSE-NG 這類外部 SDK 原始碼現在散在哪(候選:`~/tools/`、各 C++ 專案的 vcpkg 快取或 submodule、`my_skyrim_plugin_1/` 與 `scene-capture-bridge/` 的依賴目錄)。**由建置系統管理的依賴(vcpkg/CMake FetchContent)不要搬**——搬了會被重新拉回來且破壞 build；只搬「人工下載、拿來讀原始碼參考」的那些 | 得到一份「該搬 vs 該留」清單 |
| 5 | `mv projects/ModForge ModForge`、`mv projects/my_skyrim_plugin_1 .`、`mv external vendor`、`mv projects/houseCARL vendor/`、`rmdir projects`；依 4.5 清單建 `vendor/sdk/` 並搬入 | ModForge 內 `git status` 乾淨；各 C++ 專案仍能 build |
| 6 | 依步驟 1 的清單改所有 `projects/ModForge` → `ModForge`：至少涵蓋 `AGENTS.md`、`README.md`、`analysis/skyrim_mods/others/modforge-relevance.md`、`analysis/skyrim_engine/answers/ai-frameworks-modforge-relevance.md`、`wf/workflows/plans/ai-ingame-qa-loop.md` | grep 歸零 |
| 7 | 檢查工作區外的引用：`~/notes/projects/modding/skyrim/`（**唯讀確認即可，不代改**，那邊歸 notes 管）、`~/.claude/` 下的 MCP/settings 是否有硬編碼路徑、ModForge 的 `scripts/*.sh` 是否假設自己在 `projects/` 底下 | 各自確認 |
| 8 | 更新 `wf/INDEX.md` 與 `AGENTS.md` 的目錄佈局描述 | 與實況一致 |

## 風險

- **步驟 7 是最容易漏的**：`~/notes` 側與 `~/.claude/` 的 MCP 註冊可能寫死 `projects/ModForge` 絕對路徑，搬完才發現工具起不來。搬移前先 grep 過。
- **ModForge `scripts/ship.sh`** 用 `$MODFORGE_SHIP_DIR`（預設 `~/skyrim_mods/mine`），與本次搬移無關，但值得順手確認沒有相對路徑假設。
- 本工作區不是 git repo，改壞了只能靠步驟 0 的 tar。
