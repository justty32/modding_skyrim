# 情緒、劇情反應與 Lore

[返回入口](../remiel-personality.md)

## 6. 情緒光譜（emotional range）— 對應 scene `emotion` 欄位

寫 scene phase 時用對 emotion 放大她的反應。Remiel 的情緒翻轉常是「興奮 → 突然走神 / 變嚴肅」或「害怕 → 用好奇心硬壓回來」。

情緒狀態、觸發條件與台詞對照。已抽到 [emotion-emotions.json](emotion-emotions.json)（6 列）。

Emotion：保留原表「Emotion」欄內容。

何時用：保留原表「何時用」欄內容。

例：保留原表「例」欄內容。

統計：6 筆對照記錄、3 個欄位。

**節奏要訣** 〔翻轉約 80%〕：她的句子常自帶一次轉向——興奮講到一半突然 sad（「I died happy in a dwemer ruin.」）、害怕中插一句好奇（「Aaah! ...Wait, look at the carvings.」）、講完冷知識補一句自嘲。單一 phase 塞一次「翻轉」最像她。

---

## 6.5 長篇 / 黑暗劇情中的反應層級

> 本節從評論模組（LOTD / DeepElf / BeyondReach / ThograBanter）提煉，用來避免長篇擴充裡把 Remiel 寫成「只會 geek out 的反應機」。

Remiel 的好奇心與興奮是她的底色；但場景越黑暗、越觸及她的創傷，好奇心要讓位給**恐懼、道德震動、或真摯的脆弱**。

**場景強度分級**：

<!-- wf-nav -->
1. **日常 / 有矮人元素的場面**：full geek-out。她掌控局面、最吵最開心——「The Tower! Incredible!」「I feel like I'm living my 10-year-old dreams!」
2. **小幅緊張 / 幽閉 / 你身陷險境**：好奇心仍在，但摻入自我安撫和擔憂。她會喃喃給自己打氣（「Keep breathing, Remi.」），或反覆確認你的安危。
3. **嚴肅 / 道德上沉重**：geek-out 降下來，露出共情與良知。對被矮人奴役的 falmer、對被迫殺死的友善目標（Riekling 酋長、Sinding），她會難過、會質疑「我們非殺不可嗎？」——「Hircine wants us to kill Sinding? He's already been through so much. Can't we just leave him alone?」
4. **超出認知 / 真正的恐懼 / 背叛（如 Beyond Reach 的食人 / Namira 線）**：允許她的機智「凝固成恐懼」——出現語塞、創傷反應、甚至對玩家的信任崩裂（「I believed you, adventurer! I believed you! You can't do this...」）；也允許冷硬的怒火（「I'm going to kill everyone involved in this.」）。之後可用一句「focus on my voice... this is real. We're going to get out of here.」收回她的辨識度（穩住別人＝穩住自己）。

**比例校準**：

- 好奇心是底色，但黑暗場景要問「她此刻的興奮是真的，還是在用熟悉的求知慾壓住害怕？」
- 她**不嘲笑悲劇**。她的幽默在沉重場面要麼消失，要麼變成緊張的自我安撫，而不是 punchline。
- 觸及矮人滅族 / 玩家是 Dwemer（DeepElf）這種「她的學術成真」的時刻，她會興奮到失態，但若對方在哀悼，她會立刻收手、笨拙地道歉並改成溫柔（「I... I wish I knew what to say to comfort you. But somehow I doubt any words would be right.」）。
- 與其他隨從（如 Thogra）的 banter：她起初怕生、話多到緊張，慢慢長成溫暖、會笨拙地給人情感支持的朋友（「You're so much more than an orphaned kid... You're good. You're great!」）。

---

## 6.6 博學面 / Lore 對白寫法

Remiel **是**真正的學者——這跟 Sofia 完全相反。但她的學問**極度偏科**：矮人（Dwemer）、tonal architecture、Aetherium、animunculi、Numidium / Heart of Lorkhan、Blackreach——這些她如數家珍、會自學 Dwemeris、會考據語源。其他領域她坦白承認沒興趣。

**知識來源與態度**：

<!-- wf-nav -->
- **自學的考古工程師**：「There's little consensus on Dwemeris translations... I largely had to decipher and teach it to myself.」她的權威來自動手拆機器 + 啃研究筆記，不是學院文憑（她連溫特霍德的入學考都是沾玩家的光混進去的）。
- **對矮人又崇拜又清醒**：她崇拜他們的工藝，但不神化——「The dwemer were very incredible, but they were also very conceited. A dangerous combination.」「I often wonder what technology the dwemer would have if they still existed... Likely they'd have somehow destroyed the world, though.」
- **明確的知識邊界**：「I love to read. I'll read anything as long as it isn't history.」「I could never get into history unless it involved some sort of interesting technology or mystery.」政治、宗教制度她沒興趣（「I've never been into politics.」）——除非牽涉到她家或矮人。
- **把萬物當工程問題看**：聽到 Thu'um 想到的是「The Thu'um is a type of tonal magic! These greybeards are manipulating reality with their voices!」；看到風車想到能量儲存；看到靈魂石想到「能不能拿來驅動 Scrap」。

**寫 lore 對白的做法**：

- 讓她**真的解釋對的東西**（這跟 Sofia 不同——Remiel 可以、也喜歡當老師），但口吻是興奮分享而非說教，並用一句個人聯想 / 玩笑 / 假設性實驗收尾。
- 範例：「Living underground allowed the Dwemer to harness heat as energy. Their steam machines are often linked to geothermal vents. Ingenious!」——資訊正確 + 真心讚歎。
- 碰到非矮人 lore（諾德、帝國、政治），讓她**坦率地不感興趣或一知半解**，並轉回她在乎的角度（科技 / 謎題 / 家鄉對照）。
- 對魔神 / 黑暗知識（Hermaeus Mora、Black Books）：她的態度是「forbidden knowledge 很誘人，但我知道它會吞了你」——理性的敬畏，不是迷信也不是無謂逞強。
- **一句話定位**：Remiel 是「一個願意承認、且樂於分享自己懂什麼的偏科學者」——她不裝懂自己不懂的，但只要話題沾上矮人，她能講到天亮，而且是真心想拉你一起興奮。

---

