# CTD：SKSE DLL 與腳本

[lessons 索引](README.md)

**崩了先跑 snapshot 再開 MO2**：`agentctl/tools/snapshot_skse_logs.sh`（SKSE/、Skyrim.INI/SKSE/、ini、Papyrus 複製到 `~/skyrim_mods/_crash-snapshots/<時間>/`＋MANIFEST）；下一場會蓋掉各 DLL log，09-27 的就是被 10-02 蓋掉。

## upstream-skse-dll-fix-via-fork-ci

> SKSE DLL 的上游 bug 可以自己修：crash log 帶原始碼行號時直接讀 GitHub 原始碼定罪，fork 後靠 repo 自帶的 GitHub Actions 編譯，不需要本機 Windows 工具鏈（原 type: project）

2026-09-25 Constellations CTD 走通的流程，之後遇到 SKSE 外掛的上游 bug 都照這條走。

**定罪**：CrashLoggerSSE 會把 PDB 的原始碼路徑與行號印在 crash log 第一行
（`... Constellations.dll+0023374 mov rax, [rcx] | D:\source\...\SorceryPerks.cpp:168 ...`）。
用 `gh api -X GET search/code -f q='<函式名>'` 找到 repo，把那個檔案抓下來對行號。
`SorceryPerks.cpp:168` 是 `a_caster->currentSpell->GetSpellType()`，`currentSpell` 沒守 null，
與 `mov rax, [rcx]` / `rcx=0`（虛函式讀 vtable）完全吻合。**這是定罪不是推測。**

**修**：`gh repo fork` → 用 contents API 直接 PUT 改好的檔案（不必 clone，省掉數 GB 子模組）→
repo 若有 `.github/workflows/build.yml` 就 `gh workflow run ... --ref main`（fork 的 push 事件不會自動觸發）→
`gh run download` 拿產物。Constellations 這次 5 分半編完。

**換版本基底要先比 `src/`**：1.0.2 那棵樹沒有 CI workflow，所以從 main(1.0.3) 建。
先用 `gh api repos/X/Y/compare/<a>...<b>` 確認 `src/` 零改動，才敢說「同一份程式碼」。

**裝之前必看兩件事**：
1. `.pdb` 要跟 `.dll` 一起換。只換 DLL 的話，以後的 crash log 會用舊符號表標新二進位，行號全錯。
2. 用 `objdump -p` 找 `SKSEPlugin_Version` 的 RVA，手動解 PluginVersionData 比對新舊的
   `versionIndependence` 與 `compatibleVersions`。兩者相同（本次都是 `0x5`、compat 空＝走 Address Library）
   就代表載入判定路徑一樣，跨版本風險比想像小。

**驗收點**：`skse64.log` 的 `plugin X.dll (00000001 X <版本>) loaded correctly` 那一行版本號要變，
且 `loaded correctly` 總數不變。這兩條是硬證據，比「沒崩」有力得多。

相關：[[pepe-tls-end-crash-is-payloadinterpreter-dangling-listener]]、[[doomperk-advanceobject-block-ctd]]

## pepe-tls-end-crash-is-payloadinterpreter-dangling-listener

> 啟動 65–70 秒炸在 PerkEntryPointExtender.dll+025FA30 _tls_end 的 crash，真因是 PayloadInterpreter.dll 載入間歇失敗留下死 listener；重開 MO2 等它載完再 Run 即可（原 type: project）

2026-09-17 開機後兩次啟動 crash（20:22、20:25），簽名 `PerkEntryPointExtender.dll+025FA30 _tls_end`，uptime 65–70 s，crash log 只有 28k；09-13 08:33 同簽名。skse64.log 關鍵行：`plugin PayloadInterpreter.dll ... disabled, fatal error occurred while loading plugin 0 (handle 75)`，但它已登記 listener slot 75；SKSE 送 PostLoad（message type 0）到 slot 75 時打進已卸載位址，該位址現由 PEPE 佔據，所以「炸在 PEPE」。PEPE 無辜。

Opus 唯讀查證（09-17）：PI config 全是 .ini（54 檔／40 個 MCO 動作 mod），09-12 後零變動，DLL 全機只一份（v1.0.0，md5 b6c50a27…）。第三次啟動同一批檔案就 `loaded correctly`。判定 intermittent usvfs：PI 的 Load() 對 40 個 mod 合併出的 `Data/SKSE/PayloadInterpreter/Config` 跑不帶 error_code 的 directory_iterator，列舉一失敗就 throw。

**Why:** 看 crash log 第一眼會怪 PEPE；真線索在 skse64.log 的 `disabled, fatal error` 行與 listener slot 編號對應。

**How to apply:** 看到這個簽名先 grep skse64.log 的 `disabled, fatal error`，對 slot 編號；處置是重開 MO2、等列表載完再 Run，不要改 DLL。同場「cannot start skse64 / Error 87」是 MO2 剛崩完孩子後 usvfs 抽風，也是重開 MO2。若一再復發，持久修法：把 40 個 mod 的 `SKSE/PayloadInterpreter/Config/*.ini` 收成單一合併 mod；順手清 `91-189376-BFCO-I-MCO-AshinFencer/SKSE/PayloadInterpreter/Config/新建文件夹/`（非 ASCII 目錄＋壞語法副本，PI 不遞迴讀不到，無害但該清）。相關：[[custom-navm-combat-pathing-ctd]]（先查 SKSE DLL 再怪別的）、[[launch-skyrim-via-steam]]（開機後 Steam 沒起來 SKSE 會 0-byte log 秒退，是另一種症狀）。

**2026-09-20 補**：第 4 次（07:39，log 只有 28 KB 是此型特徵；B 型 112 KB 級）。持久修法成品 `PayloadInterpreter-Config-Consolidated-Dev-2026-09-20`（52 INI 合併、原檔 hash 未變）09-20 14:00 已啟用（cx-pion 三次啟動全過，進觀察期）。此型 crash 後 skse64.log 會被下次啟動覆蓋，要定案得先把它 copy 走。
另一型 **B：`SkyrimSE+01D3398` READ 0x9E42**，帶 Constellations `Sorcery` 關鍵字、owning perk `doomMagePerk 0E5F49`（ConstellationsNewSkills 贏），跟 cell／遊玩時長無關；09-20 11:05 與 13:12 兩次。**2026-09-24 結案，與 PEPE／CARP 都無關**：真因是 `doomMagePerk` 等三顆 perk 在 `ModSkillUse` 掛 `EPModSkillUsage_AdvanceObjectHasKeyword`，格擋等非物件推進會 deref 垃圾指標，補丁已實機驗證，見 [[doomperk-advanceobject-block-ctd]]。`crash-ab-carp` 測試 profile 2026-10-03 已封存到 `instance/profiles/.repo/retired/`（要再用就 git mv 回根目錄並加進 check_profiles 白名單）。證據 `agentctl/handoffs/home-2026-09-20/crash2/REPORT.md`。

## spid-outfit-manager-live-inventory-reset-ctd

> 2026-09-24 長毛象 CTD +02B789A 真因是 SPID Outfit Manager 對活體 reset inventory 觸發 3D 重掛載；call stack 沒有 SKSE DLL 不代表 SKSE DLL 無關（原 type: project）

2026-09-24 10:23 野外走路（巨人營地，cell grid `(-6,1)`）CTD，簽章 `SkyrimSE.exe+02B789A  mov rcx,[rcx+0x130]`、rcx=0，全機首見。崩在**背景載入執行緒**（frame 10-11 是 kernel32/ntdll 進入點），現場 `QueuedCharacter` / `IOManager` / `BSFadeNode "skeleton.nif"`，RDI = 長毛象 `[ACHR:001038A9]`。

真因鏈：崩潰前 **2.4 秒** SPID 對**同一個 ACHR** 做了 `[🧥] Resetting inventory`。SPID v7.3.2.16 的 Outfit Manager 開機就裝了 `ShouldBackgroundClone` / `Load3D` / `Resurrect` / `ResetInventory` hook —— 正是崩潰所在那條路。使用者目視確認長毛象模型正常 → 排除壞網格，是**已在場的 actor 被重新掛載 3D** 跟背景載入佇列對撞。

驅動者只有一支：`CT77 Remodeled Armor ...` 的 `ElderOutfit_DISTR.ini`（全 load order 唯一的 outfit 分配）。為了讓老年 NPC 換裝，SPID 把整個場景的活人活獸都 reset 一輪。修法＝空檔覆寫層 `SPID-NoElderOutfit-2026-09-24` 壓在 CT77 之上（modlist 1308）。SPID 7.3.3 changelog 無 outfit manager 修正，升級無用。

**Why:** 兩個會重複踩的誤判 ——
(1) **call stack 全是原版碼、沒有 SKSE DLL，不等於 SKSE DLL 無關**：hook 是 trampoline，跑完跳回原版碼就不留名字。要改看該 DLL 的 log 有沒有在崩潰前幾秒動過同一個 FormID。
(2) **`Resetting inventory` / `Resurrecting` 的總次數會被遊玩時長汙染**（32 分鐘實玩 vs 短煙霧），不能當 A/B 指標。

**How to apply:** SKSE plugin 的嫌疑要用「崩潰前數秒 log 裡有沒有同一個 ACHR/FormID」來定罪，不是看 call stack 有沒有它。SPID 這類 A/B 的指標用**活體 reset**＝被 `Resetting inventory` 但沒有配對 `Resurrecting` 的 ACHR 數（有配對的是屍體復活重配，屬另一類）——本案 before 75、after 0，不吃時長。相關：[[doomperk-advanceobject-block-ctd]]、[[verify-waituser-against-logs]]。

## daegon-itemfinding-script-ctd

> Daegon 的 k101DaegonItemFindingAliasScript 換地點時經 PO3 FindAllReferencesOfType 崩潰；2.2.1.2 也沒修，pex 要一直藏著（原 type: memory）

2026-09-18 晚三次同址 CTD `SkyrimSE.exe+030B0B3`（Papyrus VM 執行緒），真因是 Daegon and Kaeserius 的
`k101DaegonItemFindingAliasScript`（OnLocationChange）呼叫 po3_PapyrusExtender `FindAllReferencesOfType(player, k101TempFormList)`，
引擎掃玩家周圍參考時踩壞指標（crash log 暫存器直接印出 `Character "黛宮"`）。
升到最終版 2.2.1.2 後 byte 比對：三處呼叫原封不動，所以 `mods/Daegon-2.2.1.2/scripts/k101DaegonItemFindingAliasScript.pex.mohidden` 要一直藏。

**Why:** 作者已退圈不會再修；PO3 5.5.0.1 過舊（上游 6.5.2）是承載者但不是觸發者。
**How to apply:** 看到同址 +030B0B3 先確認 pex 還藏著；Daegon 新版 Initialize 開機會噴 6 行 SkillBooksArray/TopicArray None，是藏 pex 的直接後果，正常。升 PO3 另案。
相關：[[daegon-2212-midsave-upgrade]]

## custom-navm-combat-pathing-ctd

> 自訂多層 exterior NAVM 在敵人對玩家做戰鬥尋路時 CTD（PathingCell 空指標）；DS 港 navmesh 第 5 項的真相（原 type: memory）

2026-09-13 dsp8-meas 實機：DSPortP3 的 7 格自訂 navmesh（由 DS NVM 直轉、最多 3 層疊）
進得了遊戲、玩家能走，但屍鬼一進入戰鬥尋路（`CombatPathingRequest…FindTargetLocation`）
就 `EXCEPTION_ACCESS_VIOLATION` 讀 0x14，stack 物件 `Pathing*`／`PathingCell*`，
角色 `0xF5000D3D`、cell `0xF5000A5C`／`0xF5000A71`。crash log 存在
`agentctl/handoffs/home-2026-09-13/dsp8/meas/runtime/crash-combat-pathing-18-04.log`。

**Why:** dsp5～7 三輪走動都沒事，因為玩家用 setpos／tcl 沒讓敵人真的追；第 9 項「敵人 alive」
不等於 navmesh 可用。先前用 `placeatme` 生隨從也沒建立 teammate，所以隨從測試看不出來。

**How to apply:** 修 navmesh 時先用 `out/bisect/nonavm/` 那支（無自訂 NAVM）做對照，
確認是 NAVM 不是 NPC；驗收要「敵人主動追到玩家 15 秒不 CTD」而不是「走一圈沒事」；
懷疑點依序：跨格接縫（7 格自訂與 49 格平面沒接）、NAVM 的 NVNM 鄰接／cover 欄位、
多層疊面。相關：[[dsport-render-constraints]]、[[achr-base-must-be-npc-not-lvln]]。

**2026-09-15 更正：** 同址（SkyrimSE.exe+04D0038）崩潰在原版荒野 cell 也發生（09-08、09-15，雪狼／泥沼蟹），四次共同點是 `MaxsuCombatEscape.dll`（Better Combat Escape - NG 1.0.4）的 CellEventHandler 在 actor 換 cell 事件裡同步跑戰鬥尋路。已停用該 mod；自訂 NAVM 不再是這個位址的首要嫌犯，看到 CombatPath＋Pathing 空指標先查 SKSE DLL 的 cell 事件 hook。
