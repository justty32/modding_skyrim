# 大規模對話如何精準投放：RDO 的 condition 投放技術 — condition-overview

[返回入口](../dialogue-targeting-technique.md)

## 0. 核心矛盾

Skyrim 全境有上萬個 NPC，而 RDO 只有**一份 ESP**。它沒有、也不可能為每個 NPC 各寫一份台詞。它要解決三件事：

1. **精準**：一句台詞只出現在「該說它的 NPC」嘴裡。
2. **不重複**：同一個 NPC 不會每次都講同一句。
3. **動態**：台詞語氣隨「NPC 與玩家的關係」變化。

答案全在每一筆 `DialogResponses`（INFO record）後面掛的那一串 **condition function**。condition 是一組布林判斷，**全部為真**這句台詞才有資格被選中。本質上 RDO 不是「指定 NPC」，而是**描述一組篩選條件**，讓引擎在執行期把符合的 NPC 撈出來。

dump 中 RDO 自製的 `DialogResponses` 有 **6650 筆**（`grep -c 'Relationship Dialogue Overhaul.esp] DialogResponses'`），覆寫 vanilla 的另有 1268 筆——靠的全是這套 condition 篩選機制，而非逐一指名。

## 1. condition 頻率全景

`grep -oE 'condition: [A-Za-z]+' /tmp/mfdump/rdo.txt | sort | uniq -c | sort -rn | head -25`：

本表彙整「condition-frequency」的原始記錄。已抽到 [condition-overview-condition-frequency.json](condition-overview-condition-frequency.json)（25 列）。

次數：原表「次數」欄值。

condition function：原表「condition function」欄值。

投放維度：原表「投放維度」欄值。

統計：25 列，3 欄。

> 一個值得注意的限制：本 dump 只對 `GetIsID` / `GetInFaction` 等「指向某 record」的 condition 印出 `-> FormID`（例：`condition: GetIsIDConditionData -> 000007:Skyrim.esm` 指 PlayerRef）。`GetRelationshipRank`、`GetRandomPercent` 等的**比較運算子與數值**未在此 dump 格式中列出，本文對其閾值的描述為依據 CK 慣例與台詞語意的合理推斷，並已標明。

最關鍵的一個對比：**GetIsVoiceType（9245）vs GetIsID（1396）**。RDO 壓倒性地偏好「按嗓音類別投放」，指名單一 NPC 只佔約六分之一——這就是「一份 ESP 覆蓋上萬 NPC」的根本手法。

