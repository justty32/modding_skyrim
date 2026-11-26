# Nexus 下載自動化

[lessons 索引](README.md)

agent 從 Nexus 下載的坑：帳號保護、下載器已內建的修法、釘版本、並行控制。Nexus 查詢欄位的坑在 [housecarl-and-tools](housecarl-and-tools.md#housecarl-nexus-api-field-quirks)。

## agent-driven-nexus-download
<a id="nexus-download-manager-only-and-dom-byte-verify-gotchas"></a>

> agent 自己從 Nexus 下載：調度者親跑用 Claude in Chrome 擴充，線用 `agentctl/tools/nexus_dl/nexus_get.sh`（Xvfb 裡 headful Chrome＋profile 複本＋CDP）；做法與紅線以 `wf/workflows/nexus-intake/` 為準

**2026-09-30 使用者重點要求：不准讓他現有 Chrome 的任何帳號被登出（Google 與其他所有網站）。** 寧可下載失敗。

已整份收進現役文件，照那邊做：兩條路與帳號保護（複本只用 `agentctl/tools/nexus_dl/make_profile_copy.sh`、只留 nexusmods.com cookie、收尾只殺 `--user-data-dir=/tmp/<複本>` 的 Chrome、禁 pkill／killall、擴充路不點登出不清 cookie）、真 headless 撞 Cloudflare、不需要 ydotool／sudo、manager-only 不當閘門 → `wf/workflows/nexus-intake/download-routes.md`；紅線（不輸入憑證、不解 CAPTCHA、不接受新條款、不點 endorse/track/vote、不 sudo，碰到發 `NEEDS-USER`）、manager download（nxm）是壞的別再繞 handler、VirusTotal 連結的 hash 對 SHA-256 → `wf/workflows/nexus-intake/README.md`。

下載器已內建的修法（`agentctl/tools/nexus_dl/cdp-download.mjs` 檔頭、`agentctl/docs/KNOWN-ISSUES.md`）：以 DOM id 選 row、fail-closed（點 FILES 後 URL 的 `file_id` 會被拿掉）；只點可見控制項（多 MAIN 檔會誤點隱藏 modal）；light／shadow DOM 都查；>500MB 多一層 Standard/Resumable 選 Standard；`expected_bytes` null／0／近似值改用「大小穩定＋無 `.crdownload`」；落地檔名用 `suggestedFilename`；guest 頁（成人標記 mod 要登入才有 FILES 分頁）回 exit 3；大檔 timeout 按 bytes 分級；啟動旗標停用 optimization-guide 等元件自下載（`nexusget/common.py` 的 `CHROME_FLAGS`）。**改工具時不要把 fail-closed 性質弄丟**；不要從舊 handoff 抄 `cdp-download.mjs`。

文件沒寫的：
- 頁面 load timeout／沒觸發 download start 多半是暫態網路，先直接重試；標 manager only 的檔照常排進流程實測，多數照樣下載成功（`agentctl/handoffs/done/2026-09/home-2026-09-11/kurone/REPORT.md:57-59`）。
- exit 3 時看複本 cookie：只剩 `nexusmods_session_refresh`、沒有 `nexusmods_session`＝使用者登入已過期，agent 不碰帳號，記 WAIT_USER 請使用者在自己的 Chrome 開一次 Nexus（`agentctl/handoffs/home-2026-10-26/bodyswap2/REPORT.md` §2）。
- 自己另開 CDP Chrome（不走 `nexus_get.sh`）時，複本只帶登入 cookie＋`Preferences`＋`Local State`，不整棵複製（約 5.9 GB，`/tmp` 是 tmpfs）；照抄 `CHROME_FLAGS`，並巡 tmpfs 用量，複本 >500 MB 就是有東西在自下載（`agentctl/handoffs/home-2026-09-03/dl/`）。

CDP 下載沒有速率上限，Steam 同時在下載時別抓 >500 MB 大檔。要出可見視窗才取桌面鎖（`nexus_get.sh --mode visible` 自動取、收尾自動放）；擴充路與預設 Xvfb 不取。

**非 Nexus 來源**：Nexus 頁面版本明顯落後於社群已知相容版（如 AE 支援）時，優先查該 mod 的 GitHub repo 有沒有更新 release——houseCARL 與 CDP 工具只為 Nexus 設計。GitHub release 直連下載（如 xEdit 官方 release 的 BSArch.exe）用 `curl`/`wget` 即可，不撞 Cloudflare、不開瀏覽器、不取 `desktop.lock`（`agentctl/handoffs/done/2026-08-31/fixdis-2026-08-31/CX-FD1.md:53-57`）。

相關：[[driving-other-cli-agents]]、[[trust-gpt-sol-more]]

source: agentctl/handoffs/done/2026-08-27/cx-dl2/tools/KNOWN-ISSUES.md；agentctl/handoffs/done/2026-09/home-2026-09-03/dl/REPORT.md:62；agentctl/handoffs/done/2026-09/home-2026-09-01/hfix-2026-09-01/REPORT.md；agentctl/handoffs/done/2026-09/home-2026-09-02/lrdl/REPORT.md:65；agentctl/handoffs/done/2026-09/home-2026-09-02/mco/REPORT.md:34

## nexus-concurrent-downloads-must-serialize

> 多條線同時呼叫 nexus_get.sh 下載會互搶同一個 Chrome profile 複本，全部 timeout

2026-10-08：兩條線平行呼叫 `nexus_get.sh --batch`，同時失敗在「timeout waiting for download start」，原因判為共用同一份 Chrome profile 複本互相干擾；`nexus_get.sh` 本質是獨佔資源。

**How to apply:** 派多條線同時做 Nexus 下載任務時，交接書要明文規定序列化（一次一個 session 用 `nexus_get.sh`），不要假設批次下載可以平行跑。

## nexus-fileid-and-uploader-graphql-pinning

> 批次下載釘版本用 GraphQL modFiles 查 file_id，盤點作者全集用 uploaderId filter——都別靠檔名或關鍵字猜

檔名／版本字串／關鍵字都是人寫的表面層，file_id 與 uploaderId 才是 Nexus 的主鍵。2026-09-11 實證：先用 `housecarl_nexus_graphql` 的 modFiles 把目標版本的 file_id 釘死再餵下載器，0 抓錯版（`agentctl/handoffs/done/2026-09/home-2026-09-11/kurone/REPORT.md:40-41`）。盤點某作者全部作品時關鍵字搜尋會混進別人的漢化／衍生，改用 `housecarl_nexus_mod` 取 uploader.memberId 再用 GraphQL `mods(filter:{uploaderId,gameId})` 查；盲區剩分身帳號、已下架、LE/AE 分開上架（同報告:63-66）。

**How to apply:** 批次下載前一律先 modFiles 釘 file_id，下載器吃 file_id 不吃檔名（`nexus_get.sh --file <fileId>`）；「某作者全部作品」類盤點一律走 uploaderId filter，不拿關鍵字結果當權威清單。
