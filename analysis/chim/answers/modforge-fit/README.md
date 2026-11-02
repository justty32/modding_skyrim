# ModForge 對照：已有能力與研究邊界

[返回答案入口](../modforge-fit.md)｜[三項出貨驗收候選](output-gates.md)

此頁保留現有能力與不擴張範圍；候選尚未裁定開工，版本、方法與授權見[研究入口](../../README.md)。

## 先扣除已有能力

[Generator.cs:4–8](../../../../projects/ModForge/src/ModForge.Core/Generator.cs) 已把引擎設計成物件進出、呼叫端擁 I/O；[Generator.Build.cs:29–46](../../../../projects/ModForge/src/ModForge.Core/Build/Generator.Build.cs) 由 macro 展開後建立 records，再接 FormLinks。[Program.Dispatch.cs:11–38](../../../../projects/ModForge/src/ModForge.Cli/Commands/Program.Dispatch.cs) 已有 build/package/validate/translate/catalog 等 headless 命令。

搜尋與來源追溯也已落地：[Catalog.cs:64–80、101–106、151–162](../../../../projects/ModForge/src/ModForge.Core/Catalog/Catalog.cs) 保存 source hash／載入順序並限制 query 數量；[CatalogCmd.cs:20–67](../../../../projects/ModForge/src/ModForge.Cli/Commands/CatalogCmd.cs) 可輸出 JSON。catalog build 本身有 transaction＋temp→replace；[Catalog.Export.cs:46–60](../../../../projects/ModForge/src/ModForge.Core/Catalog/Catalog.Export.cs) 與 [ModlistSnapshotCmd.cs:21–39](../../../../projects/ModForge/src/ModForge.Cli/Commands/ModlistSnapshotCmd.cs) 已有保護輸入、flush 與替換輸出。

既有 requires[] 會在 plugin 寫入前檢查，必需 scene/MCM bridge 也有前置編譯 gate；不是全無安全措施。來源：[Program.Build.cs:22–27](../../../../projects/ModForge/src/ModForge.Cli/Commands/Program.Build.cs)、[Package.cs:29–44](../../../../projects/ModForge/src/ModForge.Cli/Commands/Package.cs)、[PackageSafetyTests.cs:10–53、89–111](../../../../projects/ModForge/tests/ModForge.Core.Tests/Build/PackageSafetyTests.cs)。

特別是剛完成的單模型 GLB→完整包 wrapper **已做 manifest、逐檔 hash、ESP readback 與可回復發布**：[model-converter/modforge_package/cli.py:79–104](../../../../projects/model-converter/modforge_package/cli.py)、[safety.py:44–72、90–107](../../../../projects/model-converter/modforge_package/safety.py)。[出貨驗收候選](output-gates.md)第二、三項只指一般 ModForge `Package.cs`／`ship.sh` 路徑，不能再把 wrapper 已做的事當新工作；若採納，應先參考內部成果。

## 不值得順勢擴張的部分

不替換 Mutagen 或重造 record writer；不把 ESS／Papyrus heap cleaner 搬進 ModForge。CHIM 確有 [save cleaner](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/chim/server.py#L1145-L1205)，但那是不同產品面，現有 spec authoring 沒有這個缺口。TES3/OpenMW/TES3MP 的 multiplayer／engine pin 規則及 TES3 資產閉包也不直接適用 Skyrim SE。

MCP 暫列次要 transport：ModForge library＋CLI 已分層，catalog 已有 bounded JSON，直接 CLI 已可服務 agent。[SkyLink MCP](../../../../projects/ModForge/scripts/skylink/skylink-call.py) 是遊戲執行期橋接，不能混同離線 authoring。日後客戶端真需要 typed tools，再以 validate／catalog 唯讀小面包裝；這次不新增 server，也不連帶續開 Living、Sofia、DSP 或隨從調整。
