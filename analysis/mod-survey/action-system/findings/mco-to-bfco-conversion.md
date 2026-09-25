# MCO／ADXP moveset → BFCO 轉換

← [action-system 中樞](../README.md)｜相關：[BFCO](bfco.md)、[SCAR](scar.md)、[moveset 實例庫](movesets-examples.md)、[Payload Interpreter](payload-interpreter.md)、[OAR 指南](../oar-replacer-guide.md)

> **落點＝五層堆疊的第 4 層（招式框架）內部的框架遷移。** 第 0–3 層（XPMSSE／Pandora／BDI・PIE・AMR／OAR）
> 在 MCO 與 BFCO 底下**完全共用**，所以這不是「換一套動作系統」，而是**同一批 `.hkx` 換一個 attack framework 的 handle**。
>
> **一句話結論**：在現行版本（BFCO ≥ 3.3、converter ≥ 1.2.0）下，**MCO moveset 轉 BFCO 的必要動作只有「批次改檔名」**——
> annotation 不必改寫、OAR 條件不必改、不必重跑 Pandora／Nemesis。有現成工具
> （[MCO to BFCO Converter, mod 119926](https://www.nexusmods.com/skyrimspecialedition/mods/119926)），
> 而且 BFCO 官方頁明載「MCO annotations can also work with BFCO」。
>
> **授權已於 2026-08-27 逐字查證**（§4.1）：三筆爭議 moveset 的 `Conversion permission` 只禁「移植到別的遊戲」，
> **不涵蓋同遊戲內的框架轉換** → **私人本機轉換無障礙、再發布一律不可**。
> 所以剩下的真門檻只有兩個：**attack-speed 手感偏移**（要實機驗）與 **NPC 路／玩家路必須分開規劃**（§4.2）。

---

<!-- wf-nav -->
- [技術差異：MCO／ADXP vs BFCO](mco-to-bfco-conversion/technical-differences.md)
- [轉換步驟與來源](mco-to-bfco-conversion/conversion-steps-and-sources.md)
- [現成工具與轉換邊界](mco-to-bfco-conversion/tools-and-boundaries.md)
- [成本判定、實機驗收與待處理事項](mco-to-bfco-conversion/costs-and-validation.md)
