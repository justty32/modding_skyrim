# POTC 新職業／成長路線擴充研究

研究基準為 FWM `971b8b5aba0c34c649e70307cebdaa4aaa7bf4de` 與 Paths addon `189f24c8a8e5b61cacfbc60b2347589c9f3eff61`；`FWM:`、`Paths:` 指固定 commit 的相對位置。官方來源為 [Fight-With-Me](https://github.com/fatalCMD/Fight-With-Me/tree/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de) 與 [paths-fwm-addon](https://github.com/fatalCMD/paths-fwm-addon/tree/189f24c8a8e5b61cacfbc60b2347589c9f3eff61)。

本文說明職業／技能樹／戰術角色關係、擴充接點、存檔與 ABI 風險及 Skald 案例；屬原始碼研究，不代表新增職業已實作或驗收。

## 結論與名詞

目前 POTC 的「職業」同時承擔成長路線與戰術角色。`Role` 是七個按順序編號的 enum；`Orders.role` 是目前角色，`Paths::kRoles` 直接等於 `Role::kCount`，每條技能樹、技能槽、配點與加成也以同一個 Role 索引。`PathsLink::KitOf(actor, role)` 直接從該 role 的槽取技能；升級成長則取 `GrowthFor(orders->role)`。不存在可獨立選擇的 PathId/currentGrowthPath。來源：FWM:`include/FWM/Orders.h:18,59`、`include/FWM/Paths.h:283,520`、`src/PathsLink.cpp:197`、`src/Leveling.cpp:223`。

這裡研究的是 POTC 選單裡可選的職業，不是要求新增或覆寫 ESP 中 NPC 的 Skyrim `CLAS`。已檢查的角色推斷路徑讀 NFF faction rank 與目前裝備／法術，沒有用 NPC Class 來對應 POTC Role；`Party::Loadout` 在 FWM:`src/Party.cpp:88`。`CSTY` 是另一層：FWM 會從 combat controller 或 NPC base 的 combatStyle 取原始樣式，產生執行期副本並套入角色偏好，見 FWM:`src/Styles.cpp:145`、`src/StyleLayer.cpp:24`。因此新增 POTC 職業本身不等於必須製作新 CLAS/CSTY record；若新技能需要新的遊戲表單或美術資產，才另外評估內容插件。

「替現有職業換／補技能」是較窄的工作：仍使用原角色的成長與戰術語意，沿用 15 節點版型時不增加角色維度，但仍須完成能力執行、存檔 ID 與雙 DLL 樹簽章的一致性。它並不會多出一個獨立可選的新職業。

「多一條可選專精，但沿用原戰術角色」概念上可行，現碼卻沒有現成支持；需要增加獨立選擇身份，決定哪些地方用成長路線、哪些繼續用戰術角色，並串接選單、技能 kit、配點、升級、儲存與跨 DLL 交換。若只要少量固定分支，也可研究在現有樹內增加互斥專精選擇，但現有版型／記錄沒有這套獨立專精狀態，不能稱為單純填設定。是否值得拆分要等玩法明確，不建議本輪先全面重構。

「真正新增第八個 Role」最符合現有架構的擴充方向，但涉及 UI、裝備／法術、成長、AI、技能資格及 ABI 多處接點；只在 enum 與樹陣列補一項不完整。新增職業若只是沿用既有戰術行為，仍要明確填入對應政策，不能依賴 default 分支。

## 必須審查的接點

完整內容見 [同名子節](CLASSES/README.md#必須審查的接點)。

## FWM 配對與 ABI

完整內容見 [同名子節](CLASSES/abi-save.md#fwm-配對與-abi)。

## 存檔、ID 與遷移

完整內容見 [同名子節](CLASSES/abi-save.md#存檔id-與遷移)。

## Skald 案例

完整內容見 [同名子節](CLASSES/skald.md#skald-案例)。

## 與普通戰鬥相容的關係

若另設普通戰鬥控制政策，仍須明確決定新職業是否依賴硬裝備／施法契約；新增 enum 不會自動取得正確政策。能力的暫時目標／移動要求也應獨立處理，不能假設新遠程角色自動繼承其他職業的特殊行為。

Party 資格／角色校正、技能資源與 kit 資格是分開入口；即使退出普通配裝控制，也不能推論它們已取消。上游位置為 FWM:`src/Party.cpp:151`、`src/PathsLink.cpp:203`、`src/Abilities.cpp:113`。

## 後續需要使用者決定的四件事

第一，「新職業」是新的可選技能路線／專精，還是同時需要不同的自動戰鬥行為、升級屬性與武器法術資格？這決定維持 Role 一對一，或投資獨立 PathId 的成本。

第二，新路線能否與舊職業並存／自由切換，是否保留多路配點，還是單一路線互斥？目前每角色各自存配點但只有當前 role 的 kit 生效，跨職業組技能並非現成介面。

第三，未來只支援 standalone POTC，還是也要與完整 FWM 配對使用？後者必須一併維護角色交換、API 版號與 tree signature；也要決定舊存檔保留與降版是否屬於支援範圍。

第四，新能力有沒有普通裝備／動作／演出依賴，並且要能用在有自訂腳本的隨從身上嗎？這決定 Native/RoleManaged 邊界及需要什麼遊戲內驗證；現在先保留方向，不代替使用者命名新職業或配置技能。
