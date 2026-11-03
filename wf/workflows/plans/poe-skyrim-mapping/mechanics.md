# 機制落地：C 級、B 級機制與共用系統

[README](README.md)｜[decisions](decisions.md)｜[design](design.md)｜[phases](phases.md)

使用者對評估報告（[poe-mechanics](../../../../agentctl/handoffs/home-2026-11-03/poe-mechanics/REPORT.md)）中 C 級與 B 級機制的裁示，原話是 [user-words 的原話六](user-words-2026-11-03.md)。星盤玩家也用、直接疊加在 perk 上，所以「隨從不會操作，因此價值低」不是剔除理由。

## 逐機制裁示

已抽到 [mechanic-decisions.csv](data/mechanic-decisions.csv)（11 列）。欄位：`機制`、`狀態`、`規格`。統計：要做 6、已定 2（規則型 keystone、keystone 負面效果，見 [keystones](keystones.md)）、待調查 1（技能類別）、擱置 1（施法速度）、使用者未提 1（圖騰、陷阱／地雷、Brand、詛咒，維持小加成）。

## 要做的機制與切片

- **能量護盾**（S9）：要做。池大小、充能延遲、特效先出規格，由使用者定再施工。吃傷害走 S5 的受傷管線。
- **藥瓶**（S13）：做成 buff，血量低於門檻時自動施放回復法術。門檻與冷卻先出提案。
- **投射物**（S8）：關聯到弓箭矢、弩矢、法術投射物（火球、冰錐等）。投射物速度的 stat 不做速度效果。
- **異常狀態**（S10）：點燃、感電、冰緩／冰凍、流血、中毒、DoT 倍率，記錄放 ESL。
- **三球（charge）**（S11）：耐力球、狂怒球、暴擊球、Rage 等，只當 buff，不上 HUD，最多加特效。
- **召喚物**（S12）：要做。
- **技能類別**（S7）：先調查能否對應到 Skyrim 的法術類別與投射物類別（箭矢、法術），結論餵給 S8。
- **施法速度**：擱置，等使用者提供參考 mod（登記在 WAIT_USER）。在那之前施速 rule 照舊轉成毀滅增傷＋減耗。

## 共用系統

- **新 ESL**（S4）：暫名 `PathOfTheCompanions_PoeStar.esl`，只放 POTC 自有記錄，不 master 任何整合包 mod。第一版放 CRIT、CRITDMG、STAGGER、BLOCK 四個 PERK，並預留 MGEF／SPEL 的 FormID 區段給 S8–S14。
- **carrier AV**：原五個原生候選及擴充候選被 plugin／PEX／config 占用而排除；為保零衝突意圖，採現役 AVG 2.3.6 API 3 的四個 POTC 專用 Functional AV、plugin-scoped remap 與四個磁碟係數 0 PERK。主線 immutable snapshot、空載入與 unloaded 0；POEC 只存 owned mask，失敗時四類中性、22 個普通 AV 繼續。詳見 [1.2.3 S4 調查](../../../../mod-library/plugins/Path-Of-The-Companions-IndependentSkills-1.2.3-dev-2026-11-03/research/S4-carriers.md)；不安裝新 framework、不變更每份值。
- **受傷管線 hook**（S5）：一個進傷害的 handler 鏈，第一批 keystone（Mind Over Matter、Wind Dancer 等）和護盾共用。施法扣耗 hook 給 Blood Magic、Eldritch Battery 共用。
- 使用者裁示的施工先後：先做 ESL＋受傷管線 hook，再做護盾。

## 暫代與存檔

- 每個機制上線前，[family-rules.json](data/family-rules.json) 裡對應的規則照現行份額給小加成；上線時改指新 atom，並在 [atoms.json](data/atoms.json) 加列（每份數值照 50 份校準反推，請使用者確認）。
- 能力集一變，存檔 tag 跟著換，舊存檔走 S1 的免費重置。
