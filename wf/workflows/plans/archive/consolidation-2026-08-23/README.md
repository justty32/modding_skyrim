# plan：工作區統整與四條新線（2026-08-23）

狀態：**已於 2026-08-23 執行完成。** 本文保留當時的提案內容；實際落地結果見
[`result.md`](result.md)。

## 使用者的要求

1. 把 `~/notes/projects/modding/skyrim` 搬進 `~/repo/moddings/skyrim`。
2. 把 `~/` 底下屬於我們的東西也收進來（`~/skyrim_mods` 除外）。
3. `projects/` 下新增四條線：
   1. **本地 Skyrim 管理** —— 裝了哪些 mod、現役 profile、MO2 設定；profile repo 當 submodule。
   2. **本地 Skyrim mod 管理** —— 下載的 mod、我們做的漢化 mod、自製插件與 mod。
   3. **整合包設計** —— mod 調查、想玩的內容與對應 mod 集合的討論、規劃。
   4. **讓 AI 操控 Skyrim 的總控 repo** —— 工作流、插件、文檔、資源；使用者建議提升到頂層。

## 兩個硬約束（先講，因為它們決定整個設計）

### A. 公開性降級

| repo | 位置 | 可見性 |
|---|---|---|
| `justty32/comp_manjaro` | `~/notes` | **PRIVATE** |
| `justty32/modding_skyrim` | `~/repo/moddings/skyrim` | **PUBLIC** |
| `justty32/modpack-kr-profiles` | MO2 instance 內 | **PRIVATE** |

`~/notes/projects/modding/skyrim`（171MB）現在活在 private repo 裡。整包倒進 public 母 repo
等於把它全部公開。**所以「搬過來」不能是單純 `mv`**——必須依內容性質分流，敏感的落到
private submodule。這也正好是下面把 1、2 設為 private 的理由。

### B. profiles 的工作目錄不能有兩份

profiles repo 的實體在
`~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles`（57MB），
**MO2 執行期要直接讀它**。git submodule 需要工作目錄真的在 submodule 路徑上，
所以「掛成 `projects/instance/profiles`」與「留在 MO2 底下」天然衝突。三個選項：

| 選項 | 做法 | 代價 |
|---|---|---|
| **B1 symlink**（建議） | 實體移到 `projects/instance/profiles`，MO2 原位置改成 symlink 指過去 | Wine 走 `Z:\home\...` 能跟隨 Linux symlink，但這是動到能跑的遊戲設定，要先備份＋實機驗證一次啟動 |
| B2 二次 clone | submodule 路徑放一份唯讀鏡像，MO2 那份照舊 | 兩份會漂移，等於沒統整；MO2 每次改 profile 都要手動同步 |
| B3 不做 submodule | 只在 `projects/instance/` 寫一份 pointer 文件記 remote 與現役 commit | 最安全、零風險，但沒達成使用者「profile 當 submodule」的要求 |

**建議 B1，但排在最後做**，且做之前先 `git push` profiles 的 4 個未推 commit。

## 風險

1. **敏感內容**：從 notes 搬出的每個檔案都要先過 API key／token／個資掃描（已派 subagent 盤點）。
2. **交叉連結**：`analysis/mod-survey/` 搬走會斷母 repo 內大量相對連結（`analysis/` 共 716 個追蹤檔）。
   搬完要跑 `scripts/check_markdown_links.py` 歸零。
3. **git 歷史**：搬進新 repo 預設會失去 notes 側的 commit 歷史。要保留就得用
   `git subtree split` 或 `git filter-repo`；不保留就在新 repo 的 README 註明歷史在 comp_manjaro 哪個路徑。
4. **未推的 commit**：動手前必須清乾淨——母 repo 3 個、profiles 4 個。
5. **`external/` 只有 1 個追蹤檔**（193MB 是 gitignore 掉的 frameworks clone），搬移前別誤以為有內容。

## 前置條件（動手前必須完成）

- [ ] 母 repo 3 個未推 commit → push
- [ ] profiles repo 4 個未推 commit → push；工作目錄 2 個未提交變更 → 決定去留
- [ ] `~/notes` 的 9 個 untracked 檔 → commit + push（含本次要搬走的 3 份 log 與 CONSOLIDATION-TODO）
- [ ] 全量 tar 備份（母 repo + notes/skyrim + profiles）
- [ ] 兩份盤點報告（`INV-notes-skyrim.md`、`INV-home.md`）確認無敏感內容

## Done when

- [ ] `~/notes/projects/modding/skyrim` 清空（或只剩一份轉址 README）
- [ ] `~/` 底下該收的都收了，`~/skyrim_mods` 未被觸碰
- [ ] 四條線各自有 remote、各自可獨立 clone、可見性正確
- [ ] `check_markdown_links.py` 全綠
- [ ] 從 Steam 點 Skyrim 仍能正常啟動（B1 若採用，這是唯一的實機驗收）

---

## 本計畫的其他部分

| 檔案 | 內容 |
|---|---|
| [`design.md`](design.md) | 提議的佈局與內容分流 |
| [`inventory.md`](inventory.md) | 兩份唯讀盤點結果 |
| [`result.md`](result.md) | 執行結果與未完成項 |
