# 動畫與 OAR

[lessons 索引](README.md)

## oar-copy-folder-bypasses-gates

> 把 OAR／DAR 資料夾的 hkx 抄進自己的覆蓋層時，原資料夾的閘門條件（HasKeyword／HasMagicEffect／PRESET 等）就沒了；判「目前贏家」只看 IsActorBase 會抄到 NPC 專用或特殊狀態的動畫，玩家直接 T 字（原 type: memory）

案例（2026-09-06）：為了保住「沒切姿態時的原本招式」，把算出的贏家資料夾抄成 `<武器>-neutral`（只留 IsEquippedType＋IsActorBase 玩家），而贏家計算只排除 NPC-only 的 IsActorBase，結果抄到古劍三隨從專用爪擊（HasKeyword Gujian3_Follower:AAF6）、召喚獸形態、EldenCounter 反擊瞬間（HasMagicEffect）等閘門動畫，玩家攻擊就 T 字。

**Why:** OAR 是在遊戲裡即時評估條件的，資料夾本身「優先度最高」不等於「玩家一般狀態會用到」。抄檔案不抄條件＝把所有閘門打開。動畫本身給別的骨架或狀態做的，套到玩家身上就是 T 字或鬼畜。

**How to apply:** 算「玩家一般狀態的贏家」時，凡有任何啟用中的 HasKeyword／IsWornHasKeyword／HasMagicEffect／HasPerk／IsInFaction／IsRace／PRESET／Random／CurrentTargetDistance／CompareValues／非武器類型的 IsEquippedHasKeyword／非玩家 IsActorBase（含 negated），一律不算候選。更好的做法是不要抄檔案，改用「條件鏡射」：覆蓋層 config 把來源的整組條件原樣帶上再加姿態條件。修好的工具在 `agentctl/handoffs/home-2026-09-06/mcofix/`。相關：[[rule-out-a-concept-scan-same-batch-siblings]]（同批要掃）、[[leads-must-not-end-turn-to-wait]]。

## oar-non-ascii-animation-dir-kills-cache

> Proton 下 OAR 掃 animations 目錄遇到任何非 ASCII（中文／俄文）檔名就整個放棄快取，所有替換動畫失效，MCO 攻擊全 T 字；裝動畫 mod 前必須掃名稱並改成 ASCII（原 type: memory）

症狀（2026-09-06）：攻擊全 T 字。證據在 `SKSE/OpenAnimationReplacer.log`：`Error while caching directories: recursive_directory_iterator ... Invalid name` 指向 `_CustomConditions/160000010-----落英双剑`，接著 `Actors\Character` 解析 1ms、0 套替換。

**Why:** Proton／Wine 的 ANSI codepage 轉不了 CJK，OAR 用窄字串組路徑，FindFirstFile 回 ERROR_INVALID_NAME，而 OAR 的快取是一個 try/catch 包整段——一個例外就全滅。第一人稱（`_1stPerson`）沒中是因為那條路徑沒有非 ASCII 名字。

**How to apply:** 任何動畫類 mod（DAR／OAR／MCO 招式）安裝前跑 `find mods -path '*/animations/*' | LC_ALL=C grep -P '[^\x00-\x7F]'`，有就改名（OAR 子目錄名不影響功能，config.json 才算；DAR 非數字名本來就 inert）；對照表在 `agentctl/handoffs/home-2026-09-06/mcofix/data/cjk-rename-map.csv`。攻擊 T 字先看 OAR log 的 caching 錯誤與 `Actors\Character` 解析時間，再猜招式。相關：[[oar-copy-folder-bypasses-gates]]、[[housecarl-merge-facegen-backslash-filename]]。

OAR/DAR 招式包若 `meshes/` 被多包一層外殼目錄，MO2 只認最外層，整包會像裝了一樣卻完全不生效；DAR 優先權資料夾還要求純數字命名，帶標籤字尾（如 `99993108---Player`）的目錄不會被引擎載入。裝完動畫包熱鍵無反應，先檢查這兩點（`agentctl/handoffs/done/2026-09/home-2026-09-06/mcoi/REPORT.md:67`）。

## oar-root-disabled-misses-subfolder-variants

> 2026-09-20 徒手衝刺「超人飛行」真凶：OAR 包根層 disabled:true 沒蓋到 male/ 子路徑變體；靜態盤點說 Omni 已停用是錯的，runtime 才抓到（原 type: project）

OAR 包根層 config 的 `disabled: true` 不涵蓋 `male/`／`female/` 子路徑變體：Omni-Man moveset（101-121382）根層已停用，實機 OAR log 的真凶仍是 `001 Omni Base Attacks/male/mt_sprintforward.hkx`（priority 8867353）（2026-09-20）。另外 OAR config 的 `name` 欄不是目錄名，多個資料夾可同名 `Main`，歸因要引 log 原始路徑。
修法：獨立修正層 `Sprint-Unarmed-Vanilla-Dev-2026-09-20`（priority 2147483640，條件玩家＋雙手空）蓋回原版，不動原包。

**Why:** 靜態掃 OAR 條件容易漏子資料夾；使用者的體感抱怨從頭到尾是對的。
**How to apply:** 動畫歸因一律以 OAR runtime log 的 replacement 路徑為準，靜態結論只當候選；停用某 moveset 的一類動作要遞迴掃所有子資料夾。相關：[[oar-copy-folder-bypasses-gates]]、[[oar-non-ascii-animation-dir-kills-cache]]

雙持握持異常的真因可能是另一包動畫裡「同名但骨骼改動範圍不同」的疊加 hkx（如某姿態包的同名檔覆寫全部 97 根骨頭含左手武器節點，原版同名檔只動一根）；OAR/DAR 條件邏輯檢查都正常卻外觀異常時，要往下比對實際生效 hkx 的骨骼動畫內容跟原版同名檔差異，尤其疊加層（`agentctl/handoffs/done/2026-10/home-2026-10-03/revgrip/REPORT-log.md`）。

禁用主控台指令時，可用 AnimationMotionRevolution.log 的微秒時間戳量「clip 標註時間／實測間隔」反推播放倍率，並找不受嫌疑影響的對照組（如 NPC）判斷是全域還是局部異常，不必靠下指令驗證（`agentctl/handoffs/done/2026-10/home-2026-10-07/meleeslow/REPORT-skse.md`）。


## oar-priority-and-disabled-mechanics

> OAR 贏家只看 config.json 的 priority 數字，不看 MO2 清單順序；user.json 停用某條動畫要路徑大小寫跟 VFS 完全一致才生效；批次裝完新包後舊的優先權空窗可能被蓋過，要重算。

priority 大者勝、同值不穩定（2026-09-01）；批次裝新招式包（2026-09-06 一次 141 套）不重算，既有疊招層會被新包優先權壓過；OAR 原始碼 `AddReplacementAnimation` 用大小寫敏感 `==` 比對路徑，user.json 寫小寫 `actors\character` 永遠對不到、停用形同虛設且不報錯（2026-10-03，`agentctl/handoffs/done/2026-10/home-2026-10-03/unarmedmove/REPORT.md`）。

**Why:** 三者同一根因：OAR 優先權／路徑比對獨立於 MO2 清單與直覺之外，「設了停用」不代表真停用。

**How to apply:** 疊招/per-NPC 層用 priority 數字設計；裝完動畫包後重跑優先權掃描；停用某條 replacement 要核對路徑大小寫＝VFS 實際路徑，用遊戲內 OAR 選單驗證真的生效。相關：[[oar-root-disabled-misses-subfolder-variants]]。

OAR 主選單報 invalid 條件，若 config.json 的 conditions 含 `MathStatement` 且 `requiredPlugin` 明確指名，是缺對應擴充插件（如 OpenAnimationReplacer-Math）造成，不是上游 mod 壞掉；裝對應插件即可解，不要碰原 config.json（`agentctl/handoffs/done/2026-08-31/oar-2026-08-31/REPORT.md:43-82`）。

從 MO2 內啟動 Pandora 時輸出走 USVFS 寫到虛擬層，讀不到上次真正落地的 `ActiveMods.json`，會誤開已停用的 mod；重跑 Pandora 前先確認 `mods/Pandora Output` 內有完整的前次輸出（不是空的或半殘），否則狀態判斷出錯（`agentctl/handoffs/done/2026-09/home-2026-09-02/mco2/REPORT.md:36`）。

自動挑選動畫來源資料夾的工具，排序鍵若用「檔案總數最多」會選到移動/待機組而非招式組；排序鍵要以目標類型檔案數為主，加「至少 N 個目標檔」門檻，判撞車要直接讀來源 mod 自己的條件檔，不要用模擬優先權近似（`agentctl/handoffs/done/2026-09/home-2026-09-12/stance/REPORT.md:206`）。

招式條件解析工具 movecond.py 曾把大寫 `0X...`（非標準小寫 `0x...`）誤判成恆假（2026-10-03 已修），只影響配置頁/總覽頁顯示文字，不影響 force_gates/oar_eval 實際判定；配置頁跟模擬結果對不上先疑 movecond 的大小寫解析（`agentctl/handoffs/done/2026-10/home-2026-10-03/eqover/REPORT.md`）。

Universal Behavior Runtime（A-Pose Fix + Auto Skeleton Patch）與 Pandora 的 XPMSSE patch 選項功能重複，兩者疊用時應關掉 Pandora 那個選項改用 UBR 版本；UBR 相容 FNIS/Nemesis/Pandora（`analysis/mod-survey/findings/frameworks-tools/universal-behavior-runtime.md:21`）。


## mco-bfco-conversion-pitfalls

> MCO↔BFCO 轉換三坑：DLL 的 PE 版本號會騙人（要看 MO2 metadata）；官方 converter 映射表有覆蓋不到的 handle，缺映射判 FAILED 不猜；部分作者已自帶雙格式檔，整包覆寫會砸掉作者特製版本。

BFCO.dll PE VERSIONINFO 寫死 0.1.0.0，實際套件 3.100.5；converter 1.2.2 不認得擴充 handle（如 14 個 `MCO_Dodge_*`）；同目錄已有雙格式且內容不同＝作者特製，要跳過（2026-08-30，`agentctl/handoffs/done/2026-08-30/mco-2026-08-30/REPORT.md`）。

**Why:** 版本號／映射表／作者客製，都是「訊息看似齊全，要另外查證」的轉換陷阱。

**How to apply:** 轉換前核對 MO2 metadata 版本，不信 DLL PE 版本；沒映射到的 handle 判 FAILED 保留證據；批次轉換前掃目標目錄是否已有雙格式，兩者都在就跳過標 SKIPPED；寫條件以實機拆開的 config 為準。

BFCO v3.100.3 自帶 21 個 OAR submod 全用 `IsEquippedType` 等裝備條件，攻擊狀態走 behavior 層；自帶 BDI 變數是 `BFCO_ComboLocked`/`LastAttack`/`NextNormal`/`NextPower`，不是 mod 頁示範的 `BFCO_iAttackVariants`（`analysis/mod-survey/action-system/findings/bfco.md:26`）。

Pandora Output／Attack MCO／1hm_behavior 三個行為檔裡，`MCO_AttackSpeed` 這個 SGVF 變數只有宣告沒綁 playbackSpeed（2026-09-02 從 BFCO 換 MCO 時留下的死路）；想靠改這個值調攻速前先用 packfile 掃描工具（如 clipbind.py）確認目前框架真的有綁這個變數（`agentctl/handoffs/done/2026-10/home-2026-10-07/meleeslow/REPORT-anim.md`）。


## precision-collision-needs-hitframe-fallback

> 只靠 Precision 碰撞事件（`Collision_Add`，無原版 `HitFrame`）的 MCO 招式，`bAttackCollisionsEnabled=0` 時攻擊零傷害；DLL 載入成功不等於功能啟用，要讀 ini 實際值。修法：builder 在碰撞窗插入原版 HitFrame（只補事件不改壓縮動作），離線用 bytes/事件/骨架 diff 驗收。

案例（2026-10-14）：MGRR 雙持招式只有 Collision_Add 事件；Precision.dll 正常載入但 ini 碰撞開關關了就不掉血。builder 只搬移 annotation array、重建 local fixups；同時揮擊只補一次（`agentctl/handoffs/done/2026-10/home-2026-10-14/dagger/REPORT.md`）。

**Why:** 「DLL 載入成功」與「該功能被 ini/MCM 開啟」是兩回事，招式作者常假設碰撞永遠開著。

**How to apply:** 「某招打不到人」先查三樣：`bAttackCollisionsEnabled` 實際值、clip 是否只有 `Collision_Add` 無 `HitFrame`、作者頁需求欄有沒有列 Precision（常漏列）。修就用 builder 補事件，驗收 bytes/事件/骨架 diff＋獨立覆蓋層；傷害仍要使用者實機確認。
