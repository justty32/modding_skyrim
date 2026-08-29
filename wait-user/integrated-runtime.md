# 整包 UI／中文／任務驗收

## EnaiRim Batch 7 終態 gate

等 Batch 1–6 施工後，確認 Audugan／Valravn private CHT 與新文字層顯示；shrine／standing stone／
High Hrothgar candidates 無穿插且可互動；Valravn 搭 BFCO／Precision／TDM／TK Dodge／WYT 的輸入、
多人節奏、武器速度、耐力與命中手感；抽查 race／faith／spell／enchantment／shout UI。固定範圍見
[`Batch 7 計畫`](../agentctl/logs/simonrim-to-enairim-final-selection-2026-08-24/batch-7-integration-promotion-plan.md)。

## Modpack-KR Batch 6 final gameplay

自動 lane 21/21 PASS、`load_epoch 1 → 2`、0 new crash 不能代替真人。需驗新遊戲、城市／NPC、BFCO、
Mysticism／Adamant、CT77／AVE、RDO、VIGILANT Altano 入口／字幕／語音、
自然跨 worldspace、MCM 與 description overlay 書。VIGILANT 四層須同版 1.8.2；Silent Voice 缺口已
接受、不需 TTS。證據見 [`Batch 6 RESULT`](../agentctl/logs/modpack-kr-final-smoke-2026-08-21/RESULT.md)。

## 四個首次生效中文層

抽查 Timing is Everything SE 2.2 MCM、The Choice is Yours 2.7 接受／拒絕對話、At Your Own Pace
8 ESP 推進選項、SkyParkour 3.6.2 `Interface/Translations` UI；確認無方框、mojibake、截斷、空白。
排序稽核：`mod-library/l10n/tools/` 的層優先權稽核。

## RDO Final 正體中文

離線 topology、文字與 script-binding gates 已過；抽查關係對話／字幕、任務／通知、賄賂金額、
Gelebor／Isran／Valerica 等待／離隊通知，確認無方框、亂碼、空白、未替換 token、截斷、新 crash。
範圍見 [`layer README`](../mod-library/l10n/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/README.md)。

## VIGILANT 1.8.2 正體中文

現役已是 exact 1.8.2，45 筆 `BOOK.DESC` 私人 text-only layer 亦已升版。到晨星城風岳旅店找
Altano，抽查主線開場、對話／字幕、日誌／目標、書籍、物品／效果、MCM，至少打開一件「石之碎片」
確認描述為正體。英／日配音保留；作者檔與私人修正不公開重發。

## 2026-08-20 任務內容批

抽查 UNSLAAD 3.0.6b、Missives 2.03、DAc0da 1.1.0b、GLENMORIL 0.96.80b 的 MCM／任務入口、
正體日誌／對話／字幕、語音與跨 worldspace。GLENMORIL 語音覆蓋 3,653/4,792，UNSLAAD 英語語音
只涵蓋 Act 1；Silent Voice 是接受狀態。證據見
[`quest batch`](../agentctl/logs/quest-content-batch-2026-08-20.md)與
[`final smoke`](../agentctl/logs/modpack-kr-final-smoke-2026-08-21/RESULT.md)。

所有本頁項目共同檢查：無方框、mojibake、截斷、空白或新 crash；未走過的流程不得稱 gameplay PASS。

## modlist 優先度修復的實機驗收（2026-08-28 套用，待驗）

2026-08-28 已把 `modlist.txt` 從事故後的名稱序重建為正確優先度並 commit（377 行／318 啟用；
winner 差異 5485→5；Pandora Output 重新壓過 TK Dodge RE；9 個被本體壓掉的中文層全回復），
資料層由 houseCARL 實查 Ordinator 天賦、ESW 武器名、AI Overhaul NPC 名、Sofia 皆已回中文。
**還沒進遊戲驗**。請用 `launch-mo2.sh` 開 MO2 確認 Active 318 → 進遊戲**離開存檔重進**，驗：
第三人稱能否正常攻擊（原症狀：BFCO 行為圖被 vanilla 壓掉）、Ordinator 天賦頁是否中文、
武器名是否中文。證據見 [`opus-apply-order`](../agentctl/handoffs/opus-apply-order-2026-08-28/)
與 [`根因`](../agentctl/logs/modlist-priority-bug-2026-08-23.md)。

## JhNPCBeautyDev 蓋掉 NPC 中文名（2026-08-28 發現，待裁示）

`JhNPCBeautyDev.esp` 在**插件層**覆蓋數個 NPC 的 `FULL`，把中文名寫成英文，已確認的有
**Lydia**（`override_depth=4`）、Bryling、Erdi、EvetteSan。症狀是「對話中文、名字英文」。
由 `loadorder.txt` 決定，**與 modlist 優先度無關**，2026-08-28 的順序修復管不到。
`opus-apply-order` 與其子線各自獨立撞到同一件事。

**先請確認範圍**：進遊戲看 Lydia 的名字是不是英文，並留意還有沒有別的 NPC 中文名變英文
（上面四個是資料層查到的，不保證窮盡）。

**兩條修法擇一**（dispatcher 2026-08-28 判定延後，理由是不在剛修好並 commit 的 load order 上
疊第二次改動、且當時沒有實機驗證窗口）：
- 調 `loadorder.txt` 把 `JhNPCBeautyDev.esp` 往前移 —— 簡單，但會讓它的**外觀**被別人蓋掉，
  而外觀正是這個 mod 的用途，等於本末倒置。
- 做一個小 patch plugin，把那幾筆 `NPC_` 的 `FULL` forward 回中文 —— 不動外觀，但要多一個插件名額。

傾向後者，但要等實機確認範圍後再定。
