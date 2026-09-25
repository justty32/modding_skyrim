# real-estate — scope-gameplay

← [調查入口](../real-estate.md)

## Scope / sources

| 項目 | 內容 |
|------|------|
| archive | `~/skyrim_mods/hdd/Real Estate v3.2 Final-14408-v3-2-1583378603.7z`（另存 `Real Estate - Core v3.1 Final-…zip` 與 `Real Estate - USSEP v3.1 Final-…zip` 兩變體）|
| 解壓 | `~/skyrim_mods/unzip/RealEstate/RE v3.2 Final/`（Core 另解到 `unzip/RealEstateCore/`）|
| plugin | `RE_RealEstate.esp`（482 records；masters = Skyrim.esm, Update.esm, **RE_RealEstate_Core.esp**）|
| master | `RE_RealEstate_Core.esp`（Core 變體只含這一支；是放 GlobalVariable 與共用 `RE_MainSafe` 容器的依賴容器 esp）|
| 出貨內容 | 1 esp + 11 `.pex`（**無 `.psc` source**）+ MCM 翻譯 `Interface/translations/RE_RealEstate_ENGLISH.txt` + 12 NPC 的 FaceGen mesh/texture + 自製告示牌 NIF（`RE_RealEstate/Sign/RE_Sign.nif`）+ 金錠堆 NIF |
| **無** | 無 SKSE `.dll`；無 PapyrusUtil / JContainers / JsonUtil / StorageUtil 任何呼叫（逐一 grep 11 個 pex 確認，零命中）|

工具：`7z x` 解壓；ModForge CLI `dump`/`questdiag`（lazy overlay，記憶體鐵律遵守）；機制 ground truth 取自 **`.pex` 的 `strings` 反推**（無 champollion 反編譯器，只能讀 pex 內的函式名/屬性名/字串字面值，**不是完整 source**——標 UNVERIFIED 處即此限制）。

## Classification

- **類型**：玩家側**房產經濟系統**（buy/sell property + 被動收租），框架性質但有薄敘事包裝（一條教學 quest）。
- **是否有 plugin**：✅ `RE_RealEstate.esp`（+ Core master）。
- **SKSE 依賴**：✅ **僅 SkyUI**（MCM 用 `SKI_ConfigBase`，見 Mechanism）。**無**自訂 SKSE DLL、**無** PapyrusUtil/JContainers——狀態全靠 GlobalVariable + 腳本屬性 + cell 所有權，純 vanilla Papyrus。
- **敘事價值**：**低**。一條 7-stage 教學 quest `RE_Quest "Becoming a Landlord"`（買書→開保險箱→買第一棟→更新帳本→收租→「打造你的房產帝國」），無角色弧線、無對白分支。
- **系統價值**：**高（對 idea #22 的所有權/收益面）**。是「玩家擁有並從一個地點獲利」這條機制最乾淨的 vanilla-only 範本。

## What it does

玩家在每棟「可買」的 vanilla 建築外會看到一塊**告示牌（Property Sign）**；啟動它跳出 message-box 選單可**買下該房產**（依城市與類型計價）。買下後：

- **房子（Houses）**：可進、可放東西、變成你的住所。
- **店鋪 / 旅店（Shops / Inns）**：每隔 N 天（MCM 可調）產生**被動收入**，錢自動進你的「地主保險箱（Landlord's Safe）」。
- **礦場（Mines）**：買下後（MCM 開關下）**敵人替換成礦工 NPC**，定期產出礦石/錠送進保險箱。
- **農場（Farms）**：定期產出農產，可選送保險箱或送某旅店。
- **賣出**：隨時可把房產賣回（賣價 = 買價 × MCM 的 `SellPriceMult`）。
- **MCM 全參數化**：基準價、各城市倍率、各類型收益倍率、收租週期、隨機收益、是否需要 perk 才能買、礦場敵人替換開關等（見 `RE_RealEstate_ENGLISH.txt` 的 page 結構：Houses/Shops、Inns/Specials、Mines/Farms、LocationMult、Compatibility、Help）。

