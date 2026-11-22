## VIGILANT 1.8.2 正體中文

現役已是 exact 1.8.2，45 筆 `BOOK.DESC` 私人 text-only layer 亦已升版。到晨星城風岳旅店找
Altano，抽查主線開場、對話／字幕、日誌／目標、書籍、物品／效果、MCM，至少打開一件「石之碎片」
確認描述為正體。英／日配音保留；作者檔與私人修正不公開重發。

agent 2026-11-22 已觀測：阿爾塔諾在**晨星城風岳客棧**（DawnstarWindpeakInn），開場兩層對話「你們是在招募斯丹達爾的警戒者嗎？」→「好，請讓我加入你們。／不需要，謝謝。我對這沒興趣。」是正體、沒方框；「石之碎片：警戒者阿爾塔諾」物品名正體。截圖 `agentctl/handoffs/home-2026-11-22/waituser-runtime/shots/S3-altano-0.jpg`、`S3-altano-1b.jpg`——請看一眼；日誌／目標、書、碎片描述、MCM 要開選單，仍要你看。

## 2026-08-20 任務內容批

抽查 UNSLAAD 3.0.6b、Missives 2.03、DAc0da 1.1.0b、GLENMORIL 0.96.80b 的 MCM／任務入口、
~~正體~~**中文**日誌／對話／字幕、語音與跨 worldspace。GLENMORIL 語音覆蓋 3,653/4,792，UNSLAAD 英語語音
只涵蓋 Act 1；Silent Voice 是接受狀態。證據見
`quest batch`（已刪：`agentctl/logs/quest-content-batch-2026-08-20.md`）與
`final smoke`（已刪：`agentctl/logs/modpack-kr-final-smoke-2026-08-21/RESULT.md`）。

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

所有本頁項目共同檢查：無方框、mojibake、截斷、空白或新 crash；未走過的流程不得稱 gameplay PASS。
