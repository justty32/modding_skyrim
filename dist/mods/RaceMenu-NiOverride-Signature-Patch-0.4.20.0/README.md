# RaceMenu 0.4.20.0 NiOverride signature patch

這是一個只針對官方 RaceMenu Anniversary Edition `0.4.20.0` Steam 版的最小
Papyrus script override。遊戲會讀取的檔案只有：

```text
Scripts/NiOverride.pex
```

它把 `GetNodeTransformScaleMode` 的 Papyrus 回傳型別從 `Float` 改為 `Int`，使
wrapper 與 `skee64.dll` 註冊的 native signature 一致。原始 PEX 為 12,935 bytes；
產物同樣是 12,935 bytes，二進位只改變一個 byte。

## 嚴格範圍

- 只處理 `Function will not be bound` 的 signature mismatch。
- 不修改 `skee64.dll`、`RaceMenu.bsa`、ESP、設定或其他 function。
- 不宣稱修好獨立的 native getter key bug。官方 DLL 仍以 scale-mode key 查值、卻拿結果
  與普通 scale key 比較；即使成功 binding，getter 仍預期落入 `-1` fallback。
- 只接受 SHA-256 為
  `862d0e76173ebb2c790fccce2305c00ed5ea11a1f8e2dfc103ea296b2fbf8a0d`
  的官方 `NiOverride.pex` 作為重建來源。其他 RaceMenu 版本會 fail closed。

## 建立與驗證

先從 exact RaceMenu `0.4.20.0` Steam `RaceMenu.bsa` 擷取
`scripts/NiOverride.pex`，再於本資料夾執行：

```bash
python tools/build_patch.py --source "/path/to/original/NiOverride.pex"
python tools/verify_patch.py --source "/path/to/original/NiOverride.pex"
dotnet run --project tools/PexContractProbe/PexContractProbe.csproj -- Scripts/NiOverride.pex
sha256sum -c MANIFEST.sha256
```

`build_patch.py` 先驗 source hash、大小與目標結構位置，才會原子寫出產物；
`verify_patch.py --source` 另外要求 source／output 恰好只有 offset `10539` 的
`D2 -> CC` 一 byte 差異。`.NET` probe 用 Mutagen `0.53.1` 完整解析 PEX，驗證
183 個 functions、2 個 state events 與唯一目標的 `Int` return type。

## 安裝／回滾邊界

把整個資料夾作為獨立 script-only mod，置於 RaceMenu 之後，讓 loose
`Scripts/NiOverride.pex` 覆蓋 BSA 成員。回滾只需停用或移除這個獨立 override；不要改寫官方
RaceMenu 目錄。實際 profile 部署與 runtime 狀態以部署工作區為準，本 artifact 不維護機器專屬狀態。

來源與授權邊界見 [SOURCE.md](SOURCE.md)，實際驗證結果見
[VERIFICATION.md](VERIFICATION.md)，現役 provider／caller snapshot 見
[evidence/active-provider-caller-scan.md](evidence/active-provider-caller-scan.md)。
