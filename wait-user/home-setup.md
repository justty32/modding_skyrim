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

## 現役 modlist 整合度盤點：敵人／怪物多樣性待決

盤點結論見 [`modpack-design/archive/content-plan/modlist-coverage-2026-09-01.md`](../modpack-design/archive/content-plan/modlist-coverage-2026-09-01.md)
（2026-09-01 公司端離線產出，未經 xEdit 與實機驗證；該檔 2026-10-23 已封存，連結改指封存路徑，本節尚未裁示的敵人／怪物多樣性問題不受影響）。原本列三件，其中「需求／生存要不要開」
**2026-10-10 已裁示**；manifest 帳本於 2026-10-17 退役，相關舊要求已移入 [結案紀錄](home-setup-closed.json)。仍待你決定的是：

<!-- wf-nav -->
- **敵人／AI／怪物多樣性要不要補**，以及是否在開新檔前補。現役只有 AI Overhaul 一個家族，
   查無怪物池類 mod；敵人池晚加會影響已生成 encounter。**仍未裁示。**
   （2026-09-05 相關進展：`lead-lrgq` 已把 LoreRim 的 creature 102 件逐件盤完並出 `DECISION.html`，
   同日使用者裁「LoreRim 的東西全都要」371 件——那批**可能覆蓋一部分怪物池**，但不等於本題已答。
   證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-05/STATE.md:68`／`:73`、
   `/home/lorkhan/repo/moddings/skyrim/modpack-design/content-plan/lorerim/gameplay-quest/`。）

另：`major-content-preflight-2026-09-01/` 的 9 件裡有 6 件其實早已安裝啟用，該批任務單與批次計畫
的框架語意需要對現況重新校正（更正段已加在 `home-batching-plan.md` 開頭；該檔 2026-10-23 已封存為
`modpack-design/archive/content-plan/quests-world/major-content-preflight-2026-09-01/home-batching-plan.md`，9 張任務單與 README 仍在原處）。

## 自己改 `~/.zshrc` 的 `MODFORGE_TTS_BIN`（2026-10-26 立）

`~/.zshrc` 的 `MODFORGE_TTS_BIN` 指向不存在的路徑，f5 venv 因此找不到；只有你能改 `~/.zshrc`（agent 不碰）。
來源：10-17 巡檢 #6，裁示單 [已封存](../wf/user/archive/2026-10-17-patrol.md)，登記依據見
[`agentctl/handoffs/home-2026-10-26/tidyall/mother2/REPORT.md`](../agentctl/handoffs/home-2026-10-26/tidyall/mother2/REPORT.md) 待裁第 2 條。

## Paths NativeCombat r3 全員預設：已部署，待實戰選裝／治療圈／Volley 驗收（2026-11-02 立、家中更新）

使用者明確要求「直接改全員預設」後，新 r3 已完成八組 host／九個 mutation／獨立 review／真 Windows DLL 與 PE／PDB／hash，並停機部署獨立覆蓋層。fresh load 全員模式生效，六名受管角色 native enabled（五名非 Varinia）、一名特殊 role 自然拒啟及兩名非 Varinia 的 bridge 快照合法；這只證非戰鬥時點與政策路由，不證全隊實戰相容。實際層、備份／回退、profile `4857a8c` 與限制見 [r3 部署驗收](../agentctl/handoffs/home-2026-11-02/nativecombat-default-deploy/REPORT.md)。

尚待自然實戰觀察原生選裝、治療圈及 Volley 能力引導；受管隨從已預設適用，不需逐人加入名單，也不為驗收強行改角色或引戰。Wine Rules EXE 未執行通過，先前 Mono Installer 已精確停止，不當作執行通過。

本項承接原 r2 未驗能力，沒有新增一件重複待辦。Varinia r1 已由使用者確認解決、維持結案；r1／r2 原層保留作回退來源。不能把載入／native enabled 或非戰鬥快照視為三項實戰驗收。

## POTC IndependentSkills 1.2.1：回家建 DLL／實機驗收（2026-11-03）

公司已完成 [source-only 候選](../mod-library/plugins/Path-Of-The-Companions-IndependentSkills-1.2.1-dev-2026-11-03/README.md)與固定離線驗收，沒有 matching Windows C++ 工具鏈，**未建 DLL、未部署**；現役仍為 NativeCombat r3、profiles `4857a8c`。

回家用既有固定依賴做真正 Windows build／PE／版本核對，才安排停機備份與另行部署驗收。重點是舊投點／PATH／UNLM、Role on/off 普通原生 AI 與技能條件、PoE 每級5點／免費 reset／Debug 只繞點數仍守連線、unit-v1 +1、低血離隊與反覆存讀；UI／中文／手把未驗。詳見候選 [BUILD](../mod-library/plugins/Path-Of-The-Companions-IndependentSkills-1.2.1-dev-2026-11-03/BUILD.md)。目前59整節點支持、只有2個可沿路購買，三屬性仍待設計；不當作全星盤已可玩。


## POTC IndependentSkills 1.2.3：回家部署與實機驗收（2026-11-03）

第一波工程 S15 離線驗證通過；Windows DLL／PE 1.2.3.0 已隔離建置，ESL 與 AVG 已裝 API 3 配置納入候選。候選仍在封存中，尚未部署；停機、備份及部署另行授權。保留上方 1.2.1 原待驗項。

1. 核對候選 DLL／PE 與 ESL／AVG 配置，依授權後的部署流程停機備份並部署。
2. 驗證已知舊 tag 免費 reset、POEC ownership 與存讀；點數和既有 PATH／UNLM 不漂移。
3. 四類增傷 MGEF 靜態已讀，其 PowerModifier 對應原版煉金；驗證隨從實際 AV 與增傷。
4. 實測護甲、抗性、回復、減耗、移速與攻速（含 CARP）是否符合 UI 有效值。
5. 驗證四類 Functional AV／PERK、AVG／ESL 缺席時安全行為及角色 unloaded 後返載。
6. 實測 SKILL 對 POTC 技能持續時間、半徑與冷卻的引擎效果。
7. 玩家入口與零 companion 路徑已補 source；實測玩家星盤與原版 perk 疊加。
8. B&B 真實 GMST 的 75／.15／0 與 Experience.ini 已讀，原校準計算已重跑但未讀取 GMST；實測傷害減免與 XP，必要時重跑校準，不預先改既定每份值。

## 已完成（封存）

### 四個指定 mod 安裝施工窗（2026-11-01 立）

施工及必要修正驗收完成，詳見 [部署驗證](../agentctl/handoffs/home-2026-11-01/wanted/INSTALL-QA.md)；自然遊玩驗收另列整包項。

### Chrome 裡重新打開一次 Nexus，讓 agent 能再下載（2026-10-26 立）

2026-11-01 使用者已重新登入，七檔下載及 hash 驗證完成；Kurone 待下載比對已移交 agent 續行。完整原項見 [結案資料](home-setup-closed.json)。

> 以下各項判定已完成／已裁示，從 open 清單移到這裡保存歷史；每項附證據絕對路徑或 commit hash。
> 前六項是 2026-09-05 逐條對照後移入，第 7 列「需求／生存要不要開」是 2026-10-23 核出使用者 2026-10-10 已裁示而移入。

已抽到 [home-setup-closed.json](home-setup-closed.json)（11 列）。

項目：原本的三級標題。

關閉日期：文中的關閉或裁示日期。

證據路徑：原文所列的證據。

內容：標題下的完整原文。

統計：11 項；各項關閉依據保留於資料檔，本次新增當前session中文讀回驗證。

### AE DLC 授權確認與 CC 第二輪

內容已抽到 closed.json 第 2 列。
