# RDO 的 FormList 投放機制 — exclusion-and-recipes

[返回入口](../rdo-formlist-mechanism.md)

## 4. PreventedActors 排除機制

### 運作方式
- ESP 出貨時 `aaa_RDOPreventedActorsList` **是空的**（0 成員），但被 936 句台詞 + 76 quest 引用為 `IsInList(...)==0`。
- 空 list + `==0` 的初始效果 = 「永遠通過」（沒人在名單裡 → 條件恆真 → 不擋任何人）。
- 一旦有 NPC 被加入這個 list（執行期由 RDO 自身腳本/MCM，或由第三方相容補丁靜態追加成員），**所有掛了 `IsInList(PreventedActorsList)==0` 的台詞會立刻對該 NPC 全部失效**——即「一鍵把某 NPC 從 RDO 的泛用對話池裡摘掉」。

### 為什麼要這樣設計
RDO 用嗓音/陣營/關係**按類**投放（§3），無可避免會掃到一些「不該講泛用台詞」的對象：重要劇情 NPC、有自己整套對話的獨特角色、其他 mod 的自訂隨從等。逐句去加排除條件成本太高，於是 RDO 把「排除」收斂成**單一共用黑名單 + 每句一條守門**：要豁免一個 NPC，只需把它丟進 `aaa_RDOPreventedActorsList`，不必動 936 句台詞。

### 證據要點
- 936 句台詞中 923 句（98.6%）用 `IsInList(PreventedActorsList)==0` 當守門（§2 統計）。
- 該 list 在 ESP 內無靜態成員、且 RDO quest 的 VMAD script property 中**找不到名稱含 "Prevent" 的屬性**（離線掃描 `mod.Quests[].VirtualMachineAdapter.Scripts[].Properties` 無命中）——印證成員是「執行期/外部填充」而非 ESP 內寫死。
- 兩個未使用的排除名單 `HatePL` / `Friend`（§1.A）是為「依關係動態切換排除集合」預留的擴充點，目前空置。

---

## 5. 可複製配方：用 FormList 做規模化投放

把 RDO 的做法抽成可重用範本。一個「規模化投放」的台詞 condition 串長這樣：

```
GetIsVoiceType == 1  voice/list = <白名單：單一 VoiceType 或 aaa_VoicesXXX FormList>   [可 OR 多條]
IsInList       == 0  list       = <黑名單：aaa_PreventedActorsList>                      ← 全域守門
<其他維度>           例如 GetRelationshipRank / GetInFaction / GetRandomPercent
```

對應到 FormList 的兩種角色：

1. **白名單（目標集合）**：建一個裝 VoiceType 的 FormList（如 `aaa_VoicesFemaleList`），用 `GetIsVoiceType==1` 引用 → 一條 condition 涵蓋整組嗓音。**用在「這組台詞要投給一大類 NPC」**。
2. **黑名單（排除集合）**：建一個**空** FormList（如 `aaa_PreventedActorsList`），用 `IsInList==0` 引用，掛在每一句台詞上 → 之後只要往這個 list 加 actor，就能把它一次從整個對話池摘除。**用在「集中管理豁免名單」**。

### 與「逐句寫 GetIsVoiceType」的差異

| 面向 | FormList 集中管理 | 逐句寫 GetIsVoiceType |
|------|------------------|----------------------|
| condition 條數 | 一條涵蓋整組（白名單 list）| 每個嗓音一條，常 OR 串接 |
| 改動成本 | 改 list 成員 → 全部引用同步生效 | 要逐句改 condition |
| 可被別的 mod 注入 | **可**（補丁往 FormList 追加成員即可，不必碰台詞）| 不可（condition 寫死在 INFO 裡）|
| 精準度 | 較粗（整組）| 較細（可只鎖「語氣對」的 1～3 種）|

RDO 的實際取捨：**目標投放用逐句 `GetIsVoiceType`**（要語氣精準，9035 次），只在「要涵蓋一大組」時退用白名單 FormList（210 次）；**排除則一律用黑名單 FormList**（集中管理 + 可被補丁注入，923 次）。白名單追求精準故少用 FormList，黑名單追求「集中 + 可注入」故全用 FormList——這是兩種需求各取所長的結果。

---

## 6. 對 ModForge 的意義

ModForge 目前**無法生成 FormList record**，condition 也**不支援 IsInList / GetIsVoiceType**。對照 `others/modforge-relevance.md`「可短期補」第 2 點，要支援 RDO 式投放，缺三塊：

### (a) FormList record builder（FLST）
- 現況：`Generator.Build.Conditions.cs` / `Generator.Build.Vendor.cs` 只能**引用**既有（vanilla）FormList——`NpcSpec.SellBuyList` 是「ref → 一個 vanilla FormList」（`Spec.Actors.cs:82`），全 Core 內**沒有任何 `AddNew*FormList` 之類的建立路徑**。
- 要補：一個 `FormListSpec`（EditorID + `items[]` 的 ref 清單），build 時建 FLST record、把成員 FormLink 填進去。成員型別不限（VoiceType / Actor / Spell / Package 都可，如 §1 所示），builder 不需限制型別。
- **特例要支援「空 FormList」**：排除名單範式（§4）的核心就是「出貨時空、執行期/補丁填充」，所以 `items[]` 允許為空。

### (b) condition 支援 IsInList（引用該 FormList）+ GetIsVoiceType
- 現況：`Generator.Build.Conditions.cs` 的 dispatch 已有 `getinfaction` / `getisid` / `haskeyword` 等 case（行 56–65），但**沒有 `isinlist`、也沒有 `getisvoicetype`**（grep 兩者皆 0 命中）。
- 要補：
  - `case "isinlist": { var d = new IsInListConditionData(); if (hasParam) d.FormList.Link.SetTo(paramFk); ... }`——paramFk 解析到 (a) 建的 FLST。
  - `case "getisvoicetype": { var d = new GetIsVoiceTypeConditionData(); if (hasParam) d.VoiceTypeOrList.Link.SetTo(paramFk); ... }`——paramFk 可指向單一 VoiceType **或** Voices FormList（同一個槽，RDO 兩種都用）。
- dispatch 結構已可擴充，這是低成本高 ROI（解鎖「按類投放」的第一步，見 `dialogue-targeting-technique.md`）。

### (c) spec 層「名單 + 一組 condition 套 N 句」的批次模板
- 現況：ModForge condition 逐句手寫，沒有「一組 condition 重用到多句台詞」的批次入口。
- 要補：一個批次 dialogue 模板，讓使用者寫一次「白名單 list ref + 排除 list ref + 一組維度 condition」，套用到一張台詞表的 N 句上，build 時對每句 INFO 複製這組 condition。對應 RDO「6650 句自製台詞共用同一套 condition 骨架」的規模化做法。
- 與 (a)(b) 合起來才完整：(a) 給 list，(b) 給能引用 list 的 condition，(c) 給「一套 condition × N 句」的批次展開。三者缺一，RDO 式投放就只能逐句手刻。

### 落地優先序（務實）
1. **(b) condition 兩個 case** —— 改一個檔、十幾行，立刻能在台詞裡引用 vanilla VoiceType / 既有 FormList 做排除與按嗓音投放。
2. **(a) FormList builder** —— 讓使用者能自建白/黑名單（尤其空黑名單）。
3. **(c) 批次模板** —— 工程較大，是把前兩者規模化的入口，最後做。
