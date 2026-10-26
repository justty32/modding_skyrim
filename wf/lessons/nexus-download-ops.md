# Nexus 下載自動化

[lessons 索引](README.md)

CDP 驅動的 Nexus Mods 下載自動化踩過的坑：瀏覽器 profile 複本的紅線、頁面判定、下載完成判準、並行控制。

## nexus-download-manager-only-and-dom-byte-verify-gotchas

> cdp-download 自動化累積坑：manager-only 頁面沒有手動下載鈕；多 MAIN 檔會誤點隱藏 modal；expected_bytes=null 被當 0 誤判超時；>500MB 多一層 Standard/Resumable 對話框；file_id 會被 Nexus 從 URL 拿掉

2026-08-27～08-30 下載線累積的同組坑：
- manager-only mod 頁面可能根本沒有 Manual download 鈕，重試無意義，先用 houseCARL 查該 mod 是否關閉 direct download。但 manager-only 旗標本身不是「下載必失敗」的判別因子——標此旗標的檔多數照樣下載成功（2026-09-05、09-11 實證，`agentctl/handoffs/done/2026-09/home-2026-09-11/kurone/REPORT.md:57-59`）；規劃批次時不要因它排除候選，照常排進既有 CDP／Manual 流程實測。
- 多 MAIN 檔時第二層點擊可能誤點隱藏 modal 抓錯檔，要用 API 回傳 bytes 核對下載結果。
- `expected_bytes=null` 會被 `Number(null)=0` 誤判超時，完成判準用「大小穩定一段時間＋無 `.crdownload`」。
- >500MB 多跳一層 Standard/Resumable 選框要選 Standard。
- 點 FILES 後 URL 的 `file_id` 會被拿掉，fallback 要改選可見 DOM 列，落地檔名用瀏覽器 `suggestedFilename` 不要硬比對 expected_filename。

**Why:** Nexus 頁面在新舊 DOM、多檔案、大檔案、關閉直接下載四種情境行為都不同，單一判準會在某情境靜默失敗或抓錯檔。

**How to apply:** 新下載線先讀 `agentctl/handoffs/done/2026-08-27/cx-dl2/tools/KNOWN-ISSUES.md`；完成判準用「大小穩定＋無 .crdownload」；下載後用 `nexus_identify`（MD5）核實身分；遇 manager-only 先查再排程、不要盲目重試。

## nexus-concurrent-downloads-must-serialize

> 多條線同時呼叫 nexus_get.sh 下載會互搶同一個 Chrome profile 複本，全部 timeout

2026-10-08：兩條線平行呼叫 `nexus_get.sh --batch` 同時失敗在「timeout waiting for download start」，原因是共用同一份 Chrome profile 複本互相干擾。

**Why:** `nexus_get.sh` 走單一 Chrome profile 複本（見 [[agent-driven-nexus-download]]），本質是獨佔資源，平行呼叫等同兩個 agent 搶同一個瀏覽器視窗。

**How to apply:** 派多條線同時做 Nexus 下載任務時，交接書要明文規定序列化（一次一個 session 用 `nexus_get.sh`），不要假設批次下載可以平行跑。

## nexus-fileid-and-uploader-graphql-pinning

> 批次下載釘版本用 GraphQL modFiles 查 file_id，盤點作者全集用 uploaderId filter——都別靠檔名或關鍵字猜

2026-09-11 實證：下載新版或多版本 mod 時，先用 `housecarl_nexus_graphql` 的 modFiles 查詢把目標版本的精確 file_id 釘死再餵下載器，0 抓錯版（`agentctl/handoffs/done/2026-09/home-2026-09-11/kurone/REPORT.md:40-41`）。盤點某作者全部作品時關鍵字搜尋會混進別人的漢化／衍生，改用 `housecarl_nexus_mod` 取 uploader.memberId 再用 GraphQL `mods(filter:{uploaderId,gameId})` 查才精準；盲區剩分身帳號、已下架、LE/AE 分開上架（同報告:63-66）。

**Why:** 檔名／版本字串／關鍵字都是人寫的表面層，file_id 與 uploaderId 才是 Nexus 的主鍵。

**How to apply:** 批次下載前一律先 modFiles 釘 file_id，下載器吃 file_id 不吃檔名；「某作者全部作品」類盤點一律走 uploaderId filter，不拿關鍵字結果當權威清單。

## agent-driven-nexus-download

> agent 自己從 Nexus 下載檔案的路徑：2026-08-27 起優先用 Claude in Chrome 擴充，退路才是 CDP + 暫存 profile 複本（原 type: memory）

**2026-09-30 使用者重點要求：不准讓他現有 Chrome 的任何帳號被登出（Google 與其他所有網站）。** 寧可下載失敗。規則寫在 `wf/workflows/nexus-intake/download-routes.md` 頂部：
- 複本用 `agentctl/tools/nexus_dl/make_profile_copy.sh`（來源唯讀快照、只留 nexusmods.com cookie、殘留自毀），不整份 cp Cookies（第二個 Chrome 共用 Google session cookie 可能觸發盜用保護把本尊登出）。
- 收尾只殺 `--user-data-dir=/tmp/<複本>` 的 Chrome，禁 pkill／killall。
- 擴充路不點登出、不清 cookie、不關使用者分頁。

**兩條路**：
- **優先：Claude in Chrome 擴充**（2026-08-27 起；`list_connected_browsers` 看得到本機 Browser）——直接驅動使用者現有的 Chrome，不必開 profile 複本也不必開 CDP port。可重跑序列在 repo 的 `agentctl/logs/nexus-download-via-chrome-extension-2026-08-27.md`。用擴充時不必取桌面鎖，因為沒有搶螢幕。
- **退路（擴充沒連線時）：Chrome DevTools Protocol（`--remote-debugging-port`）＋ 使用者 profile 的暫存複本**（2026-08-22 實測），用程式驅動頁面點 `Manual download` → `Slow download`，完全不需要鍵鼠注入。

**為什麼不是鍵鼠注入**：這台是 Wayland + KDE，`ydotool` 有裝但 `ydotoold` 起不來（`/dev/uinput` 是 `root:root 660`，要 sudo）。只要有 XWayland 視窗持有焦點，`xdotool` 的鍵盤與滑鼠都可用（2026-08-27，詳見 repo 的 `agentctl/docs/resource-locks.md`），但下載仍走瀏覽器驅動，因為那更穩、可驗證。

**profile 要用複本，但只複製必要的**：直接用使用者的 profile 會搶到既有 Chrome 實例（新 flag 被忽略），或關掉使用者的視窗。複本只需要登入 cookie ＋ `Preferences` ＋ `Local State`（約 6.7 MB），登入狀態帶得過去、不撞 Cloudflare（2026-08-30）。**不要整棵複製**——整棵約 5.9 GB，`/tmp` 是 tmpfs（記憶體），等於白燒 RAM。

**複本執行期會膨脹**：headless CDP 的 Chrome 會在背景下載 on-device ML 模型（OptGuideOnDeviceModel 等 optimization guide 元件），在 `/tmp` tmpfs 膨脹到約 4～4.6 GB 並吃頻寬（2026-09-03、10-23）。建複本在真實磁碟，或啟動時加旗標停用 optimization-guide/screen_ai/WasmTtsEngine（啟動參數見 `agentctl/handoffs/home-2026-09-03/dl/`）；過程定期巡 tmpfs 用量，複本 >500 MB 就是有東西在自下載。CDP 下載沒有速率上限，Steam 同時在下載時別抓 >500 MB 大檔。

**light-DOM fallback 別靠 URL 參數認 row**：點 FILES 分頁後 Nexus 會把 URL 裡的 `file_id` 拿掉，但那一列在 DOM 裡仍正確——要以 DOM 選 row。工具現行行為是 fail-closed（寧可抓不到也不抓錯），**改工具時不要把這個性質弄丟**。細節在 repo 的 `agentctl/handoffs/done/2026-08-27/cx-dl2/tools/KNOWN-ISSUES.md`。

**manager download 是壞的**：`nxm://` handler 送得到 MO2、`nxmhandler.exe` 回 status 0，但下載清單不會出現項目。詳見 `~/notes/projects/modding/skyrim/logs/ai-overhaul-1.9.5-nxm-download-attempt-2026-08-21.md`。官方 manual download 是被允許的，別再繞 handler。

**交接書一定要寫死的紅線**：不准輸入任何憑證、不准解 CAPTCHA、不准接受新條款、不准點 endorse/track/vote、不准 sudo 或改 group/udev。碰到就發 `NEEDS-USER` 停下來。

**免費驗證**：Nexus 檔案列上的 VirusTotal 連結帶著該檔 hash，可以直接跟下載檔的 SHA-256 比對，等於一次來源驗證。

**頁面操作的坑**（2026-10-23）：
- Nexus「Manual/Slow download」按鈕有時渲染在 shadow DOM 裡，CDP 腳本要同時查 `document` 與 `shadowRoot`、只點可見元素。
- 頁面 load timeout／沒觸發 download start 多半是暫態網路問題，先直接重試不必假設檔案本身有問題。
- houseCARL 標 manager only 的 Nexus 檔案，agent 用既有慢速下載流程（Xvfb Chrome＋profile 複本）仍可能成功，不要就此放棄。
- `cdp-download.mjs` 對 >500 MB 檔的逐檔 timeout 要按 bytes 分級（>500MB 給 900 秒、>1GB 給 2400 秒），固定 420 秒會把大檔判失敗（`agentctl/handoffs/done/2026-09/home-2026-09-03/dl/REPORT.md:62`）。

**非 Nexus 來源**：Nexus 頁面版本明顯落後於社群已知相容版（如 AE 支援）時，優先查該 mod 的 GitHub repo 是否有更新 release——housecarl 與既有 CDP 工具只為 Nexus 設計，做不到 GitHub release 下載。GitHub release 直連下載（如 xEdit 官方 release 的 BSArch.exe）用 `curl`/`wget` 即可，不撞 Cloudflare、不需要開瀏覽器、不需要取 `desktop.lock`——判斷要不要取桌面鎖先看來源是不是 Nexus（`agentctl/handoffs/done/2026-08-31/fixdis-2026-08-31/CX-FD1.md:53-57`）。

螢幕是獨佔資源，動之前取 [[aetheria-agent-coexistence]] 提到的遊戲鎖當 screen mutex 並註明用途。
相關：[[driving-other-cli-agents]]、[[trust-gpt-sol-more]]

source: agentctl/handoffs/done/2026-09/home-2026-09-01/hfix-2026-09-01/REPORT.md；agentctl/handoffs/done/2026-09/home-2026-09-02/lrdl/REPORT.md:65；agentctl/handoffs/done/2026-09/home-2026-09-02/mco/REPORT.md:34
