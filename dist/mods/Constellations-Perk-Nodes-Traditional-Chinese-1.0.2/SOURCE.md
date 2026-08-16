# Source provenance

- 目標版本：Constellations 1.0.2。
- 原始 `ConstellationsNewSkills.esp` SHA-256：`500fefc8f5cd15fa3c3caf34493a954013c93246c7fdebb343f699c7a3039baa`。
- 44 筆 winning PERK 的固定英文轉送來源 patch SHA-256：`facddcde7c8770b4694f866d2d3ab1442088603d1d0c64955544e416a5bb451d`。
- 來源 patch masters：`Skyrim.esm`、`Update.esm`、`ConstellationsNewSkills.esp`。

目標集合是 `000163`–`00018F:ConstellationsNewSkills.esp`，唯獨排除 `00017D` (`CNS_H2H_AutoPerk`)。這涵蓋技能樹實際顯示的 27 個節點與其全部 17 個後續 rank。

`tools/translation-source.tsv` 保存每筆 FormKey、EditorID、英文原文及繁中譯文。建置器會逐筆核對英文 `FULL`／`DESC` 後才生成 localized ESP，來源版本或文字不符就拒絕建置。
