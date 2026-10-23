# 回家下載／重建

## LoreRim 借用後續：只剩三題（2026-09-05 核對後縮小）

2026-09-03 已入庫 439 件／8.966 GB；原本六題，四題 09-03／09-04 已落地或裁示，剩三題還等你
（中文層拓撲 FAIL、`NO-PEX-UPSTREAM` 借用件、地形 LOD）。
內容見 [lorerim-leftovers.md](home-setup/lorerim-leftovers.md)。

## GO19 剩餘幾何：只剩兩件（2026-09-05 核對後縮小）

原文五項裡**三項已落地**（見本節末），還等你的只有幾何覆核這一段：

- **95283 The Tempest Isle（13 筆）與 136457 Pride of the Niben（38 筆）的 xEdit 幾何覆核由誰做**，
  以及**已安裝件的空間紀錄人眼覆核**。
  A＝開 xEdit 專線逐區看完（`cx-go19x2` 已把 136457 按 worldspace／grid 象限分成 ≤12 組，一區一次看得完）；
  B＝維持現況，延後所有視覺風險。
  證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-03/go19x/REPORT.md:110`／`:112`、
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-03/inst2/REPORT.md:126-127`／`:141`
  （dispatcher 依使用者「隨便」的裁示決定今天不裝、留日後 xEdit 專線）。

**已落地、不再列 open 的三項**（2026-09-05 實讀證據）：

- **71864 MCO moveset 已裝**——`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:594`
  ＝`+GO19-71864-ER-Twinblade-MCO`（啟用）；施工紀錄
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-03/inst3/REPORT.md:23`／`:74`
  （`instance/profiles` commit `34d1809`）。
- **`go19x-130252-cr.esp` 已停用**——同上 `modlist.txt:819`＝`-houseCARL - go19x-130252-cr`。
- **LOD 排程已完成**——2026-09-04 DynDOLOD 首跑成功（TexGen 1:24／DynDOLOD 35:38），
  `DynDOLOD_Output` 已裝成 mod，profiles promote 到 `ff1a09a`。證據：
  `/home/lorkhan/repo/moddings/skyrim/agentctl/logs/lod-run-2026-09-04.md`、
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-03/lod/REPORT-run.md`、
  `instance/profiles` commit `ff1a09a`。

## 現役 modlist 整合度盤點的待辦（原三件，2026-10-23 起剩兩件）

盤點結論見 [`modpack-design/content-plan/modlist-coverage-2026-09-01.md`](../modpack-design/content-plan/modlist-coverage-2026-09-01.md)
（2026-09-01 公司端離線產出，未經 xEdit 與實機驗證）。原本列三件，其中「需求／生存要不要開」
**2026-10-10 已裁示**，移到本檔末尾的已完成節；還等你的是這兩件：

<!-- wf-nav -->
1. **敵人／AI／怪物多樣性要不要補**，以及是否在開新檔前補。現役只有 AI Overhaul 一個家族，
   查無怪物池類 mod；敵人池晚加會影響已生成 encounter。**仍未裁示。**
   （2026-09-05 相關進展：`lead-lrgq` 已把 LoreRim 的 creature 102 件逐件盤完並出 `DECISION.html`，
   同日使用者裁「LoreRim 的東西全都要」371 件——那批**可能覆蓋一部分怪物池**，但不等於本題已答。
   證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-05/STATE.md:68`／`:73`、
   `/home/lorkhan/repo/moddings/skyrim/modpack-design/content-plan/lorerim/gameplay-quest/`。）
2. **查 mo2ctl 為何沒追上 profile 變動**。**2026-09-05 實讀仍然對不上**：
   `/home/lorkhan/repo/moddings/skyrim/instance/profiles/manifest.json` 的 `updated_at`＝`2026-09-03T05:20:04Z`，
   而 `instance/profiles` main 已到 `5f47044`（2026-09-05）、`modlist.txt` 啟用 1278／`plugins.txt` 啟用 851。
   原文寫的「停在 2026-08-30T09:52」已過期，但**漂移本身沒修好**。同一件事在
   `/home/lorkhan/repo/moddings/skyrim/agentctl/status/todo/06-manifest數字對不上.md` 另有一份筆記。

   **狀態（2026-09-02 晚，home 隊）**：已定位——`updated_at` 實為 2026-09-01T11:47Z；mo2ctl `cmd_enable/cmd_disable`、人工直寫與 MO2 關閉寫回都不更新 manifest，差集 605／488／181／64；修法建議（`commit_profile()` 收口／關 MO2 後 reconcile）見 [mo2ctl-drift-diagnosis.md](../agentctl/handoffs/done/2026-09/home-2026-09-02/home/mo2ctl-drift-diagnosis.md)。
   **裁示（2026-09-02 晚，引文）**：home-3 C——拆 provenance／live checkpoint，`mo2fix` 隊承接。

   **2026-09-25 22:2x 推進**：cx-wu-mo2 已把 install／uninstall／enable／disable 收口到
   `commit_profile()`（ProfileEdit 記憶體 staging＋checkpoint），新增 `reconcile`
   （預設唯讀、`--apply` 才寫、含 fail-on-drift），agent-bridge commit `3cffa0f`，122 tests 綠燈；
   現役 profile 唯讀 reconcile 差集 modlist_enabled 1946／manifest_mods 867。
   **`--apply` 待 dispatcher 持鎖時跑**，跑完這項即可結案。

另：`major-content-preflight-2026-09-01/` 的 9 件裡有 6 件其實早已安裝啟用，該批任務單與批次計畫
的框架語意需要對現況重新校正（更正段已加在 `home-batching-plan.md` 開頭）。

## 已完成（封存）

> 以下各項判定已完成／已裁示，從 open 清單移到這裡保存歷史；每項附證據絕對路徑或 commit hash。
> 前六項是 2026-09-05 逐條對照後移入，第 7 列「需求／生存要不要開」是 2026-10-23 核出使用者 2026-10-10 已裁示而移入。

已抽到 [home-setup-closed.json](home-setup-closed.json)（7 列）。

項目：原本的三級標題。

關閉日期：文中的關閉或裁示日期。

證據路徑：原文所列的證據。

內容：標題下的完整原文。

統計：7 項。

### AE DLC 授權確認與 CC 第二輪

內容已抽到 closed.json 第 2 列。
