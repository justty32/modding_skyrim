# Source — RaceMenu NiOverride signature patch

## 目標來源

- 上游：RaceMenu Anniversary Edition `0.4.20.0` Steam
- Nexus：<https://www.nexusmods.com/skyrimspecialedition/mods/19080>
- 本機官方保存檔：
  `/home/lorkhan/skyrim_mods/RaceMenu Anniversary Edition v0-4-20-0-19080-0-4-20-0-1776620918.7z`
- 建立日期：2026-08-15

| 來源物件 | bytes | SHA-256 |
|---|---:|---|
| 官方保存的 7z | 8,657,597 | `e0f5e923f1eaaefefcb0a98822df091c5b96b010d2df2b52dc377aae539097da` |
| 7z 內／已安裝的 `RaceMenu.bsa` | 16,592,056 | `2e4a47aefa8a12dad1b3d3dfa58f3b39e9672b24e66e4d0a3c2b0b7ddcc6c6ab` |
| 7z 內／已安裝的 `SKSE/Plugins/skee64.dll` | 2,521,088 | `5225e4e3b185e6fc57c8d31b0cedbe5a030a951d9a744d33071b64c45a38c208` |
| BSA 的 `scripts/NiOverride.pex` | 12,935 | `862d0e76173ebb2c790fccce2305c00ed5ea11a1f8e2dfc103ea296b2fbf8a0d` |
| 本產物 `Scripts/NiOverride.pex` | 12,935 | `d571109d7beea5b5bc7c0e2e6ca262789b4c4f77336cd90af4e84d83c44072f2` |

官方保存檔解壓後，BSA 與 DLL 均和現役 RaceMenu mod 內的檔案逐 byte 相同。上游原始
PEX 不隨本包另存；`tools/build_patch.py` 要求操作者提供 exact-hash source。

## 合約依據

RaceMenu 作者的官方 source 把此 API 寫成 `UInt32`，並用
`NativeFunction5<..., UInt32, ...>` 註冊；作者的 SKSE64 fork 把 `UInt32` 映射為
Papyrus `Int`：

- [PapyrusNiOverride.cpp：native 實作](https://github.com/expired6978/SKSE64Plugins/blob/348607e9ae5f360ccab0d623e8b0d8f42e586fa6/skee64/PapyrusNiOverride.cpp#L1147-L1152)
- [PapyrusNiOverride.cpp：native registration](https://github.com/expired6978/SKSE64Plugins/blob/348607e9ae5f360ccab0d623e8b0d8f42e586fa6/skee64/PapyrusNiOverride.cpp#L2330-L2341)
- [PapyrusValue.h：VM type enum](https://github.com/expired6978/skse64/blob/01782f27650586b71592c36ffa7229c06aedd478/skse64/PapyrusValue.h#L66-L73)
- [PapyrusArgs.cpp：`UInt32` mapping](https://github.com/expired6978/skse64/blob/01782f27650586b71592c36ffa7229c06aedd478/skse64/PapyrusArgs.cpp#L252-L259)

本機 DLL registration 反組譯也得到 return VM type `3`（Int）；相鄰的
`GetNodeTransformScale` control 為 type `4`（Float）。詳細診斷來源是部署工作區的
`logs/racemenu-nioverride-signature-2026-08-15.md`。

## 已知未修項目

官方 native getter 的 predicate 仍有另一個獨立 bug：以
`kParam_NodeTransformScaleMode` 查值，卻比較 `kParam_NodeTransformScale`。本產物沒有
也不能從 PEX 修正 DLL 機器碼，所以只恢復 native binding，不保證 getter 回傳有效 mode。

## 重製方法與授權邊界

```bash
python tools/build_patch.py --source "/path/to/extracted/scripts/NiOverride.pex"
```

工具只在 exact source hash、12,935-byte size、offset `10536` 的
`00 A3 00 D2` 結構 guard 同時成立時，把 return-type string index `D2`（`Float`）改成
`CC`（`Int`）。這是針對特定官方二進位的衍生修補；使用與散布仍須遵守 RaceMenu 上游授權與
Nexus permissions。本 repo 沒有授權以此產物取代或重新發佈 RaceMenu 本體。
