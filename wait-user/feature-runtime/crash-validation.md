## 2026-09-20：PI 啟動崩潰候選層與技能條件 crash 驗證

2026-09-24 **結案**：doom perk 補丁（移除三顆 `doom*Perk` 的 `EPModSkillUsage_AdvanceObjectHasKeyword` 條件）已部署正式 `modpack-main`（profiles `3f5c37d`），**使用者實機格擋確認不再崩潰，第 6 條 PASS**。09:16／09:34 兩次都是使用者格擋時崩潰、並非靜置重現——靜置不算證據。見 [doomperk 報告](../../agentctl/handoffs/home-2026-09-24/doomperk/REPORT.md)。

## 2026-09-24：長毛象 CTD（`SkyrimSE+02B789A`）

2026-09-25 **結案**：SPID-NoElderOutfit-2026-09-24 覆寫層部署後，使用者實機回到 cell grid (-6,1) 巨人營地確認不再崩潰（使用者 21:50 口頭確認）。

10:23 野外巨人營地（cell grid (-6,1)）CTD，崩在背景載入執行緒的 3D 掛載路徑，現場 `QueuedCharacter` / `BSFadeNode "skeleton.nif"`，RDI 是長毛象 `[ACHR:001038A9]`；崩潰前 2.4 秒 SPID Outfit Manager 對**同一個 ACHR** 做了 `Resetting inventory`。已部署覆寫層 `SPID-NoElderOutfit-2026-09-24`（profiles `f106cf3`），活體 inventory reset 由 75 降到 0。**待使用者回到該營地實機走一趟確認**；煙霧不崩不構成修復證明。見 [spid-outfit 報告](../../agentctl/handoffs/home-2026-09-24/spid-outfit/REPORT.md)與 [證據鏈](../../agentctl/handoffs/home-2026-09-24/block-crash2/REPORT.md)。

**open（cx-crash2／lead-fde920）**：PI 合併層已建立但停用（profiles `0cd417d`）；待使用者決定啟用及冷啟動 A/B。B 型 `SkyrimSE+01D3398` 仍未定罪，待原場景動作／法師立石持有狀態確認與 CARP 單 DLL A/B。不得同時改兩型變量，不能把靜態 gate 當實機已修復。詳見 [REPORT](../../agentctl/handoffs/home-2026-09-20/crash2/REPORT.md) 與 [操作步驟](../../agentctl/handoffs/home-2026-09-20/crash2/FIX-AND-AB.md)。

> **2026-09-05 核對結論（todo-23）**：Simonrim 時代的 Batch 4E／4A／4M/P 三節，
> **抽樣對象逐個實讀後全部仍在啟用清單裡，三節都不作廢**——過期的是行號與框架名（BFCO→MCO），不是清單。
> 只有 4E 的「AVE loot/vendor 階級比例」與 4M/P 的「BFCO 攻擊」兩個子條件因對象停用而作廢，已就地標註。
> 判準：`modlist.txt` 以 `+` 開頭＝啟用、`plugins.txt` 以 `*` 開頭＝啟用（檔案是 CRLF，比對前 `tr -d '\r'`）。
> 核對來源：`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/{modlist.txt,plugins.txt}`
> （`instance/profiles` main `5f47044`）。

