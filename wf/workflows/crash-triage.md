# crash-triage — 遊戲崩潰／凍結的歸因流程

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

從「遊戲崩了／卡死了」到「定罪＋處置」的固定流程；單點教訓在 [lessons/crash-dll-and-scripts](../lessons/crash-dll-and-scripts.md)、[lessons/crash-data-and-assets](../lessons/crash-data-and-assets.md)。

**何時用**：實機 CTD、啟動即崩、整個遊戲凍結、同址重複崩潰。
**何時不用**：非崩潰的行為異常（交易金幣、攻速、對話）→ [lessons/gameplay-bugs](../lessons/gameplay-bugs.md) 的歸因手法；裝 mod 前的相容評估 → profile-change／mod-install-audit。

## Done when

- 每次崩潰都有打包的 crash log＋`skse64.log` 存進線目錄（再崩先打包，不靠記憶）。
- REPORT 寫明：候選嫌疑清單、每個嫌疑的證據（frame／暫存器／來源行號）、定罪或排除的依據。
- 處置落地可觀察：停用層已寫進 modlist、或 fork 修復的 DLL＋pdb 已部署、或標 WAIT_USER 等實機驗收。

## 流程

### 現場處置與證據

1. **先分「凍結」還是「崩潰」**：畫面卡死但聲音持續＝KWin direct scanout 假當機，先 alt+tab 回來；聲音也停＋CPU 個位數全 futex＝真死鎖，關遊戲前用 CrashLogger 熱鍵留全執行緒堆疊再 kill（載入畫面 alt+tab 死鎖直接 kill，見 lessons/locks-screen-and-game 的 alt-tab 節）。
2. **打包證據**：crash log＋`skse64.log`＋當下 modlist/plugins 快照。同址（同 offset）多次崩潰與隨機位址是兩種案情；rcx 等暫存器每次相同＝資料層條件 bug 的強訊號。
### 讀 log 與歸因

3. **讀 crash log 的可信度分級**：P（probable）frame 先信、S（stack scan）frame 存疑；RIP=0 時改讀 `[RSP+偏移]` 校正真實返回位址；暫存器值要對照該指令實際讀寫的對象做排除法。callstack 點名的 SKSE DLL 先查——但 trampoline hook 在 callstack 隱形，「沒點名」不等於無辜。
4. **按層歸因**：
   - DLL 層：有原始碼就直接讀 GitHub 定罪（grep `LookupForm` 類 null-check 漏洞）；沒 PDB 用 offsets CSV 鏈式對照。定罪後 fork＋repo 自帶 CI 編譯，pdb 跟 dll 一起換（lessons/crash-dll-and-scripts 的 upstream-fork 節）。
   - 資料層：同址＋暫存器恆定→反查 keyword／perk／record 條件（doomperk 型）；載入期 NIF 崩看 crash log 的 `inputFilePath`。
   - 素材層：LE 碰撞 NIF、STAT OBND 全 0、facegen 缺件各有既有 lessons 節。
### 剝層與收線

5. **嫌疑疊加時的剝層**：不逐批二分；一次只停用最可疑一件，同症狀家族（同作者／同機制系列）窮舉掃描後整組處理（lessons/crash-dll-and-scripts 的 sequential-minimal-disable 節）。單變量 A/B 用 profile clone＋副本 mod 停目標檔，不動正式環境。
6. **收線**：真因寫進對應 lessons 檔一節（或增補既有節）；「測不出來」標 BLOCKED 保持現狀，不當成「測出來是壞的」去回滾；格擋、戰鬥類觸發只能使用者實機驗收 → WAIT_USER。

## 交接

- 定罪要停用／改 profile → profile-change；要改 DLL 原始碼 → feature-dev；需要實機煙霧 → runtime-qa。跨 session 的 open 記 agentctl/SESSION-LOG。
