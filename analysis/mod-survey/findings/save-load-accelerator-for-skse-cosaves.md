# Save & Load Accelerator for SKSE Cosaves（S.L.A.C.K.）

本頁只研究 **v1.3.2** 的來源與界線，不代表最新版選型、已安裝版本或特定存檔的性能驗收。它是 SKSE co-save I/O 加速器，不清理 ESS、不刪 morph，也不縮減持久狀態。

本輪實讀 source commit [`16248bf91027b20c25cb91e0d64543bbb4710de7`](https://github.com/just-harry/save-load-accelerator-for-skse-cosaves/tree/16248bf91027b20c25cb91e0d64543bbb4710de7)。`v1.3.2` 是 annotated tag：tag object 為 `1c97286db71cac45219e535ed04a65d7850eee11`，其 [object 指向](https://api.github.com/repos/just-harry/save-load-accelerator-for-skse-cosaves/git/tags/1c97286db71cac45219e535ed04a65d7850eee11)才是上述 source commit；二者不是兩份不同 source 的證據。下列 permalink 固定 commit，不把 tag 名稱當永不改動，也不據此認定任何部署 binary 與 source 完全同版。

## 精確版本與作用位置

AE 版本硬比對 SKSE 2.2.6 與 `skse64_1_6_1170.dll`。該版安裝位置是 `Data/DLLPlugins/Save&LoadAcceleratorForSKSECosaves.dll`，需相應 DLL preloader；不能照其他版的路徑或依賴說明安裝。版本相容依指定源碼與 release 判斷，不為追新而推論 SKSE 可任意升版。[版本定義](https://github.com/just-harry/save-load-accelerator-for-skse-cosaves/blob/16248bf91027b20c25cb91e0d64543bbb4710de7/mod/skse64/hacks/versioning.d#L9)、[硬比對](https://github.com/just-harry/save-load-accelerator-for-skse-cosaves/blob/16248bf91027b20c25cb91e0d64543bbb4710de7/mod/slack_mod/setup.d#L237)、[安裝說明](https://github.com/just-harry/save-load-accelerator-for-skse-cosaves/blob/16248bf91027b20c25cb91e0d64543bbb4710de7/documentation/description-for-nexus-mods.bbcode#L33)。

## 緩衝不等於格式遷移

它將 serialization callbacks 的小量寫入先放進記憶體，再整塊讀寫；正常路徑保留 SKSE magic、schema 1、plugin／record headers 與 callback payload。這是減少 I/O 的機制，不代表所有情況逐 byte 等價，更不代表完整讀檔等比例加速。[格式](https://github.com/just-harry/save-load-accelerator-for-skse-cosaves/blob/16248bf91027b20c25cb91e0d64543bbb4710de7/mod/skse64/serialisation.d#L15)、[payload 緩衝](https://github.com/just-harry/save-load-accelerator-for-skse-cosaves/blob/16248bf91027b20c25cb91e0d64543bbb4710de7/mod/slack_mod/save_load.d#L168)。

例外需分開看：STB Widgets 特殊路徑遇無效 pointer 會寫零；預設 ErrorFriendlyMode 捕獲 callback 例外後繼續，該插件資料可能不完整。出現 error／exception 不能因檔案仍產生就當成功。ParallelSaving 預設關閉且標 experimental，不能把單執行緒假設下的結論延伸到平行模式。[特殊 saving](https://github.com/just-harry/save-load-accelerator-for-skse-cosaves/blob/16248bf91027b20c25cb91e0d64543bbb4710de7/mod/slack_mod/save_load.d#L357)、[例外處理](https://github.com/just-harry/save-load-accelerator-for-skse-cosaves/blob/16248bf91027b20c25cb91e0d64543bbb4710de7/mod/slack_mod/save_load.d#L650)、[預設 INI](https://github.com/just-harry/save-load-accelerator-for-skse-cosaves/blob/16248bf91027b20c25cb91e0d64543bbb4710de7/mod/Save%26LoadAcceleratorForSKSECosaves.ini#L13)。

## 寫入與量測界線

寫入使用 `CREATE_ALWAYS` 與同步整塊 `NtWriteFile`，對齊後裁至實際 EOF 並檢查錯誤；依此直接寫入路徑推論，它不提供 temporary-file＋atomic replace 的交易保證。正常同步完成也不等於背景延後保存。[開檔](https://github.com/just-harry/save-load-accelerator-for-skse-cosaves/blob/16248bf91027b20c25cb91e0d64543bbb4710de7/mod/slack_mod/save_load.d#L588)、[寫入與 EOF](https://github.com/just-harry/save-load-accelerator-for-skse-cosaves/blob/16248bf91027b20c25cb91e0d64543bbb4710de7/mod/slack_mod/save_load.d#L835)。

評估時保留同來源 save pair，分開量 co-save callback、co-save 總時間及完整載入到可操作；cold／warm 樣本不能混比。除 header／chunk／EOF parse，還要驗停止載入 accelerator 後原 SKSE 能讀它寫出的新 slot，並檢查遊戲內語意。成功 parse 只證明格式可讀；通用清理判準見[存檔格式與身份證據](../../../wf/lessons/plugin-bsa-and-script-formats/README.md)。
