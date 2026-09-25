# 成本判定、實機驗收與待處理事項

← [mco-to-bfco-conversion](../mco-to-bfco-conversion.md)

## 5. 成本判定：對現役 stack 值不值得做

### 5.1 成本結構

| 項 | 成本 |
|---|---|
| 工具取得 | 一次性（mod 119926，離線工具，不進 MO2） |
| Linux 執行 | Proton／wine 跑 `.exe`，或跑作者 `.py`，或自刻 rename（§2.2）。**低** |
| 每套 moveset 的機械成本 | **一次批次改檔名**，分鐘級 |
| Pandora 重跑 | **純 moveset 不需要**；只有換框架／升 BFCO 到 3.100.7 才要 |
| OAR config 改寫 | 通常 0 |
| **實機驗收** | **這才是真成本**：每套要驗連段是否接得上、攻速手感、NPC 行為、hitbox（Precision 已在役） |
| 授權判斷 | **本輪三筆已查完**（§4.1）；新增候選才要再看一次 mod 頁 Permissions（需瀏覽器，歸調度者） |

### 5.2 判定

**值得做。** 先分 NPC／玩家兩條路（§4.2），再在每條路裡分 A／B 類：

| | **NPC 路** | **玩家路** |
|---|---|---|
| 主要手段 | 直接裝 [141893](https://www.nexusmods.com/skyrimspecialedition/mods/141893)，FOMOD 選 BFCO framework | 逐套自轉（§2.2） |
| 轉換成本 | **零**（現成品） | 每套分鐘級 |
| 授權 | ✅ 原作者明示授權 | ✅ 私人可、❌ 不得再發布（§4.1） |
| 額外前置 | SCAR + SCAR AE Support + OCF（**使用者 2026-08-27 已放行**） | 無 |
| 真成本 | 實機驗收 + 一批 NPC 行為要看 | 實機驗收（§5.4） |

每條路裡再分：

- **A 類——已有現成 BFCO 版／雙框架版**：直接取，**零轉換成本**，應優先。
  例：mod 135503（BDO Guardian Awakening）、mod 123708（DD2 Fighter）、mod 184100（DA Staff）。
- **B 類——只有 MCO 版、要自己轉**：機械成本低，但**驗收成本與 A 類相同**。
  只有在「那套動畫不可替代」時才值得。例：mod 80085（DD Daggers）。

**仍然不值得做的**：為了單一展示片新增框架依賴。使用者雖已放行 SCAR／OCF，
但那是**為了 141893 這個整包**放行的；不要把它當成「以後任何 mod 要什麼前置都可以加」。

### 5.3 `animation-combat.md` 逐筆影響

> **只讀引用。`modpack-design/` 的寫入權在 `opus-content` 手上。** 下表是本線給出的技術依據與建議，不是判定。

逐筆對照候選的現行結論、技術依據與建議。

已抽到 [costs-and-validation-candidate-impacts.json](costs-and-validation-candidate-impacts.json)（14 列）。

行：原文件行號。

候選：候選項目。

現行結論：原表記載的現行結論。

本線技術依據：本線提出的技術證據。

建議：本線建議。

統計：14 筆記錄，5 欄。

**小計**：`NO-GO-MCO-ONLY` 四筆（`:56` 的 BDO Guardian／DD Fighter／DA Staff／DD Daggers）中**三筆的事實前提不成立**、
第四筆降為 DEFER；`:80` 的**技術與授權前提都已被推翻**；`:84` 的 MCO 件前提不成立
→ **重新開放 5 筆、降 DEFER 1 筆**；`:57`、`:83` **確定關閉**（理由與本結論無關，不必再掛在 MCO 上）。
**每一筆重新開放的都必須分「NPC 路（141893 現成）」與「玩家路（自轉）」兩條寫**，理由見 §4.2。

### 5.4 實機驗收清單（交給調度者排遊戲鎖，逐條打勾）

> 本線**不取鎖、不啟動遊戲**。以下是可逐條打勾的驗收項；每一項都寫成「看什麼、算過還是算不過」。
> 前置：先確認 `selected_profile=modpack-main`，走 Steam → MO2 shim 啟動。

**V-A 玩家路（裝一套自轉的 moveset 後）**

| # | 驗什麼 | 算過的條件 |
|---|---|---|
| A1 | 普攻連段 | 連按輕擊能連出 2 段以上，且動畫不回到 vanilla 揮砍 |
| A2 | 重擊連段 | 重擊後能接輕擊（`MCO_nextattack` 被 BFCO 吃到的證據） |
| A3 | 衝刺攻擊接續 | 衝刺攻擊播完能接普攻（社群有回報這條會斷） |
| A4 | recovery 脫離 | 攻擊後搖按移動鍵能提前脫離（`MCO_Recovery` → `BFCO_DIY_recovery`） |
| A5 | 攻速手感 | 節奏沒有明顯過快／過慢；若異常，記下 BFCO FOMOD 的 `WeapSpeedStyle` 目前選項 |
| A6 | perk 攻速生效 | 裝備／perk 的攻速修飾**看得出差異**（BFCO 走 vanilla 攻速的賣點） |
| A7 | Precision hitbox | 揮空不掉血、揮中會掉血，無穿模判定 |
| A8 | 位移同步 | 沒有滑步／砍空氣（AMR `animmotion` 有生效） |

**V-B NPC 路（裝 141893 + SCAR + OCF 後）**

| # | 驗什麼 | 算過的條件 |
|---|---|---|
| B1 | NPC 出招 | 對應種族／派系的 NPC 用到新招式，不是 vanilla 揮砍 |
| B2 | NPC 連段 | NPC 打得出 2 段以上連段 |
| B3 | 玩家不受影響 | **玩家自己的招式沒有變**（141893 是 NPC 分發，§4.2） |
| B4 | `SCAR_*Dummy.hkx` | 裝了 SCAR 之後，NPC 的 ready idle 沒有異常姿勢（B5 那條未知項的實測） |
| B5 | 連段不無限 | 沒有被 NPC 連到死（否則要加 SCAR NPC Combo Limitation Patch 162497） |

**V-C 回歸（不論走哪條路都要）**

| # | 驗什麼 | 算過的條件 |
|---|---|---|
| C1 | TK Dodge | 閃避仍可用，且攻擊↔閃避能互相派生 |
| C2 | TDM | 方向移動與方向重擊沒有互卡 |
| C3 | 存檔／讀檔 | 收刀存檔、讀回無 CTD、無卡姿勢 |

> ⚠️ **不要在同一次驗收裡動 Pandora／BFCO 版本／MO2 設定**（使用者 2026-08-27 裁示：Pandora 晚上再說）。
> A1–A8 只需要放進一套 moveset 檔案，不需要重跑 behavior 生成。

---

## 6. 待驗證／需使用者決定

### 已結案（2026-08-27）

| 項 | 結果 |
|---|---|
| ~~授權查證~~ | ✅ **已完成**，見 §4.1 與 [`agentctl/logs/nexus-permissions-mco-movesets-2026-08-27.md`](../../../../../agentctl/logs/nexus-permissions-mco-movesets-2026-08-27.md)。結論：私人轉換可，再發布不可；`Conversion permission` 那條**不適用**本案 |
| ~~要不要引入 SCAR／OCF~~ | ✅ **使用者已放行**（SCAR 72014、SCAR AE Support 77285、OCF 81469） |
| ~~141893 授權是否屬實~~ | ✅ **屬實**，但它是 **NPC 分發不是玩家 moveset**（§4.2） |

### 仍待處理

<!-- wf-nav -->
1. **實機驗收（需遊戲鎖，由調度者排程與取鎖，本線不碰）**：清單見 §5.4，共 16 條可逐條打勾。
2. **Pandora／BFCO 版本：目前凍結。** 使用者 2026-08-27 裁示「晚上再說」，現在不得動
   Pandora／BFCO 版本／MO2。升級題本身仍在：BFCO 3.100.5 → 3.100.7 起
   `Running Nemesis & Pandora is now required`，升級後要重跑並重新版本化 output。
3. `mco_powerattackloop/outro` → `BFCO_PowerAttackLoop/Outro` 這組 handle **不在 BFCO 頁的動畫表上**
   （頁上寫的是 `BFCO_PowerAttack_Charge1~3.hkx` 的 DIY Charge 機制）。converter changelog 說 BFCO ≥ 3.3 支援，
   兩邊對不太上，**需要實檔或實機確認**。
4. `SCAR_*Dummy.hkx` 在**無 SCAR** 環境下的行為仍未知（推測會留下錯誤 ready idle）。
   若 NPC 路照計畫裝 SCAR，這條就不會遇到；只有走「不裝 SCAR 卻用 (SCAR) moveset」才需要驗（§5.4 B4）。
5. DA Staff 的轉換層 mod 184100 另列 `For Honor Power Attack` 前置，
   而 BFCO MCM 內建重擊熱鍵——**這條前置是否真的必要，需實機確認**。
6. §2.2 的 Linux rename `sed` 骨架**未實跑**；建議走官方工具，自刻只當離線備案。

