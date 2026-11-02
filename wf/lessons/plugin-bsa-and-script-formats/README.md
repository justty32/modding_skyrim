# 存檔體積、身份解析與清理證據

[格式事實與量測陷阱](../plugin-bsa-and-script-formats.md)｜[lessons 索引](../README.md)

## save-size-is-not-cleaning-proof

> 磁碟體積、解析後內容、身份有效性與讀取耗時是不同證據；「很大」或「可解析」都不足以批准清理。

2026-11-02 整理：ESS 的磁碟壓縮量不能直接當成解析後工作量。ChangeForm、Papyrus instance 等應按解析器的實際計法比較；來源 plugin 也不等於造成該筆變更的責任 mod。保存時的 plugin 表是身份解析基準，不能拿目前 load-order 前綴直接跨存檔比 FormID。

**Why:** 不能只憑零值決定刪除；FallrimTools 的 unattached 標籤只代表其判斷式，不自動證明垃圾或無引用。SKSE co-save 的 PLGN 保存 full／light plugin 索引與檔名；dynamic 身份仍需另找有效性證據。SKEE loader 的拒收條件可以說明機制，但未比對 source 與已安裝 binary 時，不能僅靠上游程式碼宣布特定玩家資料可刪。

**How to apply:** 把格式解析、身份對應、引用關係、原生 loader 行為及遊戲語意分層核對；保留原 pair 與回退。成功 parse 只證明格式可讀，不能代替讀回後的外觀、裝備、任務或動作驗證。callback 時間也不等於完整載入到可操作，清理減量更不能自行轉寫成加速成效。一次性、綁特定輸入的清理腳本不因此成為通用 cleaner。

來源釘選 FallrimTools `61bb57d`：[ESS 體積計法](https://github.com/mdfairch/FallrimTools/blob/61bb57d895f023617cb55045a4907849fd1ff566/src/main/java/resaver/ess/ESS.java#L1063)、[ChangeForm 計法](https://github.com/mdfairch/FallrimTools/blob/61bb57d895f023617cb55045a4907849fd1ff566/src/main/java/resaver/ess/ChangeForm.java#L145)、[保存時 plugin 身份](https://github.com/mdfairch/FallrimTools/blob/61bb57d895f023617cb55045a4907849fd1ff566/src/main/java/resaver/ess/ESS.java#L1095)、[unattached 判斷](https://github.com/mdfairch/FallrimTools/blob/61bb57d895f023617cb55045a4907849fd1ff566/src/main/java/resaver/ess/papyrus/ScriptInstance.java#L372)。這些分類／大小不等於遊戲耗時或可刪證明。

SKSE `25b7235` 的 [PLGN 讀寫](https://github.com/ianpatt/skse64/blob/25b72352adb6543fa6d0bd3795780672b2e238e0/skse64/InternalSerialization.cpp#L72)與 [ResolveFormId](https://github.com/ianpatt/skse64/blob/25b72352adb6543fa6d0bd3795780672b2e238e0/skse64/Serialization.cpp#L280)，以及 SKEE `479ecab` 的 [ActorMorphs::Load](https://github.com/expired6978/SKSE64Plugins/blob/479ecabf8e1208a31dae1e492dae3b851ec26fa2/skee64/BodyMorphInterface.cpp#L2208)，只作公開機制依據；沒有證明它們與特定已裝 binary 同版。本頁不提供刪除操作或重開舊案例。
