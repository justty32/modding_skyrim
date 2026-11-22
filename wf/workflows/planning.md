# planning — 想法成熟管線（idea → roadmap → 詳規 → 執行）

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

從萌芽到動工的四階段收在**同一條管線**，不拆成四個工作流——免得卡在「這算 idea 還是 roadmap」。

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
| **自製室內 cell／navmesh 檢查工具**（2026-11-22）| 以 Interior Inspector 1.0 為參考（只借思路、不抄碼，它的授權未知）：檢查各 mod 改過的室內是否刪 navmesh、門通虛空等。它是單檔網頁、整套 mod 一次讀進瀏覽器，要改成不爆記憶體、符合本工作區需求的版本。依據 `agentctl/handoffs/home-2026-11-22/interior-inspector/REPORT.md`、[finding](../../analysis/tool-survey/findings/interior-inspector.md)。使用者：「以後有需要可以把它當參考，我們另外做不會爆記憶體的」| 想想：延後 11-28（見 roadmap 段首） |

## roadmap（會做，何時）

**延後 11-28**（使用者 2026-11-22「8/9.都先放着，等下禮拜六。」）：上表室內檢查工具、下表標「延後 11-28」的項（含 racemenu 取景穩定化、剩餘滑桿校準與示範一輪），以及 aos 接入第 3～5 期（含舊記憶夾收尾、`tmp/aos-skyrim-agent/` 清不清，見 [aos.md](aos.md)），都延後至 2026-11-28（週六）再議，屆時由使用者開口，不自動動工。

| 事項 | 何時 / 順序 | 前提 |
|------|------------|---------|
| **RaceMenu AI 捏臉第二階段** R1–R7 | 進行中；詳規 [racemenu-face](plans/racemenu-face/README.md)；取景／校準／示範延後 11-28 | R5 正向／R4 觸發元件／R6 驗證已做（2026-11-22 離線）；R3／R4 實機試點待使用者授權（[試點頁](../user/2026-11-22-npc-face-pilot.md)）；R1、R2、R7 未排程；R3 截圖閉環工具 `face_loop` 已做並實機 6 場（2026-11-22 face-loop），重現性不足、滑桿只校準 1 軸＋3 軸半邊（女） |
| **離線出圖原型**：拆用 Skyrim Universal Viewer 的 NIF 渲染器（2026-11-22）| 延後 11-28 | 授權 pip 裝 PyQt6、執行 SUV 程式碼；依據 universal-viewer REPORT §4 A；是 [racemenu 段 3](racemenu/loop.md#3-離線預覽) 的相依 |
| **SUV 裝進 MO2 當瀏覽器**（2026-11-22）| 延後 11-28 | 授權改 MO2 安裝；它會刪檔、搬檔、寫 `.mohidden`；同上 §4 B |

## 交接

- 定下的決定 → [decisions](decisions.md)。卡在使用者 → [WAIT_USER](../../WAIT_USER.md) 一行；跨 session → [SESSION-LOG](../../SESSION-LOG.md) 一行。
