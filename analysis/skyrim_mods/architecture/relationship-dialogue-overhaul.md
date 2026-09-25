# Relationship Dialogue Overhaul (RDO Final, v1187)

## 定位

對話 overhaul，不是「新增劇情」mod。它的核心命題是：**接管 vanilla 既有的對話框架（quest / topic / scene / Story Manager 節點），把海量新台詞用「條件」投放進去**，讓全 Skyrim 的隨從、配偶、市民、商人在既有情境下講出更豐富、隨關係/隨從狀態變化的話。

判別依據（用 ESP dump 統計）：插件共 **9765 records**，其中 **8153 是 RDO 新增、1612 是 vanilla override**。但「新增」的 8153 records 絕大多數是 `DialogResponses`（INFO，6650 條）與 `DialogTopic`（1151 條）——也就是台詞與話題容器本身；真正改變遊戲對話「流向」的，是那 51 個被整個覆寫的 vanilla `Quest`、31 個覆寫的 `Scene` 與 4 個覆寫的 Story Manager 節點。RDO 把新台詞掛到既有 quest 底下，再靠每句台詞上的 condition 決定誰、何時、以多大機率聽到。

對照本目錄既有的 JContainers（純 library、零遊戲內容），RDO 是另一個極端：幾乎沒有「機制」，全是「內容 + 投放規則」。它示範的不是程式技巧，而是**規模化對話的資料工程**。

來源：
- mod 目錄 `~/skyrim_mods/Relationship Dialogue Overhaul - RDO Final-1187-Final/`（ESP 3 MB + BSA 116 MB）。
- BSA 116 MB 幾乎全是語音 `.fuz`（無工具解包，本檔不分析語音）。
- ESP 完整 dump：`/tmp/mfdump/rdo.txt`（59418 行，9765 records）。
- masters = `[Skyrim.esm, Update.esm, Dawnguard.esm, HearthFires.esm, Dragonborn.esm]`（dump 第 1 行）。

<!-- wf-nav -->
- [檔案結構](relationship-dialogue-overhaul/files-and-records.md)
- [override 策略](relationship-dialogue-overhaul/overrides-and-targeting.md)
- [對 ModForge 的意義](relationship-dialogue-overhaul/modforge-implications.md)
