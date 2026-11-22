# BodySlide 身體＋裝備曲線（女體兩梯次＋男體）實機驗收（2026-11-22）

[回清單](../feature-runtime.md)｜依據：[部署報告](../../agentctl/handoffs/home-2026-11-22/bodyslide-morph-deploy/REPORT.md)

`modpack-main` 已上線：全域 CBBE 身體（基準 `CBBE Vanilla`，外觀和原來的 Sofia 身體一樣，只多了 `.tri`）、原版／DLC／CT77 衣甲、CC 衣服、UNSLAAD 19 件，以及新的 OBody 設定（不再隨機分配身形；Aela 指定成和她裸身一樣的身形）。

同日另上線**男體**（依據：[男體施工報告](../../agentctl/handoffs/home-2026-11-22/male-body-build/REPORT.md)）：全域男性身體換成 HIMBO（裸體版，含獸人種族；生殖器與男性皮膚貼圖由 TNG 提供），原版／DLC、CC、VIGILANT 的男裝換成帶 `.tri` 的 HIMBO 零形版，主角可在 RaceMenu 用 HIMBO 滑桿捏身形；其他男 NPC 一律固定在 HIMBO 零形。

存檔裡大約 1,800 個 NPC 還記著 OBody 以前隨機分的身形數值。以前身體沒有 `.tri`，所以看不出來；現在有了，**沒做下面第 1 步之前，路上的 NPC（男女都是）身形會亂掉**。這是預期中的，照順序做就會恢復。**男女是同一個 Reset，只要做一次。**

## 1. 先做（一次就好，男女一起）

1. **先留一個部署前的存檔不要覆蓋**，萬一要回退就讀它。
2. 進遊戲、讀檔，走進一個**沒有其他 NPC 的室內**（自宅或清空的地城）。
3. 開 MCM：`Esc` → `系統`（System）→ `模組設定`（Mod Configuration）→ 左欄 `OBody NG`。
4. **先關三個開關**：`Enable ORefit`、`Enable nipple randomization`、`Enable genitals randomization` 都改成關。不關的話，穿衣服的 NPC 會被 ORefit 再改一次形，衣服就不是原樣了。
5. 同一頁點 `Reset all distributed presets`，跳出確認選「是」；再跳「PLEASE SAVE THE GAME AND EXIT」就照做。
6. **另存一個新存檔**（不要蓋掉第 1 點留的檔），完全退出遊戲，重開 MO2／遊戲，讀這個新存檔。
7. 讀檔後回到同一個 MCM 頁，把 `Respectful morph application`（或同義的「尊重其他 morph」選項）**打開**。這樣之後 OBody 再處理主角時，只清它自己的數值，不會把你在 RaceMenu 捏的身形洗掉。然後對自己（主角）點一次 `Reset this actor`，清掉主角身上以前隨機分到的舊男體數值。
8. 之後才去 RaceMenu 捏主角（第 4c 節）。順序反過來的話，Reset 可能把剛捏好的身形清掉。

## 2. 要看的

- **一般女 NPC 外觀和以前一樣**：在城裡看三、四個女 NPC，裸身／穿衣都和以前一樣，沒有突然變胖、變瘦或變形。
- **穿原版鎧甲與 CC 衣服沒有穿模、接縫、破洞**：原版鐵甲或皮甲、一件 CT77 長袍、一件 CC 衣服（例如 CC 的水手或貴族服）、一件 UNSLAAD 的甲；看領口、手腕、腳踝的接縫。CC 衣服的外形會比以前更貼身體，這是修正，不是錯。
- **UNSLAAD 披風**（半龍人那套）仍然看得到、沒有消失。
- **Aela**：裸身和以前一樣；穿上她的甲之後，甲的輪廓要接近裸身（以前甲是一般身形、比她瘦）。體重滑桿可以的話看 0 和 100 兩端。
- **自帶專屬身體的 NPC**（Kurone 系列等）裸身不變。

## 3. 少數人可能要個別重置

下面這 11 個人在 OBody 黑名單裡，但存檔裡留著以前隨機分到的身形值；Reset 不會清掉黑名單的人，所以她們的**衣甲**可能看起來比裸身胖一點或形狀不對：Camilla、Brelyna、Uthgerd、Ysolda、Frea、Delphine、Jenassa、Mjoll、Melana、Ambriel、Aniya。（4d 上線後，其中 10 人改成有指定身形、移出黑名單，第 1 步的 Reset 會一起清掉；只剩 **Ambriel** 可能要個別重置。）看到不對時：準星對準她 → 開上面那個 MCM 頁 → 點最下面 `Reset this actor: <名字>`。（Aela 不用，她有指定身形，Reset 時會自動清掉。）

## 4. 選做：身體滑桿（RaceMenu）

你的主角是男性、用原版男體，**女體滑桿捏不到他**，所以不要拿主角驗。滑桿 plugin（`RaceMenuMorphsCBBE`）已經裝好，給之後的女角色／NPC 用。想驗的話二選一：

- 準星對準一個一般女 NPC，按 OBody 的 preset 鍵，選一個明顯的 preset（例如 `CBBE Curvy`）：她的裸身和衣服要一起變。看完同一頁 `Reset this actor` 還原。
- 或開一個新的女角色測試檔，在 RaceMenu 的身體分頁拉幾個 CBBE 滑桿：裸身和穿上裝備都要跟著變。連拉幾次後滑桿如果突然沒反應，是 EngineFixes 的已知問題，見[日後決定](../later-decisions.md)那一項，回報一聲即可。

## 4b. 第二梯次：VIGILANT／GLENMORIL 女裝（同一場一起看，2026-11-22 上線）

依據：[第二梯次部署報告](../../agentctl/handoffs/home-2026-11-22/bodyslide-morph-deploy2/REPORT.md)。VIGILANT 378 件、GLENMORIL 20 件女裝換成帶 `.tri` 的 `CBBE Vanilla` 版（跟第 1 步 Reset 後的身形走）。做完上面第 1 步就能看，不用另外 Reset。

主角是男性，所以要找**女 NPC 穿**：給女隨從交易後叫她穿上；或用主控台點選一個女 NPC，打 `additem <ID> 1`，再打 `equipitem <ID>`（ID 是本次載入序算出來的，之後 mod 增減會變）。

| 要看的 | 名稱 | ID |
|---|---|---|
| VIGILANT 長袍 | 警戒者護甲 | `230A5872` |
| VIGILANT 靴子 | 尤里安諾思騎士靴子 | `23124F24` |
| VIGILANT 斗篷（這件沒有重建，維持原樣，只確認**看得到**） | 亞曆德王的斗篷 | `235714CF` |
| GLENMORIL 有體重版的件 | 女德魯伊的長袍 | `1801241D` |
| GLENMORIL 單一網格的件 | 瘟疫醫生護甲 | `182C3347` |

- **貼身、沒有破洞或穿模**：看領口、手腕、腳踝、腰。體重滑桿兩端（0 和 100）的 NPC 各看一次最好。
- **沒有隱形**：每件都要看得到。特別看斗篷那件，它和另外 6 組沒重建的件（Ancient Dreugh 甲與披風、幾件 HDT 披風、藥劑師兜帽）是同一種處理。
- **名稱是中文**：物品欄、交易畫面的名稱都還是中文（上表那些名字）。
- 選看：男 NPC 穿 VIGILANT 的朝聖者長袍、學徒長袍、精英警戒者手套時，會和女 NPC 共用新版網格（原作者就是男女共用同一個網格），看起來可能比以前更貼女體。若覺得怪，回報一聲。

agent 2026-11-22 已代驗（Reset 前、Save342）：上表 5 個 ID 現在仍正確；五件給法勞達逐件穿上都**看得到、沒有隱形**（GetEquipped 全為 1），物品欄名稱五件都和上表一致。截圖 `agentctl/handoffs/home-2026-11-22/waituser-runtime/shots/S2-faralda-*-front.jpg`。「貼身、沒穿模」要 Reset 後才準，仍要你看。

**有哪些本來就不會跟身形**：一共 258 件維持作者原樣（VIGILANT 29、GLENMORIL 127、UNSLAAD 59、DAc0da 35、原版特殊件 8），分佈表見[建置報告第 10 節](../../agentctl/handoffs/home-2026-11-22/bodyslide-morph-build/REPORT.md#10-維持作者原樣的最終彙總)（明細 [kept-as-authored.json](../../agentctl/handoffs/home-2026-11-22/bodyslide-morph-build/data/kept-as-authored.json)）。這些件穿上後是固定的作者形，不是錯。

## 4c. 男體（同一場一起看）

- **主角捏身形**：開 RaceMenu（主控台 `showracemenu`，或 RaceMenu 自己的入口）→ 身體分頁 → 找 HIMBO 的滑桿（例如胸肌、手臂、腿粗細）拉明顯一點。**裸身**和**穿原版鐵甲（或皮甲）**時身形都要跟著變。連拉幾次後若滑桿突然沒反應，是 EngineFixes 的已知問題（見[日後決定](../later-decisions.md)那一項），回報一聲即可。
- **裸體**：主角脫光後是裸體（TNG 提供），身體和頭、手、腳的膚色接得起來，脖子、手腕、腳踝沒有明顯色差或縫。TNG 有自己的 MCM（`The New Gentleman`），預設值就可以用，不用改。
- **路上的男 NPC**：看三、四個衛兵、商人，體型是 HIMBO 零形（比原版稍微結實一點的普通體型），**不能**是以前那種誇張的 Kaeserius 肌肉形；穿衣服的也一樣。
- **獸人種族男性**（貓人、蜥蜴人）各看一個：身體是 HIMBO 形，膚色沒有大塊錯色、脖子手腳沒有破洞。
- **自帶身體的男隨從**：Chadryn（Katana 那邊的隨從）若有帶在身邊，看他體型正常、沒有被拉成怪形。
- **沒轉換的男裝會回到原版身形**（已知，不是錯）：UNSLAAD、GLENMORIL、DAc0da 的男裝，以及原版裡少數件（例如 Psijic 靴、諾克圖娜（Nocturnal）長袍的男版、少數男女共用同一網格的靴子與長袍）。穿上後主角會「縮回」原版體型，手腕／脖子／腳踝可能有小縫。想確認的話穿一件 UNSLAAD 甲看看即可。

## 4d. 自帶專屬身體的女角穿甲合身（第三梯次，同一場一起看）

依據：[擬合施工報告](../../agentctl/handoffs/home-2026-11-22/body-fit/REPORT.md)。116 個自帶身體的女角（Kurone 系列 52 人、Kurone 換臉換身的城鎮 NPC、Auri、Serana、Ashe、OK 隨從等）各指定了「和她裸身一樣」的身形，原版、CT77、CC、VIGILANT 等帶 `.tri` 的衣甲會撐成她的身形。做完第 1 步的 Reset 就生效（Reset 前已在存檔裡的人，要 Reset 後才吃新指定）。

挑 5 個代表看就好（runtime ID 是本次載入序算的，之後 mod 增減會變）：

| 誰 | 代表哪一群 | 去哪找 | runtime ID |
|---|---|---|---|
| 小夜（Saya） | Kurone 私有身體 52 人（Saya、Liz、Karin、Nell、Soul Tomb 一群） | 跟著 Saya 的任務線；或主控台 `player.placeatme FE096005 1` 叫一個複本出來 | `FE096005` |
| 伊索爾達（Ysolda） | Kurone BCB 身體 14 人（Aela、Ysolda、Uthgerd、Mjoll、Elisif…） | 雪漫城市集 | `00013BAB` |
| 簡拉薩（Jenassa） | Kurone 另一套身體 6 人（Jenassa、Delphine、Frea、Jordis…） | 雪漫城「醉酒獵人」酒館 | `000B9982` |
| 瓦琳妮娅（Varinia） | Kurone All-Looks 同一套身體 10 人（Varinia、Katana、Megara、Vilja、Melana…） | 她的隨從 mod 出生點；或 `player.placeatme BD005900 1` | `BD005900` |
| Auri | 自帶 CBBE 身體的隨從（Auri、Katana 的 River／Elli、Secunda：這幾人的身體檔被改指到空 tri） | 她的隨從 mod 出生點；或 `player.placeatme 78000D63 1` | `78000D63` |

每人看兩件事：

- **裸身和以前一樣**：沒有比以前更誇張（胸、臀被再推大一次就是「推兩次」，要回報）。
- **穿原版鐵甲或皮甲後，甲的輪廓接近她的裸身**：以前甲是一般身形、比她瘦或胖，現在要貼合。穿法：主控台點選她，`additem 00012E49 1` 再 `equipitem 00012E49`（鐵甲；皮甲是 `0003619E`）。

`placeatme` 叫出來的是複本，看完點選它打 `disable`，再打 `markfordelete`。

## 5. 回報

都正常就說一聲「身體 OK」（第二梯次、男體與 4d 也一起算）。有問題請說是哪個 NPC、穿什麼、在哪裡。要整批回退就說「身體回退」，agent 會用報告裡的一行指令還原（之後讀第 1 點留的存檔）。
