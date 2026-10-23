## 2026-09-24：長毛象 CTD（`SkyrimSE+02B789A`）—— 2026-10-23 重新開啟

**原文寫的「2026-09-25 結案」是誤判，本項重新 open。** 09-25 那次「實機回巨人營地沒崩」只是沒踩到，不是修好了。

**已排除 SPID（有實證，不必再查這條線）。** 09-27 10:51 同簽章復發，受害者換成巴巴斯
`DA03BarbasRef [ACHR:00052535]`（荒野 cell），call stack 前 10 層與 09-24 一個不差；而當時覆寫層
`SPID-NoElderOutfit-2026-09-24` **已啟用且壓在 CT77 之上**（profile commit `d051485`，09-25 23:11，
是 09-27 遊玩前最後一版）——修法在位，照樣崩。更根本的是，「`Resetting inventory` ＝ SPID 動了活體」
這個前提本身就錯：讀上游原始碼（powerof3/Spell-Perk-Item-Distributor，`SPID/src/Outfits/`，main `6e66908`），
`ProcessResetInventory` 只是先印那行 log 再照原樣呼叫原版函式，`SetOutfit`／`ApplyOutfit` 開頭就是
`if (!npc->defaultOutfit) return false;`，而長毛象 `EncMammothTamedNoAggro` 的 DefaultOutfit 已確認是 null，
那行 log 記的是**原版引擎自己在 reset**。連帶地，09-24 用的「活體 reset 75 → 0」A/B 指標也站不住：
10-02 那場覆寫層照樣生效，SPID log 仍有 20,572 次 `Resetting inventory`、牽涉 11,367 個 ACHR，
09-24 的 `after=0` 只是短煙霧樣本太小。以上見 [c0927 報告](../../agentctl/handoffs/done/2026-10/home-2026-10-03/crash/c0927/REPORT.md)
`:9`／`:11`／`:13`-`:16`。

**也排除 09-30 那批部署**：崩潰比部署早三天（同報告 `:5`）。

**不要跟 10-09 那兩次併案**：10-09 的 `SkyrimSE.exe+02CF964`（與同日 10:05 的 `+02BA440` 同型，
`CellLoaderTask` 上的 MovableStatic 懸空指標，嫌疑指向被 BOS 換成動畫版的浮冰）是**不同簽章、不同函式**，
報告已明寫「跟 +02B789A 不同址……不能當作同一個 bug」。見
[10-09 crash2](../../agentctl/handoffs/done/2026-10/home-2026-10-09/crash/REPORT-crash2.md)`:38`、
[10-09 crash1](../../agentctl/handoffs/done/2026-10/home-2026-10-09/crash/REPORT-crash.md)`:27`。

**真兇未明。** 目前只能說是「背景執行緒載入生物 3D 的原版碼路徑」（`QueuedCharacter`／`IOManager`／
兩個 `BSFadeNode "skeleton.nif"`，rcx=0，讀 0x130），兩次受害者都是**野外四足生物**。
09-27 當天各 SKSE DLL 的 log 已被 10-02 那場覆蓋、沒保存下來，所以查不下去。

**覆寫層怎麼處置由你決定**：`SPID-NoElderOutfit-2026-09-24` 留著或撤掉對這個 CTD 都沒影響（撤掉＝老年 NPC 換回 CT77 衣服）。

**下次再崩，這一項真正等你的兩件事**

1. **開 MO2 之前**先把整個 SKSE log 目錄原樣打包一份（照 crash-1101 的 preserved 做法）。只要先開 MO2，各 DLL 的 log 就被蓋掉，等於放棄這次機會。
2. 回報崩潰當下在做什麼：剛快速旅行落地、騎馬／衝刺跑過野外，還是剛讀檔；現場有沒有野生四足生物、有沒有正在跟隨的狗。

原始推論鏈（保留作教訓，結論已推翻）見 [spid-outfit 報告](../../agentctl/handoffs/done/2026-09/home-2026-09-24/spid-outfit/REPORT.md)與 [證據鏈](../../agentctl/handoffs/done/2026-09/home-2026-09-24/block-crash2/REPORT.md)。

> **2026-09-05 核對結論（todo-23）**：Simonrim 時代的 Batch 4E／4A／4M/P 三節，
> **抽樣對象逐個實讀後全部仍在啟用清單裡，三節都不作廢**——過期的是行號與框架名（BFCO→MCO），不是清單。
> 只有 4E 的「AVE loot/vendor 階級比例」與 4M/P 的「BFCO 攻擊」兩個子條件因對象停用而作廢，已就地標註。
> 判準：`modlist.txt` 以 `+` 開頭＝啟用、`plugins.txt` 以 `*` 開頭＝啟用（檔案是 CRLF，比對前 `tr -d '\r'`）。
> 核對來源：`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/{modlist.txt,plugins.txt}`
> （`instance/profiles` main `5f47044`）。

