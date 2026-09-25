# vs SPID + 對 ModForge 的參考價值 + esp vs config 策略

← [skypatcher](skypatcher.md)

## 三、SkyPatcher vs SPID 差異

SPID（Spell Perk Item Distributor）是另一個常見的「無 esp」分發工具，兩者**部分重疊、部分互補**：

本表整理「三、SkyPatcher vs SPID 差異」的逐項記錄。

已抽到 [skypatcher-modforge-and-strategy-spid-comparison.json](skypatcher-modforge-and-strategy-spid-comparison.json)（16 列）。

欄位「比較面向」：保留原表的比較面向。

欄位「SkyPatcher」：保留原表的SkyPatcher。

欄位「SPID」：保留原表的SPID。

統計：16 筆記錄，3 個欄位。


**結論**：SPID 在「把東西分發給 NPC」這件事上語法更豐富（可精確篩選等級範圍、faction rank、chance%）；SkyPatcher 在「修改 record 欄位本身」這件事上更通用（武器傷害、防具評級、種族屬性等）。**兩者可並用，無需二選一。**

---

## 四、對 ModForge 的參考價值（可生成 / 需新支援 / 純參考）

### 可生成（ModForge 現有能力涵蓋）

- **esp 方式的 record 修改**：對於 NPC、武器、防具的欄位修改，ModForge 現有 `BuildNpcs`、武器/防具 builder 已可生成 override esp——這些場景 SkyPatcher 是「替代品」而不是「必要品」。
- **FormList 操作**：ModForge 可生成 FLST record；SkyPatcher config 的 `objectsAdd/objectsRemove` 是它的替代路徑。（**推斷**：ModForge 是否有 FormList 增量 override 能力待確認。）
- **Leveled List 增刪**：同上，esp 方式可生成 LVLN/LVLI override。

### 需新支援（生成 SkyPatcher config 的新輸出管道）

- **SkyPatcher config 生成器**（整體新功能）：目前 ModForge 只輸出 `.esp`；若要支援「以 SkyPatcher config 取代 esp 相容 patch」這條路線，需要：
  1. 新增一種 output target（`SkyPatcherConfig` 或類似）
  2. 把現有 spec（NPC override、keyword 增刪、leveled list 注入）轉成對應的 ini 語法
  3. 確定輸出路徑：`Data/SKSE/Plugins/SkyPatcher/<recordType>/<mod名>/patch.ini`
  
  （**推斷**：src/ 中目前無此輸出路徑，需查 Generator 出口點才能確認工程量。）

### 純參考（了解生態，不必生成）

- **視覺替換類（copyVisualStyle / skin / setRandomVisualStyle）**：這些欄位修改的是 NPC 外貌，屬於「相容 patch / NPC 改外觀 mod」的領域，ModForge 不生成此類內容。
- **iUpdateNPC 動態更新機制**：這是 SkyPatcher runtime 特性，ModForge 不可控。

---

## 五、策略問題：esp vs SkyPatcher config

這是本次 survey 的核心問題。

### 情境分析

本表整理「情境分析」的逐項記錄。

已抽到 [skypatcher-modforge-and-strategy-output-scenarios.json](skypatcher-modforge-and-strategy-output-scenarios.json)（10 列）。

欄位「情境」：保留原表的情境。

欄位「建議產物」：保留原表的建議產物。

欄位「理由」：保留原表的理由。

統計：10 筆記錄，3 個欄位。


### ModForge 產物策略建議

**ModForge 的核心是生成「有新內容」的 esp**——新 NPC、新任務、新法術、新地點。這些 SkyPatcher 做不到，esp 仍是主力。

**但在「相容 patch」與「批量欄位調整」這個次要場景上，SkyPatcher config 是值得支援的第二輸出路徑**：

1. **短期（不改架構）**：在 ModForge spec 系統中，對「addToFormList」、「addToLeveledList」、「addKeywordToNpcs」等操作，標記為「可選擇 SkyPatcher output 輸出」。讓使用者自己寫 ini，ModForge 在 spec 文件中給出範本語法即可。

2. **中期（新增生成器）**：為 `npc_patch`、`armor_patch`、`leveled_list_inject` 等場景型 spec 新增 `output: skypatcher` 選項，Generator 輸出 ini 而非 esp。適合「相容 patch 套件」或「全 load order 掃描式調整」。

3. **不建議完全放棄 esp**：SkyPatcher 無法做新增型 record（QUST、DIAL、SCEN、NAVM、NPC_[新建]等），esp 仍是 ModForge 的核心輸出，兩者應並存。

> ⚠️ 以上「需新支援」標記和策略建議均為**推斷**（未查 ModForge src/ 的 Generator 出口實現），需一次 code pass 校正實際工程量。

---

