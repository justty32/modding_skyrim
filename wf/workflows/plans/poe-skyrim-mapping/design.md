# 數值設計：預算、拆分規則與驗證

[README](README.md)｜[decisions](decisions.md)｜[mechanics](mechanics.md)｜[phases](phases.md)

依據：[poe-attrs](../../../../agentctl/handoffs/home-2026-11-03/poe-attrs/REPORT.md)（效果統計）、[poe-mechanics](../../../../agentctl/handoffs/home-2026-11-03/poe-mechanics/REPORT.md)（A／B／C 分級）、[poe-calib](../../../../agentctl/handoffs/home-2026-11-03/poe-calib/REPORT.md)（每份數值與 L50 驗證）。裁示見 [decisions](decisions.md)。

## 1. 預算模型

- 點數 `earned = 1 × 最高觀察等級`。
- 每個節點的份數依層級固定：小點與鑲嵌座 1、notable 3、keystone 5。
- 節點的每一行 stat 平分該節點的份數，每行再依規則拆到 atom 上。實際值＝份數 × 該 atom 的每份數值。每個節點的份數加總等於它的層級權重。
- **不設上限、不夾值**。速度的 30%／50%／單點 5% 只在離線設計檢查用。

[atoms.json](data/atoms.json) 共 27 列，每列一種 Skyrim 落地效果（atom）。欄位：

- `atom`：代號。
- `skyrim_target`：落地的 AV、perk entry 或介面。
- `per_share`：每份數值（整數）。
- `unit`：點、AR、百分點或 %。
- `route`：AV overlay、ESL perk＋carrier AV，或 POTC Abilities 介面。
- `calib_ref_L50`：反推每份數值用的 L50 基準，**不是 runtime 上限**；H／M／S 與回復沒有基準。
- `phase`：哪一個施工切片上線（見 [phases](phases.md)）。
- `note`：補充。

統計：AV overlay 22 種（S3）、ESL perk 4 種（S4）、POTC 技能倍率 1 種（S6）。

## 2. 拆分規則

[family-rules.json](data/family-rules.json) 共 49 條。依 `order` 比對（先把原句數字換成 `N`），第一條命中的生效。`components` 欄寫成 `atom:份額;…`，份額加總必須是 1。兩個代號：

- `DMG@`：依原句裡的詞決定增傷類別。順序是 弓／投射物 → 毀滅（法術、元素、混沌、法杖類 Wand）→ 2H（雙手、長杖）→ 1H（單手、匕首、爪、雙持、盾）→ 近戰（劍、斧、錘）→ 全物理（物理、攻擊、武器）→ 都沒命中就算全傷害。
- `ATTR@`：Str→HP 0.5＋SP 0.5；Dex→AR 0.5＋SP 0.5；Int→MP 0.7＋毀滅 0.3。一行有多個屬性時平分。

速度只出現在三條規則：閃避（AR 0.7＋攻速 0.15＋移速 0.15）、移速（移速 0.8＋SP 0.2）、攻速（攻速 0.4＋`DMG@` 0.4＋SP 回復 0.2）。

能量護盾、召喚物、藥瓶、投射物、異常、charge 的規則目前是「真機制落地前的暫代」，各自的施工切片上線時改指新 atom（見 [mechanics](mechanics.md)）。規則型 keystone 的處理見 [keystones](keystones.md)。

`grade` 欄分布（依行計）在 [grade-dist.csv](data/grade-dist.csv)。

## 3. A 類機制近似

- 暴擊率、暴擊傷害：CRIT、CRITDMG，走 ESL perk＋carrier AV。
- 回復、擊中／擊殺觸發：靜態 HealRate／MagickaRate／StaminaRate Mult，不掛事件；吸血是 HP 回復 0.6＋增傷 0.4。
- 消耗：五系減耗。法術壓制、格擋法術：魔抗。
- 格擋：BLOCK 0.6＋AR 0.4；暈眩：STAGGER。兩者都走 ESL perk。
- 武器類別：四類增傷 AV，由 `DMG@` 選類。
- 持續、範圍、冷卻、戰吼、光環：SKILL，POTC 技能的持續與半徑 ×(1+x)、冷卻 ×(1−x)。
- 曝露、穿透、轉換、額外傷害：視為增傷（`DMG@`），異常載具上線後再改。

ESL 的 perk 用 `Multiply 1+AV Mult`／`Add AV Mult` 讀 carrier AV；carrier AV 的值由 DLL 沿用 0xF100 overlay 寫入。

## 4. 驗證結果（2026-11-03，腳本實算）

- **可達性**：可購 1,993 個節點（small 1,476、notable 454、keystone 48、鑲嵌座 15）。七個起點各自都能到達全部 1,993 個，最遠 23–33 步。可達性只看圖的連線，與數值無關。
- **速度設計檢查**：全圖全買時移速 26.2%（≤30）、攻速 48.9%（≤50）；單點最大 1.2%／0.75%（≤5）。
- **L50 build**（貪婪最佳化、七起點取最佳、不夾值）：純近戰 2H 主類 +96%、純弓 +90%、純法毀滅 +116%、混合 1H＋毀滅 1H 專攻 +104%。武器類落在原版 L50 的 90–104%。50 點實際拿到 80–90 份。
- 抗性、暴擊、回復在 50 點內湊不滿基準（例如火抗最多約 30%、暴擊率約 70%），使用者接受。

逐 atom 的每份值、×50、基準、L50 最多可湊份數，以及 4 種 build 的明細，在 poe-calib 的 `data/per-share.json`、`data/builds-l50.json`。用本計畫目前的 atoms／family-rules 重跑 poe-calib 的 `poe_calib.py`，per-share 與 builds 兩表逐列相同，速度加總也相同。

重跑法：

```sh
python3 agentctl/handoffs/home-2026-11-03/poe-calib/tools/poe_calib.py <核准的 data.json> wf/workflows/plans/poe-skyrim-mapping/data <輸出目錄>
```

腳本會先核對 data.json 的 SHA `7e9f…1122`。
