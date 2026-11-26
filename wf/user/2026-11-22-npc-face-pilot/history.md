# NPC 換臉試點：舊段落（歷史）

[回試點頁](../2026-11-22-npc-face-pilot.md)

以下是 runtime-3 之前的內容，已過時，只留作紀錄。現況看試點頁最上方。

## face-pilot-2（2026-11-22 下午）

卡點解開：改在 RaceMenu 介面裡換種族、載 Hatak、按「匯出頭」，頭部件就正確了。Muiri 的換臉層做好、檢查全過（保留原體重），當時還沒裝進遊戲。細節：`agentctl/handoffs/home-2026-11-22/face-pilot-2/REPORT.md`。

## 第一次試點（2026-11-22，你出門時 agent 跑的）

**結論：沒做成。** Muiri 的臉沒換，換臉層沒產出、沒部署，遊戲裡什麼都沒留下。

- 開了 4 場遊戲做匯出（上限 4 場），每場都**沒存檔**；存檔目錄 91 個檔前後 sha256 逐檔相同。
- 卡在遊戲沒把 Hatak 的頭部件（臉型、髮型、眉眼、疤）真的換上去，只換到膚色、戰紋、唇色、髮色。拿去給 Muiri 用會變錯臉，所以停手。
- 換了三種做法、外加用全新角色試，結果都一樣。細節見 [REPORT](../../../agentctl/handoffs/home-2026-11-22/runtime-pilot/REPORT.md)。

| 原本的 Muiri（JH NPC Beauty） | 主角套 Hatak 後（只換到妝與膚色） |
|---|---|
| 原 Muiri（本機圖 `agentctl/handoffs/home-2026-11-22/runtime-pilot/s2/08-muiri-orig-front.jpg`） | 主角套 Hatak（本機圖 `agentctl/handoffs/home-2026-11-22/runtime-pilot/s2/06-player-hatak-front.jpg`） |

（主角側面：本機圖 `agentctl/handoffs/home-2026-11-22/runtime-pilot/s2/07-player-hatak-side.jpg`。原 Muiri 那張是用 `placeatme` 叫出的暫時複本，拍完刪掉，沒存檔。）

當時給的三條路：你手動一次在 RaceMenu 載 preset／打通 Creation Kit／先不做。後來 face-pilot-2 找到真因（主控台改種族後頭不重建），改在 RaceMenu 介面點種族就解了，三條路都不必走。

## 當時申請的授權（已用完）

1. **開一次遊戲做匯出**（約 20 分鐘）：取桌面與遊戲鎖，主角暫時改成女性 Breton 戴 Hatak 的臉，匯出後**不存檔**關遊戲。
2. **暫時放觸發 ESP、腳本、jslot 進 MO2**，用完用 `layer_apply --revert` 逐位元組還原；`overwrite/` 新出的匯出檔先複製到 staging 再刪。清單見 `agentctl/tools/npc_face/trigger/README.md`（這條路後來被 RaceMenu 介面匯出取代）。
3. **部署 Muiri 換臉層**：新 mod 層排在 JH NPC Beauty 之上、plugins.txt 尾端加一顆 ESL patch；收回用 `layer_apply --revert` 或在 MO2 停用。

失敗時的備案是改走 Creation Kit（CK 已裝，Linux 上能不能出臉沒驗過）；record patch 兩條路共用。

一直不做的事：不用 PROTEUS 的「清除 NPC 編輯」（會刪硬碟上的臉部檔，可能連已裝 mod 一起刪）；不存檔、不改你的存檔；不碰其他 NPC。
