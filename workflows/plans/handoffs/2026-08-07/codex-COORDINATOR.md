# 指揮權交接 — codex 接手協調 deepseek 與 agy

**2026-08-07，Claude 交棒。** 從現在起你不只做自己的任務，還要**指揮另外兩個 agent**。

## 現況

| tmux session | agent | 目前狀態 |
|---|---|---|
| `skyrim-codex` | 你（gpt-5.5，在 `~/notes`） | A1 治具已寫完並過 SkyUI 驗收，還差一個下架/隱藏案例 |
| `skyrim-deepseek` | `pi --provider deepseek --model deepseek-v4-pro`，cwd `~/skyrim_agent_out/deepseek` | **A4a 已完成**，閒置中等你派工 |
| `skyrim-agy` | Antigravity CLI（Gemini 3.6 Flash），cwd `~/skyrim_mods/.candidates` | B2-recon 進行中，還沒產出檔案 |

另有一個 `pipeline` session 是上一輪的殘留（tmux-resurrect 還原的），只剩閒置 zsh，**不要管它、不要用它**。

環境事實：
- **mongod 已在跑**（pid 18477，port 27018，`--dbpath ~/data/mongodb`）。是 Claude 手動起的，不是 systemd。
- `NEXUS_API_KEY` 在使用者的 `~/.zshrc`（**互動式 zsh 才讀得到**——`zsh -lc` 讀不到，tmux 起的互動 shell 讀得到）。**絕不要把它的值印出來或寫進任何檔案。**
- Nexus rate limit 實測 2000/小時、20000/天。1,272 個 nexus_id 一小時內跑得完，控速不是瓶頸。
- `projects/agent-bridge` 的 main **已推上 origin**（`6106646`）——上一輪「沒推所以不釘 submodule」的理由已不成立，但那是母 repo 的事，不歸你管。

## 怎麼驅動另外兩個 agent

**不能用 stdin 注入**（互動 TUI 的 stdin 是 tty，`TIOCSTI` 被 `dev.tty.legacy_tiocsti=0` 關掉）。唯一可行的是 tmux：

```bash
tmux send-keys -t skyrim-deepseek -l '你的指令文字'   # -l 是 literal，避免特殊字元被解讀
sleep 1
tmux send-keys -t skyrim-deepseek Enter               # Enter 單獨送
tmux capture-pane -t skyrim-deepseek -p -S -30        # 讀畫面
```

**長交接寫成檔案、只送路徑**——不要把整份規格塞進 send-keys。

**兩個 agent 都會跳權限確認**，要你代按：
- deepseek（pi）：多數操作不問，偶爾問。
- agy：**幾乎每個 `python3 -c` 都問**。選項 1 是 Yes，送 `Enter` 即可（游標預設就在 1）。
- 你自己這邊沒有 `/approvals` 指令（這版不支援），網路與 Mongo 存取每次都要使用者按，這部分照舊。

**使用者會自己 attach 進去插手**（`tmux attach -t <session>`）。看到 pane 裡有他自己打的字，就別再代答那一題。

## 剩下的任務佇列

### 你自己
1. **收完 A1**：還差「抽一個已下架/隱藏的 mod 判成 `gone`/`hidden` 且 `never_delete=true`」這個驗收點。找不到現成案例就直接拿一個你確知已下架的 Nexus id 測，不必硬從庫裡挑。然後 `--limit 20` 實跑、驗冪等、commit。
2. **A4-review**：交接書在 `~/repo/moddings/skyrim/workflows/plans/handoffs/2026-08-07/codex-A4-review.md`。Claude 已逐筆看過 deepseek 那 38 筆低信心配對，**約一半是錯的且錯得有規律**，六條判準缺陷都寫在裡面。你要修的是判準不是逐筆手改。
3. **B1**：`candidates` schema + `ingest_candidates.py` / `check_links.py` / `build_gallery.py`。規格在上位計畫的線 B 那一節。

### 派給 deepseek
- **A2**：等你的 `fetch_nexus_status.py` 驗收過，叫它跑全量補值（1,272 個 nexus_id）。
- 護欄要重申：**不刪任何東西（尤其 `~/skyrim_mods/.quarantine/`）、不寫 git、不改 `tools/` 下的腳本、遇 bug 回報不自修**。
  > 背景：2026-08-06 有一次外包作業把檔案移進隔離區後又把整個隔離區刪掉，107 筆記錄永久消失。這條是硬規則。
- deepseek 這輪表現很好——它自己發現了「漢化包在 Nexus 上有自己的 mod id，導致 `mods` 裡有 255 個純漢化包 stub」這個資料模型陷阱。可以信任它的判斷力，但別放寬護欄。

### 派給 agy
- 等它的 `_recon.md` 出來，**你來驗**：它報的每個站、每個連結，都要能對上 `_recon_samples/` 下實際抓到的 `page.html`。**對不上就整批退回重做**——它是 Flash 模型，幻覺風險高，這是唯一的防線。
- 驗過之後根據偵查結果定死 `meta.json` 欄位，再派 B2 正式採集。
- 它的硬護欄：**只抓不載（絕不下載 mod 本體）、需登入/入會審核的站（Naver cafe 類）不做、不寫 git 不寫 Mongo**。

## 上位文件

- 計畫：`~/repo/moddings/skyrim/workflows/plans/round-2026-08-07-catalog-and-korean.md`
- 三份原始交接書：同目錄 `handoffs/2026-08-07/` 下的 `codex-A1.md`、`deepseek-A4a.md`、`agy-B2-recon.md`

**注意**：`~/repo/moddings/skyrim` 是使用者與 Claude 在管的母 repo，**你唯讀取用，不要在裡面 commit**。你的 commit 全部落在 `~/notes`。

## 兩件要回報給使用者的事

1. deepseek 掃出的 **38 種漢化衍生標記清單**（在它的 summary.md 裡）比原計畫列的多得多，值得收進計畫文件——但那份清單裡 `MCM` 與 `CLEAN` 是誤收的，不是翻譯標記。
2. Nexus API 的判定欄位已釘死：`status='published'` + `available=True` → `live`；版本要打 `files.json` 取 `category_name='MAIN'`+`is_primary=True`（mod header 的 `version` 會落後，SkyUI 是 6.9 vs 6.11）。這兩點 Claude 還沒補進計畫文件，你可以在 `~/notes` 側記，或等使用者回頭處理母 repo。
