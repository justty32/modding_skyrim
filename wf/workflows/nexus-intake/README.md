# nexus-intake — 從 Nexus 取得 mod 到可用

從「想要某個 mod」到「它躺在庫裡、裝好、而且確定生效」的完整流水線。

```text
Done when: <檔案入庫且 hash 已驗、DB 已 rescan、若安裝則 audit 通過>
```

六個階段，**每一段都有一個會靜默失敗的地方**，寫在各段的「坑」。

```text
查證 → 版本閘門 → 下載 → 入庫 → 安裝 → 稽核
```

## 先認形態

**很少只抓一個檔。** 三種形態的共通流程是上面六段，但要抓什麼、怎麼分批不同：

| 形態 | 是什麼 | 額外規則 |
|---|---|---|
| **A 單件** | 一個獨立 mod | 就是下面六段 |
| **B 衛星件** | 某個已裝 mod 的擴充／patch／漢化 | 見 [satellites.md](satellites.md) |
| **C 系列／生態** | 一整套互相咬合的 mod（動作、perk、任務框架…） | 見 [series.md](series.md) |

**判斷形態的方式是查 requirements，不是看名字。** 一個看起來像單件的 mod，
requirements 可能拉出一整條生態；用 `housecarl_nexus_mod` 查，不要讀頁面敘述就當事實。

### 派下載線前：範圍樣板與雙 gate

「相關的」在依賴圖上可能被遞移展開；派線前要把排除條件與兩種停止閘門寫死。以下區塊可直接抄進交接書，
把 `X` 與兩個上限換成該線的實際值：

```text
範圍排除：
- 僅僅支援 X 不算——檔名或說明必須明確服務 X，才算 X 的東西。
- 反向 requirement 只展開一跳；被展開者自己的 requirement 不再展開。
- 同一頁多版本只取 latest；變體超過 2 個要先發 BLOCKED 問，不要自己全收。

雙 gate：
- 容量 gate：預估下載總量達 <容量上限>，立即停止並發 BLOCKED 詢問。
- 件數 gate：預估下載件數達 <件數上限>，立即停止並發 BLOCKED 詢問。
- 任一 gate 觸發就停下來問；另一項沒有超標也不得繼續。
```

派線端為什麼必須用排除法界定範圍，見 [agent-dispatch 的第六條防錯規則](../agent-dispatch/README.md#六條最容易錯的)。

## 1. 查證

**一律走 houseCARL MCP（無金鑰即可查 Nexus），不要開瀏覽器。**

- `housecarl_nexus_search`：用名字找 mod
- `housecarl_nexus_mod`：抓 mod 頁（requirements、建議 INI、真實最新版、完整說明），吃 id 或 URL；
  `files=true` 給完整逐檔清單（**fileId／版本／bytes 只能從這裡抄**，不能從頁面抄）
- `housecarl_nexus_check_updates`：批次以 `id#fileid` 查已裝檔是否過時

**誰能查**：houseCARL MCP 只掛在 Claude 這邊；**codex 線既沒有 houseCARL、也拿不到瀏覽器、純 HTTP
打 Nexus 回 403**（2026-08-26 實測，見 [`agentctl/docs/dispatch-windows.md`](../../../agentctl/docs/dispatch-windows.md)
「Nexus 查證：派線做不到」）。所以 Nexus 查證由調度者親做，把 id／fileId／版本／bytes 寫死進交接書再派線。

**已決定要裝的項目不必重查**：[`modpack-design/content-plan/install-plan-2026-08-27.md`](../../../modpack-design/content-plan/install/install-plan-2026-08-27.md)
每列已寫死 id／fileId／版本／bytes 與「為什麼是這個 fileId 而不是 MAIN」；中文層看
[`zh-layer-coverage-master-2026-08-28.md`](../../../modpack-design/content-plan/zh-layer/zh-layer-coverage-master-2026-08-28.md)。

**坑**：Nexus 頁面上的「最新版」與 files 分頁的實際檔案常常不同步。以 API 回的
`files` 欄位為準，不要讀頁面敘述。

### 手上已經有檔案、但不知道是什麼

從檔案內容反查，不要從檔名猜：單檔用 `housecarl_nexus_identify`（吃 MD5，無金鑰），
回 mod（id／名稱／作者／status）與 file_details（上游檔名／版本／分類），
**是比檔名可信得多的來源**。整庫批次跑用
`mod-library/db/` 的 **legacy MD5 回溯解析器**（見該目錄的 [`README.md`](../../../mod-library/db/README.md)）。

**坑**：`Light and Shade SE-77993-2-2-....7z` 的檔名寫著 77993，md5 指向的卻是
**82876**（簡中翻譯頁）。任何「用 regex 從檔名撈 id」的做法都要當成猜測看待。

查不到（404）只代表 Nexus 不認得這個 md5——對岸站台來的、或被解壓重打包過的都會 miss，
**不是檔案有問題**。實測 174 個舊命名檔只有 28 個 hit。

MD5 反查是唯讀，不改帳號狀態，不在下面的紅線內。

## 2. 版本閘門

翻譯層／patch 與本體**必須精確同版**。判斷順序：

1. 查出本機已裝的**精確版本**——看 mod 資料夾的 meta 與實際檔案，**不要只信資料夾名稱**。
2. 看候選檔的 API `version` 欄位。
3. **做二進位拓撲比對。**

**坑（踩過兩次）**：**API 的 `version` 欄位只是必要不充分條件，檔名裡的版本字串更不算數。**
Ordinator 中文層 API 標 `9.31.0`，實際內容是 `9.30.1`。真正的閘門是拓撲比對——
record 數、record identity、header、GRUP、subrecord 結構要完全一致，
差異必須**全部**落在可本地化文字 payload，非文字差異為零。
（VIGILANT 1.8.1 的合格例：129,107 records 全等，7,250 個差異全在文字 payload。）

**沒有同版就明說「無同版可用」並停手**，不要退而求其次裝不同版的層。

## 3. 下載

**這個帳號非 Premium**，`download_link.json` 會回 403，所以只能走網頁的 slow download。
**同一時間只有一條線可以開瀏覽器**，由調度者指定；沒被指定的線需要下載就發 `NEEDS-USER`。

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

**免費的來源驗證**：Nexus 檔案列上的 VirusTotal 連結**帶著該檔的 hash**。
下載後跟本地 SHA-256 比對，比不上就標記為未驗證，**不要當成功**。

**檔名要跟目標表完全一致**；不一致就停下回報，不要自己改名假裝對上。

### 硬性紅線（碰到就停，發 `NEEDS-USER`）

不輸入任何帳號憑證／密碼／2FA；不解 CAPTCHA 或任何 bot 偵測；不註冊、不買 Premium、
不接受新條款；不點 endorse／track／vote／subscribe——**任何會改變使用者 Nexus 帳號狀態的事都不做**。
cookie 橫幅只選最保守的選項。不動 nxm handler 關聯或 Wine registry（manager download 是壞的，別再繞）。

> 一次誤報教訓：正常頁面的原始 HTML 內含**未顯示**的 Cloudflare 元件字樣。
> 紅線判斷只看**實際可見的驗證頁／驗證文字**，不要 grep HTML 就宣稱遇到 challenge。

## 衛星件：擴充／patch／漢化

形態 B。衛星件散在多個 Nexus 頁面、版本節奏各自獨立，patch 還要同時對上兩邊的版本；
排序上衛星件在本體之上、翻譯層在最上。整段規則見 [satellites.md](satellites.md)。

## 4. 入庫

實體庫是 `~/skyrim_mods/`（**刻意留在 repo 外**），新下載平放進 `hdd/`。
五件事缺一不可，細節見 [`mod-library/README.md`](../../../mod-library/README.md#入庫流程2026-08-23-建立)：

1. **逐檔開壓縮檔看內容**判斷是不是 Skyrim mod——不能只看檔名。行為檔／BodySlide／
   SkyProc patcher 沒有頂層 `.esp`／`meshes/`，只掃副檔名會誤判成非 Skyrim。
2. 對既有庫去重：檔名 → 大小 → 大小相同者算 SHA-256 確認。
3. **對來源自己去重**——瀏覽器重複下載會留 `X.7z` 與 `X (1).7z`，兩個都不在庫裡，
   只比對「來源↔庫」會**兩個都收進去**。這條踩過。
4. 跑 `mod-library/db/` 的**掃庫工具** `scan` 再 `stats`，看
   `L1 exact duplicates` 是否只剩已知的既有組。
5. 檔名沒有 Nexus id 的跑 **legacy MD5 回溯解析器**還原來源（見下）。

## 5. 安裝

走 `mo2ctl install`（在 [`projects/agent-bridge/client/`](../../../projects/agent-bridge/client/)）。

**`--priority` 預設是 `bottom`，這對未驗證的第三方 mod 是正確的**（別讓它默默贏走每個檔案衝突），
**但對覆蓋層恰恰相反**。翻譯層／patch 一律要明確傳：

```sh
mo2ctl install <archive> --name "<X> Traditional Chinese" --priority "before:<本體 mod 名>"
```

**坑**：`after:<本體>` 不是「疊在上面」——`modlist.txt` 頂端才是最高優先權，
`after` = 檔案裡排在後面 = **更低**優先權。四個層曾因此完全失效。

改 profile 一律走 `feat → release → main`，見 [`instance/profiles/README.md`](../../../instance/profiles/README.md)。

## 6. 稽核

```sh
# 層優先權稽核，命令見 mod-library/l10n/tools/README.md
```

**逐檔案路徑判勝出者，不靠名字猜本體。** 名字比對會判錯——VIGILANT 的中文層在
`VIGILANT SE` 之上（正確）但在 `VIGILANT Missing Lines Voice` 之下，只有前者決定勝負；
一版名稱比對報出 20 個失效層，其中 16 個是配錯。

裝了覆蓋層還要驗**內容真的有中文**，見 [localization](../localization/README.md)。

## 何時不用

- 只是查某個 mod 是什麼、要不要裝 → 走 [investigation](../investigation/README.md)，別下載。
- 選型與整包規劃 → `modpack-design/`。
- 使用者自己下載好丟在 `~/Downloads` → 從第 4 階段接手即可。
