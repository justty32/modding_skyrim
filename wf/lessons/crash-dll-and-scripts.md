# CTD：SKSE DLL 與腳本

[lessons 索引](README.md)

**崩了先跑 snapshot 再開 MO2**：`agentctl/tools/snapshot_skse_logs.sh`（SKSE/、Skyrim.INI/SKSE/、ini、Papyrus 複製到 `~/skyrim_mods/_crash-snapshots/<時間>/`＋MANIFEST）；下一場會蓋掉各 DLL log。`_crash-snapshots` 已於 2026-10-23 依全刪裁示清空，10-13 之前的快照索引一律失效——引用那段時間快照路徑的舊報告當它不存在；目前唯一一份是 10-23 重收的 `~/skyrim_mods/_crash-snapshots/2026-10-23/`（20 份 crash log，2026-09-22～10-13）。

## upstream-skse-dll-fix-via-fork-ci

> SKSE DLL 的上游 bug 可以自己修：crash log 帶原始碼行號時直接讀 GitHub 原始碼定罪，fork 後靠 repo 自帶的 GitHub Actions 編譯，不需要本機 Windows 工具鏈（原 type: project）

2026-09-25 Constellations CTD 走通的流程，之後遇到 SKSE 外掛的上游 bug 都照這條走。

**定罪**：CrashLoggerSSE 會把 PDB 的原始碼路徑與行號印在 crash log 第一行
（`... Constellations.dll+0023374 mov rax, [rcx] | D:\source\...\SorceryPerks.cpp:168 ...`）。
用 `gh api -X GET search/code -f q='<函式名>'` 找到 repo，把那個檔案抓下來對行號。
例：`SorceryPerks.cpp:168` 是 `a_caster->currentSpell->GetSpellType()`，`currentSpell` 沒守 null，
與 `mov rax, [rcx]` / `rcx=0`（虛函式讀 vtable）完全吻合。**這是定罪不是推測。**

有公開原始碼時，裝之前或崩潰後定位可直接 `grep LookupForm(` 找「用插件名＋FormID 查找其他 mod 記錄」的呼叫，確認有沒有對回傳值做 null／數量檢查；本機實際裝的 mod 版本若缺其中一筆 FormID（如只檢查第一筆就假設其餘都在）就會對 null 呼叫虛函式崩潰，esp 層 MAST 比對抓不到這類跨 plugin 的執行期假設（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-10/crash-1/REPORT.md`）。

**修**：`gh repo fork` → 用 contents API 直接 PUT 改好的檔案（不必 clone，省掉數 GB 子模組）→
repo 若有 `.github/workflows/build.yml` 就 `gh workflow run ... --ref main`（fork 的 push 事件不會自動觸發）→
`gh run download` 拿產物（Constellations 約 5 分半編完）。

**換版本基底要先比 `src/`**：目標版本那棵樹沒有 CI workflow 時（例：Constellations 1.0.2），從有 CI 的 main（1.0.3）建，
先用 `gh api repos/X/Y/compare/<a>...<b>` 確認 `src/` 零改動，才敢說「同一份程式碼」。

**裝之前必看兩件事**：
1. `.pdb` 要跟 `.dll` 一起換。只換 DLL 的話，以後的 crash log 會用舊符號表標新二進位，行號全錯。
2. 用 `objdump -p` 找 `SKSEPlugin_Version` 的 RVA，手動解 PluginVersionData 比對新舊的
   `versionIndependence` 與 `compatibleVersions`。兩者相同（Constellations 都是 `0x5`、compat 空＝走 Address Library）
   就代表載入判定路徑一樣，跨版本風險比想像小。

**驗收點**：`skse64.log` 的 `plugin X.dll (00000001 X <版本>) loaded correctly` 那一行版本號要變，
且 `loaded correctly` 總數不變。這兩條是硬證據，比「沒崩」有力得多。

相關：[[pepe-tls-end-crash-is-payloadinterpreter-dangling-listener]]、[[doomperk-advanceobject-block-ctd]]

## pepe-tls-end-crash-is-payloadinterpreter-dangling-listener

> 啟動 65–70 秒炸在 PerkEntryPointExtender.dll+025FA30 _tls_end 的 crash，真因是 PayloadInterpreter.dll 載入間歇失敗留下死 listener；重開 MO2 等它載完再 Run 即可（2026-09-17，原 type: project）

簽名 `PerkEntryPointExtender.dll+025FA30 _tls_end`，uptime 65–70 s，crash log 約 28 KB 是此型特徵（B 型是 112 KB 級）。skse64.log 關鍵行：`plugin PayloadInterpreter.dll ... disabled, fatal error occurred while loading plugin 0 (handle 75)`，但它已登記 listener slot 75；SKSE 送 PostLoad（message type 0）到 slot 75 時打進已卸載位址，該位址現由 PEPE 佔據，所以「炸在 PEPE」。PEPE 無辜。

成因（2026-09-17 查證）：PI config 全是 .ini（54 檔／40 個 MCO 動作 mod），DLL 全機只一份（v1.0.0，md5 b6c50a27…），同一批檔案重啟就 `loaded correctly`，判定 intermittent usvfs：PI 的 Load() 對 40 個 mod 合併出的 `Data/SKSE/PayloadInterpreter/Config` 跑不帶 error_code 的 directory_iterator，列舉一失敗就 throw。

**Why:** 看 crash log 第一眼會怪 PEPE；真線索在 skse64.log 的 `disabled, fatal error` 行與 listener slot 編號對應。

**How to apply:** 看到這個簽名先 grep skse64.log 的 `disabled, fatal error`，對 slot 編號；處置是重開 MO2、等列表載完再 Run，不要改 DLL。同場「cannot start skse64 / Error 87」是 MO2 剛崩完孩子後 usvfs 抽風，也是重開 MO2。此型 crash 後 skse64.log 會被下次啟動覆蓋，要定案得先把它 copy 走。持久修法成品 `PayloadInterpreter-Config-Consolidated-Dev-2026-09-20`（52 INI 合併、原檔 hash 未變）2026-09-20 已啟用、觀察中。待清：`91-189376-BFCO-I-MCO-AshinFencer/SKSE/PayloadInterpreter/Config/新建文件夹/`（非 ASCII 目錄＋壞語法副本，PI 不遞迴讀不到，無害但該清）。相關：[[custom-navm-combat-pathing-ctd]]（先查 SKSE DLL 再怪別的）、[[launch-skyrim-via-steam]]（開機後 Steam 沒起來 SKSE 會 0-byte log 秒退，是另一種症狀）。

另一型 **B：`SkyrimSE+01D3398` READ 0x9E42**（帶 Constellations `Sorcery` 關鍵字、owning perk `doomMagePerk 0E5F49`）與 PEPE／CARP 都無關，2026-09-24 結案：`doomMagePerk` 等三顆 perk 在 `ModSkillUse` 掛 `EPModSkillUsage_AdvanceObjectHasKeyword`，格擋等非物件推進會 deref 垃圾指標，補丁已實機驗證，見 [[doomperk-advanceobject-block-ctd]]。`crash-ab-carp` 測試 profile 已封存在 `instance/profiles/.repo/retired/`（要再用就 git mv 回根目錄並加進 check_profiles 白名單）。證據 `agentctl/handoffs/home-2026-09-20/crash2/REPORT.md`。

## spid-outfit-manager-live-inventory-reset-ctd

> `SkyrimSE.exe+02B789A` 背景載入 CTD：SPID 定罪 2026-10-03 已推翻，真兇未明（原 type: project）

簽章 `SkyrimSE.exe+02B789A  mov rcx,[rcx+0x130]`、rcx=0，崩在**背景載入執行緒**（frame 10-11 是 kernel32/ntdll 進入點），現場 `QueuedCharacter` / `IOManager` / `BSFadeNode "skeleton.nif"`；受害 actor 不固定（長毛象 `[ACHR:001038A9]`、巴巴斯 `DA03BarbasRef`）。

現況（2026-10-03）：**真兇未明**。SPID 不是兇手——讀 SPID 上游源碼，`Resetting inventory` log 是記錄原版引擎自己的 reset，不是 SPID 發起；空檔覆寫層 `SPID-NoElderOutfit-2026-09-24`（壓在 CT77 `ElderOutfit_DISTR.ini` 之上，modlist 1308）生效下同簽章同 call stack 照樣復發，覆寫層無害但沒修到。見 `agentctl/handoffs/home-2026-10-03/crash/c0927/REPORT.md`。

**Why:** 兩個會重複踩的誤判 ——
(1) **call stack 全是原版碼、沒有 SKSE DLL，不等於 SKSE DLL 無關**：hook 是 trampoline，跑完跳回原版碼就不留名字；但「log 裡出現同 FormID」也只是相關不是因果。
(2) **`Resetting inventory` / `Resurrecting` 的總次數會被遊玩時長汙染**（長時間實玩 vs 短煙霧），不能當 A/B 指標。

**How to apply:** 下次再崩，開 MO2 前先打包 SKSE log 目錄（各 DLL log 會被下一場蓋掉）。SKSE plugin 的嫌疑可以從「崩潰前數秒 DLL log 裡有沒有同一個 ACHR/FormID」找線索，但要有機制證據才算定罪。crash log 讀法：
1. 每個 frame 標 [P]（precise）或 [S]（stack scan）——只有少數 frame（常是 frame 0）是 [P]，其餘多是 [S]，只能定位功能路徑不能當嚴格 unwind 因果鏈；排除「今天新裝的 mod 是兇手」不能只看它名字沒出現在 callstack，要查同簽章崩潰裝之前是否已發生（`agentctl/handoffs/done/2026-09/home-2026-09-20/crash/REPORT.md:17`）。
2. RIP=0（跳到空指標）時 CrashLogger 回推的 frame[0] 其實是浮點殘值不是真程式碼位址，要改讀 `[RSP+偏移]` 的真正返回位址重新起算，`triage_crash.py` 已有這段邏輯（`agentctl/handoffs/done/2026-10/home-2026-10-03/crash/c0928/REPORT.md`）。
3. 暫存器裡出現的插件名／FormList 字串只是「當下還留著的值」不代表是崩潰原因，要對照崩潰那一行指令實際讀寫的是哪個暫存器（`agentctl/handoffs/done/2026-10/home-2026-10-10/crash-1/REPORT.md`）。
4. 本機 .exe 被 SteamStub 加密反組譯不了時，可用 alandtse/skyrim_vr_address_library 的多份 offsets CSV（AE ID→1.6.318→se_ae_offsets→SE→1.5.97→1.5.97_comments）鏈式對照，把 crash log 匿名函式 ID 推回 SE/AE 公開名稱（`agentctl/handoffs/done/2026-10/crossbow-ctd-2026-10-09/REPORT.md`）。

（以上讀法 2026-10-23 整理。）相關：[[doomperk-advanceobject-block-ctd]]、[[verify-waituser-against-logs]]。

## daegon-itemfinding-script-ctd

> Daegon 的 k101DaegonItemFindingAliasScript 換地點時經 PO3 FindAllReferencesOfType 崩潰；2.2.1.2 也沒修，pex 要一直藏著（原 type: memory）

2026-09-18 同址 CTD `SkyrimSE.exe+030B0B3`（Papyrus VM 執行緒），真因是 Daegon and Kaeserius 的
`k101DaegonItemFindingAliasScript`（OnLocationChange）呼叫 po3_PapyrusExtender `FindAllReferencesOfType(player, k101TempFormList)`，
引擎掃玩家周圍參考時踩壞指標（crash log 暫存器直接印出 `Character "黛宮"`）。
最終版 2.2.1.2 byte 比對三處呼叫原封不動，所以 `mods/Daegon-2.2.1.2/scripts/k101DaegonItemFindingAliasScript.pex.mohidden` 要一直藏。

**Why:** 作者已退圈不會再修；PO3 5.5.0.1 過舊（上游 6.5.2）是承載者但不是觸發者。
**How to apply:** 看到同址 +030B0B3 先確認 pex 還藏著；Daegon 新版 Initialize 開機會噴 6 行 SkillBooksArray/TopicArray None，是藏 pex 的直接後果，正常。升 PO3 另案。
相關：[[daegon-2212-midsave-upgrade]]

## custom-navm-combat-pathing-ctd

> `SkyrimSE.exe+04D0038` 戰鬥尋路 PathingCell 空指標 CTD 的真凶是 Better Combat Escape - NG 的 cell 事件 hook（2026-09-15 定，已停用），不是自訂 NAVM（原 type: memory）

簽章：敵人進入戰鬥尋路（`CombatPathingRequest…FindTargetLocation`）時 `EXCEPTION_ACCESS_VIOLATION` 讀 0x14，stack 物件 `Pathing*`／`PathingCell*`。DSPortP3 自訂 navmesh（DS NVM 直轉、最多 3 層疊）與原版荒野 cell 都會發生，四次共同點是 `MaxsuCombatEscape.dll`（Better Combat Escape - NG 1.0.4）的 CellEventHandler 在 actor 換 cell 事件裡同步跑戰鬥尋路；該 mod 已停用。DSPortP3 那次的 crash log 在 `agentctl/handoffs/home-2026-09-13/dsp8/meas/runtime/crash-combat-pathing-18-04.log`。

**Why:** 用 setpos／tcl 走動不會讓敵人真的追，「敵人 alive」不等於戰鬥尋路走得通；`placeatme` 生的隨從沒建立 teammate，隨從測試也看不出來。

**How to apply:** 看到 CombatPath＋Pathing 空指標先查 SKSE DLL 的 cell 事件 hook，再懷疑 navmesh。驗 navmesh 要「敵人主動追到玩家 15 秒不 CTD」而不是「走一圈沒事」；要隔離 NAVM 時用 `out/bisect/nonavm/` 那支（無自訂 NAVM）做對照；navmesh 本身的懷疑點依序：跨格接縫（7 格自訂與 49 格平面沒接）、NAVM 的 NVNM 鄰接／cover 欄位、多層疊面。相關：[[dsport-render-constraints]]、[[achr-base-must-be-npc-not-lvln]]。

## sequential-minimal-disable-and-family-grouping-for-stacked-crashes

> 多崩潰 blocker 疊一起，逐一停用最可疑一件看新崩潰點比整批回退快；同症狀家族封閉後免逐批二分

2026-08-30 用「只停最可疑一件、重啟、看新訊號定下一步」剝出 dMenu→Phenderix→Midas 三層崩潰，不必整批回退。多次崩潰若 stack／`relevant objects` 模式相同可歸同根因家族；對可疑成因全量掃描確認家族封閉後，同族免逐批二分。`agentctl/handoffs/done/2026-08-30/diag-2026-08-30/DIAG.md`。

**Why:** 新崩潰訊號比猜整批誰可疑可靠；家族封閉後繼續二分只是重複驗證。

**How to apply:** 起不來先只停最可疑一件再測；多次崩潰先按特徵分族，全量掃描確認封閉後同族免二分。相關：[[achr-base-must-be-npc-not-lvln]]。

## loose-files-always-override-bsa-regardless-of-mo2-priority

> 同名鬆散檔永遠贏過同名 BSA 內容，與 MO2 優先度無關；SSE 只接受 BSA header version 105，Oldrim 104 會崩潰

2026-08-30 VIGILANT「版本不匹配」真因：標 `TEST HARNESS` 的舊中文層殘留鬆散 `vigsafetyquestscript.pex`（回傳 172）蓋過現役 BSA 內同名腳本（回傳 182）。BSA header version 104（Oldrim）在 archive 註冊階段 AV；同名不同內容 BSA 重複註冊是同家族另一種成員。`agentctl/handoffs/done/2026-08-30/vig-2026-08-30/ROOT-CAUSE.md`。

**Why:** VFS 覆蓋順序與 BSA 內容版本是兩條獨立規則，單看 load order 或優先度不夠。

**How to apply:** 版本對不上時額外掃鬆散檔（尤其 `scripts/*.pex`），`meta.ini` 標 TEST HARNESS 的優先懷疑；崩潰堆疊反覆同 BSA 檔名時先讀 header 版本號。
