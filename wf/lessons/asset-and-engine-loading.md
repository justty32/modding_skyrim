# 素材存在性與引擎載檔機制

[lessons 索引](README.md)

## asset-existence-and-overlay-diagnosis-needs-multilayer

> 「這東西存不存在／有沒有被蓋掉」不能只查一層；record 層、原版 BSA、同路徑跨 mod 覆蓋序，任一層漏查都會下錯結論。

2026-08-30～10-09。檔案路徑交集為 0 不代表沒衝突——兩個 mod 可能用不同檔名表達同一護甲槽，要查 record 層（ARMA model path 實際解析到哪個檔）才知道真贏家。「某類資產是否存在」要五層都查完才能下「不存在」：壓縮檔列表、已安裝 loose files、BSA 內容原始位元組掃描、本機 DB regex、md5 回溯，少一層就標 UNKNOWN；查缺件工具不掃原版遊戲 BSA 會把原版自帶檔誤判成「缺件」。UI 面板消失但沒報錯時，真因常是另一個 mod 用更舊版本的同路徑資產（如 `interface/*.swf`）覆蓋序更高。檔案路徑交集、工具自己的索引範圍、功能 mod 自身的 log，三者都只是「真相」的子集。

**How to apply:** 查「覆蓋/相容」類問題除了檔案路徑交集一定加 record-level 解析（houseCARL resolve/cross_plugin_query）；查「存不存在」跑完五層再宣告；查「功能/UI 消失但無錯誤」先 find 全 mods 目錄同路徑同名資產，列優先序與內容特徵再判贏家，不能只查功能 mod 自己的 log。「部分部位貼圖壞但不是全部」時，建一次 esp→ARMO→ARMA→nif→BSShaderTextureSet 全鏈路索引（全部啟用 mod 的 loose＋BSA），逐貼圖路徑判 WINS／BSA／ABSENT，再拿原始 FOMOD 包清單把每條 ABSENT 歸因成「上游漏檔／optional 沒裝／無害執行期覆蓋」之一（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-19/yva/REPORT.md:14-37`）。相關：[[missing-master-scan-mast-not-housecarl]]。
source: agentctl/handoffs/done/2026-08-30/bikini-2026-08-30/FINDINGS.md:25-73；agentctl/handoffs/done/2026-10/home-2026-10-09/crash/REPORT-console.md

## engine-file-loading-mechanics-not-intuitive
<a id="loose-files-always-override-bsa-regardless-of-mo2-priority"></a>

> plugin/資產贏家判定有一串違反直覺的引擎規則，不能用副檔名、modlist 位置或檔名猜；要讀 TES4 flag／實際 conflict tree／skse64.log。

2026-08～10 驗證，都是「看起來應該怎樣」跟「引擎實際怎麼做」對不上的地方。**plugin 與 master**：`.esl` 副檔名一律贏過所有 ESP 不管 modlist 位置多低，ESPFE（esp+ESL旗標）保留原位置不一定贏，判 light master 要讀 TES4 header `0x200`；`Skyrim.ccc` 裡落地的 plugin 是隱含 master、不受 plugins.txt 勾選控制（CC 大量落地會讓隱含 master 數暴增）；拔一般 esp 型 mod，Skyrim 按名字重新對應不會讓其他 plugin FormID 位移，真正留痕的是殘留腳本；「Alternate Armors」算 1 件 mod 實際是 14 個 plugin，估規模用檔案數；ESLified 補丁重排 FormID，換裝後存檔寫入即不可逆，所有 addon 要全套跟著換；有些原版 GMST 是引擎硬編預設值、esm 裡沒有該 record，衝突檢查要按 EditorID 不能按 FormID。

**鬆散檔與 BSA**：同名鬆散檔永遠贏過同名 BSA 內容，與 MO2 優先度無關；SSE 只接受 BSA header version 105，Oldrim 的 104 在 archive 註冊階段 AV，同名不同內容 BSA 重複註冊是同家族另一種（2026-08-30 VIGILANT「版本不匹配」：標 `TEST HARNESS` 的舊中文層殘留鬆散 `vigsafetyquestscript.pex` 蓋過現役 BSA 內同名腳本，`agentctl/handoffs/done/2026-08-30/vig-2026-08-30/ROOT-CAUSE.md`）。BSA 檔名跟自己 plugin 不同名，遊戲不會自動載入也不報錯，修好同名後還要查是否被更高優先權的 mod 蓋掉（RS Children 案例）；多包一層頂層 `data/` 會讓 MO2 VFS 映射成 `Data/data/...`，整包死檔不報錯；「Plugin Replacer」只換 esp 不換 bsa，要新舊都啟用用排序贏；兩個 mod 給同名 DLL/INI 要看 skse64.log 確認載入哪個版本。

**排序與 patch**：modlist（檔案優先權）與 plugins.txt（紀錄勝者）方向沒對齊會做出自相矛盾的混合狀態；要不要建 forward patch 看「有沒有東西流失」，不是 winner 是誰；「只改某 CELL」的 mod 常連帶覆寫 persistent ACHR 所需的 WRLD 頂層與外層 persistent CELL，是引擎結構性要求；navmesh 若雙方都是實質改動（非 CK ±1 頂點雜訊），排序只會讓一邊整片退化，要停工列選項給使用者裁示。

**How to apply:** 裝完任何借用／覆蓋件第一步讀安裝後實際 winner（houseCARL resolve/conflict tree 或 skse64.log），不要用副檔名／modlist 位置／檔名猜；部署 CC／框架前先查 implicit master 數；懷疑 mod「裝了沒效果」先核對 BSA 檔名是否與 plugin 同名、VFS 底下有沒有多包一層 `data/`；版本對不上時額外掃鬆散檔（尤其 `scripts/*.pex`），`meta.ini` 標 TEST HARNESS 的優先懷疑；崩潰堆疊反覆同一 BSA 檔名時先讀 header 版本號；GMST／navmesh 類衝突查無結果就改查 EditorID 或停工回報，不要硬排序。相關：[[game-rewrites-plugins-orphans-and-seq-bsa]]。
source: agentctl/handoffs/done/2026-09/home-2026-09-03/ae2/REPORT.md:104；agentctl/handoffs/done/2026-09/home-2026-09-07/rsc/REPORT.md:18,101；agentctl/handoffs/done/2026-10/home-2026-10-10/batch3/REPORT.md；agentctl/handoffs/done/2026-08-30/vig-2026-08-30/ROOT-CAUSE.md

## runtime-state-mechanics-not-file-based

> mod 的某些狀態活在存檔／執行期而非檔案層，裝新版 esp、改覆寫層、或用載入期篩選工具都動不了它。

2026-10。用 GLOBAL 控制且已寫入存檔的設定（如 DAc0da 延後開始等級），重裝新版 esp 不會回溯更新存檔裡的舊值，要玩家主控台 `set` 覆蓋；OBody NG 的快捷鍵是存在存檔裡的 Papyrus 屬性，MCM 改鍵經 `OnOptionKeyMapChange` 寫回存檔，覆寫層（layer_apply）碰不到，只能進遊戲用 MCM 改；SkyPatcher 這類「載入期依基底屬性篩選」的工具擋不到 NFF 之類「執行期才把普通 NPC 收成隨從」的情況，因為那些 NPC 的基底一開始沒有隨從 faction。

**How to apply:** 收到「改某設定/排除某類 NPC」需求前，先確認目標在 ini/esp（可覆寫層）還是存檔內 Papyrus 屬性／GLOBAL（只能進遊戲或主控台改）；用 SkyPatcher／SPID 類工具做排除清單時要在交接書寫明「無法涵蓋執行期才轉換身份的對象」，不要承諾完全涵蓋。
source: agentctl/handoffs/done/2026-10/home-2026-10-10/batch2/REPORT.md；agentctl/handoffs/done/2026-10/home-2026-10-03/obodykey/REPORT.md

## casefold-first-match-is-not-runtime-file-selection

> 靜態 resolver 的第一個大小寫匹配只能證它自己的選擇，不能證 Wine／USVFS 實際開了哪個檔。

2026-11-02。同一 Linux mod 目錄可留有僅大小寫不同、內容也不同的兩個實體。`instance/tools/whichmod_vfs.py:54–61` 的 `ci_child` 取第一個匹配；`projects/houseCARL/src/housecarl-core/AssetResolver.cs:527–546` 用 `map.TryAdd` 保留首次列舉項。兩者可支持層間優先判斷，不能解決層內碰撞，也不能把兩個 resolver 一致當成 runtime 觀測。原包相同 hash 可證來源成員；若多個 FOMOD 選項含同一成員，不能反推當初選項。

**How to apply:** 保留每個實體的 hash／來源，碰撞標未決。要證實際選檔需可信角色首次載入的 open／mmap 等事件，對回實體 inode／hash；沒有觀察到 fd 不代表未載入。NIF 可列印貼圖字串也不等於完整 shader block 解析或畫面一定採用。

來源：private `agentctl/handoffs/home-2026-11-02/recorder-facegen/REPORT.md:9–11,26,36–42`；`agentctl/handoffs/home-2026-11-02/shower-runtime/REPORT.md:35`（未取得首次載入觀測，故維持未證）。
