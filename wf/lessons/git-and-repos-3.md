# 版控、repo 佈局與文件整理（3/4）

[lessons 索引](README.md)｜同主題：[git-and-repos](git-and-repos.md)、[git-and-repos-2](git-and-repos-2.md)、[git-and-repos-4](git-and-repos-4.md)

## user-facing-pages-go-in-wf-user

> 2026-09-26 使用者裁示：給他看的東西（清單／審批／裁示單）放母 repo 頂層 wf/user/，不放 agentctl/handoffs 也盡量不進 agentctl（原 type: memory）

2026-09-26 使用者原話：「以後給我看的東西不要放在 handoffs 那邊，也盡量不要放在 agentctl 裏面。盡量往頂層 wf/ 那邊放」。當場建 `wf/user/`（README＋`YYYY-MM-DD-<主題>.md`），09-26 的 PRE-PLAY-CHECKLIST 搬進去，agentctl 原位留轉址。

**Why:** agentctl/handoffs 是 agent 間的內部交接與證據堆，他不想在裡面翻；頂層 wf/ 是他的入口。

**How to apply:** 濃縮給使用者的成品（開玩前清單、要他裁示的選項頁、驗收單）寫到 `wf/user/`，內文連回 agentctl 的 REPORT 當證據；agent 內部 REPORT／RT-QUEUE／COMMON 仍留 handoffs。要拍板的仍可同時做 Artifact（見 [[send-screenshots-to-session]]），但檔案本體在 wf/user/。與 [[archive-obsolete-and-unlink]] 的分層原則一致：給人導航的留 md。

## run-tests-in-worktree-not-main-tree

> 2026-09-18 modforge 隊在主工作樹跑 build/test，重建 dll 打掉 dsp-build 釘選的 ModForge 二進位 sha256；多隊共用 repo 時測試一律在 worktree 或隔離 clone（原 type: feedback）

2026-09-18 事故：modforge 隊在 `projects/ModForge` 主工作樹跑 `dotnet build`＋測試，產出的 dll 覆蓋了 dsp-build 隊釘選在 `0af3188` 的二進位；dsp-build 的 sha256 閘門擋下（零污染產出），之後改用隔離 clone 重釘。

**Why:** 同一 repo 的 bin/ 是共享的可變狀態；一隊的 build 就是另一隊的環境變更。

**How to apply:** 交接書寫死：任何 build／test 在 `git worktree add` 或獨立 clone 裡跑；消費二進位的一方釘 commit＋sha256 並在每次使用前驗；隊間共用 repo 時在 COMMON.md 列「誰可以動主工作樹」。相關：[[commit-explicit-paths-only]]。

## archive-obsolete-and-unlink

> 整理文件的五條原則：過時的封存並清連結；資料夾別擠太多檔（同類可放鬆）；太多 <1KB 小檔就合併；>8KB 就拆，大型同質列表抽成 .json/.csv，tools/tabledb.py 統一 CRUD；連結表>10 條才考慮、給人導航的留 md（原 type: memory）

2026-08-30 使用者定調的整理原則（五條）：

1. **過時的舊東西就封存，把指向它的連結清乾淨，當做它不存在。** 不是把連結改指到 `archive/` 路徑，而是從活文件把那條連結拿掉（留純文字或整句刪）；只有 `archive/README.md` 的索引表可以指向它。
2. **一個資料夾下不要擠太多檔案**；但若是**同類檔案**（同一種 log、同一種報告、同一系列 intake gates）這個限制可以放鬆，不必為了數字硬拆。
3. **一個資料夾下太多小檔案（<1 KB）就適當合併**成一份（例如同一天的 inbox 訊息併成一個檔、零碎的 evidence 併成一張表），內容保留、原檔消失。
4. **檔案 >8 KB 就拆**（不只 workflows/，所有活文件）。其中**條列式、每條同質性很高的大列表**（ledger、對照矩陣、候選表）不要再拆成好幾份 markdown——**抽成 `.json`／`.csv` 資料檔**，統一用母 repo `tools/tabledb.py` 做 CRUD（原本說 python/lua 腳本，同日改口：資料歸資料檔、程式只有一份通用 lib）；markdown 只留摘要與怎麼查。

**Why:** 舊文件留連結會讓後續的線把它當現役材料讀進去（modpack-design 鐵律「archive/ 不讀」就是為此）；硬按檔數拆同類檔只會多一層無意義的目錄；幾十個幾百 byte 的小檔每個都要開一次才知道內容，合併後一眼掃完；幾百列的表塞在 markdown 裡 agent 每次都得整份讀進 context，變成資料檔後只取要的那幾筆。

5. **連結表看對象**：md 裡的連結是給人點的捷徑，別為了 AI 把它拿掉。條列式連結**超過十條**才「開始考慮」轉 `.csv`／`.json`，且先判斷用途——**給人導航的**（README 路由表、目錄、派發表）留 md，走一般 8 KB 上限、超了就分層（上層只列子層入口）；**給 AI 讀的**（候選表、ledger、證據表裡的連結欄）才抽資料檔，因為連結數量會拖累 AI 判斷。

**How to apply:** 派整理線時把這五條寫進交接書；「過時」的判準是文件自述歷史／被取代／前提作廢，或它的目標 profile／批次已不存在。相關：[[wf-kernel-upstream-and-upgrade]]、[[investigate-all-then-install-once]]

**2026-08-30 晚補（第 4 條）**：抽表後的 md **不寫查詢指令、不寫工具路徑**（「怎麼查：＋三行 `python3 ../../wf/tools/tabledb.py …`」是雜訊）。理由：agent 端 kernel 已內化 `tabledb.py`，不必每檔再教；使用者端只要「看 wf 的資料檔說明」一句，不指定路徑。md 只留目的、`已抽到 [x.json](x.json)（N 列）`、欄位說明、統計。規則進 kernel v0.4.1（data-files.md＋wf-lint `QUERYCMD` 殘留檢查）。

**2026-08-30 放寬——過時或已解決的可以直接刪**：使用者原話「不用這麼嚴格，反正就是整理，
**過時或已經解決的可以清掉**」。所以工作流禁區裡那條「不刪」不是硬規則：

- **明確過時／已解決 → 直接 `git rm`**（git history 保得住，可回復，所以這不是不可逆動作）。
- **還有參考價值但非現役 → 才走 `git mv` 進 `archive/`**。
- 判準：**「這份東西以後還會有人想翻出來看嗎」**。

**我在同一輪犯的錯**：我把「指向被封存檔的連結」寫成用 `fix_moved_links.py` 改指到 `archive/`，
**跟 tidy 工作流第 1 條原則正好相反**——正確做法是**把那條連結拿掉**（改純文字或整句刪），
只有 `archive/README.md` 的索引可以連過去。`fix_moved_links.py` 只用於「搬位置但仍現役」的檔。
**教訓：派整理線之前先讀該 repo 的 `wf/workflows/tidy.md`，不要憑印象寫交接書。**
