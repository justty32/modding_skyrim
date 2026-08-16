# 驗證

建置完成後由 `tools/verify_translation.py` 驗證 exact source hash、四個 masters、11,976 筆
record 的路徑與 subrecord 拓撲、所有非文字 payload、10,689 個本地化欄位、UTF-8 字串表、
placeholder／數字 token、簡體殘字、可重現建置及完整 manifest。

三方比對另確認：官方 1.4.5 英文與 CHS 只有預期文字欄位不同；1.5 相較 1.4.5 新增七筆
record，而官方 BSA 與 `Thaumaturgy_DISTR.ini` 位元組完全相同。部署、VFS winner 與 runtime
結果記於 notes 側 Batch 4E 日誌。

最終來源分布：10,069 欄來自同 FormKey 的 1.4.5 CHS 並轉正／校詞，428 欄重用既有精確英文原句
譯文，80 欄為 1.5 人工術語覆核，10 欄為 1.5 改寫覆核，另有 102 個本來就是空白的內部欄位。
輸出 ESP SHA-256 為
`0191fd9e55edc5f21864b0729a4b644baffa7b15cbca26532f81c9c964b36fce`；`STRINGS` 與
`DLSTRINGS` 的 English／Chinese 別名各自位元組相同。
