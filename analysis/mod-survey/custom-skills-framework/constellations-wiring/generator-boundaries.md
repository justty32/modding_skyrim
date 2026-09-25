# Constellations 對 ModForge 生成器的意義

← [constellations-wiring](../constellations-wiring.md)

### 6.5 更新「對 ModForge 的意義」（看過真 schema 後的修正）

§5 的結論大方向成立，看過 Constellations 後**收斂出更精準的最小產物與分工**：

**ModForge 一個「CSF 技能」generator 該 emit 的東西：**

<!-- wf-nav -->
1. **esp records（既有能力可重用）**
   - **PERK**：樹的全部節點 perk（多階鏈只在 node 填第一階）——普通 PERK record，沿用既有 perk 生成（`PerkConditionTabCount` CTD 陷阱仍適用）。
   - **GLOB**：**實證最小只需 `level` + `ratio` + `legendary` 三個 per skill**（Constellations 連 `showMenu`/`showLevelup`/`perkPoints`/`color`/`debugReload` 都沒做也照常運作——後面這些是「獨立選單群組 + console 開選單 + 自訂點數池」才需要的可選件）。GLOB 要給 editor id。
   - **KYWD**：`CustomSkillAdvance_<Id>`（掛 perk Modify-Skill-Use entry-point，控升級速度）、`CustomSkillBook_<Id>`（技能書）、可選 `CustomSkillWorkbench_<Id>`（製作台）。
   - **MGEF**（**新發現的可選件**）：若要支援「Fortify <技能>」附魔/藥水，得做一組 fortify-skill MGEF + 一份 `ActorValueData/<Mod>_AVG.toml` 把自訂技能映射到閒置原版 *SkillAdvance AV。**這條需要一個 native SKSE plugin（Constellations 自己的 `.dll`）**——ModForge 純 esp 做不到，屬「進階加值」，預設可不做。

2. **JSON 設定**
   - 若要「住進原版技能頁」（最像原生）→ 產 `SKSE/Plugins/CustomSkills/SKILLS.json`：root 帶 `version:1` + `skydome` + `skills[]`，把 20 個原版技能字串與自訂技能 `{ "$ref": "<Mod>/<Skill>.json" }` 混排；各技能樹獨立存成 `CustomSkills/<Mod>/<Skill>.json`。
   - 若只要一棵「另開選單」的獨立技能 → 產具名 `<Id>.json`（同 skill schema），靠 `OpenCustomSkillMenu` 開。
   - skill JSON 欄位：`id`/`name`(`$`-key)/`description`/`level`/`ratio`/`legendary` 指向上面 GLOB 的 `"<Mod>.esp|FormId"`、`experienceFormula`（五參數旋鈕）、`nodes[]`（`id`/`perk`/`x`/`y`/`links`，浮點佈局、無 GridX/Y）。`form` 字串 load-order 無關，與 ModForge FormId 配置天然契合。

3. **在地化**：`$`-key + `Interface/Translations/<Mod>_ENGLISH.txt`（UTF-16 LE BOM、tab 分隔）；perk 名/述另循 esp STRINGS/inline。

4. **接線腳本（可選，視野心）**
   - **訓練師**：最省事——一支 TopicInfo TIF fragment 一行 `CustomSkills.ShowTrainingMenu(id, maxLevel, trainer)` 即可（無需自寫管理 quest）。
   - **初始化**：一支 alias script（仿 `CNS_InitScript`）在 OnInit/OnPlayerLoadGame 把 `level` GLOB 設成 `iAVDSkillStart`、授予基礎 auto-perk、做版本 gate。
   - XP 推進靠 keyword（用量）+ 訓練選單（花錢），或任意腳本呼叫 `CustomSkills.AdvanceSkill(id, mag)` / `IncrementSkill(id)`（v3 API）。**這層不必再自寫 VIGILANT 那種 `zVCSF*` kill-actor 管理腳本**——v3 API 已把 advance/training/getlevel 都包好。

**一句話分工**：**純 esp + JSON（+ 幾支薄 Papyrus）就能做出一棵接進原版技能頁的完整自訂技能；只有「Fortify-技能附魔/藥水」這條需要額外的 native SKSE plugin（`ActorValueData` + fortify MGEF）。** Constellations 的價值在於它把「最簡可行（JSON + 三個 GLOB + keyword + 訓練 TIF）」和「進階加值（私有 dll + AVG + fortify MGEF）」這兩層清楚地分了開來，正好界定了 ModForge generator 的 MVP 邊界與可選擴充。
