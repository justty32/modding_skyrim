# 案例研究（VIGILANT / GLENMORIL）+ 對 ModForge 相關性

← [custom-skills-framework](README.md)

## 3. 案例研究：VIGILANT 技能樹

「Vigilant of Stendarr」——專為 VIGILANT 任務 mod 設計的職業技能：學習對抗 Undead / Vampire / Ghost / Daedra。

- 技能 id：**`VigPious`**（設定檔 `CustomSkill.VigPious.config.txt`）。
- esp：`Perk-Vigilant.esp`（93 KB，小，安全）。
- skydome：`Interface/VIGILANT/intVigilantskydome.nif`（自帶，Stendarr 星座貼圖）。
- Globals（皆在 `Perk-Vigilant.esp`）：Level `0xD64`、Ratio `0xD63`、ShowLevelup `0xD62`、ShowMenu `0xD61`、PerkPoints `0x877`、Legendary `0x878`。
- 支援腳本：`zVCSFSkillManagerQuestScript`、`zVCSFTriggerOpenMenuScript`、`zVCSFVigilantPerkMenuOpenScript`、`zVCSFMgePerkPointScript`、`zVCSFKillActorQuestScript`（用一個 quest 管理升級、靠擊殺特定敵人推進技能、玩家觸發開選單）。

**Perk 樹**（21 節點，Node0 為隱形 root，Node1 為入口）。每節點 `PerkFile`+`PerkId`+`X`/`Y`（浮點佈局）+`GridX`/`GridY`（網格分欄）+`Links`：

記錄 VIGILANT 技能樹各節點的 Perk、FormId 與作用。

已抽到 [cases-relevance-vigilant-perks.json](cases-relevance-vigilant-perks.json)（20 列）。

#：節點編號。

Perk 名 (EDID)：Perk 名稱與 EDID。

FormId：本地 FormId。

作用（取自 esp 描述）：原 esp 描述的作用。

統計：20 筆記錄，4 欄。

樹形拓撲（`Links`）：Node1 → {2,6,10,14}（四條支線：A 攻擊/B 抗性/C 信仰/D 守衛），各支線往下分岔，末端匯入 Blood of ANU/PADOMAY 等高階節點。多階 perk 在 esp 內以 02/03/04/05 後綴的 PERK record 鏈接（樹只放 01 起點）。

翻譯：EN 版與 ZH 版只是換 `config.txt`（技能名/述）+ 換 `Perk-Vigilant.esp`（perk 名/述為 inline CJK）。

---

## 4. 案例研究：GLENMORIL（較簡）

「Insight（洞察）」——GLENMORIL 任務 mod（Bloodborne 風）的技能：使用「園丁竊取的神秘學」與槍械（rifle/pistol/gatling）的獵人能力。

- 技能 id：**`GLHunter`**（`CustomSkill.GLHunter.config.txt`，UTF-8 編碼，與 VIGILANT 的 UCS-2 不同）。
- esp：`Perk-Glenmoril.esp`（36 KB）。skydome：`Interface/GLENMORIL/intGlenmorilskydome.nif`。
- Globals（`Perk-Glenmoril.esp`）：Level `0xD62`、ShowMenu `0xD65`、Legendary `0x862`。**注意 Ratio/ShowLevelup 標為 `_Dummy UNUSED`、PerkPoints/Color/DebugReload 為空（`""`/`0`）**——示範了「可選 global 不啟用」的最小組態。
- 支援腳本含 `zGLCSFRegainQuest`/`zGLCSFRegainEffectScript`（生命/狀態回復機制），其餘與 VIGILANT 同套（kill-actor 推進、trigger 開選單、skill-level manager）。

**Perk 樹**（20 節點 + root），縱深較深（GridY 直到 5）：Hunter(0xD68) 入口 → 分槍系（Rifle 0x817 / Pistol 0x815）→ Rule(0x820) → 分 Metamorphosis 順/逆時鐘(0x81D/0x81A)、Lake(0x822)、Pistol cost(0x825) → Impurity(0x82D) → Blood Rapture(0x830)/Beast Embrace(0x835)/Gatling(0x83A)/Gatling cost(0x83F) → Communion(0x844) → Holy Body(0x847)/Holy Grail(0x84C)/Eyes(0x851, rifle 偷襲倍率 x3/x4)/Radiance(0x854)/Apocrypha(0x859) → Guidance(0x85E)。主題圍繞槍械精通、變身、神聖/邪穢二元。

翻譯模型同 VIGILANT。

---

## 5. 對 ModForge 的相關性

**結論：ModForge 完全有能力生成一個現代（JSON）CSF 自訂技能，而且大部分所需 record 已是 ModForge 既有能力。**

一個 generated 自訂技能需要產出兩塊：

**(A) esp 端 record（ModForge 既有 perk 支援可重用）**
- PERK records：技能樹的全部 perk（含多階鏈），就是普通 PERK record——ModForge 的 perk 支援直接適用（注意 memory 裡的 `PerkConditionTabCount` CTD 陷阱仍適用）。
- GLOB（GlobalVariable）records：`level`、`ratio`、`showMenu`、`showLevelup`、可選 `legendary`、`color`、`perkPoints`、`debugReload`。這些是簡單的 GLOB record，需要 editor id（console 用）。
- KYWD（Keyword）records：可選的 `CustomSkillAdvance_<Id>`、`CustomSkillBook_<Id>`、`CustomSkillWorkbench_<Id>`，並把它們掛到對應 perk entry-point / book / workbench。
- 可選：BOOK（技能書）、COBJ/workbench、以及驅動「開選單 / 推進技能」的 quest+script（如 VIGILANT 的 `zVCSF*` 那套）；或改用 v3 的 `CustomSkills.psc` API 直接呼叫，省去自寫管理腳本。
- 資產：一個 skydome `.nif`（可重用 vanilla `DLC01/.../INTVampirePerkSkydome.nif` 當預設，免自製）。

**(B) CSF 設定檔（ModForge 需新增的「generator」）**
- 產 `Data/SKSE/Plugins/CustomSkills/<X>.json`：`version:1` + `skills:[{id,name,description,level/ratio/...指向上面 GLOB 的 "Plugin.esp|FormId",nodes:[{perk,x,y,links}]}]`。
- 因為 `form` 是 `"Plugin.esp|FormId"` 字串（load-order 無關），ModForge 只要知道自己產出的 plugin 檔名 + 各 record 的本地 FormId 就能填——**這與 ModForge 既有的 FormId 配置流程天然契合**。
- 可選 `$`-key + `Data/Interface/Translations/<Plugin>_ENGLISH.txt`（UTF-16 LE BOM、tab 分隔）做在地化。

**最小可行產物** = 「N 個 PERK + 對應 GLOB（至少 level/ratio/showMenu/showLevelup）」的 esp ＋「描述樹形佈局的 X.json」。XP/選單/升級這層由 `CustomSkills.dll` runtime 接手，perk 效果這層完全沿用 ModForge 現有 perk 生成。CSF 只是「選單 + XP 殼層」，不改變 perk 本身的生成方式。

> 若要相容**舊 INI 技能樹（VIGILANT/GLENMORIL 那代）**，則改產 `Data/NetScriptFramework/Plugins/CustomSkill.<Id>.config.txt`（UCS-2/UTF-8、`Name=`/`LevelFile`+`LevelId`/`Node<n>.PerkFile`+`PerkId`+`X`/`Y`/`GridX`/`GridY`+`Links`）。語意與 JSON 一一對應，但需 NetScriptFramework runtime——建議只在維護既有 mod 時才需要，新生成一律走 JSON。

---

