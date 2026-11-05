# 階段 2 — 母 repo（1,121 檔／6.4 MB → 約 1,025 檔／5.3 MB）

[計畫入口](README.md)｜批次對應 [deletions.csv](deletions.csv) 的 B1–B7。只動母 repo 自己的檔（`wf/`、`wait-user/`、`analysis/`、根檔）；submodule pin 在階段 5。可與階段 1 平行。

wf-lint 現況（`bash wf/tools/wf-lint.sh wf`）：broken=0、oversize=2、biglist=9；超標與 BIGLIST 幾乎全在凍結中的 `plans/poe-skyrim-mapping/`，本輪只動其 `archive/`，其餘等解凍。

## 2a 刪封存類（B2、B4、B5、B6、B7）— Sonnet

**範圍**：`wf/user/archive/`（9 檔／37 KB）、`wf/workflows/plans/archive/`（30 檔／131 KB）、`plans/poe-skyrim-mapping/archive/`（6 檔／19 KB）、`workflows/investigation/archive/`（2 檔）、`workflows/common/archive/`（2 檔，含 `_mig.py`）、`analysis/{mod-survey/action-system,skyrim_mods,houseCARL,skyrim_engine}/archive/`（15 檔／49 KB）、`tidy/reports/` 舊三份（6 檔／32 KB）、`analysis/mod-survey/findings/.gitkeep`。合計 71 檔／270 KB。

**風險**：低。入站連結只有各 README 的「封存索引」一句（`analysis/README.md` 整段「封存」刪；`plans/README.md` 已結案表改純文字＋hash；`investigation/README.md`、`wf/user/README.md`、`tidy/README.md`「整理紀錄」、`tidy/reports/README.md` 各一句）。`analysis/mod-survey/` 三條 symlink 改成一行指標 md（內容：指向 `projects/ModForge/workflows/investigation/<檔>` 與 `projects/game-data/` 的純文字路徑），解決 README 自述「待頂層裁示」。

**Done when**：`find wf analysis wait-user -type d \( -name archive -o -name done -o -name superseded -o -name history \) | wc -l` → 0；`git ls-files -s analysis/mod-survey | awk '$1=="120000"' | wc -l` → 0；`python3 tools/check_markdown_links.py` → OK；`bash wf/tools/wf-lint.sh wf` 的 `ARCHIVE-DIR` → 0。

**使用者確認**：決策 1（規則）＋本批（一次勾）。

## 2b wf/user 產出物（B1）— Sonnet

- **範圍**：`wf/user/2026-11-04-all-classes/index.html`（587 KB）、`wf/user/2026-11-03-perk-units/index.html`（55 KB）。留 `render.py`、`review-data.json`。`.gitignore` 加 `wf/user/**/*.html`。
- **風險**：低。兩頁入口 md 的「可瀏覽」句改成「跑 `render.py` 重產；PoE 暫凍中不重產」。lesson `user-facing-pages-go-in-wf-user` 已規定 HTML 不進版控，這是補修。
- **Done when**：`git ls-files 'wf/user/**/*.html' | wc -l` → 0；`git check-ignore wf/user/2026-11-04-all-classes/index.html` → 命中；`wf/user/README.md` 表列仍指向兩頁的 md。
- **使用者確認**：決策 7。

## 2c wait-user 與 hub（B3、規則 4）— Opus

- **範圍**：刪 `wait-user/home-setup-closed.json`、`integrated-runtime-closed.json`、`later-decisions-closed.json`、`hub-notes-closed.json`（4 檔／80 KB／79 列）與 `wait-user/archive/`（15 檔／39 KB）；`WAIT_USER.md` 去掉「前次」欄與「基準」段；`wait-user/README.md` 規則段改成規則 4；`feature-runtime.md`「已完成（封存）」節刪。13 處指向 closed json／archive 的連結刪句或降純文字。
- **風險**：中——`waituser_count.py --check` 讀 hub 表的欄位，去「前次」欄前先讀 `tools/waituser/` 確認解析不依賴該欄（依賴就只清值不刪欄）。
- **Done when**：`git ls-files wait-user | grep -c 'closed.json\|archive/'` → 0；`python3 tools/waituser_count.py --check` → 通過；`grep -n '前次\|基準' WAIT_USER.md` → 0 行；content-trim 原文檢查 → 0 行 `LOST`。
- **使用者確認**：決策 8。

## 2d 根 hub 與 SESSION-LOG（規則 2／5 套用）— Opus

- `SESSION-LOG.md` 2.5 KB：刪「Durable 狀態入口」段（入口已在 AGENTS／INDEX／各線 README；是第二份索引），留「現役工作：無」＋暫凍一句連 NEXT；目標 ≤ 1.5 KB。
- `AGENTS.md` 開場段提到 `handoffs/done/<YYYY-MM>/` 與 `home-2026-10-17` 例子 → 改成「每場 `handoffs/home-<日期>/STATE.md`，到期即刪」。
- `wf/INDEX.md` 的 `agentctl/handoffs/`、`agentctl/inbox/` 兩列、`wait-user/` 列同步改字。
- **Done when**：`wc -c SESSION-LOG.md` ≤ 2048；`grep -n 'done/' AGENTS.md` → 0 行；`bash wf/tools/wf-lint.sh wf` → broken=0。

## 2e analysis 與 lessons（不刪、只校正）— Sonnet

- `analysis/` 680 檔／2.3 MB 是知識正本（NEXT-SESSION 載明）。暫緩專案的研究（`followers-patch/` 48 檔、`chim/` 4 檔、`port-source-survey/` 6 檔，皆 2026-09-25 後未動）**保留**（決策 15），只在各 README 第一行加「專案暫緩（2026-11-05），本夾凍結不更新」。
- `mod-survey/findings/systems-encounters/` 43 檔中 12 檔 <1 KB：同類 finding 檔放鬆（STRUCTURE 觸發 B），不合併。
- `wf/lessons/` 41 檔／378 KB：10-26 已做過內容精簡，本輪不動；`docs-organization.md` 與 `wf-kernel.md` 只套規則 7 的兩句。
- **Done when**：三個暫緩夾 README 首行含「暫緩」；`git diff --stat -- analysis` 只有 README 與 archive 刪除。

## 超標與小檔（本階段結論）

- workflows md >8 KB：僅 `plans/poe-skyrim-mapping/phases-core.md`（8,263 B，凍結）→ 不動。
- 文件 >300 行（非封存）：母 repo 0 檔。程式 >300 行：母 repo 0 檔（`tools/` 最大 ≤ 300）。
- 小檔叢集：`plans/poe-skyrim-mapping/combat-combinators/all-classes/audit/` 8/12 檔 <1 KB（凍結，不動）。
- 重複 blob：母 repo 2 個（忽略）。
- 故本階段沒有「拆檔」工作；「重構拆檔＋tidy」在母 repo 的實質是上面 2a–2e 的 tidy。
