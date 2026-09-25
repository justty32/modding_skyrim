# supply-and-demand — modforge-roadmap

← [調查入口](../supply-and-demand.md)

## 5. ModForge relevance（逐塊對應，"做不到"必 grep 驗證）

把 S&D 拆成「scaffold」與「邏輯本體」兩半看 ModForge：

**ModForge 今天就能生成的 scaffold（已驗證有對應 spec）**：

<!-- wf-nav -->
- ✅ **GLOB**：`Spec.Globals.cs` + `Generator.Build.Globals.cs` 存在 → `tc_Global_ExtinctionRatio`/`tc_Global_HideNotifications` 兩個 GLOB 可生成。
- ✅ **MGEF / SPEL（含 Script & Cloak archetype）**：`Spec.Magic.cs`/`Generator.Build.Magic.cs` 存在。
- ✅ **script-attach 到 MGEF 的 VMAD（含 typed properties + 自帶 `.psc`）**：`Spec.Magic.cs` L59-63 有 `List<ScriptAttachSpec> Scripts`（"Inline Papyrus script attach (I組 DX)"），`ScriptAttachSpec`（`Spec.Dialogue.cs` L227）有 `ScriptName`、**`Source`（指向 `.psc`，由 `package` compile）**、`List<PropertySpec> Properties`。→ **S&D 那種「script-bearing MGEF + props」結構可表達**，且 ModForge 可把使用者自寫的 `.psc` 編譯進來（`Papyrus.cs` 有 CK-Wine 與 native 兩條編譯路徑）。
- ✅ **MCM**：`Spec.Mcm.cs`/`McmGen.cs`/`Generator.Build.Mcm.cs` 存在。**但 ModForge 走 MCM-Helper（config.json + 生成 QUST/alias，見 MEMORY recipe）**，S&D 走 hand-scripted `SKI_ConfigBase`——**不同 MCM tech**，功能上都能「ship 一個有 slider/toggle 的設定選單」。
- ✅ **vanilla CELL / 容器 ref override**：ModForge 有 worldspace/cell override 能力（見 MEMORY）。

**ModForge 生不出來的邏輯本體**：

<!-- wf-nav -->
- ❌ **動態交易偵測 + 改價邏輯本身（`OnItemAdded`/`OnItemRemoved` + `SetGoldValue` + 30-array 回歸）是 hand-authored Papyrus**。ModForge **只生成自家 fragment**（quest/scene/dialogue/perk adapter），**不會替你寫 `tc_PlayerScript` 這種 controller 的演算法**。要重製 S&D，這顆 controller 必須**人工撰寫 `.psc`**，再用 `ScriptAttachSpec.Source` 掛上去由 ModForge 編譯打包——**ModForge 是 packager，不是邏輯 author**。（這不是 bug，是設計邊界。）
- ❌ **GMST editing：確認缺席**。`grep -rilE "gamesetting|gmst" src/ModForge.Core/` → **空**（與 `trade-and-barter.md` 記的 gap 一致）。S&D **本身不需要 GMST**（它不碰 barter 公式），所以這對「重製 S&D」**不構成阻礙**；但 GMST gap 仍是 economy 類普遍缺口（見 roadmap）。
- ⚠️ **MCM toggle/slider → GLOB → runtime 的端到端連線**：S&D 正是這個 pattern（MCM 寫 GLOB，script 讀）。ModForge 是否能把生成的 MCM 選項**綁到一個生成的 GLOB**，仍 **UNVERIFIED**（與 T&B finding 同一個待確認項，需對 `Generator.Build.Mcm.cs` ↔ globals 做一次 code pass）。

**結論**：S&D 的**外殼**（GLOB+MGEF+SPEL+script-attach+MCM+cell override）ModForge **今天可生成**；S&D 的**靈魂**（動態供需 controller）**必須人工寫 Papyrus**，ModForge 負責編譯與打包。

## 6. Roadmap implications（對接 `workflows/roadmap/mod-survey-gaps.md` 的 economy 缺口）

<!-- wf-nav -->
1. **新確認 pattern：「transaction-tracking controller」是真實存在且生不出邏輯的類別。** S&D 是 survey 第一個實證——roadmap 該把它記成「ModForge 提供 **scaffold + `.psc` 編譯/打包**，controller 邏輯交給使用者手寫 `.psc` + `ScriptAttachSpec.Source`」這條已支援路徑，而**不是**期待 ModForge 生成動態經濟演算法。重點是：**驗證 `ScriptAttachSpec.Source` 的 end-to-end（自帶 `.psc` → compile → 進 VMAD → in-game）真的通**，並補一個 example spec 示範「掛一顆自寫 controller 到 script-MGEF」。
2. **GMST editing gap：再次確認缺席**（與 T&B 同）。S&D **不需要**它，但它仍是 economy/balance 通用 primitive；維持 roadmap 既有的 `gameSettings:`/`gmst:` block 提案，優先級不因 S&D 改變。
3. **MCM→GLOB→runtime 連線：補強同一缺口。** T&B（perk-condition 讀 GLOB）與 S&D（script 讀 GLOB）都靠這條。**這是兩個 economy mod 的共同 enabler**——值得優先 close：確認/實作「生成的 MCM option 綁定生成的 GLOBAL，並讓 fragment/attached-script 讀得到」。
4. **可重製性定位**：T&B「ModForge 今天能生成大部分」；**S&D「ModForge 能生成全部 record scaffold，但 controller 要人工 `.psc`」**。把這組對比寫進 economy batch index，作為「靜態 overhaul = 可生成 / 動態 controller = scaffold-only」的判準範例。

---

### 實查清單（grounding）

<!-- wf-nav -->
- **實檔**：`~/skyrim_mods/unzip/SupplyAndDemand/Supply and Demand.esp` + `Scripts/{tc_PlayerScript, tc_MonitorScript, tc_AttachScript, tc_PlayerScriptAddSpell, tc_SupplyDemandMCM}.pex`（**無 `.psc`/`.dll`/`.ini`/`.json`，已 `find` 確認**）。
- **plugin**：ModForge CLI `dump` → 12 record（2 GLOB / 3 MGEF / 4 SPEL / 2 QUST / 1 CELL+1 ref override；**無 perk / GMST / Faction / VendorValues / LVLI**）。
- **pex**：`strings` 抽得 `OnItemAdded`/`OnItemRemoved`/`GetGoldValue`/`SetGoldValue`/`ValuesArray1-30`/`OriginalValuesArray1-30`/`tc_Global_ExtinctionRatio`/`SKI_ConfigBase`/"market values shift back to normal" 等（function/property/常數名為據；**邏輯細節為 inference，本機無 decompiler**）。
- **ModForge code**：GMST 缺席（`grep gamesetting|gmst` src/ModForge.Core → 空）；`Spec.Globals.cs`/`Generator.Build.Globals.cs`、`Spec.Magic.cs`(L59-63 `Scripts`)/`Generator.Build.Magic.cs`、`ScriptAttachSpec`(`Spec.Dialogue.cs` L227，有 `Source` `.psc` 欄)、`Spec.Mcm.cs`/`McmGen.cs`/`Generator.Build.Mcm.cs`、`Papyrus.cs`(雙編譯路徑) 皆存在。
