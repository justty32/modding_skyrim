# RDO 的 FormList 投放機制

> 素材：`Relationship Dialogue Overhaul.esp`。
> ESP 文字 dump 在 `/tmp/mfdump/rdo.txt`（59418 行）；但 ModForge 的 `dump` 指令對 FormList **只印出 EditorID 一行、不展開成員**（FLST 走的是 catch-all 渲染，見 dump 第 58953–58970 行），所以 FormList 成員型別、IsInList condition 的參數（指向哪個 FormList、比較值 0 還是 1）都是用一支臨時 Mutagen 程式（載入 `Skyrim.esm`/`Update.esm`/`Dawnguard.esm`/`HearthFires.esm`/`Dragonborn.esm` 五個 master 解析 master 端 FormKey）離線解碼取得，本文所列數字與成員名皆來自該解碼結果。
> 本文聚焦 **FormList 這個子機制**；對話投放的總論（condition 串如何把台詞投到正確 NPC）見 `dialogue-targeting-technique.md`，兩篇互補、可互相引用。

---

<!-- wf-nav -->
- [0. 一句話結論](rdo-formlist-mechanism/formlist-inventory.md)
- [2. FormList 怎麼被 condition 引用](rdo-formlist-mechanism/condition-references-and-voice-types.md)
- [4. PreventedActors 排除機制](rdo-formlist-mechanism/exclusion-and-recipes.md)
