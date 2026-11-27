# 換臉六人實機看臉與身形（2026-11-24；Sofia、Lydia、Melana 已於 2026-11-25 由使用者驗收，剩 Recorder、Ambriel、Aniya）

實體座位已裝好（profiles `7a9bb62`，未 push）：Recorder→克羅艾、Ambriel→莉莉絲、Lydia→嘉蒂絲、Melana→弗倫、Sofia→拉米婭、Aniya→黑暗（22:27 改裝，見下節），身體統一用 Soul Tomb 角色的 Kurone7 身形（OBody 指定層）。MO2 開過後的 `*` 重驗還沒跑，屬建置線的事，不算使用者要看的。

2026-11-25 使用者原話：「sofia,學院的門已經OK, lydia,melana也都OK。」三人（含 Sofia 的 MCM 補丁、Lydia 與 Melana 的 OBody 重置）已結案，下列只對剩下三人。

逐人看以下項目，有問題回報是哪個人、哪一項：

1. **臉與髮型**是不是素材本人。看到素臉或大媽臉，先對她的**真身** `disable` 再 `enable` 再看（存檔臉快取）；仍壞才回報。
2. **脫光看身體**（`<ref>.unequipall`）：Kurone7 身形、膚色、脖子接縫。
3. **身高**：Ambriel 變化最明顯。
4. **衣甲貼合**：穿鐵甲或皮甲看貼不貼身。
5. **Ambriel**：劇情變身前後（D62 與 DB 兩筆）臉一致。
6. **Recorder**：失落檔案回憶場景的過去版本也是克羅艾。
7. 其他已知：Aniya 原本的私有身體被 Kurone7 取代；Aniya 劇情戴原版商人帽時頭髮會被蓋住（原版規則）。

還原指令與逐項驗收表見 [INSTALL-REPORT](../../agentctl/handoffs/home-2026-11-24/kurone-looks-r2/INSTALL-REPORT.md)；安裝單見 [r1](../../agentctl/handoffs/home-2026-11-24/kurone-looks/INSTALL.md)、[r2](../../agentctl/handoffs/home-2026-11-24/kurone-looks-r2/INSTALL.md)。

## Aniya → 黑暗（2026-11-24 22:27 實體裝好，profiles `4c7b669`，取代米麗艾爾層）

看臉與髮型是不是黑暗、SMP 頭髮有沒有畫出來；`unequipall` 看身體。素臉先對她本人 `disable`→`enable`。OBody 不必重置。出處見 [aniya-darkness INSTALL-REPORT](../../agentctl/handoffs/home-2026-11-24/aniya-darkness/INSTALL-REPORT.md)。

## OK 的 10 個女隨從換成 KuroneFollowers 的臉（2026-11-24，profiles `4c7b669`）

「OK_follower and KuroneFollowers」164342，只裝 SkyPatcher ini。看 10 人的臉與髮型（先 `disable`→`enable`），重點看 Natasha、Liliana、Airi、Maya、Rosalie、Sela 有沒有「髮型對但臉是素臉」；`unequipall` 看脖子色差；對話語音照舊；跟其他隨從臉重複是預期。

還原兩份要倒序：先 `layer_apply.py --revert agentctl/handoffs/home-2026-11-24/ok-kurone/data/revert-r1.json`，再 `layer_apply.py --revert agentctl/handoffs/home-2026-11-24/aniya-darkness/data/revert-r3.json`（MO2 開過就會被拒）。出處見 [ok-kurone INSTALL-REPORT](../../agentctl/handoffs/home-2026-11-24/ok-kurone/INSTALL-REPORT.md)。

## r7：菲莉絲其他驗收（2026-11-26）

OBody 對她 Reset 一次。夜鶯、盜賊公會、宴會、囚服及預設服裝換裝時看衣服和頭髮是否消失；若曾用 NFF 隨從狼人，戰後 `getrace` 看是否變回 Breton。不對請回報服裝、畫面及種族結果。[REPORT](../../agentctl/handoffs/home-2026-11-26/look-swap-r7/REPORT.md)

## r9：Secunda 和 Livia 其他驗收（2026-11-26）

兩人 OBody 各 Reset 一次；若曾用 NFF 狼人，戰後 `getrace` 看種族。異常請回報人物與結果。[REPORT](../../agentctl/handoffs/home-2026-11-26/look-swap-r9/REPORT.md)

## r10：Vaelyra 其他驗收（2026-11-27）

OBody 對她 Reset 一次應是 `BSO Fit kurone7 (morph)`；若曾用 NFF 隨從狼人，戰後 `getrace` 看種族。[REPORT](../../agentctl/handoffs/home-2026-11-27/look-swap-r10/REPORT.md)

## r11／r11b：雪精靈其他驗收（2026-11-27）

OBody 對她 Reset 應是 `BSO Fit kurone7 (morph)`；Taeka 與奧莉安娜 Reset 後不套 preset（此為 r11b 狀態，後續 r13 改了 Taeka）。[REPORT](../../agentctl/handoffs/home-2026-11-27/look-swap-r11b/REPORT.md)

## r12／r12b：奧絲瑞爾其他驗收（2026-11-27）

到 Othriel's Cabin 敲門推進劇情，確認名字「奥丝瑞尔」與「被诅咒的阴影」沒有空白或亂碼；兩場影子 boss 戰確認黑甲，打碎鏡子重生及最後定身時各看一次。OBody Reset 應是 `BSO Fit kurone7 (morph)`。[REPORT](../../agentctl/handoffs/home-2026-11-27/look-swap-r12b/REPORT.md)

## r13：迭卡其他驗收（2026-11-27）

穿起始法袍、手套、靴、披風、藥瓶及肩上老鼠，確認都有顯示；看帽子與長髮是否穿模，天冷自動換帽時再看；晚餐任務睡覺橋段看青蛙。OBody 對她 Reset 應是 `BSO Fit kurone7 (morph)`，奧莉安娜不套 preset。異常回報衣物、場景及截圖。[REPORT](../../agentctl/handoffs/home-2026-11-27/look-swap-r13/REPORT.md)

## r14：蕾雅其他驗收（2026-11-27）

名字「蕾雅」不能亂碼。本尊與分身各在 OBody Reset 一次，應是 `BSO Fit kurone7 (morph)`。若使用 NFF 隨從狼人，變回人後看是否變回紅衛人身體。[REPORT](../../agentctl/handoffs/home-2026-11-27/look-swap-r14/REPORT.md)

## r15：阿蘭尼亞其他驗收（2026-11-27）

此輪報告只到 staging，待部署後再驗。確認準星與對話名字不是空白亂碼；確認 FDE 對話與暗精靈女聲正常，OBody Reset 應是 `BSO Fit kurone7 (morph)`；若使用 NFF 隨從狼人，變回人後看種族有無變回。[REPORT](../../agentctl/handoffs/home-2026-11-27/look-swap-r15/REPORT.md)
