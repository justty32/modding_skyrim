# 2026-10-17 工作區結構審視——裁示單

你 10-17 說「讓 fable 看看整個專案的結構，給出建議，各子專案也都去看看」。結果：版控本身很乾淨（8.8 GB 磁碟有 7 GB 是被 ignore 的建置產物，全庫 md 連結零壞），問題集中在**入口文件落後現況**、**活狀態沒守只列 open**、**幾處硬路徑與 pin 失效**。55 條逐條依據與 21 個施工包在 [REPORT](../../agentctl/handoffs/home-2026-10-17/structure-review/REPORT.md)。

15:42–15:47 另一條 patrol 線已順手修了幾處文件數字與壞連結，報告裡有標。你 15:5x 說「都按照建議做」，裁示欄已改成實際結果（做了／留給頂層／不做＋理由）。前面「可直接做」的交給 Opus 線平行跑，不用你再看；「要你拍板」的才真的需要你讀。

## 一、要你拍板（不裁不能動）

### R1 wf/lessons 記憶搬家：完成還是封存？
09-26 把 104 條記憶搬進 `wf/lessons/` 做到一半停了：34 檔、同主題編到 -9、搬家腳本還留在文件夾、沒有任何入口連進去，SESSION-LOG 也沒記。要嘛一條線把它做完（合併去重、接進 INDEX、記憶改成指標），要嘛整包封存回到只用記憶。
裁示：**做（路線 a，已完成）**——34 檔合併成 18 檔、`_mig.py` 封存、INDEX 加路由（母 repo da44b59）；記憶 `MEMORY.md` 改成指標與 09-26 後新增的約 14 條記憶未搬，留給頂層。

### R2 根目錄的 `mods-user-want.md`／`play-notes.md`
兩個都是 0 byte 卻進了版控，README 把前者列為正式入口，COMMON 又說後者「永不 git add」。你是把它們當私人貼板（就 untrack＋ignore，README 改指 modpack-design 的消化報告），還是正式入口（保留，寫清楚用法）？
裁示：**做（已完成）**——兩檔 untrack＋ignore（母 dae66b0），README 改指 `modpack-design/sources/mod-want-review-*`（d3de02a）。

### R3 mod-library 的 580 MB esp／esm 與 71 個中間版層
433 個中文層裡約 186 個不在 modlist、71 個是 TEXT2／OBJTEXT 等中間版、9 組 Combined 與 FINAL 並存，pack 已 343 MiB。先讓線出一份「現役／停用／中間版」清單（不用裁），然後你決定：搬去 superseded、改 git-lfs、或維持；真要縮 pack 得改歷史（所有 clone 失效）。
裁示：**做（搬 superseded、不改歷史，已完成）**——清單 `mod-library/l10n/mods-status.csv`（90c5666：啟用 257／停用 23／不在 modlist 153）；97 層 45.7 MiB 搬到 `l10n/mods-superseded/`（fe2485b，逐層理由在 index.csv）；56 層沒有書面取代依據未搬；pack 343 MiB 要縮必須改歷史，留給頂層。

### R4 houseCARL fork 落後上游 3,540 個 commit
我們的 fork 停在 ~v1.8.0（08-24），上游已到 v2.0.5；本機只多 3 個修正 commit。要不要開一條線 rebase 並開上游 PR？做了要重新 publish MCP 伺服器。另外 `.gitmodules` 指的分支已過期，這個不用裁、線會直接修。
裁示：**延後（只評估）**——評估交接書 `agentctl/handoffs/home-2026-10-17/improve/cleanup/HOUSECARL-REBASE-BRIEF.md`：上游 2.0 把工具整套換名（31 個），建議從 v2.0.5 開分支手動移植兩項、不 rebase；`.gitmodules` 已改 `branch=main`（母 89bdd5f）。

### R5 磁碟回收約 7 GB（全是 ignore 的產物，刪了可重建）
darksouls-port `out/` 舊變體 ~1.2 GB、houseCARL Debug／非 linux 版 ~600 MB、my_skyrim_plugin_1 舊 build 254 MB、各 repo build／.venv；profiles 兩個退役 crash-ab 的 saves 232 MB（MO2 關了才能動）。線會先給 dry-run 清單，你確認後頂層自己跑。
裁示：**留給頂層**——dry-run 腳本 `agentctl/handoffs/home-2026-10-17/improve/cleanup/cleanup.sh`（預設只列、`--yes` 才刪），可回收 2.33 GB（含 opt-in 2.74 GB），輸出在同目錄 `dryrun-2026-10-17.txt`；頂層面板確認後自己跑。

### R6 agentctl handoffs 場次夾要不要月結搬 `done/`
09-25 之後 12 個場次夾直接堆在 handoffs 頂層、命名四種。搬會動到幾萬處路徑紀錄（建議只搬不改紀錄、留對照表）；不搬就只改 README 把「場次夾留頂層」寫成規則。
裁示：**做（已完成）**——31 夾 7,559 檔月結搬進 `agentctl/handoffs/done/<月>/`（agentctl e26335f5），對照表 `done/moves-2026-10-17.tsv`，紀錄內文不改、活連結與活工具路徑已修。

### R7 小題一起裁
my_skyrim_plugin_1 其實是 DaylightDungeon 插件——要不要改 repo 名；它 `.gitignore` 掉的 `skyrim_mod/` 仍 tracked 169 檔，留或 untrack。skyrim-voicegen 自述被取代的 `voicegen.sh` 刪不刪。sofia-patch 三份影片逐字稿（檔名含空格）留不留。agentctl 4 支久未用的工具封不封存、`esplib` 共用庫留 agentctl 還是搬。mod-library 的 SOURCE.md 只有 65/433，README 可不可以代替。
裁示：**做（不刪的部分已完成）**——my_skyrim_plugin_1 保留 `skyrim_mod/`（撤 ignore）、CLAUDE→AGENTS 路由（e877c80），改名留頂層；`voicegen.sh` 刪除 gate FAIL（測試仍引用）留頂層；sofia 逐字稿改 ASCII 檔名保留（1a13c2c），去留留頂層；agentctl 3 支孤兒封存 `tools/archive/`（b18ef5d8；`mechanical_runtime_capture` 仍在用不封）；`esplib` 留 agentctl 並寫明 `ESPLIB_PATH` 契約；SOURCE.md 政策改「README 可代替」（mod-library b83da14）。

## 二、可直接做（已分成 15 個互不重疊的包，給 Opus 平行跑）

### 修、對齊、瘦身

- **修壞掉的東西**：換臉工具的預設 staging 路徑已不存在（10-17 清理後）；modpack-design 的 WAIT_USER 留著已裁示項害每次開場誤觸發；code-map 覆蓋檢查紅燈 170 支工具沒索引、CI 也沒跑它。
- **入口文件對齊現況**：母 README 的 kernel 版本與 INDEX 重疊、agentctl handoffs README／NEXT-SESSION／SESSION-LOG、instance README 直接列出「現在裝了什麼」的三個檔、mod-library README 的 47→433、modpack-design README 的入口數、projects/README 的 my_skyrim_plugin_1 描述與「同層 clone 耦合群」說明。
- **活狀態瘦身**：母 WAIT_USER.md 超標＋敘述段移走、wait-user/ 補 README 並封存三組歷史檔；ModForge 停在 08 月的 SESSION-LOG／WAIT_USER 查證後清掉。
### 對齊骨架、可重現性、拆分

- **kernel 三載點真正對齊**：補齊兩載點缺的測試、STRUCTURE 本地段標記；wf-lint 跳過 ignored 目錄（現在對整個 repo 跑的 48 個警告全是別人 clone 的噪音）；把 wf 測試與 wf-lint 加進 CI。
- **可重現性**：darksouls-port 補 ModForge pin 與 SoulsFormatsNEXT commit；houseCARL `.gitmodules` 改指 fork/main；modpack-design 53 份 dialogue.json 壓成 gz（69.6 MB→約 10 MB，不改歷史）。
- **文件拆分**：instance tools/README 的 21 列表抽資料檔、scene-capture-bridge 45 KB README 拆 docs/、model-converter 根目錄 8 個 md 收攏、mod-library l10n/tools 115 支腳本做索引。

裁示：**整批已做**——15 包全部完成（逐包 commit 與驗收見 [施工 REPORT](../../agentctl/handoffs/home-2026-10-17/improve/REPORT.md)）。兩處與建議不同：qa 兩張 png gzip 後仍 >1 MB，改成 untrack＋ignore；CI 新加的 coverage／wf-lint 兩步在公開 CI 因拿不到私人 submodule 而條件跳過。

## 三、延後或不做

- `instance/profiles` 任何整理等 MO2 關閉後（WP-11）。
- analysis/ 已休眠但仍被 21 份文件引用——保留，只把 3 條 symlink 改成指標檔、刪掉指向 125 GB 的未追蹤 symlink（在 R-類刪除清單裡）。
- 記錄類文件裡的舊絕對路徑一律不改（moving-things 規定紀錄不竄改）。
- sofia-patch 94 份 >8 KB 的台詞／劇本、ModForge 的 CODE_MAP 大檔：是內容不是流程文件，不硬拆。
