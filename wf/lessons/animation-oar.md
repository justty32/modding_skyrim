# 動畫與 OAR

[lessons 索引](README.md)｜[clip／replacement 取證與 handedness](animation-oar/README.md)

## oar-copy-folder-bypasses-gates

> 把 OAR／DAR 資料夾的 hkx 抄進覆蓋層會丟掉原資料夾的閘門條件；判「目前贏家」只看 IsActorBase 會抄到 NPC 專用或特殊狀態的動畫，玩家 T 字

2026-09-06：OAR 即時評估條件，「優先度最高」不等於「玩家一般狀態會用到」；抄檔不抄條件＝打開所有閘門，給別的骨架或狀態做的動畫套到玩家就 T 字或鬼畜。

**How to apply:** 算「玩家一般狀態的贏家」時，凡有任何啟用中的 HasKeyword／IsWornHasKeyword／HasMagicEffect／HasPerk／IsInFaction／IsRace／PRESET／Random／CurrentTargetDistance／CompareValues／非武器類型的 IsEquippedHasKeyword／非玩家 IsActorBase（含 negated），一律不算候選。更好的做法是不抄檔案，改用「條件鏡射」：覆蓋層 config 把來源整組條件原樣帶上再加姿態條件。工具在 `agentctl/handoffs/home-2026-09-06/mcofix/`。相關：[[rule-out-a-concept-scan-same-batch-siblings]]、[[leads-must-not-end-turn-to-wait]]。

## oar-non-ascii-animation-dir-kills-cache

> Proton 下 OAR 掃 animations 目錄遇到任何非 ASCII（中文／俄文）檔名就整個放棄快取，所有替換動畫失效，MCO 攻擊全 T 字；裝動畫 mod 前必須掃名稱並改成 ASCII

2026-09-06：Proton／Wine 的 ANSI codepage 轉不了 CJK，OAR 用窄字串組路徑得到 ERROR_INVALID_NAME，快取整段一個 try/catch，一個例外就全滅。證據在 `SKSE/OpenAnimationReplacer.log`：`Error while caching directories: recursive_directory_iterator ... Invalid name`，接著 `Actors\Character` 解析 1ms、0 套替換。

**How to apply:** 動畫類 mod（DAR／OAR／MCO 招式）安裝前跑 `find mods -path '*/animations/*' | LC_ALL=C grep -P '[^\x00-\x7F]'`，有就改名（OAR 子目錄名不影響功能，config.json 才算；DAR 非數字名本來就 inert）；對照表在 `agentctl/handoffs/home-2026-09-06/mcofix/data/cjk-rename-map.csv`。攻擊 T 字先看 OAR log 的 caching 錯誤與 `Actors\Character` 解析時間，再猜招式。相關：[[oar-copy-folder-bypasses-gates]]、[[housecarl-merge-facegen-backslash-filename]]。

裝完動畫包熱鍵無反應先查兩點：`meshes/` 外多包一層殼目錄（MO2 只認最外層，整包不生效）；DAR 優先權資料夾必須純數字，帶字尾（如 `99993108---Player`）不載入（`agentctl/handoffs/done/2026-09/home-2026-09-06/mcoi/REPORT.md:67`）。

## oar-priority-and-disabled-mechanics

<a id="oar-root-disabled-misses-subfolder-variants"></a>

> OAR 贏家只看 config.json 的 priority 數字，不看 MO2 清單順序；停用要路徑大小寫跟 VFS 完全一致、根層 disabled 不蓋子路徑變體；批次裝完新包要重算優先權。

- priority 大者勝、同值不穩定（2026-09-01）；批次裝新招式包後既有疊招層可能被新包壓過（2026-09-06）。疊招／per-NPC 層用 priority 數字設計，裝完動畫包重跑優先權掃描。
- OAR `AddReplacementAnimation` 用大小寫敏感 `==` 比路徑，user.json 寫小寫 `actors\character` 永遠對不到、停用形同虛設且不報錯（2026-10-03，`agentctl/handoffs/done/2026-10/home-2026-10-03/unarmedmove/REPORT.md`）。停用前核對路徑大小寫＝VFS 實際路徑，用遊戲內 OAR 選單驗。

包根層 config 的 `disabled: true` 不涵蓋 `male/`／`female/` 子路徑變體（2026-09-20 徒手衝刺「超人飛行」：Omni-Man moveset 根層已停用，log 真凶仍是 `001 Omni Base Attacks/male/mt_sprintforward.hkx`）。停用一類動作要遞迴掃所有子資料夾；修法用獨立高 priority 修正層蓋回原版（例 `Sprint-Unarmed-Vanilla-Dev-2026-09-20`，priority 2147483640，條件玩家＋雙手空），不動原包。config 的 `name` 欄不是目錄名（多個資料夾可同名 `Main`）；歸因以 OAR runtime log 的 replacement 原始路徑為準，靜態只當候選（[[static-winner-is-not-active-clip]]）。

OAR 主選單報 invalid 條件、conditions 含 `MathStatement` 且 `requiredPlugin` 指名時，是缺擴充插件（如 OpenAnimationReplacer-Math），裝插件即可，不碰原 config.json（`agentctl/handoffs/done/2026-08-31/oar-2026-08-31/REPORT.md:43-82`）。

從 MO2 內啟動 Pandora 時輸出走 USVFS，讀不到上次落地的 `ActiveMods.json`，會誤開已停用的 mod；重跑前先確認 `mods/Pandora Output` 有完整前次輸出（`agentctl/handoffs/done/2026-09/home-2026-09-02/mco2/REPORT.md:36`）。Universal Behavior Runtime（A-Pose Fix＋Auto Skeleton Patch）與 Pandora 的 XPMSSE patch 選項重複，疊用時關 Pandora 那個（`analysis/mod-survey/findings/frameworks-tools/universal-behavior-runtime.md:21`）。

自動挑動畫來源資料夾的工具，排序鍵不用「檔案總數最多」（會選到移動/待機組），改以目標類型檔數為主、設「至少 N 個目標檔」門檻；判撞車直接讀來源條件檔（`agentctl/handoffs/done/2026-09/home-2026-09-12/stance/REPORT.md:206`）。

## mco-bfco-conversion-pitfalls

> MCO↔BFCO 轉換三坑：DLL 的 PE 版本號會騙人；converter 映射表有缺的 handle，判 FAILED 不猜；作者自帶的雙格式檔不能整包覆寫。

2026-08-30（`agentctl/handoffs/done/2026-08-30/mco-2026-08-30/REPORT.md`）：BFCO.dll PE VERSIONINFO 寫死 0.1.0.0，版本以 MO2 metadata 為準；converter 1.2.2 不認擴充 handle（如 `MCO_Dodge_*`），沒映射到的判 FAILED 保留證據；同目錄已有雙格式且內容不同＝作者特製，跳過標 SKIPPED；寫條件以實機拆開的 config 為準。

BFCO v3.100.3 自帶 OAR submod 全用 `IsEquippedType` 等裝備條件，攻擊狀態走 behavior 層；BDI 變數是 `BFCO_ComboLocked`/`LastAttack`/`NextNormal`/`NextPower`，不是 mod 頁示範的 `BFCO_iAttackVariants`（`analysis/mod-survey/action-system/archive/bfco.md:28`）。

現役 Pandora Output／Attack MCO／1hm_behavior 裡 `MCO_AttackSpeed`（SGVF）只宣告沒綁 playbackSpeed；想改它調攻速前先用 packfile 掃描工具（如 clipbind.py）確認框架真的有綁（`agentctl/handoffs/done/2026-10/home-2026-10-07/meleeslow/REPORT-anim.md`）。

## precision-collision-needs-hitframe-fallback

> 只靠 Precision 碰撞事件（`Collision_Add`，無原版 `HitFrame`）的 MCO 招式，`bAttackCollisionsEnabled=0` 時零傷害；DLL 載入成功不等於功能啟用，修法是在碰撞窗補原版 HitFrame。

2026-10-14（`agentctl/handoffs/done/2026-10/home-2026-10-14/dagger/REPORT.md`）：「DLL 載入成功」與「該功能被 ini/MCM 開啟」是兩回事，招式作者常假設碰撞永遠開著。「某招打不到人」先查 `bAttackCollisionsEnabled` 實際值、clip 是否只有 `Collision_Add` 無 `HitFrame`、作者頁需求欄有沒有漏列 Precision。修法：builder 在碰撞窗插入原版 HitFrame（只補事件不改壓縮動作；只搬 annotation array、重建 local fixups，同時揮擊只補一次）；驗收 bytes/事件/骨架 diff＋獨立覆蓋層，傷害仍要使用者實機確認。
