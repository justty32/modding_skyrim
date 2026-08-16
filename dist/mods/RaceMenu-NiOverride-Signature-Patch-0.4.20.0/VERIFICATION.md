# Verification — RaceMenu NiOverride signature patch 0.4.20.0

- 驗證日期：2026-08-15
- 結果：PASS（靜態／可重現驗證）
- 遊戲／MO2／GUI：未啟動、未操作
- 實機部署：不屬於本 artifact 的離線驗證範圍；以部署工作區紀錄為準

## 預期靜態合約

- source：12,935 bytes，SHA-256 `862d0e76173ebb2c790fccce2305c00ed5ea11a1f8e2dfc103ea296b2fbf8a0d`
- output：12,935 bytes，SHA-256 `d571109d7beea5b5bc7c0e2e6ca262789b4c4f77336cd90af4e84d83c44072f2`
- binary delta：只有 zero-based offset `10539`，`D2 -> CC`
- PEX parse：1 object、1 state、183 functions + 2 state events、目標 function 恰好 1 個
- semantic delta：只有 `GetNodeTransformScaleMode` return type `Float -> Int`

反編譯差異固定保存在
[evidence/decompiled-signature.diff](evidence/decompiled-signature.diff)。

## 實際執行結果

```text
PASS output: exact size/hash, Skyrim PEX header, 263-string table,
unique GetNodeTransformScaleMode -> Int record
PASS source delta: exact upstream hash and exactly offset 10539 D2 -> CC
PASS manifest: 9 files match
RESULT: PASS

PASS Mutagen parse: objects=1 states=1 functions=183 state_events=2 total=185
GetNodeTransformScaleMode.count=1 return=Int size=12935
```

`cmp -l` 只有一行：1-based byte `10540`（zero-based `10539`），octal
`322 -> 314`，也就是 hex `D2 -> CC`。原版與產物的完整 houseCARL／Mutagen
反編譯 `diff -u` 只有 evidence 中那一個 return-type hunk。

`sha256sum -c MANIFEST.sha256` 的 9 個受管項目全部為 `OK`。`VERIFICATION.md`
與 manifest 本身刻意不列入 manifest，以免產生循環 hash。

## 尚待實機

本批不啟動 Skyrim。實機驗收只限 fresh `Papyrus.0.log` 不再出現：

```text
Native static function GetNodeTransformScaleMode does not match existing signature
on linked type NiOverride. Function will not be bound.
```

不得把 warning 消失寫成 native getter key bug 已修好，也不得以 getter 回傳 `-1` 判定本 PEX
patch 失敗；那是另一個 DLL-side 缺口。
