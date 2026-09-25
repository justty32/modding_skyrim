# 3. 對 ModForge 的參考價值（可生成 / 需新支援 / 純參考）

← [原文入口](../immersive-world-encounters-records-modforge.md)

## 3. 對 ModForge 的參考價值（可生成 / 需新支援 / 純參考）

對照 ModForge 現有能力（spec 模型在 `src/ModForge.Core/Spec.*.cs`）：

### ✅ 可生成（ModForge 今天就能做）

<!-- wf-nav -->
- **隱形 encounter quest**（無 journal 的演出容器）：`quests[].stages[]` 直接做 StartUp/中段/ShutDown 空 log stage + QF fragment——這正是 ModForge quest 模型的本命。模型在 `Spec.Dialogue.cs`。
- **Scene 三動作交織**（Dialog/Package/Timer、多 phase、`behaviorFlags=DeathEnd`）：`scenes[].phases[]` + `actions[]`（`package` ref / `timerSeconds` / 對話），`Spec.Scene.cs`。對應筆記 [scene-playidle-recipe]。
- **CTDA 反應性對白**：`dialogue[].conditions[]` 已支援 GetStage / GetIsAliasRef / HasKeyword / GetEquipped / GetIsVoiceType（皆在支援清單內），`Spec.Dialogue.cs`。對應 [conditioned-hello-one-topic-many-infos]。
- **SM node 掛原版 root**：`quests[].storyEvent`（event + keyword + conditions[]）能 additive 加掛 SMBN/SMQN 到原版 event root——IWE 的 `WEQuests` 寄生模式可直接複製。`Spec.StoryManager.cs`，對應 [story-manager-kill-recipe]、[dispatcher-magic-trigger]。
- **AI Package 用原版 template**：`packages[].travel` + 八種 template 支援，IWE 的 Travel-template 薄包裝模式 OK。`Spec.Packages.cs` / `Spec.Packages.Templates.cs`。對應 [scene-playidle-recipe] 內的 package 段。
- **LeveledNpc / LeveledItem / Outfit**：`leveledNpcs[]` / `leveledItems[]` / `outfits[]` 都會產生 record，`Spec.Items.cs`。

### ⚠️ 需新支援（IWE 的核心做法，ModForge 目前缺口）

<!-- wf-nav -->
- **【最大缺口】Quest alias 從 LeveledNpc runtime 填演員**：IWE 的「每次遭遇演員不同」完全靠這個，但 ModForge 的 alias fill 五模式（`fromEvent` / `forced` / `uniqueActor` / `createObject` / `findMatching`）**沒有 LVLN picker**——`createObject` 只能生直接 NPC ref、`findMatching` 只找已載入區域的現存 ref。要復刻 IWE 必須加一個 **alias fill = "fromLeveled (LVLN)"** 模式。優先級最高。
- **AI Package target 指到 quest alias**：IWE 的 travel marker target 是 quest alias indirection，但 ModForge `packages[].travel.place` 只能指 placed REFR/ACHR，**不能 `place: "aliasName"`**。需加 alias-indirection target。
- **SM branch/quest node 多層分流 + 權重**：ModForge 目前「一個 (root, keyword) 一條 branch」，無法做 IWE 那種 SMBN 多層分桶 + 每個 SMQN 帶不同條件/權重的「遭遇選台機」。要做 encounter generator 需擴充 SM 樹建構。
- **Scene completion conditions** ：spec 有 `completionConditions`，但 ModForge 註記為「offline-built, not yet in-game-verified」——IWE 重度依賴 phase/scene 完成條件，值得補實機驗證。

### 📖 純參考（設計範式，不一定要進 ModForge）

- **「隱形 quest」設計哲學**：encounter 不該給 journal/objective，stage 只當 fragment 狀態機——值得寫進 ModForge 的 encounter 範式文件，避免新手誤加 objective。
- **環境偵測 alias**（`myHoldImperial`/`myHoldSons` 偵測內戰歸屬）：用 alias + 條件讓遭遇隨世界狀態變化的技巧，可當未來「context-aware encounter」範例。
- **動作分工慣例**：Package=走位、Timer=節奏、Dialog=台詞——可當 ModForge scene 文件的 best-practice。
- **演員池規模感**：65 個 LVLN / 422 NPC / 31 Outfit 餵 56 個 scene——說明「內容量」才是這類 mod 的真成本，ModForge 能省的是 wiring boilerplate，不是美術/演員設計。

---

## 4. 結論：對 ModForge 路線圖的一句話

IWE 證明「**SM node（選台）→ 隱形 quest（容器）→ alias 從 LVLN 隨機填演員 → Scene 用 Package/Timer/Dialog 演出 → CTDA 對白分歧**」是路邊遭遇的標準骨架，而 ModForge **已能生成這條鏈的 70%**；唯一卡關的兩個缺口是 **alias-from-LeveledNpc fill** 與 **package/marker 的 alias-indirection target**——補上這兩個，ModForge 就能用 JSON spec 量產 IWE 式遭遇。SM 多層分流（選台機）是錦上添花的第三步。

相關既有筆記：[story-manager-kill-recipe]、[dispatcher-magic-trigger]（SM 掛載）、[scene-playidle-recipe]、[sm-quest-journal-progression]（scene/package）、[conditioned-hello-one-topic-many-infos]（CTDA 對白分歧）。
