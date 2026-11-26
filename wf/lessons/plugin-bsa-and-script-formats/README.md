# 存檔體積、身份解析與清理證據

[格式事實與量測陷阱](../plugin-bsa-and-script-formats.md)｜[lessons 索引](../README.md)

## save-size-is-not-cleaning-proof

> 磁碟體積、解析後內容、身份有效性與讀取耗時是不同證據；「很大」或「可解析」都不足以批准清理。

2026-11-02：ESS 磁碟壓縮量不等於解析後工作量，ChangeForm、Papyrus instance 按解析器實際計法比；來源 plugin 不等於責任 mod；保存時的 plugin 表是身份解析基準，不能拿目前 load-order 前綴跨存檔比 FormID。FallrimTools 的 unattached 標籤只代表其判斷式，不證明垃圾或無引用；零值不足以決定刪除。SKSE co-save 的 PLGN 存 full／light 索引與檔名，dynamic 身份要另找有效性證據；SKEE loader 拒收條件可說明機制，但沒比對 source 與已裝 binary 時不能據以宣布玩家資料可刪。

**How to apply:** 格式解析、身份對應、引用關係、原生 loader 行為、遊戲語意分層核對；保留原 pair 與回退。parse 成功只證明格式可讀，不代替讀回後的外觀、裝備、任務、動作驗證；callback 時間不等於載入到可操作，清理減量不能寫成加速成效；綁特定輸入的一次性清理腳本不是通用 cleaner。

來源（只作公開機制依據，未證明與已裝 binary 同版）：FallrimTools `61bb57d` 的 [ESS 體積](https://github.com/mdfairch/FallrimTools/blob/61bb57d895f023617cb55045a4907849fd1ff566/src/main/java/resaver/ess/ESS.java#L1063)、[ChangeForm](https://github.com/mdfairch/FallrimTools/blob/61bb57d895f023617cb55045a4907849fd1ff566/src/main/java/resaver/ess/ChangeForm.java#L145)、[保存時 plugin 身份](https://github.com/mdfairch/FallrimTools/blob/61bb57d895f023617cb55045a4907849fd1ff566/src/main/java/resaver/ess/ESS.java#L1095)、[unattached](https://github.com/mdfairch/FallrimTools/blob/61bb57d895f023617cb55045a4907849fd1ff566/src/main/java/resaver/ess/papyrus/ScriptInstance.java#L372)；SKSE `25b7235` 的 [PLGN](https://github.com/ianpatt/skse64/blob/25b72352adb6543fa6d0bd3795780672b2e238e0/skse64/InternalSerialization.cpp#L72)、[ResolveFormId](https://github.com/ianpatt/skse64/blob/25b72352adb6543fa6d0bd3795780672b2e238e0/skse64/Serialization.cpp#L280)；SKEE `479ecab` 的 [ActorMorphs::Load](https://github.com/expired6978/SKSE64Plugins/blob/479ecabf8e1208a31dae1e492dae3b851ec26fa2/skee64/BodyMorphInterface.cpp#L2208)。
