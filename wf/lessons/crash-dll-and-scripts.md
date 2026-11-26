# CTD：SKSE DLL 與腳本

[lessons 索引](README.md)

**崩了先跑 snapshot 再開 MO2**：`agentctl/tools/snapshot_skse_logs.sh`（SKSE/、Skyrim.INI/SKSE/、ini、Papyrus 複製到 `~/skyrim_mods/_crash-snapshots/<時間>/`＋MANIFEST）；下一場會蓋掉各 DLL log。2026-10-23 之前的快照已清空，舊報告引用的快照路徑當它不存在；現存只有 `~/skyrim_mods/_crash-snapshots/2026-10-23/`（20 份 crash log，2026-09-22～10-13）。歸因流程見 [crash-triage](../workflows/crash-triage.md)；crash log 讀法與歸因陷阱在 [crash-log-reading-and-attribution](crash-log-reading-and-attribution.md)。

## upstream-skse-dll-fix-via-fork-ci

> SKSE DLL 的上游 bug 可以自己修：crash log 帶原始碼行號時直接讀 GitHub 原始碼定罪，fork 後靠 repo 自帶的 GitHub Actions 編譯，不需要本機 Windows 工具鏈

2026-09-25（Constellations CTD）。**定罪**：CrashLoggerSSE 把 PDB 的原始碼路徑與行號印在 crash log 第一行（`Constellations.dll+0023374 mov rax, [rcx] | ...\SorceryPerks.cpp:168`）；`gh api -X GET search/code -f q='<函式名>'` 找 repo、抓檔對行號，那行程式碼與指令／暫存器（如 `rcx=0` 讀 vtable）吻合才算定罪。有公開原始碼時 `grep LookupForm(` 找「用插件名＋FormID 查找其他 mod 記錄」的呼叫，看有沒有對回傳值做 null／數量檢查；本機裝的版本缺其中一筆 FormID 就會對 null 呼叫虛函式，esp 層 MAST 比對抓不到這類跨 plugin 的執行期假設（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-10/crash-1/REPORT.md`）。

**修**：`gh repo fork` → contents API 直接 PUT 改好的檔（不必 clone 數 GB 子模組）→ repo 有 `.github/workflows/build.yml` 就 `gh workflow run ... --ref main`（fork 的 push 不會自動觸發）→ `gh run download` 拿產物。目標版本那棵樹沒有 CI 時從有 CI 的分支建，先 `gh api repos/X/Y/compare/<a>...<b>` 確認 `src/` 零改動才敢說「同一份程式碼」。

**裝之前**：`.pdb` 跟 `.dll` 一起換（只換 DLL，之後 crash log 行號全錯）；`objdump -p` 找 `SKSEPlugin_Version` 的 RVA，解 PluginVersionData 比對新舊 `versionIndependence` 與 `compatibleVersions`，相同就代表載入判定路徑一樣。**驗收**：`skse64.log` 的 `plugin X.dll (00000001 X <版本>) loaded correctly` 版本號要變、`loaded correctly` 總數不變；「沒崩」不算證據。

相關：[[pepe-tls-end-crash-is-payloadinterpreter-dangling-listener]]、[[doomperk-advanceobject-block-ctd]]

## pepe-tls-end-crash-is-payloadinterpreter-dangling-listener

> 啟動 65–70 秒炸在 PerkEntryPointExtender.dll+025FA30 _tls_end 的 crash，真因是 PayloadInterpreter.dll 載入間歇失敗留下死 listener；重開 MO2 等它載完再 Run 即可（2026-09-17）

特徵：簽名 `PerkEntryPointExtender.dll+025FA30 _tls_end`、uptime 65–70 s、crash log 約 28 KB。skse64.log 有 `plugin PayloadInterpreter.dll ... disabled, fatal error occurred while loading plugin 0 (handle 75)`：PI 已登記 listener slot 75 後被卸載，SKSE 送 PostLoad 到該 slot 時打進現由 PEPE 佔據的位址，所以「炸在 PEPE」，PEPE 無辜。成因是間歇的 usvfs：PI 的 Load() 對多個 mod 合併出的 `Data/SKSE/PayloadInterpreter/Config` 跑不帶 error_code 的 directory_iterator，列舉一失敗就 throw；同一批檔重啟就 `loaded correctly`。

**How to apply:** 看到這簽名先 grep skse64.log 的 `disabled, fatal error`、對 slot 編號；處置是重開 MO2、等列表載完再 Run，不改 DLL。同場「cannot start skse64 / Error 87」也是 usvfs，同樣重開 MO2。skse64.log 下次啟動會被覆蓋，要定案先 copy 走。持久修法 `PayloadInterpreter-Config-Consolidated-Dev-2026-09-20`（52 INI 合併、原檔 hash 未變）已啟用、觀察中。待清：`91-189376-BFCO-I-MCO-AshinFencer/SKSE/PayloadInterpreter/Config/新建文件夹/`（非 ASCII 目錄＋壞語法副本，PI 不遞迴讀不到，無害但該清）。

另一型 `SkyrimSE+01D3398`（帶 Constellations `Sorcery`、owning perk `doomMagePerk 0E5F49`）與 PEPE／CARP 無關，見 [[doomperk-advanceobject-block-ctd]]；A/B 用的 `crash-ab-carp` profile 在 `instance/profiles/.repo/retired/`（要再用就 git mv 回根目錄並加進 check_profiles 白名單）。證據 `agentctl/handoffs/home-2026-09-20/crash2/REPORT.md`。相關：[[custom-navm-combat-pathing-ctd]]（先查 SKSE DLL 再怪別的）、[[launch-skyrim-via-steam]]（Steam 沒起來時 SKSE 0-byte log 秒退，是另一種症狀）。

## daegon-itemfinding-script-ctd

> Daegon 的 k101DaegonItemFindingAliasScript 換地點時經 PO3 FindAllReferencesOfType 崩潰；2.2.1.2 也沒修，pex 要一直藏著

2026-09-18。同址 CTD `SkyrimSE.exe+030B0B3`（Papyrus VM 執行緒）：Daegon and Kaeserius 的 `k101DaegonItemFindingAliasScript`（OnLocationChange）呼叫 po3_PapyrusExtender `FindAllReferencesOfType(player, k101TempFormList)`，引擎掃玩家周圍參考時踩壞指標（暫存器印出 `Character "黛宮"`）。2.2.1.2 三處呼叫原封不動，`mods/Daegon-2.2.1.2/scripts/k101DaegonItemFindingAliasScript.pex.mohidden` 要一直藏。作者已退圈；PO3 5.5.0.1 過舊是承載者不是觸發者。

**How to apply:** 看到同址 +030B0B3 先確認 pex 還藏著；Daegon Initialize 開機噴 6 行 SkillBooksArray/TopicArray None 是藏 pex 的直接後果，正常。升 PO3 另案。相關：[[daegon-2212-midsave-upgrade]]

## custom-navm-combat-pathing-ctd

> `SkyrimSE.exe+04D0038` 戰鬥尋路 PathingCell 空指標 CTD 的真凶是 Better Combat Escape - NG 的 cell 事件 hook（2026-09-15 定，已停用），不是自訂 NAVM

簽章：敵人進戰鬥尋路（`CombatPathingRequest…FindTargetLocation`）時讀 0x14 AV，stack 物件 `Pathing*`／`PathingCell*`；自訂 navmesh 與原版荒野 cell 都會發生，共同點是 `MaxsuCombatEscape.dll`（1.0.4）的 CellEventHandler 在換 cell 事件裡同步跑戰鬥尋路。crash log `agentctl/handoffs/home-2026-09-13/dsp8/meas/runtime/crash-combat-pathing-18-04.log`。setpos／tcl 走動不會讓敵人真的追，「敵人 alive」不等於戰鬥尋路走得通；`placeatme` 生的隨從沒建立 teammate，這兩種測試都看不出來。

**How to apply:** CombatPath＋Pathing 空指標先查 SKSE DLL 的 cell 事件 hook，再懷疑 navmesh。驗 navmesh 要「敵人主動追到玩家 15 秒不 CTD」而不是「走一圈沒事」；隔離 NAVM 用 `out/bisect/nonavm/`（無自訂 NAVM）對照；navmesh 懷疑點依序：跨格接縫、NVNM 鄰接／cover 欄位、多層疊面。相關：[[dsport-render-constraints]]、[[achr-base-must-be-npc-not-lvln]]。

## sequential-minimal-disable-and-family-grouping-for-stacked-crashes

> 多崩潰 blocker 疊一起，逐一停用最可疑一件看新崩潰點比整批回退快；同症狀家族封閉後免逐批二分

2026-08-30。做法已寫進 [crash-triage](../workflows/crash-triage.md) 步驟 5：「只停最可疑一件、重啟、看新訊號定下一步」；stack／`relevant objects` 模式相同的歸同族，全量掃描確認家族封閉後同族免二分。`agentctl/handoffs/done/2026-08-30/diag-2026-08-30/DIAG.md`。相關：[[achr-base-must-be-npc-not-lvln]]。
