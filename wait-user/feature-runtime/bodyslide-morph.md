# BodySlide 身體＋裝備曲線（女體兩梯次＋男體）：剩選看項（2026-11-22）

[回清單](../feature-runtime.md)｜依據：[部署報告](../../agentctl/handoffs/home-2026-11-22/bodyslide-morph-deploy/REPORT.md)、[第二梯次](../../agentctl/handoffs/home-2026-11-22/bodyslide-morph-deploy2/REPORT.md)、[男體](../../agentctl/handoffs/home-2026-11-22/male-body-build/REPORT.md)、[擬合](../../agentctl/handoffs/home-2026-11-22/body-fit/REPORT.md)

`modpack-main` 已上線全域 CBBE 身體（基準 `CBBE Vanilla`）＋原版／DLC／CT77／CC／UNSLAAD／VIGILANT／GLENMORIL 女裝、男體 HIMBO 裸體版（TNG）＋男裝、OBody 不隨機＋116 人指定身形。

## 已通過（使用者 2026-11-22：「全都OK」）

- OBody 男女合一 Reset 已做完（關 ORefit 與兩個 randomization → `Reset all distributed presets` → 存新檔重開 → 開 Respectful morph application、對主角 Reset）。
- 主角 HIMBO 滑桿：裸身與穿原版鐵甲都跟著變；脖子、手腕、腳踝沒有色差或縫；路上男 NPC 是普通體型（HIMBO 零形）。
- 一般女 NPC 外觀如常；原版甲與 CC 衣服沒有穿模。
- Aela 穿甲貼合。
- 伊索爾達、簡拉薩（Kurone 兩套身體的代表）裸身如常、穿鐵甲貼合。

## 選看、未回報（玩的時候順路看；有問題才回報）

- **4b VIGILANT／GLENMORIL 女裝**：給女 NPC 穿看貼身、沒隱形、中文名。代表件（ID 隨載入序會變）：警戒者護甲 `230A5872`、尤里安諾思騎士靴子 `23124F24`、亞曆德王的斗篷 `235714CF`（沒重建，只看得到即可）、女德魯伊的長袍 `1801241D`、瘟疫醫生護甲 `182C3347`。agent 已代驗五件都看得到、名稱中文（[截圖](../../agentctl/handoffs/home-2026-11-22/waituser-runtime/REPORT.md) `S2-faralda-*`），貼身要人眼。男 NPC 穿朝聖者長袍、學徒長袍、精英警戒者手套會共用女體網格（原作者設計）。
- **其餘 4d 代表**：小夜 `FE096005`、瓦琳妮娅 `BD005900`、Auri `78000D63`（`player.placeatme <ID> 1` 叫複本，看完 `disable`、`markfordelete`）：裸身沒被推兩次、穿鐵甲（`00012E49`）貼合。
- **男體其餘**：獸人種族男性（貓人、蜥蜴人）身形與膚色；Chadryn 體型正常；UNSLAAD 披風看得到。
- **已知、不是錯**：沒轉換的男裝（UNSLAAD、GLENMORIL、DAc0da、Psijic 靴、Nocturnal 長袍男版等）穿上會縮回原版體型、可能有小縫；女裝 258 件維持作者原樣（[分佈](../../agentctl/handoffs/home-2026-11-22/bodyslide-morph-build/REPORT.md#10-維持作者原樣的最終彙總)）。
- **個別重置**：Ambriel 在 OBody 黑名單，衣甲若比裸身胖或形狀怪：準星對準她 → MCM `OBody NG` → `Reset this actor`。
- **女體滑桿**：女 NPC 套 OBody preset 或新女角拉 CBBE 滑桿；滑桿連拉後失效是 EngineFixes 已知問題（見[日後決定](../later-decisions.md)）。

要整批回退就說「身體回退」，agent 用部署報告裡的指令還原。
