# nexus-intake — 從 Nexus 取得 mod 到可用

從「想要某個 mod」到「它躺在庫裡、裝好、而且確定生效」的完整流水線。

```text
Done when: <檔案入庫且 hash 已驗、DB 已 rescan、若安裝則 audit 通過>
```

六個階段，**每一段都有一個會靜默失敗的地方**，寫在各段的「坑」。

```text
查證 → 版本閘門 → 下載 → 入庫 → 安裝 → 稽核
```

## 1. 查證

**一律走 houseCARL MCP，不要開瀏覽器。**

- `housecarl_nexus_search`：用名字找 mod
- `housecarl_nexus_mod`：抓 mod 頁（requirements、建議 INI、真實最新版、完整說明），吃 id 或 URL

**坑**：Nexus 頁面上的「最新版」與 files 分頁的實際檔案常常不同步。以 API 回的
`files` 欄位為準，不要讀頁面敘述。

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

機制：**headful Chrome ＋ 使用者 Chrome profile 的暫存複本 ＋ CDP
（`--remote-debugging-port`）**，用程式驅動頁面點
`Files 分頁 → 目標列 → Manual download → Slow download`，檔案落到 `~/Downloads/`。

- **headless 會撞 Cloudflare**，headful 才過。
- 不需要 `ydotool`／`/dev/uinput`——CDP 直接驅動頁面，**不要為此去要 sudo**。
- 用**獨立暫存 profile 複本**，不要動使用者既有的瀏覽器視窗；抓完清掉複本。
- **慢是正常的**（有等待計時器），等就好，不要為了加速找別的路徑。

**免費的來源驗證**：Nexus 檔案列上的 VirusTotal 連結**帶著該檔的 hash**。
下載後跟本地 SHA-256 比對，比不上就標記為未驗證，**不要當成功**。

**檔名要跟目標表完全一致**；不一致就停下回報，不要自己改名假裝對上。

### 硬性紅線（碰到就停，發 `NEEDS-USER`）

不輸入任何帳號憑證／密碼／2FA；不解 CAPTCHA 或任何 bot 偵測；不註冊、不買 Premium、
不接受新條款；不點 endorse／track／vote／subscribe——**任何會改變使用者 Nexus 帳號狀態的事都不做**。
cookie 橫幅只選最保守的選項。不動 nxm handler 關聯或 Wine registry（manager download 是壞的，別再繞）。

> 一次誤報教訓：正常頁面的原始 HTML 內含**未顯示**的 Cloudflare 元件字樣。
> 紅線判斷只看**實際可見的驗證頁／驗證文字**，不要 grep HTML 就宣稱遇到 challenge。

## 4. 入庫

實體庫是 `~/skyrim_mods/`（**刻意留在 repo 外**），新下載平放進 `hdd/`。
四件事缺一不可，細節見 [`mod-library/README.md`](../../../mod-library/README.md#入庫流程2026-08-23-建立)：

1. **逐檔開壓縮檔看內容**判斷是不是 Skyrim mod——不能只看檔名。行為檔／BodySlide／
   SkyProc patcher 沒有頂層 `.esp`／`meshes/`，只掃副檔名會誤判成非 Skyrim。
2. 對既有庫去重：檔名 → 大小 → 大小相同者算 SHA-256 確認。
3. **對來源自己去重**——瀏覽器重複下載會留 `X.7z` 與 `X (1).7z`，兩個都不在庫裡，
   只比對「來源↔庫」會**兩個都收進去**。這條踩過。
4. `python3 mod-library/db/scan_mod_library.py scan` 再 `stats`，看
   `L1 exact duplicates` 是否只剩已知的既有組。

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
python3 mod-library/l10n/tools/audit_layer_priority.py
```

**逐檔案路徑判勝出者，不靠名字猜本體。** 名字比對會判錯——VIGILANT 的中文層在
`VIGILANT SE` 之上（正確）但在 `VIGILANT Missing Lines Voice` 之下，只有前者決定勝負；
一版名稱比對報出 20 個失效層，其中 16 個是配錯。

裝了覆蓋層還要驗**內容真的有中文**，見 [localization](../localization/README.md)。

## 何時不用

- 只是查某個 mod 是什麼、要不要裝 → 走 [investigation](../investigation/README.md)，別下載。
- 選型與整包規劃 → `modpack-design/`。
- 使用者自己下載好丟在 `~/Downloads` → 從第 4 階段接手即可。
