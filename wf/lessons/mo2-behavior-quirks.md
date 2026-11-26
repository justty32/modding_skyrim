# MO2 本體行為坑（首次啟動、CC 落點、overlay、靜默失效）

[lessons 索引](README.md)｜mods/ 雜目錄與幽靈 profile 見 [mo2-auto-rewrites](mo2-auto-rewrites.md)

## cc-download-lands-in-cwd-data

> 1.6.1170 遊戲內 Creations 下載會成功，但檔案寫到「啟動時的工作目錄/Data」而不是遊戲目錄（2026-09-03）

遊戲的 CC 下載器用相對路徑 `Data\`，Proton 下 cwd 是 shell 的 cwd，不是 exe 所在目錄；`ae2/tools/launch-vanilla-skyrim.sh` 沒 `cd` 進遊戲目錄，檔案寫進跑腳本時 cwd 下的 `data/`，只看遊戲 `Data/` 會誤判成空跑。那批 CC 現存 `~/skyrim_mods/cc-ae-download-2026-09-03/`。

- `launch-vanilla-skyrim.sh` 要加 `cd "$G"`（或在 REPORT 註明先 cd）；找檔案時先 `find / -newermt` 全機掃，別只看預期目錄。
- CC 做成 MO2 mod（`Skyrim.ccc` 原廠 75 行從未被裁，一個位元組都別動）：**`.ccc` 列名且檔案在 VFS Data/ 的 plugin 一律當隱含 master 自動載入、不看 plugins.txt**，所以「啟用」＝勾 mod，「排除某幾件」＝把它們的 plugin＋bsa 搬到另一個停用的姊妹目錄（2026-09-04；USCCCP 才走 plugins.txt）。
- 官方簡中字串在每件 BSA 裡，抽成 `Strings/<原大小寫>_English.*` 層即可（mod-library `CC-Official-CHS-Strings-EnglishSlot-2026-09-04`）。
- 掃描「真正啟用的 plugin」不能只抓 plugins.txt 標 `*` 的行，要併入原版與 CC 等隱含載入的 masters（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-20/cell/REPORT.md:21`）。

相關：[[launch-skyrim-via-steam]]。

## mo2-first-launch-drops-new-plugin-star

> 新 plugin 第一次被 MO2 看到時，MO2 重排 plugins.txt 可能把它寫成未啟用（掉 *），第二次啟動才穩定；MO2 跑過之後 profile 三檔必須重驗，不能沿用啟動前的 houseCARL／鏡像結果（2026-09-09）

MO2 啟動時依自己的規則重寫 profile 三檔；鏡像快照是「跑之前」的狀態，「跑之前 PASS」不等於「跑之後 PASS」（例：`RSChildren-Forward…esp` 加 `*` 後跑煙霧被寫成未啟用，啟動前鏡像驗收全 PASS）。

- 加新 plugin 的窗：**MO2／遊戲關掉之後再實讀 plugins.txt 那一行有沒有 `*`**（`tr -d '\r'` 後 grep），再刷新鏡像重驗贏家；驗收證據標明時間在 MO2 關閉之後。掉了就補 `*`，第二次啟動穩定。
- MO2 正常結束會重寫 plugins.txt／loadorder.txt（CRLF 轉 LF、重排、拿掉已停用 mod 對應的已不存在 plugin 列）但不動 modlist.txt；驗「有沒有損失」時 modlist.txt 直接比 md5，plugins.txt／loadorder.txt 先正規化（排序、去 CRLF）再比集合，不能逐行 diff（2026-10-23，`agentctl/handoffs/done/2026-08-30/fix-2026-08-30/REPORT.md:107-125`）。

相關：[[profile-restore-order-and-flags]]（MO2 開著絕不改 profile、MO2 回寫另立 commit）、[[interactive-grep-is-ugrep]]（CRLF）、[[rs-children-missing-esp]]。

## eslify-overlay-snapshot-goes-stale

> 整包覆蓋 mod（如 ESLify-Overlay）凍結的是建立當下的贏家快照，更新同一支 plugin 的層只要排序在它之下，就會被靜默蓋掉，毫無錯誤訊息。

ESLify-Overlay 在 modlist 的位置不固定，要實讀行號；manifest 寫「要重查 sha256」但沒工具自動做。

- 更新被 overlay 收錄的 plugin：新層保留 ESL flag 並排在 overlay 之上，否則 FormID 槽位改變、存檔道具錯位。
- 往 overlay 加旗標複本前，逐支查來源 mod 的行號：**來源 mod 排在 overlay 上面（優先權更高）時複本會被來源蓋掉、旗標不生效**；不能為此把整個 overlay 往上搬（會蓋掉刻意排在它上面的中文層），要另開一層緊貼在來源 mod 上面（例 `ESLify-Overlay-NSV`，2026-10-26，`agentctl/handoffs/home-2026-10-26/eslapply/REPORT.md`）。
- 疑似誤停用先查 deploy-manifest，別看到停用就重啟。

來源：`agentctl/handoffs/done/2026-10/home-2026-10-09/vf-text3/DONE-eslify-shadow.md`。

## mo2-silent-collision-failure-modes

> MO2 有幾種常見靜默失效：同名 plugin 撞號、非 ASCII 資料夾名——全不報錯，只表現成「裝了沒用」或忽然 CTD。

都沒有錯誤訊息，容易誤判成「沒裝」而查錯方向。

- 同名 `.esp/.esm/.esl` 已知會 CTD，MO2 也拒絕還原該 load order；同名 plugin 的 VFS 只疊最高優先度一份，判定同角色要讀 EDID，不能只看檔名。啟用新 mod 前掃同名 provider／EDID（2026-08-30～09-01，`agentctl/handoffs/done/2026-08-31/grow-2026-08-31/dedup_fix.py:1-7`）。
- mod 資料夾中文命名會被剝高位元、整包靜默停用，新建資料夾一律純 ASCII（細節 `instance/docs/launch-and-safety.md`）。
- archive 內部路徑帶 `Data/` 前綴直接鋪成 `mods/<層>/Data/...` 會對應到遊戲 `Data/Data/...`，裝前先 `7z l` 看頂層再剝掉這層（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-01/hdmk-2026-09-01/HANDOFF-cx-hd1.md:19-35`）。
- 純覆蓋式更新層（跟既有 mod 同一個 esp 檔名、靠 VFS 排序蓋過去）絕不能在 plugins.txt／loadorder.txt 另加一行，它不是新增 plugin 槽（`agentctl/handoffs/done/2026-09/home-2026-09-08/face/REPORT.md:158`）。

同一 mod 裡大小寫不同的重複資料夾（`textures/` 與 `Textures/` 並存）：內容沒衝突時 VFS 合併看似正常，但 wine 下的 Windows 工具（ESLifier）開檔可能挑到沒有那個檔的一邊而崩潰；同路徑兩份內容不同的檔（例 `FOL-Recorder-Bugfix` 的 `000261ff.nif`／`000261FF.nif`）哪份生效不確定。跑 Windows 工具前先掃描並合併大小寫，內容不同的檔要人看過再決定留哪份（2026-10-26，`agentctl/handoffs/home-2026-10-26/eslifierpoc/REPORT.md` 步驟 3，清單 `eslifierpoc/data/case-duplicate-dirs.txt`）。

相關：[[profile-restore-order-and-flags]]。
