# planning — 想法成熟管線（idea → roadmap → 詳規 → 執行）

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

從萌芽到動工的四階段收在**同一條管線**，不拆成四個工作流——免得卡在「這算 idea 還是 roadmap」。2026-08-30 起取代原本分開的 `idea/`、`roadmap/`、`specs/` 三個工作流。

**何時用**：使用者說「記個想法」「以後要做」「排進 roadmap」「幫我規劃」「把這個討論成方案」「寫動工計畫」。
**何時不用**：三兩步的小事直接做；已有 plan 且在動工 → [feature-dev](feature-dev/README.md)；只是要調查清楚 → [investigation](investigation/README.md)。

## Done when

- idea / roadmap：下方對應表多一列，或既有列狀態欄更新。
- 詳規：[`plans/`](plans/README.md) 底下有一份計畫，含「步驟 / 驗證」段；動工完成後在 plans 的「已結案／被取代」表登記結果。

## 階段

| 階段 | 回答的問題 | 落點 |
|------|-----------|------|
| **idea** | 要不要做？ | 下方「想法」表 |
| **roadmap** | 會做，何時？ | 下方「roadmap」表 |
| **詳規** | 怎麼做？ | [`plans/README.md`](plans/README.md)——一個計畫一個項目，超過 8KB 拆成目錄型；設計取捨直接寫進計畫，本 repo 不另設 specs 夾 |
| **執行** | — | [feature-dev](feature-dev/README.md)（碰程式碼）；Skyrim 側的實作走 [WORKFLOWS.md](../WORKFLOWS.md) 的 Skyrim 專屬工作流 |

## 想法（要不要做）

| 想法 | 一句話 | 狀態（想想 / 會做→搬 roadmap / 不做＋原因）|
|------|--------|------------------------------------------|
| **把無心人物外觀用進未來任務**（2026-08-13）| 這只是人物美化完成後的可選延伸；目前主要工作是先讓經典無心人物美化在 SE/AE 1.6.1170 正常運作，見 [適配調查](investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。若日後真的建立全新具名 NPC 群，私人原型仍需從合法來源拆分 FaceGen／head parts；公開發布則必須取得 `Decent Women` 與髮型、皮膚、眉毛等完整資產許可，否則只能重做相近審美的原創外觀。| 想想 |

## roadmap（會做，何時）

| 事項 | 何時 / 順序 | 前提 |
|------|------------|---------|

## 交接

- 決定「為什麼選 A 不選 B」 → [decisions](decisions.md)。卡在使用者 → [WAIT_USER](../../WAIT_USER.md) 一行；跨 session → [SESSION-LOG](../../SESSION-LOG.md) 一行。
