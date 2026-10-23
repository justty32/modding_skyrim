# mod-update — 已裝 mod 升版的比對與後置清單

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

把「某個已裝 mod 出新版」從查證到部署收尾走完，重點是升版後**一定要重做的衍生物清單**——多次事故（BSA 重打包漏做、zh 層被新版拖垮、FOMOD 選項漏抄）都是因為把升版當成單純換檔。

**何時用**：現役 mod 要升版、或 `housecarl_update_status` 報 OUTDATED 要處理。
**何時不用**：全新安裝 → nexus-intake；只改排序/啟停 → profile-change；一整套系列新進場 → nexus-intake/series。

## Done when

- 升版比對紀錄存在（新舊版 record/FormID topology 差異、或「純素材無 plugin 變化」的判定依據）。
- 後置清單逐項有勾選紀錄（做了／不適用，缺一項不算完）。
- MO2 關閉狀態下 `reverify.py` 通過，profile 三檔實讀驗收。

## 流程

### 查證與隔離比對

1. **查證**：`housecarl_update_status` 讀本地快取拿 `id#fileid`，餵 `housecarl_nexus_check_updates` 對檔案級確認（版本字串比較會騙人，多檔頁要對準確的 fileid）；`changelog=true` 讀更新內容。版本比較判不出就標 UNKNOWN，不硬猜（lessons/housecarl-and-tools 的 version-compare 節）。
2. **隔離安裝**：新版裝進**新的 MO2 資料夾**，不覆寫舊版；FOMOD 件先跑 `instance/tools/fomod/` 工具鏈，選項對照舊版 fomod-choices／audit 結果逐項核對（照抄選項要重跑軟依賴稽核）。
3. **比對**：plugin 有變 → houseCARL 比 record 數／FormID 集合／masters（拓撲比對是同版與相容的真閘門，API 版號不是）；純素材 → 檔案清單＋md5 抽樣。比對結果決定衍生物哪些要重做。
### 後置清單（逐項勾）

4. 衍生物重做：
   - [ ] **SEQ／BSA 重打包**：該 mod 若在重打包 SEQ 的 BSA 清單內，更新後要重做（lessons/mo2-profiles 的 game-rewrites 節）。
   - [ ] **中文層**：同名覆蓋的 zh 層先跑拓撲比對，落後就以新本體 esp 為載體重搬字串，不拿舊 zh esp 出貨（lessons/translation-and-zh 的 zh-carrier 節）。
   - [ ] **facegen／換臉層**：素材更新會改 FormID、HDPT；有 Look-From 層的要重驗 facegen 對應。
   - [ ] **LOD**：查 `DynDOLOD.esp`／`Occlusion.esp` 的 master 是否釘住此 mod，有就排 LOD 重跑。
   - [ ] **補丁與下游 master**：`check_masters.py` 掃誰依賴舊版 plugin；ESL 化／FormID 重排的升版要全套 addon 跟著換。
   - [ ] **動畫**：OAR/行為檔類更新清 cache、非 ASCII 目錄名重掃。
### 部署與留檔

5. **部署與驗收**：切換啟用走 profile-change（或只產出待啟用清單交持鎖線）；MO2 關閉後跑 `reverify.py`，plugins.txt 實讀 `*`；孤兒舊 plugin `.mohidden`。
6. **留檔**：升版紀錄（舊版→新版、比對結論、後置清單勾選）進線目錄 REPORT；mod-library 來源層同步，不讓部署層單方漂移。

## 交接

- 實機行為驗收 → runtime-qa 或 WAIT_USER；升版引發崩潰 → [crash-triage](crash-triage.md)；大批升版排程 → agent-dispatch。
