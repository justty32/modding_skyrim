# 兩條實測可用的下載路徑

[nexus-intake 主線](README.md)｜[3. 下載](README.md#3-下載) 的路徑對照。

> ## ⚠️ 最高優先：不准讓使用者現有 Chrome 的任何帳號被登出（2026-09-30 使用者要求）
>
> 包括 Google 以及其他所有網站的登入。這條優先於下載成功與否——**寧可下載失敗，不可讓使用者被登出**。
>
> **CDP 路（profile 複本）**
> - 複本**一律**用 [`agentctl/tools/nexus_dl/make_profile_copy.sh`](../../../agentctl/tools/nexus_dl/make_profile_copy.sh) 建立：
>   來源只讀（sqlite 唯讀快照），複本裡**只留 `nexusmods.com` 的 cookie**，其他網域全刪，殘留就自毀。
>   **禁止手動 `cp` 整份 `Cookies`**：Google 等帳號的 session cookie 被第二個 Chrome 同時使用，
>   可能觸發該網站的 session 盜用保護，把使用者**原本的**登入作廢。
> - `--user-data-dir` 只能指向 `/tmp/` 下的複本，**絕不指向 `~/.config/google-chrome`**；
>   複本**絕不寫回**真 profile。
> - 收尾只殺**自己開的** Chrome：用 `ps -eo pid,comm,args` 比對 `--user-data-dir=/tmp/<複本>`，
>   **禁止 `pkill chrome`／`pkill -f chrome`／`killall`**——殺掉使用者的 Chrome 會丟掉只存在記憶體的 session cookie（＝登出）。
> - 在複本裡也不點 Log out、不開帳號設定頁。
>
> **Chrome 擴充路（直接驅動使用者本人的瀏覽器）**
> - 這條路操作的就是真帳號，所以：不點任何 Log out／Sign out／切換帳號；不開 `chrome://settings` 清除資料、
>   不清 cookie／site data、不用無痕視窗重登；不關使用者自己開的分頁或視窗，只關自己開的分頁。
> - 不跑任何 `Network.clearBrowserCookies`、`Storage.clearDataForOrigin` 之類的清除指令。
>
> **碰到 Nexus 要求重新登入**：發 `NEEDS-USER` 停手，請使用者自己登入。不要自己輸入帳密，也不要去動其他網站的登入。

兩條實測可用的路，都是點 `Manual download → Slow download`（左邊那顆，不碰 Premium）；擴充路落到 `~/Downloads/`，CDP 路落到 `nexus_get.sh` 的 `--out`（預設 `~/skyrim_mods/_dl-<日期>/`）：

| 誰 | 機制 | 要點 |
|---|---|---|
| 調度者（Claude）親跑 | **Claude in Chrome 擴充**，用使用者已登入的瀏覽器 | 最乾淨：不開 profile 複本、不取桌面鎖。直達 URL `/mods/<id>?tab=files&file_id=<fileId>&nmm=0` 直接落在 Slow download 頁。`browser_batch` 內的 `left_click` 不會觸發下載，要獨立呼叫。實錄見 [`agentctl/logs/nexus-download-via-chrome-extension-2026-08-27.md`](../../../agentctl/logs/nexus-download-via-chrome-extension-2026-08-27.md) |
| codex／Claude 子代理線 | **headful Chrome（藏在私有 Xvfb）＋ profile 暫存複本 ＋ CDP** | **一條命令：[`agentctl/tools/nexus_dl/nexus_get.sh`](../../../agentctl/tools/nexus_dl/nexus_get.sh)**，見下節。不要再從舊 handoff 抄 `cdp-download.mjs` |

### CDP 路：`nexus_get.sh`（2026-10-03 kitD 收編）

```sh
agentctl/tools/nexus_dl/nexus_get.sh <modid> --file <fileId> [--out DIR] [--expect-sha256 HEX]
agentctl/tools/nexus_dl/nexus_get.sh --batch list.txt      # 一行一個 modid#fileId，共用一個複本
agentctl/tools/nexus_dl/nexus_get.sh <modid> --file <fileId> --dry-run   # 只查清單不開 Chrome
```

它一次做完：keyless GraphQL 查檔案與公布大小 → `make_profile_copy.sh` 建 `/tmp/nexus-get-*` 複本 →
Xvfb 裡的 headful Chrome 開 CDP → 下載 → 比公布大小、算 sha256 → 只殺自己那棵行程樹、刪複本 →
stdout 每檔一行 JSON。預設 `--mode xvfb` 不出可見視窗、不取 `desktop.lock`（`--mode visible` 才取，收尾自動放）。

**exit `3`＝`NEEDS-USER`**（Nexus 要登入／驗證／新條款）：停手，請使用者在他自己的 Chrome 登入 Nexus 後重跑。
多檔頁 `--main`／`--latest` 會拒絕並列出 fileId，一律用 `--file`。驅動器與已知缺口見
[`agentctl/tools/nexus_dl/`](../../../agentctl/tools/nexus_dl/)。

### 通用注意

- **真 headless 會撞 Cloudflare**，headful 才過（所以預設是 Xvfb 裡的 headful）。
- 不需要 `ydotool`／`/dev/uinput`——CDP 直接驅動頁面，**不要為此去要 sudo**。
- 用**獨立暫存 profile 複本**，不要動使用者既有的瀏覽器視窗；收尾只殺自己開的 Chrome（見上方帳號保護）。
- **慢是正常的**（有等待計時器），等就好，不要為了加速找別的路徑。
- houseCARL 回的 `note: the author disabled direct download — manager (nxm) download only` **不能當閘門**，
  頁面上 `Manual download` 常常照樣可用；同頁多檔靠 `file_id` 認，不靠 mod id。
