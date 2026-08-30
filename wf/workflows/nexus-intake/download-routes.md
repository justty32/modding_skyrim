# 兩條實測可用的下載路徑

[nexus-intake 主線](README.md)｜[3. 下載](README.md#3-下載) 的路徑對照。

兩條實測可用的路，都是點 `Manual download → Slow download`（左邊那顆，不碰 Premium），檔案落到 `~/Downloads/`：

| 誰 | 機制 | 要點 |
|---|---|---|
| 調度者（Claude）親跑 | **Claude in Chrome 擴充**，用使用者已登入的瀏覽器 | 最乾淨：不開 profile 複本、不取桌面鎖。直達 URL `/mods/<id>?tab=files&file_id=<fileId>&nmm=0` 直接落在 Slow download 頁。`browser_batch` 內的 `left_click` 不會觸發下載，要獨立呼叫。實錄見 [`agentctl/logs/nexus-download-via-chrome-extension-2026-08-27.md`](../../../agentctl/logs/nexus-download-via-chrome-extension-2026-08-27.md) |
| codex 線 | **headful Chrome ＋ 使用者 Chrome profile 的暫存複本 ＋ CDP（`--remote-debugging-port`）** | 驅動器已有：[`agentctl/handoffs/done/2026-08-27/cx-dl2/tools/cdp-download.mjs`](../../../agentctl/handoffs/done/2026-08-27/cx-dl2/tools/cdp-download.mjs)。profile 複本 4.5 GB，**放 `/tmp/<線名>-trash/`，不放 `$HOME`、不進 repo**，抓完自清 |

- **headless 會撞 Cloudflare**，headful 才過。
- 不需要 `ydotool`／`/dev/uinput`——CDP 直接驅動頁面，**不要為此去要 sudo**。
- 用**獨立暫存 profile 複本**，不要動使用者既有的瀏覽器視窗。
- **慢是正常的**（有等待計時器），等就好，不要為了加速找別的路徑。
- houseCARL 回的 `note: the author disabled direct download — manager (nxm) download only` **不能當閘門**，
  頁面上 `Manual download` 常常照樣可用；同頁多檔靠 `file_id` 認，不靠 mod id。
