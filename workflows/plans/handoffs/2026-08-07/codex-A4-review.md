# 交接書 — codex · A4 覆核：deepseek 漢化配對草稿的判準修正

**這是 A1 之後的任務，先把 A1 收完再看這份。**

deepseek 已完成 A4a，產出在（repo 外，唯讀取用）：
- `/home/lorkhan/skyrim_agent_out/deepseek/translation-pairs-draft.tsv`（280 筆）
- `/home/lorkhan/skyrim_agent_out/deepseek/translation-pairs-summary.md`
- `/home/lorkhan/skyrim_agent_out/deepseek/match_translations.py`（它的比對腳本，供你參考，**不是**要納入 tools/）

結果分布：high 231（82.5%）／low 38（13.6%）／none 11。

## Claude 已逐筆看過 38 筆低信心，結論：約一半是錯的，且錯得有規律

deepseek 有守規矩——該標 low 的都標了，所以沒有髒資料流進 Mongo。但它的比對演算法有六個系統性缺陷，**你要修的是判準，不是逐筆手改**。

### 缺陷 1（最嚴重）：token overlap 單獨不足以成立

同家族 mod 共用前綴時，token overlap 會把翻譯包配到**兄弟 mod**。確認錯誤的例子：

| 漢化包 | 被配到 | 為什麼錯 |
|---|---|---|
| `CC Hendraheim - Tweaks and Enhancements` | `CC Farming - Tweaks and Enhancements` (69029) | Hendraheim ≠ Farming |
| `CC Myrwatch - Tweaks and Enhancements` | `CC Farming - Tweaks and Enhancements` (69029) | Myrwatch ≠ Farming |
| `Cities of the North - Morthal` | `Cities of the North - Dawnstar` (28952) | Morthal ≠ Dawnstar |
| `Cities of the North - Winterhold` | `Cities of the North - Dawnstar` (28952) | Winterhold ≠ Dawnstar |
| `At Your Own Pace - Companions` | `At Your Own Pace - College Quest Expansion Patch` (52704) | Companions ≠ College |
| `At Your Own Pace - Misc` | 同上 | Misc ≠ College |
| `At Your Own Pace Winterhold College` | 同上 | 這筆**可能**對，但要另外確認是不是同一個 mod |
| `JK's Skyrim - Mirai Patch` | `CFTO - JK's Skyrim Patch` (8379) | Mirai patch ≠ CFTO patch |
| `CHS-FDE-Jenassa-Inigo Patch` | `FDE Jenassa Auri Patch` (120255) | Inigo ≠ Auri |

**修法**：共用前綴的家族，**差異 token 必須也對上**，否則一律降 `none`。token overlap 分數本身不得作為唯一依據。

### 缺陷 2：本體不在庫裡時，正確答案是 `none`，不是最像的那個

上表多數案例的真正原因是**本體根本沒下載到庫裡**。token overlap 演算法在結構上表達不出「找不到」——它一定會回傳某個最高分的。這是缺陷 1 的根因，修法同上：設一個絕對門檻，過不了就 `none`。

### 缺陷 3：`patch` / `addon` / `installer` / `hub` 這類限定詞出現在單邊時視為不同 mod

| 漢化包 | 被配到 | 判定 |
|---|---|---|
| `Honed Metal Community AE Patch` | `Honed Metal AE` (61015) | patch ≠ 本體 |
| `RDO Final` | `RDO - iAFT SE Patch Final` (1187) | 本體 ≠ iAFT patch |
| `Unslaad SE` | `Unslaad Voiced - English Addon SE` (11896) | 本體 ≠ voiced addon |
| `Missing Follower Dialogue Edit` | `Missing Follower Dialogue Fix` (56115) | Edit ≠ Fix，是兩個 mod |
| `Follower Dialogue Expansion - Lydia` | `Improved Follower Dialogue - Lydia` (38473) | Expansion ≠ Improved |

### 缺陷 4：配到另一個漢化包（明確 bug）

`Beyond Skyrim - Bruma SE (CHT)` → `Beyond Skyrim Bruma - CNS` (33079)。
**`CNS` 也是漢化標記**（Chinese Simplified），但那筆 mod 沒被排進「純翻譯包 stub」名單，所以變成合法候選。
修法：排除規則不能只看 `archive_ids` 是否為空，還要看 mod 名稱本身是否帶翻譯標記。

### 缺陷 5：`MCM` 與 `CLEAN` 不是翻譯標記，不該被剝除

deepseek 掃出的 38 種標記裡混進了這兩個。`MCM` 是 mod 功能、`CLEAN` 是清理過的 plugin 變體，剝掉會讓不同變體被誤併。其餘 36 種是對的，**那份標記清單本身很有價值，收進計畫文件**。

### 缺陷 6：plugin_basename 前綴撞名要求「全中」而非「部分中」

`EldenRim1.0.62(Chinese Translation)` → `Elden Perk - beta0.0.991` (65625)。
命中的 plugin 是 `EldenPerkTree` / `EldenSkyrim` / … ——同作者的 plugin 都以 `Elden` 開頭，而且 note 自己寫了 `plugins not found: ['SCSI-RimImpactOfMob']`。
修法：plugin 比對要求**翻譯包內的 plugin 全部都在該本體 mod 內**，有一個找不到就降信心或 `none`。

## 判定為正確的低信心筆（可直接升 high）

`AI Overhaul`→21654、`Aniya`→63208、`Frozen in Time`→39732、`Black Cat-Serana Dialogue Add-On`→32161、`Morgaine-Fully Voiced Standalone Follower`→41027、`Nether's Follower Framework`(兩筆)→55653、`Secunda`→93739、`Song of the Green`(三筆)→11278、`Trade and Barter`→23081、`The Shire`→18903、`Immersive World Encounters. FINAL SE`→18330、`ETaC - Immersive Orc Strongholds SE`→legacy:etac…、`SDA Patch Chinese SE`→70782、`Thieves Guild For Good Guys - Hotfix3.9`→10745、`Path of Sorcery - Magic Perk Overhaul`→6660、`VIGILANT commentary patch - CHS`→101207

`Lightened Skyrim` 有兩個 exact name match（`111475`、`50755`）——**這筆你自己查 Nexus 決定**，你手上已經有 API 了。

## 你要做的

1. 把上面六條判準寫成 `~/notes/projects/modding/skyrim/tools/match_translations.py`（**這支才進 tools/，是正式版**），不要直接沿用 deepseek 那份草稿腳本
2. 重跑，產出修正後的配對
3. **正式寫回 Mongo 的 `translates_mod_id`**——只寫 high 信心的；low 與 none 留 `null`，並把清單留在 `docs/translation-matrix.md` 供人工續處理
4. 寫入前照慣例先 pymongo dump
5. commit 進 `~/notes`

**注意**：`translates_mod_id` 指向的是**本體**的 mod id，不是漢化包自己的 id。deepseek 發現庫裡有 **255 個純漢化包 stub**（`mods` 裡 `archive_ids` 為空的條目），因為漢化包在 Nexus 上有自己的 mod id、aggregate 時被當成獨立 mod 建了條目。這個資料模型陷阱要記進 `docs/mongodb-schema.md`。

做完印一行 `A4-REVIEW DONE`。
