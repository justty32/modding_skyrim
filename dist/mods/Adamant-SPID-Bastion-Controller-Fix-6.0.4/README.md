# Adamant 6.0.4 SPID Bastion Controller Fix

Adamant 6.0.4 的最小化 SPID 設定修正。

官方 MAIN 檔的 `Adamant_DISTR.ini` 要把 NPC 版 Bastion controller perk 分發給演員，
但設定使用不存在的 EditorID `MAG_BastionNPC`。官方 `Adamant.esp` 6.0.4 實際提供的記錄是
`MAG_BastionControllerPerkNPC`（`23284B:Adamant.esp`）。SPID 因此在 lookup 階段回報
`FAIL - editorID doesn't exist`，並跳過這一條分發。

本包完整保留官方 `Adamant_DISTR.ini`，只把該 EditorID 改成實際存在的名稱。沒有 ESP、
腳本、資產、額外規則或其他 gameplay 修改。

## 安裝契約

- 需要 Adamant 6.0.4 MAIN 與其正式依賴。
- 在 MO2 左側讓本包高於 Adamant 本體，使本包的 `Adamant_DISTR.ini` 成為 VFS winner。
- 不需要 Blade and Blunt addon；這筆 NPC controller perk 位於 Adamant 6.0.4 MAIN。
- 回滾只需停用本包，官方設定檔會立刻重新成為 winner。
