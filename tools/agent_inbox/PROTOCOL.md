# Codex agent inbox 契約

這套 inbox 讓 Codex 工作線主動回報調度者。版控腳本位於
`/home/lorkhan/repo/moddings/skyrim/tools/agent_inbox/`，執行期資料固定放在
`/home/lorkhan/skyrim_agent_out/_inbox/`。工作線只用 `inbox_send.sh` 發訊息；不可自行搬動
`new/` 的訊息、修改 `watch.list`，或清理 `.state/`。

## 發送方式

```bash
/home/lorkhan/repo/moddings/skyrim/tools/agent_inbox/inbox_send.sh \
  <session> <STATUS> '<一句自足的結論>' [body_file]
```

省略 `body_file` 時，正文從 stdin 讀取。腳本先在 inbox 根目錄完成暫存檔，再以 `mv` 原子發布到
`new/`。成功時 stdout 會印出新訊息的絕對路徑；不合法的 STATUS 會失敗退出。

訊息檔名為 `<YYYYmmddTHHMM>-<session>-<STATUS>.md`，內容契約如下：

```markdown
---
from: codex-vok
status: DONE
at: 2026-08-22T13:40:12+08:00
---
# Vokrii 相容性驗證已全數通過，產物可交付

## 做了什麼
## 產出（檔案絕對路徑 / commit hash / 分支）
## 沒做到、或證據不足要 DEFER 的部分
## 需要調度者或使用者決定的事
```

frontmatter 後第一個非空的 `# ` 標題就是通知標題，必須是單獨看也能理解的一句結論；不可只寫
「完成」、「報告」或「有問題」。

## STATUS 語意

- `DONE`：任務與承諾的驗收都已完成；正文列出產物及證據。
- `BLOCKED`：任務仍未完成，因技術障礙、缺失依賴或外部狀態而無法繼續；寫明已嘗試的事、
  阻塞證據及解除條件。卡住超過 10 分鐘必須發送，不可無聲等待。
- `NEEDS-USER`：需要使用者的選擇、授權、憑證、人工／實機操作或其他只能由使用者決定的事；
  問題與可選方案要具體。它不同於可由 agent 自己排除的 `BLOCKED`。
- `FAILED`：這次執行已終止且沒有達成目標，短期內不會自行重試；正文交代失敗點、證據與可恢復方式。
- `PROGRESS`：任務尚在正常進行的非終局里程碑；只在長任務需要同步重要進度時使用。

每條工作線在任務結束時，必須發送 `DONE`、`FAILED`、`BLOCKED` 或 `NEEDS-USER` 之一。任務如果
卡住超過 10 分鐘，即使仍打算繼續，也必須先發 `BLOCKED`（需要使用者介入則發 `NEEDS-USER`）。

## 可貼入 HANDOFF.md 的區塊

```markdown
## 完成／阻塞回報（必做）
- 本線 session：`<SESSION_NAME>`。
- 任務結束時必須用 `/home/lorkhan/repo/moddings/skyrim/tools/agent_inbox/inbox_send.sh` 回報。
- 用法：`inbox_send.sh <SESSION_NAME> <STATUS> '<一句自足結論>' [body_file]`。
- STATUS 只可用 `DONE`、`BLOCKED`、`NEEDS-USER`、`FAILED`、`PROGRESS`。
- 卡住超過 10 分鐘也必須發；需使用者決定用 `NEEDS-USER`，其他阻塞用 `BLOCKED`。
- 標題不可只寫「完成」或「報告」；正文須列出產物路徑、commit、證據與待決事項。
- 完整契約：`/home/lorkhan/repo/moddings/skyrim/tools/agent_inbox/PROTOCOL.md`。
```

## 調度者讀取與 hook 選配

`inbox_read.sh` 無參數執行，只在 `new/` 有訊息時逐行輸出摘要，不會標記已讀或搬檔。
`notify_watch.sh` 是每 20 秒輪詢一次的長駐監看器；正常無事件時 stdout 完全靜默，診斷只寫 stderr。

[`hook-settings-snippet.json`](hook-settings-snippet.json) 是 Claude Code 的 `UserPromptSubmit` hook
片段。若使用者決定啟用，請把其中的 `hooks.UserPromptSubmit` 合併到使用者層級
`~/.claude/settings.json`（若已有 `hooks` 或同名事件，需合併陣列，不要覆蓋）。這個 repo 不會自動修改
任何 `settings.json`。
