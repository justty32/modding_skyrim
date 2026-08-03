# WAIT_USER — 等待使用者的事

只列需要使用者親自做/驗證才能繼續的 open 項。完成即移除，不留完成清單。

常見類型：

- 實機或 UI 手動驗證
- 外部帳號、權限、下載、授權
- 本機環境變數或工具安裝
- 不能由 agent 代跑的指令
- 高風險操作的確認

## Open

- **把工作區 push 到 `git@github.com:justty32/modding_skyrim.git`、子 repo 當 submodule**（2026-08-03 使用者要求，**推翻 2026-07-17「這裡不做版控」的決定**）。已查明的事實與待你定的事：
  1. **目標 repo 存在、是空的、而且是 PUBLIC。** 下面幾條都因為「public」才成為問題。
  2. **三個子 repo 沒有 remote，`git submodule add` 需要可 clone 的 URL** → `darksouls-port`、`sofia-patch`、`game-data` 必須先開 remote 才能當 submodule。而前兩個先前就評估過**應該 private**（sofia-patch 含 1464 行逐字提取的對白；darksouls-port 是 DS 資產抽取器）。public 母 repo 配 private submodule 是可行的，只是沒權限的人 clone 時抓不到那兩個。
  3. **`external/` 193M、`analysis/tool-survey/` 294M 全是他人的二進位素材/工具**（external/frameworks 193M）。推到 public repo 有著作權問題，也會撞 GitHub 檔案大小限制。建議兩者都 gitignore——它們本來就是「他人素材」而不是我們的產物。
  4. **`houseCARL` 是別人 repo 的 fork**（origin＝`Avick3110/houseCARL`），且目前 HEAD 在 `fix/dialogue-encoding-lint` 不在 main。當 submodule 要決定：指向你的 fork 還是 upstream，以及釘哪個 commit。
  5. ModForge 有 1 個 commit（`110b0fc`）未 push——照慣例等你自己推。

  我還沒動任何 `git init`。要我明天做的話，我傾向：先幫三個沒 remote 的開 private repo → gitignore `external/` 與 `analysis/tool-survey/` → 母 repo `git init` + 加 10 個 submodule → 推上去。你點頭我就照這個做。

- **houseCARL:兩條 fix branch 已 rebase 到 upstream 最新(8385fc6),probe 全 PASS,待使用者決定**(2026-07-17):
  1. 是否 force-push 更新 fork 上的 `fix/linux-loose-asset-resolution`、`fix/dialogue-encoding-lint`(fork 上仍是舊 base 版本)。
  2. 是否向 upstream `Avick3110/houseCARL` 開兩個 PR——**當初 branch 推了 fork 但 PR 從未開出**;upstream 91 個新 commit 皆未修這些 Linux 問題,修正仍有效。

