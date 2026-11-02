# 相容、建構與來源維護

本頁依公開上游研究建構方式與擴充的相容界線，沒有建立新 fork、產品規格或開發排程。技能與職業接點見 [技能研究](ABILITIES.md)及[職業研究](CLASSES.md)。

## 共用來源與雙 host

研究釘選 Paths 1.2 `189f24c8` 與 FWM 0.6.0 `971b8b5`。Paths 不是獨立的完整 C++ 專案：自身 repo 主要含 Main、INI、翻譯及打包腳本，須放進 FWM 的 `paths/`，兩個 DLL 共用 FWM `src/`。CMake 排除 FWM 的 Plugin.cpp、改用 Paths Main，並以 `FWM_HOST_PATHS` 區分 host。[FWM CMakeLists.txt:424–448](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/CMakeLists.txt#L424)、[Paths README:203–205](https://github.com/fatalCMD/paths-fwm-addon/blob/189f24c8a8e5b61cacfbc60b2347589c9f3eff61/README.md#L203)。

新增技能或職業不只是修改 addon 入口；必須維持共用定義、樹簽章、跨 DLL Record 與 host ownership 一致。paired 模式與 standalone 的支援範圍應先界定，不能因能單獨編出 Paths DLL 就推論它能和任何 FWM 版本互通。[ABI 詳查](CLASSES.md#fwm-配對與-abi)

公開的另一個 [fatalCMD/potc 快照](https://github.com/fatalCMD/potc/tree/17d50320367192defc8c9966e2b7f6993874aa21) 是 1.0 initial release；其 [SOURCE-MANIFEST](https://github.com/fatalCMD/potc/blob/17d50320367192defc8c9966e2b7f6993874aa21/SOURCE-MANIFEST.json) 標記 FWM 0.5.0／Paths 1.0.0、來源 revision `6a5f5ce254f7878ef258d7ad9b655d7e2a2773d9` 且包含 working tree。它可用來研究該快照，但不能當成本頁 paired 1.2 來源；名稱相近、README 相同或 API 看似接近，都不足以證明版本可互換。

## 普通控制與能力需求

原版 Role 同時決定成長、kit、普通裝備資格與戰鬥偏好。為了與自訂隨從相容，可以研究把普通戰鬥控制與能力暫時需求分開；這是候選設計方向，不是上游已提供的任意技能／職業註冊介面。[普通裝備接管](equipment-control.md)

需要移動、目標、站定、演出或專屬裝備的新技能，須明定取得控制、優先權、失敗與撤除條件。不能假設新增 ID 後 planner 會理解新要求，也不能全停 Styles 又聲稱保留所有技能，因為既有 ShieldMaster／HeavyHands／Flanker 等使用 style tweaks。若能力刻意改變裝備偏好，就須決定它和原生選裝之間的契約。[Arts.cpp:2132](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/src/Arts.cpp#L2132)

角色資格、自動角色校正與能力資源是另外的入口；普通選裝退出不代表它們一併取消。新增職業的缺裝備行為、施法選擇與資源都要明列，不能任由 default 分支決定。[角色政策](CLASSES.md#必須審查的接點)

## 驗證種類

純 C++ 規則、ID 邊界、樹簽章、save round-trip、AUTO／資源正負例可以在適合的離線工具鏈先測。真正 Windows DLL 的編譯／連結、exports／imports／runtime 版本與配對 PDB 是另一層；上游打包腳本會建兩組 test suites，並核 DLL FileVersion 與包版號。[BuildPathsPackage.ps1:93–118](https://github.com/fatalCMD/paths-fwm-addon/blob/189f24c8a8e5b61cacfbc60b2347589c9f3eff61/tools/BuildPathsPackage.ps1#L93)

遊戲內另驗 SKSE 載入、UI／中文／手把、購買與退點、舊存檔遷移、技能發動／中斷清理與其他 mod 互動。素材變更另外驗 NIF／貼圖／音效與畫面。host tests 或主選單 smoke 都不能取代這些結果。[FWM README:168–176](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/README.md#L168)

## 長期維護候選

若確定長期擴充，可維護完整配對 FWM／Paths 來源，固定 upstream parents、CommonLib 與 build dependencies；每次交付凍結可重建 source／patch、review、測試與 manifest。僅保存變動檔快照不等於完整 source tree，patch 也應明示從哪個 parent 起算、是否累積前版修改。

名稱可使用「上游名稱與版號＋擴充名稱＋修訂＋日期」，但包名、DLL FileVersion、兩 DLL 介面版本與 co-save 格式是不同契約，不能只改資料夾名就算升版。上游腳本支援 PackageSuffix，並拒絕 DLL FileVersion 與包版號不同；shared API 改動要同步 consumer。[BuildPathsPackage.ps1:23–49、115–116](https://github.com/fatalCMD/paths-fwm-addon/blob/189f24c8a8e5b61cacfbc60b2347589c9f3eff61/tools/BuildPathsPackage.ps1#L23)

保留上游 notices、個人 `*_user.ini` 與舊成品；素材有變才另追 Effects 版本。每個候選區分 source-only、已建 DLL、已部署與已實機驗證，manifest 同時驗 committed bytes，避免 checkout 換行轉換讓 hash 不一致。[FWM split maintenance](https://github.com/fatalCMD/Fight-With-Me/blob/971b8b5aba0c34c649e70307cebdaa4aaa7bf4de/README.md#L178)
