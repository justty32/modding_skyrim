# 遊戲行為異常（非崩潰）的歸因

[lessons 索引](README.md)

不會 CTD、但玩起來不對勁的症狀：攻速、交易結算、戰鬥輸入。這類靜態掃描常常找不到元兇，靠的是「使用者實機一次停一個」的對照實驗。崩潰類在 [crash-dll-and-scripts](crash-dll-and-scripts.md)／[crash-data-and-assets](crash-data-and-assets.md)。

## carp-rightweaponspeed-counter-bug

> 玩家近戰全變慢＝CARP 1.1.5.1 右手攻速計數累積（getav WeaponSpeedMult 負數）；重開遊戲清除，使用者裁不根治

2026-10-07 玩家全部近戰（含空手）約 0.5 倍速；`player.getav WeaponSpeedMult`=-2.75、Left=1.25。真因（約七成）是 CARP（Comprehensive Attack Rate Patch 1.1.5.1）在記憶體記右手攻速計數，只在角色物件建立時歸零、遊戲內讀檔不清、扣回有漏洞；<0.5 一律壓 0.5（fMinWeaponSpeed）。腳本面全掃無元兇。報告 `agentctl/handoffs/home-2026-10-07/meleeslow/REPORT-accum.md`。

**Why:** 使用者裁示「不根治，這樣就好」——不 fork 重編 CARP。

**How to apply:** 再報攻擊變慢先請他查 `getav WeaponSpeedMult` vs Left；解法是存檔→退桌面重開→讀檔，仍異常才 `player.modav WeaponSpeedMult <差值>`；別用 forceav（重開後會多出計數）。目標值等於左手值，不是 0。

## unstack-stolen-items-eats-sale-gold

> 賣東西物品被收走但金幣沒入帳（買正常）＝Unstack Stolen Items 2.0.4 DLL；10-09 對照實驗定罪，已停用

2026-10-09 使用者回報賣東西拿不到錢（每個商人、舊 41 級角色也一樣；價格顯示正常、買東西正常）。靜態掃描找不到元兇，對照實驗停用 Unstack Stolen Items（09-05 裝，hook 背包物品合併，金幣入帳正好走這步）後錢就進來了。profiles `4f5f03a` 停用；報告 `agentctl/handoffs/home-2026-10-09/barter/REPORT-barter.md`。

**Why:** 靜態證據不足時，使用者實機一次停一個的對照最快；先看「賣價有沒有數字／買是否正常」把顯示問題與結算問題切開。

**How to apply:** 別再裝回 Unstack Stolen Items；之後若有其他 hook 物品合併／AddObjectToContainer 的 DLL 出現交易或撿物異常，先懷疑這類。

## valhalla-block-commitment-eats-release

> 精準格擋後左鍵打不出、要盾擊才解＝Valhalla Combat 1.3.3 Block Commitment 吞掉右鍵放開；MCM「开启招架」關掉即解

2026-10-18 使用者實機確認：Valhalla Combat 1.3.3 的 Block Commitment（`bBlockCommitmentToggle`，中文 MCM 誤譯為「招架系统／开启招架」）在右鍵 <0.3 秒放開時延遲補送 release，補送時不在格擋就丟掉，玩家卡在格擋狀態。修法：MCM 關掉該開關（寫進 `overwrite/MCM/Settings/ValhallaCombat.ini`），不動 profile。精準格擋開關是另一個 `bTimedBlockToggle`，要留著。

**Why:** 上游 GitHub HEAD 有補 blockStop 但未發 Nexus，更新也修不到。

**How to apply:** 重灌／換 overwrite 後若復發，先查這個值；報告在 `agentctl/handoffs/home-2026-10-18/block-attack-lock/REPORT.md`。
