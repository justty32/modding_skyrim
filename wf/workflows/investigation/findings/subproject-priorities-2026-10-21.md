# 子專案續行價值盤點 2026-10-21

本頁及資料檔保留開發前的盤點快照；使用者其後已選 DSP 與 houseCARL。最新離線成果與續接位置見 [修復與收尾記錄](../../../user/2026-10-21-offline-fixes.md)。

主推薦 **darksouls-port 的既有 P3 場景打磨**。使用者曾明確表示不滿意並要求北方不死院做完整（`projects/darksouls-port/p3/P3-PLAN.md:5–7`）；目前有尚未經實機確認的繞序修正候選，值得把已有場景做可靠。想優先玩隨從劇情則選 **Sofia Act1v2**；想修日常工具則選 **houseCARL 的 Linux 名稱解析**。

本輪只調查與記錄，不開始開發、合併、部署或大型工作。完整比較在 [15 列評估資料](subproject-priorities-2026-10-21.json)：11 個開發 repo 與 4 條主線；欄位包括價值、下一步、來源、當前 HEAD、驗證與限制。使用者摘要頁（續行建議）已於 2026-10-26 封存。

## 主推薦的可控下一步

只接續 P3 **現有地板／牆面消失點的 winding 候選修正**，先對應確切來源、工具 pin 與受測成品，再實機驗收。`dsp1003-winding@24b9feb` 仍未合入 `main@0b06fc5`，差異限於 `tools/p3_nifmat.py` 及測試；10 月 3 日的後續 A/B 已排除舊 OBND 假說，修改後資產尚未驗證（`agentctl/handoffs/done/2026-10/home-2026-10-03/dsp/REPORT-r2.md:5,11`）。

Done when: 受測包的來源 commit、converter／ModForge pin 與雜湊可核對；部署與受測產物一致；既有消失點在多個角度／距離仍可見且碰撞保留；基本敵對追擊與隨從跨格沒有退步。未通過時交付失敗證據與下一個待驗假說，不宣稱場景完成。

不能直接拿舊驗收單開跑：09-25 staging 路徑已不存在；另有 UNTESTED staging 的 486 個 NIF，不等於全部修正已驗。converter pin `cf12ae9` 與目前相同；ModForge pin `0af3188` 與目前 `d222032` 不同，重產必須控制版本。此輪 359 個離線測試通過，只證明測試範圍內契約，不能證明遊戲畫面修好。

## 兩個次選

**Sofia 是已交付內容的驗收收尾。** Act1v2 已在現役 profile 啟用，五個 ZIP 與四幕 spec 都存在；README 的「待轉 JSON」過時。Act1 v1 有對話／觸發／語音實機紀錄（`projects/ModForge/wait_todo/ingame-tests.md:24–33`）。首輪只驗 v2 女巫／Carene 分支、四段 PlayIdle 與嘴型。實讀 FUZ header：v2 共 21 檔，20 檔含 LIP；後三幕合計 101 檔沒有 LIP。先確認想玩的幕次，不把全四幕補嘴型綁成首輪門檻。

**houseCARL 有限界且當前可重現的修復題。** 10-18 查詢故障紀錄不能概括所有 API：本輪同筆 USSEP 勝出的小麥 `read_record`／`resolve`／`resolve_names=true` 均成功，但 Name 回 `å°éº¦`。相對地，`housecarl_resolve(formids=["00000F:Skyrim.esm"])` 連續兩次回 `Could not determine plugin listings path for SkyrimSE`／`LocalAppData environment variable is not set`，原版 Gold001 與原版小麥的 Name 亦 unreadable。兩種症狀未證明同根因；先固定這兩筆對照定位，不順帶追上游 v2。`ReadDisplayName`（`LoadOrderService.cs:1660`）與 `LoadOrderResolver.cs:265` 只是調查入口。部署檢查 stamp 都為 1.8.1、44 tools、exit 0，不能據此宣稱 DLL SHA 與來源相同。

## 當前工作區與失效待辦

11 個開發 repo 都 clean，各 repo 只有一個 worktree；houseCARL 在 `fix/dialogue-encoding-lint` 無 upstream，其他有 upstream 的目前分支相對本機 tracking 為 0/0。本輪沒有 fetch，未驗今日遠端狀態。agentctl `inbox/new` 為 0、最新 10-18 STATE 已收線。

instance 的既存 profile 變更保留：plugins／loadorder 刪去 39 支原已停用 plugin；1291 支啟用 plugin 的集合、順序與 HEAD 相同，modlist bytes 未變。這不證明完整 MO2 cycle 或實機驗收已過。

舊待辦不能直接排序：10-17 未 push／DLL 未部署已被晚場結案覆蓋；光柱 09-25 已人眼通過；manifest／checkpoint 在 instance 已廢止，不能再照 home-setup 的 `reconcile --apply` 派工；Godot 現已存在；Sofia 草稿狀態不能推翻已交付 ZIP。這些差異僅記錄，本輪未順手改舊文件。

## 驗證與覆蓋

本輪實跑結果：DSP 359、Sofia 9、game-data 14、voicegen 6、agent-bridge 122、ModForge focused 15、converter focused 44、Godot 真 headless 4，皆通過。DaylightDungeon packaging 13 檢查與 PRF 25 assertions 通過；scene-capture 既存 binaries 的 catalog 13／favorites 8 cases 通過，但未重建。各測試的作用與限制逐案列在資料檔，沒有把 mock 或離線綠燈當成 runtime 成功。

所有實質調查 agent 都先親讀適用的母 wf／子專案規則，再查程式。原 118 份 wf 文件中，87 份全文親讀（5,789 行），31 份歷史或個案排除；排除項另查現役入口入鏈及規則段，未發現漏掉適用本輪的規則。逐檔理由見 [閱讀覆蓋](subproject-priorities-2026-10-21-rules.json)；各線覆蓋及完成審查見 [審核資料](subproject-priorities-2026-10-21-audit.json)。獨立 reviewer 已反證舊待辦、Sofia 成熟度、DSP 候選與 houseCARL 查詢範圍，支持上述有條件排序。

記錄驗證：母 repo 47 項 unittest 通過；本輪 5 份 Markdown 的 40 個連結通過；wf-lint 的 broken／oversize／biglist 等計數皆 0；diff whitespace 通過。全工作區連結掃描另找到 1 個既有壞鏈（`agentctl/handoffs/done/2026-09/home-2026-09-20/crash2/REPORT.md:66` 指向已不存在的 `inbox/orders/cx-crash2.md`），本輪未修改該檔或順手修復。

本輪未開遊戲／MO2、未操作 DB、未安裝依賴、未改部署、未合併或 push；未驗畫面、嘴型觀感、操作手感，也未讀所有歷史記憶。推薦是下一段投資方向，並非候選修正已實機通過。
