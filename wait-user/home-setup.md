# 回家下載／重建

## LoreRim 借用後續：只剩兩題（2026-11-14 再縮小）

2026-09-03 已入庫 439 件／8.966 GB；原本六題，四題 09-03／09-04 已落地或裁示；地形 LOD 2026-11-14 裁「不跑」已移除。
剩兩題：中文層拓撲 FAIL（待回家補證）、`NO-PEX-UPSTREAM` 借用件（已裁停用，等施工）。
內容見 [lorerim-leftovers.md](home-setup/lorerim-leftovers.md)。

## 自己改 `~/.zshrc` 的 `MODFORGE_TTS_BIN`（2026-10-26 立）

`~/.zshrc` 的 `MODFORGE_TTS_BIN` 指向不存在的路徑，f5 venv 因此找不到；只有你能改 `~/.zshrc`（agent 不碰）。
來源：10-17 巡檢 #6，裁示單 `wf/user/archive/2026-10-17-patrol.md`（已刪，git 歷史可取回），登記依據見
`agentctl/handoffs/home-2026-10-26/tidyall/mother2/REPORT.md`（已刪） 待裁第 2 條。

## Paths NativeCombat r3 全員預設：已部署，待實戰選裝／治療圈／Volley 驗收（2026-11-02 立、家中更新）

使用者明確要求「直接改全員預設」後，新 r3 已完成八組 host／九個 mutation／獨立 review／真 Windows DLL 與 PE／PDB／hash，並停機部署獨立覆蓋層。fresh load 全員模式生效，六名受管角色 native enabled（五名非 Varinia）、一名特殊 role 自然拒啟及兩名非 Varinia 的 bridge 快照合法；這只證非戰鬥時點與政策路由，不證全隊實戰相容。實際層、備份／回退、profile `4857a8c` 與限制見 r3 部署驗收（已刪，取回：`git -C agentctl show 3db1b772:handoffs/home-2026-11-02/nativecombat-default-deploy/REPORT.md`）。

11-05已完成[回家準備指南](../wf/user/2026-11-05-nativecombat-r3-home-check.md)，沒有新增驗收項或實機PASS。尚待自然實戰觀察原生選裝、治療圈及 Volley 能力引導；受管隨從已預設適用，不需逐人加入名單，也不為驗收強行改角色或引戰。Wine Rules EXE 未執行通過，先前 Mono Installer 已精確停止，不當作執行通過。

本項承接原 r2 未驗能力，沒有新增一件重複待辦。Varinia r1 已由使用者確認解決、維持結案；r1／r2 原層保留作回退來源。不能把載入／native enabled 或非戰鬥快照視為三項實戰驗收。

## POTC IndependentSkills 1.2.3：回家部署與實機驗收（2026-11-03）

第一波工程 S15 離線驗證通過；Windows DLL／PE 1.2.3.0 已隔離建置，ESL 與 AVG 已裝 API 3 配置納入候選。候選已完成離線封存，尚未部署；停機、備份及部署另行授權。另承接已移除的 1.2.1 條目（2026-11-14 結案，1.2.1 不部署）留下的未驗功能：Role on/off 的普通原生 AI 與技能條件、隨從獨立身分、低血離隊、反覆存讀及 UI／中文／手把；舊投點、PATH／UNLM 與 reset 仍需核對。

1. 核對候選 DLL／PE 與 ESL／AVG 配置，依授權後的部署流程停機備份並部署。
2. 驗證已知舊 tag 免費 reset、POEC ownership 與存讀；點數和既有 PATH／UNLM 不漂移。
3. 四類增傷 MGEF 靜態已讀，其 PowerModifier 對應原版煉金；驗證隨從實際 AV 與增傷。
4. 實測護甲、抗性、回復、減耗、移速與攻速（含 CARP）是否符合 UI 有效值。
5. 驗證四類 Functional AV／PERK、AVG／ESL 缺席時安全行為及角色 unloaded 後返載。
6. 實測 SKILL 對 POTC 技能持續時間、半徑與冷卻的引擎效果。
7. 玩家入口與零 companion 路徑已補 source；實測玩家星盤與原版 perk 疊加。
8. B&B 真實 GMST 的 75／.15／0 與 Experience.ini 已讀，原校準計算已重跑但未讀取 GMST；實測傷害減免與 XP，必要時重跑校準，不預先改既定每份值。

## POTC NativeBridge1.2.4：matching build與隔離live證據（2026-11-04）

[source-only候選](../mod-library/plugins/Path-Of-The-Companions-IndependentSkills-1.2.4-dev-2026-11-04-NativeBridge/README.md)的f510來源已於11-04家中隔離建成matching Windows x64 DLL 1.2.4.0，153 source SHA、原PoE輸入及重生圖全符，見build證據（已刪，取回：`git -C agentctl show bf38e9c9e017:handoffs/home-2026-11-04/evening-recovery/native/REPORT.md`）。normal刻印能力仍關閉，未部署；公司封存包的PE NOT BUILT是原交付時點，不覆寫凍結包。不要求再帶公司raw JSON或17GB研究樹。還原入口（已刪，取回：`git -C agentctl show bf38e9c9e017:handoffs/home-2026-11-04/native-bridge/REBUILD.md`）區分Git可恢復與固定parent／SDK工具鏈。

matching工具鏈與依賴已在家中核符；本輪只編譯normal OFF，未執行DLL或Rules EXE。若要驗explicit experimental hidden probe，仍須另行確認隔離build／部署、備份與測試存檔。重點是原生施法時序／來源、marker真實例壽命與刷新、正HP傷／MP實扣、真catalog與SKSE存讀；無可見符文，不把SDK doubles PASS或PE link當實機通過。舊1.2.3 S16項保留，不以此替代。
