# 換臉六人實機看臉與身形（2026-11-24）

實體座位已裝好（profiles `7a9bb62`，未 push）：Recorder→克羅艾、Ambriel→莉莉絲、Lydia→嘉蒂絲、Melana→弗倫、Sofia→拉米婭、Aniya→米麗艾爾，身體統一用 Soul Tomb 角色的 Kurone7 身形（OBody 指定層）。MO2 開過後的 `*` 重驗還沒跑，屬建置線的事，不算使用者要看的。

逐人看以下項目，有問題回報是哪個人、哪一項：

1. **臉與髮型**是不是素材本人。看到素臉或大媽臉，先對她的**真身** `disable` 再 `enable` 再看（存檔臉快取）；仍壞才回報。
2. **脫光看身體**（`<ref>.unequipall`）：Kurone7 身形、膚色、脖子接縫。
3. **身高**：六人都有變，Ambriel 最明顯，Sofia 會變矮。
4. **衣甲貼合**：穿鐵甲或皮甲看貼不貼身。
5. **Lydia、Melana、Aniya 要在 OBody 選單各重置一次**：她們之前被 OBody 分配過 preset，存檔裡已套的不會自己換。
6. **Ambriel**：劇情變身前後（D62 與 DB 兩筆）臉一致。
7. **Recorder**：失落檔案回憶場景的過去版本也是克羅艾。
8. **Sofia**：名字回到中文「索菲亚」。MCM 補丁 `Sofia-MCM-KeepRace-Dev-2026-11-24` 已裝（profiles `2c6dc92`）。先主控台點她打 `GetIsRace AAA_NordRace`：回 `1` 正常；回 `0` 表示存檔早被改回原版諾德，回報頂層，先別動 MCM。回 `1` 再到 MCM 改一次戰鬥風格，確認臉、身體、身高不變、`GetIsRace` 仍 `1`、MCM 中文沒亂碼。細節見 [sofia-mcm-race INSTALL](../../agentctl/handoffs/home-2026-11-24/sofia-mcm-race/INSTALL.md) 末節。
9. 其他已知：Melana、Aniya 原本的私有身體被 Kurone7 取代；Aniya 劇情戴原版商人帽時頭髮會被蓋住（原版規則）；Melana 只換臉身，動畫照舊。

還原指令與逐項驗收表見 [INSTALL-REPORT](../../agentctl/handoffs/home-2026-11-24/kurone-looks-r2/INSTALL-REPORT.md)；安裝單見 [r1](../../agentctl/handoffs/home-2026-11-24/kurone-looks/INSTALL.md)、[r2](../../agentctl/handoffs/home-2026-11-24/kurone-looks-r2/INSTALL.md)。
