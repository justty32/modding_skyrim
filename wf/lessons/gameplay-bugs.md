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

2026-10-09 症狀：賣東西拿不到錢（每個商人、舊角色也一樣；價格顯示正常、買東西正常）。靜態掃描找不到元兇；Unstack Stolen Items hook 背包物品合併，金幣入帳正好走這步，對照實驗停用它後錢就進來了。profiles `4f5f03a` 停用；報告 `agentctl/handoffs/home-2026-10-09/barter/REPORT-barter.md`。

**Why:** 靜態證據不足時，使用者實機一次停一個的對照最快；先看「賣價有沒有數字／買是否正常」把顯示問題與結算問題切開。

**How to apply:**
- 別再裝回 Unstack Stolen Items；之後若有其他 hook 物品合併／AddObjectToContainer 的 DLL 出現交易或撿物異常，先懷疑這類。
- 收到「賣東西／買賣沒拿到預期結果」回報，先排除原版機制再往 mod/DLL 查——`sNotEnoughVendorGold` 商人錢不夠會跳確認框、低價物品賣出本來就是 0 金（2026-10-23）。最小對照實驗：記物品卡價格 P、賣前金幣 A、賣後金幣 C；C=A+P 才正常，C=A 才值得往 mod 查，不要一開始就翻 SKSE log（`agentctl/handoffs/done/2026-10/home-2026-10-09/barter/REPORT-barter.md`）。

## valhalla-block-commitment-eats-release

> 精準格擋後左鍵打不出、要盾擊才解＝Valhalla Combat 1.3.3 Block Commitment 吞掉右鍵放開；MCM「开启招架」關掉即解

2026-10-18 使用者實機確認：Valhalla Combat 1.3.3 的 Block Commitment（`bBlockCommitmentToggle`，中文 MCM 誤譯為「招架系统／开启招架」）在右鍵 <0.3 秒放開時延遲補送 release，補送時不在格擋就丟掉，玩家卡在格擋狀態。修法：MCM 關掉該開關（寫進 `overwrite/MCM/Settings/ValhallaCombat.ini`），不動 profile。精準格擋開關是另一個 `bTimedBlockToggle`，要留著。

**Why:** 上游 GitHub HEAD 有補 blockStop 但未發 Nexus，更新也修不到。

**How to apply:** 重灌／換 overwrite 後若復發，先查這個值；報告在 `agentctl/handoffs/home-2026-10-18/block-attack-lock/REPORT.md`。


## mod-compatibility-silent-failure-modes

> conflict tree／FormID／功能名稱這類表層檢查都有盲區

- FormID 不同不算衝突：各自新增不同 FormID 對話，conflict tree 不標紅但條件可能同時成立雙重觸發（`cx-serana`）。
- 改 VoiceType 噎死別人新對話：IFD 改 Lydia VoiceType 害 FDE 上千行新對話整批靜音，疊 VoiceType 救不回（`cx-compat`）。
- 同觸發點 perk 只一個生效：多 mod 命中附加效果 perk 掛同一 hit-trigger，其餘靜默失效（`n4batch`）。
- 功能名稱不代表衝突：Valhalla stun 與 CPR/B&B poise 掛不同 hook（`chocolate-poise`）。
- 外觀 replacer 會把戰鬥改造蓋回原版：replacer 以原版 NPC 為底整筆覆寫 NPC_／ARMO，排在戰鬥 mod 後面時，等級曲線、perk、法術、背包、AI 包、甚至中文名都退回原版（2026-10-26 Remiel：perk 39→5、法術 5→2、等級 ×1.0／20／無上限→×0.7／5／120；`agentctl/handoffs/home-2026-10-26/remiel/REPORT.md`）。

**Why:** 根因各不同，共同點是表層檢查看不出來。

**How to apply:** 列雙方新增內容找同時成立條件；共用資料源逐一查；框架類 mod 確認配實作；名稱像不像不算數要讀 hook 點。NPC 有戰鬥改造又有外觀 replacer 時，用 `instance/tools/whichmod.py <FormKey> --chain` 看最後贏家；贏家是純外觀 mod 就做合併層（戰鬥欄位取戰鬥 mod、RNAM／WNAM／PNAM／tint 等外觀欄位取 replacer），實機驗 perk 前要先走到她身邊讓 3D 載入，否則 `hasperk` 一律回 0。


## proton-shared-nvidia-shader-cache-stutter

> 多 Proton 遊戲共用同一個 NVIDIA shader 快取目錄會互擠造成卡頓

2026-10-04：Skyrim 用 sniper+Proton 沒設 `__GL_SHADER_DISK_CACHE_PATH`，快取寫全機共用 `~/.cache/nvidia/GLCache/`；同日 Helldivers 2 也沒設專屬路徑寫入同快取檔，接近常見 1 GiB 上限，可能互擠已編譯 shader 致重編卡頓。沒 frametime 時 log 只證明「有這件事」非「那次卡」，靠 HUD 與 mtime 才把尖峰實錘成 shader 編譯。`agentctl/handoffs/done/2026-10/home-2026-10-04/stutter/REPORT.md`

**Why:** Proton 遊戲沒有獨立快取路徑；量化證據比 log 時間更能定因果。

**How to apply:** 懷疑卡頓先查 GLCache 有無其他 Proton prefix 同時段活動；單一遊戲變數改在 `launch-mo2.sh` export 後 exec，不寫全域 environment.d；沒 frametime 的結論標嫌疑非真因。
