# CTD 真因與判法（1/3）

[lessons 索引](README.md)｜同主題：[crash-triage-2](crash-triage-2.md)、[crash-triage-3](crash-triage-3.md)

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

## le-collision-nif-precision-crash

> 間歇性 Havok 崩潰（hkpTriangleShape／hkpCompressedMeshShape＋Precision.dll 在呼叫鏈）＝某個世界物件的碰撞 NIF 是 LE 格式（stream 83 帶 bhkCompressedMeshShape）；全機 258 個同類檔，風港王宮門口首次踩到（原 type: project）

2026-09-07 使用者從 Windhelm 王宮走出時崩，第二次同路徑沒崩。lead-crash 掃全機 32240 個 NIF：1046 個 LE 格式、258 個帶壓縮碰撞；風港 6 個（Capital Windhelm Expansion 的 `NewPitCollsion.nif` 純碰撞看不見、魚攤 3 個、Assorted Mesh Fixes 覆蓋原版的 `whmaingatesteps.nif`／`whtempletalos3.nif`）。使用者裁「先不修」，清單在 `agentctl/handoffs/home-2026-09-07/crash/data/nif-suspects.csv`。

**Why:** SE 讀 LE 格式壓縮碰撞會把指標讀壞，但只有 Precision／HDT-SMP 的射線剛好打到壞三角形才炸，所以是間歇的；看不見的純碰撞物件更難靠畫面察覺。

**How to apply:** crash log 出現 `hkpTriangleShape`＋`hkpCompressedMeshShapeShared`＋`Precision.dll` 就先查該 cell 物件的 NIF 版本（houseCARL `nif_inspect` 回「NOT an SE stream」），不要先懷疑腳本或動畫。修法：loose 覆蓋檔移走讓原版接手；BSA 內的用 SSE NIF Optimizer／CAO 轉 SE 再 loose 覆蓋；裝飾物可用 ESL patch 停 REFR。相關：[[verify-game-alive-via-qa-not-ps]]。

## pepe-tls-end-crash-is-payloadinterpreter-dangling-listener

> 啟動 65–70 秒炸在 PerkEntryPointExtender.dll+025FA30 _tls_end 的 crash，真因是 PayloadInterpreter.dll 載入間歇失敗留下死 listener；重開 MO2 等它載完再 Run 即可（原 type: project）

2026-09-17 開機後兩次啟動 crash（20:22、20:25），簽名 `PerkEntryPointExtender.dll+025FA30 _tls_end`，uptime 65–70 s，crash log 只有 28k；09-13 08:33 同簽名。skse64.log 關鍵行：`plugin PayloadInterpreter.dll ... disabled, fatal error occurred while loading plugin 0 (handle 75)`，但它已登記 listener slot 75；SKSE 送 PostLoad（message type 0）到 slot 75 時打進已卸載位址，該位址現由 PEPE 佔據，所以「炸在 PEPE」。PEPE 無辜。

Opus 唯讀查證（09-17）：PI config 全是 .ini（54 檔／40 個 MCO 動作 mod），09-12 後零變動，DLL 全機只一份（v1.0.0，md5 b6c50a27…）。第三次啟動同一批檔案就 `loaded correctly`。判定 intermittent usvfs：PI 的 Load() 對 40 個 mod 合併出的 `Data/SKSE/PayloadInterpreter/Config` 跑不帶 error_code 的 directory_iterator，列舉一失敗就 throw。

**Why:** 看 crash log 第一眼會怪 PEPE；真線索在 skse64.log 的 `disabled, fatal error` 行與 listener slot 編號對應。

**How to apply:** 看到這個簽名先 grep skse64.log 的 `disabled, fatal error`，對 slot 編號；處置是重開 MO2、等列表載完再 Run，不要改 DLL。同場「cannot start skse64 / Error 87」是 MO2 剛崩完孩子後 usvfs 抽風，也是重開 MO2。若一再復發，持久修法：把 40 個 mod 的 `SKSE/PayloadInterpreter/Config/*.ini` 收成單一合併 mod；順手清 `91-189376-BFCO-I-MCO-AshinFencer/SKSE/PayloadInterpreter/Config/新建文件夹/`（非 ASCII 目錄＋壞語法副本，PI 不遞迴讀不到，無害但該清）。相關：[[custom-navm-combat-pathing-ctd]]（先查 SKSE DLL 再怪別的）、[[launch-skyrim-via-steam]]（開機後 Steam 沒起來 SKSE 會 0-byte log 秒退，是另一種症狀）。

**2026-09-20 補**：第 4 次（07:39，log 只有 28 KB 是此型特徵；B 型 112 KB 級）。持久修法成品 `PayloadInterpreter-Config-Consolidated-Dev-2026-09-20`（52 INI 合併、原檔 hash 未變）09-20 14:00 已啟用（cx-pion 三次啟動全過，進觀察期）。此型 crash 後 skse64.log 會被下次啟動覆蓋，要定案得先把它 copy 走。
另一型 **B：`SkyrimSE+01D3398` READ 0x9E42**，帶 Constellations `Sorcery` 關鍵字、owning perk `doomMagePerk 0E5F49`（ConstellationsNewSkills 贏），跟 cell／遊玩時長無關；09-20 11:05 與 13:12 兩次。**2026-09-24 結案，與 PEPE／CARP 都無關**：真因是 `doomMagePerk` 等三顆 perk 在 `ModSkillUse` 掛 `EPModSkillUsage_AdvanceObjectHasKeyword`，格擋等非物件推進會 deref 垃圾指標，補丁已實機驗證，見 [[doomperk-advanceobject-block-ctd]]。`crash-ab-carp` 測試 profile 留著備用。證據 `agentctl/handoffs/home-2026-09-20/crash2/REPORT.md`。
