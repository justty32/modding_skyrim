# 鎖、螢幕與開遊戲（3/3）

[lessons 索引](README.md)｜同主題：[locks-screen-and-game](locks-screen-and-game.md)、[locks-screen-and-game-2](locks-screen-and-game-2.md)

## agent-driven-nexus-download

> agent 自己從 Nexus 下載檔案的路徑：2026-08-27 起優先用 Claude in Chrome 擴充，退路才是 CDP + 暫存 profile 複本（原 type: memory）

2026-08-22 實測成功：codex 線可以自己完成 Nexus 手動下載，路徑是
**Chrome DevTools Protocol（`--remote-debugging-port`）＋ 使用者 profile 的暫存複本**，
用程式驅動頁面點 `Manual download` → `Slow download`，完全不需要鍵鼠注入。

**2026-08-27 起多一條更短的路**：使用者裝了 Claude in Chrome 擴充（`list_connected_browsers`
看得到本機 Browser），可以直接驅動他現有的 Chrome，不必開 profile 複本也不必開 CDP port。
CDP + profile 複本降為退路（擴充沒連線時用）。**2026-08-27 已用擴充實測成功**
（mod 26440 CHS 主檔，Manual → Slow download 一次過），證據與可重跑序列在
repo 的 `agentctl/logs/nexus-download-via-chrome-extension-2026-08-27.md`。
用擴充時不必取桌面鎖，因為沒有搶螢幕。

**為什麼不是鍵鼠注入**：這台是 Wayland + KDE，`ydotool` 有裝但 `ydotoold` 起不來
（`/dev/uinput` 是 `root:root 660`，要 sudo）。注意 `xdotool` 的限制**沒有**當初以為的那麼死——
2026-08-27 重測：只要有 XWayland 視窗持有焦點，`xdotool` 的鍵盤與**滑鼠**都可用，
詳見 repo 的 `agentctl/docs/resource-locks.md`。但下載仍走瀏覽器驅動，因為那更穩、可驗證。

**profile 要用複本，但只複製三樣**：直接用使用者的 profile 會搶到既有 Chrome 實例（新 flag 被忽略），
或關掉使用者的視窗。複製一份出來既能沿用 Nexus 登入 session，又不干擾使用者。
**2026-08-30 `cx-dl11` 實測：只需要登入 cookie ＋ `Preferences` ＋ `Local State`，複本 6.7 MB 就夠**，
登入狀態帶得過去、不撞 Cloudflare。`cx-dl7`（2026-08-29）整棵複製吃了 **5.9 GB**——
`/tmp` 是 tmpfs（記憶體），那等於白燒 6 GB RAM。**不要整棵複製。**

**light-DOM fallback 別靠 URL 參數認 row**：點 FILES 分頁後 Nexus 會把 URL 裡的 `file_id` 拿掉，
但那一列在 DOM 裡仍正確——要以 DOM 選 row。工具現行行為是 fail-closed（寧可抓不到也不抓錯），
**改工具時不要把這個性質弄丟**。細節在 repo 的
`agentctl/handoffs/done/2026-08-27/cx-dl2/tools/KNOWN-ISSUES.md`。

**manager download 是壞的**：`nxm://` handler 送得到 MO2、`nxmhandler.exe` 回 status 0，
但下載清單不會出現項目。詳見
`~/notes/projects/modding/skyrim/logs/ai-overhaul-1.9.5-nxm-download-attempt-2026-08-21.md`。
官方 manual download 是被允許的，別再繞 handler。

**交接書一定要寫死的紅線**：不准輸入任何憑證、不准解 CAPTCHA、不准接受新條款、
不准點 endorse/track/vote、不准 sudo 或改 group/udev。碰到就發 `NEEDS-USER` 停下來。

**免費驗證**：Nexus 檔案列上的 VirusTotal 連結帶著該檔 hash，可以直接跟下載檔的
SHA-256 比對，等於一次來源驗證。

螢幕是獨佔資源，動之前取 [[aetheria-agent-coexistence]] 提到的遊戲鎖當 screen mutex 並註明用途。
相關：[[driving-other-cli-agents]]、[[trust-gpt-sol-more]]

**2026-09-03 補**：headless CDP 的 Chrome 會自己在背景下載約 4 GB 的 on-device ML 模型（optimization guide），塞爆 /tmp tmpfs 並吃 25 Mbps 頻寬；dl 隊已加啟動旗標擋掉（見 `agentctl/handoffs/home-2026-09-03/dl/` 的 Chrome 啟動參數）。profile 複本放 /tmp 要盯大小，>500 MB 就是有東西在自下載。另：CDP 下載沒有速率上限，Steam 同時在下載時別抓 >500 MB 大檔。
