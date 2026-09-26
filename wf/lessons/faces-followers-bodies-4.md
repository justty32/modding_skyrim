# 臉、隨從、身體與動畫（4/4）

[lessons 索引](README.md)｜同主題：[faces-followers-bodies](faces-followers-bodies.md)、[faces-followers-bodies-2](faces-followers-bodies-2.md)、[faces-followers-bodies-3](faces-followers-bodies-3.md)

## daegon-2212-midsave-upgrade

> Daegon 2.0.5→2.2.1.2 中途升級成功；Legacy(112097/112191) 與 2.x 不可並存；NifSwap 要四路徑同 md5；Elven Princess v1.3 對 2.2（原 type: memory）

2026-09-19 使用者實機確認：Daegon and Kaeserius 2.0.5→2.2.1.2 在現有存檔升級成功（profiles `b9b13f4`），跳過「先 dismiss」步驟也沒事，
臉／名字／髮辮切換都對。組成：`Daegon-2.2.1.2`＋`Daegon-CHS-171488-2.2.1.2-ZH-2026-09-18`（171488 拓撲同版，forward 自家名詞 8 個＋補 201 欄）
＋`Daegon-ElvenPrincess-1.3`（有角）＋`Goam-Elven-Ears-Fair-1.0`。

**Why:** 2.2.1.2 只增不改（FormID 不重編、masters 不變、非 ESL），DLL 同 NG 模板。
**How to apply:**
- `Daegon Kaekiri 112097`／`Daegon Legacy 112191` 是 Legacy 本體，plugin 同名 `k101Daegon.esp` 但 FormID 體系不同，**不是美化、不能跟 2.x 並存**。
- 本體 DLL `NifSwap()` 在室內外切髮型時用 CopyFileW 在 `facegeom/k101Daegon.esp/00005900{,Stock}.nif` 與 `facegeom/temp/` 之間互換：換臉層四個路徑都要放同 md5，否則切一次髮辮就變回原臉。
- 角與 Goam 耳是烤進 facegen 的無 HDPT 多餘 shape，引擎容忍（作者出貨方式就是這樣）；補 HDPT 的備案工具在 `agentctl/handoffs/home-2026-09-18/dgn2/tools/`。
- 升級後開機的 alias 綁不到／None 錯誤是舊存檔過渡一次性雜訊。
相關：[[daegon-itemfinding-script-ctd]]、[[facegen-headpart-count-mismatch-discards-facegen]]

## oar-copy-folder-bypasses-gates

> 把 OAR／DAR 資料夾的 hkx 抄進自己的覆蓋層時，原資料夾的閘門條件（HasKeyword／HasMagicEffect／PRESET 等）就沒了；判「目前贏家」只看 IsActorBase 會抄到 NPC 專用或特殊狀態的動畫，玩家直接 T 字（原 type: memory）

2026-09-06 mcoi 線為了保住「沒切姿態時的原本招式」，把 recompute 算出的贏家資料夾抄成 `<武器>-neutral`（只留 IsEquippedType＋IsActorBase 玩家）。recompute 只排除 NPC-only 的 IsActorBase，結果徒手／匕首抄到古劍三隨從專用爪擊（HasKeyword Gujian3_Follower:AAF6）、斧錘抄到召喚獸形態、劍盾抄到 EldenCounter 反擊瞬間（HasMagicEffect）。使用者徒手一揮就 T 字，8 種武器全中。

**Why:** OAR 是在遊戲裡即時評估條件的，資料夾本身「優先度最高」不等於「玩家一般狀態會用到」。抄檔案不抄條件＝把所有閘門打開。動畫本身給別的骨架或狀態做的，套到玩家身上就是 T 字或鬼畜。

**How to apply:** 算「玩家一般狀態的贏家」時，凡有任何啟用中的 HasKeyword／IsWornHasKeyword／HasMagicEffect／HasPerk／IsInFaction／IsRace／PRESET／Random／CurrentTargetDistance／CompareValues／非武器類型的 IsEquippedHasKeyword／非玩家 IsActorBase（含 negated），一律不算候選。更好的做法是不要抄檔案，改用「條件鏡射」：覆蓋層 config 把來源的整組條件原樣帶上再加姿態條件。修好的工具在 `agentctl/handoffs/home-2026-09-06/mcofix/`。相關：[[rule-out-a-concept-scan-same-batch-siblings]]（同批要掃）、[[leads-must-not-end-turn-to-wait]]。

## oar-non-ascii-animation-dir-kills-cache

> Proton 下 OAR 掃 animations 目錄遇到任何非 ASCII（中文／俄文）檔名就整個放棄快取，所有替換動畫失效，MCO 攻擊全 T 字；裝動畫 mod 前必須掃名稱並改成 ASCII（原 type: memory）

2026-09-06 晚上使用者徒手、斧頭攻擊都 T 字。我先誤判成 Stances 覆蓋層抄錯來源（那也是真錯，另修），修完仍 T 字。真因在 `SKSE/OpenAnimationReplacer.log`：`Error while caching directories: recursive_directory_iterator ... Invalid name` 指向 `_CustomConditions/160000010-----落英双剑`，接著 `Actors\Character` 解析 1ms、0 套替換。那一天 mcoi 線裝進 9 個 mod 共 89 個非 ASCII 名稱（74 目錄＋15 檔案）；昨天以前 mods/ 裡零個。

**Why:** Proton／Wine 的 ANSI codepage 轉不了 CJK，OAR 用窄字串組路徑，FindFirstFile 回 ERROR_INVALID_NAME，而 OAR 的快取是一個 try/catch 包整段——一個例外就全滅。第一人稱（`_1stPerson`）沒中是因為那條路徑沒有非 ASCII 名字。

**How to apply:** 任何動畫類 mod（DAR／OAR／MCO 招式）安裝前跑 `find mods -path '*/animations/*' | LC_ALL=C grep -P '[^\x00-\x7F]'`，有就改名（OAR 子目錄名不影響功能，config.json 才算；DAR 非數字名本來就 inert）；對照表在 `agentctl/handoffs/home-2026-09-06/mcofix/data/cjk-rename-map.csv`。攻擊 T 字先看 OAR log 的 caching 錯誤與 `Actors\Character` 解析時間，再猜招式。相關：[[oar-copy-folder-bypasses-gates]]、[[housecarl-merge-facegen-backslash-filename]]。

## oar-root-disabled-misses-subfolder-variants

> 2026-09-20 徒手衝刺「超人飛行」真凶：OAR 包根層 disabled:true 沒蓋到 male/ 子路徑變體；靜態盤點說 Omni 已停用是錯的，runtime 才抓到（原 type: project）

2026-09-20 cx-sprint 靜態盤點說 Omni-Man moveset（101-121382）sprint 檔 09-12 已 `disabled: true`、贏家是 Eryx；
實機 OAR log 推翻：真凶是 `001 Omni Base Attacks/male/mt_sprintforward.hkx`（priority 8867353），
根層 config 的 disabled 沒涵蓋 `male/`／`female/` 子路徑變體。另外 OAR config 的 `name` 欄不是目錄名，多個資料夾可同名 `Main`，歸因要引 log 原始路徑。
修法：獨立修正層 `Sprint-Unarmed-Vanilla-Dev-2026-09-20`（priority 2147483640，條件玩家＋雙手空）蓋回原版，不動原包。

**Why:** 靜態掃 OAR 條件容易漏子資料夾；使用者的體感抱怨從頭到尾是對的。
**How to apply:** 動畫歸因一律以 OAR runtime log 的 replacement 路徑為準，靜態結論只當候選；停用某 moveset 的一類動作要遞迴掃所有子資料夾。相關：[[oar-copy-folder-bypasses-gates]]、[[oar-non-ascii-animation-dir-kills-cache]]
