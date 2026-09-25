# CSF 定位與兩代設定格式

← [concept-architecture](../concept-architecture.md)

## 1. CSF 是什麼

CSF 是一個 **SKSE plugin（`CustomSkills.dll`）+ Papyrus API（`CustomSkills.psc`）** 的框架。它解決的問題是：原版 Skyrim 只有 18 個固定技能（外加 Vampire / Werewolf 兩棵 Beast perk 樹），mod 作者想做「全新的技能與 perk 樹」（例如「斯坦達爾的警戒者」這種職業技能）時，原本沒有原生的選單與升級機制。

CSF 提供的是 **選單層 + 經驗值層**：
- 重用原版的「skill perk tree」UI（星座背景 skydome + perk 節點網格），渲染一棵作者自訂的 perk 樹。
- 提供 XP / 升級 / 升級訊息 / legendary 重置 / 自訂 perk point 池等機制。
- perk 本身**仍然是 esp 裡正常的 PERK record**——CSF 不發明新的 perk 格式，它只負責「把這些 perk 排成一棵樹、給它一個技能名、追蹤等級、開選單」。

換句話說：**perk 的效果由 esp 決定，技能的「外觀與進度」由 CSF 設定檔決定。**

### 關鍵架構斷層：兩代設定格式（很重要）

調查中最重要的發現：**CSF 有兩種完全不同的設定檔格式，分屬不同世代**，而題目給的 VIGILANT/GLENMORIL 封存屬於**舊格式**：

| 世代 | 後端 | 設定檔位置與格式 | API version |
|------|------|------------------|-------------|
| **舊（v1.x）** | NetScriptFramework | `Data/NetScriptFramework/Plugins/CustomSkill.<Id>.config.txt`，INI 風格 key=value | — |
| **新（v2.x / v3.x）** | 原生 SKSE plugin (`CustomSkills.dll`) | `Data/SKSE/Plugins/CustomSkills/<X>.json`，JSON | 2（v2.0.2）/ 3（v3.1.0） |

- 本機解壓的 **VIGILANT v200 / v20a、GLENMORIL v200** 三個技能樹，shipped 的設定都是 `NetScriptFramework/Plugins/CustomSkill.VigPious.config.txt`（VIGILANT）、`CustomSkill.GLHunter.config.txt`（GLENMORIL）——**舊 INI 格式**，需要 NetScriptFramework runtime。它們尚未被移植到 JSON。
- 框架封存 `Custom Skills Framework-41780-*` 三個版本（v2.0.2 SE、v2.0.2 for 1.5.97、v3.1.0）shipped 的只有 `CustomSkills.dll` + `CustomSkills*.psc/pex` + console YAML，**完全沒有 JSON 範例**——JSON 設定由各技能樹 mod 自帶。
- JSON 格式的權威定義在 wiki 與 `docs/schema/*.json`（見下節）。兩代的**欄位語意幾乎一一對應**（INI 的 `LevelFile/LevelId` ↔ JSON 的 `level: "File.esp|FormId"`），只是序列化形式不同。

> 對 ModForge 的意義：要生成「現代 CSF」設定，目標是 **JSON 格式（v2/v3）**；舊 INI 只作為理解語意的對照與既有 mod 的相容性參考。

---

