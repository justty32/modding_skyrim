# 施工切片 S1–S7：核心星盤（第一波）

[phases](phases.md)｜[design](design.md)｜[decisions](decisions.md)

path:line 相對於 `PKG/source`（見 [phases](phases.md)）。

## S1 每級 1 點＋舊存檔免費重置

依賴：無。派給：普通線（文字同步可交雜活線）。規模 M。

只把 ×5 改成 ×1 的話，現行 `DecodeRecords`（`src/PoeGraph.cpp:64` 起）會因配點超過 Earned 把舊存檔判成 malformed，所以點數與免費重置必須在同一片、同一包上線。

- 點數：`src/PoeGraph.cpp:43` 的 `Earned()` 把 `*5` 改成具名常數 `kPointsPerLevel=1`，宣告放在 `include/FWM/PoeGraph.h:22` 旁。
- 文字：`src/PoeRuntime.cpp:80` 的 log、`config/Translations/FightWithMe_ENGLISH.txt:830`、`paths/config/Translations/IndependentSkills_CHINESE.txt:26`（原文 "Five points per highest observed level"）。
- 存檔格式：`paths/src/Main.cpp:497-501` 保留 POEG v2 讀取、只供遷移；`:467-471` 寫入改成 POEG v3（u32 tag 長度＋tag＋POEP）。`src/PoeGraph.cpp:64-70` 的 `DecodeRecords` 加參數 `pointsPerLevel`，讀 v2 時用 5。
- 免費重置：`src/PoeRuntime.cpp:20`、`:115-123` 的 Load，tag 等於舊 `unit-v1` tag（`e4ea…67ab`）時保留 `highestGrantedLevel`，清空 allocated、beforeDebug、debug，設一次性提示「星盤已改版，點數已免費退回」；其他未知 tag 照舊隔離。`src/Menu.cpp:8686` 顯示提示。
- 測試：`tests/PoeGraphTests.cpp:9,13` 的期望值 5／15 改成 1／3。

Done when: `grep -n '\*5' src/PoeGraph.cpp` 沒有輸出；兩份翻譯檔都沒有 "Five points"；新測試三情境通過（舊 v2＋unit-v1 tag、allocated 5L 個 → 載入後 allocated 為空且高水位保留；未知 tag → 隔離；v3 存讀 5 輪不漂移）；`run_poe_graph.py`、`run_poe_runtime.py` exit 0。

## S2 converter：POET v3 與每份數值

依賴：無。派給：普通線。規模 M。

- `tools/convert_poe_graph.py` 的輸入與支援範圍：
  - `:18-23` 的 PATTERNS 與 `:33-37` 的 `effect()` 改成讀計畫的 `family-rules.json`、`atoms.json`、`keystones.json`，複本放 `tools/` 並附來源 sha。
  - `:24` 的 SPECIAL 與 `:66-73` 的 supported：主圖普通節點與一般鑲嵌座一律 supported；mastery、昇華、proxy、expansion、blighted 照舊不支援。

converter 的份數、輸出與檢查：

- 節點份數＝層級權重（1／3／5）；延後的 10 個 keystone 用 `佔位` 欄，第一批 keystone 在自己的段上線前走通路規則。
- `:76` 的 Effective 描述改成列出 atom 與實際值（份數 × `per_share`）。
- `:95-97`、`:112` 的 profile 改成新名（如 `share-v1`）；`:108` 升 POET v3，在 metadata 之後追加 atom 表（kind、AV 路線、`per_share`），不帶 caps 表。
- 設計檢查：全圖移速 ≤30%、攻速 ≤50%、單點速度 ≤5%，不過就 exit 非 0。
- golden：用 poe-calib 的節點解析（同一 data.json SHA）從計畫資料產生逐節點 atom 份額，存成新包的 test fixture。
- `tests/run_poe_graph.py:15-19` 的期望值改成新份額。

Done when: converter report 的 `supported`＝1993、`reachableSupported`＝1993；逐節點份額與 golden diff 為空；設計檢查印出移速 26.2、攻速 48.9 並 exit 0，速度超標的反例 fixture exit 非 0；`run_poe_graph.py` exit 0。

## S3 unit-v1 擴充為 atom runtime

依賴：S2。派給：普通線。規模 M–L。

- `include/FWM/PoeGraph.h:9-10`：Kind 擴到 27 種 atom，保留 1–9 的舊值。
- `src/PoeGraph.cpp:33`：Validate 不再要求 `kind≤8`、`amount==1`；改成 amount>0，且每個節點的份數加總等於層級權重 ±1e-4。`:39-40` 的 header 接受新 profile 並讀 v3 的 atom 表。
- `src/PoeRuntime.cpp:24-37`：固定 6 個 AV 的陣列改成依 atom 表彙總，值＝份數 × `per_share`，四類增傷合併各來源，**不夾值**。`:42` 沿用 `PoeOverlay::Amount`；`:47`、`:54` 的資源保比例擴到 Stamina；`:78` 的 pin 改成新 profile 與 convertedHash。
- `include/FWM/PoeOverlay.h:5-9`：WeaponSpeedMult 基值 0 視為 1.0，另寫專用函式。
- `src/Menu.cpp:8703`、`:8737`：UI 顯示各 atom 的有效值。
- 測試：`tests/PoeRuntimeTests.cpp`、`run_poe_runtime.py` 用 doubles 驗寫入值。

Done when: `run_poe_runtime.py` exit 0，新案例通過：混合節點的 AV 寫入值＝份數 × 每份值；notable 寫入值是小點的 3 倍；50 份 DMG_2H 寫入 +150% 不被夾；ATKSPD 基值 0→1.0；Stamina 降上限時不致死。

## S4 新 ESL＋carrier perk

依賴：S3。派給：DLL 接線給普通線；ESL 記錄本體要有 Mutagen／houseCARL 的環境（家中）。規模 M。

- 新增 `PathOfTheCompanions_PoeStar.esl`，規格見 [mechanics](mechanics.md#共用系統)：CRIT、CRITDMG、STAGGER、BLOCK 四個 PERK，各一個 entry point，用 `Add AV Mult` 或 `Multiply 1+AV Mult` 讀各自的 carrier AV；預留 S8–S14 的 MGEF／SPEL FormID 區段。
- 施工前對照 <https://ck.uesp.net/wiki/Perk_Entry_Point> 核實 entry 名稱。
- DLL：`src/PoeRuntime.cpp` 的 Apply 在 atom>0 時 `AddPerk`、=0 時 `RemovePerk`；FormID 由 `TESDataHandler::LookupForm(localId, esl名)` 取得；ESL 不在就停用這 4 個 atom 並在 UI 註明。

Done when: 以 houseCARL 掃整合包，5 個 carrier 候選的引用結果有留檔並選定 4 個零引用的 AV；`instance/tools/check_masters.py` 對新 ESL 的 `present=no` 為 0；`python3 -m esplib header` 顯示 ESL flag 與 4 筆 PERK；ESL 缺席時的停用路徑有測試且通過。

## S5 受傷管線與施法扣耗 hook

依賴：S3。派給：普通線。規模 M。

- 進傷害 hook：在扣 HP 之前呼叫一條 handler 鏈，K1 keystone 與 S9 護盾都掛在這條鏈上。hook 位置由本片先查（CommonLibSSE-NG 的命中／傷害路徑），結論寫進新包 CODE_MAP。
- 施法扣耗 hook：與 Skald `CastTimer` 同區（`src/Skald.cpp:915` 起），給 Blood Magic、Eldritch Battery 用；要蓋住 AI 施法前的魔力檢查。

Done when: 離線測試以 doubles 驗：沒有 handler 時傷害不變；掛上「40% 先扣魔力」handler 時 HP 扣 60%、MP 扣 40%；handler 拋例外時原傷害照常扣；施法扣耗改扣 HP 的 handler 生效、未掛時耗魔不變。

## S6 POTC 技能倍率

依賴：S3。派給：普通線。規模 M。

- `Abilities` 讀 SKILL 的有效值 x（份數 × 1%）。
- 持續：`include/FWM/Paths.h:708-740` 的秒數常數乘 (1+x)；Skald 演奏持續 `src/Skald.cpp:1015` 乘 (1+x)。
- 半徑：同檔 `kRainRadius`（`:724`）等常數乘 (1+x)。
- 冷卻：乘 (1−x)，不低於 ×0.5（防負值）。

Done when: `run_ability_conditions.py`、`run_nativecombat_offline.py` exit 0；新案例：SKILL=0 時所有常數不變，SKILL=25% 時持續、半徑 ×1.25、冷卻 ×0.75，SKILL=80% 時冷卻 ×0.5。

## S7 技能類別調查

依賴：無。派給：普通線（調查，走 investigation 工作流）。規模 S。

問題：PoE 的技能標籤（Spell、Attack、Projectile、AoE、Melee、Bow、Minion、Totem 等）能不能對到 Skyrim 的法術學派、施放／投遞方式、投射物種類（箭矢、弩矢、法術投射物），以及 runtime 用什麼條件區分（perk 條件函式、MGEF archetype／delivery、projectile form type）。

Done when: 調查 REPORT 存在，每個 PoE 技能標籤一列（可對應／部分／不可）並附 CK 或 CommonLib 來源位置；給 S8 的規則修改提案存成資料檔。
