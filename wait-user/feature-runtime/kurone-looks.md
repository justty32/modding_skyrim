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
