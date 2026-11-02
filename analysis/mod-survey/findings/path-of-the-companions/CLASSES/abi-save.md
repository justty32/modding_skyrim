# 跨 DLL 與存檔契約

來源行號相對 FWM `971b8b5aba0c34c649e70307cebdaa4aaa7bf4de` 與 Paths `189f24c8a8e5b61cacfbc60b2347589c9f3eff61`；固定 URL 與名詞見 [職業入口](../CLASSES.md)。

## FWM 配對與 ABI

Paths addon 本身共用 FWM 的大量來源；配對模式中 Paths 透過 OrdersLink 讀 FWM 當前角色，所以單獨把 addon 多一個職業，不能保證 FWM 選得到或能保留它。FWM:`src/OrdersLink.cpp:17` 接 interface，`:41` 把外部數字轉為 Role，僅接受小於本地 Role::kCount 的值。公開 FWM API 的 `include/FightWithMeAPI.h:12` 目前只列到 Mage=5，甚至沒命名 Skald=6；FWM:`src/Plugin.cpp:52` 仍直接 cast 內部 enum 回傳，OrdersLink 因數字範圍判斷能接到 6。這是現有表頭不完整的事實，不是新職業任意擴充的 ABI 保證。

更直接的阻礙是 Paths API v6：FWM:`include/FightWithMePathsAPI.h:13` 定版號，`:15` 固定 kRoles=7、kNodes=15、kSlots=2，`:20` Record 內含 ranks[7][15]、slots[7][2]、bonus[7]，`:102` 的介面方法也傳數字 role。`src/PathsLink.cpp:34` 依內部 Paths::kRoles 複製這些資料；若只增加內部 Role 而不改 API，會越界存取。增加角色會改 Record 記憶體布局，必須升級或重訂 API 契約並成對建置／驗證，不能沿用 v6 聲稱相容。

即使維度不變，樹內容不同也會被拒絕：FWM:`src/PathsLink.cpp:90` 與 `src/AbilityLink.cpp:41` 均驗 interface 與 TreeSignature；FWM:`src/Paths.cpp:780` 的 Signature 混入記錄版本、Ability/Perk 數、所有樹節點資訊與 level gates。Paths:`src/Main.cpp:197` 回傳版本／簽章，`:644` 只接受完全相等的 interface version。純替換技能也可能要同步配對 FWM，並非僅第八角色才觸發。

standalone 在沒有 FightWithMe.dll 時使用自己的 embedded FWM 來源，見 Paths:`src/Main.cpp:550` 的 host 選擇；它可減少外部配對部署範圍，但仍須使內部 API adapter、Record 與 enum 一致，不能繞過結構尺寸問題。

## 存檔、ID 與遷移

Role ordinal 必須保留；新增應接在 Skald 後，不在中間插入，不重用／重排既有身份。FWM:`src/OrdersCodec.cpp:70` 將 role 存為一個 byte；`:113` 在讀取時把超出本版 enum 範圍的值 clamp 回預設 Fighter。於是新版第八角色回退到舊版時，其當前身份會變 Fighter，再存檔就失去原新身份。現有 `tests/PathsTests.cpp:42` 也明確鎖住 Skald=6。

Path record 與 DLL Record 必須分開看：FWM:`src/Paths.cpp:809` 的 co-save 用 roleCount 加逐 role 資料，不是直接 dump API struct；`:887` 讀 roleCount，`:892`、`:900` 遇到未知角色／節點會消耗資料後略過。既有角色順位固定時，舊存檔載入新增角色版本可讓新角色保持 Fresh；舊版讀新檔也可能跳過新資料，但再存檔會丟失被跳過的新角色內容。這只是 codec 的容忍機制，不能承諾降版無損；需用升版、降版、再升版 roundtrip 測試證明政策。

節點按 `(Role ordinal, Perk ID, rank)` 存，Ability/Perk enum 是 append-only；同一 Perk 可在不同 path 分別記錄，但把節點搬到另一個 role 不會自動搬走投資，見 FWM:`include/FWM/Paths.h:129`、`src/Paths.cpp:903`。移除／改排節點後還有 Repair 修正排名、技能槽與支出，契約在 `include/FWM/Paths.h:615`。若要拆 PathId，必須定義舊 Role→新 PathId 的映射，以及舊配點、目前選擇和技能槽如何搬遷；不能只換型別名稱。

目前 path record version 為 5，FWM:`include/FWM/Paths.h:629`。`src/Paths.cpp:926` 處理 v5 Skald unlock 尾段；`:931` 對 v3 以前資料整體重設投資、保留最高等級；`:939` 對 v3 Healer Ward 做特定退款修復。這些既有 migration 是行為證據，不能直接複製一個 reset 當新職業遷移。技能 ID/mask 容量的詳細限制由技能線報告補充。

