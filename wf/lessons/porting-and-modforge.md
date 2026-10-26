# 資產移植與 ModForge 工具評估

[lessons 索引](README.md)

把外部遊戲資產／工具搬進 Skyrim、或評估 ModForge 能否生成某功能時反覆踩到的方法論與邊界。

## asset-porting-feasibility-checklist

> 判斷能否移植某遊戲資產進 Skyrim 要過四道獨立關卡（容器解密／網格轉換／場景佈局／碰撞），佈局最容易低估；判加密要用工具快速實測不查文件；鐵律僅本機個人使用；移植管線除靜態擺放檔也要讀事件腳本才抓得到開場初始狀態

2026-08-11 判準：四關（容器/網格/佈局/碰撞）各自查證，單一難度分數會過於樂觀；佈局最容易被低估（沒有它只抽到散裝資產），碰撞反而是唯一可通用演算法重生的一關；「已完成移植」案例若全是單體裝備、沒有地圖佈局，不能當佈局管線已解的佐證。判加密比查文件準的做法是直接拿 AssetStudio（Unity）／FModel（UE4/5）開一下安裝目錄，要完整場景重建才上 AssetRipper。移植鐵律：僅本機個人使用絕不發佈，現行營運網路遊戲（anti-cheat/EULA 禁反向工程）一律排除或降到最後。事件腳本：darksouls-port 只讀 MSB 不讀 EMEVD 會漏掉開場 `Constructor()` 關閉物件的初始狀態（例：`o8510` 補地板蓋洞口），移植版會「一開始就看到本該觸發劇情才出現的塌陷」。

**Why:** 單一難度分數或「已有人移植過」的佐證都會掩蓋佈局/事件腳本這類最容易漏掉的關卡。

**How to apply:** 評估新移植來源先四關各自查證＋鐵律排除；讀取管線除靜態擺放檔外一定連事件腳本一起讀。相關：[[dsport-render-constraints]]

## modforge-external-tool-survey-and-dependency-policy

> 外部工具/library 要補 ModForge 缺口前先查兩件事：授權（GPL 系列只能重新實作概念不能搬碼）與有沒有無頭 CLI/API；ModForge 本身外部依賴策略是 native/SWF library 一律 opt-in、預設零依賴，含用 Quest Conditional bool 做偽 MCM 免裝 SkyUI

tool-survey 盤點結果（多個候選卡在同一組關卡）：Wrye Bash 的 LeveledListsPatcher 是 GPL-3.0，想用其 leveled list 自動合併能力必須重新實作演算法不能搬碼，且邏輯綁死在 wx GUI 沒有無頭介面；CKPE 只穩定/加速 CK GUI，沒有任何 command-line/batch 介面，不能當 facegen 自動化 API；SkyPlace 證明 runtime reference 互動 UX 可行，但沒有 ESP writer（只存進存檔 sidecar）也沒有 LICENSE，不能補場景編輯缺口。依賴策略（盤點 JContainers/PapyrusUtil/powerofthree's Tweaks/SkyUI/UIExtensions 後定）：ModForge 產出的 plugin 一律不得在功能上依賴這些 native/SWF library 存在，要做開關寧可先用純 `extends Quest` Conditional bool + `GetVMQuestVariable` 做偽 MCM，只有真的需要玩家選單才 opt-in 生成 SkyUI 依賴。

**Why:** 授權與無頭介面任一缺就只能當設計參考，不能直接整合；外部依賴等於強迫終端使用者多裝 mod。

**How to apply:** 評估第三方 mod 工具先查授權＋無頭介面兩項；ModForge 新功能需要外部 library 一律設計成 opt-in 區塊，預設路徑零依賴，最低成本開關優先用偽 MCM。

## modforge-record-boundary-and-tooling-gotchas

> 評估 ModForge 能否生成某功能看核心邏輯是 record/JSON/ini 還是編譯進 DLL（不看開源與否）；大規模對話投放也是全靠 condition+FormList+override 不靠複雜 Papyrus；console `coc` 只吃 CELL EditorID 不吃 XMarker；`dump` 不展開 XMRK subrecord 要配 raw-byte grep；本機無 BSA/PEX 工具時自寫 Python parser 比找第三方庫可靠；xLODGen 要另外去官方 GitHub 抓、四個 LOD 級別要各用全新空白輸出目錄

多份 mod-survey 得出一致判準：ModForge 是 build-time JSON→esp 的 record 生成器，若選單/邏輯編譯進消費者 DLL（不論開源閉源）就只能列為前置依賴，只有 config/record/loose 文字檔層級才在可生成範圍。同一條邊界在內容規模化上也成立：參考 mod 的腳本裡，對話投給誰的邏輯全寫在 condition（尤其 `GetIsVoiceType`）＋FormList 靜態名單＋override 既有 vanilla INFO，真正需要生成的 Papyrus 只有節流計時器/短 fragment/alias clear 三類小東西，但 ModForge 目前沒有取出 vanilla Quest/DialogTopic/INFO 覆寫的入口也不支援 `GetIsVoiceType`/`IsInList`。操作面四個坑：Skyrim console 的 `coc` 只吃 CELL 的 EditorID，要送到特定 XMarker 得先 `coc` 該 cell 再 `player.setpos`；ModForge `dump` 不展開 REFR 的 `XMRK` subrecord，驗旗標要另外 `rg -aob` 對編譯後 ESP 做 raw-byte grep；本機找不到能把 BSA 當 archive 開的工具／庫時，自寫 Python 讀 BSA v105 header 就解出全部檔案，PEX 同理自寫 header/string-table 解析器不必完整反編譯器；xLODGen 不含在 SSEEdit/DynDOLOD 工具組內要去 sheson 官方 GitHub release 抓（論壇連結會 403），且已存在的 DDS 會讓它跳過生成，LOD4/8/16/32 四級要各用全新空白 output 目錄不能疊代產生。

**Why:** ModForge 的生成能力邊界在「資料驅動 vs 編譯進二進位」，內容規模化與工具鏈的「沒有官方文件化介面時自己動手」是同一種務實判準。

**How to apply:** 評估新框架/新範式先問消費的是 record/condition 還是 DLL/Papyrus 邏輯；要做對話包優先補 `GetIsVoiceType`/`IsInList` condition 與 dialogue override 入口；驗收 map marker 類 record 要加 raw-byte grep；缺工具先評估自寫 minimal parser 能否滿足需求層級再卡關；LOD 產出前先確認空白輸出目錄與工具來源。
