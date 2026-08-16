# Active provider / caller evidence

這是 `Modpack-KR-Dev` 在 2026-08-15 20:42 +08:00 的唯讀 snapshot，不是對未來
profile 狀態的永久宣稱。

```text
modlist.txt SHA-256: 93241981bbb6785254b5ed3d0e5106a56a049c0afcb459ff319a583073b7284e
enabled mods resolved: 148
loose PEX scanned:       969
packed PEX scanned:      4,019
archive read errors:     0
exact function-name hit: 1
```

唯一 provider／hit 是：

```text
RaceMenu.bsa::scripts/nioverride.pex
```

沒有其他啟用 PEX 的 string table 含 `GetNodeTransformScaleMode`，因此 snapshot 中沒有已編譯
的直接 Papyrus caller。檢查同時確認啟用 mods 沒有 loose `NiOverride.pex`；官方 RaceMenu BSA
是唯一現役 provider。

Papyrus 正常靜態呼叫會把 function 名稱留在 PEX string table，所以這能覆蓋 snapshot 中已啟用
的 loose／BSA scripts。它不涵蓋未啟用或未來新增的 mods、執行期組字串的反射呼叫，以及直接
使用 C++ interface 的 SKSE plugin。

完整方法、provider 輸出與 BSA 讀取證據記錄於部署工作區：
`/home/lorkhan/notes/projects/modding/skyrim/logs/racemenu-nioverride-signature-2026-08-15.md`。
