# CHIM 對 ModForge 有什麼可借鑑？

最值得借的是「另一套 reader 驗輸出」「驗收後才發布」「每包附可追溯 manifest」。ModForge 已有 spec authoring、headless CLI、JSON catalog 與完整組包，沒有理由換掉 Mutagen 或重造這些能力。這是研究候選，尚未裁定開工。版本、方法與授權見 [研究入口](../README.md)。

## 先扣除已有能力

[Generator.cs:4–8](../../../projects/ModForge/src/ModForge.Core/Generator.cs) 已把引擎設計成物件進出、呼叫端擁 I/O；[Generator.Build.cs:29–46](../../../projects/ModForge/src/ModForge.Core/Build/Generator.Build.cs) 由 macro 展開後建立 records，再接 FormLinks。[Program.Dispatch.cs:11–38](../../../projects/ModForge/src/ModForge.Cli/Commands/Program.Dispatch.cs) 已有 build/package/validate/translate/catalog 等 headless 命令。

搜尋與來源追溯也已落地：[Catalog.cs:64–80、101–106、151–162](../../../projects/ModForge/src/ModForge.Core/Catalog/Catalog.cs) 保存 source hash／載入順序並限制 query 數量；[CatalogCmd.cs:20–67](../../../projects/ModForge/src/ModForge.Cli/Commands/CatalogCmd.cs) 可輸出 JSON。catalog build 本身有 transaction＋temp→replace；[Catalog.Export.cs:46–60](../../../projects/ModForge/src/ModForge.Core/Catalog/Catalog.Export.cs) 與 [ModlistSnapshotCmd.cs:21–39](../../../projects/ModForge/src/ModForge.Cli/Commands/ModlistSnapshotCmd.cs) 已有保護輸入、flush 與替換輸出。

既有 requires[] 會在 plugin 寫入前檢查，必需 scene/MCM bridge 也有前置編譯 gate；不是全無安全措施。來源：[Program.Build.cs:22–27](../../../projects/ModForge/src/ModForge.Cli/Commands/Program.Build.cs)、[Package.cs:29–44](../../../projects/ModForge/src/ModForge.Cli/Commands/Package.cs)、[PackageSafetyTests.cs:10–53、89–111](../../../projects/ModForge/tests/ModForge.Core.Tests/Build/PackageSafetyTests.cs)。

特別是剛完成的單模型 GLB→完整包 wrapper **已做 manifest、逐檔 hash、ESP readback 與可回復發布**：[model-converter/modforge_package/cli.py:79–104](../../../projects/model-converter/modforge_package/cli.py)、[safety.py:44–72、90–107](../../../projects/model-converter/modforge_package/safety.py)。下文第二、三項只指一般 ModForge `Package.cs`／`ship.sh` 路徑，不能再把 wrapper 已做的事當新工作；若採納，應先參考內部成果。

## 1. 用獨立結構 reader 驗證寫出的 plugin

CHIM 的 production plugin backend 是 esplib，但 safety 預設驗證器保留另一套 legacy `walk_clean`：檢查 TES4 開頭、GRUP／record 長度與 EOF 全消耗，再 roundtrip。這能降低 writer 與同套 reader 一起誤判的風險。來源：[records.py:362–428](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/chim/esp/records.py#L362-L428)、[walk_clean:465–476](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/chim/esp/records.py#L465-L476)、[safety.py:568–622](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/chim/esp/safety.py#L568-L622)。

ModForge 的 [PluginIo.cs:7–8、46–52](../../../projects/ModForge/src/ModForge.Core/Formats/PluginIo.cs) 由 Mutagen 讀寫。[golden-hash.sh:2–12](../../../projects/ModForge/scripts/golden-hash.sh) 能抓前後 byte 漂移，不能獨立證明格式正確；單模型 wrapper 的 ESP readback 也透過既有 Mutagen catalog。

最小切片是在 staging plugin 發布前跑獨立 strict 結構驗證。驗收用人工 fixture：GRUP size 錯、截短 record、trailing bytes 都失敗；合法 nested CELL/DIAL 與壓縮 record 通過，輸入 bytes 不變。CHIM 的 [backend contract tests:68–114](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/tests/test_esplib_backend.py#L68-L114) 可參考，但 byte-identical 僅適用無修改 roundtrip。

成本低至中，人工資料可離線驗，不需 DLL／遊戲。工作區已有 [esplib/core.py:266–300](../../../agentctl/tools/esplib/core.py) 的 strict parser，可先評估；仍須確認短尾／EOF 全消耗，且 private 工具路徑不能成為公開 ModForge 的硬依賴。這項只保結構，不驗 FormID 指向型別、缺 master、HEDR 計數或玩法正確，不能代替既有語義 gate 與實機驗收。

## 2. 一般出貨路徑保住最後一份可用產物

CHIM 把 backup→write→readback→verify／restore 集中在 safety gate，mutator 只管編輯 bytes，這個責任邊界值得借。但 [safety.py:595–622](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/chim/esp/safety.py#L595-L622) 直接覆寫，只有 verifier 回 false 才還原；write/read/verify 拋例外沒有統一 rollback，也沒有 atomic replace、CAS 或 writer mutex。應借契約，不照抄安全承諾。

一般 ModForge 的 [PluginIo.cs:46](../../../projects/ModForge/src/ModForge.Core/Formats/PluginIo.cs) 直接寫 outPath；[Program.Translate.cs:20–29](../../../projects/ModForge/src/ModForge.Cli/Commands/Program.Translate.cs) 的 apply 未拒絕 input=output；[Package.cs:14–17、44、61–85](../../../projects/ModForge/src/ModForge.Cli/Commands/Package.cs) 逐步寫 outDir。ship 已有 temp staging，但 [ship.sh:73–74](../../../projects/ModForge/scripts/ship.sh) 先刪舊 zip 再寫 final dest，zip 失敗會失去舊版。

最小切片先只修 ship 最後一步：同檔案系統 sibling temp zip→驗 zip 可讀／plugin 在根→replace 最終 zip。注入 zip／驗證／replace 失敗時，舊包 hash 必須不變；成功才看見新完整包。成本低、離線 fixture 足夠。先復用 catalog／snapshot 的 temp-flush-move 與單模型 wrapper 的發布失敗契約；後者的目錄 rename＋backup 不能直接當所有平台的原子目錄交換。全包 transaction 與 in-place apply 保護可另定範圍，這次研究不展開實作。

## 3. 一般 package 附可追溯 manifest

CHIM 的 [build_modlock:106–169](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/chim/modlock.py#L106-L169) 記有序 plugins、SHA-256／CRC32／size／masters、bundle files 與 engine pin；時間戳在契約外。[write_bundle_zip:279–320](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/chim/modlock.py#L279-L320) 排序並固定 zip entry 日期。不過 manifest 按 exact-case 合併，ZIP 按 lower-case 合併，且直接寫目標檔；只能借設計，不能全盤當成熟發布方案。

ModForge 已有 catalog source hash／order、[Package.cs:48–59](../../../projects/ModForge/src/ModForge.Cli/Commands/Package.cs) 的依賴文件，以及 [package-snapshot.sh:49–62](../../../projects/ModForge/scripts/package-snapshot.sh) 的 regression hash。真缺口是一般交付包的「來源＋全部成品」單一機讀契約；單模型 wrapper 已有此能力，優先參考它的 manifest／ownership 規則。

最小切片在 staging 完成後生成 schemaVersion、ModForge／Mutagen 版本或 commit、resolved spec hash、實際 plugin masters、每個檔案相對 path／size／SHA-256，含 PEX 實際 bytes、排除 manifest 自身，排序且不含絕對路徑與生成時間。驗收同一 staging 重產 byte-identical，任何 PEX／asset 改一 byte 或增缺檔都可查出；requires[] 仍走既有 gate。成本低至中，不需遊戲。

這是交付完整性與追溯，不承諾兩次重編譯 byte-identical：[package-snapshot.sh:4–6、60](../../../projects/ModForge/scripts/package-snapshot.sh) 明示 Papyrus PEX 含 build timestamp，因此 regression snapshot 只記 PEX 路徑。manifest 應 hash 實際交付 bytes，不因此略過 PEX，也不宣稱整個工具鏈已可重現。

## 不值得順勢擴張的部分

不替換 Mutagen 或重造 record writer；不把 ESS／Papyrus heap cleaner 搬進 ModForge。CHIM 確有 [save cleaner](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/chim/server.py#L1145-L1205)，但那是不同產品面，現有 spec authoring 沒有這個缺口。TES3/OpenMW/TES3MP 的 multiplayer／engine pin 規則及 TES3 資產閉包也不直接適用 Skyrim SE。

MCP 暫列次要 transport：ModForge library＋CLI 已分層，catalog 已有 bounded JSON，直接 CLI 已可服務 agent。[SkyLink MCP](../../../projects/ModForge/scripts/skylink/skylink-call.py) 是遊戲執行期橋接，不能混同離線 authoring。日後客戶端真需要 typed tools，再以 validate／catalog 唯讀小面包裝；這次不新增 server，也不連帶續開 Living、Sofia、DSP 或隨從調整。
