# Phase 4 — 人工關卡

> 屬於 [AI 全自動 mod QA 迴圈](README.md)。

## 四、分階段任務（續）


### Phase 4 — 人工關卡

| # | 任務 | 驗證 |
|---|---|---|
| 4.1 | **⏸ 延後（D6）** 視覺驗證連拍與 before/after 對照。使用者在場時直接叫他看即可 | 使用者收到成組可比對的圖 |
| 4.2 | **簡化（D6）** `handoff_user` step 保留,但**拿掉「AI 導航到指定頁面」那半**——只要停住並通知使用者,使用者自己操作。不依賴 1.6 | 走通一次通知→使用者回覆→AI 收尾 |

#### 1.3 實測結果（2026-08-02）

執行機制：`IFormFactory` 造 `RE::Script` → `SetCommand` → `CompileAndRun(target)`，走 `GameThread::Run`（timeout 10s）。`ref` 參數是 console 的「selected reference」，給 `player.additem` 這類點號指令用的。

| 測試 | 結果 |
|---|---|
| `load <baseline stem>`（主選單） | ✅ 載入成功，6 秒後 `/state` 從空 cell 變 `WhiterunExterior15` @ (14732, -14913, -4784) |
| `coc WhiterunBanneredMare` | ✅ `/state` 變 `WhiterunBanneredMare` (0x1601E) @ (2.9, -399.9, 70.2) |
| `player.getav health` | ✅ 輸出 `GetActorValue: Health >> 100.00` |
| `getgs fMoveCharWalkBase` | ✅ 輸出 `GameSetting fMoveCharWalkBase >> 100.00` |
| 亂指令 | ✅ 輸出 `Script command "thisisnotacommand" not found.` |
| 壞 ref `0xDEADBEEF` | ✅ 400 + `no reference with form id 0xDEADBEEF` |
| 空 body | ✅ 400 + `missing "cmd"` |

**輸出擷取只有部分達成，而且踩了兩個坑（都記在子專案 README 的 Pitfall 段）**：

1. **`ConsoleLog::VPrint` 的 5-byte detour 會讓遊戲開場即 crash**（access violation，跳進不可讀位址）。這個 load order 裡 `MoreInformativeConsole.dll` 與 `ConsoleUtilSSE.dll` 都在 console 輸出路徑上，兩個 plugin patch 同一段序言，後者蓋掉前者，前者保存的「原始位元組」就變成別人 `jmp` 的一半。**通則：在真實的百來個 mod load order 裡，對熱門引擎函式做序言 detour 本來就不安全。**
2. 改讀 `ConsoleLog::lastMessage`（純結構成員存取，零衝突風險）後，發現 **before/after 比對會抓到別人插隊寫的行**——`load` 與 `coc` 明明不印東西，卻分別回了 `GetInFaction >> 0.00`、`IsShieldOut >> 0.00`。某個 mod 顯然在高頻透過 ConsoleUtil 查詢。0.2.2 改成**先印哨兵 `__agentbridge_N__` 再比對**：沒人印東西時哨兵還在，就正確回空。

**殘留限制（0.3.0 實測後定案，設計上接受，不再投入）**：
- **只拿得到最後一行**。`sqs`、`help` 這類多行輸出會被截成末行。
- **哨兵只對「執行很快的指令」有效**。實測：`player.additem`、`player.setav` 回正確的空 `output`；但 `load`、`coc` 仍分別漏出 `GetInFaction >> 0.00`、`GetNumericPackageData >> 360.00`。規律是**指令的同步執行span 越長，別的 mod 越有機會插隊寫 `lastMessage`**，而 span 長度由指令本身決定，縮不了。
- **因此 runner 的 `assert_state` 一律對 `/state` 斷言，不要對 console 輸出斷言。** console 輸出只當診斷資訊，不當事實來源。`output_captured: true` 不代表那行是這條指令印的。

#### 1.2 實測結果（2026-08-02，AgentBridge 0.3.0）

**欄位以 QA 可斷言的機器事實為準**。Mantella／MinAI 的取向是把數值轉成人看得懂的描述（MinAI 的 21 級時間描述、~60+ 地點關鍵字），適合 LLM 對話，不適合 QA 斷言。

**兩層設計**（`GET /state[?include=nearby,inventory,quests][&radius=][&limit=]`）：

- **永遠回傳**：`player`（name/level/position/angle_z/cell/worldspace/interior/health-magicka-stamina 的 current+max/carry_weight/in_combat-sneaking-weapon_drawn-dead/左右手裝備）、`game`（遊戲時間、`menus_open`、`dialogue` 的 topic/quest/speaker）。
- **選配**：`nearby_actors`（走引擎自己的 `ProcessLists::highActorHandles`，比走遍 cell 的 placed ref 便宜得多，依距離排序）、`inventory`、`quests`（active + `currentStage`）。

分層的理由：只想確認「cell 有沒有變」的 QA step，不該付整包背包和全 quest 掃描的代價。每個集合都有 `limit`（預設 32），免得一個壞請求讓主執行緒去組 900 筆陣列。

實測（白漫勇者之家內）：`nearby_actors` 依距離抓到 Jon Battle-Born(136)/Mikael(170)/Uthgerd(366)/Hulda(541)/Saadia(615)；`inventory` 抓到金幣與 `worn:true` 的礦工衣；`quests` 抓到 Live Another Life stage 200。狀態變更確實反映：`player.additem f 500` → 金幣 113→613；`player.setav health 250` → current 與 max 都變 250。

**兩個要知道的行為，不是 bug**：
- `equipped.right` / `left` 只涵蓋**雙手**（武器/法術）。盔甲不在手部 slot，空手時是 `null`——身上穿的要看 `inventory` 的 `worn: true`。
- 主選單狀態下 `/state` 可能回 **503**（task queue 沒排空）。0.1.0 時期在主選單拿得到 dummy player，但那是遊戲已完全靜止時；剛啟動還在初始化就會逾時。runner 要把「主選單 /state 逾時」當正常，靠 `/ping` 判斷進程活著。
