## VIGILANT 1.8.2 正體中文

現役已是 exact 1.8.2，45 筆 `BOOK.DESC` 私人 text-only layer 亦已升版。到晨星城風岳旅店找
Altano，抽查主線開場、對話／字幕、日誌／目標、書籍、物品／效果、MCM，至少打開一件「石之碎片」
確認描述為正體。英／日配音保留；作者檔與私人修正不公開重發。

## 2026-08-20 任務內容批

抽查 UNSLAAD 3.0.6b、Missives 2.03、DAc0da 1.1.0b、GLENMORIL 0.96.80b 的 MCM／任務入口、
~~正體~~**中文**日誌／對話／字幕、語音與跨 worldspace。GLENMORIL 語音覆蓋 3,653/4,792，UNSLAAD 英語語音
只涵蓋 Act 1；Silent Voice 是接受狀態。證據見
[`quest batch`](../../agentctl/logs/quest-content-batch-2026-08-20.md)與
[`final smoke`](../../agentctl/logs/modpack-kr-final-smoke-2026-08-21/RESULT.md)。

**對象更正（2026-09-05 實讀，四件都還在，但兩件的中文層從繁中換成簡中）**：
- **UNSLAAD**：`modlist.txt:356`＝`+Unslaad SE 3.0.6b Dev 2026-08-20`（本體啟用），
  中文層現役是 `:353`＝`+ZH-Unslaad-CHS-113238-Dev-2026-09-03`（**簡中**），
  原繁中層 `:354`＝`-Unslaad Traditional Chinese 3.0.6 Dev 2026-08-20`（**已停用**）。
- **DAc0da**：`:349`＝`+DAc0da 1.1.0b Dev 2026-08-20`（本體啟用），
  中文層現役是 `:344`＝`+ZH-DAc0da-CHS-139176-Dev-2026-09-03`（**簡中**），
  原繁中層 `:345`＝`-DAc0da Traditional Chinese 1.1.0 Dev 2026-08-20`（**已停用**）；
  另有 `:346`＝`+DAc0da-Voiced-Traditional-Chinese-Combined-Dev-2026-09-03`（語音層繁中，啟用）。
- **Missives**：`:322-332`／`:350` 共 12 個條目全啟用，仍是繁中層。
- **GLENMORIL**：`:333-338`／`:341-343` 全啟用，仍是繁中層。
所以「正體日誌／對話／字幕」這個條件對 UNSLAAD／DAc0da 已不適用，改按
「有中文、無方框破版」判（繁簡都可接受）。

## JhNPCBeautyDev 蓋掉 NPC 中文名（2026-08-28 發現，待裁示）

`JhNPCBeautyDev.esp` 在**插件層**覆蓋數個 NPC 的 `FULL`，把中文名寫成英文，已確認的有
**Lydia**（`override_depth=4`）、Bryling、Erdi、EvetteSan。症狀是「對話中文、名字英文」。
由 `loadorder.txt` 決定，**與 modlist 優先度無關**，2026-08-28 的順序修復管不到。
`opus-apply-order` 與其子線各自獨立撞到同一件事。

**先請確認範圍**：進遊戲看 Lydia 的名字是不是英文，並留意還有沒有別的 NPC 中文名變英文
（上面四個是資料層查到的，不保證窮盡）。

**2026-09-05 實讀：本項仍然有效、對象還在。**
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/plugins.txt:629`＝`*JhNPCBeautyDev.esp`（**啟用**）、
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/loadorder.txt:688`＝`JhNPCBeautyDev.esp`。
注意它**不在 `modlist.txt` 裡**（`grep -i JhNPC` 對 modlist 零命中）——這是 MO2 mod 名與 plugin 名不同名造成的，
不是它沒安裝；查它要查 `plugins.txt`／`loadorder.txt`，別只查 modlist。
同一件事另有筆記 `/home/lorkhan/repo/moddings/skyrim/agentctl/status/todo/22-JhNPCBeautyDev帳本對不上.md`。

**兩條修法擇一**（dispatcher 2026-08-28 判定延後，理由是不在剛修好並 commit 的 load order 上
疊第二次改動、且當時沒有實機驗證窗口）：
- 調 `loadorder.txt` 把 `JhNPCBeautyDev.esp` 往前移 —— 簡單，但會讓它的**外觀**被別人蓋掉，
  而外觀正是這個 mod 的用途，等於本末倒置。
- 做一個小 patch plugin，把那幾筆 `NPC_` 的 `FULL` forward 回中文 —— 不動外觀，但要多一個插件名額。

傾向後者，但要等實機確認範圍後再定。

所有本頁項目共同檢查：無方框、mojibake、截斷、空白或新 crash；未走過的流程不得稱 gameplay PASS。

