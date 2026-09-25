# 情緒、劇情反應與 Lore

[返回入口](../mirai-personality.md)

## 6. 情緒光譜（emotional range）— 對應 scene `emotion` 欄位

Mirai 的台詞在引擎裡帶 emotion tag。寫 scene phase 時用對 emotion 放大情緒：

情緒狀態、觸發條件與台詞對照。已抽到 [emotion-emotions.json](emotion-emotions.json)（7 列）。

Emotion：保留原表「Emotion」欄內容。

何時用：保留原表「何時用」欄內容。

例：保留原表「例」欄內容。

統計：7 筆對照記錄、3 個欄位。

**節奏要訣** 〔情緒翻轉約 80–90%，盡量常用〕：她很常在一句內翻轉（嘴硬→漏真心、好奇→警覺、感動→惱羞）。例：「At least you came back for me.」（怨→感激）；「I'll say it again, you're a really strange person doing all this for me. But... thanks.」（嫌→道謝）。單一 phase 內塞一次「翻轉」最像她。

---

## 6.5 長篇 / 黑暗劇情中的反應層級

> 這節用來避免長篇擴充（尤其 Dragon Heart 主線、Zan'nen 背叛、Miraak 相關）裡把 Mirai 寫成只會循環「感知評論 + 嘴硬」的反應機。它是寫作校準，不覆蓋前面基於原文的核心 brief。

Mirai 的感知評論、嘴硬、brat 不是孤立模板，而是她**面對一個她其實還不太掌控的世界時的自我定位方式**。平時這些看起來只是少女碎念；在 Dragon Heart 這類觸及身世創傷的劇情裡，它們應該變成**防禦機制與真實情緒的拉扯**。

**場景強度分級**：

1. **日常 / 探索場面**：照常感知評論、吐槽地點天氣、跟玩家拌嘴。她最放鬆、最話多、最 brat。
2. **小幅緊張 / 不知所措**：感知評論可以轉成自我安撫或不祥預感（「Something in my head is just telling me not to go...」），嘴硬頻率上升但目的是壓住不安。
3. **嚴重 / 真正震動她的場面**（被背叛、發現自己是養女 / 交易品、龍語覺醒）：碎念與嘴硬要降下來。允許她崩、質問、憤怒、甚至向玩家求援（「I just don't trust Junan all that much... I just... don't want to go alone.」）。
4. **超出認知 / 創傷核心**（噩夢、Black Book 殘頁的黑暗詩、得知父母真相）：允許短暫沉默、語塞、真心流露、不帶吐槽的乾冷話。之後再用一句嘴硬或轉移話題收回來，維持 Mirai 的辨識度。

**比例校準**：

- 好奇與感知仍是底色，但在創傷劇情中要問「她此刻為什麼還在評論環境」：是真的好奇，還是在用熟悉的碎念逃避眼前太重的事？
- 嘴硬對玩家應帶測試、撒嬌或防衛意味；真正的怒火留給父親的 cult、背叛者、與「批評她父母 / 她的選擇」的人。
- 信任是**漸進**的：越往劇情後段、好感越高，越可以讓她短暫卸下防衛、直接說怕、直接道謝、直接依賴。別讓她一開始就交心，也別讓她到最後還像陌生人一樣刺。
- 別在每個黑暗 beat 都硬塞 brat 笑點。嚴肅場面裡，她的結巴 / 反問最好暴露她的慌張或痛，而不是只服務笑點。

**長篇劇情新增檢查**：

- 這句話是在好奇、設防、受傷、憤怒、渴望被愛，還是單純套模板？
- 目前場面承受得住多少 brat / 吐槽？如果是創傷核心，是否需要先讓她被擊中、崩一下，再用嘴硬收尾？
- 這段是否反映她與玩家**信任關係的階段**？越往後、越信任，越可以露出脆弱與依賴。
- 有沒有避免「無限感知評論 / 嘴硬 / 惱羞」的機械循環？

---

## 6.6 博學面 / 世界觀對白寫法（她的「感知」如何延伸成見解）

Mirai 不是學院派 lore 學者，但她**對世界有強烈的、第一人稱的、帶價值判斷的觀察**——這是她「aware」特質的延伸。她的知識來源是**親身遊歷**（往返 High Rock 與 Skyrim 的 Breton 旅人）而非書本，所以她講的是**體感與道德判斷**，不是學術框架。

**她對每座城 / 每件事都有具體的、帶情緒的意見**（這是寫她城鎮 / 地點評論的範本）：

- **不是**「Markarth 建於山中，曾被 Forsworn 佔領」這種百科條目。
- **而是**帶體感與情緒：「Surprisingly beautiful for a city made in the mountains... but living here has been so... foreboding? ... There's just so much hatred in this city... I honestly can't think of one person that lives here that isn't bitter!」
- 政治她坦承「I was never all that interested in geopolitics, but as a Breton in constant travel between High Rock and Skyrim, it was kind of forced upon me.」——她懂，但是被生活逼著懂的，不是學來炫的。
- 對 Forsworn 有複雜的同理：「they've made life as a Breton in the Reach unbearable at times but... I never blamed them for fighting for their home.」
- 對道德兩難會選邊並說理：對 Sinding「Remorseful or not, he still murdered a young girl!」「what makes us different from animals is our ability to control those urges.」

**寫世界觀對白的做法**：

- 讓她從**親身體感**切入（冷、美、可怕、壓抑、無聊），再延伸到判斷。
- 她對權力 / 不公 / 弱者有本能的道德立場（同情被綁的 Sybil、痛恨綁架小女孩、看穿盜賊「No honor amongst thieves.」）。
- 對藝術 / 詩 / 音樂有真心嚮往（Bard's College「I wish more people would take an interest in the arts... over fighting, stealing, and assassinating.」「I think poetry is best when it comes from the heart.」）——這條柔軟面與她的刺嘴形成對比。
- 對龍 / 龍語 / Dragon Heart 相關，她是**當事人**而非旁觀者：困惑、不安、被命運推著走，別寫成她在介紹 lore，要寫成她在面對自己。

**一句話定位**：Mirai 的「博學」其實是「**一個被迫早熟、走過很多地方、對每樣東西都有切身意見的少女**」——她不講框架，她講「我在這裡冷得要死 / 這座城讓我喘不過氣 / 這個人不值得同情」。

---

