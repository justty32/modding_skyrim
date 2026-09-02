# tidy／gotchas（Windows 公司機）— 2026-08-31 實測

[tidy](README.md)｜[gotchas 本體](gotchas.md)。2026-09-02 自 `gotchas.md` 拆出（母檔 9781 B 超過 8 KB 上限）；
本檔只記公司 Windows 機專屬的坑，跨平台通則仍在 gotchas 本體。

<!-- wf-nav -->
- **codex sandbox 內整個 shell 是壞的，不只 `inbox_send.sh`**：`bash`／`sh`／`grep`／`find`／`wc` 全死在 `fatal error - CreateFileMapping <SID>.1, Win32 error 5`；PowerShell 可用但**指令一長就 `CreateProcessAsUserW failed: 5`**（實測 `env_u16_len=6454` 被拒），不能拿來當一行式替代。**唯一穩的是 `python`（`python3` 不存在）與原生 `git.exe`。** 處置：交接書裡所有 bash 管線的驗收命令（`bash wf/tools/wf-lint.sh`、`find … | wc -l`、`git status --short | grep -v …`）對 codex 工人**一律無效**，工人的自證命令全改寫成 `python`；bash 那面的驗收改由**管理線自己跑**——別拿自己測得通就推論工人也能用。驗收條數不必改，只換執行者。
- **codex 工人拿不到 `.git/modules/<sub>/index.lock` 的寫權限，做不了 `git mv`**，它們改用 `os.rename`／`shutil.move`：2026-08-31 四個 codex 搬完後，git 看到的是 **242 個未 stage 的刪除 ＋ 242 個未追蹤新檔**，`-M` 完全偵測不到 rename，交出去像刪了 242 個檔。處置：管理線收線時用**明確路徑**補 `git add -A <該線領地> <對應的 archive 路徑>`，**不可以 `git add -A .`**（會把別隊同時在動的檔一起 stage）；補完逐筆比對 `moves.tsv`——新路徑不存在 0 筆、舊路徑還在 0 筆，才算沒弄丟東西。
- **公司機的 `python3` 是 Microsoft Store 的假 shim，`wf-lint.sh --strict` 的綠燈會失真且不出警告。** `wf-lint.sh:22` 用 `command -v python3` 判有無——shim 在 PATH 上所以判「有」（`have_py=1`、不印 WARN），實際呼叫卻失敗（印「Python was not found…」，exit 49），而 88／104／124 行都是 `2>/dev/null`，空的 `out` 被當成「沒發現問題」。**後果：`biglist`／anchor／資料檔三項是「沒跑」不是「乾淨」，只有 `broken`／`residue`／`oversize` 三項是真的**（那三項是純 bash）。處置：公司端要驗這三項就用 `python wf/tools/find_big_lists.py`／`check_anchors.py`／`tabledb.py check` 手動跑，別拿公司端的 `--strict` 綠燈當回家後的保證。（`command -v` 只判存在、不判可執行，這是工具本身的缺陷，該改成實際執行一次再判；本輪只記坑、不改工具。）

## 檔案被 `MANIFEST.sha256` 釘住時，「整理」＝破壞驗證

`mod-library/l10n/mods/<成品>/` 底下的 `README.md`／`SOURCE.md`／`VERIFICATION.md`
**全部被同目錄的 `MANIFEST.sha256` 以 SHA-256 釘住**（2026-08-31 實測 21 個目錄無一例外）。
動任何一份——哪怕只是加一行 `<!-- wf-nav -->` 讓 lint 安靜——都會讓該成品自己文件裡
寫的 `sha256sum -c MANIFEST.sha256` 變紅。

**所以在這種目錄裡，BIGLIST 之類的整理指令要讓路。** 接受一個 warning，別為了消 warning
去改被釘住的檔。用包內 `update_manifest.py` 重算也不行，理由見下一條。

**通則：整理前先查目標檔有沒有被 hash／簽章／lock 檔釘住。** 有的話，「不改」才是對的。

## CRLF 讓 manifest 在 Windows 上結構性全紅，但內容零損壞

`core.autocrlf=true` 的 Windows checkout 上，逐項重算 21 個成品共 200 個 manifest 項目：
**`OK=62`／換成 LF 後相符 `138`／真正不符或缺檔 `0`**。相符的 62 個全是二進位檔（`.esp` 這類
不受換行轉換影響），文字檔則全部因為 CRLF 而 hash 不符。

**任何人在公司這台跑成品 README 寫的驗證指令，會看到整片 `FAILED` 而誤判成品損壞。**
實際上零損壞。**在 Windows 上不要重算 manifest**——重算會寫進 CRLF 版 hash，
反而讓家裡的 Linux 主力機校驗失敗，把假警報變成真故障。

## 「不得封存」的約束不要只寫在交接書裡

2026-08-31 實測：`agentctl/handoffs/done/2026-08-29/doc-refactor/cx-rl1-HANDOFF.md:56` 寫著
「`audits/l4-md5-resolution.md` 不得封存，且 heading 文字不得更動」（因為
`wait-user/later-decisions.md` 用 **GitHub anchor** 指進那個標題）。但 `audits/` 目錄本身
與該檔檔頭**都沒有任何標記**，整理線開工時讀不到，照樣封存了它。

**約束要寫在被約束的東西上。** 有跨 repo anchor 指進來、或有其他硬相依的檔，
在**檔頭**留一行說明；只寫在交接書裡等於沒寫——交接書進了 `done/` 之後就不再被讀。

同理，**anchor 連結是一種隱藏相依**。整理前除了掃 `](path)`，也要掃 `](path#anchor)`，
因為改標題不會讓任何連結檢查工具變紅，但會讓那條連結靜默失效。
