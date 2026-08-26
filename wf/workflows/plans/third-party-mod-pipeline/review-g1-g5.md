# 重審補漏 G1–G5

> 屬於 [第三方 mod 取得–安裝–驗證流水線](README.md)。

## 七、重審補漏（2026-08-04，動工前對抗式複查）

以 houseCARL 實查 + 讀 `mo2ctl.py` 原始碼複查本計畫，找到 11 項缺漏。**G1–G4 是會讓流水線出錯而非只是不完整的等級**，優先補。

### G1 — `archives.txt` 沒人管（P1 必補）

profile 裡除了三個 txt 還有 **`archives.txt`（BSA 啟用清單）**，`mo2ctl.py` 對它**完全沒有處理**（grep `archives` 只命中一句註解，`.bsa` 只出現在 `looks_like_mod_root()` 的副檔名檢查裡）。

後果：第三方 mod 帶 `.bsa` 而該 BSA 的 basename 不匹配任何啟用 plugin 時，**BSA 靜默不載入** → 資產全缺（紫貼圖／隱形／進場 CTD），而 `plugins.txt` 看起來一切正常。修法是 houseCARL 的 `housecarl_create_plugin`（其 doc 明文就是為「需要 basename 解析得到的 placeholder plugin」設計），或補 `archives.txt` 條目。

### G2 — `mo2ctl install` 落在最高優先權（P1 必補）

`mo2ctl.py:454-455` 把新 mod 插在 `modlist.txt` 第 1 行，程式碼註解自己寫著 `line 1 is top priority`。對 ModForge 的 no-op plugin 無差別；對第三方**貼圖／模型／腳本** mod，這代表**新裝的未驗證 mod 自動贏過全部 109 個既有 mod 的檔案衝突，且靜默無提示**。

P1 必須加明確的優先權落點參數，預設不再是 top。這與 D2 的「插入式排序」是同一件事的檔案層對應——D2 只講了 plugin 順序，漏掉 mod 檔案優先權，那是兩套獨立的排序。

> **2026-08-23 後續：已實作，但預設換了一種踩法。** `mo2ctl` 現在有 `--priority`
> （`bottom`／`top`／`before:<mod>`／`after:<mod>`），預設 `bottom`，G2 要求的「不再靜默贏過既有 mod」
> 已達成。**但對覆蓋層而言 `bottom` 是完全相反的錯**——翻譯層的存在意義就是要贏過本體，
> 裝在下面等於整層失效，而且**沒有任何錯誤徵兆**：檔案在磁碟上、mod 也啟用著，英文原版照樣贏。
>
> 實際踩到四個層（11 個檔）：Timing is Everything、The Choice is Yours、At Your Own Pace、SkyParkour。
> 另有一個是把 `after:<本體>` 誤解成「疊在上面」——`after` = 檔案裡排在後面 = **更低**優先權。
>
> 所以裝覆蓋層一律要明確傳 `--priority "before:<本體 mod 名>"`，並用
> `mod-library/l10n/tools/` 的層優先權稽核
> 逐檔案路徑驗證勝出者。這條與 G7 的 SKSE 副本檢查是同一類問題：**檔案層的勝負無聲無息，
> 必須主動稽核，不能靠沒報錯就當作對的。**

### G3 — 資產層完全沒檢查（D6 補強）

D6 的靜態關卡只查 record／script／dialogue。但實務上第三方 mod 失效最大宗是**資產層**：缺貼圖→紫、缺模型→隱形或 CTD。現成但未使用的工具：

- `housecarl_asset_status` — 走 MO2 VFS 解析指定 Data 相對路徑：誰提供、loose 還是 BSA、有無多方爭用、是否根本不存在。正是「為什麼我的 override 沒生效」「這貼圖從哪來」的答案。
- `housecarl_bsa_list` — 列 BSA 內容（需 BSArch 路徑，xEdit 附帶）。
- `housecarl_nif_inspect` — 模型層檢查。

### G4 — contested DLL 要做 before/after diff（D6 補強）

實查現況：**5 個 version-LOCKED SKSE DLL 全鎖 1.6.1170**（`PapyrusUtil` / `JContainers64` / `skee64` / `Fuz Ro D'oh` / `SSEFpsStabilizer`），且**已存在 2 個爭用**（`BehaviorDataInjector.dll`、`BFCO.dll`）。

第三方 mod **極常自帶** PapyrusUtil／JContainers 的副本。若它在 VFS 贏了（而 G2 的 top-priority 預設會讓它贏），這 109 個 mod 會一起壞，而症狀是散彈式的腳本失效，極難反推。所以 `housecarl_skse_inventory` 的 contested 清單必須**安裝前後各跑一次做 diff**，不是只看一次。

### G5 — 沒有 crash 三角測量步驟（D6 補強）

**`CrashLogger` v1.22.0 已裝已啟用**（`modlist.txt:84`）。P0.2b 已把 `crash_logs` 指到正確位置——注意它是把 `crash-<時間>.log` **平放在 `SKSE/` 資料夾**，沒有 Windows 慣例的 `Crash Logs` 子目錄。

#### 2026-08-04 實查 20 份既有 log 的結論（triage step 要照這些前提設計）

**1. Proton 下約 40% 的 log 沒有 call stack。** 20 份裡 8 份**完全沒有 `CALL STACK` 段落**（例：`crash-2026-07-05-19-07-04.log`，44 秒 uptime、有完整例外分析與 relevant objects，但到 `SYSTEM SPECS` 就結束）。堆疊回溯要靠 `RtlVirtualUnwind`／`StackWalk64`，Wine 的實作不完整。**所以「crash log 會指名肇事者」只有約六成成立**，triage step 不能把它當保證，拿不到堆疊時要能明說「這次無法歸因」而不是沉默。

**2. 一秒內的第二份 log 是 crash handler 自己崩掉的產物，不是第二次崩潰。** `18:44:30`+`18:44:31`、`18:48:48`+`18:48:49` 兩組相隔一秒，後者都是 700–1,000 bytes 的殘缺檔。**triage 要按時間鄰近去重**，否則會把一次事故數成兩次。

**3. `PROCESS MEMORY: Private: 117440444.07 MB`（117 TB）在每份 log 裡都出現**，是 Wine 回報的垃圾值。別去追。

**4. 這個 load order 沒有慣性肇事的第三方 plugin。** 堆疊頂端幾乎全是 `SkyrimSE.exe`（引擎）與 `d3d11.dll` / `VCRUNTIME140.dll`。`EngineFixes.dll` 出現在 3 份裡，但它本來就 hook 一大堆東西，出現不等於肇事。唯一一次第三方 plugin 出現在前三個 frame 的是 `MCM-Unlocked.dll`（1 份）。

**5. 重複出現的同一位址是最有價值的訊號。** 兩組成對：`SkyrimSE.exe+02C3957 lock inc [rax+0x170]`（6/13 兩次，26s 與 46s）與 `SkyrimSE.exe+0146110 mov rax, [rcx+0xC8]`（6/13 兩次，4 分與 24 分）。同址重現代表是可重製的問題，值得單獨追；散落的單次崩潰不值得。

**6. 唯一被證實的 plugin 衝突就是 agent-bridge 自己那次。** `crash-2026-08-02-08-41-23.log`：uptime **6,599ms**（agent-bridge README 記「~6.6s，Papyrus VM init」，分毫不差）、`Tried to execute memory at 0x000158B3D6AE`（不可讀）、`POSSIBLE RELEVANT OBJECTS` 滿是 `SkyrimScript::*` / `BSScript::Internal::VirtualMachine` / `VMInitThread`，call stack 是：

```
[0][P] 0x000158B3D6AE                            ← 跳進不可讀記憶體
[1][S] AgentBridge.dll+0054404
[2][S] ConsoleUtilSSE.dll+00B9F94  spdlog::logger::sink_it_
```

**這份 log 給了 README 那條通則的直接證據**——README 是從症狀推論「兩個 plugin patch 同一段序言」，log 直接指出碰撞對象是 ConsoleUtilSSE 的 spdlog sink。該 detour 已依決策放棄，且 AgentBridge 已於 P0.5 移出正式 profile，此案已結。

**triage step 的設計結論**：讀 `crash_logs` → 按時間鄰近去重 → 有堆疊的取前三個有模組名的 frame 交叉比對本次新裝的 mod → 沒堆疊的只回報例外位址、指令、`POSSIBLE RELEVANT OBJECTS` 與 uptime，並明確標為「無法歸因」。uptime 本身就是強訊號：**6 秒內＝載入期（plugin 衝突）、數十秒＝進場、數分鐘以上＝遊玩中（內容或記憶體問題）**。
