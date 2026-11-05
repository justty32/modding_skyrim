# 階段 0 — 規則修改（先定稿再刪檔）

[計畫入口](README.md)

**範圍**：母 repo `wf/STRUCTURE.md`、`wf/workflows/tidy/README.md`、`wf/workflows/common/data-files.md`、`wf/workflows/plans/README.md`、`wf/lessons/docs-organization.md`、`wf/lessons/wf-kernel.md`、`wf/tools/wf-lint-local.sh`（新建）、`wait-user/README.md`、`wf/user/README.md`；agentctl／modpack-design／mod-library 三載點 `wf/STRUCTURE.md` 的 local 段與各自 `AGENTS.md`。預估改 14 檔、新增 1 檔、約 +6 KB／−3 KB。**派 Opus**（改條文）。**風險**：STRUCTURE「archive 規則」段是 kernel-owned，直接改會在下次 kernel 升級被三方 diff 蓋回 → 一律寫在 `<!-- local -->` 段並在 wf-kernel lesson 記「本地覆寫 archive 規則」。

```text
Done when: 下列 7 條規則都能 grep 到在指定檔；wf/tools/wf-lint-local.sh 存在且 `bash wf/tools/wf-lint.sh wf` 的 SUMMARY 多出 local 計數；
           三載點 STRUCTURE local 段同文；plans/README 現役表有本計畫一列。
```

## 規則 1：過時即刪，不建 archive/（取代「不刪、搬 archive/」）

寫在 `STRUCTURE.md`「archive 規則」之下的 `<!-- local -->` 段，條文：

過時／被取代／已結案的文件、計畫、報告、紀錄**直接 `git rm`**，不搬 `archive/`、`done/`、`superseded/`、`history/`；追溯靠 `git log --all -- <路徑>`、`git log -S '<關鍵字>'`、`git show <hash>:<路徑>`。

刪之前做兩件事：①仍被活文件引用的**結論**先吸收進該活文件（lessons／decisions／plan／README），引用改成純文字或刪句；②刪除 commit 訊息寫「刪除：<一句理由>」，讓 `git log --grep 刪除` 找得到。

唯一例外：**成品**（mod-library 的 `l10n/mods/`、`plugins/`）與**被 hash／manifest 釘住的檔**不適用本條，走各自 README 的取代規則。

既有 `archive/` 目錄在本計畫刪光後**不得再建**；`wf-lint-local.sh` 掃到 `archive/`、`done/`、`superseded/`、`history/` 目錄就報 `ARCHIVE-DIR`。

`data-files.md`「指向 archive/ 的連結一律不該存在」維持；`tidy/README` 原則 1 改字為「過時的就刪，連結當它不存在」；`plans/README`「已結案／被取代」改成「刪除時在表留一列：計畫名、結案日、最後 commit hash，表只留最近 10 列」。

理由（寫進 decisions.md 一列）：封存目錄佔了 agentctl 80% 檔數、說明自己「視為不存在」卻仍要維護索引與連結規則；git 本身就是封存。

## 規則 2：場次夾與 handoffs 保留期（`agentctl/handoffs/README.md`）

- `home-<日期>/` 保留 **30 天或最近 5 場**（取較多）；到期由收線線整夾 `git rm`。不再月結搬 `done/`；`done/`、`history/`、`superseded/` 廢除。
- 每場進版控的非 md 資料檔**合計 ≤ 2 MB**（單檔 ≤ 1 MB 政策不變）；超過放本機 `~/notes/projects/modding/skyrim/handoffs-data/<場次>/`，REPORT 記路徑。
- `STATE.md` 每場 ≤ 8 KB、只寫本場；`NEXT-SESSION.md` ≤ 4 KB、不複製前場段、精簡不留快照；`SESSION-LOG.md` ≤ 2 KB、只列 open（非 open 內容不得寫入，凍結事項一句＋連結）。
- 到期掃描用現成 `agentctl/tools/hygiene_audit.py --older-than 30 --emit-script`；`wf-lint-local.sh` 對 `handoffs/home-*` 的 mtime >30 天報 `STALE-SESSION`。

## 規則 3：inbox 與名冊（`agentctl/inbox/README.md`、`tools/agent_inbox/PROTOCOL.md`）

- 信件 ack 後在 STATE 記一行即可，信件本體刪；`done/` 廢除；`inbox_ack.sh` 預設不再併進 `done/<日>/`。
- ROSTER 收線格直接刪，不進 `roster-history.json`。

## 規則 4：等使用者與過目頁（`wait-user/README.md`、`wf/user/README.md`、`WAIT_USER.md`）

- 結案項**直接刪**，不再搬 `*-closed.json`；hub 只有計數表，去掉「前次」欄與基準敘述；`hub-notes-closed.json` 廢除。開場仍跑 `tools/waituser_count.py --check`。
- `wf/user/` 頁面用畢 30 天刪；產出 HTML **不進版控**（`.gitignore` 加 `wf/user/**/*.html`），只留產頁腳本與資料。

## 規則 5：其他只增不減的表

- `qa/reports/` 只留最近 2 批；`status/todo/` 結案即刪；`docs/line-claims.md` 只列現役、不留 history；`tidy/reports/` 只留最近 2 份；`decisions.md` 前提失效即刪列（既有）。
- 各子 repo（含 projects/*）`SESSION-LOG.md` ≤ 2 KB 只列 open。

## 規則 6：lint local hook（新建 `wf/tools/wf-lint-local.sh`）

依 wf-kernel lesson 的 local hook 契約（`bash <它> <dir> <strict>`；finding 平時 warning、`--strict` 算失敗）。檢查三項：`ARCHIVE-DIR`（規則 1）、`STALE-SESSION`（規則 2）、`HUB-OVERSIZE`（SESSION-LOG >2 KB、NEXT-SESSION >4 KB、STATE >8 KB）。三載點各放一份同內容（project-owned，升級不覆蓋）。

## 規則 7：lessons 與 kernel 註記

- `wf/lessons/docs-organization.md`「archive-obsolete-and-unlink」：把「還有參考價值 → git mv 進 archive/」改成「一律刪」，保留使用者 2026-08-30 原話。
- `wf/lessons/wf-kernel.md`：加一句「archive 規則本地覆寫為過時即刪（2026-11-05），升級時 kernel 段照抄、local 段保留」。
