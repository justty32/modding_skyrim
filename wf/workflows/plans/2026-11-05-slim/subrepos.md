# 階段 3–5 — modpack-design、mod-library、projects/*、測試刪減、收尾

[計畫入口](README.md)｜批次對應 [deletions.csv](deletions.csv) 的 C／D／E。三個子 repo **依序**做（每個 repo 一條線、收完 commit 再開下一個），避免與階段 1／2 撞 repo。

## 3a modpack-design（952 檔／22.0 MB → 確定項後 427 檔／17.9 MB；全選加項後 221 檔／3.6 MB）

**C1 `archive/`**（523 檔／4.07 MB，含 `index.csv` 502 列）：刪整夾。入站 3 檔 6 處降純文字；`AGENTS.md` 鐵律「archive/ 不讀」改成「過時即刪」（規則 1 local 段同文）。— Sonnet

**C2 `sources/mod-want-review-2026-09-02.{md,json}`**（56 KB）：被 09-11 版取代，刪；`sources/README.md` 一列刪。— Sonnet

**C3 `content-plan/zh-layer/zh-gap-2026-09-11.{md,json}`＋`zh-layer/data/`**（13 檔／2.6 MB）：**先驗**——Opus 讀 `audit-2026-11-05/README.md` 確認 09-11 缺口表的每個 mod 都在 11-05 核實清單裡（或已不在 modlist）；是 → 刪，`zh-layer/README.md` 與 WAIT_USER 中文項改指 11-05；否 → 留，報告列差集。— Opus 判定、Sonnet 刪

**C4 `content-plan/dialogue/`**（68 隨從 ×3 檔，205 檔／11.7 MB）：**先驗**——`dialogue.json.gz` 是否可由 `projects/game-data` CLI 重抽（看 `followers/voiced-follower-overhaul/` 的產生說明）；可 → 刪 `.gz` 只留 `PROFILE.md`／`SUMMARY.json`（省約 11 MB）；不可 → 留，改列 D2 類「成品」。— Opus 判定、Sonnet 刪

**Done when**：`git ls-files archive | wc -l` → 0；`bash wf/tools/wf-lint.sh .` → broken=0、`ARCHIVE-DIR`=0；C3／C4 的判定寫在報告（含差集或重抽指令實跑一次的輸出）。

**使用者確認**：C1／C2 併決策 1；C3 決策 10；C4 決策 9。

## 3b mod-library（文件／工具層 826 檔／37 MB；成品不動）

**D1 `archive/`＋`artifacts/archive/`**（24 檔／5.0 MB）：刪。`audits/README.md` 8 處、`README.md` 2 處、`l10n` 相關 3 處改寫（多為「原路徑／現行判準見 db/README」句，整句刪）。— Sonnet

**D2 `l10n/mods-superseded/`**（101 層／555 檔／58.4 MB）：README 自述「被取代、未部署、一 byte 沒改」＝封存的另一個名字。建議刪整夾（含 `index.csv`），`l10n/README.md` 一列改成「被取代層已刪，取代關係見新層 README；git history 可取回」。注意：**pack 不縮**（464 MB `.git` 不變），刪的是工作樹與 checkout 成本。— 判定 Opus、刪 Sonnet；**決策 11**

**D3 POTC 舊版**（`IndependentSkills-1.2.1-dev`、`1.2.2-dev`、`Varinia-NativeCombat-1.2-2026-11-01`，230 檔／8.9 MB）：PoE 暫凍「不刪資料」→ 本輪**不刪**，只在 `plugins/path-of-the-companions.md` 標「解凍後清：被 1.2.3／r3 取代」。— **決策 12**

**D4 `viewer/index.html.gz`、`data.json.gz`**（1.1 MB 產出物）：`refresh.sh` 可重產 → 不進版控（`.gitignore`）；`viewer/README.md` 改一句。— Sonnet；**決策 13**

**D5 `db/cleanup_*.py`（7 支）、`ingest_candidates.py`、`review_candidates.py`**：2026-08-07 一次性清理與已停用 candidates，有對應測試 → 列入階段 4 一起決定，本階段不動。

程式 >300 行：`l10n/tools/per-layer/build_*.py` 20 支（最大 1,739 行）是各成品的一次性建層腳本、被成品 README 引用且有的被 manifest 釘住 → **不拆**（拆了成品不可重現）；`db/report_upstream_status.py`（739）、`scan_mod_library.py`（570）、`viewer/enrich_nexus.py`（564）現役有測試 → 記 refactor backlog，不在瘦身範圍。

小檔叢集：`CC-Official-CHS-Strings-EnglishSlot/Strings/` 109 檔 <1 KB 是成品字串檔 → 不動。

**Done when**：`git ls-files archive artifacts/archive | wc -l` → 0；（D2 採）`git ls-files l10n/mods-superseded | wc -l` → 0；`git check-ignore viewer/index.html.gz` → 命中；`bash wf/tools/wf-lint.sh .` → broken=0；`MANIFEST.sha256` 所在目錄零變更（`git diff --stat -- l10n/mods plugins` → 空）。

## 3c projects/*（只動我們加的文檔；上游碼不動；instance/ 排除）

**E1／E2 archive 類目錄**：ModForge 52 檔／585 KB、my_skyrim_plugin_1 10 檔／180 KB、darksouls-port 5 檔／129 KB、agent-bridge 3 檔／9 KB → 刪，各 README 一句。— Sonnet；併決策 1

**E3 model-converter 根層 10 份 md**（87 KB，無 `wf/`、無 AGENTS）：`SESSION-LOG.md` 14.6 KB → 只留 open（≤ 2 KB）；其餘 >8 KB 的 `README`（16 KB）、`PROTOCOL`（15 KB）、`PACKAGE`（13 KB）屬產品文件、暫緩專案 → 不拆。— Opus；**決策 14**

**其餘 9 個 project 的 `wf/` 骨架副本**（各 39 檔／約 138 KB；ModForge 29 檔、agent-bridge 40 檔）：保留（決策 16）。ModForge `docs/zh-TW/` 73 檔／1 MB 是產品文件 → 不動。

暫緩專案（darksouls-port、sofia-patch）與 chim：只做 E1／E2，各 AGENTS.md 首段加「暫緩（2026-11-05）」一句；整個 project 是否停用**需使用者決定**，本計畫不建議。

**Done when**：四個 repo `git ls-files | grep -c '/archive/'` → 0；model-converter `wc -c SESSION-LOG.md` ≤ 2048；各 repo 自己的 `wf-lint.sh .`（有 wf/ 者）→ broken=0；母 repo 根 `check_markdown_links.py` → OK。

## 4 測試刪減

引用另一條線的盤點 `test-audit.csv`（本場 scratchpad；280 列：留 205／待議 52／刪 16／瘦身 7；agentctl 66、model-converter 45、darksouls-port 30、ModForge 27…）。本計畫不重做盤點，只定順序：①先套「刪 16」；②「瘦身 7」照該表的 reason；③「待議 52」連同本計畫 D5（mod-library db 清理腳本）與 1c（inbox done/ 行為測試）、1d（`status/tests/fixtures/expected.html` 179 KB）一起開一頁決策單給使用者。各 repo 一條線、順序同階段 3。— Sonnet
**Done when**：每個 repo `python3 -m unittest discover -s <tools 目錄> -p 'test_*.py'` 綠；test-audit.csv 的「刪」列路徑 `git ls-files` → 0；CI `.github/workflows/docs.yml` 的指令本機實跑一次通過。

## 5 收尾

派 Opus。

1. 各 submodule 先 commit（commit 訊息以「刪除：」開頭，列批次代號）→ 母 repo 更新 pin；`tools/check_submodule_pins.py` 通過；push 依 user.md 當場確認。
2. 全庫：母 repo 根 `python3 tools/check_markdown_links.py` → OK；五個 repo `bash wf/tools/wf-lint.sh <tracked 目錄清單>` → broken=0、`ARCHIVE-DIR`=0、`STALE-SESSION`=0。
3. 文件同步：根 `README.md`、`wf/INDEX.md`、`agentctl/README.md` 目錄表、`projects/README.md` 不再提到 archive／done／logs；`plans/README.md` 本計畫移到「已結案」表一列（計畫名、結案日、最後 commit hash）。
4. 報告：`agentctl/handoffs/home-<收線日>/slim/REPORT.md` 列每批「csv 預估檔數／bytes vs 實刪」、連結降級數、使用者未勾而保留的項；`absorbed.csv` 附上。
**Done when**：上述 1–4 的指令全部通過；母 repo `git status --short` 乾淨、三處 `unpushed=0`（或 push 待確認已登記 WAIT_USER）。
