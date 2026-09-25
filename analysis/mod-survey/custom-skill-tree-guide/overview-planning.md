# Step 1：總覽 + 前置需求 + 規劃技能樹

← [custom-skill-tree-guide](README.md)

## 1. 總覽：要做出一棵技能樹，需要哪些拼圖

一棵「現代（JSON 格式）」自訂技能樹由**四到六塊**拼起來。先看全貌：

對照自訂技能樹各零件的落點、功能與必要性。

已抽到 [overview-planning-skill-components.json](overview-planning-skill-components.json)（6 列）。

#：零件代號。

零件：產物類型。

放哪：產物放置位置。

做什麼：該零件的職責。

必要性：必要或可選的程度。

統計：6 筆記錄，5 欄。

**心智模型**：`perk 的效果由 esp 決定，技能的「外觀與進度」由 CSF 設定檔（JSON）決定。** CSF 框架（`CustomSkills.dll`）只提供「選單外殼 + XP/升級引擎」——它不發明新的 perk 格式，你的 perk 就是普通的 PERK record。

最小可行產物（MVP）= **A（N 個 PERK + 3 個 GLOB + 升級 KYWD）+ B（`<X>.json`）+ C（`SKILLS.json`）+ D（init script）**。E、F 是錦上添花。

---

## 2. 前置需求

### 玩家端（執行時依賴）
- **Custom Skills Framework**（Nexus 41780）這個 SKSE plugin 必裝。它提供 `CustomSkills.dll`（runtime）與 `CustomSkills.psc`/`.pex`（Papyrus API）。
- 對應版本的 SKSE64、Address Library。

### 兩代格式：選哪一個
CSF 有**兩種完全不同的設定格式**（細節見 survey §1）：

| 世代 | 後端 | 設定檔 | 建議 |
|------|------|--------|------|
| 舊（v1.x） | NetScriptFramework | `Data/NetScriptFramework/Plugins/CustomSkill.<Id>.config.txt`（INI 風格） | **不要用**，只在維護 VIGILANT/GLENMORIL 那代舊 mod 時才碰 |
| **新（v2.x / v3.x）** | 原生 `CustomSkills.dll` | `Data/SKSE/Plugins/CustomSkills/<X>.json` | **用這個**。本指南全程走 v3 |

**強烈建議鎖定 v3**：v3 的 `CustomSkills.psc` 多了 `AdvanceSkill` / `IncrementSkill` / `ShowTrainingMenu` / `GetSkillLevel` 等便利函式（v2 只有 3 個函式），讓你**不必自寫管理 quest**。本指南假設 API version 3。

### 作者端（製作時用得到）
- **SSEEdit / xEdit** 或 **Creation Kit**：用來在 esp 裡建 PERK / GLOB / KYWD / MGEF 記錄。
- 一個文字編輯器寫 JSON（注意 `SKILLS.json` 用了 `$ref` 與 jsonc 註解風格，但出貨檔請寫成合法 JSON——範例裡的 `//` 註解是教學用，實檔要拿掉）。
- Translations 檔需存成 **UTF-16 LE + BOM、tab 分隔**。
- 若做 D（init script）/ E（訓練 TIF）：Papyrus compiler。

---

## 3. Step 1 — 規劃技能樹

動手建記錄前，先在紙上把樹畫出來。要決定的東西：

1. **技能數**：一個 mod 可以有多棵樹（Constellations 有 3 棵：HandtoHand / Athletics / Sorcery）。每棵樹是一個獨立的 `<Skill>.json`。
2. **每棵樹的 perk 節點數**：CSF 的 `nodes` 陣列**上限 127 個**。Constellations 每棵 9 個，很夠用。
3. **每個節點對應哪個 perk**：一個節點 = 一個 PERK record。**多階 perk（rank 2/3/4…）只在 node 填第一階的 FormId**，後面幾階靠 esp 裡 PERK 的 Next Perk 鏈接。
4. **節點之間的連線（links）**：哪個節點要先點才能點下一個。入口節點通常叫 `Mastery`。
5. **grid 座標 `x`/`y`**：浮點自由佈局。**注意方向反直覺：`x` 正方向朝左、`y` 正方向朝上**（survey §2.1）。渲染器自己連線，你只給座標。現代 JSON **沒有** `GridX`/`GridY`（那是舊 INI 的東西）。

### 範例小樹（本指南全程用它）

假設我們做一棵叫 **「Beast Lore（野獸學識）」** 的技能（id = `BeastLore`），5 個節點：

```
                 [Mastery]   (x=0.0, y=0.0)  入口
                  /      \
                 /        \
         [Tracking]      [Resilience]
        (x=-1.2,y=1.0)   (x=1.4,y=1.0)
            |                 |
       [Predator]        [ThickHide]
       (x=-1.8,y=2.5)    (x=2.0,y=2.5)
```

- `Mastery` → links `[ Tracking, Resilience ]`
- `Tracking` → links `[ Predator ]`
- `Resilience` → links `[ ThickHide ]`
- `Predator`、`ThickHide` 是末端，無 links。

對照真實案例：Constellations 的 `HandToHand.json` 入口 `Mastery`（x=0.4,y=0.0）分出 `UnarmedSpeed`（x=-0.3,y=0.8，往左上）與 `DamageAttack`（x=2.0,y=0.5，往右下方視覺上是左），各自再往下分支到末端。座標就是這樣憑視覺擺，框架不檢查重疊。

---

